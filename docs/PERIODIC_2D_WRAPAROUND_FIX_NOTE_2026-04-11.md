# Periodic 2D Wraparound Fix Note (2026-04-11)

## Scope

This note covers the periodic-2D minimum-image weighting bug identified in:

- `scripts/frontier_self_consistency_test.py`
- `scripts/frontier_eigenvalue_stats_and_anderson_phase.py`
- `scripts/frontier_born_rule_alpha.py`

The bug was specific to the hopping-weight builder on periodic square lattices.
Adjacency was built with torus wraparound, but the edge weight was computed from
raw coordinate differences instead of minimum-image distances. That meant a
wraparound nearest neighbor on a `side x side` torus could be treated as having
distance `side - 1` instead of `1`, suppressing the corresponding hopping.

## Fix

All three scripts now compute periodic edge lengths with minimum-image deltas:

- `dx = min(abs(x_j - x_i), side - abs(x_j - x_i))`
- `dy = min(abs(y_j - y_i), side - abs(y_j - y_i))`

The Hamiltonian weights now match the torus adjacency actually used by the
lattice builders.

## Corrected rerun status

### 1. `frontier_self_consistency_test.py`

Corrected rerun on the fixed `10x10` periodic surface:

- `1-SelfConsist`: sign margin `+30.0 +/- 0.0`, width ratio `0.3554`, boundary alpha `0.145434`
- `2-StaticInit`: sign margin `+40.0 +/- 0.0`, width ratio `0.3563`, boundary alpha `0.159548`
- `3-PosRandom`: sign margin `-0.2 +/- 6.9`, width ratio `0.6465`, boundary alpha `0.126349`
- `4-NegRandom`: sign margin `+0.2 +/- 6.9`, width ratio `1.0892`, boundary alpha `0.256546`

Corrected interpretation:

- The lane still supports a deterministic split between self-consistent and static-from-initial on this fixed torus surface.
- The lane still supports a strong separation between structured and random positive potentials.
- The corrected run does **not** change the larger methodological caveat: this is still a torus-fixed comparison, not a universal continuum statement.

### 2. `frontier_eigenvalue_stats_and_anderson_phase.py`

Corrected rerun on the fixed periodic surfaces:

- Part 1 still shows **no chaos transition**. The spectrum stays on the Poisson side for all tested `G`.
- Corrected `<r>` values:
  - `G=0`: `0.1797`
  - `G=10`: `0.3963`
  - `G=50`: `0.3984`
  - `G=100`: `0.3457`
- The maximum corrected `<r>` is `0.3984`, still below the Poisson/GOE midpoint `0.458`.

Corrected phase-map read:

- `L=8`: gravity-distinguishable at `G = 0.5, 1, 2, 5, 10, 20`
- `L=10`: gravity-distinguishable at `G = 2, 5`
- `L=12`: gravity-distinguishable at `G = 2, 5, 10, 20`
- `L=6`: only a narrow corrected window near `G = 10`

Corrected interpretation:

- The bug fix does **not** rescue a chaos claim.
- The Anderson-gravity window remains real on these corrected periodic surfaces, but it is a torus phase-map result, not yet an architecture-wide retained closure.

### 3. `frontier_born_rule_alpha.py`

Corrected rerun on the fixed `10x10` periodic surface:

- Best composite-stability alpha is still `1.00` at `G = 5, 10, 50`
- `alpha = 2.0` is still **not** uniquely selected
- Corrected sign-selectivity margin at `alpha = 2.0`: `+30`
- Best non-2.0 margin is tied at `+30`

Corrected interpretation:

- The minimum-image bug does **not** reopen the Born-rule lane.
- The corrected rerun still falsifies the original uniqueness hypothesis.
- The script now states this honestly: sign selectivity is present at `alpha = 2.0`, but not uniquely best.

## What remains invalid or limited

These issues are **not** fixed by the minimum-image patch:

### `frontier_self_consistency_test.py`

- The positive/negative random controls are still generated from absolute-value Gaussian draws rather than a tighter matched random ensemble.
- Large deterministic separations on this fixed surface should still be read as exact surface splits, not generic statistical significance claims.

### `frontier_eigenvalue_stats_and_anderson_phase.py`

- This remains a periodic-torus study.
- The disorder comparison is still a model-control experiment, not a proof that gravity and disorder are cleanly separated on all surfaces.

### `frontier_born_rule_alpha.py`

- The script still measures Hartree fixed-point convergence, not quantum measurement.
- Even after the wraparound fix, this lane remains structurally incapable of deriving the Born rule from unitary single-particle dynamics alone.

## Retention recommendation

- Treat the corrected outputs in this note as the canonical periodic-2D rerun surface for these three scripts.
- Keep the self-consistency and Anderson-phase lanes as corrected periodic-surface results.
- Keep the Born-rule lane as a corrected negative / boundary-of-validity result.
- Do **not** promote any broader claim from these reruns without separately addressing the remaining methodological limitations listed above.
