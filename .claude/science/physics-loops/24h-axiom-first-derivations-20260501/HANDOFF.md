# Handoff — 24h axiom-first derivations campaign (Block 09 view)

**Date:** 2026-05-01

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
| 08 | Unruh temperature | support, PR open (stacked on #257) | block08-unruh | #272 |
| 09 | Birkhoff theorem | support, branch ready (independent) | block09-birkhoff | pending |
| 10 | GSL | queued (depends on Blocks 01, 02, 05) | — | — |
| 11 | Bisognano-Wichmann | mostly subsumed by Block 08 (U4) | — | — |
| 12 | Tomita-Takesaki | queued (uses Block 07 cyclic-and-separating) | — | — |

## Proposed repo weaving (Block 09)

- Add Birkhoff theorem note as the framework's uniqueness theorem
  for static spherically-symmetric vacuum.
- Cross-reference in Block 02 (Hawking) since Schwarzschild is the
  canonical solution used there.

## Next exact action

Open Block 09 PR; consider Block 10 (GSL) stacked on Block 05 if
context budget permits.
