# Claim Status Certificate — R2 Block 01 (Lattice momentum conservation)

**Date:** 2026-05-02
**Block:** R2-01 — Lattice total momentum conservation from cited Noether
**Slug:** `positive-only-r2-20260502`
**Branch:** `physics-loop/positive-only-r2-block01-momentum-conservation-20260502`
**Note:** [docs/LATTICE_TOTAL_MOMENTUM_CONSERVATION_THEOREM_NOTE_2026-05-02.md](../../../../docs/LATTICE_TOTAL_MOMENTUM_CONSERVATION_THEOREM_NOTE_2026-05-02.md)
**Runner:** [scripts/lattice_total_momentum_conservation_check.py](../../../../scripts/lattice_total_momentum_conservation_check.py)
**Log:** [outputs/lattice_total_momentum_conservation_check_2026-05-02.txt](../../../../outputs/lattice_total_momentum_conservation_check_2026-05-02.txt)

## Strict-bar gate

- claim_type: positive_theorem ✓
- single load-bearing dependency named ✓ (`axiom_first_lattice_noether_theorem_note_2026-04-29`)
- zero admitted physics inputs ✓ (discrete divergence theorem and on-shell condition are pure math/structural)
- runner produces classifiable PASS lines ✓ (5/5 PASS at machine precision)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "P_total^μ(t) = sum_{x⃗} P^μ_{(t,x⃗)} is t-independent on shell; [P̂_total, H] = 0 on H_phys; periodic-lattice momentum spectrum {2π n / L_s}."
admitted_context_inputs:
  - discrete divergence theorem on the periodic lattice (pure combinatorics)
  - on-shell condition (structural)
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29
runner_classified_passes: 5 PASS at machine precision
source_sets_audit_outcome: false
```

## Review-loop status authority

This block proposes a `positive_theorem` claim type and leaves all row
outcome decisions to the independent audit lane.
