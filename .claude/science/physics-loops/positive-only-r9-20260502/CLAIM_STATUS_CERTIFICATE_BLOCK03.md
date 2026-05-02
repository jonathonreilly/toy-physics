# Claim Status Certificate — R9 Block 03 (Hopping bilinear Hermiticity + translation covariance)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r9-block03-hopping-bilinear-20260502`
**Note:** docs/HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/hopping_bilinear_hermiticity_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_lattice_noether_theorem_note_2026-04-29` retained — supplies T_a (N1) and Q̂_total (N2))
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: single-mode fermion construction definitional, tensor product Fock space definitional)
- runner: 7/7 PASS at machine precision (Hermiticity; translation covariance T H_{xy} T^† = H_{x+1, y+1}; sum invariance; real spectrum; [H, Q̂] = 0; occupation swap; full Hamiltonian translation-invariant)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "H_{xy} = a_x^† a_y + h.c. is Hermitian, translation-covariant T_a H_{xy} T_a^† = H_{x+a, y+a}, and Q̂-conserving. Sum over translation-invariant link family is a valid framework Hamiltonian."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - single-mode fermion construction (definitional)
  - tensor product Fock space (definitional)
```

Establishes the **building block of any tight-binding lattice Hamiltonian** on the framework. Any Hamiltonian H = Σ_{⟨xy⟩} t_{xy} H_{xy} with real coefficients and a translation-invariant link family is automatically Hermitian, translation-invariant, charge-conserving, with real spectrum.

Combines R7 Block 02 (translation covariance of local operators) + R7 Block 03 (per-site fermion structure) + N2 (charge conservation) into a single corollary for the canonical 2-site fermion bilinear.

Expected effective_status after clean Codex audit: **retained**.
