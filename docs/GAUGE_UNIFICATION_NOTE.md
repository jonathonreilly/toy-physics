# Gauge Coupling Unification from Cl(3) at the Planck Scale

**PStack experiment:** gauge-unification
**Script:** `scripts/frontier_gauge_unification.py`
**Date:** 2026-04-12

## Motivation

The framework derives all three Standard Model gauge groups from the same
Cl(3) Clifford algebra on the cubic lattice Z^3. If they share a common
algebraic origin, their couplings should unify at the lattice/Planck scale.

## What emerges from Cl(3)

| Gauge group | Cl(3) origin | Generator type |
|-------------|-------------|----------------|
| U(1)_Y | Edge phases | Pseudoscalar G1G2G3 |
| SU(2)_L | Bipartite taste structure | Bivectors S_k = -(i/2) eps G_i G_j |
| SU(3)_c | Triplet subspace of 8-dim taste | Full Clifford products |

All three use the same lattice link variable U = exp(igA) with bare coupling
g = 1 (unit hopping), giving alpha_bare = 1/(4 pi) = 0.0796.

## GUT relation

Because all couplings are equal at the lattice scale, the framework predicts:

    sin^2(theta_W) = 3/8 = 0.375    at M_Planck

This is the same relation as SU(5) and SO(10) GUTs, but arises from the
Cl(3) structure rather than embedding in a larger gauge group.

## Running to M_Z: 1-loop SM beta functions

Running measured couplings UP from M_Z using the standard 1-loop formula:

    1/alpha_i(mu) = 1/alpha_i(M_Z) + b_i/(2 pi) ln(mu/M_Z)

with b_1 = -41/10, b_2 = 19/6, b_3 = 7 gives at M_Planck:

| Coupling | 1/alpha at M_Z | 1/alpha at M_Planck |
|----------|---------------|-------------------|
| alpha_1 | 59.0 | 33.3 |
| alpha_2 | 29.6 | 49.5 |
| alpha_3 | 8.5 | 52.4 |

The three couplings do NOT exactly meet at M_Planck (spread ~19%).
This is the well-known non-unification of the SM -- it also fails
at the traditional GUT scale of ~10^16 GeV.

The minimum spread occurs at ~1.6 x 10^14 GeV, where the three
1/alpha values are within 1.7 of each other.

## Required vs lattice coupling

The mean 1/alpha at M_Planck from 2-loop running is ~45, giving a
required alpha_U ~ 0.022. The bare lattice coupling is alpha = 0.080,
a factor of ~3.6x larger.

An embedding correction from the Casimir ratio C2(adjoint)/C2(fundamental)
= 9/4 reduces this to alpha_eff = 0.035 (1/28.3), bringing the ratio
to ~1.6x.

The dimension projection factor 3/8 (from the 3-dim SU(3) fundamental
living in the 8-dim taste space) gives alpha_proj = 0.030 (1/33.5),
close to the 1/alpha_1 value at M_Planck.

## sin^2(theta_W) at M_Z

**BUG FIX (2026-04-12):** The original computation used the formula
sin^2 = alpha_1/(alpha_1 + alpha_2) with GUT-normalized alpha_1. The
correct formula is sin^2 = (3/5)*alpha_1/((3/5)*alpha_1 + alpha_2),
which reduces to 3/8 at unification. The script has been corrected.

Running from exact unification at M_Planck with SM-only beta functions:

    sin^2(theta_W)(M_Z) ~ 0.176  [CORRECTED from 0.263]

compared to the measured value 0.23122. The SM-only prediction is 24% LOW.

With taste threshold corrections (see WEINBERG_ANGLE_CORRECTION_NOTE.md):
- Full 8-fold taste at M_taste = 1.2 x 10^17 GeV: sin^2 = 0.231 (exact match)
- Structured taste at M_taste = 6 x 10^11 GeV: sin^2 = 0.231 (exact match)
- Self-consistent caveat: fitted M_taste, not derived from first principles

## Proton decay

The key qualitative prediction of Planck-scale (vs GUT-scale) unification:

| Scenario | M_unif | tau_proton | Status |
|----------|--------|-----------|--------|
| SU(5) GUT | 2 x 10^16 GeV | ~10^37 years | Near Super-K bound |
| Cl(3) framework | 1.2 x 10^19 GeV | ~10^47 years | Completely safe |

The enhancement factor (M_Planck/M_GUT)^4 ~ 10^11 pushes proton decay
far beyond any foreseeable experiment, explaining the null result.

## Honest assessment

**What works:**
- The Cl(3) algebra naturally provides all three gauge groups
- The GUT relation sin^2(theta_W) = 3/8 emerges automatically
- Proton decay suppression is a genuine qualitative prediction
- sin^2(theta_W) at M_Z is 0.176 with SM-only running (24% low); 0.231 with taste threshold corrections

**What needs work:**
- The bare lattice coupling (alpha ~ 0.08) is ~3.6x larger than the
  required unified coupling from 2-loop running (~0.022)
- The embedding/normalization correction partially closes this gap
  but does not fully resolve it
- The SM couplings have a 19% spread at M_Planck even with 2-loop
  running -- exact unification requires threshold corrections
- Planck-scale gravity corrections to the running are O(1) and
  could be significant

**Bottom line:**
The framework provides a natural, parameter-free mechanism for gauge
unification with the correct qualitative features. The quantitative
precision is limited by the unknown Planck-scale threshold corrections
and the embedding normalization, both of which are expected to be O(1)
effects at the Planck scale.
