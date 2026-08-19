"""Onboarding Chatbot tool - answers employee questions."""

from datetime import datetime


def answer_onboarding_question(
    employee_name: str,
    question: str,
    context: dict = None,
) -> dict:
    """Answer onboarding-related questions using AI.
    
    Args:
        employee_name: Name of the employee asking
        question: The question being asked
        context: Optional context about the employee (role, department, etc.)
    
    Returns:
        dict with answer and related resources
    """
    # Knowledge base of common onboarding questions
    knowledge_base = {
        "it_setup": {
            "keywords": ["laptop", "computer", "setup", "it", "equipment", "software"],
            "answer": "Your IT equipment should arrive within 3-5 business days. Once it arrives, follow the setup guide in your welcome email. If you need immediate assistance, contact IT Support at it-support@company.com or call ext. 5555.",
            "resources": [
                {"title": "IT Setup Guide", "url": "/resources/it-setup"},
                {"title": "Software Installation", "url": "/resources/software"},
            ]
        },
        "benefits": {
            "keywords": ["benefits", "insurance", "health", "dental", "401k", "retirement"],
            "answer": "You have 30 days from your start date to enroll in benefits. Log into the Benefits Portal at benefits.company.com. You can choose from PPO or HSA health plans, dental, vision, and 401k with 4% company match. Questions? Email benefits@company.com.",
            "resources": [
                {"title": "Benefits Overview", "url": "/resources/benefits"},
                {"title": "Plan Comparison", "url": "/resources/plan-comparison"},
            ]
        },
        "training": {
            "keywords": ["training", "course", "learn", "security", "compliance"],
            "answer": "You'll receive access to our Learning Management System (LMS) on your first day. Required training includes Security Awareness (due in 7 days), Data Privacy (due in 14 days), and role-specific courses. You can track progress at lms.company.com.",
            "resources": [
                {"title": "Training Portal", "url": "/resources/training"},
                {"title": "Training FAQ", "url": "/resources/training-faq"},
            ]
        },
        "time_off": {
            "keywords": ["vacation", "pto", "time off", "sick", "holiday"],
            "answer": "You start with 20 days PTO per year, plus company holidays. PTO accrues from day one. Submit requests through the HR Portal at hr.company.com. Sick days are unlimited - just notify your manager and log it in the system.",
            "resources": [
                {"title": "PTO Policy", "url": "/resources/pto-policy"},
                {"title": "Holiday Schedule", "url": "/resources/holidays"},
            ]
        },
        "payroll": {
            "keywords": ["pay", "salary", "paycheck", "direct deposit", "tax"],
            "answer": "Payroll runs bi-weekly on Fridays. Set up direct deposit in the HR Portal by your first payday. Your first paycheck may be delayed 1-2 pay periods while we process your tax forms. Questions? Email payroll@company.com.",
            "resources": [
                {"title": "Payroll Schedule", "url": "/resources/payroll"},
                {"title": "Tax Forms Guide", "url": "/resources/tax-forms"},
            ]
        },
        "tools": {
            "keywords": ["slack", "email", "jira", "github", "tools", "access"],
            "answer": "You should have access to email, Slack, Jira, and other tools within 24 hours of starting. If you're missing access to a specific tool, submit an IT ticket at help.company.com or ask in #it-support on Slack.",
            "resources": [
                {"title": "Tools Overview", "url": "/resources/tools"},
                {"title": "Access Request Form", "url": "/resources/access-request"},
            ]
        },
        "culture": {
            "keywords": ["culture", "team", "social", "events", "values"],
            "answer": "We have weekly team lunches, monthly all-hands meetings, and quarterly team events. Join our Slack channels (#social, #interests) to connect with colleagues. Check the Events Calendar for upcoming activities.",
            "resources": [
                {"title": "Company Culture", "url": "/resources/culture"},
                {"title": "Events Calendar", "url": "/resources/events"},
            ]
        },
    }
    
    # Find matching knowledge base entry
    question_lower = question.lower()
    matched_entry = None
    
    for category, entry in knowledge_base.items():
        if any(keyword in question_lower for keyword in entry["keywords"]):
            matched_entry = entry
            break
    
    # Generate response
    if matched_entry:
        answer = matched_entry["answer"]
        resources = matched_entry["resources"]
    else:
        # Default response for unmatched questions
        answer = f"Thanks for your question, {employee_name}. I don't have a specific answer for that, but I can connect you with the right person. For general questions, email hr@company.com. For IT issues, contact it-support@company.com. You can also ask in #general on Slack."
        resources = [
            {"title": "HR Contact", "url": "mailto:hr@company.com"},
            {"title": "IT Support", "url": "mailto:it-support@company.com"},
        ]
    
    response_id = f"chat-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    response_data = {
        "response_id": response_id,
        "employee_name": employee_name,
        "question": question,
        "answer": answer,
        "resources": resources,
        "context": context or {},
        "answered_at": datetime.now().isoformat(),
        "satisfaction_rating": None,  # Can be filled by user later
    }
    
    print(f"[CHATBOT] Answered question for {employee_name}: {question[:50]}...")
    
    return {
        "success": True,
        "response_id": response_id,
        "data": response_data,
    }
