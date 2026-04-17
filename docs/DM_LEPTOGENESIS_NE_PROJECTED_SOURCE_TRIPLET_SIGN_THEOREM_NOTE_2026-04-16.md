# DM Leptogenesis `N_e` Projected-Source Triplet Sign Theorem

**Date:** 2026-04-16  
**Status:** exact bridge theorem from the DM-lane projected Hermitian source law
to the baryogenesis-side triplet sign target  
**Script:** `scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py`

## Question

Can the baryogenesis-side triplet target be written directly at the DM-lane
endpoint `dW_e^H`, rather than only through the intermediate off-seed PMNS
coordinates?

## Bottom line

Yes.

If the projected Hermitian response pack on the charged support `E_e` is
written as

`(R11, R22, R33, S12, A12, S13, A13, S23, A23)`,

where:

- `Rii` are the diagonal Hermitian responses,
- `Sij = 2 Re(H_ij)`,
- `Aij` are the antisymmetric Hermitian responses with
  `H_ij = (Sij - i Aij)/2`,

then the baryogenesis triplet channels are exact linear functionals of that
same projected source pack:

- `gamma = A13 / 2`
- `E1 = delta + rho = (R22 - R33)/2 + (S12 - S13)/4`
- `E2 = A + b - c - d = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2`

So the live PMNS constructive gate can be stated directly at `dW_e^H` level:

- `gamma > 0`
- `E1 > 0`
- `E2 > 0`

## What this closes

This closes the bridge-shape ambiguity raised by the DM lane.

The DM route had already reduced the PMNS-assisted problem to:

`D -> D_- -> dW_e^H -> H_e -> packet -> eta`.

What was still missing was the baryogenesis-side translation of that endpoint.

This theorem supplies it:

- the DM-lane endpoint `dW_e^H` already carries the baryogenesis triplet
  channels,
- and it carries them by exact linear formulas.

So the next PMNS-side baryogenesis step no longer needs to be described as
“derive some better full-`D` law” in the abstract.

It is specifically:

- derive a microscopic law whose projected Hermitian source pack satisfies
  `gamma > 0`, `E1 > 0`, `E2 > 0`

equivalently

- derive `dW_e^H` with
  `A13 > 0`,
  `(R22 - R33)/2 + (S12 - S13)/4 > 0`,
  `R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2 > 0`.

## Canonical comparator read

On the canonical near-closing `N_e` sample, the projected Hermitian source pack
already yields:

- `gamma > 0`
- `E1 < 0`
- `E2 < 0`

So the canonical DM/PMNS comparator already has the right odd source sign but
still misses the constructive baryogenesis sheet on both real interference
channels.

## Consequence for the live target

The PMNS-side comparator target is now explicit in two equivalent ways:

- off-seed source form:
  `sin(delta) > 0`, `E1 > 0`, `E2 > 0`
- projected-source form:
  `gamma > 0`, `E1 > 0`, `E2 > 0`
  with `gamma`, `E1`, `E2` given by the linear `dW_e^H` formulas above

So the live remaining comparator task is:

- derive a full-`D` / `D_-` / `dW_e^H` law that lands on that sign system

or else

- prove a sharper exact no-go on the current PMNS branch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py
```
