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

---

## Author response (2026-04-17, revision pass 2)

Both remaining blockers addressed. Summary below.

### Blocker 1 (remaining) — fixed: single uniqueness story (Path A)

Chose **Path A** (the safer route): the retained surface proves set-uniqueness up to positive scale, with a residual `S_2` labeling ambiguity on `w_a ↔ w_b` that is Koide- and Σ-invariant. The labeled identity is an *observational labeling* fact, not a retained-theorem output. This matches what authority note §6.4 explicitly flags: the sole-axiom `S_2`-breaking primitive on `{w_a, w_b}` is a named missing primitive, not a retained theorem.

Runner prose in `scripts/frontier_charged_lepton_observational_pin_closure.py` Step 3 is downgraded accordingly:

- New scope-note docstring at the top of the uniqueness block explicitly states the retained claim is *set-uniqueness up to positive scale*, with the residual `S_2` labeling ambiguity surviving on `{w_a, w_b}` and being invisible in Koide `Q` and the Σ spectrum.
- **U1** is now framed as an *observational labeling consistency* check (species-k → slot-k reproduces the observed triple), not a retained uniqueness claim.
- **U2** is now framed as a *set-vs-labeled distinction* tautology on distinct-valued tuples, with an explicit comment that this does NOT prove the retained `Γ_1` hopping breaks the residual `S_2` on `{w_a, w_b}`. The surviving `(0, 2, 1)` permutation is called out as the `S_2` ambiguity that Koide and Σ are invariant under.
- **U3a / U3b** are unchanged (sharp-pin + scale-freedom).
- **Composite claim** now reads exactly: *"pin is unique as a set up to positive scale; residual `S_2` labeling ambiguity on `w_a ↔ w_b` is Koide- and Σ-invariant"* — matching authority note Theorem 7, §10 paper-safe wording, and §11 "what this note does not claim."

All four truth surfaces (`README`, `DERIVATION_VALIDATION_MAP`, `FULL_CLAIM_LEDGER`, `EXTERNAL_REVIEWER_GUIDE`) and `PUBLICATION_MATRIX` (already consistent) now carry the same set-uniqueness + residual-`S_2` language. Every surface tells one story.

Runner still PASS=39 / FAIL=0 after the downgrade.

### Blocker 2 (remaining) — fixed: unified 518 PASS / 0 FAIL count

Adopted `518 PASS / 0 FAIL` as the official current runner-stack total and propagated everywhere:

- `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` header, §9 dependency contract, §11 runner-manifest intro, runner-manifest row for `frontier_charged_lepton_observational_pin_closure.py` (`32 → 39`), and runner-manifest TOTAL (`511 → 518`).
- `docs/publication/ci3_z3/README.md` — `511+ PASS` → `518 PASS`.
- `docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md` — `511+ PASS` → `518 PASS`.
- `docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md` — `511 PASS` → `518 PASS`.
- `docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md` — `511+ PASS` → `518 PASS`.

Every surface now reports the same `518 PASS / 0 FAIL` total. Response and package surfaces are on one story.

### Re-verification

```
scripts/frontier_charged_lepton_observational_pin_closure.py
   PASS = 39   FAIL = 0
   VERDICT: CHARGED_LEPTON_OBSERVATIONAL_PIN_CLOSES = TRUE
```

Full 19-runner stack on `origin/main` base: `518 PASS / 0 FAIL`, unchanged from revision pass 1 (Path-A downgrade changes prose only; the PASS count is preserved because the tests themselves remain well-defined — just relabeled and tightened to match the authority-note claim).

### What did NOT change

- No retained-authority notes on `main` modified.
- No new axioms, primitives, or theorems introduced.
- Strict-review verdict `TRUE_NO_PREDICTION` preserved.
- Branch name unchanged: `claude/charged-lepton-closure-review`.

### Request

Please re-review. Both remaining blockers (uniqueness story, verification totals) are now resolved on the pushed branch; every surface tells the same story.
