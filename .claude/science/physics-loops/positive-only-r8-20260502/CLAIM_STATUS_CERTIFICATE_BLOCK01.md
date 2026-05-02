# Claim Status Certificate — R8 Block 01 (Fermion parity Z_2 grading)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r8-block01-fermion-parity-20260502`
**Note:** docs/FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/fermion_parity_z2_grading_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_lattice_noether_theorem_note_2026-04-29` retained — supplies Q̂_total via N2)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: spectral functional calculus, single-mode fermion construction definitional, tensor product Fock space definitional)
- runner: 7/7 PASS at machine precision (Hermitian; F² = I; [F, n̂_x] = 0; spectrum {+1, -1}; dim balance 2^{N-1}; {F, a_x} = 0; [F, bilinear] = 0)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "F = (-1)^Q̂ is Hermitian unitary involution; H = H_even ⊕ H_odd Z_2 grading; a_x is Z_2-odd; bilinears Z_2-even; F conserved by [F, H] = 0."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - spectral functional calculus (basic finite-dim spectral theorem)
  - single-mode fermion construction (definitional)
  - tensor product Fock space (definitional)
```

Establishes the framework's **fermion-parity superselection rule**: only Z_2-even local operators (bilinears, currents, plaquettes) can connect physical states. Single fermion operators a_x, a_x^† are Z_2-odd and cannot appear directly in observable amplitudes.

Together with R7 Block 03 (Q̂ integer spectrum) and R3 Block 01 ([H, Q̂] = 0), establishes the complete Z_2 / U(1) charge structure of the framework's Fock space.

Expected effective_status after clean Codex audit: **retained**.
