# Wilson `mu^2` Distance Sweep Note

**Date:** 2026-04-11  
**Status:** bounded-retained calibration note

**Script:** `scripts/frontier_wilson_mu2_distance_sweep.py`

**Anchor notes/scripts:**
- `docs/WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`
- `docs/WILSON_TWO_BODY_OPEN_REFINED_NOTE_2026-04-11.md`
- `scripts/frontier_wilson_two_body_open.py`

## Question

Does the open-boundary Wilson distance law stay steep as screening is reduced,
or does it soften toward Newton-compatible `d^-2` behavior?

## Sweep design

- open 3D Wilson lattice
- `G = 5`
- sides `11, 13, 15`
- separations `d = 3, 4, 5, 6`
- `mu^2 = 0.22, 0.10, 0.05, 0.01, 0.001, 0.0`

Only clean attractive rows were used in the distance-law fit, matching the
retained open-lattice Wilson convention.

## Results

All sampled points remained attractive and clean across the mu-scan surface.

Clean distance-law fits:

- `mu^2 = 0.22`: exponent `-3.290` (`R^2 = 0.9957`)
- `mu^2 = 0.10`: exponent `-2.732` (`R^2 = 0.9969`)
- `mu^2 = 0.05`: exponent `-2.394` (`R^2 = 0.9975`)
- `mu^2 = 0.01`: exponent `-1.996` (`R^2 = 0.9981`)
- `mu^2 = 0.001`: exponent `-1.872` (`R^2 = 0.9984`)
- `mu^2 = 0.0`: exponent `-1.857` (`R^2 = 0.9985`)

Per-side fits at low screening are consistent with the global trend:

- at `mu^2 = 0.01`, `side=13` gives `-1.978`
- at `mu^2 = 0.001`, `side=15` gives `-1.885`
- at `mu^2 = 0.0`, `side=15` gives `-1.869`

## Interpretation

The steep open-lattice exponent at `mu^2 = 0.22` is **screening-controlled**.

As screening is reduced:

- the exponent softens monotonically
- the law approaches Newton-compatible `d^-2`
- the mutual-attraction channel itself remains present

So the correct statement is not “the Wilson law is permanently steeper than
Newton,” but rather:

> the open-lattice Wilson mutual channel is real, and its distance exponent
> is strongly controlled by the screening mass.

This note only calibrates the **distance-law side** of the Wilson lane.

It does **not** close the mass-law side, because the current both-masses
runner varies Poisson source weights without introducing independent inertial
masses in the two orbital Hamiltonians.

## Conclusion

This is a calibration result, not a separate Newton-law derivation.

It supports the use of the open Wilson lane as a screened crossover study and
shows that the steep `mu^2 = 0.22` exponent should not be treated as a fixed
universality class.

The exact next observable needed for a retained Wilson Newton claim is:

- independent inertial masses `M_A`, `M_B` in `H_A`, `H_B`
- early-time mutual momentum transfer
  - `P_A^mut = M_A * a_A^(shared-self_only)`
  - `P_B^mut = M_B * a_B^(shared-self_only)`
- on the same open weak-screening surface

Until that exists, this note should only be cited as a distance-law
calibration.
