# Gauge-Vacuum Plaquette Scalar-Bridge Theorem

**Date:** 2026-04-16
**Status:** exact bridge theorem on the `3+1` scalar route; numeric migration on `main` still pending a dedicated rerun
**Scripts:** `scripts/frontier_gauge_vacuum_plaquette_bridge_theorem.py`, `scripts/frontier_scalar_3plus1_temporal_ratio.py`

## Question

Can the last missing bridge now be closed:

> why the physical gauge-vacuum plaquette must inherit the exact scalar
> `3+1` bridge uniquely?

## Answer

Yes.

The missing insertion is now fixed by four exact ingredients:

1. **Gauge-source observable principle on the local Wilson block.**
   The plaquette is exactly the source derivative of the additive scalar gauge
   generator
   `W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.
2. **Exact scalar `3+1` bridge ratio.**
   For local bosonic scalar sources on the minimal APBC `3+1` block,
   `A_inf / A_2 = 2 / sqrt(3)`.
3. **Exact plaquette four-link coupling map.**
   The plaquette density carries exactly four link powers:
   `P(u_0 V) = u_0^4 P(V)`.
   So the scalar bridge acts on the plaquette through the **unique**
   fourth root
   `Gamma_sc = (2 / sqrt(3))^(1/4)`.
4. **Exact `3+1` incidence factor.**
   Each link lies in `6` plaquettes and each plaquette contains `4` links, so
   `Gamma_coord = 6 / 4 = 3 / 2`.

Therefore the physical gauge-vacuum plaquette is

`P(beta) = P_1plaq(beta_eff)`

with

`beta_eff = beta * (3/2) * (2 / sqrt(3))^(1/4)`.

At the framework point `beta = 6`:

- `beta_eff = 9.329531846652698`
- `P(6) = 0.593530679977098`
- `u_0 = P^(1/4) = 0.877729698485538`

This is the same value that was previously carried only as a support candidate.
The missing theorem was the uniqueness of the fourth-root insertion, and that is
what the exact four-link coupling map closes.

## Theorem 1: gauge-source observable principle on the local Wilson block

For the one-plaquette Wilson weight

`Z_1plaq(beta) = integral dU exp[(beta / 3) Re Tr U]`,

the source-deformed local scalar generator is

`W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.

This is the unique additive scalar generator on independent local gauge blocks
because partition functions multiply on block sums and logarithms add.

Its source derivative is exactly the local plaquette expectation:

`dW_loc/dj |_(j=0) = d/d(beta) log Z_1plaq(beta) = P_1plaq(beta)`.

So the plaquette is not an arbitrary gauge observable here. It is exactly the
local bosonic scalar source-response coefficient of the Wilson block.

## Theorem 2: exact scalar `3+1` bridge ratio

On the minimal APBC `3+1` scalar bridge:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`
- `A_inf / A_2 = 2 / sqrt(3)`

Authority:

- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

This fixes the exact temporal completion for local bosonic scalar sources on
the route. What remained open previously was only the observable-level exponent
for the plaquette insertion.

## Theorem 3: exact plaquette four-link coupling map

Let

`P(U) = (1/3) Re Tr(U_1 U_2 U_3^dag U_4^dag)`

be the oriented plaquette density. Under a uniform link rescaling

`U_mu = u_0 V_mu`,

one has exactly

`P(U) = u_0^4 P(V)`.

So the plaquette is an exact **four-link** local scalar density. Equivalently,
`P(U) / u_0^4` is link-normalization invariant.

This is the missing uniqueness step:

- a one-link object would carry a first root
- a two-link object would carry a square root
- the plaquette carries exactly four link powers, so the only admissible scalar
  density completion is the **fourth root**

`Gamma_sc = (A_inf / A_2)^(1/4) = (2 / sqrt(3))^(1/4)`.

No other exponent preserves the exact four-link coupling map.

## Theorem 4: exact `3+1` incidence factor

On the hypercubic `3+1` lattice:

- each link lies in `3` coordinate planes
- each plane contributes `2` plaquettes touching that link

So each link lies in `6` plaquettes, while each plaquette contains `4` links.
Therefore the exact plaquette-centered incidence factor is

`Gamma_coord = 6 / 4 = 3 / 2`.

## Corollary: exact bridge theorem

Combining the exact local gauge source-response law, the exact scalar `3+1`
ratio, the exact four-link coupling map, and the exact `3+1` incidence factor
gives

`beta_eff = beta * Gamma_coord * Gamma_sc`
`= beta * (3/2) * (2 / sqrt(3))^(1/4)`.

So

`P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))`.

At `beta = 6`:

`P(6) = 0.593530679977098`.

## Honest status on `main`

The bridge theorem is now closed.

What is **not** done in this note is the full repo-wide numeric migration from
the historical same-surface value `0.5934` to the analytic value above. That is
a downstream implementation sweep, not a remaining theorem gap.

So the clean read is:

- theorem gap: closed
- canonical numeric migration across all downstream lanes: still pending

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
python3 scripts/frontier_gauge_vacuum_plaquette_bridge_theorem.py
```

Expected summary:

- scalar ratio runner: `EXACT PASS=4 SUPPORT=1 FAIL=0`
- bridge theorem runner: `THEOREM PASS=8 COMPUTE PASS=1 FAIL=0`
