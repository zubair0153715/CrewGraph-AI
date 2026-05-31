"""
CrewGraph-AI v3.0 - Universal Agent Factory
Full Autonomous Multi-Agent System with Unlimited Custom Agents
Every type of agent for every type of task - Social Media, Freelance, Business, Research, Code, etc.
"""

import os
import json
import time
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from crewai import Agent, Task, Crew, Process
import chromadb
from chromadb.config import Settings
import requests
from duckduckgo_search import ddg
from PIL import Image
import base64
import io

# ==================== CONFIGURATION ====================

class Config:
    """Global configuration for Universal Agent Factory"""
    OLLAMA_BASE_URL = "http://localhost:11434"
    LLM_MODEL = "qwen2.5:7b"
    VISION_MODEL = "llava:7b"
    EMBEDDING_MODEL = "nomic-embed-text"
    CHROMA_PERSIST_DIR = "./chroma_db_universal"
    MAX_AGENTS = 50
    MAX_WORKFLOWS = 100
    
    # Agent Categories
    AGENT_CATEGORIES = {
        "social_media": ["Instagram Manager", "Twitter/X Strategist", "LinkedIn Optimizer", "Facebook Ads Specialist", "TikTok Creator", "YouTube SEO Expert"],
        "freelance": ["Fiverr Rank Booster", "Upwork Proposal Writer", "Freelance Pricing Analyst", "Client Communication Manager", "Portfolio Builder"],
        "business": ["Business Analyst", "Market Researcher", "Competitor Analyzer", "Financial Advisor", "HR Recruiter", "Sales Funnel Optimizer"],
        "content": ["Blog Writer", "SEO Specialist", "Copywriter", "Video Script Writer", "Podcast Producer", "Newsletter Curator"],
        "technical": ["Full Stack Developer", "DevOps Engineer", "Data Scientist", "ML Engineer", "Cybersecurity Analyst", "QA Tester"],
        "creative": ["Graphic Designer Assistant", "Brand Strategist", "Content Planner", "Storyteller", "Music Composer Assistant"],
        "automation": ["Workflow Automator", "Email Marketing Bot", "CRM Manager", "Lead Generator", "Appointment Scheduler"],
        "research": ["Academic Researcher", "News Analyst", "Trend Spotter", "Data Miner", "Patent Analyst"],
        "personal": ["Life Coach", "Fitness Trainer", "Nutrition Advisor", "Travel Planner", "Language Tutor"]
    }

config = Config()

# ==================== UNIVERSAL AGENT FACTORY ====================

class UniversalAgentFactory:
    """Create any type of AI agent for any task"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, Dict] = {}
        self.active_workflows: Dict[str, Dict] = {}
        
    def create_agent(self, 
                    name: str, 
                    category: str, 
                    role: str, 
                    goal: str, 
                    backstory: str,
                    skills: List[str],
                    tools: Optional[List] = None,
                    verbose: bool = True) -> Agent:
        """
        Create a custom agent with specific role and capabilities
        """
        if len(self.agents) >= config.MAX_AGENTS:
            raise Exception(f"Maximum agent limit ({config.MAX_AGENTS}) reached")
        
        # Build comprehensive system prompt
        system_prompt = f"""You are {name}, a highly skilled {role}.
        
YOUR GOAL: {goal}

BACKGROUND: {backstory}

YOUR SKILLS:
{chr(10).join(['• ' + skill for skill in skills])}

INSTRUCTIONS:
- Think step-by-step before acting
- Use available tools effectively
- Provide detailed, actionable outputs
- Adapt to user's specific needs
- Maintain professional tone
- Ask clarifying questions when needed
- Learn from feedback and improve

