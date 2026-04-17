# Review: `claude/cl3-minimality`

## Current Call

This branch is materially stronger than the prior `native-su2-tightness`
submission because it now adds a separate
`native-gauge-scope-theorem-2026-04-17.md` instead of trying to get retained
closure by re-reading the tightness note alone.

My current disposition is:

- **No** as retained G16 / `d_s = 3` closure
- **Yes** as a support-note package, including the new native-gauge route, if
  the retained-grade overclaim is downgraded and the branch is rebased onto
  current `main`

So the branch is **still not ready to land as retained closure**, but it now
contains a cleaner and more useful support-level route than the previous round.

## Branch Hygiene

Before any resubmission, **rebase this branch onto the latest `origin/main`**.

At the time of this pass:

- merge-base with `origin/main`: `0e166f090a6bf56efaa2e0ad01c7f23fe142cd00`
- branch is **15 behind / 17 ahead**

So even if the science claims were acceptable, this branch is not landable
as-is. It needs a clean replay on top of the current package surface before any
merge discussion.

## Replay Status

- `python3 -m py_compile scripts/frontier_cl3_minimality.py` passes
- `python3 scripts/frontier_cl3_minimality.py` ends with
  `THEOREM_PASS=50 SUPPORT_PASS=32 FAIL=0`
- `python3 -m py_compile scripts/frontier_native_su2_tightness.py` passes
- `python3 scripts/frontier_native_su2_tightness.py` ends with
  `THEOREM_PASS=19 SUPPORT_PASS=16 FAIL=0`
- `python3 -m py_compile scripts/frontier_native_gauge_scope.py` passes
- `python3 scripts/frontier_native_gauge_scope.py` ends with
  `THEOREM_PASS=23 SUPPORT_PASS=22 FAIL=0`
- `python3 -m py_compile scripts/frontier_tetragonal_stabilizer_mu_tau_invariance.py`
  passes
- `python3 scripts/frontier_tetragonal_stabilizer_mu_tau_invariance.py` ends
  with `THEOREM_PASS=18 SUPPORT_PASS=8 FAIL=0`

The issue is not syntax or arithmetic. The issue is still the retained status
of the new premise being introduced.

## Current Findings

### 1. The scope theorem still upgrades an `n = 3` retained code fact into a new arbitrary-`n` framework principle

The new scope note is a better decomposition than the previous branch, but it
still does not close the retained-bar blocker.

What the current retained authority on `main`
`docs/NATIVE_GAUGE_CLOSURE_NOTE.md` actually establishes is:

- on the cubic `Z^3` surface
- `Cl(3)` in taste space
- `Cl(3)` **contains** an `su(2)` subalgebra

The new scope theorem then takes the literally correct `n = 3` code fact

- the retained `S_k` are exactly the three `Cl(3)` bivectors up to
  normalization

and promotes it to the stronger comparison-family statement

- for arbitrary `n`
- the weak generators are all bivectors
- with no selector
- therefore the family Lie algebra is `spin(n)`

That stronger family statement is still not a retained consequence of the
present framework stack. It is a new comparison-family extension principle
built from:

- the retained `n = 3` construction fact
- standard chiral-matrix / Clifford extension machinery

That is why the branch is still below retained bar.

### 2. The scope runner still certifies the consequences of the chosen arbitrary-`n` recipe, not that the retained authority forces it

`scripts/frontier_native_gauge_scope.py` now does one genuinely valuable thing
in Part A:

- it proves that the retained `n = 3` `S_k` operators are exactly the three
  `Cl(3)` bivectors up to normalization

But after that, Parts B and C:

- build `Cl(n)` for general `n` with the standard chiral-matrix recipe
- enumerate all bivectors
- define the native gauge recipe at family scope as “all bivectors”
- then verify the downstream selector-free counting and Lie-algebra
  consequences

So the runner certifies:

- `retained n=3 code fact` + `standard arbitrary-n extension recipe`
  -> selector-free `spin(n)` family

It does **not** certify:

- `current retained native-gauge theorem itself`
  -> selector-free `spin(n)` family

That is still the unresolved retained-grade gap.

### 3. The tightness note still overstates `d_s = 3` as retainedly derived because it treats the unresolved scope theorem as already retained

The tightness note is cleaner than the earlier branch and the separation into:

- scope theorem
- tightness theorem

is the right architecture.

But it still says the blocker is solved and that `d_s = 3` is derived from a
"newly-retained" native-gauge scope theorem. Since the companion scope theorem
is not yet retained-grade, this downstream note is still support-level rather
than retained closure.

So the right status is still:

- **No** as retained `d_s = 3` closure
- **Yes** as a stronger support route, if the retained-grade language is
  downgraded

## Main Blocker

### The new scope theorem still upgrades an `n = 3` retained construction fact into an arbitrary-`n` framework principle

The new scope theorem fixes the previous branch’s weakest point in one real
sense: it no longer says

