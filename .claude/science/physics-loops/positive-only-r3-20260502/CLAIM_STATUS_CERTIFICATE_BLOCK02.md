# Claim Status Certificate — R3 Block 02 ((CPT)² = I)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r3-block02-cpt-squared-20260502`
**Note:** docs/CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/cpt_squared_is_identity_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade dep ✓ (`cpt_exact_note` retained, provides (CP)² = I)
- zero admitted physics inputs ✓ (antiunitary commutation rule + T² = I are basic linear algebra)
- runner: 4/4 PASS at machine precision (max resid 0.000e+00)

## Author classification

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "(CPT)² = I exactly on H_phys, with no phase factor"
upstream_dependencies:
  - cpt_exact_note (retained)
admitted_context_inputs:
  - antiunitary commutation rule T·U = U*·T
  - T² = K² = I
```

Expected `effective_status` after clean Codex audit: **retained**.
