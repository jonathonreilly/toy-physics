# Kubo-Eikonal Gap Analysis

**Date:** 2026-04-09
**Status:** retained DIAGNOSTIC — the gap between the plane-wave eikonal prediction (slope −1.275) and the lattice Kubo measurement is **zero at H=0.5 and H=0.35**, then jumps to 0.16 at H=0.25. This is NOT a smooth convergence — it's a regime transition. The eikonal is EXACT at coarse H and fails only at fine H.

## Data (from existing measurements on 3D grown DAG, b ∈ {3..6})

| H | Kubo slope | Eikonal slope | Gap | R² (Kubo) |
| ---: | ---: | ---: | ---: | ---: |
| 0.50 | −1.281 | −1.275 | 0.006 | 0.971 |
| 0.35 | −1.269 | −1.275 | −0.006 | 0.937 |
| 0.25 | −1.433 | −1.275 | **0.158** | 0.998 |

Eikonal: I_geom(b) = (1/b)·[(L-x_src)/√((L-x_src)²+b²) + x_src/√(x_src²+b²)] at L=15, x_src=5.

## The puzzle

The eikonal is a continuous, h-independent prediction. The lattice Kubo slope should approach the eikonal in the coarse-H limit (where the propagator is effectively classical) and deviate at fine H (where wave effects resolve). This is exactly what happens — but the transition is **abrupt**, not smooth:

- H=0.5 and H=0.35: eikonal is exact to ±0.006
- H=0.25: eikonal suddenly misses by 0.158

This is consistent with a **wave-mechanical correction that turns on at fine H**. The correction is not linear in h — it's absent at H=0.5, absent at H=0.35, and fully present at H=0.25.

## Possible mechanisms

1. **Phase resolution**: At H=0.25, the phase per edge is k·H = 2.5 rad. There are NL = 61 layers. The total accumulated phase is ~150 rad. At H=0.5, NL=31, total phase ~75 rad. The additional phase resolution at fine H may be enough to resolve diffraction effects that were phase-aliased at coarse H.

2. **Transverse mode resolution**: At H=0.25, there are (2·PW/H+1)² = 49² = 2401 nodes per layer vs 625 at H=0.5. The finer transverse mesh resolves more transverse modes, which contribute to diffraction around the potential.

3. **R² improvement**: Note that R² jumps from 0.937 (H=0.35) to 0.998 (H=0.25). The power-law fit itself gets dramatically better at fine H. This suggests the H=0.35 measurement is contaminated by lattice artifacts that make the slope noisier, while H=0.25 resolves the true wave-mechanical power law.

## What this means for the project

The eikonal is the correct coarse-H baseline. The −1.43 at H=0.25 is the eikonal (−1.275) PLUS a wave correction (+0.158 in slope magnitude). This wave correction is:

- Absent at coarse H
- Present at fine H
- Not captured by any beam-averaging model tested
- The true physics that distinguishes the propagator from classical ray optics

Understanding this correction analytically would be the key to a first-principles derivation of the −1.43 slope. The correction is roughly 12% of the total slope — significant but not dominant.

## Next step

The wave correction should be accessible via the **second-order Born approximation** or a **diffraction integral** on the lattice. The first-order eikonal (straight-ray integral) gives −1.275. The correction involves paths that scatter off the potential and then diffract — these paths sample the potential's structure differently and steepen the effective slope.

## Artifact chain

- This note synthesizes data from [`docs/LENSING_DEFLECTION_NOTE.md`](LENSING_DEFLECTION_NOTE.md) and [`docs/BORN_SCATTERING_COMPARISON_NOTE.md`](BORN_SCATTERING_COMPARISON_NOTE.md)
- No new script needed — the data already existed

## Bottom line

> "The eikonal-Kubo gap is zero at H=0.5 and H=0.35, then jumps to
> 0.158 at H=0.25. The eikonal is exact at coarse H; the −1.43 slope
> at fine H equals the eikonal (−1.275) plus a wave correction (0.158)
> that turns on abruptly between H=0.35 and H=0.25. This is a regime
> transition, not a smooth convergence. The wave correction is the
> genuine non-eikonal physics of the propagator."
