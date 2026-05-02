# Claim Status Certificate — R2 Block 02 (CPT lifetime equality)

**Date:** 2026-05-02
**Block:** R2-02 — CPT particle/antiparticle lifetime equality
**Slug:** `positive-only-r2-20260502`
**Branch:** `physics-loop/positive-only-r2-block02-cpt-lifetime-20260502`
**Note:** [docs/CPT_PARTICLE_ANTIPARTICLE_LIFETIME_EQUALITY_THEOREM_NOTE_2026-05-02.md](../../../../docs/CPT_PARTICLE_ANTIPARTICLE_LIFETIME_EQUALITY_THEOREM_NOTE_2026-05-02.md)
**Runner:** [scripts/cpt_particle_antiparticle_lifetime_check.py](../../../../scripts/cpt_particle_antiparticle_lifetime_check.py)
**Log:** [outputs/cpt_particle_antiparticle_lifetime_check_2026-05-02.txt](../../../../outputs/cpt_particle_antiparticle_lifetime_check_2026-05-02.txt)

## Strict-bar gate

- claim_type: positive_theorem ✓
- single load-bearing dep at retained-grade on live ledger ✓ (`cpt_exact_note` is at `effective_status: retained`)
- zero admitted physics inputs ✓ (resonance pole convention + CPT operator action are structural)
- runner produces classifiable PASS lines ✓ (4/4 PASS including negative control)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Γ_antiparticle = Γ_particle (and hence τ equal) for every unstable species in the retained matter content."
admitted_context_inputs:
  - resonance pole convention
  - CPT operator action on resonance states
  - antiunitary conjugation preserves resonance pole structure
upstream_dependencies:
  - cpt_exact_note (effective_status: retained)
runner_classified_passes: 4 PASS at machine precision (identical |Im(E)|, width equality, 5-trial universality, negative control without CPT shows split widths)
```

## Expected `effective_status` after audit

If Codex returns clean + positive_theorem → `effective_status = retained`.

## Implementation note

Convention bug caught during runner development: under the antiunitary CPT representation, particle and antiparticle have complex-conjugate eigenvalues (equal energies, opposite-sign Im parts). The physical decay-width equality is `|Im(E_p)| = |Im(E_a)|`, not signed Im equality. Updated runner accordingly.
