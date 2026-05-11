# Fine-H (H=0.25) Lensing: Three-Family Portability

**Date:** 2026-04-09 (revised same day after review)
**Status:** proposed_retained POSITIVE (bounded) — all three DAG families produce lensing slopes in the −1.38 to −1.43 band at H=0.25, closing the earlier Fam1-only gap. However, a proper family-mean significance test shows Fam2 vs Fam3 at t=2.37 (~p≈0.05), so a small residual family offset cannot be ruled out. The claim is **three-family portability**, not universality or kernel-independence.
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-04-26):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = medium`, `chain_closes = false`, and `claim_type
= bounded_theorem`. The audit chain-closure explanation is exact:
"The source note gives a detailed finite-sweep table, but the cited
raw log is missing from the worktree and the only listed runner is a
slow per-family/seed batch tool rather than an aggregate replay of
the 15-seed statistics. A live audit run did not complete even the
first family/seed within the audit window, so the current packet
does not provide reproducible runner output for the table or the
t-tests." This rigorization edit only sharpens the boundary of the
conditional perimeter; nothing here promotes audit status. The
supported content of this note is exactly the structural framing —
the per-seed slope table, the cross-family statistics, and the
significance-test framework — read against the registered runner
[`scripts/lensing_fine_h_batch.py`](../scripts/lensing_fine_h_batch.py)
(per-family/seed batch tool, slow under the audit-lane window). The
log file referenced in §"Artifact chain"
([`logs/2026-04-09-lensing-fine-h-families.txt`](../logs/2026-04-09-lensing-fine-h-families.txt))
is the historical raw-output archive; future runner-source rigorization
deferred to a follow-up that adds an aggregate 15-seed replay
runner with `AUDIT_TIMEOUT_SEC` set high enough for in-budget audit
completion (cache-refresh required, runner SHA would change).

## Data

### Per-seed slopes at H=0.25, b ∈ {3, 4, 5, 6}

| Family | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | Mean | Sample σ | SEM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fam1 | −1.424 | −1.399 | −1.358 | −1.459 | −1.356 | **−1.399** | 0.044 | 0.020 |
| Fam2 | −1.428 | −1.435 | −1.404 | −1.474 | −1.406 | **−1.429** | 0.028 | 0.013 |
| Fam3 | −1.397 | −1.387 | −1.353 | −1.429 | −1.358 | **−1.385** | 0.031 | 0.014 |

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
| Grand mean slope (15 seeds) | −1.404 |
| Grand population σ (15 seeds) | **0.036** |
| Grand sample σ (15 seeds) | 0.038 |
| Inter-family mean spread | 0.044 |

### Pairwise family-mean significance tests

| Comparison | Δ(mean) | SE(diff) | t | Significant? |
| --- | ---: | ---: | ---: | --- |
| Fam1 vs Fam2 | 0.030 | 0.023 | 1.28 | No |
| Fam1 vs Fam3 | 0.014 | 0.024 | 0.60 | No |
| **Fam2 vs Fam3** | **0.045** | **0.019** | **2.37** | **Borderline** (p≈0.05) |

Fam2 (slope −1.429) is marginally steeper than Fam3 (slope −1.385). With only 5 seeds per family, this is at the edge of statistical significance. A residual family effect cannot be ruled out.

## Interpretation

1. **The −1.4 slope is not Fam1-only.** All three families land in the −1.38 to −1.43 band. This closes the P1 gap from the earlier cross-family review.

2. **There may be a small Fam2/Fam3 offset.** The Fam2-Fam3 difference (0.045) reaches t=2.37 on a proper two-sample test. This is borderline significant and could indicate a real (small) family effect on the slope. More seeds would be needed to confirm or reject this.

3. **The eikonal gap is consistent across families.** Fam1 gap = 0.124, Fam2 gap = 0.154, Fam3 gap = 0.109. All are clearly above per-seed noise.

4. **Scope of the claim.** This artifact shows portability across three parameter settings of the same grown-DAG generator (drift/restore variations). It does NOT show geometry-independence or that the slope is a general "kernel property." The supported claim is:

> "The fine-H lensing slope is portable across three DAG families within
> the −1.38 to −1.43 band, with a possible residual Fam2/Fam3 offset
> (t=2.37) that needs more seeds to resolve."

NOT:

> ~~"The slope is a kernel property"~~ or ~~"universality confirmed"~~

## Comparison with H=0.5 results

| Quantity | H=0.5 | H=0.25 |
| --- | ---: | ---: |
| Grand mean slope | −1.30 | **−1.40** |
| Grand population σ (15 seeds) | ~0.19 | **0.036** |
| R² (per-seed) | 0.94–0.95 | **>0.997** |
| Eikonal gap | ~0 (below noise) | **0.13** |

The H=0.25 measurement is dramatically cleaner: σ drops 5×, R² jumps from ~0.94 to >0.997.

## Artifact chain

- [`scripts/lensing_fine_h_batch.py`](../scripts/lensing_fine_h_batch.py) — single (family, seed) runner
- [`logs/2026-04-09-lensing-fine-h-families.txt`](../logs/2026-04-09-lensing-fine-h-families.txt) — raw output

## Bottom line

> "All three DAG families produce lensing slopes in the −1.38 to −1.43
> band at H=0.25 (grand mean −1.404, population σ = 0.036, all R² > 0.997).
> This closes the earlier Fam1-only gap. However, a Fam2 vs Fam3 offset
> of 0.045 reaches t=2.37 (borderline significant), so a small residual
> family effect cannot be ruled out with 5 seeds per family. The eikonal
> gap (0.11–0.15) is consistent across families. The supported claim is
> three-family portability within this DAG generator class, not geometry-
> independence or kernel universality."
