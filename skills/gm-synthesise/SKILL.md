---
name: gm-synthesise
description: Organises and summarises everything the brand coach has learned from the GM — classifies knowledge on the GM skill map, merges duplicates, generalises repeated rules into decision patterns, resolves conflicts, writes one summary per domain, refreshes the skill map with depth per sub-skill, and finds cross-domain themes in how the GM thinks. Use when the user says "summarise what you learned", "organise the knowledge", "show my skill map", "what do you know about how I run P&L", "what are the gaps".
---

# GM Synthesise — classify and summarise the GM's know-how

A Brand GM's skills are very broad. Conversations produce knowledge in no particular order. This skill turns it into a clear map: what the GM knows, how they think in each domain, how deep the coach's copy is, and what is still missing.

Shared references in `../../shared/` relative to this skill's base directory (`${CLAUDE_PLUGIN_ROOT}/shared/`): read `classify-and-synthesise.md` (the method, always), `competency-framework.md` (skill map), `decision-logic-capture.md` (pattern structure), `knowledge-card-format.md`, `language-and-glossary.md`.

## Steps

1. **Inventory.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb_tool.py validate .` (fix errors) and read all items in `knowledge/` (approved and draft), `gm-mind.md`, recent `conversations/`, and `exam/shadow/`. Without Python, use Glob/Grep and read front matter.

2. **Classify.** Check every item has the right `domain`, primary `skill`, `level` and tags (method in `classify-and-synthesise.md`). Fix obvious mistakes directly. Note unclear ones for the GM.

3. **Clean up — propose, then apply after the GM agrees:**
   - Duplicates to merge (keep all sources and contributors).
   - Three or more items with the same logic → draft ONE decision pattern that explains them; keep originals as examples. A new pattern built by Claude is a `draft` until the GM confirms it.
   - Conflicts → find the condition that separates them; if unclear, list as an open question.
   - Sub-skills to split or mark "not relevant to <Brand>"; new sub-skills to add for this brand (record in the domain summary).
   Show the proposals as a short numbered list in the GM's language; the GM answers "ok all", or by number.

4. **Write domain summaries** `summaries/<Dn>-<slug>.md` for every domain with at least one approved item, using the template in `classify-and-synthesise.md`. Write in the workspace default language with key terms in English; cite item IDs and contributor names. Summaries describe only approved knowledge; drafts go in "Tensions & open questions".

5. **Refresh the skill map.** Run `kb_tool.py skillmap .` and `kb_tool.py fidelity .` (or build `skill-map.md` by hand with the same depth rules). Add at the bottom: top 5 gaps as natural conversation openers.

6. **Cross-domain themes.** Look across all domains for the GM's recurring logic (same priority order, same first question, same way of testing small before scaling, same people judgement). Propose up to 5 as "I notice you often … — is this how you think?" Add confirmed ones to `gm-mind.md` with "(synthesis <date>)".

7. **Connect the thinking.** Check `links` across items: every pattern should link to the cases, reasoning examples or Shadow rounds it came from, and to its principles; add missing links (propose, GM agrees). Conclusions with no reasoning behind them (a rule or pattern with no case, reasoning example or GM quote) → list them as "ask the GM why" topics for gm-talk.
8. **Read the flags.** Include `feedback/` (open and closed) in the domain summaries' "Tensions & open questions" and "Gaps"; clusters of flags lower a sub-skill's depth until a retro closes them.
9. **Rebuild** `index.md` with `kb_tool.py index .`.

## Report to the GM (one screen, their language)

- **Your skill map in one look**: count of sub-skills by depth ⬜ 🟡 🟠 🟢, and the 3 strongest and 3 weakest areas.
- **How you think — in 5 lines**: the cross-domain themes (confirmed ones).
- **Changes made**: merged N, new patterns proposed N, conflicts found N.
- **Shadow GM match rate** overall and the domain with the lowest match.
- **Next 3 conversations** to have, as questions.

When asked about one domain only ("what do you know about how I run P&L?"), show that domain's summary in plain language and ask: "What is wrong or missing?" — then continue in gm-talk.
