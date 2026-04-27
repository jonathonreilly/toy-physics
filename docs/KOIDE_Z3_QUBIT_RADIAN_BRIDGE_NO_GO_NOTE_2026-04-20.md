# Koide Z_3-Qubit Radian-Bridge No-Go Note

**Date:** 2026-04-20
**Lane:** Scalar-selector cycle 1 — closure attempt on the residual radian-bridge postulate P.
**Status:** **No-go.** Postulate P cannot be closed from proposed_retained Cl(3)/Z³ + d=3 on
the physical selected-line CP¹ base. The precise obstruction and the minimal
additional structural input are named.
**Primary runner:** `scripts/frontier_koide_z3_qubit_radian_bridge_no_go.py` (PASS=23 FAIL=0)
**Companion:** `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` §4 (names P).

---

## 0. Summary

Postulate **P** asserts `ρ_δ := (real DOF of b) / (real dim Herm_d) = 2/d² = δ (radians)`,
i.e. at d=3, `2/9 (dimensionless) = 2/9 (radians)`. The task candidate theorem
was: on the physical selected line, the Pancharatnam-Berry holonomy per Z_3
cyclic element on the qubit CP¹ equals `2/d²` in radians at d=3.

**Result: fails.** The PB holonomy per Z_3 element on the qubit equator is
`π/3` at d=3 (a rational multiple of π), not `2/9`. Three subsidiary retained
closure candidates (full-orbit Bargmann, Plancherel-weight, interior-point
structural selector) each fail in a specific checked way. The structural
obstruction is sharp.

---

## 1. Retained ingredients used

- **R1.** Selected-line CP¹ PB structure (KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md §4):
  `s(m) = (1/√2)v_1 + (1/2)e^{iθ(m)}v_ω + (1/2)e^{-iθ(m)}v_ω̄`,
  projective doublet `[1:e^{-2iθ}]`, `A = dθ`, `δ(m) = θ(m) − 2π/3` open-path holonomy.
- **R2.** Bundle obstruction (KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md):
  physical base is an interval; no closed-loop Berry holonomy forced by topology.
- **R3.** Character decomposition (KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md A.2):
  dim ratio `(2 DOF of b) / dim_ℝ Herm_3 = 2/9` (dimensionless).
- **R4.** Selected-line boundary points: `m_0 = -0.2658` (δ=0, unphased),
  `m_pos = -1.2958` (δ=π/12, positivity threshold), `m_* = -1.1604` (δ=2/9, physical).

---

## 2. Four retained closure candidates — all fail

### 2.1 Candidate A: PB phase per Z_3 element on qubit equator

With `χ(θ) = (1, e^{-2iθ})/√2` and Z_3 shift `θ ↦ θ + 2π/3`:
`γ_PB(g) = arg⟨χ(θ)|χ(θ+2π/3)⟩`. Using `(1 + e^{-2ix})/2 = cos(x) e^{-ix}` with
`x = 2π/d`: at d=3, `cos(2π/3) = -1/2 < 0`, so `γ_PB(g) = -2π/3 + π = π/3 ≈ 1.047`
rad, **independent of base point** (Bargmann invariant of three equidistant
equator points). At general d it is a rational multiple of π:

| d  | γ_PB(g)     | 2/d²   |
|----|-------------|--------|
| 3  | π/3         | 0.2222 |
| 5  | -2π/5       | 0.0800 |
| 7  | -2π/7       | 0.0408 |
| 11 | -2π/11      | 0.0165 |

**Fail:** `γ_PB(g_d)` is a rational multiple of π at every d; `2/d²` is a pure
rational. They disagree at every d checked (the failure is structural, not a
d=3 coincidence).

### 2.2 Candidate B: Closed-orbit Bargmann phase

Closed 3-step PB product around the Z_3 orbit on the equator is `arg(∏) = π`
(half 2π solid angle of great-circle equator triangle). Rational-coefficient
rescalings (π/d², π/d, π/9) never equal 2/9. **Fail.**

### 2.3 Candidate C: Plancherel-weight identification

The dim ratio `2/d²` on Herm_d is a dimensionless Plancherel count with no
canonical map to radians on Cl(3)/Z_3. Restating P as "Plancherel weight 2/d²
equals radian δ" is a reformulation of P, not a derivation. **Fail (tautology).**

### 2.4 Candidate D: Interior-point structural selector on H_sel

On the physical first branch δ sweeps (0, π/12) from m_0 to m_pos. We searched
for retained conditions pinning m_* in the interior:

1. Pancharatnam midpoint gives δ = π/24 ≠ 2/9.
2. Equal-overlap selector: same midpoint.
3. Selected-slice eigenline geometric phases (R1 §6): `γ_lower(m_0 → m_*) ≈ 0.178`,
   `γ_upper(m_0 → m_*) ≈ 0.276`; equation `γ_lower = δ(m)` selects m ≈ -0.877, not m_*.
