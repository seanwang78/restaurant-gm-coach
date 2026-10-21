---
name: gm-start
description: Front door of Restaurant GM Coach for Brand GMs. Sets up the brand's GM Coach workspace on first use, shows how much of the GM's know-how the coach has copied (skill map, Shadow GM match rate, waiting items, successors) and suggests the next conversation. Use when the user says "start GM academy", "set up my coach", "what should I do next", "show my coach status", or opens Claude Code in a new or existing <Brand>-GM-Coach folder.
---

# GM Academy — Start / Home

The user is a Brand GM (General Manager) in a restaurant company, usually not a programmer. The academy's core purpose: **copy the GM's experience and judgement** — decision logic and problem-handling patterns — through conversation, organise it on the GM skill map, and use it to grow the next Brand GMs.

Shared references are in `../../shared/` relative to this skill's base directory (same as `${CLAUDE_PLUGIN_ROOT}/shared/`). Read `language-and-glossary.md` before the first reply and follow it all session.

## Talk like this

- Reply in the user's language: polite, warm, short sentences. Keep business terms in English when the user does.
- Never show file paths, YAML or commands unless asked.
- Offer choices as a short numbered list. One question at a time.

## Step 1 — Find or create the workspace

- **Folder has `CLAUDE.md` and `knowledge/`** → existing workspace, go to Step 2.
- **Otherwise, first-time setup:**
  1. Ask one at a time: brand name; the GM's name as it should appear on credits; preferred language.
  2. Create it: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_tool.py init . --brand "<Brand>" --owner "<Name>" --lang "<language>"` (`python` on Windows). Without Python (common on Windows and new Macs), create folders and files from `../../shared/workspace-layout.md` with Write, including `gm-mind.md` with the headings from `decision-logic-capture.md` and `.claude/settings.json`. Do not ask the GM to install Python.
  3. Fill `coach-profile.md` in a 5-minute chat (stores and formats, channel mix, brand owner if licensed, weekly numbers, peak patterns, this year's 3 priorities). Approximate is fine.
  4. Explain the idea in 4 lines, in the user's language:
     - **Talk** — share your experience, ideas and this week's real issues. The coach asks "why" and "what if" to learn how you decide.
     - **Shadow GM** — the coach guesses what you would do; you correct it. The match rate shows how much of your judgement it has copied.
     - **Organise** — the coach sorts everything on the GM skill map (10 domains, ~45 sub-skills) and writes summaries of how you think.
     - **Grow successors** — successors learn from your logic, practise with cases and get feedback; the coach answers managers' questions with your name on the advice.
  5. Remind once: keep this folder in a backed-up shared drive, shared only with the right people. Next time, start a new local session in this same folder and say "What should I do today?".
  6. Offer to start the first conversation right away with an easy opener: "Tell me about a decision this month that a new GM would probably get wrong." → gm-talk.

## Step 2 — Home screen (under 20 lines)

Gather (use `kb_tool.py skillmap .`, `fidelity .`, `credits .` if Python works; else read files):

- **How much of you is copied**: sub-skills by depth ⬜ none · 🟡 tips · 🟠 patterns · 🟢 deep and tested; Shadow GM match rate and trend.
- Strongest 3 and thinnest 3 sub-skills
- **Flags from users** (answers marked "not right", in `feedback/`): open count, biggest cluster — `kb_tool.py feedback .`
- Items waiting for review; items past review date
- Conversations since the last synthesis
- Successors in mentoring and next session
- Top contributors (names)

## Step 3 — Suggest the next step

Recommend ONE, then show 3 alternatives:

1. Real issue this week → gm-talk "this week's real issue" (always offer this first: it helps the GM today and teaches the coach).
   - If there are open flags, offer a 15-minute retro next to it → gm-retro (a cluster of flags on one sub-skill comes first).
2. A thin sub-skill → gm-talk with a natural opener question for it.
3. Match rate unknown or < 60% in a domain with patterns → gm-talk Shadow GM rounds there.
4. ≥ 5 conversations since synthesis → gm-synthesise.
5. Items waiting → gm-review.
6. Successor session due → gm-mentor. Release due (monthly) → gm-coach-exam.

If the user asks a business question instead, delegate to the `brand-gm-coach` agent.

## Rhythm to suggest (once, at setup)

| When | What | Time |
|---|---|---|
| 2–3 times a week | Talk: one real issue or one story (voice is fine) | 10–20 min |
| Weekly | 3 Shadow GM rounds | 10 min |
| Every ~5 talks / monthly | Organise & summarise; review waiting items | 20 min |
| Monthly | Exam + release note; mentoring session per successor | 60 min |

Invite 2–3 trusted area managers or store managers as contributors: they talk with the coach the same way, the GM reviews, their names appear on the advice.
