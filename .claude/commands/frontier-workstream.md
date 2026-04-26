# /frontier-workstream — Long-Running Physics Workstream

Run the repo-native frontier workstream skill from:

`docs/ai_methodology/skills/frontier-workstream/SKILL.md`

## Invocation

```text
/frontier-workstream "<science goal>" [--mode plan|run|resume|status] [--runtime DURATION] [--target STATUS] [--literature] [--max-cycles N]
```

Examples:

```text
/frontier-workstream "retire the DM/leptogenesis 16v support import" --mode plan
/frontier-workstream "close the Koide Q bridge or prove the next no-go" --mode run --literature
/frontier-workstream --mode resume --workstream dm-leptogenesis-16v
```

## Required Behavior

1. Read the skill file above before acting.
2. If execution is requested and `--runtime` is absent, ask the user how long
   to run unattended before launching work.
3. Create or update a durable workstream pack under
   `.claude/science/frontier-workstreams/<slug>/`.
4. Ground in current repo authority surfaces, retained work, no-go history,
   atlas/tool surfaces, and relevant publication tables before route selection.
5. For science execution, fetch `origin`, create a clean dedicated branch from
   `origin/main`, commit coherent science artifacts there, push that branch to
   `origin`, and do not open a PR.
6. Build an assumption/import ledger before new derivation work.
7. Generate and score a route portfolio; execute only a route that can move
   claim state, retire an import, close a blocker, prove a no-go, or create a
   decisive artifact.
8. Checkpoint `STATE.yaml` and `HANDOFF.md` throughout unattended work.
9. Run `review-loop` after each major artifact unless explicitly disabled.
10. Keep science runs science-only. Record proposed repo weaving in
   `HANDOFF.md`; do not update repo-wide authority surfaces until later review
   and backpressure integration.

## Non-Negotiables

- No hidden fitted values, selectors, observations, normalizations, or
  literature imports.
- No Nature-grade or retained closure language without decisive artifact
  support and review-loop backpressure.
- Do not re-open prior no-go routes unless a new premise is named.
- Do not run low-value churn: more prose, nearby scripts, or repeated wording
  passes are not major workstream progress.
- Push only the dedicated science branch. Do not push to `main` or open a PR.
