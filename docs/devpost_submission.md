# Devpost Submission — All Things Agentic Hackathon

## Project Name
OnboardFlow

## Category
The Taskmaster

## Short Description (150 chars max)
Autonomous employee onboarding agent that detects new hire events and executes multi-step workflows across Jira, Slack, Calendar, and Email — zero human intervention.

## Full Description

### What problem does your project solve?

Employee onboarding is a mess of manual tasks spread across multiple systems. HR teams create Jira tickets, send Slack messages, schedule meetings, and write welcome emails — all by hand. It takes hours per hire, things get missed, and the process doesn't scale.

OnboardFlow eliminates this entirely. When a new hire event is published, an autonomous agent takes over — creating tickets, sending messages, scheduling meetings, and sending emails across four different systems without any human intervention.

### How does it work?

OnboardFlow is an event-driven autonomous agent built with Google ADK (Agent Development Kit) and Gemini 3.5 Flash.

1. **Event Trigger**: A new hire event is published to Google Pub/Sub (JSON payload with employee name, role, department, start date, email, manager)
2. **Agent Activation**: Cloud Run receives the event and activates the OnboardFlow agent
3. **Autonomous Execution**: The agent orchestrates a multi-step workflow:
   - Creates a Jira ticket with full onboarding checklist
   - Sends a welcome message to the team Slack channel
   - Schedules an orientation meeting on Google Calendar
   - Sends a personalized welcome email to the new hire
4. **State Tracking**: Every action is logged to Firestore — creating a complete audit trail of what was done, when, and with what result

The agent handles the entire workflow autonomously. No human clicks buttons. No one copies data between systems. No steps get forgotten.

### What makes it different?

Most AI agents are chatbots — they wait for you to ask something and respond with text. OnboardFlow is different:

- **Autonomous, not conversational**: It doesn't chat. It acts. It watches for events and executes workflows without being told.
- **Multi-system orchestration**: It coordinates across 4 different tools (Jira, Slack, Calendar, Email) in a single workflow.
- **Event-driven architecture**: Built on Pub/Sub for real-time, scalable triggering — not polling or manual activation.
- **State-aware**: Every action is tracked in Firestore, enabling audit trails, resume capability, and analytics.
- **Production-minded**: Clean separation of concerns, error handling, and observability built in from the start.

### Technical Architecture

```
Pub/Sub → Cloud Run → ADK Agent → Tools (Jira, Slack, Calendar, Email)
                                    ↓
                                 Firestore (state tracking)
```

**Tech Stack:**
- Gemini 3.5 Flash (via Gemini API)
- Google ADK (Agent Development Kit)
- Google Cloud Run (serverless deployment)
- Google Firestore (state management & audit log)
- Google Pub/Sub (event-driven triggers)
- FastAPI (HTTP endpoints)
- Python 3.11

### What's next?

- Real API integrations (Jira Cloud API, Slack Web API, Google Calendar API, SendGrid)
- Configurable onboarding templates per department/role
- Web dashboard for monitoring onboarding status
- HRIS integration (BambooHR, Workday) as event source
- Multi-language welcome emails
- Retry logic for failed steps

### Links
- Repository: [GitHub URL]
- Demo Video: [YouTube URL]
- Architecture Diagram: [docs/architecture.html]
