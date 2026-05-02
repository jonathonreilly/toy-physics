# YT Zero-Mode Prescription Import Audit Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / zero-mode prescription import audit  
**Runner:** `scripts/frontier_yt_zero_mode_prescription_import_audit.py`  
**Certificate:** `outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json`

## Purpose

The scalar zero-mode theorem reduced the PR #230 analytic blocker to a very
specific missing input: a retained gauge-fixing, zero-mode, IR, and
finite-volume prescription for the interacting scalar denominator.

This audit checks whether the repo already contains such an authority.

## Audited Surfaces

The runner checks the strongest current candidates:

- `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
- `docs/CONTINUUM_IDENTIFICATION_NOTE.md`
- `docs/YT_FH_LSZ_PRODUCTION_MANIFEST_NOTE_2026-05-01.md`
- `outputs/yt_scalar_ladder_kernel_input_audit_2026-05-01.json`
- `outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json`
- `outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json`
- `outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json`
- `outputs/yt_fh_lsz_production_manifest_2026-05-01.json`

## Runner Result

```text
python3 scripts/frontier_yt_zero_mode_prescription_import_audit.py
# SUMMARY: PASS=8 FAIL=0
```

Findings:

- perturbative BZ notes use an IR regulator and gauge-parameter convention but
  do not select the PR #230 scalar zero-mode prescription;
- the continuum-identification note warns about alternative gauge fixings
  rather than deriving the PR #230 scalar denominator limit;
- the FH/LSZ manifest requires finite-volume/IR/zero-mode control as an input;
- scalar ladder certificates keep `proposal_allowed=false`.

## Claim Boundary

This is not closure.  It only rules out a hidden import source for the
zero-mode prescription.  PR #230 still needs either a new gauge-fixing /
zero-mode / IR / finite-volume theorem for the scalar denominator, or
production same-source scalar pole measurements with an explicitly selected
prescription.
