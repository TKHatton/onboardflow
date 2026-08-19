# 🚀 OnboardFlow

**Autonomous Employee Onboarding with AI-Powered Decision Making**

OnboardFlow is an intelligent onboarding agent that uses Google's Gemini AI to autonomously plan and execute employee onboarding workflows. Unlike traditional scripted solutions, OnboardFlow reasons about each new hire's role and department to determine the optimal onboarding steps.

## ✨ Key Features

- **🧠 Autonomous Reasoning**: Gemini AI analyzes each new hire and decides what tools to use
- **⚡ Real-Time Streaming**: Server-Sent Events (SSE) provide live updates as the agent works
- **🎨 Modern React UI**: Beautiful, responsive interface with real-time workflow visualization
- **🔧 Multi-Tool Orchestration**: Integrates with Jira, Slack, GitHub, Calendar, Email, CRM, and Asana
- **📊 State Tracking**: Complete audit trail in Firestore for compliance and analytics
- **🌐 Event-Driven**: Pub/Sub triggers enable scalable, asynchronous processing

## 🏗️ Architecture

```
┌─────────────┐
│  React UI   │ ← Real-time SSE updates
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│   FastAPI Backend (Python)  │
│   - Autonomous Agent        │
│   - Gemini 2.0 Flash        │
│   - SSE Streaming           │
└──────┬──────────────────────┘
       │
       ├─► Jira (create tickets)
       ├─► GitHub (create accounts)
       ├─► Slack (send messages)
       ├─► Calendar (schedule meetings)
       ├─► Email (send welcome)
       ├─► CRM (setup access)
       └─► Asana (create projects)
       │
┌──────▼──────┐
│  Firestore  │ ← State tracking & audit
└─────────────┘
```

## 🎯 Use Cases

### Software Engineer Onboarding
Agent automatically:
- Creates Jira ticket with engineering tasks
- Sets up GitHub account with repo access
- Sends Slack welcome message
- Schedules orientation meeting
- Sends welcome email with dev resources

### Sales Representative Onboarding
Agent automatically:
- Creates Jira ticket with sales onboarding tasks
- Sets up CRM access with appropriate permissions
- Sends Slack welcome message
- Schedules sales training sessions
- Sends welcome email with sales materials

### Marketing Manager Onboarding
Agent automatically:
- Creates Asana project for marketing campaigns
- Sets up GitHub for marketing assets
- Sends Slack welcome message
- Schedules brand orientation
- Sends welcome email with brand guidelines

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud account
- Gemini API key

### 1. Clone and Install

```bash
git clone https://github.com/TKHatton/onboardflow.git
cd onboardflow
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Run Locally

**Terminal 1 - Backend:**
```bash
# From project root
python -m src.onboardflow.server
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## 📖 How It Works

### 1. User Submits New Hire Data
The React form collects employee details (name, role, department, start date, email, manager).

### 2. Agent Reasons About Workflow
Gemini analyzes the role and department to determine:
- Which tools are needed
- What order to execute them
- What parameters to use

Example reasoning:
> "For a Software Engineer in Engineering, I need to create a Jira ticket for task tracking, set up GitHub access for code repositories, send a welcome message to the team Slack channel, schedule an orientation meeting, and send a welcome email with development resources."

### 3. Tools Execute Autonomously
The agent calls each tool in sequence:
- Creates Jira ticket with engineering onboarding checklist
- Sets up GitHub account with appropriate repo access
- Sends personalized Slack welcome message
- Schedules orientation meeting on Google Calendar
- Sends welcome email with dev resources

### 4. Real-Time Updates
The React UI shows:
- Agent reasoning process
- Each step as it starts and completes
- Tool results and any errors
- Final workflow summary

### 5. State Persisted
All workflow data is logged to Firestore for:
- Audit trail
- Analytics
- Compliance
- Debugging

## 🎨 Demo

### Test Different Roles

Try these examples to see how the agent adapts:

