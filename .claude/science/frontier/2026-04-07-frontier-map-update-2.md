# Frontier Map Update #2 — 2026-04-07 (cross-generator negative)

## Reversal of the previous update

The previous update (2026-04-07-frontier-map-update.md) recorded a
**modest bump** against the harshest critique on the strength of the
universality classifier. That bump is now **reversed** by the
independent-generator held-out lane.

## What happened

The classifier rule from the universality_classifier lane was
`(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)`, fitted on the
26-family sweep and validated by:
- LOO at 84.6%
- 8-family in-family held-out at 7/8 rule, 8/8 pre-committed predictions

A new lane held the rule out against **9 genuinely different generator
families** (random k-regular forward DAG, Erdős–Rényi forward, long-range
random, tree-like, hub-and-spoke, bipartite expander). Both predictions
and the rule were applied without refit.

> Pre-committed predictions: 4/9 = 44.4%
> Rule applied without refit: 6/9 = 66.7%
> Generators reproducing the full package: 2/9 (both ER at high p)

## Updated scorecard direction

| Row | Previous | This update | Reason |
| --- | --- | --- | --- |
| Strength against harshest critique | small bump | **reverted** | rule does not survive cross-generator held-out |
| Compact underlying principle | small bump | **reverted** | the 2-property AND form is too narrow; need a 3rd predictor or different functional form |
| Theory compression | open | open | unchanged; the negative result actually clarifies what a derivation would need to capture |
| Matter / inertial closure | open | open | unchanged |
| Independent reproduction | flagged | partially addressed (own-author cross-generator), still open for non-author |

## What the negative result tells us positively

Two passers (E1, E2) are both Erdős–Rényi at high `avg_deg`. Failures
include random k-regular and expander generators with the same
nominal structural numbers. This points to:

- The required predictor is **not** just degree count; it is some
  measure of **statistical Z2 symmetry under dense random sampling**
- The original rule was a within-family proxy for spatial coherence
  in the grown-DAG generator; the proxy doesn't generalize
- A 3-property classifier (or a variance-based predictor) is the
  natural next step

## What the next moves now look like

1. **Do not re-fit** the classifier on the new 9 — that would be
   data dredging. The honest move is to acknowledge the empirical
   classifier does not generalize.

2. **Build a 3rd predictor** that captures statistical Z2 symmetry
   over edges, not just the mean. Run it on both the swept set and
   the 9 independent generators with no refit on the latter.

3. **Matter / inertial closure** is now a higher-priority next
   moonshot than further classifier hardening, because the universality
   row is now constrained from above by what a 2-property rule can do
   on this family of generators.

4. **Analytic derivation** is still the highest leverage move but
   highest cost. It would now have a sharper target: explain why
   spatial neighbor-square stencils plus high density give the package,
   while random k-regular at the same density does not.

## Bottom line

The earlier modest bump is gone. The static + dynamic classifier
within the grown-DAG family is real, but it does not generalize to
qualitatively different generators. The "small engineered basin"
critique stands, with sharper boundaries and a clearer target for
the next attack.
