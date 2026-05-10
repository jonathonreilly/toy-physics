# Causal Field Portability Note

**Date:** 2026-04-06 (audit-status note added 2026-05-10)
**Status:** bounded portability probe — exact-null control plus diagnosed family boundary on the configured fixed-anchor cross-family replay; not a cross-family portability law.

## Artifact Chain

- [`scripts/causal_field_portability_probe.py`](../scripts/causal_field_portability_probe.py)
- [`logs/2026-04-06-causal-field-portability-probe.txt`](../logs/2026-04-06-causal-field-portability-probe.txt)
- causal propagating-field context:
  - [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)

## Audit-status note (2026-05-10)

The 2026-05-04 audit verdict (`audited_conditional`, chain_closes=false)
confirmed that the runner genuinely computes the reported ratios over
families, seeds, fields, and detector centroids rather than printing
constants, but flagged a missing-dependency edge: the runner imports
the structured-growth, propagation, and detector-centroid operators
from `evolving_network_prototype_v6.py`, and the audit packet does
not provide an executable certificate that those imports implement
the intended axiom-level operators.

> "the restricted packet does not include the implementation of
> build_structured_growth, propagate, or centroid_y from
> evolving_network_prototype_v6. Without that imported module, the
> derivation from the stated framework primitive cannot be independently
> closed inside the packet."

Admitted-context inputs (carrier framework, not derived in this note):

- `build_structured_growth` (drift / restore grown geometry constructor
  on the H=0.5 family, parameterised by `(N_LAYERS, HALF, drift, restore, seed)`)
- `propagate` (forward amplitude propagation on the layered DAG with
  background scalar field)
- `centroid_y` (final-layer detector centroid readout)

Configured probe parameters (proxy thresholds, not derived):

- three grown families with drift/restore pairs `(0.20, 0.70)`,
  `(0.05, 0.30)`, `(0.50, 0.90)` labeled center / portable-2 / portable-3
- six seeds, source anchor target `(y, z) = (0, 3)` at
  `SOURCE_LAYER = 2 * N_LAYERS // 3`
- field strength `5e-5`, field epsilon `0.1`, dynamic cone values
  `c ∈ {1.0, 0.5}`
- forward-only ratio spread `0.423` and dynamic(c=0.5)/instantaneous
  spread `0.352` interpreted as the family-boundary diagnostic on this
  configured probe

Blocked-on: this note stays `audited_conditional` until either
`evolving_network_prototype_v6.py` is registered as a retained
framework-operator carrier with executable verification of
`build_structured_growth`, `propagate`, and `centroid_y` against
the named axiom-level operators, or a retained portability-criterion
theorem is supplied that derives the configured probe metric and
threshold from the framework primitives. The bounded computational
diagnostic — exact-null control survives, and the configured
forward-only and dynamic-cone ratios split across the three
configured grown families — is unaffected by this status note.

## Question

Does the causal propagating-field observable from the center grown family stay
portable onto the second and third portable families under exact-null control,
or do the ratios diagnose a family boundary?

## Result

The exact-null control stays exact on all three families:

- max `|delta_y|` across families: `0.000e+00`
- max `|field|` across families: `0.000e+00`

The retained center family keeps the original forward-only scale, but the
other two families do not track it cleanly:

| family | inst delta | forward delta | forward / inst | dynamic(c=0.5) / inst |
| --- | ---: | ---: | ---: | ---: |
| center grown family | `2.921e-07` | `1.951e-07` | `0.668` | `0.938` |
| portable family 2 | `4.802e-07` | `1.758e-07` | `0.366` | `0.728` |
| portable family 3 | `1.927e-07` | `1.522e-07` | `0.790` | `1.080` |

## Safe Read

What survives:

- the exact-null control is stable and exact on the replay
- the center family keeps the retained forward-only causal-field behavior

What does not survive:

- the second and third portable families do not sit on the same forward-only
  ratio as the center family
- the finite-cone ratio also moves enough to break a clean cross-family
  portability claim

## Boundary Call

The spread is large enough to freeze the claim as a diagnosed family boundary:

- forward-only ratio spread across the three families: `0.423`
- dynamic(c=0.5)/instantaneous ratio spread: `0.352`

So the current causal-field observable is real on the center family, but it is
not yet a cross-family portability law on the second and third portable
families.

## Final Verdict

**bounded computational diagnostic on the configured fixed-anchor probe:
the exact-null control survives, and the configured forward-only and
dynamic-cone ratios split across the three configured grown families
rather than tracking a cross-family portability law. This is the result
of a probe with the fixed parameters and source anchor listed in the
audit-status note above, not a derivation of a portability law from
framework primitives.**
