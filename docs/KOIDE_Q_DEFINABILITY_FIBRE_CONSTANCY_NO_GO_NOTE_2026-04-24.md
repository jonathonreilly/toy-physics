# Koide Q definability/fibre-constancy no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_definability_fibre_constancy_no_go.py`  
**Status:** no-go for retained-only proof; exact conditional theorem if the
physical source language forgets retained rank/orbit-type predicates

## Theorem Attempt

The next obstruction after the quotient universal-property audit is:

```text
derive_physical_readout_factorization_through_operational_quotient
```

For Q alone this is fibre constancy:

```text
p_plus = p_perp.
```

This route tries to derive that equality from definability/parametricity:

> If the physical charged-lepton source readout is definable only in the
> quotient language, then it cannot name the retained C3 representatives
> `{0}` and `{1,2}`.  The two fibre components are exchangeable, so the source
> must be uniform.

## Brainstormed Variants

1. **Pure quotient language:** no predicate distinguishes the two fibres.
2. **Parametricity:** all quotient-language definable source states are
   invariant under fibre swap.
3. **What if retained rank is physical?** Then rank/orbit size distinguishes
   the fibres and uniformity is not forced.
4. **What if rank is only bookkeeping?** Then a retained theorem must say rank
   is not a source-language predicate.
5. **What if source preparation is prior-like?** Then the rank-counting prior
   remains a definable nonclosing counterstate unless excluded.

## Conditional Positive Result

In the quotient language, the two source components have a swap automorphism.
For a normalized source:

```text
p = (u, 1-u)
```

swap invariance gives:

```text
u = 1-u
u = 1/2.
```

Therefore:

```text
K_TL = 0
Q = 2/3.
```

This is not a fitted Koide value.  The same computation gives uniformity on
any finite quotient orbit.

## Retained Countermodel

The current retained `Cl(3)/Z3` language contains the real block dimensions:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

Equivalently, the C3 orbit representatives are distinguishable:

```text
plus = {0}
perp = {1,2}.
```

The swap violates that rank/orbit-size predicate, so it is not an automorphism
of the retained labelled source object.  Normalization alone leaves:

```text
p = (u, 1-u)
```

free.

The retained-language definable rank-counting state is:

```text
p_plus = 1/(1+2) = 1/3
p_perp = 2/(1+2) = 2/3.
```

It gives:

```text
Q = 1
K_TL = 3/8
<Z> = -1/3.
```

So definability closes Q only after adding the physical theorem that the source
language forgets retained rank/orbit type.

## Hostile Review

- **Circular assumption:** exact.  Taking the quotient language as physical is
  equivalent to deleting the retained source label.
- **Target import:** none.  `Q=2/3` is computed after swap invariance.
- **Hidden observational pin:** none.
- **Missing axiom link:** exact.  Need a retained law that rank/orbit-size data
  are not physical source predicates.
- **Closure claim:** rejected for retained-only closure.

## Residual

```text
RESIDUAL_SCALAR =
  derive_physical_source_language_forgets_retained_rank_orbit_type

RESIDUAL_Q =
  fibre_constancy_excluding_rank_definable_source_state

COUNTERSTATE =
  rank_definable_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Musk Simplification Pass

1. **Make requirements less wrong:** the live requirement is not "derive
   uniformity"; it is "derive that rank/orbit-size is not source language."
2. **Delete:** category language can be deleted; the obstruction is a retained
   unary predicate distinguishing the two fibres.
3. **Simplify:** the proof is one automorphism equation `u=1-u` plus one
   counterpredicate `rank=(1,2)`.
4. **Accelerate:** future routes should test whether they exclude the
   rank-counting state `(1/3,2/3)`.
5. **Automate:** this runner guards against promoting quotient-language
   parametricity while retained rank predicates remain physical.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_definability_fibre_constancy_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DEFINABILITY_FIBRE_CONSTANCY_NO_GO=TRUE
Q_DEFINABILITY_FIBRE_CONSTANCY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_PHYSICAL_LANGUAGE_FORGETS_RANK_ORBIT_TYPE=TRUE
RESIDUAL_SCALAR=derive_physical_source_language_forgets_retained_rank_orbit_type
RESIDUAL_Q=fibre_constancy_excluding_rank_definable_source_state
COUNTERSTATE=rank_definable_w_plus_1_over_3_Q_1_K_TL_3_over_8
```
