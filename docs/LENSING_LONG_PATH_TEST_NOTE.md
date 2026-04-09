# Lensing Long-Path Test — Falsifies the Finite-Path Explanation

**Date:** 2026-04-07
**Status:** retained negative for the previous "finite-path explains the slope" claim, but a NEW positive finding: the measured slope of `kubo_true(b)` on b ∈ {3..6} at H=0.25 fine refinement is **≈ −1.43 independent of T_phys** in the tested range (T=7.5, 15). The analytical Fermat finite-path formula predicts very different slopes at the two T values (−1.73 and −1.42), so it does NOT explain the measurement. The previous "1.5% match at T=15" was a single-point coincidence. The actual finding — an L-independent slope ≈ −1.43 — is a different and unexplained physics fact that warrants its own investigation.

## Artifact chain

- [`scripts/lensing_long_path_test.py`](../scripts/lensing_long_path_test.py)
- [`logs/2026-04-07-lensing-long-path-test.txt`](../logs/2026-04-07-lensing-long-path-test.txt)
- Falsifies: [`LENSING_FINITE_PATH_EXPLANATION_NOTE.md`](LENSING_FINITE_PATH_EXPLANATION_NOTE.md)

## Question

The previous explanation note claimed:

> "The Lane L+ measured slope of −1.43 on b ∈ {3..6} at H=0.25 matches
> the analytical finite-path-length deflection formula
> α(b, L) = s·L/(b·√((L/2)² + b²)) with L_eff = 10 to within 1.5%."

If true, this would generate a clean falsifiable prediction: at
T_phys = 7.5 (L_eff = 5), the slope should drop to ≈ −1.73. At
T_phys = 45 (L_eff = 30), the slope should rise to ≈ −1.08.

This lane runs both tests.

## Setup

Self-contained harness that reuses the Lane L parallel-perturbation
propagator but accepts arbitrary T_phys (overriding the default 15.0):

- Same physical parameters as Lane L: PW=6, k*H=2.5, S=0.004, Fam1
- Same b values: {3, 4, 5, 6}
- Same `imposed_field` (2D 1/r in (x, z))
- Two new T_phys values: **7.5** (short path, predicted slope −1.73)
  and **45** (long path, predicted slope −1.08)
- Refinements:
  - T_phys=7.5: tested at H ∈ {0.5, 0.35, 0.25} (small lattice, all feasible)
  - T_phys=45: tested at H=0.5 only (NL=90 dominates memory)

## Result

### Short path (T_phys=7.5, L_eff=5)

| H | NL | slope (kubo) | R² | analytical | \|Δ\| |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 15 | −1.39 | 0.99 | −1.73 | 0.35 |
| 0.35 | 21 | −1.49 | 1.00 | −1.73 | 0.25 |
| **0.25** | **30** | **−1.44** | **1.00** | **−1.73** | **0.30** |

### Long path (T_phys=45, L_eff=30)

| H | NL | slope (kubo) | R² | analytical | \|Δ\| |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 90 | −1.81 | 0.69 | −1.08 | 0.74 |

The long-path H=0.5 fit has very poor R² (0.69) because the per-b
data is **non-monotone** (b=4 spikes 32% above b=3). At T_phys=15
the same H=0.5 lattice gave clean monotone data — so the non-monotone
behavior at T_phys=45 H=0.5 is most likely a beam-diffraction
artifact at long propagation length on a coarse lattice. We do
NOT have fine-H data at T_phys=45 to disentangle.

### Comparison: H=0.25 measurements at T=7.5 and T=15

The decisive comparison is at H=0.25 fine refinement:

| T_phys | L_eff | measured slope | analytical predict | difference |
| ---: | ---: | ---: | ---: | ---: |
| 7.5 | 5 | **−1.44** | −1.73 | 0.29 |
| 15 | 10 | **−1.43** | −1.42 | 0.01 |

**At H=0.25 fine refinement, the measured slope is essentially
identical at T=7.5 and T=15 (−1.44 vs −1.43)**, but the analytical
formula predicts completely different values (−1.73 vs −1.42).

The kubo curves themselves are also striking:

| b | T=7.5 H=0.25 | T=15 H=0.25 | ratio (T=15/T=7.5) |
| ---: | ---: | ---: | ---: |
| 3 | 2.456 | 5.986 | 2.44 |
| 4 | 1.669 | 3.820 | 2.29 |
| 5 | 1.211 | 2.826 | 2.34 |
| 6 | 0.904 | 2.212 | 2.46 |

The ratio is essentially constant (2.30–2.46). **The T=15 curve is
just a uniform 2.4× scaled version of the T=7.5 curve** — same shape,
different overall normalization. A ray-deflection formula with
different L would give different slopes, not the same slope at a
different scale.

## What this falsifies

The previous explanation note claimed the Fermat finite-path
formula explained the slope. **It does not.** The "1.5% match at
T_phys=15" was a coincidence: the analytical −1.42 happens to fall
essentially on top of the measured −1.43 at that one T value. At
T=7.5 the analytical predicts −1.73 but the measurement gives −1.44.

The previous note's "regime test" table predicted that varying T_phys
should produce different slopes (−1.73 → −1.42 → −1.08 as T grows).
**This regime transition is not observed** at H=0.25 fine refinement
in the tested T range.

## What the new finding suggests

**The slope ≈ −1.43 appears to be a property of the model that is
independent of L (in the tested range) at the H=0.25 fine refinement.**

