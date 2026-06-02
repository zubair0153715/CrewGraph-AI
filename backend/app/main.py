"""
CrewGraph Sales OS - Main FastAPI Application
AI Sales Automation System with Multi-Agent Architecture
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="CrewGraph Sales OS",
    description="AI Sales Automation System - Lead Generation & Outreach",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class LeadRequest(BaseModel):
    niche: str
    country: Optional[str] = "US"
    count: Optional[int] = 10

class CampaignRequest(BaseModel):
    niche: str
    country: Optional[str] = "US"
    email_tone: Optional[str] = "professional"
    follow_ups: Optional[int] = 3

class Lead(BaseModel):
    company_name: str
    website: str
    email: Optional[str]
    industry: str
    country: str

class EmailTemplate(BaseModel):
    subject: str
    body: str
    follow_up_sequence: List[str]

class CampaignResult(BaseModel):
    leads: List[Lead]
    emails: List[EmailTemplate]
    strategy: str

# Health Check
@app.get("/")
async def root():
    return {
        "message": "🧠 CrewGraph Sales OS is running!",
        "status": "active",
        "features": [
            "Lead Finder Agent",
            "Research Agent", 
            "Cold Email Agent",
            "Follow-up Agent",
            "Sales Strategy Agent"
        ]
    }

# Find Leads Endpoint
@app.post("/api/find-leads", response_model=List[Lead])
async def find_leads(request: LeadRequest):
    """
    Find leads in specified niche using Lead Finder Agent
    """
    # TODO: Integrate with Lead Finder Agent
    # Mock response for MVP
    return [
        Lead(
            company_name=f"{request.niche} Company {i}",
            website=f"https://example{i}.com",
            email=f"contact@example{i}.com",
            industry=request.niche,
            country=request.country
        )
        for i in range(1, min(request.count + 1, 6))
    ]

# Generate Cold Emails Endpoint
@app.post("/api/generate-emails", response_model=EmailTemplate)
async def generate_emails(niche: str, tone: str = "professional"):
    """
    Generate personalized cold emails using Cold Email Agent
    """
    # TODO: Integrate with Cold Email Agent
    return EmailTemplate(
        subject=f"Boost Your {niche} Business with AI Automation",
        body=f"""Hi there,

I noticed your company in the {niche} space and wanted to reach out...

[Personalized pitch based on research]

Would you be open to a quick call this week?

Best regards,
Your AI Assistant""",
        follow_up_sequence=[
            "Quick follow-up on my previous email...",
            "Just checking if you saw my message...",
            "Final attempt - would love to connect..."
        ]
    )

# Full Campaign Endpoint
@app.post("/api/run-campaign", response_model=CampaignResult)
async def run_campaign(request: CampaignRequest):
    """
    Run complete sales campaign: Find leads → Research → Generate emails → Strategy
    """
    # TODO: Integrate with Orchestrator + All Agents
    leads = [
        Lead(
            company_name=f"{request.niche} Corp {i}",
            website=f"https://{request.niche.lower()}{i}.com",
            email=f"info@{request.niche.lower()}{i}.com",
            industry=request.niche,
            country=request.country
        )
        for i in range(1, 4)
    ]
    
    emails = [
        EmailTemplate(
            subject=f"Transform Your {request.niche} Outreach with AI",
            body=f"Personalized email for {lead.company_name}...",
            follow_up_sequence=["Follow-up 1", "Follow-up 2", "Follow-up 3"]
        )
        for lead in leads
    ]
    
    return CampaignResult(
        leads=leads,
        emails=emails,
        strategy=f"Focus on {request.niche} pain points. Offer free demo. Follow up every 3 days."
    )

# Agent Status Endpoint
@app.get("/api/agents/status")
async def get_agents_status():
    """
    Get status of all AI agents
    """
    return {
        "orchestrator": "ready",
        "lead_finder": "ready",
        "research_agent": "ready",
        "email_agent": "ready",
        "follow_up_agent": "ready",
        "strategy_agent": "ready",
        "memory_agent": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
