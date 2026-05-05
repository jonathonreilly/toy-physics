# Discrete Einstein/Regge Lift on the Restricted Strong-Field Class

**Date:** 2026-04-13
**Claim type:** bounded_theorem
**Status:** bounded - restricted 3+1 lift on the current bridge surface; not full nonlinear GR
**Primary runner:** `scripts/frontier_universal_gr_isotropic_glue_operator.py`

## Purpose

The restricted strong-field package already has:

- an exact shell source;
- an exact same-charge bridge;
- an exact local static-constraint lift;
- an exact microscopic Schur boundary action;
- an exact microscopic Dirichlet principle;
- support-class widening beyond the star-supported benchmark class.

The remaining local interpretation question is:

> can the bridge and shell law be written as one discrete local field equation
> whose stationarity reproduces the exact shell trace and the current bridge,
> rather than only being presented as a static-conformal package?

This note answers that bounded question on the current restricted class.

## Exact Local Field Equation

Let `Gamma_R` be the sewing shell at `R = 4` and let

```text
Lambda_R = H_tt - H_tb H_bb^(-1) H_bt
```

be the exact Schur-complement Dirichlet-to-Neumann matrix of the exterior
microscopic lattice Laplacian.

For any shell trace field `f` with microscopic flux source `j`, define the
boundary functional

```text
I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f.
```

Then the local discrete junction equation is the stationarity condition

```text
delta I_R = 0  <=>  Lambda_R f = j.
```

On the exact source classes already represented by
[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](OH_SCHUR_BOUNDARY_ACTION_NOTE.md), the
exact shell trace `f_*` of the exterior projector field satisfies
`j = Lambda_R f_*`, so `f_* = Lambda_R^(-1) j` is the exact minimizer.

Equivalently,

```text
I_R(f ; j) = I_R(f_* ; j) + 1/2 (f - f_*)^T Lambda_R (f - f_*).
```

Because `Lambda_R` is symmetric positive definite on the current bridge
surface, the bridge trace is the unique global minimizer of the exact
microscopic boundary energy.

## Restricted Discrete 3+1 Lift

The same shell trace drives the local static conformal fields

```text
psi = 1 + phi_ext
chi = 1 - phi_ext = alpha psi
```

and the induced source/stress fields

```text
sigma_R = H_0 phi_ext
rho = sigma_R / (2 pi psi^5)
S = 0.5 rho (1/alpha - 1)
```

so the exact local static-conformal constraint pair remains

```text
H_0 psi = 2 pi psi^5 rho
H_0 chi = -2 pi alpha psi^5 (rho + 2S).
```

That is the restricted discrete `3+1` lift: the same shell trace that
minimizes the microscopic boundary action also fixes the local conformal lapse
and metric source data.

## Einstein/Regge Analogue

The lattice boundary functional plays the same role on the current restricted
class that a junction term or simplicial curvature term would play in a full
Einstein/Regge derivation:

- it is local on the shell trace;
- it is quadratic and positive definite on the current class;
- its Euler-Lagrange equation is the exact shell law;
- its minimizer is the native same-charge bridge.

So the bridge is not just harmonic packaging. It is the exact stationary point
of the microscopic boundary functional on the restricted strong-field class.

## What This Closes

This closes the field-equation-vs-bridge-packaging ambiguity on the current
restricted class:

> the exact shell law and current bridge are the stationary point of one local
> discrete boundary functional, i.e. the current-class Einstein/Regge-style
> `3+1` lift.

That is stronger than the static-conformal package alone and is the strongest
restricted lift currently defensible on this route.

## What This Does Not Close

This note does not close:

1. extension beyond the current static conformal bridge;
2. noncompact or long-range support classes;
3. fully general nonlinear GR.

The live gap is the extension to a broader microscopic bridge principle and
then to full nonlinear GR in full generality.
