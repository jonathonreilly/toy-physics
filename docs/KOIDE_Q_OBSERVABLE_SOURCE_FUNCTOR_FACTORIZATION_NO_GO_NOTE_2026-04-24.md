# Koide Q observable-source functor factorization no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_observable_source_functor_factorization_no_go.py`  
**Status:** no-go; observable principle does not by itself retain the needed
source-domain quotient

## Theorem Attempt

Derive quotient-center anonymity by proving that the physical charged-lepton
source functor factors through the reduced scalar observable-jet quotient.  The
observable jets of the two normalized first-live slots agree, so this
factorization would erase `C3` orbit type and force the uniform center state.

## Result

Negative under current retained structure.

The observable principle fixes:

```text
W[J] = log |det(D+J)| - log |det D|
```

and scalar observables as source derivatives.  But its source domain still
contains central source projectors.  On the retained charged-lepton carrier:

```text
P_plus = C3 singlet projector
P_perp = real-doublet projector
Z = P_plus - P_perp
```

The runner verifies:

```text
[C3, P_plus] = 0
[C3, P_perp] = 0
C3 Z C3^-1 = Z
Z^2 = I.
```

So `Z` is a retained, central, `C3`-invariant label coordinate.

## Counterfunctor

A label-dependent source

```text
K = a I + b Z
```

is `C3`-equivariant and compatible with the source-response domain.  Trace
normalization removes `a`, but leaves `b`, exactly the `K_TL` source direction.

The state-level version is:

```text
K_TL = 0 <=> w = 1/2
```

but a retained label-visible source state may use:

```text
w = 1/3 -> Q = 1, K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR = source_domain_factorization_excluding_C3_label_map_Z
RESIDUAL_PRIMITIVE =
  derive_physical_source_domain_forgets_retained_C3_orbit_label
```

## Hostile Review

- **Target import:** none.  The target midpoint appears only as the residual
  condition.
- **External empirical mass/witness input:** none.
- **Hidden source-free law:** none promoted.
- **Missing axiom link:** exact.  The observable principle tells how to read
  scalar responses once a source direction is supplied; it does not forbid the
  retained central label direction `Z` as source-visible data.
- **Closure claim:** rejected.  The runner prints
  `Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_CLOSES_Q=FALSE`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_observable_source_functor_factorization_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
PASSED: 12/12
KOIDE_Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_NO_GO=TRUE
Q_OBSERVABLE_SOURCE_FUNCTOR_FACTORIZATION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=source_domain_factorization_excluding_C3_label_map_Z
RESIDUAL_PRIMITIVE=derive_physical_source_domain_forgets_retained_C3_orbit_label
```

## Consequence

The observable-jet quotient remains the closest conditional positive route, but
positive retention still requires an independent theorem excluding the retained
`C3` label map `Z` from physical source preparation.
