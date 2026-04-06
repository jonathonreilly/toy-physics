# Causal Source Placement Robustness Note

**Date:** 2026-04-06  
**Status:** diagnosed deeper boundary: family-aware source placement changes the causal ratios, but it does not restore a clean portable causal-field signal across all three families

## Artifact Chain

- [`scripts/causal_source_placement_robustness.py`](/Users/jonreilly/Projects/Physics/scripts/causal_source_placement_robustness.py)
- [`logs/2026-04-06-causal-source-placement-robustness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-causal-source-placement-robustness.txt)
- retained causal-field context:
  - [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)
  - [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)
  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)

## Question

The low-SNR cross-family replay used a fixed nominal anchor target `(y, z) =
(0, 3)` and produced a family split. Does a family-aware source-placement rule
restore the causal-field signal more cleanly, or does the boundary remain?

This probe compares three placement rules:

- fixed nominal target: `(0, 3)`
- family source-layer centroid registration
- family source-layer ordinal / median registration

The observable is still the final-layer detector centroid `y` shift relative
to the free propagation baseline.

## Frozen Result

Exact-zero control:

- max `|delta_y| = 0.000e+00` across all families and all placement rules
- max `|field| = 0.000e+00` across all families and all placement rules

Placement comparison:

| family | placement | forward / inst | dynamic(c=1) / inst | dynamic(c=0.5) / inst |
| --- | --- | ---: | ---: | ---: |
| center grown family | fixed nominal | `0.029` | `-0.394` | `-0.402` |
| center grown family | family centroid | `0.406` | `0.462` | `0.126` |
| center grown family | family ordinal | `2.124` | `2.670` | `2.363` |
| portable family 2 | fixed nominal | `0.350` | `0.529` | `0.506` |
| portable family 2 | family centroid | `1.017` | `1.399` | `1.488` |
| portable family 2 | family ordinal | `0.938` | `1.027` | `1.042` |
| portable family 3 | fixed nominal | `0.060` | `-0.255` | `0.042` |
| portable family 3 | family centroid | `0.363` | `-0.147` | `1.237` |
| portable family 3 | family ordinal | `2.276` | `2.891` | `1.713` |

## Safe Read

What survives:

- the exact zero-source control survives in every placement rule
- the family-aware placements do change the measured ratios, so the harness is
  not blind to source registration

What does not survive:

- no family-aware rule restores the center-family causal-field scale cleanly
- the nominal anchor remains a low-SNR boundary
- the centroid and ordinal family-aware registrations shift the numbers, but
  they do not produce a single portable cross-family causal-field law

## Boundary Call

The best family-aware registration is useful diagnostically, but it does not
turn the causal-field observable into a clean cross-family portability law.

The fixed nominal anchor replay was not just a bad choice of target; the
family-aware rules expose a deeper placement-sensitive boundary:

- fixed nominal: low-SNR boundary
- family centroid: shifted boundary, not a rescue
- family ordinal: shifted boundary, not a rescue

## Final Verdict

**diagnosed deeper boundary: family-aware source placement changes the
measured causal ratios, but it does not restore a clean portable causal-field
signal across all three families**
