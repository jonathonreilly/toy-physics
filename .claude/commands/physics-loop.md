# /physics-loop — Long-Running Physics Loop

Run the repo-native physics loop skill from:

`docs/ai_methodology/skills/physics-loop/SKILL.md`

## Invocation

```text
/physics-loop "<science goal>" [--mode plan|run|resume|status|campaign] [--runtime DURATION] [--target STATUS] [--literature] [--max-cycles N] [--deep-block DURATION] [--no-pr]
```

Examples:

```text
/physics-loop "retire the DM/leptogenesis 16v support import" --mode plan
/physics-loop "close the Koide Q bridge or prove the next no-go" --mode run --literature --runtime 12h
/physics-loop "work the best open science opportunities" --mode campaign --runtime 12h --target best-honest-status
/physics-loop --mode resume --loop dm-leptogenesis-16v
```

Infer `--mode campaign` for overnight, unattended, long-running, or 12-hour
execution requests even when the user says only `run`.

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
8. For unattended runs longer than one major cycle, build
   `OPPORTUNITY_QUEUE.md` and keep selecting the next ranked retained-positive
   opportunity until runtime/max cycles expires or the refreshed queue is
   globally exhausted.
9. Write `CLAIM_STATUS_CERTIFICATE.md` for each science block. Do not use bare
   `retained` / `promoted` status language in branch-local source notes. Use
   `proposed_retained` / `proposed_promoted` only when the certificate supports
   a theorem-grade proposal and marks the later independent audit requirement;
   otherwise demote branch-local, conditional, same-surface,
   admitted-observation, or Axiom* consequences to the narrowest honest status.
10. Checkpoint `STATE.yaml` and `HANDOFF.md` throughout unattended work.
11. After two audit/no-go/blocker cycles in a row, run a stretch attempt before
   declaring a route blocked. If stuck, fan out 3-5 orthogonal premises before
   declaring global queue exhaustion.
12. Run `review-loop` after each major artifact unless explicitly disabled.
   Treat review demotions/blockers as block-level demotion/pivot events, not
   campaign stops.
13. At each coherent science-block closure, open or prepare one review PR
    unless `--no-pr` was supplied; do not wait until the 12-hour campaign ends
    if the block is already coherent.
14. Keep science runs science-only. Record proposed repo weaving in
   `HANDOFF.md`; do not update repo-wide authority surfaces until later review
   and backpressure integration.

## Campaign Rule

If the user asks for a 12-hour unattended run, do not exit early just because a
lane hits a no-go, support-only boundary, human-judgment blocker, failed
retained-proposal certificate, dirty PR, or missing GitHub auth. Checkpoint/demote or
backlog the current block, refresh the opportunity queue, and continue on the
next science target. Stop early only for runtime/max-cycle exhaustion, unsafe
worktree/lock conflict, or documented global queue exhaustion.

## Non-Negotiables

- No hidden fitted values, selectors, observations, normalizations, or
  literature imports.
- No Nature-grade or retained-grade proposal language without decisive artifact
  support, a passing retained-proposal certificate, review-loop backpressure,
  and explicit independent-audit handoff.
- Do not re-open prior no-go routes unless a new premise is named.
- Do not run low-value churn: more prose, nearby scripts, or repeated wording
  passes are not major loop progress.
- Do not write bare `retained` / `promoted`, `retained branch-local`, or
  hypothetical/Axiom* consequences as retained on the actual current surface.
  `proposed_retained` / `proposed_promoted` are allowed only as audit-ready
  author proposals, never as audit-ratified retained status.
- Push only dedicated science block branches. Do not push science work to
  `main`, merge PRs, or open PRs without enough review surface for
  `review-loop`.
