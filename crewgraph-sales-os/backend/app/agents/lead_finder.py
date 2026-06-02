"""
Lead Finder Agent - Finds leads from multiple sources
"""
from crewai import Agent, Task, Crew
from ..config import settings
import json


class LeadFinderAgent:
    """Agent that finds qualified leads from various sources"""
    
    def __init__(self, llm=None):
        self.llm = llm or self._get_llm()
        
        self.agent = Agent(
            role="Lead Generation Specialist",
            goal="Find high-quality leads matching specific criteria from multiple sources",
            backstory="""You are an expert lead generation specialist with years of experience 
            finding qualified prospects for B2B sales teams. You know how to identify decision-makers,
            analyze company fit, and extract accurate contact information.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]  # Will add scraping tools later
        )
    
    def _get_llm(self):
        """Get LLM from Groq or fallback"""
        if settings.GROQ_API_KEY:
            from langchain_groq import ChatGroq
            return ChatGroq(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.LLM_MODEL
            )
        else:
            raise ValueError("GROQ_API_KEY not configured")
    
    def find_leads(self, niche: str, country: str, count: int = 10) -> list:
        """
        Find leads based on criteria
        
        Args:
            niche: Industry/niche (e.g., "SaaS", "E-commerce")
            country: Target country
            count: Number of leads to find
        
        Returns:
            List of lead dictionaries
        """
        task = Task(
            description=f"""Find {count} qualified leads in the {niche} industry located in {country}.
            
            For each lead, provide:
            - Company name
            - Website URL
            - Email address (if available)
            - Industry/sub-niche
            - Employee count estimate
            - Country
            - Why they might need our services
            
            Focus on companies that:
            - Are actively growing
            - Have online presence
            - Fit typical B2B buyer profile
            
            Return results as a JSON array.""",
            expected_output="JSON array of lead objects with company details",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse JSON from result
        try:
            # Extract JSON from markdown code blocks if present
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', result.raw, re.DOTALL)
            if json_match:
                leads = json.loads(json_match.group(1))
            else:
                leads = json.loads(result.raw)
            return leads
        except Exception as e:
            print(f"Error parsing leads: {e}")
            return []


# Example usage
if __name__ == "__main__":
    finder = LeadFinderAgent()
    leads = finder.find_leads(niche="SaaS", country="US", count=5)
    print(f"Found {len(leads)} leads:")
    for lead in leads:
        print(f"- {lead.get('company_name', 'Unknown')}")
