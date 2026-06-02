"""
Lead Finder Agent - Finds potential leads based on niche and criteria
Uses web search, scraping, and data enrichment
"""

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LeadFinderAgent:
    def __init__(self):
        # Initialize LLM (Groq for free usage)
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.agent = Agent(
            role='Lead Generation Specialist',
            goal='Find high-quality leads in specified niches with accurate contact information',
            backstory="""You are an expert lead generator with years of experience in B2B sales.
            You excel at finding decision-makers, verifying contact information, and 
            identifying companies that would benefit from specific services.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def find_leads(self, niche: str, country: str = "US", count: int = 10):
        """
        Find leads in the specified niche
        """
        task = Task(
            description=f"""Find {count} companies in the {niche} industry located in {country}.
            
            For each company, provide:
            1. Company name
            2. Website URL
            3. Email address (if available)
            4. Industry/sub-niche
            5. Company size (if available)
            6. Key decision makers (if available)
            
            Focus on companies that are likely to need automation and AI solutions.
            Prioritize quality over quantity.""",
            expected_output="List of leads with complete contact information",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=2
        )
        
        result = crew.kickoff()
        return result

# Example usage
if __name__ == "__main__":
    finder = LeadFinderAgent()
    leads = finder.find_leads(niche="SaaS", country="US", count=5)
    print(leads)
