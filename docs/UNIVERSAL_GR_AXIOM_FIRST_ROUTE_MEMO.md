# Universal GR: Axiom-First Route Survey

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Purpose:** direct-to-universal-GR architecture memo, treating the current restricted-class tensor ladder as a diagnostic reference rather than the primary route.

## Executive summary

If the goal is truly **straight-to-universal GR from the axioms**, the cleanest
architecture is not the current restricted-class tensor-boundary ladder.

The best direct route is:

> derive a universal gravitational action from the axiom-side
> observable/self-consistency principle, then recover Einstein/Regge dynamics
> as its Euler-Lagrange content.

The concrete implementation of that route is a discrete `3+1` variational action.
The restricted tensor ladder is useful only as a test bench and blocker
localizer.

## Ranked direct-to-universal routes

These are ranked by how directly they can plausibly yield universal GR without
starting from a special shell/source class.

### 1. Observable-principle effective-action route

- **Core idea:** derive the gravitational action as the unique local effective
  action compatible with the observable principle, self-consistency, locality,
  and covariance.
- **Why it is the best direct route:** it is the most axiom-native architecture
  in the current stack. It does not begin from a restricted source family; it
  begins from a candidate universality principle.
- **Why it beats the restricted-class-first route conceptually:** full GR is a
  universal field theory, so the natural proof shape is a universal action or
  uniqueness theorem, not a local tensor completion on one audited source class.
- **Current blocker:** the branch has a universal scalar self-consistency
  closure for Poisson, but no exact tensor-valued action or tensor-valued
  uniqueness theorem at the full metric level.

### 2. Discrete `3+1` variational action route

- **Core idea:** build the universal gravity law as a discrete local action on
  the full spacetime side, then derive the field equations as stationarity.
- **Why it is second:** it is the concrete realization of the effective-action
  route. It is the first implementation target once the universal principle is
  fixed.
- **Why it is still cleaner than the restricted-class ladder:** it asks for the
  full tensor dynamics law directly, instead of bootstrapping from a special
  support block and then widening.
- **Current blocker:** the current exact action machinery is still scalar/
  shell-level; the tensor extension is not exact yet.

### 3. Axiom-first spacetime lift from `S^3` and anomaly-forced time

- **Core idea:** derive the spacetime background first, then force GR as the
  unique compatible `3+1` dynamics.
- **Why it ranks below the action route:** it is a strong kinematic scaffold,
  but it still needs a dynamics bridge.
- **Current blocker:** exact `S^3` and exact single-clock time are in hand, but
  no universal tensor dynamics theorem yet.

### 4. Exact finite-rank source-to-metric theorem

- **Core idea:** use the exact finite-rank source family and boundary/action
  laws to prove a unique source-to-metric map.
- **Why it is not the primary universal route:** it remains source-family
  dependent, so it is not as architecture-clean as an action-first derivation.
- **Current blocker:** it still leaves a tensor completion gap between source
  families.

### 5. Direct lattice Green/resolvent route

- **Core idea:** derive the metric directly from the lattice operator resolvent.
- **Why it is lower ranked:** it is elegant, but it still needs a tensor-valued
  readout and tends to reintroduce boundary-class dependence.

## Why the restricted-class ladder is not the primary route

The restricted tensor ladder is valuable, but it is a foothold, not the end
game:

- it localizes the missing tensor object
- it gives exact scalar support laws
- it identifies the bright channels
- it does **not** by itself supply universal GR

So the restricted-class ladder is best treated as:

- a test bench
- a blocker localizer
- a consistency check for any universal action candidate

not as the main proof architecture.

## Single best candidate route

The single best candidate is the **observable-principle effective-action
route**, with the **discrete `3+1` variational action** as the concrete theorem
form.

Why this wins conceptually:

1. It starts from axiom-level universality rather than a special source class.
2. It matches the structure of a universal field theory: action first, metric
   equations second.
3. It has the right failure mode: if it fails, the failure is a missing tensor
   action/uniqueness theorem, not another local fit.

## Current theorem step

The current direct-universal theorem step is not a closure claim. It is a
sharp blocker note:

- [`UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md`](./UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md)
- [`frontier_universal_gr_tensor_action_blocker.py`](../scripts/frontier_universal_gr_tensor_action_blocker.py)

That blocker says the direct universal route is exact at the scalar observable
principle level and exact at the `3+1` kinematic lift level, but still missing
the first exact tensor-valued action or uniqueness theorem on the full metric
space.

The minimal missing primitive is therefore:

1. an exact tensor-valued `3+1` variational action
2. or an exact tensor-valued source operator on `PL S^3 x R`
3. or an exact uniqueness theorem forcing Einstein/Regge dynamics from the
   observable principle

Until one of those lands, the direct route remains the best architecture but
not a closure theorem.

## Formal support check

Use [`frontier_universal_gr_axiom_first_route_scan.py`](../scripts/frontier_universal_gr_axiom_first_route_scan.py)
to score the route survey by how strongly each route depends on restricted
class language versus axiom-principle / action / self-consistency language.

The expected outcome is that the observable-principle / variational-action
family ranks above the restricted tensor ladder for a direct-to-universal-GR
program.
