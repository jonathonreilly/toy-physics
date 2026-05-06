# PR230 Determinant-Positivity Bridge Intake Gate

**Date:** 2026-05-05  
**Status:** bounded-support / staggered-Wilson determinant positivity is useful positivity-preservation support, not PR230 `y_t` closure  
**Runner:** `scripts/frontier_yt_pr230_det_positivity_bridge_intake_gate.py`  
**Certificate:** `outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json`

## Question

`origin/main` landed
`docs/STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`,
which proves configuration-by-configuration positivity of the staggered +
Wilson determinant on a symmetric-canonical surface.

This note asks whether that new positive theorem changes PR #230's missing
top-Yukawa bridge.

## Verdict

It helps, but it does not close.

The determinant-positivity bridge supplies positive-measure /
positivity-preservation support.  PR #230's clean source-only theorem route
needs a stronger object:

```text
neutral scalar response transfer is primitive / positivity improving
```

or a measured bridge:

```text
canonical O_H plus C_sH/C_HH pole rows
```

or a physical-response bridge:

```text
same-source W/Z response rows with identity certificates
```

Positive determinant alone is compatible with a reducible neutral scalar
response sector.  A block-diagonal positive transfer matrix can preserve all
source-only rows while leaving an orthogonal neutral scalar direction alive.

## Why This Matters

This resolves a tempting shortcut.  The newly landed determinant theorem is
framework-native and useful, but it should not be upgraded into the missing
`O_s -> O_H` identity, `kappa_s = 1`, or neutral rank-one theorem.

It can become load-bearing only after one of the missing bridge objects exists:

- same-surface neutral primitive-cone / irreducibility certificate;
- canonical `O_H/h` with `C_sH/C_HH` pole rows;
- same-source W/Z response rows;
- strict production FH/LSZ plus matching.

## Non-Claims

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not use determinant positivity as `y_t`, `O_H`, or `kappa_s`; does not use
`H_unit`, `yt_ward_identity`, or observed targets; and does not treat
positivity preservation as positivity improvement.

## Verification

```bash
python3 scripts/frontier_yt_pr230_det_positivity_bridge_intake_gate.py
# SUMMARY: PASS=15 FAIL=0
```
