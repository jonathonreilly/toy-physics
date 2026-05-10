# Global Free-Beam Coherence Predictor — Modest Revival

> **2026-04-07 update:** the off-scaffold held-out lane
> ([`GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md`](GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md))
> reversed this lane's advantage. On 9 continuous-position generators,
> `free_coh ≥ 7.96e-04` gives 5/9 = 55.6%, exactly matching the old
> rule. The revival was scaffold-specific. The classifier lane is now
> closed; this note is kept for the record.

**Date:** 2026-04-07
**Last sync:** 2026-05-10 — runner declared `AUDIT_TIMEOUT_SEC = 900` so the
live replay completes inside the audit window, and the runner now asserts
the archived 7/9 vs 6/9 scaffolded numbers from
`logs/2026-04-07-global-coherence-predictor.txt` against the live rerun.
No headline numbers change.
**Status:** bounded - historical scaffold-specific evidence. The 2026-04-07 off-scaffold lane reversed the advantage to 5/9 = 55.6%, exactly matching the prior rule, so the original 7/9 = 77.8% revival was scaffold-specific. The classifier program is closed; this note is kept as historical finite evidence only.

## Artifact chain

- [`scripts/global_coherence_predictor.py`](../scripts/global_coherence_predictor.py)
- [`logs/2026-04-07-global-coherence-predictor.txt`](../logs/2026-04-07-global-coherence-predictor.txt)

## Question

Two prior negatives closed the simple node-level classifier line:

1. The 2-property rule `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` did
   not generalize to 9 genuinely different generators (6/9 = 66.7%)
2. The most natural 3rd predictor `local_z_asym` was rejected by a
   3-property classifier search (cross-gen unchanged at 6/9)

The hypothesis from the previous review was that the missing predictor
must be **global**, not node-level — likely a path-counting or spectral
property. Random k-regular and expander generators fail at the same
nominal `avg_deg` because **paths spread thin and path phases randomize**.
Grown-DAG and dense ER pass because paths interfere coherently at the
detector.

This lane tests that hypothesis with two genuinely global metrics
computed from the **free-beam propagation** (no source field):

- `free_p_det` = `Σ |amp|²` over detector cells (total free-beam intensity reaching detector)
- `free_coh`   = `|Σ amp|² / (Σ |amp|² · N_det)` (Kuramoto-style amplitude coherence on detector cells; 1.0 = phase-aligned, ~1/N_det = random)

Both depend on the **full graph + propagator system**, not on per-node
degree statistics.

## Distribution

| Group | `free_p_det` range | `free_coh` range |
| --- | --- | --- |
| swept PASS | [3.97e-30, 1.45e+21] | [0.0008, 0.7959] |
| swept FAIL | [0, 9.75e+11] | [0.0000, 0.0216] |
| indep PASS | [8.89e-35, 1.29e-14] | [0.0000, 0.0010] |
| indep FAIL | [0, 1.30e-27] | [0.0000, 0.0012] |

The `free_coh` metric **separates the swept set cleanly**: PASS minimum
0.0008 vs FAIL maximum 0.0216 — slight overlap but a much sharper
gap than the node-level metrics gave. The independent set is harder:
PASS and FAIL ranges overlap heavily because random connectivity
never builds up the same kind of phase-coherent buildup that the
spatial neighbor stencil does.

## Result

### Single-property classifiers on the swept set (with new metrics)

| Rule | In-sample | Cross-generator (no refit) |
| --- | ---: | ---: |
| `reach_frac ≥ 0.8587` | 92.3% | 5/9 = 55.6% |
| `free_p_det ≥ 3.97e-30` | 88.5% | **7/9 = 77.8%** |
| `free_coh ≥ 7.96e-04` | 92.3% | **7/9 = 77.8%** |

Two single-property rules using the new global metrics give 7/9 on
cross-generator. The best in-sample 1-prop rule (`reach_frac`) gives
5/9 cross-generator.

### 2-property AND search (new metrics in pool)

The 2-property AND search picks `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)`,
the same rule as before, with in-sample 92.3% and cross-generator 6/9.

> The 2-property search **fails to find the better cross-generator
> rule** because in-sample accuracy ties between the node-level and
> global rules, and the search breaks ties on enumeration order, not
> on cross-generator performance. This is a known overfitting failure
> of in-sample-optimal classifier search: ties resolve toward the
> overfitted rule.

### Cross-generator comparison

| Rule | Cross-generator |
| --- | ---: |
| `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` (old, 2-prop) | 6/9 = 66.7% |
| `free_coh ≥ 7.96e-04` (new, single global metric) | **7/9 = 77.8%** |
| `free_p_det ≥ 3.97e-30` (new, single global metric) | **7/9 = 77.8%** |

