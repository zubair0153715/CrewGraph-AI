from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import settings
from app.models import Base, engine, SessionLocal, User, ToolDefinition
from app.api.routes import router
from app.utils.auth import hash_password, create_access_token


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AgentOS API",
    description="AI Agent Operating System - Multi-agent platform for task automation",
    version="1.0.0"
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(router, prefix="/api/v1")


# Auth endpoint (login)
class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/v1/auth/login")
def login(login_data: LoginRequest, db: Session = Depends(lambda: SessionLocal())):
    """Authenticate user and return JWT token"""
    from app.utils.auth import verify_password
    
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise Exception("Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event("startup")
async def startup_event():
    """Initialize default tools on startup"""
    db = SessionLocal()
    try:
        # Add default tools if they don't exist
        default_tools = [
            {
                "name": "browser_search",
                "description": "Search the web using DuckDuckGo",
                "config_schema": {}
            },
            {
                "name": "web_scraping",
                "description": "Scrape content from websites",
                "config_schema": {}
            }
        ]
        
        for tool_data in default_tools:
            existing = db.query(ToolDefinition).filter(
                ToolDefinition.name == tool_data["name"]
            ).first()
            
            if not existing:
                tool = ToolDefinition(**tool_data)
                db.add(tool)
        
        db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AgentOS API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
