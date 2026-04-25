# Koide dimensionless source-domain closure Nature review

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_dimensionless_source_domain_closure_nature_review.py`  
**Status:** positive closure packet for the dimensionless charged-lepton Koide lane

## Closure Statement

The dimensionless charged-lepton Koide lane closes from two retained
source-domain theorems.

## Q

The retained determinant generator uses `J` as a probe source:

```text
W[J] = log |det(D+J)| - log |det D|.
```

Scalar observables are Taylor coefficients at the undeformed theory `J=0`.
On the normalized two-channel carrier this gives:

```text
Y = (1,1)
K_TL = 0
Q = 2/3.
```

The undeformed-background exclusion theorem sharpens the broad `J0` objection.
Writing

```text
J0 = (s+z, s-z),
```

only the traceless component `z` can change dimensionless Q.  The common
component `s` cancels from Q and belongs to the separate `v0`/scale boundary.

## Delta

The physical selected endpoint source is local to the selected-line boundary
point, so its source algebra is:

```text
End(L_chi),
```

not ambient:

```text
End(V).
```

This is defended by the selected-line locality derivation theorem.  The
pullback of ambient endomorphisms along

```text
i_chi: L_chi -> V
```

kills the normal complement:

```text
i_chi^* Q_chi i_chi = 0.
```

Retaining ambient `End(V)` endpoint sources therefore requires an additional
normal source coordinate:

```text
j_norm.
```

The normal endpoint-source exclusion theorem then shows that `j_norm` alone is
still pullback-kernel data for selected-line local readout.  It can affect
delta only if a separate normal endpoint observable or ambient trace
normalization is retained and coupled to the endpoint readout.

The normalized positive source in `End(L_chi)` is uniquely:

```text
P_chi.
```

Therefore:

```text
selected_channel = 1
spectator_channel = 0.
```

The retained real selected-line section fixes the endpoint basepoint:

```text
c = 0.
```

With the independent APS/ABSS value:

```text
eta_APS = 2/9,
```

the physical endpoint is:

```text
delta_physical = 2/9.
```

## Hostile Review

- **No target import:** `Q` follows after probe-source coefficient evaluation;
  `delta` follows after selected-line local source support and basepoint
  trivialization.
- **Old no-gos remain valid:** they apply to broader source domains: nonzero
  undeformed charged-lepton source backgrounds and ambient `End(V)` endpoint
  sources.
- **Exact falsifiers:** retain either a native traceless undeformed source
  background `z != 0` or a normal endpoint observable / ambient normalization
  coupled to delta.
- **Boundary:** the overall lepton scale `v0` is not addressed.

## Verification

```bash
python3 scripts/frontier_koide_dimensionless_source_domain_closure_nature_review.py
python3 scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py
python3 scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py
python3 scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py
python3 -m py_compile scripts/frontier_koide_dimensionless_source_domain_closure_nature_review.py
```

Expected closeout:

```text
KOIDE_DIMENSIONLESS_SOURCE_DOMAIN_CLOSURE_NATURE_REVIEW=PASS
KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE
KOIDE_DELTA_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=TRUE
KOIDE_FULL_DIMENSIONLESS_LANE_SOURCE_DOMAIN_CLOSURE=TRUE
Q_PHYSICAL=2/3
DELTA_PHYSICAL=2/9
NO_TARGET_IMPORT=TRUE
FALSIFIERS=retained_traceless_background_z_ne_0_or_retained_normal_endpoint_observable_coupled_to_delta
BOUNDARY=overall_lepton_scale_v0_not_addressed
```
