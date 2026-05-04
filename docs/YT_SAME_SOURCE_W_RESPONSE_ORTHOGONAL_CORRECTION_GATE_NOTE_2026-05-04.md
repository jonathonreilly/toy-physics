# Same-Source W-Response Orthogonal-Correction Gate

Status: open / same-source W-response orthogonal-correction gate not passed,
not retained and not proposed_retained.

The same-source W-response decomposition gives

```text
g_2 R_t / (sqrt(2) R_W) = y_h + y_x kappa_x/kappa_h.
```

This gate records the exact correction needed before that readout can be used
as physical `y_t`:

```text
y_h = g_2 R_t / (sqrt(2) R_W) - delta_perp
delta_perp = y_x kappa_x/kappa_h.
```

The source normalization still cancels.  The new load-bearing input is the
orthogonal correction `delta_perp`.  It must come from one of:

- an orthogonal-top null theorem;
- a tomography correction row measuring `delta_perp`;
- source-Higgs Gram-purity rows proving the source pole is the canonical Higgs
  pole;
- a neutral rank-one theorem removing the orthogonal neutral sector.

## Current Result

The formula is exact support, but the current PR230 surface does not pass the
gate.  No same-source W response rows exist, no orthogonal-correction
certificate exists, the source-Higgs Gram-purity rows are absent, and the
selection-rule route already has an exact negative boundary.

```bash
python3 scripts/frontier_yt_same_source_w_response_orthogonal_correction_gate.py
# SUMMARY: PASS=17 FAIL=0
```

## Rejected Shortcuts

The gate rejects setting `delta_perp = 0` without a null/purity certificate,
backsolving `delta_perp` from observed `y_t`, using a correction row from a
different source coordinate, and importing `H_unit`, Ward, `alpha_LM`,
plaquette/u0, `c2=1`, or `Z_match=1`.

## Next Action

Produce a same-source W response row plus one valid correction authority:
orthogonal-top null theorem, tomography `delta_perp` row, source-Higgs
Gram-purity row, or neutral rank-one theorem.
