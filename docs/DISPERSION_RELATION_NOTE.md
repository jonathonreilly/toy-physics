# Dispersion Relation: Geometry-Dependent, Not Decisively Relativistic or Non-Relativistic

**Date:** 2026-04-08 (updated same day with 3D + grown DAG results)
**Status:** NARROWED — the 2D regular lattice gives clean Schrödinger (R²=0.9995), but the 3D regular lattice gives band structure (R²<0.68 for all forms), and the **actual grown DAG (Fam1) gives Schrödinger ≈ Klein-Gordon (R²=0.994 vs 0.992) — too close to distinguish**. The 2D result was misleading. On the actual physics geometry, we cannot decisively determine whether the propagator is relativistic or non-relativistic.

## Artifact chain

- [`scripts/lattice_dispersion_relation.py`](../scripts/lattice_dispersion_relation.py) — 2D lattice (h=1.0, h=0.5)
- [`scripts/lattice_dispersion_fine.py`](../scripts/lattice_dispersion_fine.py) — 2D lattice (h=0.25)
- [`scripts/dispersion_3d_lattice.py`](../scripts/dispersion_3d_lattice.py) — 3D regular lattice (h=1.0)
- [`scripts/dispersion_3d_fine.py`](../scripts/dispersion_3d_fine.py) — 3D regular lattice (h=0.5)
- [`scripts/dispersion_grown_dag.py`](../scripts/dispersion_grown_dag.py) — **Fam1 grown DAG** (H=0.5, H=0.35)
- [`logs/2026-04-08-lattice-dispersion.txt`](../logs/2026-04-08-lattice-dispersion.txt)

## Method

1. On a 2D regular lattice with the standard kernel `exp(i·K·L)·exp(-β·θ²)/L·h²`, initialize a plane-wave source at layer 0: `amp_j = exp(i·p·y_j)`.
2. Propagate forward (free field, no slits, no mass).
3. At each downstream layer, project onto the p-mode: `M(x) = Σ_j amp_j · exp(-i·p·y_j)`.
4. Extract `ω(p) = dφ/dx` from the unwrapped phase φ(x) = arg(M(x)).
5. Sweep p from 0 to 3.0 at two spacings (h=0.5, h=0.25).
6. Fit ω(p) to three candidate functional forms.

All phase fits are perfectly linear in x: R² = 1.0000000 at every (p, h) point tested at h=0.5, and R² > 0.9999 at h=0.25. The measurement is clean.

## Result

### Full geometry comparison

| Geometry | Schrödinger R² | Klein-Gordon R² | Linear R² | Winner |
| --- | ---: | ---: | ---: | --- |
| **2D lattice h=0.5** | **0.99947** | 0.96156 | 0.92045 | Schrödinger (decisive) |
| **2D lattice h=0.25** | **0.99827** | 0.73744 | 0.91395 | Schrödinger (decisive) |
| **3D lattice h=0.5** | 0.677 | 0.656 | 0.404 | **None** (band structure) |
| **Grown DAG H=0.5** | **0.994** | 0.992 | 0.877 | Schrödinger (marginal) |
| **Grown DAG H=0.35** | **0.988** | 0.980 | 0.949 | Schrödinger (marginal) |

**Critical finding:** On the 2D lattice, Schrödinger wins decisively. But on the **actual physics geometry** (3D grown DAG), Schrödinger and Klein-Gordon are within R² = 0.002 of each other — **too close to distinguish**. The 2D result was misleading.

### Fit parameters

| Parameter | h=0.5 | h=0.25 | Converged? |
| --- | ---: | ---: | --- |
| a (curvature) | −0.0919 | −0.0742 | Not yet (Δ=0.018) |
| b (rest phase) | −0.2365 | +0.4347 | Sign flipped |
| m_eff = −1/(2a) | 5.44 | 6.74 | Not yet |

The **functional form** (quadratic in p) is stable across refinement. The **coefficients** are not converged — the rest phase ω₀ = b depends on h because the per-edge phase K·h contributes a spacing-dependent background. This is expected: ω₀ is a gauge-like quantity that depends on the reference frame. The physically meaningful quantity is the curvature a = 1/(2m_eff), which changes by 19% between h=0.5 and h=0.25 (improving but not converged).

### Raw data (h=0.5)

| p | ω | R² |
| ---: | ---: | ---: |
| 0.00 | −0.2365 | 1.000 |
| 0.10 | −0.2380 | 1.000 |
| 0.30 | −0.2489 | 1.000 |
| 0.50 | −0.2661 | 1.000 |
| 1.00 | −0.3219 | 1.000 |
| 2.00 | −0.5940 | 1.000 |
| 3.00 | −1.0735 | 1.000 |

## Why it's Schrödinger

