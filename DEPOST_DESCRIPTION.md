# OnboardFlow - Devpost Submission Description

## Project Name
OnboardFlow

## Tagline (short, punchy)
Autonomous AI agent that orchestrates complete employee onboarding across 11+ systems

## Short Description (under 500 characters)
OnboardFlow is an autonomous AI agent that eliminates manual employee onboarding by intelligently orchestrating workflows across 11+ enterprise systems. Using Google's Gemini AI and Agent Development Kit, it analyzes each new hire's role and department to autonomously provision equipment, assign training, set up accounts, enroll in benefits, and schedule meetings—all without human intervention. Includes real-time dashboard and chatbot assistant.

## Full Description

### The Problem
Employee onboarding is broken. HR teams spend 15-20 hours per new hire manually coordinating across dozens of systems—ordering equipment, creating accounts, scheduling training, sending welcome emails, enrolling in benefits. It's repetitive, error-prone, and doesn't scale. Critical steps get missed, new hires have poor first impressions, and HR teams burn out on administrative work instead of focusing on people.

### The Solution
OnboardFlow is an autonomous AI agent that handles the entire onboarding process end-to-end. When a new hire is submitted, the agent:

1. **Analyzes the role and department** using Google's Gemini AI
2. **Reasons about what's needed** - not following a hardcoded script, but making intelligent decisions based on the specific role
3. **Executes across 11+ systems** autonomously:
   - Equipment provisioning (laptops, monitors, peripherals)
   - GitHub account creation with repository access
   - CRM setup for sales teams
   - Asana project creation for marketing
   - Jira ticket creation for task tracking
   - Slack welcome messages to teams
   - Calendar scheduling for orientation
   - Email communications with resources
   - Training course assignments with deadlines
   - Security and compliance training
   - Benefits enrollment (health, dental, vision, 401k)
   - Automated follow-up verification

4. **Tracks everything** in Firestore for audit trails and compliance
5. **Provides real-time visibility** via a React dashboard with server-sent events
6. **Answers questions** via an integrated chatbot that has full context about the onboarding

### What Makes It Different
Most automation tools follow hardcoded workflows. OnboardFlow reasons. 

For a Software Engineer, the agent decides: "They need GitHub access to code repositories, high-spec equipment for development, technical training on our stack."

For an HR Coordinator, it decides: "They need standard workstation equipment, HR-specific training, compliance modules, benefits enrollment."

For a Sales Representative, it decides: "They need CRM access, sales training, customer onboarding materials."

Same system, completely different workflows. The agent adapts to each role automatically.

### Technical Architecture
- **Frontend**: React 18 with TypeScript, Vite, real-time dashboard
- **Backend**: FastAPI (Python) with server-sent events for streaming
- **AI**: Google Agent Development Kit (ADK) with Gemini 3.6 Flash
- **State**: Google Firestore for audit trails and workflow state
- **Tools**: 11+ modular tool integrations (Jira, GitHub, Slack, Calendar, Email, etc.)
- **Chatbot**: Integrated Q&A assistant with full onboarding context

### Key Features
✅ **Autonomous reasoning** - Agent decides what tools to use based on role  
✅ **Real-time streaming** - Watch the agent think and execute live  
✅ **Role-based adaptation** - Different workflows for different roles  
✅ **11+ tool integrations** - Comprehensive system coverage  
✅ **Chatbot assistant** - 24/7 Q&A for new hires  
✅ **State tracking** - Full audit trail in Firestore  
✅ **Error handling** - Graceful degradation on failures  

### Impact
- **Time savings**: 15-20 hours of manual work → 20 seconds
- **Consistency**: Every new hire gets comprehensive onboarding
- **Scalability**: Handle 1 or 100 new hires with the same effort
- **Compliance**: Complete audit trail for every action
- **Experience**: New hires get personalized, thorough onboarding

### Built With
- Google Agent Development Kit (ADK)
- Gemini 3.6 Flash
- Google Cloud Firestore
- FastAPI (Python)
- React 18 + TypeScript
- Server-Sent Events
- Docker

### Try It
- **Source Code**: https://github.com/TKHatton/onboardflow
- **Live Demo**: [URL]
- **Demo Video**: [URL]

### Future Enhancements
- HRIS integration (Workday, BambooHR)
- Custom onboarding templates per company
- Approval workflows for sensitive actions
- Analytics dashboard with metrics
- Multi-language support
- Slack/Teams bot interface

---

## Notes for Submission
- Keep the demo video under 4 minutes
- Show the reasoning panel (judges want to see Gemini thinking)
- Demonstrate role-based adaptation (show 2 different roles)
- Highlight the chatbot feature
- Mention Google Cloud services used (Firestore, Gemini, ADK)
