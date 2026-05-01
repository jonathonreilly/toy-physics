# YT QFP Selector No-Go Note

**Date:** 2026-05-01
**Status:** no-go / exact-negative-boundary for QFP-as-selector
**Runner:** `scripts/frontier_yt_qfp_selector_no_go.py`
**Certificate:** `outputs/yt_qfp_selector_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: "QFP remains useful bounded support for transport robustness after a UV boundary condition is supplied."
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "IR quasi-fixed-point focusing compresses trajectories but does not select one without a UV boundary condition."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Can the top Yukawa be derived from IR quasi-fixed-point focusing alone, without
the direct MC route, the old Ward route, or Planck stationarity?

## Verdict

No.

Quasi-fixed-point focusing is useful bounded support for transport robustness.
It is not a selector.

The runner isolates the basic Pendleton-Ross mechanism in a simplified
one-loop flow.  It confirms that the IR flow compresses the UV range, but a
family remains:

| Test | Result |
|---|---|
| UV spread `[0.20, 0.80]` | compressed to IR spread `0.205` |
| Local response near Ward proxy | `dy_t(v)/dy_t(M_Pl) = 0.247` |
| Selector status | nonunique; UV boundary remains load-bearing |

Thus QFP focusing can reduce sensitivity to a UV boundary condition.  It
cannot replace that boundary condition.

## Authority Boundary

[YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
already states `Status: bounded support`.  It assumes a gauge anchor and a UV
boundary condition.  This note prevents that support result from being
misread as a retained selector theorem.

## Relationship To PR #230

The QFP route does not rescue full retained closure for PR #230.  The live
routes remain:

- production correlator measurement plus independent mass pin;
- a repaired/audited UV boundary condition;
- Planck stationarity if separately derived;
- explicit conditional selector if adopted as a new premise.

## Verification

```bash
python3 scripts/frontier_yt_qfp_selector_no_go.py
# SUMMARY: PASS=7 FAIL=0
```
