# 3D Correction Master Note

**Date:** 2026-04-08
**Status:** This note documents the systematic 3D correction pass applied to the day's dispersion + lensing analysis. Several conclusions drawn from 2D lattice measurements were found to be **misleading or wrong** when tested on 3D lattice and 3D grown DAG geometries.

## What happened

1. The dispersion relation was first measured on a **2D regular lattice**, giving a clean Schrödinger (non-relativistic) result with R²=0.9995 and Klein-Gordon R²=0.962 — a decisive gap.

2. Based on this, the lensing analysis was reframed as "non-relativistic scattering" and the eikonal comparison was done using 2D geometry.

3. The user asked: **"shouldn't we try all these measures in 3D+1 not 2D? for literally everything we have falsified so far?"**

4. Testing in 3D revealed the 2D conclusions were wrong:

## What changed

### Dispersion relation

| What | 2D conclusion | 3D reality |
| --- | --- | --- |
| Best fit | Schrödinger (R²=0.9995) | Schrödinger ≈ KG (R²=0.994 vs 0.992) |
| KG rejected? | Yes (R²=0.962, decisively poor) | **No** (R²=0.992, nearly tied) |
| Propagator type | "Non-relativistic" | **Undetermined** |
| Clean parabolic? | Yes (monotone decreasing ω(p)) | Mostly (no band peak on DAG) |

**Root cause:** In 2D, the angular weight exp(−β·θ²) integrates over one transverse dimension, giving a clean Gaussian in p-space → clean p². In 3D, it integrates over two transverse dimensions with a 1/L² kernel factor (not 1/L), which modifies the effective dispersion shape enough that Schrödinger and Klein-Gordon become indistinguishable.

### Eikonal lensing comparison

| Model | Slope | Δ from −1.43 |
| --- | ---: | ---: |
| Plane-wave eikonal | −1.28 | 0.15 |
| 2D beam eikonal (β=0.8) | −0.35 | 1.08 |
| **3D beam eikonal (β=0.8, 1/L²)** | **−0.77** | **0.66** |
| Canonical 1/b | −1.00 | 0.43 |
| Lattice (target) | −1.43 | 0.00 |

**Finding:** The 3D beam correction (using cos²θ from the 1/L² kernel) is better than the 2D beam correction (−0.77 vs −0.35) but STILL worse than the plane-wave baseline (−1.28). The plane-wave eikonal remains the best theoretical prediction, now tested against both 2D and 3D beam corrections.

### Intermediate result: 3D regular lattice

The 3D regular lattice (h=0.5, W=6, L=15) showed **band structure** — a dispersion peak near p≈0.7 followed by falloff. None of the three standard forms fit (all R²<0.68). This is NOT seen on the grown DAG, where the randomness smooths out the band edges.

## Notes updated

1. [`DISPERSION_RELATION_NOTE.md`](DISPERSION_RELATION_NOTE.md) — status changed from "retained STRONG POSITIVE" to "NARROWED"; added full geometry comparison table; retracted "non-relativistic" claim for the grown DAG
2. [`BORN_SCATTERING_COMPARISON_NOTE.md`](BORN_SCATTERING_COMPARISON_NOTE.md) — status changed to "NARROWED"; added beam-averaging falsification results; retracted "non-relativistic eikonal" framing
3. [`LENSING_COMBINED_INVARIANT_NOTE.md`](LENSING_COMBINED_INVARIANT_NOTE.md) — added post-hoc analysis section documenting the 3D corrections; updated frontier map

## Scripts added

| Script | What it tests |
| --- | --- |
| `dispersion_3d_lattice.py` | 3D regular lattice dispersion (h=1.0) |
| `dispersion_3d_fine.py` | 3D regular lattice dispersion (h=0.5) |
| `dispersion_grown_dag.py` | **Fam1 grown DAG dispersion** (H=0.5, H=0.35) |
| `eikonal_3d_corrected.py` | 3D beam-averaged eikonal with 1/L² kernel |

## Lesson learned

**Test on the actual physics geometry first.** The 2D regular lattice is a useful analytical sandbox, but its conclusions do not necessarily transfer to the 3D grown DAG. Key differences:

1. **Dimensionality**: 2D → 3D changes the transverse Fourier transform, the kernel normalization (1/L vs 1/L²), and the number of transverse modes.
2. **Randomness**: The grown DAG's positional noise smooths out band-structure artifacts present in the regular 3D lattice, making the dispersion appear cleaner than on the ordered lattice.
3. **Kernel scaling**: The 3D kernel uses H²/L² while the 2D kernel uses h²/L. This changes the effective angular weight and beam width.

Future analyses should run on the grown DAG from the start, using the 2D lattice only as a cross-check.

## Current state of all lensing derivation attempts

| # | Attempt | Slope | Δ | Status |
| ---: | --- | ---: | ---: | --- |
| 1 | Canonical 1/b | −1.00 | 0.43 | Wrong regime |
| 2 | Finite-path Fermat | −1.28* | varies | Falsified (L-independent) |
| 3 | Narrow-beam β=5 | −1.00 | 0.43 | Coincidence (sign flip at H=0.35) |
| 4 | Plane-wave eikonal | −1.28 | **0.15** | **Best available** |
| 5 | 2D beam eikonal | −0.35 | 1.08 | Beam too wide |
| 6 | 3D beam eikonal | −0.77 | 0.66 | Beam still too wide |
| 7 | "Non-relativistic" framing | — | — | Premise wrong (dispersion undetermined) |

The plane-wave eikonal at Δ=0.15 is the closest anyone has come. The remaining gap and the L-independence are open problems.
