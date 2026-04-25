# Koide primitive-based readout universal-property derivation no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_primitive_based_readout_universal_property_derivation_no_go.py`  
**Status:** no-go for retained-only derivation; exact conditional derivation
from quotient factorization

## Theorem Attempt

Try to derive the new physical law

```text
primitive_based_operational_boundary_readout
```

from the universal property of the operational quotient.  If this succeeds,
the law would no longer be an added primitive: it would be forced by the
retained quotient construction itself.

Precise theorem attempt:

> The retained charged-lepton readout functor is forced to factor through the
> operational quotient and to be based/primitive on the boundary.  Therefore
> source-visible C3 labels, spectator boundary channels, and endpoint-exact
> phase shifts are excluded by universal property alone.

## Exact Conditional Derivation

For the Q source, quotient factorization is exactly fibre constancy:

```text
p_plus = p_perp
p_plus + p_perp = 1
```

so:

```text
p_plus = p_perp = 1/2
K_TL = 0
Q = 2/3.
```

For delta, a based primitive boundary functor imposes:

```text
selected = 1
spectator = 0
c = 0
```

so:

```text
delta_open = eta_closed
```

for arbitrary closed eta.  The independent APS computation supplies:

```text
eta_APS = 2/9.
```

Thus the universal-property route proves the correct implication:

```text
fibre-constant based primitive quotient functor
  -> primitive-based readout law
  -> Q = 2/3 and delta = 2/9.
```

## Why This Still Fails As Retained-Only Proof

The universal property of a quotient applies only to functors already constant
on quotient fibres.  The retained embedded source category still allows a
label-visible functor:

```text
plus label = {0}
perp label = {1,2}
p_plus = 1/3
p_perp = 2/3
```

This functor is normalized but not fibre-constant:

```text
p_plus - p_perp = -1/3.
```

It gives:

```text
Q = 1
K_TL = 3/8.
```

Similarly, retained boundary affine data still allow:

```text
selected=1/2, spectator=1/2, c=0 -> delta_open=1/9
selected=1, spectator=0, c=1/9 -> delta_open=1/3.
```

So the universal property cannot be applied until the physical readout is
already known to factor through the quotient and to be based/primitive.

## Hostile Review

- **Circular assumption:** exact.  Assuming fibre constancy is assuming the Q
  part of the new law.
- **Target import:** none.  Values are computed after the symbolic constraints.
- **Hidden observational pin:** none.
- **Missing axiom link:** exact.  Need retained physics deriving readout
  factorization through the operational quotient.
- **Closure claim:** rejected for retained-only closure.

## Residual

```text
RESIDUAL_SCALAR =
  derive_physical_readout_factorization_through_operational_quotient

RESIDUAL_Q =
  fibre_constancy_excluding_source_visible_C3_labels

RESIDUAL_DELTA =
  primitive_based_boundary_functor_excluding_spectator_and_c
```

## Musk Simplification Pass

1. **Make requirements less wrong:** the universal property is not enough; the
   requirement is a retained factorization theorem for the physical readout.
2. **Delete:** remove category language when it only restates
   `p_plus=p_perp`; the live Q obstruction is fibre constancy.
3. **Simplify:** Q is one equation, `p_plus-p_perp=0`.
4. **Accelerate:** test any future route by asking whether it excludes the
   explicit functor `(1/3,2/3)`.
5. **Automate:** this runner prevents quotient universal-property language from
   being promoted as a derivation unless the factorization premise is proven.

## Verification

Run:

```bash
python3 scripts/frontier_koide_primitive_based_readout_universal_property_derivation_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_DERIVATION_NO_GO=TRUE
PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_Q_RETAINED_ONLY=FALSE
PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_DELTA_RETAINED_ONLY=FALSE
CONDITIONAL_CLOSURE_IF_FACTORING_BASED_PRIMITIVE_FUNCTOR=TRUE
RESIDUAL_SCALAR=derive_physical_readout_factorization_through_operational_quotient
```
