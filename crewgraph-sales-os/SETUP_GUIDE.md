# CrewGraph Sales OS - Setup Guide (FREE)

## 🚀 Quick Start - $0 Cost Setup

### Step 1: Get FREE API Keys

#### 1. Groq API (Free LLM)
1. Visit: https://console.groq.com
2. Sign up with Google/GitHub
3. Create API Key
4. Copy the key

#### 2. Neon Database (Free PostgreSQL)
1. Visit: https://neon.tech
2. Sign up
3. Create new project
4. Copy connection string

#### 3. Qdrant Cloud (Free Vector DB - Optional for MVP)
1. Visit: https://cloud.qdrant.io
2. Sign up
3. Create free cluster (1GB free)
4. Copy URL and API key

---

### Step 2: Clone & Setup Project

```bash
# Navigate to project
cd /workspace/crewgraph-sales-os

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Copy environment file
cp .env.example .env
```

---

### Step 3: Configure Environment

Edit `.env` file with your keys:

```bash
# Only GROQ_API_KEY is required for MVP!
GROQ_API_KEY=gsk_your_actual_key_here

# Optional for later:
DATABASE_URL=postgresql://...
QDRANT_URL=...
```

---

### Step 4: Run Backend

```bash
# Start FastAPI server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs for API documentation

---

### Step 5: Test Agents

```bash
# Test Lead Finder Agent
python backend/app/agents/lead_finder.py

# Test Email Agent
python backend/app/agents/cold_email.py

# Test Orchestrator
python backend/app/orchestrator/brain.py
```

---

## 🎯 MVP Features (Working Now)

### ✅ Available Endpoints:

1. **GET /** - Health check
2. **POST /api/find-leads** - Find leads by niche
3. **POST /api/generate-emails** - Generate cold emails
4. **POST /api/run-campaign** - Full campaign automation
5. **GET /api/agents/status** - Check agent status

### Example API Calls:

#### Find Leads:
```bash
curl -X POST http://localhost:8000/api/find-leads \
  -H "Content-Type: application/json" \
  -d '{"niche": "SaaS", "country": "US", "count": 5}'
```

#### Run Campaign:
```bash
curl -X POST http://localhost:8000/api/run-campaign \
  -H "Content-Type: application/json" \
  -d '{"niche": "E-commerce", "country": "UK"}'
```

---

## 💰 Monetization Options

### Option 1: Freelancing (Fast Money)
- Offer on Fiverr/Upwork
- Price: $100-$1000 per setup
- Service: "AI Lead Generation System"

### Option 2: Agency Model
- Monthly clients
- Price: $500-$5000/month
- Service: Done-for-you lead gen

### Option 3: SaaS Product
- Subscription model
- Price: $19/$49/$99 per month
- Platform: Self-serve dashboard

---

## 📁 Project Structure

```
crewgraph-sales-os/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── agents/
│   │   │   ├── lead_finder.py   # Lead generation
│   │   │   ├── research.py      # Company research
│   │   │   └── cold_email.py    # Email generation
│   │   └── orchestrator/
│   │       └── brain.py         # Workflow orchestration
│   └── requirements.txt
├── frontend/                    # Next.js (to be built)
├── data/                        # Local storage
├── .env                         # Your API keys
├── .env.example                # Template
└── README.md                   # This guide
```

---

## 🔧 Troubleshooting

### Issue: Groq API Error
- Check API key is correct
- Ensure no extra spaces in .env
- Verify internet connection

### Issue: Module Not Found
```bash
pip install -r backend/requirements.txt --upgrade
```

### Issue: Port Already in Use
```bash
# Change port in main.py or kill process
lsof -ti:8000 | xargs kill
```

---

## 🎓 Next Steps

1. ✅ Test all agents locally
2. 📝 Build simple frontend (Next.js)
3. 🗄️ Add database integration
4. 🌐 Deploy to free hosting (Render/Vercel)
5. 💼 Get first client on Fiverr

---

## 🆘 Need Help?

Check these resources:
- Groq Docs: https://console.groq.com/docs
- CrewAI Docs: https://docs.crewai.com
- FastAPI Docs: http://localhost:8000/docs

**Remember**: Perfect system mat banao — working MVP banao! 🚀
