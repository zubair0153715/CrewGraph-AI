# AgentOS - AI Agent Operating System

A scalable multi-agent AI platform for automating real business tasks.

## 🚀 Features

- **Multi-Agent System**: Create and manage AI agents with specific roles
- **Task Orchestration**: Automated workflow execution using CrewAI + LangGraph
- **Browser Automation**: Web scraping and automation capabilities
- **Code Execution**: Safe sandboxed code execution
- **Memory System**: Persistent agent memory with Qdrant/ChromaDB
- **YouTube Automation**: Video creation and upload workflows
- **Dashboard**: Modern Next.js frontend for agent management

## 🏗️ Architecture

```
agent-os/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core configuration
│   │   ├── agents/   # Agent definitions (CrewAI)
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic
│   │   └── utils/    # Utilities
│   └── tests/
├── frontend/         # Next.js dashboard
├── docker/           # Docker configurations
└── docs/
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Python web framework
- **CrewAI** - Agent orchestration
- **LangGraph** - Workflow management
- **PostgreSQL** - Primary database
- **Qdrant** - Vector database for memory
- **Docker** - Sandboxed execution

### Frontend
- **Next.js 14** - React framework
- **TailwindCSS** - Styling
- **TypeScript** - Type safety

### AI Providers
- OpenRouter / Groq / OpenAI

## 📦 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker
- PostgreSQL
- Qdrant (or use Docker)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your backend URL
npm run dev
```

### Docker Setup

```bash
docker-compose up -d
```

## 🤖 Available Agents (MVP)

1. **Research Agent** - Internet research and trend analysis
2. **Content Agent** - Script, blog, and SEO content creation
3. **Task Runner Agent** - General task execution

## 🔧 Configuration

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/agentos
QDRANT_URL=http://localhost:6333
OPENROUTER_API_KEY=your_key_here
BROWSER_USE_API_KEY=your_key_here
```

## 💰 Monetization Ready

- Subscription tiers (Basic/Pro/Agency)
- Usage-based billing
- Agent marketplace support

## 📄 License

MIT

## 🎯 Roadmap

- [x] MVP: Basic agent system
- [ ] YouTube automation
- [ ] Code execution sandbox
- [ ] Advanced memory system
- [ ] Agent marketplace
- [ ] Team collaboration
