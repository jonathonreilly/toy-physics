# Review Note: `claude/g1-complete`

## Status

Current verdict: **do not merge as-is**.

The branch is cleaner than the earlier G1 submissions. The stale theorem-note
cross-reference is fixed, and the unrelated plaquette contamination appears to
be gone from the current delta. But the load-bearing flagship-closure blockers
are still open on the current tip `87ec25fb`.

## Current Re-Review (`87ec25fb`)

Result: **still no material review change on the claim-bearing science**.

The current branch still overstates what has been proved in three places:

1. the omnibus closure note still headlines the DM flagship gate as
   `CLOSED` and presents a unique perturbative-regime chamber solution, even
   though the retained route still depends on the conditional `q_H = 0`
   branch, the observational hierarchy pairing `sigma_hier = (2, 1, 0)`, and
   the weaker scale-cutoff selector rather than a theorem-native microscopic
   basin discriminator;
2. the Schur baseline note still proves only
   `commuting baseline => scalar baseline`, then upgrades that conditional
   statement into the stronger physical claim that the live zero-source
   baseline itself must be scalar;
3. the perturbative-uniqueness note still explicitly admits that the strong
   retained convergence condition `rho(H_base^{-1} J) < 1` fails at all three
   in-chamber basins, and then selects Basin 1 by the weaker norm statement
   `||J|| <= ||H_base||`.

So the current tip is improved presentation, not a closed flagship selector.

## What Is Resolved Since Earlier Reviews

- the old stale path to the perturbative-uniqueness note is fixed;
- the branch now looks like a G1-focused delta rather than a mixed G1 +
  plaquette rewrite branch.

Those are real cleanups. They just do not close the flagship claim.

## Live Blockers

### 1. Omnibus closure note is still too strong

The omnibus note currently says the flagship gate is `CLOSED` on the live
sheet and that the observational PMNS route yields a unique perturbative-regime
chamber solution.

That is stronger than the retained proof surface currently supports. The live
route still depends on:

- `q_H = 0` via the Z_3 trichotomy branch;
- the observational hierarchy pairing `sigma_hier = (2, 1, 0)`;
- the upper-octant chamber condition;
- Basin 1 being preferred by the weaker scale cutoff rather than by a retained
  microscopic selector theorem.

If those conditions remain unproved, then the flagship headline must carry them
explicitly or be demoted from `CLOSED`.

### 2. Schur lane still imports the missing physical premise

The Schur theorem itself is mathematically fine:

- if a baseline commutes with the retained three-generation algebra, then it is
  scalar.

What is still not proved is the physical upgrade:

- the live zero-source baseline on the actual source sheet must commute with
  that full retained algebra.

Until that premise is derived on the live sheet, the note must stop concluding
that the physical zero-source baseline is axiom-natively scalar.

### 3. Basin uniqueness is still only the weaker scale-cutoff route

The perturbative-uniqueness note is honest that true Taylor/log-det convergence
fails at all three in-chamber basins. Basin 1 is then selected by the weaker
criterion `||J|| <= ||H_base||`.

That may be a reasonable admissibility rule, but it is not yet a theorem-native
closure of the basin-selector problem.

If you want a merge-ready uniqueness claim, you still need one of:

- a retained theorem deriving that admissibility rule from accepted framework
  structure;
- a different retained discriminator that uniquely selects Basin 1;
- a stronger retained convergence/result criterion that Basin 1 satisfies while
  the competitors do not.

Otherwise the note should be framed as a conditional PMNS route under the added
scale rule, not final flagship closure.

## Acceptable Resubmission Shapes

### Option A: Conservative mergeable shape

Land the clean pieces only:

- the obstruction stack;
- the PMNS-as-`f(H)` chamber map;
- the citation-chain cleanup around the charged-lepton route;
- no flagship-closure headline.

### Option B: Strong closure resubmission

Keep the flagship-closure claim only if all three live blockers are genuinely
closed:

- derive the commuting-baseline premise on the live source sheet or demote the
  Schur lane to conditional/support status;
- derive a retained basin selector rather than relying only on the weaker norm
  cutoff;
- surface or derive the charged-lepton / hierarchy / octant conditions at the
  same strength as the headline claim.

## Bottom Line

This branch has real value and is much cleaner than the earlier G1 attempts.
But at the present claim level it is still not merge-ready. The fastest path is
either:

1. demote the current branch to a clean conditional PMNS route plus obstruction
   stack; or
2. actually close the Schur physical premise and the basin-selector theorem,
   then resubmit the flagship-closure headline.
