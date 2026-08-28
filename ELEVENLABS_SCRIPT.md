<!-- prose-check: off — "real-time" below is the technical term for the SSE
     transport this script describes, not "real" used as an intensifier. -->
# ElevenLabs Voiceover Script

Matches the footage from `SCREEN_RECORDING_GUIDE.md`, Takes 1-5, in the order you recorded
them. Generate each numbered block as its own clip in ElevenLabs (don't paste the whole page
in at once, they're timed to different moments in the footage), then drag each audio clip
onto CapCut lined up with the matching scene.

Each block also lists roughly how long the matching footage runs, so you know if a
generated clip is way off and needs a pacing adjustment.

---

## 0. Opening (over the address bar / first couple seconds of Take 1)

Footage: ~3-5 seconds, the browser address bar showing the live URL before you filled the form.

> Employee onboarding eats fifteen to twenty hours of HR time per new hire: ordering
> equipment, setting up accounts, scheduling training, sending the right emails to the right
> people. Most automation for this is a hardcoded checklist that runs the same steps for
> everyone. OnboardFlow doesn't do that. It reasons about each new hire's role and decides,
> from scratch, what they actually need. This is live right now at
> onboardflow-hackathon.netlify.app.

---

## 1a. Take 1, reasoning panel appears (~0:12 into the clip)

Footage: the moment the "Agent Reasoning" paragraph shows up, before steps start filling in.

> Watch what happens before a single tool runs. Gemini reads the role and department and
> plans its own sequence: this new hire needs GitHub access, developer-grade equipment,
> technical training, plus the standard onboarding steps. Nothing here is a template, the
> agent decided this.

## 1b. Take 1, steps streaming in (~0:12 to ~0:35 of the clip)

Footage: the ten step cards filling in one by one, ending on "Workflow complete!"

> Each of these is a live tool call, streamed to the browser the instant it completes: a
> Jira ticket, equipment ordered, GitHub access provisioned, a welcome email, a Slack
> announcement, orientation scheduled, training assigned, security modules scheduled,
> benefits enrollment, and a follow-up check. Ten tool calls, ten different systems, zero
> hardcoded logic connecting them.

---

## 2. Take 2, second role (10-15 second clip)

Footage: the second onboarding run, reasoning panel and step list for the different role.

> Same system, same code, completely different plan. This time there's no GitHub step,
> Gemini decided it doesn't apply, and it substitutes role-appropriate tools instead. This
> is the actual proof point: nothing is if-role-equals-engineer hardcoded. The reasoning
> happens fresh, every single time.

---

## 3. Take 3, New Hire view (20-25 second clip)

Footage: the view switch, the checklist landing, opening the chatbot, one suggested
question.

> Everything up to this point was the HR side. Here's the other half: this is the new
> hire's own screen, not another tab in the admin view, a completely separate experience
> with none of the internal tooling on it. It leads with what actually matters to them: a
> checklist of what's still on them and what's already been taken care of, each pulled
> from the workflow's own results, not a generic to-do list. If they have a question, the
> assistant is one click away, powered by the same Gemini reasoning, now with context
> about their specific onboarding.

---

## 4. Take 4, Pub/Sub terminal (10-15 second clip)

Footage: the terminal running, ending on the SUCCESS line.

> The web form isn't the only way in. OnboardFlow also exposes a Pub/Sub push endpoint, so
> an actual HR system, a Workday, a BambooHR, could publish a new-hire event directly, and
> the exact same autonomous agent picks it up and runs, with nobody touching a browser.
> This is what makes it an integration pattern instead of a demo toy: the reasoning engine
> is decoupled from the UI.

---

## 5. Take 5, Onboarding Activity payoff (5-10 second clip)

Footage: the Onboarding Activity list, the workflow ID from Take 4 sitting at the top.

> And here's the part that ties it together: every one of these runs, whether it started
> from the form or from that Pub/Sub call a second ago, gets written to Firestore. Nothing
> here is thrown away after the browser tab closes. This list is pulled from persisted
> records, that Pub/Sub run I just triggered from the terminal is already sitting in it.

---

## 6. Close (over the completed workflow screen, or the live URL)

Footage: whatever you want to end on, the finished workflow or the browser URL.

> Fifteen to twenty hours of manual coordination, down to seconds, reasoned fresh for
> every role, every time, live at onboardflow-hackathon.netlify.app right now. That's
> OnboardFlow. Code's open source, try it yourself.

---

## Optional: Architecture (only if you separately grab footage of the diagram)

You didn't record this as one of the five Takes, so there's no footage for it yet. Skip
this block entirely, or if you want it in, screen-record `docs/architecture.html` for 5-10
seconds (open it in a browser, no interaction needed) and slot this in wherever fits, most
naturally right after block 5 and before the close.

> Under the hood: a FastAPI backend on Cloud Run calls Gemini directly to reason about
> each new hire and select from eleven-plus tools, Jira, GitHub, Slack, calendar, email,
> training, benefits, and more. Every tool call streams to the React frontend in real time
> over server-sent events, so you're watching the agent think and act as it happens.
> Frontend's on Netlify, backend's on Cloud Run, both live at the URLs on screen right now.

---

## Total runtime estimate

Blocks 0 through 6 (skipping the optional architecture block) run to roughly 3:45-4:05
spoken aloud at a normal pace, matching the ~85-105 seconds of raw footage stretched with
pauses and held shots. If ElevenLabs reads faster than your footage runs, that's fine,
just add a beat of silence or slow the pacing in CapCut rather than re-recording anything.
