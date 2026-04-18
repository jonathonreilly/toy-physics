# DM Blocker 3 Deep Impossibility Triangulation — Candidate Retention Note

**Date:** 2026-04-18
**Status:** CANDIDATE THEOREM PROMOTION — seven-lane triangulation of the
DM flagship gate's direct-microscopic-selector blocker, replacing the
retained Case 3 Microscopic Polynomial Impossibility Theorem with a
sharper, baseline-conditional structural statement
**Dedicated verifier:**
`scripts/frontier_dm_blocker_3_deep_impossibility_triangulation.py`
**Relates to:**
`docs/DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`,
`docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`,
`docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`

## Summary

Seven structurally-independent axiom-only attack routes on the DM flagship
gate's direct-microscopic-selector blocker (blocker 3) all terminate at a
single unified structural wall. This note consolidates their results and
**retracts** the retained Case 3 Impossibility Theorem's strongest claim:
> *Every retained microscopic polynomial invariant of H on the active chart
> depends on (δ, q_+) only through (δ², q_+).*

That claim is accurate on the **source-only slice** `H_src = m·T_m +
δ·T_δ + q_+·T_q`, but **overstated on the full live family**
`H = H_base + H_src`. The live retained `H_base` explicitly breaks the
`(2 ↔ 3)` swap symmetry that generates δ-evenness, so
`Tr(H²), Tr(H³), det(H)` all carry nonzero δ-odd parts.

**Crucially, this crack does not close the selector gap.** The replacement
statement is sharper and more informative:

> **Blocker 3 is not a δ-evenness problem — it is a missing-physical-selector
> problem.** Local Cl(3)/Z³ data is rich enough to **invert from target values**
> (several two-equation systems on fixed `m` uniquely recover `(δ_*, q_+*)`;
> adding `Tr(H)` recovers the full triple), but the retained surface provides
> no **target-independent physical selector law** that would pick `(δ_*, q_+*)`
> as a special point without observational input.

The retained candidate extrema (Schur-Q, Tr(H²), det(H), Frobenius F1) all
land on the **chamber boundary** `q_+ = E_1 − δ`, while the observed pin is
**interior** with slack ≈ `0.015855` from the boundary. So extremum-type
selectors are both non-unique AND boundary-supported, whereas the
target is a specific interior point.

## Unit system and axiom base

- **Unit system:** dimensionless on `M_3(ℂ)`; real-trace pairing.
- **Axiom base:**
  - **A0.** Cl(3) on Z³ (single axiom).
  - **A1.** Retained affine chart `H = H_base + m·T_m + δ·T_δ + q_+·T_q`
    with `γ = 1/2`, `E_1 = √(8/3)`, `E_2 = √8/3`.
  - **A2.** `S_3` axis-permutation action (follows from Cl(3)/Z³ axiomatic
    equality of the three spatial axes plus retained hw=1 generation space).
  - **A3.** Observable principle `W[J] = log|det(D+J)| − log|det D|`
    (retained, `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`).

No PDG masses. No back-fitting.

## Seven-lane triangulation summary

Each lane attacks a distinct assumption in the retained Case 3 impossibility
framing. All seven independently-verified by dedicated runners.

| Lane | Assumption dropped | Verdict | Independently-verified content |
|---|---|---|---|
| A (spectral flow / topological index) | A2.3 (locality) | DEAD | **Every Z_3-invariant spectral functional (η, spectral flow, Maslov, APS mod-2, caustic count, Matsubara det) is δ-even** — extends Case 3 from local-polynomial to all Z_3-invariant spectral content (107/107 PASS) |
| B (Pfaffian / bivector) | A2.4 (`W[J]` is the canonical scalar generator) | DEAD / PARTIAL | ω-eigenvector-cubed scalars exist and are δ-odd, but **three independent defects**: phase-gauge dependence, q_+-blindness, CPT-odd non-observability (26/26 PASS) |
| C (chart change / `Im(z³)`) | A1.2 (affine chart parametrization) | PARTIAL | Naive `Im(z³)` construction fails Z_3-invariance; correct ω-eigenvector-cubed invariant `S(H) = 54·δ(δ² − m²)` is axiom-native δ-odd — **but q_+-independent**: real obstruction is q_+-silence, not δ-evenness (50/50 PASS) |
| D (cross-hw / full taste cube) | A2.5 (carrier is `H_hw=1`) | DEAD | **A_2 sign-irrep of `S_3` is absent from the taste-cube representation**: `C^8 ≅ 4A_1 ⊕ 2E`, `C^16 = 8A_1 ⊕ 4E`, `mult(A_2) = 0`. δ-odd observable content requires A_2; Cl(3)/Z³ supplies none (41/41 PASS) |
| E (combinatorial / equation selector) | A3.1 (variational) | DEAD / PARTIAL | **Theorem 3 crack:** full-H `Tr(H²), Tr(H³), det(H)` DO have δ-odd terms when `H_base` included; Z_3-reality equation `Im Tr(H² C_3) = 0` gives `q_+ = (√2−√6)/3 ≈ -0.345` **outside the physical chamber** — active chamber contradiction, stronger than silence (28/28 PASS) |
| F (discrete fixed-point / flow) | A3.3 (global extremum) | DEAD | Full retained discrete group `⟨C_3, T_x, T_y, T_z⟩` enumerated (24 elements); **zero** have fixed point at the observed pin; joint fixed-locus inconsistent; Z_3-averaging doesn't close on chart (25/25 PASS) |
| G (P-conditional / Schur-free) | A4.1 (Schur baseline) | DEAD | **Replacement theorem:** δ-evenness is baseline-conditional — holds iff `P H_base P = H_base` where `P = (2↔3)` swap. Live `H_base` has `‖P H_base P − H_base‖_F = √393/3`. Decisive at **`k = 2`** by Cayley-Hamilton. Amends retained Case 3 Theorem 3 (18/18 PASS) |

