import { useState, useEffect } from 'react';
import { NewHireForm } from './components/NewHireForm';
import { WorkflowDashboard } from './components/WorkflowDashboard';
import { Chatbot } from './components/Chatbot';
import { WorkflowHistory } from './components/WorkflowHistory';
import { NewHireChecklist } from './components/NewHireChecklist';
import { onboardAPI } from './api';
import type { NewHireData, WorkflowState, WorkflowUpdate } from './types';
import './App.css';

function App() {
  const [workflow, setWorkflow] = useState<WorkflowState>({
    phase: 'idle',
    steps: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [currentEmployee, setCurrentEmployee] = useState<NewHireData | null>(null);
  const [activeTab, setActiveTab] = useState<'onboarding' | 'history'>('onboarding');
  const [viewMode, setViewMode] = useState<'hr' | 'employee'>('hr');

  useEffect(() => {
    const checkHealth = async () => {
      const isOnline = await onboardAPI.healthCheck();
      setApiStatus(isOnline ? 'online' : 'offline');
    };
    checkHealth();
  }, []);

  const handleStartOnboarding = async (data: NewHireData) => {
    setIsLoading(true);
    setCurrentEmployee(data);
    setWorkflow({
      phase: 'reasoning',
      steps: [],
    });

    const eventSource = onboardAPI.streamWorkflow(data, (update: WorkflowUpdate) => {
      console.log('Workflow update:', update);

      if (update.type === 'reasoning_start') {
        setWorkflow((prev) => ({
          ...prev,
          phase: 'reasoning',
        }));
      } else if (update.type === 'reasoning_complete') {
        setWorkflow((prev) => ({
          ...prev,
          phase: 'executing',
          reasoning: update.reasoning,
          steps_planned: update.steps_planned,
        }));
      } else if (update.type === 'step_start') {
        setWorkflow((prev) => ({
          ...prev,
          current_step: update.step,
          steps: [
            ...prev.steps,
            {
              step: update.step!,
              action: update.action!,
              tool: update.tool!,
              status: 'running',
            },
          ],
        }));
      } else if (update.type === 'step_complete') {
        setWorkflow((prev) => ({
          ...prev,
          steps: prev.steps.map((s) =>
            s.step === update.step
              ? { ...s, status: 'completed', result: update.result }
              : s
          ),
        }));
      } else if (update.type === 'step_error') {
        setWorkflow((prev) => ({
          ...prev,
          steps: prev.steps.map((s) =>
            s.step === update.step
              ? { ...s, status: 'failed', error: update.error }
              : s
          ),
        }));
      } else if (update.type === 'workflow_complete') {
        setWorkflow((prev) => ({
          ...prev,
          phase: 'complete',
        }));
        setIsLoading(false);
      } else if (update.type === 'error') {
        setWorkflow((prev) => ({
          ...prev,
          phase: 'error',
          error: update.error,
        }));
        setIsLoading(false);
      }
    });

    // Cleanup on unmount
    return () => {
      eventSource.close();
    };
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 OnboardFlow</h1>
        <p>Autonomous Employee Onboarding with AI</p>
        <div className={`api-status ${apiStatus}`}>
          API: {apiStatus === 'checking' ? 'Checking...' : apiStatus === 'online' ? '✅ Online' : '❌ Offline'}
        </div>
        <div className="view-switcher">
          <span className="view-switcher-label">Viewing as:</span>
          <button
            className={viewMode === 'hr' ? 'active' : ''}
            onClick={() => setViewMode('hr')}
          >
            🧑‍💼 HR Team
          </button>
          <button
            className={viewMode === 'employee' ? 'active' : ''}
            onClick={() => setViewMode('employee')}
          >
            👤 New Hire
          </button>
        </div>
      </header>

      <main className="app-main">
        {viewMode === 'hr' && (
          <>
            <div className="tab-navigation">
              <button
                className={activeTab === 'onboarding' ? 'active' : ''}
                onClick={() => setActiveTab('onboarding')}
              >
                📋 Onboarding Workflow
              </button>
              <button
                className={activeTab === 'history' ? 'active' : ''}
                onClick={() => setActiveTab('history')}
              >
                📨 Onboarding Activity
              </button>
            </div>

            {activeTab === 'onboarding' && (
              <>
                <div className="form-section">
                  <NewHireForm onSubmit={handleStartOnboarding} isLoading={isLoading} />
                </div>

                {workflow.phase !== 'idle' && (
                  <div className="dashboard-section">
                    <WorkflowDashboard workflow={workflow} />
                  </div>
                )}
              </>
            )}

            {activeTab === 'history' && (
              <div className="history-section">
                <WorkflowHistory />
              </div>
            )}
          </>
        )}

        {viewMode === 'employee' && (
          <div className="employee-portal">
            <div className="employee-portal-banner">This is what the new hire sees. No admin tools, no other employees' data, just their own onboarding assistant.</div>
            {currentEmployee ? (
              <>
                <div className="employee-portal-greeting">
                  <h2>
                    Welcome, {currentEmployee.preferred_name || currentEmployee.employee_name}
                  </h2>
                  <p>
                    {currentEmployee.role} &middot; {currentEmployee.department}
                  </p>
                </div>
                {workflow.steps.length > 0 && (
                  <NewHireChecklist steps={workflow.steps} startDate={currentEmployee.start_date} />
                )}
                <div className="chatbot-section">
                  <Chatbot
                    employeeName={currentEmployee.preferred_name || currentEmployee.employee_name}
                    employeeContext={{
                      role: currentEmployee.role,
                      department: currentEmployee.department,
                      start_date: currentEmployee.start_date,
                    }}
                  />
                </div>
              </>
            ) : (
              <p className="employee-portal-empty">
                No onboarding has been started yet this session. Switch to the HR view, submit
                the form, then come back here to see the new hire's side of it.
              </p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
