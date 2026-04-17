# Review Note: `claude/g1-complete`

## Status

Current verdict: **do not merge as-is**.

This branch has real science in it, but the flagship-closure claim is still too
strong for the current proof surface, and the branch is mixed with unrelated
plaquette edits. A clean resubmission is possible, but it needs to satisfy the
closure conditions below.

## Update After Re-Review (`7f6abe4a`)

I re-reviewed the branch after the follow-up theorem-note polish commit
`7f6abe4a`.

Result: **no material review change**.

The new commit improves phrasing, but it does not fix the substantive blockers:

- the Schur lane still imports the commuting-baseline premise instead of
  deriving it;
- the PMNS uniqueness lane still chooses Basin 1 by the weaker norm cutoff
  `||J|| <= ||H_base||` after the note itself admits that true log-det
  convergence fails at every basin;
- the flagship headline still understates the conditional `q_H = 0` and
  observational `sigma_hier = (2,1,0)` inputs;
- the branch is still mixed with unrelated plaquette authority rewrites.

One mechanical issue also still remains on the current tip:

- the PMNS closure note still links to the old filename
  `SELECTOR_PHYSICIST_J_PERTURBATIVE_UNIQUENESS_NOTE_2026-04-17.md`
  instead of the live
  `DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md`.

## What Must Be True For A "Closed" Resubmission

### 1. Split out the unrelated plaquette edits

This branch is not a clean G1 delta right now.

Before resubmitting G1 closure:

- remove the plaquette authority rewrites from this branch, including the
  deletion of the tensor-transfer note/runner and the companion bridge-surface
  wording edits; or
- move those plaquette changes onto a separate branch with its own review.

Recommended baseline: rebuild the G1 resubmission from current `main`.

### 2. Either really close the Schur-baseline premise, or demote it

The current Schur runner proves only:

- if the baseline commutes with the retained three-generation algebra, then it
  is scalar.

It does **not** prove the load-bearing premise:

- the physical zero-source baseline on the live source sheet must commute with
  that algebra.

To close this lane, you need one of:

- a retained theorem on the live source sheet deriving that commutation
  requirement from already-accepted framework structure; or
- a narrower rewrite that presents the Schur result only as a **conditional**
  or **support** theorem and stops using it as the load-bearing promotion from
  diagnostic baseline to theorem-native physical baseline.

If this is not closed, then the omnibus note must stop saying the
baseline-choice sub-objection is fully gone.

### 3. Either derive a real basin selector, or stop calling the PMNS route unique

The current perturbative note explicitly says:

- no in-chamber basin satisfies the actual log-det convergence condition
  `rho(H_base^{-1} J) < 1`;
- Basin 1 is chosen by the weaker cutoff `||J|| <= ||H_base||`.

That is not yet a theorem-native uniqueness proof. It is a new admissibility
rule.

To close the PMNS lane at publication grade, you need one of:

- a retained theorem deriving the admissibility rule `||J|| <= ||H_base||`
  from accepted atlas inputs on the live source sheet; or
- a different retained discriminator that uniquely selects Basin 1 from the
  exact basin set; or
- a stronger theorem showing Basin 1 satisfies the actual retained response
  criterion while the competitors do not.

If none of those is available, then the PMNS note must be demoted from
"unique closure" to a narrower statement such as:

- explicit PMNS-as-`f(H)` map on the chamber;
- exact observational pinning **given** the added scale cutoff;
- conditional support route, not final flagship closure.

### 4. Surface the charged-lepton conditions honestly in every closure claim

Right now the load-bearing charged-lepton conditions are:

- `q_H = 0` on the trichotomy route: **CONDITIONAL**
- `sigma_hier = (2,1,0)`: **OBSERVATIONAL**
- `theta_23` upper octant: **CONDITIONAL / falsifiable**

Any note that says "flagship gate closed" or "selector closed" must include all
of those conditions if they remain unproved.

Minimum acceptable wording if you do **not** derive them:

- closure via the observational PMNS route,
- conditional on `q_H = 0`,
- conditional on the observational hierarchy pairing `sigma_hier = (2,1,0)`,
- conditional on `theta_23` upper octant / threshold.

If you want the stronger headline, then derive those conditions or reduce them
to already-retained equivalences.

### 5. Fix the package wording before asking for merge

Until items 2 through 4 are resolved, the package/front-door surfaces should
not say:

- `flagship gate CLOSED`
- `selector gate closes`
- `publication-grade closure`

Safe fallback wording is:

- strong new obstruction stack plus explicit PMNS observational route;
- PMNS-as-`f(H)` chamber map is built;
- Basin 1 is the preferred conditional candidate under the added scale rule;
- final flagship closure remains open pending a retained baseline premise and a
  retained basin selector.

## Mechanical Cleanup Needed On Resubmission

- update stale links from
  `SELECTOR_PHYSICIST_J_PERTURBATIVE_UNIQUENESS_NOTE_2026-04-17.md`
  to
  `DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md`
  in the PMNS closure note.
- keep package surfaces aligned with whichever claim boundary you choose; do not
  leave the omnibus, PMNS note, and companion tightening note at different
  strength levels.

## Two Acceptable Resubmission Shapes

### Option A: Conservative resubmission

Land only the parts that are already scientifically clean:

- obstruction tour;
- charged-lepton citation-chain cleanup;
- explicit PMNS chamber map as a conditional observational route;
- no flagship-closure claim.

This is the easier path.

### Option B: Strong closure resubmission

Resubmit a real flagship closure only if all of the following are true:

- clean branch off current `main`;
- no unrelated plaquette edits;
- commuting-baseline premise closed or replaced by a retained theorem;
- basin uniqueness closed by a retained discriminator, not a heuristic cutoff;
- charged-lepton / permutation / octant conditions either derived or carried
  explicitly in the headline claim.

## Bottom Line

The branch is close enough that it should not be discarded, but it is **not**
yet ready for merge at the current claim level.

If you want the fastest path to a useful resubmission:

1. rebuild from current `main`;
2. keep only the G1 obstruction stack + PMNS map + citation cleanup;
3. downgrade the closure language unless you can close the Schur premise and
   the basin selector cleanly.
