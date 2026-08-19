export interface NewHireData {
  employee_name: string;
  role: string;
  department: string;
  start_date: string;
  email: string;
  manager?: string;
}

export interface WorkflowStep {
  step: number;
  action: string;
  tool: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
}

export interface WorkflowUpdate {
  type: 'reasoning_start' | 'reasoning_complete' | 'step_start' | 'step_complete' | 'step_error' | 'workflow_complete' | 'error';
  message?: string;
  reasoning?: string;
  steps_planned?: number;
  step?: number;
  action?: string;
  tool?: string;
  result?: any;
  error?: string;
  total_steps?: number;
}

export interface WorkflowState {
  phase: 'idle' | 'reasoning' | 'executing' | 'complete' | 'error';
  reasoning?: string;
  steps_planned?: number;
  steps: WorkflowStep[];
  current_step?: number;
  error?: string;
}
