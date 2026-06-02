# 📅 7-Day MVP Build Plan - CrewGraph Sales OS

> **Goal:** Go from zero to working MVP in 7 days
> **Rule:** Perfect system mat banao — working MVP banao!

---

## 🎯 MVP Scope (Minimum Viable Product)

**Core Features Only:**
1. ✅ User Registration/Login
2. ✅ Lead Finder Agent (AI-powered)
3. ✅ CRM Database (store leads)
4. ✅ Campaign Management
5. ✅ Basic Analytics Dashboard
6. ⏳ Cold Email Generator (basic)
7. ⏳ Manual email sending (no automation yet)

**Out of Scope for MVP:**
- ❌ Automatic email sending
- ❌ Follow-up sequences
- ❌ Meeting booking
- ❌ Advanced analytics
- ❌ Multi-user teams
- ❌ Payment integration

---

## 📆 Day-by-Day Plan

### **Day 1: Foundation & Setup** ✅

**Goals:**
- [x] Project structure setup
- [x] Database models created
- [x] Environment configuration
- [x] Basic FastAPI server running

**Tasks:**
```bash
# 1. Create project structure
mkdir -p backend/app/{agents,orchestrator,tools,models,database}
mkdir -p frontend/src/{components,pages,styles}

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure .env file
cp .env.example .env
# Edit with your Groq API key

# 4. Initialize database
python -c "from app.database import init_db; init_db()"

# 5. Test server
uvicorn app.main:app --reload
```

**Deliverables:**
- ✅ Working FastAPI server
- ✅ Database initialized
- ✅ Health check endpoint working
- ✅ `.env` configured

**Time Estimate:** 4-6 hours

---

### **Day 2: Authentication System** ✅

**Goals:**
- [ ] User registration
- [ ] User login
- [ ] JWT token authentication
- [ ] Protected routes

**Tasks:**
```python
# Implement these endpoints:
POST /auth/register  # Create account
POST /auth/login     # Get access token
GET  /auth/me        # Get current user
```

**Test Cases:**
1. Register new user → Get token
2. Login with credentials → Get token
3. Access protected route with token → Success
4. Access protected route without token → 401 error

**Frontend (Optional):**
- Simple login/register page
- Store token in localStorage

**Deliverables:**
- ✅ Working auth system
- ✅ Users can register/login
- ✅ Token-based security

**Time Estimate:** 4-5 hours

---

### **Day 3: Lead Finder Agent** 🔍

**Goals:**
- [ ] Lead Finder Agent implementation
- [ ] AI-powered lead generation
- [ ] Save leads to database

**Tasks:**

**1. Create Agent:**
```python
# backend/app/agents/lead_finder.py
class LeadFinderAgent:
    def find_leads(niche, country, count):
        # Use CrewAI + Groq LLM
        # Return list of companies
```

**2. Create API Endpoint:**
```python
POST /api/leads/find
{
  "niche": "SaaS",
  "country": "US",
  "count": 10
}
```

**3. Test:**
```bash
curl -X POST http://localhost:8000/api/leads/find \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"niche": "SaaS", "country": "US", "count": 5}'
```

**Expected Output:**
```json
[
  {
    "company_name": "Example Corp",
    "website": "example.com",
    "email": "contact@example.com",
    "industry": "SaaS",
    "country": "US"
  }
]
```

**Deliverables:**
- ✅ Lead Finder Agent working
- ✅ Can find 10+ leads in any niche
- ✅ Leads saved to database

**Time Estimate:** 6-8 hours

---

### **Day 4: CRM & Lead Management** 💾

**Goals:**
- [ ] View all leads
- [ ] Filter leads by status
- [ ] Update lead status
- [ ] Delete leads

**API Endpoints:**
```python
GET    /api/leads              # List all leads
GET    /api/leads/{id}         # Get single lead
PUT    /api/leads/{id}         # Update lead
DELETE /api/leads/{id}         # Delete lead
PATCH  /api/leads/{id}/status  # Update status only
```

**Lead Statuses:**
- `new` → `contacted` → `replied` → `interested` → `meeting_booked` → `closed`

**Frontend (Optional):**
- Lead table view
- Filter by status
- Search by company name

**Deliverables:**
- ✅ Full CRUD for leads
- ✅ Status tracking
- ✅ Lead management UI (if time permits)

**Time Estimate:** 5-6 hours

---

### **Day 5: Campaign System** 📧

**Goals:**
- [ ] Create campaigns
- [ ] Link leads to campaigns
- [ ] Track campaign stats

**Database Models:**
```python
Campaign:
  - name
  - target_niche
  - target_country
  - total_leads
  - emails_sent
  - replies
  - status (draft/active/completed)
```

**API Endpoints:**
```python
POST   /api/campaigns           # Create campaign
GET    /api/campaigns           # List campaigns
GET    /api/campaigns/{id}      # Get campaign details
POST   /api/campaigns/{id}/run  # Start campaign
```

**Campaign Workflow:**
1. Create campaign
2. Find leads (using Lead Finder)
3. Add leads to campaign
4. Generate emails (manual for MVP)
5. Send emails (manual for MVP)
6. Track results

