# Born/Eikonal Scattering Comparison with Lattice Lensing

**Date:** 2026-04-08 (updated same day with 3D corrections)
**Status:** NARROWED — the plane-wave eikonal gives slope −1.28 (Δ=0.15 from lattice), which remains the closest theoretical prediction. Beam-averaging corrections (both 2D and 3D) WORSEN the match. The original framing as "non-relativistic eikonal" was based on the 2D Schrödinger characterization, which does NOT transfer to the 3D grown DAG (where Schrödinger and Klein-Gordon are indistinguishable). The eikonal integral itself is geometry-agnostic — it's the same regardless of whether the underlying dispersion is relativistic or non-relativistic.

## Context

The [dispersion relation measurement](DISPERSION_RELATION_NOTE.md) originally established Schrödinger on 2D lattice, but 3D follow-up showed **Schrödinger ≈ Klein-Gordon on the actual grown DAG** (R² Δ=0.002). The eikonal comparison is valid regardless of the dispersion type — it's a geometric-optics prediction for the deflection integral along a straight path through a 1/r potential.

## The prediction

For a non-relativistic particle on a straight path from x=0 to x=L, passing a 2D 1/r potential at (x_src, b), the eikonal deflection integral gives:

```
I_geom(b) = (1/b) · [(L-x_src)/√((L-x_src)²+b²) + x_src/√(x_src²+b²)]
```

At the lattice configuration (L=15, x_src=5):

| b | I_geom | local slope |
| ---: | ---: | ---: |
| 3 | 0.605 | — |
| 4 | 0.427 | −1.21 |
| 5 | 0.320 | −1.29 |
| 6 | 0.250 | −1.37 |

Power-law fit on b ∈ {3..6}: **I_geom ≈ 2.48 · b^(−1.28)**, R² = 0.999.

## Comparison

| Quantity | Eikonal prediction | Lattice measurement |
| --- | ---: | ---: |
| Slope on b ∈ {3..6} | −1.28 | −1.43 |
| Local slope at b=5→6 | −1.37 | ≈−1.43 |
| R² of power-law fit | 0.999 | 0.998 |
| Steepening with b? | Yes | Yes |
| L-dependent? | Yes (strongly) | **No** (Lane L++) |

## The discrepancy

The slope difference Δ = 0.15 is small but real. Three factors contribute:

1. **Gaussian beam profile**: The eikonal assumes a plane wave (zero transverse localization). The actual propagator has a Gaussian angular weight exp(−β·θ²) which localizes the beam transversely. A tighter beam averages less over the potential landscape, producing a steeper effective slope. The β sweep confirmed this: slope varies from −0.79 (β=0.1, wide beam) to −1.93 (β=20, narrow beam). At β=0.8, the lattice gives −1.43, which is steeper than the eikonal's −1.28 — exactly the right direction.

2. **Wave-mechanical corrections**: The eikonal is a classical-path approximation. Quantum corrections (diffraction around the potential) modify the slope. These corrections are of order λ/b where λ is the de Broglie wavelength.

3. **L-independence**: The eikonal prediction IS L-dependent (it's the same finite-path formula falsified by Lane L++). But the lattice measurement is L-independent at fine H. This is the deepest discrepancy — the eikonal predicts something the lattice doesn't do.

## Interpretation

The eikonal prediction captures the **right functional form** (power law, steepening toward ≈ −1.4 at large b, finite-path transition regime) but **fails on the L-dependence**. This means:

- The b-dependence is largely geometric (finite-path integral geometry)
- The L-independence is a **wave-mechanical effect** beyond the eikonal — likely related to the Gaussian beam's effective transverse coherence length being the relevant scale, not the path length L
- The Gaussian angular weight β=0.8 provides the specific correction that shifts −1.28 → −1.43

## Beam-averaging corrections (BOTH TESTED AND FALSIFIED)

The queued follow-up was to compute beam-corrected eikonals. Both 2D and 3D beam corrections were tested and both **WORSEN** the match:

| Model | Slope | Δ from −1.43 | Status |
| --- | ---: | ---: | --- |
| Plane-wave (single ray) | −1.28 | 0.15 | **BEST** |
| 2D beam average (β=0.8) | −0.35 | 1.08 | Falsified |
| 3D beam average (β=0.8, 1/L²) | −0.77 | 0.66 | Falsified |
| Canonical 1/b | −1.00 | 0.43 | Wrong |
| Lattice measurement | −1.43 | 0.00 | Target |

Scripts: [`gaussian_beam_eikonal.py`](../scripts/gaussian_beam_eikonal.py), [`eikonal_3d_corrected.py`](../scripts/eikonal_3d_corrected.py)

**Why beam averaging fails:** At β=0.8, the beam width at the source position is σ_z ≈ 3.5–4.0, comparable to the impact parameters b ∈ {3..6}. Averaging over this wide beam smears out the 1/b structure, flattening the slope. The 3D correction (1/L² kernel factor) tightens the beam slightly (σ_z: 3.95 → 3.54) but not enough.

## What this establishes

- The plane-wave eikonal is the **best available theoretical prediction** (Δ=0.15)
- Beam corrections make things worse, not better — the effective deflection is closer to single-ray optics than to wave optics for this observable
- ~~The whole picture is coherent~~ — **the picture is INCOMPLETE**: the Δ=0.15 gap between eikonal (−1.28) and lattice (−1.43) is unexplained by any correction tested
- The L-independence remains unexplained
- The original "non-relativistic" framing is uncertain: the DAG's dispersion doesn't clearly distinguish Schrödinger from Klein-Gordon

## Bottom line

> "The plane-wave eikonal for a 2D 1/r potential at L=15, x_src=5
> gives slope −1.28 on b ∈ {3..6} (Δ=0.15 from lattice −1.43).
> This is the closest theoretical prediction achieved. Beam-averaging
> corrections (2D and 3D) both worsen the match to Δ=1.08 and
> Δ=0.66 respectively. The remaining Δ=0.15 and the L-independence
> are unexplained. The original framing as 'non-relativistic eikonal'
> was based on a 2D dispersion result that does not transfer to the
> 3D grown DAG."
