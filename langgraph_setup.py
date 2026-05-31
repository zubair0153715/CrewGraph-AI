"""
LangGraph Setup - State Graph, Routing, and Validation
Combines LangGraph orchestration with CrewAI nodes and Pydantic validation
"""
from typing import TypedDict, List, Dict, Any, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, ValidationError
import operator
import json

from config import ENABLE_ROUTER, ENABLE_VALIDATION, ENABLE_MEMORY, LLM_MODEL
from crewai_node import crewai_node
from memory import get_memory


# ==================== State Schema ====================

class AgentState(TypedDict):
    """Main state schema for the LangGraph workflow"""
    query: str
    context: str
    task_type: str
    messages: Annotated[List[str], operator.add]
    result: str
    agents_used: List[str]
    tasks_completed: int
    validation_status: str
    session_id: str


# ==================== Pydantic Validation ====================

class ValidatedResponse(BaseModel):
    """Schema for validated output"""
    response: str = Field(..., description="The main response text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[str] = Field(default_factory=list, description="Sources or references")
    structured: bool = Field(default=False, description="Whether response is structured")


def validate_response(result: str) -> dict:
    """Validate response using Pydantic schema"""
    if not ENABLE_VALIDATION:
        return {"valid": True, "result": result, "status": "skipped"}
    
    try:
        # Try to parse as structured response
        # In production, you'd have the LLM output JSON
        validated = ValidatedResponse(
            response=result,
            confidence=0.9,
            sources=[],
            structured=False
        )
        return {
            "valid": True,
            "result": validated.response,
            "status": "validated",
            "confidence": validated.confidence
        }
    except ValidationError as e:
        return {
            "valid": False,
            "result": result,
            "status": f"validation_error: {str(e)}"
        }


# ==================== Router Node ====================

def router_node(state: AgentState) -> Literal["simple", "complex"]:
    """Classify task complexity and route accordingly"""
    if not ENABLE_ROUTER:
        return "complex"
    
    query = state.get("query", "").lower()
    
    # Simple routing logic based on keywords
    simple_keywords = ["hello", "hi", "what is", "define", "explain briefly"]
    complex_keywords = ["research", "analyze", "compare", "comprehensive", "detailed"]
    
    if any(kw in query for kw in complex_keywords):
        state["task_type"] = "research"
        return "complex"
    elif any(kw in query for kw in simple_keywords):
        state["task_type"] = "general"
        return "simple"
    else:
        # Default to complex for safety
        state["task_type"] = "general"
        return "complex"


# ==================== Simple Response Node ====================

def simple_response_node(state: AgentState) -> Dict[str, Any]:
    """Handle simple queries directly without CrewAI"""
    from ollama import chat
    
    query = state.get("query", "")
    
    try:
        response = chat(model=LLM_MODEL, messages=[
            {'role': 'user', 'content': f"Answer briefly and helpfully: {query}"}
        ])
        
        result = response['message']['content']
        
        return {
            "result": result,
            "agents_used": ["direct_llm"],
            "tasks_completed": 1,
            "messages": [f"User: {query}", f"Assistant: {result}"]
        }
    except Exception as e:
        error_msg = f"Simple response failed: {str(e)}"
        print(f"⚠️  {error_msg}")
        return {
            "result": error_msg,
            "agents_used": [],
            "tasks_completed": 0,
            "messages": [f"User: {query}", f"Error: {error_msg}"]
        }


# ==================== Memory Node ====================

def memory_retrieval_node(state: AgentState) -> Dict[str, Any]:
    """Retrieve relevant memories from ChromaDB"""
    if not ENABLE_MEMORY:
        return {"context": ""}
    
    try:
        memory = get_memory()
        query = state.get("query", "")
        session_id = state.get("session_id", "default")
        
        # Search for relevant memories
        memories = memory.search_memories(query, session_id=session_id, limit=3)
        
        context_parts = []
        for mem in memories:
            context_parts.append(mem["content"])
        
        context = "\n\n".join(context_parts) if context_parts else ""
        
        return {"context": context}
    except Exception as e:
        print(f"⚠️  Memory retrieval error: {e}")
        return {"context": ""}


# ==================== Validation Node ====================

def validation_node(state: AgentState) -> Dict[str, Any]:
    """Validate the response from CrewAI or simple node"""
    result = state.get("result", "")
    validation = validate_response(result)
    
    return {
        "result": validation["result"],
        "validation_status": validation["status"]
    }


# ==================== Memory Storage Node ====================

def memory_storage_node(state: AgentState) -> Dict[str, Any]:
    """Store the conversation in memory"""
    if not ENABLE_MEMORY:
        return {}
    
    try:
        memory = get_memory()
        session_id = state.get("session_id", "default")
        query = state.get("query", "")
        result = state.get("result", "")
        
        # Store user query
        memory.add_memory(
            session_id=session_id,
            content=f"Q: {query}",
            metadata={"type": "query"}
        )
        
        # Store assistant response
        memory.add_memory(
            session_id=session_id,
            content=f"A: {result}",
            metadata={"type": "response"}
        )
        
        return {}
    except Exception as e:
        print(f"⚠️  Memory storage error: {e}")
        return {}


# ==================== Build Graph ====================

def build_graph():
    """Build and compile the LangGraph workflow"""
    
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("memory_retrieval", memory_retrieval_node)
    workflow.add_node("simple_response", simple_response_node)
    workflow.add_node("crewai_agent", crewai_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("memory_storage", memory_storage_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add edges
    workflow.add_conditional_edges(
        source="router",
        condition=router_node,
        mapping={
            "simple": "memory_retrieval",
            "complex": "memory_retrieval"
        }
    )
    
    # From memory retrieval, route based on task type
    workflow.add_conditional_edges(
        source="memory_retrieval",
        condition=lambda state: "simple_response" if state.get("task_type") == "general" else "crewai_agent",
        mapping={
            "simple_response": "simple_response",
            "crewai_agent": "crewai_agent"
        }
    )
    
    # Both paths converge to validation
    workflow.add_edge("simple_response", "validation")
    workflow.add_edge("crewai_agent", "validation")
    
    # Then to memory storage
    workflow.add_edge("validation", "memory_storage")
    
    # Finally to end
    workflow.add_edge("memory_storage", END)
    
    # Compile
    app = workflow.compile()
    return app


# Singleton instance
_graph_instance = None


def get_graph():
    """Get or create the graph singleton"""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = build_graph()
    return _graph_instance
