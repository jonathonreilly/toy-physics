# Koide delta selected-line local boundary-source Nature review

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py`  
**Status:** adversarial review pass for delta endpoint mark/basepoint closure

## Review Target

The theorem under review derives the two live delta endpoint primitives:

```text
selected_channel = 1
spectator_channel = 0
c = 0
```

from selected-line local boundary-source physics.

The load-bearing move is a source-domain theorem:

```text
physical endpoint source algebra = End(L_chi)
```

where `L_chi` is the pulled-back tautological fibre on the actual selected-line
`CP1` carrier.  It is not the ambient full-block algebra:

```text
End(V).
```

## Verdict

The review accepts the theorem as a positive delta endpoint closure under
retained selected-line local boundary-source semantics.

The normalized positive source in `End(L_chi)` is uniquely:

```text
P_chi = |chi><chi|.
```

Therefore:

```text
selected_channel = 1
spectator_channel = 0.
```

The retained real selected-line section fixes the unphased endpoint:

```text
theta0 = 2 pi / 3,
endpoint(theta0) = 0 -> c = 0.
```

With the independent APS value:

```text
eta_APS = 2/9,
```

the open endpoint is:

```text
delta_physical = eta_APS = 2/9.
```

## Hostile Review Answers

- **Target import:** no.  The support theorem is symbolic in `eta`; `2/9`
  enters only after `selected_channel=1` and `c=0` are derived.
- **Fitted selected weight:** no.  The weight is forced by the one-dimensional
  algebra `End(L_chi)`.
- **Endpoint offset:** no.  The offset is fixed by the based real selected-line
  section, not by the APS value.
- **Old no-gos:** compatible.  They allowed ambient `End(V)` mixed/full-block
  sources; this theorem restricts physical endpoint sources to selected-line
  local `End(L_chi)`.
- **Falsifier:** show that the physical endpoint source is an ambient
  rank-two density rather than a selected-line local source.

## Boundary

This closes the delta endpoint mark and basepoint problem.  It does not address
the Q/source closure question or the overall lepton scale `v0`.

## Verification

```bash
python3 scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py
python3 -m py_compile scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py
```

Expected closeout:

```text
KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW=PASS
KOIDE_DELTA_ENDPOINT_MARK_AND_BASEPOINT_CLOSED=TRUE
KOIDE_DELTA_ENDPOINT_CLOSED_RETAINED_SELECTED_LINE_LOCAL_SOURCE=TRUE
DELTA_PHYSICAL=ETA_APS=2/9
NO_TARGET_IMPORT=TRUE
FALSIFIER=physical_endpoint_source_is_ambient_EndV_density_not_selected_line_local_source
BOUNDARY=Q_source_status_and_overall_lepton_scale_v0_not_addressed
```
