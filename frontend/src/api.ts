import axios from 'axios';
import type { NewHireData, WorkflowUpdate, WorkflowSummary } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const onboardAPI = {
  startWorkflow: async (data: NewHireData): Promise<string> => {
    const response = await api.post('/api/onboard', data);
    return response.data.workflow_id;
  },

  streamWorkflow: (data: NewHireData, onEvent: (event: WorkflowUpdate) => void): EventSource => {
    const params = new URLSearchParams({
      employee_name: data.employee_name,
      role: data.role,
      department: data.department,
      start_date: data.start_date,
      email: data.email,
      manager: data.manager || '',
    });

    const eventSource = new EventSource(`${API_BASE_URL}/api/onboard/stream?${params}`);
    let finished = false;

    eventSource.onmessage = (event) => {
      try {
        const update: WorkflowUpdate = JSON.parse(event.data);
        if (update.type === 'workflow_complete' || update.type === 'error') {
          finished = true;
        }
        onEvent(update);
        if (finished) {
          eventSource.close();
        }
      } catch (error) {
        console.error('Failed to parse workflow update:', error);
      }
    };

    eventSource.onerror = (error) => {
      // The backend closes the stream once it's done sending events, which
      // makes the browser's EventSource fire onerror even on a clean finish.
      // Only treat this as a real error if we hadn't already reached a
      // terminal event.
      if (finished) {
        return;
      }
      console.error('EventSource error:', error);
      onEvent({
        type: 'error',
        error: 'Connection lost to server',
      });
      eventSource.close();
    };

    return eventSource;
  },

  chat: async (employeeName: string, question: string, context?: any): Promise<any> => {
    const response = await api.post('/api/chat', {
      employee_name: employeeName,
      question: question,
      context: context,
    });
    return response.data;
  },

  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await api.get('/');
      return response.status === 200;
    } catch {
      return false;
    }
  },

  getWorkflows: async (): Promise<WorkflowSummary[]> => {
    const response = await api.get('/api/workflows');
    return response.data.workflows;
  },
};