4. Fractional position `δ_*/δ_pos = 2/9 ÷ π/12 = 8/(3π)` is not a retained rational
   (π is not Cl(3)-native).

**Fail:** no retained structural condition on Cl(3)/Z_3 + selected-line geometry
pins θ(m_*) = 2π/3 + 2/9 as an interior point.

---

## 3. The precise obstruction

All four candidates fail by one underlying reason: **retained Cl(3)/Z_3
character data has no canonical unit of angle**.

- Retained character-algebra data produces dimensionless pure rationals (dim
  counts, Plancherel weights) and rational multiples of π (angles from
  `e^{i·2π/d}`, solid-angle integrals, boundary angles).
- `δ = 2/9` is a pure rational measured in radians — neither a rational
  multiple of π, nor a dimensionless ratio.

> **Obstruction.** Every retained radian on Cl(3)/Z_3 + d=3 is of the form
> `(rational) × π`. Every retained dimensionless ratio is a pure rational.
> `δ = 2/d² = 2/9` in radians requires a bridge mapping a pure rational to
> a radian without a π factor. No such bridge is retained.

---

## 4. Minimal additional structural inputs

Any one of the following would close P. None is currently retained.

**Input (a): Lattice propagator radian quantum.** A retained Euclidean lattice
propagator identity `G_{C_3}(1) = exp(i · 2/d²) · G_0` on a specific
C_3-equivariant lattice, where `2/d²` appears literally as a radian phase.
Candidate routes (KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md) have
not produced this.

**Input (b): 4×4 hw=1+baryon non-uniform Wilson holonomy.** Extending hw=1 from
the retained 3×3 triplet to a 4×4 sector with baryon coupling, where the
C_3 Wilson-line phase on the baryon-projected line equals `2/d²` rad. The 4×4
extension is an open frontier (SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md).

**Input (c): Z_3-orbit Wilson-line d²-power quantization.** A retained
quantization `W_{Z_3}^{d²} = exp(2i) · 𝟙`, giving per-element phase `2/d²`
rad. The retained Z_3 group-theoretic quantization gives `W_{Z_3}^3 = 𝟙`
(rational multiples of π only) — not this.

All three preserve the physical base topology (no ambient-S² enlargement, no
Chern class, no monopole charge) so they respect the bundle-obstruction
theorem R2. P remains a clean single-real-number postulate; this no-go
sharpens its status from "unproved" to "proved to require a named extra input."

---

## 5. Impact on the Koide program

- The linking theorem `δ = Q/d`
  (KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md) stays conditional:
  under P, closing `Q = 2/d` or `δ = 2/d²` closes the other; without P, both open.
- The selected-slice Berry eigenline no-go (R1 §6) is reconfirmed.
- The angle-1 (PB per Z_3 element) and angle-2 (Plancherel weight) routes
  suggested in the task are both refuted as closures.

**Remaining Open Imports register entry (suggested):**

> Radian-bridge P for `δ = 2/d²`. No-go against four retained Cl(3)/Z_3
> closure candidates. Minimal inputs to close: (a) lattice propagator radian
> quantum; (b) 4×4 hw=1+baryon Wilson holonomy; (c) Z_3-orbit Wilson-line
> d²-power quantization. None currently retained. See this note.

**Strict-reviewer disclosure:** on the retained Cl(3)/Z_3 surface plus the
selected-line CP¹ Berry identification, exactly one structural postulate
remains — P. This no-go proves P is not a natural closure of existing
retained structure; it is a genuinely new structural input whose minimal
form is (a), (b), or (c).

---

## 6. Runner PASS list (23/23)

- F1a–c: per-Z_3 PB phase magnitude and base-point independence (Bargmann invariant).
- F2a–c: general-d structure — rational multiple of π at every d, never `2/d²`.
- F3a–b: closed-orbit Bargmann = π, no rescaling gives 2/9.
- F4a–b: Pancharatnam midpoint gives π/24 (midpoint verified).
- F5a–b: fractional position `8/(3π)` is not a retained rational.
- F6a–c: every retained radian is `(rational) × π`; 2/9 is not.
- F7a–b: Plancherel weight `2/d²` is dimensionless; no retained angle equals 1 rad.
- F8a–b: R1 §6 eigenline selector no-go reconfirmed.
- F9a–d: all four candidates fail (A by π/3, B by π, C as tautology, D by π/24).

---

## 7. Cross-references

- KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md (P named)
- KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md (R1)
- KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md (R2)
- KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md (R3, A.2)
- KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md (candidate input (a))
- KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md (candidate input (c))
- SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md (stack context)
