# Lensing Slope — Finite-Path Surrogate FALSIFIED at a Second T_phys

**Date:** 2026-04-07 (revised twice: first narrowed by literal-geometry check, then falsified by Lane L++ short-path test)
**Status:** RETRACTED as an explanation of the slope. Two independent issues invalidate the previous "1.5% analytical match" claim:

> **Issue 1 (parallel narrowing, bd14a30):** The "1.5% match" used a
> *centered* finite-path surrogate with `L = 10`. The literal harness
> geometry is NOT centered: the mass is at `x_src ≈ 5`, the beam
> traverses `x ∈ [0, 14.75]`, so the integration is asymmetric. When
> reduced to the actual geometry directly, the analytical surrogate
> gives slope ≈ −1.24 to −1.34 (depending on weighting), not −1.42.
> The "1.5% match" was sensitive to the centering convention.
>
> **Issue 2 (Lane L++ short-path test, this commit):** Even putting
> aside the centering issue, the surrogate makes a clean falsifiable
> regime-transition prediction: at T_phys = 7.5 (L_eff = 5) the slope
> should drop to ≈ −1.73; at T_phys = 45 (L_eff = 30) the slope
> should rise to ≈ −1.08. The Lane L++ short-path measurement at
> T_phys = 7.5 with H=0.25 fine refinement gives slope ≈ −1.44 —
> essentially **identical** to the T_phys=15 measurement of −1.43
> at the same H. The slope is approximately **L-independent** at
> H=0.25 in the tested range, which a ray-deflection formula cannot
> give. The regime-transition prediction is falsified.

The combined picture: the finite-path Fermat formula explains
neither (a) the literal-geometry version of the same observable
nor (b) the slope at a second T_phys value. The "1.5% analytical
match" at T_phys=15 with the centered surrogate was a coincidence
of two narrow choices (centering convention + the specific T value)
that landed on top of the actual measurement.

See [`LENSING_LONG_PATH_TEST_NOTE.md`](LENSING_LONG_PATH_TEST_NOTE.md)
for the Lane L++ falsifying data and the new "L-independent slope"
finding.

## Artifact chain

- [`scripts/lensing_analytical_finite_path.py`](../scripts/lensing_analytical_finite_path.py)
- [`logs/2026-04-07-lensing-analytical-finite-path.txt`](../logs/2026-04-07-lensing-analytical-finite-path.txt)

## Question

Lane L (H=0.35 only) headlined the sweep as "matches 1/b
gravitational lensing" with slope `−1.03`. Lane L+ (H=0.25 added)
downgraded that to "clean power law with exponent ≈ `−1.43`, not
standard 1/b lensing." The natural question was: **why isn't the
model giving the canonical 1/b law?**

The first attempt at an explanation used a centered finite-path
integral with `L = 10` and got an excellent numerical match. The
problem is that this is a **surrogate geometry**, not the literal
geometry used by the harness.

## Useful surrogate vs literal harness geometry

The propagator action `S = L(1−f)` is literally Fermat's principle
with refractive index `n = 1−f`. We impose `f = s/(r + ε)` where
**`r = √((x − x_src)² + (z − z_src)²)`** — this is the **2D**
distance in (x, z), the y coordinate is ignored in
[`imposed_field`](../scripts/kubo_continuum_limit.py).

If one models the observable as a beam passing a mass on a **centered
interaction segment** of length `L`, then the deflection-angle
integral gives the earlier surrogate formula:

```
α_centered(b, L) = s · L / (b · √((L/2)² + b²))
```

This surrogate has the expected three regimes:

1. **L ≫ b** (asymptotic, long-path): √((L/2)² + b²) ≈ L/2, so
   α ≈ s · L / (b · L/2) = **2s/b** → **canonical 1/b lensing**.
   This is the standard Newton/Einstein weak-field deflection.
2. **L ≪ b** (short-path): √((L/2)² + b²) ≈ b, so
   α ≈ s · L / b² → **1/b² falloff**, much steeper.
3. **L ≈ b** (transition regime): power somewhere between −1 and −2.

## What the harness actually does

The literal lensing sweep geometry is different:

- the mass is **static** at `x_src = round(NL/3) · H ≈ 5`
- the beam propagates over the **full** interval `x ∈ [0, (NL−1)H]`
- at `H = 0.25`, the detector is at `x_det = 14.75`
- the imposed field uses the **regularized** denominator `r + 0.1`
- the reported observable is **detector centroid shift** (`dM` / `kubo_true`), not outgoing angle

That means the earlier "`L_eff = 10` because the source is active for
the last 2/3 of the path" interpretation was incorrect for this lane.
`x_src` is the mass position, not an activation time.

## Comparison of surrogate and literal reductions

On the retained fine subset `b ∈ {3, 4, 5, 6}`:

