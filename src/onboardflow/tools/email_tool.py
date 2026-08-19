"""Email MCP tool - sends welcome emails."""

import os
from datetime import datetime
from typing import Optional


def send_welcome_email(
    to_email: str,
    employee_name: str,
    role: str,
    start_date: str,
    manager_name: Optional[str] = None,
) -> dict:
    """Send a welcome email to the new hire.
    
    Args:
        to_email: Recipient email address
        employee_name: Name of the new hire
        role: Job title/role
        start_date: Start date (YYYY-MM-DD)
        manager_name: Manager name (optional)
    
    Returns:
        dict with message_id, status, and details
    """
    # Mock implementation - in production, this would send email via SMTP/API
    message_id = f"email-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    subject = f"Welcome to the team, {employee_name}!"
    
    body = f"""Hi {employee_name},

Welcome aboard! We're excited to have you join us as our new {role}.

Your start date is {start_date}. Here's what to expect:

- Your manager{f' ({manager_name})' if manager_name else ''} will reach out to schedule your first day
- You'll receive access to our systems (Slack, Jira, etc.)
- We'll have an orientation session to get you up to speed

If you have any questions before your start date, don't hesitate to reach out.

Looking forward to working with you!

Best regards,
The HR Team
"""
    
    email_data = {
        "message_id": message_id,
        "to": to_email,
        "subject": subject,
        "body": body,
        "sent_at": datetime.now().isoformat(),
        "metadata": {
            "employee_name": employee_name,
            "role": role,
            "start_date": start_date,
        },
    }
    
    # Log the action
    print(f"[EMAIL] Sent welcome email to {to_email}")
    
    return {
        "success": True,
        "message_id": message_id,
        "data": email_data,
    }
