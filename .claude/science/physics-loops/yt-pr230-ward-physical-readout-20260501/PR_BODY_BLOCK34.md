## Block34 checkpoint: complete additive-top Jacobian refresh

Landed a W/Z-subtraction support refresh after the final chunk package:

- `outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json` now consumes
  chunks001-063 from the committed package audit, records `row_count=63`,
  `complete_chunk_packet=true`, active chunks `[]`, and preserves production
  seed/selected-mass/three-mass-scan metadata.
- `outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json`
  now recognizes those rows as complete bounded support only.  Strict
  subtraction still needs per-configuration additive rows, W/Z response rows,
  matched covariance, strict non-observed `g2`, accepted same-source EW/Higgs
  action, and a final subtracted-response readout.

Validation:

```text
python3 scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
# SUMMARY: PASS=22 FAIL=0
```

No retained/proposed_retained closure is claimed; PR #230 remains draft/open.
