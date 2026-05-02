# OPPORTUNITY QUEUE — 24h axiom-first derivations campaign

**Date:** 2026-05-01
**Refresh policy:** after each block close (commit + PR + review).

## Ranked queue

Score = (retained-positive probability) × (impact) / (dependency depth).
"Indep" indicates whether the block is independent of prior block output.

| Rank | Slug | Target | Dependencies (retained/admitted) | Impact | Indep? | Status |
|---|---|---|---|---|---|---|
| 1 | `kms-from-rp` | KMS condition for transfer-matrix Gibbs state | RP, SC1-SC4, Wick rotation | foundational thermal QFT | yes | queued |
| 2 | `hawking-temperature` | T_H = κ/(2π) for framework Killing horizon | KMS (block 1) + framework GR action + Killing horizon definition | Nobel-tier | depends on 1 | queued |
| 3 | `bekenstein-bound` | S ≤ 2π R E / ℏc | spectrum cond + framework area law (BH 1/4) | foundational holographic | yes | queued |
| 4 | `microcausality` | [O(x), O(y)] = 0 spacelike | lattice locality (A2/A3) + cluster decomp + spectrum cond + Lorentz kernel | foundational locality | yes | queued |
| 5 | `first-law-bh-mechanics` | dM = (T_H / 8π G) dA + ΩdJ + ΦdQ | BH 1/4 (Wald-Noether) + Hawking T_H (block 2) + framework GR | foundational gravity thermodynamics | depends on 2 | queued |
| 6 | `unruh-temperature` | T_Unruh = a/(2π) for uniformly accelerated observer | KMS (block 1) + framework Lorentz kernel + Bisognano-Wichmann sketch | foundational QFT | depends on 1 | queued |
| 7 | `stefan-boltzmann` | u(T) = (π²/15)(k_B T)⁴ / (ℏc)³ photon energy density | KMS (block 1) + photon spectrum from gauge structure | foundational thermodynamics | depends on 1 | queued |
| 8 | `reeh-schlieder` | local algebra cyclicity | spectrum cond + cluster decomp | foundational AQFT | yes | queued |
| 9 | `gsl-monotonicity` | δ(S_BH + S_matter) ≥ 0 | BH 1/4 + KMS + second-law of thermodynamics | foundational gravity-entropy | depends on 1, 2 | queued |
| 10 | `birkhoff-vacuum-spherical` | spherically-symmetric vacuum sol → static | framework GR action + spherical-symmetry reduction | foundational GR | yes | queued |
| 11 | `bisognano-wichmann` | wedge boost ↔ thermal Rindler state | RP + Lorentz kernel + framework GR | foundational AQFT | yes | queued |
| 12 | `tomita-takesaki` | local-algebra modular flow | RP + spectrum cond + cyclic vector | foundational AQFT | yes | queued |

## Independence scoring rationale

Blocks 1 (KMS), 3 (Bekenstein), 4 (microcausality), 8 (Reeh-Schlieder),
10 (Birkhoff), 11 (Bisognano-Wichmann), 12 (Tomita-Takesaki) are
independent of one another — they can run in any order from retained deps.

Blocks 2 (Hawking), 6 (Unruh), 7 (Stefan-Boltzmann), 9 (GSL) require
block 1 (KMS) closed first.

Block 5 (first-law-of-BH-mechanics) requires block 2 (Hawking) closed
first.

## Execution order

Run 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 by default.
Pivot to next-independent if a block hits a no-go that blocks its
dependents.

## Last refresh

2026-05-01 (initial build)
