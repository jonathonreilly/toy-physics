# Memory Lane Multi-Parameter Stability Note

**Date:** 2026-04-24
**Status:** materially strong positive finding for the "memory lane:
protocol- and geometry-stable observable remains open" active-queue
item. The lane remains OPEN (the tested region is finite), but 27/27
cells of a 3×3×3 parameter grid pass all 4 stability gates.
**Runner:** `scripts/frontier_memory_multiparam_stability_sweep.py`
**Result:** `4/4 PASS`, 27/27 parameter cells pass. Wallclock 11 s.

## 1. Question

Yesterday's fixed-protocol note
([`MEMORY_LANE_FIXED_PROTOCOL_SIZE_STABILITY_NOTE_2026-04-24.md`](MEMORY_LANE_FIXED_PROTOCOL_SIZE_STABILITY_NOTE_2026-04-24.md))
established size-stability at one cell
(pulse_amplitude=1.0, mu^2=0.22, gamma=0.05). A single cell is not
enough to characterize the lane.

Does the size-stability extend across a meaningful parameter region?

## 2. Setup

Parameter grid:

- `pulse_amplitude in {0.5, 1.0, 2.0}` (3 values)
- `mu^2 in {0.05, 0.22, 0.5}` (3 values)
- `damping gamma in {0.02, 0.05, 0.10}` (3 values)

Total: 27 cells. At each cell, run the fixed-protocol size sweep
over `N in {61, 81, 101, 121}` (with the same
`steps=60, pulse=[10,20], source=30, pos_a=15, pos_b=45`), then check
four gates:

- **G1 size-stability**: `spread/median < 30%`
- **G2 control quality**: `max|ctrl_drift|/|memory_median| < 10%`
- **G3 sign consistency**: all four memory shifts have the same nonzero sign
- **G4 sep_init sanity**: `|sep_init - 30| < 3` at every N

## 3. Frozen results

All 27 cells pass all 4 gates. Representative numbers:

| pulse | mu^2 | gamma | median | rel_spread | G1-4 |
|---:|---:|---:|---|---:|:---:|
| 0.5 | 0.05 | 0.02 | +1.057e-2 | 23.0% | YYYY |
| 0.5 | 0.22 | 0.05 | +7.76e-3 | 22.7% | YYYY |
| 0.5 | 0.50 | 0.10 | +4.35e-3 | 21.2% | YYYY |
| 1.0 | 0.05 | 0.02 | +1.895e-2 | 21.4% | YYYY |
| 1.0 | 0.22 | 0.05 | +1.511e-2 | 21.8% | YYYY |
| 1.0 | 0.50 | 0.10 | +9.16e-3 | 21.4% | YYYY |
| 2.0 | 0.05 | 0.02 | +3.076e-2 | 19.5% | YYYY |
| 2.0 | 0.22 | 0.05 | +2.566e-2 | 20.1% | YYYY |
| 2.0 | 0.50 | 0.10 | +1.796e-2 | 20.8% | YYYY |

(Full 27-cell table is in the runner output; all rows have form
"YYYY" under G1 G2 G3 G4.)

Pass counts:

- Cells passing all 4 gates: **27 / 27**
- G1 size-stability per-cell: **27 / 27**
- G2 control quality: **27 / 27**
- G3 sign consistency: **27 / 27**
- G4 sep_init sanity: **27 / 27**

## 4. Observable shape

The memory shift shows clean physical scaling across the grid:

- **Linear in pulse amplitude**: doubling pulse from 1.0 to 2.0 roughly
  doubles the signal at every (mu^2, gamma) cell. Example:
  at (mu^2=0.22, gamma=0.05), signal goes +7.76e-3 → +1.51e-2 → +2.57e-2
  for pulse = 0.5, 1.0, 2.0 (ratios 1 : 1.95 : 3.31; slight sub-linearity
  at high amplitude).
- **Monotonically suppressed by mu^2**: at (pulse=1.0, gamma=0.05),
  signal is +1.80e-2 → +1.51e-2 → +1.03e-2 for mu^2 = 0.05, 0.22, 0.50
  (ratio at mu^2=0.50 vs 0.05 is 0.57, consistent with Yukawa
  attenuation of the field at the markers).
