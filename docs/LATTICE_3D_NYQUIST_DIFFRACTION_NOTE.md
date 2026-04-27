# Lattice 3D Nyquist Diffraction Note

**Date:** 2026-04-04  
**Status:** bounded Nyquist-flip probe on the proposed_retained 3D ordered-lattice family

## Artifact chain

- Script: [`scripts/lattice_3d_nyquist_diffraction_probe.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_nyquist_diffraction_probe.py)
- Log: [`logs/2026-04-04-lattice-3d-nyquist-diffraction-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-nyquist-diffraction-probe.txt)

This probe freezes the narrow question that was only described in the commit
message:

- does the gravity-side centroid shift flip sign at a lattice cutoff
  `k_flip ≈ π/h`?
- does that flip stay field-independent?
- does it move with `h` as a lattice artifact should?

The probe scans `k` on the retained ordered-lattice family for:

- `h = 0.5`
- `h = 0.25`

and compares two field strengths:

- `1e-4`
- `1e-2`

## Frozen result

### `h = 0.5`

- Nyquist: `π/h = 6.283185`
- `strength = 1e-4`
  - first positive-to-negative flip: `6.199467`
  - relative error vs `π/h`: `1.332%`
- `strength = 1e-2`
  - first positive-to-negative flip: `6.107077`
  - relative error vs `π/h`: `2.803%`
- mean flip: `6.153272`
- mean / `π/h`: `0.979324`

### `h = 0.25`

- Nyquist: `π/h = 12.566371`
- `strength = 1e-4`
  - first positive-to-negative flip: `11.932917`
  - relative error vs `π/h`: `5.041%`
- `strength = 1e-2`
  - first positive-to-negative flip: `12.085990`
  - relative error vs `π/h`: `3.823%`
- mean flip: `12.009454`
- mean / `π/h`: `0.955682`

## Safe read

The bounded conclusion is:

- the first gravity sign flip tracks the lattice Nyquist scale
- the flip is field-independent to the tested order of magnitude
- the flip moves with `h`, so it is not a fixed continuum-scale prediction

So the honest interpretation is:

- this is a real discrete-lattice UV effect
- it is a lattice artifact in the continuum limit, because `k_flip ∝ 1/h`
- if `h` is interpreted as a physical spacetime spacing, then it becomes a
  physical UV cutoff prediction instead

## What this is not

- not a continuum theorem
- not a new low-energy gravity law
- not a claim that classical gravity reverses in ordinary macroscopic settings

## Relation to the retained lattice lane

This note should be read alongside the valley-linear finite-lattice bridge:

- [`VALLEY_LINEAR_ASYMPTOTIC_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ASYMPTOTIC_BRIDGE_NOTE.md)
- [`docs/START_HERE.md`](/Users/jonreilly/Projects/Physics/docs/START_HERE.md) if you want the retained 3D gravity lane in the broader repo context

The difference is:

- the valley-linear bridge is about the sign and tail of the low-k gravity lane
- this note is about the UV cutoff where the sign flips under phase scanning

## Best next move

The next honest step is not to promote this to a continuum claim.

The right follow-up is one of:

- a thinner lattice step to see the flip move again as `1/h`
- or a cleaner theoretical note explaining why the flip is exactly the lattice
  aliasing point for the chosen discrete propagator

If neither is done, the safe read stays:

- a field-independent Nyquist flip exists on the discrete lattice
- it is a bounded lattice prediction, not a retained continuum result
