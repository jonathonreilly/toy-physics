# Taste-Corner Scalar-Carrier Import Audit

**Date:** 2026-05-01
**Status:** exact negative boundary / taste-corner scalar-carrier import audit
**Runner:** `scripts/frontier_yt_taste_carrier_import_audit.py`
**Certificate:** `outputs/yt_taste_carrier_import_audit_2026-05-01.json`

## Purpose

The finite zero-mode-removed ladder crossings are dominated by non-origin
Brillouin-zone taste corners.  This audit checks whether any current retained
or audit-clean authority lets PR #230 use those corners as the physical scalar
carrier and therefore as scalar-pole / LSZ evidence.

## Result

```text
python3 scripts/frontier_yt_taste_carrier_import_audit.py
# SUMMARY: PASS=8 FAIL=0
```

The strongest candidates do not close the import:

| Candidate | Audit status | Why it does not close PR #230 |
|---|---|---|
| `cl3_taste_generation_theorem` | `audited_renaming` | verifies taste-cube algebra, but physical taste-to-generation/readout identification remains open |
| `taste_scalar_isotropy_theorem_note` | `audited_conditional` | exact fermion-CW isotropy only; scalar-spectrum consequences are bounded |
| `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | `audited_conditional` | conditional PT formula layer with non-clean `H_unit` / normalization surfaces |
| scalar ladder input audit | exact support | still lists scalar color/taste/spin projector as missing |
| taste-corner finite witness block | exact negative boundary | non-origin corners dominate finite crossings and physical-origin filtering removes them |

No retained/audit-clean authority currently admits the non-origin BZ corners as
the physical scalar carrier for PR #230.

## Claim Boundary

This does not rule out a future taste/scalar-carrier theorem.  It rules out
using the current finite taste-corner-dominated ladder crossings as retained
scalar pole, scalar LSZ, `kappa_s`, or top-Yukawa evidence.

The next analytic route must derive the taste/scalar-carrier projection and
continuum/projector limit, or the campaign must use production same-source
FH/LSZ pole data.
