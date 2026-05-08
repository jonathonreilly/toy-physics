# Wilson `mu^2` Distance Sweep Note

**Date:** 2026-04-11  
**Status:** bounded companion calibration note

**Script:** `scripts/frontier_wilson_mu2_distance_sweep.py` (current main reproduces the table to within ~0.5% drift in the 3rd-decimal exponent: `-3.315` vs noted `-3.290` at `mu^2=0.22`, `-1.992` vs `-1.996` at `mu^2=0.01`, `-1.871` vs `-1.872` at `mu^2=0.001` — qualitative monotone softening preserved)

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

The later both-masses momentum-transfer runner still does **not** close the
mass-law side:

- anchor impulse slices fall below retained linearity (`R^2 ≈ 0.94`)
- full-grid normalized impulses drift by `35-38%`
- action-reaction fails on every grid row

So the distance exponent can be calibrated honestly, but full Newton closure is
still open.

## Conclusion

This is a calibration result, not a separate Newton-law derivation.

It supports the use of the open Wilson lane as a screened crossover study and
shows that the steep `mu^2 = 0.22` exponent should not be treated as a fixed
universality class.

That observable has now been attempted and it fails because the shared-minus-
self residual is dominated by common propagation slowing once both inertial
masses vary.

So this note should still be cited only as a distance-law calibration, not as
a retained Wilson Newton claim.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [wilson_two_body_open_note_2026-04-11](WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md)
- [wilson_two_body_open_refined_note_2026-04-11](WILSON_TWO_BODY_OPEN_REFINED_NOTE_2026-04-11.md)
