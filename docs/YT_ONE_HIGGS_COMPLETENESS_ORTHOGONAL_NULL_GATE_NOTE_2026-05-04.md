# One-Higgs Completeness Orthogonal-Null Gate

Status: conditional-support / one-Higgs completeness orthogonal-null theorem;
premise absent.  Not retained and not proposed_retained.

The existing SM one-Higgs gauge-selection theorem is useful support, but it is
not a PR230 `O_sp = O_H` identity and does not by itself remove the orthogonal
neutral top-coupling blocker.  This gate records the narrower valid statement:

If a future same-source PR230 electroweak action certificate proves one-Higgs
field completeness for the neutral top-coupled scalar sector, then the
orthogonal correction in the W-response readout is zero.

With

```text
g_2 R_t/(sqrt(2) R_W) = y_h + y_x kappa_x/kappa_h,
delta_perp = y_x kappa_x/kappa_h,
```

one-Higgs field completeness means the orthogonal top-coupled scalar basis is
empty on that same source/action surface.  Equivalently `kappa_x=0` in the
readout, so

```text
delta_perp = 0,
g_2 R_t/(sqrt(2) R_W) = y_h.
```

## Current Result

The conditional theorem passes, but the current gate does not.  The current
surface has no same-source EW action certificate and no one-Higgs completeness
certificate.  The pre-existing no-go still blocks importing `delta_perp=0`
from current charges or from one-Higgs notation alone.

```bash
python3 scripts/frontier_yt_one_higgs_completeness_orthogonal_null_gate.py
# SUMMARY: PASS=13 FAIL=0
```

## Non-Claims

This gate does not claim physical `y_t`, retained closure, or
proposed_retained closure.  It does not treat SM one-Higgs gauge selection
alone as `O_sp = O_H`, and it does not set `delta_perp=0` on the current
surface.  It uses no `H_unit`, Ward route, observed selector, `alpha_LM`,
plaquette/u0, `c2=1`, `Z_match=1`, or `cos(theta)=1` shortcut.

## Next Action

Supply a same-source EW action certificate with one-Higgs field completeness,
or measure `delta_perp` by tomography/source-Higgs Gram rows.
