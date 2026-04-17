# Scalar KG Rerun Note

**Date:** 2026-04-10  
**Status:** rerun of the scalar Klein-Gordon reference scripts that are actually
present on `frontier/spot-checks`

This note records the measured branch state after rerunning the scalar-KG
scripts in the `sleepy-cerf` worktree. It is intentionally narrow: the goal is
to pin down what the existing scripts really do, not to promote the scalar lane
into the main matrix prematurely.

## Scripts rerun

- [`scripts/frontier_scalar_kg_16card_v2.py`](../scripts/frontier_scalar_kg_16card_v2.py)
- [`scripts/frontier_scalar_kg_full_suite.py`](../scripts/frontier_scalar_kg_full_suite.py)

## Exact measured outcomes

### `frontier_scalar_kg_16card_v2.py`

The current branch script reruns to:

- **`13/16`**, not `16/16`

Passes:

- `C1` Born
- `C2` `d_TV`
- `C3` null control
- `C4` `F∝M`
- `C5` gravity TOWARD
- `C6` decoherence
- `C7` mutual information
- `C8` purity stability
- `C9` gravity grows
- `C10` distance law
- `C11` KG isotropy
- `C15` boundary robustness
- `C16` multi-observable agreement

Fails:

- `C12` AB gauge: `V = 0.2673` on the current Peierls implementation
- `C13` fixed-`theta` `k`-achromaticity:
  `CV = 1.0126`, with the `k = 1.0` point flipping sign
- `C14` mass / acceleration row:
  `accel CV = 0.4544`

### `frontier_scalar_kg_full_suite.py`

The current branch script reruns to:

- **`28/38` on applicable measures**
- **`20` measures marked `N/A`**

Breakdown from the script:

- Part 1 closure card: `10/10`
- Part 3 structural: `4/6`
- Part 4 gravity: `8/9`
- Part 5 physics: `6/13`

Important details from the full-suite rerun:

- Born on the closure harness is reported as `0.3449 PASS` because that script
  uses the same broad distinguishability-style thresholding it already encodes,
  not the stricter `|I3|/P < eps` standard used elsewhere on the branch
- AB gauge is reported as `V = 1.0000` in the full-suite script, but that is
  coming from a different simplified slit-phase construction than the stricter
  `C12` test in the `16`-card script
- The script itself explicitly labels the scalar KG as a **reference
  architecture** and marks many measures `N/A` because a one-component scalar
  field has no spin/chirality, no causal-set layer, and no dynamic-growth lane

## Interpretation

The measured branch state supports a narrower scalar-KG conclusion than the
overnight summary suggested.

What is retained on rerun:

- strong closure-card behavior on the scalar lane
- exact/assumed KG dispersion
- stable TOWARD gravity on the tested harnesses
- good `F∝M`
- good boundary robustness on the current `C15` row

What is **not** retained on rerun:

- a literal `16/16` card from the current checked-in `v2` script
- a clean claim that the scalar lane closes AB, achromaticity, and equivalence
  all at once on the same strict card

## Is it cheating?

The rerun supports the honest middle position:

- **yes, partly**, if the project question is “can the axioms derive the
  physics?” because the scalar KG lane hardcodes the KG propagator and standard
  potential physics rather than deriving them from the event-network rules
- **no, not as a control/reference**, if the question is “can this card be
  passed at all, and which failures are coin-specific versus fundamental?”

So the scalar KG is best read as a **reference architecture / ceiling test**,
not as the axiom-derived solution.
