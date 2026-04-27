# Kubo-Eikonal Gap Analysis

**Date:** 2026-04-09 (revised same day after review)
**Status:** proposed_retained DIAGNOSTIC (bounded) — comparing the plane-wave eikonal prediction (slope −1.275) against existing Fam1/seed0 Kubo slopes at three H values shows a gap that is small at coarse H and larger at H=0.25. However, all three Kubo points are Fam1-only on the LENSING_DEFLECTION_NOTE's single-seed configuration, and the cross-family note reports per-seed slope σ ≈ 0.16–0.23 at H=0.5. The coarse-H "agreement" (±0.006) is well below this noise floor, so the note cannot claim the eikonal is "exact" at coarse H — only that the three available points are suggestive of a widening gap under refinement.

## Data (from existing Fam1 measurements, b ∈ {3..6})

Source: [`LENSING_DEFLECTION_NOTE.md`](LENSING_DEFLECTION_NOTE.md), which reports slopes from the `lensing_deflection_sweep.py` harness on Fam1 seed 0.

| H | Kubo slope | Eikonal slope | Gap | R² (Kubo) | Notes |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0.50 | −1.281 | −1.275 | 0.006 | 0.971 | Within per-seed noise (σ≈0.16–0.23) |
| 0.35 | −1.269 | −1.275 | −0.006 | 0.937 | Within per-seed noise |
| 0.25 | −1.433 | −1.275 | **0.158** | 0.998 | Fam1-only, untested on Fam2/Fam3 |

Eikonal: I_geom(b) = (1/b)·[(L-x_src)/√((L-x_src)²+b²) + x_src/√(x_src²+b²)] at L=15, x_src=5.

## Observations

The three Fam1 data points show:
- At H=0.5 and H=0.35: the Kubo slope and eikonal agree to ±0.006
- At H=0.25: the gap opens to 0.158

**Caveats that limit interpretation:**

1. **Per-seed noise dominates at coarse H.** The cross-family note reports per-seed slope σ ≈ 0.16–0.23 at H=0.5. A gap of ±0.006 is 30× below this noise floor. The coarse-H "agreement" may be coincidental rather than physical.

2. **Single seed, single family.** All three slopes come from Fam1 seed 0. The H=0.25 point is untested on Fam2/Fam3. The gap could be seed-specific.

3. **The gap at H=0.25 (0.158) is within the per-seed σ.** Even the largest gap is comparable to the single-seed noise. Multi-seed, multi-family confirmation is needed.

The supported claim is:

> "On the three available Fam1/seed0 data points, the Kubo-eikonal gap
> appears to widen at H=0.25, but the coarse-H agreement is below the
> known per-seed noise floor and cannot be called exact."

NOT:

> ~~"The eikonal is exact at coarse H and fails at fine H via a regime transition."~~

## If the gap IS real

If multi-seed confirmation shows the gap genuinely widens at fine H, possible mechanisms include:

1. **Phase resolution**: At H=0.25 there are ~150 rad of total phase vs ~75 at H=0.5. Finer phase structure may resolve diffraction effects phase-aliased at coarse H.

2. **Transverse mode resolution**: 2401 nodes/layer at H=0.25 vs 625 at H=0.5 resolves more transverse modes.

3. **R² improvement**: R² jumps from 0.937 (H=0.35) to 0.998 (H=0.25), suggesting the H=0.25 power-law fit is genuinely cleaner, not just a noise artifact.

## Artifact chain

- This note synthesizes data from [`LENSING_DEFLECTION_NOTE.md`](LENSING_DEFLECTION_NOTE.md) (source of the three Kubo slopes) and [`BORN_SCATTERING_COMPARISON_NOTE.md`](BORN_SCATTERING_COMPARISON_NOTE.md) (eikonal formula)
- The script `kubo_eikonal_gap.py` was an attempt to reproduce on a 2D regular lattice with different geometry (L=40, W=20, K=5 fixed) and does NOT reproduce the grown-DAG numbers — it is not part of this note's evidence

## Bottom line

> "Comparing three existing Fam1/seed0 Kubo slopes against the
> plane-wave eikonal (−1.275), the gap is ±0.006 at H=0.5 and H=0.35
> (below per-seed noise σ≈0.2) and 0.158 at H=0.25. Suggestive of a
> widening gap under refinement, but the coarse-H agreement is below
> the noise floor and the fine-H point is single-seed/single-family.
> Multi-seed confirmation needed before interpreting as a regime
> transition."
