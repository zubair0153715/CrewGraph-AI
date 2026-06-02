"""
Database Models - SQLAlchemy models for Leads, Campaigns, Emails
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    website = Column(String)
    email = Column(String)
    industry = Column(String)
    country = Column(String, default="US")
    company_size = Column(String)
    decision_maker = Column(String)
    status = Column(String, default="new")  # new, contacted, replied, converted
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    emails = relationship("Email", back_populates="lead")
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    def __repr__(self):
        return f"<Lead {self.company_name}>"

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    niche = Column(String)
    target_country = Column(String, default="US")
    status = Column(String, default="active")  # active, paused, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    leads = relationship("Lead", back_populates="campaign")
    
    def __repr__(self):
        return f"<Campaign {self.name}>"

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    subject = Column(String)
    body = Column(Text)
    email_type = Column(String)  # cold, follow_up_1, follow_up_2, follow_up_3
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    response_received = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="emails")
    
    def __repr__(self):
        return f"<Email to {self.lead_id}>"

# Database Setup
def get_database_url():
    """Get database URL from environment or use SQLite for MVP"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Use SQLite for local development (free, no setup needed)
        return "sqlite:///./data/crewgraph.db"
    return db_url

# Create engine
engine = create_engine(
    get_database_url(),
    connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {}
)

# Create tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    # Initialize database
    init_db()
    print("✅ Database initialized successfully!")
    
    # Test creating a lead
    db = SessionLocal()
    test_lead = Lead(
        company_name="Test Company",
        website="https://test.com",
        email="contact@test.com",
        industry="SaaS",
        country="US"
    )
    db.add(test_lead)
    db.commit()
    print(f"✅ Created test lead: {test_lead}")
    db.close()
