# YT Planck Double-Criticality Selector Note

**Date:** 2026-04-30  
**Status:** conditional-support / open selector route  
**Runner:** `scripts/frontier_yt_planck_double_criticality_selector.py`  
**Certificate:** `outputs/yt_planck_double_criticality_selector_2026-04-30.json`

```yaml
actual_current_surface_status: conditional-support / open selector route
conditional_surface_status: "If beta_lambda(M_Pl)=0 is derived from the Cl(3)/Z^3 substrate, this becomes a candidate non-MC y_t selector."
hypothetical_axiom_status: "Planck double-criticality: lambda(M_Pl)=0 and beta_lambda(M_Pl)=0."
admitted_observation_status: "y_t(v), m_H, m_t, and 1/sqrt(6) appear only as after-the-fact comparators."
proposal_allowed: false
proposal_allowed_reason: "The route depends on the new beta_lambda(M_Pl)=0 selector premise, which is not derived in this note."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Summary

This note records a route reset for the `y_t` lane.  Instead of trying to
pin the top mass directly from a month-scale lattice Monte Carlo campaign, it
tests whether the Higgs-sector Planck boundary can select the top Yukawa:

```text
lambda(M_Pl) = 0
beta_lambda(M_Pl) = 0
```

Given the weak-scale gauge inputs used by the framework Higgs runner, the
runner solves a boundary-value problem:

1. choose `g_1(M_Pl)`, `g_2(M_Pl)`, and `g_3(M_Pl)`;
2. impose `lambda(M_Pl)=0`;
3. solve `beta_lambda(M_Pl)=0` for `y_t(M_Pl)`;
4. run the full SM RGE system down to `v`;
5. tune only the Planck-scale gauge boundary values so the low-scale gauge
   couplings match the framework gauge inputs.

No observed top mass or observed `y_t` value is used by the solve.  The
accepted `y_t(v)` and Higgs mass values are comparators after the result is
computed.

## Numerical Result

The strict 3-loop boundary-value solve gives:

| Loop order | `y_t(M_Pl)` | `y_t(v)` | `lambda(v)` | `m_H` from `lambda(v)` |
|---:|---:|---:|---:|---:|
| 1 | 0.3877569751 | 0.9006132253 | 0.1275251922 | 124.379013 GeV |
| 2 | 0.3886073755 | 0.9249614221 | 0.1344526964 | 127.712637 GeV |
| 3 | 0.3887468134 | 0.9208739295 | 0.1315645095 | 126.333488 GeV |

Comparator readout:

| Quantity | Selector readout | Comparator | Difference |
|---|---:|---:|---:|
| `y_t(v)` | 0.9208739295 | 0.9176 | 0.3568% |
| `m_H` | 126.333488 GeV | 125.25 GeV | 1.083488 GeV |
| `y_t(v)/g_3(v)` | 0.8082488311 | `1/sqrt(6)=0.4082482905` | not imposed |

The 2-loop to 3-loop `y_t(v)` spread is `0.4439%`; the 1-loop to 3-loop
spread is `2.2002%`.  This is good enough to justify treating the route as a
serious candidate, not enough to claim closure.

## Why This Is Different From The Failed Top-Sector Routes

The route does not use:

- the `H_unit` matrix element;
- the old `yt_ward_identity_derivation_theorem`;
- a definition of `y_t_bare`;
- a top-quark correlator;
- an observed top mass target;
- the identity `y_t/g_s = 1/sqrt(6)`.

The selected `y_t(v)` is the output of the Planck double-criticality boundary
solve.  The ratio `y_t(v)/g_3(v)` is reported only as a diagnostic and is not
set to the Ward value.

## Load-Bearing Input

The load-bearing new premise is exactly:

```text
beta_lambda(M_Pl) = 0
```

The framework already uses `lambda(M_Pl)=0` as the Higgs classicality boundary.
This note does not prove that classicality also forces beta-function
stationarity.  That proof is now the narrowed hard problem.

The low-scale gauge inputs are the same framework-side gauge values used by
the full 3-loop Higgs runner:

```text
g_1(v) = 0.464
g_2(v) = 0.648
alpha_s(v) = 0.1033
```

Those gauge inputs must remain separately audited.  The selector does not
repair the gauge-input authority chain by itself.

## Claim Boundary

This note supports the following statement:

> Conditional on a substrate derivation of Planck double-criticality
> (`lambda=0` and `beta_lambda=0` at `M_Pl`), the SM RGE boundary-value
> problem selects `y_t(v)=0.9208739295` at 3-loop order, within `0.3568%` of
> the accepted top-Yukawa comparator, without using the old Ward/H-unit chain
> or an observed top-mass target.

This note does not claim:

- an audit-ratified derivation of `y_t`;
- a direct lattice measurement of `m_t`;
- closure of the top pole mass conversion;
- derivation of `beta_lambda(M_Pl)=0`;
- derivation of the weak-scale gauge inputs;
- replacement of the direct-correlator PR #230 lane as an audited-clean
  result.

## Next Hard Problem

The next useful physics-loop target is narrow:

```text
derive or rule out beta_lambda(M_Pl)=0 from the Cl(3)/Z^3 substrate
```

Follow-up status:
[YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md](YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md)
rules this out on the current surface.  The current substrate derives the
`lambda(M_Pl)=0` boundary and finite scalar source response, but it does not
derive the separate scale-stationarity condition `beta_lambda(M_Pl)=0`.  The
double-criticality selector therefore remains conditional on a new substrate
scale-stationarity theorem or an explicit new selector premise.

Second follow-up status:
[YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md](YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md)
attacks the narrower route through fixed-lattice symmetries.  It closes that
route negatively: `Z^3` has no nontrivial continuous dilation automorphism, the
current lattice Noether theorem supplies translation and `U(1)` currents but
not a scale current, and the physical-lattice note treats continuum/RG
families as extra structure.  Thus the missing premise cannot be recovered
from current same-surface lattice scale symmetry.

Third follow-up status:
[YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md](YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md)
tests the trace-anomaly route.  It also closes negatively on the current
surface: existing trace artifacts are gauge/hypercharge trace catalogues or
scalar-trace no-gos, the lattice Noether note does not provide a quantum
energy-momentum trace theorem, and scalar trace zero would not isolate
`beta_lambda=0` without a new operator-independence/conformal-boundary theorem.

Fourth follow-up status:
[YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md](YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md)
tests the weaker vacuum-stability route.  It closes negatively as a selector:
`lambda(M_Pl)=0` plus one-sided local stability below the upper boundary gives
only `beta_lambda(M_Pl) <= 0`, not the equality `beta_lambda(M_Pl)=0`.  Thus
vacuum stability supplies a family/bound unless an additional double-zero or
multiple-point tangency theorem is added.

Assumption-sensitivity follow-up:
[YT_PLANCK_SELECTOR_GAUGE_INPUT_SENSITIVITY_NOTE_2026-05-01.md](YT_PLANCK_SELECTOR_GAUGE_INPUT_SENSITIVITY_NOTE_2026-05-01.md)
tests whether double-criticality would select a unique `y_t` without fixed
electroweak gauge boundary data.  It does not: at one loop the selected
`y_t(M_Pl)` is a function of `g_1(M_Pl)` and `g_2(M_Pl)`, and perturbing the
weak-scale gauge inputs moves the selected value.  Therefore the route also
requires retained authority for the gauge boundary data and running bridge.

Scale-anchor follow-up:
[YT_PLANCK_SELECTOR_SCALE_ANCHOR_SENSITIVITY_NOTE_2026-05-01.md](YT_PLANCK_SELECTOR_SCALE_ANCHOR_SENSITIVITY_NOTE_2026-05-01.md)
checks whether the selector is invariant under dimensional endpoint choices.
It is not: changing the `M_Pl/v` running interval moves the one-loop selected
boundary value.  The effect is smaller than the stationarity blocker, but it
confirms that endpoint anchors and the SM RGE bridge are explicit imports.

Fixed-point follow-up:
[YT_ASYMPTOTIC_SAFETY_FIXED_POINT_NO_GO_NOTE_2026-05-01.md](YT_ASYMPTOTIC_SAFETY_FIXED_POINT_NO_GO_NOTE_2026-05-01.md)
tests whether `beta_lambda(M_Pl)=0` can be obtained by treating the Planck
boundary as a perturbative SM beta-vector fixed point.  It cannot: the
one-loop SM gauge beta functions have only the Gaussian fixed point, and full
one-loop beta-vector stationarity forces `y_t=0`, not the selector value.

Promising attack frames:

1. boundary-action stationarity of the taste scalar at the Planck surface;
2. multiple-point / vacuum-degeneracy interpretation of the composite-Higgs
   critical surface;
3. exact scale-current stationarity at the physical lattice cutoff, now closed
   negatively on the current fixed-lattice symmetry surface;
4. no-go proof showing `lambda(M_Pl)=0` does not imply `beta_lambda(M_Pl)=0`
   without adding a new selector.
5. quantum EMT / trace-anomaly stationarity, now closed negatively on the
   current authority surface unless new conformal-boundary structure is added.
6. one-sided vacuum stability at the high-scale boundary, now closed
   negatively as a unique selector because it gives an inequality rather than
   stationarity.
7. gauge-input sensitivity, now recorded as an assumption boundary: criticality
   is a family unless the electroweak gauge boundary data are fixed upstream.
8. scale-anchor sensitivity, now recorded as an assumption boundary: the
   criticality readout depends on the `M_Pl/v` running interval and bridge
   convention.
9. perturbative SM fixed-point / asymptotic-safety reading, now closed
   negatively on the current surface: full beta-vector stationarity gives the
   Gaussian point.

Until that premise is derived, this is a conditional selector and a route
portfolio upgrade, not a retained-grade theorem.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_yt_planck_double_criticality_selector.py
# SUMMARY: PASS=19 FAIL=0
```
