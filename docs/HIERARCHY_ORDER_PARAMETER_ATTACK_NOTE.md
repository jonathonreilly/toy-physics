# Hierarchy Order-Parameter Attack Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Purpose:** Codex-owned note on the remaining determinant-to-VEV gap in the
hierarchy route.

## Current status

The hierarchy work on `claude/youthful-neumann` has materially narrowed the
structural side of the problem:

- `16 = 2 x 2^3` is now a credible `3+1` exponent mechanism
- the minimal temporal block `L_t = 2` is much better motivated
- the reduced-vs-unreduced Planck-mass normalization bug is real and fixed

But the load-bearing theorem is still missing:

> Why is the physical electroweak order parameter the `L_t = 2` one-block
> object, and why does it map to `v` with unit prefactor?

## First negative result

The obvious shortcut does **not** work:

- raw determinant factorization at `L_t = 2n`
  `det(D_{2n}) = det(D_2)^n * C_n`
  is exact in the coupling-scaling sense
- but the mass-inserted determinant ratio
  `det(D_{2n} + m) / det(D_{2n})`
  does **not** factorize exactly through the `L_t = 2` block

In other words:

- coupling-independent constants can be discarded for the raw determinant
  scaling problem
- they do **not** automatically disappear in the physical mass-deformed
  observable

That means the final theorem cannot be:

- “`det(D)` factorizes, therefore the hierarchy observable is one block”

It has to be:

- derive the actual intensive order parameter from the condensate or effective
  action, and only then prove how the one-block contribution is singled out

## Concrete theorem target

The right mathematical object is not the raw determinant itself, but one of:

1. the condensate
   `\langle \bar{\psi}\psi \rangle = \partial_m \ln Z`
2. the effective-action difference
   `\Delta V_eff(\phi) = -(1/V_4) \ln [det(D + y \phi) / det(D)]`
3. the curvature / stationarity condition at the minimum of that effective
   potential

Any successful closure must show that:

- the intensive/local observable above reduces to the `L_t = 2` block
  contribution plus terms that are either:
  - coupling-independent and field-independent, or
  - suppressed / decoupled in the UV matching limit

## Immediate implications

Three things are now clear:

1. **Part 3 cannot be closed by exponent counting alone.**
   The missing theorem is not about `u_0` power.

2. **The proof has to go through the effective-action side.**
   If the one-block theorem is true, it should emerge from the local
   condensate / free-energy density, not the extensive determinant.

3. **Spatial APBC is still a separate issue.**
   Even if the order-parameter theorem closes, the even-`L` spatial APBC
   ambiguity still needs either:
   - a framework derivation, or
   - a BC-independence theorem for the exponent / intensive observable.

## Best next move

The next serious attack is:

1. define the intensive order parameter on the `3+1` staggered block
2. test whether the free-energy density per temporal block, or its
   mass/field derivative, is approximately or exactly `L_t`-independent
   after subtracting the zero-field piece
3. if yes, derive the corresponding one-block theorem
4. if not, identify the additional microscopic assumption currently hidden in
   the hierarchy note and stop calling the route closed

## Honest conclusion

The hierarchy route is stronger than it was, but the determinant-to-VEV map
is still the real open theorem. The new Codex-side result is useful because it
rules out the easiest fake proof and forces the next step onto the correct
condensate / effective-action surface.