> the old retained theorem can simply be re-read as `spin(n) = su(2)`

Instead it now tries to prove a separate theorem:

> the retained native-gauge construction is literally the recipe
> “gauge generators := Clifford bivectors of `Cl(n)`”, selector-free, at
> comparison-family scope

That is a better decomposition. But it is still **not yet retained closure**.

What the current retained authority
`docs/NATIVE_GAUGE_CLOSURE_NOTE.md` actually establishes is:

- on the cubic `Z^3` surface
- `Cl(3)` in taste space
- exact native `SU(2)` generated by the three operators implemented there

The new scope theorem then observes, correctly, that at `n = 3` those three
operators are literally the three `Cl(3)` bivectors. From there it imports the
standard staggered-phase / chiral-matrix construction of `Cl(n)` on `Z^n` and
promotes the recipe to:

- for arbitrary `n`,
- native gauge generators are **all** bivectors,
- with no selector,
- therefore the comparison-family Lie algebra is `spin(n)`

That is mathematically natural, but it is still a **new comparison-family
extension principle**. It is not something the current retained native-gauge
authority already proves by itself.

So the branch has moved from:

- “reinterpret the retained `n=3` theorem more strongly”

to:

- “add a new theorem that extends the retained `n=3` construction to an
  arbitrary-`n` family using standard Clifford/lattice machinery”

That is an improvement, but it is still a premise upgrade. The new scope
theorem is not yet a retained consequence of the present framework stack; it is
a proposed stronger theorem built from standard comparison-family inputs plus
the retained `n=3` code fact.

## Runner Weakness

### The new scope runner certifies the consequences of the arbitrary-`n` recipe after adopting it

`scripts/frontier_native_gauge_scope.py` is cleaner than the previous runner.
In particular, its Part A does genuinely certify the important local fact:

- at `n = 3`, the retained `S_k` operators are exactly the three Clifford
  bivectors up to normalization

That is useful and should stay.

But the runner’s family-wide claim is still not independently certified.
After Part A, it:

- builds `Cl(n)` for general `n` using the standard chiral-matrix recipe
- enumerates all bivectors
- declares that “the native gauge generators per recipe `R` are all bivectors”
- then verifies the downstream selector-free counting and Lie-algebra
  consequences

So `23 THEOREM / 22 SUPPORT / 0 FAIL` is evidence for:

- the algebra and counting **if** one accepts recipe `R` at comparison-family
  scope

It is **not** evidence that the existing retained native-gauge theorem itself
forces recipe `R` beyond the `n = 3` surface.

In other words, the runner now certifies:

- `retained n=3 code fact` + `standard arbitrary-n extension recipe`
  -> selector-free `spin(n)` family

It does **not** certify:

- `current retained framework stack alone`
  -> selector-free `spin(n)` family

That gap is exactly why the branch is still below retained bar.

## What Improved

The branch did fix the previous review’s exact complaint.

- The old blocker was: the tightness theorem was overclaiming by re-reading the
  retained native-SU(2) theorem.
- The new branch now separates that into:
  - a scope theorem
  - a tightness theorem that depends on the scope theorem

That is the right architecture.

So this review should not be read as “nothing changed.” Something important did
change. The remaining problem is simply that the new scope theorem is still not
yet retained-grade at the stronger arbitrary-`n` scope it claims.

## Best Outcome From Here

### Best immediate outcome

Do **not** land this as retained `d_s = 3` closure.

Instead:

1. keep `cl3-minimality-conditional-support-2026-04-17.md` as the canonical
   CL3 support note
2. keep the new native-gauge scope + tightness package as a stronger
   support-grade route to `d_s = 3`
3. state explicitly that the family-wide selector-free recipe is still a new
   comparison-family theorem, not yet retained framework authority

That yields an honest and scientifically useful support package. Again: do this
only after rebasing onto the current `main`.

### What would actually get this to retained

To convert this into real retained closure, the branch needs the new scope
theorem itself to be accepted as retained framework authority rather than as a
standard-family extension proposal.

Concretely, it would need to close something like:

> The framework’s native weak-gauge closure principle is itself
> comparison-family-scoped and canonically selector-free, so the full
> Clifford bivector Lie algebra is the weak algebra at arbitrary `n`, not
> merely at the retained cubic `n = 3` implementation surface.

Only once that stronger scope statement is independently retained can the
companion tightness theorem legitimately deliver:

> `spin(n) = su(2)` -> `n(n-1)/2 = 3` -> `n = 3`

as retained closure.

### Concrete science work that would enable the upgrade

If the goal is to **upgrade** this branch to retained rather than downgrade it,
the worker should focus on the following scientific program.

#### 1. Prove a family-scope uniqueness theorem, not just a family-scope extension

Right now the branch shows:

- the retained `n = 3` construction uses the three `Cl(3)` bivectors
- the standard `Cl(n)` machinery lets one extend that recipe to arbitrary `n`

