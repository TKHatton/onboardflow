"""Autonomous OnboardFlow Agent with comprehensive onboarding tools."""

import os
import json
from typing import AsyncGenerator
from google import genai

from .tools import (
    create_jira_ticket,
    create_github_account,
    send_slack_message,
    schedule_meeting,
    send_welcome_email,
    setup_crm_access,
    create_asana_project,
    assign_training_courses,
    provision_equipment,
    schedule_security_training,
    enroll_in_benefits,
    verify_onboarding_completion,
    answer_onboarding_question,
)


class AutonomousAgent:
    """Autonomous agent that plans and executes onboarding workflows."""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"
        
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
            "assign_training_courses": {
                "func": assign_training_courses,
                "description": "Assign role-based training courses with deadlines"
            },
            "provision_equipment": {
                "func": provision_equipment,
                "description": "Order and provision equipment based on role (laptop, monitor, etc.)"
            },
            "schedule_security_training": {
                "func": schedule_security_training,
                "description": "Schedule mandatory security and compliance training modules"
            },
            "enroll_in_benefits": {
                "func": enroll_in_benefits,
                "description": "Enroll employee in benefits programs (health insurance, 401k, etc.)"
            },
            "verify_onboarding_completion": {
                "func": verify_onboarding_completion,
                "description": "Verify onboarding tasks completion and send follow-ups"
            },
            "answer_onboarding_question": {
                "func": answer_onboarding_question,
                "description": "Answer onboarding-related questions from employees"
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
        Use Gemini to autonomously plan and execute comprehensive onboarding workflow.
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
- What equipment should be provisioned?
- What training courses are required (role-based and security)?
- Who should be notified?
- What meetings should be scheduled?
- What benefits information should be sent?
- Should we schedule a follow-up verification?

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

Include a comprehensive set of tools. For most roles, you should include:
- Equipment provisioning
- System access (GitHub for engineers, CRM for sales, Asana for marketing)
- Training courses (role-based)
- Security training (mandatory for all)
- Benefits enrollment
- Welcome communications
- Follow-up verification

Don't use all tools for everyone - be thoughtful about what's relevant."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=planning_prompt,
            config={
                "temperature": 0.7,
                "response_mime_type": "application/json",
            }
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
                
                # Normalize parameter names
                param_mapping = {
                    "employee_email": "email",
                    "recipient_email": "to_email",
                    "user_email": "email",
                    "hire_date": "start_date",
                    "first_day": "start_date",
                    "supervisor": "manager",
                    "reporting_manager": "manager",
                }
                
                # Apply mapping
                normalized_params = {}
                for key, value in params.items():
                    mapped_key = param_mapping.get(key, key)
                    normalized_params[mapped_key] = value
                
                # Add common parameters if not present
                if "employee_name" not in normalized_params:
                    normalized_params["employee_name"] = employee_name
                if "role" not in normalized_params:
                    normalized_params["role"] = role
                if "department" not in normalized_params:
                    normalized_params["department"] = department
                if "email" not in normalized_params:
                    normalized_params["email"] = email
                if "start_date" not in normalized_params and tool_name in ["schedule_meeting", "send_welcome_email", "enroll_in_benefits"]:
                    normalized_params["start_date"] = start_date
                if "manager" not in normalized_params:
                    normalized_params["manager"] = manager
                
                # Filter to only accepted parameters
                import inspect
                sig = inspect.signature(tool_func)
                valid_params = {}
                for param_name, param_value in normalized_params.items():
                    if param_name in sig.parameters:
                        valid_params[param_name] = param_value
                
                result = tool_func(**valid_params)
                
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
            "message": f"Comprehensive onboarding workflow completed for {employee_name}",
            "total_steps": len(plan["steps"])
        }
    
    def chat(self, employee_name: str, question: str, context: dict = None) -> dict:
        """
        Answer onboarding questions using the chatbot tool.
        """
        return answer_onboarding_question(
            employee_name=employee_name,
            question=question,
            context=context
        )
