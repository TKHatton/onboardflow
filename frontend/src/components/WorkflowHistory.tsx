import { useEffect, useState } from 'react';
import { onboardAPI } from '../api';
import type { WorkflowSummary } from '../types';
import './WorkflowHistory.css';

export function WorkflowHistory() {
  const [workflows, setWorkflows] = useState<WorkflowSummary[]>([]);
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');

  const load = () => {
    setStatus('loading');
    onboardAPI
      .getWorkflows()
      .then((data) => {
        setWorkflows(data);
        setStatus('ready');
      })
      .catch(() => setStatus('error'));
  };

  useEffect(() => {
    load();
  }, []);

  const formatDate = (iso: string | null) => {
    if (!iso) return '–';
    return new Date(iso).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  return (
    <div className="workflow-history">
      <div className="workflow-history-header">
        <div>
          <h3>Past Onboardings</h3>
          <p>Every run below is a real record persisted in Firestore, not sample data.</p>
        </div>
        <button className="refresh-btn" onClick={load} disabled={status === 'loading'}>
          Refresh
        </button>
      </div>

      {status === 'loading' && <p className="history-empty">Loading...</p>}

      {status === 'error' && (
        <p className="history-empty">Couldn't reach the history endpoint. Try refreshing.</p>
      )}

      {status === 'ready' && workflows.length === 0 && (
        <p className="history-empty">
          No onboardings recorded yet. Run one from the Onboarding Workflow tab, then check back
          here.
        </p>
      )}

      {status === 'ready' && workflows.length > 0 && (
        <div className="history-list">
          {workflows.map((wf) => (
            <div key={wf.workflow_id} className={`history-item history-${wf.status}`}>
              <div className="history-main">
                <span className="history-name">{wf.employee_name}</span>
                <span className="history-role">
                  {wf.role} &middot; {wf.department}
                </span>
              </div>
              <div className="history-meta">
                <span className={`history-status-badge history-status-${wf.status}`}>
                  {wf.status.replace('_', ' ')}
                </span>
                <span className="history-steps">{wf.step_count} steps</span>
                <span className="history-time">{formatDate(wf.started_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
