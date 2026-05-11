# Probe Z-S4b-RGE Import-Tier Review

**Date:** 2026-05-08 (review sync 2026-05-10)
**Status:** bounded import-tier review
**Claim type:** bounded_theorem
**Primary runner:** [`scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py`](../scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py)
**Cache:** [`logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt`](../logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt)

## Scope

This note reviews the unlanded Y-S4b-RGE proposal that a three-loop
SM `beta_lambda` run from `lambda(M_Pl) = 0` down to `v_EW` closes the
Probe X-S4b-Combined Higgs gap. It does not land or ratify that positive
proposal. It records the narrower, runner-backed import-tier boundary:
the sub-percent three-loop arithmetic is reproducible, but it is not a
from-framework theorem over the physical `Cl(3)` local algebra plus
the `Z^3` spatial substrate.

The independent audit lane owns all verdicts and effective statuses.
Review-loop only seeds this bounded claim surface for later audit.

## Result

The reviewed Y-S4b-RGE arithmetic table is:

| Loop order | `lambda(v)` | `m_H` | PDG comparator gap |
| --- | ---: | ---: | ---: |
| 1-loop | `0.140609` | `130.60 GeV` | `+4.27%` |
| 2-loop | `0.128882` | `125.04 GeV` | `-0.17%` |
| 3-loop | `0.129087` | `125.14 GeV` | `-0.09%` |

The runner reproduces this table and then classifies the load-bearing
ingredients:

| Ingredient | Review class | Boundary |
| --- | --- | --- |
| 1-loop `beta_lambda` coefficient | retained-grade support | Scheme-universal one-loop counterterm structure with group-theoretic factors. |
| 2-loop `beta_lambda` scalar weights | imported | FJJ92/LWX03 MSbar dimensional-regularization coefficients; not derived in the framework. |
| 3-loop `beta_lambda` scalar weights | imported | CZ12/BPV13 MSbar coefficients with explicit `zeta(3)` terms. |
| `lambda(M_Pl) = 0` boundary condition | admitted/postulated | A high-scale boundary condition, not derived from physical `Cl(3)` plus `Z^3`. |
| `v -> M_Pl` uplift of couplings | import-contaminated at two loops and beyond | Uses higher-loop gauge/Yukawa running in the same imported class. |

The strongest bounded from-framework layer is therefore the 1-loop-only
run, which gives `m_H = 130.60 GeV`, `+4.27%` from the PDG comparator.
The sub-percent 3-loop closure is useful numerical support, but it rests
on imported higher-loop coefficients plus the admitted high-scale
boundary condition.

## Dependency Surface

Load-bearing references:

- [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)
  for the imported higher-loop MSbar coefficient precedent.
- [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
  for the existing 3-loop RGE machinery and uncertainty band being reviewed.
- [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md)
  for the admitted SM Higgs-potential form.
- [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
  for the high-scale `lambda(M_Pl) = 0` boundary-condition label.
- [`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py)
  for the beta-function implementation being inspected.

The PDG Higgs mass is used only as a falsifiability comparator, not as a
derivation input.

## Not Claimed

- This note does not add a new axiom or a new boundary condition.
- This note does not promote Y-S4b-RGE to a retained or positive theorem.
- This note does not derive the two-loop or three-loop SM beta-function
  coefficients from the framework.
- This note does not derive `lambda(M_Pl) = 0`; it treats that boundary
  condition as admitted for the bounded numerical replay.

## Falsifiers

The bounded review would fail if any of the following is supplied:

- a framework-native derivation of the two-loop and three-loop
  `beta_lambda` scalar coefficients without importing MSbar
  dimensional-regularization machinery;
- a derivation of `lambda(M_Pl) = 0` from the physical `Cl(3)` local
  algebra and `Z^3` spatial substrate rather than an admission;
- a runner reproduction showing that the one-loop-only table does not
  give `m_H = 130.60 GeV` under the reviewed inputs;
- a successful reclassification of the higher-loop uplift coefficients
  as retained-grade framework outputs.

## Command

```bash
python3 scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py
```

Expected summary:

```text
PASS = 4, FAIL = 0, ADMITTED = 4
Tier: BOUNDED
```
