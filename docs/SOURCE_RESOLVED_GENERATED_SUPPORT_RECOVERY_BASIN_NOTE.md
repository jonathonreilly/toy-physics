# Source-Resolved Generated Support Recovery Basin Note

**Date:** 2026-04-05  
**Status:** tiny basin probe around the proposed_retained generated-family support recovery

## Artifact chain

- [`scripts/source_resolved_generated_support_recovery_basin.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_support_recovery_basin.py)

## Question

Is the retained generated-family support recovery a one-point fluke or a small
basin around the current `kNN`-floor tweak?

This probe stays deliberately narrow:

- compact generated 3D DAG family
- tiny grid around the retained positive connectivity tweak
- one centroid-sign observable
- one detector-support observable

## Frozen result

The probe sweeps a tiny `k_nearest / min_edges` grid around the retained
positive tweak and records only:

- sign count
- `support_frac` above `1%` of peak

The frozen readout is:

| `k_nearest` | `min_edges` | centroid shift | sign | `support_frac` |
| --- | --- | ---: | --- | ---: |
| `2` | `4` | `+6.221421e-01` | `4/4` TOWARD | `0.448` |
| `2` | `5` | `+3.089781e-01` | `3/4` TOWARD | `0.448` |
| `2` | `6` | `+5.032603e-01` | `4/4` TOWARD | `0.427` |
| `3` | `4` | `+8.042905e-01` | `4/4` TOWARD | `0.458` |
| `3` | `5` | `+3.850909e-01` | `3/4` TOWARD | `0.458` |
| `3` | `6` | `+5.025787e-01` | `4/4` TOWARD | `0.438` |
| `4` | `4` | `+3.592356e-01` | `3/4` TOWARD | `0.438` |
| `4` | `5` | `+9.208924e-02` | `2/4` TOWARD | `0.448` |
| `4` | `6` | `+3.692716e-01` | `3/4` TOWARD | `0.438` |

## Safe read

The positive region persists over more than one nearby point:

- every point in the tiny scanned basin remains `TOWARD`
- support fraction stays above the baseline `0.311`
- the best support fraction in the sweep is `0.458`

So the generated-family rescue is not a one-point fluke.

## Honest limitation

This probe does not test a new field architecture.

It only asks whether the current generated-family support recovery has:

- a tiny basin of stability
- or just a single tuned positive point

## Branch verdict

Treat this as the basin-level check for the generated-family rescue attempt.
The strongest useful outcome is a small retained positive basin; that is what
the frozen grid now shows.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [source_resolved_generated_support_recovery_note](SOURCE_RESOLVED_GENERATED_SUPPORT_RECOVERY_NOTE.md)
- [source_resolved_generated_family_probe_note](SOURCE_RESOLVED_GENERATED_FAMILY_PROBE_NOTE.md)
- [source_resolved_generated_support_mass_scaling_note](SOURCE_RESOLVED_GENERATED_SUPPORT_MASS_SCALING_NOTE.md)
