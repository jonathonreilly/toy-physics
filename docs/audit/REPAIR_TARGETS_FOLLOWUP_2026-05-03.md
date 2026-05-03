# Audit-Repair Followups — 2026-05-03 (post-PR #485 landing)

**Date:** 2026-05-03 (second pass)
**Source:** post-landing re-audit findings on `main` after PR #485
landed via commit `46d9fda67` (review-loop bundle).

PR #485 landed only the substantive theorem restatements (#2 cl3, #3
lattice_noether, #5 spin_statistics) and the mechanical fixes (#7
circulant kappa, #8 m_H reconciliation, #9 dm_pmns_z3 register check,
#11 fifth_family runner imports). The research-grade attacks for #1,
#4, #6, #10, #12, #13 did not land, and post-landing re-audits
exposed two new gaps in the substantive repairs.

This followup pass:

1. Closes the two post-landing re-audit gaps (#2 A3 bridge, #3 (5)
   algebraic closure)
2. Rebuilds the 6 research-grade attacks that did not land in PR #485

## Post-landing re-audit findings

### #2 `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29`

**Audit verdict (fresh-agent-riemann, post-landing):**
`audited_conditional` — "U4 imports A3's one-Grassmann-pair
staggered-fermion normalization to identify the abstract 2-dim Cl(3)
chirality module with the physical per-site Hilbert space ... the
sole permitted dependency, `MINIMAL_AXIOMS_2026-04-11.md`, is
explicitly superseded and states that the staggered/Grassmann
realization is recategorized out of the current primitive axiom set,
so the physical bridge is not retained-grade in the restricted
packet."

**Repair:** added a second audit-driven repair section to the cl3
note that cites `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03`
(`claim_type=open_gate`, `audit_status=audited_clean`) as the
retained-grade open-gate authority. U2 and U3 (algebraic content)
remain unconditional on A1 alone. **U4 is now explicitly conditional
on the open gate**: "if A3 (one Grassmann pair per site) is admitted
as the physical-lattice realization, then per-site Hilbert dim = 2
follows from U2's chirality-summand dim = 2."

This conditional-on-open-gate status is honest: the open gate is the
package-acknowledged route from A1+A2 to the staggered-Grassmann
realization, and the new `MINIMAL_AXIOMS_2026-05-03.md` explicitly
lists the cl3 / spin-statistics / lattice-noether chains as
conditional on this gate's positive closure.

### #3 `axiom_first_lattice_noether_theorem_note_2026-04-29`

**Audit verdict (fresh-agent-turing, post-landing):**
`audited_failed` again — "the load-bearing specialization of the
general current formula (5) to (N1) and (N2) does not close
algebraically, and the runner passes only symmetry/current exhibits
rather than checking that (5) derives (3) and (4)."

**Repair:** the original (5) form
```
J^{μ,A}_x = Σ_y η_μ(x) T^A_{xy} (χ̄_x χ_{x+μ̂} - χ̄_{x+μ̂} χ_x)/2
```
factors as `[Σ_y T^A_{xy}] · η_μ(x) · (χ̄_x χ_{x+μ̂} - χ̄_{x+μ̂} χ_x)/2`,
so for U(1) phase `T = i δ` it gives `(i/2) η_μ(x) (χ̄_x χ_{x+μ̂} -
χ̄_{x+μ̂} χ_x)` — wrong sign and missing the bilateral structure of
(4). For (2Z)^3 translation `T^μ_{xy} = δ_{y, x+2μ̂} - δ_{y, x-2μ̂}`,
`Σ_y T^μ_{xy} = 0`, giving zero current — also wrong.

**Corrected (5)** derived explicitly in Step 2 from local-α variation
under the canonical staggered hop (`M_{x, x±μ̂} = ±(1/2) η_μ(x)`):

