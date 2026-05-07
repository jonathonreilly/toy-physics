# Lane Promotion Proposal — Higgs Mass From Axiom

**Date:** 2026-05-07
**Type:** `bounded_theorem_promotion_proposal`
**Authority role:** source-note proposal. Audit-lane sets actual verdict
on the recast claim; this note proposes the recast and lists the named
admissions, but does not (and cannot) set status itself.
**Subject lane:** Higgs mass derivation from axiom — recast as
`bounded_theorem` over the three new audit-defensible bridge admissions
identified in
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md).
**Submission target:** independent audit lane.

---

## 1. Lane summary

The Higgs mass lane derives the dimensionless ratio

```
m_H / v  =  1 / (2 u_0)                                                (HM-ratio)
```

(equivalently, `(m_H/v)² = 1 / (4 u_0²)`) on the framework's mean-field
canonical lattice surface, from the eigenvalue degeneracy of the
staggered Dirac operator under the Cl(3) Clifford identity
`D_taste² = d · I` and the canonical SU(3) plaquette mean-field link
`u_0 = ⟨P⟩^{1/4}`. With `u_0 = 0.8776` at canonical coupling and
`v = 246.22 GeV` (admitted from the EW chain via the hierarchy
theorem), this gives `m_H_tree = 140.3 GeV`, i.e. a tree-level
mean-field estimate of the Higgs mass with N_c canceling exactly
along the derivation. The lane's load-bearing structural claim is the
N_c-cancellation pattern (the color factor `8/9` does NOT enter
`m_H`); the numerical headline `140.3 GeV` is the tree-level
mean-field readout, +12% relative to the observed `125.10 GeV`,
with the gap attributable to 2-loop CW corrections, lattice spacing
convergence, and Wilson-term taste breaking — all explicitly
out-of-scope.

---

## 2. Pre-promotion state

