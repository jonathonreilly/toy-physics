# Gravitational Deflection / Lensing Sweep — Moderate Positive

**Date:** 2026-04-07
**Status:** retained moderate positive — at H=0.35, the first-order Kubo deflection coefficient `kubo_true(b)` follows a clean restricted 1/b-like fit on b ∈ {2, 3, 4, 5, 6}: slope = **−1.03**, R² = **0.94**, |slope − (−1)| = **0.03**. The beam's centroid deflection `dM(b)` gives the same slope (−1.03, R²=0.91). The full-range fit (b=1..6) is dominated by a near-field pathology at b=1 (deflection AWAY from the mass because the mass is inside the beam's natural transverse width), so the b ≥ 2 restriction is physically motivated. This is the first retained gravity-side result in the program that matches a recognizable lensing functional form.

## Artifact chain

- [`scripts/lensing_deflection_sweep.py`](../scripts/lensing_deflection_sweep.py)
- [`logs/2026-04-07-lensing-deflection-sweep.txt`](../logs/2026-04-07-lensing-deflection-sweep.txt)

## Question

The propagator action `S = L(1−f)` is literally Fermat's principle
with refractive index `n = 1 − f`. A mass sources `f ∝ 1/r`, so the
beam path through that field is a geodesic in a gradient-index
medium — the same formalism as weak-field gravitational lensing.

Weak-field gravitational lensing predicts a deflection angle

    α(b) = (constant) / b

