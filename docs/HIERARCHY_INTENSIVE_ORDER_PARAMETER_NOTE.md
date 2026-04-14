# Hierarchy Intensive Order-Parameter Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_hierarchy_intensive_order_parameter.py`

## Question

Can the remaining determinant-to-VEV gap be attacked by moving from the raw
staggered determinant to an **intensive** order parameter such as the
free-energy density or condensate density?

This is the right question because the raw zero-mass determinant factorization

`det(D_{2n}) = det(D_2)^n * C_n`

is exact in the coupling-scaling sense, but the mass-deformed determinant ratio

`det(D_{2n} + m) / det(D_{2n})`

does **not** factorize exactly through the `L_t = 2` block.

## Result

Three facts emerge.

### 1. Raw factorization is exact, but only for the extensive zero-mass determinant

At `m = 0`,

- `det(L_t=4) / det(L_t=2)^2` is `u_0`-independent to machine precision
- `det(L_t=6) / det(L_t=2)^3` is `u_0`-independent to machine precision

So the exponent structure really does live in the minimal block.

### 2. The obvious physical shortcut fails

For the mass-deformed normalized ratios at `u_0 = 0.9`,

- `q4 / q2^2` deviates from `1` by about `10%` to `18%`
- `q6 / q2^3` deviates from `1` by about `15%` to `44%`

across the tested mass window.

That means the theorem cannot be:

> raw determinant factorization => one-block physical observable

The physical observable has to be an **intensive** quantity.

### 3. Intensive observables stabilize quickly, and the mismatch compresses hard under roots

For the condensate density

`(1/N) Tr[(D + m)^{-1}]`

and the free-energy density difference

`(1/N) [ln det(D + m) - ln det(D)]`,

the sequence stabilizes rapidly for `L_t >= 4`.

At `u_0 = 0.9`:

- for `m = 10^{-2}`, the condensate-density ratio `Lt=10 / Lt=2` is about
  `1.1547`
- the fourth-root compression of that ratio is only about `1.0366`
- the sixteenth-root compression is only about `1.0090`

So the large determinant-level mismatch is already only a few-percent effect
once the observable is converted into a low-root intensive scale.

## Interpretation

This is the first Codex-side result that makes the hierarchy near-match look
structurally plausible without pretending the theorem is already done.

What it says:

- the raw determinant carries the right exponent information
- the wrong observable (`det` itself, or its simple mass-deformed ratio) has
  too large a residual to justify closure
- but the residual becomes naturally small once the observable is intensive
  and scale-like

What it does **not** yet say:

- which exact intensive observable is the physical EWSB order parameter
- which root or normalization is the correct one
- whether the sign/direction of the correction lands on the observed
  `C_obs ~= 0.97`

## Practical conclusion

The determinant-to-VEV theorem is still open, but the correct attack surface
is now much sharper:

1. derive the intensive effective-action / condensate observable from the
   framework
2. prove that the `L_t > 2` block corrections reduce to an intensive
   `O(1)` normalization factor
3. show how that normalization enters the final scale extraction

This note does not close Part 3. It does show that the factorization route is
not dead, and that the remaining mismatch is of the right order **after**
passing to the kind of intensive observable a real order parameter should use.
