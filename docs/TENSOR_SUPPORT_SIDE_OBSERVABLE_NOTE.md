# Exact Support-Side `A1` Observable on the Current Restricted Gravity Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact support-side theorem, not yet a full tensor completion theorem

## Purpose

The shell/junction route is now known to be projectively blind to the remaining
`A1` shape ratio `r = s/e0` at fixed total charge. The exact question is:

> what exact microscopic support-side observable survives that blindness and
> can carry the last restricted-gravity law?

The answer on the current retained stack is the exact support-side center
excess scalar.

## Exact support-side observable

Work on the exact seven-site star support with the canonical `A1` basis:

- `e0 = A1(center)`
- `s = A1(shell-average)`

and normalize the shell mode by unit total charge:

- `s / sqrt(6)`.

Let `phi_support = G_S q` be the exact support potential induced by the exact
support Green matrix `G_S`.

Then the surviving support-side scalar is

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

This is exact on the current restricted class.

## Exact endpoint coefficients

For the two unit-charge `A1` endpoints:

- `e0`
- `s / sqrt(6)`

the exact support-side coefficients are:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

So the exact projective `A1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

has the exact support-side law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

## Why this matters

This is the first exact microscopic observable that survives the shell/junction
blindness theorem. It gives the only exact scalar datum currently available on
the microscopic `A1` support block.

## What it does not yet give

This is still **not** the exact tensor boundary observable on
`A1 x {E_x, T1x}`. The tensor coefficients currently remain tied to the
numerical `eta_floor_tf` pipeline, so the exact tensor endpoint theorem is
still blocked.

## Practical conclusion

The retained stack now contains:

- exact shell/junction blindness to `r`
- exact support-side center-excess observable `delta_A1`
- exact endpoint support coefficients at `e0` and `s / sqrt(6)`

What is still missing is the exact tensor-side observable that lifts this
scalar support law to the bright `E_x` and `T1x` tensor channels.
