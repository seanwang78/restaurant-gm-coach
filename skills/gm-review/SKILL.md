---
name: gm-review
description: Lets the Brand GM review, approve, edit, merge or retire the coach's knowledge items, especially drafts from other contributors (area managers, store managers) and patterns Claude proposed during synthesis. Use when the user says "review drafts", "approve", "what is waiting for me", "edit this card", "this is out of date".
---

# GM Review — keep the coach's knowledge right

Shared references in `../../shared/` relative to this skill's base directory (`${CLAUDE_PLUGIN_ROOT}/shared/`): `knowledge-card-format.md`, `decision-logic-capture.md`, `privacy-and-safety.md`, `language-and-glossary.md`.

Most items written with the owner GM are approved inside gm-talk. This skill handles the rest. Only the owner GM, or a delegate named in `CLAUDE.md`, approves.

## Steps

1. List what is waiting, grouped by domain and sub-skill: drafts (with contributor and date), items tagged `needs-gm-review`, items past `review_by`, patterns proposed by synthesis. Show the count first: "12 waiting: 7 from Somporn R., 3 proposed patterns, 2 past review date."
2. Show each item as a short readable card in the GM's language (not YAML): for a pattern, the logic order (first look → diagnosis → options → what matters most → decision → handling → check); for others, When / Do / Why / Numbers.
3. Offer: ✅ approve · ✏️ edit (the GM says what to change) · 🔀 merge with similar item · ✂️ split · ⏸ later · 🗑 reject · 📦 retire (out of date).
4. If the GM edits, ask one follow-up "why?" — the reason behind a correction is often a new principle; offer to add it.
5. Apply: approve → `status: approved`, `approved_by: <GM>`; retire → `status: retired` (never delete approved history); reject drafts → delete the file and note it in the conversation log.
6. The GM can say "approve all from <name>" after seeing the list; still show any item tagged `needs-gm-review` individually.
7. After the batch, run `kb_tool.py validate .`, `kb_tool.py index .` and `kb_tool.py skillmap .` (or check by hand). Report: approved N, edited N, sub-skills that moved up in depth, contributors credited.
