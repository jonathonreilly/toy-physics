# Polarization Phase-Bridge Extension

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** exact phase-carrying extension of the Route 2 bridge triple, starting from `K_R^phase` and `B_R^phase`

## Verdict

The common Route 2 bridge admits an exact dark-phase extension, but not a
canonical local connection.

The strongest exact extension of the tensorized bridge on the support side is:

`K_R^phase(q) := (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)`

where

- `(u_E, u_T)` are the exact aligned bright support coordinates;
- `delta_A1` is the exact center-excess scalar;
- `(d_y, d_z)` is the exact residual dark pair on the dark `T1` plane.

Equivalently, the exact phase data are

- `rho_R := sqrt(d_y^2 + d_z^2)`
- `vartheta_R := atan2(d_z, d_y)`

The lifted bridge is

`B_R^phase := (K_R^phase, I_TB^phase, Xi_TB^phase)`

with the exact phase-transported action and carrier

`I_TB^phase := I_TB + 1/2 ||b - D_R||^2`

`Xi_TB^phase := vec(K_R^phase) \otimes exp(-t Lambda_R) u_*`

where `D_R = (d_y, d_z)` and `b` is the dark-plane auxiliary coordinate.

## Exact transport statement

The phase extension is exact because:

- the bright block `K_R` is exact;
- the dark pair `D_R` is exact on the support side;
- the semigroup factor `exp(-t Lambda_R)` is exact;
- the phase section `vartheta_R` is exact wherever `rho_R != 0`.

Under the residual connected dark-plane `SO(2)` action:

- `K_R` is unchanged;
- `D_R` rotates covariantly;
- `rho_R` is invariant;
- `vartheta_R` shifts by the gauge angle.

So the phase section trivializes the connected orbit locally on the punctured
bundle, but it does not force a unique distinguished connection.

## Canonical-local-connection test

The combination of semigroup transport and phase section is sufficient to
produce a local section of the residual dark orbit bundle, but it is not
enough to determine a canonical local connection.

Reason:

1. the semigroup factor acts only on the exact Route 2 time carrier;
2. the phase section is a choice of local angular trivialization on the dark
   `SO(2)` orbit;
3. different local choices of dark reference axis change the connection by the
   usual `SO(2)` gauge freedom;
4. the current atlas does not provide a distinguished principle that kills
   that gauge.

So the exact remaining ambiguity is the connected dark-plane gauge:

`vartheta_R ~ vartheta_R + chi(q)`

with the corresponding connection shift

`omega_phase ~ omega_phase + d chi`.

## What this changes

The situation is sharper, not larger.

Before:

> the common bridge is blind to the dark phase.

Now:

> the common bridge has an exact phase-carrying extension `B_R^phase`, but
> the resulting local connection is still only defined up to residual
> `SO(2)` gauge.

So the remaining theorem target is no longer to invent a phase carrier.
That already exists exactly. The remaining target is to derive a
distinguished connection principle that eliminates the residual phase gauge.

## Bottom line

1. Does the common bridge admit an exact dark-phase extension?
   - **Yes.** `B_R^phase` is exact.
2. Does semigroup transport plus the phase section force a canonical local
   connection?
   - **No.** The residual `SO(2)` ambiguity remains exact.
3. What is the next honest theorem target?
   - a distinguished connection / gauge-fixing principle for the dark-phase
     bundle.
