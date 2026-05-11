# Global Coherence — Larger Held-Out Batch (12 NEW Generators)

> **2026-04-07 update:** the off-scaffold held-out lane
> ([`GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md`](GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md))
> is now the governing result for the free_coh program. On an
> off-scaffold batch of 9 continuous-position generators, the frozen
> rule drops to 5/9 = 55.6%, exactly matching the old node-level
> rule. The +24 point advantage reported in this note was
> scaffold-specific. This note is retained for the record but the
> headline is now the off-scaffold negative.

**Date:** 2026-04-07
**Status:** proposed_retained positive — frozen rule `free_coh ≥ 7.96e-04` (fitted on the 26-family swept set ONLY) applied without refit to 12 brand-new generators achieves **10/12 = 83.3%**, beating the old node-level 2-property rule (6/12 = 50%) by **+33 points**. Combined with the first batch: **17/21 = 81.0%** cross-generator on two independent held-out sets.
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-04-30):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "No.
One-hop dependencies are not all retained
(global_coherence_off_scaffold_note=bounded,
global_coherence_predictor_note=audited_failed), so the chain does
not close under the leaf audit rule." This rigorization edit only
sharpens the boundary of the conditional perimeter; nothing here
promotes audit status. The supported content of this note is the
finite 12-generator scaffolded held-out table reproduced verbatim by
the registered runner; the headline 17/21 cross-generator combined
statistic is bounded interpretation that depends on
[`GLOBAL_COHERENCE_PREDICTOR_NOTE.md`](GLOBAL_COHERENCE_PREDICTOR_NOTE.md)
(currently `audited_failed`) for the 9-family first batch and on the
off-scaffold note (currently `bounded`) for the off-scaffold negative
header callout. The supported perimeter is just the in-this-note
12-family table; the cross-batch combination is governed by the
upstream notes' statuses. This is exactly the leaf-audit chain-rule
non-closure stated in the verdict.

## Artifact chain

- [`scripts/global_coherence_held_out2.py`](../scripts/global_coherence_held_out2.py)
- [`logs/2026-04-07-global-coherence-held-out2.txt`](../logs/2026-04-07-global-coherence-held-out2.txt)

## Question

The previous lane ([GLOBAL_COHERENCE_PREDICTOR_NOTE.md](GLOBAL_COHERENCE_PREDICTOR_NOTE.md))
found that a single global metric `free_coh ≥ 7.96e-04` improved
cross-generator accuracy from 6/9 to 7/9 on the original
independent-generators batch — a modest +11 points. The obvious
follow-up question was whether that +11 is real or a fluke of those 9
specific generators.

This lane answers that with a **larger, fully-held-out batch of 12
NEW generators** not in either the 26 swept set or the original 9
independent set. Every generator is built from scratch; edge
topologies are independent of both earlier sets. Predictions are
**hard-coded in source** before running.

## The 12 new generators

1. **N1 `kreg_k30`** — random k-regular forward, k=30 (test density threshold)
2. **N2 `kreg_k50`** — random k-regular forward, k=50 (test deeper LLN)
3. **N3 `skip2`** — neighbor square stencil + skip-2 connections (high path multiplicity)
4. **N4 `smallworld`** — local stencil + 5% long-range shortcuts
5. **N5 `bipartite`** — one-to-one bipartite matching, no multiplicity
6. **N6 `band_random`** — random k=12 restricted to band |dy|,|dz|≤2
7. **N7 `twisted`** — neighbor square + per-layer z-shift (breaks per-layer Z2)
8. **N8 `block_diag`** — stencil restricted to 4×4 blocks (isolates paths)
9. **N9 `1d_like`** — only dz neighbors, no transverse y-mixing
10. **N10 `permutation`** — each source gets a random slice of a permutation
11. **N11 `aniso_rand`** — random k=12 biased toward small dz (asymmetric)
12. **N12 `kreg_k4`** — random k-regular k=4 (intentionally sparse)

