# Diamond Phase-Ramp Bridge Card Note

**Date:** 2026-04-06  
**Status:** proxy-level bridge card, not an absolute NV claim

## Artifact Chain

- [`scripts/diamond_phase_ramp_bridge_card.py`](/Users/jonreilly/Projects/Physics/scripts/diamond_phase_ramp_bridge_card.py)
- [`docs/DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md)
- [`docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md)
- [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md)
- [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PREDICTION_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_V2_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)

## Question

Can we turn the retained exact-family phase-ramp results into the cleanest
possible diamond/NV handoff card, while keeping the claim surface strictly
proxy-level?

## Bridge Row

The highlighted retained row is the exact-family phase-ramp point at
`s = 0.004`.

The proxy phasor is written in normalized in-repo units, not lab counts:

| quantity | raw proxy | normalized vs `s = 0.001` reference |
| --- | ---: | ---: |
| `X` | `-0.966` | `-1.308` |
| `Y` | `-0.259` | `+0.384` |
| `phi` | `-2.880 rad` | `+3.892` |
| phase-ramp slope | `-0.4925 rad / z` | `+4.053` |

Interpretation:

- the raw proxy row is the retained exact-family phase-ramp point
- the normalized columns are relative to the retained `s = 0.001` reference
- the sign structure is what matters here, not any absolute NV amplitude

## Source-Strength Sweep

The retained exact-family phase-ramp law is source-strength sensitive:

| `s` | `phi` (rad) | ramp slope (rad / z) | `phi / s` | `slope / s` | `wave/same` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `-0.740` | `-0.1215` | `-740.0` | `-121.5` | `60.022` |
| `0.0020` | `-1.473` | `-0.2444` | `-736.5` | `-122.2` | `60.604` |
| `0.0040` | `-2.880` | `-0.4925` | `-720.0` | `-123.1` | `60.707` |
| `0.0080` | `+0.337` | `-1.0274` | `+42.1` | `-128.4` | `55.887` |

The source-strength ladder says:

- the phase lag stays coherent on the retained exact family
- the phase-ramp slope steepens with source strength
- the detector response remains far above the same-site control

## Nearby Separation Change

The retained exact-family mechanism note also gives a nearby depth /
separation scan:

| layer | depth | phase lag (rad) | ramp slope (rad / z) | `R^2` |
| --- | ---: | ---: | ---: | ---: |
| `1` | `31` | `-0.589` | `-0.2422` | `0.969` |
| `2` | `30` | `-0.696` | `-0.2718` | `0.967` |
| `3` | `29` | `-0.793` | `-0.2989` | `0.966` |
| `4` | `28` | `-0.877` | `-0.3226` | `0.965` |

This is the smallest nearby separation change that is already retained in-repo:

- the ramp steepens as the source moves closer to the detector plane
- the phase lag becomes more negative in lockstep
- the coherence stays high

## What This Does And Does Not Say

What it does say:

- the retained exact-family phase-ramp observable is coherent
- the card can be written in a calibration-friendly form
- the strongest tightening handle is the normalized phase-ramp slope

What it does not say:

- no absolute NV counts
- no lab noise-floor estimate
- no validated transfer coefficient
- no claim that the proxy phasor is already a physical readout budget

## Narrow Conclusion

The repo now has a clean diamond/NV bridge card in proxy units:

- one highlighted exact-family row
- one source-strength ladder
- one nearby depth / separation ladder
- the absolute NV conversion remains external calibration work

So the best current handoff is:

**bridge-ready in proxy units, with the normalized phase-ramp slope as the
cleanest calibration handle; absolute NV units are still blocked by the missing
transfer coefficient**
