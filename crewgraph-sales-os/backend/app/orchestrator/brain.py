"""
Orchestrator - The Brain that coordinates all agents and manages workflows
Uses LangGraph for workflow orchestration
"""

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import Graph, END
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Import agents
from .lead_finder import LeadFinderAgent
from .research import ResearchAgent
from .cold_email import ColdEmailAgent

load_dotenv()

class WorkflowState(TypedDict):
    niche: str
    country: str
    count: int
    leads: list
    research_results: list
    emails: list
    strategy: str
    error: str

class Orchestrator:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize agents
        self.lead_finder = LeadFinderAgent()
        self.researcher = ResearchAgent()
        self.email_agent = ColdEmailAgent()
    
    def find_leads_node(self, state: WorkflowState):
        """Find leads based on niche"""
        try:
            print(f"🔍 Finding leads in {state['niche']}...")
            leads = self.lead_finder.find_leads(
                niche=state['niche'],
                country=state['country'],
                count=state['count']
            )
            return {"leads": leads}
        except Exception as e:
            return {"error": f"Lead finder failed: {str(e)}"}
    
    def research_node(self, state: WorkflowState):
        """Research each lead"""
        try:
            print(f"📊 Researching {len(state['leads'])} companies...")
            if not state['leads']:
                return {"research_results": []}
            
            research_results = self.researcher.batch_research(state['leads'])
            return {"research_results": research_results}
        except Exception as e:
            return {"error": f"Research failed: {str(e)}"}
    
    def generate_emails_node(self, state: WorkflowState):
        """Generate personalized emails"""
        try:
            print("✉️ Generating cold emails...")
            if not state['research_results']:
                return {"emails": []}
            
            emails = []
            for item in state['research_results']:
                lead = item['lead']
                email = self.email_agent.generate_email(
                    company_name=lead.get('company_name', ''),
                    industry=lead.get('industry', state['niche']),
                    pain_point="",  # Can extract from research
                    tone='professional'
                )
                emails.append(email)
            
            return {"emails": emails}
        except Exception as e:
            return {"error": f"Email generation failed: {str(e)}"}
    
    def strategy_node(self, state: WorkflowState):
        """Generate overall sales strategy"""
        try:
            print("📈 Creating sales strategy...")
            strategy = f"""
            SALES STRATEGY for {state['niche']} in {state['country']}:
            
            1. Focus on pain points: Manual processes, time-consuming outreach
            2. Offer: Free demo of AI automation
            3. Follow-up cadence: Day 1, Day 4, Day 8, Day 15
            4. Key messaging: Save 20+ hours/week on lead gen
            5. Social proof: Mention similar companies helped
            
            Total leads found: {len(state['leads']) if state['leads'] else 0}
            Emails generated: {len(state['emails']) if state['emails'] else 0}
            """
            return {"strategy": strategy}
        except Exception as e:
            return {"error": f"Strategy failed: {str(e)}"}
    
    def should_continue(self, state: WorkflowState):
        """Decide next step based on current state"""
        if state.get('error'):
            return "end"
        if not state.get('leads'):
            return "find_leads"
        if not state.get('research_results'):
            return "research"
        if not state.get('emails'):
            return "generate_emails"
        return "strategy"
    
    def build_graph(self):
        """Build the workflow graph using LangGraph"""
        workflow = Graph()
        
        # Add nodes
        workflow.add_node("find_leads", self.find_leads_node)
        workflow.add_node("research", self.research_node)
        workflow.add_node("generate_emails", self.generate_emails_node)
        workflow.add_node("strategy", self.strategy_node)
        
        # Set entry point
        workflow.set_entry_point("find_leads")
        
        # Add edges
        workflow.add_edge("find_leads", "research")
        workflow.add_edge("research", "generate_emails")
        workflow.add_edge("generate_emails", "strategy")
        workflow.add_edge("strategy", END)
        
        return workflow.compile()
    
    def run_campaign(self, niche: str, country: str = "US", count: int = 10):
        """Run complete campaign workflow"""
        initial_state = {
            "niche": niche,
            "country": country,
            "count": count,
            "leads": [],
            "research_results": [],
            "emails": [],
            "strategy": "",
            "error": ""
        }
        
        app = self.build_graph()
        result = app.invoke(initial_state)
        
        return result

# Example usage
if __name__ == "__main__":
    orchestrator = Orchestrator()
    result = orchestrator.run_campaign(niche="SaaS", country="US", count=5)
    print("\n" + "="*50)
    print("CAMPAIGN RESULTS:")
    print("="*50)
    print(f"Leads: {len(result.get('leads', []))}")
    print(f"Strategy: {result.get('strategy', '')}")
