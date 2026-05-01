# YT Planck Selector Gauge-Input Sensitivity Note

**Date:** 2026-05-01
**Status:** conditional-support / assumption-sensitivity boundary
**Runner:** `scripts/frontier_yt_planck_selector_gauge_input_sensitivity.py`
**Certificate:** `outputs/yt_planck_selector_gauge_input_sensitivity_2026-05-01.json`

```yaml
actual_current_surface_status: conditional-support / assumption-sensitivity boundary
conditional_surface_status: "Planck double-criticality selects y_t only after gauge boundary inputs and beta_lambda(M_Pl)=0 are supplied."
hypothetical_axiom_status: "Planck stationarity selector beta_lambda(M_Pl)=0."
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The selector is a family unless electroweak gauge boundary data are fixed by upstream authority."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Assume, for stress testing, that the missing stationarity premise is granted:

```text
lambda(M_Pl) = 0
beta_lambda(M_Pl) = 0
```

Does this alone select a unique top Yukawa value?

## Verdict

No.  It selects `y_t` only after gauge boundary data are fixed.

At one loop, with `lambda=0`, the selector is

```text
y_t^4 = (1/16) [ 2 g_2^4 + (g_2^2 + g'^2)^2 ].
```

So the selected `y_t(M_Pl)` is a function of `g_1(M_Pl)` and `g_2(M_Pl)`.
If those gauge values move, the selected Yukawa moves.  If they are not fixed
by retained upstream authority, the route is a family rather than a
single-number derivation.

## Assumption Sensitivity

The runner checks two sensitivity classes:

1. common rescaling of the Planck electroweak gauge boundary;
2. perturbing the weak-scale gauge inputs that are run up to the Planck scale.

Results:

| Test | Result |
|---|---|
| Common Planck gauge rescaling | `y_t(M_Pl)` rescales homogeneously at one loop. |
| 20% gauge-boundary scan | `y_t(M_Pl)` spread is `0.155103`. |
| Weak-scale `g_1`, `g_2` perturbations | One-loop selected `y_t(M_Pl)` moves by up to `2.939%` in the tested range. |
| `alpha_s` at one loop | Does not enter the one-loop `lambda=0` selector value, though it matters in higher-loop running. |

## Claim Boundary

This does not invalidate the Planck double-criticality selector.  It clarifies
its import ledger:

- `beta_lambda(M_Pl)=0` is still the main missing stationarity premise;
- the electroweak gauge boundary inputs are also load-bearing for the selected
  numerical value;
- observed `y_t`, `m_t`, and `m_H` remain comparators only.

Therefore the non-MC route cannot be promoted as a retained single-number
derivation from the criticality equations alone.

## Verification

```bash
python3 scripts/frontier_yt_planck_selector_gauge_input_sensitivity.py
# SUMMARY: PASS=8 FAIL=0
```
