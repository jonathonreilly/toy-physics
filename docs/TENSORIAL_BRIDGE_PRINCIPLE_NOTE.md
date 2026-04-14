# Tensorial Bridge Principle Test on the Current Strong-Field Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensorial_bridge_principle.py`  
**Status:** Bounded tensor correction on the current static conformal bridge class

## Purpose

The restricted strong-field package on the branch has already closed the
shell source, same-charge bridge, local static-constraint lift, Schur boundary
action, and microscopic Dirichlet principle on the current source classes.

The remaining gravity gap is therefore narrower:

> can the universal anisotropic DtN shell mode be promoted into a genuine
> broader microscopic nonlocal / tensor bridge principle that improves the
> full 4D Einstein/Regge residual beyond the current static conformal bridge?

This note tests the smallest plausible tensor/shear completion and reports the
result sharply.

## Tensor candidate tested

Start from the exact shell source on the current bridge class and split it into
its radial and anisotropic pieces:

- `sigma_R = sigma_rad + delta_sigma`

The anisotropic remainder is the universal zero-monopole DtN orbit mode already
identified on the branch.

Promote that mode into the minimal traceless spatial shear deformation of the
static conformal metric:

- `g_tt = -alpha^2`
- `g_xx = psi^4 exp(eps s)`
- `g_yy = psi^4 exp(-eps s)`
- `g_zz = psi^4`

with `s` the normalized anisotropic mode field and `eps` the tensor amplitude.

This is the smallest local tensor/shear correction that could plausibly extend
the current static conformal bridge.

## Exact boundary-side result

On both current exact source classes

- exact local `O_h`
- exact finite-rank

the shell-mode trace of the anisotropic candidate has:

- zero monopole after removing the scalar charge mode
- strictly positive Schur boundary-action curvature

So the tensor/shear deformation is not a flat direction of the exact microscopic
boundary problem. It costs positive boundary energy immediately.

## Einstein-residual scan

The script scans `eps` on a symmetric interval around zero and evaluates the
full 4D Einstein tensor residual at exterior probe points.

Result:

- the best residual occurs at nonzero `eps` on both source classes
- the tensor/shear mode lowers the 4D Einstein residual relative to the scalar
  bridge, but does not close the gap

So the anisotropic DtN mode is a real first correction rather than a no-go.
It improves the 4D residual, but the remaining residual is still substantial
and the optimal amplitude is family-dependent.

## Smallest tensor correction

The smallest tensor candidate is the universal zero-monopole anisotropic DtN
orbit mode itself. When promoted into the metric as a local traceless shear,
it does two things:

1. raises the exact microscopic boundary action by a positive quadratic amount
2. lowers the 4D Einstein residual relative to the scalar bridge

That is the cleanest bounded tensor correction currently visible on the branch.
It is not a closure theorem because the residual remains nonzero.

## What this means

The remaining gravity gap is now very explicit:

- the current static conformal bridge is still the baseline local closure on
  the tested exact source classes
- the universal anisotropic DtN mode exists as a controlled first tensor
  correction, but it does not close the 4D residual
- therefore any broader bridge principle, if it exists, must be genuinely
  nonlocal or tensorially richer than this minimal local shear completion

## What this does not close

This does **not** close:

1. a broader nonlocal/tensor bridge principle
2. full nonlinear GR in full generality

## Updated gravity target

After this test, the remaining gap is sharper:

- the first tensor/shear correction is real and bounded
- the only plausible next step is a genuinely nonlocal or tensorially broader
  bridge principle, or a sharper tensor completion theorem that drives the
  residual further down
