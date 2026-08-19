import type { WorkflowState } from '../types';
import './WorkflowDashboard.css';

interface WorkflowDashboardProps {
  workflow: WorkflowState;
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

      {workflow.error && (
        <div className="error-section">
          <h3>Error</h3>
          <p className="error-text">{workflow.error}</p>
        </div>
      )}
    </div>
  );
}
