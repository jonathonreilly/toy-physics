# FH/LSZ Model-Class Semantic Firewall

Status: bounded-support / gate hardening only, not retained and not
proposed_retained.

The chunk pole-fit route needs scalar-LSZ model-class authority before finite
Euclidean shell fits can be treated as a physical pole derivative or residue.
This firewall hardens the future model-class gate so a candidate cannot pass by
setting `model_class_gate_passed: true` without a real proof class and
FV/IR/threshold control.

## Hardened Checks

`scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py` now validates a
future model-class certificate with:

- `certificate_kind == fh_lsz_pole_fit_model_class`;
- accepted `model_class_certificate_kind`;
- non-shortcut model-class reference;
- finite-shell deformation exclusion;
- isolated scalar pole;
- correct derivative identifier;
- FV/IR/zero-mode control;
- threshold or scalar-denominator control;
- firewall rejection of observed selectors, `H_unit`/Ward authority,
  `alpha_LM`/plaquette authority, and `kappa/c2/Z_match` shortcuts.

## Stress Cases

The semantic firewall runner rejects candidate shapes that try to use:

- static EW algebra as model-class authority;
- Ward identity as model-class authority;
- self-declared model-class booleans;
- absent FV/IR/threshold control;
- observed target selectors;
- `kappa/c2/Z_match` shortcuts;
- candidate-local `proposal_allowed: true`.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py \
  scripts/frontier_yt_fh_lsz_model_class_semantic_firewall.py

python3 scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_model_class_semantic_firewall.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This does not provide scalar LSZ normalization, a scalar denominator theorem,
pole saturation, or physical `y_t`.  It only prevents future finite-shell chunk
fits from being promoted by a shallow model-class certificate.
