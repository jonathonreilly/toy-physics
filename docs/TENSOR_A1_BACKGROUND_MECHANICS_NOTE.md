# Mechanics of the Last A1-Background Renormalization Law

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_a1_background_mechanics.py`  
**Status:** bounded mechanistic explanation

## Purpose

The previous gravity frontier reduced the remaining gap to:

- exact shell-amplitude normalization from the retained reduced shell law
- exact local two-channel bright selection in `E_x` and `T1x`
- one last scalar renormalization law on the `A1` background manifold

This note identifies the actual mechanics of that last scalar law on the
audited restricted class.

## Setup

Write the scalar `A1` background with fixed total charge `Q` as

- `q_A1(r; Q) = Q * (e0 + r s) / (1 + sqrt(6) r)`

where:

- `e0` is the center-supported `A1` basis vector
- `s` is the shell-supported `A1` basis vector
- `r = s/e0` is the shell-versus-center shape ratio

For the two bright tensor channels, define the shell-normalized local response
coefficients

- `gamma_E = beta_E_x / A_aniso`
- `gamma_T = beta_T1x / A_aniso`

with the exact retained shell amplitude

- `A_aniso = c_aniso * Q`

## Result

At fixed `r`, the normalized bright coefficients are nearly independent of
total charge `Q`.

On the audited grid:

- `r in {0.75, 1.25, 1.75}`
- `Q in {0.5, 1.0, 1.5}`

the worst Q-spreads are:

- `max spread(gamma_E) = 4.150e-07`
- `max spread(gamma_T) = 3.331e-07`

So after the exact shell-amplitude law is factored out, the remaining bright
coefficient law is not primarily a charge law.

It is a shape law.

## Interpretation

That means the actual mechanics behind the last renormalization step are:

1. The retained reduced-shell theorem fixes the total-amplitude scale exactly.
2. The local tensor lift sees only the bright aligned channels `E_x` and `T1x`.
3. The remaining mismatch is controlled mainly by the scalar `A1` background
   shape parameter `r = s/e0`.

So the live gravity target is no longer:

- “find a new tensor completion principle” in the broad sense

but:

- derive the scalar background-shape law
  `r -> (gamma_E(r), gamma_T(r))`

## Current best gravity read

The strongest honest statement now is:

> on the audited restricted class, the actual mechanics of the last tensor
> renormalization step are now exposed: total-charge scaling is already fixed
> by the exact shell law, and the remaining bright tensor coefficients are
> governed primarily by one scalar `A1` background-shape parameter.
