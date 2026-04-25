# Koide delta selected-line locality derivation theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py`  
**Status:** defense theorem for selected-line local endpoint source domain

## Objection Defended

A reviewer may say:

```text
"End(L_chi), not End(V), is a new physical law."
```

This note records the defense: `End(L_chi)` is the pullback-local source
algebra of the retained selected-line endpoint map.  Ambient `End(V)` sources
require an additional normal/complement endpoint source coordinate.

## Theorem

At each selected-line endpoint, the retained Brannen map includes the
tautological fibre:

```text
i_chi: L_chi -> V.
```

The pullback of ambient endomorphisms is:

```text
A -> i_chi^* A i_chi.
```

For the selected projector `P_chi` and normal complement `Q_chi = I-P_chi`:

```text
i_chi^* P_chi i_chi = 1
i_chi^* Q_chi i_chi = 0.
```

Thus a normal-complement source is invisible to the selected-line endpoint
pullback.  Retaining it as physical data enlarges the source domain from the
selected-line endpoint to an ambient endpoint with an additional normal probe.

## Source-Rank Statement

The selected-line local endpoint probe has one source coordinate:

```text
J_local = j P_chi.
```

Ambient endpoint sources have two independent coordinates:

```text
J_ambient = j_sel P_chi + j_norm Q_chi.
```

The `j_norm` coordinate is not supplied by the retained selected-line endpoint.
Adding it is exactly the extra physical input that the older mixed-source
counterstates require.

## Consequence

For a selected-line local positive source:

```text
rho = lambda P_chi.
```

Normalization gives:

```text
lambda = 1,
rho = P_chi.
```

Therefore:

```text
selected_channel = 1
spectator_channel = 0.
```

## Falsifier

Retain a physical normal endpoint source:

```text
j_norm != 0.
```

That would enlarge the endpoint source domain to ambient `End(V)` and reopen
the selected/spectator mixture family.

## Verification

```bash
python3 scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py
python3 -m py_compile scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py
```

Expected closeout:

```text
KOIDE_DELTA_SELECTED_LINE_LOCALITY_DERIVATION_THEOREM=TRUE
END_LCHI_SOURCE_DOMAIN_DERIVED_FROM_PULLBACK_LOCALITY=TRUE
AMBIENT_ENDV_ENDPOINT_SOURCE_REQUIRES_EXTRA_NORMAL_PROBE=TRUE
DELTA_ORIENTED_SELECTED_ENDPOINT_MARK_DEFENDED=TRUE
NO_TARGET_IMPORT=TRUE
FALSIFIER=retained_physical_normal_endpoint_source_j_norm
```
