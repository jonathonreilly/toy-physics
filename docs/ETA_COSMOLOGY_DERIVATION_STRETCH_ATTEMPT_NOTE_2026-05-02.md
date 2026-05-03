# η Cosmology Derivation — Stretch Attempt with Named Obstructions

**Date:** 2026-05-02
**Type:** stretch_attempt (output type c)
**Claim scope:** documents a worked stretch attempt at the
framework-internal derivation of the baryon-to-photon ratio η
≈ 6.12 × 10^{-10}. The attempt's content is: (1) verification of
the framework's two existing partial predictions η/η_obs ≈ 0.1888
and η/η_obs ≈ 1.0; (2) the geometric observation
1/0.189 ≈ 4π/√6 (3.2% mismatch); (3) catalogue of multiple
structural near-fits to 0.1888 (17/90, 31/32·√6/(4π), (7/8)^(1/4)·√6/(4π))
none derived; (4) three named obstructions to closure.

**Status:** stretch attempt, audit-lane ratification required for any
retained-grade interpretation. This is not a closing derivation.

**Runner:** [`scripts/frontier_eta_cosmology_stretch_attempt.py`](./../scripts/frontier_eta_cosmology_stretch_attempt.py)

**Authority role:** sharpens the η-derivation gap with explicit
named obstructions and a near-coincidence audit.

## A_min (minimal allowed premise set)

- (P1, retained_bounded) Framework's leptogenesis transport
  infrastructure (`DM_LEPTOGENESIS_*` cluster), supplying transport
  computations conditional on package constants.
- (P2, retained) Framework's Koide character infrastructure
  (`KOIDE_*` cluster), supplying the analytically constant character
  norm |z| = √6/2 on the selected slice.
- (P3, retained) Framework's three-generation matter structure
  (`THREE_GENERATION_STRUCTURE_NOTE`).

## Forbidden imports

- **η_obs as derivation input**: η_obs ≈ 6.12 × 10^{-10} from
  Planck 2018 is used ONLY as a comparator in the ratio
  η/η_obs (admitted-context comparator role label). It does NOT
  enter any derivation as input.
- **Ω_b, H_0 from observation**: not used as derivation inputs.
- **Package constants K_H, ε_1, γ, E1, E2, K00 as derivation inputs**:
  these are imported from the framework's exact_package, NOT derived.
  Their boundedness is the chain's load-bearing limitation.
- **No fitted selectors**.
- **No same-surface family arguments**.

## Worked attempt

### Step 1: Verify framework's existing partial predictions

From `OMEGA_LAMBDA_DERIVATION_NOTE.md`:

```text
Reduced surface (exact one-flavor transport): η/η_obs = 0.1888
Low-action PMNS support branch:                η/η_obs = 1.0
```

Both numbers are framework-internal computations on bounded
machinery. Neither is currently retained-grade.

The 1.0 value is suspiciously exact — likely a phenomenological
match. The 0.1888 value is more interesting: it's a framework-internal
prediction without obvious tuning.

### Step 2: Geometric observation 4π/√6

From `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`:

```text
1/0.189 ≈ 5.29
4π/√6 ≈ 5.13
Mismatch: 3.2%
```

Geometric interpretation:
- 4π = full solid angle on S²
- √6/2 = analytically constant Koide character norm |z|

Equivalent: 0.189 ≈ √6/(4π) = 0.1949, mismatch -3.1%.

This is an OBSERVATION ONLY. No formal derivation of the connection
between transport and Koide geometry exists in the framework.

### Step 3: Multiple near-fits to 0.1888

Numerical near-coincidence audit:

| Candidate structural origin | Value | Match with 0.1888 |
|----|----|----|
| 17/90 | 0.18889 | -0.05% (closest) |
| 31/32 · √6/(4π) | 0.1888 | -0.02% (very close) |
| (7/8)^(1/4) · √6/(4π) | 0.1885 | -0.16% |
| √6/(4π) | 0.1949 | -3.1% (geometric) |
| 1/(3π) | 0.1061 | -77% (ruled out) |

The framework's 0.1888 value is consistent with **multiple plausible
structural origins**. None is currently derived from framework
primitives. **The numerical near-coincidence is NOT evidence; it's a
RECORDING of the open derivation question.**

### Step 4: Why the framework's 0.1888 isn't currently a derivation

The 0.1888 prediction comes from the exact one-flavor transport
calculation in the leptogenesis cluster. That calculation depends on
admitted package constants:

- ε_1: CP-asymmetry parameter
- K_H: washout factor
- γ: damping rate
- E_1, E_2: heavy-neutrino energy scales
- K_00: matter-radiation coefficient

These are imported from `exact_package` (a framework data structure),
NOT derived from retained primitives. Hence the 0.1888 prediction
inherits the boundedness of those imports.

To make the prediction retained-grade, EACH of these constants needs
to be derived from framework primitives (not just supplied).

## Named Obstructions

### Obstruction 1: Package constants not derived from framework primitives

The leptogenesis transport calculation imports ε_1, K_H, γ, E_1, E_2,
K_00 from the framework's exact_package. **None is currently a
retained-grade derivation from minimal axioms.**

