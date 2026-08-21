# 🚀 OnboardFlow

**Autonomous AI-Powered Employee Onboarding System**

OnboardFlow is an intelligent onboarding agent that uses Google's Gemini AI to autonomously plan and execute comprehensive employee onboarding workflows. Unlike traditional scripted solutions, OnboardFlow reasons about each new hire's role and department to determine the optimal onboarding steps across 11+ integrated systems.

## ✨ Key Features

### 🧠 Autonomous Reasoning
- Gemini AI analyzes each new hire and decides what tools to use
- Role-based intelligence: engineers get GitHub, sales gets CRM, marketing gets Asana
- No hardcoded workflows - the agent thinks and adapts

### 🔧 11+ Integrated Tools
- **Equipment Provisioning** - Orders laptops, monitors, and peripherals based on role
- **GitHub Setup** - Creates accounts and assigns repository access
- **CRM Access** - Sets up Salesforce/HubSpot for sales teams
- **Asana Projects** - Creates marketing project templates
- **Jira Tickets** - Tracks onboarding tasks and progress
- **Slack Integration** - Sends welcome messages to teams
- **Calendar Scheduling** - Books orientation and training sessions
- **Email Communications** - Sends personalized welcome emails
- **Training Courses** - Assigns role-based learning paths with deadlines
- **Security Training** - Mandatory compliance and security modules
- **Benefits Enrollment** - Health insurance, 401k, and perks setup
- **Verification System** - Automated follow-up checks at 7 and 30 days

### 💬 Chatbot Assistant
- New hires can ask questions about their onboarding
- Answers questions about equipment, benefits, training, and policies
- Provides relevant resources and documentation links
- Available 24/7 for instant support

### 📊 Real-Time Dashboard
- Live workflow visualization with Server-Sent Events
- See the agent's reasoning process as it happens
- Track each tool execution in real-time
- Beautiful React UI with gradient design

## 🏗️ Architecture

```
┌─────────────────┐
│   React UI      │ ← Real-time SSE updates
│   (TypeScript)  │
└────────┬────────┘
         │
┌────────▼──────────────────────┐
│   FastAPI Backend (Python)    │
│   - Autonomous Agent          │
│   - Gemini 2.0 Flash          │
│   - SSE Streaming             │
└────────┬──────────────────────┘
         │
         ├─► Equipment Provisioning
         ├─► GitHub Setup
         ├─► CRM Access
         ├─► Asana Projects
         ├─► Jira Tickets
         ├─► Slack Integration
         ├─► Calendar Scheduling
         ├─► Email Communications
         ├─► Training Courses
         ├─► Security Training
         ├─► Benefits Enrollment
         └─► Verification System
         │
┌────────▼──────┐
│  Firestore    │ ← State tracking & audit
└───────────────┘
```

## 🎯 How It Works

### 1. User Submits New Hire Data
The React form collects employee details (name, role, department, start date, email, manager).

### 2. Agent Reasons About Workflow
Gemini analyzes the role and department to determine:
- Which tools are needed
- What order to execute them
- What parameters to use

**Example reasoning:**
> "For a Software Engineer in Engineering, I need to provision a high-spec laptop with dual monitors, create a GitHub account with access to frontend/backend repos, assign technical training courses, schedule security training, send a welcome email with dev resources, create a Jira ticket for onboarding tasks, and schedule a follow-up verification in 7 days."

### 3. Tools Execute Autonomously
The agent calls each tool in sequence:
- Orders equipment from IT procurement
- Creates GitHub account with appropriate repo access
- Assigns role-specific training courses with deadlines
- Schedules mandatory security training
- Sends personalized welcome email
- Creates Jira ticket with onboarding checklist
- Schedules follow-up verification

### 4. Real-Time Updates
The React UI shows:
- Agent reasoning process
- Each step as it starts and completes
- Tool results and any errors
- Final workflow summary

### 5. Chatbot Support
New hires can ask questions like:
- "When will I receive my equipment?"
- "What training do I need to complete?"
- "How do I enroll in benefits?"
- "What's the PTO policy?"

### 6. State Persisted
All workflow data is logged to Firestore for:
- Audit trail
- Analytics
- Compliance
- Debugging

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

## 🎨 Demo

### Test Different Roles

Try these examples to see how the agent adapts:

**Software Engineer:**
- Name: Sarah Chen
- Role: Software Engineer
- Department: Engineering
- Email: sarah.chen@company.com
- Expected: GitHub, high-spec equipment, technical training

**Sales Representative:**
- Name: Michael Torres
- Role: Sales Representative
- Department: Sales
- Email: michael.torres@company.com
- Expected: CRM access, sales training, customer onboarding

**Marketing Manager:**
- Name: Jennifer Lee
- Role: Marketing Manager
- Department: Marketing
- Email: jennifer.lee@company.com
- Expected: Asana projects, brand guidelines, creative tools

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
- **CSS** - Custom styling

### Infrastructure
- **Google Cloud Run** - Serverless deployment
- **Google Pub/Sub** - Event-driven triggers
- **Docker** - Containerization

## 📊 Judging Criteria Alignment

### Innovation & Operational Utility (40%)
✅ **Autonomous decision-making** - Agent reasons about each role  
✅ **Real-world friction removal** - Eliminates manual onboarding tasks  
✅ **Multi-system orchestration** - Coordinates across 11+ tools  
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

### `GET /api/onboard/stream`
Start onboarding workflow with SSE streaming.

**Query Parameters:**
```
employee_name=Sarah Chen
role=Software Engineer
department=Engineering
start_date=2026-02-01
email=sarah.chen@company.com
manager=Alex Rodriguez
```

**Response:** Server-Sent Events stream with real-time updates.

### `POST /api/chat`
Answer onboarding questions using the chatbot.

**Request:**
```json
{
  "employee_name": "Sarah Chen",
  "question": "When will I receive my equipment?",
  "context": {
    "role": "Software Engineer",
    "department": "Engineering"
  }
}
```

**Response:**
```json
{
  "answer": "Your equipment will arrive within 3-5 business days...",
  "resources": [
    {"title": "IT Setup Guide", "url": "/resources/it-setup"}
  ]
}
```

### `GET /health`
Health check endpoint.

## 🔮 Future Enhancements

- [ ] HRIS integration (Workday, BambooHR)
- [ ] Custom onboarding templates per company
- [ ] Approval workflows for sensitive actions
- [ ] Analytics dashboard with metrics
- [ ] Multi-language support
- [ ] Slack/Teams bot interface
- [ ] Mobile app for new hires
- [ ] Integration with learning management systems

## 📄 License

MIT

## 🏆 Hackathon

Built for **All Things Agentic Hackathon** (Google) - August 2026

**Track:** The Taskmaster  
**Prize Category:** $20,000

---

**Built with ❤️ using Google ADK + Gemini**
