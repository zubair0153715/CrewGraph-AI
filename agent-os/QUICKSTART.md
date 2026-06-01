# Quick Start Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional, for easy setup)
- API Keys for LLM providers (OpenAI/OpenRouter/Groq)

## Option 1: Docker Setup (Recommended)

### 1. Clone and Setup

```bash
cd agent-os
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Qdrant vector database  
- Backend API (port 8000)
- Frontend dashboard (port 3000)

### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option 2: Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Start PostgreSQL and Qdrant (use Docker or install locally)
docker run -d --name postgres -e POSTGRES_PASSWORD=agentos_password -e POSTGRES_USER=agentos -e POSTGRES_DB=agentos -p 5432:5432 postgres:15-alpine
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Start development server
npm run dev
```

## First Steps

### 1. Create an Account

- Go to http://localhost:3000
- Click "Create Account"
- Fill in your details

### 2. Create Your First Agent

- Login to the dashboard
- Click "Create Agent"
- Choose a template or create custom:
  - **Research Agent**: For web research and analysis
  - **Content Agent**: For writing blogs, scripts, etc.
  - **Task Runner**: General purpose assistant

### 3. Run Your First Task

- Click on an agent card
- Click "Run Task"
- Enter your task description, e.g.:
  - "Find the latest trends in AI for 2024"
  - "Write a blog post about machine learning"
  - "Research competitors in the SaaS market"

## Configuration

### Environment Variables

**Backend (.env):**
```env
# Database
DATABASE_URL=postgresql://agentos:agentos_password@localhost:5432/agentos

# Vector DB
QDRANT_URL=http://localhost:6333

# LLM Provider (choose one)
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key

# JWT Secret
JWT_SECRET_KEY=change-this-to-random-string
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Available Features (MVP)

✅ User authentication (register/login)
✅ Create custom AI agents
✅ 3 pre-built agent templates
✅ Web search tool (DuckDuckGo)
✅ Task execution with agents
✅ Agent memory system (Qdrant)
✅ Task history and status tracking

## Troubleshooting

### Backend won't start
- Check if PostgreSQL is running: `docker ps | grep postgres`
- Verify database connection in `.env`
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Clear browser cache

### Agent tasks failing
- Verify LLM API key is set correctly
- Check API quota/billing
- Review backend logs for errors

## Next Steps

Once you're comfortable with the MVP:

1. **Add more tools**: YouTube API, code execution, email automation
2. **Multi-agent workflows**: Chain multiple agents together
3. **Advanced memory**: Improve RAG and context management
4. **Deployment**: Deploy to production (Railway, Render, AWS)
5. **Monetization**: Add Stripe for subscriptions

## Support

- API Documentation: http://localhost:8000/docs
- GitHub Issues: [Your repo]
- Discord: [Your community link]

---

**Ready to build?** 🚀

Start by creating your first agent and giving it a task!
