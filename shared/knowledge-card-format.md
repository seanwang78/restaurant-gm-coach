# Knowledge Card Format

A knowledge card is one small, reusable piece of the GM's know-how. The most valuable cards are **decision patterns** and **principles** (how the GM thinks); see `decision-logic-capture.md` for their structure. The coach answers only from cards, so card quality is coach quality. One idea per card. A card a store manager can read in under one minute.

## File name and location

`knowledge/<type>/<ID>-<short-slug>.md`, for example `knowledge/rules/R-D3-014-peak-staffing-weekend-brunch.md`.

- `<type>` folder: `patterns`, `principles`, `reasoning`, `rules`, `cases`, `benchmarks`, `red-lines`, `playbooks`, `glossary`
- `<ID>`: type letter + domain + 3-digit number: M (decision pattern), V (principle), T (reasoning example), R (rule), C (case), B (benchmark), X (red line), P (playbook), G (glossary). Example: `M-D2-003`, `C-D2-007`.
- Slug: lowercase English words joined by hyphens, even when the card is in another language (file names stay ASCII).

## Card types

| Type | Use it for | Example |
|---|---|---|
| pattern | How the GM diagnoses and decides a type of problem (structure in `decision-logic-capture.md`) | "A store's profit drops: what I check first, how I tell causes apart, how I decide" |
| principle | A belief or priority that guides many decisions | "Guest trust before this month's margin: never cut portion size to hit food cost" |
| reasoning | A real situation the GM thought through step by step, in their own words: what they noticed, each "because… so…", what they ruled out and why (structure in `decision-logic-capture.md`) | "Mall store evening drop: how I thought it through, step by step" |
| rule | A heuristic or "how we do it" with a reason | "When it rains after 15:00, add one person on the pass; delivery jumps 15–20%." |
| case | A real situation, what was done, the result | "Mall closed early for a protest; how we moved sales to delivery in one hour." |
| benchmark | A number or normal range the GM uses to judge | "Healthy labour % for a mall store: 14–17% of sales." |
| red-line | Something never to do, or a locked standard | "Never skip temperature checks on chilled deliveries." |
| playbook | A short ordered procedure for a recurring event | "Long weekend: 10 steps from 14 days before to the day after." |
| glossary | A brand or company term people must understand |

## Front matter (YAML)

```yaml
---
id: R-D3-014
type: rule                      # pattern | principle | reasoning | rule | case | benchmark | red-line | playbook | glossary
domain: D3                      # D1–D10, see competency-framework.md
skill: D3.2                     # primary sub-skill from the skill map
level: L2                       # level of the decision: L1 store … L4 whole brand
tags: [X1, peak, weekend]       # optional, free words allowed
title: Staff the weekend brunch peak from 10:00
title_alt: Weekend brunch peak — staff up from 10:00   # optional: same title in a second team language
language: th                    # language of the body: th | en
brand: Example Coffee          # or "All brands"
scope: Mall stores    # where it applies; say "All stores" if general
contributors:                   # who taught it; names are shown to users
  - name: Somporn R.
    role: Area Manager, city malls
    years: 14
approved_by: Wanida P.          # Brand GM or delegate; empty while draft
status: draft                   # draft | approved | retired
confidence: high                # high | medium | low (how sure the contributor is)
evidence: "Seen across 214 long-weekend days, 2019–2025"   # data, cases, or "experience"
created: 2026-10-21
review_by: 2027-10-21           # when to re-check; default 12 months
sources: [conversations/2026-10-21-ops-peaks.md]
links:                          # how this item connects to others (keeps the thinking connected)
  - rel: derived_from           # derived_from | based_on | example_of | refines | conflicts_with | see_also
    id: C-D3-002
    note: "learned from the 2025 holiday-weekend case"
  - rel: based_on
    id: V-D2-001
---
```

### Links

Links keep the reasoning connected when knowledge is exported to other systems. Add them whenever you know them:

| rel | Meaning | Example |
|---|---|---|
| `derived_from` | This item was learned from that case, reasoning example, Shadow round or feedback | pattern ← case |
| `based_on` | This item applies that principle | pattern → principle |
| `example_of` | This case or reasoning example illustrates that pattern | reasoning → pattern |
| `refines` | This item adds a boundary or exception to that one | rule → pattern |
| `conflicts_with` | These two disagree; `note` says the condition that separates them | rule ↔ rule |
| `see_also` | Related, useful to read together | |

## Body sections

Write in the contributor's language. Add a 1–2 line summary in the other language at the end when the team works in two languages (optional).

```markdown
## When
The situation that triggers this card. Be concrete: store type, time, signal.

## Do
The action in numbered steps or one clear sentence.

## Why
The reason, so a successor can adapt it when the situation is different.

## Watch out
Common mistakes, exceptions, when NOT to apply it.

## Numbers
Thresholds, ranges, targets (optional; mark "approximate" if from memory).

## Example
One short real example (optional for rules, required for cases).

## Summary
One or two lines (optionally in a second team language).
```

Case cards replace Do/Why with: `## Situation`, `## Options considered`, `## Decision`, `## Result`, `## Lesson`.

## Quality bar (check before saving)

1. One idea only. Split if the card has two "Do" actions for different situations.
2. Concrete trigger. "When sales drop" is too vague; "When a mall store's weekday lunch bills fall 10% for 3 weeks" is good.
3. A reason is given. Without "why", the successor cannot adapt it.
4. Numbers have units and a range or "approximate".
5. No personal data about staff or guests (names of employees, phone numbers, ID numbers, health details). Contributor names are fine.
6. No confidential deal terms unless the workspace is marked internal-only (see `privacy-and-safety.md`).
7. Red lines and food-safety items are written as locked: the coach must never advise breaking them.

## Coverage targets (for a first useful coach)

| Domain | Minimum approved cards | Of which cases | Exam scenarios |
|---|---|---|---|
| Each of D1–D10 | 8 (incl. 2 patterns) | 2 | 4 |
| Total first release | 80+ | 20+ | 40+ |

A coach with fewer cards can still be used, but tell users which domains are thin.

Examples of finished cards are in `examples/` (format only; their content is illustrative).
