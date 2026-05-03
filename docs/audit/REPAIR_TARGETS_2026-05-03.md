# Audit Failure Repair Targets — 2026-05-03

**Date:** 2026-05-03
**Source:** the 13 claims with `effective_status = audited_failed` as of
2026-05-03T18:27Z. Each row records the auditor's repair target, the
mechanical or substantive nature of the gap, and any in-flight repair
applied in this pass.

**Reading rule:** "mechanical" means the repair does not change physics
content (renamed import, stale string match, value reconciliation against
a current runner). "Substantive" means the repair changes a load-bearing
theorem statement, derivation, or verifier and requires fresh derivation
work plus an independent re-audit before retention.

The repair-status column does not promote any row to `retained` —
re-audit by an independent auditor remains required for that.

## Summary

| # | claim_id | criticality | claim_type | repair_class | this-pass action |
|---|---|---|---|---|---|
| 1 | `architecture_note_directional_measure` | critical | bounded_theorem | substantive | none — needs derivation of `beta = 0.8` from first principles, or demotion to "tuned support" |
| 2 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | critical | positive_theorem | substantive | **DONE** — Step 1 corrected to `Cl(3,0) ≅ M_2(C)` real-algebra identification; new Steps 2-3 introduce central pseudoscalar `ω = γ_1γ_2γ_3` (`ω² = -1`, central) and derive complexification splitting `Cl(3)⊗_R C ≅ M_2(C) ⊕ M_2(C)` with the two summands indexed by chirality `ω = ±i`; U2 restated as uniqueness-within-chirality (`ρ_+(γ_i) = +σ_i` canonical, `ρ_-(γ_i) = -σ_i` parity-conjugate, not unitarily equivalent); U4 hypothesis explicitly A1 + A3; runner adds E6 chirality exhibit (PASS=6/6); status reset to `unaudited` |
| 3 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | high | positive_theorem | substantive | **DONE** — (N1) restated on the `(2Z)^3` sublattice (the index-2 sublattice the runner actually verifies); proof Step 4 reworked with explicit two-site invariance derivation `η_ν(x + 2μ̂) = η_ν(x)`; new Step 5 documents why one-site shifts fail (η_2 and η_3 flip under x_1 → x_1 + 1); A2 hypothesis updated to `(2Z)^3` sublattice; corollary C2 narrows the Brillouin zone description; runner labels updated to match; runner stays PASS=4/4; status reset to `unaudited` |
| 4 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | positive_theorem | substantive (research-grade) | none — needs first-principles derivation of OS factorisation for the exact A_min staggered+Wilson SU(3) action, not citation of OS/STW/Menotti |
| 5 | `axiom_first_spin_statistics_theorem_note_2026-04-29` | medium | positive_theorem | substantive (chained) | **DONE** — chained on the #2 cl3 repair. Fact 2.1 updated to acknowledge the chirality structure (both `ρ_+` and `ρ_-` are 2-dim, so the dimensional conclusion the chain depends on is chirality-independent); Fact 2.5 updated; Hypothesis section made explicit that A1 enters via cl3's U2/U4 and A3 + A1 give the per-site Fock-space dimension match; (S1)-(S4) and runner unchanged (PASS=4/4); status reset to `unaudited` |
| 6 | `bh_entropy_derived_note` | critical | bounded_theorem | substantive | none — runner has internally inconsistent pass aggregation (failed subchecks, but PASSED 6/6); finite-L 1/4 match is class G; needs derivation of BH coefficient or honest demotion |
| 7 | `circulant_response_master_identity_narrow_theorem_note_2026-05-02` | medium | positive_theorem | mechanical | **DONE** — kappa formulation now restricted to `g_1 != 0`; global cone equation `g_0² = 2|g_1|²` is the canonical statement; runner still PASS=16/0; status reset to `unaudited` for re-audit |
| 8 | `complete_prediction_chain_2026_04_15` | medium | positive_theorem | partially mechanical | **partially DONE** — stale m_H values updated to runner output (`125.10` vs old `129.7`, runner is the live computation). Structural gaps remain: (a) note's one-hop dependencies are not registered in the citation graph, (b) runner hardcodes load-bearing bridges. Status reset to `unaudited` from note hash drift |
| 9 | `dm_pmns_z3_doublet_block_center_positive_sheet_no_go_theorem_note_2026-04-20` | medium | no_go | mechanical | **DONE** — runner's PART 4 register check now points at the current authoritative I5 status note (`DM_PMNS_LOCAL_SELECTOR_FAMILY_NO_GO_THEOREM_NOTE_2026-04-20.md`) rather than the refactored open-imports register. Runner now PASS=12/0. The no-go geometry was already correct per audit; this clears the brittle string-match block. Re-audit can now ratify as `retained_no_go` |
| 10 | `ew_coupling_derivation_note` | medium | bounded_theorem | substantive | none — note's `g_1` calculation diverges from the runner's `taste_weight` parameter scan; needs note↔runner re-synchronisation, plus the open `g_2(v)` and `lambda(v)` derivations the note explicitly defers |
| 11 | `fifth_family_radial_boundary_note` | medium | positive_theorem | mechanical (executable evidence restored) | **DONE** — runner imports now point at the current API (`_build_radial_shell_connectivity` is in `DISTANCE_LAW_PORTABILITY_COMPARE.py`; `_measure_family` is in `CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP.py`). Runner reproduces the exact `(drift=0.20, seed=0)` boundary row the note claims (`plus = -2.028e-06, minus = +2.028e-06`). The "no independent derivation" gap remains: this is restored as a bounded empirical observation, not a closed theorem |
| 12 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | medium | bounded_theorem | substantive | none — runner uses seeded least-squares to find 2 nondegenerate roots; needs interval arithmetic, symbolic resultant, or degree-counting certificate to rule out additional roots in the bounded chart |
| 13 | `higgs_mass_from_axiom_note` | high | positive_theorem | substantive | none — note's headline 140.3 GeV is the tree-level `m_H = v/(2u_0)` value; named runner reports 119.93 GeV via a different RGE route. Deeper issue is the asserted-not-derived map from taste-channel curvature to physical Higgs mass (audit class F). Needs (a) derivation of the curvature-to-physical-readout normalisation, (b) note↔runner reconciliation on which observable is the headline |

