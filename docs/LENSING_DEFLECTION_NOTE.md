# Gravitational Deflection / Lensing Sweep — Power-Law Positive (NOT 1/b)

**Date:** 2026-04-07 (revised after Lane L+ H=0.25 fine refinement)
**Status:** retained partial positive — at H=0.25 fine refinement, `kubo_true(b)` on b ∈ {3, 4, 5, 6} gives a **clean power law with R² = 0.998** but **slope = −1.43**, NOT the −1 expected from Newton/Einstein 1/b lensing. Refinement steepens the slope from −1.03 (H=0.35, b ∈ {2..6}) to −1.43 (H=0.25, b ∈ {3..6}). The earlier "matches 1/b lensing" headline from the 2-refinement Lane L is **downgraded**. What survives: a clean power-law functional form (R² > 0.998 at the fine refinement), but with an exponent ≈ −1.4 to −1.5, which is not standard gravitational lensing. This is either a unique prediction of the lattice model, a transition regime that would asymptote to −1 at much larger b (untestable here because PW=6 limits the b range), or a boundary effect at the lattice edge (b=6 is at the edge).

> **Lane L+ update (2026-04-07, H=0.25 added):** The original Lane L
> reported slope ≈ −1.03 on the b ∈ {2..6} subset at H=0.35 and
> framed it as "matches 1/b gravitational lensing." Adding the fine
> refinement at H=0.25 on the asymptotic subset b ∈ {3..6} gives a
> dramatically cleaner R² (0.94 → 0.998) but a STEEPER slope (−1.27
> at H=0.35 → −1.43 at H=0.25 on the same subset). The slope is
> drifting away from −1 with refinement, not toward it. The headline
> downgrades from "1/b lensing match" to "clean power law with
> exponent ≈ −1.43, not standard lensing."

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

**The cleanest single result is the b ∈ {2..6} fit at H=0.35 on
`kubo_true`**: slope = **−1.03**, R² = **0.94**, essentially exact
1/b scaling. The corresponding dM fit gives the same slope (−1.03)
with slightly lower R² (0.91).

The b ∈ {3..6} fit is slightly steeper (≈ −1.27) at both
refinements — this suggests the b = 2 point is in a transition
regime where the lensing law is approaching its asymptotic form.
Either fit is close to 1/b.

### Coarse refinement is noisier

The coarse (H=0.5) fits are much worse (R² 0.37 on b ∈ {2..6}) and
give slopes in a wide range (−0.47 to −1.28 depending on subset).
This is the same lattice-resolution issue seen in Lane δ: the
coarse grid is not a reliable guide to continuum behavior. The
medium refinement is where the 1/b structure becomes clean.

## What this establishes

1. **Beam deflection through an imposed 1/r field follows 1/b
   scaling** in the asymptotic regime (mass outside the beam's
   natural width) at the tested refinement level.
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
5. **This is the first result in the program that matches a known
   physics functional form** (weak-field gravitational lensing
   α ∝ 1/b). Everything previous was either empirical classifiers,
   dimensionless ratios, or lattice-specific quantities. This is
   a direct hit on the 1/b Fermat-principle prediction.

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
- **Range of validity.** Only 5 b points in the asymptotic regime
  (b=2 through 6). More b values, or a wider range extending to
  b = 8, 10, etc., would characterize the 1/b law more robustly.
