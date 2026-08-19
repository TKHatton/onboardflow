# OnboardFlow — Build Plan

## Project Overview
Autonomous employee onboarding workflow agent that detects new hire events and executes multi-step onboarding across systems without manual intervention.

## Why This Wins
- **Innovation & Operational Utility (40%)**: Autonomous action, not chat. Agent watches for events, decides what to do, executes across multiple systems.
- **Architectural Discipline (30%)**: Event-driven architecture, state management, multi-system orchestration, failure handling.
- **Demo & Production Readiness (30%)**: Clear visual workflow, reproducible setup, runs on Google Cloud.

## Tech Stack
- **Gemini 3.5 Flash** via Gemini API
- **Google ADK** (Agent Development Kit) with MCP tools
- **Google Cloud Run** (deployment)
- **Google Firestore** (state management)
- **Google Pub/Sub** (event triggers)
- **Python 3.11+**

## Architecture

```
┌─────────────────┐
│  Pub/Sub Topic  │ ← New hire events
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cloud Run API  │ ← Receives events, triggers agent
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OnboardFlow    │ ← ADK Agent (orchestrator)
│  Agent          │
└────────┬────────┘
         │
         ├─────────────┬─────────────┬─────────────┐
         ▼             ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
    │  Jira   │  │  Slack  │  │ Google  │  │ Email   │
    │  MCP    │  │  MCP    │  │ Cal MCP │  │  MCP    │
    │  Tool   │  │  Tool   │  │  Tool   │  │  Tool   │
    └─────────┘  └─────────┘  └─────────┘  └─────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                        │
                        ▼
                  ┌───────────┐
                  │ Firestore │ ← State, audit log
                  └───────────┘
```

## Core Workflow
1. **Event Trigger**: Pub/Sub receives "new_hire" event (name, start_date, role, department)
2. **Agent Activation**: Cloud Run invokes OnboardFlow agent
3. **Agent Decides**: Gemini determines onboarding steps based on role/department
4. **Execute Steps**:
   - Create Jira ticket: "Onboarding: [Name] - [Role]"
   - Send Slack welcome message to #general
   - Schedule 1:1 meeting with manager (Google Calendar)
   - Send welcome email to new hire
5. **State Tracking**: Each completed step logged to Firestore
6. **Completion**: Agent marks onboarding complete when all steps done

## Implementation Phases

### Phase 1: Core Agent (Days 1-3)
**Goal**: Working agent that can orchestrate onboarding steps locally

**Tasks**:
- [x] Set up project structure
- [x] Install google-adk, google-cloud-firestore
- [x] Create basic ADK agent with Gemini 3.5 Flash
- [x] Implement mock MCP tools (Jira, Slack, Calendar, Email)
- [x] Test agent can call tools in sequence
- [ ] Add Firestore state tracking

**Deliverable**: Agent runs locally, executes mock onboarding workflow, logs to Firestore

### Phase 2: Real MCP Tools (Days 4-6)
**Goal**: Connect to real services (or realistic mocks)

**Tasks**:
- [ ] Implement Jira MCP tool (create issues)
- [ ] Implement Slack MCP tool (send messages)
- [ ] Implement Google Calendar MCP tool (create events)
- [ ] Implement Email MCP tool (send emails)
- [ ] Test each tool individually
- [ ] Test full workflow with real tools

**Deliverable**: Agent executes real onboarding actions across services

### Phase 3: Event-Driven Architecture (Days 7-8)
**Goal**: Agent triggered by Pub/Sub events

**Tasks**:
- [ ] Create Pub/Sub topic for new_hire events
- [ ] Create Cloud Run endpoint to receive Pub/Sub messages
- [ ] Wire endpoint to trigger agent
- [ ] Test end-to-end: publish event → agent executes → state logged

**Deliverable**: Event-driven workflow works end-to-end

### Phase 4: Deployment & Demo (Days 9-10)
**Goal**: Deploy to Google Cloud, record demo

**Tasks**:
- [ ] Deploy to Cloud Run
- [ ] Set up Firestore database
- [ ] Configure Pub/Sub
- [ ] Test deployed version
- [ ] Record demo video (show event → agent → actions)
- [ ] Create architecture diagram

**Deliverable**: Live deployment, demo video, architecture diagram

### Phase 5: Submission (Days 11-12)
**Goal**: Complete Devpost submission

**Tasks**:
- [ ] Write project description
- [ ] Document tech stack
- [ ] Write README with setup instructions
- [ ] Create GitHub repo (public)
- [ ] Submit to Devpost
- [ ] Post to social media (bonus points)

**Deliverable**: Complete submission

## Scope Control

### MUST HAVE (for submission)
- Agent orchestrates onboarding workflow
- Calls 4+ tools (Jira, Slack, Calendar, Email)
- State tracking in Firestore
- Runs on Google Cloud (Cloud Run)
- Demo video showing workflow
- Architecture diagram
- Public GitHub repo with README

### NICE TO HAVE (if time permits)
- Web UI to trigger onboarding manually
- Dashboard showing onboarding progress
- Error handling and retry logic
- Support for different onboarding templates by role

### NOT NEEDED (for this hackathon)
- Multi-tenant support
- Authentication/authorization
- Production-grade error handling
- Monitoring/alerting
- Mobile app

## Demo Story
**Opening**: "Employee onboarding is a mess. HR manually creates tickets, sends messages, schedules meetings. It takes hours and things get missed."

**Problem**: Show a messy spreadsheet of onboarding tasks, some marked complete, some forgotten.

**Solution**: "OnboardFlow automates this. When a new hire is added to the system, the agent takes over."

**Demo**:
1. Publish a "new hire" event to Pub/Sub (show the JSON)
2. Agent activates (show Cloud Run logs)
3. Jira ticket created (show Jira UI)
4. Slack message sent (show Slack channel)
5. Calendar event created (show Google Calendar)
6. Welcome email sent (show email client)
7. Firestore shows all steps completed (show Firestore console)

**Closing**: "One event. Four systems. Zero manual work. That's autonomous onboarding."

## Risk Mitigation

### Risk: MCP tools too complex to implement in time
**Mitigation**: Use realistic mocks that simulate real behavior. Judges care about architecture, not whether Jira actually received the ticket.

### Risk: Google Cloud costs too high
**Mitigation**: Use free tier, scale to zero, delete resources after demo. $150 in credits should be enough.

### Risk: Agent makes wrong decisions
**Mitigation**: Hard-code the workflow logic in the agent's instructions. Let Gemini decide the order, but constrain the actions.

### Risk: Demo fails live
**Mitigation**: Record demo multiple times. Use the best take. Show logs as backup proof.

## Success Criteria
- [ ] Agent executes full onboarding workflow autonomously
- [ ] All 4 tools called successfully
- [ ] State tracked in Firestore
- [ ] Deployed to Google Cloud
- [ ] Demo video < 4 minutes
- [ ] Architecture diagram clear
- [ ] GitHub repo public with README
- [ ] Submitted to Devpost before Aug 31 8:00 PM EDT
