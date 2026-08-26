# Screen Recording Guide (silent capture, narrate later in ElevenLabs/CapCut)

No talking needed during capture. Just hit these in order, hold where noted, cut the rest in
CapCut. Timings below are measured from two live timed runs on 2026-08-26, not estimates.

## Before you hit record

1. Start the backend: open a terminal in the repo root, run
   ```
   python -m onboardflow.server
   ```
2. Start the frontend: open a second terminal, run
   ```
   npm run dev
   ```
   (from the `frontend/` folder, or `npm run dev --prefix frontend` from repo root)
3. Open `http://localhost:5173` in a clean browser window. Close every other tab.
4. Resize the browser window to something clean, 1920x1080 or 1280x720. Zoom to 100 percent
   (Ctrl+0) so text isn't tiny or huge on export.
5. Confirm the header badge says "API: ✅ Online" before you start recording. If it says
   "Offline," the backend isn't up yet, don't record until it flips green.

## Take 1: Software Engineer (the main run, show this one in full)

Type these exact values into the form:

| Field | Value |
|---|---|
| Employee Name | Jordan Lee |
| Role | Software Engineer |
| Department | Engineering (dropdown) |
| Start Date | any date a few weeks out |
| Email | jordan.lee@example.com |
| Manager | Alex Rodriguez |

Click **Start Onboarding**.

**What happens and when (measured, not estimated):**
- 0:00 → click. Button goes to "Processing..." with a spinning brain icon and "Agent is
  reasoning..." text.
- 0:00-0:12 → nothing else changes on screen. This is Gemini thinking. Don't cut this out
  entirely, a couple seconds of it is good, it's the "reasoning, not scripted" beat.
- ~0:12 → the "Agent Reasoning" paragraph appears, and step cards start populating and turning
  green one by one.
- ~0:12-0:35 → all 10 step cards fill in and go green, fastest part to watch, this is the part
  worth lingering on and possibly speeding up 1.5-2x in the edit.
- ~0:35-0:36 → the header flips to "✅ Workflow complete!"

**Hold on the completed screen for 2-3 full seconds before doing anything else.** That green
"Workflow complete!" state is the payoff shot, don't cut away from it too fast.

Total run time to plan around: **about 35-40 seconds, click to complete.**

## Take 2: HR Coordinator (the "it adapts" beat)

Reload the page (or just refill the form over the completed one, either works). Use:

| Field | Value |
|---|---|
| Employee Name | Maria Santos |
| Role | HR Coordinator |
| Department | HR (dropdown) |
| Start Date | any date a few weeks out |
| Email | maria.santos@example.com |
| Manager | leave blank |

Click **Start Onboarding** again.

Same shape as Take 1, but watch for: no GitHub step this time, and only 9 step cards instead of
10. That contrast (fewer/different steps for a non-engineering role) is the entire point of this
clip, so frame the edit to put both step lists on screen at some point, side by side or back to
back, so the difference actually reads.

Total run time: **about 33-35 seconds.**

You don't need to record this one in full if you're keeping the video lean. Ten seconds of it
starting to diverge from Take 1's step list is enough, cut in fast.

## Take 3: Chatbot (short, one question is plenty)

1. Click the **💬 Ask Questions** tab at the top (only appears after a workflow has run).
2. Click the suggested question chip **"When will I receive my equipment?"** (don't type, the
   chip click is cleaner on camera and faster).
3. Wait about 3-4 seconds for the answer to stream in, including the "RELATED RESOURCES" links
   at the bottom.
4. Hold 1-2 seconds on the finished answer, then stop.

## What to skip if you're keeping this lean

- **Pub/Sub / terminal demo**: skip it. It requires switching to a terminal window and re-explaining
  what Pub/Sub is, not worth the runtime for a lean cut. It's confirmed working if you ever want to
  add it back in later, just not today.
- **Architecture diagram**: skip it for now. It still has the open ADK/Firestore accuracy question
  we haven't resolved, don't put it on camera until that's settled.

## Minimum viable recording order (if you want the absolute leanest cut)

1. Take 1, full (35-40s, this is the one complete demonstration)
2. Take 2, first ~10s only, showing the different reasoning + fewer steps
3. Take 3, full (10-15s)

That's roughly 60-65 seconds of raw footage to work with in CapCut, plenty to cut down to a
tight 2-3 minute video once you add ElevenLabs narration over it, with room to slow down or
freeze-frame on the good beats (the reasoning text, the green "Workflow complete!", the chatbot
answer).
