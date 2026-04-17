# Gauge-Vacuum Plaquette Framework-Point Underdetermination

**Date:** 2026-04-16
**Status:** exact obstruction theorem on the current plaquette support stack;
analytic `P(6)` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py`

## Question

Do the exact plaquette theorems already on `main` force the framework-point
value `P(6)`?

## Answer

No.

The current exact stack closes:

- existence and uniqueness of an implicit finite-surface reduction law
  `P_L(beta) = P_1plaq(beta_eff,L(beta))`,
- analyticity and strict monotonicity of `beta_eff,L`,
- the exact onset jet
  `beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)`,
- the exact infinite connected-hierarchy structure,
- and the existence/uniqueness of the equivalent compact spectral measure.

But those facts do **not** yet determine the explicit nonperturbative
framework-point reduction parameter `beta_eff(6)`.

In particular, there exist distinct real-analytic strictly increasing witness
laws on `[0,6]` that share the exact closed onset jet through order `beta^5`
but produce different framework-point values, hence different candidate
plaquettes after composition with the exact monotone one-plaquette block
`P_1plaq`.

So the current exact stack does **not** yet force analytic `P(6)`.

## Setup

Let

`a = 1 / 26244`.

The exact mixed-cumulant audit and reduction-existence theorem already close

`beta_eff(beta) = beta + a beta^5 + O(beta^6)`,

with `beta_eff` analytic and strictly increasing on the finite Wilson source
surface.

Define two witness laws:

`beta_eff^-(beta) = beta + a beta^5`,

`beta_eff^+(beta) = beta + a beta^5 + c beta^6`,

with

`c = 10^(-7)`.

Both are entire real-analytic functions.

## Theorem 1: same exact jet through order `beta^5`

The two witness laws satisfy

`beta_eff^+(beta) - beta_eff^-(beta) = c beta^6 = O(beta^6)`.

Therefore both share the exact closed onset jet

`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)`.

## Theorem 2: both witnesses are strictly increasing on `[0,6]`

Their derivatives are

`d beta_eff^- / d beta = 1 + 5 a beta^4`,

`d beta_eff^+ / d beta = 1 + 5 a beta^4 + 6 c beta^5`.

Both are strictly positive for all `beta >= 0`, hence on `[0,6]`.

So both witnesses satisfy the same current exact regularity boundary:

- real-analytic,
- strictly increasing,
- same exact onset through order `beta^5`.

## Corollary 1: the framework point is not fixed by the current exact jet

At `beta = 6`,

`beta_eff^+(6) - beta_eff^-(6) = c 6^6 = 46656 / 10^7 = 0.0046656 > 0`.

So the current exact onset jet and monotonicity data do not determine a unique
framework-point reduction parameter.

## Corollary 2: the framework-point plaquette is not fixed by the current exact stack

The exact one-plaquette block `P_1plaq(beta)` is strictly increasing.

Therefore

`P_1plaq(beta_eff^+(6)) > P_1plaq(beta_eff^-(6))`.

So the current exact plaquette data already closed on `main`

- do not yet determine a unique explicit `beta_eff(6)`,
- and therefore do not yet determine a unique analytic `P(6)`.

## Spectral-measure interpretation

The exact spectral-measure theorem says that the full finite Wilson hierarchy is
equivalent to one compact positive measure `mu_L` on `[-1,1]`, and Hausdorff
uniqueness says that the **full** moment sequence uniquely determines `mu_L`.

That does **not** imply that the finite jet already closed on `main`
determines `mu_L`. The witness reduction laws above show exactly why:

> current exact onset data plus analyticity/monotonicity still leave multiple
> admissible nonperturbative framework-point reductions.

So explicit spectral identification at `beta = 6` remains a genuinely new
theorem target rather than something already implied by the existing atlas.

## What this closes

- exact proof that the current closed jet does not force a unique
  framework-point reduction parameter
- exact proof that the current closed jet does not force a unique analytic
  plaquette at `beta = 6`
- exact clarification that the remaining plaquette gap is not structural
  existence, but explicit nonperturbative identification

## What this does not close

- explicit identification of the compact plaquette spectral measure
- explicit closed form for `beta_eff(6)`
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=2 FAIL=0`
