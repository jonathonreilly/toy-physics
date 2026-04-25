# Koide Q Orbit-Dimension Coefficient No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_orbit_dimension_coefficient_no_go.py`  
**Status:** executable no-go for deriving the Koide quadratic coefficient from
`Z3` orbit-dimension data alone

## Theorem Attempt

The support route is attractive because the retained cyclic basis has the
exact singlet/doublet norm ratio

```text
Tr(B1^2) / Tr(B0^2) = Tr(B2^2) / Tr(B0^2) = 2.
```

The attempted theorem was:

> the retained `Z3` real-irrep dimension pattern `1+2`, or equivalently the
> cyclic-basis norm ratio `1:2`, forces the Koide source-law quadratic
> coefficient.

The audit rejects that theorem.  The orbit-dimension ratio explains why the
number `2` is natural support, but it does not choose the source-law
coefficient.

## Route Ranking

1. **Orbit-dimension coefficient law:** strongest remaining support route
   after cyclic-compression scalar blindness, because it attacks the exact
   coefficient rather than the whole carrier.
2. **What if the coefficient is just the irrep norm ratio?** invert the
   missing-law assumption and test whether `1:2` already is the law.
3. **Quadratic `C3` covariance:** enumerate all invariant quadratics and see
   whether cross-term removal also fixes the singlet/doublet coefficient.
4. **Metric normalization:** ask whether changing basis normalization is doing
   hidden work.
5. **Return to source grammar:** if coefficient remains free, only a retained
   source law can pick it.

## Exact Support

For the retained cyclic basis:

```text
B0 = I,
B1 = C + C^T,
B2 = i(C - C^T),
```

the runner verifies:

```text
Tr(B0^2) = 3,
Tr(B1^2) = 6,
Tr(B2^2) = 6.
```

So the norm/orbit-dimension ratio is exactly:

```text
6 / 3 = 2.
```

This remains good support for the singlet/doublet split.

## Obstruction

The most general retained `C3`-invariant quadratic in the cyclic response
coordinates has the form

```text
alpha r0^2 + beta (r1^2 + r2^2).
```

The `C3` action removes cross terms:

```text
r0 r1, r0 r2, r1 r2.
```

But it does not fix the coefficient ratio `beta/alpha`.

Equivalently, after normalizing the doublet coefficient to `-1`, `C3` allows:

```text
Q_c = c r0^2 - (r1^2 + r2^2)
```

for any `c`.  The Koide support-chain quadratic is the special member:

```text
c = 2.
```

Thus the residual scalar is:

```text
c - 2.
```

## Hostile Review

This no-go does **not** use:

- `K_TL = 0`;
- source-freeness;
- `Q = 2/3` as a proof input;
- `delta = 2/9`;
- PDG masses;
- the observational `H_*` pin.

The desired value `c=2` is used only as the coefficient whose derivation is
being tested.  The audit therefore preserves support while preventing a
renamed primitive from being promoted as a theorem.

## Executable Result

```text
PASSED: 13/13

KOIDE_Q_ORBIT_DIMENSION_COEFFICIENT_NO_GO=TRUE
Q_ORBIT_DIMENSION_COEFFICIENT_CLOSES_Q=FALSE
RESIDUAL_SCALAR=c-2
```

## Consequence

The orbit-dimension route explains why `2` keeps reappearing in the support
package.  It does not derive the physical source-law coefficient.  Closure
still requires a retained law selecting

```text
c = 2
```

or equivalently the normalized traceless-source condition already isolated as
`K_TL = 0`.

## Musk Simplification Pass

This is the third failed route after the previous simplification pass:

1. selected-line Berry endpoint law for `delta`;
2. cyclic-compression scalar law for `Q`;
3. orbit-dimension coefficient law for `Q`.

The simplified state is:

1. **Make requirements less wrong:** the package does not need another broad
   carrier.  It needs one retained endpoint/source coefficient law.
2. **Delete:** route decoration can be stripped away.  Full-cube averaging,
   semigroup positivity, cyclic compression, orbit dimensions, and
   selected-line Berry geometry are support surfaces, not the missing law.
3. **Simplify:** the remaining tests should ask whether a proposed retained
   law fixes one scalar exactly:
   - `K_TL`;
   - `rho`;
   - `c - 2`;
   - `theta_end - theta0 - eta_APS`.
4. **Accelerate:** future runners should reject any route that only proves
   covariance, positivity, or support arithmetic without an equation for one
   of those scalars.
5. **Automate:** the hostile-review guard should check for disguised imports
   of `K_TL=0`, `Q=2/3`, `delta=2/9`, observational `H_*`, or endpoint/source
   primitives.
