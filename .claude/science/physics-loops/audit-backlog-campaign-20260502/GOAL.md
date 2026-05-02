# Audit-Backlog Retained Campaign — 2026-05-02

## Mandate

Run a 24-hour campaign on the audit backlog. Attempt actual derivation work on
each candidate using the full physics-loop methodology — not just LHF picking.
Every coherent science block opens a PR with honest claim-status certification:
`proposed_retained` when the seven retained-proposal certificate criteria are
met, otherwise the narrowest honest status (exact support / exact negative
boundary / no-go / demotion / named obstruction).

The campaign's aim is retained-positive movement; the output is whatever honest
claim-state movement actually happens.

## Scope

The audit ledger is the lane map. Candidates are mined from
`docs/audit/data/audit_ledger.json` and ranked by:

1. downstream transitive descendants (blast radius)
2. named-residual tractability (does the verdict name a specific repair target
   with a candidate retained chain?)
3. dependency cleanliness (fraction of deps with retained-grade
   effective status)
4. independence from already-attempted no-go routes

## Forbidden Imports

These cannot be consumed as proof inputs in any cycle:

- PDG observed values for the target lane
- Literature numerical comparators (only allowed as audit comparators with
  explicit role label)
- Fitted selectors
- Admitted unit conventions when retention claim depends on them
- Same-surface family arguments (e.g., A² conventions for CKM)

## Stop Conditions

Stop only on:

- 24h runtime exhausted
- 30 cycles exhausted
- Refreshed `OPPORTUNITY_QUEUE.md` proves every viable target globally blocked
- Worktree/lock conflict prevents safe continuation
- Core tooling for every viable route is unavailable

Do NOT stop on: retained-cert failure, dirty/missing PR, GitHub auth/network
failure, missing optional literature, human-judgment blocker on one row,
review-loop returning demote/block on the current artifact. These are
checkpoint-and-pivot events.

## PR Policy

One branch per coherent science block:
`physics-loop/<slug>-block<NN>-20260502`. Push to `origin`. Open one PR per
block with title prefix `[physics-loop][science]` and a status label in the
title (one of: `proposed_retained`, `exact-support`, `exact-negative-boundary`,
`named-obstruction`, `no-go`, `demotion`, `support-firewall`). Never merge.
Never push to main.

## Recent Landed Output (do not duplicate)

- PR #246, #247: audit-hygiene runner stale-path cleanups
- PR #248: LHF leverage map synthesis
- PR #249 (MERGED): Fierz-channel exact group-theory derivation of (N_c²-1)/N_c²
- PR #250: cycle-cleanup integration into yt_ew + RCONN + OZI
- PR #253: SU(2)²×U(1)_Y anomaly cancellation for LH doublets
