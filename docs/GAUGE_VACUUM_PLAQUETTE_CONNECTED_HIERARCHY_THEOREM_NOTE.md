# Gauge-Vacuum Plaquette Connected-Hierarchy Theorem

**Date:** 2026-04-16
**Status:** exact connected-cumulant hierarchy theorem for the Wilson
plaquette reduction law on finite evaluation surfaces; explicit closure at
`beta = 6` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py`

## Question

After closing the exact implicit reduction law and its exact susceptibility
transport equation, can we identify the exact nonperturbative object that still
blocks analytic closure of the plaquette at the framework point?

## Answer

Yes.

The remaining object is not just an unnamed scalar function `chi_L(beta)`. It
is an exact connected plaquette hierarchy.

If

`X_p(U) = (1/3) Re Tr U_p`

and

`Z_L[J; beta] = integral DU exp[beta sum_p X_p(U) + sum_p J_p X_p(U)]`,

then with

`W_L[J; beta] = log Z_L[J; beta]`

the connected `n`-point plaquette cumulants are

`C_n(p_1, ..., p_n; beta) = d_(J_{p_1}) ... d_(J_{p_n}) W_L[J; beta] |_(J=0)`.

Because `beta` enters as one common source on every plaquette, one has the
exact operator identity

`d/d beta = sum_r d/d J_r`

on the source-shifted finite Wilson surface. Therefore:

`d/d beta C_n(p_1, ..., p_n; beta) = sum_r C_(n+1)(p_1, ..., p_n, r; beta)`.

In particular,

- `P_L(beta) = C_1(p_0; beta)`,
- `chi_L(beta) = sum_r C_2(p_0, r; beta)`,
- `chi_L'(beta) = sum_(r,s) C_3(p_0, r, s; beta)`.

So explicit nonperturbative closure of `beta_eff(beta)` is equivalent to
closing this exact connected plaquette hierarchy on the accepted `3 spatial +
1 derived-time` surface.

## Theorem 1: uniform-source shift identity

The source-deformed finite Wilson partition function depends on `beta` and the
plaquette sources only through the shifted combination

`y_p = beta + J_p`.

Equivalently,

`W_L[J; beta] = \widetilde{W}_L(y_1, ..., y_(N_plaq))`

with `y_p = beta + J_p`.

Therefore, on the finite Wilson source surface,

`d/d beta = sum_r d/d y_r = sum_r d/d J_r`.

This is an exact finite-volume identity, not a large-volume or perturbative
approximation.

## Corollary 1: exact connected hierarchy

Applying the previous identity after taking `n` source derivatives gives

`d/d beta C_n(p_1, ..., p_n; beta) = sum_r C_(n+1)(p_1, ..., p_n, r; beta)`.

This is the exact BBGKY-style hierarchy for connected plaquette cumulants on
the finite periodic Wilson evaluation surface.

The first two levels are:

- `P_L(beta) = C_1(p_0; beta)`,
- `chi_L(beta) = dP_L/d beta = sum_r C_2(p_0, r; beta)`,
- `chi_L'(beta) = sum_(r,s) C_3(p_0, r, s; beta)`.

So the exact susceptibility flow theorem is already one collapsed projection of
this hierarchy.

## Corollary 2: exact transport hierarchy for `beta_eff`

From the exact susceptibility-flow theorem,

`beta_eff'(beta) = chi_L(beta) / chi_1plaq(beta_eff(beta))`.

Differentiating once more and substituting the hierarchy gives

`beta_eff''(beta) = [sum_(r,s) C_3(p_0, r, s; beta)] / chi_1plaq(beta_eff(beta))
                    - [chi_1plaq'(beta_eff(beta)) / chi_1plaq(beta_eff(beta))]
                      * (beta_eff'(beta))^2`.

So:

- explicit closure of `beta_eff'` needs the shell-summed two-point connected
  field,
- explicit closure of `beta_eff''` already needs the shell-summed three-point
  connected field,
- and higher derivatives require the full connected hierarchy.

This is the exact sense in which the remaining gap is a hierarchy closure
problem, not a missing constant or a missing local bridge factor.

## Corollary 3: exact onset hierarchy data

The previously closed onset theorems give

`P_L(beta) - P_1plaq(beta) = beta^5 / 472392 + O(beta^6)`,

hence

`chi_L(beta) - chi_1plaq(beta) = 5 beta^4 / 472392 + O(beta^5)`,

and

`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)`,

so

`beta_eff'(beta) = 1 + 5 beta^4 / 26244 + O(beta^5)`,

`beta_eff''(beta) = 20 beta^3 / 26244 + O(beta^4)
                  = 5 beta^3 / 6561 + O(beta^4)`.

Using the exact common slope `chi_1plaq(0) = 1/18`, the first summed connected
three-point correction is therefore fixed at onset:

`sum_(r,s) C_3(p_0, r, s; beta)
 = 5 beta^3 / 118098 + O(beta^4)`.

So even the first hierarchy level beyond `chi_L` is now constrained exactly at
small `beta`.

## What this closes

- exact uniform-source derivative identity on the finite Wilson source surface
- exact connected plaquette hierarchy
- exact identification of `chi_L` as the shell-summed connected two-point
  plaquette field
- exact identification of `beta_eff''` as depending on the shell-summed
  connected three-point field
- exact first onset coefficient for the hierarchy beyond `chi_L`

## What this does not close

- an explicit closed form for the full connected two-point plaquette field at
  `beta = 6`
- an explicit closed form for the shell-summed connected three-point field
- explicit nonperturbative closure of the hierarchy
- analytic closure of `P(6)`

## Support consequence for the live package

The live package can now say:

- reduction-law existence is exact,
- reduction-law transport is exact,
- the missing object is exactly the connected plaquette hierarchy,
- not a guessed bridge factor and not a missing local normalization.

That is the right rigorous endpoint for the current plaquette lane.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=4 FAIL=0`