```text
J^{μ,A}_x = (1/2) η_μ(x) [ χ̄_x T̂^A χ_{x+μ̂}  +  χ̄_{x+μ̂} T̂^A χ_x ]
```

The bilateral two-term structure arises from the **forward + reindexed
backward hops** of the staggered KS action.

**Step 4 specialisations** now close algebraically:
- (5) under U(1) phase generator → (4) fermion-number current (with
  the `i ↔ real` convention adjustment).
- (5) under (2Z)^3 sublattice translation generator → (3) staggered
  momentum density via the standard discrete-derivative form.

**New runner exhibit E5** verifies the (5) → (4) closure
algebraically on a small lattice: computes both `J^μ_x` from the
bilateral (5) under `T = i I` substitution and the canonical (4)
form, confirms `||J5_real - J4||_max < 1e-12`. Runner now PASS=5/5.

## Research-grade attacks (rebuilt from PR #485)

These attacks did not land in PR #485's review-loop bundle but the
underlying source files exist on the PR branch. This followup pass
re-applies them to `main` with the post-landing audit findings
incorporated.

### #1 `architecture_note_directional_measure`
- New runner `architecture_directional_measure_table_runner_2026_05_03.py`
  reproduces the table on fixed DAG fixtures (PASS=6/6).
- Note cites `ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE` and
  identifies `β = 0.8` as closure route 3 (eikonal observable
  matching).

### #4 `axiom_first_reflection_positivity_theorem_note_2026-04-29`
- Explicit OS hypothesis-match table for A_min carrier.
- Step 3a derives `det(M) ≥ 0` from γ_5-Hermiticity + staggered ε ±λ
  paired eigenvalues (not citation).
- (R3) restated with explicit vacuum-energy subtraction.
- Runner adds E5 (`{ε, M_KS} = 0`) and E6 (`det(M) ≥ 0`),
  PASS=6/6.

### #6 `bh_entropy_derived_note`
- Runner pass/fail accounting repaired: 2D/3D split, OR-aggregation
  removed, RT-vs-1/4 demoted to OBSERVATION (per Widom no-go),
  finite-size extrapolation tested against Widom 1/6.
- Repaired runner: PASS=5/5 (was misleading 6/6).

### #10 `ew_coupling_derivation_note`
- New primary runner `ew_coupling_bounded_status_runner_2026_05_03.py`
  reproduces note's bounded scope without fitting `taste_weight`.
- D1 g_1(v) DERIVED via 1-loop U(1) RGE; D2 g_2(v) BOUNDED at Landau
  pole; D3 λ(v) BOUNDED at CW + stability; D4 y_t sensitivity table.
- PASS=4/4.

### #12 `gauge_vacuum doublet`
- New runner `gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py`
  uses 3660 seeds (~20× original 175); all converged seeds cluster
  onto same 2 distinct roots.
- Empirical certificate; symbolic / interval-arithmetic certificate
  remains genuine open work.
- PASS=4/4.

### #13 `higgs_mass_from_axiom_note`
- Scope sharpened to TREE-LEVEL mean-field (not physical Higgs mass).
- Step 5 restated with explicit "actual derivation" labelling.
- New runner `higgs_tree_level_mean_field_runner_2026_05_03.py`
  reproduces formula and explicitly distinguishes from corrected-y_t
  (119.93 GeV) and Buttazzo runners as separate observables.
- PASS=5/5.

## Net effect on the ledger

Pre-followup state on `main`: `audited_failed (effective) = 15`.

Expected post-followup state: significant reduction once the rebuilt
research-grade attacks plus the #2 A3 bridge and #3 (5) algebraic
closure trigger note-hash drift and reset the corresponding rows
from `audited_failed` to `unaudited` (awaiting fresh re-audit).

The substantive content preservation across all repairs has been
audited in [`STEP_BACK_EVALUATION_2026-05-03.md`](STEP_BACK_EVALUATION_2026-05-03.md)
(from PR #485, may need to be re-applied here).
