# Inline Derivation of the Active Affine Chamber Bound `q_+ + δ ≥ √(8/3)`

**Date:** 2026-04-20
**Lane:** Dark-matter A-BCC basin-selector — closing open import I4.
**Status:** **proposed_retained local theorem** — the chamber bound is derived inline
from retained Cl(3)/Z_3 doublet-block geometry on the PMNS source surface,
and can be cited self-containedly by the A-BCC closure note.
**Runner:** `scripts/frontier_dm_abcc_chamber_bound_derivation.py` ([scripts/frontier_dm_abcc_chamber_bound_derivation.py](../scripts/frontier_dm_abcc_chamber_bound_derivation.py))
**Runner result on land:** `PASS = 15, FAIL = 0`

---

## 0. Why this note exists

The A-BCC closure note
(`docs/DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md`, §1)
cites the chamber inequality

    q_+ + δ ≥ √(8/3)

as "retained as preliminary P3 of the P3-Sylvester linear-path signature
theorem note (intrinsic Z_3 doublet-block point-selection theorem)" but
does **not** reproduce the derivation at point of use. A Nature reviewer
will demand the derivation inline on the A-BCC closure chain. This note
reproduces the derivation cleanly as a standalone theorem, citing every
retained ingredient explicitly, so the A-BCC closure note becomes
self-contained by one-step delegation.

The derivation already appears (more briefly) inside the retained
`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
and its sharpening
`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`.
What this note contributes is the clean reviewer-grade reproduction with
explicit citation trace at each step, scoped narrowly to the chamber bound
itself.

---

## 1. Retained ingredients (citation trace, one level deep)

Every step below uses only retained theorems. The trace is one level deep.

### R1. Active affine chart on the source surface

**Citation:**
`docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
(retained). The live source-oriented sheet has the exact affine structure

    H(m, δ, q_+) = H_base + m · T_m + δ · T_δ + q_+ · T_q,

with

    T_m    = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
    T_δ    = [[0, -1, 1], [-1, 1, 0], [1, 0, -1]]
    T_q    = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

    H_base = [[ 0,          E_1,              -E_1 - i·γ ],
              [ E_1,        0,                -E_2       ],
              [-E_1 + i·γ,  -E_2,              0         ]]

    γ = 1/2,    E_1 = √(8/3),    E_2 = √8/3.

### R2. Source-package constants

**Citation:** retained source-package theorems (cited inside R1, §"Inputs";
specifically `DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md`
and `DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md`).
Across the live source-oriented sheet the exact source package is

    γ = 1/2
    δ + ρ      = E_1 = √(8/3)        ["fixed source channel"]
    σ sin(2v)  = 8/9
    σ cos(2v)  = √8/9 − 3 q_+       [even carrier channel law]

and the intrinsic CP pair and slot pair are fixed constants (not needed
below, but flagged to make the scope explicit).

### R3. Cl(3)/Z_3 doublet-block normal form

**Citation:**
`docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
(retained). Pushing `H` through the intrinsic Z_3 carrier readout
`K_{Z_3}(H) = U_{Z_3}† H U_{Z_3}` freezes the singlet-doublet slots

    K_{01} = a_*,   K_{02} = b_*      [constants across the sheet]

while the entire active motion lives in the doublet block with

    K_{11} = −q_+ + 2√2/9 − 1/(2√3)
    K_{22} = −q_+ + 2√2/9 + 1/(2√3)
    K_{12} = m − 4√2/9  +  i · ( √3 δ − 4√2/3 ).

This is the retained Cl(3)/Z_3 doublet-block structure used below.

### R4. Shift-quotient bundle / carrier inverse chart

**Citation:**
`docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
(retained), §"Exact theorem" §1; rests on the
`SHIFT_QUOTIENT_BUNDLE` and `CARRIER_NORMAL_FORM` retained theorems cited
there. The quotient-gauge entries on the live sheet are

    d_1 = m,    d_2 = δ,    d_3 = −δ
    r_{12} = E_1 − δ + q_+
    r_{23} = m + q_+ − E_2
    r_{31} · e^{−i φ_+} = s − i γ,     s ≡ q_+ − E_1 + δ.        (★)