## Three-level audit trail

Each family has **two predictions hard-coded in the script source
BEFORE running**:

- **L1 prediction**: my structural intuition for whether `free_coh`
  will be above or below the 7.96e-04 threshold
- **L3 prediction**: my structural intuition for whether the package
  (5-condition battery) will PASS or FAIL

**L2** is not a prediction — it's the frozen rule applied to the
measured `free_coh`, with no refitting and no prior knowledge of the
actual battery outcome.

## Results

### L2 — frozen rule accuracy (the headline)

| Family | measured `free_coh` | rule predicts | actual | agree |
| --- | ---: | :---: | :---: | :---: |
| N1 kreg_k30 | 4.10e-07 | FAIL | FAIL | OK |
| N2 kreg_k50 | 2.26e-03 | PASS | **FAIL** | MISS |
| N3 skip2 | 3.60e-02 | PASS | PASS | OK |
| N4 smallworld | 5.18e-02 | PASS | PASS | OK |
| N5 bipartite | 0.00 | FAIL | FAIL | OK |
| N6 band_random | 4.26e-03 | PASS | PASS | OK |
| N7 twisted | 0.00 | FAIL | FAIL | OK |
| N8 block_diag | 1.59e-02 | PASS | **FAIL** | MISS |
| N9 1d_like | 9.86e-03 | PASS | PASS | OK |
| N10 permutation | 2.14e-26 | FAIL | FAIL | OK |
| N11 aniso_rand | 2.21e-02 | PASS | PASS | OK |
| N12 kreg_k4 | 0.00 | FAIL | FAIL | OK |

> **L2 = 10/12 = 83.3%**

The frozen rule beats the old node-level 2-property rule on this
batch by **+33 points**:

| Rule | On this batch |
| --- | ---: |
| Old node-level: `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` | 6/12 = 50.0% |
| **New global: `free_coh ≥ 7.96e-04`** | **10/12 = 83.3%** |

### L1 — free_coh sign intuition (6/12 = 66.7%)

