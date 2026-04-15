# Polarization Connection Distinguished-Connection Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** connection-only attack from `Pi_A1`, the quotient kernel,
`B_R = (K_R, I_TB, Xi_TB)`, and the Maurer-Cartan orbit connection  
**Purpose:** test whether stationarity, minimality, flatness, and compatibility
with the exact semigroup transport / tensorized action uniquely fix a
distinguished connection

## Verdict

They do **not** uniquely fix a distinguished connection.

The strongest canonical candidate the current atlas supports is the block
connection

`nabla^cand = nabla_A1 ⊕ nabla_B ⊕ omega_MC`,

with

`P_R^cand = (Pi_A1, B_R, O_R)` and `B_R = (K_R, I_TB, Xi_TB)`.

That candidate is exact on the invariant `A1` core and on the Route 2 bridge
triple, but the complement remains an orbit bundle rather than a canonical
section. So the current constraints select a canonical block structure, not a
fully distinguished full connection.

## What is exact already

### Exact `A1` core

The direct-universal stack fixes the exact rank-2 invariant projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

This selects the lapse channel `h_00` and the spatial trace `tr(h_ij)` and is
frame-invariant across valid `3+1` rotations.

### Exact Route 2 bridge

The common Route 2 bridge triple is

`B_R = (K_R, I_TB, Xi_TB)`.

Its exact pieces are:

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`,

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - K_R(q)||^2`,

`Xi_TB(t ; q) = vec(K_R(q)) ⊗ exp(-t Lambda_R) u_*`.

The exact semigroup factor `exp(-t Lambda_R)` is frame-independent.

### Exact orbit connection

The complementary `E ⊕ T1` channels organize into the natural orbit /
Maurer-Cartan connection on the valid `3+1` frame orbit.

That orbit connection is exact, but it is only a connection on the orbit
bundle. It is not a distinguished section.

## What the variational / transport constraints actually do

The constraints under audit are:

1. stationarity on the invariant `A1` block;
2. minimality of the extension from the exact bridge triple;
3. flatness of the orbit transport;
4. compatibility with `Xi_TB` semigroup transport;
5. compatibility with the tensorized Route 2 action `I_TB`.

These constraints do three things:

1. they force the `A1` core to stay fixed;
2. they force the Route 2 bridge to stay exact;
3. they force the complement to be an orbit bundle with the natural
   Maurer-Cartan transport.

They do **not** collapse the orbit bundle to a canonical section.

## Strongest canonical candidate

The strongest canonical connection candidate currently supported by the atlas
is:

`nabla^cand = nabla_A1 ⊕ nabla_B ⊕ omega_MC`.

Interpretation:

- `nabla_A1` is flat on the invariant `A1` core;
- `nabla_B` is the exact Route 2 transport induced by `exp(-t Lambda_R)`;
- `omega_MC` is the orbit / Maurer-Cartan connection on the complement.

This is the smallest candidate compatible with all current exact data.

## Exact residual gauge

The current atlas leaves exact residual gauge freedom on both sides of the
candidate.

### Universal side

The complement of `Pi_A1` is an `SO(3)` orbit bundle on the valid `3+1`
frame orbit.

So the exact residual universal gauge is:

`SO(3)`.

The current constraints do not pick a unique `Pi_curv` or a unique
distinguished connection on that orbit.

### Support side

The support-side bright/dark splitting is canonical only up to the already
identified endpoint conventions.

After those are fixed, the remaining residual gauge is:

`O(1) × O(2)`.

This is the gauge freedom on the unused support complement, not on the
bright carrier itself.

## Honest conclusion

The connection-only attack does not produce a uniquely distinguished
connection from the current atlas alone.

What it does produce is the sharpest canonical completion available today:

`nabla^cand = nabla_A1 ⊕ nabla_B ⊕ omega_MC`.

The exact residual gauge left after all stationarity, minimality, flatness,
and transport-compatibility constraints is:

- `SO(3)` on the universal complement;
- `O(1) × O(2)` on the support-side dark complement.

That is the exact boundary of the current connection attack.