Remember: You are an autonomous agent capable of handling complex tasks independently."""

        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=True,
            llm=f"ollama/{config.LLM_MODEL}",
            tools=tools or [],
            system_template=system_prompt
        )
        
        self.agents[name] = agent
        self.agent_configs[name] = {
            "category": category,
            "role": role,
            "goal": goal,
            "skills": skills,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        print(f"✅ Agent '{name}' created successfully in category '{category}'")
        return agent
    
    def get_available_categories(self) -> Dict[str, List[str]]:
        """Get all available agent categories and predefined roles"""
        return config.AGENT_CATEGORIES
    
    def list_agents(self) -> List[Dict]:
        """List all created agents"""
        return [
            {
                "name": name,
                **config_data
            }
            for name, config_data in self.agent_configs.items()
        ]
    
    def delete_agent(self, name: str) -> bool:
        """Delete an agent"""
        if name in self.agents:
            del self.agents[name]
            del self.agent_configs[name]
            print(f"🗑️ Agent '{name}' deleted")
            return True
        return False

# ==================== SPECIALIZED TOOL KITS ====================

class ToolKits:
    """Pre-built tool kits for different agent types"""
    
    @staticmethod
    def social_media_tools() -> List:
        """Tools for social media management agents"""
        from crewai_tools import SerperDevTool, ScrapeWebsiteTool
        return [
            # Web search for trends
            {"type": "web_search", "name": "Trend Finder"},
            # Content analyzer
            {"type": "content_analyzer", "name": "Post Performance Analyzer"},
            # Hashtag generator
            {"type": "hashtag_generator", "name": "Smart Hashtag Generator"},
            # Scheduling assistant
            {"type": "scheduler", "name": "Optimal Post Scheduler"}
        ]
    
    @staticmethod
    def freelance_tools() -> List:
        """Tools for freelance platform optimization"""
        return [
            {"type": "keyword_optimizer", "name": "Gig SEO Optimizer"},
            {"type": "proposal_writer", "name": "Winning Proposal Generator"},
            {"type": "pricing_analyzer", "name": "Competitive Pricing Analyzer"},
            {"type": "review_manager", "name": "Client Review Booster"}
        ]
    
    @staticmethod
    def business_tools() -> List:
        """Tools for business operations"""
        return [
            {"type": "market_research", "name": "Market Intelligence"},
            {"type": "competitor_analysis", "name": "Competitor Tracker"},
            {"type": "financial_modeling", "name": "Financial Forecaster"},
            {"type": "crm_integration", "name": "CRM Auto-Updater"}
        ]
    
    @staticmethod
    def content_tools() -> List:
        """Tools for content creation"""
        return [
            {"type": "seo_analyzer", "name": "SEO Optimizer"},
            {"type": "grammar_checker", "name": "Advanced Grammar Check"},
            {"type": "plagiarism_checker", "name": "Originality Verifier"},
            {"type": "readability_scorer", "name": "Readability Analyzer"}
        ]
    
    @staticmethod
    def technical_tools() -> List:
        """Tools for technical tasks"""
        return [
            {"type": "code_executor", "name": "Safe Code Sandbox"},
            {"type": "debugger", "name": "Auto Debugger"},
            {"type": "documentation_generator", "name": "Doc Generator"},
            {"type": "testing_framework", "name": "Test Suite Creator"}
        ]

# ==================== AUTONOMOUS WORKFLOW ENGINE ====================

class WorkflowEngine:
    """Execute complex multi-agent workflows autonomously"""
    
    def __init__(self, agent_factory: UniversalAgentFactory):
        self.factory = agent_factory
        self.workflows: Dict[str, Dict] = {}
        
    def create_workflow(self, 
                       name: str,
                       description: str,
                       agents: List[str],
                       tasks: List[Dict],
                       auto_execute: bool = False) -> str:
        """
        Create a workflow with multiple agents and tasks
        """
        workflow_id = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:8]
        
        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "agents": agents,
            "tasks": tasks,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "auto_execute": auto_execute
        }
        
        self.workflows[workflow_id] = workflow
        
        if auto_execute:
            asyncio.create_task(self.execute_workflow(workflow_id))
        
        return workflow_id
    
    async def execute_workflow(self, workflow_id: str) -> Dict:
        """Execute a workflow autonomously"""
        if workflow_id not in self.workflows:
            raise Exception("Workflow not found")
        
        workflow = self.workflows[workflow_id]
        workflow["status"] = "running"
        
        results = []
        for task_config in workflow["tasks"]:
            agent_name = task_config["agent"]
            task_description = task_config["description"]
            
            if agent_name not in self.factory.agents:
                raise Exception(f"Agent '{agent_name}' not found")
            
            agent = self.factory.agents[agent_name]
            
            # Create CrewAI task
            task = Task(
                description=task_description,
                agent=agent,
                expected_output="Detailed, actionable result with next steps"
            )
            
            # Execute task
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            results.append({
                "task": task_description,
                "agent": agent_name,
                "result": str(result),
                "timestamp": datetime.now().isoformat()
            })
        
        workflow["status"] = "completed"
        workflow["results"] = results
        workflow["completed_at"] = datetime.now().isoformat()
        
        return workflow

# ==================== PRE-BUILT AGENT TEMPLATES ====================

class AgentTemplates:
    """Ready-to-use agent templates for common use cases"""
    
    @staticmethod
    def create_social_media_manager(factory: UniversalAgentFactory, platforms: List[str]) -> Agent:
        """Create a comprehensive social media manager"""
        platforms_str = ", ".join(platforms)
        
        return factory.create_agent(
            name="SocialMediaPro",
            category="social_media",
            role="Social Media Manager",
            goal=f"Manage and grow presence on {platforms_str}, increase engagement, and build brand authority",
            backstory="""You are an expert social media strategist with 10+ years of experience managing accounts for Fortune 500 companies.
