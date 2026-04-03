# Lattice Family Validation Note

**Date:** 2026-04-03  
**Status:** review-safe ordered-lattice same-family two-harness bridge

This note freezes the strongest retained ordered-lattice bridge result on the
ordered 2D lattice family.

Artifacts:

- [`scripts/lattice_family_validation.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_family_validation.py)
- [`logs/2026-04-03-lattice-family-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-family-validation.txt)
- companion distance-law note:
  [`docs/LATTICE_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_DISTANCE_LAW_NOTE.md)

## What is measured

The retained lattice read uses **one ordered-lattice family** with two
measurement harnesses:

1. **Barrier lattice**
   - Born companion audit on a same-family 3-slit Sorkin aperture
   - not the exact same 2-slit card used for MI / `d_TV` / gravity
   - MI
   - `d_TV`
   - CL-bath purity
   - gravity
   - `k=0`
2. **No-barrier lattice**
   - distance-law magnitude fit

The geometry family is the same regular 2D lattice with forward `|Δy| <= 1`
transport. The barrier / no-barrier split is a measurement-geometry change,
not a change of graph family. This is therefore a **same-family two-harness
bridge**, not a promoted one-harness unification.

## Retained barrier-lattice card

Configuration:

- `N = 40`
- half-width `= 20`
- `k = 5.0`
- barrier slits with upper/lower openings and a central closed band
- gravity row at `b = 7`

Results:

| observable | value |
|---|---:|
| `MI` | `0.537498` bits |
| `pur_min` | `0.592563` |
| `pur_cl` | `0.942834` |
| `1 - pur_cl` | `0.0572` |
| `d_TV` | `0.713772` |
| gravity | `-5.740317` |
| Born `|I3|/P` | `2.98e-16` |
| `k=0` | `0.00e+00` |
| `S_norm` | `0.783263` |

Interpretation:

- Born is machine-clean on the same-family companion Sorkin aperture, not on
  the exact same 2-slit card used for the coexistence metrics
- the `k=0` control stays exactly zero
- MI and `d_TV` are both clearly nonzero
- CL decoherence is real but modest on this family
- gravity is strong in magnitude, but the sign on this centroid read is the
  beam-depletion / opposite-shift sign rather than the naive “centroid toward
  mass” sign

## Retained no-barrier distance-law branch

On the same ordered lattice family, but without the barrier:

```text
|delta| ~= 23.5071 * b^(-1.052)
R^2 = 0.9850
```

on the far-field window `b >= 7`.

That branch is frozen separately in:

- [`docs/LATTICE_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_DISTANCE_LAW_NOTE.md)

## Safe conclusion

The ordered lattice family now supports a real same-family two-harness bridge:

- Born-clean barrier coexistence
- nontrivial MI / slit separation
- real CL-bath decoherence
- strong phase-mediated gravity
- clean `1/b`-like distance-law magnitude on the no-barrier branch

## Important limits

This is **not yet** a review-safe “all 10 properties on one family” claim.

Still missing on the ordered-lattice family:

- a same-slit attractive-gravity card on the retained two-slit coexistence
  aperture
- a retained mass-law card
- a retained large-`N` purity-scaling card
- a retained “gravity grows with `N`” card

So the safe statement is:

- **ordered lattice is now the strongest distance-law branch**
- **ordered lattice also supports a real Born-clean coexistence pocket**
- **but it remains a same-family two-harness bridge because the same-slit
  gravity-sign problem is unresolved**

## Next step

The highest-value next move is:

- build a lattice-mirror hybrid or ordered-symmetry extension that keeps the
  ordered-lattice distance law while strengthening the decoherence side

That remains the cleanest next decision test for a true one-family unification.
