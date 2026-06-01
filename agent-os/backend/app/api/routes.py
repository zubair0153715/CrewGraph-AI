from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

from app.models import SessionLocal, User, Agent, Task, ToolDefinition, generate_uuid
from app.utils.auth import get_current_user, hash_password
from app.agents.orchestrator import AgentOrchestrator, DEFAULT_AGENT_TEMPLATES


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schemas
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    subscription_tier: str
    
    class Config:
        from_attributes = True


class AgentCreate(BaseModel):
    name: str
    role: str
    description: str = None
    autonomy_level: str = "medium"
    tools: List[str] = []
    memory_enabled: bool = True
    system_prompt: str = None


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    autonomy_level: str
    tools: list
    memory_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    agent_id: str
    title: str
    description: str
    priority: int = 1
    input_data: dict = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    agent_id: str
    output_data: dict = None
    error_message: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth endpoints
@router.post("/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


# Agent endpoints
@router.get("/agents/templates")
def get_agent_templates():
    """Get predefined agent templates"""
    return {"templates": DEFAULT_AGENT_TEMPLATES}


@router.post("/agents", response_model=AgentResponse)
def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    agent = Agent(
        owner_id=current_user.id,
        **agent_data.model_dump()
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent


@router.get("/agents", response_model=List[AgentResponse])
def list_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all agents for current user"""
    agents = db.query(Agent).filter(Agent.owner_id == current_user.id).all()
    return agents


@router.get("/agents/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific agent"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.delete("/agents/{agent_id}")
def delete_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an agent"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(agent)
    db.commit()
    
    return {"message": "Agent deleted successfully"}


# Task endpoints
@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    # Verify agent exists and belongs to user
    agent = db.query(Agent).filter(
        Agent.id == task_data.agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    task = Task(
        owner_id=current_user.id,
        **task_data.model_dump()
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for current user"""
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).order_by(
        Task.created_at.desc()
    ).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.post("/tasks/{task_id}/execute")
def execute_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a task with its assigned agent"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status == "running":
        raise HTTPException(status_code=400, detail="Task is already running")
    
    # Get agent
    agent = db.query(Agent).filter(Agent.id == task.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update task status
    task.status = "running"
    task.started_at = datetime.utcnow()
    db.commit()
    
    try:
        # Execute task using orchestrator
        orchestrator = AgentOrchestrator(agent)
        result = orchestrator.execute_task(
            task_description=f"{task.title}: {task.description}",
            expected_output="Complete and well-formatted result"
        )
        
        # Update task with result
        task.status = "completed"
        task.output_data = {"result": result}
        task.completed_at = datetime.utcnow()
        db.commit()
        
        return {"status": "completed", "result": result}
        
    except Exception as e:
        task.status = "failed"
        task.error_message = str(e)
        db.commit()
        
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@router.get("/tools")
def list_tools(db: Session = Depends(get_db)):
    """List available tools"""
    tools = db.query(ToolDefinition).filter(ToolDefinition.is_active == True).all()
    return {"tools": [t.name for t in tools]}
