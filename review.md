# Review: `claude/cl3-minimality`

## Current Call

This branch is materially better again. The new
`admissibility-closure-from-graph-eta-taste-2026-04-17.md` note is
exactly the kind of science push the prior review asked for: it targets
`A2`, `A4`, and `A5` directly rather than polishing another downstream
corollary.

My current disposition is:

- **No** as retained G16 / `d_s = 3` closure
- **Still yes** as a strong support-route packet

The blocker has changed shape. It is no longer:

> you never tried to close `A2 / A4 / A5`.

It is now:

> the branch closes `A2 / A4 / A5` only **after promoting the family-scope
> extension recipe itself (`Recipe-R`) to a retained rule**, and that is still
> the very thing that is not yet proved from the current retained stack.

## Branch Hygiene

At the time of this pass:

- branch is **0 behind / 25 ahead** `origin/main`

So hygiene is clean. The issue is scientific / evidentiary, not git state.

## Replay Status

- `python3 -m py_compile scripts/frontier_admissibility_closure_from_graph_eta_taste.py scripts/frontier_native_gauge_family_uniqueness.py scripts/frontier_native_su2_tightness.py` passes
- `python3 scripts/frontier_admissibility_closure_from_graph_eta_taste.py` ends with
  `THEOREM_PASS=42 SUPPORT_PASS=39 FAIL=0`
- `python3 scripts/frontier_native_gauge_family_uniqueness.py` ends with
  `THEOREM_PASS=26 SUPPORT_PASS=9 FAIL=0`
- `python3 scripts/frontier_native_su2_tightness.py` ends with
  `THEOREM_PASS=19 SUPPORT_PASS=16 FAIL=0`
- `python3 scripts/frontier_native_gauge_scope.py` still replays cleanly

The branch is not failing computationally.

## What Improved

Three real improvements are now present:

1. There is now a dedicated admissibility-closure note instead of a
   vague “canonical reading” gap.
2. The new runner does direct work on the actual previously-missing
   objects: grade purity, `S = {2}` functoriality, axis-permutation /
   sign-flip covariance, and selector-freeness.
3. The follow-up sections in the uniqueness and tightness notes now try
   to integrate the new closure rather than simply leaving the old
   blocker in place.

That is genuine progress.

## Main Blocker

### The new closure note still assumes the family-scope recipe it needs to derive from retained authority

The load-bearing move of the new note is:

- take the retained `n = 3` construction,
- define the family-scope extension rule

  `Recipe-R: V_n^framework := span { (1/2) Γ_μ Γ_ν : 1 ≤ μ < ν ≤ n }`

- then prove `A2`, `A4`, and `A5` from that definition.

That is mathematically coherent. But it means:

- `A4` is obtained because the generators were **defined** to be
  bivector products,
- `A5` is obtained because the generators were **defined** using only
  the `Γ_k`,
- and the branch's “retained closure” claim now hinges on the statement
  that this family-scope extension rule is itself already retained.

That is exactly the unresolved step.

The branch has therefore moved the blocker from:

- “you have not closed `A2 / A4 / A5`”

to:

- “you have not shown that the current retained framework itself forces
  `Recipe-R`, rather than you choosing `Recipe-R` as the extension rule.”

In one sentence:

> the new note proves consequences of the family-scope bivector recipe,
> but it still does not prove that the retained stack on `main`
> uniquely or natively entails that recipe at arbitrary `n`.

## Runner Boundary

### The new runner certifies definitional consequences of `Recipe-R`, not the retained forcing of `Recipe-R`

The new runner is honest about what it computes, and the computations
are good. But the crucial function is literally:

> `V_n^framework := span { (1/2) Γ_μ Γ_ν : μ < ν }`

From there:

- grade-2 purity is immediate,
- selector-freeness is immediate,
- and the combined closure section declares success under the retained
  extension recipe.

So the runner certifies:

- if you adopt `Recipe-R`, then `A2`, `A4`, `A5` follow.

It does **not** certify:

- that the current retained native-gauge authority on `main`
  already determines `Recipe-R` as the unique family-scope extension.

That makes the new runner evidence for a stronger **support-route
proposal**, not yet for retained closure.

## Internal Package Problem

The branch also now has an internal status mismatch:

- the new admissibility note says the package is retained and that
  `d_s = 3` is retained-grade under `Recipe-R`,
- but the companion uniqueness and tightness notes still label
  themselves support-route / conditional and still say the package does
  **not** yet upgrade `d_s = 3` on `main`.

So even before deciding the science, the CL3 authority surface is not
yet speaking with one voice.

## Best Outcome From Here

If the goal is still to reach **retained** `d_s = 3`, the real next
science is now even narrower than before:

1. Prove that the current retained native-gauge authority itself
   determines `Recipe-R` at family scope, rather than taking it as the
   chosen extension rule.
2. Or prove a genuine uniqueness statement saying that any
   family-scope extension of the retained `n = 3` recipe satisfying the
   framework-native graph / η-phase / taste rules must equal `Recipe-R`.
3. Then make the runner certify that forcing step directly.

If the branch cannot do that yet, the honest landing is:

- keep the admissibility-closure note,
- keep the new runner,
- keep the whole packet explicitly support-route,
- and remove any new retained-grade language tied to `Recipe-R`.

## Bottom Line

This is real progress and the right kind of progress. But it still does
not clear retained `d_s = 3` closure, because the new “closure” is only
after elevating `Recipe-R` itself to a retained family-scope rule.

So my recommendation is:

- **do not clear as retained closure**
- **do clear only as a stronger support-route packet if the statuses are made consistent**
- **do not push more side corollaries until `Recipe-R` itself is forced from retained framework structure**
