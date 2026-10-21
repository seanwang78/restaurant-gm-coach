# Capturing How a GM Thinks

The goal is not a list of tips. The goal is to copy the GM's **judgement**: how they notice a problem, how they diagnose it, which options they consider, what they weigh most, how they decide, how they handle it, and how they check it worked. Tips are a by-product.

Three kinds of knowledge come out of conversations:

| What | File | Example |
|---|---|---|
| `knowledge/patterns/M-<domain>-<nnn>-<slug>.md` | "A store's profit drops: how I diagnose and decide" |
| `knowledge/principles/V-<domain>-<nnn>-<slug>.md` | "Guest trust before this month's margin" |
| `gm-mind.md` (one per GM) | priorities order, risk appetite, how they read numbers, how they judge people |

| `knowledge/reasoning/T-<domain>-<nnn>-<slug>.md` | "Mall store evening drop: how I thought it through, step by step" |

Rules, benchmarks, red lines, playbooks and cases (see `knowledge-card-format.md`) are still written when a conversation produces them.

**Keep the thinking, not only the conclusion.** A conclusion ("don't cut staff") without the reasoning is a tip; other systems and successors cannot adapt it. Every conclusion should be reachable from a pattern (the structure), a reasoning example (the GM thinking in their own words), and the principles it rests on (links).

## Decision pattern structure

Write a pattern with these sections (body in the GM's language; optionally a 1–2 line summary in a second team language at the end):

```markdown
## Problem type
What kind of situation this is, and how the GM recognises it ("I know it's this when…").

## First look
Signals and numbers the GM checks, in order, and where they look (report, store visit, staff, guests).

## Diagnosis
Possible causes and how the GM tells them apart. Write as a small tree:
- If <signal A> → most likely <cause 1> → check <X>
- If <signal B> but not <C> → <cause 2>

## Options
The options the GM normally considers, including "do nothing / wait".

## What matters most
The criteria and their order when they conflict (e.g. safety > guest trust > team > profit this month).

## Decision rule
"If … and …, I do A. If …, I do B. Unless …"

## How I handle it
Steps, who to involve, what to say to whom, timing.

## Check & adjust
How the GM knows it worked, after how long, and when they change course.

## Boundaries
When this pattern does NOT apply. Variations found with what-if questions.

## Stories behind it
Links to case cards or conversation notes (roles, not staff names).
```

A pattern is good when a capable successor, reading only this, would make the same decision as the GM in most variations of the situation.

## Reasoning example structure

Write one when the GM thinks a real situation through out loud. Keep the GM's own words (short quotes) — that is the point.

```markdown
## Situation
What the GM faced, with numbers. Roles, no staff names.

## Thinking step by step
1. Noticed: "…" (quote) → meaning: …
2. Checked: … because "…"
3. Ruled out: … because "…"
4. Weighed: … vs … → chose … because "…"
5. Would change my mind if: …

## Decision

## What a less experienced manager would do
And why it would go wrong.

## Result (if known)
```

Link it: `example_of` the pattern it illustrates, `based_on` the principles it uses.

## Shadow GM round record

One file per round: `exam/shadow/S-<nnn>-<slug>.md`. The full record matters more than the score: where the coach guessed wrong is where the GM's judgement differs from an ordinary manager's.

```markdown
---
id: S-007
skill: D2.1
result: partial            # full | partial | miss
date: 2026-10-21
items_used: [M-D2-001, V-D2-001]     # what the coach based its guess on
learned_items: [M-D2-001, T-D2-003]  # items created or changed because of this round
---
## Situation
## Coach prediction
The decision and the reasoning, step by step.
## GM's real decision
## Why
The GM's explanation, in their words.
## Gap
What the coach missed: a signal, a boundary, a priority, a principle.
```

## Probing techniques

Use these naturally inside the conversation, one question at a time:

1. **Laddering why** — "Why that?" → "And why does that matter?" (2–3 levels) until you reach a principle.
2. **What-if variation** — change ONE thing: "Same situation, but it's a street store / it's December / the manager is new / the drop is 5% not 15%. Same decision?" This finds the boundaries of the rule.
3. **Contrast** — "You closed store A but kept store B with similar numbers. What was different?"
4. **First signal** — "What did you notice first, before the report showed it?"
5. **Threshold** — "At what number do you start to worry? At what number do you act?"
6. **Trade-off** — "If you can only protect one: guest rating or labour cost this month, which one and why?"
7. **Change my mind** — "What would make you decide the opposite?"
8. **Who disagrees** — "Who in the company would do it differently? Who is right in which situation?"
9. **Novice mistake** — "What would a new GM do here that you would not?"
10. **Teach-back** — summarise the logic in 3–5 lines and ask the GM to correct it. Their corrections are the most valuable part.
11. **Predict and correct** (Shadow GM) — give a situation, state what you think the GM would decide and why, using only what you have learned; ask them to correct you. The gap is new knowledge.

## The GM mind profile (`gm-mind.md`)

One file per GM, built slowly across many conversations. Sections:

```markdown
# How <GM name> thinks
## Priorities when things conflict
## What I look at every week
## How I read a P&L / a store / a report
## How I judge people
## Risk appetite
## How I decide)
## Questions I always ask my managers
## Things I never do
## What I believe about our guests and our brand
## How my thinking changed over the years
```

Each line ends with where it came from, e.g. `(conversation 2026-10-21)`. Propose updates to the GM; never add a belief they did not say or confirm.

## Saving without slowing the conversation

- Keep the conversation flowing. Do not show YAML or files during the talk.
- Take notes silently into `conversations/<YYYY-MM-DD>-<topic-slug>.md` (questions, the GM's words, your reflections).
- At natural pauses and at the end, show **"What I learned"**: each pattern / principle / tip in 2–4 plain lines. The GM confirms, corrects or drops each one.
- When the **owner GM** confirms in the conversation, save it as `status: approved`, `approved_by: <GM>`. When another contributor confirms, save as `draft` for the GM to approve later.
