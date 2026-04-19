# Review: `frontier/lepton-mass-tower`

Reviewed branch tip: `63b1e5ec`
Review date: 2026-04-19
Reviewer: independent verification agent (opus 4.7, strict Cl(3)/Z³-only check)

## Verdict

**CONFIRMED — promotable to retained after two minor cosmetic cleanups.**

Independent re-execution of `scripts/frontier_koide_z3_scalar_potential.py`: **33/33 PASS**.

All load-bearing algebraic claims are exact and reproducible. The Clifford-involution
derivation of the scalar potential coefficients is a genuine axiom-tight result.

## Verified (exact)

| Claim | Status |
|---|---|
| `T_m² = I_3` (Clifford involution) | EXACT, machine precision |
| `Tr(T_m) = 1`, `Tr(T_m²) = 3`, `Tr(T_m³) = 1`, `det(T_m) = -1` | EXACT |
| `V(m) = V_0 + (c_1 + c_2/2)·m + (3/2)·m² + (1/6)·m³` | EXACT (symbolic re-expansion; 4×10⁻¹⁵ match at 9 test points) |
| Cubic coupling `1/6` pinned by `Tr(T_m³) = 1` | EXACT |
| Quadratic `3/2` pinned by `Tr(T_m²) = 3` | EXACT |
| `det(K_sel)` leading coefficient = -1 from Levi-Civita / `det(T_m) = -1` | EXACT, machine-precision fit |
| `Tr(K_frozen) = 0` kills m² cross-term in Tr(K³) | EXACT |
| V_eff minimum at `m_V ≈ -0.433` from `m² + 6m + 2L = 0` with `L ≈ 1.2057` | EXACT |
| Physical `m_* ≈ -1.1605` ≠ V_eff minimum (0.73 gap) | CONFIRMED; honestly flagged in note |
| Mass matching at `m_*`: sqrt-mass errors < 0.05% after one scale | CONFIRMED (on sqrt-mass metric with hardcoded witness; see cleanup #1 below) |
| Transport gap `1/η_ratio = 5.297` vs `4π/√6 = 5.130` (3.1% gap) | CONFIRMED as observation-only; honestly flagged |
| `κ(m_pos) = -1/√3` at positivity threshold | EXACT, matches to 10⁻¹² |

## NEW axiom-native finding (bonus — extends the retained structure)

> **`Tr(K_frozen) = 0` is actually stronger than stated: it holds at `m = 0` for ALL `(δ, q)` in the affine slice, not just the selected value `δ = q = √6/3`.**
>
> This is a structural property of `kz_from_h ∘ active_affine_h`, not just a coincidence at the selected point.

**Implication:** the m² cross-term vanishing in `Tr(K³)` is a general affine-slice identity, not tied to the Koide selected slice. This extends the retained axiom-tight structure beyond what the original note claimed and strengthens the derivation: the scalar potential's m² cross-term vanishing holds throughout the chamber, not just at the Koide selector point.

Worth capturing as an explicit lemma in the theorem note.

## Minor cleanups flagged (non-blocking)

1. **Stale hardcoded `kappa_star` value in the runner.** 
   - Runner hardcodes `kappa_star = -0.6079056980`
   - Retained `hstar_witness_kappa()` returns `-0.607912649682`
   - Discrepancy: `7×10⁻⁶`
   - Consequence: mass-level electron error reports as `9.2×10⁻⁴` (0.092%) instead of the `4.6×10⁻⁴` (0.046%) that holds with the retained witness. All three masses are under 0.05% on the mass level when the retained witness is used.
   - **Recommended fix:** replace the magic number with `from frontier_koide_selected_line_cyclic_response_bridge import hstar_witness_kappa; kappa_star = hstar_witness_kappa()`.

2. **`c_2` docstring.** 
   - Runner comment suggests `c_2 = 7√6/6` (= 2.8577) 
   - Numerically `c_2 = 35/12` (= 2.91667) exactly, verified to `4×10⁻¹³`
   - **Recommended fix:** update docstring / comment to `c_2 = 35/12`. Not load-bearing (numerics pass either way).

3. **"< 0.05%" metric specification in theorem note.**
   - Current phrasing in `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md` doesn't specify mass vs sqrt-mass.
   - The 0.05% claim holds on **sqrt-mass** with the hardcoded witness, and on **mass** with the retained witness.
   - **Recommended fix:** either specify "< 0.05% on sqrt(mass)" explicitly, or adopt cleanup #1 (retained witness) so the claim holds on the more intuitive mass metric.

## Open gap (honestly documented in the note)

V_eff minimum at `m_V ≈ -0.433` does NOT coincide with the physical selected point
`m_* ≈ -1.1605`. The V(m) potential alone does not select `m_*`; the H_* witness
ratio `r_* = w_*/v_* ≈ 4.1009` (equivalently `κ_* ≈ -0.6079`) does. Whether
this witness ratio is itself axiom-derivable remains an open research target,
correctly flagged in the note.

## Recommendation

**Promote to retained** after cleanups #1 and #2. The cubic coupling `g_3 = 1/6`
being forced by `Tr(T_m³) = 1` — not fitted — is a genuine axiom-tight result
worth landing. The new generalized `Tr(K_frozen) = 0` finding (bonus above)
strengthens it further.

## Files examined (reviewer side)

- `scripts/frontier_koide_z3_scalar_potential.py` (the runner — 33/33 PASS)
- `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` (affine chart source)
- `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` (K_Z3 source)
- `scripts/frontier_koide_selected_line_cyclic_response_bridge.py` (retained H_* witness)
- `scripts/frontier_dm_leptogenesis_full_microscopic_reduction.py` (retained η_ratio)
- `docs/KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md` (theorem note)
