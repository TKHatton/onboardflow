"""Benefits Enrollment tool - health insurance and perks."""

from datetime import datetime, timedelta


def enroll_in_benefits(
    employee_name: str,
    email: str,
    start_date: str,
) -> dict:
    """Enroll new hire in benefits and perks programs.
    
    Args:
        employee_name: Name of the new hire
        email: Employee email
        start_date: Employee start date
    
    Returns:
        dict with enrollment details
    """
    # Standard benefits package
    benefits = {
        "health_insurance": {
            "provider": "BlueCross BlueShield",
            "plans": ["PPO", "HSA"],
            "enrollment_deadline_days": 30,
            "status": "pending_enrollment",
        },
        "dental_insurance": {
            "provider": "Delta Dental",
            "enrollment_deadline_days": 30,
            "status": "pending_enrollment",
        },
        "vision_insurance": {
            "provider": "VSP",
            "enrollment_deadline_days": 30,
            "status": "pending_enrollment",
        },
        "retirement": {
            "provider": "Fidelity 401k",
            "company_match": "4% match",
            "vesting_period": "4 years",
            "enrollment_deadline_days": 60,
            "status": "pending_enrollment",
        },
        "perks": [
            "Gym membership reimbursement ($50/month)",
            "Professional development budget ($1000/year)",
            "Commuter benefits",
            "Employee assistance program",
        ]
    }
    
    # Calculate enrollment deadline
    start_dt = datetime.fromisoformat(start_date)
    enrollment_deadline = start_dt + timedelta(days=30)
    
    enrollment_id = f"benefits-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    enrollment_data = {
        "enrollment_id": enrollment_id,
        "employee_name": employee_name,
        "email": email,
        "start_date": start_date,
        "benefits": benefits,
        "enrollment_deadline": enrollment_deadline.isoformat(),
        "welcome_kit_sent": True,
        "benefits_portal_access": True,
        "hr_contact": "benefits@company.com",
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[BENEFITS] Sent enrollment info to {employee_name} (deadline: {enrollment_deadline.strftime('%Y-%m-%d')})")
    
    return {
        "success": True,
        "enrollment_id": enrollment_id,
        "data": enrollment_data,
    }
