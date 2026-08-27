<!-- prose-check: off — "real-time" below is the technical term for the SSE
     transport this checklist describes, not "real" used as an intensifier. -->
# OnboardFlow - Hackathon Submission Checklist

## Current Status
✅ Core application built and tested locally
✅ 11+ tools implemented
✅ Autonomous agent with Gemini AI
✅ React frontend with real-time dashboard, redesigned 2026-08-26 (was generic purple-gradient scaffolding)
✅ Chatbot assistant for Q&A
✅ Code pushed to GitHub
✅ **Deployed live, 2026-08-26, Firestore added 2026-08-27:**
  - Backend (Cloud Run): https://onboardflow-883489836236.europe-west1.run.app
  - Frontend (Netlify): https://onboardflow-hackathon.netlify.app
  - Verified end-to-end against the live URLs: full onboarding workflow, chatbot, Pub/Sub
    trigger, and Firestore-backed Past Onboardings history, all clean
  - Architecture diagram matches the running code (ADK removed, Firestore genuinely wired
    in, not just described)

## Pre-Submission Tasks

### 1. API Key Setup: DONE
- [x] Set GOOGLE_API_KEY in .env file on this server
- [x] Test autonomous agent execution
- [x] Verify all 11+ tools work correctly
- [x] Test chatbot functionality

### 2. Google Cloud Deployment: DONE (2026-08-26)
- [x] Create Google Cloud project (used existing billed project `gen-lang-client-0721805096`)
- [x] Enable required APIs (Cloud Run, Cloud Build auto-enabled by the deploy flow)
- [x] Deploy backend to Cloud Run: https://onboardflow-883489836236.europe-west1.run.app
- [x] Deploy frontend to Netlify: https://onboardflow-hackathon.netlify.app
- [x] Set up environment variables in Cloud Run (GOOGLE_API_KEY)
- [x] Test deployed application (full workflow + chatbot verified live)
- [x] Get public URLs for submission (both above)

### 3. Demo Video Recording
- [ ] Follow `DEMO_SCRIPT.md` (updated 2026-08-26 for the live URLs and the new design)
- [ ] Record screen capture per `SCREEN_RECORDING_GUIDE.md`
- [ ] Add voiceover (ElevenLabs) and edit in CapCut
- [ ] Upload to YouTube (unlisted or public)
- [ ] Get shareable link

### 4. Architecture Diagram
- [ ] Create/update architecture diagram showing:
  - React frontend
  - FastAPI backend
  - Gemini AI integration
  - All 11+ tools
  - Data flow
- [ ] Export as PNG/SVG
- [ ] Add to README and submission

### 5. Documentation
- [ ] Update README.md with:
  - Project overview
  - Features list
  - Setup instructions
  - Deployment guide
  - Screenshots/GIFs
- [ ] Create ARCHITECTURE.md
- [ ] Add code comments where needed

### 6. Devpost Submission
- [ ] Create account on Devpost (if needed)
- [ ] Find "All Things Agentic" hackathon
- [ ] Fill out submission form:
  - Project name: OnboardFlow
  - Tagline
  - Short description (500 chars)
  - Full description (from docs/devpost_submission_v2.md)
  - Team members
  - Technologies used
  - Demo video link
  - Code repository link: https://github.com/TKHatton/onboardflow
  - Live demo URL: https://onboardflow-hackathon.netlify.app
- [ ] Upload architecture diagram
- [ ] Review and submit

### 7. Final Checks
- [ ] All links work (repo, demo, video)
- [ ] Code is public and accessible
- [ ] README is clear and complete
- [ ] Demo video is under 4 minutes
- [ ] Submission follows all hackathon rules
- [ ] Submitted before deadline (Aug 31)

## Post-Submission
- [ ] Share on social media (Twitter, LinkedIn)
- [ ] Monitor for judge questions/feedback
- [ ] Prepare for potential follow-up questions

## Notes
- 2026-08-26: everything above that was blocked on Norton or a missing API key is
  resolved. The app is live on Cloud Run + Netlify, verified end-to-end.
- What's left: record the demo video, finalize the architecture diagram's ADK
  question, then submit to Devpost.
