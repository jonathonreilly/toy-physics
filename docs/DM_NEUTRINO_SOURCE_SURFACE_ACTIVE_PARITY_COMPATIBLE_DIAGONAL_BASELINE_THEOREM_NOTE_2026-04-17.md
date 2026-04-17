# DM Neutrino Source-Surface Active Parity-Compatible Diagonal Baseline Theorem

**Date:** 2026-04-17  
**Status:** exact active-parity baseline theorem on the live `2`-real active
pair  
**Script:** `scripts/frontier_dm_neutrino_source_surface_active_parity_compatible_diagonal_baseline_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else used below is an atlas-native derived row, not a second axiom
or an external import.

## Question

The diagonal-baseline curvature theorem already showed:

- the scalar baseline `D = m I_3` is not unique,
- the full Euclidean diagonal family is `D = diag(A,B,B)`,
- and every such family member gives the same chamber minimizer
  `delta_* = q_+* = sqrt(6)/3`.

Can that larger family be characterized intrinsically from the exact active
grammar itself?

More precisely:

- the live active pair is already split into one `23`-odd direction `T_delta`
  and one `23`-even direction `T_q`;
- so if a positive diagonal baseline is to be compatible with the current
  active odd/even decomposition, what form can it have?

## Bottom line

Exactly one form:

- `D = diag(A,B,B)`.

Let

- `P_23 = [[1,0,0],[0,0,1],[0,1,0]]`

be the exact `23` exchange.

On the live active pair,

- `P_23 T_delta P_23 = -T_delta`
- `P_23 T_q P_23 = T_q`.

So `T_delta` is exactly `23`-odd and `T_q` is exactly `23`-even.

Now take any positive diagonal baseline

- `D = diag(A,B,C)`.

If it is compatible with this exact active parity grammar, it must preserve the
odd/even split, equivalently

- `P_23 D P_23 = D`

or

- `[D, P_23] = 0`.

For a diagonal matrix, that is equivalent to

- `B = C`.

So the exact active-parity-compatible diagonal family is precisely

- `D = diag(A,B,B)`.

By the earlier curvature boundary theorem, every such baseline yields the same
Euclidean comparison quadratic on the live active pair, up to an overall
positive factor, and therefore the same chamber minimizer

- `delta_* = q_+* = sqrt(6)/3`.

So within the class of diagonal baselines that actually respect the current
active odd/even grammar, the residual baseline ambiguity disappears.

This still does **not** close the DM selector lane. It removes the diagonal
baseline ambiguity only **inside** the parity-compatible class. The remaining
gap is still the physical selector principle itself, or the direct
right-sensitive `2`-real `Z_3` doublet-block law.

## Inputs

This note combines:

- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md)

No new selector axiom is added here. The point is to identify the exact
diagonal baseline class compatible with the live active parity decomposition.

## Exact theorem

### 1. The live active pair already has an exact `23` odd/even grading

On the live source-oriented affine chart,

- `T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]`
- `T_q     = [[0,1,1],[1,0,1],[1,1,0]]`.

Under `23` exchange

- `P_23 T_delta P_23 = -T_delta`
- `P_23 T_q P_23 = T_q`.

So the unresolved active pair is not just two arbitrary real directions. It is
already split into one exact `23`-odd direction and one exact `23`-even
direction.

### 2. A diagonal baseline preserves that grading iff it is `23`-symmetric

Let `D = diag(A,B,C)` be positive diagonal.

If `D` is to be compatible with the active odd/even decomposition, it must
commute with the parity involution:

- `P_23 D P_23 = D`.

For a diagonal matrix this is equivalent to

- `diag(A,C,B) = diag(A,B,C)`,

hence exactly

- `B = C`.

Therefore the active-parity-compatible diagonal family is precisely

- `D = diag(A,B,B)`.

### 3. Inside that family, the chamber minimizer is canonical

The active-curvature baseline boundary theorem already showed that for every
positive `23`-symmetric diagonal baseline,

- the descended observable-principle curvature on `(T_delta,T_q)` is Euclidean
  up to a positive prefactor,
- and the exact chamber minimizer is always
  `delta_* = q_+* = sqrt(6)/3`.

So once one restricts to diagonal baselines that are actually compatible with
the live active parity grammar, there is no remaining baseline ambiguity in the
comparison point.

## The theorem-level statement

**Theorem (Exact active-parity-compatible diagonal baseline family).**
Assume the exact active-affine point-selection boundary and the exact
`23`-symmetric baseline boundary theorem. Let

- `P_23 = [[1,0,0],[0,0,1],[0,1,0]]`

be the `23` exchange involution on the live active chart. Then

- `P_23 T_delta P_23 = -T_delta`,
- `P_23 T_q P_23 = T_q`.

Hence the live active pair carries an exact `23` odd/even grading. A positive
diagonal baseline `D = diag(A,B,C)` is compatible with that grading iff
`P_23 D P_23 = D`, equivalently iff `B = C`. Therefore the exact
active-parity-compatible diagonal family is precisely `D = diag(A,B,B)`. By
the exact curvature boundary theorem, every such baseline yields the same
chamber minimizer `delta_* = q_+* = sqrt(6)/3`.

## What this closes

This closes the diagonal-baseline ambiguity **within the natural active
parity-compatible class**.

The branch can now say more sharply:

- not every diagonal baseline is relevant,
- the ones that respect the exact active odd/even grammar are exactly the
  `23`-symmetric baselines,
- and on that whole compatible class the comparison point is already fixed.

## What this does not close

This note still does **not** close the DM selector lane.

It does **not** prove:

- that the physical selector must be obtained by minimizing the descended
  curvature,
- that a specific `diag(A,B,B)` baseline is canonically selected by the current
  bank,
- or that the right-sensitive `2`-real `Z_3` doublet-block law is solved.

So this removes one exact ambiguity in the observable-curvature route, but it
does not yet derive the physical selector law.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_active_parity_compatible_diagonal_baseline_theorem.py
```
