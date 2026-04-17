# Gauge-Vacuum Plaquette Mixed-Cumulant Audit and First Nonlinear Coefficient

**Date:** 2026-04-16
**Status:** exact first-nonlinear-coefficient theorem on the accepted Wilson
`3 spatial + 1 derived-time` surface
**Script:** `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py`

## Question

After ruling out the naive constant-lift law, can the first genuine
higher-order coefficient of the full-vacuum reduction law be closed exactly?

## Answer

Yes, at small `beta`.

The mixed repeated-plaquette audit now closes the onset theorem

`P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O(beta^6)`

and therefore

`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)`

on the accepted Wilson `3 spatial + 1 derived-time` surface.

This is the first exact nonlinear coefficient of the full-vacuum reduction law.
It is a real upgrade. It is **not** yet full analytic plaquette closure at
`beta = 6`.

## Setup

Write the plaquette observable as

`O = (1/3) Re Tr U_p`

and the Wilson action density as

`X_q = (1/3) Re Tr U_q`.

Then

`P_full(beta) = sum_(n >= 1) beta^n / n! * sum_(q1,...,qn) kappa(O ; X_q1, ..., X_qn)`

where `kappa` denotes the exact connected Haar cumulant at `beta = 0`.

The local one-plaquette block `P_1plaq(beta)` contains precisely the cumulants
with every `q_i = p`. The question is therefore:

> what is the first nonlocal connected cumulant, and what is its exact
> coefficient?

## Theorem 1: leaf plaquettes factorize exactly

Let `q` be a plaquette in a connected distinct-support graph that shares only
one link with the rest of the support. Let `U` denote that shared link and let
`A` be the ordered product of the other three links around `q`.

Those three nonshared links appear nowhere else in the support, so under the
Haar product measure:

- `A` is Haar-distributed,
- `A` is independent of `U` and of the rest of the support,
- `U A` is Haar-distributed for every fixed `U`.

Therefore for every polynomial `F` in the single plaquette variable `X_q`,

`E[F(X_q) | rest, U] = c_F`

is a constant independent of both `U` and the rest of the support.

So any repeated insertion carried by a leaf plaquette factors off exactly from
the rest of the support. Consequently:

> any mixed connected cumulant whose distinct-support graph is a tree vanishes
> exactly after iterative leaf peeling.

This is the missing repeated-plaquette mechanism: repeated leaves do not create
new connected nonlocal coefficients.

## Corollary 1: only leafless distinct supports can contribute nonlocally

After subtracting the local one-plaquette block, every surviving nonlocal term
must reduce to a **leafless** distinct support containing the observed
plaquette.

So the onset problem is a finite leafless-support classification problem.

## Theorem 2: there is no nonlocal correction through order `beta^4`

For order `n <= 4`, every nonlocal support must touch each of the four observed
edges at least once. Since a distinct non-observed plaquette can touch at most
one observed edge, the only leafless size-`4` candidate class is:

- one distinct action plaquette on each observed edge.

The runner exhaustively checks all

`5^4 = 625`

such local supports and tests all `2^5` orientation assignments. None satisfies
the exact link-balance condition required for a nonzero `SU(3)` Haar integral.

So

`P_full(beta) - P_1plaq(beta) = O(beta^5)`.

## Theorem 3: the only distinct order-`beta^5` survivors are the four cube shells

At order `beta^5`, a distinct leafless support must still include one action
plaquette on each observed edge, plus one extra action plaquette.

The runner exhaustively checks every such local candidate support and finds:

- `37176` exact local candidates are tested,
- exactly `4` survive,
- they are precisely the four elementary cube shells through the observed
  plaquette.

Geometrically, the observed plaquette lies in four elementary `3`-cubes on the
accepted `3 spatial + 1 derived-time` hypercubic surface:

- positive and negative offset in transverse direction `2`,
- positive and negative offset in transverse direction `3`.

No other distinct order-`beta^5` support survives.

## Theorem 4: each cube shell contributes exactly `1 / 18^5`

For one oriented cube shell:

- there are `6` plaquette factors total, one observed plus five action faces,
- there are `2` surviving global orientation choices,
- each plaquette density contributes the factor `(Tr + Tr^dagger) / 6`,
- the closed cube surface has `V = 8` vertices and `E = 12` edges,
- each edge integration contributes `1/3`,
- the resulting raw color contraction gives `3^V / 3^E = 1 / 3^4 = 1/81`.

So the exact per-shell contribution is

`2 * (1/6)^6 * (1/81) = 1 / 18^5`.

Since there are exactly `4` cube shells, the first nonlocal coefficient is

`4 / 18^5 = 1 / 472392`.

## Corollary 2: first nonlinear coefficient of the reduction law

The exact local one-plaquette slope is

`P_1plaq'(0) = 1 / 18`.

So if

`P_full(beta) = P_1plaq(beta_eff(beta))`

holds as a formal small-`beta` reduction law, then the first nonlinear term is
forced to be

`beta_eff(beta) = beta + (1 / 26244) beta^5 + O(beta^6)`.

Equivalently:

`P_full(beta) = P_1plaq(beta) + (1 / 472392) beta^5 + O(beta^6)`.

## What this closes

- the mixed repeated-plaquette audit through the first nonlocal order
- the first exact nonlocal coefficient of the full-vacuum plaquette expansion
- the first exact nonlinear coefficient of the reduction law `beta_eff(beta)`

## What this does not close

- the full nonperturbative function `beta_eff(beta)` at `beta = 6`
- full analytic repinning of the canonical plaquette package
- repo-wide downstream migration from `<P> = 0.5934`

The current live boundary is therefore:

> the onset of the full-vacuum reduction law is now exact, but the
> nonperturbative continuation to the framework point `beta = 6` is still open.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=1 FAIL=0`
