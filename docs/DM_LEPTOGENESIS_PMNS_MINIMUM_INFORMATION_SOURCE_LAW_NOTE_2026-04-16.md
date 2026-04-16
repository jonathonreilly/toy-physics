# DM Leptogenesis PMNS Minimum-Information Source Law

**Date:** 2026-04-16  
**Status:** invented post-axiom selector law for the PMNS-assisted `N_e` route  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_mininfo_source_law.py`

## Law

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
   `eta_{i_*} / eta_obs = 1`, choose the one minimizing `I_seed`

This is the invented selector law for the off-seed `5`-real source.

## Output

The law selects:

- `x_min = (0.47937029, 0.43463700, 0.77599271)`
- `y_min = (0.23114281, 0.39486835, 0.29398884)`
- `delta_min ≈ 0`

so the off-seed source is

- `xi_min = (-0.08396304, -0.12869633, 0.21265938)`
- `eta_min = (-0.07552386, 0.08820168, -0.01267783)`
- `delta_min ≈ 0`

and the resulting flavored transport values are

`eta / eta_obs = (1.0, 0.50519888, 0.78233530)`.

The favored column remains column `0`, and exact closure is reached there.

## Why this is stronger than the earlier extremal candidate

The earlier transport-extremal construction only showed:

- an overshooting off-seed source exists
- therefore, by continuity, a closure point exists

This law removes the remaining arbitrariness by choosing the
**least-deformed** exact closure source relative to the derived native seed
surface.

So it is a real law, not just an existence argument.

## Interpretation

This is not a sole-axiom theorem.

It is an invented **post-axiom dynamical selector law** inside the same
framework:

- the sole axiom fixes the carrier and seed pair
- exact transport fixes the favored column
- the invented information principle fixes the off-seed source

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_mininfo_source_law.py
```
