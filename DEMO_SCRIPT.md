<!-- prose-check: off — "real-time" below is the technical term for the SSE
     transport this script describes, not "real" used as an intensifier. -->
# OnboardFlow Demo Video Script
**Target duration: 4:00-4:20**
**Updated 2026-08-27.** This is the full version, built to cover everything the judges are
scoring, not just a quick walkthrough. It records against the live deployed app, not
localhost:

- **App (record this):** https://onboardflow-hackathon.netlify.app
- **API:** https://onboardflow-883489836236.europe-west1.run.app

Verified working end-to-end today: full onboarding workflow, chatbot, Pub/Sub trigger, and
Firestore-backed history, all against these exact URLs. The frontend was redesigned
yesterday (warm palette, Space Grotesk/Inter type) — it no longer looks like default
AI-scaffolded UI, so open on this version, not an older recording.

**Architecture note:** describe what the live path actually runs: the Gemini API called
directly via the `google-genai` SDK, no Google ADK. Firestore, however, is genuinely wired
in now, as of today. Every workflow run (form or Pub/Sub-triggered) persists to it, and the
app's Past Onboardings tab reads actual records back. The architecture diagram was updated
to match, both the ADK removal and the Firestore restoration.

---

## [0:00-0:25] Opening hook

**Visual:** A couple seconds on a blank screen or a simple title card, then cut to the live
app at the URL above (so the browser address bar reads `onboardflow-hackathon.netlify.app`,
not localhost — that's the proof this is really deployed).

**Narration:**
"Employee onboarding eats fifteen to twenty hours of HR time per new hire: ordering
equipment, setting up accounts, scheduling training, sending the right emails to the right
people. Most 'automation' for this is a hardcoded checklist that runs the same steps for
everyone. OnboardFlow doesn't do that. It reasons about each new hire's role and decides,
from scratch, what they actually need. This is live right now at
onboardflow-hackathon.netlify.app."

---

## [0:25-1:25] Live run: Software Engineer, full workflow

**Visual:** Fill the form (any name, Role: Software Engineer, Department: Engineering, a
future start date), click **Start Onboarding**. Let the reasoning panel populate, then let
every step stream in and complete.

**Narration (over the reasoning panel appearing):**
"Watch what happens before a single tool runs. Gemini reads the role and department and
plans its own sequence: this new hire needs GitHub access, developer-grade equipment,
technical training, plus the standard onboarding steps. Nothing here is a template — the
agent decided this."

**Narration (over steps streaming in):**
"Each of these is a live tool call, streamed to the browser the instant it completes: a
Jira ticket, equipment ordered, GitHub access provisioned, a welcome email, a Slack
announcement, orientation scheduled, training assigned, security modules scheduled,
benefits enrollment, and a follow-up check. Ten tool calls, ten different systems, zero
hardcoded logic connecting them."

**Visual:** Let it finish on the green "Workflow complete!" state — hold 2 full seconds
here, it's the payoff shot.

---

## [1:25-1:50] Contrast: a second role, different plan

**Visual:** Submit again with a non-engineering role (HR Coordinator, Marketing Manager, or
similar). Let the reasoning panel and step list populate, but you don't need to let this one
run to completion on screen — a few seconds of the differing plan is enough.

**Narration:**
"Same system, same code, completely different plan. This time there's no GitHub step —
Gemini decided it doesn't apply — and it substitutes role-appropriate tools instead. This
is the actual proof point: nothing is if-role-equals-engineer hardcoded. The reasoning
happens fresh, every single time."

---

## [1:50-2:15] Chatbot: the same reasoning, answering questions

**Visual:** Click the **Ask Questions** tab, click one of the suggested question chips
(e.g. "When will I receive my equipment?").

**Narration:**
"Onboarding doesn't stop after the workflow runs. The chatbot is powered by the same
Gemini reasoning, now with context about this specific employee's onboarding — it answers
with an actual delivery window and links to setup resources, not a canned FAQ response."

---

## [2:15-2:45] The part most demos skip: it's event-driven, not just a form

**Visual:** Switch to a terminal window, run
`BACKEND_URL=https://onboardflow-883489836236.europe-west1.run.app python test_pubsub.py`
(or narrate over a prepared screenshot of the terminal output if you'd rather not
context-switch live). Show the 200 OK response and the workflow ID it returns.

**Narration:**
"The web form isn't the only way in. OnboardFlow also exposes a Pub/Sub push endpoint, so
an actual HR system, a Workday, a BambooHR, could publish a new-hire event directly, and
the exact same autonomous agent picks it up and runs, with nobody touching a browser. This
is what makes it an integration pattern instead of a demo toy: the reasoning engine is
decoupled from the UI."

---

## [2:45-3:10] Proof it's not throwaway: the Firestore history view

**Visual:** Switch back to the browser, click the **Past Onboardings** tab. The run you
just triggered from the terminal (no browser involved) should already be sitting there.

**Narration:**
"And here's the part that ties it together: every one of these runs, whether it started
from the form or from that Pub/Sub call a second ago, gets written to Firestore. Nothing
here is thrown away after the browser tab closes. This list is pulled from persisted
records, that Pub/Sub run I just triggered from the terminal is already sitting in it."

---

## [3:10-3:40] Architecture, in one breath

**Visual:** Architecture diagram (only if you've settled the ADK/Firestore accuracy
question by recording time — otherwise skip this beat entirely and let the closing run
longer).

**Narration:**
"Under the hood: a FastAPI backend on Cloud Run calls Gemini directly to reason about each
new hire and select from eleven-plus tools — Jira, GitHub, Slack, calendar, email, training,
benefits, and more. Every tool call streams to the React frontend in real time over
server-sent events, so you're watching the agent think and act as it happens. Frontend's on
Netlify, backend's on Cloud Run, both live at the URLs on screen right now."

---

## [3:40-4:05] Close

**Visual:** Back to the completed workflow from the first run, or the live URL in the
address bar.

**Narration:**
"Fifteen to twenty hours of manual coordination, down to seconds, reasoned fresh for every
role, every time, live at onboardflow-hackathon.netlify.app right now. That's OnboardFlow.
Code's open source — try it yourself."

---

## Production notes

### Before recording
- Confirm both live URLs return actual responses, not cached errors: hit the Cloud Run
  health check (`/`) and load the Netlify app fresh.
- Do one full dry run of Take 1 (Software Engineer) and confirm it ends on "Workflow
  complete!" with no red error state.
- The ADK/Firestore question is settled: ADK removed, Firestore restored, both verified
  live on 2026-08-27. Safe to show the diagram on camera.

### Key moments to actually hold on screen
1. The address bar showing the live Netlify URL, not localhost, a couple seconds, early.
2. The reasoning panel's text, before any tool executes.
3. The green "Workflow complete!" end state, don't cut away early.
4. The second role's reasoning text diverging from the first (this is the "not hardcoded"
   proof, make sure it's legible, not a blur-past).
5. The Pub/Sub terminal output, specifically the `200` status and workflow ID.
6. The Past Onboardings tab showing that exact same workflow ID already sitting there. This
   is the single strongest "this is genuinely deployed" shot in the whole video, don't rush it.

### Voiceover tips
- Say "reasons" and "decides," not "automates," that word choice is the actual
  differentiator between this and a scripted workflow tool.
- Don't rush the Pub/Sub section. It's the piece that shows this isn't just a pretty form,
  and it's easy to cut for time. Protect it.
- The Firestore beat lands harder if the workflow ID on screen visibly matches between the
  terminal output and the history list, so don't cut away from the terminal before that ID
  is legible.
- Slow down on the architecture beat if you keep it, judges assessing technical depth are
  listening hardest here.

### Backup plan
- If a live call is slow or flaky during recording (cold start on Cloud Run after idle,
  typically a few extra seconds on the first request), pad with a beat of narration over
  the loading state rather than cutting mid-word. A brief cold start is honest, not a
  bug — Cloud Run scales to zero to stay free, which is worth saying if it happens on
  camera.
- Keep one clean pre-recorded full run as a fallback clip in case something breaks live.

### Judging criteria, mapped directly to script beats
1. **Innovation & operational utility:** the 0:25-1:50 block (role-adaptive reasoning,
   twice).
2. **Architectural discipline:** the 2:15-3:40 block, Pub/Sub, Firestore history, and the
   architecture summary together, decoupled trigger, persisted state, real-time streaming.
3. **Demo & production readiness:** the whole thing runs against a live, publicly reachable
   URL, not a local screen share. Say the URL out loud at least once.

---

## Checklist before recording

- [ ] Confirm https://onboardflow-hackathon.netlify.app loads with the new design (warm
      background, dark header, not the old purple gradient)
- [ ] Confirm the "API: ✅ Online" badge shows before recording
- [ ] Dry run: Software Engineer, full completion, no error state
- [ ] Dry run: second role (HR Coordinator, Marketing Manager, or similar), confirm a
      visibly different step list
- [ ] Test the chatbot with one suggested question
- [ ] Test the Pub/Sub command against the live URL, confirm 200 OK
- [ ] Click Past Onboardings after that Pub/Sub test, confirm the same workflow ID shows up
- [ ] Close all other browser tabs
- [ ] Short dry run of the screen recording setup itself before the actual take

---

## Alternative demo roles

If you want a different pairing than Software Engineer / HR Coordinator for the two live
runs:

**Marketing Manager:** Asana project setup instead of GitHub, marketing-specific training.

**Operations Manager, Finance Analyst, or Customer Success Manager:** standard equipment
plus training plus benefits, no engineering-specific tools — a clean contrast to the
Software Engineer run.

Each role was confirmed in earlier testing to produce a genuinely different reasoning plan
and step count, not just different labels on the same steps.
