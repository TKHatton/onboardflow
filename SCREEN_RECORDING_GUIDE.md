# Screen Recording Guide (silent capture, narrate later in ElevenLabs/CapCut)

No talking needed during capture. Just hit these in order, hold where noted, cut the rest in
CapCut. Timings below are measured from live timed runs against the actual deployed URLs,
not localhost, not estimates. Updated 2026-08-27 to add Take 5 (Firestore history), now
that state persistence is genuinely wired in.

**Record against the live app, not a local dev server:**
- App: https://onboardflow-hackathon.netlify.app
- API: https://onboardflow-883489836236.europe-west1.run.app

The frontend was redesigned today too: warm paper background, dark header, burnt-orange
accent, not the old purple gradient. Make sure what's on screen matches that before you hit
record. If it still looks like a purple gradient, hard-refresh (Ctrl+Shift+R) to clear a
cached old version.

## Before you hit record

1. Open https://onboardflow-hackathon.netlify.app in a clean browser window. Close every
   other tab.
2. Resize the browser window to something clean, 1920x1080 or 1280x720. Zoom to 100 percent
   (Ctrl+0) so text isn't tiny or huge on export.
3. Confirm the header badge says "API: ✅ Online" before you start recording. If it says
   "Offline," wait a few seconds and refresh, Cloud Run may be cold-starting after being
   idle, which can take a few extra seconds on the very first hit.
4. Have a terminal window ready off to the side for Take 4 (Pub/Sub), open it now so you're
   not fumbling for it mid-recording. Open PowerShell (Start menu, type "powershell", Enter),
   then run:
   ```
   cd C:\Dev\GitHub\onboardflow
   ```
   Leave this next command typed out but **not run** until Take 4 (this is PowerShell syntax,
   not the Unix-style `VAR=value command` form, that fails silently in PowerShell):
   ```
   $env:BACKEND_URL="https://onboardflow-883489836236.europe-west1.run.app"; python test_pubsub.py
   ```
   Confirmed working against this exact live URL and in this exact PowerShell form on
   2026-08-27 (200 OK, workflow ID returned). Without `BACKEND_URL` set, it defaults to
   localhost, which won't be running.

## Take 1: Software Engineer (the main run, show this one in full)

Type these exact values into the form:

| Field | Value |
|---|---|
| Employee Name | Jordan Lee |
| Preferred Name (Optional) | Jordan |
| Pronouns (Optional) | he/him |
| Role | Software Engineer |
| Department | Engineering (dropdown) |
| Start Date | any date a few weeks out |
| Email | jordan.lee@example.com |
| Manager (Optional) | Alex Rodriguez |

Click **Start Onboarding**.

**What happens and when (measured, not estimated):**
- 0:00, click. Button goes to "Processing..." with a spinning brain icon and "Agent is
  reasoning..." text.
- 0:00-0:12, nothing else changes on screen. This is Gemini thinking. Don't cut this out
  entirely, a couple seconds of it is good, it's the "reasoning, not scripted" beat.
- ~0:12, the "Agent Reasoning" paragraph appears, and step cards start populating, each one
  turning its status color as it completes.
- ~0:12-0:35, all 10 step cards fill in, fastest part to watch, this is the part worth
  lingering on and possibly speeding up 1.5-2x in the edit.
- ~0:35-0:36, the header flips to "✅ Workflow complete!"

**Hold on the completed screen for 2-3 full seconds before doing anything else.** That state
is the payoff shot, don't cut away from it too fast.

Total run time to plan around: **about 35-40 seconds, click to complete.**

## Take 2: a second role (the "it adapts" beat)

Reload the page (or just refill the form over the completed one, either works). Use an HR
Coordinator, Marketing Manager, or any non-engineering role:

| Field | Value |
|---|---|
| Employee Name | Maria Santos |
| Preferred Name (Optional) | Maria |
| Pronouns (Optional) | she/her |
| Role | HR Coordinator |
| Department | HR (dropdown) |
| Start Date | any date a few weeks out |
| Email | maria.santos@example.com |
| Manager (Optional) | leave blank |

Click **Start Onboarding** again.

