# Canonical-Higgs Operator Semantic Firewall

Status: bounded-support / gate hardening only; proposal_allowed=false.

The source-Higgs route now depends on a future same-surface canonical-Higgs
operator certificate.  This firewall hardens that future gate so a candidate
cannot self-declare `O_H` by filling booleans and pointing at static EW algebra,
`H_unit`, Ward identity, observed-target selectors, or generic harness notes.

## Hardened Checks

`scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py` now requires
more than the original syntactic fields.  A future candidate must also provide:

- non-shortcut identity and normalization references;
- accepted `identity_certificate_kind` and `normalization_certificate_kind`;
- `canonical_higgs_operator_normalization_passed: true`;
- an accepted `source_overlap_closure_mode`;
- `forbidden_shortcut_audit_passed: true`.

The blocked shortcut references include the Ward theorem, `H_unit` candidate
gate, static EW Higgs gauge-mass algebra, SM one-Higgs monomial selection, the
operator gate itself, the realization gate, and source-Higgs harness
instrumentation.

## Stress Cases

The semantic firewall runner rejects candidate shapes that try to use:

- static EW gauge-mass algebra as the identity/normalization reference;
- `H_unit` as the operator;
- `yt_ward_identity` as authority;
- self-declared identity and normalization classes;
- observed target selectors;
- candidate-local `proposal_allowed: true`.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py \
  scripts/frontier_yt_canonical_higgs_operator_semantic_firewall.py

python3 scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_canonical_higgs_operator_semantic_firewall.py
# SUMMARY: PASS=10 FAIL=0
```

## Claim Boundary

This does not provide `O_H`, `C_sH/C_HH` rows, or physical `y_t`.  It only
prevents the next bridge from accepting the same definition-as-derivation
pattern that caused the Ward chain demotion.
