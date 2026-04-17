# Connectivity Family V2 Elliptical Duplicate Note

**Date:** 2026-04-06  
**Status:** diagnostic duplicate of the portable sign-law fixed point; not a new retained family

## Artifact Chain

- [`scripts/CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP.py)
- [`scripts/CONNECTIVITY_FAMILY_V2_BASIN.py`](/Users/jonreilly/Projects/Physics/scripts/CONNECTIVITY_FAMILY_V2_BASIN.py)
- [`scripts/CONNECTIVITY_FAMILY_V2_FM_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/CONNECTIVITY_FAMILY_V2_FM_TRANSFER.py)
- [`scripts/CONNECTIVITY_FAMILY_V2_FAILURE_AUDIT.py`](/Users/jonreilly/Projects/Physics/scripts/CONNECTIVITY_FAMILY_V2_FAILURE_AUDIT.py)
- [`logs/2026-04-06-connectivity-family-v2-elliptical-targeted.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-connectivity-family-v2-elliptical-targeted.txt)
- retained invariant: [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
- out-of-band holdout: [`docs/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_NOTE.md)

## Question

Does a parity-tapered elliptical-shell connectivity rule on the no-restore grown
slice produce a second independent sign-law family beyond the portable sign-law
invariant already retained on main?

## Targeted Rows

Low-drift rows on the same slice are clean:

- `drift=0.00, seed=0`
- `drift=0.02, seed=0`
- `drift=0.05, seed=0`
- `drift=0.10, seed=0`

These rows keep:
- exact zero-source baseline
- exact neutral same-point cancellation
- plus/minus antisymmetry
- weak-field `F~M = 1.000`

## Boundary Rows

Nearby rows do not broaden the family:

- `drift=0.15, seed=1`
- `drift=0.05, seed=1`
- `drift=0.10, seed=1`

These rows keep the exact zero / neutral controls, but they flip sign
orientation and fail the exact gate.

## Safe Read

This ellipse-tapered rule is not a new retained family.

It reproduces the already-retained portable sign-law fixed point on a narrow
seed-0 slice, and the nearby seed-1 rows fall over at the sign-orientation
boundary. In other words:

- the control surface is real
- the weak-field slope is real
- the family does not broaden beyond the retained sign-portability invariant

So this lane is best read as a **diagnostic duplicate**, not a second
independent structured family.

## Relation to the Retained Invariant

The result sits inside the same control surface summarized in
[`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md):

- exact zero-source cancellation
- exact neutral cancellation
- plus/minus antisymmetry
- weak-field response pinned near unit slope

The elliptical-shell geometry only changes the basin width and the seed-local
selectivity. It does not add a new order parameter.

## Final Verdict

**diagnosed duplicate boundary: the parity-tapered elliptical-shell family
reproduces the portable sign-law fixed point on a narrow slice, but it does not
produce a new independent retained family**
