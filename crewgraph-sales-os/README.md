# 🚀 CrewGraph Sales OS - Complete AI Sales Automation Platform

> **AI-powered sales workforce that finds leads, qualifies prospects, sends personalized emails, books meetings, and closes deals automatically.**

## 🎯 What It Does

CrewGraph Sales OS automates your entire sales pipeline:

1. **Find Leads** - Scrape LinkedIn, Google Maps, Crunchbase, company websites
2. **Qualify Prospects** - AI filters leads based on budget, fit, and intent
3. **Research Companies** - Deep analysis of pain points and needs
4. **Write Cold Emails** - Hyper-personalized outreach sequences
5. **Send Emails** - Gmail/SMTP integration with sending queue
6. **Auto Follow-ups** - Smart follow-up sequences
7. **Book Meetings** - Detect interest & schedule calendar invites
8. **CRM Management** - Track lead status from New → Closed
9. **ROI Dashboard** - Real-time analytics on conversions

---

## 🤖 AI Agent Team (8 Specialized Agents)

### 1. 🔍 Lead Finder Agent
**Sources:** LinkedIn, Google Maps, Crunchbase, Apollo, Company Directories
- Extract: Company name, website, email, industry, size, location
- Filter by niche, country, revenue, employee count

### 2. ✅ Prospect Qualification Agent
**Scoring System:**
- Budget potential (High/Medium/Low)
- Company fit score (0-100)
- Intent signals (website traffic, hiring, tech stack)
- **Output:** Qualified vs Unqualified leads

### 3. 📊 Company Research Agent
**Deep Analysis:**
- Recent news & funding
- Tech stack detection
- Pain points identification
- Competitor analysis
- Decision makers mapping

### 4. ✍️ Cold Email Agent
**Personalization Engine:**
- Generate 5 email variations
- Tone adjustment (formal/casual)
- A/B testing subject lines
- Spam score optimization

### 5. 📧 Outreach Engine (Not just an agent)
**Email Sending:**
- Gmail API integration
- SMTP support
- Daily sending limits
- Warm-up schedules
- Bounce handling
- Unsubscribe management

### 6. 🔄 Follow-up Agent
**Smart Sequences:**
- 3-5 email follow-up chains
- Time-based triggers
- Reply detection
- Variation generation to avoid spam

### 7. 📅 Meeting Booking Agent
**Conversion Focus:**
- Detect interested replies
- Suggest calendar slots
- Send calendar invites
- Meeting prep summaries
- CRM status update → "Meeting Booked"

### 8. 💼 Sales Strategy Agent
**Closing Intelligence:**
- Pricing recommendations
- Objection handling scripts
- Negotiation tips
- Close probability scoring

### 9. 💾 Memory Agent
**Long-term Learning:**
- Store all lead interactions
- Campaign history
- Email performance data
- Learn from successful patterns

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                 User Dashboard                       │
│  (Next.js + Tailwind)                               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              API Gateway (FastAPI)                   │
│  - Authentication                                   │
│  - Rate Limiting                                    │
│  - Request Validation                               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│            Orchestrator (Brain)                      │
│  - Task routing                                     │
│  - Workflow management                              │
│  - Error handling                                   │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┬──────────────┬──────────┐
        ▼                 ▼              ▼          ▼
   ┌─────────┐      ┌──────────┐   ┌────────┐  ┌─────────┐
   │  Lead   │      │ Research │   │ Email  │  │ Meeting │
   │ Finder  │      │  Agent   │   │ Agent  │  │ Booking │
   └─────────┘      └──────────┘   └────────┘  └─────────┘
        │                 │              │          │
        └─────────────────┴──────────────┴──────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    CRM Database        │
              │  (PostgreSQL + Qdrant) │
              └───────────────────────┘
