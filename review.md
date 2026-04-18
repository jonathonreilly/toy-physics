# Review: `claude/cl3-minimality`

## Verdict

Still reject as retained `d_s = 3` closure at the current tip
`64e7f957`.

The branch has made real progress. The old blocker about `(R3)` being an
explicit added full-rotation premise is materially improved: the new v3
`Recipe-R` forcing note now tries to derive that step from graph `B_n`
symmetry plus `Λ²(R^n)` irreducibility, and the main runners replay cleanly.

But the load-bearing family-scope premise has not disappeared; it has moved to
`(R0)`. The retained-grade claim still depends on a definitional "retained
family-scope lift" assumption that is doing the critical work of turning the
retained `n = 3` fact into a statement about all `n`.

## Replay

Representative CL3 runners replay cleanly:

- `frontier_recipe_r_forcing_from_retained_n3.py`
  → `THEOREM_PASS=97 SUPPORT_PASS=21 FAIL=0`
- `frontier_native_gauge_family_uniqueness.py`
  → `THEOREM_PASS=26 SUPPORT_PASS=9 FAIL=0`
- `frontier_native_su2_tightness.py`
  → `THEOREM_PASS=19 SUPPORT_PASS=16 FAIL=0`

So this is not a runtime rejection.

## Main Blocker

### `(R0)` is still an added family-scope lift condition, and it is now load-bearing

The updated forcing theorem now says:

- `(R1)+(R2)` give `V_n ⊆ Λ²(R^n)`;
- `(R0)` gives `V_n` `B_n`-invariance;
- `Λ²(R^n)` is `B_n`-irreducible;
- retained `V_3 = Λ²(R^3)` plus the "uniform recipe" from `(R0)` give
  `V_n ≠ 0`;
- therefore `V_n = Λ²(R^n)` and `(R3)` follows.

That is mathematically coherent, but it is still not "retained `n = 3`
authority alone forces Recipe-R." The critical family step is still being
supplied by `(R0)`:

- `(R0)` is explicitly introduced as a **definitional** retained-lift
  condition;
- it is then used to infer both `B_n`-invariance and nontriviality across the
  whole family;
- those two inferences are exactly what make the irreducibility argument go
  through.

So the branch no longer needs an added `(R3)` premise, but it still needs an
added family-scope lift premise. That keeps this at support-route / retained-
lift science rather than retained closure from the current `main` authority
surface alone.

## Runner Boundary

### The runner still narrates the decisive `(R0)` step instead of certifying it

The new runner genuinely certifies:

- the retained `n = 3` bivector / rotation-on-`Γ` facts,
- the Clifford grade-preservation lemma,
- the center quotient,
- the `B_n` orbit spanning of `Λ²(R^n)`,
- and the `so(n)` adjoint-image dimension.

But the final family-forcing step is still asserted rather than audited:

- it states `V_n B_n-invariant [R0 + H1]`,
- it states `V_3 = Λ²(R^3) retained, uniform recipe => V_n != 0`,
- and then the final `(H-conclusion)` check is hard-coded as `True`.

So the runner still does not computationally certify the exact step that turns
the retained `n = 3` data into a nonzero, selector-free family object at each
`n`. It certifies the surrounding algebra, then narrates the decisive
family-lift consequence.

## Remaining Status Mismatch

The downstream CL3 surfaces still do not speak with one voice.

- The forcing / uniqueness / tightness notes now headline the chain as
  retained-grade.
- But `frontier_native_su2_tightness.py` still explicitly labels Steps 1–4 as
  "conditional support-route theorem content" and still prints
  "does not yet change the retained axiom table on main."

That is still a live contradiction between the reviewer-facing note surface and
the runner-level status surface.

## Practical Call

This branch is better than the last CL3 pass, but it still does not clear as
retained closure.

The honest current reading is:

- **No** as retained `d_s = 3` closure on `main`
- **Yes** as stronger support-route / retained-lift science, if the status
  surfaces are downgraded back into alignment

## Best Next Step

If the goal remains retained closure, there is now one narrow science task left:

1. derive the family-scope lift condition `(R0)` itself from the retained
   `n = 3` authority plus axioms, instead of defining it as what a "retained
   family-scope lift" means

If that cannot be done yet, the correct landing is still:

1. keep the new forcing theorem and runner as stronger support-route science,
2. remove the retained-grade upgrade language from the uniqueness / tightness
   surfaces, and
3. stop pushing downstream CL3 corollaries until `(R0)` is genuinely forced.
