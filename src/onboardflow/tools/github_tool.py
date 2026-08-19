"""GitHub tool - creates accounts and sets up access."""

from datetime import datetime


def create_github_account(
    employee_name: str,
    role: str,
    email: str,
    repositories: list[str] | None = None,
) -> dict:
    """Create GitHub account and configure repository access.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        email: Employee email address
        repositories: List of repos to grant access to
    
    Returns:
        dict with account details
    """
    # Generate username from name
    username = employee_name.lower().replace(" ", ".").replace("'", "")
    
    # Default repos based on role
    if repositories is None:
        if "engineer" in role.lower() or "developer" in role.lower():
            repositories = ["frontend", "backend", "infrastructure", "docs"]
        elif "data" in role.lower():
            repositories = ["data-pipelines", "analytics", "ml-models", "docs"]
        else:
            repositories = ["docs", "marketing-assets"]
    
    account_id = f"gh-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    account_data = {
        "account_id": account_id,
        "username": username,
        "email": email,
        "role": role,
        "repositories": repositories,
        "teams": ["engineering"] if "engineer" in role.lower() else ["contributors"],
        "two_factor_enabled": True,
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[GITHUB] Created account {username} with access to: {', '.join(repositories)}")
    
    return {
        "success": True,
        "account_id": account_id,
        "data": account_data,
    }