The single-property `free_coh` rule is **+1 family better** on
cross-generator than the old 2-property rule, while matching its
in-sample accuracy.

## Where the improvement comes from

The old rule's 3 misses (R1, R3, X1) are all **false positives** —
random/expander graphs at high enough `avg_deg` that the rule admits
them, but the actual battery rejects them. The new `free_coh` rule
fixes all three: their `free_coh` is exactly 0.0000 because path phases
are randomized and the detector receives an uncorrelated amplitude
distribution.

The new rule introduces:
- 1 **false negative**: E1_er_p005 has `free_coh = 0.0000` (passing
  the package via dense Gaussian buildup, not phase coherence) but is
  excluded by the threshold
- 1 **false positive**: L1_longrange_k12 has `free_coh = 0.0012` (just
  above threshold) but actually fails the package

Net: 3 misses → 2 misses. **+1 family.**

## Honest read

This is a **modest revival**, not a closure. Specifically:

What the new metric gives:
- Cross-generator improves by **+11 points** (67% → 78%) with a single global predictor
- The hypothesis "path coherence at the detector matters" is **partially supported**
- The classifier program is **alive again** with a sharper, generator-agnostic predictor candidate
- It exhibits a known failure mode of in-sample-optimal classifier search (tie-breaking misses generalization gains)

What it does NOT give:
- The cross-generator gap is **not closed** — 78% is still much weaker than the in-family 87.5%
- The new rule has its own miss patterns (E1 false negative, L1 false positive)
- The metric is still **empirical**, not derived from the path-sum + S=L(1−f)
- 78% on 9 families is not a universality theorem
- E1 is a specific counterexample showing coherence is **not necessary** for the package — E1 passes the battery despite `free_coh = 0.0000` (it passes via dense Gaussian buildup from the law of large numbers, not via phase coherence)

## What this tells us positively

The improvement is small but its structural meaning is clean:

> **Most cross-generator failures are exactly the cases where the
> free beam's path phases randomize at the detector.** Random k-regular,
> expander, and tree-like generators all have `free_coh ≈ 0` because
> paths spread without correlation. Grown-DAG with the neighbor
> square stencil has high `free_coh` because the spatial structure
> aligns paths. Dense ER (E2) at high p has moderate `free_coh`
> because the law of large numbers partially recovers phase alignment.

This identifies **path-phase coherence** as a **strong empirical
predictor** of the package: on the swept set the single threshold
`free_coh ≥ 7.96e-04` achieves 92.3% in-sample accuracy, the same as
the best 2-property node-level rule. Sufficiency is **not established**
— the swept set has a 7.7% residual, so there are swept-set cases
where coherence is above threshold but the package fails, or the
reverse. And E1 is a specific counterexample showing coherence is
not even necessary in general (E1 passes the battery via dense
uniform sampling without phase coherence).

## Frontier map adjustment (from Update 2)

| Row | Previous (Update 2, post-negative) | This update |
| --- | --- | --- |
| Strength against harshest critique | reverted | **modest restoration** (+11 points cross-generator) |
| Compact underlying principle | reverted | **modest restoration** (a single global metric does most of the work) |
| Theory compression | sharper target: global path/spectral | **partially answered**: free-beam coherence is one such metric |

The previous reversal (Update 2) said the simple-classifier line was
exhausted. This update **partially walks that back** — not to the
original "modest bump" claim, but to "global free-beam coherence is
a real predictor that improves cross-generator generalization by
+11 points."

## What to attack next

The honest next moves, in priority order:

1. **A larger cross-generator set with `free_coh` predictions
   pre-committed** — to confirm or refute the +11 points on a separate batch
2. **Analytic derivation** of why high `free_coh` implies the package
   (path-sum + S=L(1−f) → constructive interference → monotone gravity).
   The metric gives the theorem a sharper target than before.
3. **Matter / inertial closure** is still a higher-leverage move on
   a different scorecard column

## Bottom line

> "Adding a single global free-beam coherence metric `free_coh ≥ 7.96e-04`
> improves cross-generator accuracy from 6/9 = 66.7% to 7/9 = 77.8%
> while matching the in-sample accuracy (92.3%) of the node-level
> rule. The 2-property AND search misses this because in-sample ties
> resolve toward the overfitted rule, not the better generalizer.
> The classifier program is alive but still empirical; path-phase
> coherence is necessary but not sufficient (E1 passes without it
> via dense uniform sampling)."
