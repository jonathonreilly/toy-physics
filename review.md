# Review Note: `claude/g1-complete`

## Status

Current verdict: **do not merge as-is**.

The branch has improved since the earlier G1 pass. It is more explicit about
the `q_H = 0` conditionality, it no longer sells the weak norm cutoff as the
primary uniqueness story, and it now tries to separate the Schur lane from the
live-sheet closure lane.

But the current tip `1f6f95df` still does **not** clear the retained-bar
blockers, and the branch is now badly mixed relative to current `origin/main`.

## Current Re-Review (`1f6f95df`)

Result: **still not retained flagship closure**.

Three issues remain load-bearing:

1. the Schur runner still proves only a conditional commutant statement and
   then reuses it as if it forced the live-sheet baseline;
2. the new inertia/source-branch uniqueness story is cleaner than the old norm
   cutoff, but it still imposes a branch-choice rule rather than deriving it
   from retained framework structure;
3. the omnibus closure headline still says the DM flagship gate is `CLOSED`,
   which is stronger than the present proof boundary.

## Branch Hygiene

This branch is also **not clean against current `origin/main`**.

At review time it is substantially diverged from `origin/main` and still
reverts unrelated current-main package work. The current delta touches CKM,
charged-lepton, evanescent-barrier, Higgs/YT, publication-surface, and other
non-G1 files. In particular, relative to `origin/main`, the branch:

- downgrades the live CKM neutron-EDM split back to a plain bounded lane;
- deletes the current evanescent-barrier theorem surface;
- deletes the charged-lepton review package that is already live on `main`.

So even if the science blockers were gone, the branch would still be
non-landable as-is.

**Required hygiene step before any resubmission:** rebase or cherry-pick the G1
work onto the latest `origin/main`, and keep only the G1-related files in the
delta.

## Live Science Blockers

### 1. Schur lane is still only a commutant-class lemma

The note header now honestly says the live `H_base` does **not** commute with
the retained three-generation algebra, so the scalar-baseline result is only a
commutant-class structural lemma.

That demotion is correct.

But the runner still states the load-bearing premise that the axiom-native
baseline "must commute" with the retained generation algebra, then uses that
premise to promote

`D = m I_3` and `Q(delta, q_+) = 6(delta^2 + q_+^2)/m^2`

into theorem-native live-sheet curvature.

That is still the same unresolved gap in executable form:

- proved: `if D commutes with the retained generation algebra, then D = m I_3`
- not proved: the live DM-neutrino source-sheet baseline actually satisfies
  that commutation premise

Until the live-sheet commutation premise is derived, the Schur lane must remain
strictly a **conditional commutant-class lemma**, not a promoted live-sheet
curvature theorem.

### 2. Inertia/source-branch uniqueness is still an added admissibility rule

Replacing the old norm cutoff with Sylvester inertia is mathematically cleaner.
It is a real improvement over the previous `||J|| <= ||H_base||` packaging.

But the load-bearing step is still not derived from retained framework
structure.

The current note defines the "retained source branch" to be the connected
component of

`det(H_base + J) != 0`

that contains `J = 0`, equivalently the component with preserved signature
`signature(H_base + J) = signature(H_base) = (2, 0, 1)`.

Then it excludes the competing exact basins because they lie on a different
signature component.

What is still missing is the physical bridge:

- why the physical PMNS closure must remain on the baseline-connected
  non-caustic component rather than another admissible component on which
  `W[J] = log|det(H_base + J)|` is also well-defined

So the new uniqueness story is still:

- algebraically nicer than the old norm rule
- but still an added branch-choice principle, not a retainedly forced selector

### 3. Flagship closure header is still too strong

Because the Schur lane is still conditional and the source-branch selector is
still imposed rather than derived, the omnibus note still overstates the branch
by calling the DM flagship gate `CLOSED`.

The branch now supports a stronger and cleaner **conditional/support closure
story** than before:

- `sigma_hier = (2, 1, 0)` is surfaced explicitly
- `q_H = 0` is surfaced explicitly
- the upper-octant conditionality is surfaced explicitly
- Basin 1 is isolated by the branch-choice rule more cleanly than before

But that is not yet the same thing as a fully retained closure of the selector
gate.

## Acceptable Resubmission Shapes

### Option A: Clean support / conditional package

If the worker wants a mergeable near-term resubmission, the safe shape is:

- keep the obstruction stack;
- keep the PMNS-as-`f(H)` construction;
- keep the explicit `q_H = 0`, `sigma_hier`, and upper-octant conditions;
- demote the flagship headline from `CLOSED` to conditional/support status;
- keep the Schur lane explicitly as a commutant-class lemma only;
- keep the source-branch selector explicitly as a branch-choice rule /
  conditional admissibility principle, not a retained theorem.

### Option B: Strong retained-closure resubmission

If the worker wants to retain the flagship-closure headline, they still need to
close both load-bearing gaps:

1. **Close the live-sheet Schur premise.**
   Derive, on the actual source-oriented sheet, why the relevant zero-source
   baseline must commute with the retained three-generation algebra; or else
   stop using Schur to promote live-sheet curvature.

2. **Close the branch-choice principle.**
   Derive why the physical closure must lie on the baseline-connected
   `det != 0` component rather than another non-caustic component; or else
   demote the inertia/source-branch selector to conditional support status.

Without both of those, the gate is not fully retainedly closed.

## Required Rebase Discipline

Before any next reviewer pass:

1. start from the latest `origin/main`;
2. cherry-pick or re-implement only the G1 files;
3. confirm that CKM, charged-lepton, evanescent, Higgs/YT, and unrelated
   publication-surface files are not regressed;
4. resubmit the clean G1-only batch.

## Bottom Line

This branch is scientifically sharper than the earlier G1 attempts.

But the present tip still does **not** clear the retained-bar blockers, and it
is also operationally non-landable because it regresses unrelated current-main
package work.

The fastest honest path is:

1. rebase/cherry-pick onto latest `origin/main` as a clean G1-only delta; and
2. either
   - demote the package to a conditional/support PMNS closure story, or
   - actually derive the live-sheet Schur premise and the source-branch
     admissibility rule, then resubmit the flagship-closure headline.