**Software Engineer:**
- Name: Sarah Chen
- Role: Software Engineer
- Department: Engineering
- Email: sarah.chen@company.com

**Sales Representative:**
- Name: Michael Torres
- Role: Sales Representative
- Department: Sales
- Email: michael.torres@company.com

**Marketing Manager:**
- Name: Jennifer Lee
- Role: Marketing Manager
- Department: Marketing
- Email: jennifer.lee@company.com

Each role triggers different tools and workflows!

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **Google ADK** - Agent Development Kit
- **Gemini 2.0 Flash** - Fast, efficient reasoning
- **Firestore** - NoSQL database for state
- **Server-Sent Events** - Real-time streaming

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **CSS Modules** - Scoped styling

### Infrastructure
- **Google Cloud Run** - Serverless deployment
- **Google Pub/Sub** - Event-driven triggers
- **Docker** - Containerization

## 📊 Judging Criteria Alignment

### Innovation & Operational Utility (40%)
✅ **Autonomous decision-making** - Agent reasons about each role  
✅ **Real-world friction removal** - Eliminates manual onboarding tasks  
✅ **Multi-system orchestration** - Coordinates across 7+ tools  
✅ **No human intervention** - Fully autonomous execution  

### Architectural Discipline & Tech Stack (30%)
✅ **Clean separation of concerns** - Tools, agent, API, UI  
✅ **Event-driven architecture** - Pub/Sub for scalability  
✅ **State management** - Firestore for audit and resume  
✅ **Error handling** - Graceful degradation on failures  
✅ **Production-ready** - Docker, CORS, streaming  

### Demo & Production Readiness (30%)
✅ **Live demo** - Real-time workflow visualization  
✅ **Clean architecture diagram** - Clear system overview  
✅ **Reproducible setup** - README with step-by-step instructions  
✅ **Google Cloud deployed** - Cloud Run + Firestore  
✅ **Public GitHub repo** - Open source code  

## 🚢 Deployment

### Deploy to Google Cloud Run

```bash
# Build and push Docker image
docker build -t gcr.io/YOUR_PROJECT/onboardflow .
docker push gcr.io/YOUR_PROJECT/onboardflow

# Deploy to Cloud Run
gcloud run deploy onboardflow \
  --image gcr.io/YOUR_PROJECT/onboardflow \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your-key,GOOGLE_CLOUD_PROJECT=your-project"
```

### Deploy Frontend

```bash
cd frontend
npm run build
# Deploy dist/ to your hosting (Netlify, Vercel, etc.)
```

## 📝 API Endpoints

### `POST /api/onboard/stream`
Start onboarding workflow with SSE streaming.

**Request:**
```json
{
  "employee_name": "Sarah Chen",
  "role": "Software Engineer",
  "department": "Engineering",
  "start_date": "2026-02-01",
  "email": "sarah.chen@company.com",
  "manager": "Alex Rodriguez"
}
```

**Response:** Server-Sent Events stream with real-time updates.

### `GET /health`
Health check endpoint.

## 🎓 Learnings

### What Worked
- **Gemini for reasoning** - Fast, accurate tool selection
- **SSE streaming** - Smooth real-time updates
- **Modular tools** - Easy to add new integrations
- **React visualization** - Clear workflow representation

### Challenges Overcome
- **Streaming architecture** - Implemented SSE for real-time updates
- **Error handling** - Graceful degradation when tools fail
- **State management** - Firestore for audit and resume capability

## 🔮 Future Enhancements

- [ ] HRIS integration (Workday, BambooHR)
- [ ] Custom onboarding templates
- [ ] Approval workflows for sensitive actions
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Slack/Teams bot interface

## 📄 License

MIT

## 🏆 Hackathon

Built for **All Things Agentic Hackathon** (Google) - August 2026

**Track:** The Taskmaster  
**Prize Category:** $20,000

---

**Built with ❤️ using Google ADK + Gemini**
