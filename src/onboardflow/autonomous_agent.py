"""Autonomous OnboardFlow Agent with real Gemini reasoning."""

import os
import json
import asyncio
from typing import AsyncGenerator
from dataclasses import dataclass
from google import genai
from google.genai import types

from .tools import (
    create_jira_ticket,
    create_github_account,
    send_slack_message,
    schedule_meeting,
    send_welcome_email,
    setup_crm_access,
    create_asana_project,
)


@dataclass
class WorkflowStep:
    """A step in the onboarding workflow."""
    action: str
    tool: str
    reasoning: str
    status: str = "pending"
    result: dict | None = None


class AutonomousAgent:
    """Agent that uses Gemini to autonomously decide onboarding steps."""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
        
        # Available tools with descriptions
        self.tools = {
            "create_jira_ticket": {
                "func": create_jira_ticket,
                "description": "Create a Jira ticket for task tracking and project management"
            },
            "create_github_account": {
                "func": create_github_account,
                "description": "Create GitHub account and add to repositories"
            },
            "send_slack_message": {
                "func": send_slack_message,
                "description": "Send a welcome message to Slack channels"
            },
            "schedule_meeting": {
                "func": schedule_meeting,
                "description": "Schedule orientation and welcome meetings"
            },
            "send_welcome_email": {
                "func": send_welcome_email,
                "description": "Send welcome email with resources and next steps"
            },
            "setup_crm_access": {
                "func": setup_crm_access,
                "description": "Set up CRM access for sales and customer-facing roles"
            },
            "create_asana_project": {
                "func": create_asana_project,
                "description": "Create Asana project for marketing and creative work"
            },
        }
    
    async def plan_onboarding(
        self,
        employee_name: str,
        role: str,
        department: str,
        start_date: str,
        email: str,
        manager: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """
        Use Gemini to autonomously plan and execute onboarding workflow.
        Yields real-time updates as the agent reasons and executes.
        """
        
        # Step 1: Gemini reasons about what steps to take
        yield {
            "type": "reasoning_start",
            "message": f"Analyzing onboarding requirements for {role} in {department}..."
        }
        
        planning_prompt = f"""You are an autonomous onboarding agent. Based on the new hire details below, decide what steps to take.

New Hire Details:
- Name: {employee_name}
- Role: {role}
- Department: {department}
- Start Date: {start_date}
- Email: {email}
- Manager: {manager or 'Not specified'}

Available tools:
{chr(10).join(f'- {name}: {info["description"]}' for name, info in self.tools.items())}

Decide which tools to use and in what order. Consider:
- What systems does this role need access to?
- Who should be notified?
- What meetings should be scheduled?
- What's the appropriate welcome process for this department?

Respond in this exact JSON format:
{{
  "reasoning": "Your thought process about what this role needs",
  "steps": [
    {{
      "action": "What you're doing and why",
      "tool": "tool_name",
      "parameters": {{...tool parameters...}}
    }}
  ]
}}

Only include the tools that make sense for this specific role. Don't use all tools for everyone."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=planning_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            )
        )
        
        plan = json.loads(response.text)
        
        yield {
            "type": "reasoning_complete",
            "reasoning": plan["reasoning"],
            "steps_planned": len(plan["steps"])
        }
        
        # Step 2: Execute each planned step
        for i, step_data in enumerate(plan["steps"], 1):
            tool_name = step_data["tool"]
            
            if tool_name not in self.tools:
                yield {
                    "type": "step_error",
                    "step": i,
                    "message": f"Unknown tool: {tool_name}"
                }
                continue
            
            yield {
                "type": "step_start",
                "step": i,
                "action": step_data["action"],
                "tool": tool_name
            }
            
            # Execute the tool
            try:
                tool_func = self.tools[tool_name]["func"]
                params = step_data.get("parameters", {})
                
                # Add common parameters if not present
                if "employee_name" not in params:
                    params["employee_name"] = employee_name
                if "role" not in params:
                    params["role"] = role
                if "email" not in params:
                    params["email"] = email
                if "start_date" not in params and tool_name in ["schedule_meeting", "send_welcome_email"]:
                    params["start_date"] = start_date
                if "manager" not in params:
                    params["manager"] = manager
                
                result = tool_func(**params)
                
                yield {
                    "type": "step_complete",
                    "step": i,
                    "tool": tool_name,
                    "result": result
                }
                
            except Exception as e:
                yield {
                    "type": "step_error",
                    "step": i,
                    "tool": tool_name,
                    "message": str(e)
                }
        
        # Step 3: Final summary
        yield {
            "type": "workflow_complete",
            "message": f"Onboarding workflow completed for {employee_name}",
            "total_steps": len(plan["steps"])
        }
