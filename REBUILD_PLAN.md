# OnboardFlow — Rebuild Plan

## Goal
Rebuild with actual autonomous decision-making (Gemini reasoning) + React UI for demo/portfolio.

## Architecture

### Backend (Python/FastAPI)
- **Real Gemini integration**: Agent receives new hire data, Gemini decides what steps to take based on role/department
- **Streaming**: Server-Sent Events (SSE) to push real-time updates to React UI
- **Mock tools with realistic responses**: Each tool returns detailed, realistic data
- **Reasoning transparency**: Gemini explains WHY it's choosing certain actions

### Frontend (React + Vite + TypeScript)
- **NewHireForm**: Clean form to enter employee details
- **WorkflowDashboard**: Real-time visualization of workflow execution
- **AgentReasoning**: Shows what Gemini is thinking/deciding
- **StepCard**: Individual step status with details
- **ArchitectureView**: Shows the system architecture

## Demo Flow (for video)
1. Show React UI
2. Enter new hire details (different roles to show adaptation)
3. Click "Start Onboarding"
4. Watch Gemini reason: "For a Senior Software Engineer in Engineering, I need to: create Jira ticket, set up GitHub access, send Slack message, schedule orientation..."
5. See each step execute in real-time
6. Show final summary with all completed actions

## Key Difference from v1
- v1: Hardcoded steps (always does Jira → Slack → Calendar → Email)
- v2: Gemini DECIDES what steps based on role/department
  - Software Engineer → Jira + GitHub + Slack + Calendar
  - Sales Rep → CRM + Slack + Calendar + Email
  - Marketing → Asana + Slack + Calendar + Email

## Implementation Order
1. Backend: Wire up real Gemini reasoning
2. Backend: Add SSE streaming
3. Frontend: React app with Vite
4. Frontend: Connect to backend via SSE
5. Frontend: Real-time workflow visualization
6. Test end-to-end
