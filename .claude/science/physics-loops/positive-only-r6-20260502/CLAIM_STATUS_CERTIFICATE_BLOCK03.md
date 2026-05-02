# Claim Status Certificate — R6 Block 03 (SU(3) C_2(3) = 4/3 on color fundamental)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r6-block03-su3-casimir-fundamental-20260502`
**Note:** docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/su3_casimir_fundamental_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`cl3_color_automorphism_theorem` retained — supplies SU(3)_c on V_3 with Gell-Mann generators T^a = λ^a/2 and trace-normalization Tr[T^a T^b] = (1/2) δ^{ab})
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: Schur's lemma, SU(N) Casimir formula C_2(N) = (N²-1)/(2N))
- runner: 7/7 PASS at machine precision (Hermitian; trace ortho; su(3) closure; Schur scalar; numerical = 4/3 exact; formula = 4/3 exact)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "SU(3)_c quadratic Casimir on fundamental V_3 = 4/3 in standard Gell-Mann normalization."
upstream_dependencies:
  - cl3_color_automorphism_theorem (retained)
admitted_context_inputs:
  - Schur's lemma (Lie-algebra representation theory)
  - SU(N) Casimir formula C_2(N) = (N² - 1) / (2N) (standard)
```

Universal "color charge squared" of any color-triplet quark in the framework, invariant of flavor / generation / EW quantum numbers. Coefficient of the static qq̄ Coulomb potential V(r) = -(4/3) α_s / r, of the one-loop quark self-energy color factor, and of any color-singlet bilinear projection involving two triplets.

Expected effective_status after clean Codex audit: **retained**.
