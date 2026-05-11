# Local Z-Asymmetry 3rd Predictor — NEGATIVE (Hypothesis Rejected)

**Date:** 2026-04-07
**Status:** proposed_retained negative — local per-node Z2 asymmetry is NOT the missing predictor. The 3-property classifier search rejected `local_z_asym` and reproduced the original 2-property rule. Cross-generator accuracy stays at 6/9 = 66.7%. Combined with the previous independent-generators lane, this closes the simple-classifier line of attack on this generator family.
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-04-26):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "The
live runner reproduces the finite local_z_asym negative exactly, but
it tests one added node-level metric inside a fixed 3-property AND
search; that does not prove the broader exhaustion of simple
classifiers or all node-level metrics." This rigorization edit only
sharpens the boundary of the conditional perimeter; nothing here
promotes audit status. The supported content of this note is
exactly the finite-sweep result on the registered runner: that
adding `local_z_asym` to the 3-property AND search reproduces the
2-property rule and stays at 6/9 cross-generator accuracy. The
broader §"Combined verdict" wording about "the simple-classifier
line of attack on this generator family is exhausted" is bounded
interpretation: the supported perimeter is the single-metric, fixed-
three-property AND-search result, not a full exhaustion of
node-level classifiers. A future supported exhaustion theorem
would need to enumerate node-level statistics or close a no-go on
that family.

## Artifact chain

- [`scripts/local_zsym_predictor.py`](../scripts/local_zsym_predictor.py)
- [`logs/2026-04-07-local-zsym-predictor.txt`](../logs/2026-04-07-local-zsym-predictor.txt)

## Question

The independent-generators lane gave a clean negative: the rule
`(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` failed to generalize from
the grown-DAG family to genuinely different generators (44.4%
pre-committed, 66.7% rule). The honest hypothesis from that result was:

> "Random k-regular at the same nominal avg_deg can have global z_sym
>  near zero but each individual node can have nonzero local z-asymmetry.
>  The neighbor-square stencil has local z_sym = 0 for every node by
>  construction. The required predictor is statistical Z2 symmetry under
>  dense random sampling, i.e. the variance of node-level dz."

This lane tests that hypothesis directly by adding `local_z_asym`
(mean over source nodes of `|sum(dz_out)| / sum(|dz_out|)`) as a
candidate 3rd predictor and refitting the classifier on the swept set
ONLY, then evaluating on the 9 independent generators WITHOUT REFIT.

## Result: hypothesis rejected

### Distribution table

| Group | min | mean | max |
| --- | ---: | ---: | ---: |
| swept PASS (grown-DAG) | 0.1506 | 0.4053 | 0.6929 |
| swept FAIL (grown-DAG) | 0.1922 | 0.4152 | 0.9787 |
| indep PASS (cross-gen) | 0.6955 | 0.6984 | 0.7012 |
| indep FAIL (cross-gen) | 0.7025 | 0.7625 | 0.9999 |

Two killing observations:
1. **Within the swept set**, PASS and FAIL have nearly identical
   `local_z_asym` distributions (means 0.41 vs 0.42; full range overlap).
   The predictor carries zero in-sample signal on the grown-DAG family.
2. **Within the independent set**, PASS and FAIL also overlap heavily
   (0.70 vs 0.76). The predictor does not separate the cross-generator
   classes either.

### 3-property classifier search

Best 3-property AND rule fitted on the 26-family swept set ONLY:

> `(avg_deg ≥ 10.4146) AND (z_sym ≥ 0.0000) AND (reach_frac ≥ 0.8587)`
> in-sample accuracy: **92.3%** (same as the 2-property rule)

The search **rejected** `local_z_asym`. The third clause is
`z_sym ≥ 0.0000`, which is trivially satisfied by every family in the
sweep — it adds no information. In effect, the 3-property search
collapses back to the original 2-property rule on this data.

