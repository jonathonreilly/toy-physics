# `M_W` Same-Surface Consistency Probe on the Retained EW Lane

**Date:** 2026-04-18 (revised after review)
**Status:** package-captured **bounded same-surface consistency probe** on the
retained EW lane. Reviewer-facing comparison against PDG / CDF / ATLAS / CMS /
LHCb pole measurements only; **not** a retained or manuscript-facing
quantitative claim.
**Primary runner:** `scripts/frontier_w_mass_prediction.py`
**Upstream authorities:**
[`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md),
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md),
[`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)

## Authority Role

This note records the W-boson pole-mass lane as a **same-surface consistency
probe** on the retained EW normalization surface. Its readouts use only
retained same-surface values plus the SM 1-loop SU(2) beta coefficient
`b_2 = 19/6` (the same pure group-theory coefficient already used by the
retained sin^2(theta_W) / alpha_EM running bridge and by
[`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)).

The lane is **not** a retained claim. It is package-captured only in the
bounded companion portfolio. Its residual against pole measurements does not
meet the precision floor of the SM indirect `M_W` prediction (which is set at
the few-MeV level by modern SM 2-loop / `Delta r_rem` analyses), so it cannot
be read as an SM-parity prediction. It is an internal consistency probe only.

## Safe Statement

On the current retained EW normalization surface on `main`, solving the
fixed-point equation `M_W = g_2(M_W) * v / 2` with `g_2` run by the SM
1-loop SU(2) beta function from the retained `g_2(v)` (no pole value
imported into the solve):

- tree readout:
  `M_W^tree = g_2(v) * v / 2 = 79.7956 GeV`
- one-loop RGE readout (same-surface probe):
  `M_W^RGE = g_2(M_W) * v / 2 = 80.5573 GeV`

with the framework-side M_Z cross-check
`M_Z^tree = sqrt(g_Y^2 + g_2^2) * v / 2 = 91.2663 GeV` (+0.086% of PDG
`M_Z = 91.1876 GeV`).

- tree vs PDG world average (80.3692 GeV): `-0.714%`
- RGE vs PDG world average:                  `+0.234%`
- RGE vs CDF-II 2022 (80.4335 GeV):          `+0.154%`

The ~`0.2 GeV` RGE residual is **not** of ordinary SM 2-loop / `Delta r_rem`
size. It tracks the precision already carried by the retained `g_2(v)`
lane itself. On the retained
[`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
surface the framework value `g_2(v)_framework = 0.64795` is `+0.26%`
above `g_2(v)_observed = 0.64629`. At the W scale that `0.26%` input gap
propagates directly into M_W at the same fractional size. The lane
therefore inherits — it does not escape — the existing retained EW
normalization precision.

## Canonical Chain

```
Cl(3) on Z^3
  |-> v = 246.282818290129 GeV                 [OBSERVABLE_PRINCIPLE]
  |-> g_2(v) = 0.6480                           [YT_EW_COLOR_PROJECTION]
  |-> g_1_GUT(v) = 0.4644                       [YT_EW_COLOR_PROJECTION]
  |-> g_Y(v) = g_1_GUT(v) * sqrt(3/5) = 0.3597  [SM convention]
  |
  |-> tree readout:
  |     M_W^tree = g_2(v) * v / 2 = 79.7956 GeV
  |     M_Z^tree = sqrt(g_Y^2 + g_2^2) * v / 2 = 91.2663 GeV
  |
  |-> 1-loop RGE fixed-point solve (no pole import):
        1/alpha_2(mu) = 1/alpha_2(v) + (b_2 / (2 pi)) * ln(mu / v)
        b_2 = 19/6   (SM 1-loop SU(2), no active top at W scale)
        solve  M_W = g_2(M_W) * v / 2  by fixed-point iteration
        M_W^RGE = 80.5573 GeV    (converged in 6 iterations to < 1e-10 GeV)
```

## What This Lane Does NOT Claim

- it is **not** a retained theorem
- it is **not** within the precision floor of the SM indirect `M_W`
  prediction, which is at the few-MeV level; the ~`0.2 GeV` RGE residual
  is **not** an artifact of missing SM 2-loop / `Delta r_rem` corrections
- it does **not** adjudicate the CDF-vs-LHC `M_W` tension; the readout
  resolution is too coarse to speak to experimental central values at the
  ~`0.01 GeV` level
- it does **not** import a pole value into the framework-side solve;
  experimental central values enter only in the comparison table below
- it is package-captured only as a bounded same-surface EW diagnostic;
  its `CLAIMS_TABLE.md` entry is bounded-companion only, and it is **not**
  promoted to the retained quantitative surface or
  `PREDICTION_SURFACE_2026-04-15.md`

## Package Role

This lane is a framework-side bounded same-surface consistency probe. Its tree
readout uses only retained same-surface values; the RGE fixed-point solve adds
only the SM 1-loop SU(2) coefficient `b_2 = 19/6`, reused from the retained
EW normalization and `alpha_s` lanes.

Publication placement on `main`: bounded companion section / appendix only.

It remains distinct from:

- the retained EW normalization lane (`g_1(v)`, `g_2(v)`,
  `sin^2 theta_W(M_Z)`, `1/alpha_EM(M_Z)`)
- the retained strong-coupling lane (`alpha_s(M_Z)`)
- the YT / top / Higgs bounded lanes

## Validation Snapshot

Comparison against pole measurements (framework-side values, no fits):

| Measurement            | central (GeV) | sigma (GeV) | `M_W^tree Delta` | `M_W^RGE Delta` |
|------------------------|---:|---:|---:|---:|
| PDG 2024 world average | `80.3692` | `0.0133` | `-0.5736 GeV` | `+0.1881 GeV` |
| CDF-II 2022            | `80.4335` | `0.0094` | `-0.6379 GeV` | `+0.1238 GeV` |
| ATLAS 2024 reanalysis  | `80.3665` | `0.0159` | `-0.5709 GeV` | `+0.1908 GeV` |
| CMS 2024               | `80.3602` | `0.0099` | `-0.5646 GeV` | `+0.1971 GeV` |
| LHCb 2022              | `80.3540` | `0.0320` | `-0.5584 GeV` | `+0.2033 GeV` |

- tree vs PDG: `-0.714%`
- tree vs CDF: `-0.793%`
- RGE vs PDG: `+0.234%`
- RGE vs CDF: `+0.154%`
- M_Z tree vs PDG: `+0.086%`

Consistency check for the residual interpretation:

- retained `g_2(v)` precision vs observed SM MS-bar:  `+0.265%`
  (`YT_EW_COLOR_PROJECTION_THEOREM`: `0.64795` vs `0.64629`)
- framework-side `M_W^RGE` gap vs PDG:                 `+0.234%`

The two percentages agree at better than `0.05%`, consistent with the
`M_W` residual being a direct inheritance of the retained `g_2(v)` input
precision rather than a missing loop correction on the SM indirect surface.

## Primary Runner

- `scripts/frontier_w_mass_prediction.py` (numpy only)
- reference log (gitignored by repo convention): `logs/2026-04-18-w-mass-prediction.txt`
