# Experiment Design: Interference Geometry Sensitivity

## Date
2026-03-30

## Observables
1. **Fringe contrast** — (max - min) / (max + min) of center detector probability across phase sweep. Ranges from 0 (flat, no interference) to 1 (perfect interference).
2. **Center detector probability** — P(y=0) as a function of phase_shift_upper.
3. **Full screen distribution** — P(y) for all screen positions, at selected geometry points.
4. **Record suppression ratio** — fringe contrast with record / fringe contrast without record.

## Parameters

| Parameter | Min | Max | Steps | Scale |
|-----------|-----|-----|-------|-------|
| phase_shift_upper | 0 | 2*pi | 24 | linear |
| grid_width | 8 | 28 | 6 values: 8,12,16,20,24,28 | linear |
| slit_half_separation | 2 | 8 | 4 values: 2,4,6,8 | linear |
| record_created | False, True | - | 2 | boolean |

Total combinations: 24 phases x 6 widths x 4 separations x 2 record modes = 1,152 runs.
Each run is a single path-sum on a small grid (~O(100) nodes). Estimated <0.1s per run.
Total runtime: ~2 minutes.

## Controls
- **Baseline**: default geometry (width=16, height=10, slit_ys={-4,4}) matches existing `two_slit_distribution()`. Must reproduce identical results.
- **Record control**: every geometry point tested with BOTH record_created=True and False.
- **Phase control**: phase=0 should match the existing no-phase-shift case.

## Systematic Error Checks
- Grids too narrow (width < barrier_x) would break the setup. Guard: width must be >= barrier_x + 2.
- Slit separation exceeding grid height would place slits outside the grid. Guard: slit_half_sep < height.
- Zero normalization: if total probability is 0 at a screen position, flag as degenerate rather than divide-by-zero.

## Reuse Check
- `two_slit_distribution()` (line 23141) — direct reuse with parameterization.
- `center_detector_phase_scan()` (line 23240) — logic reused for phase sweep.
- `build_rectangular_nodes()`, `derive_local_rule()`, `derive_node_field()`, `infer_arrival_times_from_source()`, `build_causal_dag()` — all called internally, no changes needed.

## Script Plan
One script: `scripts/interference_geometry_sweep.py`
- Parameterized version of `two_slit_distribution()` accepting width, height, slit_ys, barrier_x.
- Outer loop: geometry x record_created.
- Inner loop: phase sweep.
- Output: structured text log with one block per geometry point.

## Runtime
~2 minutes interactive. No autopilot needed.
