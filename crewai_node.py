"""
CrewAI Node - Isolated multi-agent execution node for LangGraph
Integrates CrewAI agents as a single node in the LangGraph workflow
"""
from typing import TypedDict, List, Dict, Any
from crewai import Agent, Task, Crew
from config import LLM_MODEL, OLLAMA_BASE_URL
import os

# Set Ollama base URL for CrewAI
os.environ["OPENAI_API_BASE"] = OLLAMA_BASE_URL
os.environ["OPENAI_MODEL_NAME"] = LLM_MODEL
os.environ["OPENAI_API_KEY"] = "ollama"  # Required but not used


class CrewAINodeInput(TypedDict):
    """Input schema for CrewAI node"""
    query: str
    context: str
    task_type: str


class CrewAINodeOutput(TypedDict):
    """Output schema for CrewAI node"""
    result: str
    agents_used: List[str]
    tasks_completed: int


def create_researcher_agent():
    """Create a research specialist agent"""
    return Agent(
        role="Senior Research Analyst",
        goal="Find accurate and relevant information for any query",
        backstory="""You are an expert researcher with years of experience 
        analyzing complex topics. You break down questions systematically 
        and provide well-researched, factual answers.""",
        verbose=True,
        allow_delegation=False,
        llm=f"ollama/{LLM_MODEL}"
    )


def create_writer_agent():
    """Create a content synthesis agent"""
    return Agent(
        role="Content Synthesizer",
        goal="Transform research findings into clear, structured responses",
        backstory="""You are a skilled writer who excels at organizing 
        information logically. You create well-structured, easy-to-understand 
        responses from complex data.""",
        verbose=True,
        allow_delegation=False,
        llm=f"ollama/{LLM_MODEL}"
    )


def execute_crewai_node(input_data: CrewAINodeInput) -> CrewAINodeOutput:
    """
    Execute CrewAI multi-agent workflow as a LangGraph node
    
    Args:
        input_data: Dictionary with query, context, and task_type
        
    Returns:
        Dictionary with result, agents_used, and tasks_completed
    """
    query = input_data.get("query", "")
    context = input_data.get("context", "")
    task_type = input_data.get("task_type", "general")
    
    # Create agents
    researcher = create_researcher_agent()
    writer = create_writer_agent()
    
    # Create tasks based on task type
    if task_type == "research":
        research_task = Task(
            description=f"""Research and analyze: {query}
            
            Context: {context}
            
            Provide comprehensive findings with key points and insights.""",
            expected_output="Detailed research findings with bullet points",
            agent=researcher
        )
        
        synthesis_task = Task(
            description=f"""Synthesize the research findings into a clear response.
            
            Original query: {query}
            
            Create a well-structured answer that's easy to understand.""",
            expected_output="Clear, structured final response",
            agent=writer
        )
    else:
        # General task
        general_task = Task(
            description=f"""Address this query comprehensively: {query}
            
            Context: {context}
            
            Provide a helpful, accurate, and well-organized response.""",
            expected_output="Complete and helpful answer",
            agent=researcher
        )
        
        review_task = Task(
            description="Review and refine the response for clarity and accuracy",
            expected_output="Polished final response",
            agent=writer
        )
    
    # Create and run crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, synthesis_task] if task_type == "research" else [general_task, review_task],
        verbose=2
    )
    
    try:
        result = crew.kickoff()
        return CrewAINodeOutput(
            result=str(result),
            agents_used=["researcher", "writer"],
            tasks_completed=2
        )
    except Exception as e:
        error_msg = f"CrewAI execution failed: {str(e)}"
        print(f"⚠️  {error_msg}")
        return CrewAINodeOutput(
            result=error_msg,
            agents_used=[],
            tasks_completed=0
        )


# Simple function wrapper for LangGraph compatibility
def crewai_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph-compatible node function"""
    input_data = {
        "query": state.get("query", ""),
        "context": state.get("context", ""),
        "task_type": state.get("task_type", "general")
    }
    
    output = execute_crewai_node(input_data)
    
    return {
        "result": output["result"],
        "agents_used": output["agents_used"],
        "tasks_completed": output["tasks_completed"]
    }
