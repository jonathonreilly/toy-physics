# YT RGE-Only Selector No-Go Note

**Date:** 2026-05-01
**Status:** no-go / exact-negative-boundary for RGE-only selector
**Runner:** `scripts/frontier_yt_rge_only_selector_no_go.py`
**Certificate:** `outputs/yt_rge_only_selector_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: "The SM/QCD RGE bridge remains valid transport once a boundary condition is supplied."
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "RGE flow transports a boundary value; it does not choose the boundary value."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Can the SM RGE bridge itself select `y_t` without direct production data, Ward
repair, observed-mass admission, or Planck stationarity?

## Verdict

No.

The RGE is a transport map, not a selector.  Given a weak-scale or UV boundary
condition it predicts the value at another scale.  Without that boundary
condition, it carries a continuum of trajectories.

The runner demonstrates this in a deliberately simplified one-loop flow with
fixed gauge couplings.  Different weak-scale `y_t(v)` inputs remain distinct at
`M_Pl`; the RGE map is monotonic over the tested interval and leaves a
nonzero family spread.

## Relationship To Other PR #230 Routes

This no-go is separate from the Planck double-criticality selector.  In that
route, the selector is the extra boundary condition

```text
lambda(M_Pl) = 0
beta_lambda(M_Pl) = 0
```

The RGE bridge only transports the result.  Since
`beta_lambda(M_Pl)=0` is not derived on the current surface, the Planck route
remains conditional support rather than retained closure.

## Verification

```bash
python3 scripts/frontier_yt_rge_only_selector_no_go.py
# SUMMARY: PASS=7 FAIL=0
```
