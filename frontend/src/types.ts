export interface NewHireData {
  employee_name: string;
  role: string;
  department: string;
  start_date: string;
  email: string;
  manager?: string;
  preferred_name?: string;
  pronouns?: string;
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
  workflow_id?: string;
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
  workflow_id?: string;
  reasoning?: string;
  steps_planned?: number;
  steps: WorkflowStep[];
  current_step?: number;
  error?: string;
}

export interface WorkflowSummary {
  workflow_id: string;
  employee_name: string;
  preferred_name?: string | null;
  role: string;
  department: string;
  status: 'in_progress' | 'completed' | 'failed';
  started_at: string;
  completed_at: string | null;
  step_count: number;
}

export interface WorkflowDetailStep {
  tool: string;
  action: string;
  success: boolean;
  result: any;
  completed_at: string;
}

export interface WorkflowDetail {
  workflow_id: string;
  employee_name: string;
  preferred_name?: string | null;
  pronouns?: string | null;
  reasoning?: string | null;
  role: string;
  department: string;
  start_date: string;
  email: string;
  status: 'in_progress' | 'completed' | 'failed';
  started_at: string;
  completed_at: string | null;
  steps: WorkflowDetailStep[];
}