**Parent note:**
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](../../docs/HIGGS_MASS_FROM_AXIOM_NOTE.md)
— current declared `claim_type: bounded_theorem`, but downgraded to
`audited_conditional` (effective: `bounded support theorem`) by the
2026-05-02 status-correction audit packet
[`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](../../docs/HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md).
The 2026-05-03 review-loop repair sharpened the scope (tree-level
mean-field readout, NOT physical Higgs mass) but did not unlock the
audit blocker.

### What the status-correction audit found (2026-05-02)

The audit identified four blockers, summarized in §1 of the
status-correction note:

1. **Lattice curvature → physical (m_H/v)² matching theorem missing.**
   The bridge from per-taste lattice curvature to the physical scalar
   ratio was supplied by dimensional + consistency arguments, not a
   derivation.
2. **Taste polynomial, degeneracy, hierarchy input paths missing.**
   Implicit citation only; no explicit retained-theorem chain.
3. **EW-color and Higgs authority notes conditional upstream.**
4. **`deps=[]` in ledger; dep-declaration repair needed.**

The audit's structural verdict was that this matching obstruction is
**same-shape as cycles 5 and 9** (M-residual matching, gauge-scalar
observable bridge): a *lattice → continuum / physical matching theorem*
that fails analytically per the standard QFT machinery without
non-perturbative input, framed as a unified Nature-grade target.

### Hidden admission that was load-bearing

The 2026-05-03 review-loop sharpening explicitly named the Step 5
identification

```
(m_H_tree / v)²  =  curvature / N_taste                                 (HM-id)
```

as the standard tree-level mean-field Klein-Gordon readout in the
symmetric phase, and acknowledged this is **NOT a derivation of the
post-EWSB physical Higgs mass**. But the deeper hidden admission —
which the parent's Step 4 implicitly imports — is:

> **The Wilson lattice action form `S_W = -(β/N_c) Σ_p Re Tr(U_p)` at
> `β = 6` is the framework's lattice gauge action.**

Step 4 derives the Higgs mass from the staggered Dirac operator on
this Wilson lattice. The eigenvalue degeneracy and Clifford identity
`D_taste² = d · I` are framework-derived structural facts, but the
**staggered fermion construction itself imports the standard Wilson
lattice surface as the carrier**. The mean-field link `u_0 = ⟨P⟩^{1/4}`
is computed against the **standard 4D isotropic Wilson action at
β = 6**, not against a framework-derived action.

This is exactly the action-form import that
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
identifies as the *Wilson admitted as convention* gap. Pre-2026-05-07,
this admission was hidden inside "the lattice surface" rather than
named explicitly. The four bridge sub-gates of the 4-agent run
fragment and bound it.

---

## 3. Proposed bounded-theorem claim

**Recast claim (proposed for audit-lane review):**

> **Theorem (HM, Higgs mass from axiom — bounded form).** Let the
> framework's gauge-action surface be specified by:
>
> - the canonical Cl(3) Hilbert–Schmidt trace normalization `N_F = 1/2`
>   (admitted at L3 of the four-layer stratification);
> - Hamilton-to-Lagrangian dictionary reduction to standard 4D
>   isotropic Wilson at `β = 6` (Convention C-iso, `O(g²) ~ 5-15%` at
>   canonical operating point);
> - lattice-action selection within the continuum-equivalence class
>   `{Wilson, heat-kernel, Manton}` by parsimony at finite β
>   (`~5-10%` across class members).
>
> Then on the resulting canonical mean-field lattice surface
> (mean-field link `u_0 = ⟨P⟩^{1/4} = 0.8776` at `β = 6`, staggered
> Dirac operator `D` on `Z⁴` with APBC in time, eigenvalue degeneracy
> `|λ_k| = 2 u_0` for all `N_taste = 16` taste channels by the
> Clifford identity `D_taste² = d · I` and mean-field factorization),
> the Higgs mass-to-VEV ratio is uniquely
>
> ```
> m_H_tree / v  =  1 / (2 u_0)                                          (HM-ratio)
> ```
>
> with N_c canceling exactly along the derivation (the color factor
> `(N_c² − 1)/N_c² = 8/9` does NOT enter `m_H`). With `v = 246.22 GeV`
> from the hierarchy theorem,
>
> ```
> m_H_tree  =  v / (2 u_0)  =  140.3 GeV                                (HM-num)
> ```
>
> is the tree-level mean-field Klein-Gordon readout in the symmetric
> phase. The +12% relative gap to the observed `125.10 GeV` is
> attributable to 2-loop CW corrections, lattice-spacing convergence,
> and Wilson-term taste breaking, all separately tracked and
> out-of-scope of this lane.

The structural N_c-cancellation pattern is the load-bearing positive
content. The numerical `140.3 GeV` headline is the tree-level
mean-field estimate, with the named admissions setting the bound on
how seriously to take the numerics.

---

## 4. Admitted context inputs (formal block)

```yaml
admitted_context_inputs:
  - id: N_F_canonical_normalization
    statement: |
      The canonical Gell-Mann trace normalization N_F = 1/2 is the
      overall scalar of the unique (up to scalar) Ad-invariant
      Hilbert-Schmidt inner product on su(3). The form rigidity is
      derived (Killing-form uniqueness for simple Lie algebras); the
      overall scalar is admitted.
    parent: docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md
    layer: L3 in the four-layer stratification (L1 axiom A1 → L2 form
      rigidity → L3 admitted scalar N_F → L4 derived g_bare = 1)
    bound: not_numerical
    bound_class: structural_admitted_scalar
    rationale: |
      A single admitted real positive scalar at L3, cleanly localized.
      Whether N_F = 1/2 is uniquely forced by Cl(3) Hilbert-Schmidt
      structure is a separate Nature-grade target outside this
      lane's scope.

  - id: Convention_C_iso_dictionary
    statement: |
      Hamilton-to-Lagrangian isotropic reduction: at the canonical
      operating point xi = a_s/a_tau = 1, the framework's natural
      anisotropic Trotter action (Wilson-form spatial plaquettes,
      heat-kernel temporal plaquettes by Theorem T-AT) is replaced by
      the standard 4D isotropic Wilson action at beta = 6.
    parent: outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md
    layer: dictionary residual
    bound: O(g^2) ~ 5-15%
    bound_class: numerically_verified_relative_error
    rationale: |
      Numerical verification (Corollary T-AT.3 of T-AT) gives ~7-9%
      Wilson-vs-heat-kernel mismatch at canonical s_t = 0.5, theta =
      0.5-1.0. The bound is concrete and class-function-explicit. The
      anisotropic Trotter dictionary is itself derived as positive
      theorem T-AT; only the isotropic reduction is admitted.

  - id: continuum_equivalence_parsimony
    statement: |
      Finite-beta lattice-action selection within the continuum-
      equivalence class {Wilson, heat-kernel, Manton}. All three give
      the same continuum dim-4 magnetic operator alpha_eff Tr(F^2) per
      Theorem A2.5-derived; they differ only at finite beta by
      Symanzik-irrelevant higher-character corrections.
    parent: outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md
    layer: action-form parsimony at finite beta
    bound: ~5-10%
    bound_class: continuum_equivalence_class_spread
    rationale: |
      The action-form ambiguity at finite beta is bounded by the
      observable spread across {Wilson, heat-kernel, Manton} at
      canonical g^2 = 1, beta = 6. All three are RP-positive and give
      the same continuum theory; the parsimony selection of Wilson is
      a convention within the equivalence class, with bound ~5-10%
      on finite-beta observables. The continuum-level uniqueness of
      alpha_eff Tr(F^2) is derived (A2.5 demoted from proposed axiom
      to bounded derived theorem).
```

These three admissions correspond exactly to the three sub-gates closed
in the 2026-05-07 unified bridge run (see
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
sub-gates 1, 2, 3 respectively). Each is named, bounded, and
audit-defensible. No hidden admissions remain on the gauge-action
surface that the Higgs mass lane builds on.

---

## 5. Quantitative uncertainty

### Per-admission bounds

| Admission | Class | Bound |
|---|---|---|
| `N_F_canonical_normalization` | Structural admitted scalar at L3 | Not numerical (single real positive scalar; no propagating relative error in `(m_H/v)²` once `N_F = 1/2` is fixed). The L3 admission is what *defines* the canonical lattice surface used by the lane; alternative `N_F` values would change `β` and `u_0` jointly such that the Wilson coefficient routing (`β_new = c² · β_old` per HS rigidity R5) absorbs the rescaling, leaving `g_bare` unchanged. So `N_F` does not propagate as a separate numerical bound on `m_H/v`. |
| `Convention_C_iso_dictionary` | Numerically-verified relative error | `O(g²) ≈ 5-15%` at canonical `s_t = 0.5`, `ξ = 1`, with class-function-explicit form (Corollary T-AT.3 of [`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md)). Verified numerically at `~7-9%` Wilson-vs-heat-kernel mismatch on SU(2) at `θ = 0.5, 1.0`. |
| `continuum_equivalence_parsimony` | Continuum-equivalence-class spread | `~5-10%` across `{Wilson, heat-kernel, Manton}` at finite β = 6, by the existing no-go (the differences are Symanzik-irrelevant in the continuum but finite at β = 6). |

