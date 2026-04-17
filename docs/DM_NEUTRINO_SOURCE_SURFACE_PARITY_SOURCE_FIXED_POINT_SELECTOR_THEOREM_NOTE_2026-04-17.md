# DM Neutrino Source-Surface Parity/Source Fixed-Point Selector Theorem

**Date:** 2026-04-17  
**Status:** exact conditional selector theorem on the strongest current native
local route  
**Script:** `scripts/frontier_dm_neutrino_source_surface_parity_source_fixed_point_selector_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else used below is an atlas-native derived row, not a second axiom
or an external import.

## Question

After the current branch reductions, the remaining live selector problem on the
source-oriented sheet is the exact active pair

- `(delta, q_+)`

on the chamber

- `q_+ >= sqrt(8/3) - delta`.

The current honest boundary is:

- the old exact bank was already point-blind on that chamber,
- the observable-principle scalar route became exact only after restricting to
  the active-parity-compatible diagonal family `D = diag(A,B,B)`,
- and the source side is already closed sharply only as the swap-even source
  mode `tau_E = tau_T = 1/2`.

Can those two exact native quotient structures together force the live point,
without adding a free variational ansatz?

## Bottom line

Yes, on that exact local route.

There are two exact quotient facts:

1. **Active curvature quotient.**
   On every positive active-parity-compatible diagonal baseline
   `D = diag(A,B,B)`, the zero-source observable-principle curvature on the
   active pair is

   - `Q_(A,B)(delta,q_+) = lambda(A,B) (delta^2 + q_+^2)`

   with positive scalar factor

   - `lambda(A,B) = 2 (A + 2 B) / (A B^2)`.

   So the current exact local scalar selector route is blind to the active
   coordinate labels and descends to the quotient under

   - `A(delta,q_+) = (q_+, delta)`.

   Therefore any unique selected point on that route must lie on the fixed set

   - `delta = q_+ = t`.

2. **Sharp even-source quotient.**
   The exact sharp source theorem already fixes the even source as the swap-even
   projector with coordinates

   - `(tau_E, tau_T) = (1/2, 1/2)`,
   - `tau_+ = 1`.

   On the live source-oriented sheet, the exact active generator `T_delta`
   redistributes the fixed source channel

   - `E1 = delta + rho = sqrt(8/3)`

   between the two complementary legs `delta` and `rho`, and the current exact
   source-facing bank carries no sharp source-side datum distinguishing those
   two legs separately.

   So, by the same quotient logic as the exact weak even swap-reduction
   theorem, the sharp source route descends to the split quotient

   - `(delta, rho) ~ (rho, delta)`

   at fixed `delta + rho = E1`.

   Therefore any unique selected split on that route must satisfy

   - `delta = rho = E1 / 2`.

Combining the two exact quotient conditions gives

- `delta_* = q_+* = rho_* = E1 / 2 = sqrt(6) / 3`,

and therefore

- `r31,* = 1/2`,
- `phi_+,* = pi/2`.

So the live point is forced on the strongest currently native local selector
route:

- parity-compatible observable curvature gives the active diagonal fixed set,
- sharp even-source symmetry gives the equal source split,
- and the unique compatible point is the same one found earlier by the
  diagnostic and support routes.

## Inputs

This theorem combines:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md)

No free variational selector is added here. The point is to use the two exact
native quotient structures that are already present on the local source-side
route.

## Exact theorem

### 1. The native local scalar selector route descends to the active exchange quotient

The observable principle gives the unique additive CPT-even scalar generator.
On the exact active pair and on every positive diagonal baseline compatible
with the exact `23` odd/even grading,

- `D = diag(A,B,B)`,

the zero-source curvature is

- `Q_(A,B)(delta,q_+) = lambda(A,B) (delta^2 + q_+^2)`.

So the local scalar route is exactly invariant under the active-coordinate
exchange

- `A(delta,q_+) = (q_+, delta)`.

Therefore any unique selected point on that exact local scalar route must be
`A`-fixed:

- `delta = q_+ = t`.

### 2. The sharp even source descends to the source-split quotient

The exact sharp source theorem fixes

- `(tau_E, tau_T) = (1/2, 1/2)`,
- `tau_+ = 1`.

On the live source-oriented sheet, the active generator `T_delta` redistributes
the fixed source channel

- `E1 = delta + rho = sqrt(8/3)`

between two complementary legs `delta` and `rho`.

But on the current exact sharp source side there is no separate source label
for those two legs: only the swap-even source mode survives exactly. So the
current sharp source route descends to the quotient

- `(delta, rho) ~ (rho, delta)`

at fixed `delta + rho = E1`.

Therefore any unique selected split on that sharp source route must be fixed by
that swap:

- `delta = rho = E1 / 2`.

### 3. The unique compatible live point is forced

From the active curvature quotient:

- `delta = q_+ = t`.

From the sharp even-source quotient:

- `delta = rho = E1 / 2`.

Since `E1 = sqrt(8/3)`,

- `t = E1 / 2 = sqrt(6) / 3`.

Therefore

- `delta_* = q_+* = rho_* = sqrt(6) / 3`.

The exact active-half-plane inverse chart then gives

- `r31,* = 1/2`,
- `phi_+,* = pi/2`.

## The theorem-level statement

**Theorem (Parity/source fixed-point selector on the live source-oriented
sheet).**
Assume:

1. the exact additive CPT-even scalar observable principle,
2. the exact active-half-plane theorem,
3. the exact active-affine point-selection boundary,
4. the exact active-parity-compatible diagonal baseline theorem,
5. the exact sharp source-amplitude theorem,
6. the exact weak even swap-reduction pattern for quotient logic on a
   source-side swap-indistinguishable carrier.

Then:

1. on every positive active-parity-compatible diagonal baseline
   `D = diag(A,B,B)`, the local scalar curvature on the active pair is
   `Q_(A,B)(delta,q_+) = lambda(A,B) (delta^2 + q_+^2)`, so the exact native
   local scalar route descends to the active exchange quotient and any unique
   selected point satisfies `delta = q_+`;
2. the exact sharp source route fixes only the swap-even source mode
   `(tau_E, tau_T) = (1/2, 1/2)` and hence descends to the unresolved split
   quotient `(delta, rho) ~ (rho, delta)` at fixed `delta + rho = sqrt(8/3)`,
   so any unique selected split satisfies `delta = rho = sqrt(8/3) / 2`;
3. therefore the unique compatible live point is
   `delta_* = q_+* = rho_* = sqrt(6) / 3`,
   with `r31,* = 1/2` and `phi_+,* = pi/2`.

## What this closes

This closes the last local selector gap on the strongest current native route.

The branch can now say more sharply:

- the parity-compatible observable-curvature route already forces the active
  diagonal fixed set,
- the exact sharp source route already forces the equal split of the fixed
  `E1` channel,
- and the unique compatible live point is
  `delta_* = q_+* = rho_* = sqrt(6) / 3`.

So the remaining open DM/leptogenesis work is no longer local point selection
on the source surface.

## What this does not close

This note does **not** claim that every conceivable future selector route must
factor through this exact local route.

It closes the strongest currently native local route. It does not say there is
no alternative future microscopic route that could rederive the same point more
directly from a different right-sensitive object.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_parity_source_fixed_point_selector_theorem.py
```
