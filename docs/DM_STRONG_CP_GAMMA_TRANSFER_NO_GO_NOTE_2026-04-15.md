# DM Strong-CP `\gamma`-Transfer Boundary

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
and the DM neutrino Hermitian carrier  
**Script:** `scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py`

## Question

Does the current strong-CP + CKM closure already populate the DM neutrino
Hermitian bridge carrier, especially the CP-odd triplet source `gamma`?

In other words: can the current exact weak-only `Z_3` source and quark-block
tensor-slot package already close the DM denominator?

## Bottom line

No.

The current strong-CP / CKM package helps only up to **source orientation**.
It does not yet give a neutrino-side coefficient law for the DM carrier.

What is exact now:

- the strong-CP theorem keeps the CP source **weak-sector only**
- the strong-CP theorem keeps the color commutant **blind to the weak phase**
- the CKM tensor-slot theorem is **quark-block specific**
- the exact weak source orientation is `delta_src = 2 pi / 3`

But fixing `phi = 2 pi / 3` on the active neutrino Hermitian branch still
leaves a continuum of distinct triplets `(delta,rho,gamma)` and therefore a
continuum of distinct DM CP kernels.

So the current strong-CP / CKM package does **not** already populate

`B_H,min = (A,B,u,v,delta,rho,gamma)`.

## Exact reason

The DM target is the exact three-real breaking-triplet carrier

`span_R{T_delta, T_rho, T_gamma}`.

The current strong-CP package does not provide a three-real neutrino-side
coefficient law. It provides:

- one fixed discrete source orientation `delta_src = 2 pi / 3`
- factorized weak/color structure
- a quark-block tensor carrier `K_R`

That is enough to orient a source direction. It is not enough to determine the
neutrino Hermitian coefficients.

This is visible directly on the DM branch: holding

`phi = 2 pi / 3`

fixed still permits distinct values of:

- `gamma = r_31 sin(phi)`
- `delta + rho`
- `A + b - c - d`

and therefore distinct values of the intrinsic leptogenesis tensor

- `Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3`
- `Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3`.

So the current strong-CP closure is **not** the missing DM theorem. It is only
part of the scaffolding.

## What this closes

This closes the idea that strong-CP closure by itself should already finish DM.

It is now exact that the current branch is **not** blocked on:

- understanding whether the strong-CP source is weak-only
- understanding whether color and weak stay factorized
- understanding whether the quark tensor-slot package exists

It is still blocked on the missing cross-sector step:

> a transfer / coefficient law that populates the neutrino Hermitian carrier
> `B_H,min`, especially the triplet leg `(delta,rho,gamma)`.

## What this does not close

This note does **not** prove that no future transfer theorem can exist.

It only proves that the **current** strong-CP + CKM closure does not already
supply it.

So this is a current-stack no-go / boundary theorem, not an absolute
impossibility theorem.

## Command

```bash
python3 scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py
```
