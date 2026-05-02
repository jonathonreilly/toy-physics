# Handoff — 24h axiom-first derivations campaign

**Date:** 2026-05-01

## Summary

Active campaign producing NEW first-principles derivations on `A_min` plus
the retained Apr 29 axiom-first foundations (RP, spectrum cond, CPT,
spin-statistics, cluster decomp, lattice Noether, Coleman-Mermin-Wagner,
BH 1/4 carrier).

## Block-by-block status

| Block | Slug | Status | Branch | PR |
|---|---|---|---|---|
| 01 | KMS | support, PR open | block01-kms | #257 |
| 02 | Hawking T_H | support, PR open (stacked on #257) | block02-hawking | #259 |
| 03 | Bekenstein bound | support, PR open | block03-bekenstein | #261 |
| 04 | Microcausality | support, PR open | block04-microcausality | #263 |
| 05 | First law of BH mechanics | support, PR open (stacked on #259) | block05-firstlaw | #265 |
| 06 | Stefan-Boltzmann | support, PR open (stacked on #257) | block06-stefanboltzmann | #266 |
| 07 | Reeh-Schlieder cyclicity | support, PR open | block07-reehschlieder | #269 |
| 08 | Unruh temperature | support, branch ready (stacked on #257) | block08-unruh | pending |
| 09 | GSL | queued (depends on Blocks 01, 02, 05) | — | — |
| 10 | Birkhoff vacuum-spherical | queued (independent) | — | — |
| 11 | Bisognano-Wichmann | mostly subsumed by Block 08 (U4) | — | — |
| 12 | Tomita-Takesaki | queued (uses Block 07 cyclic-and-separating) | — | — |

## Proposed repo weaving (deferred to integration)

This is recorded here per physics-loop SKILL §14 for later integration.
Do NOT update repo-wide authority surfaces during the science run.

If/when Block 01 is integrated:

- Add KMS support note to the axiom-first foundations row in
  `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md` (if a new
  `axiom-first-foundations` row is created).
- Add a one-line entry to `docs/CANONICAL_HARNESS_INDEX.md` for the new
  runner.
- Add to `docs/work_history/repo/LANE_STATUS_BOARD.md` under a new
  `axiom-first-foundations` lane (or extend the existing one).
- Cross-reference KMS as a corollary in
  `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`'s
  Corollaries section (C5: KMS condition holds for the Gibbs state on
  the periodic-time block).

If/when Block 08 is integrated:

- Add Unruh note as a corollary of Block 01 KMS + retained Lorentz
  kernel.
- Cross-reference in Block 02 (Hawking) as the parallel-structure
  derivation.

## Next exact action

Open Block 08 stacked PR (base = Block 01 KMS); pivot to Block 09
(GSL) stacked on Block 05.
