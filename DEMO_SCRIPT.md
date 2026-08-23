# OnboardFlow Demo Video Script
**Target Duration: 4 minutes**

---

## [0:00-0:30] Opening Hook (30 seconds)

**Visual:** Start with a split screen - left side shows chaotic manual onboarding (spreadsheets, emails, multiple tools), right side shows clean OnboardFlow interface

**Narration:**
"Employee onboarding is broken. HR teams spend 15-20 hours per new hire manually coordinating across dozens of systems - ordering equipment, setting up accounts, scheduling training, sending welcome emails. It's repetitive, error-prone, and doesn't scale.

What if an AI agent could handle all of this autonomously? Not just follow a script, but actually reason about what each new hire needs based on their role?"

---

## [0:30-1:30] Live Demo: HR Coordinator (60 seconds)

**Visual:** Show the React UI, fill out the form with Maria Santos data

**Narration:**
"Meet OnboardFlow. Let's onboard Maria Santos, an HR Coordinator starting September 1st."

**Visual:** Click "Start Onboarding", show the reasoning panel

**Narration:**
"Watch what happens. The agent doesn't just execute a hardcoded workflow. It analyzes Maria's role and reasons: 'As an HR Coordinator, she needs standard workstation equipment, HR-specific training, compliance modules, benefits enrollment, and orientation meetings. She doesn't need GitHub access or CRM tools.'"

**Visual:** Show the workflow executing in real-time - equipment being ordered, training assigned, benefits set up

**Narration:**
"In seconds, the agent has:
- Ordered a laptop, monitor, and peripherals for remote work
- Created a Jira ticket to track the onboarding workflow
- Assigned HR-specific training courses with deadlines
- Scheduled mandatory security and compliance training
- Enrolled Maria in health insurance, dental, vision, and 401k plans
- Scheduled a follow-up check-in for one week after start date

All autonomous. No human intervention. No copy-pasting between systems."

---

## [1:30-2:15] Show Adaptability: Different Role (45 seconds)

**Visual:** Clear the form, enter a Software Engineer

**Narration:**
"But here's what makes this powerful - the agent adapts. Let's onboard a Software Engineer instead."

**Visual:** Fill out form for "Alex Chen, Software Engineer, Engineering"

**Narration:**
"Now the agent reasons differently: 'Engineers need GitHub access to code repositories, high-spec equipment for development, technical training on our stack, and integration with our CI/CD pipeline. They don't need CRM access or sales training.'"

**Visual:** Show different tools being executed - GitHub account created, different equipment ordered, technical training assigned

**Narration:**
"Same system, completely different workflow. The agent makes intelligent decisions based on the role, department, and start date. No two onboarding experiences are the same."

---

## [2:15-2:45] Chatbot Feature (30 seconds)

**Visual:** Switch to the chatbot tab

**Narration:**
"But onboarding doesn't end after day one. New hires have questions. That's where the chatbot comes in."

**Visual:** Type questions in the chatbot

**Narration:**
"Maria can ask: 'When will my equipment arrive?' The chatbot, powered by the same Gemini model, has full context about her onboarding. It knows her equipment was ordered, knows the estimated delivery date, and can even check the verification system to confirm it shipped.

She can ask about training deadlines, benefits enrollment, or company policies. It's like having an HR assistant available 24/7."

---

## [2:45-3:30] Technical Architecture (45 seconds)

**Visual:** Show architecture diagram

**Narration:**
"So how does this work under the hood?

OnboardFlow is built on Google's Agent Development Kit and powered by Gemini 3.6 Flash. The agent uses a tool-calling architecture - it has access to 11+ tools for different systems: Jira for task tracking, GitHub for code access, Slack for team communication, calendar for scheduling, email for notifications, and more.

The key innovation is the reasoning layer. When a new hire is submitted, Gemini analyzes the role and department, decides which tools are relevant, determines the execution order, and fills in the parameters. It's not just calling APIs - it's making decisions.

All state is tracked in Firestore for audit trails and compliance. The React frontend provides real-time visibility via server-sent events, so you can watch the agent think and execute."

---

## [3:30-4:00] Closing & Impact (30 seconds)

**Visual:** Show completed workflow summary, then show metrics

**Narration:**
"The impact? What used to take 15-20 hours of manual coordination now takes 20 seconds. Every new hire gets a consistent, comprehensive onboarding experience tailored to their role. Nothing gets missed. Nothing gets forgotten.

OnboardFlow transforms onboarding from a manual nightmare into an autonomous, intelligent system. It's not just automation - it's augmentation. The AI handles the coordination, so HR teams can focus on what matters: welcoming new team members.

This is the future of employee onboarding. Autonomous, intelligent, and scalable."

**Visual:** Show GitHub repo link, end screen

**Narration:**
"The code is open source. Try it yourself."

---

## Production Notes

### Screen Recording Setup
- Use OBS Studio or similar
- Record at 1920x1080, 60fps
- Capture both the React UI and terminal (for showing the agent reasoning)

### Key Moments to Highlight
1. **0:45** - The reasoning panel showing Gemini's thought process
2. **1:00** - First tool executing (equipment provisioning)
3. **1:45** - Different workflow for Software Engineer
4. **2:20** - Chatbot answering a question with context
5. **3:00** - Architecture diagram with tool connections

### Voiceover Tips
- Speak clearly and at moderate pace
- Pause briefly between sections
- Emphasize "autonomous" and "reasoning" - these are the key differentiators
- Don't rush the technical section - judges want to understand the architecture

### What to Show in the UI
- The form being filled out
- The reasoning panel (most important!)
- The workflow steps executing in real-time
- The chatbot interface
- The architecture diagram (can be a static image)

### Backup Plan
If the live demo has issues, you can:
- Pre-record the workflow execution
- Show the terminal output instead of the UI
- Use screenshots with voiceover

### Judging Criteria Alignment
Make sure to emphasize:
1. **Innovation & Operational Utility (40%)** - Autonomous reasoning, not scripted
2. **Architectural Discipline (30%)** - Clean tool-calling architecture, state management
3. **Demo & Production Readiness (30%)** - Live demo, real-time updates, deployed on GCP

---

## Checklist Before Recording

- [ ] Backend running on localhost:8000
- [ ] Frontend running on localhost:5173
- [ ] Gemini API key set in .env
- [ ] Test with HR Coordinator first
- [ ] Test with Software Engineer second
- [ ] Test chatbot with a few questions
- [ ] Have architecture diagram ready
- [ ] Close all other browser tabs
- [ ] Test screen recording setup
- [ ] Do a dry run without recording

---

## Alternative Demo Data

If you want to show more variety, here are other roles that work well:

**Operations Manager:**
- Equipment provisioning
- Project management tools
- Training courses
- Security training
- Benefits enrollment

**Finance Analyst:**
- Equipment provisioning
- Financial system access
- Compliance training
- Security training
- Benefits enrollment

**Customer Success Manager:**
- Equipment provisioning
- CRM access
- Customer onboarding training
- Security training
- Benefits enrollment

Each role will trigger different tools and show the agent's adaptability.
