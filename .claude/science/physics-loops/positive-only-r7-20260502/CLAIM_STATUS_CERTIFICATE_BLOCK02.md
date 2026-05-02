# Claim Status Certificate — R7 Block 02 (T_a O(x) T_a^† = O(x + a))

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r7-block02-translation-covariance-20260502`
**Note:** docs/TRANSLATION_COVARIANCE_LOCAL_OP_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/translation_covariance_local_op_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_lattice_noether_theorem_note_2026-04-29` retained — supplies T_a as unitary translation symmetry)
- zero admitted physics inputs ✓ (admitted-context inputs are definitional: position-basis decomposition, local support definition)
- runner: 6/6 PASS at machine precision (X̂ shift exact; site projector covariance exact across full 64-site sweep; hopping covariance exact; sum invariance exact; support relocation exact)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "T_a O(x) T_a^† = O(x + a) for any local operator O(x) on H_phys; operator-level form of N1 translation invariance."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - position-basis decomposition (definitional)
  - local support definition (definitional)
```

Operator-level statement of N1 translation invariance: lifts the abstract symmetry to a concrete computational rule for how any site-local operator transforms under conjugation by T_a. Provides the foundational tool for verifying that any framework Hamiltonian / current built from translation-invariant local terms automatically commutes with T_a.

Companion to R6 Block 02 (group structure of T_a) and complements R5 Block 02 ([P̂, Q̂] = 0). Together they close the operator-level translation-covariance toolkit.

Expected effective_status after clean Codex audit: **retained**.
