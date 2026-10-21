# Feedback on Coach Answers

When a store manager, area manager, successor or crew member gets a coach answer that does not fit what they face, they flag it. Each flag becomes one file in `feedback/`. The Brand GM reviews flags in a **retro** (gm-retro): the GM decides what the right thinking is, the coach's knowledge is fixed, and the case becomes a test so the same mistake does not come back.

Flags are among the most valuable inputs the coach gets: they come from real situations the GM did not think to mention.

## File: `feedback/F-<YYYYMMDD>-<nnn>.md`

```markdown
---
id: F-20261021-001
status: open               # open | in_review | closed
created: 2026-10-21
source: claude-code        # claude-code | ops-app | chat | import
asker_role: "Store manager"            # role, not a name
store: "Mall store, city centre"           # type and area; a store code is fine
reason: not_applicable     # wrong | not_applicable | missing | unclear | outdated | other
skill: D2.3                # sub-skill of the question (classify if the asker did not)
items_used: [M-D2-001, V-D2-001]       # items the coach cited in its answer
question: "Morning bills down 5 weeks. Should I cut the morning shift?"
cause:                     # filled in the retro: no_knowledge | wrong_item_chosen | missing_boundary | outdated | explained_badly | asker_was_right | coach_was_right | other
resolved_by:               # GM name
resolution_items: []       # items created or changed in the retro
---
## Question
## Context
What the asker told the coach (numbers, store type, time).
## Coach answer
The answer as given (or a faithful summary), with item IDs.
## What was not right
In the asker's words.
## What I actually did
Optional.
## Result
Optional; can be added later.
## GM retro
Filled by gm-retro: the GM's answer and reasoning, the cause, what changed.
```

## Rules

- No personal data: use roles, not names of staff or guests. The asker's own name may be kept only if they agree to be credited (`asker_credit: <name>`) when their flag leads to new knowledge.
- Never edit approved knowledge directly from a flag. Flags go to the GM; the GM decides.
- A flag is not a vote. One flag from a real situation can be enough to add a boundary; ten flags can still be "the coach was right, explain it better".

## JSON for other systems (store ops apps, coaching tools, chat bots)

Systems that host the coach send flags in this shape; `kb_tool.py import-feedback <workspace> <file.json>` turns them into feedback files (a list or a single object):

```json
{
  "source": "ops-app",
  "created": "2026-10-21",
  "asker_role": "Store manager",
  "store": "Mall store, city centre",
  "reason": "not_applicable",
  "skill": "D2.3",
  "question": "Morning bills down 5 weeks. Should I cut the morning shift?",
  "context": "Office building next door closed in September.",
  "coach_answer": "…",
  "items_used": ["M-D2-001", "V-D2-001"],
  "comment": "The cause is permanent, the coach still said don't cut.",
  "what_i_did": "",
  "result": ""
}
```
