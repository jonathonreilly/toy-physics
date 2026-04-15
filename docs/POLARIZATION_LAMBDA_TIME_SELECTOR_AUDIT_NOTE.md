# Polarization Lambda Time/Extrinsic Selector Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** time / extrinsic selector only  
**Purpose:** test whether anomaly-forced `3+1` time, the exact semigroup
`exp(-t Lambda_R)`, the phase-carrying bridge `B_R^phase`, or any odd-in-time
primitive in the atlas canonically fixes the remaining `lambda`

## Verdict

The current atlas does **not** canonically fix `lambda` by time-sensitive
structure.

The exact time data are real:

- anomaly-forced time gives a single clock;
- Route 2 has the exact slice generator `Lambda_R`;
- the bounded transfer bridge is `T_R = exp(-Lambda_R)`;
- the phase-carrying bridge `B_R^phase` exists exactly;
- the support dark phase `vartheta_R` is exact on the punctured dark plane.

But all of those inputs are still compatible with the same residual connected
`SO(2)` gauge. The exact time transport acts on the Route 2 semigroup factor,
not on the multiplicity-space angle that mixes the two universal weight-1
doublets.

So the sharp conclusion is:

> time-sensitive structure in the current atlas does not select a canonical
> `lambda`; it leaves the same one-parameter residual family
> `L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

## Exact inputs checked

### 1. Route 2 time transport

The exact slice generator is symmetric positive definite:

`Lambda_R = Lambda_R^T`, `Lambda_R > 0`.

The exact one-step transfer is the self-adjoint contraction

`T_R = exp(-Lambda_R)`.

This is genuine time-carrying structure, but it is scalar on the weight-1
multiplicity space. It does not distinguish the two universal weight-1
sectors.

### 2. Phase-carrying bridge

The exact support-side phase extension is

`B_R^phase = (K_R^phase, I_TB^phase, Xi_TB^phase)`.

The dark phase `vartheta_R` is exact, but the induced connection family remains

`A_lambda = lambda d vartheta_R`.

That is a flat family on the punctured complement, and time transport does not
canonically fix the coefficient.

### 3. Universal weight-1 multiplicity

The universal complement contains two exact weight-1 doublets. Therefore the
most general normalized equivariant lift from the support dark doublet into the
universal target is

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

The mixing angle `lambda` lives in the multiplicity space. Time evolution does
not act there.

## Time-odd / canonical-momentum tests

The atlas suggests three natural time-sensitive candidates:

1. the odd part under `t -> -t`;
2. the first time derivative, interpreted as a canonical momentum / extrinsic
   curvature proxy;
3. the time-integrated holonomy of the phase connection.

All three fail for the same reason:

- the semigroup factor is common to both weight-1 sectors;
- the lift angle `lambda` is time-independent;
- the dark phase enters only as a spatial orbit coordinate;
- the existing atlas has no exact tensor-valued time-odd primitive that
  couples differently to the two weight-1 sectors.

So any observable built only from the current Route 2 semigroup transport and
the current phase bridge remains `lambda`-blind as a selector.

## What would be needed to fix `lambda`

To canonically fix `lambda`, the atlas would need at least one new exact
primitive that is genuinely time-odd and sector-selective, for example:

- an exact extrinsic-curvature / canonical-momentum operator that couples
  differently to the shift-like and purely spatial weight-1 sectors;
- an exact constraint-algebra selector that forces one weight-1 sector to be
  physical and the other gauge;
- an exact tensor-valued time-coupling law whose odd part is not common-mode
  across the two universal weight-1 doublets.

None of those primitives are present in the current atlas.

## How to avoid needing `lambda`

The only clean way to not need a canonical `lambda` is to stop asking for a
section-valued phase-to-curvature map and work only with the orbit-valued
correspondence:

`[vartheta_R]_{SO(2)}  <->  [alpha_curv]_{SO(2)}`.

That is exact, but it is not a canonical section. It is an orbit theorem, not
closure.

## Sharp residual obstruction

After all time-sensitive checks, the exact residual obstruction remains:

> the connected `SO(2)` dark-plane gauge, equivalently the one-parameter
> normalized weight-1 mixing family `L_lambda`.

So the current atlas does not derive a canonical `lambda` from time or
extrinsic structure.

The best exact statement is negative:

> Route-2 time transport is exact, but it is common-mode on the weight-1
> multiplicity space, so it cannot select a unique `lambda`.