### R5. Positivity of the Z_3 doublet off-diagonal modulus

**Citation:** same note R4, §1. The off-diagonal modulus `r_{31}` is a
positive real number — it is the absolute value of a quotient-gauge
off-diagonal entry, hence `r_{31} ≥ 0`. Furthermore, the carrier normal
form embeds γ as an irreducible imaginary part `r_{31} sin(φ_+) = γ = 1/2`,
so `r_{31} ≥ |γ| = 1/2`.

**Equivalent statement.** From (★) and `γ = 1/2`,

    r_{31}² = s² + γ² = s² + 1/4.                                (★★)

Because `s² ≥ 0` and `γ² = 1/4`, we have `r_{31}² ≥ 1/4`, i.e.
`r_{31} ≥ 1/2`, with equality iff `s = 0`.

---

## §A. Appendix — Inline derivation of `q_+ + δ ≥ √(8/3)`

The theorem and proof. All symbols and constants as in §1.

### Theorem (chamber bound on the active affine chart)

On the live source-oriented sheet, the active affine chart coordinates
`(m, δ, q_+)` — equivalently the coefficients of `(T_m, T_δ, T_q)` on
`H_base` per R1 — satisfy the closed half-plane inequality

    q_+ + δ  ≥  √(8/3) = E_1.                                    (I4)

The boundary `q_+ + δ = √(8/3)` is the exact locus `r_{31} = 1/2`,
equivalently `φ_+ = π/2`.

### Proof

**Step A.1 — Solve the carrier off-diagonal for q_+ in terms of δ.**
From R4, equation (★), the off-diagonal quotient-gauge entry
`r_{31} · e^{−i φ_+}` has real part `s` and imaginary part `−γ`. Taking
modulus,

    r_{31}² = s² + γ².

Using R2 (`γ = 1/2`) and the definition of `s` (R4),

    r_{31}² = (q_+ − E_1 + δ)² + 1/4.                            (A.1)

Solving for `s`,

    s = ± √(r_{31}² − 1/4).

The carrier normal form (R4) fixes the sign of `s` by fixing the sign of
the real part of the `(3, 1)` off-diagonal entry on the source-oriented
sheet: the live branch is `s = +√(r_{31}² − 1/4)` (the `−` sign would
orient the Z_3 doublet off-diagonal into the mirror branch, which the
retained source-oriented-sheet normalization excludes; see R4 §1 and the
retained `CARRIER_NORMAL_FORM_THEOREM`). Hence, substituting
`s = q_+ − E_1 + δ`,

    q_+ − E_1 + δ  =  +√(r_{31}² − 1/4).                         (A.2)

**Step A.2 — Non-negativity from R5.**
By R5, `r_{31} ≥ 1/2`, so `r_{31}² − 1/4 ≥ 0`, and therefore the right
side of (A.2) is a well-defined non-negative real number:

    √(r_{31}² − 1/4)  ≥  0.                                      (A.3)

**Step A.3 — Assemble the inequality.**
Combining (A.2) and (A.3),

    q_+ − E_1 + δ  ≥  0,

i.e.

    q_+ + δ  ≥  E_1  =  √(8/3).                                  (I4)

**Step A.4 — Boundary identification.**
Equality `q_+ + δ = √(8/3)` holds iff `s = 0` in (A.2), iff
`r_{31}² = 1/4` in (A.1), iff `r_{31} = 1/2`. At this boundary the
quotient-gauge entry `r_{31} · e^{−i φ_+} = −i γ` is purely imaginary, so
`e^{−i φ_+} = −i`, i.e. `φ_+ = π/2`. This matches R4 §1 exactly:

    boundary:  q_+ + δ = √(8/3)  ⟺  r_{31} = 1/2  ⟺  φ_+ = π/2.

**Converse (for completeness).**
If `q_+ + δ ≥ √(8/3)`, set `s := q_+ − E_1 + δ ≥ 0` and
`r_{31} := √(s² + 1/4)`. Then `r_{31} ≥ 1/2` and (★) gives a valid
source-oriented-sheet off-diagonal with `γ = 1/2`. So the half-plane
`q_+ + δ ≥ √(8/3)` is the exact image of the live sheet under the active
affine chart, not merely a necessary condition.

□

