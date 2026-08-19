import axios from 'axios';
import type { NewHireData, WorkflowUpdate } from './types';

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

    eventSource.onmessage = (event) => {
      try {
        const update: WorkflowUpdate = JSON.parse(event.data);
        onEvent(update);
      } catch (error) {
        console.error('Failed to parse workflow update:', error);
      }
    };

    eventSource.onerror = (error) => {
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
};