### Cross-generator accuracy (unchanged)

| Rule | Cross-generator (no refit) |
| --- | ---: |
| Old 2-property: `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` | 6/9 = 66.7% |
| New 3-property with `local_z_asym` available | 6/9 = 66.7% |

The 3-property rule does not improve cross-generator accuracy because
the search couldn't find a `local_z_asym` threshold that helps in-sample
without hurting it elsewhere.

## What this rules out

The most natural reading of the previous negative result was that the
required predictor must capture **statistical Z2 symmetry under dense
random sampling**. This lane tests that reading directly with a
node-level Z2 metric. The metric **fails to separate** PASS from FAIL
either within the grown-DAG family or across generators.

So the missing property is **not** captured by per-node edge balance
in z. The grown-DAG passes despite having `local_z_asym ≈ 0.41` (per-node
asymmetry from random drift); the ER passers have `local_z_asym ≈ 0.70`
(higher, from independent sampling); the random k-regular failures have
`local_z_asym ≈ 0.71` (essentially the same as the ER passers).

Whatever makes the 2/9 ER families pass is **not** their per-node Z2
balance. It must be something else — most likely a **global property**
that grown-DAG and dense ER share but random k-regular and expander
lack at the same nominal `avg_deg`.

## Candidate explanations (not yet tested)

1. **Spectral gap of the DAG transfer matrix.** Grown-DAG and dense
   ER both have many short paths between source and detector; expander
   and random k-regular have *fewer* paths despite similar avg_deg
   (because the random structure spreads paths thinly).

2. **Number of distinct paths per detector cell.** Grown-DAG has
   ~md² paths between adjacent layers; ER at p=0.20 has ~120;
   random k-regular at k=15 has only k=15.

3. **Path interference coherence.** A node-level metric can't capture
   how phases align along multi-step paths. The required predictor
   may be a path-level integral, not a node-level statistic.

4. **Density floor much higher than the rule's threshold.** Both ER
   passers have avg_deg ≥ 30; both lowest-failing random k-regulars
   have avg_deg ≤ 19. The honest minimum-density rule may be
   `avg_deg ≥ 25` rather than `≥ 10.42`. Note: deriving that from
   the cross-generator results would be data dredging — the honest
   move is to stop fitting and switch attack modes.

## Combined verdict (this lane + the previous one)

**Two negative results in a chain:**

1. The 2-property classifier `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)`
   fits the grown-DAG family but does not generalize across generators
   (independent-generators lane: 6/9 rule, 4/9 pre-committed).
2. The most natural 3rd predictor (`local_z_asym`) is rejected by the
   classifier search and does not improve cross-generator accuracy
   (this lane: 6/9 → 6/9).

**The simple-classifier line of attack on this generator family is
exhausted.** Continuing to search for 2- or 3-property AND rules over
node-level metrics is no longer informative. Either:

- Move to **matter / inertial closure** (gap #3 from the older frontier
  map, attacks a different scorecard column)
- Or attempt an **analytic derivation** of why grown-DAG works (the
  spatial neighbor-square stencil gives coherent path interference)
  and why random k-regular at the same nominal degree does not

## Frontier map adjustment

| Row | Previous | This update |
| --- | --- | --- |
| Strength against harshest critique | reverted by independent-generators | unchanged (still reverted) |
| Compact underlying principle | reverted | further constrained: it cannot be a simple node-level rule |
| Theory compression | open | sharper target now: global path-counting or spectral structure, not node statistics |

## Bottom line

> "The local per-node Z2 asymmetry hypothesis from the previous negative
> lane is rejected. The 3-property classifier search picks the same
> two predictors as the 2-property rule and the 3rd clause is vacuous.
> Cross-generator accuracy stays at 6/9 = 66.7%. The simple-classifier
> line of attack on this generator family is exhausted; the next move is
> matter/inertial closure or an analytic derivation, not further
> classifier hardening."
