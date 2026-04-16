# DM Leptogenesis Benchmark Decomposition

**Date:** 2026-04-15  
**Status:** exact factor decomposition of the benchmark `eta ~= 0.30 eta_obs`  
**Script:** `scripts/frontier_dm_leptogenesis_benchmark_decomposition.py`

## Question

Why does the current benchmark land at

`eta ~= 1.81e-10 ~= 0.30 eta_obs`

instead of much smaller or much larger?

## Bottom line

Almost entirely because the current reduced CP kernel only realizes about
`27.7%` of the Davidson-Ibarra ceiling at the same `M_1` and washout.

At the benchmark:

- `eta = 7.04 * C_sph * d * kappa * epsilon_1`
- `eta_DI = 7.04 * C_sph * d * kappa * epsilon_DI`

Numerically:

- `eta_DI ~= 6.54e-10 ~= 1.07 eta_obs`
- `epsilon_1 / epsilon_DI ~= 0.277`

Therefore

`eta / eta_obs = (epsilon_1 / epsilon_DI) * (eta_DI / eta_obs)`

and numerically

`eta / eta_obs ~= 0.277 * 1.068 ~= 0.296`.

So the benchmark `0.30` is mainly a CP-kernel suppression number, not a
washout or staircase-placement failure.

## Extra decomposition

On the current reduced kernel:

- the `N_2` term contributes about `0.269` of the DI ceiling
- the `N_3` term contributes about `0.0085`

So the benchmark is strongly `N_2`-dominated, but the total still only reaches
`27.7%` of the DI ceiling.

## What this closes

This closes the immediate “why 0.30?” question sharply:

- not mainly washout
- not mainly `M_1`
- not mainly the staircase placement
- mainly the reduced CP kernel

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_benchmark_decomposition.py
```
