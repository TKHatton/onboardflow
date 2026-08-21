# OnboardFlow Demo Video Script
**Duration: 4 minutes**

---

## 0:00 - 0:30 | Introduction (30 seconds)

**[Screen: Title slide with OnboardFlow logo]**

**Voiceover:**
"Employee onboarding is broken. HR teams waste hours manually setting up accounts, ordering equipment, assigning training, and coordinating across dozens of systems. New hires wait days for access, training gets missed, and nothing scales.

Introducing OnboardFlow - an autonomous AI agent that orchestrates the entire onboarding process across 11+ systems, intelligently adapting to each employee's role and department."

---

## 0:30 - 1:00 | The Problem & Solution (30 seconds)

**[Screen: Split view - Left side shows chaotic manual process, right side shows OnboardFlow dashboard]**

**Voiceover:**
"Traditional onboarding requires HR to manually create tickets in Jira, order equipment from IT, set up GitHub access, assign training courses, schedule meetings, and send welcome emails. It's time-consuming, error-prone, and inconsistent.

OnboardFlow replaces this chaos with intelligence. One form, one click, and the AI agent handles everything - reasoning about what each new hire needs based on their role."

---

## 1:00 - 1:30 | Live Demo: Software Engineer (30 seconds)

**[Screen: React UI - Fill out form for Sarah Chen, Software Engineer]**

**Voiceover:**
"Let's see it in action. I'm onboarding Sarah Chen, a new Software Engineer in the Engineering department.

**[Action: Fill out the form]**
- Name: Sarah Chen
- Role: Software Engineer
- Department: Engineering
- Start Date: 2026-02-01
- Email: sarah.chen@company.com
- Manager: Alex Rodriguez

**[Action: Click 'Start Onboarding']**

Watch as the AI agent analyzes the role and starts executing the workflow..."

---

## 1:30 - 2:30 | Real-Time Execution (60 seconds)

**[Screen: Dashboard showing live workflow execution]**

**Voiceover:**
"The dashboard shows the agent's reasoning in real-time. It's decided Sarah needs:

**[Watch as each step completes]**

1. **Equipment Provisioning** - Orders a high-spec laptop with dual monitors and mechanical keyboard for engineering work

2. **GitHub Setup** - Creates account and grants access to frontend, backend, and infrastructure repositories

3. **Training Courses** - Assigns technical training: Advanced Git, CI/CD pipelines, and code review best practices

4. **Security Training** - Schedules mandatory security awareness and compliance modules

5. **Jira Ticket** - Creates onboarding ticket with all tasks and assigns to manager

6. **Slack Welcome** - Sends welcome message to #engineering channel

7. **Email Notification** - Sends personalized welcome email with first-day instructions

8. **Calendar Invites** - Schedules orientation meeting and 1:1 with manager

Each step executes autonomously, with full audit trails in Firestore."

---

## 2:30 - 3:00 | Role Adaptation (30 seconds)

**[Screen: Show different role examples]**

**Voiceover:**
"The agent adapts intelligently. For a Sales Representative, it provisions CRM access instead of GitHub, assigns sales training instead of technical courses, and creates Asana projects for marketing campaigns.

**[Quick cuts showing different role outputs]**

No hardcoded workflows. The AI reasons about what each role needs and executes accordingly."

---

## 3:00 - 3:30 | Chatbot Assistant (30 seconds)

**[Screen: Switch to Chatbot tab]**

**Voiceover:**
"But onboarding doesn't end after day one. New hires have questions.

**[Action: Type questions in chatbot]**

'When will I receive my equipment?'
'What training do I need to complete?'
'How do I enroll in benefits?'

The chatbot provides instant answers with relevant resources. It's available 24/7, reducing HR support tickets and improving the new hire experience."

---

## 3:30 - 4:00 | Technical Architecture & Closing (30 seconds)

**[Screen: Architecture diagram]**

**Voiceover:**
"Built on Google Cloud with FastAPI, React, and Gemini 2.0 Flash. The autonomous agent uses the Agent Development Kit to orchestrate 11+ tools, with real-time updates via Server-Sent Events and persistent state in Firestore.

**[Screen: Return to dashboard showing completed workflow]**

OnboardFlow transforms onboarding from a manual nightmare into an intelligent, autonomous experience. One form. One click. Complete onboarding across all systems.

The future of employee onboarding is autonomous."

**[Screen: OnboardFlow logo + GitHub link]**

---

## Production Notes

### Recording Setup
- Use OBS Studio or similar for screen recording
- Record at 1080p, 60fps
- Use a good microphone for voiceover
- Record in a quiet environment

### Screen Sections to Prepare
1. Title slide (can create in Canva or similar)
2. React UI with form filled out
3. Dashboard showing workflow execution
4. Different role examples (pre-run these)
5. Chatbot with questions typed
6. Architecture diagram

### Timing Tips
- Speak clearly and at moderate pace
- Pause briefly between sections
- Let the dashboard animations play out
- Don't rush the tool execution - let viewers see each step

### Post-Production
- Add captions/subtitles for accessibility
- Add background music (quiet, professional)
- Trim any dead space
- Export as MP4, under 200MB for Devpost

### Upload
- Upload to YouTube as "Unlisted" or "Public"
- Title: "OnboardFlow - Autonomous AI Employee Onboarding"
- Description: Brief summary + GitHub link
- Copy the shareable URL for Devpost submission
