# Koide Q/delta retained observable-completeness no-hidden-boundary no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_delta_retained_observable_completeness_no_hidden_boundary_no_go.py`  
**Status:** no-go; retained observable completeness does not derive the
primitive-based no-hidden-boundary law

## Theorem Attempt

Remove the remaining primitive-based readout condition by strengthening
retained observability to observable completeness:

```text
all physically retained charged-lepton source and endpoint observables factor
through the operational quotient;
kernel labels, spectator channels, and endpoint-exact lifts are gauge.
```

If this were derived, the earlier new-law closure packet would become retained:

```text
source quotient orbit -> w_plus = w_perp -> K_TL = 0 -> Q = 2/3
primitive based endpoint -> delta_open = eta_APS = 2/9.
```

## Result

Negative from the current retained packet.  Observable completeness has two
inequivalent meanings, and neither gives retained closure.

## Q Obstruction

Completing the current retained source algebra keeps the central label

```text
Z = P_plus - P_perp.
```

The runner verifies:

```text
C3 Z C3^-1 = Z
Z^2 = I.
```

On the reduced two-slot source state,

```text
<I> = 1
<Z> = 2w - 1.
```

Thus quotient observables are blind to `w`, but the complete retained algebra
distinguishes the non-midpoint states.  Example:

```text
w = 1/3
<Z> = -1/3
K_TL = 3/8
Q = 1.
```

So retained completeness does not delete `Z`; it makes `Z` a legitimate
distinguishing source observable unless a further quotient law is added.

## Delta Obstruction

The independent APS computation fixes the closed value:

```text
eta_APS = 2/9.
```

After total anomaly normalization the exact open residual is:

```text
delta_open / eta_APS - 1 = -spectator + c / eta_APS.
```

At `eta_APS = 2/9` this is:

```text
delta_open / eta_APS - 1 = -spectator + (9/2)c.
```

The retained Wilson/APS boundary mark is scalar on the rank-two multiplicity
space, so it cannot select a unique primitive rank-one Brannen line.  The
closed observables have zero Jacobian on `(spectator, c)`.

Exact countermodels preserve the retained closed totals but change the open
endpoint:

```text
closing:   spectator=0,   c=0   -> delta_open=2/9
spectator: spectator=1,   c=0   -> delta_open=0
mixed:     spectator=1/2, c=0   -> delta_open=1/9
shifted:   spectator=0,   c=1/9 -> delta_open=1/3
```

## Completeness Fork

There are two possible principles:

```text
complete retained observable algebra
  keeps Z and leaves boundary spectator/exact endpoint coordinates unresolved;

complete operational quotient algebra
  deletes Z, spectator channel, and endpoint-exact lift.
```

The second principle is exactly the primitive-based operational boundary
readout law.  It is a viable new-law closure packet, but it is not derived by
the current retained structures.

## Residual

```text
RESIDUAL_SCALAR = quotient_complete_observable_algebra_not_retained
RESIDUAL_Q = source_domain_factorization_excluding_C3_label_map_Z
RESIDUAL_DELTA = primitive_selected_boundary_channel_and_based_endpoint_lift
NEXT_THEOREM = derive_quotient_completeness_or_keep_new_law_status
```

## Falsifiers

- A retained theorem proving `Z` is not a physical charged-lepton source
  observable even though it is central and `C3` invariant.
- A retained non-scalar boundary mark selecting the primitive rank-one Brannen
  line.
- A retained based endpoint-section theorem forcing `c = 0`.
- A derivation that observable completeness must be applied only after the
  operational quotient, without importing that quotient as a new law.

## Hostile Review

- **Target import:** none.  The target values appear only as consequences of
  quotienting or as countermodel comparisons.
- **Hidden fitted value:** none; all residual variables are symbolic.
- **Closure claim:** rejected for retained-only status.  The runner prints
  negative closeout flags for Q, delta, and the full lane.
- **Boundary:** the primitive-based packet remains a positive new-law closure,
  not a retained-only closure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_retained_observable_completeness_no_hidden_boundary_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_NO_HIDDEN_BOUNDARY_NO_GO=TRUE
Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_Q=FALSE
Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_DELTA=FALSE
Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_FULL_LANE=FALSE
RESIDUAL_SCALAR=quotient_complete_observable_algebra_not_retained
RESIDUAL_Q=source_domain_factorization_excluding_C3_label_map_Z
RESIDUAL_DELTA=primitive_selected_boundary_channel_and_based_endpoint_lift
```
