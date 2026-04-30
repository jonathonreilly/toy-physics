# Causal Distance Tail Note

**Date:** 2026-04-06  
**Status:** bounded causal-field distance-tail probe

## Artifact Chain

- [`scripts/causal_distance_tail_probe.py`](../scripts/causal_distance_tail_probe.py)
- [`logs/2026-04-06-causal-distance-tail-probe.txt`](../logs/2026-04-06-causal-distance-tail-probe.txt)
- causal propagating-field context:
  - [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](../docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)

## Question

Does the causal-field modification preserve a recognizable distance-law tail
on any retained grown family, or does the tail break once the field becomes
forward-only / finite-cone?

## Result

The exact zero-source control stays exact on every family. The broad field
cases (instantaneous, forward-only, and dynamic c=1) keep a clear
distance-law tail, but the exponent is steeply below Newtonian on every
tested family. The finite-cone dynamic c=0.5 case collapses the tail
further and acts as the clean boundary.

### center grown family

- exact zero control: `+0.000e+00`

| field | alpha | R^2 | TOWARD count |
| --- | ---: | ---: | ---: |
| instantaneous | `-1.853` | `1.000` | `5/5` |
| forward-only | `-1.928` | `1.000` | `5/5` |
| dynamic(c=1) | `-1.955` | `0.992` | `5/5` |
| dynamic(c=0.5) | `-8.734` | `0.992` | `3/5` |

Safe read:
- the broad causal-field variants remain tail-like but steeper than
  Newtonian on this family
- dynamic c=0.5 collapses the tail further, so the finite-cone case
  is the clean boundary diagnostic

### portable family 2

- exact zero control: `+0.000e+00`

| field | alpha | R^2 | TOWARD count |
| --- | ---: | ---: | ---: |
| instantaneous | `-1.874` | `1.000` | `5/5` |
| forward-only | `-1.928` | `1.000` | `5/5` |
| dynamic(c=1) | `-1.957` | `0.990` | `5/5` |
| dynamic(c=0.5) | `-8.621` | `0.991` | `3/5` |

Safe read:
- the broad causal-field variants remain tail-like but steeper than
  Newtonian on this family
- dynamic c=0.5 collapses the tail further, so the finite-cone case
  is the clean boundary diagnostic

### portable family 3

- exact zero control: `+0.000e+00`

| field | alpha | R^2 | TOWARD count |
| --- | ---: | ---: | ---: |
| instantaneous | `-1.865` | `1.000` | `5/5` |
| forward-only | `-1.927` | `1.000` | `5/5` |
| dynamic(c=1) | `-1.958` | `0.992` | `5/5` |
| dynamic(c=0.5) | `-8.644` | `0.990` | `3/5` |

Safe read:
- the broad causal-field variants remain tail-like but steeper than
  Newtonian on this family
- dynamic c=0.5 collapses the tail further, so the finite-cone case
  is the clean boundary diagnostic

## Claim Boundary

This probe does not claim a universal theorem for the causal-field
modification. It only shows that the broad forward-only / c=1 variants
keep a recognizable tail, while the finite-cone c=0.5 case breaks the
Newtonian exponent and is best treated as the boundary.

## Conclusion

The causal-field modification does not rescue a portable Newtonian
distance law. The broad variants keep a recognizable but steeper tail,
and the finite-cone c=0.5 case is the diagnosed boundary.
