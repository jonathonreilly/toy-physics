# GOAL — Cycle 21 PMNS Branch Selector

## Parent obstruction

Cycle 09 (PR #411) Obstruction 2:

> "Branch selector not derived: framework has two partial η/η_obs
> predictions, 0.1888 (reduced surface, exact one-flavor transport)
> and 1.0 (low-action PMNS support branch); without a derivation of
> WHICH branch is physical, the framework cannot uniquely predict η."

## Problem statement

The framework's `dW_e^H` source-side bundle admits two distinct
"branches" of admissible transport closures:

- **Branch A** (one-flavor reduced surface): exact theorem-native
  radiation transport on the reduced one-flavor surface, computing
  `η/η_obs = 0.18879` directly from `(516/53009) · Y₀² · F_CP ·
  κ_axiom`. Cycle 18 reported this structural decomposition.

- **Branch B** (PMNS-assisted off-seed source): on the fixed native
  N_e seed surface `(x̄, ȳ) = (0.5633, 0.3067)`, the constructive
  projected-source chamber contains an exact `η/η_obs = 1` closure
  point at `λ_* = 0.7955` along the seed↔witness interpolation. The
  selector among off-seed sources is one of:
    - **min-info** (`D_KL(x||x_seed) + D_KL(y||y_seed) + (1 - cos δ)`),
    - **observable-relative-action** (`Tr(H_seed^{-1} H_e) -
      log det(H_seed^{-1} H_e) - 3`),
    - **transport-extremal** (`max_i η_i / η_obs`),
    - **constructive continuity closure** (the explicit λ_* root).

## Honest target

Stretch attempt — output type (c) — at the genuine new physics
question of WHICH branch is framework-native.

## Best ranked route

Route D (symmetry / parity / CP-sheet blindness). This is the
strongest negative-structural result already carried on the current surface
(`DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16`),
which proves all four Branch-B selectors are even under `δ → -δ`
while the source channel `γ = x_1 y_3 sin(δ)` is odd.

## Forbidden imports

- No PDG observed values (η_obs, m_β, etc.) as derivation inputs.
- No literature numerical comparators as proof inputs.
- No fitted selectors.
- No same-surface family arguments.
- Cycle 18's (516/53009)·Y₀²·F_CP·κ_axiom decomposition is admitted
  as prior-cycle output.

## What this cycle aims to deliver

1. A branch-selector note with five named routes (A-E) scored.
2. A runner that:
   - reproduces the four candidate Branch-B selectors numerically,
   - verifies the CP-sheet blindness parity argument symbolically,
   - documents the (Branch-A vs Branch-B) frame distinction, and
   - records counterfactual: a hypothetical CP-odd selector would
     break the parity.
3. A V1-V5 promotion-value-gate certificate.

## What this cycle does NOT claim

- Does NOT promote any selector to retained.
- Does NOT close cycle 09 Obstruction 2 by constructing a positive
  selector — sharpens it into a structural exclusion.
- Does NOT consume η_obs as derivation input.