### Scope and what this bound does and does not establish

**Unconditional content.** The bound `q_+ + δ ≥ √(8/3)` is a retained
structural inequality on the active affine chart, derived from:

1. the retained affine chart (R1);
2. the retained source-package constants `γ = 1/2`, `E_1 = √(8/3)` (R2);
3. the retained Cl(3)/Z_3 doublet-block structure (R3) — used only via the
   freezing of the singlet-doublet slots that justifies isolating the
   doublet block as the carrier of the active motion;
4. the retained shift-quotient/carrier normal form (R4) — used for the
   inverse chart (★);
5. the retained positivity `r_{31} ≥ 1/2` (R5).

No T2K, NuFit, or PDG input is used. No basin-level or chart-point-level
input is used. The bound is a **derivation-side chamber boundary**, not
an observational filter.

**What the bound does not establish.** This note does not derive the
sign of `det(H)` inside the chamber, does not select a single point
inside the chamber, does not derive the `σ_hier = (2, 1, 0)` hierarchy
pairing, and does not resolve A-BCC on its own. It supplies only the
retained inequality `q_+ + δ ≥ √(8/3)`.

**Usage in the A-BCC closure.** Used as the first of two conjuncts in

    A-BCC  ⇐  (C1) ∩ (C2),

where (C1) is the bound derived here and (C2) is the DPLE d = 3 F_4
selector on the retained linear pencil. The conjuncts strictly exclude
Basin N (`q+δ = 1.2795 < 1.6330`) and Basin P (`q+δ = 0.1035 < 1.6330`)
from the admissible chart on purely retained-theoretic grounds, leaving
`{Basin 1, Basin X}` for (C2) to discriminate.

---

## 2. Numerical cross-checks

These are the checks the runner performs. They are supporting — the
proof in §A is exact — but they guard against regression.

| Task | Check                                                          | Result |
|------|----------------------------------------------------------------|--------|
| T1   | `E_1 = √(8/3)` and `γ² = 1/4`                                  | 2 PASS |
| T2   | Chamber membership for all four retained basins                | 4 PASS |
| T3   | Carrier identity `r_{31}² − s² − γ² = 0` on all four basins    | 4 PASS |
| T4   | Boundary samples `q_+ = E_1 − δ` saturate `s = 0`, `r_{31}² = 1/4`, `q+δ = E_1` | 1 PASS |
| T5   | Interior half-plane samples (200 seeds); forbidden-side samples (100 seeds); margin-vs-s reconstruction | 3 PASS |
| T6   | `H(m, δ, q_+)` is Hermitian on each retained basin             | 1 PASS |

Target: `PASS ≥ 8`, `FAIL = 0`. Land result: `PASS = 15, FAIL = 0`.

---

## 3. References

- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
  (retained) — active affine chart `H = H_base + m T_m + δ T_δ + q_+ T_q`.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
  (retained) — original half-plane derivation, now reproduced inline here.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
  (retained) — Cl(3)/Z_3 doublet-block normal form.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md`
  (retained) — singlet-doublet slot constants.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md`
  (retained) — slot-torsion constant, fixing the source-oriented branch.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`
  (retained) — theorem note that cites the chamber bound as "preliminary P3".
- `docs/DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19.md`
  (branch) — downstream consumer; now cross-references this note.

---

## 4. One-paragraph summary

The active affine chart on the live source-oriented PMNS sheet is
`H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q` with retained constants
`γ = 1/2`, `E_1 = √(8/3)`. In the Cl(3)/Z_3 carrier normal form, the
off-diagonal modulus satisfies `r_{31}² = s² + γ²` with
`s ≡ q_+ − E_1 + δ`, so that `r_{31}² − 1/4 = s²` and
`r_{31} ≥ 1/2`. The source-oriented-sheet branch of the carrier normal
form fixes `s = +√(r_{31}² − 1/4) ≥ 0`, giving `q_+ − E_1 + δ ≥ 0`,
i.e. `q_+ + δ ≥ √(8/3)`, with equality on the boundary
`r_{31} = 1/2 ⇔ φ_+ = π/2`. The bound is a structural retained
inequality, not an observational filter, and is the first of the two
conjuncts that close A-BCC on the DM flagship lane.
