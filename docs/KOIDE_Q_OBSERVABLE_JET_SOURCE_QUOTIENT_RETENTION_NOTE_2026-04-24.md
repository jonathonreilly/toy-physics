# Koide Q observable-jet source-quotient retention attack

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_observable_jet_source_quotient_retention.py`  
**Status:** conditional positive route; not retained closure

## Theorem Attempt

Use the already-retained scalar observable principle to force the physical
charged-lepton source to factor through the reduced observable-jet quotient.
On that quotient the two normalized first-live second-order slots have the
same scalar jet.  If source preparation sees only that quotient, the source
object has a transitive `S2` swap, so naturality forces the uniform center
state.

## Result

The runner verifies the conditional positive theorem:

```text
W_red = log(1+k_+) + log(1+k_perp)
one-slot jets at zero agree
observable-jet quotient Aut = S2
Aut-invariant source state -> w_+ = 1/2
K_TL = 0
Y = I_2
E_+ = E_perp
kappa = 2
Q = 2/3
```

This is the cleanest route so far for deriving the exact source invisibility
needed by quotient-center anonymity.

## Retention Failure

The retained `Cl(3)/Z3` carrier still supplies a label-valued map:

```text
P_plus orbit = {0}
P_perp orbit = {1,2}
```

A source functor allowed to see those retained labels has only the identity
automorphism:

```text
Aut_retained = {id}.
```

Then every center state `(w,1-w)` is natural.  In particular:

```text
w=1/3 -> Q=1, K_TL=3/8.
```

Therefore the observable-jet route closes `Q` only after the additional
factorization theorem:

```text
physical charged-lepton source preparation factors through the reduced
observable-jet quotient and not through retained C3 orbit labels.
```

## Exact Residual

```text
RESIDUAL_SCALAR = source_functor_jet_factorization_residual
RESIDUAL_PRIMITIVE =
  derive_physical_source_functor_factors_through_observable_jet_quotient
```

## Hostile Review

- **Target import:** none.  `Q=2/3` appears only as the consequence of the
  uniform quotient state.
- **PDG/H_* pin:** none.
- **Hidden source-free law:** not promoted.  The runner explicitly keeps the
  retained closeout flag false.
- **Missing axiom link:** the missing link is now precise: observable principle
  fixes scalar readouts, but does not by itself forbid label-valued source
  preparation.
- **Overbroad claim:** rejected.  This is a conditional positive route, not a
  retained closure packet.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_observable_jet_source_quotient_retention.py
```

Expected closeout:

```text
PASSED: 14/14
KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_RETENTION=CONDITIONAL
KOIDE_Q_OBSERVABLE_JET_SOURCE_QUOTIENT_CLOSES_Q=FALSE
CONDITIONAL_Q_CLOSURE_IF_SOURCE_FACTORS_THROUGH_OBSERVABLE_JET=TRUE
RESIDUAL_SCALAR=source_functor_jet_factorization_residual
RESIDUAL_PRIMITIVE=derive_physical_source_functor_factors_through_observable_jet_quotient
```

## Next Route

The next positive route should attack the residual directly: prove that a
physical source prepared from the retained Grassmann scalar generator is a
natural transformation of observable jets, not of embedded `C3` character-orbit
labels.  If that cannot be derived, the source-domain factorization is a new
selector primitive.
