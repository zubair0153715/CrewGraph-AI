"""
CrewAI Node - Isolated multi-agent execution node for LangGraph
Integrates CrewAI agents as a single node in the LangGraph workflow
Includes: Parallel execution, Advanced agents, Document processing
"""
from typing import TypedDict, List, Dict, Any, Optional
from crewai import Agent, Task, Crew
from config import LLM_MODEL, OLLAMA_BASE_URL
import os
import uuid

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


class SubTask:
    """Represents a decomposed sub-task"""
    def __init__(self, id: str, description: str, assigned_agent: str, status: str = "pending", result: Optional[str] = None):
        self.id = id
        self.description = description
        self.assigned_agent = assigned_agent
        self.status = status
        self.result = result


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


def create_analyst_agent():
    """Create a data analysis specialist"""
    return Agent(
        role="Data Analysis Expert",
        goal="Analyze patterns, trends, and insights from data",
        backstory="""You are a data scientist with expertise in finding 
        meaningful patterns and providing actionable insights.""",
        verbose=True,
        allow_delegation=False,
        llm=f"ollama/{LLM_MODEL}"
    )


def create_coder_agent():
    """Create a coding specialist agent"""
    return Agent(
        role="Senior Software Engineer",
        goal="Write clean, efficient, and well-documented code",
        backstory="""You are an experienced developer who writes production-ready 
        code with proper error handling and best practices.""",
        verbose=True,
        allow_delegation=False,
        llm=f"ollama/{LLM_MODEL}"
    )


def create_reviewer_agent():
    """Create a quality review agent"""
    return Agent(
        role="Quality Assurance Specialist",
        goal="Review and improve content for accuracy and clarity",
        backstory="""You have a keen eye for detail and ensure all outputs 
        meet high quality standards.""",
        verbose=True,
        allow_delegation=False,
        llm=f"ollama/{LLM_MODEL}"
    )


def execute_crewai_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute CrewAI multi-agent workflow as a LangGraph node
    
    Args:
        state: LangGraph state dictionary
        
    Returns:
        Dictionary with result, agents_used, and tasks_completed
    """
    query = state.get("query", "")
    context = state.get("context", "")
    task_type = state.get("task_type", "general")
    
    # Select agents based on task type
    if task_type == "code":
        agents = [create_coder_agent(), create_reviewer_agent()]
    elif task_type == "analysis":
        agents = [create_analyst_agent(), create_writer_agent()]
    else:
        agents = [create_researcher_agent(), create_writer_agent()]
    
    # Create tasks based on task type
    if task_type == "research":
        research_task = Task(
            description=f"""Research and analyze: {query}
            
            Context: {context}
            
            Provide comprehensive findings with key points and insights.""",
            expected_output="Detailed research findings with bullet points",
            agent=agents[0]
        )
        
        synthesis_task = Task(
            description=f"""Synthesize the research findings into a clear response.
            
            Original query: {query}
            
            Create a well-structured answer that's easy to understand.""",
            expected_output="Clear, structured final response",
            agent=agents[1]
        )
        tasks = [research_task, synthesis_task]
    elif task_type == "code":
        coding_task = Task(
            description=f"""Write code for: {query}
            
            Requirements:
            - Clean, readable code
            - Proper error handling
            - Comments where needed
            - Best practices""",
            expected_output="Complete, working code solution",
            agent=agents[0]
        )
        
        review_task = Task(
            description="Review the code for quality, efficiency, and correctness",
            expected_output="Reviewed and improved code",
            agent=agents[1]
        )
        tasks = [coding_task, review_task]
    else:
        # General task
        general_task = Task(
            description=f"""Address this query comprehensively: {query}
            
            Context: {context}
            
            Provide a helpful, accurate, and well-organized response.""",
            expected_output="Complete and helpful answer",
            agent=agents[0]
        )
        
        review_task = Task(
            description="Review and refine the response for clarity and accuracy",
            expected_output="Polished final response",
            agent=agents[1]
        )
        tasks = [general_task, review_task]
    
    # Create and run crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2
    )
    
    try:
        result = crew.kickoff()
        return {
            "result": str(result),
            "agents_used": [agent.role.split()[0] for agent in agents],
            "tasks_completed": len(tasks)
        }
    except Exception as e:
        error_msg = f"CrewAI execution failed: {str(e)}"
        print(f"⚠️  {error_msg}")
        return {
            "result": error_msg,
            "agents_used": [],
            "tasks_completed": 0
        }


def execute_parallel_crew(sub_tasks: List, query: str) -> List[Dict]:
    """
    Execute multiple crews in parallel for sub-tasks
    
    Args:
        sub_tasks: List of SubTask objects
        query: Original query for context
        
    Returns:
        List of results from each sub-task execution
    """
    results = []
    
    for sub_task in sub_tasks:
        try:
            # Create appropriate agent for sub-task
            if "research" in sub_task.description.lower():
                agent = create_researcher_agent()
            elif "analyze" in sub_task.description.lower():
                agent = create_analyst_agent()
            elif "code" in sub_task.description.lower():
                agent = create_coder_agent()
            else:
                agent = create_writer_agent()
            
            task = Task(
                description=f"{sub_task.description}\n\nContext: {query}",
                expected_output="Clear, focused result",
                agent=agent
            )
            
            crew = Crew(agents=[agent], tasks=[task], verbose=1)
            result = crew.kickoff()
            
            results.append({
                "success": True,
                "result": str(result),
                "sub_task_id": sub_task.id
            })
        except Exception as e:
            results.append({
                "success": False,
                "result": f"Error: {str(e)}",
                "sub_task_id": sub_task.id
            })
    
    return results


def process_document(file_path: str, query: str) -> Dict[str, Any]:
    """
    Process a document (PDF, TXT, MD) with CrewAI agents
    
    Args:
        file_path: Path to the document
        query: Query about the document
        
    Returns:
        Analysis result
    """
    try:
        # Read document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        researcher = create_researcher_agent()
        analyst = create_analyst_agent()
        
        # Task 1: Extract relevant information
        extraction_task = Task(
            description=f"""From this document, extract information relevant to: {query}
            
            Document Content:
            {content[:5000]}  # Limit content length
            
            Provide key excerpts and relevant sections.""",
            expected_output="Extracted relevant information",
            agent=researcher
        )
        
        # Task 2: Analyze and answer query
        analysis_task = Task(
            description=f"""Based on the extracted information, answer: {query}
            
            Provide a comprehensive answer with references to the document.""",
            expected_output="Detailed answer based on document",
            agent=analyst
        )
        
        crew = Crew(agents=[researcher, analyst], tasks=[extraction_task, analysis_task], verbose=2)
        result = crew.kickoff()
        
        return {
            "success": True,
            "result": str(result),
            "document_processed": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "result": f"Document processing failed: {str(e)}",
            "document_processed": file_path
        }
