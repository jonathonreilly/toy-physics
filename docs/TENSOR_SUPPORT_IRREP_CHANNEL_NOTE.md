# Tensor Drive Organizes in Support-Irrep Coordinates

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_support_irrep_channel_scan.py`  
**Status:** bounded positive narrowing on the exact star-supported source class

## Purpose

The previous note proved an exact structural statement:

- orbit-summed shell data come from the scalar `A1` support sector
- intra-orbit shell structure comes from the non-scalar `E ⊕ T1` support
  sectors

This note asks the next bounded question:

> does the remaining tensor-drive coefficient already organize naturally in
> those same support-irrep coordinates?

The answer is yes, on the exact star-supported source class audited here.

## Setup

Take the exact finite-rank source and decompose it into:

- scalar `A1` part
- non-scalar `E` part
- non-scalar `T1` part

Then hold the scalar `A1` sector fixed and turn on:

- `E` alone
- `T1` alone
- `E + T1`

The runner evaluates the scalar-derived tensor drive

`c_eta = eta_floor_tf / |I_scalar|`.

## Endpoint values

- `A1` only: `c_eta = 3.336065453544e-03`
- `A1 + E`: `c_eta = 3.308585771378e-03`
- `A1 + T1`: `c_eta = 3.344558668003e-03`
- `A1 + E + T1`: `c_eta = 3.317194181484e-03`

So:

- the `E` sector lowers `c_eta`
- the `T1` sector raises `c_eta`

## Nearly additive channel law

The shifts are:

- `E` shift: `-2.747968216672e-05`
- `T1` shift: `+8.493214458438e-06`
- full finite-rank shift: `-1.887127205981e-05`

The additivity error is only:

- `1.151956484694e-07`

So on this audited exact source direction, the full finite-rank correction is
already very close to the sum of independent `E` and `T1` channel
contributions.

## Nearly linear one-parameter response

The one-parameter scans are also nearly linear:

- max discrete second difference along the `E` scan:
  `4.778393e-08`
- max discrete second difference along the `T1` scan:
  `2.761301e-10`

That means the support-irrep organization is not just a good endpoint
decomposition. It behaves like the right coordinate system for the tensor-drive
response on the current exact source family.

## What this changes

Before this note, the live gravity target was:

- derive a support-irrep lift from non-scalar source content into the tensor
  boundary drive

After this note, the target is sharper:

- derive the `E` and `T1` transfer coefficients into the tensor boundary drive

That is now a much more concrete theorem target than “derive more microscopic
source data.”

## Current best gravity read

The strongest honest statement now is:

> on the exact star-supported source class, the remaining tensor-drive
> coefficient is already naturally organized in support-irrep coordinates: the
> `E` sector lowers it, the `T1` sector raises it, and the full finite-rank
> correction is nearly additive in those two non-scalar channels.

This is still bounded, not full GR closure. But it is a real positive route
toward the remaining microscopic theorem.