**Specific repair targets**:

- (1a) Derive ε_1 from the framework's CP-violation structure.
  Currently `ckm_cp_phase_structural_identity_theorem_note_2026-04-24`
  (audited_conditional, td=117) cites unratified upstream — needs
  retention.
- (1b) Derive K_H from framework's heavy-neutrino sector. Connects
  to `neutrino_majorana_operator_axiom_first_note` (cycle 06
  closing addressed this — would need cycle 06 audit-ratified).
- (1c) Derive γ, E_1, E_2, K_00 from framework's thermal/scattering
  cross-sections. Substantial QFT computation chain.

### Obstruction 2: Branch selector not derived

The framework has TWO partial predictions:
- 0.1888 (reduced surface, exact one-flavor transport)
- 1.0 (low-action PMNS branch)

Without a derivation of WHICH branch is physical, the framework
cannot uniquely predict η.

**Specific repair target**: derive the selector that picks one
branch over the other from framework primitives. Connects to:

- PMNS minimum-information / observable-relative-action / transport-extremal
  selectors (currently audited_conditional in
  `dm_leptogenesis_pmns_selector_bank_cp_sheet_blindness_theorem_note`,
  td=108).

### Obstruction 3: Geometric interpretation 4π/√6 not derived as exact

The geometric observation 1/0.189 ≈ 4π/√6 is a near-coincidence
(3.2% mismatch). If 4π/√6 IS the structural answer, the 3% mismatch
must come from higher-order corrections; if it's NOT the exact answer,
the 0.1888 needs a different structural origin (multiple candidates
listed in Step 3, none derived).

**Specific repair target**: derive the EXACT structural origin of
0.1888 from framework primitives, distinguishing the 4π/√6 geometric
hypothesis from alternatives (17/90, 31/32 · √6/(4π), etc.).

## Possible future paths (not pursued)

For future cycles:

1. **Promote ε_1 derivation**: connect `ckm_cp_phase` audit closure to
   the leptogenesis ε_1 input. If the CP-phase chain becomes
   retained, ε_1 becomes derived.
2. **Promote selector derivation**: identify which PMNS selector
   (minimum-info, observable-relative-action, transport-extremal)
   is the framework-native one, eliminating branch ambiguity.
3. **Geometric derivation of 4π/√6 connection**: build a runner that
   computes the transport gap from Koide character geometry directly,
   testing whether the framework's machinery gives EXACTLY √6/(4π)
   in some limit.
4. **Higher-order calculation**: if 4π/√6 is the leading term,
   compute next-order corrections to test the 3% gap explanation.

## What this claims

- `(P1)` Numerical verification of framework's 0.1888 and 1.0 partial
  predictions.
- `(P2)` Geometric observation 1/0.189 ≈ 4π/√6 numerically reproduced
  (3.2% mismatch).
- `(P3)` Catalogue of multiple structural near-fits to 0.1888.
- `(P4)` Three named obstructions documented with specific repair
  targets.

## What this does NOT claim

- Does NOT derive η from framework primitives.
- Does NOT pick between branches (0.1888 vs 1.0).
- Does NOT derive the structural origin of 0.1888 (multiple
  candidates noted, none derived).
- Does NOT close any audit-conditional row directly. Sharpens the
  named obstruction on the `dm_leptogenesis_*` cluster.
- Does NOT consume any PDG observed value as derivation input.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1, retained_bounded) `DM_LEPTOGENESIS_TRANSPORT_*` cluster.
- (P2, retained) `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19`
  for character norm and 4π/√6 observation.
- (P3, retained) `THREE_GENERATION_STRUCTURE_NOTE.md`.

## Forbidden imports check

- η_obs used only as comparator (ratio interpretation), not derivation
  input.
- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_eta_cosmology_stretch_attempt.py`](./../scripts/frontier_eta_cosmology_stretch_attempt.py)
verifies:

1. Framework's predicted η/η_obs = 0.1888 (numerically exact match
   to 4 decimals).
2. Geometric observation: √6/(4π) = 0.1949, mismatch 3.1% with
   framework prediction.
3. 1/0.189 ≈ 5.29 vs 4π/√6 ≈ 5.13, mismatch 3.2%.
4. Multiple structural near-fits catalogued: 17/90, 31/32 · √6/(4π),
   (7/8)^(1/4) · √6/(4π); each within sub-percent of 0.1888.
5. Counterfactual: 1/(3π) ≈ 0.106 — much further; ruled out as a
   simple geometric origin.
6. Three named obstructions explicitly recorded.

## Cross-references

- [`OMEGA_LAMBDA_DERIVATION_NOTE.md`](OMEGA_LAMBDA_DERIVATION_NOTE.md) —
  records the η import status and partial predictions.
- [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md) —
  records the 4π/√6 geometric observation.
- [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md) —
  parent row whose verdict cycle 09's named obstructions sharpen.
- [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md) —
  cycle 06: relevant to Obstruction 1b (heavy-neutrino sector).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) —
  audited_conditional; relevant to Obstruction 1a (ε_1 derivation).
