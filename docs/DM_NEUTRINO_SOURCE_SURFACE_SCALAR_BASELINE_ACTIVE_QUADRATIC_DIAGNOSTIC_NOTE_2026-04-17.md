# DM Neutrino Source-Surface Scalar-Baseline Active Quadratic Diagnostic Note

**Date:** 2026-04-17  
**Status:** bounded diagnostic tool on the live `2`-real active pair  
**Script:** `scripts/frontier_dm_neutrino_source_surface_scalar_baseline_active_quadratic_diagnostic.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else used below is an atlas-native derived row, not a second axiom
or an external import.

## Question

Is there still a useful zero-import comparison tool on the live active pair
`(delta, q_+)`, even though the current exact bank does **not** contain a
theorem-native selector law?

## Bottom line

Yes, but only in a bounded sense.

If one restricts the observable-principle scalar generator

- `W[J] = log|det(D+J)| - log|det D|`

to the exact active family

- `J_act(delta,q_+) = delta T_delta + q_+ T_q`

and then further restricts the baseline to a **chosen scalar matrix**

- `D = m I_3`,

the zero-source curvature is exactly isotropic on the active pair:

- `K_m(T_delta, T_delta) = 6 / m^2`
- `K_m(T_q, T_q) = 6 / m^2`
- `K_m(T_delta, T_q) = 0`.

So the scalar-baseline diagnostic quadratic is exactly

- `Q_scalar(delta,q_+) = m^2 K_m(J_act,J_act)`
- `= 6(delta^2 + q_+^2)`.

Minimizing this **diagnostic** quadratic on the exact active chamber

- `q_+ >= sqrt(8/3) - delta`

returns the same chamber point as the older variational note:

- `delta_* = q_+* = sqrt(6)/3`
- `rho_* = sqrt(6)/3`
- `r31,* = 1/2`
- `phi_+,* = pi/2`.

That makes this a useful comparison tool for future microscopic selector work.
It does **not** prove that the physical active point is selected by minimizing
this quadratic.

## Inputs

This diagnostic uses only existing atlas-native rows:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)

No new physics claim is added here. The point is only to record a reusable
diagnostic/comparison law.

## Exact scalar-baseline identity

### 1. The active family is already exact

Take the exact active source family

- `J_act(delta,q_+) = delta T_delta + q_+ T_q`,

with

- `T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]`
- `T_q     = [[0,1,1],[1,0,1],[1,1,0]]`.

On a scalar baseline `D = m I_3`, direct determinant evaluation gives

- `det(m I_3 + J_act) = (m + 2 q_+) ((m - q_+)^2 - 3 delta^2)`.

So the observable-principle source-response is explicit on the active pair.

### 2. The scalar-baseline zero-source curvature is isotropic

At zero source, the curvature bilinear form is

- `K_m(X,Y) = - d^2/ds dt W[sX + tY] |_(s=t=0)`.

For the scalar baseline this reduces to

- `K_m(X,Y) = (1/m^2) Tr(XY)`

on the active traceless block. Since

- `Tr(T_delta T_delta) = 6`
- `Tr(T_q T_q) = 6`
- `Tr(T_delta T_q) = 0`,

the scalar-baseline quadratic is exactly

- `Q_scalar(delta,q_+) = 6(delta^2 + q_+^2)`.

### 3. The chamber minimizer of this diagnostic is exact

The active-half-plane theorem gives the exact admissible chamber

- `q_+ >= sqrt(8/3) - delta`.

The diagnostic quadratic is strictly convex, so its constrained minimizer is
unique and lies on the boundary. Substituting

- `q_+ = sqrt(8/3) - delta`

gives

- `Q_bdy(delta) = 6(delta^2 + (sqrt(8/3) - delta)^2)`,

whose derivative vanishes exactly at

- `delta_* = sqrt(6)/3`.

Hence

- `q_+* = sqrt(6)/3`
- `rho_* = sqrt(6)/3`
- `r31,* = 1/2`
- `phi_+,* = pi/2`.

## Why this is useful

This diagnostic is worth keeping because it:

- gives a closed, exact comparison law on the live active pair,
- singles out the same chamber point as the earlier variational construction,
- provides a concrete target against which future microscopic selector laws can
  be compared,
- helps separate “which point does this tool prefer?” from the stronger and
  still-open question “why is that preference physically forced?”

## What this does **not** say

This note does **not** close the DM selector law.

In particular, it does **not** say:

- that the physical active point is the minimizer of `Q_scalar`,
- that the minimization principle is already contained in the current exact
  bank,
- that the scalar baseline `D = m I_3` is the unique canonical baseline on the
  live sheet,
- that the open right-sensitive `2`-real `Z_3` doublet-block selector law is
  solved.

For generic positive baselines `D`, the descended curvature on
`(T_delta, T_q)` is not isotropic and can acquire a mixed term, so the
quadratic recorded here is specifically a **scalar-baseline diagnostic**, not a
baseline-independent theorem-native selector.

## Clean unresolved issue to attack later

The exact issue is now sharply exposed.

To upgrade this diagnostic into real selector closure, one would need at least
one of the following:

- a theorem-native reason that the physically relevant descended curvature must
  be evaluated on a canonical scalar baseline, rather than on a generic
  positive baseline,
- or a theorem-native reason that the physical active point is selected by
  minimizing a specific right-sensitive functional on the active chamber,
- or a direct microscopic derivation of the missing right-sensitive
  `2`-real `Z_3` doublet-block law itself, making the quadratic comparison tool
  unnecessary.

Without one of those upgrades, the present law remains exactly what it is:

- a strong comparison diagnostic,
- a useful target for future selector attempts,
- not the physical selector theorem.

## Safe packaging statement

This is a reusable diagnostic tool on the DM open gate:

- exact under the chosen scalar baseline,
- useful for attack planning and law comparison,
- not authority for the live DM selector closure.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_scalar_baseline_active_quadratic_diagnostic.py
```
