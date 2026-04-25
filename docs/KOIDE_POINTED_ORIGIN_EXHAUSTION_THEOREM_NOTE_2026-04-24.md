# Koide Pointed-Origin Exhaustion Theorem

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py`
**Status:** retained support/no-go theorem. This note does **not** close the
dimensionless charged-lepton Koide lane.

## Decision

The reviewed `koide-dimensionless-closure-proposal` branch contains one
landable result: within the current residual Koide atlas, unpointed retained
data cannot select the closing representative.

The stronger branch claim,

```text
physical source/boundary origin law is already derived
-> Q = 2/3 and delta = 2/9 are retained/native closure
```

is not landed. It still requires the physical theorem identifying the
charged-lepton readout with background-zero / `Z`-erasure, the physical
Brannen endpoint with selected-line local boundary-source support, and the
open endpoint readout with a based endpoint section.

## Theorem

Let the residual dimensionless Koide atlas carry three unpointed freedoms:

```text
Q source-response:       background-source translation
Brannen endpoint:        CP1/selected-line source choice in the rank-two primitive
open endpoint readout:   endpoint torsor translation
```

Then the retained unpointed tests are invariant along these fibres, while the
open charged-lepton readouts change. Therefore origin-free retained data do
not force the simultaneous closing representative

```text
physical background source = 0 / Z erased
selected-line local boundary source selected
endpoint torsor basepoint = 0
```

The next positive theorem remains a retained physical source/boundary-origin
law, not a value-matching argument.

## Exact Checks

### Q source-origin fibre

On the normalized residual response slice,

```text
Y = (1+a, 1-a),
Q = (1 + Y_perp/Y_plus)/3.
```

The Koide value is selected only at `a = 0`:

```text
Q = 2/3  <=>  a = 0.
```

But finite polynomial invariants of an unpointed translation fibre are
constant:

```text
P(a+r) = P(a) for all r  =>  P is constant.
```

Thus unpointed source data cannot choose the zero-background / `Z`-erased
representative.

### Brannen endpoint line fibre

On the real nontrivial `Z3` primitive, the only trace-one symmetric mark
commuting with the retained `120 degree` rotation is `I/2`. This scalar mark is
not a rank-one CP1 projector and is blind to CP1 line angle. A rank-one line
choice therefore remains extra boundary data unless a retained descent or
absence theorem removes it.

### Endpoint torsor fibre

Before a unit basepoint is selected, the open endpoint coordinate is a torsor:

```text
R_c(phi) = phi + c.
```

Differences and affine gluing are invariant under `c` translation. Finite
polynomial invariants of the translation action cannot choose `c = 0`.

## Consequence

The zero representative would imply the dimensionless values:

```text
Q = 2/3
delta = eta_APS = 2/9
```

But this theorem proves only necessity and atlas exhaustion, not the missing
positive physical law. The branch's positive closure/review packet is therefore
demoted to an open proposal.

## Explicit Non-Claims

- Does not claim retained/native Koide dimensionless closure.
- Does not derive the physical background-zero / `Z`-erasure law for `Q`.
- Does not derive the selected-line local boundary-source law for `delta`.
- Does not derive the open endpoint section as based/unit-preserving.
- Does not address the separate overall lepton scale `v_0`.

## Verification

```bash
python3 scripts/frontier_koide_pointed_origin_exhaustion_theorem.py
```

Expected closeout:

```text
KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM=TRUE
RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE
POINTED_ORIGIN_LAW_WOULD_CLOSE_DIMENSIONLESS_LANE_WITHIN_RESIDUAL_ATLAS=TRUE
POINTED_ORIGIN_LAW_IS_NECESSARY_WITHIN_RESIDUAL_ATLAS=TRUE
KOIDE_DIMENSIONLESS_LANE_CLOSED_BY_THIS_RUNNER=FALSE
RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws
NEXT_THEOREM=derive_physical_source_boundary_origin_laws_from_retained_charged_lepton_physics
```
