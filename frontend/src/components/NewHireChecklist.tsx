import type { WorkflowStep } from '../types';
import './NewHireChecklist.css';

interface ChecklistItem {
  label: string;
  date?: string;
}

function extractChecklist(steps: WorkflowStep[]): { done: ChecklistItem[]; todo: ChecklistItem[] } {
  const done: ChecklistItem[] = [];
  const todo: ChecklistItem[] = [];

  for (const step of steps) {
    if (step.status !== 'completed') continue;
    const data = step.result?.data;
    if (!data) continue;

    switch (step.tool) {
      case 'provision_equipment':
        done.push({ label: 'Equipment ordered', date: data.estimated_delivery });
        break;
      case 'create_github_account':
        done.push({ label: 'GitHub account created' });
        break;
      case 'create_jira_ticket':
        done.push({ label: 'Onboarding tracked in Jira' });
        break;
      case 'create_asana_project':
        done.push({ label: 'Project workspace set up in Asana' });
        break;
      case 'setup_crm_access':
        done.push({ label: 'CRM access granted' });
        break;
      case 'send_welcome_email':
        done.push({ label: 'Welcome email sent', date: data.sent_at });
        break;
      case 'send_slack_message':
        done.push({ label: 'Introduced to the team on Slack' });
        break;
      case 'schedule_meeting':
        done.push({ label: `${data.summary} scheduled`, date: data.start });
        break;
      case 'enroll_in_benefits':
        done.push({ label: 'Benefits portal access granted' });
        todo.push({ label: 'Complete benefits enrollment', date: data.enrollment_deadline });
        break;
      case 'assign_training_courses':
        todo.push({ label: 'Complete required training courses', date: data.deadline });
        break;
      case 'schedule_security_training':
        (data.training_modules || []).forEach((m: any) => {
          todo.push({ label: `Complete: ${m.name}`, date: m.deadline });
        });
        break;
      default:
        break;
    }
  }

  todo.sort((a, b) => (a.date || '').localeCompare(b.date || ''));
  return { done, todo };
}

function formatDate(iso?: string): string {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

// A plain "YYYY-MM-DD" date (no time) is parsed by `new Date()` as UTC
// midnight, which renders as the previous day in any timezone behind UTC.
// Build the Date from its parts directly instead, so it stays local.
function formatPlainDate(plainDate: string, options: Intl.DateTimeFormatOptions): string {
  const [year, month, day] = plainDate.split('-').map(Number);
  return new Date(year, month - 1, day).toLocaleDateString(undefined, options);
}

interface NewHireChecklistProps {
  steps: WorkflowStep[];
  startDate?: string;
}

export function NewHireChecklist({ steps, startDate }: NewHireChecklistProps) {
  const { done, todo } = extractChecklist(steps);
  if (done.length === 0 && todo.length === 0) return null;

  return (
    <div className="new-hire-checklist">
      <div className="checklist-header">
        <h3>Your Onboarding Checklist</h3>
        {startDate && (
          <span className="checklist-start-date">
            Start date: {formatPlainDate(startDate, { weekday: 'long', month: 'long', day: 'numeric' })}
          </span>
        )}
      </div>

      {todo.length > 0 && (
        <div className="checklist-group">
          <span className="checklist-group-label">Still on you</span>
          {todo.map((item, i) => (
            <div key={i} className="checklist-item checklist-todo">
              <span className="checklist-box">☐</span>
              <span className="checklist-label">{item.label}</span>
              {item.date && <span className="checklist-date">Due {formatDate(item.date)}</span>}
            </div>
          ))}
        </div>
      )}

      {done.length > 0 && (
        <div className="checklist-group">
          <span className="checklist-group-label">Already handled for you</span>
          {done.map((item, i) => (
            <div key={i} className="checklist-item checklist-done">
              <span className="checklist-box">✅</span>
              <span className="checklist-label">{item.label}</span>
              {item.date && <span className="checklist-date">{formatDate(item.date)}</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
