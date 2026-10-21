# Restaurant GM Coach

A Claude Code plugin that copies an experienced restaurant **Brand GM's judgement** into a coach agent — so the experience in one senior person's head becomes something the whole organisation can use, test and pass on.

Restaurant groups run on operating experience: how a GM reads a drop in sales, when they cut labour and when they never do, how they handle a landlord, a viral complaint, a weak store manager. Most of it is never written down. When that GM leaves, it leaves with them. Restaurant GM Coach captures it through **conversation**, not forms.

## How it works

1. **Talk.** The GM shares real issues, stories and ideas. The coach asks one question at a time and keeps going deeper — *What did you look at first? Why that option? Would you do the same in a street store, with a new manager? What would change your mind?* — until "it depends" becomes explicit logic.
2. **Structure.** What comes out is saved as **decision patterns** (first look → diagnosis → options → what matters most → decision rule → how to handle → check & adjust → boundaries), **principles**, **reasoning examples** (the GM thinking a real case through in their own words), cases, rules, benchmarks and red lines — all linked to each other.
3. **Classify and summarise.** Everything sits on a **GM skill map**: 10 domains, ~45 sub-skills (strategy, P&L, operations, guests & channels, marketing & menu, people, growth, supply chain & food safety, partners, risk & crisis) plus decision making, data mindset and influence. Domain summaries and a depth map show what is copied and what is still thin.
4. **Shadow GM.** The coach predicts what the GM would decide in a situation; the GM corrects it. The gap is the most valuable knowledge, and the match rate shows how much of the GM has been copied.
5. **Flags and retros.** Anyone using the coach can flag an answer that did not fit. The GM reviews flags in a retro, fixes the knowledge, and the case becomes a regression test.
6. **Grow successors.** Readiness assessment (L1 store → L4 ready to run the brand), 90-day plans, case drills compared step by step with the GM's reasoning, and decision reviews.
7. **Reuse in systems.** Export a **four-layer thinking package** (points, pattern structures, reasoning examples, the GM's way of thinking + tests) so ops apps and other agents reason like the GM instead of repeating conclusions.

The coach answers only from knowledge the GM approved, shows whose experience each answer comes from, and says plainly when it has not learned something yet.

## What's inside

| Part | What it does |
|---|---|
| `gm-start` skill | Sets up a brand workspace, shows how much is copied, suggests the next conversation |
| `gm-talk` skill (main) | Free sharing, this week's real issue, coach-led questions, Shadow GM, war stories, documents |
| `gm-synthesise` skill | Classifies on the skill map, merges duplicates, turns repeated rules into patterns, resolves conflicts, writes domain summaries, links the thinking |
| `gm-review` skill | Approve / edit / merge / retire items, e.g. from area managers |
| `gm-flag` skill | Any user marks an answer that did not fit their situation |
| `gm-retro` skill | GM reviews flags: GM answers first, cause found, knowledge fixed, regression test, reply to the asker |
| `gm-coach-exam` skill | Exam scenarios with rubrics, blind runs, release gate, release notes with contributor credits, export |
| `gm-mentor` skill | Successor readiness, development plans, case drills, decision reviews, progress reports |
| `brand-gm-coach` agent | Answers by walking the GM's decision patterns, cites item IDs and contributor names |
| `shared/` | Skill map, probing techniques, item formats, feedback and export formats, privacy rules, examples |
| `scripts/kb_tool.py` | Optional helper (Python 3.8+, standard library): init, validate, coverage, index, skill map, Shadow match rate, credits, feedback inbox, import flags, export |

## Install

In Claude Code (terminal, desktop app Code tab, or VS Code):

```
/plugin marketplace add seanwang78/restaurant-gm-coach
/plugin install restaurant-gm-coach@restaurant-gm-coach
```

Or from your shell: `claude plugin install restaurant-gm-coach --marketplace seanwang78/restaurant-gm-coach`

In the desktop app you can then manage it from **+** next to the prompt box → **Plugins**.

## Quick start

1. Create an empty folder for the brand, e.g. `MyBrand-GM-Coach`, somewhere backed up and shared only with the right people.
2. Open Claude Code in that folder (desktop app: Code tab → Local → choose the folder).
3. Say **"Start GM academy"**. Answer three questions and a five-minute brand profile.
4. Then just talk: *"Let me tell you about a problem this week…"* Voice dictation is fine.
5. Try **"Guess what I would do — P&L"** for a Shadow GM round.
6. After about five talks: **"Summarise what you learned and show my skill map."**
7. Anyone can ask: *"Ask the coach: our weekday lunch bills dropped 10% for three weeks — where do I look first?"*

Suggested rhythm: 2–3 talks a week (10–20 min), 3 Shadow GM rounds a week, a retro when there are flags, a summary every ~5 talks, a monthly exam and release.

## Your data stays yours

This repository contains only the method. Everything a GM teaches lives in their own workspace folder (`knowledge/`, `conversations/`, `summaries/`, `gm-mind.md`…), never in the plugin. The skills avoid storing staff or guest personal data (roles, not names), keep mentoring notes private, and treat food safety, legal compliance and brand-owner standards as locked red lines.

## Adapting it

- **Skill map:** edit `shared/competency-framework.md` to fit your company; `kb_tool.py` reads the sub-skill table from it.
- **Language:** the coach replies in the user's language; items are written in the contributor's language with an optional second-language title.
- **Systems:** `shared/export-format.md` (thinking package) and `shared/feedback-format.md` (flags as JSON) are the contract for connecting ops apps, chat bots or other agents.

## License

MIT — see [LICENSE](LICENSE).
