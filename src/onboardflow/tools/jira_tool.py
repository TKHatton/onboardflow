"""Jira MCP tool - creates onboarding tickets."""

import os
from datetime import datetime
from typing import Optional


def create_jira_ticket(
    employee_name: str,
    role: str,
    department: str,
    start_date: str,
    manager: Optional[str] = None,
) -> dict:
    """Create a Jira ticket for employee onboarding.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        department: Department name
        start_date: Start date (YYYY-MM-DD)
        manager: Manager name (optional)
    
    Returns:
        dict with ticket_id, status, and details
    """
    # Mock implementation - in production, this would call Jira API
    ticket_id = f"ONBOARD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "summary": f"Onboarding: {employee_name} - {role}",
        "description": f"""New hire onboarding for {employee_name}.

Role: {role}
Department: {department}
Start Date: {start_date}
Manager: {manager or 'TBD'}

Onboarding checklist:
- [ ] Create accounts (email, Slack, Jira, etc.)
- [ ] Schedule orientation meeting
- [ ] Assign onboarding buddy
- [ ] Set up equipment
- [ ] Add to team channels
- [ ] Send welcome materials""",
        "project": "HR",
        "issue_type": "Task",
        "priority": "High",
        "status": "To Do",
        "created_at": datetime.now().isoformat(),
    }
    
    # Log the action
    print(f"[JIRA] Created ticket {ticket_id}: {ticket_data['summary']}")
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "data": ticket_data,
    }
