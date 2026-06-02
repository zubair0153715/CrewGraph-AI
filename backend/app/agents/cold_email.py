"""
Cold Email Agent - Generates personalized cold emails and follow-up sequences
"""

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class ColdEmailAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.agent = Agent(
            role='Cold Email Copywriter',
            goal='Write high-converting personalized cold emails that get responses',
            backstory="""You are a world-class copywriter specializing in B2B cold emails.
            Your emails have 40%+ open rates and 15%+ response rates.
            You know how to craft compelling subject lines, personalize at scale,
            and create urgency without being pushy.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_email(self, company_name: str, industry: str, pain_point: str = "", tone: str = "professional"):
        """
        Generate personalized cold email with follow-up sequence
        """
        task = Task(
            description=f"""Write a cold email for {company_name} in the {industry} industry.
            
            Pain point to address: {pain_point if pain_point else 'general business automation'}
            Tone: {tone}
            
            Deliverables:
            1. Compelling subject line (under 50 characters)
            2. Email body (150-200 words max)
            3. Clear call-to-action
            4. 3 follow-up emails (each shorter than the previous)
            
            Best practices:
            - Personalize with company name
            - Focus on their pain points
            - Keep it concise
            - Include social proof if possible
            - End with a soft CTA""",
            expected_output="Complete email sequence with subject line, body, and 3 follow-ups",
            agent=self.agent
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=2
        )
        
        result = crew.kickoff()
        return result
    
    def generate_sequence(self, leads: list, niche: str):
        """
        Generate email sequence for multiple leads
        """
        emails = []
        for lead in leads:
            email = self.generate_email(
                company_name=lead.get('company_name', ''),
                industry=lead.get('industry', niche),
                pain_point=lead.get('pain_point', ''),
                tone='professional'
            )
            emails.append(email)
        return emails

# Example usage
if __name__ == "__main__":
    email_agent = ColdEmailAgent()
    email = email_agent.generate_email(
        company_name="TechCorp Inc",
        industry="SaaS",
        pain_point="manual lead generation is time-consuming"
    )
    print(email)
