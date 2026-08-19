"""MCP tools for OnboardFlow agent."""

from .jira_tool import create_jira_ticket
from .slack_tool import send_slack_message
from .calendar_tool import schedule_meeting
from .email_tool import send_welcome_email
from .github_tool import create_github_account
from .crm_tool import setup_crm_access
from .asana_tool import create_asana_project
from .training_tool import assign_training_courses
from .equipment_tool import provision_equipment
from .security_tool import schedule_security_training
from .benefits_tool import enroll_in_benefits
from .verification_tool import verify_onboarding_completion
from .chatbot_tool import answer_onboarding_question

__all__ = [
    "create_jira_ticket",
    "send_slack_message",
    "schedule_meeting",
    "send_welcome_email",
    "create_github_account",
    "setup_crm_access",
    "create_asana_project",
    "assign_training_courses",
    "provision_equipment",
    "schedule_security_training",
    "enroll_in_benefits",
    "verify_onboarding_completion",
    "answer_onboarding_question",
]
