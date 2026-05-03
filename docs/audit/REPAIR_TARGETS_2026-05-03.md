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
| 1 | `architecture_note_directional_measure` | critical | bounded_theorem | substantive (closure-route documentation + runner) | **DONE** — runner [`scripts/architecture_directional_measure_table_runner_2026_05_03.py`](../../scripts/architecture_directional_measure_table_runner_2026_05_03.py) reproduces all 6 table rows on fixed DAG fixtures (Born rule, V > 0.95, k=0 → real, gravity sign 6/8 attract, gravity scaling R(8..20) > 0, beta-sweep monotonicity); architecture note now cites [`ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`](../ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md) (existing bounded no-go) as the retained dependency that explains why β = 0.8 is empirical, not derivable from primitive axioms; β handling explicit per the no-go's "safe wording" — observable-matched (route 3) against eikonal slope, with empirical Gaussian moment-match (β ≈ 0.595) flagged as distinct from the gravity-card value 0.8; status reset to `unaudited` |
| 2 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | critical | positive_theorem | substantive | **DONE** — Step 1 corrected to `Cl(3,0) ≅ M_2(C)` real-algebra identification; new Steps 2-3 introduce central pseudoscalar `ω = γ_1γ_2γ_3` (`ω² = -1`, central) and derive complexification splitting `Cl(3)⊗_R C ≅ M_2(C) ⊕ M_2(C)` with the two summands indexed by chirality `ω = ±i`; U2 restated as uniqueness-within-chirality (`ρ_+(γ_i) = +σ_i` canonical, `ρ_-(γ_i) = -σ_i` parity-conjugate, not unitarily equivalent); U4 hypothesis explicitly A1 + A3; runner adds E6 chirality exhibit (PASS=6/6); status reset to `unaudited` |
| 3 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | high | positive_theorem | substantive | **DONE** — (N1) restated on the `(2Z)^3` sublattice (the index-2 sublattice the runner actually verifies); proof Step 4 reworked with explicit two-site invariance derivation `η_ν(x + 2μ̂) = η_ν(x)`; new Step 5 documents why one-site shifts fail (η_2 and η_3 flip under x_1 → x_1 + 1); A2 hypothesis updated to `(2Z)^3` sublattice; corollary C2 narrows the Brillouin zone description; runner labels updated to match; runner stays PASS=4/4; status reset to `unaudited` |
| 4 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | positive_theorem | substantive (research-grade) | **DONE** — explicit OS hypothesis-match table verifies each OS/STW/MP precondition against A_min; new Step 3a derives `det(M) ≥ 0` from γ_5-Hermiticity + staggered ε-paired ±λ eigenvalues (instead of citation); (R3) restated with explicit vacuum-energy subtraction (`T̃ := T/λ_max(T)`); runner adds E5 (`{ε, M_KS} = 0`) and E6 (`det(M) ≥ 0`), PASS=6/6 |
| 5 | `axiom_first_spin_statistics_theorem_note_2026-04-29` | medium | positive_theorem | substantive (chained) | **DONE** — chained on the #2 cl3 repair. Fact 2.1 updated to acknowledge the chirality structure (both `ρ_+` and `ρ_-` are 2-dim, so the dimensional conclusion the chain depends on is chirality-independent); Fact 2.5 updated; Hypothesis section made explicit that A1 enters via cl3's U2/U4 and A3 + A1 give the per-site Fock-space dimension match; (S1)-(S4) and runner unchanged (PASS=4/4); status reset to `unaudited` |
| 6 | `bh_entropy_derived_note` | critical | bounded_theorem | substantive (runner accounting + observation/PASS split) | **DONE** — runner pass/fail accounting repaired: each subcheck split into 2D vs 3D; OR-based aggregation removed (was masking 3D 51% deviation); RT-ratio-vs-1/4 demoted to OBSERVATION ONLY (consistent with the retained Widom no-go that the asymptote is 1/6 not 1/4); finite-size extrapolation now tested against Widom 1/6 instead of 1/4; area-law thresholds aligned with the note's documented R² > 0.998 (was using 0.999 internally); frozen-star scaling marked as by-construction sanity not PASS. Repaired runner: PASS=5/5 (down from misleading 6/6, now honest); note's check table replaced with observation-vs-PASS split |
| 7 | `circulant_response_master_identity_narrow_theorem_note_2026-05-02` | medium | positive_theorem | mechanical | **DONE** — kappa formulation now restricted to `g_1 != 0`; global cone equation `g_0² = 2|g_1|²` is the canonical statement; runner still PASS=16/0; status reset to `unaudited` for re-audit |
| 8 | `complete_prediction_chain_2026_04_15` | medium | positive_theorem | partially mechanical | **partially DONE** — stale m_H values updated to runner output (`125.10` vs old `129.7`, runner is the live computation). Structural gaps remain: (a) note's one-hop dependencies are not registered in the citation graph, (b) runner hardcodes load-bearing bridges. Status reset to `unaudited` from note hash drift |
| 9 | `dm_pmns_z3_doublet_block_center_positive_sheet_no_go_theorem_note_2026-04-20` | medium | no_go | mechanical | **DONE** — runner's PART 4 register check now points at the current authoritative I5 status note (`DM_PMNS_LOCAL_SELECTOR_FAMILY_NO_GO_THEOREM_NOTE_2026-04-20.md`) rather than the refactored open-imports register. Runner now PASS=12/0. The no-go geometry was already correct per audit; this clears the brittle string-match block. Re-audit can now ratify as `retained_no_go` |
| 10 | `ew_coupling_derivation_note` | medium | bounded_theorem | substantive (new bounded-status runner) | **DONE (note↔runner re-sync)** — new primary runner [`scripts/ew_coupling_bounded_status_runner_2026_05_03.py`](../../scripts/ew_coupling_bounded_status_runner_2026_05_03.py) reproduces exactly the note's bounded scope: D1 g_1(v) DERIVED via 1-loop U(1) RGE from M_Pl (~+27% from observed, expected at 1-loop SU(5)), D2 g_2(v) BOUNDED with Landau pole barrier explicitly identified, D3 λ(v) BOUNDED with CW lower bound + stability upper window, D4 y_t sensitivity table reproducing note Part 5. No `taste_weight` fit anywhere. The taste-weight runner (`frontier_yt_ew_coupling_derivation.py`) remains in the repo as a separate distinct derivation attempt and is no longer named as this note's primary runner. PASS=4/4. The structural claim about g_2 and λ remaining BOUNDED until SU(2) non-perturbative matching is derived is unchanged — that's the honest scope. |
| 11 | `fifth_family_radial_boundary_note` | medium | positive_theorem | mechanical (executable evidence restored) | **DONE** — runner imports now point at the current API (`_build_radial_shell_connectivity` is in `DISTANCE_LAW_PORTABILITY_COMPARE.py`; `_measure_family` is in `CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP.py`). Runner reproduces the exact `(drift=0.20, seed=0)` boundary row the note claims (`plus = -2.028e-06, minus = +2.028e-06`). The "no independent derivation" gap remains: this is restored as a bounded empirical observation, not a closed theorem |
| 12 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | medium | bounded_theorem | substantive (empirical dense-seed certificate) | **DONE (empirical certificate)** — new runner [`scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py`](../../scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py) uses 3660 seeds (~20× the original 175): 2160 structured + 1500 random uniformly across the bounded chart. All 2201 converged seeds (60%) cluster onto the same two distinct roots — no additional cluster emerges. Per-cell volume ~8.5e-3 rad³, vs chart volume ~31 rad³. The bounded theorem now records local exact-solve + empirical global root-count; symbolic / interval-arithmetic certificate (resultants for transcendental target) remains genuine open work. Note acknowledges the empirical-vs-symbolic distinction. PASS=4/4. |
| 13 | `higgs_mass_from_axiom_note` | high | positive_theorem | substantive (scope sharpening + new tree-level runner) | **DONE** — note's scope sharpened to **TREE-LEVEL mean-field** estimate `m_H_tree = v/(2 u_0) = 140.3 GeV` (NOT the physical Higgs mass; the +12% gap requires CW + RGE corrections out-of-scope here). Step 5 restated: (a) dimensional matching is necessary not sufficient, (b) tree-level mean-field Klein-Gordon readout IS the actual derivation (with explicit limits where it's exact), (c) susceptibility is consistency cross-check not independent. New primary runner [`scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`](../../scripts/higgs_tree_level_mean_field_runner_2026_05_03.py) reproduces the formula via T1 V_taste curvature, T2 per-channel curvature, T3 m_H_tree value, T4 N_c-independence, T5 explicit distinction from corrected-y_t (119.93 GeV) and Buttazzo runners as separate observables. PASS=5/5. The corrected-y_t runner is no longer named as primary; it remains a separate auxiliary calculation along a different chain. |

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

