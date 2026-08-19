# OnboardFlow

Autonomous employee onboarding workflow agent that detects new hire events and executes multi-step onboarding across systems without manual intervention.

## Overview

OnboardFlow automates the employee onboarding process by:
- Detecting new hire events via Pub/Sub
- Creating Jira tickets for onboarding tasks
- Sending welcome messages to Slack
- Scheduling orientation meetings on Google Calendar
- Sending welcome emails to new hires
- Tracking all actions in Firestore

Built with Google ADK (Agent Development Kit), Gemini 3.5 Flash, and Google Cloud services.

## Architecture

```
Pub/Sub → Cloud Run → ADK Agent → Tools (Jira, Slack, Calendar, Email)
                                    ↓
                                 Firestore (state tracking)
```

## Tech Stack

- **Gemini 3.5 Flash** - AI reasoning and orchestration
- **Google ADK** - Agent framework with MCP tools
- **Google Cloud Run** - Serverless deployment
- **Google Firestore** - State management and audit log
- **Google Pub/Sub** - Event-driven triggers
- **Python 3.11+** - Core implementation

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud account with billing enabled
- Gemini API key (get from https://aistudio.google.com/app/apikey)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd onboardflow
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Google Cloud project and API key
```

### Local Testing

Run the test workflow:
```bash
python test_onboarding.py
```

This will execute a sample onboarding workflow with mock tools and show you the results.

### Deployment to Google Cloud

1. Enable required APIs:
```bash
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy onboardflow \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your-key
```

3. Set up Pub/Sub trigger:
```bash
gcloud pubsub topics create new-hire-events
gcloud pubsub subscriptions create onboardflow-sub \
  --topic=new-hire-events \
  --push-endpoint=<your-cloud-run-url>
```

## Usage

### Triggering Onboarding

Publish a new hire event to Pub/Sub:

```bash
gcloud pubsub topics publish new-hire-events \
  --message='{
    "employee_name": "Sarah Chen",
    "role": "Senior Software Engineer",
    "department": "Engineering",
    "start_date": "2026-09-15",
    "email": "sarah.chen@example.com",
    "manager": "Alex Rodriguez",
    "manager_email": "alex.rodriguez@example.com"
  }'
```

The agent will automatically:
1. Create a Jira ticket
2. Send Slack welcome message
3. Schedule orientation meeting
4. Send welcome email
5. Log all actions to Firestore

## Project Structure

```
onboardflow/
├── src/
│   └── onboardflow/
│       ├── __init__.py
│       ├── agent.py          # Core agent orchestration
│       └── tools/            # MCP tools
│           ├── jira_tool.py
│           ├── slack_tool.py
│           ├── calendar_tool.py
│           └── email_tool.py
├── tests/
├── docs/
├── test_onboarding.py        # Local test script
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Development

### Adding New Tools

1. Create a new tool in `src/onboardflow/tools/`
2. Export it in `tools/__init__.py`
3. Add it to the agent's tool list in `agent.py`

### Testing

Run tests:
```bash
pytest tests/
```

## License

MIT

## Hackathon

Built for the All Things Agentic Hackathon (Google) - August 2026
