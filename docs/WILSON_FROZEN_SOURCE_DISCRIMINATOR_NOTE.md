# Wilson Frozen-Source Discriminator Note

## What was tested

Three-way comparison on the open 3D Wilson lattice to determine whether the
mutual-channel attraction signal is genuinely dynamic or merely a static-field
artefact.

Three modes run on every (side, distance, placement) configuration:

| Mode | Definition |
|------|-----------|
| SHARED | Both packets source a shared gravitational field, recomputed every step |
| SELF_ONLY | Each packet sees only its own field, recomputed every step |
| FROZEN_SOURCE | Compute phi once from initial rho_A(0) + rho_B(0), evolve in that fixed field forever |

The discriminator is: a_mutual(SHARED) - a_mutual(FROZEN_SOURCE), where
a_mutual(X) = a_sep(X) - a_sep(SELF_ONLY).

If the discriminator is reliably positive, the dynamic field update adds real
signal beyond the static initial potential. If not, the mutual channel is
explained by the frozen field.

## Parameters

Identical to the audited robustness sweep:

- sides: 18, 20, 22
- separations: 4, 6, 8, 10, 12
- placements: centered, face_offset, corner_offset
- G=5, mu2=0.001, MASS=0.3, WILSON_R=1.0, DT=0.08, N_STEPS=15, SIGMA=1.0
- Early-time window: steps 2-10

Total: 45 configurations (3 sides x 3 families x 5 separations).

## Result

**FAIL: The mutual-channel signal is predominantly a static-field effect.**

### Summary numbers

| Metric | Value |
|--------|-------|
| discriminator > 0 (SHARED stronger) | 15/45 (33.3%) |
| discriminator < 0 (FROZEN stronger) | 30/45 (66.7%) |
| mean(discriminator) | -0.0068 |
| mean(a_mutual_shared) | -0.199 |
| mean(a_mutual_frozen) | -0.192 |

### Pattern by separation

| d | disc > 0 | mean(disc) |
|---|----------|------------|
| 4 | 0/9 | -0.049 |
| 6 | 0/9 | -0.020 |
| 8 | 0/9 | -0.006 |
| 10 | 6/9 | +0.008 |
| 12 | 9/9 | +0.034 |

At short separations (d=4,6,8), the FROZEN field produces *stronger* attraction
than SHARED. This is consistent with the packets spreading under evolution: the
dynamically updated field weakens as the density disperses, while the frozen
field retains the concentrated initial profile. At large separations (d=10,12),
this reversal flips because the initial field is weaker at large distances and
the dynamic update can partially compensate via density redistribution.

### Pattern by side

The effect is slightly worse on larger lattices (side=22 has only 3/15
disc > 0 vs 6/15 on side=18), consistent with the frozen field retaining more
relative advantage on larger boxes where packets spread more freely.

### Pattern by placement family

Essentially identical across all three families (5/15 disc > 0 each). The
frozen-vs-dynamic distinction does not depend on placement.

## Interpretation

The mutual-channel attraction signal reported in the robustness sweep is
almost entirely explained by the static initial gravitational potential.
Freezing the potential at t=0 reproduces (and at short range exceeds) the
attraction seen with fully dynamic updates.

This does NOT invalidate the existence of mutual attraction on the Wilson
lattice. Both SHARED and FROZEN_SOURCE show clear attraction relative to
SELF_ONLY. What it shows is that the attraction is sourced by the *initial
overlap of the combined density*, not by a dynamically evolving gravitational
feedback loop.

## What this means for the side lane

The Wilson mutual-attraction lane cannot claim a dynamically evolving
gravitational channel. The observed signal is a static-field effect: the
initial combined density creates a potential well, and both packets fall
into it regardless of whether the field is updated.

This control was the specific gate requested by review. The lane remains
HELD until a genuinely dynamic signal is identified (if one exists at these
parameters).

## Bounded claims

- The test covers 3 sides, 5 separations, 3 placements = 45 configs
- Parameters are identical to the audited robustness sweep
- The FROZEN_SOURCE mode is the simplest possible frozen control (phi
  computed once from initial combined density, never updated)
- No Newton closure is claimed
- No both-masses closure is claimed
- The result is specific to these Wilson parameters (MASS=0.3, G=5, etc.)

## Script

`scripts/frontier_wilson_frozen_source_discriminator.py`
