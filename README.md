# 🧠 CrewGraph Sales OS - AI Sales Automation System

> **AI system jo businesses ke liye leads find kare, outreach kare aur sales pipeline automate kare.**

## 🎯 Vision
Automate lead generation, company research, cold email writing, aur follow-ups using multi-agent AI system.

## 🚀 Features
- 🔍 **Lead Finder Agent**: Web search + scraping se leads dhundhta hai
- 📊 **Research Agent**: Company analysis aur pain points identify karta hai
- ✉️ **Cold Email Agent**: Personalized emails generate karta hai
- 🔁 **Follow-up Agent**: Automatic follow-up sequences manage karta hai
- 📈 **Sales Strategy Agent**: Pricing aur conversion strategy suggest karta hai
- 💾 **Memory Agent**: Leads aur campaign history store karta hai

## 🏗️ Architecture
```
User Input → Orchestrator Agent → Agent Router → Specialized Agents → Output
```

## 💰 Use Cases
1. **Freelancing**: $100-$1000 per client setup
2. **Agency**: $500-$5000/month recurring revenue
3. **SaaS**: $19-$99/month subscription model

## 🛠️ Tech Stack
- **Backend**: Python FastAPI
- **Agents**: CrewAI + LangGraph
- **LLM**: Groq (Free) / OpenAI / Ollama
- **Database**: PostgreSQL + Qdrant (Vector DB)
- **Frontend**: Next.js + Tailwind CSS
- **Tools**: Playwright, Docker Sandbox

## 📁 Project Structure
```
crewgraph-sales-os/
├── backend/
│   ├── app/
│   │   ├── agents/          # All AI agents
│   │   ├── tools/           # Web scraping, email tools
│   │   ├── models/          # Database models
│   │   └── orchestrator/    # Main brain logic
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/      # React components
│       └── pages/           # Dashboard pages
└── data/                    # Local storage for MVP
```

## 🚀 Quick Start (Free Setup)
1. Get free API keys: Groq, Neon (PostgreSQL), Qdrant
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Set environment variables in `.env`
4. Run: `python backend/app/main.py`
5. Access dashboard at `http://localhost:3000`

## 📈 MVP Build Plan (7 Days)
- Day 1: Project setup & base structure
- Day 2: Lead Finder Agent
- Day 3: Company Research Agent
- Day 4: Email Generator Agent
- Day 5: Orchestrator logic
- Day 6: Simple UI dashboard
- Day 7: Full workflow test

## 💡 First Customer Strategy
Offer on Fiverr/Upwork: *"I will automate your lead generation and outreach using AI agents"*

---
**Remember**: Perfect system mat banao — working MVP banao! 🚀
