# YT Ward-Ratio Stationarity No-Go Note

**Date:** 2026-05-01
**Status:** no-go / exact-negative-boundary
**Runner:** `scripts/frontier_yt_ward_ratio_stationarity_no_go.py`
**Certificate:** `outputs/yt_ward_ratio_stationarity_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: "Even a future Ward repair would not by itself derive beta_lambda(M_Pl)=0."
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The Ward ratio is forbidden as a PR #230 proof input and does not imply Planck beta stationarity."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

If the old Ward ratio

```text
y_t / g_s = 1 / sqrt(6)
```

were re-permitted in a future audit, would it imply

```text
beta_lambda(M_Pl) = 0?
```

## Verdict

No.

At the 3-loop Planck gauge point used by the double-criticality selector, the
one-loop beta-stationarity value is

```text
y_star(M_Pl) = 0.388965102494.
```

The Ward-ratio value at the same `g_3(M_Pl)` is

```text
y_ward(M_Pl) = g_3(M_Pl) / sqrt(6) = 0.198866111706.
```

Plugging the Ward-ratio value into the quartic beta function at `lambda=0`
gives

```text
beta_lambda(lambda=0, y_t=g_3/sqrt(6)) = 1.279548e-01,
```

not zero.

To make the Ward ratio and beta-stationarity coincide at the same electroweak
`g_1`, `g_2` point, one would need

```text
g_3(M_Pl) = sqrt(6) y_star = 0.952766,
```

while the selector's 3-loop Planck value is

```text
g_3(M_Pl) = 0.487121.
```

## Claim Boundary

This note does not rehabilitate the Ward route.  The `H_unit`/Ward chain
remains forbidden as a PR #230 proof input because it is the audited-renaming
trap.  The point here is narrower:

> even if the Ward ratio were repaired in a separate future audit, it would not
> automatically derive `beta_lambda(M_Pl)=0`.

Thus the Planck-stationarity blocker is independent of the Ward-renaming
blocker.

## Verification

```bash
python3 scripts/frontier_yt_ward_ratio_stationarity_no_go.py
# SUMMARY: PASS=7 FAIL=0
```
