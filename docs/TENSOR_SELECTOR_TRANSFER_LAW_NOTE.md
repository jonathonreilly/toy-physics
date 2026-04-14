# Tensor Selector-Transfer Law on the Retained Gravity Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_selector_transfer_law.py`  
**Status:** bounded positive narrowing: the exact reduced shell law fixes the
tensor normalization scale, leaving one near-universal transfer coefficient

## Purpose

The previous selector-normalized kernel note showed that the raw tensor-kernel
obstruction is not the whole story:

- raw universal `K_tensor` fails
- but the normalized kernel shape is already close to universal

That still left one serious ambiguity:

> is the normalization itself still arbitrary, or is it already fixed by the
> exact reduced shell law?

This note answers that question as tightly as the current branch allows.

## Exact reduced shell amplitude law already on the branch

The retained reduced shell result gives one exact anisotropic amplitude law:

`A_aniso = c_aniso * Q`

with one exact lattice constant

`c_aniso = 0.081435402995901`

and this constant is exactly the same on the exact local `O_h` and finite-rank
families.

So the anisotropic shell normalization scale itself is no longer free.

## Tensor-side normalization

On the tensor frontier, the scalar-derived tensor drive is

`c_eta = eta_floor_tf / |I_scalar|`.

The key observation is that the remaining tensor normalization can be written
as

`c_eta = tau_tensor * c_aniso`

with one family-near-universal transfer coefficient `tau_tensor`.

The script finds:

- `tau_tensor(O_h) = 4.388505204452727e-02`
- `tau_tensor(finite-rank) = 4.073405496172977e-02`
- relative difference: `7.180115e-02`

So the current branch no longer needs an arbitrary family-by-family tensor
normalization law. It needs one transfer law from the exact reduced
anisotropic shell amplitude into the tensor-channel drive.

## Common selector-transfer candidate

Using:

- the exact universal `c_aniso`
- the average near-universal `tau_tensor`
- the previously derived normalized kernel shape

the common candidate predicts the normalized tensor completion coordinate
within:

- `5.122663e-02` on exact local `O_h`
- `6.555167e-02` on finite-rank

That is the same bounded accuracy level as the selector-normalized kernel note,
but with a much sharper interpretation:

> the exact shell law already fixes the tensor normalization scale; the only
> remaining gravity normalization gap is one transfer coefficient.

## What this changes

Before this note, the positive gravity route looked like:

- derive a selector/coarse-graining/source law for the tensor normalization

After this note, it is narrower:

- derive the transfer coefficient `tau_tensor` from the microscopic lift of the
  exact reduced anisotropic DtN mode

That is materially better. The missing gravity principle is no longer a vague
normalization rule. It is one specific shell-to-tensor transfer law.

## What this does and does not close

This **does** close:

- that the anisotropic shell normalization scale is already fixed exactly by
  the retained reduced shell law
- that the remaining tensor normalization freedom is only one near-universal
  transfer coefficient on the audited restricted class

This does **not** close:

1. an exact theorem for `tau_tensor`
2. the full tensor completion theorem
3. full nonlinear GR in full generality

## Current best gravity read

The strongest honest statement now is:

> on the retained restricted gravity class, the exact reduced shell law fixes
> the anisotropic shell amplitude exactly, and the remaining tensor completion
> gap reduces to one near-universal selector-transfer coefficient from that
> shell amplitude into the tensor boundary drive.

That is the sharpest positive gravity narrowing on the branch so far.
