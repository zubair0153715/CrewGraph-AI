"""
Main FastAPI Application - CrewGraph Sales OS
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from .config import settings
from .database import engine, get_db, init_db
from .auth import get_current_user, create_access_token
from .models import User, Organization, Lead, Campaign, Email
from .agents.lead_finder import LeadFinderAgent

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered sales automation platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Pydantic Schemas ==============

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    organization_name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class LeadFindRequest(BaseModel):
    niche: str
    country: str
    count: int = 10


class LeadResponse(BaseModel):
    id: int
    company_name: str
    website: Optional[str]
    email: Optional[str]
    industry: Optional[str]
    country: Optional[str]
    status: str
    qualification_score: Optional[float]


class CampaignCreate(BaseModel):
    name: str
    target_niche: str
    target_country: str
    description: Optional[str] = None


class CampaignResponse(BaseModel):
    id: int
    name: str
    status: str
    total_leads: int
    emails_sent: int
    replies: int


class AnalyticsResponse(BaseModel):
    total_leads: int
    total_campaigns: int
    emails_sent: int
    reply_rate: float
    meetings_booked: int


# ============== Auth Routes ==============

@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create organization
    org = Organization(
        name=user_data.organization_name or f"{user_data.email.split('@')[0]}'s Org"
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=pwd_context.hash(user_data.password),
        full_name=user_data.full_name,
        organization_id=org.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate token
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token}


@app.post("/auth/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    from .auth import verify_password
    
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token}


@app.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "plan": current_user.plan.value,
        "organization_id": current_user.organization_id
    }


# ============== Lead Routes ==============

@app.post("/api/leads/find", response_model=List[LeadResponse])
async def find_leads(
    request: LeadFindRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Find new leads using AI agent"""
    try:
        # Use Lead Finder Agent
        finder = LeadFinderAgent()
        leads_data = finder.find_leads(
            niche=request.niche,
            country=request.country,
            count=request.count
        )
        
        # Save leads to database
        created_leads = []
        for lead_data in leads_data:
            lead = Lead(
                organization_id=current_user.organization_id,
                user_id=current_user.id,
                company_name=lead_data.get("company_name", "Unknown"),
                website=lead_data.get("website"),
                email=lead_data.get("email"),
                industry=lead_data.get("industry"),
                country=lead_data.get("country", request.country),
                employee_count=lead_data.get("employee_count"),
                source="ai_agent",
                status="new"
            )
            db.add(lead)
            created_leads.append(lead)
        
        db.commit()
        
        # Refresh to get IDs
        for lead in created_leads:
            db.refresh(lead)
        
        return [
            LeadResponse(
                id=lead.id,
                company_name=lead.company_name,
                website=lead.website,
                email=lead.email,
                industry=lead.industry,
                country=lead.country,
                status=lead.status.value,
                qualification_score=lead.qualification_score
            )
            for lead in created_leads
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding leads: {str(e)}"
        )


@app.get("/api/leads", response_model=List[LeadResponse])
async def get_leads(
    status_filter: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all leads for current user"""
    query = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    )
    
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    
    leads = query.order_by(Lead.created_at.desc()).limit(limit).all()
    
    return [
        LeadResponse(
            id=lead.id,
            company_name=lead.company_name,
            website=lead.website,
            email=lead.email,
            industry=lead.industry,
            country=lead.country,
            status=lead.status.value,
            qualification_score=lead.qualification_score
        )
        for lead in leads
    ]


# ============== Campaign Routes ==============

@app.post("/api/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new campaign"""
    campaign = Campaign(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        **campaign_data.dict(),
        status="draft"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    return CampaignResponse(
        id=campaign.id,
        name=campaign.name,
        status=campaign.status,
        total_leads=campaign.total_leads,
        emails_sent=campaign.emails_sent,
        replies=campaign.replies
    )


@app.get("/api/campaigns", response_model=List[CampaignResponse])
async def get_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all campaigns"""
    campaigns = db.query(Campaign).filter(
        Campaign.organization_id == current_user.organization_id
    ).order_by(Campaign.created_at.desc()).all()
    
    return [
        CampaignResponse(
            id=camp.id,
            name=camp.name,
            status=camp.status,
            total_leads=camp.total_leads,
            emails_sent=camp.emails_sent,
            replies=camp.replies
        )
        for camp in campaigns
    ]


@app.post("/api/campaigns/{campaign_id}/run")
async def run_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run a campaign (find leads + generate emails)"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Update status
    campaign.status = "active"
    db.commit()
    
    # TODO: Implement full campaign workflow
    # 1. Find leads using LeadFinderAgent
    # 2. Qualify leads using QualifierAgent
    # 3. Generate emails using ColdEmailAgent
    # 4. Send emails using OutreachEngine
    
    return {
        "message": "Campaign started",
        "campaign_id": campaign_id,
        "status": "running"
    }


# ============== Analytics Routes ==============

@app.get("/api/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard analytics"""
    # Total leads
    total_leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).count()
    
    # Total campaigns
    total_campaigns = db.query(Campaign).filter(
        Campaign.organization_id == current_user.organization_id
    ).count()
    
    # Emails sent
    emails_sent = db.query(Email).filter(
        Email.status == "sent"
    ).join(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).count()
    
    # Replies
    replies = db.query(Email).filter(
        Email.status == "replied"
    ).join(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).count()
    
    # Reply rate
    reply_rate = (replies / emails_sent * 100) if emails_sent > 0 else 0.0
    
    # Meetings booked
    meetings_booked = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        Lead.status == "meeting_booked"
    ).count()
    
    return AnalyticsResponse(
        total_leads=total_leads,
        total_campaigns=total_campaigns,
        emails_sent=emails_sent,
        reply_rate=reply_rate,
        meetings_booked=meetings_booked
    )


# ============== Health Check ==============

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "database": "connected",
        "llm": "configured" if settings.GROQ_API_KEY else "not configured",
        "vector_db": "configured" if settings.QDRANT_URL else "not configured"
    }
