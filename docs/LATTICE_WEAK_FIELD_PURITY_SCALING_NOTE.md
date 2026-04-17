# Lattice Weak-Field Purity Scaling Note

**Date:** 2026-04-03  
**Status:** retained bounded scaling law on the weak-field ordered-lattice pocket

This note freezes the purity-scaling follow-up on the reopened ordered-lattice
family.

Artifacts:

- [`scripts/lattice_weak_field_purity_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_weak_field_purity_scaling.py)
- [`logs/2026-04-03-lattice-weak-field-purity-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-weak-field-purity-scaling.txt)
- weak-field reopening note:
  [`docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md)

## Question

The weak-field reopening note showed that the dense ordered lattice has a narrow
weak-field pocket where Born stays clean, gravity is positive, and the same
two-slit family keeps nontrivial MI / decoherence.

The follow-up question here is narrower:

- does the CL-bath purity on that retained pocket show a real scaling law as `N`
  changes,
- or is the apparent exponent just a small-window descriptive fit?

## Setup

The canonical sweep uses the retained weak-field lattice family:

- ordered 2D lattice with explicit `Z2` symmetry
- standard linear propagator only
- `max_dy = 5`
- slit family `wide_center = [3, 4, 5]`
- field strength `0.0005`
- mass convention `top_slit + 1`
- `N = 20, 30, 40, 50, 60, 80, 100`
- Born reported as a same-family companion Sorkin audit, not the exact same
  two-slit aperture card used for MI / `d_TV` / gravity

## Canonical Rows

| `N` | `MI` | `d_TV` | `1 - pur_cl` | gravity@`b=6` | Born `|I3|/P` | `k=0` | retain |
|---|---:|---:|---:|---:|---:|---:|---|
| 20 | `0.712` | `0.894` | `0.490` | `+0.0501` | `5.35e-16` | `0` | no |
| 30 | `0.684` | `0.878` | `0.482` | `+0.0879` | `5.59e-16` | `0` | yes |
| 40 | `0.617` | `0.839` | `0.465` | `+0.1627` | `4.24e-16` | `0` | yes |
| 50 | `0.556` | `0.800` | `0.446` | `+0.2217` | `4.44e-16` | `0` | yes |
| 60 | `0.514` | `0.769` | `0.431` | `+0.2828` | `1.03e-15` | `0` | yes |
| 80 | `0.424` | `0.697` | `0.397` | `+0.4081` | `9.88e-16` | `0` | yes |
| 100 | `0.360` | `0.639` | `0.369` | `+0.5218` | `5.36e-16` | `0` | yes |

The canonical `N=40` row matches the weak-field reopening note:

- `MI = 0.617`
- `d_TV = 0.839`
- `1 - pur_cl = 0.465`
- gravity at `b = 6` is `+0.1627`
- Born `4.24e-16`
- `k=0 = 0`

## Fit

Using the retained rows only, the purity complement fits:

```text
1 - pur_cl ~= 1.0467 * N^(-0.222)
R^2 = 0.9683
```

If all rows are included, the fit is slightly shallower:

```text
1 - pur_cl ~= 0.8705 * N^(-0.178)
R^2 = 0.9131
```

## Interpretation

This is a **real retained bounded scaling law**, not a one-off fluke:

- the retained rows are Born-clean
- `k=0` remains exactly zero
- MI and decoherence remain nontrivial
- gravity stays positive on the retained rows
- the retained-row exponent is stable enough to be review-safe on the tested
  window

But it is still **bounded**, not asymptotic:

- the fitted exponent is modest, not dramatic
- `N=20` misses the retained pocket
- the fit should be read as a retained-window law on the weak-field pocket,
  not a universal theorem for all `N`

## Safe Conclusion

The weak-field ordered-lattice pocket now supports:

- a review-safe Born-clean coexistence row
- a retained weak-field purity-scaling law on the same family
- a positive-gravity pocket on the same linear propagator

So the right synthesis wording is:

- **ordered lattice has a narrow weak-field retained pocket with a bounded but
  real purity-scaling law**

Do **not** promote this to a blanket lattice theorem or a full one-family
unification claim.
