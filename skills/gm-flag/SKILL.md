---
name: gm-flag
description: Lets anyone using the brand coach (store manager, area manager, successor, crew) flag a coach answer that did not fit their situation, so the Brand GM can review it in a retro. Use when the user says "this answer is wrong", "doesn't fit my store", "not helpful", "flag this", "report to GM".
---

# GM Flag — "this answer did not fit"

Shared references in `../../shared/` relative to this skill's base directory (`${CLAUDE_PLUGIN_ROOT}/shared/`): read `feedback-format.md` (file format, always), `privacy-and-safety.md`, `language-and-glossary.md`.

Make flagging take under one minute. Thank the person: their flag teaches the coach something the GM did not think to mention.

## Steps

1. Find the answer being flagged: the most recent coach answer in this conversation (question, the answer, and the item IDs it cited). If there is none, ask the person to paste the question and the answer.
2. Ask at most three short questions, one at a time, in their language:
   1. "What was not right?" → offer: ❌ wrong · 🏪 does not fit my store/situation · ❓ missing something · 😕 unclear · 📅 out of date
   2. "What is different about your situation?" (numbers, store type, what they know that the coach did not)
   3. Optional: "What did you do, or plan to do?"
3. Ask their role and store type (not their name). If they would like credit when their flag leads to new knowledge, record `asker_credit: <name>`.
4. Classify the question's sub-skill (`competency-framework.md`).
5. Write `feedback/<id>.md` with `status: open` exactly as in `feedback-format.md`. ID: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_tool.py next-feedback .`, or `F-<today YYYYMMDD>-<next 3-digit number>` from the files in `feedback/`. Remove any staff or guest personal data.
6. Confirm in one or two lines: "Sent to the Brand GM for review". If useful, add what they can safely do meanwhile, without contradicting red lines.

Never change knowledge items here. Only the Brand GM changes the coach, in gm-retro.
