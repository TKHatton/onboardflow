<!-- prose-check: off — "real-time" below is the technical term for the SSE transport
     this script describes, not "real" used as an intensifier. -->
# OnboardFlow Demo Video Script
**Target Duration: 4 minutes**
**Updated 2026-08-26.** Rewritten against the app state verified live on 2026-08-25: full local
end-to-end pass (20/20 test steps), two live browser runs (Software Engineer, HR Coordinator),
chatbot Q&A, and the Pub/Sub trigger endpoint, all clean. The "Connection lost to server" false
error after a successful run is fixed (`d1bcfbe`), so a completed run now ends on a clean
"Workflow complete!" instead of a red error banner.

**Architecture note:** this version describes what the live path actually runs, the Gemini API
called directly via the `google-genai` SDK, no Google ADK, no Firestore. The repo also contains
an ADK-based `agent.py` and a Firestore `state_tracker.py`, but neither is wired into `server.py`
or `autonomous_agent.py`, which is what the demo shows. Say what's true of the running code.

---

## [0:00-0:30] Opening Hook (30 seconds)

**Visual:** Split screen. Left side shows chaotic manual onboarding (spreadsheets, emails,
multiple tools), right side shows the OnboardFlow interface.

**Narration:**
"Employee onboarding is broken. HR teams spend 15-20 hours per new hire manually coordinating
across dozens of systems: ordering equipment, setting up accounts, scheduling training, sending
welcome emails. It's repetitive, error-prone, and doesn't scale.

What if an AI agent could handle all of this autonomously? Not just follow a script, but actually
reason about what each new hire needs based on their role?"

---

## [0:30-1:30] Live Demo: Software Engineer (60 seconds)

**Visual:** Show the React UI, fill out the form for a new Software Engineer (name of your
choice, department Engineering, any future start date).

**Narration:**
"Meet OnboardFlow. Let's onboard a new Software Engineer joining the Engineering team."

**Visual:** Click "Start Onboarding," show the reasoning panel appear.

**Narration:**
"Watch what happens. The agent doesn't execute a hardcoded workflow. Gemini reasons about the
role first: engineers need GitHub access, developer-grade equipment, technical training, and the
standard HR steps, welcome email, Slack announcement, orientation, benefits. It plans that whole
sequence itself, then the frontend streams each step live over server-sent events as the agent
executes it."

**Visual:** Let it run to completion, ten steps, ending on the green "Workflow complete!" state.

**Narration:**
"In seconds, the agent has created a Jira tracking ticket, ordered equipment, set up GitHub
access, sent the welcome email, posted to Slack, scheduled orientation, assigned training,
scheduled security and compliance modules, enrolled the employee in benefits, and scheduled a
follow-up verification check. Ten tool calls, zero human intervention, and it all reasoned its own
way there."

---

## [1:30-2:15] Show Adaptability: Different Role (45 seconds)

**Visual:** Clear the form, submit an HR Coordinator instead (different department).

**Narration:**
"Here's what makes this more than a script: the agent adapts to the role. Let's onboard an HR
Coordinator instead."

**Visual:** Show the reasoning panel producing a different plan, and a different, shorter set of
steps executing (no GitHub account this time).

**Narration:**
"Same system, different reasoning. This time Gemini decides GitHub access doesn't apply, skips
it, and instead plans the standard HR onboarding: equipment, welcome communications, orientation,
training, and benefits. No two roles get the same workflow, because nothing is hardcoded per role.
The agent is deciding this fresh, every time, from the tools it has available."

---

## [2:15-2:45] Chatbot Feature (30 seconds)

**Visual:** Switch to the "Ask Questions" tab.

**Narration:**
"Onboarding doesn't end after the workflow runs. New hires have questions, so there's a chatbot
built on the same Gemini model, with full context about that employee's onboarding."

**Visual:** Click one of the suggested questions (e.g. "When will I receive my equipment?").

**Narration:**
"It answers with actual context: expected delivery window, who to contact, and links to the
relevant setup guides. Same underlying reasoning engine, now answering questions instead of
executing a workflow."

