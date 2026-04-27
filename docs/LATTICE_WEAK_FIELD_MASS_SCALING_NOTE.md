# Lattice Weak-Field Mass-Scaling Note

**Date:** 2026-04-03  
**Status:** proposed_retained sub-linear mass-response on the weak-field ordered-lattice pocket

This note freezes the weak-field mass-scaling follow-up on the ordered lattice.
It answers a narrow question:

- does the retained weak-field pocket support a genuine `F∝M` law, or only a
  positive but sub-linear response to the mass proxy?

Artifacts:

- [`scripts/lattice_weak_field_mass_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_weak_field_mass_scaling.py)
- [`logs/2026-04-03-lattice-weak-field-mass-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-weak-field-mass-scaling.txt)
- upstream reopening note:
  [`docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md)

## Mass encoding

The canonical mass proxy in this chain is **field strength**, not node count.

- node count is held fixed
- the sweep changes the strength of one fixed mass node
- this keeps the question focused on amplitude response rather than mass-size
  confounds

## Setup

- ordered 2D lattice with explicit `Z2` symmetry
- standard linear propagator only
- canonical family: `max_dy = 5`, `wide_center` slit family
- fixed mass position: the same `top_row + 1` convention used in the retained
  weak-field reopening note
- field-strength sweep:
  - `1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4`
- same-family Born companion audit retained from the lattice harness

## Canonical row

The canonical row is the top end of the retained weak-field pocket:

- `max_dy = 5`
- `slit = wide_center`
- `strength = 0.0005`

Readout:

| observable | value |
|---|---:|
| `MI` | `0.616978` |
| `d_TV` | `0.839206` |
| `1 - pur_cl` | `0.464598` |
| gravity | `+0.162694` |
| Born `|I3|/P` | `4.24e-16` |
| `k=0` | `0.00e+00` |
| positive gravity points | `11/11` |
| barrier-harness tail fit | `alpha = -1.00`, `R^2 = 0.93` |

## Mass-response sweep

The sweep is monotonic and positive throughout:

| strength | MI | `1-pur_cl` | gravity | Born | retain |
|---|---:|---:|---:|---:|---|
| `1e-5` | `0.564` | `0.445` | `+0.0428` | `4.24e-16` | yes |
| `2e-5` | `0.568` | `0.446` | `+0.0588` | `4.24e-16` | yes |
| `5e-5` | `0.576` | `0.450` | `+0.0874` | `4.24e-16` | yes |
| `1e-4` | `0.584` | `0.453` | `+0.1144` | `4.24e-16` | yes |
| `2e-4` | `0.596` | `0.458` | `+0.1428` | `4.24e-16` | yes |
| `5e-4` | `0.617` | `0.465` | `+0.1627` | `4.24e-16` | yes |

Power-law fit:

```text
gravity = 2.6960 * strength^0.353
R^2 = 0.971
```

## Interpretation

This is a real retained mass-response, but it is **sub-linear**.

- Born stays machine-clean on every tested row
- `k=0` stays exactly zero
- MI and decoherence stay nontrivial throughout the sweep
- gravity stays positive throughout the sweep
- the response grows with mass proxy, but the exponent is far below `1`

So the safe conclusion is:

- the weak-field ordered-lattice pocket retains a genuine positive mass-response
- but the `F∝M` claim should **not** be promoted on this chain
- the retained result is a **bounded sub-linear response**, not a linear law

## Project-level read

The ordered-lattice branch now has two distinct retained bridge results:

1. a weak-field coexistence pocket with Born, MI, decoherence, and positive gravity
2. a separate ordered-lattice distance-law branch on the no-barrier harness

This mass-scaling note strengthens the first of those, but it does not turn the
ordered lattice into a fully unified one-card architecture.

The safest synthesis wording is:

- ordered lattice retains a narrow weak-field mass-response pocket
- the response is positive and review-safe
- the response is sub-linear, so `F∝M` is not promoted

