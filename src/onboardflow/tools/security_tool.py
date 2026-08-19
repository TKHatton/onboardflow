"""Security Training tool - mandatory compliance training."""

from datetime import datetime, timedelta


def schedule_security_training(
    employee_name: str,
    email: str,
    department: str,
) -> dict:
    """Schedule mandatory security and compliance training.
    
    Args:
        employee_name: Name of the new hire
        email: Employee email
        department: Department name
    
    Returns:
        dict with training schedule details
    """
    # All employees need these
    mandatory_training = [
        {
            "name": "Information Security Awareness",
            "duration": "2 hours",
            "deadline_days": 7,
            "priority": "critical",
        },
        {
            "name": "Data Privacy & GDPR",
            "duration": "1.5 hours",
            "deadline_days": 14,
            "priority": "high",
        },
        {
            "name": "Workplace Harassment Prevention",
            "duration": "1 hour",
            "deadline_days": 30,
            "priority": "medium",
        },
    ]
    
    # Department-specific additions
    if department.lower() in ["engineering", "data", "it"]:
        mandatory_training.append({
            "name": "Secure Coding Practices",
            "duration": "3 hours",
            "deadline_days": 30,
            "priority": "high",
        })
    elif department.lower() in ["sales", "marketing"]:
        mandatory_training.append({
            "name": "Customer Data Handling",
            "duration": "2 hours",
            "deadline_days": 21,
            "priority": "high",
        })
    
    # Calculate deadlines
    start_date = datetime.now()
    training_schedule = []
    
    for course in mandatory_training:
        deadline = start_date + timedelta(days=course["deadline_days"])
        training_schedule.append({
            **course,
            "deadline": deadline.isoformat(),
            "assigned": True,
        })
    
    schedule_id = f"security-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    schedule_data = {
        "schedule_id": schedule_id,
        "employee_name": employee_name,
        "email": email,
        "department": department,
        "training_modules": training_schedule,
        "total_modules": len(training_schedule),
        "platform": "Compliance LMS",
        "reminder_emails": True,
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[SECURITY] Scheduled {len(training_schedule)} compliance modules for {employee_name}")
    
    return {
        "success": True,
        "schedule_id": schedule_id,
        "data": schedule_data,
    }
