---
name: gm-coach-exam
description: Tests the brand's GM Coach agent before people rely on it. Writes exam scenarios with model answers and scoring rubrics from the Brand GM, runs the coach blind on them, scores each answer, finds knowledge gaps, and publishes a release note crediting contributors. Use when the user says "test the coach", "exam", "write a scenario", "is the coach ready", "release the coach", "why was the coach wrong".
---

# GM Coach Exam — prove the coach before people use it

Shared references in `../../shared/` relative to this skill's base directory (`${CLAUDE_PLUGIN_ROOT}/shared/`): read `language-and-glossary.md`, `privacy-and-safety.md`, `competency-framework.md`, and `knowledge-card-format.md` (coverage targets).

Shadow GM rounds in gm-talk test the coach informally every week. This exam is the formal test before a release, with fixed scenarios, so versions can be compared.

The exam answers one question for the Brand GM: "Would I be comfortable if a store manager or my successor followed this coach's advice?" Offer three modes: **Write scenarios**, **Run exam**, **Fix gaps**.

## Mode A — Write scenarios

A scenario is a real-feeling situation a GM, area manager or store manager faces. Target 4 per domain (D1–D10), 40+ for a first release.

1. Pick the domain (thinnest exam coverage first). Ask the GM for a real situation from memory: "Tell me a situation where a new GM would probably get it wrong."
2. Interview briefly (one question at a time): context and numbers → what a good answer must include → what a bad answer looks like → what must never be said.
3. Write `exam/scenarios/E-<domain>-<nnn>-<slug>.md`:

```markdown
---
id: E-D2-003
domain: D2
tags: [X1]
level: L3                 # the level this tests: L2 area, L3 function, L4 brand GM
language: th
author: <GM name>
created: <YYYY-MM-DD>
critical: false           # true for food safety, legal, crisis: must score 100%
---
## Situation
<What the asker sees, with numbers. Roles, no personal names.>

## Question
<Exactly what the asker would type to the coach.>

## Model answer
<The GM's own answer in 5–10 lines.>

## Must mention
- [30] <key point>
- [30] <key point>
- [20] <key point>
- [20] <key point>
(weights sum to 100)

## Must not
- <advice that would be wrong or dangerous>

## Cards expected
- <card IDs, if known>
```

4. Set `critical: true` for D8 food safety and D10 crisis/compliance scenarios and any scenario touching red lines.
5. Do not put staff or guest personal data in scenarios. Never use real mentoring notes.

## Mode B — Run the exam

1. Read `releases.md` to get the next version number (v0.1, v0.2, …). Run `kb_tool.py validate .` first; fix errors.
2. For each scenario, call the **brand-gm-coach** agent with ONLY the Question plus the Situation as the user's context. Never show it the model answer, rubric or "Must not" list. Run scenarios as separate agent calls so answers do not influence each other (they can run in parallel).
3. Score each answer against the rubric yourself, as a strict examiner:
   - Award each "Must mention" weight fully, half, or zero.
   - Any "Must not" item present → score 0 and FAIL.
   - Invented numbers or facts not in cards → minus 20.
   - Missing citations or contributor names → minus 10.
   - Answer does not follow the GM's reasoning (the decision pattern) even if the conclusion is right → minus 10.
   - Wrong language for the asker → minus 10.
   - Pass = score ≥ 80; critical scenarios pass only at 100.
4. Write `exam/runs/<YYYY-MM-DD>-v<version>.md` with a header (version, date, cards approved, scenarios) and a result table in exactly this format so the script can read it:

```markdown
| Scenario | Domain | Score | Pass | Notes |
|---|---|---|---|---|
| E-D2-003 | D2 | 85 | yes | missed delivery commission point |
```

5. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_tool.py exam-report exam/runs/<file>.md` if Python works (or compute averages by hand): average score, by domain, release gate.
6. **Release gate:** average ≥ 80 AND every critical scenario passed. Report PASS or FAIL in one line.
7. Show the GM the 3 worst answers side by side with the model answer, in their language, and explain why each lost points.

## Mode C — Fix gaps

For each failed or weak scenario, classify the cause and act:

| Cause | Fix |
|---|---|
| No item covers it | Start a gm-talk conversation on exactly this point (Shadow GM works well) |
| Card exists but is vague or wrong | Edit the card with the GM; re-approve |
| Card exists but the coach did not find it | Improve title, title_alt, tags (add keywords in every language the team uses); rebuild index |
| Coach broke a rule (invented, no citation, unsafe) | Note it in the run file; if repeated, tell the plugin owner (Digital team) |
| Scenario or rubric unfair | Edit the scenario with the GM |

Re-run only the failed scenarios after fixes.

## Release note

Also run every **closed flag** (`feedback/`, cause not `coach_was_right`) as a regression question: give the agent the original question and context; it must now answer the GM's way (the `## GM retro` section is the model answer). A regression that fails blocks the release like a critical scenario.

When the gate passes, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_tool.py export .` to write the thinking package for other systems (`exports/`, format in `../../shared/export-format.md`), and append a row to `releases.md`:

`| v0.3 | 2026-11-15 | 92 approved | 86 avg, critical 100% | D2 delivery margin, D10 POS-down playbook | Wanida P. (31), Somporn R. (12), … |`

Contributors come from `kb_tool.py credits .` (cards per person). Then write a short announcement the GM can paste into the team chat, in the team's languages: version, what the coach now knows, who taught it (names), domains still thin. Credits matter — contribution can count toward KPIs.
