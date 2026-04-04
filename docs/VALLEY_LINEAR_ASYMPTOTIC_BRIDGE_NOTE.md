# Valley-Linear Asymptotic Bridge Note

**Date:** 2026-04-04  
**Status:** bounded finite-size bridge on the 3D ordered-lattice `1/L^2` family

## One-line read

The widened valley-linear 3D replay is still genuinely TOWARD and stays
Born-clean, but the far-tail exponent is still slice-dependent enough that the
safe read remains:

- near-Newtonian finite-lattice replay
- not yet a stabilized universal `-1.00` theorem

## Primary artifact

- Script: [`scripts/valley_linear_asymptotic_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/valley_linear_asymptotic_bridge.py)
- Log: [`logs/2026-04-04-valley-linear-asymptotic-bridge.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-valley-linear-asymptotic-bridge.txt)

The script keeps fixed:

- the retained 3D valley-linear family
- the `1/L^2` kernel with `h^2` measure
- the detector geometry and barrier sanity checks

It varies only a small `h/W` ladder:

- coarse anchor: `h = 0.5`, `W = 8`
- core retained: `h = 0.25`, `W = 10`
- wide replay: `h = 0.25`, `W = 12`

## Frozen replay result

| slice | Born | `k=0` | `F~M` | gravity | TOWARD | peak tail | far tail |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse anchor `h=0.5, W=8` | `2.50e-15` | `0` | `1.00` | `+0.000144` | `7/9` | `z>=5: -1.47`, `R²=0.996` | `-1.47`, `R²=0.996` |
| core retained `h=0.25, W=10` | `4.20e-15` | `0` | `1.00` | `+0.000224` | `9/9` | `z>=4: -1.00`, `R²=0.979` | `z>=5: -1.12`, `R²=0.991` |
| wide replay `h=0.25, W=12` | `4.82e-15` | `0` | `1.00` | `+0.000232` | `9/9` | `z>=4: -0.90`, `R²=0.985` | `z>=5: -1.00`, `R²=0.995` |

## Safe interpretation

- The finite-lattice 3D valley-linear family keeps the sign we want:
  TOWARD persists across the tested ladder.
- `F~M = 1.00` stays fixed across the tested ladder.
- The far-tail exponent is **not** fully stabilized:
  - the coarse anchor is steeper
  - the retained `h = 0.25` rows move closer to `-1.00`
  - the wider replay changes the tail shape again even while staying near
    Newtonian
- So the result is stronger than a raw finite-size artifact, but it is still
  slice-dependent enough that we should not call it a universal theorem.

## What this means

This bridge is the narrowest honest summary of the current valley-linear
asymptotic status:

- sign persistence is retained
- near-linear mass scaling is retained
- the best far-tail read is near-Newtonian on the widened slices
- the exponent still moves with `h` and `W`, so the asymptotic law is not
  fully stabilized

## What this is not

- It is not an exact `1/b` proof.
- It is not a universal continuum theorem.
- It is not a replacement for the already-frozen same-family action note or
  the wide-tail replay note.

The safest wording is:

- the ordered 3D valley-linear lane gives a near-Newtonian finite-lattice
  replay
- the asymptotic bridge is stronger than before, but still slice-dependent
- the remaining physics question is what finite-size correction rule, if any,
  turns this into a stable continuum law
