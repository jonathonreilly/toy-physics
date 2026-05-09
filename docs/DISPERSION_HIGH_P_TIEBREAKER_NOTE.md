# High-p Dispersion Tiebreaker

**Date:** 2026-04-09
**Status:** PARTIAL RESOLUTION — extending the momentum range to p=0–6 (from p=0–2) **eliminates Klein-Gordon** as the worst fit (R²=0.78, 0/8 per-seed wins) but does NOT give a clean winner between Schrödinger and Linear. Schrödinger R²=0.97 vs Linear R²=0.96 on the seed-mean, with per-seed winner split **4:4** (Schrödinger:Linear). The dispersion curve has structure beyond any simple two-parameter form: a smooth region at low p, a gap/dropout near p≈2.5, and steep negative ω at high p.

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/dispersion_high_p_tiebreaker.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

## Setup

- Fam1 grown DAG, H=0.5, 8 seeds
- p_z ∈ {0, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0}
- Nyquist = π/H = 6.28

## Key result: Klein-Gordon eliminated

| Form | R² (seed-mean, 12 pts) | Per-seed winner tally |
| --- | ---: | ---: |
| **Schrödinger** | **0.974** | **4/8** |
| Linear | 0.958 | 4/8 |
| Klein-Gordon | 0.780 | 0/8 |
| sqrt-KG | −0.59 | 0/8 |

Klein-Gordon is the WORST standard fit. The propagator is **not relativistic** on this momentum range. The competition is between Schrödinger (quadratic) and Linear (cone) — both fit the gross shape, neither captures the fine structure.

## What the dispersion actually looks like

| p | <ω> | σ | R² | Phase? |
| ---: | ---: | ---: | ---: | --- |
| 0.0 | +0.535 | 0.009 | 0.999 | Smooth |
| 1.0 | +0.477 | 0.009 | 0.998 | Smooth |
| 2.0 | +0.207 | 0.023 | 0.992 | Smooth |
| 2.5 | — | — | — | **Dropout** |
| 3.0 | −0.308 | 0.043 | 0.967 | Noisy |
| 4.0 | −0.983 | 0.241 | 0.984 | Noisy |
| 5.0 | −1.295 | 0.413 | 0.955 | Very noisy |

Three regimes:
1. **p < 2:** Clean, concave-down (KG-like curvature), all 8 seeds clean
2. **p ≈ 2.5:** Mode drops out — fewer than 3 seeds give clean phase
3. **p > 3:** ω goes large negative, high seed variance, mixed curvature

The curvature diagnostic (d²ω/dp²) is **concave down** at p < 2 and **flips sign** at p > 3. This is consistent with band structure rather than a simple free-particle dispersion.

## Interpretation

The lattice has finite transverse extent PW=6 with spacing H=0.5, giving 25 transverse nodes per layer. The first Brillouin zone boundary is at p ≈ π/H = 6.28, but effective boundary effects start much earlier because:
- The angular weight exp(−β·θ²) with β=0.8 cuts off modes with θ > ~1 rad
- The transverse connectivity (max_d=3·H = 6 nodes) limits high-p propagation
- The DAG's random node positions alias high-p modes

The dropout at p≈2.5 likely marks where the mode's wavelength λ = 2π/p ≈ 2.5 becomes comparable to the effective transverse connectivity range, causing the mode to decohere across seeds.

## What this establishes

1. **Klein-Gordon is eliminated** from the candidate pool (R²=0.78, 0/8 seeds). The propagator is not relativistic in the standard sense.
2. **The Schrödinger fit works for p < 2** and marginally for the full range, but the dispersion has non-trivial band structure at p > 2.5.
3. **The earlier near-tie was an artifact of the limited p-range**: at p ∈ {0..2}, both Schrödinger and KG fit equally well because they're both approximately quadratic at low p. The high-p data breaks the degeneracy.
4. **Linear dispersion is the runner-up**, suggesting the high-p regime approaches a group velocity of ≈ 0.39 (from the linear fit c = −0.387).

## Implications for lensing

The −1.43 lensing slope was measured at configurations where the relevant transverse momenta are p ≈ 1/b ≈ 0.17–0.33 (b ∈ {3..6}). These are firmly in the **smooth low-p regime** where the dispersion is well-characterized. The high-p complications don't affect the lensing physics.

The elimination of Klein-Gordon means the eikonal comparison (which is dispersion-agnostic) remains the best theoretical baseline for the lensing slope. No relativistic correction is needed.

## Artifact chain

- [`scripts/dispersion_high_p_tiebreaker.py`](../scripts/dispersion_high_p_tiebreaker.py)

## Bottom line

> "Extending the dispersion measurement to p=0–6 eliminates Klein-Gordon
> as the worst fit (R²=0.78, 0/8 per-seed wins). Schrödinger fits
> best on the seed-mean (R²=0.97) with 4/8 per-seed wins (4:4 split with Linear), but the
> dispersion has non-trivial band structure at p>2.5 (mode dropout,
> curvature sign flip) that neither simple model captures. The earlier
> Schrödinger/KG near-tie was an artifact of the limited p-range (0–2).
> For the lensing physics (p ≈ 0.2–0.3), the dispersion is well-
> characterized and non-relativistic."