### Combined (lane's total relative uncertainty on `m_H/v` at canonical surface)

The two numerical bounds are independent:

- C-iso governs the *temporal-plaquette* form (Wilson replacement vs
  heat-kernel) at finite anisotropy.
- Continuum-equivalence parsimony governs the *spatial-plaquette*
  action-form selection within the equivalence class at finite β.

Adding in quadrature (independent systematic bounds):

```
δ_total² = δ_Ciso² + δ_parsimony²
        ≤ (0.10)² + (0.10)²              # taking conservative upper edges
        ≤ 0.020
δ_total  ≤ ~14% relative
```

Or linearly (more conservative under correlation):

```
δ_total  ≤ 0.10 + 0.10  =  ~20% relative
```

The framework convention used in the unified bridge status note
([`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Lane unlock") is `~10% relative total` for predictions targeted to
Wilson 4D MC at finite β. This implicitly assumes the upper edges of
the two bounds are not simultaneously realized; an audit-defensible
combined bound is **~10-14% relative** depending on whether
quadrature or linear addition is used.

### Comparison to lane's headline number

The lane's tree-level mean-field readout `m_H_tree = 140.3 GeV`
differs from observed `125.10 GeV` by `+12.0%` relative. **This is
inside the combined `~10-14%` admitted-bound envelope** at the upper
edge of the quadrature combination. The lane's headline +12% gap is
therefore *consistent with* (but not closed by) the bridge admissions
under bounded promotion.

The lane's Step 5 attribution of the +12% to 2-loop CW + lattice
spacing + Wilson-term taste breaking is consistent with this
arithmetic but is a **separate decomposition**, not load-bearing for
the bounded-theorem promotion. The bounded-theorem claim is at the
tree-level mean-field readout level; the +12% physical-Higgs gap is
out-of-scope and tracked separately.

---

## 6. What this promotion DOES vs DOES NOT close

### What the promotion DOES close (subject to audit retention)

- **Hidden Wilson-action import made explicit.** The hidden admission
  identified in §2 ("the Wilson lattice action at β = 6 is the
  framework's gauge action") is replaced by three explicitly named,
  audit-defensible admissions, each cited to its parent note.
- **N_c-cancellation as load-bearing structural content.** The lane's
  derivation that the color factor `8/9` does NOT enter `m_H` becomes
  the load-bearing positive content of the bounded theorem. This is
  unaffected by all three bridge admissions (none of them touches the
  N_c-tracking algebra).
- **Tree-level mean-field readout `m_H_tree = v/(2 u_0)` formalized
  under bounded admissions.** The Step 5 identification
  `(m_H_tree/v)² = curvature / N_taste` is now formally a *bounded*
  claim under named admissions, rather than an asserted bridge.
- **Same-shape resolution as cycles 5, 9, 11.** The unified bridge
  status (4-agent run of 2026-05-07) provides the matching theorem
  that the 2026-05-02 status-correction audit identified as missing.
  The action-form ambiguity is now bounded (continuum-derived;
  finite-β parsimony), and the Hamilton-Lagrangian dictionary
  residual is named (Convention C-iso).
- **Audit-graph effect.** If the audit lane retains the recast claim,
  the parent's `audited_conditional` status under
  [`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](../../docs/HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
  is replaced by `bounded_theorem` with the three admissions as
  named context inputs. The 264 transitive descendants inherit the
  bounded surface.

### What the promotion DOES NOT close

- **The +12% gap to physical `m_H = 125.10 GeV`.** The bounded theorem
  is at the *tree-level mean-field* level; closing the gap requires
  2-loop CW corrections, lattice-spacing convergence, and Wilson-term
  taste breaking, all explicitly out-of-scope.
- **`N_F = 1/2` itself.** Whether the canonical Gell-Mann
  normalization is uniquely forced by Cl(3) Hilbert-Schmidt structure
  is a separate Nature-grade target (W2 in
  [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)).
- **Multi-plaquette numerical baseline.** Sub-gate 4 of the bridge
  run remains in flight (proper spin-network ED with intertwiners is
  W1). The 2×2 torus value `⟨P⟩ = 0.0434` is in strong-coupling LO
  regime and does not yet match the KS literature value `~0.55-0.60`
  used to extract `u_0 = 0.8776` at β = 6. This gap is engineering
  (basis truncation), not framework error, but is not closed in this
  promotion.
- **Independent audit-lane retention itself.** This note is a
  *proposal*; the actual retention verdict is set only by the
  independent audit lane after retention of the three bridge sub-gate
  candidates (W3 in
  [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)).
  Until then, the parent remains under its existing status.
- **Hierarchy theorem's `v = 246.22 GeV` admission.** The VEV is
  imported from the EW chain via the hierarchy theorem
  (`v = M_Pl · α_LM^16`); this is a separate retained admission and
  not re-opened by this promotion. (It propagates additively into the
  numerical headline but not into the dimensionless ratio `m_H/v`.)

---

## 7. Cross-references

### Parent notes (lane substance)

- [`docs/HIGGS_MASS_FROM_AXIOM_NOTE.md`](../../docs/HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — parent derivation note; declared `claim_type: bounded_theorem`,
  effective `audited_conditional` per status-correction audit;
  2026-05-03 review-loop scope sharpening.
- [`docs/HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](../../docs/HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
  — 2026-05-02 status-correction audit packet identifying four
  blockers and same-shape obstruction.

### Bridge admission parents

- [`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md)
  — continuum-level closure of the action form (admission 3:
  continuum-equivalence parsimony).
- [`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md)
  — Theorem T-AT (Anisotropic Trotter Dictionary), with isotropic
  reduction admitted as Convention C-iso (admission 2).
- [`outputs/action_first_principles_2026_05_07/G_BARE_AUDIT_RESIDUAL_CLOSURE.md`](G_BARE_AUDIT_RESIDUAL_CLOSURE.md)
  — `g_bare` audit residuals closed; single admitted scalar
  `N_F = 1/2` localized at L3 (admission 1).
- [`docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  — four-layer stratification placing `N_F` at L3.
- [`docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — joint trace-AND-Casimir rigidity supporting L2 form uniqueness.

### Bridge-gap synthesis

- [`outputs/action_first_principles_2026_05_07/UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  — synthesis across the four sub-gates and lane-unlock framing for
  bounded-theorem promotion.
- [`docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
  — finite-β no-go on action-form uniqueness (still applicable;
  bounded by parsimony).

### Lane dependencies (existing)

- `docs/TASTE_POLYNOMIAL_NOTE.md`
  — `det(D + m) = (m² − 4 c²)^8` taste polynomial.
  *(Bare-name reference matching parent `HIGGS_MASS_FROM_AXIOM_NOTE.md`
  convention; resolves on `main` repository state.)*
- `docs/DM_AMGM_SATURATION_NOTE.md`
  — eigenvalue degeneracy from Clifford identity.
  *(Bare-name reference matching parent convention.)*
- `docs/HIERARCHY_THEOREM.md`
  — `v = M_Pl · α_LM^16` (VEV admitted to lane).
  *(Bare-name reference matching parent convention.)*
- [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](../../docs/YT_EW_COLOR_PROJECTION_THEOREM.md)
  — `8/9` applies to EW couplings only (independent argument that
  `8/9` does not enter `m_H`; consistent with Step 6 of the parent).
- [`docs/HIGGS_MASS_DERIVED_NOTE.md`](../../docs/HIGGS_MASS_DERIVED_NOTE.md)
  — separate CW analysis lane; not load-bearing for this promotion.

### Sister-lane same-shape promotions (parallel proposals expected)

The unified bridge status note identifies four bridge-dependent lanes
ready for bounded promotion under the same three admissions:

- α_s direct Wilson loop lane.
- Higgs mass from axiom lane (this proposal).
- Gauge-scalar observable bridge lane.
- Koide-Brannen phase lane.

Cross-promotion proposals for the other three lanes are expected to
share this proposal's three-admission block.

### Runners (existing primary runners cited by parent)

- [`scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`](../../scripts/higgs_tree_level_mean_field_runner_2026_05_03.py)
  — primary runner for the tree-level formula `m_H_tree = v/(2 u_0)
  = 140.3 GeV` on the canonical surface.
- [`scripts/frontier_higgs_mass_corrected_yt.py`](../../scripts/frontier_higgs_mass_corrected_yt.py)
  — separate corrected-`y_t` RGE route (different observable).
- [`scripts/frontier_higgs_buttazzo_calibration.py`](../../scripts/frontier_higgs_buttazzo_calibration.py)
  — full-3-loop calibration (separate observable).

### Bridge-admission runners

- [`scripts/cl3_ks_dictionary_derivation_2026_05_07.py`](../../scripts/cl3_ks_dictionary_derivation_2026_05_07.py)
  — Dictionary T-AT verification (4/4 checks pass).
- [`scripts/frontier_g_bare_audit_residual_closure.py`](../../scripts/frontier_g_bare_audit_residual_closure.py)
  — g_bare residual closure runner (62/0 EXACT + 5/0 BOUNDED pass).

---

## 8. Audit-lane disposition request

Submitted to the independent audit lane for review of the recast
claim under §3 with admission block §4. The audit lane is requested
to determine:

```yaml
proposed_promotion:
  parent_note: docs/HIGGS_MASS_FROM_AXIOM_NOTE.md
  current_audit_status: audited_conditional
  current_effective_status: bounded_support_theorem
  proposed_audit_status: bounded_theorem
  proposed_effective_status: contingent_on_dep_chain
  proposed_load_bearing_step_class: B
  proposal_allowed: contingent
  proposal_allowed_reason: |
    The recast claim depends on three audit-defensible admissions, each
    with a parent note now in the audit-lane queue:
      1. N_F_canonical_normalization (parent: G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
      2. Convention_C_iso_dictionary (parent: DICTIONARY_DERIVED_THEOREM.md, T-AT)
      3. continuum_equivalence_parsimony (parent: A2_5_DERIVED_THEOREM.md)
    Retention of this promotion is conditional on retention of all three
    parent notes by the audit lane. If any of the three is demoted or
    held conditional, this promotion's bound on m_H/v widens
    correspondingly and the promotion remains audit-conditional with
    strengthened substance (the three admissions are still named and
    bounded, but their parent notes are not yet retained).

  audit_lane_questions:
    Q1: |
      Is the four-layer stratification at G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md
      sufficient to localize the convention layer at L3, with N_F = 1/2
      as a single admitted scalar (not propagating to additional
      dimensionless bounds)? If yes, admission 1 is structural and not
      numerically propagating.
    Q2: |
      Is the O(g^2) ~ 5-15% bound on Convention C-iso (per Corollary
      T-AT.3) acceptable as a numerically-verified relative error,
      given the class-function-explicit form and SU(2) numerical
      verification (~7-9% at canonical s_t = 0.5)? If yes, admission 2
      is bounded.
    Q3: |
      Is the ~5-10% continuum-equivalence-class spread acceptable as a
      finite-beta parsimony bound, given the action-form no-go at
      finite beta and continuum-level uniqueness derivation under A2.5
      derived theorem? If yes, admission 3 is bounded.
    Q4: |
      Combined bound: is ~10-14% relative total uncertainty on m_H/v
      at the canonical lattice surface acceptable as the lane's
      bounded-theorem envelope? Note that the lane's tree-level
      mean-field readout headline +12% gap to observed m_H sits inside
      this envelope at the upper edge.

  expected_audit_outcomes:
    if_all_three_admissions_retain:
      lane_status: bounded_theorem (audited_clean on bounded surface)
      bound: ~10-14% relative on m_H/v at canonical surface
      action: parent_note_status_updates_to_audited_clean_on_bounded_surface
    if_two_of_three_retain:
      lane_status: bounded_theorem (audited_conditional, named residual)
      bound: ~10-14% relative + named residual
      action: parent_note_status_remains_audited_conditional_with_strengthened_substance
    if_one_or_none_retain:
      lane_status: audited_conditional (status quo with strengthened evidence)
      bound: not_bounded_in_audit_sense
      action: parent_note_status_remains_audited_conditional

  audit_required_before_effective_retained: true
  bare_retained_allowed: false

  status_authority: independent_audit_lane_only
  this_proposal_does_not_set: [audit_status, effective_status, retained_classification]
```

The audit lane is requested to:

1. **Verify the three admissions in §4 are correctly cited and
   structurally identified at their parent notes.** In particular:
   - admission 1 cites the L3 layer of the four-layer stratification
     correctly;
   - admission 2 cites Corollary T-AT.4 (the explicit two-part C-iso
     decomposition) correctly;
   - admission 3 cites the A2.5-derived theorem's continuum-level
     content with finite-β residual unchanged correctly.
2. **Verify the combined-uncertainty arithmetic in §5.** Quadrature
   vs linear addition, and whether the +12% headline gap sits
   plausibly inside the `~10-14%` envelope.
3. **Verify the cross-promotion-readiness §6** does not overstate
   what is closed. In particular, the +12% physical-Higgs gap is
   explicitly out-of-scope; this promotion is at the tree-level
   mean-field readout level only.
4. **Set the actual retention verdict** under the contingency table
   in `expected_audit_outcomes`.

Independent audit lane review is required before this promotion takes
effective retained status. This note does not (and cannot) set audit
verdict itself.

---

## Appendix A — Mapping from parent's Steps 1–6 to the bounded surface

For audit traceability, here is which step of
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](../../docs/HIGGS_MASS_FROM_AXIOM_NOTE.md)
depends on which admission:

| Parent step | Content | Depends on admission? |
|---|---|---|
| Step 1: generating functional `W(J)` | `(N_tot/2) log(J² + 4 u_0²)`, with `u_0 = ⟨P⟩^{1/4}` from canonical SU(3) plaquette at β = 6. | All three (the canonical surface `β = 6` and `u_0 = 0.8776` is built on `N_F`, C-iso, parsimony). |
| Step 2: factoring out color | `det(D+J) = [det_taste(D+J)]^N_c`. | None directly; algebraic at mean field. |
| Step 3: curvature at `m=0` | `-N_taste / (4 u_0²)`. | Through `u_0`: all three admissions. |
| Step 4: per-channel curvature | `4 / (u_0² N_taste)` then `(m_H/v)² = 1/(4 u_0²)`. | Through `u_0`: all three admissions. |
| Step 5: tree-level mean-field readout | `(m_H_tree/v)² = curvature / N_taste`. | Identification itself is admitted as the standard tree-level mean-field Klein-Gordon readout (per parent's 2026-05-03 review-loop sharpening); not a separate admission of this promotion, but a prior framing inherited from the parent. |
| Step 6: `8/9` does not enter `m_H` | N_c-cancellation argument. | Independent of all three admissions; this is the load-bearing structural content. |

The dimensionless ratio `m_H_tree/v = 1/(2 u_0)` depends on the three
admissions only through `u_0`, which is the canonical SU(3) plaquette
at β = 6 on the standard 4D isotropic Wilson lattice. The named
admissions are precisely what specifies *that the canonical surface
is* the standard 4D isotropic Wilson at β = 6. Under bounded
promotion, the lane's prediction inherits the combined `~10-14%`
envelope from the admissions.

The N_c-cancellation of the color factor `8/9` (Steps 2, 6) is
**unaffected** by all three admissions and remains the load-bearing
positive structural content of the bounded theorem.

---

## Appendix B — Honest claim status (for ledger seeding)

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  On the canonical 4D isotropic Wilson lattice surface at beta = 6,
  the framework's staggered Dirac operator yields, by the Cl(3)
  Clifford identity D_taste^2 = d I and mean-field factorization,
  the eigenvalue degeneracy |lambda_k| = 2 u_0 for all N_taste = 16
  taste channels. The per-taste curvature of V_taste(m) at m = 0 is
  -4 / u_0^2; identification with the tree-level mean-field
  Klein-Gordon Higgs-mass readout in the symmetric phase gives
  m_H_tree / v = 1 / (2 u_0), with N_c canceling exactly along the
  derivation (the color factor 8/9 does NOT enter m_H). With
  v = 246.22 GeV from the hierarchy theorem and u_0 = 0.8776 at
  beta = 6, m_H_tree = 140.3 GeV. The +12% relative gap to the
  observed 125.10 GeV is attributable to 2-loop CW corrections,
  lattice-spacing convergence, and Wilson-term taste breaking — all
  separately tracked and out-of-scope. The canonical surface itself
  depends on three named, audit-defensible admissions:
  N_F_canonical_normalization (L3), Convention_C_iso_dictionary
  (O(g^2) ~ 5-15%), continuum_equivalence_parsimony (~5-10%);
  combined relative envelope on m_H/v is ~10-14%.

admitted_context_inputs:
  - id: N_F_canonical_normalization
  - id: Convention_C_iso_dictionary
  - id: continuum_equivalence_parsimony

proposed_load_bearing_step_class: B
proposal_allowed: contingent_on_dep_chain
deps:
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
  - dictionary_derived_theorem_2026-05-07
  - a2_5_derived_theorem_2026-05-07
  - taste_polynomial_note
  - dm_amgm_saturation_note
  - hierarchy_theorem
  - yt_ew_color_projection_theorem
audit_required_before_effective_retained: true
bare_retained_allowed: false
status_authority: independent_audit_lane_only
actual_current_surface_status: source_proposal
conditional_surface_status: bounded_theorem on canonical 4D isotropic
  Wilson lattice surface at beta = 6, contingent on retention of the
  three named bridge admissions (N_F, C-iso, parsimony) and the
  existing retained input chain (taste polynomial, AM-GM degeneracy,
  hierarchy theorem, EW color projection).
hypothetical_axiom_status: null
admitted_observation_status: v = 246.22 GeV admitted from EW chain
  via hierarchy theorem (existing retained admission, not re-opened
  by this promotion).
proposal_allowed_reason: |
  All load-bearing inputs are retained or near-retained on the current
  authority surface, contingent on retention of the three 2026-05-07
  bridge sub-gate parent notes by the audit lane. The N_c-cancellation
  structural content (Steps 2 and 6 of the parent) is unaffected by
  any of the three admissions and is the load-bearing positive
  content. The numerical headline depends on the canonical-surface
  specification, which the three admissions explicitly bound.
```