**Total: 295 independent checks across 7 lanes, all PASS.**

## The unified deep impossibility statement

Combining the seven lane results:

**Deep Impossibility (7-lane consolidation).**

*Let `H(m, δ, q_+) = H_base + m·T_m + δ·T_δ + q_+·T_q` be the retained
affine chart on `H_hw=1` (A1).*

1. **Source-only P-covariance** (Lane G). The `(2↔3)` swap `P ∈ S_3`
   generates δ-reflection on `H_src`: `P H_src(δ) P = H_src(−δ)`. Source-
   only δ-evenness of any conjugation-invariant polynomial follows.
2. **Full-H baseline-conditional crack** (Lane G, Lane E). Extension
   to the full family requires `P H_base P = H_base`, which the live
   `H_base` fails with `‖·‖_F = √393/3`. Hence `Tr(H²), Tr(H³), det(H)`
   have nonzero δ-odd parts, starting at quadratic order
   (`Tr(H²)_odd = −(16√6/3)·δ`).
3. **But extremum-based selectors miss the target** (Lane D, Lane F).
   Candidate retained extrema (Schur-Q, Tr(H²), det(H), Frobenius F1)
   are chamber-boundary solutions with `q_+ = E_1 − δ`. The observed
   pin `(δ_*, q_+*) = (0.933806, 0.715042)` is **interior** with slack
   `E_1 − δ_* − q_+* ≈ 0.015855`. No retained discrete action fixes
   the observed pin.
4. **Nonlocal and chart-change escapes are blocked** (Lane A, Lane B,
   Lane C). Every Z_3-invariant spectral functional is A_1-valued →
   δ-even; ω-eigenvector-cubed δ-odd invariants are CPT-odd
   (non-observable) and q_+-blind.
5. **The deep structural reason** (Lane D). The S_3 sign irrep A_2 is
   **absent** from the axiom-native taste-cube representation `C^8` and
   its `3+1`-lift `C^16`. δ-odd content in the observable sense requires
   A_2-valued scalars; Cl(3)/Z³ does not supply them.

**Consequence.** Blocker 3 cannot be closed by any combination of:
local-polynomial invariants, nonlocal spectral / topological invariants,
Z_3-invariant scalars of any order, retained discrete group-action fixed
points, CPT-even observables on `H_hw=1` alone, full-lattice taste-cube
cross-hw content, or equivariant Schur-reduced commutants.

## The sharper framing: inversion works, selection does not

Agent Lane E and the integrated analysis establish a **refined**
characterization of the blocker:

**Inversion is possible.** On fixed `m = m_* = 0.657061`, there exist
multiple two-equation systems using retained local data that uniquely
recover `(δ_*, q_+*)`. Example: `(Tr(H), Tr(H²))` at specified target
values yields the interior pin. Adding a third equation recovers the
full triple `(m, δ, q_+)`. So local data is **informationally
sufficient** to specify the pin.

**Target-independent selection is not.** No retained axiom-native
principle picks out the values `Tr(H)*`, `Tr(H²)*`, etc. *without*
knowing the target. The retained extrema (Schur-Q, Tr(H²), det(H), F1)
produce candidate pins, but these are:
- chamber-BOUNDARY points (not interior), and
- mutually incompatible — no single selector picks a unique pin.

**The real blocker is target-independent selection, not information
capacity.** The axiom surface can ENCODE the pin via local invariants;
it cannot DERIVE the pin.

This clarifies the research target:
- ❌ "Find a δ-odd local invariant" — red herring; they exist (Lane G) but
  are uninformative for selection (Lane E).
- ❌ "Find a global extremum" — DEAD (Lane F, Lane D boundary analysis).
- ❌ "Find a nonlocal spectral invariant" — DEAD (Lane A).
- ✅ **"Derive `H_base`'s P-breaking direction from a sharper Cl(3)/Z³
  principle and check whether it pins `(δ_*, q_+*)` as an interior point
  via matched chamber-zero locus."**

## Retained status changes (if retained)