```

---

## 🗄️ Database Schema

### Users Table
```sql
id, email, password_hash, organization_id, plan, created_at
```

### Organizations Table
```sql
id, name, subscription_plan, usage_limits, api_keys
```

### Leads Table
```sql
id, org_id, company_name, website, email, industry, 
country, employee_count, revenue, qualification_score, 
status (New/Contacted/Replied/Interested/Meeting/Closed/Lost),
source, created_at
```

### Campaigns Table
```sql
id, org_id, name, target_niche, country, status, 
total_leads, emails_sent, replies, meetings_booked, 
created_at
```

### Emails Table
```sql
id, lead_id, campaign_id, content, subject, type 
(cold/follow-up-1/follow-up-2...), status (sent/opened/replied), 
sent_at, opened_at, replied_at
```

### Interactions Table
```sql
id, lead_id, type (email/reply/meeting), content, timestamp
```

---

## 📊 ROI Dashboard Metrics

Real-time analytics showing:

- **Leads Generated** (Total, This Week, This Month)
- **Emails Sent** (Daily limit, Total sent)
- **Open Rate** (%)
- **Reply Rate** (%)
- **Meetings Booked** (Count, Conversion %)
- **Deals Closed** (Revenue tracked)
- **ROI** = (Revenue - Cost) / Cost × 100

---

## 🔧 Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Agent Framework:** CrewAI + LangGraph
- **Database:** PostgreSQL (Supabase/Neon free tier)
- **Vector DB:** Qdrant (for memory & semantic search)
- **ORM:** SQLAlchemy + Alembic migrations
- **Auth:** JWT tokens + OAuth2
- **Email:** Gmail API + SMTP (SendGrid/Mailgun)
- **Scheduler:** Celery + Redis (for email queues)

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI:** Tailwind CSS + Shadcn/ui
- **State:** Zustand
- **Charts:** Recharts
- **Tables:** TanStack Table

### AI/LLM
- **Primary:** Groq (Llama3 70B) - FREE
- **Backup:** OpenAI GPT-4, Claude 3
- **Local:** Ollama (for offline use)
- **Embeddings:** sentence-transformers

### Tools & Integrations
- **Lead Sources:** 
  - LinkedIn Scraper (Playwright)
  - Google Maps API
  - Crunchbase API
  - Clearbit API
  - Hunter.io (email finder)
- **Email:** Gmail API, SendGrid, Mailgun
- **Calendar:** Google Calendar API, Calendly
- **CRM:** Built-in + HubSpot/Salesforce sync (future)

### DevOps
- **Container:** Docker + Docker Compose
- **Hosting:** Vercel (frontend), Railway/Render (backend)
- **CI/CD:** GitHub Actions
- **Monitoring:** Sentry + Prometheus

---

## 🚀 Quick Start (FREE Setup)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)
- Free API keys (see below)

### Step 1: Get FREE API Keys

1. **Groq (LLM):** https://console.groq.com → Create API Key
2. **Neon (PostgreSQL):** https://neon.tech → Create project
3. **Qdrant (Vector DB):** https://cloud.qdrant.io → Free cluster
4. **Gmail (Optional):** Enable Gmail API in Google Cloud Console

### Step 2: Clone & Install

```bash
cd /workspace/crewgraph-sales-os

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Step 3: Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit .env with your keys
GROQ_API_KEY=your_groq_key_here
DATABASE_URL=postgresql://user:pass@host:5432/dbname
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_key
GMAIL_CLIENT_ID=optional_for_email_sending
GMAIL_CLIENT_SECRET=optional
```

### Step 4: Run Locally

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit: http://localhost:3000

### Step 5: Test API

```bash
# Find leads
curl -X POST http://localhost:8000/api/leads/find \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"niche": "SaaS", "country": "US", "count": 10}'

