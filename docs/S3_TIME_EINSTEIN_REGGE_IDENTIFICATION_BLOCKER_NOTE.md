# Route 2 Einstein/Regge Identification Blocker on the Restricted Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** sharp blocker, not an identification theorem

## Verdict

Route 2 now has an exact microscopic bilinear carrier and an exact tensorized
construction on the current restricted class:

- exact carrier: `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`
- exact tensorized action: `I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`
- exact spacetime carrier: `Xi_TB(t ; q) = vec K_R(q) \otimes exp(-t Lambda_R) u_*`

But these objects are still only a **construction** on the retained route-2
surface. The current atlas does not yet supply an exact theorem showing that
this construction is the Einstein/Regge tensor dynamics law on the current
restricted class.

## Exact facts already in hand

1. `S^3` compactification is exact.
2. anomaly-forced time is exact and single-clock.
3. the current route-2 background is `PL S^3 x R`.
4. the scalar Schur boundary action is exact on the restricted strong-field
   class.
5. the exact bilinear carrier `K_R` is exact on the microscopic support block.
6. the exact tensorized construction `I_TB` and `Xi_TB` are exact algebraic
   builds from those exact inputs.

## Sharp blocker

The missing theorem is not another carrier, not another transfer matrix, and
not a new class-widening step.

The missing theorem is:

> an exact dynamics-bridge / uniqueness theorem that identifies the exact
> carrier-action package with the Einstein/Regge tensor law on the current
> restricted class.

Equivalently:

- the current route-2 stack is exact as kinematics and as a tensorized
  construction
- it is still not exact as the GR dynamics law itself

## Why the identification is blocked

The route-2 action remains a quadratic tensorized penalty around the exact
carrier `K_R`:

- `I_TB = I_R + 1/2 ||a - vec K_R||^2`

That is enough to organize the retained tensor channels, but not enough to
prove that the resulting dynamics is uniquely the Einstein/Regge tensor law.
The atlas still lacks an exact `PL S^3 x R` dynamics bridge or a uniqueness
theorem forcing the GR metric law from the retained route-2 primitives alone.

So the remaining blocker is still **identification-level**, not class-widening.
The restricted class is already the right working surface; what is missing is
the exact theorem that ties the exact carrier/action to the Einstein/Regge law.

## What would close it

Any one of the following would close the blocker:

1. an exact `PL S^3 x R` dynamics action whose Euler-Lagrange equations are
   the Einstein/Regge equations on the restricted class
2. an exact spacetime-lift observable whose variational content reconstructs
   the same tensor dynamics
3. a uniqueness theorem showing that the exact route-2 carrier/action is the
   only compatible tensor dynamics on the restricted class

## Bottom line

The exact Route-2 carrier/action is real, but the exact Einstein/Regge
identification is still open.

The blocker is:

- exact carrier/action: yes
- exact GR dynamics identification: no
- remaining issue: identification, not class widening
