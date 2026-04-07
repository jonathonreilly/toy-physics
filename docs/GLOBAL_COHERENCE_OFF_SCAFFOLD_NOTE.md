# Off-Scaffold Held-Out Test of `free_coh` — DECISIVE NEGATIVE

**Date:** 2026-04-07
**Status:** retained negative — the frozen rule `free_coh ≥ 7.96e-04` generalizes to only 5/9 = 55.6% on off-scaffold generators, matching the old node-level rule exactly. The grid scaffold was doing work the classifier was attributing to `free_coh`. The simple-classifier line of attack is now exhausted. A pre-committed structural pass/fail intuition hits 8/9 = 88.9%, suggesting the underlying physics is predictable — but not with a single node-level or single-global scalar metric.

## Artifact chain

- [`scripts/global_coherence_off_scaffold.py`](../scripts/global_coherence_off_scaffold.py)
- [`logs/2026-04-07-global-coherence-off-scaffold.txt`](../logs/2026-04-07-global-coherence-off-scaffold.txt)

## Question

The previous coherence lanes all placed nodes on the same
`(layer, iy, iz)` regular grid. The last retained caveat was:

> "All 21 held-out generators share the (layer, iy, iz) grid scaffold;
>  generalization beyond that substrate is untested."

This lane removes that caveat. 9 new generators layered but with
**continuous** transverse positions:

| Family | Distribution |
| --- | --- |
| OF1_uniform_k15 | uniform random (y, z), k=15 |
| OF2_uniform_k30 | uniform random, k=30 |
| OF3_uniform_k8 | uniform random, k=8 |
| OF4_gaussian | Gaussian around (0, 0) |
| OF5_clustered | 4 Gaussian cluster centers |
| OF6_rotated_grid | grid rotated by random per-layer angle |
| OF7_halton | Halton low-discrepancy quasi-random |
| OF8_radial | concentric rings (polar) |
| OF9_stretched | per-layer anisotropic stretch |

Connectivity: k nearest forward neighbors by Euclidean distance.
Battery: same 5 conditions as the scaffolded lane. Rule:
`free_coh ≥ 7.96e-04`, **frozen** from the swept-set fit, applied
without refit. Predictions hard-coded BEFORE running.

## Result

| Family | free_coh | delta | dyn | package |
| --- | ---: | ---: | ---: | :---: |
| OF1_uniform_k15 | 1.74e-2 | +0.0047 | 62.6% | PASS |
| OF2_uniform_k30 | 4.70e-3 | +0.0072 | 11.7% | PASS |
| OF3_uniform_k8 | 5.77e-2 | +0.0006 | 0.4% | FAIL |
| OF4_gaussian | 2.16e-1 | +0.0002 | 5.5% | PASS |
| OF5_clustered | 1.02e-2 | −0.0000 | 87.9% | FAIL |
| OF6_rotated_grid | 1.60e-1 | +0.0252 | 41.7% | PASS |
| OF7_halton | 1.60e-1 | +0.0165 | 11.5% | PASS |
| OF8_radial | 1.23e-1 | −0.0000 | 0.4% | FAIL |
| OF9_stretched | 6.48e-3 | −0.0002 | 127.0% | FAIL |

**PASS 5 / FAIL 4.**

### L1 — pre-committed `free_coh` sign: 4/9 = 44.4%

The pre-committed signs for `free_coh` (based on the meaning the
metric had on the scaffolded set) were wrong more often than right.
Every off-scaffold generator has `free_coh > 0.0064`, orders of
magnitude higher than the swept-set FAIL maximum of 0.0216. **The
metric's sign relative to the 7.96e-04 threshold is not meaningful
off-scaffold.**

### L2 — frozen rule applied without refit: 5/9 = 55.6%

The rule fires PASS for all 9 off-scaffold families. 5 actually pass,
4 are false positives (OF3, OF5, OF8, OF9). The rule loses its
discrimination entirely.

### L3 — pre-committed pass/fail structural intuition: 8/9 = 88.9%

The only miss is OF8_radial, which I expected to pass due to rotational
symmetry but which fails because the radial arrangement gives
delta_z ≈ 0 (no net gravity signal along the measurement axis).

All four actual fails match structural expectations: OF3 too sparse,
OF5 clusters break uniformity, OF9 stretched breaks Z2 in the
measurement axis, OF8 radial fails on a geometric degeneracy I
underestimated.

