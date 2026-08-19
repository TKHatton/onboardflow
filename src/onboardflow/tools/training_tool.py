"""Training Platform tool - assigns role-based courses."""

from datetime import datetime, timedelta


def assign_training_courses(
    employee_name: str,
    role: str,
    department: str,
    email: str,
) -> dict:
    """Assign role-based training courses to new hire.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        department: Department name
        email: Employee email
    
    Returns:
        dict with training assignment details
    """
    # Role-based training paths
    training_paths = {
        "engineering": {
            "required": [
                "Security Awareness Training",
                "Code Review Best Practices",
                "CI/CD Pipeline Overview",
                "Company Architecture Standards",
            ],
            "recommended": [
                "Advanced Git Workflows",
                "Performance Optimization",
                "Testing Strategies",
            ]
        },
        "sales": {
            "required": [
                "Product Knowledge 101",
                "Sales Methodology Training",
                "CRM Best Practices",
                "Compliance & Ethics",
            ],
            "recommended": [
                "Advanced Negotiation",
                "Customer Success Stories",
                "Competitive Analysis",
            ]
        },
        "marketing": {
            "required": [
                "Brand Guidelines",
                "Content Strategy",
                "Marketing Tools Overview",
                "Compliance & Legal",
            ],
            "recommended": [
                "SEO Best Practices",
                "Social Media Strategy",
                "Analytics & Reporting",
            ]
        },
        "default": {
            "required": [
                "Company Overview",
                "Security Awareness",
                "HR Policies",
                "IT Setup Guide",
            ],
            "recommended": [
                "Team Building",
                "Communication Best Practices",
            ]
        }
    }
    
    # Get training path based on department
    dept_key = department.lower()
    path = training_paths.get(dept_key, training_paths["default"])
    
    # Calculate completion deadline (30 days from now)
    start_date = datetime.now()
    deadline = start_date + timedelta(days=30)
    
    assignment_id = f"training-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    assignment_data = {
        "assignment_id": assignment_id,
        "employee_name": employee_name,
        "email": email,
        "role": role,
        "department": department,
        "required_courses": path["required"],
        "recommended_courses": path["recommended"],
        "deadline": deadline.isoformat(),
        "platform": "Company LMS",
        "login_credentials_sent": True,
        "created_at": datetime.now().isoformat(),
    }
    
    total_courses = len(path["required"]) + len(path["recommended"])
    print(f"[TRAINING] Assigned {total_courses} courses to {employee_name} (deadline: {deadline.strftime('%Y-%m-%d')})")
    
    return {
        "success": True,
        "assignment_id": assignment_id,
        "data": assignment_data,
    }
