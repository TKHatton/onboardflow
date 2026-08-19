import { useState } from 'react';
import type { NewHireData } from '../types';
import './NewHireForm.css';

interface NewHireFormProps {
  onSubmit: (data: NewHireData) => void;
  isLoading: boolean;
}

export function NewHireForm({ onSubmit, isLoading }: NewHireFormProps) {
  const [formData, setFormData] = useState<NewHireData>({
    employee_name: '',
    role: '',
    department: '',
    start_date: '',
    email: '',
    manager: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const departments = [
    'Engineering',
    'Marketing',
    'Sales',
    'Product',
    'Design',
    'HR',
    'Finance',
    'Operations',
  ];

  return (
    <div className="new-hire-form">
      <h2>New Employee Onboarding</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="employee_name">Employee Name</label>
          <input
            type="text"
            id="employee_name"
            name="employee_name"
            value={formData.employee_name}
            onChange={handleChange}
            required
            disabled={isLoading}
            placeholder="John Doe"
          />
        </div>

        <div className="form-group">
          <label htmlFor="role">Role</label>
          <input
            type="text"
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
            disabled={isLoading}
            placeholder="Software Engineer"
          />
        </div>

        <div className="form-group">
          <label htmlFor="department">Department</label>
          <select
            id="department"
            name="department"
            value={formData.department}
            onChange={handleChange}
            required
            disabled={isLoading}
          >
            <option value="">Select Department</option>
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="start_date">Start Date</label>
          <input
            type="date"
            id="start_date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={isLoading}
            placeholder="john.doe@company.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="manager">Manager (Optional)</label>
          <input
            type="text"
            id="manager"
            name="manager"
            value={formData.manager}
            onChange={handleChange}
            disabled={isLoading}
            placeholder="Jane Smith"
          />
        </div>

        <button type="submit" disabled={isLoading} className="submit-btn">
          {isLoading ? 'Processing...' : 'Start Onboarding'}
        </button>
      </form>
    </div>
  );
}
