# Gauge-Vacuum Plaquette Infinite-Hierarchy Obstruction

**Date:** 2026-04-16
**Status:** support - exact obstruction theorem on the finite Wilson source surface; explicit connected-hierarchy closure at `beta = 6` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py`

## Question

After identifying the remaining gap as the explicit connected plaquette
hierarchy, can that hierarchy close exactly at some finite order?

## Answer

No.

On both the local one-plaquette block and the full finite Wilson source
surface, the diagonal source generator is exactly nonpolynomial. Therefore the
connected hierarchy cannot truncate at any finite order.

This does not close analytic `P(6)`, but it sharpens the remaining gap:

> explicit plaquette closure requires either
> - an exact nonpolynomial solution of the full connected hierarchy, or
> - some new exact generating object equivalent to that hierarchy.

It cannot come from an exact finite-order truncation.

## Setup

For the finite Wilson source surface define the diagonal generator

`K_L(t) = W_L[t 1; 0] = log Z_L(t) - log Z_L(0)`

where `1` is the uniform plaquette-source vector. Then

`K_L'(t) = N_plaq P_L(t)`.

Similarly for the one-plaquette block,

`K_1(t) = log Z_1plaq(t) - log Z_1plaq(0)`,

so

`K_1'(t) = P_1plaq(t)`.

The exact connected hierarchy on the diagonal source surface is encoded in the
Taylor coefficients of these generators.

If the diagonal hierarchy truncated exactly at order `N`, then `K(t)` would be
a polynomial of degree at most `N`.

## Theorem 1: polynomial truncation is impossible for the local one-plaquette block

The local exact plaquette satisfies:

- `P_1plaq(0) = 0`,
- `0 <= P_1plaq(t) < 1` for finite `t`,
- `P_1plaq(t) -> 1` as `t -> infinity`.

Suppose the local diagonal hierarchy truncated at finite order. Then
`K_1(t)` would be a polynomial, so `P_1plaq(t) = K_1'(t)` would also be a
polynomial.

But any polynomial with a finite limit as `t -> infinity` is constant.
Therefore `P_1plaq(t)` would have to be constant.

That contradicts `P_1plaq(0)=0` and `lim_(t->infinity) P_1plaq(t)=1`.

So:

> the local one-plaquette connected hierarchy does not truncate at any finite
> order.

## Theorem 2: polynomial truncation is impossible for the finite Wilson surface

On every finite periodic Wilson `L^4` surface,

- `P_L(0) = 0`,
- `0 <= P_L(t) < 1` for finite `t`,
- `P_L(t) -> 1` as `t -> infinity` by compact Laplace concentration on the
  maximum-action gauge orbit.

If the full diagonal connected hierarchy truncated at finite order, then
`K_L(t)` would be a polynomial and therefore `P_L(t) = K_L'(t)/N_plaq` would
also be a polynomial.

Again, any polynomial with a finite limit at infinity is constant. So `P_L`
would have to be constant, contradicting `P_L(0)=0` and `lim_(t->infinity)
P_L(t)=1`.

Therefore:

> the finite Wilson diagonal connected plaquette hierarchy does not truncate at
> any finite order.

## Corollary: what remains open

The remaining analytic gap is not a missing finite set of coefficients.

It is the explicit closure of an inherently infinite connected hierarchy on the
accepted `3 spatial + 1 derived-time` Wilson source surface.

This rules out one tempting hope:

> analytic plaquette closure cannot come from an exact finite-order connected
> cumulant truncation.

It must come from either:

- an exact nonpolynomial solution of the hierarchy, or
- a new exact generating representation equivalent to it.

## What this closes

- exact obstruction to finite-order diagonal connected-hierarchy truncation
- exact obstruction to finite-order polynomial closure of the diagonal source
  generator
- sharper identification of the remaining plaquette gap

## What this does not close

- an explicit nonpolynomial solution of the connected hierarchy
- an explicit closed form for `chi_L(beta)`
- analytic closure of `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

The conditional verdict flagged the asserted endpoint/asymptotic Wilson-surface premises (`P_L(0) = 0`, `lim_(t -> infinity) P_L(t) = 1` by compact Laplace concentration on the maximum-action gauge orbit). The compact-Laplace concentration argument (and the `P_1plaq(beta) -> 1` endpoint) is established in:

- [gauge_vacuum_plaquette_reduction_existence_theorem_note](GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md) — currently `audited_conditional`; the retained-status of this row is therefore **blocked on** that upstream conditional. The local algebra of this note (finite Taylor support implies polynomial `K(t)`) is unchanged by that uplink.
- `GAUGE_VACUUM_PLAQUETTE_HIERARCHY_OBSTRUCTION_LEMMAS_BOUNDED_NOTE_2026-05-10.md` (reader pointer; see-also cross-reference, not a load-bearing dependency of this note's local algebra) — companion bounded note added 2026-05-10 supplying the four analytic premises flagged by the 2026-05-02 audit verdict (one-plaquette endpoints `P_1plaq(0) = 0`, `P_1plaq(t) → 1`; finite-periodic Wilson endpoints `P_L(0) = 0`, `P_L(t) → 1`; finite Taylor support ⟺ polynomial `K(t)` globally on `R`; global-vs-formal convention check). The four lemmas are proved from textbook compact-Lie-group analysis admissions (Haar orthogonality, compact Laplace concentration, entire partition representation, analytic continuation of finite-support Taylor series) listed there as bounded admissions `(BA-1)–(BA-4)`. This companion is itself `bounded_theorem` and will be audited on its own row; the local algebra of this note is unchanged by registering it.