### Substantive (research-grade) — 1 of 6 done (closure-route documentation)

These need fresh derivation work and should not be done without an
independent reviewer or substantial new physics input. Where existing
work in the repo establishes a no-go on the naive derivation, the
honest repair cites that no-go and documents which closure route the
empirical value sits on.

- ✅ #1 `architecture_note_directional_measure` — β handling made explicit per the existing angular-kernel underdetermination no-go (closure route 3, observable matching against eikonal); runner added that reproduces the table on fixed DAG fixtures
- ✅ #4 `axiom_first_reflection_positivity_theorem_note_2026-04-29` — explicit OS hypothesis-match table (each OS/STW/MP precondition verified against A_min carrier); explicit Step 3a derivation of `det(M) ≥ 0` via γ_5-Hermiticity + ε-paired eigenvalues (no longer just citation); `(R3)` restated as vacuum-energy-subtracted `T̃ := T/λ_max(T)`, `H̃ := -log(T̃)/a_τ` so `||T̃|| = 1` is automatic; runner adds E5 (staggered chirality anticommutation `{ε, M_KS} = 0`) and E6 (`det(M) ≥ 0` across multiple sizes/masses on the canonical surface), now PASS=6/6 (was 4/4)
- ✅ #6 `bh_entropy_derived_note` — runner accounting repaired (5/5 honest), RT-vs-1/4 demoted to observation, finite-size extrapolation tested against Widom 1/6 (the retained no-go)
- ✅ #10 `ew_coupling_derivation_note` — note↔runner re-sync done (new primary runner reproduces note's bounded scope without fitting taste_weight); g_2(v)/lambda(v) deeper derivation remains open
- ✅ #12 `gauge_vacuum_plaquette doublet` — empirical dense-seed root-count certificate (3660 seeds, all converged seeds cluster to same 2 roots); symbolic certificate remains open work
- ✅ #13 `higgs_mass_from_axiom_note` — scope sharpened to tree-level mean-field; Step 5 restated with explicit "actual derivation" labelling; new primary runner reproduces tree-level formula and distinguishes from other Higgs runners

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
