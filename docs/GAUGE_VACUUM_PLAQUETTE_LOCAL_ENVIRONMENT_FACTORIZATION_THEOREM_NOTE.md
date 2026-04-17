# Gauge-Vacuum Plaquette Local / Environment Factorization Theorem

**Date:** 2026-04-17
**Status:** exact source-sector sharpening theorem on the accepted Wilson `3 spatial + 1 derived-time` source surface; the remaining open object is the residual environment-response sequence after the exact local Wilson marked-link factor is removed
**Script:** `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py`

## Question

After the exact source-sector factorization

`T_src(6) = exp(3 J) D_6 exp(3 J)`,

is the whole diagonal coefficient sequence `D_6` still equally open, or can any
part of it now be identified exactly?

## Answer

Yes. One exact part can now be identified.

In temporal gauge, the mixed one-step Wilson kernel factorizes exactly over the
spatial links. On the marked plaquette, the four links of the plaquette loop
therefore contribute one exact local Wilson convolution factor each.

That local link contribution is explicit in the `SU(3)` character basis:

`a_(p,q)(beta) = c_(p,q)(beta) / (d_(p,q) c_(0,0)(beta))`,

with:

- `d_(p,q) = (p+1)(q+1)(p+q+2)/2`,
- `c_(p,q)(beta)` the exact Wilson class-function coefficient
  `sum_n det[I_(n + lambda_j + i - j)(beta/3)]`,
- `lambda = (p+q, q, 0)`.

Because the marked plaquette loop contains exactly four links, the exact local
marked-link contribution on the plaquette character sector is

`D_beta^loc chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

Therefore the full source-sector diagonal coefficient sequence factors as

`kappa_(p,q)(beta) = a_(p,q)(beta)^4 epsilon_(p,q)(beta)`,

with `epsilon_(p,q)(beta) >= 0` the residual environment-response sequence.

So the exact remaining constructive target is no longer the whole `D_6`. It is
the residual environment sequence

`E_6 chi_(p,q) = epsilon_(p,q)(6) chi_(p,q)`.

That is the sharpened open object.

## Setup

From the exact transfer-operator / source-sector factorization stack already on
`main`:

- the finite Wilson source surface admits one exact one-clock transfer
  operator,
- the local plaquette source is the explicit class-function operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`,
- the `beta = 6` source-sector transfer law factorizes as
  `T_src(6) = exp(3 J) D_6 exp(3 J)`,
- and `D_6` is a positive conjugation-symmetric diagonal operator in the
  `SU(3)` character basis.

What remained open was the constructive identification of that diagonal
sequence.

## Theorem 1: exact one-link Wilson convolution coefficients

Fix one spatial link on one mixed plaquette in temporal gauge. Its mixed
Wilson weight is the central class function

`w_beta(g) = exp[(beta / 3) Re Tr g]`.

By the `SU(3)` character expansion of the Wilson class function,

`w_beta(g) = sum_(p,q) d_(p,q) a_(p,q)(beta) chi_(p,q)(g)`,

with explicit coefficients

`a_(p,q)(beta) = c_(p,q)(beta) / (d_(p,q) c_(0,0)(beta))`,

and

`c_(p,q)(beta)
 = sum_(n in Z) det[I_(n + lambda_j + i - j)(beta/3)]_(i,j=1)^3`,

for `lambda = (p+q, q, 0)`.

Therefore convolution by `w_beta` acts on each irreducible matrix coefficient
of type `(p,q)` by the exact scalar `a_(p,q)(beta)`.

## Theorem 2: exact four-link marked-plaquette local factor

On the accepted Wilson `3+1` surface, the marked plaquette loop contains
exactly four spatial links.

After temporal gauge fixing on one clock step, the mixed kernel factorizes
exactly over the spatial links. So on the plaquette character
`chi_(p,q)(U_1 U_2 U_3^dag U_4^dag)`, the four marked link convolutions act
independently and each contributes the same scalar `a_(p,q)(beta)`.

Hence the exact local marked-link factor on the plaquette character sector is

`D_beta^loc chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

This is exact and no longer open.

## Corollary 1: exact local / environment factorization of the mixed-kernel coefficients

Split the mixed one-step kernel into:

- the four marked link factors,
- the remaining environment factors.

These pieces commute before source-sector compression because they act on
disjoint link sets. On the marked plaquette character sector, the first piece is
already the scalar `a_(p,q)(beta)^4`.

So the full diagonal mixed-kernel coefficients must factor as

`kappa_(p,q)(beta) = a_(p,q)(beta)^4 epsilon_(p,q)(beta)`,

with `epsilon_(p,q)(beta) >= 0` and
`epsilon_(p,q)(beta) = epsilon_(q,p)(beta)`.

Equivalently,

`D_beta = D_beta^loc E_beta`,

with:

- `D_beta^loc chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`,
- `E_beta chi_(p,q) = epsilon_(p,q)(beta) chi_(p,q)`.

## Corollary 2: sharpened remaining gap

The constructive plaquette gap is therefore narrower than it was in the older
`D_6` phrasing.

What is still open is not:

- the exact local Wilson marked-link contribution,
- nor the exact source-sector factorization law itself.

What remains open is:

> the exact residual environment-response sequence `epsilon_(p,q)(6)`,
> equivalently the Perron state of
> `exp(3 J) D_6^loc E_6 exp(3 J)` after the exact local Wilson factor
> `D_6^loc` is stripped off.

## What this closes

- exact temporal-gauge reduction of the mixed kernel to one-link Wilson
  convolution factors on the marked plaquette
- exact `SU(3)` character coefficients of the one-link Wilson class function
- exact four-link local marked-plaquette factor `a_(p,q)(beta)^4`
- exact narrowing of the remaining open source-sector datum from the whole
  `D_6` sequence to the residual environment-response sequence `E_6`

## What this does not close

- explicit values of `epsilon_(p,q)(6)`
- explicit `beta = 6` Perron moments after the environment factor is included
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`