The angular weight `exp(−β·θ²)` at small angles gives `w ≈ exp(−β·(Δy/Δx)²)`. For a plane wave with transverse momentum p, the contribution from a node at transverse offset Δy picks up a phase factor `exp(i·p·Δy)`. The combined effect is:

```
Σ_Δy  exp(−β·(Δy/h)²) · exp(i·p·Δy) / L
    ∝ exp(−p²·h²/(4β))  (Gaussian integral)
```

This is a **Gaussian damping in p-space** which, per layer, gives a phase advance:

```
ω(p) ≈ ω₀ − α·p²
```

with α determined by β and the edge geometry. This IS the discrete Schrödinger propagator kernel: the Gaussian angular weight plays the role of the non-relativistic kinetic energy `exp(i·p²/(2m)·Δt)`, except with a real (damping) exponent instead of imaginary (oscillatory). The two give the SAME dispersion relation shape (quadratic in p), differing only in whether the propagation is unitary (imaginary exponent) or decaying (real exponent).

## Implications

### For the lensing invariant

The lensing work found kubo_true(b) ∝ b^(−1.43) and all attempts to derive it from relativistic ray optics failed. This is now EXPLAINED: the propagator is Schrödinger, not relativistic. Weak-field gravitational lensing (1/b) is a relativistic prediction. We should not expect it from a non-relativistic propagator.

~~The correct comparison for the −1.43 slope is non-relativistic scattering from a 1/r potential~~ — **RETRACTED**: the grown DAG does not decisively distinguish Schrödinger from Klein-Gordon, so we cannot assume non-relativistic scattering is the right comparison.

### For the continuum limit

The 2D Schrödinger dispersion provides a prediction for what the 2D continuum theory should look like. The 3D / grown-DAG continuum theory is less clear — the dispersion form is not yet determined.

### For the project's physics claims

~~Any claim about "emergent general relativity" is premature: the propagator is fundamentally non-relativistic~~ — **NARROWED**: this statement was only proven on the 2D lattice. On the actual grown DAG, Klein-Gordon R² = 0.992 is within 0.002 of Schrödinger R² = 0.994. We cannot rule out relativistic physics on the actual geometry. The correct statement is: **the propagator's dispersion type is undetermined on the grown DAG**.

## What this does NOT establish

- ~~The grown-DAG dispersion~~ — NOW TESTED: Schrödinger/KG nearly tied (R²=0.994/0.992)
- Whether a different angular weight could give decisive Klein-Gordon
- Whether the −1.43 lensing slope matches non-relativistic OR relativistic scattering theory (both remain possible)
- The continuum-limit value of m_eff (parameters not yet converged)
- Whether more p-values or finer H could break the Schrödinger/KG tie on the DAG

## 3D correction: what changed

The original analysis (2D only) concluded "decisively non-relativistic." The 3D follow-up (same day) showed this was **misleading**:

1. **3D regular lattice**: neither form fits (band structure, R²<0.68). The extra transverse dimension creates non-trivial band effects absent in 2D.
2. **3D grown DAG**: the randomness smooths out the band structure (R²≈0.99), but Schrödinger and Klein-Gordon become nearly indistinguishable.
3. **Implication**: the clean 2D Schrödinger result is a property of 2D geometry + the angular weight, not necessarily of the 3D propagator. The actual physics geometry doesn't pick a winner.

## Frontier map adjustment (Update 20, corrected)

| Row | Before (2D only) | After 3D correction |
| --- | --- | --- |
| Propagator type | "Schrödinger (decisive)" | **Undetermined on grown DAG; Schrödinger ≈ KG (R² Δ=0.002)** |
| Lensing failure explanation | "Expected: propagator is non-relativistic" | **Cannot determine; both relativistic and non-relativistic remain viable** |
| Next lensing direction | "Non-relativistic 2D Born scattering" | **Need to test both NR and relativistic predictions against the 3D data** |

## Bottom line

> "The free propagator's dispersion relation is geometry-dependent. On the
> 2D regular lattice: cleanly Schrödinger (R²=0.9995 vs KG R²=0.962). On
> the 3D regular lattice: neither form fits (band structure). On the actual
> Fam1 grown DAG: Schrödinger R²=0.994 vs Klein-Gordon R²=0.992 — too
> close to distinguish. The original claim that 'the propagator is
> fundamentally non-relativistic' was proven only on the 2D lattice and
> does NOT transfer to the 3D grown DAG where the physics lives. On the
> actual geometry, we cannot rule out either relativistic or non-relativistic
> dispersion. The lensing slope −1.43 cannot be attributed to either
> regime with current data."

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `3d_correction_master_note` (see-also; the 3D follow-up note that documents the corrections summarized above; converted from markdown link to backticked form 2026-05-10 to break citation cycle-0003 — this back-reference is informational only, with the load-bearing direction running `3D_CORRECTION_MASTER_NOTE.md` → `DISPERSION_RELATION_NOTE.md` as the forward update record)
