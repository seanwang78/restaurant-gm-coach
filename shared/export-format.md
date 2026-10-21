# Thinking Package

`kb_tool.py export <workspace>` writes `exports/thinking-package-<date>.json`: the brand coach's approved knowledge in a form other systems (a store operations app, a coaching tool, a chat bot, alerts on POS (point of sale) data) can reuse **without losing the GM's thinking**. A list of conclusions is not enough; the package carries four layers plus tests.

| Layer | Contents | How a system uses it |
|---|---|---|
| `layer1_points` | rules, benchmarks, red lines, playbooks, glossary | quick lookups, thresholds for alerts, locked red lines |
| `layer2_structures` | decision patterns, each split into its steps: problem type, first look, diagnosis, options, what matters most, decision rule, how I handle it, check & adjust, boundaries | the agent reasons in this order, step by step, filling each step with live data |
| `layer3_examples` | reasoning examples (the GM's step-by-step thinking in their words), cases (options considered, decision, result, lesson), Shadow GM rounds (coach guess vs GM's real decision and why) | worked examples so the agent learns to think like the GM, not to repeat conclusions |
| `layer4_mind` | the GM mind profile (priorities when things conflict, risk appetite, decision style…), principles, and the link graph between items | weighing a new situation the coach never saw, in the GM's priority order |
| `tests` | exam scenarios, Shadow round IDs, and feedback regressions (flagged questions with the GM's corrected answer) | run before the agent goes live in a new system, and after every update, to prove it still thinks like the GM |

Every item keeps its ID, sub-skill, level (L1 store … L4 brand), scope, confidence, contributors (names shown to users), links, and its body split into named sections.

**Never exported:** drafts, retired items, raw conversation notes, mentoring files, personal data.

## Rules for a system that uses the package

1. Answer by walking a layer-2 pattern, not by matching a layer-1 sentence.
2. Use layer-3 examples as examples of reasoning; do not present them as rules.
3. When nothing fits, weigh with layer-4 priorities and say clearly that no approved experience covers the case; send the question back as feedback (`feedback-format.md`).
4. Show item IDs and contributor names with every answer.
5. Filter by `level` and `scope` for the asker (a crew member does not need L4 brand strategy).
6. Re-run `tests` after every new package version; do not go live below the exam release gate.
