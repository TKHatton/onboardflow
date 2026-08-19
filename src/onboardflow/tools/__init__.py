"""MCP tools for OnboardFlow agent."""

from .jira_tool import create_jira_ticket
from .slack_tool import send_slack_message
from .calendar_tool import schedule_meeting
from .email_tool import send_welcome_email
from .github_tool import create_github_account
from .crm_tool import setup_crm_access
from .asana_tool import create_asana_project

__all__ = [
    "create_jira_ticket",
    "send_slack_message",
    "schedule_meeting",
    "send_welcome_email",
    "create_github_account",
    "setup_crm_access",
    "create_asana_project",
]
