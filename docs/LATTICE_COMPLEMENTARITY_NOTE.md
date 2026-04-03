# Lattice Complementarity Note

**Date:** 2026-04-03  
**Status:** retained bounded tradeoff curve with a sweet spot

This note freezes the ordered-lattice complementarity result as a canonical
artifact chain. It does **not** promote the ordered lattice to a one-card
unification architecture.

Artifacts:

- [`scripts/lattice_complementarity_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_complementarity_sweep.py)
- [`logs/2026-04-03-lattice-complementarity-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-complementarity-sweep.txt)

## Setup

- ordered 2D lattice with forward `|Δy| <= 1`
- `N = 40`
- half-width `= 20`
- standard linear propagator only
- fixed detector observable: final-layer centroid shift
- slit-width sweep implemented as a central blocked-band half-width
  `gap = 1..7`
- per-side slit width is therefore `20 - gap`
- fixed mass convention: one mass node at `first_open_upper_row + 4`
- fixed distance-law fit: barrier-card far-field fit of `|delta|` vs `b` on
  `b >= 7`
- Born is measured on a **same-family companion Sorkin aperture**, not the
  exact same 2-slit card used for MI / `d_TV` / gravity

## Tradeoff Table

| gap | per-side slit width | mass row | `MI` | `d_TV` | `pur_cl` | `1-pur_cl` | distance alpha | distance `R^2` | gravity | sign | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| 1 | `19` | `6` | `0.405` | `0.610` | `0.939` | `0.061` | `-1.103` | `0.969` | `-4.8583` | away | `8.03e-16` | `0.00e+00` |
| 2 | `18` | `7` | `0.537` | `0.714` | `0.943` | `0.057` | `-0.893` | `0.930` | `-5.7403` | away | `5.17e-16` | `0.00e+00` |
| 3 | `17` | `8` | `0.664` | `0.803` | `0.946` | `0.054` | `-0.614` | `0.871` | `-6.2564` | away | `5.64e-16` | `0.00e+00` |
| 4 | `16` | `9` | `0.779` | `0.878` | `0.950` | `0.050` | `-0.405` | `0.814` | `-6.6794` | away | `5.25e-16` | `0.00e+00` |
| 5 | `15` | `10` | `0.868` | `0.930` | `0.954` | `0.046` | `-0.300` | `0.790` | `-7.1844` | away | `5.15e-16` | `0.00e+00` |
| 6 | `14` | `11` | `0.926` | `0.962` | `0.954` | `0.046` | `-0.252` | `0.766` | `-7.7483` | away | `6.36e-16` | `0.00e+00` |
| 7 | `13` | `12` | `0.963` | `0.982` | `0.953` | `0.047` | `-0.221` | `0.738` | `-8.4206` | away | `7.45e-16` | `0.00e+00` |

## Sweet Spot Row

The canonical sweep uses one explicit balance guard for a retained sweet spot:

- Born `<= 1e-12`
- `|k=0| <= 1e-9`
- `MI >= 0.50`
- `1 - pur_cl >= 0.05`
- distance-law fit `R^2 >= 0.90`

On that declared guard, the retained sweet spot is:

- `gap = 2`
- per-side slit width `= 18`
- mass row `= 7`
- `MI = 0.537`
- `d_TV = 0.714`
- `pur_cl = 0.943`
- `1 - pur_cl = 0.057`
- distance-law exponent `alpha = -0.893`
- distance-law fit `R^2 = 0.930`
- gravity `= -5.7403` on the same slit card
- Born companion audit `= 5.17e-16`
- `k=0 = 0.00e+00`

This is the only row in the sweep that clears the full bounded-balance guard.

## What Is Retained

The ordered-lattice result is best described as:

- **a bounded tradeoff curve with a sweet spot**

That statement is retained because the canonical script reproduces a stable
trend:

- as slits narrow, `MI` rises from `0.405` to `0.963`
- `d_TV` rises from `0.610` to `0.982`
- CL decoherence stays nontrivial across the full sweep:
  `1 - pur_cl = 0.046 .. 0.061`
- barrier-card distance-law quality degrades as slits narrow:
  `R^2 = 0.969 -> 0.738`
- Born companion audit stays machine-clean on `7/7` rows
- `k=0` stays exactly zero on `7/7` rows

So the safe promoted read is:

- the ordered lattice supports a continuous tradeoff between
  decoherence/which-slit structure and distance-law quality
- there is a bounded sweet spot where both are simultaneously present

## What Is Not Retained

The following claims are **not** promoted from this artifact chain:

- same-card attractive gravity
- full one-family unification
- a claim that Born, MI, decoherence, distance law, and attractive gravity all
  coexist on one retained slit card

The same-card gravity read stays negative on every slit width in the sweep:

- gravity sign is `away` on `7/7` rows

So this note must be read alongside the existing negative one-harness decision,
not as a reversal of it.

## Promoted Wording Recommendation

Use:

- **ordered lattice supports a continuous tradeoff between
  decoherence/which-slit structure and distance-law quality, with a bounded
  sweet spot where both are simultaneously present**

Do not use:

- **full one-family unification**
- **same-card attractive gravity on the ordered-lattice sweet spot**
- **ordered lattice has a promoted unified architecture**
