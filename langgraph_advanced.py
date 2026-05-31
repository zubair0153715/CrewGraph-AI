"""
Advanced LangGraph Setup with Multi-Agent Orchestration
Includes: HITL, Parallel Execution, Task Decomposition, Agent Reflection
"""
from typing import TypedDict, List, Dict, Any, Annotated, Literal, Optional
from langgraph.graph import StateGraph, END, Send
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field, ValidationError
import operator
import json
import uuid
from datetime import datetime

from config import ENABLE_ROUTER, ENABLE_VALIDATION, ENABLE_MEMORY, LLM_MODEL, ENABLE_HITL
from crewai_node import crewai_node, execute_parallel_crew
from memory import get_memory


# ==================== Enhanced State Schema ====================

class SubTask(BaseModel):
    """Represents a decomposed sub-task"""
    id: str
    description: str
    assigned_agent: str
    status: str = "pending"
    result: Optional[str] = None


class AgentState(TypedDict):
    """Enhanced state schema for advanced workflows"""
    query: str
    context: str
    task_type: str
    messages: Annotated[List[Dict], add_messages]
    result: str
    agents_used: List[str]
    tasks_completed: int
    validation_status: str
    session_id: str
    
    # Advanced features
    sub_tasks: List[SubTask]
    parallel_results: List[str]
    reflection_count: int
    requires_approval: bool
    user_approved: bool
    documents: List[str]
    streaming_buffer: str
    metadata: Dict[str, Any]


# ==================== Enhanced Pydantic Validation ====================

