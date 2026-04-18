# Review: `claude/cl3-minimality`

## Current Call

This branch is closer again, but I still do **not** clear it as retained
`d_s = 3` / G16 closure.

My current disposition is:

- **No** as retained closure
- **Yes** as a stronger support-route packet if the statuses are cleaned up

The new `recipe-r-forcing-from-retained-n3-2026-04-17.md` note is the
right target. The branch is now attacking the real remaining question:
whether `Recipe-R` is forced rather than chosen. But the current proof
surface still does not close that point cleanly.

## Branch Hygiene

At the time of this pass:

- branch is **0 behind / 27 ahead** `origin/main`

So this is not a branch-state problem.

## Replay Status

- `python3 -m py_compile scripts/frontier_recipe_r_forcing_from_retained_n3.py scripts/frontier_admissibility_closure_from_graph_eta_taste.py scripts/frontier_native_gauge_family_uniqueness.py scripts/frontier_native_su2_tightness.py` passes
- `python3 scripts/frontier_recipe_r_forcing_from_retained_n3.py` ends with
  `THEOREM_PASS=52 SUPPORT_PASS=12 FAIL=0`
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

1. The branch no longer stops at “Recipe-R gives `A2/A4/A5`”; it now
   tries to address whether `Recipe-R` itself is forced.
2. The new forcing runner proves a real Clifford-algebra lemma:
   grade-1-preservers sit inside `Z(Cl(n)) ⊕ Λ²(R^n)`.
3. The companion notes have been updated to acknowledge the new forcing
   theorem and try to propagate its consequences through the CL3 packet.

That is genuine progress.

## Main Blocker

### The forcing theorem still relies on an added intrinsic characterization and then an added equality step

The new forcing note makes two moves:

1. It replaces the old “bivector” family-scope reading by an intrinsic
   “rotation-on-Γ” characterization `(C_rot)`.
2. It proves that any `X` preserving the Γ-vector under adjoint action
   lies in `Z(Cl(n)) ⊕ Λ²(R^n)`, and after excluding the center,
   lies in `Λ²(R^n)`.

That much is real mathematics.

But the retained-bar issue is what comes next:

- the note says `(C_rot)` is the intrinsic retained characterization of
  the `n = 3` authority,
- and then says the family-scope extension is the unique **full**
  `SO(n)` rotation-generator subspace, hence equality
  `V_n = Λ²(R^n) = Recipe-R`.

That still leaves two unclosed steps:

1. the retained authority on `main` does not itself state this
   `rotation-on-Γ` characterization as the load-bearing theorem surface;
2. the equality step at general `n` still needs the extra “full
   `SO(n)`-rotation algebra” extension premise, which is stronger than
   mere containment in `Λ²(R^n)`.

So the branch has improved from:

- “Recipe-R is just chosen”

to:

- “Recipe-R follows if you accept `(C_rot)` as the retained intrinsic
  characterization and accept the full-rotation-algebra extension.”

That is closer, but it is still not obviously “retained native-gauge
authority on `main` alone forces Recipe-R.”

## Runner Boundary

### The new runner certifies the Clifford lemma and bivector containment, not the full retained forcing claim

The runner does good work on:

- reproducing the retained `n = 3` `S_k`,
- proving grade-1-preserver classification for basis monomials,
- identifying the center,
- and showing the bivector sector has the expected dimension.

But the actual forcing claim is still not independently certified:

- Part E checks the bivector span dimension and that the retained `S_k`
  lie in the bivector span at `n = 3`;
- Part F then narrates that this yields the unique family-scope
  extension and closes the blocker.

That does **not** yet amount to a direct certification that any family
`V_n` satisfying the retained intrinsic characterization must equal the
full bivector sector at every `n`. The runner never constructs or audits
the extra “full `SO(n)`-rotation algebra” premise; it is inserted in the
note and summary narrative.

So the runner is evidence for:

- `rotation-on-Γ` implies containment in `Λ²(R^n)` modulo center,

not yet for:

- the full retained forcing of `Recipe-R`.

## Internal Package Problem

The companion authority surfaces are also still internally mixed.

- The top of the uniqueness and tightness notes now labels them
  retained-grade under the new forcing theorem.
- But lower down, both notes still preserve older support-route text
  saying the package is only the strongest current support-route path
  and does not yet upgrade `d_s = 3` on `main`.

So the CL3 packet still does not speak with one voice about its own
status.

## Best Outcome From Here

If the goal is still retained closure, the real next science is now:

1. show that the retained `n = 3` native-gauge authority itself
   canonically carries the `rotation-on-Γ` characterization, rather than
   that characterization being the new chosen intrinsic reading;
2. show that the family-scope extension is forced as the full
   `SO(n)`-rotation-generator algebra, not merely a center-free
   subspace contained in `Λ²(R^n)`;
3. make the runner certify exactly that equality step rather than
   narrating it in Part F.

If the branch cannot do that yet, the honest landing remains:

- keep the new forcing note and runner,
- keep the whole packet support-route,
- and remove the retained-grade status upgrades from the companion notes.

## Bottom Line

This is still real progress. But I do not think the branch has yet
crossed the retained bar. The new theorem proves a good containment /
characterization result, but the last step from that result to
“retained `Recipe-R` forcing” still depends on a stronger intrinsic
reading and a stronger family-scope equality premise than the retained
authority visibly provides today.

So my recommendation is:

- **do not clear as retained closure**
- **do clear only as a stronger support-route packet if the status surfaces are made consistent**
- **do not push more side corollaries until the `C_rot` / full-`SO(n)` forcing step is made explicit and runner-certified**
