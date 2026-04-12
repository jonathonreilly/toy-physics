# SU(3) Native-Bridge Blocker Note

**Date:** 2026-04-12  
**Status:** BLOCKED on the current native `Cl(3)` surface  
**Script:** `scripts/frontier_su3_bivector_ks_bridge.py`

## Claim Under Review

Can the retained native `Cl(3)` / bivector weak lane be canonically bridged to
the Kawamoto-Smit (KS) factor `su(2)` used in the formal commutant theorem?

The stronger publication claim would require a basis-free intertwiner `U`
such that the native bivector generators are conjugate to the KS factor
generators in the precise sense needed by the `SU(3)` theorem.

## Verdict

**Not established on the current surface.**

The current review surface supports two separate facts:

1. The native staggered `Cl(3)` bivector lane exists and is stable.
2. The KS tensor-factor theorem gives a valid `su(3) \oplus u(1)` commutant
   on the KS surface.

What is missing is the canonical bridge between them.

## Why the bridge is blocked

The obstruction is not that the KS theorem fails. It does not. The obstruction
is that the native bivector data do not canonically determine the KS factor
decomposition.

On the native bivector surface:

- the `su(2)` action has a 4-dimensional multiplicity space
- the commutant is `16`-dimensional
- therefore there is a nontrivial `U(4)` freedom on the multiplicity space

That means the current native data do not pick out a unique intertwiner `U`.
Any bridge requires an extra selector:

- a canonical `S_3 -> Z_2` weak-axis choice, or
- an intrinsic order parameter that fixes the residual stabilizer, or
- another basis-free mechanism that reduces the native multiplicity freedom
  to the KS factorization

None of those are established by the current retained surface alone.

## Safe Paper Reading

The strongest defensible statement right now is:

> Within the KS tensor-factor realization, a distinguished `su(2)` together
> with the residual cubic swap has commutant `su(3) \oplus u(1)`.

What is **not** yet defensible is:

> Native cubic `Cl(3)` alone canonically derives the KS factor `su(2)` and
> therefore closes the full `SU(3)` lane.

## Required Next Step

If this lane is to close, the next theorem must construct a canonical selector
for the weak axis on the native taste surface and prove that the resulting
intertwiner is unique up to the allowed cubic/internal symmetries.

Until then, the bridge remains a review-only blocker.
