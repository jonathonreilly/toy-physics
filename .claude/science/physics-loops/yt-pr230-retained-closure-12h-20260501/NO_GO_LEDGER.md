# No-Go Ledger

## `lambda(M_Pl)=0` does not imply `beta_lambda(M_Pl)=0`

Closed by `docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md`
and `scripts/frontier_yt_beta_lambda_planck_stationarity_no_go.py`.

## Fixed `Z^3` lattice does not supply a scale current

Closed by `docs/YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_scale_stationarity_substrate_no_go.py`.

Exact reason: scalar dilation is a `Z^3` automorphism only for `k=+/-1`, so
there is no one-parameter dilation generator for a Noether scale current.

## Current Noether theorem does not close quantum trace anomaly

Closed by `docs/YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_trace_anomaly_stationarity_no_go.py`.

The Noether note explicitly closes translation and `U(1)` currents and defers
full EMT/anomaly closure.  Existing anomaly-trace catalogues are gauge and
hypercharge trace arithmetic, not quantum stress-tensor trace identities.

## One-sided vacuum stability does not imply beta stationarity

Closed by `docs/YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_vacuum_stability_stationarity_no_go.py`.

At an upper boundary with `lambda(M_Pl)=0`, local nonnegativity below the
boundary gives `beta_lambda(M_Pl)<=0`, not equality.  Equality is a separate
double-zero/multiple-point premise.

## Planck selector is gauge-input sensitive

Recorded by `docs/YT_PLANCK_SELECTOR_GAUGE_INPUT_SENSITIVITY_NOTE_2026-05-01.md`
and `scripts/frontier_yt_planck_selector_gauge_input_sensitivity.py`.

This is an assumption boundary rather than a no-go against the selector:
`beta_lambda(M_Pl)=0` selects `y_t` only after electroweak gauge boundary data
are fixed.  Without those inputs, the route is a family.

## Planck selector is scale-anchor sensitive

Recorded by
`docs/YT_PLANCK_SELECTOR_SCALE_ANCHOR_SENSITIVITY_NOTE_2026-05-01.md` and
`scripts/frontier_yt_planck_selector_scale_anchor_sensitivity.py`.

The non-MC selector uses the `M_Pl/v` running interval.  Changing the endpoint
anchors changes the selected one-loop boundary value.  This is an assumption
boundary for retained closure, not the primary blocker.

## Perturbative SM fixed point does not supply the selector

Closed by `docs/YT_ASYMPTOTIC_SAFETY_FIXED_POINT_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_asymptotic_safety_fixed_point_no_go.py`.

At one loop the SM gauge beta-vector has only the Gaussian fixed point.  Full
beta-vector stationarity therefore forces `y_t=0`.  Partial beta conditions
are added selectors unless new UV fixed-point structure is supplied.

## Ward ratio does not imply Planck beta stationarity

Closed by `docs/YT_WARD_RATIO_STATIONARITY_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_ward_ratio_stationarity_no_go.py`.

At the selector's Planck gauge point, `y_t=g_3/sqrt(6)` gives nonzero
`beta_lambda(lambda=0)`.  Therefore the Planck stationarity blocker is
independent of any future Ward-ratio repair.

## IR quasi-fixed-point focusing is not a standalone selector

Closed by `docs/YT_QFP_SELECTOR_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_qfp_selector_no_go.py`.

QFP focusing compresses UV trajectory dependence, but different UV boundary
values still map to different IR `y_t(v)` values.  It is bounded support for
transport robustness, not retained closure.

## Observed mass/comparator inversion is not proof

Closed by `docs/YT_OBSERVED_MASS_INVERSION_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_observed_mass_inversion_no_go.py`.

Using observed `m_t`, `m_H`, or accepted `y_t` values as inputs imports the
target.  It can calibrate or compare a route, but it cannot be the retained
substrate derivation.

## The RGE bridge is not a selector

Closed by `docs/YT_RGE_ONLY_SELECTOR_NO_GO_NOTE_2026-05-01.md` and
`scripts/frontier_yt_rge_only_selector_no_go.py`.

The SM RGE bridge transports a boundary value across scales.  It does not
choose that boundary value without measurement, Ward repair, production
certificate, or a separately derived Planck stationarity condition.
