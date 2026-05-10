# Gauge-Vacuum Plaquette Local / Environment Factorization Theorem

**Date:** 2026-04-17 (scope-tightening re-frame: 2026-05-02)
**Type:** bounded_theorem
**Claim scope:** mixed-kernel locality factorization on the marked-plaquette
character sector at the accepted Wilson `3+1` source surface; explicitly
*out of scope*: residual source-sector environment data, framework-point
Perron state at `beta = 6`, and analytic closure of `P(6)`.
**Bounded scope (what this note proves):** after trivial-channel
normalization the mixed-kernel source-sector action on the marked
plaquette character sector is exactly the local Wilson marked-link factor
`a_(p,q)(beta)^4`. Equivalently, the normalized mixed-kernel compression
contributes no further representation-dependent environment sequence
beyond that local factor.
**Bounded scope (what this note explicitly does not prove):** the
residual source-sector environment operator outside the normalized mixed
kernel; the framework-point Perron state of the full source-sector
transfer law; explicit `beta = 6` Perron moments; analytic closure of
canonical `P(6)`. Those objects are tracked in named companion notes
(`gauge_vacuum_plaquette_residual_environment_identification_theorem_note`,
`gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note`,
`gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`)
and remain open-grade independently of the bounded-theorem statement here.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py`

## Question

After the exact source-sector factorization

`T_src(6) = exp(3 J) D_6 exp(3 J)`,

does the residual diagonal source-sector datum really remain open already inside
the normalized mixed-kernel part, or does the mixed kernel localize more
strongly than that?

## Answer

It localizes more strongly.

In temporal gauge, the one-step Wilson mixed kernel factorizes exactly over the
spatial links. On the marked plaquette source sector:

- each of the four marked links contributes one explicit normalized Wilson
  convolution eigenvalue `a_(p,q)(beta)`,
- every non-marked mixed-link factor acts only through the trivial irrep on the
  marked plaquette class-function sector and therefore contributes a
  rep-independent scalar.

So after dividing out the trivial-channel scalar, the normalized mixed-kernel
compression is exactly

`D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

That means the mixed kernel itself contributes no further nonlocal
representation-dependent environment sequence.

The still-open object is therefore narrower and cleaner than the previous
mixed-kernel phrasing suggested:

> the remaining framework-point ambiguity is residual source-sector environment
> data beyond the normalized mixed kernel, not hidden mixed-kernel coefficient
> freedom on top of the exact local Wilson marked-link factor.

## Setup

From the exact transfer-operator / source-sector factorization stack already on
`main`:

- the finite Wilson source surface admits one exact one-clock transfer
  operator,
- the local plaquette source is the explicit class-function operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`,
- the `beta = 6` source-sector transfer law factors through the exact marked
  half-slice multiplier `exp(3 J)` and one residual positive diagonal
  source-sector operator,
- and the mixed one-step Wilson kernel factorizes exactly over spatial links in
  temporal gauge.

The question is whether that mixed-kernel part already contains residual
representation-dependent environment freedom after the exact local marked-link
factor is stripped off.

## Theorem 1: exact one-link Wilson convolution coefficients

Fix one spatial link on one mixed plaquette in temporal gauge. Its mixed Wilson
weight is the central class function

`w_beta(g) = exp[(beta / 3) Re Tr g]`.

By the `SU(3)` character expansion of the Wilson class function,

`w_beta(g) = c_(0,0)(beta) sum_(p,q) d_(p,q) a_(p,q)(beta) chi_(p,q)(g)`,

with:

- `a_(0,0)(beta) = 1`,
- `d_(p,q) = (p+1)(q+1)(p+q+2)/2`,
- `a_(p,q)(beta) = c_(p,q)(beta) / (d_(p,q) c_(0,0)(beta))`,
- `c_(p,q)(beta)
   = sum_(n in Z) det[I_(n + lambda_j + i - j)(beta/3)]_(i,j=1)^3`,
- `lambda = (p+q, q, 0)`.

Therefore normalized one-link Wilson convolution acts on each irreducible
matrix coefficient of type `(p,q)` by the exact scalar `a_(p,q)(beta)`.

## Theorem 2: non-marked mixed-link factors are scalar on the marked source sector

Let `f(W)` be any class function of the marked plaquette holonomy `W`.

If a mixed-kernel link factor acts on a spatial link not belonging to the
marked plaquette loop, then `f(W)` is independent of that link variable.

So normalized convolution by that non-marked link factor acts by

`C_ell^norm f = f`,

because only the trivial irrep is seen on that link and `a_(0,0)(beta) = 1`.

Equivalently, before trivial-channel normalization each non-marked mixed-link
factor contributes the same scalar `c_(0,0)(beta)` independently of `(p,q)`.

Therefore all non-marked mixed-link factors collapse to one rep-independent
scalar on the marked plaquette source sector.

## Theorem 3: the normalized mixed-kernel compression is exactly local

On the accepted Wilson `3+1` source surface, the marked plaquette loop contains
exactly four spatial links.

Each marked-link factor contributes the normalized irrep eigenvalue
`a_(p,q)(beta)`, while every non-marked mixed-link factor contributes only a
rep-independent scalar.

Hence after trivial-channel normalization the full mixed-kernel compression on
the marked plaquette character sector is exactly

`D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

