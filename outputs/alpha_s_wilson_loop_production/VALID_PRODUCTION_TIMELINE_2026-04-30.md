# Valid Alpha_s Wilson-Loop Production Timeline

**Date:** 2026-04-30
**Status:** revised after thread autotune and autocorrelation pilot

## Validity Rule

The fixed `20-50` sweep separation is replaced by a measured-autocorrelation
rule: estimate `tau_int` from the gauge stream, save configurations separated
by at least `ceil(5 tau_int)`, and compute final uncertainties with blocked
jackknife/bootstrap on the actual production ensembles.

This is standard Monte Carlo error control.  It does not change the observable
or introduce the forbidden `alpha_LM/u0` route.

## Local Measurements

Thread autotune on `12^3 x 24`, OR=3:

```text
threads=4: 3.468 us/link, 52.62x
threads=6: 2.744 us/link, 66.50x
threads=8: 3.119 us/link, 58.51x
threads=10: 2.819 us/link, 64.73x
```

Recommended local setting for the small production volume:

```text
NUMBA_NUM_THREADS=6
```

Autocorrelation pilot on `12^3 x 24`, OR=3, 80 post-thermalization measured
sweeps:

```text
slowest observable: plaquette
tau_int:            1.0697 sweeps
recommended sep:   ceil(5 tau_int) = 6 sweeps
recommended block: ceil(10 tau_int) = 11 samples
```

Measured full `R,T <= 8` Wilson-loop measurement overhead on `12^3 x 24`:

```text
~3.27 s per saved configuration after subtracting update sweeps
```

## Revised Timeline

For a strict-runner-compatible baseline of `500` saved configurations per
volume:

```text
thermalization: 1000 sweeps
saved configs:  500
separation:     6 sweeps
total updates:  4000 sweeps per volume
```

Estimated wall-clock time:

| Volume | Update time | Measurement time | Total |
|---|---:|---:|---:|
| `12^3 x 24` | 0.51 h | 0.45 h | 0.96 h |
| `16^3 x 32` | 2.89 h | 1.43 h | 4.32 h |
| `24^3 x 48` | 11.85 h | 7.26 h | 19.11 h |
| Sequential total | 15.25 h | 9.15 h | 24.39 h |
| Ideal parallel wall | - | - | 19.11 h |

For `1000` saved configurations per volume:

| Volume | Update time | Measurement time | Total |
|---|---:|---:|---:|
| `12^3 x 24` | 0.89 h | 0.91 h | 1.79 h |
| `16^3 x 32` | 5.06 h | 2.87 h | 7.93 h |
| `24^3 x 48` | 20.74 h | 14.52 h | 35.26 h |
| Sequential total | 26.68 h | 18.29 h | 44.98 h |
| Ideal parallel wall | - | - | 35.26 h |

The `500`-configuration plan is the recommended first production certificate:
it satisfies the strict runner's `n_cfg >= 500` loop-statistics requirement
while preserving autocorrelation control.

## Production Commands

Use `OR=3`, `separation=6`, checkpointing, and 500 saved configurations.

```bash
NUMBA_NUM_THREADS=6 python3 scripts/alpha_s_numba_wilson_loop_mc.py ensemble \
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

```bash
python3 scripts/alpha_s_numba_wilson_loop_mc.py ensemble \
  --dims 16,16,16,32 \
  --therm 1000 \
  --measurements 500 \
  --separation 6 \
  --overrelax 3 \
  --ape-steps 5 \
  --max-r 8 \
  --max-t 8 \
  --checkpoint-npz outputs/alpha_s_wilson_loop_production/ensemble_16x16x16x32_checkpoint.npz \
  --output outputs/alpha_s_wilson_loop_production/ensemble_16x16x16x32.json
```

```bash
python3 scripts/alpha_s_numba_wilson_loop_mc.py ensemble \
  --dims 24,24,24,48 \
  --therm 1000 \
  --measurements 500 \
  --separation 6 \
  --overrelax 3 \
  --ape-steps 5 \
  --max-r 8 \
  --max-t 8 \
  --checkpoint-npz outputs/alpha_s_wilson_loop_production/ensemble_24x24x24x48_checkpoint.npz \
  --output outputs/alpha_s_wilson_loop_production/ensemble_24x24x24x48.json
```

If a job is interrupted, rerun the same command with `--resume-checkpoint`.

## Remaining Work After Production Runs

1. Combine the three ensemble JSON files.
2. Run blocked jackknife/bootstrap with block size at least `11` saved
   configurations unless production autocorrelation says otherwise.
3. Fit static potentials and Sommer scale.
4. Run scheme conversion/RGE to `M_Z`.
5. Emit `outputs/alpha_s_direct_wilson_loop_certificate_2026-04-30.json`.
6. Run `scripts/frontier_alpha_s_direct_wilson_loop.py` strict mode.
