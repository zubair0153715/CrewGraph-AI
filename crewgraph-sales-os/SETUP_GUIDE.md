# 🚀 CrewGraph Sales OS - Complete Setup Guide

> Step-by-step guide to set up and run your AI Sales Automation Platform for **FREE**

---

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for frontend)
- Git
- A free Groq API key

---

## 🎯 Step 1: Get FREE API Keys

### 1. Groq API Key (LLM - FREE)
1. Visit: https://console.groq.com
2. Sign up with Google/GitHub
3. Click "Create API Key"
4. Copy the key (starts with `gsk_...`)
5. **Important:** This gives you FREE access to Llama3 70B model

### 2. Neon Database (PostgreSQL - FREE tier)
*Optional - SQLite works fine for local dev*
1. Visit: https://neon.tech
2. Sign up
3. Create new project
4. Copy connection string

### 3. Qdrant Cloud (Vector DB - FREE tier)
*Optional - skip for MVP*
1. Visit: https://cloud.qdrant.io
2. Sign up
3. Create free cluster
4. Copy URL and API key

---

## 💻 Step 2: Clone & Setup Project

```bash
# Navigate to project
cd /workspace/crewgraph-sales-os

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

---

## 📦 Step 3: Install Dependencies

```bash
# Install Python packages
pip install -r backend/requirements.txt

# Install Playwright browsers (for web scraping)
playwright install
```

---

## ⚙️ Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

### Minimum Configuration (Required)

```env
GROQ_API_KEY=gsk_your_actual_key_here
DATABASE_URL=sqlite:///./data/crewgraph.db
SECRET_KEY=my-super-secret-key-change-this
DEBUG=True
```

### Optional Configuration (For Email Sending)

```env
# Gmail OAuth2 (recommended for production)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret

# OR SMTP (easier for testing)
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

---

## 🗄️ Step 5: Initialize Database

```bash
# Create data directory
mkdir -p data

# The database will auto-initialize when you start the server
# Or manually initialize:
cd backend
python -c "from app.database import init_db; init_db()"
```

---

## 🚀 Step 6: Run Backend Server

```bash
# From backend directory
cd backend

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## 🧪 Step 7: Test API

### Option 1: Swagger UI (Easiest)
Visit: http://localhost:8000/docs

1. Click `/auth/register` endpoint
2. Try it out with:
   ```json
   {
     "email": "test@example.com",
     "password": "test123",
     "full_name": "Test User",
     "organization_name": "Test Org"
   }
   ```
3. Copy the access token from response
4. Use token in Authorization header for other endpoints

### Option 2: cURL Commands

```bash
# Register new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'

# Save the token from response
TOKEN="your_access_token_here"

# Find leads
curl -X POST http://localhost:8000/api/leads/find \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "niche": "SaaS",
    "country": "US",
    "count": 5
  }'

# Get analytics
curl http://localhost:8000/api/analytics \
  -H "Authorization: Bearer $TOKEN"
```

### Option 3: Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "database": "connected",
  "llm": "configured",
  "vector_db": "not configured"
}
```

---

## 🖥️ Step 8: Setup Frontend (Optional)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: http://localhost:3000

---

## 🐳 Step 9: Run with Docker (Alternative)

```bash
# Build and run all services
docker-compose up --build

# Or run in background
docker-compose up -d
```

Services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432
- Qdrant: localhost:6333

---

## 🎯 Step 10: First Campaign

### Via API:

```bash
# 1. Create campaign
curl -X POST http://localhost:8000/api/campaigns \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "SaaS Outreach",
    "target_niche": "SaaS",
    "target_country": "US",
    "description": "Finding SaaS companies for outreach"
  }'

# 2. Find leads for campaign
curl -X POST http://localhost:8000/api/leads/find \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "niche": "SaaS",
    "country": "US",
    "count": 10
  }'

# 3. View leads
curl http://localhost:8000/api/leads \
  -H "Authorization: Bearer $TOKEN"

# 4. Run campaign
curl -X POST http://localhost:8000/api/campaigns/1/run \
  -H "Authorization: Bearer $TOKEN"
```

### Via Swagger UI:
1. Go to http://localhost:8000/docs
2. Authenticate with your token
3. Use the interactive interface to test all endpoints

---

## 🔧 Troubleshooting

### Issue: "GROQ_API_KEY not configured"
**Solution:** Make sure `.env` file exists and has valid key:
```bash
cat .env | grep GROQ
```

### Issue: Database errors
**Solution:** 
```bash
# Delete old database
rm data/crewgraph.db

# Reinitialize
cd backend
python -c "from app.database import init_db; init_db()"
```

### Issue: Port already in use
**Solution:** Use different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: Module not found
**Solution:** 
```bash
# Make sure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 What You Have Now

✅ **Working Backend API** with:
- User authentication (register/login)
- Lead generation using AI agents
- Campaign management
- CRM database
- Analytics dashboard

✅ **AI Agents Ready**:
- Lead Finder Agent (finds companies)
- Prospect Qualifier (scores leads)
- Company Researcher (analyzes companies)
- Cold Email Writer (generates emails)
- Follow-up Agent (creates sequences)
- Meeting Booker (detects interest)

✅ **Database Schema**:
- Users & Organizations
- Leads with status tracking
- Campaigns
- Emails with tracking
- Interactions history

✅ **API Endpoints**:
- `/auth/register` - Create account
- `/auth/login` - Get token
- `/api/leads/find` - AI-powered lead generation
- `/api/leads` - View all leads
- `/api/campaigns` - Manage campaigns
- `/api/analytics` - Dashboard metrics

---

## 🎓 Next Steps

### Day 1-2: Test Core Features
- [ ] Register a test user
- [ ] Find 10 leads in your niche
- [ ] Review leads in database
- [ ] Create a campaign

### Day 3-4: Add More Agents
- [ ] Implement Qualifier Agent
- [ ] Add Cold Email Generator
- [ ] Create email templates

### Day 5-6: Email Integration
- [ ] Set up Gmail API or SMTP
- [ ] Test sending emails
- [ ] Add open/reply tracking

### Day 7: Launch MVP
- [ ] Deploy to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Get first real user

---

## 💡 Pro Tips

1. **Start Small**: Don't try to build everything at once
2. **Manual Review**: Review AI-generated emails before sending
3. **Warm Up**: Start with 10-20 emails/day, gradually increase
4. **Track Everything**: Monitor open rates, reply rates, bounces
5. **Iterate Fast**: Get feedback, improve, repeat

---

## 🆘 Need Help?

- Check logs: `tail -f logs/app.log`
- API Docs: http://localhost:8000/docs
- GitHub Issues: Report bugs
- Discord: Join community (coming soon)

---

## 🚀 You're Ready!

Your AI Sales Automation Platform is now running locally. Start finding leads and automating your outreach!

**Remember:** Perfect system mat banao — working MVP banao! 🎯