So there is no remaining nonlocal representation-dependent mixed-kernel freedom
after the exact local Wilson marked-link factor is stripped off.

## Corollary 1: the remaining open object is not mixed-kernel coefficient freedom

The constructive plaquette gap is therefore sharper than the previous
source-sector phrasing suggested.

What is still open is not:

- the normalized mixed-kernel diagonal coefficient sequence,
- nor any hidden mixed-kernel environment sequence on top of
  `a_(p,q)(6)^4`.

What remains open (and is explicitly *outside* this note's bounded
theorem scope) is:

> the residual source-sector environment operator beyond the normalized mixed
> kernel, equivalently the framework-point Perron state of the full exact
> source-sector transfer law after the mixed-kernel local factor has been
> identified.

That residual object is tracked in separate companion notes
(`gauge_vacuum_plaquette_residual_environment_identification_theorem_note`,
`gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note`,
`gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`).
The bounded theorem stated here is independent of any progress on
those successor notes; they consume `a_(p,q)(beta)^4` as a closed
local factor.

## Bounded-theorem scope summary

This note's `claim_type` is `bounded_theorem`:

- *Closed within scope:* normalized Wilson mixed-kernel compression on the
  marked-plaquette character sector factorizes exactly as the four
  marked-link local factor `a_(p,q)(beta)^4`. The chain from the Bessel-
  determinant character coefficients and the trivial-irrep action of
  non-marked links closes algebraically.
- *Not claimed here:* residual source-sector environment data,
  `beta = 6` Perron moments after full environment, framework-point
  closure of `P(6)`, repo-wide repinning of the canonical plaquette.
- *Companion successor notes:* the residual environment object is
  named and tracked separately; nothing in those still-open notes is
  treated as a load-bearing input here, and the bounded factorization
  theorem can be reviewed independently of their disposition.

## What this closes

- exact normalized one-link Wilson convolution coefficients on the mixed kernel
- exact proof that non-marked mixed-link factors act only by a trivial-channel
  scalar on the marked source sector
- exact proof that the normalized mixed-kernel compression is exactly the local
  four-link Wilson factor `a_(p,q)(beta)^4`
- exact relocation of the remaining plaquette gap away from hidden mixed-kernel
  coefficient freedom and into residual source-sector environment data

## What this does not close

- explicit residual source-sector environment data at `beta = 6`
- explicit `beta = 6` Perron moments after the full source-sector environment
  is included
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

The conditional verdict flagged the asserted operator/surface premises (temporal-gauge mixed-kernel factorization over spatial links, accepted Wilson `3+1` source surface). Those premises are already established in:

- [gauge_vacuum_plaquette_transfer_operator_character_recurrence_note](GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md) — establishes the one-clock Wilson transfer operator on the accepted `3 spatial + 1 derived-time` source surface and the `SU(3)` character recurrence on the marked-plaquette class-function sector.
- [gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md) — establishes the marked half-slice multiplier `exp[(beta/2) J]`, the residual source-sector compression `D_beta` on the marked-plaquette class-function sector, and the central-diagonal action that supplies the marked / non-marked compression map invoked here. This upstream is `audited_clean` / `retained_bounded`.