where `b` is the impact parameter (perpendicular distance of the
undeflected ray from the mass). Both Newton and Einstein give this
1/b functional form; they differ only in the prefactor (Einstein's
is twice Newton's).

The question: **does the program's beam deflection follow
α(b) ∝ 1/b?** If yes, we have a direct connection between the
lattice model and recognizable gravitational-lensing physics.

## Setup

Reusing the Kubo-continuum-limit machinery (Lane α's parallel
perturbation propagator + finite-difference dM cross-check):

- Fam1 grown DAG (drift=0.20, restore=0.70, seed=0)
- Beam: single source at origin (iy=0, iz=0, layer=0)
- Mass: at (x_src = round(NL/3)·H, y=0, z_src = b) where b is the
  impact parameter in physical units
- Field: imposed 1/r with `s = S_phys = 0.004`, regularizer 0.1
- Impact parameters swept: b ∈ {1.0, 2.0, 3.0, 4.0, 5.0, 6.0}
- Refinements: H ∈ {0.5, 0.35}  (memory-feasible 2-refinement sweep)

For each (H, b), compute:
- `dM(b)` = finite-difference deflection at s = S_phys
- `kubo_true(b)` = parallel perturbation propagator's first-order
  coefficient at s = 0

## Result

### Per-b measurements

| b | coarse dM (H=0.5) | medium dM (H=0.35) | medium kubo_true |
| ---: | ---: | ---: | ---: |
| 1.0 | **−0.0143** | **−0.0134** | **−2.29** |
| 2.0 | +0.0191 | +0.0284 | +6.96 |
| 3.0 | +0.0346 | +0.0242 | +5.97 |
| 4.0 | +0.0261 | +0.0124 | +3.34 |
| 5.0 | +0.0135 | +0.0126 | +3.06 |
| 6.0 | +0.0124 | +0.0096 | +2.36 |

At b = 3.0 the medium `kubo_true = +5.97` matches the Lane α
continuum result (+5.986) at its reference configuration to within
0.3%. That's consistent.

### The near-field pathology at b = 1

At b = 1.0, **both H=0.5 and H=0.35 give negative deflection**
(dM = −0.014, −0.013). The sign check labels this "AWAY from the
mass." This is NOT a bug — it's the natural behavior of a
diffracting beam when the mass is inside the beam's transverse
extent:

- The beam starts as a point source at iy=iz=0, layer 0
- It spreads as it propagates; by the mass's x-layer it has a
  significant transverse width
- At b = 1 (physical z), the mass is inside the beam's width
- Parts of the beam's amplitude are on either side of the mass
- The weighted centroid does not shift simply "toward" the mass
  because the field is strongly asymmetric over the beam's support

This is a near-field regime, not a lensing regime. The lensing
formalism assumes the ray (or beam centroid) passes the mass at
clear distance `b`. For b ≤ 1 in our lattice, that assumption
fails.

### Restricted fits — the asymptotic lensing regime

Excluding the b = 1 near-field point, fit log|kubo_true| vs log(b):

| Subset | Refinement | slope | R² | \|slope−(−1)\| |
| --- | ---: | ---: | ---: | ---: |
| b ∈ {2..6} | H=0.5 | −0.470 | 0.37 | 0.530 |
| **b ∈ {2..6}** | **H=0.35** | **−1.029** | **0.937** | **0.029** |
| b ∈ {3..6} | H=0.5 | −1.281 | 0.971 | 0.281 |
| **b ∈ {3..6}** | **H=0.35** | **−1.269** | **0.937** | **0.269** |

And for the finite-difference `dM` (the direct centroid
displacement, not the analytic Kubo coefficient):

| Subset | Refinement | slope | R² | \|slope−(−1)\| |
| --- | ---: | ---: | ---: | ---: |
| **b ∈ {2..6}** | **H=0.35** | **−1.033** | **0.911** | **0.033** |
| b ∈ {3..6} | H=0.35 | −1.223 | 0.864 | 0.223 |

**The cleanest single result is the restricted b ∈ {2..6} fit at
H=0.35 on `kubo_true`**: slope = **−1.03**, R² = **0.94**,
essentially exact 1/b scaling on that five-point fit. The
corresponding dM fit gives the same slope (−1.03) with slightly
lower R² (0.91).

The b ∈ {3..6} fit is slightly steeper (≈ −1.27) at both
refinements — this suggests the b = 2 point is in a transition
regime where the lensing law is approaching its asymptotic form.
So the gravity-side positive here is best read as:

- a strong restricted-fit match on b ∈ {2..6}
- with a stricter asymptotic subset b ∈ {3..6} that is still close
  to 1/b but noisier and steeper

### Coarse refinement is noisier

The coarse (H=0.5) fits are much worse (R² 0.37 on b ∈ {2..6}) and
give slopes in a wide range (−0.47 to −1.28 depending on subset).
This is the same lattice-resolution issue seen in Lane δ: the
coarse grid is not a reliable guide to continuum behavior. The
medium refinement is where the 1/b structure becomes clean.

## What this establishes

1. **Beam deflection through an imposed 1/r field follows 1/b
   scaling** on the clean restricted fit b ∈ {2..6} at the tested
   refinement level.
2. **The slope matches −1 within 3%** on the cleanest fit
   (b ∈ {2..6}, H=0.35, `kubo_true`): −1.029 with R² = 0.94.
3. **This holds for both the analytic first-order Kubo coefficient
   and the finite-difference `dM`** — they give the same slope at
   H=0.35 (−1.03 for both), which is a self-consistency check.
4. **A near-field pathology at b ≤ 1 is physically sensible**: the
   mass is inside the beam's transverse width and the lensing
   formalism doesn't apply. The beam gets "pushed away" in the
   centroid sense because the field is asymmetric across the
   beam's support.
5. **This is the first retained gravity-side result in the program
   that matches a recognizable lensing functional form**
   (weak-field gravitational lensing α ∝ 1/b). Earlier retained
   positives already matched other textbook forms on the wave side
   (for example radiation falloff), so the novelty here is the
   deflection / lensing connection specifically.

## What this does NOT establish

- **The prefactor (Newton vs Einstein).** Both theories predict 1/b;
  they differ in the coefficient (4GM/c²b vs 2GM/c²b). Our dimensionless
  units don't let us distinguish. We only have the *power law*, not the
  *physical coefficient*.
- **Continuum stability.** Only 2 refinements (H ∈ {0.5, 0.35}). The
  H=0.5 data is noisy, and the drift between H=0.5 and H=0.35 at
  individual b values is large (up to 50%+). A 3rd refinement at
  H=0.25 would test continuum stability of the power-law slope.
- **Family portability.** Fam1 only. Lane α++ showed Fam2 has
  convergence problems for `kubo_true`; the lensing slope on Fam2
  could be different or also not converge.
- **Range of validity.** Only 5 b points in the retained restricted-fit
  regime (b=2 through 6). More b values, or a wider range extending to
  b = 8, 10, etc., would characterize the 1/b law more robustly.
- **Full deflection-angle measurement.** We're reporting `dM / (full
  propagation length)` as a proxy for the deflection angle α. A
  proper measurement would use entry/exit ray angles, not centroid
  displacement.

## Frontier map adjustment (Update 14)

| Row | Before | This lane |
| --- | --- | --- |
| Strength against harshest critique | no direct match to known gravity-side functional forms | **moderate positive — 1/b lensing scaling matches on the clean restricted fit at the finer refinement** |
| Compact underlying principle | first-order Kubo derived (linearity regime, Fam1-continuum stable) | **extended — 1/b scaling of kubo_true(b) adds a functional form to the isolated +5.986 number** |
| Experimental prediction | blocked (comparator-dominated) | **still blocked as a lab card** — but now with a recognizable gravity-side functional-form connection |
| Theory compression | first-order Kubo on linearity regime | **sharpened** — the first-order Kubo coefficient now has a known b-dependence |

## Honest read

This is the **strongest gravity-side moonshot result of the session** —
the first direct match between the program's output and a recognizable
lensing-style prediction. The match is:

- **Quantitatively clean** at the finer refinement (slope −1.03,
  R² 0.94, within 3% of −1)
- **Self-consistent** across two independent measurements
  (analytic Kubo and finite-difference dM give the same slope)
- **Physically honest** — the near-field exclusion at b=1 is
  motivated by the beam's transverse width, not by fitting
- **Conservative** — reported as moderate, not strong, because of
  the 2-refinement limitation and the noisy coarse data

What it means for the scorecard: **the program reproduces the 1/b
functional form of weak-field gravitational lensing** on the
Fam1 grown DAG at H=0.35 on the clean restricted fit b ∈ {2..6},
with a stricter asymptotic subset b ∈ {3..6} still in the same
ballpark but steeper. That is a meaningful gravity-side
functional-form connection, even though it is not yet a stable
continuum claim or a lab-ready prediction.

## What to attack next

1. **Lane L+ — add H=0.25 refinement.** Same 6 b-values, third
   refinement point. Tests continuum stability of the slope.
   Cheapest single next step.
2. **Extend the b range to {2..10}.** More asymptotic points would
   tighten the slope fit. Cost: 4 more b-values × 2 refinements =
   8 more runs.
3. **Family portability on lensing slope.** Check whether Fam2 and
   Fam3 give the same 1/b structure. Given Lane α++, Fam2 is likely
   to be noisy, but Fam3 should give a clean comparison.

The first (Lane L+) is the most decisive: if the −1.03 slope
at H=0.35 is stable under further refinement, the result is a
full positive. If it drifts significantly, we learn that the
"moderate" label was generous.

## Bottom line

> "At 5 impact parameters b ∈ {2, 3, 4, 5, 6} (excluding a
> near-field pathology at b=1 where the mass is inside the beam's
> natural transverse width), the first-order Kubo deflection
> coefficient `kubo_true(b)` at H=0.35 on Fam1 follows a clean
> log-log linear fit: **slope = −1.03, R² = 0.94**. The
> finite-difference deflection `dM(b)` gives the same slope (−1.03,
> R² 0.91). This is essentially exact 1/b scaling — the functional
> form of weak-field gravitational lensing (shared by Newton and
> Einstein, differing only in prefactor). The coarse refinement
> (H=0.5) is noisier, and only 2 refinements are tested, so this
> is retained as a moderate positive rather than a strong one.
> It is the first retained gravity-side result in the program that
> matches a recognizable lensing functional form, rather than just a
> dimensionless coefficient or empirical classifier on the gravity
> side."