---

## [2:15-2:45] Event-Driven Trigger: Pub/Sub (30 seconds)

**Visual:** Show a terminal running `python test_pubsub.py`, or narrate over the architecture
diagram if you'd rather not split attention on camera.

**Narration:**
"The form isn't the only way to trigger this. OnboardFlow also exposes a Pub/Sub push endpoint,
so an HR system can publish a new-hire event directly and the same autonomous workflow runs
without anyone touching the UI. Confirmed working end-to-end against the running server."

---

## [3:15-3:45] Technical Architecture (30 seconds)

**Visual:** Show architecture diagram (verify it matches what you say before recording, see the
note at the top of this file).

**Narration:**
"Under the hood: a FastAPI backend calls Gemini directly to reason about each new hire and select
from eleven-plus tools: Jira, GitHub, Slack, calendar, email, training, benefits, and more. Each
tool call streams back to the React frontend in real time over server-sent events, so you're
watching the agent think and act as it happens, not waiting on a spinner."

---

## [3:45-4:00] Closing & Impact (15 seconds)

**Visual:** Show the completed workflow summary, then the GitHub repo link and end screen.

**Narration:**
"What used to take fifteen to twenty hours of manual coordination now takes seconds, reasoned
fresh for every role, every time. That's OnboardFlow. The code is open source, try it yourself."

---

## Production Notes

### Screen Recording Setup
- Backend on localhost:8000, frontend on localhost:5173, both already running.
- Record at 1920x1080, 60fps.
- Close other browser tabs before recording so the API status badge and page are clean.

### Key Moments to Highlight
1. The reasoning panel showing Gemini's plan before any tool runs.
2. The first tool executing and completing (equipment provisioning).
3. The second role producing a visibly different plan and step list.
4. The chatbot answering with actual context.
5. The clean "Workflow complete!" end state. This used to show a false error; it's fixed now,
   so let it finish on screen instead of cutting away before it does.

### Voiceover Tips
- Moderate pace, brief pause between sections.
- Emphasize "reasons" and "decides," not "automates," the differentiator is that nothing is
  hardcoded per role.
- Let each workflow run to its actual completion on screen at least once, since the fixed
  end state is itself evidence the app is solid.

### Backup Plan
If the live demo has issues during recording:
- Do a dry run first without recording (recommended regardless).
- Pre-record one clean full run as a fallback clip.
- Worst case, narrate over the terminal log output, which shows every tool call succeeding.

### Judging Criteria Alignment
1. **Innovation & Operational Utility**: autonomous reasoning per role, not a fixed script.
2. **Architectural Discipline**: tool-calling architecture, real-time streaming, clean error
   states.
3. **Demo & Production Readiness**: live demo, real-time updates via SSE.

---

## Checklist Before Recording

- [ ] Backend running on localhost:8000 (`python -m onboardflow.server` from repo root)
- [ ] Frontend running on localhost:5173 (`npm run dev` in `frontend/`)
- [ ] `GOOGLE_API_KEY` set in `.env`
- [ ] Do one full dry run with Software Engineer, confirm it ends on "Workflow complete!"
- [ ] Do one full dry run with HR Coordinator (or another non-engineering role)
- [ ] Test chatbot with at least one suggested question
- [ ] Decide the ADK/Firestore question on the architecture diagram before showing it on camera
- [ ] Close all other browser tabs
- [ ] Test screen recording setup with a short dry run

---

## Alternative Demo Data

Other roles that produce visibly different plans, if you want more variety than
Software Engineer and HR Coordinator:

**Marketing Manager:** Asana project setup instead of GitHub, marketing-specific training.

**Operations Manager, Finance Analyst, or Customer Success Manager:** standard equipment plus
training plus benefits, no engineering-specific tools. Good contrast against the Software
Engineer run without repeating the HR Coordinator flow.

Each role was confirmed to trigger a different reasoning plan and step count in earlier testing.
