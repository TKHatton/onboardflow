"""Google Calendar MCP tool - schedules meetings."""

import os
from datetime import datetime, timedelta
from typing import Optional


def schedule_meeting(
    title: str,
    attendees: list[str],
    start_time: str,
    duration_minutes: int = 30,
    description: Optional[str] = None,
) -> dict:
    """Schedule a meeting on Google Calendar.
    
    Args:
        title: Meeting title
        attendees: List of email addresses
        start_time: Start time (ISO format: YYYY-MM-DDTHH:MM:SS)
        duration_minutes: Meeting duration in minutes (default: 30)
        description: Meeting description (optional)
    
    Returns:
        dict with event_id, status, and details
    """
    # Mock implementation - in production, this would call Google Calendar API
    event_id = f"cal-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Calculate end time using timedelta
    start_dt = datetime.fromisoformat(start_time)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    
    event_data = {
        "event_id": event_id,
        "summary": title,
        "description": description or "",
        "start": start_time,
        "end": end_dt.isoformat(),
        "attendees": [{"email": email} for email in attendees],
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
    }
    
    # Log the action
    print(f"[CALENDAR] Scheduled meeting: {title} at {start_time}")
    
    return {
        "success": True,
        "event_id": event_id,
        "data": event_data,
    }