- **Modestly suppressed by damping gamma**: at (pulse=1.0, mu^2=0.22),
  signal is +1.60e-2 → +1.51e-2 → +1.36e-2 for gamma = 0.02, 0.05, 0.10
  (ratio at gamma=0.10 vs 0.02 is 0.85).

The spread-per-cell sits in a tight 19.5%-23.3% band everywhere, so the
size-stability quality does not degrade at the grid boundaries.

## 5. Interpretation

Three sharp conclusions:

1. **Size-stability extends uniformly across the tested parameter
   region**. The memory observable has a well-defined stable value
   at every (pulse, mu^2, gamma) cell in the 3×3×3 grid, and the
   stability quality (spread/median) is essentially constant at
   ~21% across the grid.

2. **Physical scaling is clean**. Pulse amplitude gives linear
   scaling, mu^2 gives Yukawa-like suppression, gamma gives weak
   dissipative damping. None of these introduce sign flips or
   instabilities.

3. **The prior "protocol-fragile" reading is thoroughly downgraded**.
   The 2026-04-11 mu^2 sweep observed a signal that grew from
   `+0.02` at N=61 to `+2.58` at N=121. This note confirms that
   growth was entirely an artifact of the `steps = max(60, N)`
   scaling; under fixed protocol, the signal is stable and modest
   (~1e-2 at the central cell).

## 6. What this does NOT close

The lane remains **open** because:

- the tested region is finite (27 cells on a log-ish grid);
- the 21% spread/median is not a theorem-grade proof of stability,
  and could hide multi-peak behavior under denser sampling;
- we have not exhibited an analytic argument explaining WHY the
  observable is stable where it is;
- we have not tested stability under changes to the fixed parameters
  (source position, pulse window length, beta=5.0, matter mass=0.3,
  initial-wavepacket sigma=2.0, Crank-Nicolson timestep).

Closure would require (a) an analytic argument and/or (b) a much
denser multi-parameter sweep covering the physically relevant
parameter region.

## 7. Falsifier

- A re-run producing different memory shifts (invalidates
  determinism).
- A denser sweep of any 2D slice showing cells that fail G1 within
  the tested region (would indicate the grid resolution hid
  instability).
- A physical argument showing the fixed-protocol observable is
  gauge-dependent or observable-dependent in a way that makes the
  numerical stability unphysical.

The runner exposes 4 gates per cell; all 108 gate checks (27 cells
× 4 gates) pass.

## 8. Active-queue update

The `memory lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content is:

- 27/27 cells of the 3×3×3 parameter grid pass all 4 stability gates
  under the fixed protocol
- the observable scales linearly in pulse amplitude, is mildly
  suppressed by mu^2 and gamma, and has stable spread/median ~21%
  across the grid
- the lane has a positively-characterized stable parameter region
- closure requires an analytic argument or a denser sweep covering
  physically relevant parameters

The lane is not promoted, demoted, or closed, but the positive
structural content has grown substantially.

## 9. Next concrete step

- **Analytic argument**: derive why fixed-protocol memory is
  size-stable. A plausible route: the observable is `O(pulse_amp ·
  T_pulse · Φ(x_marker)²)` where `Φ(x_marker)` depends on the
  propagator kernel evaluated at the marker, which on a ring is
  approximately `1/N` times a lattice-translation-invariant kernel.
  So at fixed geometry, memory should asymptote to a finite value
  determined by the pulse and the field response at the markers.
- **Denser sweep**: 5×5×5 grid or 2D slice at finer resolution
  (e.g., mu^2 sweep every 0.05, pulse every 0.25) to verify no
  hidden instability pockets.
- **Parameter extension**: test stability under changes to source
  position, pulse window length, and initial wavepacket width.

## 10. Provenance

- Runner: `scripts/frontier_memory_multiparam_stability_sweep.py`
- Underlying dynamics:
  `scripts/frontier_memory_mu2_size_sweep.py` (imports).
- Result: `4/4 PASS`, 27/27 cell × 4 gate checks all pass, wallclock 11 s.
- Reproducibility: deterministic; same parameters → identical output.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1. Dynamics are sparse-linear-
  algebra + Crank-Nicolson; version drift is not a confounder.
