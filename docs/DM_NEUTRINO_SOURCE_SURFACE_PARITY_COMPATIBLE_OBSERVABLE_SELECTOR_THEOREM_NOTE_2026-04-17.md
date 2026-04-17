# DM Neutrino Source-Surface Parity-Compatible Observable Selector Theorem

**Date:** 2026-04-17  
**Script:** `scripts/frontier_dm_neutrino_source_surface_parity_compatible_observable_selector_theorem.py`

## Statement

On the strongest currently native local route in which the selector is taken to
come from the observable-principle scalar generator restricted to the exact
parity-compatible diagonal baseline family

`D = diag(A,B,B)`, `A > 0`, `B > 0`,

the active selector law closes exactly at

`delta_* = q_+* = sqrt(6)/3`,

and the exact source constraint then gives

`rho_* = sqrt(6)/3`, `r31,* = 1/2`, `phi_+,* = pi/2`.

However, the selected slice remains transport-subcritical: at `m = 0` it gives
a subcritical flavored readout, and even after optimizing the spectator line
`m` on the fixed selected slice `(delta_*, q_+*)`, the best exact readout stays
below `eta/eta_obs = 1`.

## Input stack

1. The observable-principle note gives the unique additive CPT-even scalar
   generator

   `W_D[J] = log|det(D+J)| - log|det D|`.

2. The active-affine source theorem gives the exact live source family

   `J_act(delta,q_+) = delta T_delta + q_+ T_q`.

3. The active-parity-compatible diagonal baseline theorem gives the exact local
   baseline family

   `D = diag(A,B,B)`.

4. The active half-plane theorem gives the exact admissible chamber

   `q_+ >= sqrt(8/3) - delta`

   together with the exact source constraint `delta + rho = sqrt(8/3)`.

## Exact determinant and curvature law

For `D = diag(A,B,B)` and `J_act(delta,q_+) = delta T_delta + q_+ T_q`,

`det(D + J_act) = A B^2 - (A + 2 B) (delta^2 + q_+^2) - 6 delta^2 q_+ + 2 q_+^3`.

At zero source, the exact bosonic curvature is isotropic on the active pair:

`- d^2 W_D |_(0,0) = 2 (A + 2 B) / (A B^2) * (delta^2 + q_+^2)`.

Because `2 (A + 2 B) / (A B^2) > 0`, the canonical positive quadratic selector
law on this route is a positive multiple of `delta^2 + q_+^2`.

## Exact minimizer on the active chamber

On the boundary `q_+ = sqrt(8/3) - delta`, the route action is proportional to

`delta^2 + (sqrt(8/3) - delta)^2`.

This is strictly convex and has unique stationary point

`delta_* = sqrt(8/3) / 2 = sqrt(6)/3`.

Hence

`q_+* = sqrt(8/3) - delta_* = sqrt(6)/3`.

Then the exact source constraint gives

`rho_* = sqrt(8)/sqrt(3) - delta_* = sqrt(6)/3`.

So the selected point is

`delta_* = q_+* = rho_* = sqrt(6)/3`,

with

`r31,* = 1/2`, `phi_+,* = pi/2`.

## Scope

This closes the **strongest currently native local parity-compatible diagonal route**.

It is **not yet route-independent current-bank closure**.

It is also **not yet full quantitative DM closure**, because this selected route
is still transport-subcritical.

The broader flagship blocker remains the route-independent right-sensitive
microscopic selector law on `dW_e^H = Schur_Ee(D_-)`, equivalently the
intrinsic `2`-real `Z_3` doublet-block point-selection law, together with the
quantitative route that must land on the constructive `eta/eta_obs = 1` point.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_parity_compatible_observable_selector_theorem.py
```
