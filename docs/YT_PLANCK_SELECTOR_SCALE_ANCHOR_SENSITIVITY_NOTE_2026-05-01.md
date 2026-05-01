# YT Planck Selector Scale-Anchor Sensitivity Note

**Date:** 2026-05-01
**Status:** conditional-support / assumption-sensitivity boundary
**Runner:** `scripts/frontier_yt_planck_selector_scale_anchor_sensitivity.py`
**Certificate:** `outputs/yt_planck_selector_scale_anchor_sensitivity_2026-05-01.json`

```yaml
actual_current_surface_status: conditional-support / assumption-sensitivity boundary
conditional_surface_status: "Planck double-criticality needs fixed dimensional endpoint anchors and the SM RGE bridge."
hypothetical_axiom_status: "Planck stationarity selector beta_lambda(M_Pl)=0."
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Changing the M_Pl/v running interval changes the selected one-loop boundary value."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Does the Planck double-criticality selector remain invariant if the dimensional
running anchors are varied?

The route uses a boundary-value bridge from `v` to `M_Pl`.  This note tests
whether that bridge is inert or load-bearing.

## Verdict

It is load-bearing.

At the one-loop analytic-selector level, changing the running interval changes
the gauge values at `M_Pl`, and therefore changes the selected
`y_t(M_Pl)`.

The runner finds:

| Anchor variation | One-loop selected `y_t(M_Pl)` shift |
|---|---:|
| unreduced to reduced Planck mass | `0.126%` |
| factor-10 Planck anchor scan | up to `0.196%` |
| `v` endpoint shifted by 5% | up to `0.0031%` |

The effect is not the dominant blocker; `beta_lambda(M_Pl)=0` remains the
primary missing premise.  But the test confirms that the non-MC selector is
not a pure algebraic statement independent of scale-setting and running
conventions.

## Claim Boundary

For retained closure, the criticality route would need:

1. a derivation of `beta_lambda(M_Pl)=0`;
2. retained electroweak gauge boundary data;
3. retained dimensional endpoint anchors;
4. a retained or explicitly bounded SM RGE bridge and scheme convention.

Without these, the route is a conditional consequence map.

## Verification

```bash
python3 scripts/frontier_yt_planck_selector_scale_anchor_sensitivity.py
# SUMMARY: PASS=7 FAIL=0
```
