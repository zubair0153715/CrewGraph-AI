"""
Database Models for CrewGraph Sales OS
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base


class PlanType(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    AGENCY = "agency"


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    REPLIED = "replied"
    INTERESTED = "interested"
    MEETING_BOOKED = "meeting_booked"
    CLOSED = "closed"
    LOST = "lost"


class EmailStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"
    REPLIED = "replied"
    BOUNCED = "bounced"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    plan = Column(SQLEnum(PlanType), default=PlanType.FREE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    leads = relationship("Lead", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")


class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subscription_plan = Column(SQLEnum(PlanType), default=PlanType.FREE)
    monthly_email_limit = Column(Integer, default=1000)
    emails_sent_this_month = Column(Integer, default=0)
    api_key = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="organization")
    leads = relationship("Lead", back_populates="organization")
    campaigns = relationship("Campaign", back_populates="organization")


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Company Info
    company_name = Column(String, nullable=False)
    website = Column(String)
    email = Column(String)
    phone = Column(String)
    industry = Column(String)
    country = Column(String)
    employee_count = Column(Integer)
    revenue = Column(String)
    
    # Qualification
    qualification_score = Column(Float, default=0.0)  # 0-100
    budget_potential = Column(String)  # High/Medium/Low
    intent_signals = Column(Text)  # JSON string
    
    # Status
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW)
    source = Column(String)  # linkedin/google_maps/crunchbase/etc
    
    # Metadata
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="leads")
    user = relationship("User", back_populates="leads")
    emails = relationship("Email", back_populates="lead")
    interactions = relationship("Interaction", back_populates="lead")


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String, nullable=False)
    description = Column(Text)
    target_niche = Column(String)
    target_country = Column(String)
    
    # Stats
    total_leads = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    meetings_booked = Column(Integer, default=0)
    
    status = Column(String, default="draft")  # draft/active/paused/completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    user = relationship("User", back_populates="campaigns")
    emails = relationship("Email", back_populates="campaign")


class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    email_type = Column(String)  # cold/follow-up-1/follow-up-2/etc
    
    status = Column(SQLEnum(EmailStatus), default=EmailStatus.PENDING)
    sent_at = Column(DateTime(timezone=True))
    opened_at = Column(DateTime(timezone=True))
    replied_at = Column(DateTime(timezone=True))
    
    # Tracking
    message_id = Column(String)
    bounce_reason = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="emails")
    campaign = relationship("Campaign", back_populates="emails")


class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    
    interaction_type = Column(String, nullable=False)  # email/reply/meeting/call
    content = Column(Text, nullable=False)
    direction = Column(String)  # outbound/inbound
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="interactions")
