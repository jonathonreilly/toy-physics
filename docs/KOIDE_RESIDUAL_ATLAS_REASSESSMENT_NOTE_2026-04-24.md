# Koide residual-atlas reassessment

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_residual_atlas_reassessment.py`  
**Status:** planning/review-control artifact; not closure

## Surviving residuals

After the finite-geometry, KMS, Maslov, and special-Frobenius audits, the lane
has collapsed to two live primitives.

For `Q`:

```text
derive the physical label-counting center source
equivalently: derive K_TL = 0
equivalently: justify the special Frobenius center counit over the rank trace.
```

For `delta`:

```text
derive theta_end - theta0 = eta_APS
equivalently: provide the selected-line open endpoint trivialization/functor.
```

## Forbidden closure moves

- Postulate `K_TL=0` or equal center labels.
- Postulate special Frobenius center source without a physical derivation.
- Choose a log-2 KMS sector gap by hand.
- Identify the open selected-line endpoint with `eta_APS` by endpoint gauge.
- Fit a smooth Berry integral or endpoint trivialization.
- Use PDG masses or `H_*` as source data.

## Ranked candidate queue

1. **Q: operational copy/delete theorem for center labels**  
   Can a physical copying/deleting principle force the label-counting dagger
   instead of the inherited rank dagger?

2. **Q: equivariant K-theory/index pairing**  
   Can a retained index pairing forbid the rank trace or force label count on
   the quotient?

3. **Q: Davies/Markov sector semigroup**  
   Can retained irreversible dynamics have unique stationary state `u=1/2`
   without chosen rates?

4. **Q: relative-entropy/least-distinguishable state**  
   Can a variational principle select the center state against the rank state
   without importing a target prior?

5. **Q: higher-order local `Cl(3)` source grammar**  
   Can all local equivariant source polynomials be exhausted beyond previous
   low-order audits?

6. **delta: spin-c/lens-space eta refinement**  
   Can spin structure or lens-space refinement identify the open selected-line
   endpoint?

7. **delta: open determinant functor trivialization**  
   Can a canonical determinant-line trivialization turn closed APS holonomy into
   the selected open phase?

8. **delta: denominator-9 Maslov refinement**  
   Can a retained orbifold/Maslov refinement produce `2/9` rather than
   denominator-12 data?

9. **joint: boundary anomaly inflow with center source**  
   Can one physical boundary theory derive both the label-counting source and
   the APS endpoint?

10. **Q: normalized special Frobenius retention theorem**  
    Can specialness be forced by topological boundary/unitarity rather than
    postulated?

## Next attack

The operational copy/delete route is the highest-value next attack because it
is the only route near a positive `Q` theorem: special Frobenius would derive
the correct source law, but it currently fails review as an unretained source
primitive.

## Closeout

```text
KOIDE_RESIDUAL_ATLAS_REASSESSMENT=TRUE
KOIDE_RESIDUAL_ATLAS_CLOSES_Q=FALSE
KOIDE_RESIDUAL_ATLAS_CLOSES_DELTA=FALSE
RESIDUAL_Q=justify_label_counting_center_source_equiv_K_TL
RESIDUAL_DELTA=theta_end-theta0-eta_APS
NEXT_ATTACK=operational_copy_delete_center_label_theorem
```
