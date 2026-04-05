# Wave Amplification Near Horizon

**Date:** 2026-04-05  
**Status:** bounded negative against the stronger near-horizon amplification claim on the retained exact-lattice harness

## Artifact chain

- [`scripts/wave_amplification_near_horizon.py`](/Users/jonreilly/Projects/Physics/scripts/wave_amplification_near_horizon.py)
- [`logs/2026-04-05-wave-amplification-near-horizon.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-wave-amplification-near-horizon.txt)

## Question

Does the oscillating retarded-source signal become genuinely amplified near the
absorptive trapping threshold, or were the earlier large ratios mostly a
small-denominator artifact?

This note is intentionally narrow:

- one family: exact 3D lattice
- one comparison: static retarded source vs oscillating retarded source
- one absorber sweep: `alpha`
- one safety check: always read the ratio alongside the raw static deflection

## Frozen result

The frozen harness uses:

- exact 3D lattice with `h = 0.5`, `W = 6`, `L = 30`
- `s = 0.1`
- finite field speed `c = 0.8`
- oscillation period `T = 8`
- oscillation amplitude `A = 2`

Frozen readout:

| `alpha` | static deflection | wave deflection | `|wave/static|` | escape |
| --- | ---: | ---: | ---: | ---: |
| `0.00` | `-7.764007e-01` | `-5.676026e-01` | `0.731` | `1.552` |
| `0.50` | `-3.468626e+00` | `-3.508877e+00` | `1.012` | `0.009` |
| `0.80` | `-4.053685e+00` | `-4.044895e+00` | `0.998` | `0.002` |
| `1.00` | `-4.246098e+00` | `-4.236546e+00` | `0.998` | `0.001` |
| `2.00` | `-4.567770e+00` | `-4.582237e+00` | `1.003` | `0.000` |

Largest ratio on the retained harness:

- `1.012` at `alpha = 0.50`

## Safe read

The strongest retained statement is:

- on this retained exact-lattice harness, the oscillating-source signal is
  **not** dramatically amplified near the absorptive threshold
- the retained ratio stays close to `1x`
- the earlier 5x to 1000x narrative does not survive this sanity check

## Honest limitation

This is a bounded negative only for this exact harness.

- it does not prove every possible oscillating-source / trapping combination is
  flat
- it does show that the stronger amplification story is not currently retained
  on the main exact-lattice replay

## Branch verdict

Treat this as another useful overclaim-killer:

- the retarded-field branch still has real bounded observables
- but the strong near-horizon wave-amplification headline is not currently
  supported by a retained harness
