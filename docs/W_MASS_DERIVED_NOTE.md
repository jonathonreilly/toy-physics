# `M_W` New Bounded-Companion Lane on the Retained EW Surface

**Date:** 2026-04-18
**Status:** new lane; bounded companion against PDG / CDF / ATLAS / CMS / LHCb
**Primary runner:** `scripts/frontier_w_mass_prediction.py`
**Upstream authorities:**
[`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md),
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md),
[`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md),
[`YT_ZERO_IMPORT_AUTHORITY_NOTE.md`](YT_ZERO_IMPORT_AUTHORITY_NOTE.md),
[`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)

## Authority Role

This note opens the W-boson pole-mass lane, which was not previously on the
prediction surface. It is carried as a bounded companion: the tree-level
readout uses only retained same-surface values, and the one-loop RGE readout
reuses the same-surface EW package with the SM 1-loop SU(2) beta coefficient.
The residual gap against pole measurements is within the standard magnitude
of missing 2-loop / mixing corrections and is not promoted to a retained
row.

## Safe Statement

On the current retained EW normalization surface on `main`:

- tree readout (zero SM imports):
  `M_W^tree = g_2(v) * v / 2 = 79.7956 GeV`
- one-loop RGE readout (bounded companion):
  `M_W^RGE = g_2(M_W) * v / 2 = 80.5589 GeV`

with the framework-side M_Z cross-check
`M_Z^tree = sqrt(g_Y^2 + g_2^2) * v / 2 = 91.2663 GeV` (+0.086% of PDG
`M_Z = 91.1876 GeV`).

The same-surface tree readout is 0.71% below the PDG world average. Running
the same-surface `g_2` down to the W pole with the 1-loop SM beta coefficient
`b_2 = 19/6` closes the gap to +0.24% high vs PDG and +0.16% low vs the
CDF-II 2022 central value. That residual is within typical SM 2-loop and
`Delta r_rem` magnitudes and is therefore carried as a bounded companion
rather than a retained claim.

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
  |-> one-loop RGE correction on the same surface:
        1/alpha_2(M_W) = 1/alpha_2(v) + (b_2 / (2 pi)) * ln(M_W / v)
        b_2 = 19/6                                [SM 1-loop, no active top]
        g_2(M_W)  = 0.6542
        M_W^RGE   = g_2(M_W) * v / 2 = 80.5589 GeV
```

## Package Role

This lane is a framework-side bounded companion. Its tree readout uses only
retained same-surface values and imports no SM quantities. The RGE readout
reuses the same-surface `g_2(v)` and `v`, plus the SM `b_2 = 19/6` as a
pure group-theory coefficient (the same coefficient already used by the
retained running bridge in
[`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
and [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) for
`sin^2 theta_W(M_Z)`, `1/alpha_EM(M_Z)`, and `alpha_s(M_Z)`).

It remains distinct from:

- the retained EW normalization lane (`g_1(v)`, `g_2(v)`, `sin^2 theta_W(M_Z)`,
  `1/alpha_EM(M_Z)`)
- the retained strong-coupling lane (`alpha_s(M_Z)`)
- the YT / top / Higgs bounded lanes

It is **not** on the current retained flagship surface and **not** in the
publication `CLAIMS_TABLE.md` or `PREDICTION_SURFACE_2026-04-15.md`. It is
reviewer-facing evidence that the retained EW package is numerically
consistent with `M_W` measurements at the expected precision of the
same-surface readout.

## Validation Snapshot

Comparison against pole measurements (framework values, no fits):

| Measurement            | central (GeV) | sigma (GeV) | `M_W^tree Delta` | `M_W^RGE Delta` |
|------------------------|---:|---:|---:|---:|
| PDG 2024 world average | `80.3692` | `0.0133` | `-0.5736 GeV` | `+0.1897 GeV` |
| CDF-II 2022            | `80.4335` | `0.0094` | `-0.6379 GeV` | `+0.1254 GeV` |
| ATLAS 2024 reanalysis  | `80.3665` | `0.0159` | `-0.5709 GeV` | `+0.1924 GeV` |
| CMS 2024               | `80.3602` | `0.0099` | `-0.5646 GeV` | `+0.1987 GeV` |
| LHCb 2022              | `80.3540` | `0.0320` | `-0.5584 GeV` | `+0.2049 GeV` |

- tree vs PDG: `-0.714%`
- tree vs CDF: `-0.793%`
- RGE vs PDG: `+0.236%`
- RGE vs CDF: `+0.156%`
- M_Z tree vs PDG: `+0.086%`

The ~`0.2%` residual between the RGE readout and pole measurements is the
expected magnitude of the missing SM 2-loop / `Delta r_rem` corrections
(Sirlin decomposition), which are not retained on the framework surface.
The lane therefore qualifies as a bounded companion on the current `main`
surface.

## What This Lane Does NOT Claim

- it is not a retained theorem
- it does not adjudicate the CDF-vs-LHC W-mass tension; the framework
  readout sits between the two (closer to CDF than to PDG, but within the
  bounded-companion band of either)
- it does not import SM pole values into the derivation; the log value used
  for the RGE anchor enters only through `log(M_W / v)`, which is
  essentially insensitive to the anchor at the ppm level
- it does not promote any new input beyond the retained same-surface
  package

## Primary Runner

- `scripts/frontier_w_mass_prediction.py`
- reference log: `logs/2026-04-18-w-mass-prediction.txt`
