# Universal GR Supermetric Normal Form on `PL S^3 x R`

**Status:** exact support theorem - local supermetric normal form
**Date:** 2026-05-06
**Branch:** `claude/science-fix/universal_gr_supermetric_normal_form_note-9e374e18`
**Role:** direct universal route / post-localization theorem step

## Verdict

The direct universal Hessian is now pinned down more sharply than
"block-localized."

On the exact `SO(3)`-invariant lifted background

`D = diag(a,b,b,b)`,

the route-defined universal Hessian is exactly the inverse-metric contraction
on symmetric `3+1` perturbations.

Equivalently, in the canonical lapse / shift / trace / shear basis, the
Hessian is already the exact local supermetric normal form

`H = -a^-2 P_lapse - (ab)^-1 P_shift - b^-2 P_trace - b^-2 P_shear`.

So the direct universal route is no longer open at the level of local tensor
normal form.

This note does not re-derive the scalar-observable selection premises behind
the log-det generator, and it does not identify the local Hessian with the full
Einstein/Regge dynamics. Its closed claim is the algebraic normal form of the
Hessian once the route's scalar generator and lifted invariant background are
the inputs.

## Local inputs

The local calculation in this note uses these displayed inputs:

- scalar observable generator
  `W[J] = log|det(D+J)| - log|det D|`
- `3+1` lift `PL S^3 x R`
- metric-source Hessian definition
  `B_D(h,k) := D^2 W[0](h,k)`
- canonical lapse / shift / trace / shear frame
- invariant-background Schur localization context

The new step identifies what that localized Hessian actually is:

> it is exactly the inverse-metric supermetric pairing on the invariant
> background.

In other words, the local algebraic tensor form is already fixed.

## Exact formula

For symmetric perturbations `h, k` on the invariant background
`D = diag(a,b,b,b)`, the universal Hessian is

`B(h,k) = -Tr(D^-1 h D^-1 k)`.

That is exactly the inverse-metric contraction pairing.

Here is the derivation, with no substitution step hidden.

For positive `a,b`, the determinant is positive in a neighborhood of
`J=0`, so the local Hessian can be computed from

`W[J] = log det(D+J) - log det D`.

Let

`A(s,t) = D + s h + t k`.

Jacobi's formula gives

`partial_s log det A(s,t) = Tr(A(s,t)^-1 h)`.

Differentiating this expression in the `t` direction and using

`partial_t A^-1 = -A^-1 k A^-1`

gives

`partial_t partial_s log det A(s,t)|_(s=t=0)`
`= -Tr(D^-1 k D^-1 h)`.

By cyclicity of trace,

`-Tr(D^-1 k D^-1 h) = -Tr(D^-1 h D^-1 k)`.

Therefore the universal Hessian defined as the second variation of the route
generator is exactly

`B_D(h,k) = D^2 W[0](h,k) = -Tr(D^-1 h D^-1 k)`.

This is the missing identification: it follows directly from the log-det
generator and the matrix inverse variation identity.

## Canonical block evaluation

Use the Frobenius-orthonormal symmetric basis

- lapse: `e_00`
- shifts: `(e_0i + e_i0)/sqrt(2)`, `i=1,2,3`
- spatial trace: `(e_11 + e_22 + e_33)/sqrt(3)`
- shear: the two diagonal traceless spatial modes plus the three normalized
  spatial off-diagonal modes

with `D^-1 = diag(a^-1,b^-1,b^-1,b^-1)`.

In this basis the previous formula gives:

- lapse: `B(e_00,e_00) = -a^-2`
- each shift: `B((e_0i+e_i0)/sqrt(2), same) = -(ab)^-1`
- spatial trace: `-(1/3)(b^-2+b^-2+b^-2) = -b^-2`
- each shear mode: `-b^-2`

All cross terms vanish. For disjoint matrix entries this is immediate from the
trace contraction. For trace-shear cross terms it is the traceless identity:

`(1/sqrt(3)) * (q_11 + q_22 + q_33) = 0`.

So the Gram matrix in the canonical basis is

`diag(-a^-2, -(ab)^-1, -(ab)^-1, -(ab)^-1, -b^-2, -b^-2, -b^-2, -b^-2, -b^-2, -b^-2)`.

In the canonical symmetric basis, this gives the exact diagonal block
weights:

- lapse: `-a^-2`
- shift: `-(ab)^-1`
- trace: `-b^-2`
- shear: `-b^-2`

with no cross-block leakage.

## Runner evidence

The paired runner is
[`scripts/frontier_universal_gr_supermetric_normal_form.py`](../scripts/frontier_universal_gr_supermetric_normal_form.py).

It now checks the load-bearing step directly:

1. Symbolically differentiates `log det(D+s h+t k)` for general symmetric
   perturbations `h,k` and verifies the exact identity
   `D^2W[0](h,k) = -Tr(D^-1 h D^-1 k)`.
2. Symbolically evaluates the canonical lapse / shift / trace / shear Gram
   matrix and verifies the exact diagonal weights above.
3. Numerically replays the same identity on representative positive
   invariant backgrounds.

The corresponding refreshed output is
[`outputs/frontier_universal_gr_supermetric_normal_form_2026-05-06.txt`](../outputs/frontier_universal_gr_supermetric_normal_form_2026-05-06.txt).

## Re-audit packet

For a restricted re-audit of this note, the load-bearing packet is
self-contained:

- the displayed local generator `W[J] = log det(D+J) - log det D`
- the displayed Hessian definition `B_D(h,k) := D^2W[0](h,k)`
- the displayed positive invariant background `D = diag(a,b,b,b)`
- the canonical symmetric basis listed above
- [`../scripts/frontier_universal_gr_supermetric_normal_form.py`](../scripts/frontier_universal_gr_supermetric_normal_form.py)
  for the symbolic and numerical proof artifact

The route-context notes named elsewhere in the GR stack explain why this local
object is interesting, but they are not needed to verify the matrix-calculus
identity closed here.

## What this changes

This removes another layer of ambiguity.

Before:

> maybe the remaining issue was still local block normalization or local
> tensor matching.

Now:

> the local tensor form is already exact. The direct universal Hessian is
> already the canonical isotropic supermetric normal form.

So the remaining GR gap is no longer local.

## What is still open

This still does **not** by itself prove full GR.

The remaining missing theorem is now:

> the exact dynamical gluing law that identifies this local supermetric
> normal form with the full Einstein/Regge operator on `PL S^3 x R`,
> using the route-2 slice dynamics rather than only the local Hessian.

Equivalently:

- local supermetric form: exact
- slice generator / transfer law: present separately
- exact Einstein/Regge glue between them: still missing

That is the current sharp frontier.

## Honest status

This note closes one local algebraic step:

- given the displayed log-det generator, the Hessian is exactly
  `-Tr(D^-1 h D^-1 k)`
- in the canonical symmetric basis on `D = diag(a,b,b,b)`, that Hessian has
  the displayed lapse / shift / trace / shear normal form
- the scalar-observable selection premises, route-wide kinematic inputs, and
  final dynamical gluing / Einstein-Regge identification remain outside this
  note's proof scope
