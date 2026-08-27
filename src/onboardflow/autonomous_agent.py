"""Autonomous OnboardFlow Agent with comprehensive onboarding tools."""

import os
import json
import inspect
from datetime import datetime
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
from .state_tracker import StateTracker


class AutonomousAgent:
    """Autonomous agent that plans and executes onboarding workflows."""

    # Parameter names Gemini tends to invent, mapped onto the names the tool
    # functions actually declare.
    PARAM_ALIASES = {
        "employee_email": "email",
        "user_email": "email",
        "recipient_email": "to_email",
        "recipient": "to_email",
        "hire_date": "start_date",
        "first_day": "start_date",
        "supervisor": "manager",
        "reporting_manager": "manager",
        "meeting_time": "start_time",
        "meeting_date": "start_time",
        "meeting_title": "title",
        "subject": "title",
        "participants": "attendees",
        "attendee_list": "attendees",
        "invitees": "attendees",
        "duration": "duration_minutes",
    }

    def __init__(self, state: StateTracker | None = None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"
        self.state = state or StateTracker()
        
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
    
    def _tool_catalog(self) -> str:
        """Describe each tool to Gemini with its real parameter names.

        Without this the prompt lists only prose descriptions, so Gemini has to
        guess parameter names and frequently guesses wrong.
        """
        lines = []
        for name, info in self.tools.items():
            sig = inspect.signature(info["func"])
            required, optional = [], []
            for param_name, param in sig.parameters.items():
                if param.default is inspect.Parameter.empty:
                    required.append(param_name)
                else:
                    optional.append(param_name)
            detail = f"required: {', '.join(required)}" if required else "no required parameters"
            if optional:
                detail += f"; optional: {', '.join(optional)}"
            lines.append(f'- {name}: {info["description"]} ({detail})')
        return chr(10).join(lines)

    @staticmethod
    def _parameter_fallbacks(
        employee_name: str,
        role: str,
        department: str,
        start_date: str,
        email: str,
        manager: str | None,
        preferred_name: str | None = None,
    ) -> dict:
        """Values to fill in for any tool parameter Gemini leaves out.

        Keyed by the parameter names the tools declare, so filling is driven by
        each tool's signature instead of a hand-maintained per-tool list.
        """
        # Every communication-facing tool (email, Slack, calendar) addresses the
        # employee by whatever "employee_name" it's given, so a preferred name
        # flows into every generated message automatically. Legal name is still
        # what's on the submitted form and in Firestore's own employee_name field.
        display_name = preferred_name or employee_name
        channel = f"#{department.lower().replace(' ', '-')}" if department else "#general"
        return {
            "employee_name": display_name,
            "role": role,
            "department": department,
            "email": email,
            "to_email": email,
            "start_date": start_date,
            "manager": manager,
            "manager_name": manager,
            "title": f"Orientation: {display_name}",
            "attendees": [addr for addr in (email,) if addr],
            "start_time": f"{start_date}T09:00:00",
            "channel": channel,
            "message": (
                f"Welcome {display_name} to the team as our new {role}!"
            ),
        }

    @staticmethod
    def _coerce_params(params: dict, start_date: str, email: str) -> dict:
        """Reshape Gemini's values into what the tools expect.

        Gemini returns a plausible-looking value for the right key often enough
        that the tools fail on shape rather than absence: a bare string where a
        list of attendees belongs, or a date where a full timestamp does.
        """
        coerced = dict(params)

        if "attendees" in coerced:
            attendees = coerced["attendees"]
            if isinstance(attendees, str):
                attendees = [attendees]
            elif not isinstance(attendees, list):
                attendees = list(attendees or [])
            coerced["attendees"] = [a for a in attendees if a] or [email]

        if "start_time" in coerced:
            coerced["start_time"] = AutonomousAgent._coerce_start_time(
                coerced["start_time"], start_date
            )

        if "duration_minutes" in coerced:
            try:
                coerced["duration_minutes"] = int(coerced["duration_minutes"])
            except (TypeError, ValueError):
                coerced.pop("duration_minutes")

        return coerced

    @staticmethod
    def _coerce_start_time(value, start_date: str) -> str:
        """Return an ISO timestamp the calendar tool can parse.

        schedule_meeting calls datetime.fromisoformat on this, which raises on a
        bare time or free text, so anything unparseable falls back to 9am on the
        employee's start date.
        """
        default = f"{start_date}T09:00:00"
        if not isinstance(value, str) or not value.strip():
            return default
        candidate = value.strip().replace("Z", "+00:00").replace(" ", "T", 1)
        try:
            parsed = datetime.fromisoformat(candidate)
        except ValueError:
            return default
        # A date with no time parses to midnight; use business hours instead.
        if parsed.hour == 0 and parsed.minute == 0 and "T" not in candidate:
            return f"{parsed.date().isoformat()}T09:00:00"
        return parsed.isoformat()

    async def plan_onboarding(
        self,
        employee_name: str,
        role: str,
        department: str,
        start_date: str,
        email: str,
        manager: str | None = None,
        preferred_name: str | None = None,
        pronouns: str | None = None,
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
- Legal Name: {employee_name}
- Preferred Name: {preferred_name or 'same as legal name'}
- Pronouns: {pronouns or 'not specified'}
- Role: {role}
- Department: {department}
- Start Date: {start_date}
- Email: {email}
- Manager: {manager or 'Not specified'}

When you write the "action" text for any step involving direct communication with the
employee (welcome email, Slack message, meeting title), address them by their preferred
name if one is given, and use their pronouns correctly if specified.

Available tools (use these exact parameter names):
{self._tool_catalog()}

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

        workflow_id = await self.state.log_workflow_start(
            employee_name, role, department, start_date, email,
            preferred_name=preferred_name, pronouns=pronouns,
            reasoning=plan.get("reasoning"),
        )

        yield {
            "type": "reasoning_complete",
            "workflow_id": workflow_id,
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

                # Gemini invents its own parameter names, so map the common
                # variations onto the names the tool functions actually declare.
                normalized_params = {
                    self.PARAM_ALIASES.get(key, key): value
                    for key, value in params.items()
                }

                # Fill anything the tool needs that Gemini did not supply.
                # Driven off each tool's real signature rather than a per-tool
                # list, so a tool that declares to_email/attendees/start_time
                # gets them the same way one declaring email/start_date does.
                fallbacks = self._parameter_fallbacks(
                    employee_name, role, department, start_date, email, manager,
                    preferred_name=preferred_name,
                )
                sig = inspect.signature(tool_func)
                for param_name in sig.parameters:
                    if param_name not in normalized_params and param_name in fallbacks:
                        normalized_params[param_name] = fallbacks[param_name]

                # Gemini sometimes fills employee_name with the legal name even
                # when told to prefer the given name, since the parameter is
                # literally called "employee_name". Force it here rather than
                # relying on instruction-following for something a real HR
                # system would never get wrong.
                if preferred_name and "employee_name" in normalized_params:
                    normalized_params["employee_name"] = preferred_name

                # Drop anything this tool does not accept, then coerce the
                # values Gemini does send into the shapes the tools expect.
                valid_params = {
                    name: value
                    for name, value in normalized_params.items()
                    if name in sig.parameters
                }
                valid_params = self._coerce_params(valid_params, start_date, email)

                missing = [
                    name
                    for name, param in sig.parameters.items()
                    if param.default is inspect.Parameter.empty
                    and name not in valid_params
                ]
                if missing:
                    yield {
                        "type": "step_error",
                        "step": i,
                        "tool": tool_name,
                        "message": f"Missing required parameter(s): {', '.join(missing)}"
                    }
                    continue

                result = tool_func(**valid_params)
                await self.state.log_step(
                    workflow_id, tool_name, step_data["action"], True, result
                )

                yield {
                    "type": "step_complete",
                    "step": i,
                    "tool": tool_name,
                    "result": result
                }

            except Exception as e:
                await self.state.log_step(
                    workflow_id, tool_name, step_data["action"], False, {"error": str(e)}
                )
                yield {
                    "type": "step_error",
                    "step": i,
                    "tool": tool_name,
                    "message": str(e)
                }

        # Step 3: Final summary
        await self.state.log_workflow_complete(workflow_id)
        yield {
            "type": "workflow_complete",
            "workflow_id": workflow_id,
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
