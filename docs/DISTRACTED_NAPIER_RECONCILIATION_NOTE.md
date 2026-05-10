# Distracted Napier Reconciliation Note

---

**This is a branch-reconciliation / classification note. It does not
establish any retained claim.**
For retained claims on gap-physics / `distracted-napier` content, see
the per-claim notes referenced from the `## Audit scope` block below.

---

**Date:** 2026-04-02
**Status:** support / branch-classification record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / branch-classification record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Scope:** branch-only science in `.claude/worktrees/distracted-napier`

This note classifies the remaining branch-only gap-physics claims against the
current `main` state after the later cleanup work.

## Audit scope (relabel 2026-05-10)

This file is a **branch-reconciliation / classification note** for
the `distracted-napier` worktree's gap-physics content. It is **not**
a single retained theorem and **must not** be audited as one. The
audit ledger row for `distracted_napier_reconciliation_note`
classified this source as conditional/positive_theorem with auditor's
repair target:

> register a runner/proof note for the load-bearing step or cite an
> audited retained dependency.

The minimal-scope response in this PR is to **relabel** this document
as a branch-reconciliation classification record rather than to
register a runner or cite an audited retained dependency for the
classification verdicts here. Those steps belong in dedicated
review-loop or per-claim audit passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The "Already Superseded by `main`" / "Still Useful" / "Branch
  History Only" classification verdicts and per-script "Status:
  support" labels below are **historical branch-classification
  memory only**.
- The retained-status surface for any gap-physics, Born, gravity, or
  decoherence sub-claim is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim notes, **not**
  this branch-reconciliation record.
- Retained-grade does **NOT** propagate from this reconciliation note
  to any branch script, classification verdict, or successor cleanup.

For any retained claim about gap-physics content, audit the
corresponding dedicated note (or its `main`-side replacement) and its
runner as a separate scoped claim — not this branch-reconciliation
record.

---

## Executive Summary

`distracted-napier` was valuable as the original gap-physics branch, but most of
its strongest claims have now been superseded by cleaner `main` work:

- `main` now has the matched geometry head-to-head card
- `main` now has the generated asymmetry-persistence lane
- `main` now has the corrected gravity-law cleanup notes
- `main` now has the corrected collapse Born calibration script

The branch still contains useful historical detail, but only a small subset of
its ideas are still worth porting.

## Already Superseded by `main`

### `gap_ln_born_check.py`

Branch claim:
- `LN + |y|` is Born-clean at machine precision and gives a very large
  effective range (`N_half ~ 85k`)

Why this is superseded:
- `main` now uses corrected Born calibrations and shows that layer norm is not
  generically Born-clean in 3D chokepoint form
- the branch Born check uses an older Sorkin setup and is not aligned with the
  corrected harness standard now used on `main`
- the very large `N_half` claim is therefore not review-safe as a canonical
  result

**Status:** support - structural or confirmatory support note
- keep as branch history only
- do **not** promote as a main claim without rerunning on the corrected harness

### `gap_joint_coexistence.py`

Branch claim:
- `|y|<2` removal is the best joint gravity+decoherence lane at `N=80`

Why this is superseded:
- `main` now has a matched head-to-head comparison of the competing bounded
  geometry lanes
- `main` also has the generated asymmetry-persistence joint card, which is a
  stronger and more explicit same-graph joint result

Status:
- the branch claim is directionally consistent, but it is no longer the
  canonical comparison
- the branch script is superseded by the more controlled `main` lane cards

### `gap_layernorm_combined.py`

Branch claim:
- `LN + |y|` produces the strongest combined scaling result
- branch summary advertises an especially large `N_half`

Why this is superseded:
- `main` now has a stricter matched comparison between `LN + modular gap`,
  `LN + |y|` and generated hard-geometry lanes
- the best combined result on `main` is now reported more conservatively and is
  explicitly bounded by dense-geometry regime and Born-clean checks

Status:
- the combined idea is still live
- the branch implementation is not the canonical source anymore

### `gap_y_removal_sweep.py`

Branch claim:
- `|y|<2` is the optimal threshold and the joint coexistence is strong from
  `N=25` to `N=100`

Why this is mostly superseded:
- `main` now has the same-family head-to-head comparison and later generated
  geometry work
- the `|y|`-removal idea itself remains valid, but the branch sweep is no longer
  the best evidence package

Status:
- concept still worth keeping
- branch sweep itself is superseded by `main` comparison notes

## Still Worth Porting

### `gap_y_removal_sweep.py` idea, not the script as-is

Why it is still worth keeping:
- the simplest hard-geometry rule remains scientifically important
- `|y|`-removal is still one of the cleanest bounded geometry lanes
- it remains a good comparison point against generated hard geometry

What to port:
- the conceptual result, not the stale branch summary
- if needed, port only the threshold-sweep framing into a fresh `main` card

### `gap_layernorm_combined.py` idea, not the branch claims

Why it is still worth keeping:
- hard geometry plus layer normalization is still a real combined lane
- the branch was part of the route that led to the later, cleaner matched
  comparisons

What to port:
- the combined-lane intuition
- not the older unqualified `N_half` headline

## Unsafe / Stale

### `gap_ln_born_check.py` as a canonical Born result

Reason:
- older harness
- not aligned with corrected Sorkin / Born calibration
- branch summary overclaims Born cleanliness

### `gap_joint_coexistence.py` as the final joint comparison

Reason:
- superseded by the later matched geometry head-to-head and generated
  asymmetry-persistence joint cards on `main`

### Any claim that `LN + |y|` is the definitive asymptotic escape from the
ceiling

Reason:
- `main` now treats the combined bounded lanes more conservatively
- the asymptotic question remains open

## Bottom Line

`distracted-napier` should be treated as the historical source of the gap
program, not the canonical source of the current claim set.

What survives into `main`:

- the gap as a topological boundary condition
- `|y|`-removal as a simple bounded hard-geometry rule
- the importance of joint gravity+decoherence comparison

What does **not** survive unchanged:

- the branch Born headline for `LN + |y|`
- the branch `N_half ~ 85k` claim
- the branch-level joint-comparison wording

Recommended use:

- cite `main` for the current claims
- keep `distracted-napier` only as historical provenance and for the idea
  origin of `|y|`-removal / combined geometry
