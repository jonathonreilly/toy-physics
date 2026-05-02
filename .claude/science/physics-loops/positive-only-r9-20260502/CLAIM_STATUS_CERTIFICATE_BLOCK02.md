# Claim Status Certificate — R9 Block 02 (Multi-site Pauli group P_N order 4^{N+1})

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r9-block02-multisite-pauli-group-20260502`
**Note:** docs/MULTISITE_PAULI_GROUP_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/multisite_pauli_group_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` retained)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: tensor product Fock space definitional, group generation theory, Pauli multiplication identity)
- runner: 6/6 PASS at machine precision (BFS enumeration |P_1| = 16, |P_2| = 64, |P_3| = 256; central Z_4; quotient (Z_2 × Z_2)^N; central extension)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Multi-site Pauli group P_N has order 4^{N+1}; center Z(P_N) ≅ Z_4 (scalar phases); quotient ≅ (Z_2 × Z_2)^N; central extension 1 → Z_4 → P_N → (Z_2 × Z_2)^N → 1."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - tensor product Fock space (definitional)
  - group generation theory (basic finite-group)
  - Pauli multiplication identity (mathematical)
```

Multi-site generalization of R8 Block 03 (per-site P_1 order 16). The N-qubit Pauli group P_N is the framework's natural finite multiplicative symmetry group on N-site Fock space, and the canonical multi-qubit Pauli group used throughout quantum information theory (multi-qubit stabilizer codes, surface codes, color codes, fault-tolerant quantum computation).

Expected effective_status after clean Codex audit: **retained**.