Same shape as Take 1, but watch for: no GitHub step this time, and fewer step cards overall
(9 instead of 10 for HR Coordinator). That contrast is the entire point of this clip, it's
the proof that nothing is hardcoded per role. Let at least the reasoning paragraph and first
few steps play out so the difference actually reads on screen; you don't need the full
completion.

Total run time if played in full: **about 33-35 seconds.**

## Take 3: New Hire screen, checklist first, then the chatbot on demand

This is the shot that proves the new hire has a completely different screen from HR, not
just another tab in the same admin view. Don't cut straight to the chatbot, show the switch
and let the checklist land first, that's the default view now, not the chat window.

1. At the top of the page, click the **👤 New Hire** button in the "Viewing as:" switcher
   (it's next to 🧑‍💼 HR Team). Hold 1-2 seconds on this switch, it's a full-screen change:
   greeting plus the **Your Onboarding Checklist** panel (Still On You / Already Handled For
   You), no admin tools anywhere.
2. Hold 2-3 seconds on the checklist itself, this is the payoff of this shot, let the
   checkmarks and due dates actually be readable.
3. Click the **💬 Ask Your Onboarding Assistant** button near the bottom. The chatbot opens
   below the checklist, with a **✕ Close Assistant** button above it.
4. Click the suggested question chip **"When will I receive my equipment?"** (don't type, the
   chip click is cleaner on camera and faster).
5. Wait about 3-4 seconds for the answer to stream in, including the "RELATED RESOURCES" links
   at the bottom.
6. Hold 1-2 seconds on the finished answer, then click **🧑‍💼 HR Team** to switch back before
   moving to Take 4, that return switch reinforces the split too.

## Take 4: Pub/Sub trigger (don't skip this one)

This is what proves the agent isn't just wired to a form, and it's what a judge assessing
architecture will actually care about seeing.

1. Front the terminal window you set up earlier (already `cd`'d into the repo root).
2. Run:
   ```
   $env:BACKEND_URL="https://onboardflow-883489836236.europe-west1.run.app"; python test_pubsub.py
   ```
3. **Do not switch away or stop recording yet.** It takes about 3-5 seconds to finish. You'll
   see it print the fake employee data first, that's not the end, keep the terminal on screen.
4. **You'll know it's actually done when you see these two lines, in this order, near the
   bottom:**
   ```
   Response Status: 200

   ✓ SUCCESS: Pub/Sub message processed successfully!
   ```
   Everything above that (the JSON payload, "Sending to...") is setup, not the result. Wait
   for the word **SUCCESS** specifically.
5. Once you see `✓ SUCCESS`, hold 1-2 more seconds on that line before cutting or moving on.

If you'd rather not context-switch to a terminal mid-recording, a screenshot of this output
with narration over it works too. Just don't cut it entirely.

## Take 5: Firestore history (the payoff for Take 4)

This is the shot that proves the Pub/Sub run you just triggered from a terminal, with no
browser involved at all, actually persisted to Firestore.

1. Switch back to the browser tab, make sure you're on the **🧑‍💼 HR Team** view.
2. Click the **📨 Onboarding Activity** tab.
3. Click **Refresh** if the run from Take 4 isn't showing yet (it usually is immediately).
4. Hold 2 seconds on the list. The employee name and workflow ID should visibly match what
   just printed in the terminal in Take 4, that match is the whole point of this shot.

Total time: **5-10 seconds**, but don't rush the hold at the end.

## Recording order

1. Take 1, full (35-40s): the one complete demonstration
2. Take 2, at least the reasoning and first few steps (10-15s): the adaptability proof
3. Take 3, full (20-25s): the view switch, the checklist, then the chatbot on demand
4. Take 4, full (10-15s): Pub/Sub, the architecture proof
5. Take 5, full (5-10s): Firestore history, the proof Take 4 was genuine

That's roughly 85-105 seconds of raw footage, enough to build a tight 4:00-4:20 final video
once you add ElevenLabs narration and slow down or freeze-frame the good beats (the
reasoning text, the completed state, the Pub/Sub response, the matching history entry) per
`DEMO_SCRIPT.md`.
