# LITERATURE BRIDGES — Plaquette Bootstrap Closure

**Date:** 2026-05-03
**Literature flag:** allowed (`--literature` passed by user)

## Primary literature comparators

| Reference | Role | Key result |
|---|---|---|
| Anderson & Kruczenski 2017 (arXiv:1612.08140) | foundational lattice bootstrap reference | original lattice bootstrap method |
| **Kazakov & Zheng 2022** [arXiv:2203.11360](https://arxiv.org/abs/2203.11360), [Phys. Rev. D 107.L051501](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.107.L051501) | SU(∞) lattice YM bootstrap | At L_max=16, ~100k loop equations, 6505×6505 matrices reduced to 15×78 blocks via 20 irreps. Bracket ⟨P⟩ ≈ 0.59-0.61 near λ≈1.35 in 4D. ~20 CPU h per data point. |
| **Kazakov & Zheng 2024** [arXiv:2404.16925](https://arxiv.org/abs/2404.16925), [JHEP 03(2025) 099](https://link.springer.com/article/10.1007/JHEP03(2025)099) | Finite N (SU(2), SU(3)) lattice YM bootstrap | SU(2) precision 0.1% in physical range D=3,4 |
| **JHEP 12(2025) 033** [link](https://link.springer.com/article/10.1007/JHEP12(2025)033) | SU(3) lattice YM bootstrap (most directly relevant) | extends finite N bootstrap to SU(3) with multi-trace Wilson loops |
| Li & Zhou — Abelian bootstrap [JHEP 08(2024) 154](https://link.springer.com/article/10.1007/JHEP08(2024)154) | Z₂ + U(1) lattice gauge bootstrap | two-sided bounds on Wilson loop averages |

## Framework-internal "literature" (already retained / bounded)

| Reference | Role |
|---|---|
| `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` | A11 — load-bearing reflection positivity input for the bootstrap |
| `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` | A7 — closed-form determinant on minimal block (fermion sector) |
| `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` | comparator: bounded MC value 0.5934 + bridge-support analytic upper-bound 0.59353 |
| `GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md` | sister obstruction: framework-point underdetermination |
| `G_BARE_RIGIDITY_THEOREM_NOTE.md` | g_bare = 1 forced by HS trace form on derived su(3) ⊂ End(V) |

## Standard QFT references (admitted-context)

- Wilson 1974 — original lattice gauge theory
- Eguchi-Kawai 1982 — large-N reduction, loop equations
- Migdal 1983 — Migdal-Makeenko equations
- Osterwalder-Seiler 1978 — RP for Wilson plaquette
- Sharatchandra-Thun-Weisz 1981 — RP for staggered fermions
- Drouffe-Zuber 1983 / Münster 1981 — SU(N) mean-field for plaquette

## Forbidden literature usage

- Any literature `⟨P⟩(β=6)` numerical value as derivation input
- Hard-coded Kazakov-Zheng bootstrap bracket as load-bearing
- Phenomenological 7/8 from Stefan-Boltzmann (irrelevant)
- Beyond-textbook claims without independent re-derivation

## Bridges if literature is invoked

When invoking literature, record the exact role in the runner output and
the note's "Out of scope (admitted-context)" section. Do NOT promote
admitted-context literature to load-bearing without independent
framework derivation.
