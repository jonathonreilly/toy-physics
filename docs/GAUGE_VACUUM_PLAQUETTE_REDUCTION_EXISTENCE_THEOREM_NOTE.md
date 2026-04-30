# Gauge-Vacuum Plaquette Reduction Existence and Uniqueness Theorem

**Date:** 2026-04-16
**Status:** support - exact implicit reduction-law theorem on the finite Wilson evaluation surface; explicit nonperturbative closed form still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py`

## Question

After closing the first nonlinear onset coefficient, can we derive something
stronger than a guessed reduction ansatz without already solving the full
nonperturbative plaquette at `beta = 6`?

## Answer

Yes.

On every finite periodic Wilson `L^4` evaluation surface, there is an exact
unique implicit reduction law

`P_L(beta) = P_1plaq(beta_eff,L(beta))`

with

- `beta_eff,L(0) = 0`,
- `beta_eff,L'(0) = 1`,
- `beta_eff,L(beta) = beta + beta^5 / 26244 + O(beta^6)`.

This is a real derivation step. It removes the question of whether a reduction
law exists at all. The remaining gap is narrower:

> derive an explicit nonperturbative characterization of `beta_eff(beta)` at
> the framework point `beta = 6`.

## Theorem 1: the local one-plaquette map is analytic and strictly increasing

Define

`P_1plaq(beta) = d/d beta log Z_1plaq(beta)`

with

`Z_1plaq(beta) = integral dU exp[(beta/3) Re Tr U]`.

Because the integration domain is compact and the integrand is entire in
`beta`, `Z_1plaq(beta)` and `P_1plaq(beta)` are analytic for real `beta`.

Differentiating once more gives

`P_1plaq'(beta) = Var_beta(X)`

for

`X(U) = (1/3) Re Tr U`.

The measure density `exp(beta X)` is strictly positive for every finite `beta`,
while `X` is not constant on `SU(3)`:

- `X(I) = 1`,
- `X(e^{2 pi i / 3} I) = -1/2`.

So `Var_beta(X) > 0` and therefore:

> `P_1plaq(beta)` is strictly increasing on `beta >= 0`.

Also:

- `P_1plaq(0) = 0` by Haar symmetry,
- `P_1plaq(beta) < 1` for finite `beta`,
- `P_1plaq(beta) -> 1` as `beta -> infinity` by compact Laplace concentration
  at the identity manifold.

Hence `P_1plaq` is a bijection from `[0, infinity)` onto `[0, 1)`.

## Theorem 2: the finite Wilson plaquette map is analytic and strictly increasing

On a finite periodic symmetric Wilson `L^4` surface, define

`P_L(beta) = (1 / N_plaq) d/d beta log Z_L(beta)`

with

`Z_L(beta) = integral DU exp[(beta/3) sum_p Re Tr U_p]`.

Again, compactness gives analyticity in `beta`.

Differentiating gives

`P_L'(beta) = (1 / N_plaq) Var_beta(S_L)`

where

`S_L = sum_p (1/3) Re Tr U_p`.

The finite-volume Wilson density is strictly positive for finite `beta`, and
`S_L` is not constant on configuration space: the identity link field has
plaquette average `1`, while an explicit one-link deformed field has smaller
average plaquette. Therefore `Var_beta(S_L) > 0`.

So:

> `P_L(beta)` is strictly increasing on `beta >= 0`.

Also:

- `P_L(0) = 0`,
- `0 <= P_L(beta) < 1` for finite `beta`.

## Corollary 1: exact unique implicit reduction law

Since `P_1plaq` is a bijection `[0,infinity) -> [0,1)` and `P_L(beta)` lies in
`[0,1)` for every finite `beta`, the quantity

`beta_eff,L(beta) := P_1plaq^{-1}(P_L(beta))`

is well-defined and unique.

This is not a fit ansatz. It is an exact implicit reduction law on the finite
Wilson evaluation surface.

Because `P_1plaq' > 0`, the inverse function theorem gives:

> `beta_eff,L(beta)` is analytic wherever `P_L(beta)` is analytic.

And because both numerator and denominator are positive:

`beta_eff,L'(beta) = P_L'(beta) / P_1plaq'(beta_eff,L(beta)) > 0`.

So the exact implicit reduction law is itself strictly increasing.

## Corollary 2: exact onset data

The strong-coupling slope theorem gives

`P_L'(0) = P_1plaq'(0) = 1/18`.

So

`beta_eff,L'(0) = 1`.

The mixed-cumulant audit already proved the first nonlinear coefficient:

`beta_eff,L(beta) = beta + beta^5 / 26244 + O(beta^6)`.

Thus the onset of the exact implicit reduction law is now completely fixed.

## What this closes

- exact existence of the reduction law on the finite Wilson evaluation surface
- exact uniqueness of that reduction law
- exact analyticity / monotonicity of the implicit reduction map
- exact onset data through the first nonlinear coefficient

## What this does not close

- an explicit closed form for `beta_eff(beta)`
- a theorem-grade nonperturbative characterization at `beta = 6`
- repo-wide repinning of the canonical plaquette value

So the remaining open question is no longer:

> does an exact reduction law exist?

It is now the narrower question:

> can we close the explicit nonperturbative reduction law at the framework
> point?

## Support consequence for the live package

Applying the exact implicit inverse to the canonical same-surface plaquette
value gives the unique implicit reduction parameter

`beta_eff^can = P_1plaq^{-1}(0.5934) = 9.326167920875534`.

This sits very close to the older constant-lift support candidate

`9.329531846652698`,

but that closeness is now only a support fact. The theorem-grade content is the
existence and uniqueness of the implicit reduction law, not the old closed-form
guess.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=4 FAIL=0`
