# GOAL — Plaquette Bootstrap Closure Campaign

**Slug:** `plaquette-bootstrap-closure-20260503`
**Date launched:** 2026-05-03
**Mode:** campaign (12h budget, literature allowed)
**Source-note authority:** branch-local; later audit lane decides ratified status

## Net call (background)

This campaign continues the user's H1 ladder for closing `⟨P⟩(β=6)`
analytically. H1 Route 1 (mean-field saddle on V-invariant minimal block)
landed as named-obstruction stretch in PR
[#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410)
of the prior campaign (`vev-v-singlet-derivation-20260502`). H1 Route 3
(modern lattice bootstrap) was explicitly out of scope of that campaign
because of (a) ~6-month research-project scope and (b) missing SDP
infrastructure (CVXPY/Mosek). The user has asked to launch H1 Route 3
as its own 12h campaign.

## Scope reality-check (after preflight)

| Constraint | Finding |
|---|---|
| CVXPY available? | NO — system Python is PEP 668-restricted (`pip install` blocked). No SDP solver in environment. |
| SciPy / NumPy available? | YES — `scipy 1.17.1`, `numpy 2.4.4`. Sufficient for small-matrix analytical PSD checks. |
| Reflection-positivity theorem on framework? | YES — `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` proves R1-R4 on A_min for canonical CL3-on-Z3 action. **This is exactly the load-bearing positivity input the bootstrap needs.** |
| Wilson loop / Migdal-Makeenko infrastructure on framework? | NOT explicitly — must derive small-set loop equations on framework surface as part of this campaign |
| Recent literature? | Kazakov-Zheng 2022 (SU(∞), [arXiv:2203.11360](https://arxiv.org/abs/2203.11360)); Kazakov-Zheng 2024 finite N ([arXiv:2404.16925](https://arxiv.org/abs/2404.16925)); JHEP 12(2025) 033 SU(3) lattice YM bootstrap; JHEP 08(2024) 154 Abelian. Current best published bracket near λ≈1.35: ⟨P⟩ ≈ 0.59–0.61 at L_max=16 with ~100k loop equations + 6505×6505 matrices reduced to 15×78 blocks. |

**Realistic 12h scope:** small-truncation (L_max ≤ 4) analytical bound via the
framework's existing RP theorem + small Gram-matrix PSD conditions, NOT a
full numerical SDP bracket. Output: a NEW analytical lower bound on
`⟨P⟩(β=6)` derived inside the framework's retained surface.

## Campaign target

**Block 01 (PRIMARY):** Bootstrap framework integration + smallest non-trivial
analytical bound:

- Explicit identification of the framework's reflection-positivity
  theorem as a sufficient condition for Wilson-loop Gram-matrix PSD
  on the V-invariant minimal Klein-four block
- Smallest-truncation Gram matrix `M_2 = ⟨W_i^† W_j⟩` for `i, j ∈ {1, P}` on
  the minimal block (2x2 case)
- Loop equation for `⟨P²⟩` in terms of `⟨P⟩` and β (Migdal-Makeenko or
  Schwinger-Dyson on the minimal block)
- Combine PSD + loop equation to derive a NEW analytical lower bound on
  `⟨P⟩(β=6)`

**Block 02 (SECONDARY):** Framework-specific positivity refinement:

- Larger truncation Gram matrix (3x3 with `{1, P, P²}`) using same RP setup
- Cl(3)/Klein-four-specific positivity constraints from the framework's
  V-invariant subspace
- Refine the analytical bound; integrate with bridge-support stack
  (PLAQUETTE_SELF_CONSISTENCY analytic upper-bound P(6) ≈ 0.59353)

## Stop conditions

- Runtime exhaustion (12h)
- Volume cap (5 PRs / 24h)
- Cluster cap (2 PRs per `gauge_vacuum_plaquette_*` family per campaign)
- Corollary exhaustion (no new load-bearing premise / residual remains)
- Value-gate exhaustion (V1-V5 fail on every remaining queue item)

## Forbidden imports

- PDG `v_meas`, `m_H`, etc. as derivation input (comparator only)
- Lattice-MC `⟨P⟩ = 0.5934` as load-bearing (comparator only)
- Hard-coded bootstrap bound (must DERIVE from PSD + loop equations)
- Same-surface family arguments
- Support-tier routes used to claim retained-tier equality
