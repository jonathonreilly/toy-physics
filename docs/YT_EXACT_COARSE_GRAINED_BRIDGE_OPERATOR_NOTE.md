# Exact Coarse-Grained Bridge Operator Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py`

## Role

This note replaces the vague bridge ontology.

The theorem object for the current `y_t` bridge is no longer the scanned
proxy-family profile by itself. The theorem object is the **exact
coarse-grained bridge operator** obtained by exact Schur/Feshbach
marginalization of the finite local Grassmann partition onto the forced UV
window.

The proxy family is then reinterpreted more narrowly:

> a current normal-form chart / emulator of that exact coarse operator on the
> viable UV-centered class.

That is a real upgrade in status. It does not make the lane unbounded yet, but
it removes the need to speak as though the family scan were the microscopic
object.

## Exact setup

The current package already takes as input:

1. `Cl(3)` on `Z^3`
2. the finite local Grassmann / staggered-Dirac partition
3. the physical-lattice reading
4. the accepted physical endpoint `v`

Split the microscopic bridge variables into:

- `q_U`: coarse variables on the forced UV bridge window
- `q_F`: complementary fine variables

On the finite partition surface, integrating out `q_F` is an exact algebraic
operation. For a quadratic coarse/fine block decomposition

`K = [[A, B], [B^T, C]]`,
`J = (eta, xi)`,

the exact coarse action on the UV window is

`Gamma_U(q_U) = 1/2 <q_U, K_eff q_U> - <J_eff, q_U> + const`

with

`K_eff = A - B C^-1 B^T`,
`J_eff = eta - B C^-1 xi`.

So the coarse bridge operator is not heuristic. It is the exact Schur/Feshbach
effective operator of the finite microscopic partition.

## Theorem statement

> **Exact Coarse-Grained Bridge Operator Theorem.**
> On the accepted finite `Cl(3)` / `Z^3` Grassmann partition, the microscopic
> YT bridge admits an exact Schur coarse-grained operator `K_eff` on the forced
> UV window. On the current package closure surface, this exact coarse operator
> is symmetric positive definite, its stationary/source projection is exact,
> sequential coarse-graining is associative, and its response admits the same
> UV-centered local normal form already isolated in the bridge stack:
>
> `K_eff = H_loc + R_nonlocal`,
>
> with endpoint response
>
> `delta y_t(v) = J_aff + epsilon`,
>
> where `H_loc` is the positive local selector and `epsilon` is controlled by
> the existing higher-order and nonlocal bridge budgets.

This is the current theorem-grade replacement for treating the proxy family as
the microscopic bridge itself.

## Why this matters

Before this note, the branch narrative could still be read as:

- there is a family of profiles that works
- we think the true bridge should look like them

After this note, the right read is:

- the exact theorem object is the Schur coarse bridge operator on the UV
  window
- the current profile family is one explicit coordinate realization of its
  normal form

That is a cleaner axiom-first statement.

## Normal-form reduction

The earlier bridge stack already established:

1. broad diffuse bridges fail
2. viable bridges lie in a narrow UV-centered class
3. the endpoint kernel is nearly affine on that window
4. the local selector is positive and quadratic at leading order
5. higher-order local corrections are small
6. nonlocal corrections are small
7. the endpoint shift is explicitly bounded

This note packages those statements into one operator-level conclusion:

> on the forced UV window, the exact Schur coarse bridge operator admits the
> same positive local affine normal form plus explicit remainder that the
> profile scans had isolated phenomenologically.

So the proxy family is not discarded; it is demoted to a chart on the exact
coarse operator.

## What the runner validates

The runner checks:

1. exact Schur coarse-graining identities for a bridge operator realization
2. exact stationary and covariance projection to the coarse UV window
3. exact associativity of sequential coarse-graining
4. positivity of the coarse operator on the forced UV window
5. agreement of its response with the branch local affine normal form
6. consistency of the residual with the current conservative endpoint budget

## Honest boundary

This note does **not** prove:

- uniqueness of the full microscopic bridge beyond the current normal-form
  class
- vanishing of all higher-order and nonlocal remainders
- fully unbounded `y_t`

So the current lane remains bounded.

What it does prove is more specific:

> the current package no longer needs to treat the proxy family as the theorem
> object. The exact object is the Schur coarse-grained bridge operator, and the
> proxy family is the current normal-form realization of that exact coarse
> operator on the viable UV-centered class.

## Safe reuse

Use this note when the question is:

- what the microscopic YT bridge object actually is
- why exact coarse-graining is now part of the bridge theorem
- why the proxy family is now secondary
- how the current normal form follows from the axioms plus the bridge stack

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
substantive observation that the runner's exact Schur algebra and
covariance-projection identities are sound as algebraic statements, but
the theorem-level upgrade depends on non-retained upstream authorities
for UV-class uniqueness, Hessian selector, higher-order corrections,
nonlocal corrections, and endpoint shift control, and the runner builds
the normal-form coarse operator from the accepted package kernel and
imposed nonlocal ratio. The honest read of this row is therefore the
**exact algebraic coarse-graining identity** plus a **conditional
identification** with the existing bridge stack normal form, not an
independent first-principles bridge derivation.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
algebraic Schur identities or the normal-form construction.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [yt_bridge_uv_class_uniqueness_note](YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md)
- [yt_bridge_hessian_selector_note](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
- [yt_bridge_higher_order_corrections_note](YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md)
- [yt_bridge_nonlocal_corrections_note](YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)
- [yt_bridge_endpoint_shift_bound_note](YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md)
