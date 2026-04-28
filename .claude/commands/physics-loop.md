# /physics-loop — Long-Running Physics Loop

Run the repo-native physics loop skill from:

`docs/ai_methodology/skills/physics-loop/SKILL.md`

## Invocation

```text
/physics-loop "<science goal>" [--mode plan|run|resume|status] [--runtime DURATION] [--target STATUS] [--literature] [--max-cycles N] [--deep-block DURATION] [--no-pr]
```

Examples:

```text
/physics-loop "retire the DM/leptogenesis 16v support import" --mode plan
/physics-loop "close the Koide Q bridge or prove the next no-go" --mode run --literature --runtime 12h
/physics-loop --mode resume --loop dm-leptogenesis-16v
```

## Required Behavior

1. Read the skill file above before acting.
2. If execution is requested and `--runtime` is absent, ask the user how long
   to run unattended before launching work.
3. Create or update a durable loop pack under
   `.claude/science/physics-loops/<slug>/`. Existing
   `.claude/science/frontier-workstreams/<slug>/` packs may be read as legacy
   resume surfaces.
4. Ground in current repo authority surfaces, retained work, no-go history,
   atlas/tool surfaces, and relevant publication tables before route selection.
5. For science execution, fetch `origin`, create clean dedicated science block
   branches from `origin/main`, commit coherent science artifacts there, and
   push those branches to `origin`.
6. Build an assumption/import ledger before new derivation work.
7. Generate and score a route portfolio; execute only a route that can move
   claim state, retire an import, close a blocker, prove a no-go, create a
   decisive artifact, or make a recorded first-principles stretch attempt on a
   named hard residual.
8. Checkpoint `STATE.yaml` and `HANDOFF.md` throughout unattended work.
9. After two audit/no-go/blocker cycles in a row, run a stretch attempt before
   declaring stop. If stuck, fan out 3-5 orthogonal premises before stopping.
10. Run `review-loop` after each major artifact unless explicitly disabled.
11. At loop end, open or prepare one review PR per coherent science block
    unless `--no-pr` was supplied.
12. Keep science runs science-only. Record proposed repo weaving in
   `HANDOFF.md`; do not update repo-wide authority surfaces until later review
   and backpressure integration.

## Non-Negotiables

- No hidden fitted values, selectors, observations, normalizations, or
  literature imports.
- No Nature-grade or retained closure language without decisive artifact
  support and review-loop backpressure.
- Do not re-open prior no-go routes unless a new premise is named.
- Do not run low-value churn: more prose, nearby scripts, or repeated wording
  passes are not major loop progress.
- Push only dedicated science block branches. Do not push science work to
  `main`, merge PRs, or open PRs without enough review surface for
  `review-loop`.
