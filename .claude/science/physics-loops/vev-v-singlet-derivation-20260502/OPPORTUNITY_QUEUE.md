# OPPORTUNITY QUEUE — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02
**Refresh policy:** rebuild after each block closure, after each no-go,
or before any global-stop decision.

## Active queue

| Rank | Slug | Route | Block | Retained-positive probability | Imports | Branch independence | Notes |
|---|---|---|---|---|---|---|---|
| 1 | H2 reformulation: f_vac V-singlet derivation of (7/8)^(1/4) | H2-A | block 01 | HIGH | retires B1, B2, B3 (introduces C1) | independent of cluster obstruction | primary target; 3-4 cycles |
| 2 | H1 Route 2 cheap probe: β=6 from Cl(3) + Klein-four counting | H1-R2 | block 02 | LOW | none new | independent | half-day attempt, likely no-go |
| 3 | H1 Route 1 deep stretch: minimal-block self-consistent saddle | H1-R1 | block 03 | LOW-MED | none new | independent | famous open lattice problem; partial result acceptable |
| 4 | m_H representation-theoretic distinction (sister to H2) | H2-B | (block 01 corollary) | MEDIUM | C1 from H2-A | depends on H2-A | side benefit; record as corollary in H2 note |

## Out-of-scope (recorded for future campaigns)

| Slug | Why excluded |
|---|---|
| H1 Route 3 bootstrap closure | requires SDP infrastructure not in repo; ~6 month project; record as future-direction in HANDOFF |
| Lattice → physical matching cluster (cycles 5, 9, 11, 17 cluster) | Nature-grade target; outside H2 scope; tracked in `LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md` |
| Hierarchy baseline `M_Pl·α_LM^16` retention (B5) | separate lane; depends on plaquette/α_LM chain; out of scope for this campaign |

## Stop heuristics

- After block 01 (H2-A): if PR opens with `pass`/`passed_with_notes`, pivot to
  block 02. If demoted, refresh queue and consider whether the demotion is
  C1-cleanable or fundamental.
- After block 02 (H1-R2): expected no-go. Pivot to block 03.
- After block 03 (H1-R1): expected stretch-attempt note. Refresh queue.
- After 5 PRs in 24h or 2 PRs per cluster: stop and report.
- After ~5 substantive cycles: apply corollary-churn check before each new
  cycle. Stop if the only remaining moves are relabelings.
