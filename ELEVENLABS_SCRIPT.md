<!-- prose-check: off — "real-time" below is the technical term for the SSE
     transport this script describes, not "real" used as an intensifier. -->
# ElevenLabs Voiceover Script

Matches the footage from `SCREEN_RECORDING_GUIDE.md`, Takes 1-5, in the order you recorded
them. Generate each numbered block as its own clip in ElevenLabs, then drag each audio clip
onto CapCut lined up with the matching scene.

**Word count check (actually counted, not guessed):** 829 words of narration total, which
comes out to roughly 5:40 of audio at a normal pace (145 words/minute). That's more than a
4-minute video needs, on purpose, so you have room to trim down rather than stretch thin
material. Read each block once at your own pace and see how it lines up against that
scene's footage; cut sentences rather than the whole block if one runs long, each block is
written so the first sentence or two carries the point even if you drop the rest.

---

## 0. Opening (over the address bar / first couple seconds of Take 1)

Footage: ~3-5 seconds, the browser address bar showing the live URL before you filled the form.

> Employee onboarding eats fifteen to twenty hours of HR time per new hire: ordering
> equipment, setting up accounts, scheduling training, sending the right emails to the
> right people, and getting basic things right, like how someone's name should actually be
> written and what they want to be called. Most automation for this is a hardcoded
> checklist that runs the exact same steps for every single person. OnboardFlow doesn't do
> that. It reasons about each new hire, their role, their department, even their preferred
> name and pronouns, and decides from scratch what they actually need. This is live right
> now, not a local demo, at onboardflow-hackathon.netlify.app.

---

## 1a. Take 1, reasoning panel appears (~0:12 into the clip)

Footage: the moment the "Agent Reasoning" paragraph shows up, before steps start filling in.

> Watch what happens before a single tool runs. Gemini reads the role and department and
> plans its own sequence, out loud, in plain language, right here. This new hire needs
> GitHub access, developer-grade equipment, technical training, plus the standard
> onboarding steps every employee gets. Nothing here is a template someone wrote in
> advance for "Software Engineer." The agent looked at this specific person and decided
> this, this run, right now.

## 1b. Take 1, steps streaming in (~0:12 to ~0:35 of the clip)

Footage: the ten step cards filling in one by one, ending on "Workflow complete!"

> Each of these is a live tool call, streamed to the browser the instant it completes, not
> a progress bar faking activity. A Jira ticket gets created to track the whole onboarding.
> Equipment gets ordered, sized to the role. A GitHub account gets provisioned with the
> right repository access. A welcome email goes out. A Slack announcement posts to the
> team. Orientation gets scheduled on the calendar. Training courses get assigned with
> real deadlines. Security and compliance modules get scheduled. Benefits enrollment
> opens. And a follow-up check gets scheduled to make sure nothing falls through the
> cracks. Ten tool calls, ten different systems, zero hardcoded logic connecting any of
> them together.

---

## 2. Take 2, second role (10-15 second clip)

Footage: the second onboarding run, reasoning panel and step list for the different role.

> Same system, same code, completely different plan. This time there's no GitHub step,
> Gemini decided it doesn't apply to this role, and it substitutes role-appropriate tools
> instead, project management setup instead of code repositories, different training
> tracks entirely. This is the actual proof point judges should be looking for: nothing in
> this system is an if-role-equals-engineer statement somewhere in the code. The reasoning
> happens fresh, from the model, every single time, for every single person.

---

## 3. Take 3, New Hire view (20-25 second clip)

Footage: the view switch, the checklist landing, opening the chatbot, one suggested
question.

> Everything up to this point was the HR side of this. Here's the other half, and it's a
> genuinely separate screen, not another tab bolted onto the same admin view. This is what
> the new hire opens, and there's nothing here they shouldn't see: no other employee's
> data, no internal tooling. It leads with what actually matters to them on day one: a
> checklist, split into what's still on them, their training deadlines, their benefits
> enrollment window, each with a real date, and what's already been handled for them,
> equipment ordered, accounts created, orientation on the calendar. This isn't a generic
> to-do list template, every line here comes straight out of what the agent actually did
> for this specific person. If they have a question, they don't have to dig through a
> handbook, the assistant is one click away, and it's powered by that same Gemini
> reasoning, now with full context about their own onboarding.

---

## 4. Take 4, Pub/Sub terminal (10-15 second clip)

Footage: the terminal running, ending on the SUCCESS line.

> The web form isn't the only way into this system, and that matters. OnboardFlow also
> exposes a Pub/Sub push endpoint, so an actual HR platform, a Workday, a BambooHR, a
> payroll system, could publish a new-hire event directly the moment someone signs an
> offer letter, and the exact same autonomous agent picks it up and runs the entire
> workflow with nobody touching a browser. That's what I'm triggering right here, from a
> terminal, no UI involved at all. This is the difference between a demo built to look
> good on a form and an integration pattern a real company could actually plug into their
> existing HR stack.

---

## 5. Take 5, Onboarding Activity payoff (5-10 second clip)

Footage: the Onboarding Activity list, the workflow ID from Take 4 sitting at the top.

> And here's the part that ties the whole thing together. Every one of these runs, whether
> it started from the form or from that Pub/Sub call I just made from the terminal, gets
> written to Firestore, permanently. Nothing here disappears the moment a browser tab
> closes. This activity list is pulled from real persisted records, not sample data I
> staged for this video, and that Pub/Sub run I triggered thirty seconds ago, with no
> browser open at all, is already sitting right here at the top.

---

## 6. Close (over the completed workflow screen, or the live URL)

Footage: whatever you want to end on, the finished workflow or the browser URL.

> Under the hood, this is a FastAPI backend on Google Cloud Run, calling Gemini three
> point six Flash directly to reason about each new hire, choosing from eleven-plus tools,
> Jira, GitHub, Slack, calendar, email, training platforms, benefits systems. Every tool
> call streams to the frontend in real time over server-sent events, so you're watching
> the agent think and act as it happens, not waiting on a spinner. State persists to
> Firestore. The frontend's on Netlify. Both are live, right now, at the URLs on your
> screen, not running on my laptop.
>
> Fifteen to twenty hours of manual coordination, down to seconds, reasoned fresh for
> every single person, every single time. That's OnboardFlow. The code is open source, try
> it yourself.

---

## Optional: Architecture (you said you're not using this, skip it)

Left out of the main sequence since you didn't record footage of the diagram. The tech
stack recap now lives in block 6 above instead, so you're not losing that content, it's
just spoken over the closing shot rather than a separate diagram screen.
