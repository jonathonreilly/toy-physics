# Review: `claude/cl3-minimality`

## Current Call

This branch still does **not** clear as retained `d_s = 3` / G16 closure.

My current disposition is:

- **No** as retained closure
- **Yes** as a stronger support-route packet if the status surfaces are
  downgraded back into alignment

The branch has made real progress. The new `Recipe-R forcing v2` work is
materially better than the prior pass. But it still does not show that the
retained authority on `main` itself forces the family-scope extension
`Recipe-R`; it shows that `Recipe-R` follows once an extra family-scope
full-rotation-algebra reading is imposed.

## Branch Hygiene

At the time of this pass:

- branch is **12 behind / 29 ahead** `origin/main`

That is not the main blocker here, but the branch is no longer in a clean
rebase state.

## Replay Status

- `python3 -m py_compile scripts/frontier_recipe_r_forcing_from_retained_n3.py scripts/frontier_admissibility_closure_from_graph_eta_taste.py scripts/frontier_native_gauge_family_uniqueness.py scripts/frontier_native_su2_tightness.py` passes
- `python3 scripts/frontier_recipe_r_forcing_from_retained_n3.py` ends with
  `THEOREM_PASS=72 SUPPORT_PASS=16 FAIL=0`
- `python3 scripts/frontier_native_gauge_family_uniqueness.py` still ends with:
  `It does not, by itself, upgrade d_s = 3 from axiom to retained theorem on main.`
- `python3 scripts/frontier_native_su2_tightness.py` still ends with:
  `It is the strongest current support-route derivation of n = 3, not yet a retained replacement for the d_s = 3 primitive on main.`

So the rejection is not a runtime one.

## What Improved

Three real improvements are now present:

1. The new forcing note now states the equality step explicitly and no longer
   stops at mere containment in `Λ²(R^n)`.
2. The forcing runner was extended in a real way: it now certifies the
   Clifford-grade lemma, the center quotient, and the bivector-to-`so(n)`
   adjoint image dimension.
3. The old “top says retained, body says support-route” inconsistency in the
   family-uniqueness note is narrower than before.

That is genuine progress.

## Main Blocker

### The last forcing step still comes from an added family-scope `R3` premise

The new forcing note proves a real theorem up to the following point:

- `(R2)` rotation-on-`Γ` gives
  `V_n ⊆ Z(Cl(n)) ⊕ Λ²(R^n)`
- `(R1)` center-freeness gives
  `V_n ⊆ Λ²(R^n)`

That part is solid.

The remaining equality

`V_n = Λ²(R^n) = Recipe-R`

is then obtained by adding

- `(R3)` full rotation algebra: `ad(V_n) = so(n)`

and the note explicitly says that at family scope this is

> the natural requirement that the native gauge generator space realize all
> infinitesimal `SO(n)` rotations of the `Γ`-vector — this is what "native
> gauge" means.

That is still the load-bearing gap. The retained authority on `main`
(`docs/NATIVE_GAUGE_CLOSURE_NOTE.md`) proves exact native cubic `SU(2)` at
`n = 3`; it does **not** itself state that every family-scope native-gauge
extension must realize the full `SO(n)` rotation algebra on the `Γ`-vector.

So the current branch has improved from:

- “Recipe-R is chosen”

to:

- “Recipe-R is forced if the family-scope extension is required to realize the
  full `SO(n)` rotation algebra.”

That is better, but it is still not “retained authority on `main` alone forces
Recipe-R.”

## Runner Boundary

### The runner still narrates the forcing claim more strongly than it certifies it

The runner now does certify:

- the monomial classification,
- the center structure,
- the center-free containment in bivectors,
- and the fact that bivectors realize full `so(n)`.

But its own internal logic still shows the open point:

- Part E says `(U1)`–`(U3)` already force `Recipe-R`
- Part F says Parts B–E close the follow-up blocker
- Part G then says equality actually required the extra strengthened premise
  `(R3)` and certifies that stronger theorem instead

So the runner now certifies:

- `Recipe-R` under `(R1)+(R2)+(R3)`

not:

- `Recipe-R` from the retained stack alone

That is the right support-route science result. It is still not a retained
forcing result.

## Remaining Surface Mismatch

The downstream CL3 authority surfaces still outrun the actual certified status.

- The top of the uniqueness and tightness notes now treats the CL3 packet as
  retained-grade under the new forcing theorem.
- But the companion runners still end by saying the family-uniqueness /
  tightness route is the strongest current conditional or support-route path,
  not yet a retained replacement on `main`.

So the package still does not speak with one voice about its own status. The
science and the scripts are now closer than before, but the note surfaces are
still one step stronger than the certified result.

## Best Outcome From Here

If the goal is retained closure, there is now only one worthwhile science push:

1. derive the family-scope full-rotation-algebra premise itself from the
   retained native-gauge authority, instead of defining it as what “native
   gauge” means at arbitrary `n`

If the branch cannot do that yet, the honest landing remains:

1. keep the new forcing note and runner
2. keep the CL3 packet support-route / comparison-family
3. remove the retained-grade upgrades from the uniqueness / tightness
   authority surfaces

## Bottom Line

The branch is meaningfully better than the last pass. But the remaining blocker
is still real and now very narrow:

- **Recipe-R is not yet retained-forced from the current `main` authority**
- it is forced only after adding the family-scope full-`SO(n)` premise

So my recommendation remains:

- **do not clear as retained closure**
- **do clear as a stronger support-route packet after status cleanup**
- **do not spend more time pushing downstream CL3 corollaries unless the next work directly derives the family-scope `R3` forcing step**
