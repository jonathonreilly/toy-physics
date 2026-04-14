# Exact `A1` Projective Blindness of the Current Shell/Junction Tensor Toolbox

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_a1_shell_projective_blindness.py`  
**Status:** exact obstruction plus bounded contrast

## Purpose

The current gravity frontier had localized the remaining tensor gap to:

- the bright aligned source channels `E_x` and `T1x`
- one scalar `A1` background-shape ratio
  - `r = s / e0`

That still left one honest axiom-first question:

> can the missing `r`-law be derived from the current exact shell/junction
> stack, or is the attack using the wrong primitive object?

This note answers that question directly.

## Exact theorem: the current shell/junction stack is projectively blind to `r`

Work on the exact seven-site star support with support basis

- `A1(center) = e0`
- `A1(shell) = s`

and normalize `s` to unit total charge by `s / sqrt(6)`.

The runner checks the exact retained shell objects on the sewing band
`3 < r <= 5`:

- exterior-projector potential `u = Pi_R^ext phi`
- shell source `sigma = H_0 u`

Result:

- `u(e0) / 1 = u(s) / sqrt(6)` exactly on the sewing band
- `sigma(e0) / 1 = sigma(s) / sqrt(6)` exactly on the sewing band

with machine-precision differences

- `u/Q`: `1.214e-17`
- `sigma/Q`: `5.551e-17`

Therefore any scalar `A1` background

`q_A1 = a e0 + b s`

enters the retained shell stack only through total charge

`Q = a + sqrt(6) b`

not through the projective ratio `r = b/a`.

## Exact corollary for shell/junction linear response

The retained static-conformal shell lift gives exact shell/junction fields

- `rho = sigma / (2 pi psi^5)`
- `S = rho * u / (1 - u)`
- `psi = 1 + u`

For any non-scalar perturbation direction `p`, the exact linear responses are

- `du = u(p)`
- `d sigma = sigma(p)`
- `d rho = d sigma / (2 pi psi^5) - 5 sigma du / (2 pi psi^6)`
- `dS = d rho * u / (1 - u) + rho * du / (1 - u)^2`

Because the background shell data `(u, sigma)` are already projectively blind
inside `A1`, these exact shell/junction responses at fixed total charge are
also projectively blind to `r`.

The runner verifies this directly on the canonical `Q = 1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

for `r = 0.75, 1.25, 1.75`.

For the bright directions `E_x` and `T1x`, the exact bandwise response spreads
are:

### `E_x`

- `du`: `0`
- `d sigma`: `0`
- `d rho`: `1.355e-19`
- `dS`: `6.776e-21`

### `T1x`

- `du`: `0`
- `d sigma`: `0`
- `d rho`: `4.337e-19`
- `dS`: `2.033e-20`

So the current exact shell/junction tensor toolbox cannot distinguish the
projective `A1` background ratio at fixed total charge.

## Bounded contrast: the numerical tensor drive still sees `r`

On the same `Q = 1` projective grid, the current numerical tensor-boundary
drive coefficients still vary:

- `beta_E_x` spread: `2.343e-06`
- `beta_T1x` spread: `8.935e-07`

So the missing `r`-law is real on the current tensor frontier.

## Consequence

This gives a sharp obstruction:

> the remaining `A1` background-shape law cannot be derived from the current
> retained shell/junction stack alone.

That is stronger than the earlier blocker note. It says the current primitive
object is wrong for the last step.

The shell/junction stack is already exact, but it is **projectively blind** to
the very datum that the remaining tensor law still depends on.

## Clean axiom-first pivot

The first place the missing `r`-dependence can honestly live is now clear:

- the microscopic `2 x 2` `A1` support block before exterior projection

So the cleaner axiom-first gravity route is no longer:

- keep pushing `eta_floor_tf` directly
- or keep searching for a shell-side scalar renormalization law

It is:

1. derive an exact microscopic support-side mixed response operator on
   `A1 x {E_x, T1x}`
2. derive the exact tensor boundary observable from that support-side operator
   rather than from the current numerical Einstein-residual pipeline
3. only then recover the tensor boundary action / completion theorem

## Practical conclusion

This note does **not** close full nonlinear GR.

But it does close one more fake route:

> the last gravity theorem will not come from more algebra on the current exact
> shell/junction observables.

If the gravity lane is going to close axiom-first on the current restricted
class, it has to close from the microscopic support block.
