# Grown Transfer Basin Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow grown-row basin positive, but selective rather than family-wide

## Artifact chain

- [`scripts/GROWN_TRANSFER_BASIN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/GROWN_TRANSFER_BASIN_SWEEP.py)
- [`scripts/GROWN_TRANSFER_BASIN_TARGETED.py`](/Users/jonreilly/Projects/Physics/scripts/GROWN_TRANSFER_BASIN_TARGETED.py)
- [`scripts/GROWN_TRANSFER_BASIN_DIAG.py`](/Users/jonreilly/Projects/Physics/scripts/GROWN_TRANSFER_BASIN_DIAG.py)
- retained grown-row controls:
  [`docs/FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md)
  and
  [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)

## Question

Do the retained moderate-drift grown-row positives survive on a small
neighborhood of nearby grown rows, without broadening the claim surface too
far?

This basin is intentionally tiny:

- signed-source transfer on nearby grown rows
- complex-action carryover on the same nearby rows
- no family-wide growth rule claim
- no geometry-generic transfer claim

## What Was Checked

The nearby rows were sampled around the retained moderate-drift grown row
`drift = 0.2`, `restore = 0.7`.

The checked neighborhood includes:

- previously observed reduced-basin nearby rows:
  - `drift = 0.15, restore = 0.60`
  - `drift = 0.20, restore = 0.70`
  - `drift = 0.25, restore = 0.80`
- the new middle diagnostic row:
  - `drift = 0.20, restore = 0.60`

## Frozen Read

The safe, reviewable statement is:

- the fixed-field signed-source transfer survives on the nearby basin
- the complex-action carryover survives on the same nearby basin when the
  correct criterion is used
- the basin is selective: the transfer survives on nearby rows, but not by
  broadening into a family-wide claim

### Middle diagnostic row

The new one-row diagnostic at `drift = 0.20, restore = 0.60` gives:

- zero-source and neutral same-point controls: printed zero
- single `+1`: AWAY
- single `-1`: TOWARD
- charge exponent: `1.000`
- complex-action crossover: `gamma = 0` TOWARD, `gamma = 0.5` AWAY
- weak-field `F~M`: `1.000` on both `gamma = 0` and `gamma = 0.5`

That row therefore sits inside the same narrow basin as the retained moderate-
drift positive.

## Code Note

The basin checker originally used the wrong complex-action survival criterion.
The fix is:

- do **not** require zero deflection at `gamma = 0`
- do require the retained `TOWARD -> AWAY` crossover plus near-linear
  `F~M`

That is why the basin is meaningful even though `gamma = 0` still produces a
nonzero deflection on the retained grown row.

## Relation To The Early Graph-Ladder Work

The old Gate B graph-ladder architecture work applies here only as a design
lesson:

- fixed connectivity and structured geometry are the bottleneck
- naive local rewires or generic noisy growth are not enough
- geometry-sector style rules can preserve a far-field package on a narrow
  family

That maps cleanly onto the current basin result:

- the nearby grown rows preserve the sign-law and complex-action package
- the basin is narrow and selective
- the surviving pattern looks connectivity-structured, not arbitrary

Relevant older notes:

- [`docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md)
- [`docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md)

## Final Verdict

**retained narrow basin positive**

The basin does meaningfully narrow the transfer gap, but only in the narrow
review-safe sense:

- the retained grown-row sign law survives on nearby rows
- the retained grown-row complex-action crossover also survives on nearby rows
- the neighborhood is still selective, so this is not family-wide transfer