What it still needs to prove is stronger:

> among all comparison-family extensions compatible with the retained native
> gauge construction, the only admissible one is “native gauge generators :=
> the full bivector sector of `Cl(n)`,” with no selector.

That means the worker should write a theorem of the form:

> **Family-scope native-gauge uniqueness theorem.**
> Given the retained graph / staggered / taste construction, together with the
> requirement that the comparison-family closure:
> - reduces to the retained `n = 3` generators,
> - is functorial in `n`,
> - is basis-independent up to Clifford automorphism,
> - is closed under commutator,
> - introduces no external selector field or extra structure,
> then the weak-gauge generator space is uniquely the full bivector space.

That is the theorem that would close the present gap. The current branch only
constructs one natural extension; it does not yet prove that this extension is
forced.

#### 2. Derive the arbitrary-`n` construction from retained framework rules, not from textbook availability alone

The step that still reads as external is:

- "`Cl(n)` exists via the standard chiral-matrix / staggered-phase
  construction, therefore recipe `R` extends"

To get retained status, the worker should prove that the framework’s own
native-gauge construction principle determines that extension.

Concretely:

- start from the same graph-first / η-phase / taste-doubling logic used by the
  retained `n = 3` theorem
- formulate it for `Z^n`
- show that the comparison-family `Γ_k` are fixed up to standard Clifford
  equivalence by that graph construction
- then show that the induced native-gauge sector is the bivector sector

That would convert the arbitrary-`n` step from
"standard family extension we choose to use"
into
"framework-native family theorem."

#### 3. Prove that no proper bivector subset can play the same role without adding extra structure

This is the selector issue in its strongest form.

The worker should prove a no-go statement such as:

> any proper subset of bivectors either
> - fails closure under commutator,
> - breaks comparison-family symmetry / automorphism covariance,
> - fails to reduce canonically to the retained `n = 3` construction,
> - or requires an additional selector not present in the framework inputs.

This is important because it turns “we use all bivectors” from a design choice
into a forced theorem. Without this no-go step, the current recipe remains a
natural choice rather than a uniquely determined consequence.

#### 4. Make the runner certify the uniqueness theorem, not only the chosen recipe

The current scope runner should be upgraded so that it does more than say:

- build `Cl(n)`
- define gauge generators as all bivectors
- verify the consequences

It should instead certify a theorem of the form:

- any admissible comparison-family extension compatible with the retained
  `n = 3` construction, automorphism covariance, closure, and no extra
  selector structure must equal the full bivector sector

That would make the runner evidence for a **forced** family theorem rather than
for one chosen extension recipe.

Instead it should certify the missing theorem-level content. For example:

- verify exact reduction to the retained `n = 3` construction
- verify covariance of the bivector sector under the relevant Clifford / lattice
  symmetry actions
- verify that proper subsets fail one of the admissibility criteria above for
  low `n` test cases
- verify that the full bivector sector is the unique commutator-closed,
  selector-free, comparison-family-covariant candidate under the stated rules

That would make the runner evidence for the actual retained claim, not just for
the algebra after assuming it.

#### 5. Only then rerun the tightness theorem as the short corollary

Once the scope theorem above is really closed, the current tightness note is
basically fine:

- full bivector Lie algebra = `spin(n)`
- observed weak algebra = `su(2)`
- therefore `spin(n) = su(2)`
- hence `n(n-1)/2 = 3`
- hence `n = 3`

So the right order for a true retained upgrade is:

1. retained family-scope native-gauge uniqueness theorem
2. retained tightness theorem as corollary
3. optional connection back to the older cubic support note

### Short version to give the worker

If you want this upgraded to retained, do **not** spend more time polishing the
dimension-counting corollary. The real missing science is:

- prove that the framework itself forces the selector-free family rule
  “weak gauge = full Clifford bivector sector” at arbitrary `n`
- prove that no proper subset / selector-based extension is framework-admissible
- make the runner certify that uniqueness statement directly

## Bottom Line

This branch is worth keeping alive, but not as retained closure yet.

The right next move is:

1. **rebase to the latest `main`**
2. either:
   - downgrade the scope + tightness pair to support-grade and land them as
     support material, or
   - do the additional family-scope uniqueness work above and come back for a
     real retained pass

Until then, the honest call remains:

- **No** as retained G16 / `d_s = 3` closure
- **Yes** as a stronger support-note package

If that theorem is closed, the retained `d_s = 3` upgrade should follow
quickly. Without it, the branch remains a strong support route rather than a
retained closure.

## Bottom Line

My current call:

- **No** as retained G16 / `d_s = 3` closure
- **Yes** as a support-note package, including the new native-gauge route, if
  the retained-grade claim is downgraded

The branch now contains a better future route than before:

- prove the selector-free family scope theorem at retained bar
- then the tightness theorem gives `d_s = 3` immediately

That is a good route. It is just not yet the same thing as a retained proof.
