# Claim Status Certificate — R7 Block 01 (SU(3) Adjoint Casimir = 3)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r7-block01-su3-adjoint-casimir-20260502`
**Note:** docs/SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/su3_adjoint_casimir_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`cl3_color_automorphism_theorem` retained — supplies SU(3)_c with Gell-Mann generators in fundamental and trace-normalization Tr[T^a T^b] = (1/2) δ^{ab})
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: adjoint representation construction, Schur's lemma)
- runner: 7/7 PASS at machine precision (Hermitian; su(3) closure; trace ortho; Schur scalar; numerical = 3 exact; trace argument; ratio 9/4)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "SU(3)_c quadratic Casimir on adjoint = N = 3 in standard Gell-Mann normalization."
upstream_dependencies:
  - cl3_color_automorphism_theorem (retained)
admitted_context_inputs:
  - adjoint representation construction (Lie-algebra)
  - Schur's lemma (Lie-algebra representation theory)
```

Universal "color charge squared" of any gluon mode in the framework. Companion to R6 Block 03 (C_2(fund) = 4/3); together they form the basic Casimir table for SU(3)_c. C_2(adj) = 3 is the prefactor of the gluonic contribution to the QCD β-function leading order.

Expected effective_status after clean Codex audit: **retained**.
