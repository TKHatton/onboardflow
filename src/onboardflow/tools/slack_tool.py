"""Slack MCP tool - sends welcome messages."""

import os
from datetime import datetime
from typing import Optional


def send_slack_message(
    channel: str,
    message: str,
    employee_name: str,
    role: str,
) -> dict:
    """Send a welcome message to Slack.
    
    Args:
        channel: Slack channel name (e.g., "#general")
        message: Message text
        employee_name: Name of the new hire
        role: Job title/role
    
    Returns:
        dict with message_id, status, and details
    """
    # Mock implementation - in production, this would call Slack API
    message_id = f"slack-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    message_data = {
        "message_id": message_id,
        "channel": channel,
        "text": message,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "employee_name": employee_name,
            "role": role,
            "message_type": "welcome",
        },
    }
    
    # Log the action
    print(f"[SLACK] Sent message to {channel}: {message[:100]}...")
    
    return {
        "success": True,
        "message_id": message_id,
        "data": message_data,
    }
