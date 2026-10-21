# Coach Workspace Layout

Each Brand GM keeps one workspace folder for their brand's coach. Put it in a folder that is backed up and shared with the right people only (for example the brand's shared drive folder). GMs use the **Claude desktop app, Code tab, local session**: choose this folder with the project folder control before starting the session.

The setup also writes `.claude/settings.json` so the GM is not asked to approve every note Claude saves in this folder:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": ["Bash(python3:*)", "Bash(python:*)"]
  }
}
```

```
<Brand>-GM-Coach/
├── .claude/settings.json      # lets Claude save notes in this folder without asking each time
├── CLAUDE.md                  # who owns this coach, brand, language, rules (created by setup)
├── coach-profile.md           # brand facts: stores, formats, channels, partners, key numbers
├── gm-mind.md                 # how the GM thinks: priorities, beliefs, decision style (built from conversations)
├── skill-map.md               # the whole GM skill map with depth per sub-skill (rebuilt by gm-synthesise)
├── summaries/                 # one summary per domain D1–D10 (rebuilt by gm-synthesise)
├── knowledge/                 # the coach's knowledge (only approved cards are used in answers)
│   ├── patterns/              # decision patterns (most valuable)
│   ├── principles/
│   ├── reasoning/             # the GM thinking real situations through, in their own words
│   ├── rules/
│   ├── cases/
│   ├── benchmarks/
│   ├── red-lines/
│   ├── playbooks/
│   └── glossary/
├── conversations/             # notes of each conversation with the GM or a contributor
├── feedback/                  # answers that users flagged as not right (F-YYYYMMDD-nnn.md), for GM retro
├── exports/                   # thinking packages (JSON) for other systems
├── sources/                   # documents the GM drops in: SOPs, decks, P&L reviews (read-only input)
├── exam/
│   ├── scenarios/             # E-<domain>-<nnn>.md: question, context, model answer, rubric
│   ├── runs/                  # results of each exam run, by date and version
│   └── shadow/                # one file per Shadow GM round: coach prediction vs GM's real decision and why
├── mentoring/
│   └── <successor-slug>/      # profile.md, assessment.md, plan.md, sessions/, decisions/
├── releases.md                # coach versions, what changed, who contributed
└── index.md                   # generated list of cards and coverage (do not edit by hand)
```

## CLAUDE.md template (written at setup)

```markdown
# <Brand> GM Coach workspace

Owner: <GM name>, Brand GM, <Brand>
Default language: <the GM's language>; answer in the language the user writes in.
Purpose: capture the brand's operating know-how, test it, and use it to develop the next Brand GMs.

Rules for Claude in this folder:
- Use the restaurant-gm-coach skills: gm-talk (main), gm-retro (review flagged answers), gm-synthesise, gm-review, gm-coach-exam, gm-mentor, gm-flag; use the brand-gm-coach agent to answer questions.
- Keep the thinking, not only the conclusions: patterns, reasoning examples, links between items, Shadow GM corrections.
- The main work is conversation: copy how the GM thinks (decision logic, handling patterns), classify it with the skill map, and summarise it.
- Only cards with `status: approved` are used in coach answers. Drafts are shown only when the owner asks.
- Show contributor names on every tip.
- Never store personal data of staff or guests. Never copy confidential files outside this folder.
- Food-safety, legal and red-line cards are locked: never suggest breaking them.
```

## coach-profile.md template

```markdown
# <Brand> profile
- Stores: <number> in <countries>; formats: <mall, street, kiosk, delivery-only…>
- Channels: dine-in %, take-away %, delivery % (approximate)
- Brand owner / franchisor: <if licensed>
- Key numbers the GM watches weekly: <e.g. SSSG, average check, labour %, food cost %, rating>
- Peak patterns: <hours, days, holidays>
- Current priorities this year: <3 lines>
```