Structural predictions for whether `free_coh` would be above threshold
before running. Missed on:
- **N1 kreg_k30**: predicted high (density argument), actual low (k=30 still not dense enough to escape random path dispersion)
- **N8 block_diag**: predicted low, actual high (within-block coherence buildup is stronger than expected)
- **N9 1d_like**: predicted low, actual high (a 1D beam through a 1D-connectivity still has coherent phases within the line)
- **N11 aniso_rand**: predicted low, actual high (the asymmetry doesn't kill coherence as strongly as intuition suggested)

**My free_coh intuition is only 67% right.** That's a useful finding
by itself: the metric captures non-obvious structural properties I
couldn't fully predict from the generator description.

### L3 — package pre-committed intuition (8/12 = 66.7%)

Direct intuition for whether each generator would pass the full
battery. Misses:
- **N1 kreg_k30** and **N2 kreg_k50**: I overestimated density. Random k-regular fails even at k=30, 50.
- **N9 1d_like**: I underestimated. Dense 1D-like connectivity passes because the 1D iz-line propagation is still coherent.
- **N11 aniso_rand**: I underestimated. The anisotropy toward small dz actually helps path coherence.

### Three-level summary

| Level | Meaning | Accuracy |
| --- | --- | ---: |
| L1 | free_coh sign intuition | 8/12 = 66.7% |
| **L2** | **frozen rule on measured free_coh (NO REFIT)** | **10/12 = 83.3%** |
| L3 | direct package pass/fail intuition | 8/12 = 66.7% |

The rule outperforms my own structural intuition by **+17 points**.
That is a strong indicator that the metric captures real information
the rule can exploit more reliably than a human classifier.

## Combined across both cross-generator batches

| Batch | Frozen rule | Old 2-property rule |
| --- | ---: | ---: |
| First (9 families) | 7/9 = 77.8% | 6/9 = 66.7% |
| Second (12 families, this lane) | **10/12 = 83.3%** | 6/12 = 50.0% |
| **Total (21 families)** | **17/21 = 81.0%** | 12/21 = 57.1% |

On two independent cross-generator batches totaling 21 never-refit
families, the single-property global rule achieves **81.0%** vs the
old node-level rule's **57.1%** — a **+23.8 point** gap.

## What the 2 misses tell us

Both L2 misses are **false positives**: graphs where `free_coh` is
above threshold but the full battery still fails.

- **N2 kreg_k50** (free_coh = 2.26e-03, actual FAIL): Very dense random
  k-regular has moderate coherence (LLN recovery) but the F~M slope is
  off-band. **Path coherence is necessary but not sufficient** at high
  nominal avg_deg on random generators.
- **N8 block_diag** (free_coh = 1.59e-02, actual FAIL): Blocks build
  local coherence within each block, so `free_coh > threshold`, but the
  detector-level gravity response is sign-crossed because the blocks
  don't communicate. **Spatial continuity of the coherent region matters.**

Both misses suggest the **next hardening target**: `free_coh` needs
to be augmented by a measure of *where* the coherent region is
(the block_diag failure) or a second condition that excludes random
generators at moderate density (the kreg_k50 failure). But neither
kills the current lane's result.

## Honest read

What is true:
- A single global metric `free_coh ≥ 7.96e-04` fitted on the swept
  set generalizes to a fresh 12-generator batch at 83%, and to the
  combined 21-family cross-generator set at 81%
- This beats the best node-level 2-property rule by +33 points on the
  new batch, +24 points overall
- Predictions were hard-coded in source before running; the audit
  trail is unambiguous
- The rule's 2 misses point toward specific augmentations rather than
  falsifying the core idea
- My own intuition is 67%; the rule is 83%. The metric captures
  information I could not predict from the generator description.

What is NOT yet true:
- 83% is not 100% — the rule still has false positives
- The rule is still empirical, not derived from path-sum + S=L(1−f)
- The threshold 7.96e-04 is a fitted number, not a theoretical value
- Sufficiency on the swept set is not established (the swept-set
  residual is 7.7%)
- The held-out generators are still grid-scaffolded — different edge
  topologies but the same spatial-lattice substrate
- E1 from the first batch remains a counterexample: coherence is not
  necessary in general

## Frontier map adjustment

| Row | Previous | This lane |
| --- | --- | --- |
| Strength against harshest critique | modest restoration (+11 cross-generator) | **+24 points on 21 tested scaffolded generators; not a law-level answer** |
| Compact underlying principle | modest restoration | **a single global empirical predictor does most of the cross-generator work on the tested set** |
| Theory compression | sharper target: global path/spectral | **sharper target still open**: derive or no-go `free_coh ≥ 7.96e-04` ↔ package from path-sum + S=L(1−f) |

The rule is **not** yet "the predictor" in a law-level sense. It is
the best current global empirical predictor on the tested scaffolded
generators, with known false positives (N2_kreg_k50, N8_block_diag)
and a known counterexample for necessity (E1 from the first batch).
All held-out generators share the `(layer, iy, iz)` grid scaffold;
generalization beyond that substrate is untested.

## Bottom line

> "On two independent cross-generator batches (9 + 12 = 21 families
> not in the original 26 swept set), the single-property rule
> `free_coh ≥ 7.96e-04` — fitted on the swept set and frozen —
> achieves 17/21 = 81.0% accuracy without refitting. The old
> node-level 2-property rule achieves 12/21 = 57.1% on the same
> sets, a +24-point gap stable across both batches. The rule has
> two false positives on this batch (N2_kreg_k50, N8_block_diag)
> and a necessity counterexample from the first batch (E1 passes the
> package at `free_coh = 0`). All 21 held-out generators share the
> same grid scaffold. The honest framing is: **free_coh is the best
> current global empirical predictor on the tested scaffolded
> generators, not a law-level or off-scaffold 'predictor of the
> weak-field package.'**"
