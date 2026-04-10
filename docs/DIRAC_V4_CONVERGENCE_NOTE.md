# Dirac v4 Convergence Note

Date: 2026-04-10

This note records the larger-lattice attack in
[`scripts/frontier_dirac_walk_3plus1d_v4_convergence.py`](../scripts/frontier_dirac_walk_3plus1d_v4_convergence.py).

## Setup

- Architecture: 4-component Dirac walk
- Gravity coupling: reversed, `m(r) = m0 * (1 + f(r))`
- Boundary comparison: periodic vs open/absorbing
- Lattice sizes: `n = 17, 21, 25, 29`
- N-sweep target: `n = 29`
- Distance-law target: `n = 29`, `N = 16`

The run was repeated at two masses:

- `m0 = 0.30`
- `m0 = 0.10`

The `m0 = 0.10` point is the better of the two and is the one to carry forward.

## Best Results

### Closure improvement on larger periodic lattices

At `m0 = 0.10`, periodic closure stays at `7/10` across the larger lattice sweep:

- `n = 17, N = 12` -> `7/10`
- `n = 21, N = 12` -> `7/10`
- `n = 25, N = 12` -> `7/10`
- `n = 29, N = 12` -> `7/10`

The score does not improve with larger `n`.

### Gravity monotonicity over N

At `n = 29`, `offset = 3`:

- Periodic: sign flips across `N = 8..24`, no monotone increasing TOWARD bias
- Open/absorbing: same qualitative pattern, no monotone increasing TOWARD bias

The open boundary does not remove the N oscillation.

### Distance law over offset

At `n = 29`, `N = 16`:

- Periodic: mixed sign across offsets 2..6, `3/5` TOWARD, no valid single power-law fit
- Open/absorbing: same mixed sign pattern, `3/5` TOWARD, no valid single power-law fit

The non-periodic boundary does not cure the offset-law failure.

## Interpretation

The larger-lattice Dirac walk is not rescued by simply going bigger.
At the tuned mass point, the closure score improves from the weaker `6/10` case to `7/10`,
but the remaining gravity monotonicity and distance-law failures persist.

The periodic and open runs agree on the important qualitative point:
the remaining Dirac failures are not just a periodic-torus artifact.
They survive the boundary change and therefore look structural in the current
factorized 4-component implementation.

## Carry-Forward

- Keep `m0 = 0.10` as the best observed operating point from this v4 probe.
- Treat the monotonicity and offset-law failures as structural until a coupled
  Dirac coin or a different observable changes them.
- Use this script as the large-lattice baseline for the next attack round.
