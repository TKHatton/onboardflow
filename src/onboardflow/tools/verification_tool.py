"""Follow-up Verification tool - checks completion status."""

from datetime import datetime, timedelta
import json


def verify_onboarding_completion(
    employee_name: str,
    email: str,
    days_after_start: int = 7,
) -> dict:
    """Verify onboarding tasks completion and send follow-ups.
    
    Args:
        employee_name: Name of the new hire
        email: Employee email
        days_after_start: Days after start date to check
    
    Returns:
        dict with verification results and follow-up actions
    """
    # Checklist of items to verify
    verification_items = [
        {
            "task": "Equipment received",
            "category": "equipment",
            "verification_method": "email_survey",
            "status": "pending_verification",
        },
        {
            "task": "System access working (email, Slack, etc.)",
            "category": "access",
            "verification_method": "automated_check",
            "status": "pending_verification",
        },
        {
            "task": "Security training completed",
            "category": "training",
            "verification_method": "lms_check",
            "status": "pending_verification",
        },
        {
            "task": "Benefits enrollment started",
            "category": "benefits",
            "verification_method": "hr_system_check",
            "status": "pending_verification",
        },
        {
            "task": "First team meeting attended",
            "category": "integration",
            "verification_method": "manager_checkin",
            "status": "pending_verification",
        },
        {
            "task": "Role-specific training progress",
            "category": "training",
            "verification_method": "lms_check",
            "status": "pending_verification",
        },
    ]
    
    # Simulate verification results
    verified_items = []
    pending_items = []
    
    for item in verification_items:
        # Simulate 80% completion rate
        if hash(f"{employee_name}{item['task']}") % 10 < 8:
            item["status"] = "verified"
            item["verified_at"] = datetime.now().isoformat()
            verified_items.append(item)
        else:
            item["status"] = "pending"
            pending_items.append(item)
    
    # Generate follow-up actions
    follow_ups = []
    
    if pending_items:
        follow_ups.append({
            "action": "send_checkin_email",
            "to": email,
            "subject": f"Checking in on your onboarding, {employee_name}",
            "message": f"Hi {employee_name}, just checking in on your onboarding progress. Please complete the following: {', '.join([item['task'] for item in pending_items])}",
            "scheduled_for": (datetime.now() + timedelta(days=1)).isoformat(),
        })
        
        follow_ups.append({
            "action": "notify_manager",
            "message": f"{employee_name} has pending onboarding items. Please schedule a check-in meeting.",
            "channel": "manager_notifications",
        })
    
    # Schedule 30-day check-in
    follow_ups.append({
        "action": "schedule_checkin_meeting",
        "participants": [employee_name, "manager", "hr_buddy"],
        "purpose": "30-day onboarding review",
        "scheduled_for": (datetime.now() + timedelta(days=30 - days_after_start)).isoformat(),
    })
    
    verification_id = f"verify-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    verification_data = {
        "verification_id": verification_id,
        "employee_name": employee_name,
        "email": email,
        "days_after_start": days_after_start,
        "total_items": len(verification_items),
        "verified_items": len(verified_items),
        "pending_items": len(pending_items),
        "completion_rate": f"{(len(verified_items) / len(verification_items) * 100):.1f}%",
        "verification_results": verification_items,
        "follow_up_actions": follow_ups,
        "verified_at": datetime.now().isoformat(),
    }
    
    print(f"[VERIFICATION] Checked {len(verification_items)} items for {employee_name}: {len(verified_items)} complete, {len(pending_items)} pending")
    
    return {
        "success": True,
        "verification_id": verification_id,
        "data": verification_data,
    }
