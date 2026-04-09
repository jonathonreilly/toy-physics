# Fine-H (H=0.25) Lensing: Family Universality Confirmed

**Date:** 2026-04-09
**Status:** retained POSITIVE — all three DAG families produce the same lensing slope at H=0.25 within per-seed noise. Grand mean slope: **−1.404 ± 0.031** (15 seeds, all R² > 0.997). The inter-family spread (0.044) is 1.4× the per-seed σ (0.031) — consistent within noise. The eikonal gap (0.11–0.15) is also consistent across families.

This closes the P1 gap from the earlier cross-family review: **fine-H universality is now tested, not extrapolated.**

## Data

### Per-seed slopes at H=0.25, b ∈ {3, 4, 5, 6}

| Family | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | Mean | σ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fam1 | −1.424 | −1.399 | −1.358 | −1.459 | −1.356 | **−1.399** | 0.039 |
| Fam2 | −1.428 | −1.435 | −1.404 | −1.474 | −1.406 | **−1.429** | 0.025 |
| Fam3 | −1.397 | −1.387 | −1.353 | −1.429 | −1.358 | **−1.385** | 0.028 |

All 15 per-seed fits have R² > 0.997.

### Seed-mean fits

| Family | Slope | Prefactor | R² |
| --- | ---: | ---: | ---: |
| Fam1 | −1.397 | 27.7 | 0.9982 |
| Fam2 | −1.427 | 32.5 | 0.9982 |
| Fam3 | −1.383 | 27.2 | 0.9978 |

### Cross-family statistics

| Quantity | Value |
| --- | ---: |
| Grand mean slope | −1.404 |
| Grand σ (all 15 seeds) | 0.031 |
| Inter-family spread | 0.044 |
| Spread / per-seed σ | 1.4× |
| Eikonal baseline | −1.275 |
| Mean eikonal gap | −0.129 |

## Interpretation

1. **The −1.4 slope is universal across families at H=0.25.** This was the key untested claim from the cross-family note. It is now confirmed: the slope does not depend on the DAG's drift/restore parameters.

2. **The grand mean (−1.404) is slightly shallower than the original Fam1/seed0 measurement (−1.433).** The 5-seed Fam1 mean is −1.399, consistent with the original single-seed point falling within the per-seed distribution.

3. **The eikonal gap (0.11–0.15) is consistent across families.** Fam1 gap = 0.124, Fam2 gap = 0.154, Fam3 gap = 0.109. The gap is real (well above per-seed noise of ~0.03) and universal.

4. **The inter-family spread (0.044) is marginal.** At 1.4× the per-seed σ, there may be a small family effect (Fam2 slightly steeper than Fam3), but it's not statistically significant with only 5 seeds per family.

## Comparison with H=0.5 results

| Quantity | H=0.5 | H=0.25 |
| --- | ---: | ---: |
| Grand mean slope | −1.30 | **−1.40** |
| Per-seed σ | 0.16–0.23 | **0.025–0.039** |
| R² (per-seed) | 0.94–0.95 | **>0.997** |
| Eikonal gap | ~0 | **0.13** |

The H=0.25 measurement is **dramatically cleaner** than H=0.5: per-seed σ drops 5–8×, R² jumps from ~0.94 to >0.997, and the power-law form sharpens into a high-precision invariant. The eikonal gap, which was within noise at H=0.5, is now clearly resolved.

## Updated combined invariant

With 15 seeds across 3 families at H=0.25:

> **kubo_true(b) ≈ 29 · b^(−1.40)** on b ∈ {3, 4, 5, 6}
>
> Grand mean slope: −1.404 ± 0.031 (15 seeds, 3 families)
> All per-seed R² > 0.997
> Eikonal gap: −0.129 ± 0.019

The original single-seed estimate of −1.433 was within 1σ of this multi-seed/multi-family grand mean.

## Artifact chain

- [`scripts/lensing_fine_h_batch.py`](../scripts/lensing_fine_h_batch.py) — single (family, seed) runner
- [`scripts/lensing_fine_h_single.py`](../scripts/lensing_fine_h_single.py) — single (family, seed, b) runner
- [`logs/2026-04-09-lensing-fine-h-families.txt`](../logs/2026-04-09-lensing-fine-h-families.txt) — raw output

## Bottom line

> "All three DAG families produce the same lensing slope at H=0.25:
> grand mean −1.404 ± 0.031 across 15 seeds with all R² > 0.997.
> Inter-family spread (0.044) is 1.4× per-seed σ — consistent within
> noise. The eikonal gap (0.13 ± 0.02) is also universal. Fine-H
> universality is now confirmed, not extrapolated."
