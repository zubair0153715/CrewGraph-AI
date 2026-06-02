"""
Company Research Agent - Analyzes companies to find pain points and personalization angles
"""

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.5,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.agent = Agent(
            role='Business Research Analyst',
            goal='Deep dive into companies to uncover pain points, needs, and personalization opportunities',
            backstory="""You are a seasoned business analyst with expertise in market research.
            You can quickly understand a company's business model, identify their challenges,
            and find the perfect angles for personalized outreach.
            You excel at connecting company information to potential solutions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def research_company(self, company_name: str, website: str, industry: str):
        """
        Research a specific company to find pain points and personalization data
        """
        task = Task(
            description=f"""Research {company_name} ({website}) in the {industry} industry.
            
            Provide:
            1. Company overview (size, focus, target market)
            2. Likely pain points related to sales/lead generation
            3. Current challenges in their industry
            4. Personalization hooks (recent news, growth, funding, etc.)
            5. Decision makers to target
            6. Why they would need AI automation
            
            Be specific and actionable. Avoid generic statements.""",
            expected_output="Detailed company research report with pain points and personalization angles",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=2
        )
        
        result = crew.kickoff()
        return result
    
    def batch_research(self, leads: list):
        """
        Research multiple companies
        """
        results = []
        for lead in leads:
            research = self.research_company(
                company_name=lead.get('company_name', ''),
                website=lead.get('website', ''),
                industry=lead.get('industry', '')
            )
            results.append({
                'lead': lead,
                'research': research
            })
        return results

# Example usage
if __name__ == "__main__":
    researcher = ResearchAgent()
    research = researcher.research_company(
        company_name="Stripe",
        website="https://stripe.com",
        industry="Fintech"
    )
    print(research)
