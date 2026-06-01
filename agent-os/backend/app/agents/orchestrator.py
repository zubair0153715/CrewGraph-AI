from crewai import Agent, Task, Crew
from typing import List, Dict, Any, Optional
from langchain_core.tools import Tool
from app.models import Agent as AgentModel, Task as TaskModel
from app.services.llm import get_llm
from app.services.memory import memory_service
from app.utils.tools import (
    get_browser_search_tool,
    get_web_scraping_tool,
)


class AgentOrchestrator:
    """Orchestrates CrewAI agents based on user-defined agent configurations"""
    
    def __init__(self, db_agent: AgentModel):
        self.db_agent = db_agent
        self.llm = get_llm()
        self.tools = self._load_tools()
    
    def _load_tools(self) -> List[Tool]:
        """Load tools based on agent configuration"""
        tools = []
        agent_tools = self.db_agent.tools or []
        
        if "browser_search" in agent_tools or settings.ENABLE_BROWSER_AUTOMATION:
            tools.append(get_browser_search_tool())
        
        if "web_scraping" in agent_tools:
            tools.append(get_web_scraping_tool())
        
        # Add more tools as needed
        return tools
    
    def create_agent(self) -> Agent:
        """Create a CrewAI agent from database configuration"""
        
        # Build system prompt
        system_prompt = self.db_agent.system_prompt or f"""
        You are a {self.db_agent.name} with the role of {self.db_agent.role}.
        {self.db_agent.description or ''}
        
        Your autonomy level is {self.db_agent.autonomy_level}.
        - Low: Ask for confirmation before major decisions
        - Medium: Make routine decisions independently
        - High: Full autonomy to complete tasks
        
        Always be helpful, accurate, and efficient.
        """
        
        # Load relevant memories if enabled
        context = ""
        if self.db_agent.memory_enabled:
            recent_memories = memory_service.search_memories(
                self.db_agent.id,
                query=self.db_agent.role,
                limit=3
            )
            if recent_memories:
                context = "\n\nRelevant memories from past experiences:\n"
                for mem in recent_memories:
                    context += f"- {mem['content']}\n"
        
        return Agent(
            role=self.db_agent.role,
            goal=f"Excel at {self.db_agent.role.lower()} tasks",
            backstory=system_prompt + context,
            verbose=True,
            tools=self.tools,
            llm=self.llm,
            allow_delegation=self.db_agent.autonomy_level == "high",
        )
    
    def execute_task(self, task_description: str, expected_output: str = "") -> str:
        """Execute a task with the configured agent"""
        
        agent = self.create_agent()
        
        task = Task(
            description=task_description,
            expected_output=expected_output or "Complete and well-formatted result",
            agent=agent,
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=2,
        )
        
        result = crew.kickoff()
        
        # Save to memory if enabled
        if self.db_agent.memory_enabled:
            memory_service.add_memory(
                agent_id=self.db_agent.id,
                content=f"Task: {task_description}\nResult: {str(result)}",
                metadata={"task_type": "execution"}
            )
        
        return str(result)
    
    def execute_multi_agent_workflow(
        self,
        tasks: List[Dict[str, Any]],
        sequential: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a multi-agent workflow
        
        Args:
            tasks: List of task definitions with agent_id, description, expected_output
            sequential: If True, tasks run sequentially; if False, parallel (future)
        
        Returns:
            Dictionary with task results
        """
        results = {}
        
        if sequential:
            for i, task_def in enumerate(tasks):
                # Get or create agent for this task
                if "agent_id" in task_def:
                    # Load different agent from DB
                    from app.models import SessionLocal, Agent as AgentModel
                    db = SessionLocal()
                    task_agent = db.query(AgentModel).filter(
                        AgentModel.id == task_def["agent_id"]
                    ).first()
                    db.close()
                    
                    if task_agent:
                        orchestrator = AgentOrchestrator(task_agent)
                        result = orchestrator.execute_task(
                            task_def["description"],
                            task_def.get("expected_output")
                        )
                        results[f"task_{i}"] = result
                else:
                    # Use current agent
                    result = self.execute_task(
                        task_def["description"],
                        task_def.get("expected_output")
                    )
                    results[f"task_{i}"] = result
        
        return results


# For MVP - Predefined agent templates
DEFAULT_AGENT_TEMPLATES = {
    "research_agent": {
        "name": "Research Agent",
        "role": "Senior Research Analyst",
        "description": "Expert at finding, analyzing, and synthesizing information from the web",
        "tools": ["browser_search", "web_scraping"],
        "autonomy_level": "medium",
        "system_prompt": """
        You are a Senior Research Analyst with expertise in:
        - Finding accurate information online
        - Analyzing trends and patterns
        - Synthesizing complex information into clear insights
        - Fact-checking and verifying sources
        
        Always provide sources when possible and note confidence levels.
        """
    },
    "content_agent": {
        "name": "Content Agent",
        "role": "Senior Content Creator",
        "description": "Expert at creating engaging content for blogs, scripts, and social media",
        "tools": ["browser_search"],
        "autonomy_level": "medium",
        "system_prompt": """
        You are a Senior Content Creator with expertise in:
        - Writing engaging blog posts and articles
        - Creating video scripts
        - SEO optimization
        - Adapting tone and style for different audiences
        
        Always create original, valuable content that engages readers.
        """
    },
    "task_runner_agent": {
        "name": "Task Runner Agent",
        "role": "Executive Assistant",
        "description": "General-purpose agent for executing various tasks",
        "tools": ["browser_search"],
        "autonomy_level": "low",
        "system_prompt": """
        You are an Executive Assistant who helps with various tasks:
        - Following instructions precisely
        - Organizing information clearly
        - Asking clarifying questions when needed
        - Providing structured outputs
        
        Always confirm understanding before proceeding with complex tasks.
        """
    }
}

from app.core.config import settings
