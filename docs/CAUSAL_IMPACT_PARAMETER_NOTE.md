# Causal Impact-Parameter Note

**Date:** 2026-04-06  
**Status:** bounded causal-field impact-parameter probe on the proposed_retained center grown family

## Artifact Chain

- [`scripts/causal_impact_parameter_probe.py`](../scripts/causal_impact_parameter_probe.py)
- [`logs/2026-04-06-causal-impact-parameter-probe.txt`](../logs/2026-04-06-causal-impact-parameter-probe.txt)
- causal-field context:
  - [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](../docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)
  - [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](../docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)

## Question

Does the retained causal-field modification preserve a recognizable
impact-parameter deflection law on the retained center grown family when
the field is instantaneous, forward-only, or finite-cone dynamic?

## Result

- exact zero control: `delta = +0.000e+00`
- exact zero field max: `+0.000e+00`

| field | alpha | R^2 | TOWARD count |
| --- | ---: | ---: | ---: |
| instantaneous | `-0.067` | `0.832` | `5/5` |
| forward-only | `-0.077` | `0.812` | `5/5` |
| dynamic(c=1) | `-0.100` | `0.807` | `5/5` |
| dynamic(c=0.5) | `-0.084` | `0.687` | `5/5` |

## Safe Read

The impact-parameter sweep is real on the retained center grown family,
but the causal variants do not all behave the same way.

The broad variants do not preserve a recognizable `~1/b` law on this family.
The finite-cone variant is the boundary.

## Diagnostic Snapshot

- instantaneous tail-like exponent: `-0.067`
- forward-only tail-like exponent: `-0.077`
- dynamic(c=1) tail-like exponent: `-0.100`
- dynamic(c=0.5) exponent: `-0.084`

## Narrow Conclusion

The causal-field modification does not preserve a recognizable impact-parameter law shape on the retained center grown family.
The finite-cone dynamic case is the diagnosed boundary.
