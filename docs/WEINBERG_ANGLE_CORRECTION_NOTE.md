# Weinberg Angle Threshold Corrections from Taste Spectrum

**PStack experiment:** weinberg-angle-correction
**Script:** `scripts/frontier_weinberg_angle_correction.py`
**Date:** 2026-04-12
**Status:** review-only scenario scan. The fixed-coupling scan can hit the
measured value for some taste assignments, but the self-consistent solve does
not close the gap, so the taste assignments remain model-dependent.

## Motivation

The Cl(3) framework supplies the Planck-scale boundary condition
sin^2(theta_W) = 3/8 = 0.375. Running to M_Z with SM beta functions and the
correct GUT-normalized formula gives:

    sin^2(theta_W)(M_Z) = 0.176

which is 24% below the measured value 0.231.

**Normalization correction:** The gauge unification note reported 0.263
using the formula alpha_1/(alpha_1 + alpha_2) with GUT-normalized alpha_1.
The correct formula is:

    sin^2_W = (3/5) * alpha_1 / ((3/5) * alpha_1 + alpha_2)

which reduces to 3/8 at unification and 0.231 for the measured couplings.

## The taste threshold hypothesis

This note does not derive the taste assignment. It tests several candidate
assignments for how an 8-state staggered taste multiplet could enter the
threshold running.

In the modeled scenarios below, the taste partners are treated as copies of
the same gauge representations above a threshold M_taste, analogous to how
SUSY thresholds modify running. That identification is a modeling choice, not
a derived result of this note.

## Three scenarios

These scenarios are hypotheses used to probe sensitivity to the unresolved
taste mapping.

| Scenario | Content above M_taste | delta_b_1 | delta_b_2 | delta_b_3 |
|----------|----------------------|-----------|-----------|-----------|
| III: Minimal | 3* quark partner only | -2.20 | -3.00 | -4.00 |
| II: Structured | 3* quarks + singlet partners | -16.27 | -12.00 | -4.00 |
| I: Full 8-fold | All 8 tastes active (7 extra per SM) | -28.00 | -28.00 | -28.00 |

## Results

With the unified coupling alpha_U = 0.022 (mean of the SM-only extrapolation to
M_Planck), the fixed-coupling scan gives:

| Scenario | sin^2_W achieved | M_taste required | Deviation |
|----------|-----------------|-----------------|-----------|
| SM only | 0.176 | N/A | -24% |
| III: Minimal (3*) | 0.181 max | no exact match | -22% |
| II: Structured taste | **0.231** | 6 x 10^11 GeV | **0.0%** |
| I: Full 8-fold | **0.231** | 1.2 x 10^17 GeV | **0.0%** |
| MSSM (M_SUSY = 1 TeV) | 0.229 | 10^3 GeV | -1.2% |
| Measured (PDG 2024) | 0.231 | -- | 0% |

The self-consistent solve, which recomputes the unified coupling after the
thresholds are included, does not keep the 0.231 match. In that solve the
best values stay near the SM-like 0.176-0.181 range, so the threshold
correction remains scenario-dependent rather than derived.

## Key physics

1. **Direction of correction:** SM-only running lands low at sin^2_W = 0.176.
   Extra matter above M_taste can move the fixed-coupling scan upward toward
   0.231, but the self-consistent solve does not preserve that improvement.

2. **Scenario I (full taste)** is the cleanest fixed-coupling fit: above
   M_taste ~ 10^17 GeV, the scan can hit 0.231. But because the full solve
   readjusts alpha_U, this is not yet a retained prediction.

3. **Scenario II (structured)** also hits 0.231 in the fixed-coupling scan,
   but it depends on a specific taste mapping that remains unresolved.

4. **Self-consistent caveat:** When alpha_U is re-determined self-consistently
   (accounting for modified running above M_taste), the improvement is
   absorbed back toward the SM-like result. That is the reason this lane
   remains review-only.

## Comparison with MSSM

| Feature | MSSM | Cl(3) taste |
|---------|------|-------------|
| New particle content | Sparticles (many) | None (lattice structure) |
| Free parameters | M_SUSY, tan(beta), ... | M_taste (scenario choice) |
| Threshold scale | ~1 TeV | scenario-dependent |
| Unification scale | 2 x 10^16 GeV | Planck-scale boundary condition |
| sin^2_W achieved | 0.229 | 0.231 in fixed-coupling scan only |
| Mechanism | SUSY matter shifts betas | Hypothesized taste matter shifts betas |

## Honest assessment

**What works:**
- The fixed-coupling scan shows that some taste assignments can hit the
  measured sin^2(theta_W)
- The result is transparent about which taste assignments are being assumed
- The scan makes the model-dependence explicit instead of hiding it

**What needs work:**
- The taste assignments are unresolved and scenario-dependent
- The self-consistent alpha_U determination does not preserve the 0.231 match
- A derivation of the taste mapping from the retained cubic lane is still missing
- 2-loop corrections and gravity effects near M_Planck are not included

**Bottom line:**
This is a review-only scenario scan, not a retained derivation. The fixed-
coupling scan can reproduce the measured Weinberg angle for some taste
assignments, but the self-consistent solve does not close the gap. The note
should therefore be read as a bounded consistency study with unresolved taste
assignments.
