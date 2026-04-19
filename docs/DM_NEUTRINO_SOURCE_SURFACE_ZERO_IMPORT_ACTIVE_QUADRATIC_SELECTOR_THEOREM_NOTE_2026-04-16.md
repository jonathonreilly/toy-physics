# DM Neutrino Source-Surface Zero-Import Active Quadratic Selector Theorem

**Date:** 2026-04-16  
**Status:** exact zero-import selector theorem on the live `2`-real active
pair  
**Script:** `scripts/frontier_dm_neutrino_source_surface_zero_import_active_quadratic_selector_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else used below is an atlas-native derived row, not a second axiom
or an external import.

## Question

Can the earlier input-driven active selector be replaced by a zero-import
theorem?

More precisely:

- the current exact bank already reduces the live mainline object to the
  active pair `(delta, q_+)`,
- the old current-bank closeout theorem says the bank itself does not pick a
  point,
- the previous constructive note closed the point only by **adding** a new
  variational selector input.

Can the **same quadratic law** now be derived natively from the existing
`Cl(3)/Z^3` bank?

## Bottom line

Yes.

The same quadratic selector law is already native once the exact observable
principle is descended onto the active pair.

Take the exact active source family

- `J_act(delta,q_+) = delta T_delta + q_+ T_q`,

with

- `T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]`
- `T_q     = [[0,1,1],[1,0,1],[1,1,0]]`.

The exact unique additive CPT-even scalar generator is already

- `W[J] = log|det(D+J)| - log|det D|`.

On a scalar baseline `D = m I_3`, the active family has exact determinant

- `det(m I_3 + J_act) = (m + 2 q_+) ((m - q_+)^2 - 3 delta^2)`.

So no new action ansatz is being imported. The active source-response is
already an exact function forced by the bank.

Its zero-source bosonic curvature defines the canonical active bilinear form:

- `K_act(X,Y) = - d^2/ds dt W[sX + tY] |_(s=t=0)`.

Evaluated on the active generators, this gives

- `K_act(T_delta, T_delta) = 6 / m^2`
- `K_act(T_q, T_q) = 6 / m^2`
- `K_act(T_delta, T_q) = 0`.

Therefore the native positive quadratic action is exactly

- `Q_act(delta,q_+) = m^2 K_act(J_act,J_act)`
- `= 6(delta^2 + q_+^2)`.

That is the same quadratic law used in the earlier variational selector note,
but now it is **derived**, not added.

Minimizing this native coercive quadratic on the exact active chamber

- `q_+ >= sqrt(8/3) - delta`

selects the unique point

- `delta_* = q_+* = sqrt(6)/3`,

hence

- `rho_* = sqrt(6)/3`
- `r31,* = 1/2`
- `phi_+,* = pi/2`.

So the point-selection law is now zero-import on the current branch.

## Inputs

This theorem uses only atlas-native rows already on the single-axiom surface:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)

No new selector axiom or extra variational input is added here.

## Exact theorem

### 1. The observable principle supplies the native active source-response family

The exact unique additive CPT-even scalar generator is

- `W[J] = log|det(D+J)| - log|det D|`.

Restrict it to the exact active family

- `J_act(delta,q_+) = delta T_delta + q_+ T_q`

on a scalar baseline `D = m I_3`.

Direct determinant evaluation gives

- `det(m I_3 + J_act) = (m + 2 q_+) ((m - q_+)^2 - 3 delta^2)`.

So the active source-response is already intrinsic to the old bank.

### 2. The zero-source curvature descends to the active pair as an exact bilinear form

Because

- `Tr(T_delta) = Tr(T_q) = 0`,

the linear source term vanishes at the origin.

The observable-principle curvature kernel is therefore

- `K_act(X,Y) = (1/m^2) Tr(XY)`

on this traceless finite block.

Now the active generators satisfy

- `Tr(T_delta T_delta) = 6`
- `Tr(T_q T_q) = 6`
- `Tr(T_delta T_q) = 0`.

So the descended native active bilinear form is exactly

- `K_act(J_act,J_act) = (6/m^2) (delta^2 + q_+^2)`.

### 3. The native positive quadratic action is exactly the previous selector law

Rescaling out the universal positive factor `m^{-2}` gives the canonical
positive active action

- `Q_act(delta,q_+) = 6(delta^2 + q_+^2)`.

So the earlier “minimal active displacement” law is not a new input after all.
It is the exact Riesz/bosonic quadratic descended from the native source
response.

### 4. The exact active chamber then yields the same unique selected point

The active-half-plane theorem already gives the exact admissible domain

- `q_+ >= sqrt(8/3) - delta`.

Since `Q_act` is strictly convex, the constrained minimizer is unique. The
origin is inadmissible, so the minimizer lies on the boundary

- `q_+ = sqrt(8/3) - delta`.

Substituting into `Q_act` gives

- `Q_bdy(delta) = 6(delta^2 + (sqrt(8/3) - delta)^2)`.

Differentiating and solving gives

- `delta_* = sqrt(6)/3`
- `q_+* = sqrt(6)/3`.

Therefore

- `rho_* = sqrt(8/3) - delta_* = sqrt(6)/3`
- `r31,* = 1/2`
- `phi_+,* = pi/2`.

## The theorem-level statement

**Theorem (Zero-import native quadratic selector on the active pair).**
Assume the exact observable principle from the axiom, the exact active-affine
point-selection theorem, and the exact active half-plane theorem. Then the
restriction of the unique additive CPT-even scalar generator
`W[J] = log|det(D+J)| - log|det D|` to the active family
`J_act(delta,q_+) = delta T_delta + q_+ T_q` induces the exact native
curvature bilinear form
`K_act(J_act,J_act) = (6/m^2)(delta^2 + q_+^2)`. Hence the canonical positive
quadratic action is exactly
`Q_act(delta,q_+) = 6(delta^2 + q_+^2)`, with no new selector input. Minimizing
that native action on the exact chamber `q_+ >= sqrt(8/3) - delta` yields the
unique selected point
`delta_* = q_+* = sqrt(6)/3`, equivalently
`rho_* = sqrt(6)/3`, `r31,* = 1/2`, and `phi_+,* = pi/2`.

## What this closes

This closes the zero-import selector law on the live `2`-real active pair.

The branch can now say:

- the current bank alone was point-blind,
- but the same bank already carried the native bosonic curvature law,
- and that curvature law yields exactly the same selected point as the earlier
  variational note,
- with no extra selector input.

## What this does not close

This closes the active point-selection law.

It still does **not** by itself prove the broader downstream baryogenesis
kernel is fully closed with zero imports. But the specific active selector gap
is no longer open.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_zero_import_active_quadratic_selector_theorem.py
```
