# Hierarchy Matsubara Decomposition Note

**Date:** 2026-04-13  
**Script:** `scripts/frontier_hierarchy_matsubara_decomposition.py`

## Question

Can the hierarchy determinant and condensate be written in an exact temporal
mode decomposition on the minimal APBC hypercube, so that the remaining Part 3
gap becomes a precise temporal-averaging problem rather than a vague prefactor?

## Exact result

Yes.

On the minimal spatial APBC block `L_s = 2`, all spatial momenta are fixed at
the Brillouin-zone corners, so:

- `sin^2(k_i) = 1` for `i = 1,2,3`
- the full `L_t` dependence sits only in the temporal APBC momenta
  `omega_n = (2n+1) pi / L_t`

For the full staggered Dirac operator with mass `m`:

`|det(D + m)| = prod_omega [m^2 + u_0^2 (3 + sin^2 omega)]^4`

This is an exact closed form on the `L_s = 2` APBC hypercube.

## Consequences

### 1. The determinant is no longer mysterious

The old numerical factorization

`det(D_{2n}) = det(D_2)^n * C_n`

is now explained exactly: it is just the product over the APBC Matsubara
frequencies.

### 2. The intensive observables are also exact

The free-energy density difference is:

`Delta f = (1 / (2 L_t)) sum_omega ln(1 + m^2 / [u_0^2 (3 + sin^2 omega)])`

and the condensate density is:

`(1/N) Tr[(D+m)^(-1)] = (m / L_t) sum_omega 1 / [m^2 + u_0^2 (3 + sin^2 omega)]`

Both formulas match the direct matrix computation to machine precision.

### 3. The remaining theorem is now sharply stated

The open question is no longer:

> what is the prefactor?

It is:

> which temporal averaging of this exact Matsubara formula is the physical
> EWSB order parameter?

That is a much better problem.

## UV endpoint picture

`L_t = 2` is the unique APBC endpoint where every temporal mode has
`sin^2 omega = 1`.

So the one-block hierarchy route is the **maximal temporal-gap endpoint** of
the exact Matsubara family, not an arbitrary guess.

Larger `L_t` values average in lower-gap temporal modes. The exact condensate
density ratio between `L_t = 10` and `L_t = 2` at `u_0 = 0.9`, `m = 10^-2` is:

`R ~= 1.15469`

The crucial compression result is:

- `R^(-1/16) ~= 0.99105`  (too small to explain the observed `253 -> 246` gap)
- `R^(-1/4)  ~= 0.96468`  (in the right few-percent range)

So the exact Matsubara formulas support the interpretation that the final
normalization problem is much more naturally a **dimension-4 effective-potential
density** issue than a direct sixteenth-root correction to the scale.

## Honest conclusion

This still does **not** close the hierarchy theorem.

What it closes is the temporal algebra:

- determinant formula: exact
- free-energy density formula: exact
- condensate density formula: exact

What remains open:

1. why the physical electroweak order parameter is the `L_t = 2` UV endpoint,
   or an explicitly derived function of the exact Matsubara average
2. why the corresponding normalization lands on the observed
   `C_obs ~= 0.97`
3. the spatial APBC issue on even `L = 2`
4. the framework-native derivation of `alpha_LM`

But Part 3 is now much tighter:

> the final theorem is an order-parameter selection / normalization theorem on
> top of an already-exact temporal mode decomposition.
