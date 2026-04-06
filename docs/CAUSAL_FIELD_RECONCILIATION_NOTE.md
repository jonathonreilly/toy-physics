# Causal Field Reconciliation Note

**Date:** 2026-04-06  
**Status:** diagnosed harness boundary for the fixed-anchor cross-family replay; retained center-family causal-field result remains valid

## Artifact Chain

- [`scripts/causal_field_portability_probe.py`](/Users/jonreilly/Projects/Physics/scripts/causal_field_portability_probe.py)
- [`logs/2026-04-06-causal-field-portability-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-causal-field-portability-probe.txt)
- [`logs/2026-04-06-causal-field-reconciliation-diagnostic.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-causal-field-reconciliation-diagnostic.txt)
- retained causal-field note:
  - [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- portability boundary note:
  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)

## Question

The retained causal-field note says the dynamic `c=0.5` cone gives a stable
`~0.45` observable on the center grown family and preserves the crossover.
The low-SNR cross-family replay, however, reported a family boundary.

Are these results contradictory, or are they probing different regimes?

## Diagnosis

They are not the same measurement in practice.

The retained `c=0.5` result is a center-family causal-field observable in a
regime where the dynamic cone signal is already resolved and stable.

The portability probe fixes a single nominal source target
`(y, z) = (0, 3)` at `source_layer = 8` and reuses that same target across
the three grown families. That means the actual selected source node shifts
slightly family-to-family even though the nominal target is fixed.

The diagnostic log shows the resulting issue clearly:

- the exact-null control remains exact
- but the centroid shifts are only `O(10^-7)` to `O(10^-6)`
- the associated standard errors are of comparable size
- the `dynamic(c=0.5)/instantaneous` ratio therefore becomes source-placement
  sensitive and can even flip sign across families

The small-signal ratio is not stable enough to override the retained
center-family result.

## What Causes The Mismatch

Primary cause:
- fixed source placement across different growth families

Secondary cause:
- low-SNR centroid observable in the replay

Not the main cause:
- seed handling
- zero-control failure
- a field-strength-only effect

The field-strength scan in the reconciliation diagnostic shows that the
family-specific ratios do not collapse to the retained `~0.45` value simply
by increasing strength within the same fixed-anchor replay. So this is not
just a single bad strength window.

## Safe Conclusion

The low-SNR cross-family replay is trustworthy as a **diagnosis of the fixed
anchor replay harness boundary**, but not as a refutation of the retained
center-family causal-field result.

So the correct retained split is:

- **retained positive:** the center-family dynamic causal cone observable
  with `c=0.5` and preserved crossover
- **diagnosed boundary:** the same fixed-anchor replay does not stay portable
  across all three families

## Recommended Next Step

If we want to push this lane further, the next discriminating test should use
either:

- family-registered source placement, or
- a higher-SNR observable that does not rely on tiny centroid differences

That would tell us whether the family boundary is fundamental or just an
artifact of the fixed-anchor replay geometry.
