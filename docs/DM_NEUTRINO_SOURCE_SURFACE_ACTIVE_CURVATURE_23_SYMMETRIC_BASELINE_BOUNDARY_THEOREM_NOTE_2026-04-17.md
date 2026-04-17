# DM Neutrino Source-Surface Active Curvature `23`-Symmetric Baseline Boundary Theorem

**Date:** 2026-04-17  
**Status:** exact observable-curvature boundary theorem for the live `2`-real
active pair  
**Script:** `scripts/frontier_dm_neutrino_source_surface_active_curvature_23_symmetric_baseline_boundary.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else used below is an atlas-native derived row, not a second axiom
or an external import.

## Question

The scalar-baseline diagnostic already shows that on the chosen diagonal
baseline

- `D = m I_3`

the observable-principle zero-source curvature on the active pair
`(T_delta, T_q)` is isotropic and yields the exact comparison quadratic

- `Q_scalar(delta,q_+) = 6(delta^2 + q_+^2)`.

How special is that scalar choice?

More precisely: for a general positive diagonal baseline

- `D = diag(A,B,C)`,

when is the descended observable-principle curvature on the active pair

- free of a mixed term,
- isotropic,
- and therefore equivalent up to a positive scalar factor to
  `delta^2 + q_+^2`?

## Bottom line

The scalar baseline is **not** the unique diagonal baseline with isotropic
active curvature.

For the exact active generators

- `T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]`
- `T_q     = [[0,1,1],[1,0,1],[1,1,0]]`

and any positive diagonal baseline

- `D = diag(A,B,C)`,

the zero-source observable-principle curvature on the active pair is exactly

- `K(T_delta,T_delta) = (A(B^2 + C^2) + 2BC(B+C)) / (A B^2 C^2)`
- `K(T_q,T_q)         = 2(A+B+C) / (A B C)`
- `K(T_delta,T_q)     = 2(B-C) / (A B C)`.

Therefore

- `K(T_delta,T_q) = 0` iff `B = C`,
- `K(T_delta,T_delta) = K(T_q,T_q)` iff `B = C`,
- and
  `K(T_delta,T_delta) - K(T_q,T_q) = (B-C)^2 / (B^2 C^2)`.

So the exact isotropic diagonal family is not just the scalar line
`A = B = C`. It is the full `23`-symmetric positive family

- `D = diag(A,B,B)`.

On that family, the active quadratic is always

- `Q_(A,B)(delta,q_+) = lambda(A,B) (delta^2 + q_+^2)`

with positive factor

- `lambda(A,B) = 2(A+2B) / (A B^2)`.

Hence every `23`-symmetric positive diagonal baseline picks the same chamber
minimizer

- `delta_* = q_+* = sqrt(6)/3`

as a **diagnostic** comparison point.

This still does **not** close the DM selector lane. The current bank does not
derive a canonical positive `23`-symmetric baseline, nor does it derive the
physical minimization principle itself.

## Inputs

This note sharpens the existing observable-principle comparison route:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md)

No new selector axiom is added here. The point is to characterize exactly when
the observable-principle diagonal curvature on the active pair becomes
Euclidean.

## Exact theorem

### 1. The diagonal-baseline active curvature has an exact closed form

For the observable-principle scalar generator

- `W[J] = log|det(D+J)| - log|det D|`,

the zero-source curvature on a positive diagonal baseline

- `D = diag(A,B,C)`

is

- `K(X,Y) = Tr(D^{-1} X D^{-1} Y)`

on the traceless active block.

Evaluating this on the exact active generators gives the closed formulas

- `K(T_delta,T_delta) = (A(B^2 + C^2) + 2BC(B+C)) / (A B^2 C^2)`
- `K(T_q,T_q)         = 2(A+B+C) / (A B C)`
- `K(T_delta,T_q)     = 2(B-C) / (A B C)`.

### 2. The mixed term vanishes exactly on the `23`-symmetric diagonal family

The mixed term is

- `K(T_delta,T_q) = 2(B-C)/(A B C)`.

So the diagonal-baseline active curvature is block-diagonal on the active pair
if and only if

- `B = C`.

No stronger scalar condition is needed.

### 3. Isotropy is equivalent to the same `23` symmetry

Subtracting the two diagonal entries gives

- `K(T_delta,T_delta) - K(T_q,T_q) = (B-C)^2 / (B^2 C^2)`.

Therefore the diagonal-baseline active curvature is isotropic if and only if

- `B = C`.

So the exact isotropic diagonal family is precisely

- `D = diag(A,B,B)`.

### 4. On that family, the chamber minimizer is baseline-independent

If `D = diag(A,B,B)`, then

- `K(T_delta,T_delta) = K(T_q,T_q) = 2(A+2B)/(A B^2)`
- `K(T_delta,T_q) = 0`.

So the active quadratic is

- `Q_(A,B)(delta,q_+) = [2(A+2B)/(A B^2)] (delta^2 + q_+^2)`.

The active chamber is still exactly

- `q_+ >= sqrt(8/3) - delta`.

Since the positive prefactor does not affect the minimizer, every diagonal
`23`-symmetric baseline gives the same chamber point

- `delta_* = q_+* = sqrt(6)/3`

as the older scalar-baseline diagnostic.

## The theorem-level statement

**Theorem (Exact `23`-symmetric baseline boundary for diagonal active
curvature).**
Assume the exact observable principle, the exact active-affine point-selection
boundary, and the exact active half-plane theorem. Let
`D = diag(A,B,C)` be any positive diagonal baseline and let `K` denote the
zero-source observable-principle curvature restricted to the active pair
spanned by `(T_delta,T_q)`. Then

- `K(T_delta,T_delta) = (A(B^2 + C^2) + 2BC(B+C)) / (A B^2 C^2)`
- `K(T_q,T_q)         = 2(A+B+C) / (A B C)`
- `K(T_delta,T_q)     = 2(B-C) / (A B C)`

and hence

- `K(T_delta,T_q) = 0` iff `B = C`,
- `K(T_delta,T_delta) = K(T_q,T_q)` iff `B = C`.

Equivalently, the diagonal-baseline observable-principle curvature on the live
active pair is Euclidean up to an overall positive factor exactly on the
`23`-symmetric positive family `D = diag(A,B,B)`, with scalar baselines as a special case.
On that family, minimizing the resulting comparison quadratic on the exact
active chamber always yields the same chamber point `delta_* = q_+* = sqrt(6)/3`.

## What this closes

This closes the diagonal-baseline isotropy question exactly.

The branch can now say more sharply:

- the scalar-baseline comparison law was not unique to scalar baselines,
- the exact Euclidean diagnostic family is the larger `23`-symmetric diagonal
  family,
- and the chamber minimizer is robust across that whole family.

## What this does not close

This note still does **not** close the DM selector lane.

It does **not** prove:

- that the current bank canonically selects a positive `23`-symmetric baseline,
- that the physical active point is selected by minimizing this diagnostic
  quadratic,
- or that the right-sensitive `2`-real `Z_3` doublet-block law is solved.

So this is an exact boundary theorem for the observable-curvature route, not a selector-closeout theorem.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_active_curvature_23_symmetric_baseline_boundary.py
```
