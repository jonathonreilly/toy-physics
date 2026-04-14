# Hierarchy `Z_4` Spinor Selector Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_hierarchy_z4_spinor_selector.py`

## Question

Can the final hierarchy selector principle be tied to deeper framework
structure than the generic “uniform temporal orbit” rule?

## Stronger selector

Yes.

For fermions on the APBC temporal circle, the mode phases are:

`z_n = exp(i (2n+1) pi / L_t)`.

The deeper spinorial structure is not just a `Z_2` sign flip. Fermions live on
the double cover, so the minimal resolved phase cycle is naturally a
`Z_4` orbit:

`z_0 * {1, i, -1, -i}`.

On the APBC lattice, the unique even `L_t` for which the full temporal orbit is
exactly one such `Z_4` spinor orbit is:

`L_t = 4`.

## Why this improves the selector

The older selector principle was:

> choose the minimal resolved uniform orbit.

The stronger version is:

> choose the minimal APBC temporal orbit that realizes the full spinor
> `Z_4` cycle and therefore resolves the fermionic phase structure beyond the
> unresolved `Z_2` endpoint.

This is closer to the underlying framework because:

1. temporal APBC is already derived from spin-statistics
2. `L_t = 2` is only the unresolved sign-flip endpoint
3. `L_t = 4` is the first orbit with:
   - four distinct APBC phases
   - exact closure under `z -> i z`
   - exact closure under complex conjugation (time reversal)
   - exact closure under `z -> -z` (fermionic half-cycle sign)

So `L_t = 4` is the unique minimal orbit that resolves the full discrete
spinor phase cycle.

## Consequence for the hierarchy

The exact correction is again:

`C_phys = C(4) = (7/8)^(1/4)`

giving:

- baseline `253.4 GeV`
- selected value `245.08 GeV`
- measured value `246.22 GeV`
- relative error `0.46%`

## Honest status

This is the strongest closure route so far.

If one accepts:

> the EWSB order parameter must be built on the minimal resolved spinor
> temporal orbit rather than the unresolved sign-flip endpoint,

then the selector is no longer ad hoc and the hierarchy route is effectively
closed on the exact minimal block.

What still remains, at the strictest possible bar, is one final conceptual
step:

> prove that the physical EWSB order parameter must use the minimal resolved
> spinor `Z_4` orbit, rather than merely showing that this is the unique exact
> candidate.

So the mathematical structure is now very tight, but one interpretive bridge
still remains if the standard spinorial selector principle is not accepted.
