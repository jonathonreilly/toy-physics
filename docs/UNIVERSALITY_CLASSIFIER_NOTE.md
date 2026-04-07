# Universality Classifier: Empirical Two-Property Predictor on a Wide Family Sweep

**Date:** 2026-04-07 (revised, dynamic-augmented battery)
**Status:** retained positive — empirical 2-property classifier on a 26-family sweep with **5-condition battery (4 static + 1 dynamic Lane 6 gap)**. In-sample 92.3%, leave-one-out 84.6%, 8-family held-out with pre-committed predictions 8/8 (in-sample-fitted rule applied to held-out 7/8). NOT a derived universality theorem.

## Artifact chain

- [`scripts/universality_classifier.py`](../scripts/universality_classifier.py)
- [`logs/2026-04-07-universality-classifier.txt`](../logs/2026-04-07-universality-classifier.txt)

## Question

The hostile critique against the program was *"three families is a small
engineered basin."* This lane attempts to widen the basin and find a
structural rule that predicts pass/fail on the dynamic-augmented
weak-field package (4 static conditions + the Lane 6 retarded-vs-instantaneous
gap on a (2+1)D wave-equation field).

## Battery (4 static + 1 dynamic)

The observable battery is now **5 conditions**:

Static (4):
- gravity sign under an imposed 1/r field
- F~M slope across 4 source strengths
- Born |I3|/P (3-slit interferometer)
- null at s=0

Dynamic (1, added in this revision):
- **Lane 6 retarded-vs-instantaneous gap** on a (2+1)D wave-equation
  field with the source moving in z. The harness builds both the
  retarded history M and an instantaneous comparator I (cached static
  slices per source position) and runs the beam through both. PASS
  requires the relative gap |dM − dI| / max(|dM|, |dI|) > 0.05.

PASS = (gravity TOWARD) AND (|F~M − 1| < 0.10) AND (Born < 1e-10)
       AND (|null| < 1e-10) AND (dyn_gap > 0.05).

Adding the dynamic condition is decisive: **two families that pass
the static-only battery fail the dynamic condition** (E2_PW10_wide
and K3_NL5). The dynamic condition is genuine new information,
not redundant with the static checks.

## Sweep

26 grown-DAG families across 12 generator axes (drift, restore,
neighbor reach, beam width, lattice depth, structural mode, anisotropy,
seed, pathological corners). Result with the dynamic-augmented battery:
**21 / 26 PASS, 5 / 26 FAIL**.

The five failures are explicit:

