# Claim Status Certificate — R5 Block 03 (Per-site Hilbert ≅ j=1/2 su(2) irrep)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r5-block03-per-site-spin-half-20260502`
**Note:** docs/PER_SITE_SU2_SPIN_HALF_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/per_site_su2_spin_half_check.py

## Strict-bar gate

- claim_type: positive_theorem ✓
- single retained-grade one-hop dep ✓ (`axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` retained)
- zero admitted physics inputs ✓ (admitted-context inputs are mathematical: bivector → spin Lie algebra and Casimir ↔ irrep label correspondence)
- runner: 7/7 PASS at machine precision (Cl(3) anticommutation exact; su(2) Lie algebra exact; Casimir = 3/4 exact; S_z eigenvalues ±1/2 exact)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Per-site Cl(3) Hilbert ≅ unique j=1/2 irrep of su(2); no other per-site spin content possible."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - bivector → spin generator identification (Clifford → spin Lie algebra)
  - Casimir ↔ irrep label correspondence (Schur / standard Lie algebra)
```

Closes the previously-stipulated "matter is spin-1/2" load-bearing input to `axiom_first_spin_statistics_theorem_note_2026-04-29` as a derived per-site representation-theoretic fact. Together with R4 Block 01 (per-site dim = 2), uniquely pins the framework's elementary fermion spin label at j = 1/2.

Expected effective_status after clean Codex audit: **retained**.
