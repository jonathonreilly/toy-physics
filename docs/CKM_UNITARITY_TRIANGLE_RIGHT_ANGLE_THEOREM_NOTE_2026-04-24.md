# CKM Unitarity Triangle Right-Angle Theorem (α = 90°)

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Direct geometric corollary of the retained `ρ = 1/6, η = √5/6` from [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md): the unitarity-triangle angle `α` is **exactly 90°** on the retained CKM atlas. This follows from the elementary trigonometric identity `arctan(x) + arctan(1/x) = 90°` for `x > 0`. The result is striking and falsifiable but is not currently named on `main`.
**Primary runner:** `scripts/frontier_ckm_unitarity_triangle_right_angle.py`

---

## 0. Statement

**Theorem (CKM unitarity triangle right angle).** On the retained CKM atlas surface ([`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)) with retained Wolfenstein `(ρ̄, η̄) = (1/6, √5/6)` from [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md), the three unitarity-triangle angles are exactly:

```text
(T1)   α  =  90°  EXACTLY                                          (right angle)
(T2)   β  =  arctan(1/√5)  ≈  24.0948°
(T3)   γ  =  arctan(√5)    ≈  65.9052°
       α + β + γ  =  180°                                          (trivially by unitarity)
```

The α = 90° identity follows from the elementary trigonometric fact

```text
(I)   arctan(x) + arctan(1/x)  =  π/2  =  90°,    for x > 0,
```

applied at `x = √5`: `β + γ = arctan(1/√5) + arctan(√5) = 90°`, hence `α = 180° − 90° = 90°`.

In the rescaled `(ρ̄, η̄)` coordinate plane, the unitarity triangle has vertices `(0, 0)`, `(1, 0)`, `(1/6, √5/6)` with **rescaled area**

```text
(T5)   Area_{rescaled}  =  η̄ / 2  =  √5 / 12  EXACTLY.
```

These are **pure structural identities** independent of any coupling. They are direct consequences of the retained `1 + 5` Schur decomposition of the quark-block projector that gives `(ρ̄, η̄) = (1/6, √5/6)`.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| CKM atlas / Wolfenstein parameterisation | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| Retained `ρ̄ = 1/6, η̄ = √5/6` from CP-phase identity | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Retained Wolfenstein `λ² = α_s(v)/2`, `A² = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| Standard CKM unitarity-triangle definitions | textbook (Branco, Lavoura, Silva 1999; PDG) |

## 2. Background: unitarity triangle angles

The CKM unitarity triangle in the rescaled `(ρ̄, η̄)` plane has vertices at:

- `A` = `(0, 0)`
- `B` = `(1, 0)`
- `C` = `(ρ̄, η̄)`

The three interior angles `α, β, γ` (also called `φ_2, φ_1, φ_3`) are defined by:

- `β` (`= φ_1`): angle at vertex `B = (1, 0)` between sides `B→A` and `B→C`
- `γ` (`= φ_3`): angle at vertex `A = (0, 0)` between sides `A→B` and `A→C`
- `α` (`= φ_2`): angle at vertex `C = (ρ̄, η̄)` between sides `C→A` and `C→B`

In the rescaled plane:

```text
β  =  arctan(η̄ / (1 − ρ̄))     (geometry at B)
γ  =  arctan(η̄ / ρ̄)            (geometry at A, when ρ̄ > 0)
α  =  π − β − γ                  (sum of interior angles = π)
```

These are all defined modulo CKM unitarity which is exact (Wolfenstein expansion at any order).

## 3. Derivation

### 3.1 (T2) β = arctan(1/√5)

Substituting retained `ρ̄ = 1/6, η̄ = √5/6`:

```text
β  =  arctan(η̄ / (1 − ρ̄))
   =  arctan((√5/6) / (1 − 1/6))
   =  arctan((√5/6) / (5/6))
   =  arctan(√5 / 5)
   =  arctan(1/√5).                                                  (T2)
```

Numerically `β = arctan(1/√5) = arctan(0.4472…) = 24.0948°`.

### 3.2 (T3) γ = arctan(√5)

```text
γ  =  arctan(η̄ / ρ̄)
   =  arctan((√5/6) / (1/6))
   =  arctan(√5).                                                    (T3)
```

Numerically `γ = arctan(√5) = arctan(2.2361…) = 65.9052°`.

This is exactly the retained `δ_CKM` from [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md). The Wolfenstein angle `γ` and the CP-phase `δ` coincide in this convention (both satisfy `tan = √5`).

### 3.3 (T1) α = 90° EXACTLY via trigonometric identity

The elementary trig identity

```text
(I)   arctan(x) + arctan(1/x)  =  π/2  for all x > 0
```

applied at `x = √5` gives

```text
arctan(√5) + arctan(1/√5)  =  π/2  =  90°.                          (I')
```

Combining (T2) and (T3):

```text
β + γ  =  arctan(1/√5) + arctan(√5)  =  90°.
```

Therefore by `α + β + γ = 180°` (unitarity-triangle interior angle sum):

```text
α  =  180° − (β + γ)  =  180° − 90°  =  90°.                        (T1)
```

The unitarity triangle is a **right triangle with the right angle at vertex C = (1/6, √5/6)**. ∎

### 3.4 Verification of (I) at x = √5

Direct algebraic verification of `arctan(x) + arctan(1/x) = π/2`:

```text
tan(arctan(x) + arctan(1/x))  =  (x + 1/x) / (1 − x · (1/x))
                                =  (x + 1/x) / (1 − 1)
                                =  (x + 1/x) / 0  =  ∞.
```

`tan(α) = ∞` ⟹ `α = π/2` (for x > 0, both arctans are in [0, π/2], so sum is in [0, π]). ∎

### 3.5 (T5) Rescaled triangle area

The rescaled triangle has vertices `(0, 0)`, `(1, 0)`, `(1/6, √5/6)`. The signed area via the shoelace formula:

```text
Area  =  (1/2) |x_B (y_C − y_A) + x_C (y_A − y_B) + x_A (y_B − y_C)|
      =  (1/2) |1 × (√5/6 − 0) + (1/6) × (0 − 0) + 0 × (0 − √5/6)|
      =  (1/2) × √5/6
      =  √5 / 12.                                                    (T5)
```

The unitarity triangle has rescaled area exactly `√5/12 ≈ 0.1863`.

This connects to the Jarlskog invariant via `J = 2 × A² λ⁶ × Area_{rescaled}`, with retained Wolfenstein:

```text
J  =  2 × (2/3) × (α_s(v)/2)³ × (√5/12)
   =  α_s(v)³ × √5 / 72.
```

(Matches the Jarlskog factorisation from my CP-phase theorem.)

## 4. Numerical verification

| Quantity | Symbolic | Numerical |
|----------|----------|-----------|
| `ρ̄` | 1/6 | 0.16667 |
| `η̄` | √5/6 | 0.37268 |
| `β` | `arctan(1/√5)` | 24.0948° |
| `γ` | `arctan(√5)` | 65.9052° |
| `α` | 180° − β − γ | **90.0000°** |
| `β + γ` | 90° (exactly) | **90.0000°** |
| `tan(β + γ)` | ∞ (exactly) | ~10¹⁵ (limit of double precision) |
| Rescaled area | √5/12 | 0.1863 |

## 5. Comparison with PDG 2024 global fit

Observational values (PDG 2024 / CKMfitter):

| Angle | Framework | PDG 2024 | Deviation |
|-------|-----------|----------|-----------|
| α | **90.000°** | (84.1 ± 4.0)° | +5.9° (~1.5σ above) |
| β | 24.095° | (22.2 ± 0.7)° | +1.9° (~2.7σ above) |
| γ | 65.905° | (66.2 ± 3.4)° | −0.3° (within 1σ) |

Framework prediction:
- `γ = 65.9°`: matches PDG within 1σ — strongest agreement.
- `β = 24.1°`: ~2.7σ above PDG `22.2°`.
- `α = 90.0°`: ~1.5σ above PDG `84.1°`.

The framework prediction `α = 90°` is at the edge of (but consistent with) the current PDG 2σ envelope. Tightening `α` measurements at LHCb / Belle II will sharpen the test.

## 6. Structural observations

### 6.1 The right angle is geometric, not coincidental

The `α = 90°` identity is **structurally forced** by the retained `(ρ̄, η̄) = (1/6, √5/6)` — it is not a numerical coincidence. The point `(ρ̄, η̄)` lies on the geometric locus where `arctan(η̄/(1−ρ̄)) + arctan(η̄/ρ̄) = 90°`, equivalently:

```text
η̄ / (1 − ρ̄)  =  ρ̄ / η̄        ⟺      η̄²  =  ρ̄ (1 − ρ̄).
```

Substituting `ρ̄ = 1/6`: `ρ̄(1 − ρ̄) = (1/6)(5/6) = 5/36 = η̄²`. ✓

So the right-angle locus is **the circle of vertices satisfying `η̄² = ρ̄(1 − ρ̄)`** — in the rescaled plane, the diameter of this circle is the segment `[0, 1]`. The retained vertex `(1/6, √5/6)` lies on this circle, automatically giving `α = 90°` (by the inscribed-angle theorem: any triangle inscribed in a circle with one side as diameter has a right angle opposite the diameter).

### 6.2 Geometric interpretation: triangle inscribed in a semicircle

The retained `(ρ̄, η̄)` vertex is on the upper semicircle of diameter `[0, 1]` in the (ρ̄, η̄) plane (the "Thales circle"). By Thales' theorem, the angle at the vertex on the circle is exactly 90°.

This is the elementary geometric reason for the structural identity — and a striking visual consequence of the `1 + 5` Schur decomposition.

### 6.3 Right-angle constraint as a 1-parameter family

The constraint `η̄² = ρ̄(1 − ρ̄)` defines a 1-parameter family of CP-violating points all with `α = 90°`. The retained `(1/6, √5/6)` is one specific point in this family. Other points (e.g. `(1/2, 1/2)`) would also give `α = 90°` but different `(β, γ)` values.

## 7. Falsifiability

Sharp:

- A confirmed `α_CKM` significantly different from 90° (say `α < 80°` or `α > 100°` at >5σ) would falsify the retained `(ρ̄, η̄) = (1/6, √5/6)`.
- LHCb / Belle II projected precision on `α` to ~1° by 2030 will sharpen the test.

Current status: PDG 2024 `α = 84.1° ± 4.0°` is consistent with framework prediction `90°` at ~1.5σ. Future precision will be definitive.

The angles `β`, `γ` are also retained predictions; combined `(α, β, γ)` measurements provide three independent tests. Currently:
- γ is in best agreement (within 1σ)
- β is ~2.7σ above PDG (slight tension)
- α is ~1.5σ above PDG

## 8. Scope and boundary

**Claims:**

- (T1) `α = 90°` exactly on retained CKM atlas + `(ρ̄, η̄) = (1/6, √5/6)`.
- (T2) `β = arctan(1/√5) ≈ 24.095°`.
- (T3) `γ = arctan(√5) ≈ 65.905°` (= δ_CKM).
- (T5) Rescaled triangle area `= √5/12` exactly.
- The retained `(ρ̄, η̄)` point lies on the Thales circle (diameter `[0,1]`).

**Does NOT claim:**

- `(ρ̄, η̄) = (1/6, √5/6)` itself; this is the retained CP-phase theorem's input.
- The Schur `1 + 5` decomposition; that's the parent CKM atlas theorem.
- Higher-precision Wolfenstein corrections (the `(ρ̄, η̄)` are leading-order).
- BSM CKM extensions or 4-generation effects.

## 9. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_ckm_unitarity_triangle_right_angle.py
```

Expected: all checks pass.

The runner:

1. Computes `β`, `γ` from retained `(ρ̄, η̄)` numerically.
2. Verifies `β + γ = 90°` to machine precision via `arctan(1/√5) + arctan(√5)`.
3. Confirms `α = 180° − β − γ = 90°` exactly.
4. Symbolic (sympy) verification of trigonometric identity `arctan(x) + arctan(1/x) = π/2`.
5. Computes rescaled triangle area = √5/12 exactly via shoelace formula.
6. Verifies the Thales-circle locus: `η̄² = ρ̄(1 − ρ̄)` at retained `(ρ̄, η̄)`.
7. Compares to PDG 2024 angles (within stated uncertainties).

## 10. Cross-references

- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) — retained `(ρ̄, η̄) = (1/6, √5/6)`
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) — retained `λ²`, `A²`
- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) — parent retained CKM theorem
- Branco, Lavoura & Silva 1999 *CP Violation* — standard unitarity-triangle reference
- Wolfenstein 1983, PRL 51, 1945 — Wolfenstein parameterisation
