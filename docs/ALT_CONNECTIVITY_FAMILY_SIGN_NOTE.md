# ALT Connectivity Family Sign Note

**Date:** 2026-04-06  
**Status:** proposed_retained bounded positive alternative connectivity family

## Artifact Chain

- [`scripts/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.py)
- [`logs/2026-04-06-alt-connectivity-family-sign.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-alt-connectivity-family-sign.txt)

## Question

Can a genuinely new structured connectivity family, distinct from the current
geometry-sector rule, preserve the old sector-style signed-source lesson on the
no-restore grown slice?

## Family

The tested family uses:

- no-restore grown geometry
- angular sector partitioning in the `y/z` plane
- a parity-rotated sector-transition map between adjacent layers

This is not the current geometry-sector rule. It is a different connectivity
construction that keeps the sector lesson but changes the layer-to-layer rule.

## Result

Controls:

- exact zero-source baseline: passed
- exact neutral `+/-` cancellation: passed
- sign orientation: passed on the retained rows
- weak charge scaling: exponent `1.000035` among passing rows

Rows:

- passed: `10/15`
- drift coverage among passes: `0.0, 0.1, 0.2, 0.3, 0.5`

The retained rows are seed-selective:

- `drift = 0.0`: `3/3` pass
- `drift = 0.1`: `1/3` pass
- `drift = 0.2`: `3/3` pass
- `drift = 0.3`: `1/3` pass
- `drift = 0.5`: `2/3` pass

## Safe Read

This is a real bounded positive alternative family, but not a family-wide
closure.

What survives:

- exact zero and neutral controls
- sign orientation
- near-linear charge response

What does not survive cleanly:

- all seeds at every tested drift
- any geometry-generic or family-wide statement

## Conclusion

The old sector-style lesson does generalize beyond the current geometry-sector
rule, but only narrowly. The parity-rotated sector-transition family is a real
alternative structured connectivity candidate on the no-restore grown slice.