| Family | failure mode |
| --- | --- |
| E2_PW10_wide | dyn gap = 2.03% < 5% (wide beam → field doesn't have time to differentiate retarded from instantaneous) |
| G2_asym_z | grav sign collapses, F~M=1.79; z_sym=0.996 (broken Z2 in measurement axis) |
| H1_ring | grav goes AWAY (−0.0055); avg_deg=17.7 (too sparse) |
| I1_drift_y | field doesn't reach detector; avg_deg=10.4 (sheared + sparse); also dyn=0% |
| K3_NL5 | dyn gap = 0.00% (NL=5 too short for the wave equation to evolve) |

E2 and K3 are NEW failures introduced by the dynamic condition — they
pass the static battery but fail the Lane 6 gap. This is the test that
the dynamic condition adds genuine information.

## Empirical classifier (in-sample, dynamic-augmented)

Two-property AND rule, fitted on the 26-family sweep with the
5-condition (4 static + 1 dynamic) battery:

> `(avg_deg ≥ 10.415) AND (reach_frac ≥ 0.859)` → **24/26 = 92.3%** in-sample

Where:
- `avg_deg` = average forward degree (mean number of forward neighbors)
- `reach_frac` = fraction of detector-layer nodes reachable from origin

The static-only rule from the previous revision was
`(avg_deg ≥ 20.74) AND (z_sym ≤ 0.002)` and hit 100% on the static
battery. Adding the dynamic condition demoted it. The dynamic-augmented
rule shifts the second predictor from z_sym to reach_frac and the
in-sample accuracy drops by 7.7 points. **This degradation is honest:
it tells us the static-only rule was over-fitted to the static battery
and that the dynamic condition is not captured by the same predictors.**

## Validation

### Leave-one-family-out cross-validation

For each family in turn, refit the 2-property AND rule on the remaining
25 (using the dynamic-augmented battery) and apply it to the held-out family.

> **LOO accuracy: 22/26 = 84.6%**

LOO misses (4) on the dynamic-augmented battery:
- `E2_PW10_wide` (truth=FAIL, predicted=PASS): the LOO rule admits E2 because reach_frac=0.929 passes the threshold
- `G1_asym_y` (truth=PASS, predicted=FAIL): the LOO rule excludes G1 because its reach_frac=0.504 is below threshold
- `G2_asym_z` (truth=FAIL, predicted=PASS): the LOO rule re-fits to `reach_frac >= 0.504` and admits G2
- `K3_NL5` (truth=FAIL, predicted=PASS): the LOO rule chooses the static-era thresholds and admits K3

The misses are still **threshold-instability** cases. Two of them
(E2, K3) are the new dynamic-fail families, which the rule doesn't
capture cleanly with these two predictors. This is informative:
**the dynamic condition appears to need a third predictor or a
different second predictor** that the current 2-property AND search
space does not contain.

### Held-out family validation (8 families, predictions pre-committed)

A separate set of 8 families was constructed AFTER the in-sample
classifier was found. Predictions for each were **hard-coded in
HELDOUT_PREDICTIONS in the script source** before running. The audit
trail is in the script itself.

| Family | pre-committed | actual | in-sample-rule pred | agree |
| --- | :---: | :---: | :---: | :---: |
| HELD_dense_sym | PASS | PASS | PASS | OK |
| HELD_grid_seed7 | PASS | PASS | PASS | OK |
| HELD_ring_md3 | FAIL | FAIL | FAIL | OK |
| HELD_asym_z_seed7 | FAIL | FAIL | FAIL | OK |
| HELD_asym_y_seed7 | PASS | PASS | PASS | OK |
| HELD_drift_y_seed7 | FAIL | FAIL | FAIL | OK |
| HELD_aniso_z3 | PASS | PASS | PASS | OK |
| HELD_cross_seed7 | PASS | PASS | PASS | OK |

> **Pre-committed predictions: 8/8 = 100.0%**
> **In-sample-fitted rule applied to held-out without refit: 7/8 = 87.5%**

The pre-committed predictions still hold 8/8: my structural intuition
about which families would pass or fail is unchanged by the addition
of the dynamic condition (none of the 8 held-out families fall in the
"passes static, fails dynamic" failure mode of E2/K3).

The in-sample-fitted rule applied to the held-out set drops to 7/8.
The miss is `HELD_asym_y_seed7`, which actually PASSES the
dynamic-augmented battery but is excluded by the rule because its
reach_frac=0.504 is below the 0.859 threshold. This is a case where
the rule is more conservative than the underlying physics: structures
with low reach_frac can still satisfy the package if they happen to
be Z2-symmetric in z, which the new (avg_deg, reach_frac) rule doesn't
encode.

## Honest read

This is an **empirical classifier** on a swept family set with a
**dynamic-augmented battery**, validated by LOO cross-validation
and a held-out predicted set. It is **not yet a derived universality
theorem**.

What is true after the dynamic augmentation:
- 21 of 26 swept families exhibit the full 5-condition package
- The 5 failures are exhibited explicitly, with structural reasons
- 2 of the 5 failures (E2, K3) are NEW — discovered only by the dynamic condition
- A 2-property AND rule achieves 92.3% in-sample, 84.6% LOO, 87.5% held-out (rule), 100% held-out (pre-committed)
- The held-out set contains both positive and negative predictions made before the run
- Adding the dynamic condition LOWERED the in-sample accuracy from 100% to 92.3%, which is the right behavior — it tells us the static-only rule was over-fitted to the static battery

What is **not** yet true:
- The classifier is empirical, not derived from the path-sum + S=L(1−f)
- The dynamic-augmented thresholds are fitted, not theoretically motivated
- The miss patterns suggest the 2-property AND search space is too restrictive for the full 5-condition battery
- The held-out set is itself constructed by the same author, on the same lattice, with the same generator family
- A genuinely independent generator family (random k-regular, hyperbolic, expander) has not been tested

## What changes about the critique

The "small engineered basin" critique is weakened, not killed:
- 26 swept + 8 held-out = 34 families total, with 5 explicit negatives
- The battery now includes one dynamic condition (Lane 6 gap), not just static
- The dynamic condition discovers 2 failure modes the static battery missed
- A simple 2-property rule still gives 87.5% on a separate held-out set

What remains for a stronger statement:
- Analytic derivation of the rule from the propagator + action (or a no-go)
- A held-out set built by an independent generator family (random k-regular, hyperbolic, expander)
- A 3-property classifier search to capture the dynamic condition cleanly
- Independent reproduction by a non-author generator

## Bottom line

An empirical classifier on a 5-condition battery with LOO and pre-committed
held-out validation is stronger than the original three-family story,
and stronger than the static-only revision, but still weaker than a
universality theorem. The current honest framing is:

> "On 26 swept + 8 held-out grown-DAG families, the dynamic-augmented
> weak-field package (4 static + 1 Lane 6 gap > 5%) is empirically
> predicted by `(avg_deg ≥ 10.42) AND (reach_frac ≥ 0.86)` with
> 92.3% in-sample, 84.6% leave-one-out, 87.5% held-out (in-sample-fitted
> rule), and 100% held-out (author's pre-committed predictions)."
