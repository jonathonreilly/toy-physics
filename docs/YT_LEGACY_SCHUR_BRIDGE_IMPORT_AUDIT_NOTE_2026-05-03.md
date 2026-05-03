# YT Legacy Schur Bridge Import Audit

```yaml
actual_current_surface_status: exact negative boundary / legacy Schur bridge stack is not PR230 y_t closure
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_legacy_schur_bridge_import_audit.py`  
**Certificate:** `outputs/yt_legacy_schur_bridge_import_audit_2026-05-03.json`

## Purpose

The repo already contains a YT Schur normal-form, stability-gap, and
microscopic-admissibility stack:

- `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`
- `docs/YT_SCHUR_STABILITY_GAP_NOTE.md`
- `docs/YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md`

This audit answers whether that older stack is the missing PR #230 closure.
It is not.

## Result

The runner verifies that the legacy Schur stack is bounded/conditional support
for the older UV-transport bridge.  The audit ledger currently classifies the
normal-form uniqueness row as `audited_conditional`; the stability-gap and
microscopic-admissibility rows are bounded/unaudited support.  The old runner
surface also contains the legacy transport setup (`PLAQ`, `U0`, `ALPHA_LM`,
`V_DERIVED`, and `y_t = g3/sqrt(6)`), which PR #230 is explicitly not allowed
to import as a physical top-Yukawa measurement.

Most importantly, the legacy runners do not emit the PR #230 evidence rows:

- no same-surface Schur `A/B/C` kernel rows;
- no `D_eff'(pole)` row certificate;
- no certified `O_H/C_sH/C_HH` pole rows;
- no same-source W/Z mass-response rows with identity certificates.

The runner passes:

```bash
python3 scripts/frontier_yt_legacy_schur_bridge_import_audit.py
# SUMMARY: PASS=13 FAIL=0
```

## Boundary

This does not demote the older Schur stack as support.  It only blocks a hidden
import into PR #230.  The positive PR #230 closure targets remain explicit
same-surface Schur `A/B/C` rows, certified source-Higgs pole rows, or
same-source W/Z response rows.

This block does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0` as PR #230 evidence.
