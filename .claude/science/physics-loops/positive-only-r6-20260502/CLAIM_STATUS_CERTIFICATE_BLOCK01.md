# Claim Status Certificate — R6 Block 01 (No per-site γ_5 chirality on Cl(3))

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r6-block01-no-per-site-chirality-20260502`
**Note:** docs/NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/no_per_site_chirality_check.py

## Strict-bar gate

- claim_type: positive_theorem (in no-go form) ✓
- single retained-grade one-hop dep ✓ (`axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` retained)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: Clifford volume-element identity and Pauli basis spans M_2(C))
- runner: 6/6 PASS at machine precision (ω = i·I exact; ω central exact; ω² = -I exact; null space dim 0; no γ_5 candidate)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Cl(3) volume element ω = i·I in Pauli rep; no per-site γ_5 chirality operator exists in M_2(C)."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - Clifford volume-element commutation identity (Lawson–Michelsohn)
  - Pauli matrices span M_2(C) (basic linear algebra)
```

Local instance of the "no chirality in odd total dim" fact. Confirms at the per-site algebraic level that recovering γ_5 requires extending Cl(3) (e.g. to Cl(3,1) by adding a temporal direction) — consistent with the framework's `anomaly_forces_time` narrative.

Expected effective_status after clean Codex audit: **retained**.
