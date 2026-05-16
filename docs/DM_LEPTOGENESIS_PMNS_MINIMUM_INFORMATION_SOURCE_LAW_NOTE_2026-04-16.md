# DM Leptogenesis PMNS Minimum-Information Source Law

**Status:** bounded - bounded or caveated result note  
**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_mininfo_source_law.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Scope and honest framing

This note documents the consequences of **adopting** a post-axiom selector
law on the charged-lepton-active `N_e` branch. The selector law itself is an
explicit definition; it is not derived here from the framework axiom.

The note is therefore a **conditional** result:

> IF the minimum-information selector law (defined below) is adopted as a
> post-axiom convention on the fixed native `N_e` seed surface, THEN it picks
> out a unique exact-closure off-seed source on the transport-favored column.

The deriving-the-selector question — does the sole axiom itself force the
information cost `I_seed` (or some equivalent functional) to be the correct
selector? — is **not** answered here. It is the subject of separate sister
notes (see the relative-action stationarity theorem and the observable
relative-action law, both of which strengthen this framing by rebuilding the
objective from a framework-internal scalar `log|det|` observable principle).

## Definition of the law

On the fixed native charged-lepton-active seed surface with

- `xbar = 0.5633333333333334`
- `ybar = 0.30666666666666664`

define the information-deformation cost

`I_seed = D_KL(x || x_seed) + D_KL(y || y_seed) + (1 - cos delta)`

where

- `x_seed = (xbar, xbar, xbar)`
- `y_seed = (ybar, ybar, ybar)`.

Then:

1. determine the transport-favored flavor column `i_*` from the exact
   transport-extremal class
2. among all positive off-seed sources on that same seed surface satisfying
   `eta_{i_*} / eta_obs = 1`, choose the one minimizing `I_seed`.

This is the adopted selector law for the off-seed `5`-real source. It is a
choice of objective imported from information geometry. It is **not** derived
from `Cl(3)` on `Z^3`.

## Conditional output

If the law is adopted, the runner-verified selection is:

- `x_min = (0.47937029, 0.43463700, 0.77599271)`
- `y_min = (0.23114281, 0.39486835, 0.29398884)`
- `delta_min ~ 0`

so the off-seed source is

- `xi_min = (-0.08396304, -0.12869633, 0.21265938)`
- `eta_min = (-0.07552386, 0.08820168, -0.01267783)`
- `delta_min ~ 0`

and the resulting flavored transport values are

`eta / eta_obs = (1.0, 0.50519888, 0.78233530)`.

Conditional on the law, the favored column remains column `0`, and exact
closure is reached there.

## What this note does claim

- the minimum-information functional `I_seed` is a valid post-axiom selector
  in the sense that it has a unique stationary point on the exact closure
  manifold (12/12 runner PASS)
- conditional on adopting `I_seed`, the off-seed `5`-real source is fixed
- conditional on adopting `I_seed`, the selected closure source is strictly
  closer to the seed than the canonical near-closing sample, with
  `I_seed = 0.058549869343`
- conditional on adopting `I_seed`, the selected source still respects the
  transport-favored column identified by the exact extremal class

## What this note does NOT claim

- it does **not** claim that `I_seed` follows from `Cl(3)` on `Z^3`
- it does **not** claim that the minimum-information functional is the
  unique correct selector — alternative selectors (relative bosonic action,
  multistart selector support, analytic stationary classification) all give
  matching low-action branches on the same reduced surface, but each is its
  own conditional framing
- it does **not** close the sole-axiom chain for the PMNS-assisted `N_e`
  branch — that question is parked at the relative-action stationarity
  theorem and the observable relative-action law

## Why this note is still useful

The note materially strengthens the closure picture in three ways:

1. it removes the residual arbitrariness of the earlier extremal candidate
   by giving a fully explicit, runner-reproducible selector
2. it confirms that the closure source on the favored column is genuinely
   off-seed but information-cheap (small KL deformation, near-zero phase),
   which is the qualitative expectation
3. it provides a baseline against which the stronger framework-internal
   selectors (`S_rel` and KKT classification) can be benchmarked

The note is therefore retained as `support` rather than positive-theorem
authority. The closure on the PMNS-assisted `N_e` branch should be cited
through the sister theorems whose objectives are framework-internal, with
this note used to anchor the post-axiom interpretation.

## Runner imports (transparency)

The runner imports the following local helpers from the same repository:

- `dm_leptogenesis_exact_common`: exact thermal package, `eta_obs`, etc.
- `frontier_dm_leptogenesis_flavor_column_functional_theorem`: transport
  kernel and column functional
- `frontier_dm_leptogenesis_pmns_active_projector_reduction`: active
  packet map
- `frontier_dm_leptogenesis_pmns_projector_interface`: canonical
  charged-block construction

These are not external libraries; they are sister modules in the same
research repo. Each has its own audit status; the present note inherits
their bounds.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_mininfo_source_law.py
```
