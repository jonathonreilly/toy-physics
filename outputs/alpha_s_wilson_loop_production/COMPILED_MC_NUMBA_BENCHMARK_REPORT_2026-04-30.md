# Alpha_s Direct Wilson-Loop Compiled-MC Benchmark Report

**Date:** 2026-04-30
**Branch:** `claude/alpha-s-direct-wilson-loop-2026-04-30`
**PR:** #227
**Status:** compiled backend added, but production speed/validity gate not met

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
- a pilot ensemble writer for raw Wilson-loop data.

This satisfies the "compiled inner loops" implementation requirement in the
limited sense that the expensive link-update and Wilson-loop loops are under
`numba @njit`.  It does not satisfy the production-compute requirement because
the measured speedup is below the requested `50x` threshold and the
overrelaxation path currently fails a basic plaquette-stability diagnostic.

No production `alpha_s(M_Z)` certificate was generated.
No direct `alpha_s(M_Z)=0.1181` measurement is claimed.

## Benchmarks

Reference pure-Python heat-bath timing from `scripts/frontier_color_projection_mc.py`:

```text
8^4: 182.5 us/link
```

Reference pure-Python Metropolis timing from the first production blocker:

```text
12^3 x 24: 85.49 us/link
```

Measured numba heat-bath-only timing:

| Kernel | Dims | Sweeps | Overrelaxation | us/link | Speedup vs Python heat-bath | 50x gate |
|---|---:|---:|---:|---:|---:|---|
| numba heat-bath | `4^4` | 20 | 0 | 4.503 | 40.53x | FAIL |
| numba heat-bath | `8^4` | 100 | 0 | 5.205 | 35.06x | FAIL |
| numba heat-bath | `8^3 x 16` | 20 | 0 | 5.446 | 33.51x | FAIL |

Measured numba heat-bath plus requested overrelaxation:

| Kernel | Dims | Sweeps | Overrelaxation | us/link | Speedup vs Python heat-bath | 50x gate |
|---|---:|---:|---:|---:|---:|---|
| numba heat-bath + OR | `8^4` | 20 | 4 | 22.258 | 8.20x | FAIL |

The overrelaxation-4 benchmark produced a plaquette diagnostic near
`0.00195` after the short run, while the heat-bath-only benchmarks stayed in
the expected rough beta=6 range around `0.56`.  This means the current
overrelaxation implementation is not production-valid and must not be used to
certify the theorem.

## Files Written

Benchmark outputs:

- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_4x4x4x4_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_8x8x8x8_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_8x8x8x8_100sweeps_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_benchmark_8x8x8x16_2026-04-30.json`
- `outputs/alpha_s_wilson_loop_production/numba_heatbath_overrelax4_benchmark_8x8x8x8_2026-04-30.json`

Pilot Wilson-loop smoke output:

- `outputs/alpha_s_wilson_loop_production/numba_pilot_2x2x2x4_2026-04-30.json`

The pilot is a compile/runtime smoke test only.  It is not production evidence.

## Production Consequence

Using the measured overrelaxation-4 timing of `22.258 us/link`, the requested
`21000` sweeps per volume would still require approximately:

| Volume | Links/sweep | Sweep-only wall time |
|---|---:|---:|
| `12^3 x 24` | 165888 | 0.90 days |
| `16^3 x 32` | 524288 | 2.84 days |
| `24^3 x 48` | 2654208 | 14.36 days |
| Total | - | 18.10 days |

This excludes Wilson-loop measurement for `R,T <= 8`, APE/HYP smearing,
jackknife/bootstrap, plateau fitting, autocorrelation analysis, and reruns.

Since the compiled speedup is below the requested `50x` gate and the
overrelaxation implementation is not production-valid, Phase 2 remains blocked.
The strict alpha_s runner should continue to fail until a validated compiled
kernel and real production Wilson-loop/static-potential certificate exist.

## Next Honest Technical Options

1. Optimize or replace the numba kernels so heat-bath plus overrelaxation is
   both numerically stable and at least `50x` faster than the pure-Python
   heat-bath reference.
2. Move the inner loops to a hand-written C/CFFI or external lattice-QCD code
   path and re-run the benchmark gate.
3. Treat direct Wilson-loop `alpha_s(M_Z)` as a production-compute dependency
   outside the current repo/runtime rather than as a certifiable PR-local run.
