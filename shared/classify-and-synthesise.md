# Classify and Synthesise

A GM talks the way they think: one story touches P&L, people, a landlord and a guest complaint at once. The coach must sort this into a clear structure and keep summarising it, so the brand's know-how becomes a map, not a pile of notes.

## 1. Classify every learning (during and after each conversation)

For each thing learned (pattern, principle, rule, benchmark, case…):

1. **One primary sub-skill** from the skill map in `competency-framework.md` (e.g. `skill: D2.4`, `domain: D2`). Choose by the decision being made, not by the words used: "we cut delivery promotions because commission ate the margin" is D2.4 channel economics, not D5.1 campaigns.
2. **Secondary tags**: other sub-skills it touches, plus X1 / X2 / X3 when the learning is really about deciding, using data, or influencing people.
3. **Level**: the level of the decision — L1 store, L2 area, L3 brand function, L4 whole brand. Store-level tips and brand-level judgement are both valuable; label them so successors study the right level.
4. **Kind of knowledge**: is it how the GM *diagnoses*, *decides*, *executes*, or *believes*? Diagnose/decide → pattern; believe → principle; execute → playbook or rule.
5. One story often produces several learnings in different sub-skills. Split them; link them through `sources` and the case card.

## 2. Synthesise (the gm-synthesise skill; suggest after every ~5 conversations or monthly)

Write and refresh these files:

### `summaries/<domain>-<slug>.md` — one per domain D1–D10

```markdown
# D2 P&L & commercial — how <Brand> runs it
Updated <date> from <n> approved items. Contributors: <names>.

## In one paragraph
How this GM thinks about this domain, in their own logic.

## Core principles
3–6 principles, each with item IDs.

## How we handle the main situations
Per sub-skill: the main decision patterns in 2–3 lines each, with IDs.

## Key numbers
Benchmarks and thresholds, with units and IDs.

## Red lines

## Tensions & open questions
Where items conflict, depend on context, or the GM was unsure. Ask the GM in the next conversation.

## Gaps
Sub-skills with little or no knowledge; suggested questions.
```

### `skill-map.md` — the whole GM on one page

- A table of all sub-skills: items (approved / draft), patterns, principles, depth rating, last updated.
- **Depth rating** per sub-skill: ⬜ none · 🟡 tips only (rules/benchmarks, no pattern) · 🟠 at least one decision pattern · 🟢 patterns + principles + cases, tested by Shadow GM with ≥ 70% match.
- Top 5 gaps to talk about next, as natural conversation openers in the GM's language.

### Cross-domain themes in `gm-mind.md`

Look across domains for the GM's recurring logic: the same priority order, the same first question, the same way of testing an idea small before scaling. These are the deepest part of the GM's judgement. Propose them to the GM as "I notice you often… Is that right?" and add only what they confirm.

## 3. Keep the knowledge clean

During synthesis:

- **Merge duplicates**: same idea said twice → keep one item, add both conversations to `sources`, keep all contributors.
- **Generalise**: three or more rules or cases with the same logic → propose one decision pattern that explains them; keep the originals as examples.
- **Resolve conflicts**: two items that disagree → find the condition that separates them (store type, season, size of drop) and add it to Boundaries; if unclear, put it in "Tensions" and ask the GM.
- **Re-classify**: if a sub-skill collects very different things, propose a split; if a sub-skill stays empty and does not apply to this brand, mark it "not relevant to <Brand>".
- **Retire** items the GM says are out of date (`status: retired`), never delete approved history.

## 4. Use the structure in answers

The coach agent reads `skill-map.md` and the relevant domain summary first, then the detailed items. Its answer follows the GM's logic: first look → diagnosis → options → what matters most → decision → how to handle → check and adjust.