# Run full campaign
curl -X POST http://localhost:8000/api/campaigns/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "SaaS Outreach", "niche": "Marketing Tools"}'
```

---

## 💰 Monetization Models

### Model 1: Freelance Service (FAST MONEY)
**Offer:** "I'll build & run your AI sales automation"
- Charge: $500 - $2000 per client
- Delivery time: 1-2 weeks
- Platforms: Upwork, Fiverr, LinkedIn

### Model 2: Agency Model (RECURRING)
**Service:** Monthly lead gen + outreach management
- Charge: $1000 - $5000/month per client
- Includes: Lead sourcing, email campaigns, meeting booking
- Manage 5-10 clients = $5k-$50k/month

### Model 3: SaaS Platform (SCALE)
**Subscription Tiers:**
- **Starter:** $29/month (500 leads, 1000 emails)
- **Pro:** $99/month (2000 leads, 5000 emails, advanced analytics)
- **Agency:** $299/month (Unlimited, white-label, API access)
- **Enterprise:** Custom (On-premise, custom integrations)

### Model 4: Marketplace (FUTURE)
- Sell pre-built agent templates
- Share revenue with creators
- Industry-specific playbooks

---

## 📁 Project Structure

```
crewgraph-sales-os/
├── README.md                  # You are here
├── SETUP_GUIDE.md             # Detailed setup instructions
├── BUILD_PLAN.md              # 7-day MVP roadmap
├── .env.example               # Environment template
├── .gitignore
├── docker-compose.yml         # Full stack deployment
│
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Settings & env vars
│   │   ├── database.py        # DB connection
│   │   ├── auth.py            # JWT authentication
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── lead_finder.py       # 🔍 Lead scraping
│   │   │   ├── qualifier.py         # ✅ Lead scoring
│   │   │   ├── researcher.py        # 📊 Company analysis
│   │   │   ├── cold_email.py        # ✍️ Email writing
│   │   │   ├── follow_up.py         # 🔄 Follow-up sequences
│   │   │   ├── meeting_booking.py   # 📅 Calendar integration
│   │   │   ├── sales_strategy.py    # 💼 Closing intelligence
│   │   │   └── memory.py            # 💾 Long-term storage
│   │   │
│   │   ├── orchestrator/
│   │   │   ├── brain.py             # Main workflow engine
│   │   │   ├── router.py            # Task distribution
│   │   │   └── workflows.py         # Pre-built pipelines
│   │   │
│   │   ├── tools/
│   │   │   ├── linkedin_scraper.py
│   │   │   ├── google_maps.py
│   │   │   ├── email_sender.py
│   │   │   ├── calendar_manager.py
│   │   │   └── crm_sync.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── lead.py
│   │   │   ├── campaign.py
│   │   │   ├── email.py
│   │   │   └── interaction.py
│   │   │
│   │   └── api/
│   │       ├── routes/
│   │       │   ├── auth.py
│   │       │   ├── leads.py
│   │       │   ├── campaigns.py
│   │       │   ├── emails.py
│   │       │   ├── analytics.py
│   │       │   └── settings.py
│   │       └── schemas/
│   │           ├── request.py
│   │           └── response.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   │   ├── page.tsx       # Dashboard home
│   │   │   ├── login/page.tsx
│   │   │   ├── leads/page.tsx
│   │   │   ├── campaigns/page.tsx
│   │   │   ├── analytics/page.tsx
│   │   │   └── settings/page.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── ui/            # Reusable UI components
│   │   │   ├── LeadTable.tsx
│   │   │   ├── CampaignBuilder.tsx
│   │   │   ├── EmailPreview.tsx
│   │   │   ├── AnalyticsChart.tsx
│   │   │   └── MeetingCalendar.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts         # API client
│   │   │   ├── utils.ts
│   │   │   └── constants.ts
│   │   │
│   │   └── styles/
│   │       └── globals.css
│   │
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── data/                      # Local SQLite (dev mode)
└── docs/                      # Documentation
    ├── api.md
    ├── agents.md
    └── deployment.md
```

---

## 🎯 MVP Roadmap (7 Days)

### Day 1: Foundation
- [ ] Project setup
- [ ] Database schema
- [ ] Auth system
- [ ] Basic API structure

### Day 2: Lead Finder
- [ ] LinkedIn scraper
- [ ] Google Maps integration
- [ ] Lead storage in DB
- [ ] API endpoint: `/api/leads/find`

### Day 3: Research + Qualification
- [ ] Company research agent
- [ ] Qualification scoring
- [ ] Enrichment pipeline

### Day 4: Email Engine
- [ ] Cold email generator
- [ ] Gmail/SMTP integration
- [ ] Email sending queue
- [ ] Template system

### Day 5: Orchestrator
- [ ] Workflow engine
- [ ] Agent coordination
- [ ] Error handling
- [ ] Campaign runner

### Day 6: Frontend Dashboard
- [ ] Login/Register
- [ ] Lead table view
- [ ] Campaign builder
- [ ] Basic analytics

### Day 7: Testing & Launch
- [ ] End-to-end test
- [ ] Bug fixes
- [ ] Deploy to production
- [ ] First customer demo

---

## ⚠️ Important Considerations

### Legal & Compliance
- **GDPR:** Respect EU data protection laws
- **CAN-SPAM:** Include unsubscribe links
- **LinkedIn ToS:** Use official API or respect rate limits
- **Data Privacy:** Never store sensitive personal data without consent

### Best Practices
- Start with **manual email review** before auto-sending
- Implement **daily sending limits** (50-100/day initially)
- Add **spam score checking** before sending
- Use **domain warm-up** for new email accounts
- Monitor **bounce rates** closely (<5% is good)

### Scaling Tips
- Use **separate domains** for high-volume sending
- Implement **IP rotation** for scraping
- Cache **frequently accessed data**
- Use **message queues** for async tasks
- Add **rate limiting** on all APIs

---

## 🤝 Support & Community

- **GitHub Issues:** Report bugs & feature requests
- **Discord:** Join our community (coming soon)
- **Documentation:** https://docs.crewgraph.ai
- **Email:** support@crewgraph.ai

---

## 📄 License

MIT License - Feel free to use for commercial projects.

---

## 🚀 Ready to Build?

```bash
# Get started in 5 minutes
git clone <repo-url>
cd crewgraph-sales-os
./setup.sh  # Automated setup script

# Or follow SETUP_GUIDE.md for manual installation
```

**Remember:** Perfect system mat banao — working MVP banao! 🎯

Start with 4 core features:
1. Lead Finder
2. Research Agent
3. Email Generator
4. CRM Storage

Then iterate based on real user feedback.

---

**Built with ❤️ for sales teams who want to close more deals with less effort.**
