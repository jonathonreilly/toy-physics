# Claim Status Certificate — R7 Block 03 (Q̂ integer spectrum on Fock space)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r7-block03-q-integer-spectrum-20260502`
**Note:** docs/Q_INTEGER_SPECTRUM_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/q_integer_spectrum_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` retained)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: single-mode fermion construction definitional, tensor product Fock space definitional, binomial coefficient counting combinatorial)
- runner: 6/6 PASS at machine precision ({a, a^†} = I exact; n eigenvalues {0,1} exact; multi-site commutation exact; integer spectrum exact; binomial multiplicities exact; σ_3 formula exact)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Per-site n̂_x has eigenvalues {0, 1}; Q̂_total = Σ n̂_x has integer spectrum {0, 1, ..., N} with binomial multiplicities C(N, k)."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - single-mode fermion creation/annihilation (definitional)
  - tensor product Fock space (definitional)
  - binomial coefficient counting (combinatorial)
```

Establishes **kinematic charge quantization** on the framework's Fock space: every state has an integer-valued total charge in {0, 1, ..., N_sites}, with no fractional or continuous Q permitted. Provides the Q-sector decomposition H = ⊕_k H_k that any Hamiltonian H (commuting with Q via N2) preserves.

Companion to:
- R3 Block 01 ([H, Q̂] = 0 — conservation)
- R5 Block 02 ([P̂, Q̂] = 0 — momentum-charge commute)
- R7 Block 02 (T_a covariance of any local operator — including local Q̂_x)

Together they close the framework's "Q-sector kinematics + dynamics + symmetry transport" picture.

Expected effective_status after clean Codex audit: **retained**.
