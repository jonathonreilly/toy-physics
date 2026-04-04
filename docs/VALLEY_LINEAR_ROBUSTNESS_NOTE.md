# Valley-Linear Robustness Note

**Date:** 2026-04-04
**Status:** artifact-backed bounded replay on the 3D ordered-lattice family

## What is frozen here

This note is the conservative readout for the dedicated sweep harness:

- [scripts/valley_linear_robustness_sweep.py](/Users/jonreilly/Projects/Physics/scripts/valley_linear_robustness_sweep.py)
- [logs/2026-04-04-valley-linear-robustness-sweep.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-valley-linear-robustness-sweep.txt)

The replay uses:

- action `S = L(1-f)`
- kernel `1/L^2` with `h^2` measure
- `h = 0.5`
- the 3D ordered-lattice family only

It measures the same observables that matter for the current valley-linear branch:

- Born
- d_TV
- MI
- decoherence
- gravity sign / magnitude
- `F~M`
- distance tail when there are enough post-peak points

## Width sweep

Fixed `L=12`, `max_d=3`, `h=0.5`.

| W | Born | d_TV | MI | Decoh | Gravity | F~M | Tail |
|---|------|------|----|-------|---------|-----|------|
| 4 | `2.1e-15` | `0.76` | `0.57` | `49.2%` | `+0.000114` T | `1.00` | n/a |
| 6 | `2.5e-15` | `0.78` | `0.61` | `49.5%` | `+0.000136` T | `1.00` | n/a |
| 8 | `2.5e-15` | `0.79` | `0.59` | `49.4%` | `+0.000144` T | `1.00` | `b^(-1.47)`, `R²=0.996` |
| 10 | `2.2e-15` | `0.79` | `0.57` | `49.4%` | `+0.000150` T | `1.00` | `b^(-1.08)`, `R²=0.941` |

## Connectivity sweep

Fixed `L=12`, `W=8`, `h=0.5`.

| max_d | Born | d_TV | MI | Decoh | Gravity | F~M | Tail |
|-------|------|------|----|-------|---------|-----|------|
| 1 | `6.9e-16` | `0.91` | `0.83` | `50.0%` | `+0.000229` T | `1.00` | `b^(-0.85)`, `R²=0.931` |
| 2 | `1.6e-15` | `0.77` | `0.60` | `48.4%` | `+0.000165` T | `1.00` | `b^(-0.47)`, `R²=0.888` |
| 3 | `2.5e-15` | `0.79` | `0.59` | `49.4%` | `+0.000144` T | `1.00` | `b^(-1.47)`, `R²=0.996` |

## Length sweep

Fixed `W=8`, `max_d=3`, `h=0.5`.

| L | Born | d_TV | MI | Decoh | Gravity | F~M | Tail |
|---|------|------|----|-------|---------|-----|------|
| 8  | `2.1e-15` | `0.78` | `0.56` | `49.6%` | `+0.000114` T | `1.00` | `b^(-0.93)`, `R²=0.962` |
| 10 | `2.2e-15` | `0.80` | `0.59` | `49.6%` | `+0.000133` T | `1.00` | `b^(-1.19)`, `R²=0.978` |
| 12 | `2.5e-15` | `0.79` | `0.59` | `49.4%` | `+0.000144` T | `1.00` | `b^(-1.47)`, `R²=0.996` |
| 15 | `2.7e-15` | `0.77` | `0.59` | `49.2%` | `+0.000164` T | `1.00` | `b^(-1.02)`, `R²=0.887` |
| 18 | `2.1e-15` | `0.75` | `0.58` | `48.7%` | `+0.000178` T | `1.00` | `b^(-1.06)`, `R²=0.941` |

## Conservative interpretation

The strongest safe summary from this frozen replay is:

- the valley-linear action is **robust on the tested 3D ordered-lattice slices**
- Born stays machine-clean on every row in the sweep
- `F~M` stays at `1.00` on every tested row
- gravity stays TOWARD throughout the tested width, connectivity, and length rows
- the distance tail is real, but the fitted exponent is slice-dependent and should not be read as a universal theorem

What this note does **not** claim:

- robustness across all architectures
- universality of the tail exponent
- that the action law is fully settled
- that the sweep proves any continuum theorem

For the broader action-law comparison, use:

- [VALLEY_LINEAR_ACTION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ACTION_NOTE.md)
- [ACTION_CROSSOVER_NOTE.md](/Users/jonreilly/Projects/Physics/docs/ACTION_CROSSOVER_NOTE.md)