This is consistent with `kubo_true` being a wave-mechanical Kubo
response, not a ray deflection. For a delocalized beam (which our
propagator gives — it's a heavily diffracting wavefront, not a
focused ray), the centroid response under a small phase perturbation
is determined by the propagator's intrinsic spatial response
function, which depends on the b range and the propagator's
angular weighting (the `BETA = 0.8` parameter), but NOT on L in
the same way that ray-deflection geometry would.

What we'd need to actually understand the slope:

1. **An analytic calculation of `kubo_true(b)` for the actual
   wave-mechanical propagator**, not just for a ray. This involves
   evaluating the Kubo formula `<z · ∂H/∂s>` over the propagator's
   amplitude distribution. Much harder than the ray-formula
   integral.
2. **A test of whether the slope depends on `BETA`**, the
   angular weight parameter. If the slope changes with BETA, it
   confirms the slope is determined by the propagator's path
   distribution (which BETA controls). If it doesn't, the slope
   is determined by something else.
3. **A test at a different propagator coupling `k`**. The phase
   per edge is `k·L·(1−f)`. Varying k changes how strongly the
   field couples to the beam. If the slope is independent of k,
   it's purely geometric. If it depends on k, it's a coupled
   wave-mechanical effect.

None of these is in this lane. They're queued for follow-up.

## What survives from Lane L / Lane L+

What is NOT changed by this falsification:

1. **The model still gives a clean power law in b ∈ {3..6}** at
   the H=0.25 fine refinement. R² = 0.998 on the kubo_true fit.
2. **The slope is reproducible**: same value (−1.43 to −1.44) at
   two different T_phys. Whatever determines it is robust.
3. **The b=3 reference point still matches Lane α** (kubo_true =
   +5.986 at T_phys=15, b=3, H=0.25, which is the Lane α reference
   configuration).
4. **The deflection IS toward the mass** (positive sign of dM)
   for all b ∈ {3..6} at all tested T_phys. Gravity sign is
   correct in this regime.

What IS changed:

- The Lane L "matches 1/b lensing" headline — already downgraded
  by Lane L+ — is now **also** not explained by the finite-path
  formula. The slope is non-canonical AND non-Fermat.
- The previous "STRONG positive" claim that the slope was
  derived from first principles is RETRACTED.
- The retained finding now is just: a clean power law of unknown
  origin, with slope ≈ −1.43, independent of L_eff in the tested
  range at H=0.25 fine refinement.

## Frontier map adjustment (Update 16)

| Row | Update 15 (finite-path explanation) | Update 16 (this falsification) |
| --- | --- | --- |
| Strength against harshest critique | "STRONG — first-principles match at 1.5%" | **retracted to weak partial — clean power law of unknown origin, slope ≈ −1.43** |
| Compact underlying principle | "derived from analytical formula" | **NOT derived** — analytical formula doesn't match at multiple T values |
| Experimental prediction | "falsifiable regime transition" | **prediction tested and FALSIFIED** at the next data point |
| Theory compression | "derived deflection law" | **back to open** — actual mechanism is unexplained |

## Honest read

This is a hard but important reversal. The previous note claimed
a strong first-principles result; the falsifying data shows that
claim was based on a single-point coincidence. The honest current
status is:

- The model gives a clean power law `kubo_true(b) ∝ b^(−1.43)`
  on b ∈ {3..6} at fine refinement
- This slope is reproducible across two different T_phys values
- It is NOT what the 2D Fermat ray formula predicts (the formula
  predicts a strong T-dependence; the measurement shows essentially
  no T-dependence)
- The actual mechanism that gives this slope is **unknown**

The session's net pattern is: every "moonshot positive" we've claimed
has either been narrowed, downgraded, or now falsified. This is the
right behavior of honest science — claims that don't survive the
next test get retracted. But it does mean the program currently has
NO retained "strong positive" on the gravity-side functional-form row.

What remains real:

- The wave equation's continuum-stable physics (Lanes 4-8b on the
  scorecard, unaffected by any of today's lensing work)
- The first-order Kubo derivation on the linearity-regime subset
  (Lane α on Fam1, +5.986 with 0.2% drift; Fam3 agrees to 0.5%)
- The retained negatives that constrain the program (matter,
  classifier, comparator, and now the lensing finite-path
  explanation)

## What to attack next

1. **Derive `kubo_true(b)` from the actual adjoint-weighted path-sum**,
   not a ray approximation. This is the active mechanism lane now.
2. **Test slope dependence on `k`** (propagator coupling).
   Same idea, different parameter.
3. **Family sweep on the retained fine-`H` slope** to see whether the
   broad-kernel mechanism is Fam1-specific or shared.
4. **Stop claiming gravity-side first-principles matches** until
   one survives a regime-transition test.

## Bottom line

> "The Lane L++ short-path test (T_phys=7.5) at H=0.25 fine
> refinement gives slope = −1.44, essentially identical to the
> T_phys=15 measurement of −1.43. The analytical Fermat finite-path
> formula predicts very different slopes at the two T values (−1.73
> vs −1.42), so the previous 'finite-path explanation' note is
> falsified. The match at T=15 was a single-point coincidence.
> The actual finding — that the kubo_true(b) slope is approximately
> L-independent at H=0.25 fine refinement — is a different and
> unexplained physics fact. The program currently has NO retained
> first-principles derivation of the gravity-side slope, only the
> empirical observation that it's a clean power law with exponent
> ≈ −1.43 on b ∈ {3..6}."