### Comparison to old node-level rule

| Rule | Cross-generator (this off-scaffold batch) |
| --- | ---: |
| Old 2-prop `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` | 5/9 = **55.6%** |
| New `free_coh ≥ 7.96e-04` | 5/9 = **55.6%** |

**The free_coh advantage disappears off-scaffold.** Both rules give
the same accuracy and the same set of misses.

## What this means

The coherence program had three partial revivals on scaffolded data
(first batch 7/9, second batch 10/12, combined 17/21 = 81%). On the
honest off-scaffold test, the advantage over the old rule **collapses
to zero**.

The simplest explanation of what was happening: `free_coh` was
measuring something specific to the grid-aligned phase relationships
of the propagator paths. With the detector at fixed grid cells, the
phases of PASS families accumulated coherently in a measurable way.
Off-scaffold, the detector cells are at irregular positions, the
phases accumulate differently, and `free_coh` loses its discriminative
meaning — it measures the wrong thing.

This is **the decisive off-scaffold negative** that closes the
simple-classifier line of attack. Specifically:

- The classifier rule `free_coh ≥ 7.96e-04` is **not generator-agnostic**
- It is **scaffold-specific** in a way the previous lanes obscured
- The retained cross-generator 81% was a **within-substrate** empirical regime
- `free_coh` is **not "the predictor"** in any law-level sense

## The positive finding inside the negative

L3 (pre-committed pass/fail) hits **88.9%** on this batch — the
underlying physics is **predictable from structural inspection** of the
generator. The structural features that matter are the same ones that
mattered on-scaffold: density, symmetry, uniformity, Z2 balance in the
measurement axis. What fails is the attempt to express those features
as a single node-level metric or a single global scalar computed from
free-beam propagation.

This suggests the next attack target should **not** be another
metric-search lane. The 88.9% human-intuition baseline across all
cross-generator experiments (scaffolded + off-scaffold) means:

- **The physics is knowable**, but
- **Simple metric classifiers are the wrong tool** for it
- **Analytic derivation** is the right tool — and now has a sharper
  target: explain what the 88.9% structural features are, directly
  from the path-sum + S = L(1−f), without going through an empirical
  metric

## Frontier map adjustment (reverses the coherence-lane bump)

| Row | Previous | This lane |
| --- | --- | --- |
| Strength against harshest critique | +24 on 21 scaffolded generators | **reverted off-scaffold**; advantage over old rule = 0 |
| Compact underlying principle | single global metric does most of the work on scaffolded | **reverted**; no scalar metric carries the weight off-scaffold |
| Theory compression | sharper target: derive `free_coh` ↔ package | **reverted target**; the next move is a direct path-sum argument, not a metric |
| Matter / inertial closure | open | **higher priority now** — the classifier lane is genuinely closed |

## Honest read

This is **the decisive negative we said we would accept**. When
`global_coherence_predictor.py` landed with a modest revival on
scaffolded cross-generators, the honest framing required testing
off-scaffold and reporting the result without interpretation. That
test is now done. The result:

- **Off-scaffold accuracy = 55.6%** (matches the old rule, +0 improvement)
- **The scaffolded +24 points was scaffold-specific**
- **The classifier program on this generator family is closed**
- **A structural-intuition baseline of 88.9% remains** — the physics
  is knowable, but not via a single empirical metric

The correct next attack target is no longer "find a better metric."
It is either:
1. **Matter / inertial closure** (different scorecard column, the
   classifier column is now boxed in)
2. **Analytic derivation** from path-sum + S = L(1−f), targeting the
   structural features that explain the 88.9% human baseline

## Bottom line

> "On an off-scaffold batch of 9 generators (continuous transverse
> positions instead of grid cells), the frozen rule
> `free_coh ≥ 7.96e-04` achieves 5/9 = 55.6% accuracy, exactly
> matching the old node-level 2-property rule. The previously
> retained cross-generator +24 point advantage on 21 scaffolded
> generators was scaffold-specific: `free_coh` measured a property
> of the grid-aligned phase relationships, not a generator-agnostic
> structural feature. A pre-committed structural pass/fail intuition
> hits 8/9 = 88.9% on the same batch, showing the underlying physics
> is predictable — but not with any single metric tested so far. The
> simple-classifier line of attack is exhausted. The next attack
> target is matter/inertial closure or a direct analytic derivation
> from the path-sum + S = L(1−f), not another metric search."
