# Claim Status Certificate — R2 Block 03 (CMW 2D/1D sublattice no-SSB)

**Date:** 2026-05-02
**Block:** R2-03 — No SSB on 1D/2D sublattices of Z^3 from retained CMW
**Slug:** `positive-only-r2-20260502`
**Branch:** `physics-loop/positive-only-r2-block03-cmw-low-d-20260502`
**Note:** [docs/CMW_2D_SUBLATTICE_NO_SSB_THEOREM_NOTE_2026-05-02.md](../../../../docs/CMW_2D_SUBLATTICE_NO_SSB_THEOREM_NOTE_2026-05-02.md)
**Runner:** [scripts/cmw_2d_sublattice_no_ssb_check.py](../../../../scripts/cmw_2d_sublattice_no_ssb_check.py)
**Log:** [outputs/cmw_2d_sublattice_no_ssb_check_2026-05-02.txt](../../../../outputs/cmw_2d_sublattice_no_ssb_check_2026-05-02.txt)

## Strict-bar gate

- claim_type: positive_theorem ✓
- single load-bearing dep at retained-grade on live ledger ✓ (`axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29` is at `effective_status: retained`)
- zero admitted physics inputs ✓ (sublattice definition + Hamiltonian restriction are structural)
- runner produces classifiable PASS lines ✓ (5/5 PASS, including IR-divergence verification at three dimensions)

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "On any 1D line or 2D plane sublattice of the framework's Z^3, no continuous global symmetry can spontaneously break at any finite temperature T > 0; the Gibbs state is unique."
admitted_context_inputs:
  - sublattice definition (structural)
  - restriction of Hamiltonian to sublattice (structural)
upstream_dependencies:
  - axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29 (effective_status: retained)
runner_classified_passes: 5 PASS at machine precision (I_1 linear divergence, I_2 logarithmic divergence, I_3 finite limit, divergence ratios stable, Bogoliubov bound decreasing)
```

## Expected `effective_status` after audit

If Codex returns clean + positive_theorem → `effective_status = retained`.
