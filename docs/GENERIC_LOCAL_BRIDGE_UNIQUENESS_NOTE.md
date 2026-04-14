# Generic Finite-Support Local Bridge Uniqueness on the Current Bridge Surface

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_generic_local_bridge_uniqueness.py`  
**Status:** Exact affine bridge preservation plus bounded generic-support
nonlinear exclusion

## Purpose

The bridge package is now exact on generic finite support on the current box.

That still leaves one possible escape hatch:

> perhaps the same shell/action package can be closed by a different nonlinear
> local scalar bridge once we move beyond the original star-supported benchmark

This note tightens that gap.

## Exact affine preservation statement

Let `phi_ext` be the exact exterior projector field on the current generic
finite-support bridge class. It is discrete harmonic on the exterior bulk:

- `H_0 phi_ext = 0`.

Any local scalar bridge channel of the form

- `u = F(phi_ext)`

that is also exterior harmonic on the same bulk must preserve the discrete
mean-value identity on the realized neighbor data.

Affine channels preserve that identity exactly. So the native bridge channels

- `psi = 1 + phi_ext`
- `chi = 1 - phi_ext`

remain exact on this broader class.

## Bounded nonlinear exclusion on generic finite support

The companion script samples several genuinely non-star finite-support source
operators and compares the affine bridge with quadratic local deformations

- `F(phi) = 1 + phi + a_2 phi^2`.

It finds:

- the affine bridge remains exterior harmonic to machine precision
- quadratic local deformations immediately produce bulk residual
- the same failure appears as a Jensen/mean-value gap on nontrivial exterior
  neighbor data

So the old “maybe the benchmark bridge is only locally special” escape hatch is
now weaker on the broader generic finite-support class too.

## What this closes

This closes one more benchmark-specific objection:

> the local-scalar bridge uniqueness obstruction is not confined to the
> star-supported benchmark geometry; it persists on the broader generic
> finite-support class on the current box

That means the remaining gravity gap is no longer plausibly a hidden nonlinear
local scalar bridge inside the current finite-support bridge surface.

## What this still does not close

This note still does **not** close:

1. nonlocal or tensorially broader bridge structures
2. closure beyond the current static conformal bridge
3. noncompact or long-range support classes
4. fully general nonlinear GR

## Practical conclusion

The gravity gap is narrower again:

- finite-support closure is no longer benchmark-star-specific
- local scalar bridge freedom is no longer plausibly hiding there either
- the remaining work is now genuinely beyond the current static conformal
  bridge class, not just another local reparameterization inside it
