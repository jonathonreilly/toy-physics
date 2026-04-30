# Lattice Field-Strength Unification Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note

This note freezes the follow-up that rechecks the ordered-lattice symmetry
decision after adding the missing field-strength axis.

Artifacts:

- [`scripts/lattice_field_strength_unification.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_field_strength_unification.py)
- [`logs/2026-04-03-lattice-field-strength-unification.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-field-strength-unification.txt)
- prior fixed-strength decision:
  [`docs/LATTICE_SYMMETRY_UNIFICATION_DECISION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_SYMMETRY_UNIFICATION_DECISION_NOTE.md)

## Question

The fixed-strength lattice decision was negative:

- Born stayed clean
- MI and decoherence stayed real
- but positive gravity never appeared on the symmetric two-slit card

The new question is narrower:

- was that truly a geometry limit,
- or was the standard field strength simply too large for coherent lattice
  transport?

## Setup

- same ordered 2D lattice + explicit `Z2` symmetry family
- standard linear propagator only
- dense sweep over `max_dy = 4, 5, 6`
- slit families:
  - `narrow_center = [4]`
  - `wide_center = [3, 4, 5]`
  - `wide_outer = [4, 5, 6]`
- mass convention: `top_slit + 1`
- strength sweep:
  - `0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1`
- same detector centroid read as the prior decision
- Born reported as a same-family companion Sorkin audit, not the exact same
  two-slit aperture card

Retained row criteria:

- Born companion audit `<= 1e-12`
- `k=0` control `<= 1e-9`
- nontrivial MI
- nontrivial decoherence
- positive gravity at **all** tested `b`
- decaying barrier-harness distance tail with `R^2 >= 0.80`

## Canonical Reopening Row

To keep continuity with the prior decision note, the canonical promoted row uses
the same slit family as before:

- `max_dy = 5`
- `slit = wide_center`
- `strength = 0.0005`

Readout:

| observable | value |
|---|---:|
| `MI` | `0.616978` |
| `d_TV` | `0.839206` |
| `1 - pur_cl` | `0.464598` |
| gravity at `b = 6` | `+0.162694` |
| Born `|I3|/P` | `4.24e-16` |
| `k=0` | `0.00e+00` |
| positive gravity points | `11/11` |
| barrier-harness tail fit | `alpha = -1.00`, `R^2 = 0.93` |

Signed barrier-harness curve:

```text
b=2:+0.0950  b=3:+0.1167  b=4:+0.1328  b=5:+0.1504  b=6:+0.1627
b=7:+0.1597  b=8:+0.1397  b=10:+0.0853  b=13:+0.0666  b=16:+0.0661
b=19:+0.0583
```

So the same two-slit lattice card now keeps:

- Born-clean same-family companion audit
- `k=0` exactly zero
- nontrivial MI and decoherence
- gravity **toward mass** at every tested `b`
- a real decaying tail on the **same barrier harness**

## Retained Weak-Field Pocket

Across the full `3 x 3 x 8 = 72` rows:

- Born-clean rows: `72/72`
- positive gravity rows: `6/72`
- all-`b`-positive rows: `4/72`
- retained weak-field rows: `4/72`

The retained rows are:

| `max_dy` | slit family | strength | `MI` | `1-pur_cl` | gravity@`b=6` | tail fit |
|---|---|---:|---:|---:|---:|---|
| 5 | `narrow_center` | `0.0005` | `0.6969` | `0.4865` | `+0.1783` | `alpha=-1.09`, `R^2=0.95` |
| 5 | `narrow_center` | `0.0010` | `0.7211` | `0.4885` | `+0.0995` | `alpha=-0.83`, `R^2=0.97` |
| 5 | `wide_center` | `0.0005` | `0.6170` | `0.4646` | `+0.1627` | `alpha=-1.00`, `R^2=0.93` |
| 5 | `wide_center` | `0.0010` | `0.6351` | `0.4693` | `+0.1222` | `alpha=-0.67`, `R^2=0.92` |

Everything outside that pocket fails for a clear reason:

- `max_dy = 4` and `6` stay gravity-negative across the full strength sweep
- `strength >= 0.002` on `max_dy = 5` flips or degrades the sign
- `wide_outer` on `max_dy = 5` does not keep the same all-`b` positivity and
  fit quality needed for promotion

## Interpretation

The prior negative decision was real on the fixed standard-strength slice.

But it was **not** the last word on the lattice family, because field strength
changes the mechanism regime:

- at the old standard strength, coherent phase disruption dominates and the
  centroid shifts by beam depletion
- at weak field, the lattice enters a linear-response regime where attraction
  survives on the same two-slit card

So the decisive missing degree of freedom was:

- **field strength**, not Born safety
- and not a total lack of path multiplicity

## Safe conclusion

The ordered-lattice symmetry line is now **reopened**.

The review-safe read is:

- the old standard-strength lattice decision remains a valid negative result on
  that fixed slice
- but there is now a **narrow weak-field retained pocket** on the same ordered
  lattice family
- that pocket keeps:
  - Born-clean companion audit
  - nontrivial MI and decoherence
  - positive gravity on the same two-slit card
  - a real decaying barrier-harness distance tail

This is still **not** a blanket lattice unification theorem.
It is a narrow retained pocket centered on:

- `max_dy = 5`
- slit families `narrow_center` and `wide_center`
- strengths `5e-4` to `1e-3`

## Project-level read

This upgrades the ordered-lattice branch from:

- only a same-family two-harness bridge

to:

- a same-family bridge **plus** a narrow weak-field one-card pocket

It still does **not** displace exact mirror as the flagship coexistence lane,
but it materially strengthens the ordered-lattice branch as a genuine unified
secondary architecture.
