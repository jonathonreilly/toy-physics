# Finite-Rank Support Canonical Frame

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_support_canonical_frame.py`  
**Status:** canonical support block frame exists; full `Pi_3+1` remains blocked because the dark complement is not canonically fixed by the current support stack

## Verdict

Starting from the exact noncanonical support enlargement

`A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`

and the exact bright coordinates

`u_E = <E_x, q>`, `u_T = <T1x, q>`,

the strongest axiom-native support-side structure currently forced is not a
fully rigid polarization frame. It is a canonical block frame:

- the exact `A1(center)` and `A1(shell)` sector is fixed by the endpoint law;
- the exact ordered bright pair `u_E, u_T` is fixed by the Route 2 carrier;
- the support-irrep split `A1 ⊕ E ⊕ T1` is exact.

What is **not** fixed is the dark complement. That leftover freedom is the
minimal residual gauge.

## What the endpoint constraints fix

The exact support scalar is

`delta_A1 = (phi_support(center) - phi_support(arm_mean)) / Q`.

On the canonical projective `A1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`,

the exact scalar law is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

So the two exact `A1` endpoints are rigid:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

Those endpoint constraints canonically fix the scalar background axis.

## What the Route 2 carrier fixes

The exact microscopic tensor carrier is

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

Its endpoint columns are exact and separate the aligned bright channels:

- `E_x` column: `[(1, 0), (delta_A1, 0)]`
- `T1x` column: `[(0, 1), (0, delta_A1)]`

This fixes the ordered bright pair once the endpoint sign conventions are
chosen. In that sense the support-side canonical frame has a distinguished
bright block.

## Why `I_TB` does not rigidify the frame

The tensorized Route 2 action is

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`.

Because the correction is purely Euclidean, it is blind to orthogonal
reparameterizations of the bright carrier coordinates. So `I_TB` does not
canonically select a unique basis inside the bright block.

That means the action commutes with the exact bright-block reparameterization
freedom but does not eliminate it.

## What support-irrep normalization fixes

The exact finite-rank source splits as

`A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`.

This decomposition is exact and reconstructs the finite-rank shell source.
It also isolates the non-scalar microscopic content into the `E ⊕ T1`
sector.

However, irrep normalization alone only fixes the decomposition, not the full
orthonormal frame in the dark complement. The exact support response operator
still collapses to rank one after renormalization, so there is no canonical
way to promote the dark complement into a full `Pi_3+1`.

## Minimal residual gauge freedom

After endpoint sign conventions are fixed, the leftover freedom is exactly the
orthogonal freedom on the unused dark complement:

- `O(1)` on the one-dimensional `E_perp` direction
- `O(2)` on the two-dimensional dark `T1` plane

This is the smallest exact residual gauge consistent with the current axioms,
the endpoint constraints, and the Route 2 tensorized action.

Equivalently:

> the axioms force a canonical support block frame, but not a fully canonical
> support-side polarization bundle.

## Consequence for `Pi_3+1`

The support-side data are strong enough to define a canonical block
decomposition:

- exact scalar `A1` sector
- exact ordered bright pair `u_E, u_T`
- exact dark complement

But they are not strong enough to define a canonical `Pi_3+1`. Any attempt to
promote the current support side to a full lapse/shift/spatial-trace/shear
splitting must supply a new primitive that kills the residual `O(1) × O(2)`
gauge on the dark complement.

## Bottom line

The strongest axiom-native support-side canonical frame currently available is
the canonical block frame induced by

`A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`

together with the exact bright pair `u_E, u_T`.

The exact residual gauge freedom is

`O(1)_{E_perp} × O(2)_{T1_darken}`.

That is the exact obstruction to a canonical `Pi_3+1` from the current
support stack alone.
