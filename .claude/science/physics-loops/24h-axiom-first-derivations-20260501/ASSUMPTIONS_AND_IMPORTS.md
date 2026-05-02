# Assumptions and Imports — 24h axiom-first campaign

**Date:** 2026-05-01

## A_min (allowed bare premises)

From `docs/MINIMAL_AXIOMS_2026-04-11.md`:

1. **A1 — local algebra:** physical local algebra is `Cl(3)`.
2. **A2 — substrate:** physical spatial substrate is `Z^3`.
3. **A3 — microscopic dynamics:** finite Grassmann/staggered-Dirac partition
   plus lattice operators built on that surface.
4. **A4 — canonical normalization:** `g_bare = 1` plus accepted plaquette /
   `u_0` surface and minimal APBC hierarchy block where applicable.

## Retained framework primitives allowed without re-derivation

- exact native `SU(2)` and graph-first structural `SU(3)`
- anomaly-forced `3+1` dimensions
- one-generation matter closure; three-generation matter structure
- retained `v = 246.282818290129 GeV`, `alpha_s(M_Z) = 0.1181`,
  `sin²θ_W(M_Z) = 0.2306`, `g_1`, `g_2`
- retained gravity stack:
  - `UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`
  - `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`
  - `UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
  - `SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- Apr 29 axiom-first foundations:
  - `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` (RP)
  - `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md` (SC1-SC4)
  - `AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
  - `AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  - `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
  - `AXIOM_FIRST_COLEMAN_MERMIN_WAGNER_THEOREM_NOTE_2026-04-29.md`
  - `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`
  - `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- Planck primitive coframe boundary carrier `c_cell = 1/4`
  (`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`)

## Admitted-context literature inputs allowed (with explicit ledger)

These are universal physics conventions that the framework adopts as inputs
but does not re-derive in this campaign. They must be flagged in each block
as admitted-context inputs.

- **Wick rotation** between Euclidean and Lorentzian signature (used by
  RP / spectrum condition reconstruction).
- **Standard imaginary-time periodicity ↔ thermal state correspondence**
  for the KMS derivation (this is what KMS *is*; the block derives it from
  RP, spectrum condition, and cyclic-trace structure of the transfer matrix).
- **Killing horizon / surface gravity κ** definition for the Hawking block
  (standard differential-geometric definition; the framework's GR action
  surface admits Killing vector fields).
- **Wald-Noether entropy formula** (already admitted in the BH 1/4 carrier
  retained note; we inherit that admission for first-law-of-BH-mechanics).
- **Standard differential geometry / variational calculus on the framework's
  smooth GR action surface** (already admitted in retained gravity stack).

## Forbidden imports

- No fitted parameters or selectors.
- No observed target values used as proof inputs.
- No literature theorems beyond the explicit admitted-context list above
  unless added to this ledger first.
- No re-use of already-derived identities listed in the "Out of scope"
  section of GOAL.md without an additive new-derivation step.

## Status discipline

Per `docs/repo/CONTROLLED_VOCABULARY.md` and the physics-loop SKILL:

- Branch-local source notes use `support`, `derived`, `bounded support`,
  `exact support`, `proposed_retained`, or `proposed_promoted`.
- `proposed_retained` / `proposed_promoted` only when
  `CLAIM_STATUS_CERTIFICATE.md` per block records `proposal_allowed: true`
  and audit-required: true.
- Bare `retained` / `promoted` is forbidden in branch-local artifacts.
