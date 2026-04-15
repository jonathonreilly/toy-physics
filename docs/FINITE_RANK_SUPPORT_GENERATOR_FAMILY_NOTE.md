# Finite-Rank Support Generator Family: Exact Enlargement and Minimal Extra Channels

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_support_generator_family.py`  
**Status:** exact enlargement from existing atlas objects exists, but it is noncanonical and still does not yield a canonical `Pi_3+1`

## Purpose

This note takes the finite-rank widening lane one step beyond the pure rank
obstruction.

The question is not merely whether the current support stack is rank one.
That is already known. The sharper question is:

> what exact support-side enlargement can already be built from the existing
> atlas objects, and what is the smallest explicit extra generator set needed
> to reach lapse, shift, and spatial trace/shear splitting?

## Exact enlargement from existing atlas objects

The current atlas already supplies an exact noncanonical enlargement of the
support side:

- the exact support-irrep frame
  `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`
- the exact Route 2 bilinear carrier
  `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

On the finite-rank source family, the support-irrep frame reconstructs the
shell source exactly:

- exact shell-source reconstruction error: `2.776e-16`

The support-irrep split is exact:

- `A1(center)` and `A1(shell)` generate the orbit-constant shell data
- `E ⊕ T1` generate the intra-orbit shell fine structure

So the atlas already contains an exact enlargement of the support-side frame.
It is not canonical, but it is exact.

## Exact support-side coordinates in Route 2

The Route 2 interface exposes the aligned bright support coordinates

- `u_E = <E_x, q>`
- `u_T = <T1x, q>`

on the same finite-rank source.

For the audited finite-rank source, the exact values are:

- `u_E = 2.058846739693e-01`
- `u_T = 3.811992559293e-02`
- `delta_A1 = 3.307783365857e-02`

The exact carrier is therefore not just symbolic. It is explicitly realized
by the current atlas objects on the finite-rank source.

## Constructive support-side enlargement

The smallest exact enlargement visible from the atlas is the three-channel
source-family frame:

- total charge / scalar `A1`
- aligned bright `E` channel
- aligned bright `T1` channel

At the source-irrep level, that corresponds to:

- `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`

At the Route 2 interface level, it corresponds to:

- `Q_eff`
- `u_E`
- `u_T`

This is the exact support-side enlargement that can already be built from the
current atlas objects.

## What it achieves

This enlargement is enough to separate the non-scalar support content into the
correct `3+1`-relevant channels:

- lapse-like scalar sector
- shift-like aligned bright sector
- spatial trace/shear-like aligned bright sector

It does so noncanonically, because the support response operator still
collapses to rank one after renormalization. So the enlargement exists, but it
does not yet define a canonical polarization bundle or a canonical `Pi_3+1`.

The associated channel scan gives the expected signed response:

- `E` sector lowers the tensor-drive coefficient
- `T1` sector raises it
- the combined shift is nearly additive

This is the strongest explicit support-side evidence currently available.

## Minimal extra generator set

The smallest explicit extra support-side generator set needed beyond total
charge is:

> two non-scalar generators, concretely the aligned bright channels `u_E` and
> `u_T`, backed microscopically by the exact `E ⊕ T1` support-irrep content.

This is the minimum that the current atlas can expose for a plausible
lapse/shift/spatial-trace-shear split.

## Why canonical closure still fails

The exact enlargement does not become canonical because:

- the support response operator remains rank one after renormalization
- the exact support Green/Hessian has no mixed `A1`-bright block
- the second active quotient mode is not canonically sourced by the current
  support span

So the widening lane now has an exact noncanonical enlargement, but it still
lacks a canonical support-side `Pi_3+1`.

## Bottom line

The constructive finite-rank support result is:

> the current atlas already contains an exact noncanonical support-side
> enlargement, realized by `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1` and by the
> Route 2 bright channels `u_E` and `u_T`.

The remaining theorem is the canonicalization step:

> derive a support-side polarization bundle that makes that enlargement
> canonical and produces an exact `Pi_3+1`.
