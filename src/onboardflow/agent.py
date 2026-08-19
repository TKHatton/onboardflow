"""OnboardFlow Agent - Orchestrates employee onboarding workflow."""

import os
import json
from datetime import datetime, timedelta
from typing import Optional

from .tools import (
    create_jira_ticket,
    send_slack_message,
    schedule_meeting,
    send_welcome_email,
)
from .state_tracker import StateTracker


class OnboardFlowAgent:
    """Autonomous onboarding workflow agent."""
    
    def __init__(self):
        self.tools = [
            create_jira_ticket,
            send_slack_message,
            schedule_meeting,
            send_welcome_email,
        ]
        self._adk_agent = None
        self.state_tracker = StateTracker()
    
    def _get_adk_agent(self):
        """Lazy-load ADK agent (requires API key)."""
        if self._adk_agent is None:
            from google.adk.agents import Agent
            from google.adk.tools import FunctionTool
            
            self._adk_agent = Agent(
                model="gemini-3.5-flash",
                name="onboardflow_agent",
                description="Autonomous employee onboarding workflow agent",
                instruction=self._get_instruction(),
                tools=[FunctionTool(tool) for tool in self.tools],
            )
        return self._adk_agent
    
    def _get_instruction(self) -> str:
        """Get the agent's system instruction."""
        return """You are OnboardFlow, an autonomous employee onboarding agent.

When you receive a new hire event, you must execute the complete onboarding workflow:

1. Create a Jira ticket for the onboarding process
2. Send a welcome message to the team Slack channel
3. Schedule an orientation meeting with the new hire and their manager
4. Send a welcome email to the new hire

For each step:
- Use the appropriate tool
- Wait for confirmation before proceeding
- Track what was completed

If any step fails, log the error but continue with remaining steps.

Always provide a summary of what was completed at the end.
"""
    
    async def execute_onboarding(
        self,
        employee_name: str,
        role: str,
        department: str,
        start_date: str,
        email: str,
        manager: Optional[str] = None,
        manager_email: Optional[str] = None,
    ) -> dict:
        """Execute the complete onboarding workflow.
        
        Args:
            employee_name: Name of the new hire
            role: Job title/role
            department: Department name
            start_date: Start date (YYYY-MM-DD)
            email: Employee email address
            manager: Manager name (optional)
            manager_email: Manager email (optional)
        
        Returns:
            dict with workflow results
        """
        # Log workflow start to Firestore
        workflow_id = await self.state_tracker.log_workflow_start(
            employee_name=employee_name,
            role=role,
            department=department,
            start_date=start_date,
            email=email,
        )
        
        results = {
            "workflow_id": workflow_id,
            "employee_name": employee_name,
            "started_at": datetime.now().isoformat(),
            "steps": [],
        }
        
        # Step 1: Create Jira ticket
        print(f"\n=== Step 1: Creating Jira ticket for {employee_name} ===")
        jira_result = create_jira_ticket(
            employee_name=employee_name,
            role=role,
            department=department,
            start_date=start_date,
            manager=manager,
        )
        results["steps"].append({
            "step": "create_jira_ticket",
            "result": jira_result,
        })
        await self.state_tracker.log_step(workflow_id, "create_jira_ticket", jira_result["success"], jira_result)
        
        # Step 2: Send Slack welcome message
        print(f"\n=== Step 2: Sending Slack welcome message ===")
        slack_message = f"🎉 Welcome {employee_name} to the team! They're joining us as our new {role} in {department}. Say hello!"
        slack_result = send_slack_message(
            channel="#general",
            message=slack_message,
            employee_name=employee_name,
            role=role,
        )
        results["steps"].append({
            "step": "send_slack_message",
            "result": slack_result,
        })
        await self.state_tracker.log_step(workflow_id, "send_slack_message", slack_result["success"], slack_result)
        
        # Step 3: Schedule orientation meeting
        print(f"\n=== Step 3: Scheduling orientation meeting ===")
        # Schedule for start date at 10:00 AM
        meeting_time = f"{start_date}T10:00:00"
        attendees = [email]
        if manager_email:
            attendees.append(manager_email)
        
        calendar_result = schedule_meeting(
            title=f"Orientation: {employee_name}",
            attendees=attendees,
            start_time=meeting_time,
            duration_minutes=60,
            description=f"Welcome orientation for {employee_name} ({role})",
        )
        results["steps"].append({
            "step": "schedule_meeting",
            "result": calendar_result,
        })
        await self.state_tracker.log_step(workflow_id, "schedule_meeting", calendar_result["success"], calendar_result)
        
        # Step 4: Send welcome email
        print(f"\n=== Step 4: Sending welcome email ===")
        email_result = send_welcome_email(
            to_email=email,
            employee_name=employee_name,
            role=role,
            start_date=start_date,
            manager_name=manager,
        )
        results["steps"].append({
            "step": "send_welcome_email",
            "result": email_result,
        })
        await self.state_tracker.log_step(workflow_id, "send_welcome_email", email_result["success"], email_result)
        
        results["completed_at"] = datetime.now().isoformat()
        results["status"] = "completed"
        
        # Log workflow completion to Firestore
        await self.state_tracker.log_workflow_complete(workflow_id)
        
        print(f"\n=== Onboarding workflow completed for {employee_name} ===")
        
        return results


# Create global agent instance
agent = OnboardFlowAgent()
