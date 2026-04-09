# Independent-Generator Held-Out Test of the Universality Classifier — NEGATIVE RESULT

**Date:** 2026-04-07
**Status:** retained negative — the classifier rule from `universality_classifier.py` generalizes to only 2/9 genuinely different generator families. Pre-committed predictions: 4/9 = 44.4%. In-sample rule applied without refit: 6/9 = 66.7%. The rule is brittle to truly independent generators.

## Artifact chain

- [`scripts/independent_generators_heldout.py`](../scripts/independent_generators_heldout.py)
- [`logs/2026-04-07-independent-generators-heldout.txt`](../logs/2026-04-07-independent-generators-heldout.txt)

## Question

The universality classifier (Lane 9) was validated on a 26-family sweep
plus an 8-family held-out set. Both sets were parameter variations of
the same underlying generator (a regular `(layer, iy, iz)` lattice with
neighbor square stencil and Gaussian drift). The "small engineered
basin" critique remains because the held-out set is the same generator
family.

This lane evaluates the in-sample-fitted rule
`(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` on **9 genuinely different
generator families**, with predictions hard-coded BEFORE running.
The rule is applied **without refit**.

## Independent generators

All generators place nodes on the same `(layer, iy, iz)` grid scaffolding
so the wave-equation field measurement still works, but the EDGE topology
is independent of the original neighbor square stencil:

| Family | Generator | avg_deg target |
| --- | --- | ---: |
| R1 | random k-regular forward, k=15 | 15 |
| R2 | random k-regular forward, k=8 | 8 |
| R3 | random k-regular forward, k=20 | 20 |
| E1 | Erdős–Rényi forward, p=0.05 | ~30 |
| E2 | Erdős–Rényi forward, p=0.20 | ~120 |
| L1 | long-range random, k=12 over layers t+1..t+3 | 12 |
| T1 | tree-like, fanout=4, no convergence | ~1 |
| H1 | hub-and-spoke (one hub per layer) | low |
| X1 | bipartite expander, k=12 with shift mixing | 12 |

## Result

| Family | committed | actual | rule | agree-c | agree-r |
| --- | :---: | :---: | :---: | :---: | :---: |
| R1_kreg_k15 | PASS | **FAIL** | PASS | MISS | MISS |
| R2_kreg_k8 | FAIL | FAIL | FAIL | OK | OK |
| R3_kreg_k20 | PASS | **FAIL** | PASS | MISS | MISS |
| E1_er_p005 | FAIL | **PASS** | PASS | MISS | OK |
| E2_er_p020 | PASS | PASS | PASS | OK | OK |
| L1_longrange_k12 | PASS | **FAIL** | FAIL | MISS | OK |
| T1_tree_fan4 | FAIL | FAIL | FAIL | OK | OK |
| H1_hub | FAIL | FAIL | FAIL | OK | OK |
| X1_expander_k12 | PASS | **FAIL** | PASS | MISS | MISS |

> **Pre-committed predictions: 4/9 = 44.4%**
> **In-sample-fitted rule (no refit): 6/9 = 66.7%**

Only **2/9** generators pass the full 5-condition battery: `E1_er_p005`
and `E2_er_p020`. Both are Erdős–Rényi forward random — the closest
in spirit to the original grown-DAG (random but uniformly Z2-symmetric
with high avg_deg).

## What the failures mean

The decisive cases are R1, R3, and X1. All three have high avg_deg
(11.5–19.2) AND high reach_frac (0.90–0.94). The rule says PASS for
all of them. But all three FAIL the actual battery:

- **R1_kreg_k15** (avg_deg=14.4, reach=0.93): delta_z = −0.003
  (gravity AWAY); F~M = 0.877 (out of band)
- **R3_kreg_k20** (avg_deg=19.2, reach=0.94): delta_z = +0.104
  (much too large); F~M = 1.168 (out of band)
- **X1_expander_k12** (avg_deg=11.5, reach=0.896): delta_z = 0;
  F~M = nan (field doesn't reach detector coherently)

So **dense random connectivity at the same nominal `avg_deg` does NOT
reproduce the weak-field package**. Something specific to the
**spatially-organized neighbor square stencil** of the original
grown-DAG generator is doing the work, not just the count of forward
neighbors per node.

The two passing generators (E1, E2) are both ER with high
`avg_deg` (29.9 and 119.9). They pass because the random ER
sampling at high density approximates a uniform stencil — the
*spatial coherence* of the connectivity is partially restored by
the law of large numbers.

## What this changes about the harshest critique

This is a **strong negative result** that **reverses** the modest
"Strength against harshest critique" bump from the previous lane:

| Row | Previous read | Updated read |
| --- | --- | --- |
| Strength against harshest critique | static + 26 swept + 8 held-out | + 9 independent generators with **44.4% pre-committed and 66.7% rule accuracy** |
| Compact underlying principle | 2-property AND rule predicts 8/8 in-family | rule fails on 7/9 truly independent generators |
| Theory compression | open | open + this lane shows the classifier does not generalize |

The "small engineered basin" critique is **strengthened** by this
result. The classifier was a within-family fit, not a universal
predictor.

## What this tells us positively (yes, there is a positive)

Even a negative result has structural information. The 2/9 passers
share two specific features that the 7/9 failures lack:

1. **Very high avg_deg** (E1: 29.9, E2: 119.9 vs failures: 11.5–19.2)
2. **Z2-symmetric uniform random sampling** (ER samples each pair
   independently → no preferred direction; the failing random k-regular
   picks distinct edges per source node which may break statistical
   uniformity at the per-node level)

This points toward an updated empirical hypothesis:

> The package may require not just "average degree above threshold"
> but **statistical Z2 symmetry of the connectivity** — the *average*
> over edges in the measurement direction must be balanced when
> sampled densely enough that the law of large numbers applies.

This is a **3rd predictor candidate**, not a 2-property AND rule. The
existing universality_classifier 2-property search space is too
restrictive. Either:
- A 3-property classifier is needed
- Or the predictor must be the *variance* of dz across edges, not the
  mean

Either way, the original classifier statement should be downgraded from
"empirical predictor with held-out validation" to **"empirical
within-family predictor that does not survive cross-generator
held-out validation."**

## Honest read

- **Negative result on out-of-distribution generalization**
- 4/9 pre-committed predictions correct (worse than chance for some
  individual families)
- 6/9 rule predictions correct
- 2/9 generators reproduce the full package (both ER, both high avg_deg)
- 7/9 generators fail despite some satisfying the rule's structural conditions

This is **the right kind of moonshot result**: it tells us the
classifier is empirical and fragile, and points to the next required
hardening (a 3rd predictor or a different functional form). It does
not save the universality story, and it should not be presented as
doing so.

## What I commit to next

1. **Update UNIVERSALITY_CLASSIFIER_NOTE.md** with a new section
   pointing at this negative result and downgrading the bottom line
2. **Update the frontier map note** to record the reversal of the
   "modest bump against the harshest critique"
3. **Do NOT** re-fit the classifier on the new data — that would be
   data dredging. The honest move is to acknowledge the empirical
   classifier does not generalize and identify what would.

## Bottom line

> "The universality classifier rule
> `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` was held out against
> 9 genuinely different generator families. Pre-committed predictions
> achieved 44.4%, rule applied without refit achieved 66.7%, and only
> 2/9 generators reproduced the full 5-condition package. The rule
> is a within-family fit, not a universal predictor. The 'small
> engineered basin' critique is strengthened by this result."
