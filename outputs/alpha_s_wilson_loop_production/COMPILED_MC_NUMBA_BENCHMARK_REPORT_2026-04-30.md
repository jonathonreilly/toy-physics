# Alpha_s Direct Wilson-Loop Compiled-MC Benchmark Report

**Date:** 2026-04-30
**Branch:** `claude/alpha-s-direct-wilson-loop-2026-04-30`
**PR:** #227
**Status:** compiled backend fixed; production campaign not yet run to full statistics

## Summary

A numba-backed SU(3) Wilson-loop MC backend was added in
`scripts/alpha_s_numba_wilson_loop_mc.py`.  The compiled kernels cover:

- SU(3) matrix multiplication, dagger, projection, and trace helpers;
- Cabibbo-Marinari SU(2)-subgroup heat-bath updates;
- SU(2)-subgroup overrelaxation updates;
- staple sums;
- plaquette diagnostics;
- APE spatial smearing;
- rectangular Wilson-loop measurement;
- resumable checkpointed ensemble generation.

The first compiled attempt failed because the SU(2) subgroup projection used
the raw `2x2` determinant rather than the quaternionic SU(2) component that
controls `Re Tr(R W)` in a Cabibbo-Marinari update.  That made the
overrelaxation step drift instead of staying microcanonical.  The fixed path
uses the quaternionic projection, scratch-buffer in-place staple construction,
checkerboard-parallel updates, and a parallel buffer-reusing Wilson-loop
measurement kernel.

The compiled heat-bath and representative heat-bath-plus-overrelaxation paths
now pass the local compiled-speed and plaquette-stability checks.  The
production-compute blocker is no longer "missing compiled inner loops"; it is
the remaining multi-day wall-clock campaign needed for the `12^3 x 24`,
`16^3 x 32`, and `24^3 x 48` production statistics.

No production `alpha_s(M_Z)` certificate was generated.
No direct `alpha_s(M_Z)=0.1181` measurement is claimed.

## Benchmarks

Reference pure-Python heat-bath timing from
`scripts/frontier_color_projection_mc.py`:

```text
8^4: 182.5 us/link
```

Reference pure-Python Metropolis timing from the first production blocker:

```text
12^3 x 24: 85.49 us/link
```

Superseded first-attempt timings are kept in the JSON artifacts for audit
traceability.  The fixed backend timings are:

| Kernel | Dims | Sweeps | Overrelaxation | us/link | Speedup vs Python heat-bath | 50x gate |
|---|---:|---:|---:|---:|---:|---|
| numba heat-bath | `12^3 x 24` | 50 | 0 | 0.941 | 194.01x | PASS |
| numba heat-bath | `16^3 x 32` | 20 | 0 | 1.421 | 128.39x | PASS |
| numba heat-bath | `24^3 x 48` | 5 | 0 | 1.198 | 152.35x | PASS |
| numba heat-bath + OR | `8^4` | 20 | 4 | 3.506 | 52.06x | PASS |
| numba heat-bath + OR | `8^3 x 16` | 100 | 4 | 3.505 | 52.07x | PASS |
| numba heat-bath + OR | `12^3 x 24` | 50 | 3 | 3.074 | 59.38x | PASS |

The fixed overrelaxation diagnostics stay in the expected beta=6 rough range:

```text
8^4, OR=4:          plaquette = 0.5960
8^3 x 16, OR=4:    plaquette = 0.5945
12^3 x 24, OR=3:   plaquette = 0.5948
```

The full `16^3 x 32` and `24^3 x 48` heat-bath-plus-three-overrelaxation
benchmarks are stable but do not clear the strict `50x` comparison when
overrelaxation sweeps are included in the denominator:

```text
16^3 x 32, OR=3: 4.963 us/link, 36.77x
24^3 x 48, OR=3: 4.018 us/link, 45.42x
```

The heat-bath kernel itself is well above `50x` on those geometries; the
remaining cost is the deliberately requested extra microcanonical sweeps.

## Files Written

Fixed-backend benchmark outputs:

- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_12x12x12x24_parallel_50sweeps_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_16x16x16x32_parallel_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_24x24x24x48_parallel_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax3_benchmark_12x12x12x24_parallel_50sweeps_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax3_benchmark_16x16x16x32_parallel_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax3_benchmark_24x24x24x48_parallel_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax4_benchmark_8x8x8x8_parallel_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax4_benchmark_8x8x8x16_parallel_100sweeps_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_measurement_overhead_12x12x12x24_r8t8_parallel_2026-04-30.json`

Pilot Wilson-loop smoke outputs are present for compile/runtime validation
only.  They are not production evidence.

## Production Consequence

Using three overrelaxation sweeps, the requested `21000` update sweeps per
volume plus a conservative `400` full `R,T <= 8` measurements would require
approximately:

| Volume | Links/sweep | Update wall time | Measurement wall time | Total estimate |
|---|---:|---:|---:|---:|
| `12^3 x 24` | 165888 | 2.97 h | 0.35 h | 3.33 h |
| `16^3 x 32` | 524288 | 15.18 h | 1.11 h | 16.29 h |
| `24^3 x 48` | 2654208 | 62.21 h | 5.61 h | 67.83 h |
| Total | - | 80.37 h | 7.07 h | 87.44 h |

This excludes jackknife/bootstrap, plateau fitting, autocorrelation analysis,
failed-plateau reruns, and any scheme-conversion/RGE analysis work.

The strict alpha_s runner should continue to fail until those production
statistics exist and have been converted into a Wilson-loop/static-potential
certificate.

## Recommended Production Commands

A follow-up autocorrelation pilot on `12^3 x 24` measured
`tau_int = 1.0697` sweeps for the slowest tracked observable and recommends
`separation = ceil(5 tau_int) = 6`.  The revised strict-runner-compatible
500-configuration timeline is documented in:

```text
outputs/alpha_s_wilson_loop_production/VALID_PRODUCTION_TIMELINE_2026-04-30.md
```

Run each volume with checkpointing.  Example for `12^3 x 24`:

```bash
NUMBA_NUM_THREADS=6 \
python3 scripts/alpha_s_numba_wilson_loop_mc.py ensemble \
  --dims 12,12,12,24 \
  --therm 1000 \
  --measurements 500 \
  --separation 6 \
  --overrelax 3 \
  --ape-steps 5 \
  --max-r 8 \
  --max-t 8 \
  --checkpoint-npz outputs/alpha_s_wilson_loop_production/ensemble_12x12x12x24_checkpoint.npz \
  --output outputs/alpha_s_wilson_loop_production/ensemble_12x12x12x24.json
```

Repeat with `16,16,16,32` and `24,24,24,48`.  If interrupted, add
`--resume-checkpoint` with the same checkpoint path.
