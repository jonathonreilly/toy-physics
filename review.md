# Review: `claude/cl3-minimality`

## Current Call

This branch is now in materially better shape than the earlier CL3 submissions.

Current disposition:

- **not retained G16 closure**
- **yes as a conditional/support note on the retained cubic surface**
- **the latest remote tip is scientifically fine at that support-note bar**

So the best current outcome is:

- land this as a **conditional minimality / consistency support note**
- do **not** present it as first-principles closure of `d_s = 3`

## Replay Status

- `python3 -m py_compile scripts/frontier_cl3_minimality.py` passes
- `python3 scripts/frontier_cl3_minimality.py` ends with
  `THEOREM_PASS=50 SUPPORT_PASS=32 FAIL=0`

The new remote tip `b150c644` is a small runner-docstring alignment commit on top
of the substantive v4 theorem work. The branch replays cleanly.

## What Is Now In Good Shape

The main issues from the earlier reviews have been addressed at the support-note
level:

1. the note no longer overclaims axiom-depth closure
2. the matrix-level `Cl(3; C) = M_2(C) ⊕ M_2(C)` / `Cl^+(3) ≅ M_2(C)` runner
   story is explicit
3. the `spin(n)` / `so(n)` language is corrected
4. the stale runner-summary mismatch is gone
5. the four-generation section is no longer just residual counting plus an
   `n = 3` citation; it now gives an actual family-wide algebra construction on
   the scoped cubic odd-`n` comparison family

In particular, the present Part F does more than the earlier branch:

- the `n` translation operators produce `n` distinct joint sign patterns on the
  `hw=1` sector
- those patterns give rank-1 projectors `P_i`
- the cyclic axis-permutation operator supplies the needed off-diagonal moves
- `P_i C^k P_j` generates the full matrix-unit basis
- the resulting algebra is `M_n(C)`, hence irreducible

At the scope actually claimed in the note, that is a coherent support-level
four-generation no-go on the cubic odd-`n` comparison family.

## One Remaining Cleanup

I do not see a new scientific blocker on the latest remote tip, but there is
still one wording cleanup that would make the claim boundary tighter.

### The four-generation theorem is not literally “comparison-level-only”

The note still says:

> the four-generation exclusion below is comparison-level-only

But the same note also says, correctly, that the theorem is being read on the
cubic `Cl(n)/Z^n` family **with the retained `hw`-orbit-is-physical-species
semantics**.

That means the clean wording is:

- comparison-family theorem
- under the retained `hw`-orbit semantics

not a completely semantics-free comparison theorem.

This is **not** a scientific blocker at the support-note bar, because the scope
section already says the right thing. It is just worth aligning the dependency
table prose with the actual scope statement so reviewers do not think you are
claiming more abstraction-independence than you really are.

## Best Outcome From Here

### Best immediate outcome

Land this as a **support / consistency note**.

That gives you:

- an honest answer to “why `Cl(3)` rather than nearby `Cl(n)` options?”
- a concrete matrix-level Clifford verification
- a scoped four-generation incompatibility theorem on the cubic odd-`n`
  comparison family
- no false claim that the framework has solved the axiom-depth `d_s = 3`
  question

### Best small edit before landing

Change the “comparison-level-only” sentence to something like:

> The four-generation exclusion below is a comparison-family theorem on the
> cubic odd-`n` surface, read under the retained `hw`-orbit-is-physical-species
> semantics.

That would make the boundary language match the theorem’s actual scope.

### Best long-term outcome

If you later want true retained closure of G16, that is still a separate
program:

1. derive `n = 3` non-circularly
2. do not rely on the retained cubic `8 = 1 + 1 + 3 + 3` surface as the
   selector

This branch is not trying to do that anymore, which is the right call.

## Bottom Line

My current call:

- **No** as retained G16 closure
- **Yes** as a conditional/support note
- **Recommended action:** land it at that support-note status, with one small
  claim-boundary wording cleanup if you want the cleanest reviewer-facing
  surface