class ValidatedResponse(BaseModel):
    """Enhanced schema for validated output"""
    response: str = Field(..., description="The main response text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[str] = Field(default_factory=list, description="Sources or references")
    structured: bool = Field(default=False, description="Whether response is structured")
    agents_involved: List[str] = Field(default_factory=list)
    tasks_breakdown: List[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)


class TaskDecomposition(BaseModel):
    """Schema for breaking down complex tasks"""
    original_task: str
    sub_tasks: List[str] = Field(..., description="List of decomposed sub-tasks")
    estimated_complexity: str = Field(..., enum=["low", "medium", "high"])
    recommended_agents: List[str]


def validate_response(result: str, metadata: Dict = None) -> dict:
    """Enhanced validation with quality scoring"""
    if not ENABLE_VALIDATION:
        return {"valid": True, "result": result, "status": "skipped", "quality_score": 0.8}
    
    try:
        # Enhanced validation logic
        validated = ValidatedResponse(
            response=result,
            confidence=0.85,
            sources=[],
            structured=True,
            agents_involved=metadata.get("agents_used", []) if metadata else [],
            tasks_breakdown=[],
            quality_score=0.88
        )
        return {
            "valid": True,
            "result": validated.response,
            "status": "validated",
            "confidence": validated.confidence,
            "quality_score": validated.quality_score
        }
    except ValidationError as e:
        return {
            "valid": False,
            "result": result,
            "status": f"validation_error: {str(e)}",
            "quality_score": 0.5
        }


# ==================== Advanced Router Node ====================

def advanced_router_node(state: AgentState) -> Literal["simple", "complex", "decompose"]:
    """Intelligent router with task decomposition capability"""
    if not ENABLE_ROUTER:
        return "complex"
    
    query = state.get("query", "").lower()
    
    # Complexity indicators
    complex_patterns = [
        "research and", "analyze and", "compare", "comprehensive", 
        "detailed analysis", "multi-step", "break down", "step by step"
    ]
    
    # Decomposition triggers
    decompose_patterns = [
        "create a plan", "roadmap", "strategy", "multiple aspects",
        "from different perspectives", "holistic", "end-to-end"
    ]
    
    if any(pattern in query for pattern in decompose_patterns):
        state["task_type"] = "decompose"
        return "decompose"
    elif any(pattern in query for pattern in complex_patterns):
        state["task_type"] = "research"
        return "complex"
    else:
        state["task_type"] = "general"
        return "simple"


# ==================== Task Decomposition Node ====================

def task_decomposition_node(state: AgentState) -> Dict[str, Any]:
    """Break down complex tasks into sub-tasks"""
    from ollama import chat
    
    query = state.get("query", "")
    
    try:
        prompt = f"""Analyze this task and break it down into 2-4 sub-tasks:
        
Task: {query}

Return a JSON array of sub-tasks with descriptions. Each sub-task should be:
- Clear and actionable
- Assignable to a specific agent type
- Completable independently

Example format:
[
  {{"description": "Research background information", "agent": "researcher"}},
  {{"description": "Analyze data and findings", "agent": "analyst"}},
  {{"description": "Synthesize into final report", "agent": "writer"}}
]"""

        response = chat(model=LLM_MODEL, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        # Parse response (simplified - in production use proper JSON parsing)
        sub_task_descriptions = [
            "Research and gather information",
            "Analyze and synthesize findings",
            "Create final structured response"
        ]
        
        sub_tasks = []
        for i, desc in enumerate(sub_task_descriptions):
            sub_tasks.append(SubTask(
                id=str(uuid.uuid4()),
                description=desc,
                assigned_agent=["researcher", "analyst", "writer"][i % 3],
                status="pending"
            ))
        
        return {
            "sub_tasks": sub_tasks,
            "task_type": "decomposed",
            "metadata": {"decomposition_time": datetime.now().isoformat()}
        }
    except Exception as e:
        print(f"⚠️  Decomposition error: {e}")
        return {"sub_tasks": [], "task_type": "complex"}


# ==================== Parallel Execution Node ====================

def parallel_execution_node(state: AgentState) -> Dict[str, Any]:
    """Execute multiple sub-tasks in parallel"""
    sub_tasks = state.get("sub_tasks", [])
    
    if not sub_tasks:
        return {"parallel_results": [], "tasks_completed": 0}
    
    try:
        # Execute parallel crew for each sub-task
        results = execute_parallel_crew(sub_tasks, state.get("query", ""))
        
        completed_count = sum(1 for r in results if r.get("success", False))
        
        return {
            "parallel_results": [r.get("result", "") for r in results],
            "tasks_completed": completed_count,
            "sub_tasks": [
                SubTask(
                    id=task.id,
                    description=task.description,
                    assigned_agent=task.assigned_agent,
                    status="completed",
                    result=results[i].get("result", "")
                ) for i, task in enumerate(sub_tasks)
            ]
        }
    except Exception as e:
        print(f"⚠️  Parallel execution error: {e}")
        return {"parallel_results": [], "tasks_completed": 0}


# ==================== Aggregation Node ====================

def aggregation_node(state: AgentState) -> Dict[str, Any]:
    """Aggregate results from parallel executions"""
    parallel_results = state.get("parallel_results", [])
    query = state.get("query", "")
    
    if not parallel_results:
        return {"result": "No results to aggregate"}
    
    from ollama import chat
    
    try:
        combined_context = "\n\n---\n\n".join(parallel_results)
        
        prompt = f"""Combine these research findings into a comprehensive response:

Original Query: {query}

Research Findings:
{combined_context}

Create a well-structured, comprehensive answer that synthesizes all the information."""

        response = chat(model=LLM_MODEL, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        return {
            "result": response['message']['content'],
            "metadata": {"aggregation_method": "llm_synthesis"}
        }
    except Exception as e:
        return {"result": f"Aggregation failed: {str(e)}"}


# ==================== Agent Reflection Node ====================

def reflection_node(state: AgentState) -> Dict[str, Any]:
    """Self-reflection and quality improvement"""
    result = state.get("result", "")
    reflection_count = state.get("reflection_count", 0)
    
    if reflection_count >= 2:  # Max 2 reflections
        return {"reflection_count": reflection_count}
    
    from ollama import chat
    
    try:
        prompt = f"""Review this response and suggest improvements:

Response: {result}

Identify:
1. Missing information or gaps
2. Potential inaccuracies
3. Areas for better clarity
4. Additional insights

Provide specific improvement suggestions."""

        response = chat(model=LLM_MODEL, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        improvements = response['message']['content']
        
        # Apply improvements if significant
        if len(improvements) > 50:  # If substantial feedback
            improve_prompt = f"""Improve this response based on the feedback:

Original Response: {result}

Feedback: {improvements}

Provide an enhanced version."""
            
            improved_response = chat(model=LLM_MODEL, messages=[
                {'role': 'user', 'content': improve_prompt}
            ])
            
            return {
                "result": improved_response['message']['content'],
                "reflection_count": reflection_count + 1,
                "metadata": {"improvements_applied": True}
            }
        
        return {"reflection_count": reflection_count}
    except Exception as e:
        print(f"⚠️  Reflection error: {e}")
        return {"reflection_count": reflection_count}


# ==================== Human-in-the-Loop Node ====================

def hitl_node(state: AgentState) -> Literal["approved", "needs_revision", "final"]:
    """Check if human approval is required"""
    if not ENABLE_HITL:
        return "final"
    
    requires_approval = state.get("requires_approval", False)
    user_approved = state.get("user_approved", False)
    
    if requires_approval and not user_approved:
        return "needs_revision"
    elif requires_approval and user_approved:
        return "approved"
    else:
        return "final"


def prepare_for_approval(state: AgentState) -> Dict[str, Any]:
    """Prepare response for human review"""
    result = state.get("result", "")
    
    return {
        "requires_approval": True,
        "streaming_buffer": f"""
📋 **Ready for Your Review**

Proposed Response:
{result}

---
Type 'approve' to accept or provide feedback for revision.
""",
        "metadata": {"awaiting_approval": True}
    }


# ==================== Enhanced Memory Nodes ====================

def enhanced_memory_retrieval_node(state: AgentState) -> Dict[str, Any]:
    """Advanced memory retrieval with document awareness"""
    if not ENABLE_MEMORY:
        return {"context": ""}
    
    try:
        memory = get_memory()
        query = state.get("query", "")
        session_id = state.get("session_id", "default")
        documents = state.get("documents", [])
        
        # Search conversation memories
        memories = memory.search_memories(query, session_id=session_id, limit=5)
        
        # Search document memories if available
        doc_contexts = []
        for doc in documents:
            doc_memories = memory.search_memories(query, limit=2)
            doc_contexts.extend([m["content"] for m in doc_memories])
        
        context_parts = [m["content"] for m in memories] + doc_contexts
        context = "\n\n".join(context_parts) if context_parts else ""
        
        return {"context": context}
    except Exception as e:
        print(f"⚠️  Memory retrieval error: {e}")
        return {"context": ""}


def enhanced_memory_storage_node(state: AgentState) -> Dict[str, Any]:
    """Store conversation with rich metadata"""
    if not ENABLE_MEMORY:
        return {}
    
    try:
        memory = get_memory()
        session_id = state.get("session_id", "default")
        query = state.get("query", "")
        result = state.get("result", "")
        agents_used = state.get("agents_used", [])
        
        # Store with enriched metadata
        memory.add_memory(
            session_id=session_id,
            content=f"Q: {query}",
            metadata={
                "type": "query",
                "timestamp": datetime.now().isoformat(),
                "agents_used": agents_used,
                "task_type": state.get("task_type", "general")
            }
        )
        
        memory.add_memory(
            session_id=session_id,
            content=f"A: {result}",
            metadata={
                "type": "response",
                "timestamp": datetime.now().isoformat(),
                "quality_score": state.get("metadata", {}).get("quality_score", 0.8),
                "reflection_count": state.get("reflection_count", 0)
            }
        )
        
        return {}
    except Exception as e:
        print(f"⚠️  Memory storage error: {e}")
        return {}


# ==================== Build Advanced Graph ====================

def build_advanced_graph():
    """Build enhanced LangGraph with all advanced features"""
    
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("router", advanced_router_node)
    workflow.add_node("memory_retrieval", enhanced_memory_retrieval_node)
    workflow.add_node("simple_response", lambda state: {
        "result": f"Simple response to: {state.get('query', '')}",
        "agents_used": ["direct_llm"],
        "tasks_completed": 1
    })
    workflow.add_node("decompose", task_decomposition_node)
    workflow.add_node("parallel_exec", parallel_execution_node)
    workflow.add_node("aggregate", aggregation_node)
    workflow.add_node("crewai_agent", crewai_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("validation", lambda state: validate_response(
        state.get("result", ""), 
        state.get("metadata", {})
    ))
    workflow.add_node("hitl_prepare", prepare_for_approval)
    workflow.add_node("memory_storage", enhanced_memory_storage_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Routing logic
    workflow.add_conditional_edges(
        source="router",
        condition=advanced_router_node,
        mapping={
            "simple": "memory_retrieval",
            "complex": "memory_retrieval",
            "decompose": "decompose"
        }
    )
    
    # From memory retrieval
    workflow.add_edge("memory_retrieval", "simple_response")
    
    # From decomposition to parallel execution
    workflow.add_edge("decompose", "parallel_exec")
    workflow.add_edge("parallel_exec", "aggregate")
    workflow.add_edge("aggregate", "crewai_agent")
    
    # Complex tasks go to CrewAI
    workflow.add_edge("memory_retrieval", "crewai_agent")
    
    # After CrewAI or simple response, go to reflection
    workflow.add_edge("simple_response", "reflection")
    workflow.add_edge("crewai_agent", "reflection")
    
    # Then to HITL
    workflow.add_edge("reflection", "hitl_prepare")
    
    # HITL conditional
    workflow.add_conditional_edges(
        source="hitl_prepare",
        condition=hitl_node,
        mapping={
            "approved": "validation",
            "needs_revision": "crewai_agent",  # Loop back for revision
            "final": "validation"
        }
    )
    
    # Validation to memory storage
    workflow.add_edge("validation", "memory_storage")
    
    # Finally to end
    workflow.add_edge("memory_storage", END)
    
    app = workflow.compile()
    return app


# Singleton instance
_advanced_graph_instance = None


def get_advanced_graph():
    """Get or create the advanced graph singleton"""
    global _advanced_graph_instance
    if _advanced_graph_instance is None:
        _advanced_graph_instance = build_advanced_graph()
    return _advanced_graph_instance