## Repair classes

### Mechanical (3 of 13 done)

These do not change theorem content. They restore executable evidence
or align documentation with the current code, both of which the audit
explicitly required.

- ✅ #7 `circulant_response_master_identity_narrow_theorem_note_2026-05-02` — kappa domain restriction
- ✅ #9 `dm_pmns_z3_doublet_block_center_positive_sheet_no_go_theorem_note_2026-04-20` — runner register check
- ✅ #11 `fifth_family_radial_boundary_note` — runner import drift

### Partially mechanical (1 of 13, partial)

- ◐ #8 `complete_prediction_chain_2026_04_15` — value reconciliation done; structural dependency-registration and runner-bridge issues remain

### Substantive (theorem restatements) — 3 of 3 done

- ✅ #2 `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` — `Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C)` chirality split; canonical positive-chirality convention; runner E6 chirality exhibit
- ✅ #3 `axiom_first_lattice_noether_theorem_note_2026-04-29` — restated to `(2Z)^3` sublattice symmetry; one-step shifts documented as out-of-scope staggered/taste symmetries
- ✅ #5 `axiom_first_spin_statistics_theorem_note_2026-04-29` — chained on #2; chirality-independent dimensional conclusion preserves the chain

### Substantive (research-grade) — none done

These need fresh derivation work and should not be done without an
independent reviewer or substantial new physics input.

- ☐ #1 `architecture_note_directional_measure` — derive `beta = 0.8` or demote
- ☐ #4 `axiom_first_reflection_positivity_theorem_note_2026-04-29` — derive OS factorisation for exact A_min, not citation
- ☐ #6 `bh_entropy_derived_note` — derive BH coefficient or demote class G match
- ☐ #10 `ew_coupling_derivation_note` — derive `g_2(v)`, `lambda(v)`; runner re-sync
- ☐ #12 `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` — global root count certificate
- ☐ #13 `higgs_mass_from_axiom_note` — derive curvature-to-physical-readout normalisation

## Net effect on the ledger

| stage | `audited_failed (effective)` | `unaudited` (reset for re-audit) |
|---|---:|---:|
| Before this pass | 13 | — |
| After mechanical (PR #485 commits 1-5) | 11 | +2 (circulant kappa, complete_prediction_chain m_H) |
| After substantive (PR #485 commits 6-8) | 8 | +5 (lattice_noether, cl3, spin_statistics; the runner-only #9 and #11 are still audited_failed but with working runners) |

## What this document is not

- Not a substitute for re-audit. None of the rows above are promoted by
  this document. Mechanical fixes restore the conditions under which an
  independent auditor can re-evaluate; substantive fixes still require
  fresh derivation work.
- Not a justification for archival. Per the user's clarification on
  2026-05-03, `retained_no_go` must mean a proven negative result, not
  a broken positive proof routed through `archive_unlanded/`. Failed
  positive theorems stay visible as `audited_failed` until either
  repaired (followed by re-audit) or genuinely closed as a proven no-go.
