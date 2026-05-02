# Claim Status Certificate — R10 Block 01 (Staggered chiral-symmetric spectrum)

**Date:** 2026-05-02
**Branch:** `physics-loop/positive-only-r10-block01-staggered-chiral-symmetry-20260502`
**Note:** docs/STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/staggered_chiral_symmetry_check.py

## Strict-bar gate (with R10 stricter criteria from quality review)

- **claim_type**: positive_theorem ✓
- **single retained-grade one-hop dep** ✓ (`cpt_exact_note` retained — supplies H_phys = i·D, C = diag(ε(x)), {C, H_phys} = 0)
- **zero admitted physics inputs** ✓ (only mathematical: spectral theorem for finite-dim Hermitian operators)
- **runner**: 7/7 PASS at machine precision

### Stricter R10 quality gates (added after quality review of R5-R9 PRs)

- ✓ **Result is non-obvious given the retained dep.** cpt_exact_note states [CPT, H] = 0 and SME=0, but does **NOT** extract σ(H) = −σ(H) from C: H ↦ −H. This block makes the spectral consequence explicit.
- ✓ **Framework specificity is load-bearing.** Uses staggered ε(x) sublattice parity construction directly. Result requires bipartite Z³ lattice geometry (even L) to hold; doesn't generalize to arbitrary qubit/Hermitian systems.
- ✓ **No admitted-context input restates the conclusion.** "{C, H} = 0" is cited as input from the retained note (not "spectrum is symmetric"). The chiral-pairing derivation is the new content.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "σ(H_phys) = -σ(H_phys); chiral pairing C|E⟩ ↔ |-E⟩; chiral index dim ker_+ - dim ker_- on staggered lattice."
upstream_dependencies:
  - cpt_exact_note (retained)
admitted_context_inputs:
  - spectral theorem for finite-dim Hermitian operators
```

The runner exhibits the 4³ = 64 spectrum: 8 zero modes (Brillouin-zone corners), 28 positive, 28 negative — a balanced "Dirac" spectrum reflecting the chiral C-pairing.

Expected effective_status after clean Codex audit: **retained**.
