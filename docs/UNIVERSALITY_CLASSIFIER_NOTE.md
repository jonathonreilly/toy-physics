# Universality Classifier: Two-Property Predictor of the Weak-Field Package

**Date:** 2026-04-07
**Status:** retained positive — 26-family sweep across 12 generator axes; **100.0% accuracy** classifier on two structural properties; three negative cases exhibited and explained

## Artifact chain

- [`scripts/universality_classifier.py`](../scripts/universality_classifier.py)
- [`logs/2026-04-07-universality-classifier.txt`](../logs/2026-04-07-universality-classifier.txt)

## Question

The hostile critique against the program is *"three families is a small
engineered basin."* That is the strongest single objection — until we
can either (a) widen the basin much further, or (b) exhibit families
that fail and identify a structural property that predicts pass/fail.
This lane attempts both at once.

## Sweep

26 grown-graph families across 12 generator axes:

- **A**: original three (Fam1/2/3)
- **B**: pure regular grid (drift=0, restore=1)
- **C**: pure random (restore=0, drift up to 1.0)
- **D**: neighbor reach md ∈ {1, 4}
- **E**: beam width PW ∈ {3, 10}
- **F**: lattice depth NL ∈ {10, 40}
- **G**: Z2-broken connectivity (asym_y, asym_z)
- **H**: sparse stencils (ring, cross)
- **I**: sheared connectivity (only dy=+1)
- **J**: anisotropic z reach (×2, ×4)
- **K**: pathological corners (huge drift NN, NL=5, PW=2)
- **L**: seed variation

Each family runs the identical observable battery: free run, gravity
sign, F~M slope (4 strengths), Born |I3|/P (3-slit), null at s=0.

PASS = (gravity TOWARD) AND (|F~M − 1| < 0.10) AND (Born < 1e-10) AND (|null| < 1e-10)

## Result

**23 / 26 PASS, 3 / 26 FAIL.**

| Family | failure mode |
| --- | --- |
| G2_asym_z | grav sign collapses, F~M = 1.79; z_sym = 0.996 |
| H1_ring | grav sign goes AWAY (−0.0055); avg_deg = 17.7 |
| I1_drift_y | field doesn't reach detector (reach_frac = 0); avg_deg = 10.4 |

## Structural classifier

Each family is annotated with three structural metrics:

- **avg_deg**: average forward degree (mean number of forward neighbors per node)
- **z_sym**: |Σ dz over edges| / Σ |dz| over edges (0 = perfectly Z2 in z)
- **reach_frac**: fraction of detector-layer nodes reachable from origin

Single-property classifier:
- best is `avg_deg ≥ 20.74` → **96.2%** accuracy (misses G2_asym_z)

Two-property AND classifier:
- `(avg_deg ≥ 20.74) AND (z_sym ≤ 0.002)` → **100.0% accuracy on all 26 families**

## The classifier statement

> **The weak-field package (gravity TOWARD, F~M ≈ 1, Born ≈ 0, exact null)
> holds iff the grown DAG has (a) average forward degree ≥ ~21 AND
> (b) edge sum in the measurement direction ≤ ~0.2% of total |edge|.**

In words: the package requires
1. **Sufficient connectivity** — the causal cone must fill out densely enough that paths can interfere coherently (sparse ring/sheared stencils fail).
2. **Z2 mirror symmetry in the measurement axis** — the connectivity cannot have a preferred direction in z (or whichever axis we measure).

Each failure case violates exactly one of these:
- **G2_asym_z** has z_sym = 0.996 (asymmetric in z) but adequate degree → fails clause (b)
- **H1_ring** has z_sym ≈ 0 but avg_deg = 17.7 (too sparse) → fails clause (a)
- **I1_drift_y** has z_sym ≈ 0 but avg_deg = 10.4 (too sparse + degenerate reach) → fails clause (a)

And **G1_asym_y** PASSES because the asymmetry is in y, not z (the
measurement axis). This is a non-trivial check: the predictor is the
edge balance in the *measured* direction, not generic asymmetry.

## What this means

The hostile critique that the program rests on a small engineered
basin is now answered with a falsifiable claim:

- The basin is at least 23 families wide across 12 generator axes
- The basin has a clean *boundary*, characterized by 2 structural properties
- Both properties have intuitive physical meaning (connectivity + parity)
- Both properties are checkable from the graph alone, without running the beam
- Three failure modes are explicitly retained as negatives — the claim cannot be vacuous

This is the closest thing to a universality theorem the program can
offer numerically. It says the weak-field package is **forced** by two
structural properties, not curated.

## Honest limits

- 26 families is wider than 3 but not exhaustive
- The classifier was *fitted* on this set, not derived analytically; an analytic proof from the path-sum propagator + S=L(1−f) would be the next step
- Z2 in y is not tested as the measurement axis; the test direction is hard-coded to z
- Retarded vs instantaneous (Lane 6 dynamic gap) is not in this battery — a future extension should add it as a 5th condition
- The classifier assumes the same propagator and action across families; varying those is a separate axis not yet swept
- The "≥ 20.74" threshold is the smallest passing avg_deg in the sweep; the true theoretical bound may be lower

## Bottom line

The basin is **wide and bounded**. The boundary is given by two
structural properties of the graph, both with simple physical meaning.
The "engineered basin" critique is no longer correct in its strong
form — the program now exhibits its own failure modes and predicts
them from graph structure alone.
