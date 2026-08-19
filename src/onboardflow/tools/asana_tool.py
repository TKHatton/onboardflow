"""Asana tool - creates projects for marketing and creative work."""

from datetime import datetime


def create_asana_project(
    employee_name: str,
    role: str,
    department: str,
    manager: str | None = None,
) -> dict:
    """Create Asana project for marketing and creative work.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        department: Department name
        manager: Manager name
    
    Returns:
        dict with project details
    """
    # Determine project template based on role
    if "designer" in role.lower() or "creative" in role.lower():
        template = "Creative Projects"
        sections = ["Design Requests", "In Progress", "Review", "Completed"]
    elif "marketing" in role.lower() or "content" in role.lower():
        template = "Marketing Campaigns"
        sections = ["Campaign Ideas", "Planning", "In Production", "Published", "Analytics"]
    else:
        template = "General Projects"
        sections = ["Backlog", "To Do", "In Progress", "Done"]
    
    project_id = f"asana-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    project_data = {
        "project_id": project_id,
        "name": f"{employee_name} - {role}",
        "template": template,
        "department": department,
        "sections": sections,
        "manager": manager,
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[ASANA] Created {template} project for {employee_name}")
    
    return {
        "success": True,
        "project_id": project_id,
        "data": project_data,
    }
