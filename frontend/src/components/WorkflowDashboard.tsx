import type { WorkflowState, WorkflowStep } from '../types';
import './WorkflowDashboard.css';

interface WorkflowDashboardProps {
  workflow: WorkflowState;
}

const COMMUNICATION_TOOLS = ['send_welcome_email', 'send_slack_message', 'schedule_meeting'];

interface TimelineEntry {
  when: string;
  label: string;
}

function buildTimeline(steps: WorkflowStep[]): TimelineEntry[] {
  const entries: TimelineEntry[] = [];

  for (const step of steps) {
    const data = step.result?.data;
    if (!data) continue;

    switch (step.tool) {
      case 'send_welcome_email':
        entries.push({ when: data.sent_at, label: `Welcome email sent to ${data.to}` });
        break;
      case 'send_slack_message':
        entries.push({ when: data.timestamp, label: `Slack announcement posted to ${data.channel}` });
        break;
      case 'schedule_meeting':
        entries.push({ when: data.start, label: `${data.summary}` });
        break;
      case 'assign_training_courses':
        if (data.deadline) {
          entries.push({ when: data.deadline, label: 'Role-specific training due' });
        }
        break;
      case 'schedule_security_training':
        (data.training_modules || []).forEach((m: any) => {
          entries.push({ when: m.deadline, label: `${m.name} due (${m.priority} priority)` });
        });
        break;
      case 'enroll_in_benefits':
        if (data.enrollment_deadline) {
          entries.push({ when: data.enrollment_deadline, label: 'Benefits enrollment deadline' });
        }
        break;
      case 'verify_onboarding_completion':
        (data.follow_up_actions || []).forEach((a: any) => {
          let label = a.action;
          if (a.action === 'send_checkin_email') label = 'Automated check-in reminder email';
          else if (a.action === 'schedule_checkin_meeting') label = '30-day onboarding review meeting';
          else if (a.action === 'notify_manager') label = 'Manager notified of pending items';
          entries.push({ when: a.scheduled_for, label });
        });
        break;
      default:
        break;
    }
  }

  return entries.filter((e) => e.when).sort((a, b) => a.when.localeCompare(b.when));
}

function relativeDay(iso: string): string {
  const target = new Date(iso);
  const now = new Date();
  const diffMs = target.getTime() - now.getTime();
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays <= 0) return 'Today';
  if (diffDays === 1) return 'Tomorrow';
  return `In ${diffDays} days`;
}

export function WorkflowDashboard({ workflow }: WorkflowDashboardProps) {
  const getPhaseIcon = () => {
    switch (workflow.phase) {
      case 'reasoning':
        return '🧠';
      case 'executing':
        return '⚙️';
      case 'complete':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⏸️';
    }
  };

  const getPhaseText = () => {
    switch (workflow.phase) {
      case 'reasoning':
        return 'Agent is reasoning...';
      case 'executing':
        return 'Executing workflow...';
      case 'complete':
        return 'Workflow complete!';
      case 'error':
        return 'Error occurred';
      default:
        return 'Waiting...';
    }
  };

  const getStepIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'running':
        return '🔄';
      case 'failed':
        return '❌';
      default:
        return '⏸️';
    }
  };

  const messages = workflow.phase === 'complete'
    ? workflow.steps.filter((s) => COMMUNICATION_TOOLS.includes(s.tool) && s.result?.data)
    : [];
  const timeline = workflow.phase === 'complete' ? buildTimeline(workflow.steps) : [];

  return (
    <div className="workflow-dashboard">
      <div className="phase-indicator">
        <span className="phase-icon">{getPhaseIcon()}</span>
        <span className="phase-text">{getPhaseText()}</span>
      </div>

      {workflow.reasoning && (
        <div className="reasoning-section">
          <h3>Agent Reasoning</h3>
          <p className="reasoning-text">{workflow.reasoning}</p>
        </div>
      )}

      {workflow.steps.length > 0 && (
        <div className="steps-section">
          <h3>Workflow Steps ({workflow.steps.length})</h3>
          <div className="steps-list">
            {workflow.steps.map((step, index) => (
              <div key={index} className={`step-item step-${step.status}`}>
                <div className="step-header">
                  <span className="step-icon">{getStepIcon(step.status)}</span>
                  <span className="step-number">Step {step.step}</span>
                  <span className="step-tool">{step.tool}</span>
                </div>
                <p className="step-action">{step.action}</p>
                {step.result && (
                  <div className="step-result">
                    <strong>Result:</strong>
                    <pre>{JSON.stringify(step.result, null, 2)}</pre>
                  </div>
                )}
                {step.error && (
                  <div className="step-error">
                    <strong>Error:</strong> {step.error}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {messages.length > 0 && (
        <div className="messages-section">
          <h3>What They'll Receive</h3>
          <div className="messages-list">
            {messages.map((step, index) => {
              const data = step.result.data;
              if (step.tool === 'send_welcome_email') {
                return (
                  <div key={index} className="message-card">
                    <span className="message-kind">📧 Email &middot; {data.to}</span>
                    <p className="message-subject">{data.subject}</p>
                    <pre className="message-body">{data.body}</pre>
                  </div>
                );
              }
              if (step.tool === 'send_slack_message') {
                return (
                  <div key={index} className="message-card">
                    <span className="message-kind">💬 Slack &middot; {data.channel}</span>
                    <p className="message-body-inline">{data.text}</p>
                  </div>
                );
              }
              if (step.tool === 'schedule_meeting') {
                return (
                  <div key={index} className="message-card">
                    <span className="message-kind">📅 Calendar invite</span>
                    <p className="message-subject">{data.summary}</p>
                    <p className="message-body-inline">
                      {new Date(data.start).toLocaleString(undefined, {
                        weekday: 'short',
                        month: 'short',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                      })}
                      {data.attendees?.length ? ` · ${data.attendees.map((a: any) => a.email).join(', ')}` : ''}
                    </p>
                  </div>
                );
              }
              return null;
            })}
          </div>
        </div>
      )}

      {timeline.length > 0 && (
        <div className="timeline-section">
          <h3>Onboarding Timeline</h3>
          <p className="timeline-caption">
            Everything below executed instantly for this demo. In production these would fire
            on the schedule shown, not all at once.
          </p>
          <div className="timeline-list">
            {timeline.map((entry, index) => (
              <div key={index} className="timeline-item">
                <span className="timeline-when">{relativeDay(entry.when)}</span>
                <span className="timeline-label">{entry.label}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {workflow.error && (
        <div className="error-section">
          <h3>Error</h3>
          <p className="error-text">{workflow.error}</p>
        </div>
      )}
    </div>
  );
}
