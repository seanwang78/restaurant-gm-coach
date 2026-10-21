---
name: gm-retro
description: Runs a retro (after-action review) with the Brand GM on coach answers that users flagged as not right — shows each flagged case, finds why the coach got it wrong, asks the GM how they would really think it through, fixes the knowledge (boundaries, new patterns, reasoning examples), turns the case into a regression test, and drafts a reply to the person who flagged it. Use when the user says "review flags", "retro", "what did people flag", "why was the coach wrong", or when gm-start shows open feedback.
---

# GM Retro — learn from answers that did not fit

Shared references in `../../shared/` relative to this skill's base directory (`${CLAUDE_PLUGIN_ROOT}/shared/`): read `feedback-format.md`, `decision-logic-capture.md` (probing, pattern and reasoning-example structure), `knowledge-card-format.md` (links), `classify-and-synthesise.md`, `language-and-glossary.md`, `privacy-and-safety.md`.

Only the owner Brand GM (or a delegate named in `CLAUDE.md`) runs a retro and changes knowledge.

## 1. Show the inbox

Run `kb_tool.py feedback .` (or read `feedback/` front matter). Show in the GM's language, under 10 lines:
- Open flags: count, grouped by sub-skill, oldest first.
- Clusters: 2+ flags on the same sub-skill or the same item → "3 flags on M-D2-001 (staffing when sales drop)". Start with clusters; they show a real gap.
- Ask which to start with, or suggest the biggest cluster.

## 2. For each flag (one at a time, ~3–5 minutes each)

1. **Show the case** as a short card: who asked (role, store type), the question and context, what the coach answered and which items it used (with contributors), and what the asker said was not right. Set `status: in_review`.
2. **Ask the GM first, before giving your diagnosis:** "How would you answer this? What would you look at first?" Their answer, not yours, is the knowledge. Probe like gm-talk: why → what makes this case different → what would change your mind. One question at a time.
3. **Diagnose together** and record `cause`:

| Cause | Meaning | Fix |
|---|---|---|
| `no_knowledge` | No approved item covers this | Capture a new pattern / reasoning example now |
| `wrong_item_chosen` | Right knowledge exists, coach picked the wrong one | Improve titles, tags (in every language the team uses), scope; add `see_also` links |
| `missing_boundary` | The item applies in general but not here | Add the condition to Boundaries / Decision rule of the item; add a `refines` item if large |
| `outdated` | The brand or market changed | Update or retire the item; new review date |
| `explained_badly` | Content right, answer unclear | Improve the item's wording or example |
| `asker_was_right` | The asker's approach is better | Capture it as new knowledge with the asker as contributor (if they agreed to credit) |
| `coach_was_right` | The answer fits; the asker's situation does not change it | Add the reason to "Why" so the next answer explains itself better |

4. **Fix the knowledge with the GM** (show changes in plain words, GM confirms):
   - Edit or create items per `knowledge-card-format.md`; patterns per `decision-logic-capture.md`. When the GM thought it through, also write a **reasoning example** (T-item) in their words.
   - Add links: new or changed items get `derived_from: <feedback id>` in `links` (and in `sources`), plus `refines` / `see_also` / `conflicts_with` as fits.
   - Items the GM confirms → `approved`; unsure → `draft`.
5. **Close the flag**: fill `## GM retro` with the GM's answer and reasoning (5–10 lines, their words), set `cause`, `resolved_by`, `resolution_items`, `status: closed`. Closed flags are exported as regression tests: the coach must answer this question the GM's way from now on.
6. **Reply to the asker**: draft a short message in the asker's language the GM can send (chat or the ops app): what the GM would do in their situation and why, and thanks. If their flag created new knowledge and they agreed to credit, say their name now appears on it.

## 3. After the retro

- Run `kb_tool.py validate .`, `index .`, `skillmap .`.
- Quick check: for 1–2 closed flags, call the `brand-gm-coach` agent with the original question and context only. If it still answers the old way, refine the items' titles/tags/boundaries and try once more; tell the GM the result.
- Summary (5 lines): flags closed, causes, items changed/created, sub-skills affected, flags still open. If several flags were `no_knowledge` in one sub-skill, suggest a gm-talk conversation on it.

Suggest a retro weekly when there are open flags (15 minutes).
