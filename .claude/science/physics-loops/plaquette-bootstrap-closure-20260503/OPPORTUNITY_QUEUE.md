# OPPORTUNITY QUEUE — Plaquette Bootstrap Closure

**Date:** 2026-05-03

## Active queue

| Rank | Slug | Route | Block | Retained-positive probability | Cluster | Notes |
|---|---|---|---|---|---|---|
| 1 | RP-based 2x2 Gram + Migdal-Makeenko analytical bound on ⟨P⟩(β=6) | BB-1 | block 01 | MEDIUM | gauge_vacuum_plaquette_* | smallest non-trivial bootstrap on framework surface |
| 2 | 3x3 Gram extension + framework-specific positivity refinement | BB-2 + BB-3 | block 02 | LOW-MED | gauge_vacuum_plaquette_* | tighter bound; cluster-cap limit at 2 PRs/family |
| 3 | Numerical verification via scipy small-matrix PSD check | BB-4 | (no PR) | LOW (verification only) | — | record in HANDOFF, no science branch |

## Out-of-scope (recorded for future campaigns)

| Slug | Why excluded |
|---|---|
| Full numerical SDP via CVXPY/Mosek | CVXPY install blocked by PEP 668; needs separate environment-setup work |
| L_max = 6+ truncation | requires industrial SDP solver |
| Lattice → physical matching cluster (cycles 5, 9, 11, 17) | Nature-grade target; not bootstrap-related |

## Stop heuristics

- After block 01: if PR opens with PASS, pivot to block 02. If demoted,
  refresh queue.
- After block 02: cluster cap reached for `gauge_vacuum_plaquette_*`.
  Stop or pivot to a different cluster (no orthogonal bootstrap targets
  remain in this campaign's scope).
- Maximum 5 PRs/24h volume cap; well below this expected.
