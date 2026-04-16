# Gauge-Vacuum Plaquette Distinct-Shell Theorem

**Date:** 2026-04-16
**Status:** exact support theorem on the accepted Wilson `3 spatial + 1 derived-time` surface
**Script:** `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py`

## Question

What exact geometric strong-coupling statement can already be proved for the
full interacting plaquette after the naive constant-lift law has been ruled out?

## Answer

The exact distinct-shell statement is:

> On the accepted Wilson `3 spatial + 1 derived-time` surface, the minimal
> distinct connected shell containing a marked plaquette is the six-face
> elementary cube boundary.

Equivalently:

- the first **distinct connected** nonlocal numerator shell uses five action
  plaquettes;
- the first connected vacuum shell uses six action plaquettes.

This is a real reusable theorem, but it is **not** yet a full theorem for the
first nonlinear term of `beta_eff(beta)`, because mixed repeated-plaquette
clusters still need a connected-cumulant audit.

## Theorem 1: the minimal distinct shell around a marked plaquette is the cube boundary

Fix the observed plaquette `p0` in the `(0,1)` plane.

Any **distinct** plaquette sharing the boundary of `p0` shares exactly one of
its four edges. A distinct plaquette cannot share two edges with `p0`; that
would force it to be the same plaquette.

Therefore any distinct shell closing the four marked edges must use at least
four action plaquettes.

The script exhaustively checks all `5^4 = 625` one-per-edge distinct choices on
the accepted local `3+1` patch and finds:

`no four-action shell closes the boundary of p0`.

An explicit five-action shell does close it: the other five faces of an
elementary cube containing `p0`.

So the minimal distinct connected shell containing a marked plaquette has total
size `6`, i.e. one observed face plus five action faces.

## Corollary 1: the first distinct connected numerator shell is order `beta^5`

In the plaquette numerator, the marked plaquette is already supplied by the
observable insertion. A distinct connected shell therefore first appears when
the action contributes the other five faces of the cube boundary.

So the first distinct connected nonlocal numerator shell is order `beta^5`.

## Corollary 2: the first connected vacuum shell is order `beta^6`

For the vacuum partition function there is no marked face supplied in advance.
Any connected closed shell must therefore contain a seed plaquette plus at least
five others.

The same cube boundary realizes that minimum.

So the first connected vacuum shell is order `beta^6`.

## What this closes

- the exact minimal distinct-shell geometry around a marked plaquette
- the exact first distinct-shell orders for the numerator and vacuum sectors
- a reusable atlas tool for future plaquette strong-coupling work

## What this does not close

- the full analytic reduction law `P_full(beta) = P_1plaq(beta_eff(beta))`
- the first actual nonlinear coefficient of `beta_eff(beta)`
- repo-wide replacement of the current canonical same-surface plaquette value

The open coefficient problem is therefore sharper, but it is still open:

> perform the mixed repeated-plaquette connected-cumulant audit and derive the
> first genuine higher-order coefficient of the full-vacuum reduction law.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=1 FAIL=0`
