# SU(3) L_s=2 Z3 APBC Variant Probe

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support calculation over named exploratory APBC variants, unaudited.
**Primary runner:** `scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py`

## Question

[`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md)
shows that the existing L_s=2 APBC implementation is numerically the same as
the all-forward L_s=2 PBC candidate:

```text
P_cube(beta=6) = 0.4291049969.
```

That note leaves one implementation question open: whether the framework's
APBC wording should include explicit Z3 center-twist phase factors for
non-self-conjugate SU(3) sectors.

This note preserves the narrow runner-backed result from the closed campaign
packet: three named Z3 phase variants were tried, and none closes the bridge.
This is not a definition of the repo's APBC convention.

## Result

The runner evaluates the same source-sector Perron solve as the full-rho
reference after modifying the candidate environment weights by named Z3
phase factors:

| Variant | P(beta=6) | Gap to 0.5935306800 | Gap / epsilon_witness |
|---|---:|---:|---:|
| PBC reference | 0.4291049969 | 0.1644 | 543x |
| Z3 symmetric APBC | 0.4291049969 | 0.1644 | 543x |
| Z3 one-direction APBC | 0.4191656069 | 0.1744 | 575x |
| Z3 cocycle APBC | 0.4291049969 | 0.1644 | 543x |

No named variant lands within `epsilon_witness = 3.03e-4`, or even within
`0.05`, of the bridge-support comparator.

## Interpretation

For the closed L_s=2 cube, uniform Z3 twists cancel globally in the tested
partition-function weights. The one-direction toy twist moves the value away
from the comparator rather than toward it.

The bounded conclusion is only:

> the three named Z3 APBC phase variants tested by the runner do not close the
> L_s=2 cube bridge gap.

The note does not prove that every possible APBC implementation is equivalent
to PBC. A non-trivial APBC effect would require additional framework
specification, for example a non-uniform twist, a non-Z3 boundary projection,
or an open-boundary convention. Those are framework-spec questions, not
derived outputs of this calculation.

## Scope

In scope:

- PBC reference reproduction against the landed full-rho value.
- Z3 symmetric, one-direction, and cocycle phase probes.
- Numeric no-closure result for those named probes.

Out of scope:

- adopting any APBC phase convention as repo authority;
- proving an all-APBC no-go theorem;
- promoting the bridge parent chain;
- deriving the plaquette comparator.

## Audit Consequence

```yaml
claim_id: su3_z3_apbc_variant_probe_2026-05-04
note_path: docs/SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md
runner_path: scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_cube_full_rho_perron_2026-05-04
```