| Item | Before | After 7-lane consolidation |
|---|---|---|
| Case 3 Theorem 3 δ-evenness scope | "every polynomial invariant is δ-even" | Accurate on `H_src`; **overstated on full H** (Lane G amendment) |
| Decisive order for δ-evenness | Unspecified high-order claim | **k=2 via Cayley-Hamilton + Newton identities** (Lane G) |
| Source of δ-evenness | Generic Z_3-doublet contraction | **Single `S_3` involution `P = (23)`** (Lane G) |
| Real blocker on full H | "no δ-odd content exists" | **"δ-odd content exists but is target-independent; no physical selector law"** |
| Nonlocal content | "open, unexplored" | **Provably does not escape on Z_3-invariant spectral functionals** (Lane A) |
| Cross-hw content | "speculative escape route" | **A_2-silence on `C^8` and `C^16`: no escape** (Lane D) |
| Retained candidate pins | Schur-Q, Tr(H²), det(H), F1 listed | **All chamber-boundary; target is interior with slack 0.0159** |
| Research target | Generic "nonlocal selector principle" | **Specific: derive H_base's P-breaking from Cl(3)/Z³** (Lane G) |

## Connection to Koide one-scalar obstruction triangulation

The Koide one-scalar obstruction triangulation theorem
(`KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`,
already landed on main) identified the charged-lepton Koide promotion
gap as a **single scalar** `κ = g_0²/|g_1|² = 2` on the retained
`C_3[111]` commutant of Hermitian source operators. The seven-lane DM
triangulation here converges on the **same structural pattern**:

| Problem | On retained surface | Single-scalar form | Structural class |
|---|---|---|---|
| Koide κ = 2 | A_1 content of circulant commutant | `g_0² = 2|g_1|²` on `D⁻¹` | S_3 / C_3 invariance class |
| DM `(δ_*, q_+*)` | Interior pin in 2-real chamber | No target-independent selector | S_3 / C_3 invariance class |

Both problems reduce to: **"the retained axiom surface is structurally
A_1-only for observables; the open scalar (κ in Koide; `(δ, q_+)`
direction in DM) requires A_2-like content or new S_3-breaking primitive
to close."** Any axiom-native derivation that closes one would close the
other.

## Reproduction

```bash
# Seven-lane master verifier
PYTHONPATH=scripts python3 scripts/frontier_dm_blocker_3_deep_impossibility_triangulation.py

# Individual lane verifiers
PYTHONPATH=scripts python3 scripts/frontier_dm_case3_z3_invariant_spectral_flow.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_bivector_pfaffian_scout.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_z3_doublet_phase_chart_scout.py
PYTHONPATH=scripts python3 scripts/frontier_dm_koide_cross_hw_shared_bottleneck_attack.py
PYTHONPATH=scripts python3 scripts/frontier_dm_blocker_3_lane_e_combinatorial_equation_selector.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_discrete_fixed_point_attractor_scout.py
PYTHONPATH=scripts python3 scripts/frontier_dm_blocker_3_lane_g_p_conditional_delta_evenness.py
```

All runners should emit `FAIL=0`.

## Proposed status classification

**CANDIDATE THEOREM PROMOTION — AWAITING REVIEW**

The theorem is mathematically tight:
- Seven independent axiom-only attack routes verified.
- 295 individual PASS checks across the lanes.
- Clean group-theoretic mechanism (Lane G: `P = (23) ∈ S_3`).
- Cayley-Hamilton decisive-order argument (Lane G).
- S_3 representation-theoretic unification (Lane D: `mult(A_2) = 0`).
- Amends retained Case 3 Theorem 3 with sharper conditional statement.
- Identifies specific tractable next research target.
- Converges with Koide one-scalar obstruction (already landed on main).

If retained, the DM flagship gate's selector-derivation target shifts from
"find any axiom-native selector" to the specific, tractable target:
**"derive `H_base`'s P-breaking direction from Cl(3)/Z³ and verify it
pins `(δ_*, q_+*)` as an interior chamber point."**

## File references

- Retained impossibility theorem (amended): `DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`
- Affine chart source: `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
- Observable principle: `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- Koide convergence: `KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md` (on main)
- Lane A: `docs/DM_CASE3_SPECTRAL_FLOW_NONLOCAL_INDEX_OBSTRUCTION_NOTE_2026-04-18.md`
- Lane B: `docs/DM_NEUTRINO_SOURCE_SURFACE_BIVECTOR_PFAFFIAN_SCOUT_NOTE_2026-04-18.md`
- Lane C: `docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_PHASE_CHART_SCOUT_NOTE_2026-04-18.md`
- Lane D: `docs/DM_KOIDE_CROSS_HW_SHARED_BOTTLENECK_SCOUT_NOTE_2026-04-18.md`
- Lane E: `docs/DM_BLOCKER_3_LANE_E_COMBINATORIAL_EQUATION_SELECTOR_SCOUT_NOTE_2026-04-18.md`
- Lane F: `docs/DM_NEUTRINO_SOURCE_SURFACE_DISCRETE_FIXED_POINT_ATTRACTOR_SCOUT_NOTE_2026-04-18.md`
- Lane G: `docs/DM_BLOCKER_3_LANE_G_P_CONDITIONAL_DELTA_EVENNESS_THEOREM_NOTE_2026-04-18.md`
- Master verifier: `scripts/frontier_dm_blocker_3_deep_impossibility_triangulation.py`
