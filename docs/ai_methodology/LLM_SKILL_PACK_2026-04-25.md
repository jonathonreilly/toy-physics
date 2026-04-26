# AI Physics Methodology LLM Skill Pack

**Date:** 2026-04-25
**Status:** reusable skill-pack surface for the AI-methodology lane

This is the reusable-tool artifact for the methodology lane. It is organized as
LLM skills rather than conventional CLI tooling because the synthesized method
is procedural judgment: how an agent opens a lane, pressures it, lands only the
honest subset, and synthesizes the history into a paper-ready account.

The skills are derived from:

- [`METHODOLOGY_SYNTHESIS_2026-04-25.md`](./METHODOLOGY_SYNTHESIS_2026-04-25.md)
- [`METHODOLOGY_CASE_STUDIES_2026-04-25.md`](./METHODOLOGY_CASE_STUDIES_2026-04-25.md)
- the raw workflow commands in [`raw/claude_project_commands.md`](./raw/claude_project_commands.md)

## Why Skills Instead Of CLIs

The reusable unit is not just a script. It is a disciplined agent behavior:

- inspect the repo before asserting status;
- preserve candidate work off-main;
- pair notes with runners or explicit evidence;
- force claim-strength labels to match the support surface;
- treat no-go results as useful outputs;
- route review findings through live queues and work-history archives;
- synthesize evidence without turning raw chat into authority.

That behavior is best captured as skill instructions that another LLM can load
and follow.

## Skill Inventory

| Skill | Purpose | Path |
|---|---|---|
| `ai-physics-lane-builder` | Open and develop a bounded physics lane with note/runner pairing, status labels, and landing gates. | [`skills/ai-physics-lane-builder/SKILL.md`](./skills/ai-physics-lane-builder/SKILL.md) |
| `frontier-workstream` | Plan, launch, resume, and checkpoint long-running theoretical-physics workstreams on clean remote science branches, targeting major claim-state movement rather than small iteration. | [`skills/frontier-workstream/SKILL.md`](./skills/frontier-workstream/SKILL.md) |
| `physics-claim-reviewer` | Perform adversarial review of a candidate theorem, runner, or branch and classify findings into actionable dispositions. | [`skills/physics-claim-reviewer/SKILL.md`](./skills/physics-claim-reviewer/SKILL.md) |
| `review-loop` | Run an iterative physics review loop across code/runners, claim boundaries, imported values, Nature-grade retention, and repo-governance surfaces. | [`skills/review-loop/SKILL.md`](./skills/review-loop/SKILL.md) |
| `reviewer-backpressure-integrator` | Convert review pressure into narrow honest fixes, demotions, rejections, or selective landings. | [`skills/reviewer-backpressure-integrator/SKILL.md`](./skills/reviewer-backpressure-integrator/SKILL.md) |
| `methodology-paper-synthesizer` | Turn raw prompt, repo-history, review, and landing evidence into methods-paper source material. | [`skills/methodology-paper-synthesizer/SKILL.md`](./skills/methodology-paper-synthesizer/SKILL.md) |

## Use Pattern

For a new AI-assisted theoretical-physics project:

1. use `ai-physics-lane-builder` to open a bounded lane and define what would
   count as retained, bounded, support, open, no-go, or rejected;
2. use `frontier-workstream` when the target is a major open lane or problem
   that needs durable state, assumption/import accounting, no-go memory,
   route-portfolio selection, unattended checkpoints, milestone review, and
   clean remote branch delivery before later integration;
3. use `physics-claim-reviewer` to attack the note, runner, assumptions, and
   claim boundary, including semantic bridge failures;
4. use `review-loop` when a branch needs repeated parallel pressure across
   runners, claim status, imported values, support-only demotions, and
   Nature-grade retention gates;
5. use `reviewer-backpressure-integrator` to convert findings into repo-facing
   changes without burying useful negative results;
6. use `methodology-paper-synthesizer` to preserve the process as reusable
   evidence.

These skills are intentionally repo-native and portable. A downstream user can
copy a skill folder into their LLM skill system, or simply give the `SKILL.md`
body to an agent as operating instructions. For Codex-style skill systems,
each skill folder now has a standalone `SKILL.md` plus UI metadata in
`agents/openai.yaml`. Install by copying the individual skill folder into a
skill root.

## Paper Role

The skill pack should become a boxed protocol or appendix table in the
methodology paper. It is the concrete answer to: "How can another group get the
same gains?"

The answer is not "use the same model." The answer is to enforce the same
artifact discipline:

- off-main exploration;
- executable evidence;
- adversarial review;
- status-controlled claim boundaries;
- selective landing;
- historical archiving.

## Minimum Quality Bar

A downstream skill use is successful only if it leaves behind:

- a stated lane question or review target;
- an evidence chain or explicit statement that one is missing;
- a status decision that does not outrun the evidence;
- a review/backpressure disposition;
- a next action or archive/landing decision.
