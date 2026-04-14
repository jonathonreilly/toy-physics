# Tensor Transfer-Coefficient Obstruction from the Retained Shell Toolbox

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_transfer_coefficient_obstruction.py`  
**Status:** exact obstruction on the current retained shell surface

## Purpose

The selector-transfer law already narrowed the tensor normalization gap to one
near-universal coefficient

`c_eta = tau_tensor * c_aniso`.

That still left one serious ambiguity:

> is `tau_tensor` secretly determined by the retained reduced shell data we
> already have, or does full gravity now genuinely need additional microscopic
> source/lift information?

This note answers that question sharply.

## What is already identical across the audited restricted families

On the exact local `O_h` and finite-rank families, the branch already proved
the same retained reduced shell law:

- same radial shell kernel
- same normalized anisotropic orbit mode
- same shell-mean exterior response
- same exact anisotropic amplitude constant

The script confirms those equalities again at machine precision:

- radial shell law difference: `5.551e-16`
- orbit-mode difference: `1.110e-16`
- shell-mean total difference: `2.602e-18`
- shell-mean anisotropic difference: `1.762e-18`
- `c_aniso` relative difference: `5.112e-16`

So the retained shell toolbox is not merely similar on the two families. It is
the same on the reduced surface.

## What is also shared on the tensor-correction side

The projected microscopic tensor-correction quotient still gives the same
active orbit direction on the two families:

- pair-quotient rank: `2`
- active-direction difference: `2.220e-16`

So even after augmenting the retained shell data by the exact shared active
orbit direction, the two families are still indistinguishable on the current
reduced shell-plus-direction surface.

## But tau_tensor is still different

The selector-transfer coefficients remain:

- `tau_tensor(O_h) = 4.388505e-02`
- `tau_tensor(finite-rank) = 4.073405e-02`
- relative difference: `7.180115e-02`

That is small enough to support the bounded positive narrowing, but it is not
zero.

## Exact obstruction

This yields the clean obstruction:

> No theorem that factors only through the current retained reduced shell data
> and the shared active orbit direction can determine `tau_tensor` exactly on
> the audited restricted class.

Reason:

- the inputs on that surface are identical across the two families
- the output `tau_tensor` is not

So the remaining gravity gap is not hidden in the current retained shell
toolbox.

## What this changes

Before this note, the strongest open gravity target was:

- derive `tau_tensor` from the microscopic lift of the exact reduced
  anisotropic DtN mode

After this note, that target is sharper:

- the missing theorem must use **additional microscopic source/lift data beyond
  the current reduced shell surface**

In other words, further shell-only rewrites are exhausted on the current
audited class.

## Current best gravity read

The strongest honest statement now is:

> the retained shell toolbox already fixes the scalar reduced shell law
> exactly, and even the shared active tensor-correction direction does not
> force the remaining selector-transfer coefficient. Full gravity therefore
> needs an additional microscopic source/lift theorem beyond the current
> reduced shell data.

This does **not** close full nonlinear GR. It does sharply eliminate one more
family of false-positive closure routes.
