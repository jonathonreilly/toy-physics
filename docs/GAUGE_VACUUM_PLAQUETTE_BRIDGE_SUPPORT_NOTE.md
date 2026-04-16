# Gauge-Vacuum Plaquette Scalar-Bridge Support

**Date:** 2026-04-16
**Status:** exact local/source/coupling support stack; the final physical-vacuum insertion remains support-level
**Scripts:** `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py`, `scripts/frontier_scalar_3plus1_temporal_ratio.py`

## Question

How much of the plaquette bridge is actually closed on `main`, and what still
prevents a full analytic promotion of the physical gauge-vacuum plaquette?

## Answer

The bridge is materially stronger, but not fully closed.

What is exact now:

1. **Local Wilson source-response on the one-plaquette block.**
   The one-plaquette expectation is exactly the source derivative of the local
   Wilson scalar generator
   `W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.
2. **Exact scalar `3+1` bridge ratio.**
   On the minimal APBC `3+1` scalar bridge,
   `A_inf / A_2 = 2 / sqrt(3)`.
3. **Exact plaquette four-link coupling map.**
   Under a uniform link rescaling one has the exact algebraic identity
   `P(u_0 V) = u_0^4 P(V)`.
4. **Exact `3+1` incidence factor.**
   On the hypercubic `3+1` lattice, `Gamma_coord = 6 / 4 = 3 / 2`.

What is **not** closed by those facts alone is the final physical statement

`P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))`

for the interacting gauge vacuum. That last observable-level insertion is still
a sharp support candidate rather than a theorem-grade derivation.

## Exact support piece 1: local Wilson source-response

For the one-plaquette Wilson weight

`Z_1plaq(beta) = integral dU exp[(beta / 3) Re Tr U]`,

the source-deformed local scalar generator is

`W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.

Its source derivative is exactly the local plaquette expectation:

`dW_loc/dj |_(j=0) = d/d(beta) log Z_1plaq(beta) = P_1plaq(beta)`.

So the plaquette is exactly the local bosonic scalar source-response
coefficient of the Wilson block.

## Exact support piece 2: scalar `3+1` bridge ratio

On the minimal APBC `3+1` scalar bridge:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`
- `A_inf / A_2 = 2 / sqrt(3)`

Authority:

- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

This closes the exact scalar bridge ratio. It does **not** by itself decide how
that ratio must lift a specific interacting gauge observable.

## Exact support piece 3: plaquette four-link coupling map

Let

`P(U) = (1/3) Re Tr(U_1 U_2 U_3^dag U_4^dag)`

be the oriented plaquette density. Under a uniform link rescaling

`U_mu = u_0 V_mu`,

one has exactly

`P(U) = u_0^4 P(V)`.

So the plaquette is an exact **four-link** local scalar density. This fixes the
natural scalar-density exponent to the fourth root on any route that already
proves the bridge acts through a uniform scalar-density normalization.

That is strong support. It is not yet a proof that the interacting gauge vacuum
must inherit the scalar bridge in exactly that way.

## Exact support piece 4: `3+1` incidence factor

On the hypercubic `3+1` lattice:

- each link lies in `3` coordinate planes
- each plane contributes `2` plaquettes touching that link

So each link lies in `6` plaquettes, while each plaquette contains `4` links.
Therefore

`Gamma_coord = 6 / 4 = 3 / 2`.

Again, this is exact combinatorics. What remains open is the unique insertion
law taking this factor into the full interacting plaquette expectation.

## Current best analytic candidate

If one composes the exact local/source/coupling pieces above, the sharp current
analytic candidate is

`beta_eff = beta * (3/2) * (2 / sqrt(3))^(1/4)`

and therefore

`P_cand(beta) = P_1plaq(beta_eff)`.

At the framework point `beta = 6`:

- `beta_eff = 9.329531846652698`
- `P_cand(6) = 0.593530679977098`
- `u_0,cand = P_cand^(1/4) = 0.877729698485538`

This sits only `1.3068e-4` (`0.022%`) above the current canonical same-surface
value `0.5934`, so it is a very strong support candidate.

## Remaining gap

The remaining theorem-grade gap is:

> why the physical interacting gauge-vacuum plaquette must inherit the scalar
> bridge with that specific observable-level insertion law, rather than merely
> being sharply supported by it.

Until that step is closed, the live package should keep the plaquette as:

- exact local/source/coupling support stack plus
- canonical same-surface evaluated value on the live quantitative surface

## Honest status on `main`

Current clean read:

- exact local/source/coupling ingredients: closed
- physical-vacuum bridge insertion: support-level
- canonical plaquette on the live package: still `0.5934`

So there is **not** yet a basis for repo-wide numeric migration or for removing
the residual “same-surface evaluated” language from downstream quantitative
lanes.

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
python3 scripts/frontier_gauge_vacuum_plaquette_bridge_support.py
```

Expected summary:

- scalar ratio runner: `EXACT PASS=4 SUPPORT=1 FAIL=0`
- bridge support runner: `EXACT PASS=6 SUPPORT=2 FAIL=0`
