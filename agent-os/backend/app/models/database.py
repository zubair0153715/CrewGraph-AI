from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List
import uuid

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    """User model for authentication and agent ownership"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    
    # Subscription
    subscription_tier = Column(String, default="basic")  # basic, pro, agency
    subscription_expires = Column(DateTime, nullable=True)


class Agent(Base):
    """Agent model - user-created AI agents"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., "Research Agent", "Content Agent"
    description = Column(Text)
    autonomy_level = Column(String, default="medium")  # low, medium, high
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Configuration
    tools = Column(JSON, default=list)  # List of enabled tools
    memory_enabled = Column(Boolean, default=True)
    system_prompt = Column(Text)  # Custom system instructions
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    tasks = relationship("Task", back_populates="agent", cascade="all, delete-orphan")


class Task(Base):
    """Task model - represents a task to be executed by an agent"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=1)  # 1-5, 1 being highest
    input_data = Column(JSON)  # Input parameters for the task
    output_data = Column(JSON)  # Result from task execution
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")


class AgentMemory(Base):
    """Vector memory storage for agents (metadata, actual vectors in Qdrant)"""
    __tablename__ = "agent_memories"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON)  # Additional context
    embedding_ref = Column(String)  # Reference to Qdrant vector ID
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent")


class ToolDefinition(Base):
    """Available tools that can be assigned to agents"""
    __tablename__ = "tool_definitions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    config_schema = Column(JSON)  # JSON schema for tool configuration
    is_active = Column(Boolean, default=True)


# Indexes for performance
from sqlalchemy import Index
Index('idx_tasks_status', Task.status)
Index('idx_tasks_owner', Task.owner_id)
Index('idx_agents_owner', Agent.owner_id)
