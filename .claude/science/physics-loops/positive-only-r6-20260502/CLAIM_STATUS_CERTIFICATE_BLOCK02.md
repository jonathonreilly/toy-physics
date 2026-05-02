# Claim Status Certificate — R6 Block 02 (T_a T_b = T_{a+b} abelian translation group)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r6-block02-translation-abelian-20260502`
**Note:** docs/TRANSLATION_ABELIAN_COMPOSITION_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/translation_abelian_composition_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_lattice_noether_theorem_note_2026-04-29` retained — supplies T_a as translation symmetry)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: Z^3 group structure, regular-representation construction)
- runner: 7/7 PASS at machine precision (T_0 = I exact; closure exact; commutativity exact; T_{-a} = T_a† exact; T_e_i^L = I exact; group order = L^3 exact; faithfulness exact)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "T_a T_b = T_{a+b} on H_phys with [T_a, T_b] = 0; T : Z^3 → U(H_phys) faithful unitary rep of abelian translation group."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - Z^3 group structure (set-theoretic)
  - regular-representation construction (group theory)
```

Establishes the exact group-theoretic structure of lattice translations on H_phys: faithful, unitary, abelian, regular-representation. Provides the kinematic basis for momentum-eigenstate construction (Brillouin zone via Stone's theorem) and complements R5 Block 02 ([P̂, Q̂] = 0).

Expected effective_status after clean Codex audit: **retained**.