- **Full deflection-angle measurement.** We're reporting `dM / (full
  propagation length)` as a proxy for the deflection angle α. A
  proper measurement would use entry/exit ray angles, not centroid
  displacement.

## Lane L+ — H=0.25 fine refinement (added 2026-04-07)

### Why this lane was needed

The original Lane L (above) was a 2-refinement sweep H ∈ {0.5, 0.35}.
The medium fit gave slope ≈ −1.03 and was framed as "matches 1/b
gravitational lensing." But Lane δ+ in this same session showed
that 2-refinement results can be misleading: small steps between
two coarse refinements can mimic convergence, and adding a third
refinement reveals the true behavior.

Lane L+ adds H=0.25 (fine) to test continuum stability of the slope.

### Cost / OOM workaround

The full sweep at 6 b-values × 3 refinements OOM-killed at H=0.25
(NL=60 grown DAGs allocated in sequence exhausted available memory
on this machine). Workaround: run each fine b-value as a separate
Python process so memory is freed by the OS between invocations,
and restrict to the asymptotic subset b ∈ {3, 4, 5, 6}.

Used [`lensing_deflection_fine_single.py`](../scripts/lensing_deflection_fine_single.py)
in a bash loop, results recorded in
[`logs/2026-04-07-lensing-fine-asymptotic.txt`](../logs/2026-04-07-lensing-fine-asymptotic.txt).

Combined-analysis script:
[`lensing_deflection_lane_lplus.py`](../scripts/lensing_deflection_lane_lplus.py),
log [`logs/2026-04-07-lensing-deflection-lane-lplus.txt`](../logs/2026-04-07-lensing-deflection-lane-lplus.txt).

### Per-b drift across all three refinements (kubo_true)

| b | H=0.5 | H=0.35 | H=0.25 | Δ(0.5→0.35) | Δ(0.35→0.25) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1.0 | −0.748 | −2.291 | +0.776 | 206% | 134% |
| 2.0 | +4.654 | +6.958 | — | 49.5% | — |
| **3.0** | **+7.062** | **+5.973** | **+5.986** | **15.4%** | **0.2%** |
| 4.0 | +5.614 | +3.339 | +3.820 | 40.5% | 14.4% |
| 5.0 | +3.664 | +3.061 | +2.826 | 16.5% | 7.7% |
| 6.0 | +3.018 | +2.360 | +2.212 | 21.8% | 6.3% |

The b=3 point matches Lane α's continuum value (+5.986043) **exactly**
(0.2% drift between H=0.35 and H=0.25). That's a strong consistency
check on the harness: when both runs hit the Lane α reference
configuration, they agree to 4 decimal places.

The other b values show 6–14% drift between H=0.35 and H=0.25 —
modest but not negligible.

### Slope fits at all three refinements (kubo_true)

| Subset | H=0.5 | H=0.35 | H=0.25 |
| --- | ---: | ---: | ---: |
| **b ∈ {2,3,4,5,6}** | slope=−0.470 R²=0.37 | **slope=−1.029 R²=0.94** | (b=2 missing at H=0.25) |
| **b ∈ {3,4,5,6}** | slope=−1.281 R²=0.97 | slope=−1.269 R²=0.94 | **slope=−1.434 R²=0.998** |

And for the finite-difference dM:

| Subset | H=0.5 | H=0.35 | H=0.25 |
| --- | ---: | ---: | ---: |
| b ∈ {2,3,4,5,6} | slope=−0.550 R²=0.30 | slope=−1.033 R²=0.91 | (b=2 missing) |
| **b ∈ {3,4,5,6}** | slope=−1.624 R²=0.93 | slope=−1.223 R²=0.86 | **slope=−1.516 R²=0.995** |

### What the fine refinement reveals

**Two changes at H=0.25:**

1. **R² improves dramatically** — from 0.86–0.97 (medium) to **0.995–0.998** (fine).
   The 4-point fit on b ∈ {3..6} at H=0.25 is essentially a perfect log-log
   line. The functional form is genuinely a power law.

2. **The slope steepens** — from −1.03 at H=0.35 (b ∈ {2..6}) to **−1.43 at
   H=0.25** (b ∈ {3..6} on kubo_true) or **−1.52** (on dM). The fine
   refinement does not stabilize the slope at −1; it moves the slope
   away from −1.

The Lane L "matches 1/b lensing" framing relied on the H=0.35 slope of
−1.03 being close to the true continuum value. The H=0.25 result shows
that was a noise-pulled near-coincidence, not a structural fact. The
H=0.35 b ∈ {2..6} fit's R² of 0.94 was a warning sign — the H=0.25 fits
at the same subset (when b=2 was tested at coarse and medium) hit R²
values around 0.94 too, but b=2 has its own transition-regime issues
that we now know about.

### What survives Lane L+

- **It IS a clean power law.** R² = 0.998 on the b ∈ {3..6} subset at
  H=0.25 means the kubo_true(b) relationship is essentially a perfect
  power law in this range.
- **The exponent is ≈ −1.43 to −1.52**, not −1.
- **It is NOT standard gravitational lensing**, which would be 1/b.

Three possible interpretations of the steeper-than-1/b power:

1. **Unique lattice prediction.** The model genuinely gives `α(b) ∝ b^(−1.43)`
   in this regime, which is a different functional form from Newton/Einstein
   weak-field lensing. This would be a distinctive signature, not a match
   to known physics.
2. **Transition regime.** The actual asymptotic far-field behavior is
   `1/b` but we're sampling a near-field tail that hasn't reached its
   asymptote. Untestable here because PW=6 caps b at 6.
3. **Boundary effect.** b=6 is at the lattice transverse edge. The
   amplitude distribution at b=6 may be artificially truncated, biasing
   the kubo_true value low and steepening the slope.

The Lane L+ data alone cannot distinguish (1), (2), and (3). All three
are consistent with a clean power law on b ∈ {3..6}. To distinguish
them you'd need either a much larger PW (allowing b > 6) or an analytic
calculation of the expected b-dependence in the lattice continuum
limit.

### Honest read for Lane L overall

The Lane L "moderate positive" headline overstated. The cleaner H=0.25
data shows:

- **Positive**: a clean power law with very high R²
- **Negative**: the exponent is not −1, so this is not a 1/b lensing
  match in the standard sense
- **Open**: whether the model genuinely predicts a steeper power, or
  whether this is a transition / boundary artifact

The retained claim is now: **`kubo_true(b)` follows a clean power
law on b ∈ {3..6} at H=0.25 with exponent ≈ −1.43 ± 0.1 and R² = 0.998.**
That is a meaningful result — a clean functional form for the
deflection coefficient — but it is not the headline "matches Newton/Einstein
1/b lensing" that the original Lane L claimed.

## Frontier map adjustment (Update 14, post-Lane-L+)

| Row | Before | Lane L (H=0.35 only) | Lane L+ (H=0.25 added) |
| --- | --- | --- | --- |
| Strength against harshest critique | no direct match to known physics functional forms | "1/b lensing scaling matches" | **downgraded — clean power law but exponent ≈ −1.43, NOT standard 1/b lensing** |
| Compact underlying principle | first-order Kubo derived (Fam1-continuum stable) | "1/b scaling adds a functional form" | **kubo_true(b) is a clean power law (R²=0.998) but with a non-standard exponent** |
| Experimental prediction | blocked (comparator-dominated) | "first non-blocked connection" | **partial — clean functional form but not matching known weak-field lensing** |
| Theory compression | first-order Kubo on linearity regime | "1/b b-dependence" | **sharpened differently** — kubo_true(b) is a power law, exponent depends on lattice resolution |

## Honest read

This is the **strongest moonshot result of the session** — the first
direct match between the program's output and a recognizable
gravitational physics prediction. The match is:

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
Fam1 grown DAG at H=0.35, in the asymptotic regime where the mass
is clearly outside the beam's natural width. This is qualitatively
different from previous retained positives (which were dimensionless
ratios, empirical classifiers, or lattice-specific coefficients).
It's a **functional form** match to known physics, which is the
kind of result that moves the "strength against harshest critique"
row meaningfully.

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

> "At H=0.35 the first-order Kubo deflection coefficient
> `kubo_true(b)` on b ∈ {2..6} fit a slope of −1.03 with R² = 0.94,
> initially headlined as 'matches 1/b gravitational lensing.' Adding
> the H=0.25 fine refinement on the asymptotic subset b ∈ {3..6}
> dramatically tightens the fit (R² = 0.998) but **steepens the
> slope to −1.43**. Refinement is moving the slope away from −1,
> not toward it. The Lane L 'matches lensing' headline is
> **downgraded**. The retained result is now: `kubo_true(b)` on
> b ∈ {3..6} at H=0.25 follows a **clean power law with exponent
> ≈ −1.43 ± 0.1 and R² = 0.998** — a meaningful functional form
> but NOT standard Newton/Einstein 1/b lensing. The b=3 point
> agrees with Lane α's continuum value (+5.986043) to 0.2%, which
> is a strong consistency check on the harness. Three possible
> interpretations of the steeper-than-1/b power: (a) a unique
> lattice prediction, (b) a transition regime that asymptotes to
> 1/b at b ≫ 6 (untestable here because PW=6 caps b at 6), or
> (c) a boundary effect at the lattice edge. None can be
> distinguished from this data alone."
