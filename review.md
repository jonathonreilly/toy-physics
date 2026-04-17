# Review: `claude/charged-lepton-closure-review`

## Current Call

This branch is much closer than the previous charged-lepton pass.

Current disposition:

- the original four blockers are **mostly fixed**
- the branch is **not yet ready to land as written**
- the remaining issues are now about **internal convergence and package-surface consistency**, not the original math holes

So the best current outcome is:

- one short cleanup pass
- then likely re-review for landing at its intended review-facing / bounded package status

## Replay Status

- `python3 -m py_compile scripts/frontier_charged_lepton_observational_pin_closure.py` passes
- I could not independently replay the full charged-lepton observational-pin runner in this desktop Python because `sympy` is not installed in the default local environment here

The review below is therefore based on direct inspection of the pushed branch
content plus consistency checks across the authority note, runner, and package
truth surfaces.

## What Is Fixed

Relative to the previous pass, the branch did make the expected substantive
improvements:

1. the disjointness note now states trivial intersection / direct-sum structure,
   not orthogonality
2. the observational-pin runner now contains a real uniqueness test structure
   rather than hardcoded `True`
3. the mass-vs-mass-squared convention choice is surfaced explicitly in the
   authority note and in the runner
4. the charged-lepton package is now wired into the missing publication/package
   surfaces

Those are real fixes. The branch is now blocked by a smaller set of
consistency issues.

## Remaining Blockers

### 1. The branch still has two different uniqueness stories

**Problem**

The new runner Step 3 now claims a stronger result than the authority/package
surfaces.

The runner says, in substance:

- only the identity permutation is consistent with the retained `Γ_1` hopping
  structure
- the pin is therefore unique as a labeled bijection up to positive scale

But the authority note still states the weaker claim:

- the triple is unique **as a set** up to scale
- a residual `S_2` labeling ambiguity on `w_a ↔ w_b` persists on the retained
  surface

And the package truth surfaces still repeat that weaker theorem-level story.

So the branch has not actually converged on one stable claim:

- either the retained structure still leaves an `S_2` ambiguity
- or the new runner proves that ambiguity is gone

At the moment, both stories are present at once.

**Why it matters**

This is the main remaining blocker because uniqueness is load-bearing for how
the closure class is being summarized. A reviewer should not have to infer
whether the package is claiming:

- "unique up to scale and `S_2` relabeling"

or

- "fully labeled unique up to scale"

from conflicting surfaces.

**What would clear this**

Pick one of the two paths and make every surface match it:

#### Path A: Keep the weaker theorem-level claim

This is the safer route unless there is a real retained argument eliminating the
`w_a ↔ w_b` ambiguity.

Required changes:

- keep Theorem 7 exactly at the current weaker statement:
  - unique as a set up to scale
  - residual `S_2` labeling ambiguity remains
- downgrade the runner/review prose that now says the retained `Γ_1` hopping
  map picks out the full labeled identity permutation
- explain that the runner’s permutation test is an observational labeling
  check, not a retained proof that the symmetry is gone

#### Path B: Upgrade the theorem/package surfaces to labeled uniqueness

If the worker believes the stronger claim is actually correct, then they must:

- prove that the retained `Γ_1` hopping data really breaks the surviving
  `w_a ↔ w_b` ambiguity at the theorem level
- update Theorem 7, `PUBLICATION_MATRIX`, and the package summaries to the
  stronger labeled-uniqueness statement

Right now the branch does neither cleanly.

### 2. The runner-count / package-count story is stale and inconsistent

**Problem**

The branch’s response text says the revised charged-lepton campaign is now:

- `518 PASS / 0 FAIL`

after the new uniqueness and convention-cross-check subclaims were added.

But the actual pushed authority/package surfaces still advertise the older
totals:

- [docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  says `511 PASS / 0 FAIL`
- [docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md](docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md)
  still says `511 PASS / 0 FAIL`
- the package summaries use `511+ PASS` language rather than the new specific
  branch total

So the branch still has two verification stories:

- the response/review thread says `518`
- the authority/package surfaces still say `511`

**Why it matters**

This is not a deep science blocker, but it weakens reviewer trust immediately.
Once a branch claims a new verification total, every truth surface needs to
either:

- adopt that number

or

- avoid a specific total and state the verification more conservatively

**What would clear this**

Choose one clean package story and propagate it everywhere:

- if the new official count is `518 PASS / 0 FAIL`, update the review note,
  authority note, and package truth surfaces to that exact value
- otherwise, keep the more conservative wording everywhere and stop claiming
  `518` in the response thread

## Best Outcome From Here

### Best immediate outcome

Land this after one short consistency pass.

The branch no longer looks scientifically broken at first pass. It now looks
like a package that has:

- mostly fixed the original issues
- but not yet converged on one uniqueness claim
- and not yet propagated one verification count

### Best short edit

I would do these two edits before resubmission:

1. decide whether Theorem 7 is:
   - unique as a set up to scale with residual `S_2` ambiguity
   - or fully labeled unique up to scale
2. make the runner, authority note, `PUBLICATION_MATRIX`, and package summaries
   all tell the same story
3. choose either `511` or `518` as the official current runner-stack total and
   propagate it consistently

## Bottom Line

My current call:

- **No** as currently written
- **Close** after a short cleanup pass
- remaining blockers:
  - uniqueness story not converged
  - verification totals not converged
