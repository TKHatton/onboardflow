"""CRM tool - sets up CRM access for sales roles."""

from datetime import datetime


def setup_crm_access(
    employee_name: str,
    role: str,
    email: str,
    manager: str | None = None,
) -> dict:
    """Set up CRM access for sales and customer-facing roles.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        email: Employee email address
        manager: Manager name
    
    Returns:
        dict with CRM account details
    """
    # Determine CRM permissions based on role
    if "manager" in role.lower() or "director" in role.lower():
        permissions = ["full_access", "team_view", "reports", "admin"]
        territory = "All"
    elif "account" in role.lower() or "sales" in role.lower():
        permissions = ["full_access", "own_accounts", "reports"]
        territory = "Assigned"
    else:
        permissions = ["read_only", "own_accounts"]
        territory = "Limited"
    
    account_id = f"crm-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    account_data = {
        "account_id": account_id,
        "email": email,
        "role": role,
        "permissions": permissions,
        "territory": territory,
        "manager": manager,
        "license_type": "Sales" if "sales" in role.lower() else "Service",
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[CRM] Set up {role} account with {', '.join(permissions)} permissions")
    
    return {
        "success": True,
        "account_id": account_id,
        "data": account_data,
    }
