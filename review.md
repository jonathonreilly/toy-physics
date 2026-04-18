# Review: `claude/cl3-minimality`

## Current Call

This branch is again materially better than the prior round. The new
`native-gauge-family-uniqueness-2026-04-17.md` finally adds the theorem the
previous review asked for: a family-scope uniqueness result, not just a scope
extension or a tightness corollary.

My current disposition is:

- **No** as retained G16 / `d_s = 3` closure
- **Yes** as a strong support-route package if the retained-grade language is
  downgraded accordingly

The branch is now close in the right way. The remaining blocker is no longer
"you have no uniqueness theorem." The remaining blocker is:

- the uniqueness theorem is proved **under the admissibility package
  (A1)-(A5)**,
- and the note's own premise table still classifies load-bearing pieces of that
  package as **comparison-family**, not retained.

So the branch now proves:

> if the native gauge family satisfies (A1)-(A5), then it is forced to be the
> full bivector sector `Lambda^2(R^n)`, and the tightness corollary gives
> `d_s = 3`.

That is valuable. But it is still not the same as:

> the current retained framework stack already proves (A1)-(A5), therefore
> `d_s = 3` is retainedly derived.

## Branch Hygiene

Before any landing discussion, **rebase this branch onto current
`origin/main`**.

At the time of this pass:

- branch is **3 behind / 19 ahead** `origin/main`

So even if the science were accepted at retained bar, this branch is not yet
landable as-is.

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
- `python3 -m py_compile scripts/frontier_native_gauge_family_uniqueness.py`
  passes
- `python3 scripts/frontier_native_gauge_family_uniqueness.py` ends with
  `THEOREM_PASS=26 SUPPORT_PASS=9 FAIL=0`

The issue is not syntax or arithmetic. The issue is the retained status of the
new admissibility package.

## What Improved

Three real improvements are now present:

1. The branch no longer relies only on the old
   `native-gauge-scope-theorem-2026-04-17.md` story.
2. The new family-uniqueness note actually proves a clean mathematical result:
   `(A1)-(A5) -> V_n = Lambda^2(R^n)`.
3. The new runner adds real content beyond the prior round:
   - explicit grade-subset elimination at `n = 3`,
   - direct commutant checks for bivector irreducibility,
   - a cleaner separation between uniqueness and the `spin(n)=su(2)` tightness
     corollary.

That is genuine progress, and the review note should acknowledge it directly.

## Main Blocker

### The new uniqueness theorem still depends on an admissibility package that is not yet retainedly closed

The key theorem now begins with:

- `(A1)` reduction at `n = 3`
- `(A2)` `O(n)` covariance
- `(A3)` commutator closure
- `(A4)` grade-homogeneity / functoriality
- `(A5)` no external selector

Then the proof is:

- `(A4)` gives `V_n = ⊕_{k in S} Lambda^k(R^n)`
- `(A1)` at `n = 3` forces `S = {2}`
- therefore `V_n = Lambda^2(R^n)` for all `n`

That proof is mathematically coherent. The retained-bar problem is that the
note's own premise table explicitly says:

- `A3-A4` are **comparison-family**
- `A2+A5` are treated as retained only in a `"canonical"` reading

So the branch is still not deriving `d_s = 3` from the current retained stack
alone. It is deriving it from:

- current retained `n = 3` native-gauge authority,
- plus a new admissibility package whose most load-bearing step
  (`A4` grade-homogeneity / functoriality) is not yet retainedly closed.

That is the current blocker in one sentence:

> the uniqueness theorem is now real, but it is still conditional on a new
> admissibility layer rather than derived from already-retained framework
> rules.

## Runner Weakness

### The new runner certifies the conditional pipeline, but still not the retained status of that pipeline

The new runner is better than the earlier scope runner, but it still does not
certify the missing retained-grade step.

What it does certify:

- the `n = 3` eta-phase facts,
- the standard Clifford realization across `n`,
- irreducibility/no-proper-subset evidence for the bivector sector,
- the grade-subset elimination at `n = 3`.

What it does **not** certify:

- that `(A2)`, `(A4)`, and `(A5)` are already forced by the current retained
  framework stack,
- or that the present `main` native-gauge authority itself entails the full
  admissibility package.

And the final theorem-certifying pipeline in Part E is still written as a
restatement of the conclusion under `(A1)-(A5)`, rather than an independent
verification that the retained stack itself forces those premises.

So `26/9 PASS` is evidence for the **conditional uniqueness theorem**, not for
the stronger claim that `d_s = 3` is now retainedly closed from existing
framework inputs alone.

## Best Outcome From Here

If the goal is to get this branch to **retained**, the worker should stop
polishing the tightness corollary and instead close the status of the
admissibility package itself.

Specifically:

1. Prove that `A4` grade-homogeneity / functoriality is a retained
   framework-native rule, not just a natural comparison-family axiom.
2. Prove that `A2` covariance and `A5` no-selector are retained framework
   primitives at family scope, not only a canonical reading of the `n = 3`
   case.
3. Make the runner certify those points directly, instead of only certifying
   the downstream uniqueness once `(A1)-(A5)` are granted.

That is the actual remaining science.

If the worker cannot do that yet, the honest landing is:

- keep the new uniqueness theorem,
- mark it as a **support-route / comparison-family conditional theorem**,
- and do **not** present the downstream `d_s = 3` notes as retained closure.

## Bottom Line

This branch now contains a real and useful theorem that the earlier rounds did
not have. But it is still not retained `d_s = 3` closure, because the
load-bearing admissibility package is not yet itself retainedly derived.

So my current recommendation is:

- **do not land as retained closure**
- **do keep this as the strongest support-route version so far**
- **upgrade only after the admissibility package is itself closed at retained
  bar**
