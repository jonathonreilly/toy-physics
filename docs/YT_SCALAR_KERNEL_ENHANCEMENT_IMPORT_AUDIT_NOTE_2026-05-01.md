# Scalar-Kernel Enhancement Import Audit

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar-kernel enhancement import audit
**Runner:** `scripts/frontier_yt_scalar_kernel_enhancement_import_audit.py`
**Certificate:** `outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json`

## Purpose

The unit-projector threshold block showed that the best finite ladder row has
`lambda_max = 0.442298920672` after unit taste projection.  A finite pole would
therefore require an extra scalar-channel kernel multiplier
`2.26091440260`.  This audit checks whether any current retained or
audit-clean surface supplies that enhancement without fitting it as a pole
selector.

## Result

```text
python3 scripts/frontier_yt_scalar_kernel_enhancement_import_audit.py
# SUMMARY: PASS=7 FAIL=0
```

No checked candidate closes the chain:

| Candidate | Status | Why it does not supply the enhancement |
|---|---|---|
| HS/RPA contact coupling | exact negative boundary | local `G` is not in `A_min`; gauge-exchange-to-contact collapse is scale dependent |
| scalar ladder input audit | exact support | formulae are reusable, but kernel, projector, IR/volume limit, crossing, and residue remain missing |
| same-1PI four-fermion coefficient | exact negative boundary | fixes `y^2 D_phi`, not a separately normalized scalar pole or kernel multiplier |
| Ward/gauge/Feshbach response identities | exact negative boundary | pole condition fixes `K(x_pole)`, not `K'(x_pole)` or common dressing |

## Claim Boundary

This is not retained or proposed-retained closure.  It does not add or fit a
scalar contact coupling, set `kappa_s = 1`, use `H_unit`, use
`yt_ward_identity`, select by observed values, or import alpha/plaquette/`u0`,
`c2 = 1`, or `Z_match = 1`.

The remaining analytic route must derive the interacting scalar-channel kernel
enhancement and `K'(x_pole)` from retained Wilson-staggered dynamics, or the
campaign must use production same-source FH/LSZ pole data.