**Deliverables:**
- ✅ Campaign creation
- ✅ Campaign listing
- ✅ Basic campaign stats

**Time Estimate:** 5-6 hours

---

### **Day 6: Cold Email Generator** ✍️

**Goals:**
- [ ] AI email generator agent
- [ ] Personalized email templates
- [ ] Subject line optimization

**Create Agent:**
```python
# backend/app/agents/cold_email.py
class ColdEmailAgent:
    def generate_email(lead, service_description):
        # Generate personalized cold email
        # Return subject + body
```

**API Endpoint:**
```python
POST /api/emails/generate
{
  "lead_id": 1,
  "service": "We provide AI sales automation",
  "tone": "professional"  # or casual, friendly
}
```

**Output:**
```json
{
  "subject": "Quick question about your sales process",
  "body": "Hi [Name],\n\nI noticed [Company] is...",
  "variations": [...]
}
```

**Email Templates:**
- Cold email (initial outreach)
- Follow-up 1 (3 days later)
- Follow-up 2 (7 days later)
- Breakup email (14 days later)

**Deliverables:**
- ✅ Email generator working
- ✅ Personalized emails
- ✅ Multiple variations

**Time Estimate:** 6-7 hours

---

### **Day 7: Analytics & Polish** 📊

**Goals:**
- [ ] Analytics dashboard
- [ ] Bug fixes
- [ ] Documentation
- [ ] Deploy to production

**Analytics Endpoint:**
```python
GET /api/analytics
```

**Response:**
```json
{
  "total_leads": 150,
  "total_campaigns": 5,
  "emails_sent": 300,
  "reply_rate": 12.5,
  "meetings_booked": 8
}
```

**Testing Checklist:**
- [ ] Register new user
- [ ] Find leads in different niches
- [ ] Create campaign
- [ ] Generate emails
- [ ] Update lead statuses
- [ ] View analytics

**Documentation:**
- [ ] Update README.md
- [ ] Write API documentation
- [ ] Create deployment guide

**Deployment (Choose One):**
- Railway.app (easiest)
- Render.com (free tier)
- Fly.io (free allowance)

**Deliverables:**
- ✅ Analytics dashboard
- ✅ All bugs fixed
- ✅ Documentation complete
- ✅ Deployed to production

**Time Estimate:** 8-10 hours

---

## 🎯 MVP Success Metrics

After 7 days, you should have:

✅ **Functional Product:**
- Users can register/login
- AI finds qualified leads
- Leads stored in CRM
- Campaigns can be created
- Emails can be generated
- Basic analytics visible

✅ **Code Quality:**
- Clean, documented code
- Working tests
- No critical bugs
- Deployed and accessible

✅ **Ready for Users:**
- Can onboard first customer
- Can demonstrate value
- Can collect feedback

---

## 🚀 Post-MVP Roadmap

### Week 2: Email Automation
- [ ] Gmail/SMTP integration
- [ ] Automatic email sending
- [ ] Open/reply tracking
- [ ] Bounce handling

### Week 3: Advanced Features
- [ ] Follow-up sequences
- [ ] Meeting booking agent
- [ ] LinkedIn integration
- [ ] Calendar sync

### Week 4: SaaS Features
- [ ] Subscription plans
- [ ] Usage limits
- [ ] Payment integration (Stripe)
- [ ] Multi-user teams

### Month 2: Scale
- [ ] Advanced analytics
- [ ] A/B testing
- [ ] Custom integrations
- [ ] White-label option

---

## 💡 Daily Routine

**Morning (2-3 hours):**
- Review yesterday's work
- Plan today's tasks
- Code new features

**Afternoon (2-3 hours):**
- Testing
- Bug fixes
- Documentation

**Evening (1 hour):**
- Commit code
- Update progress
- Plan next day

---

## ⚠️ Common Pitfalls to Avoid

❌ **Don't:**
- Try to build everything at once
- Perfect every feature before moving on
- Skip testing
- Ignore error handling
- Forget to commit code

✅ **Do:**
- Ship fast, iterate faster
- Focus on core features only
- Test as you build
- Document decisions
- Get user feedback early

---

## 🎓 Resources

**Documentation:**
- FastAPI: https://fastapi.tiangolo.com
- CrewAI: https://docs.crewai.com
- Groq: https://console.groq.com/docs

**Tools:**
- Postman: API testing
- Swagger: API docs (auto-generated)
- Git: Version control

**Deployment:**
- Railway: https://railway.app
- Vercel: https://vercel.com (frontend)
- Render: https://render.com

---

## 🏁 Final Checklist

Before calling MVP "done":

- [ ] Can register new user
- [ ] Can login and get token
- [ ] Can find leads with AI
- [ ] Can view all leads
- [ ] Can create campaign
- [ ] Can generate emails
- [ ] Can update lead status
- [ ] Can view analytics
- [ ] No critical bugs
- [ ] Deployed online
- [ ] README updated
- [ ] API docs accessible

---

**Remember:** Your MVP doesn't need to be perfect. It needs to WORK and SOLVE THE CORE PROBLEM.

**Launch fast, learn faster!** 🚀
