import { useEffect, useState } from 'react';
import { onboardAPI } from '../api';
import type { WorkflowSummary, WorkflowDetail, WorkflowState } from '../types';
import { WorkflowDashboard } from './WorkflowDashboard';
import './WorkflowHistory.css';

function detailToWorkflowState(detail: WorkflowDetail): WorkflowState {
  return {
    phase: detail.status === 'completed' ? 'complete' : detail.status === 'failed' ? 'error' : 'executing',
    reasoning: detail.reasoning || undefined,
    error: detail.status === 'failed' ? 'This workflow did not finish successfully.' : undefined,
    steps: detail.steps.map((s, i) => ({
      step: i + 1,
      action: s.action,
      tool: s.tool,
      status: s.success ? 'completed' : 'failed',
      result: s.success ? s.result : undefined,
      error: s.success ? undefined : s.result?.error,
    })),
  };
}

export function WorkflowHistory() {
  const [workflows, setWorkflows] = useState<WorkflowSummary[]>([]);
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<WorkflowDetail | null>(null);
  const [detailStatus, setDetailStatus] = useState<'loading' | 'ready' | 'error'>('loading');

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

  const openDetail = (workflowId: string) => {
    setSelectedId(workflowId);
    setDetailStatus('loading');
    onboardAPI
      .getWorkflowDetail(workflowId)
      .then((data) => {
        setDetail(data);
        setDetailStatus('ready');
      })
      .catch(() => setDetailStatus('error'));
  };

  const formatDate = (iso: string | null) => {
    if (!iso) return '–';
    return new Date(iso).toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  if (selectedId) {
    return (
      <div className="workflow-history">
        <div className="workflow-history-header">
          <div>
            <button className="back-btn" onClick={() => setSelectedId(null)}>
              ← Back to activity log
            </button>
          </div>
        </div>

        {detailStatus === 'loading' && <p className="history-empty">Loading...</p>}
        {detailStatus === 'error' && <p className="history-empty">Couldn't load this record.</p>}
        {detailStatus === 'ready' && detail && (
          <>
            <div className="detail-identity">
              <span className="detail-name">
                {detail.preferred_name || detail.employee_name}
                {detail.preferred_name && detail.preferred_name !== detail.employee_name && (
                  <span className="detail-legal-name"> ({detail.employee_name})</span>
                )}
              </span>
              <span className="detail-meta">
                {detail.role} &middot; {detail.department}
                {detail.pronouns ? ` · ${detail.pronouns}` : ''}
              </span>
            </div>
            <WorkflowDashboard workflow={detailToWorkflowState(detail)} />
          </>
        )}
      </div>
    );
  }

  return (
    <div className="workflow-history">
      <div className="workflow-history-header">
        <div>
          <h3>Onboarding Activity</h3>
          <p>
            What was sent to each new hire and when, pulled from Firestore. Click any entry
            for the full detail.
          </p>
        </div>
        <button className="refresh-btn" onClick={load} disabled={status === 'loading'}>
          Refresh
        </button>
      </div>

      {status === 'loading' && <p className="history-empty">Loading...</p>}

      {status === 'error' && (
        <p className="history-empty">Couldn't reach the activity log. Try refreshing.</p>
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
            <button
              key={wf.workflow_id}
              className={`history-item history-${wf.status}`}
              onClick={() => openDetail(wf.workflow_id)}
            >
              <div className="history-main">
                <span className="history-name">{wf.preferred_name || wf.employee_name}</span>
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
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