| Model | What it computes | slope | R² | `|Δ slope|` vs measured |
| --- | --- | ---: | ---: | ---: |
| **measured H=0.25** | `kubo_true(b)` | **−1.4335** | **0.9984** | — |
| centered `L=10` surrogate | earlier finite-path formula | **−1.4188** | **0.9988** | **0.0147** |
| actual full path, no regularizer | static mass over `x∈[0,14.75]` | −1.2793 | 0.9992 | 0.1543 |
| actual full path, `r+0.1` | same, literal denominator | −1.2425 | 0.9990 | 0.1910 |
| full path + lever-arm weight | crude detector-shift proxy | −1.3400 | 0.9987 | 0.0936 |

Two facts follow immediately:

1. The earlier `L=10` surrogate really does match the fine slope very well.
2. The **literal harness geometry does not reduce to that surrogate directly**.

So the earlier note was right to notice a finite-path-scale effect,
but too strong in calling it an exact first-principles derivation of
the measured observable.

## What still looks right

- A finite-path / finite-support effect is clearly relevant.
- The clean H=0.25 power law is real.
- The asymptotic `1/b` limit is still the natural long-path expectation
  for the surrogate angle model.

But what is **not** established yet is the exact reduction from the
beam/DAG detector-centroid observable to a 1D analytical formula.
The best current literal proxy is the lever-arm-weighted full-path
integral, and it is still noticeably shallower than the measured
`−1.4335`.

## What would actually close this

There are two clean next moves:

1. **Layer-weighted analytical reduction.**
   Derive the first-order `kubo_true` contribution layer-by-layer from
   the actual free beam, instead of collapsing immediately to a uniform
   1D ray integral.
2. **Long-path numerical test.**
   Increase `T_phys` and check whether the measured slope moves toward
   `−1` as the surrogate model suggests. This is still useful, but it
   should be framed as a test of the heuristic finite-path story, not a
   verification of an already-derived formula.

## What this means for the lensing lane

### What survives

1. **Lane L+ still gives a clean retained gravity-side power law** at
   fine `H`.
2. **A finite-path surrogate can reproduce the slope numerically.**
3. **The exact mechanism is not yet derived** from the literal harness
   geometry.

### The honest framing

The Lane L "`1/b` match" headline was wrong. The Lane L+ downgrade to
"clean non-standard power law" was numerically right. The attempted
finite-path rescue then went too far in the opposite direction: it
used a surrogate centered-segment formula that matches the fine slope,
but treated that surrogate as if it were the literal static-mass
harness geometry.

The retained claim should now be:

> "The fine lensing lane retains a clean gravity-side power law
> (`−1.4335`, `R² = 0.9984` on `b ∈ {3..6}` at `H=0.25`). A centered
> finite-path surrogate reproduces that slope closely, which is strong
> evidence that finite-path / finite-support effects matter. But the
> literal static-mass full-path geometry gives a shallower slope
> (`≈ −1.24` to `−1.34` in the tested reductions), so the exact
> analytical reduction of the detector-centroid observable remains open."

## Frontier map adjustment (revised)

| Row | Lane L+ (downgraded) | Revised read |
| --- | --- | --- |
| Strength against harshest critique | "downgrade — clean power law but non-standard exponent" | **partial recovery** — finite-path effects clearly matter, but the exact reduction is not derived yet |
| Compact underlying principle | "kubo_true(b) is a clean power law with non-standard exponent" | **better heuristic picture, not yet a closed derivation** |
| Experimental prediction | "partial — clean functional form but not matching known weak-field lensing" | **still partial** — long-path test remains useful, but current slope explanation is heuristic |
| Theory compression | "sharpened differently" | **sharpened, but still open** — literal beam-weighted reduction is the next target |

## Honest read

This is not the strong rescue it first looked like.

What is real:

- the fine H=0.25 power law is real
- the simple centered finite-path surrogate really does reproduce the slope
- finite-path / finite-support effects are therefore a serious clue

What is not yet real:

- an exact first-principles derivation of the measured `−1.4335` from
  the literal harness geometry
- a clean statement that the current setup is already explained by the
  static full-path 2D `1/r` integral

So this note stays valuable, but as a **diagnostic narrowing**, not as
the final explanation.

## Bottom line

> "The fine lensing lane measures a clean power law
> (`−1.4335`, `R² = 0.9984` on `b ∈ {3..6}` at `H=0.25`). A centered
> finite-path surrogate reproduces that slope almost exactly, so
> finite-path effects are clearly implicated. But the literal
> static-mass full-path geometry gives a shallower slope
> (`≈ −1.24` to `−1.34` in the tested reductions), so the current
> 'finite-path explanation' is not yet a closed first-principles
> derivation. The right next move is a layer-weighted reduction of
> the actual detector-centroid observable, or a long-path numerical
> test framed as a heuristic check rather than a proof."
