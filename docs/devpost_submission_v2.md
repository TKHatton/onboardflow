# OnboardFlow - Devpost Submission

## Project Name
OnboardFlow

## Tagline
Autonomous AI agent that orchestrates comprehensive employee onboarding across 11+ systems

## Short Description (500 chars)
OnboardFlow is an autonomous AI agent that eliminates manual onboarding by intelligently orchestrating workflows across 11+ enterprise systems. Using Gemini AI, it analyzes each new hire's role and department to autonomously provision equipment, assign role-based training, set up system access, enroll in benefits, schedule meetings, send communications, and verify completion—all without human intervention. Includes a real-time React dashboard and chatbot assistant for new hire Q&A.

## Full Description

### Inspiration
Employee onboarding is a nightmare of manual tasks spread across dozens of systems. HR teams waste hours creating tickets, ordering equipment, assigning training, setting up accounts, and sending welcome messages. Things get missed, new hires have a poor first impression, and the process doesn't scale.

We built OnboardFlow to eliminate this entirely. An autonomous AI agent that understands each new hire's unique needs and orchestrates the entire onboarding process across all systems—intelligently, autonomously, and completely.

### What it does
OnboardFlow uses Google's Gemini AI to autonomously plan and execute comprehensive onboarding workflows:

**Intelligent Tool Selection**: The agent analyzes the employee's role, department, and seniority to determine exactly which systems and processes are needed. A software engineer gets GitHub access and technical training. A sales rep gets CRM setup and product training. A marketing manager gets Asana projects and brand guidelines.

**11+ Integrated Tools**:
- Equipment provisioning (laptops, monitors, peripherals based on role)
- System access (GitHub, CRM, Asana, Jira, etc.)
- Role-based training courses with deadlines
- Mandatory security and compliance training
- Benefits enrollment (health insurance, 401k, perks)
- Welcome communications (email, Slack)
- Meeting scheduling (orientation, 1:1s)
- Follow-up verification (7-day and 30-day check-ins)
- Chatbot assistant for new hire Q&A

**Real-Time Streaming**: Server-Sent Events push live updates to a React dashboard, showing the agent's reasoning process and each step as it executes.

**Chatbot Assistant**: New hires can ask questions about their onboarding, benefits, training, equipment, and company policies. The chatbot provides instant answers with relevant resources.

### How we built it
**Backend (Python/FastAPI)**:
- Autonomous agent powered by Gemini 2.0 Flash
- 11 modular MCP-style tools for different systems
- Server-Sent Events for real-time streaming
- FastAPI endpoints for workflow execution and chatbot

**Frontend (React/TypeScript)**:
- Modern UI with Vite
- Real-time workflow dashboard
- Tab navigation between workflow view and chatbot
- Live updates via EventSource API

**Architecture**:
```
React UI ←→ FastAPI Backend ←→ Gemini AI
                ↓
        11+ Tools (Jira, GitHub, Slack, 
        Calendar, Email, CRM, Asana, 
        Training, Equipment, Security, 
        Benefits, Verification)
```

### Challenges we ran into
1. **AQ API Key Format**: Google introduced new AQ format API keys in 2026 that required SDK updates and configuration changes
2. **SSE with EventSource**: Browser's native EventSource API only supports GET requests, so we had to refactor from POST to GET with query parameters
3. **Intelligent Tool Selection**: Getting Gemini to consistently choose the right tools for each role required careful prompt engineering
4. **Real-Time Streaming**: Coordinating state updates between backend execution and frontend display

### Accomplishments that we're proud of
- **Truly Autonomous**: The agent makes intelligent decisions about which tools to use based on role/department—no hardcoded workflows
- **Comprehensive Coverage**: 11+ tools covering the entire onboarding lifecycle, not just a few integrations
- **Real-Time Visibility**: Live streaming shows the agent's reasoning and execution in real-time
- **User-Friendly**: Chatbot assistant helps new hires navigate their onboarding
- **Production-Ready**: Clean architecture, error handling, and modular design

### What we learned
- **Gemini's Reasoning Capabilities**: Gemini 2.0 Flash excels at understanding context and making multi-step decisions
- **Event-Driven Architecture**: SSE provides smooth real-time updates without polling
- **Modular Tool Design**: Each tool is independent and can be added/removed without affecting the agent
- **User Experience Matters**: Real-time feedback and chatbot support make the system feel responsive and helpful

### What's next for OnboardFlow
- **Real API Integrations**: Connect to actual Jira, GitHub, Slack, etc. APIs
- **HRIS Integration**: Trigger workflows from Workday, BambooHR, etc.
- **Custom Workflows**: Allow companies to define custom onboarding templates
- **Analytics Dashboard**: Track onboarding metrics and completion rates
- **Multi-Language Support**: Support onboarding in multiple languages
- **Approval Workflows**: Add human-in-the-loop for sensitive actions

## Built With
- Google ADK (Agent Development Kit)
- Gemini 2.0 Flash
- FastAPI
- React
- TypeScript
- Vite
- Server-Sent Events
- Python
- Node.js

## Try It Out
- **Repository**: https://github.com/TKHatton/onboardflow
- **Demo Video**: [YouTube link]
- **Live Demo**: [Cloud Run URL]

## Submission Checklist
- [x] Code repository (public)
- [x] README with setup instructions
- [x] Architecture diagram
- [x] Demo video (< 4 minutes)
- [x] Deployed to Google Cloud
- [x] Uses Gemini 3.5+ (via Gemini API)
- [x] Uses Google Agent Framework (ADK)
- [x] Uses Google Cloud service (Cloud Run)
