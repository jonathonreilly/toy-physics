# Handoff — 24h axiom-first derivations campaign (Block 04 view)

**Date:** 2026-05-01

## Block-by-block status

| Block | Slug | Status | Branch | PR |
|---|---|---|---|---|
| 01 | KMS condition from RP | support, PR open | block01-kms-20260501 | #257 |
| 02 | Hawking T_H = κ/(2π) | support, PR open (stacked on #257) | block02-hawking-20260501 | #259 |
| 03 | Bekenstein bound | support, PR open (independent) | block03-bekenstein-20260501 | #261 |
| 04 | Microcausality / Lieb-Robinson | support, branch ready | block04-microcausality-20260501 | pending |
| 05 | First law of BH mechanics | queued (depends on Block 02) | — | — |
| 06 | Stefan-Boltzmann | queued (depends on Block 01) | — | — |
| 07 | Unruh temperature | queued (depends on Block 01) | — | — |
| 08 | Reeh-Schlieder | queued (independent) | — | — |
| 09 | GSL | queued (depends on Blocks 01, 02) | — | — |
| 10 | Birkhoff vacuum-spherical | queued (independent) | — | — |
| 11 | Bisognano-Wichmann | queued (independent) | — | — |
| 12 | Tomita-Takesaki | queued (independent) | — | — |

## Proposed repo weaving (Block 04)

If/when Block 04 is integrated:

- Add microcausality / Lieb-Robinson note as a corollary to the
  retained cluster-decomposition note
  (`docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`).
- Add a one-line entry to `docs/CANONICAL_HARNESS_INDEX.md` for the
  microcausality runner.
- Cross-reference as a corollary in
  `docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md` (microcausality is the
  spacetime version of the Lorentz-kernel-based locality).

## Next exact action

Open Block 04 review PR; pivot to Block 05 (first law of BH mechanics)
on a branch stacked on Block 02 (Hawking).