You understand algorithm changes, viral content patterns, and audience psychology across all major platforms.""",
            skills=[
                "Content strategy and calendar planning",
                "Viral post creation and optimization",
                "Hashtag research and trending topics",
                "Analytics interpretation and ROI tracking",
                "Community management and engagement",
                "Influencer collaboration",
                "Paid advertising campaign management",
                "Crisis communication and reputation management"
            ],
            tools=ToolKits.social_media_tools()
        )
    
    @staticmethod
    def create_fiverr_optimizer(factory: UniversalAgentFactory) -> Agent:
        """Create a Fiverr ranking specialist"""
        return factory.create_agent(
            name="FiverrRankBooster",
            category="freelance",
            role="Fiverr Ranking Specialist",
            goal="Optimize gigs, write winning proposals, and achieve top seller status on Fiverr",
            backstory="""You are a Top Rated Seller on Fiverr with multiple $100k+ earning gigs.
You know exactly what makes gigs rank #1, how to write proposals that convert, and how to maintain 5-star ratings consistently.""",
            skills=[
                "Gig SEO optimization (titles, tags, descriptions)",
                "High-converting gig image and video creation",
                "Pricing strategy and package optimization",
                "Buyer requirement analysis",
                "Custom offer creation",
                "Review generation and management",
                "Response time optimization",
                "Order completion rate improvement"
            ],
            tools=ToolKits.freelance_tools()
        )
    
    @staticmethod
    def create_business_automator(factory: UniversalAgentFactory) -> Agent:
        """Create a business operations automator"""
        return factory.create_agent(
            name="BizAutoPilot",
            category="business",
            role="Business Operations Automator",
            goal="Automate repetitive business tasks, optimize workflows, and increase operational efficiency",
            backstory="""You are a business process expert who has automated operations for 500+ companies.
You specialize in identifying bottlenecks, implementing automation tools, and creating scalable systems.""",
            skills=[
                "Process mapping and optimization",
                "Workflow automation (Zapier, Make, n8n)",
                "CRM implementation and management",
                "Email marketing automation",
                "Lead generation and nurturing",
                "Customer support ticketing systems",
                "Inventory and supply chain management",
                "Financial reporting and forecasting"
            ],
            tools=ToolKits.business_tools()
        )
    
    @staticmethod
    def create_full_stack_dev(factory: UniversalAgentFactory) -> Agent:
        """Create a full-stack development agent"""
        return factory.create_agent(
            name="CodeMaster3000",
            category="technical",
            role="Full Stack Developer",
            goal="Build, test, deploy, and maintain complete web applications autonomously",
            backstory="""You are a senior full-stack developer with expertise in modern frameworks and cloud deployment.
You can take a project from idea to production-ready application without human intervention.""",
            skills=[
                "Frontend development (React, Vue, Angular)",
                "Backend development (Node.js, Python, Go)",
                "Database design and optimization (SQL, NoSQL)",
                "API design and integration (REST, GraphQL)",
                "Cloud deployment (AWS, GCP, Azure)",
                "CI/CD pipeline setup",
                "Security best practices",
                "Performance optimization"
            ],
            tools=ToolKits.technical_tools()
        )

