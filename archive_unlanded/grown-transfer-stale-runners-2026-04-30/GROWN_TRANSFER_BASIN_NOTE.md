# Grown Transfer Basin Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/grown-transfer-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/grown-transfer-stale-runners-2026-04-30/` (failure reason: stale runners — the targeted basin checker uses the wrong complex-action survival criterion, and its current output for the four declared nearby rows reports 0/4 surviving)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: `scripts/GROWN_TRANSFER_BASIN_TARGETED.py` still requires `abs(row.action_gamma0) < 1e-12`, the exact complex-action survival criterion that the source note says is wrong. Its live output for the four declared nearby rows prints zero/neutral controls, charge exponent 1.000, F0/F05 = 1.000, and toward = (3, 0), but then reports `nearby rows surviving both observables: 0/4` and `the retained positives do not survive this nearby basin`. Why this blocks: the headline retained basin claim depends on the same-row signed-source plus complex-action survival decision, and the declared artifact chain currently gives a contradictory pass/fail verdict for that decision rather than a clean regenerated basin log. Repair target: patch the targeted basin checker to use the source note's stated criterion, require same-row intersection of signed-source and complex-action survival, rerun/archive the targeted and full basin outputs, and update the note only after the executable SAFE READ matches the retained claim. Claim boundary until fixed: safely claim that the central retained grown row and the single middle diagnostic row at drift=0.20, restore=0.60 pass the corrected signed-source and complex-action checks; do not claim a retained nearby basin or graph-ladder transfer beyond that repaired runner output.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

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

