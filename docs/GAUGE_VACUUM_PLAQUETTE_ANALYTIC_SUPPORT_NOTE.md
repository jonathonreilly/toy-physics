# Gauge-Vacuum Plaquette Analytic Support Note

**Date:** 2026-04-16
**Status:** exact subtools plus bridge-conditioned analytic candidate
**Scripts:** `scripts/frontier_gauge_vacuum_plaquette_analytic_support.py`, `scripts/frontier_scalar_3plus1_temporal_ratio.py`

## Question

Do we now have enough to replace the canonical same-surface plaquette value

`<P>(beta = 6) = 0.5934`

with a fully promoted analytic theorem?

## Answer

Not yet.

What is now closed exactly is:

1. the local `SU(3)` one-plaquette block
2. the scalar `3+1` bridge endpoint ratio `A_inf / A_2 = 2 / sqrt(3)`
3. the exact `3+1` plaquette/link incidence factor `6 / 4 = 3 / 2`

Combining those exact subtools with the **support-level** dimension-4
scalar-density insertion candidate

`Gamma_sc = (2 / sqrt(3))^(1/4)`

gives the analytic plaquette candidate

`P_cand(6) = 0.593530679977098`.

This sits only `1.3068e-4` (`0.022%`) above the canonical same-surface value
`0.5934`, so it materially strengthens the plaquette lane. But the final
observable-level insertion from the scalar bridge into the physical gauge
vacuum is still not independently closed as a theorem.

So on `main`:

- the analytic candidate is live support
- the canonical plaquette remains the same-surface evaluated value

## Exact subtool 1: local `SU(3)` one-plaquette block

For the one-plaquette Wilson weight

`exp[(beta_loc / 3) Re Tr U]`,

the exact local partition function is

`Z_1plaq(beta_loc) = sum_(m in Z) det[I_(m+i-j)(beta_loc/3)]_(i,j=0..2)`,

and the exact local plaquette expectation is

`P_1plaq(beta_loc) = d/d(beta_loc) log Z_1plaq(beta_loc)`.

The runner checks this against:

- finite-difference differentiation of `log Z_1plaq`
- independent Weyl-angle integration

At bare `beta = 6`:

`P_1plaq(6) = 0.422531739649983`.

## Exact subtool 2: scalar `3+1` temporal ratio

The exact scalar bridge theorem is:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`
- `A_inf / A_2 = 2 / sqrt(3)`

Authority:

- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

The fourth-root factor

`Gamma_sc = (2 / sqrt(3))^(1/4)`

is carried here only as the dimension-4 scalar-density insertion candidate.

## Exact subtool 3: exact `3+1` incidence factor

On the hypercubic `3+1` lattice:

- each link lies in `3` coordinate planes
- each plane contributes `2` plaquettes touching that link

So each link lies in exactly `6` plaquettes, while each plaquette contains `4`
links. Therefore the exact plaquette-centered incidence factor is

`Gamma_coord = 6 / 4 = 3 / 2`.

## Combined analytic support candidate

Using the support-level dimension-4 scalar-density insertion candidate:

`beta_eff,cand = beta * Gamma_coord * Gamma_sc`
`= beta * (3/2) * (2 / sqrt(3))^(1/4)`.

At `beta = 6`:

- `beta_eff,cand = 9.329531846652698`
- `P_cand(6) = P_1plaq(beta_eff,cand) = 0.593530679977098`
- `u_0,cand = P_cand^(1/4) = 0.877729698485538`

The local block remains internally exact at `beta_eff,cand`; the runner again
checks Bessel-determinant and Weyl-angle agreement there.

## Honest boundary

This note does **not** claim:

- full analytic plaquette closure
- replacement of the canonical same-surface plaquette value on `main`

The remaining missing theorem is the final local-to-vacuum insertion:

> why the physical gauge-vacuum plaquette must inherit this scalar bridge as
> its unique observable-level completion.

Until that is closed independently, the correct live status is:

- exact subtools
- bridge-conditioned analytic candidate
- canonical plaquette still same-surface evaluated

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
python3 scripts/frontier_gauge_vacuum_plaquette_analytic_support.py
```

Expected summary:

- scalar ratio runner: `EXACT PASS=4 FAIL=0`, `SUPPORT=1`
- plaquette support runner: `EXACT PASS=4 FAIL=0`, `SUPPORT=3`