# ==================== MAIN SYSTEM ====================

class CrewGraphUniversal:
    """Main universal agent system"""
    
    def __init__(self):
        self.factory = UniversalAgentFactory()
        self.workflow_engine = WorkflowEngine(self.factory)
        self.templates = AgentTemplates()
        self.sessions: Dict[str, List] = {}
        
    def quick_start(self, use_case: str) -> Agent:
        """Quick start with pre-built agents for common use cases"""
        if use_case == "social_media":
            return self.templates.create_social_media_manager(self.factory, ["Instagram", "Twitter", "LinkedIn"])
        elif use_case == "fiverr":
            return self.templates.create_fiverr_optimizer(self.factory)
        elif use_case == "business":
            return self.templates.create_business_automator(self.factory)
        elif use_case == "development":
            return self.templates.create_full_stack_dev(self.factory)
        else:
            raise ValueError(f"Unknown use case: {use_case}")
    
    def create_custom_agent(self, **kwargs) -> Agent:
        """Create a fully custom agent"""
        return self.factory.create_agent(**kwargs)
    
    def run_autonomous_task(self, agent_name: str, task: str) -> str:
        """Run a single autonomous task"""
        if agent_name not in self.factory.agents:
            raise Exception(f"Agent '{agent_name}' not found")
        
        agent = self.factory.agents[agent_name]
        
        crew_task = Task(
            description=task,
            agent=agent,
            expected_output="Complete, detailed solution with actionable steps"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[crew_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)

# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    print("🚀 CrewGraph-AI v3.0 - Universal Agent Factory")
    print("=" * 60)
    
    # Initialize system
    system = CrewGraphUniversal()
    
    # Example 1: Create social media manager
    print("\n📱 Creating Social Media Manager...")
    sm_agent = system.quick_start("social_media")
    
    # Example 2: Create Fiverr optimizer
    print("\n💼 Creating Fiverr Ranking Specialist...")
    fiverr_agent = system.quick_start("fiverr")
    
    # Example 3: Create custom agent
    print("\n🎯 Creating Custom E-commerce Manager...")
    ecommerce_agent = system.create_custom_agent(
        name="EcomBoss",
        category="business",
        role="E-commerce Store Manager",
        goal="Manage entire e-commerce operation from product listing to customer service",
        backstory="Expert e-commerce manager with $10M+ in sales across Shopify, Amazon, and WooCommerce",
        skills=[
            "Product research and sourcing",
            "Listing optimization",
            "Inventory management",
            "Customer service automation",
            "PPC campaign management",
            "Conversion rate optimization"
        ]
    )
    
    # Example 4: Run autonomous task
    print("\n⚡ Running Autonomous Task...")
    result = system.run_autonomous_task(
        "FiverrRankBooster",
        "Analyze my Fiverr gig titled 'Logo Design' and provide 10 specific improvements to rank #1"
    )
    print(f"\nResult:\n{result}")
    
    print("\n✅ System ready! Create unlimited agents for any task.")
