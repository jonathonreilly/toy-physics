# Lepton Block Scalar-Singlet Composite Uniqueness (D17-prime)

**Date:** 2026-05-10

**Status:** proposed_retained narrow positive theorem on the lepton (2,1)
block. Establishes the analog of the YT-lane's D17 (scalar-singlet
composite uniqueness on the Q_L = (2,3) block) for the L_L = (2,1)
lepton-doublet block. The theorem proves that, on the framework's
Yukawa-shaped trilinear `L̄_L × H × e_R`, the unique unit-normalized
isospin-singlet × Lorentz-scalar × hypercharge-conserving composite
operator is

```text
H_unit^lep = (1/√2) Σ_α=1,2 L̄_L^α H_α e_R       (lepton-D17)
```

with normalization `Z² = N_c × N_iso = 1 × 2 = 2`. All other admissible
composite reps either give different `Z²` values or do not form a valid
Yukawa-shaped trilinear under the SM matter content (no triplet of `e_R`,
no color sector to contract).

**Primary runner:** `scripts/frontier_lepton_block_scalar_singlet_composite_uniqueness.py`

**Lane:** 6 — Charged-lepton mass retention (M5-a partial unblock)

---

## 1. Theorem statement

**Theorem (D17-prime: lepton-block scalar-singlet composite uniqueness).**

On the L_L = (2,1) lepton-doublet block of the framework's
Yukawa-shaped trilinear

```text
   L̄_L^α  ⊗  H_α  ⊗  e_R                                          (1.1)
```

where:

- `L_L = (ν_L, e_L)^T` — SU(2) doublet, color singlet, hypercharge `Y = -1/2`
- `H = (H⁺, H⁰)^T` — SU(2) doublet, color singlet, hypercharge `Y = +1/2`
- `e_R` — SU(2) singlet, color singlet, hypercharge `Y = -1`
- `α = 1, 2` is the SU(2) doublet index

the unique unit-normalized isospin-singlet × Lorentz-scalar ×
hypercharge-conserving composite operator is

```text
   H_unit^lep := (1/√2) Σ_α=1,2 L̄_L^α H_α e_R                     (1.2)
```

with normalization

```text
   Z²_lep := N_c × N_iso = 1 × 2 = 2                                 (1.3)
```

so that `H_unit^lep` is unit-normalized in the sense
`<H_unit^lep | H_unit^lep>_iso-color = 1`.

## 2. Setup and conventions

### 2.1 Block representation labels

For a doublet × doublet × singlet trilinear, the relevant labels are:

- **Color:** SU(N_c) representation — for the lepton block, both `L_L`
  and `e_R` are color singlets, so `N_c = 1` (only the trivial rep
  exists).
- **Isospin:** SU(2)_L representation — `L_L` and `H` are doublets,
  `e_R` is a singlet. Doublet × doublet decomposes as 1 ⊕ 3.
- **Lorentz:** Dirac scalar (γ_5²-even) or pseudoscalar (γ_5-odd).
- **Hypercharge:** the gauge-allowed Yukawa monomial is `bar L_L H e_R`
  (using H, NOT H̃). In the doubled-hypercharge convention from
  `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`:

```text
   L_L : Y = -1   (doubled, std -1/2)
   e_R : Y = -2   (doubled, std -1)
   H   : Y = +1   (doubled, std +1/2)
   H̃   : Y = -1   (doubled; H̃ = i σ² H*)
```

The selected monomials are:

```text
   bar L_L H e_R:   sum = -Y(L_L) + Y(H)  + Y(e_R) = +1 + 1 + (-2) =  0  ✓ ALLOWED
   bar L_L H̃ e_R:  sum = -Y(L_L) + Y(H̃) + Y(e_R) = +1 + (-1) + (-2) = -2  ✗ REJECTED
```

The H-coupled trilinear is the standard charged-lepton Yukawa. The
H̃-coupled monomial would be the up-quark-style coupling and is rejected
on the lepton block by hypercharge. See
`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md` §2 for
the parallel derivation.

### 2.2 Block dimension

The Yukawa trilinear sums over the SU(2) doublet indices α = 1, 2:

```text
   Σ_α L̄_L^α H_α e_R                                                (2.2.1)
```

The number of SU(2) doublet DOFs being summed is **N_iso = 2**.

The number of color DOFs is **N_c = 1** (color singlet block).

Hence the total block dimension is

```text
   DIM_(L_L) = N_c × N_iso = 1 × 2 = 2                              (2.2.2)
```

### 2.3 Unit normalization of the composite

For a Yukawa-shaped trilinear `Σ_a O^a` with `a` running over `Z²_lep`
identical fundamental DOFs, the unit-normalized composite is

```text
   H_unit := (1/√Z²) Σ_a O^a                                        (2.3.1)
```

so that the inner product

```text
   <H_unit | H_unit> = (1/Z²) Σ_{a,b} <O^a | O^b> = (1/Z²) × Z² = 1  (2.3.2)
```

(using diagonality of the orthonormal basis on the fundamental DOFs).

This is the same convention as YT-lane's D17 on Q_L:

```text
   H_unit^Q_L = (1/√6) Σ_{i,α=1..3, β=1..2} Q̄_L^{i,α} H_β q_R^{i}  (2.3.3)
```

with `Z²_Q_L = N_c × N_iso = 3 × 2 = 6`.

The lepton block specializes `N_c = 1`:

```text
   H_unit^lep = (1/√2) Σ_α=1,2 L̄_L^α H_α e_R                       (2.3.4)
```

with `Z²_lep = 1 × 2 = 2`.

## 3. Uniqueness argument

A scalar-singlet × hypercharge-conserving composite on the L_L × H × e_R
trilinear is determined by:

1. **Color rep:** uniquely (1, 1, 1) since `L_L`, `H`, `e_R` are all color
   singlets. No alternative color contractions exist.

2. **Isospin rep:** the product 2 ⊗ 2 ⊗ 1 of SU(2) decomposes as
   `(1 ⊕ 3) ⊗ 1 = 1 ⊕ 3`. The two candidate isospin contractions are:

   - **Singlet (1):** the SU(2) singlet contraction
     `Σ_α L̄_L^α H_α e_R` (using L̄_L in the 2̄ ≅ 2 of SU(2),
     contracted with H in the 2 via the natural pairing).
     This is the standard charged-lepton Yukawa contraction and is the
     (1.2) composite.
   - **Triplet (3):** the symmetric combination
     `(σ^a)^β_α L̄_L^α H_β e_R^a` for a = 1, 2, 3.

   The triplet contraction REQUIRES three components `e_R^a` (a Lorentz
   scalar transforming as a 3 of SU(2)_L). The SM matter content has
   only one `e_R` per generation (a single SU(2) singlet field), so the
   triplet contraction is **not realized** under the framework's
   anomaly-forced + hw=1 matter content.

3. **Lorentz rep:** Dirac scalar (γ_5²-even, parity-conserving) or
   pseudoscalar (γ_5-odd, parity-violating). The Yukawa coupling is
   conventionally taken as the scalar form; the pseudoscalar form is
   CP-violating and corresponds to a different (and not currently
   retained) framework branch.

4. **Hypercharge:** uniquely fixed by the gauge selection
   (the `bar L_L H e_R` form is allowed (sum = 0); `bar L_L H̃ e_R`
   is rejected (sum = -2)).

Therefore, on the L_L × H × e_R trilinear with the framework's matter
content and the parity-conserving Yukawa convention, **the unique
isospin-singlet × Lorentz-scalar composite is `H_unit^lep` of (1.2)**,
with `Z²_lep = 2`.

## 4. Comparison to YT D17 (Q_L = (2,3) block)

| | Q_L block (D17) | L_L block (D17-prime, this note) |
|---|---|---|
| Color N_c | 3 | 1 |
| Isospin N_iso | 2 | 2 |
| Z² | 6 | 2 |
| Composite | `(1/√6) Σ Q̄_L^{i,α} H_α q_R^i` | `(1/√2) Σ L̄_L^α H_α e_R` |
| Color octet alternative | (1, 8) Z² = 8 | not realized (no color) |
| Color triplet alternative | (3, 1) Z² = 9/2 | not realized (no color) |
| Color octet × isospin triplet | (8, 3) Z² = 24 | not realized (no color) |
| SU(2) iso triplet | excluded by D17 | not realized (no triplet of e_R) |

The lepton block is **strictly simpler** because it lacks both the color
sector (eliminating 4 candidate reps) and the matter content for an
SU(2) triplet RH partner (eliminating the iso triplet). The uniqueness
argument is therefore tighter on (2,1) than on (2,3).

## 5. Significance

### 5.1 What this theorem closes

D17-prime is the **lepton-sector analog of D17 from the YT-lane chain
D1-D17**. It establishes one of the structural primitives that an
analogous y_τ derivation chain would need.

### 5.2 What this theorem does NOT close

- It does **not** complete a y_τ Ward identity. The full chain analog
  would also require:
  - **D12-prime:** an SU(2) Fierz-analog factor on the (2,1) block playing
    the role of the SU(N_c) color Fierz `1/√(2 N_c)`. SU(2) Pauli
    completeness exists, but the integration through the rest of the chain
    (with the W boson playing the role of the gluon) needs to be verified.
  - **D16-prime:** tree-level Feynman-rule completeness of the bare
    framework action on the lepton scalar-singlet channel. The (2,3)
    proof relied on absence of fundamental scalar fields and bare contact
    4-fermion vertices in the action; the same conditions hold for the
    lepton sector by inspection, but the full diagrammatic enumeration
    has not been audited for the W-exchange topology.
  - **A combined identity argument** producing a sqrt-rational `y_τ_bare`
    in the form `g_? × C_τ`.
- It does **not** falsify the
  `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md` no-go.
  That no-go's falsifier requires "a worked SU(2)-Fierz-analog on the
  (2,1) block reproducing the YT-T1 structure with `sqrt(2 N_w) = 2`,
  including a verified D17-prime on (2,1)." This note proves the
  D17-prime half; the SU(2)-Fierz-analog half remains open.
- It does **not** predict any numerical lepton mass or Yukawa value.

### 5.3 What this theorem enables

- **M5-a unblocking partial:** the `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
  surviving research-level routes named M5-a as "D17-prime on (2,1)
  block — open structural problem with no current candidate." This
  note delivers the candidate. M5-a now reduces from "no current
  candidate" to "candidate established + needs SU(2)-Fierz-analog
  + D16-prime."
- **Cross-sector Koide-anchored work:** future M5-c attempts (Koide
  flagship Q + δ closure followed by cross-sector y_τ ↔ y_t identity)
  can cite D17-prime as established structural content.
- **Consistency check on the YT-lane chain:** the lepton-block analog's
  Z² = 2 is half of the Q_L block's Z² = 6, matching the heuristic
  `Z²_lep / Z²_Q = N_c^Q / N_c^lep = 3/1` after iso-cancellation.

## 6. Falsifiers

The theorem is falsified by any one of:

1. A demonstrated SU(2) iso triplet `e_R^a` (a = 1, 2, 3) field in the
   framework's anomaly-forced + hw=1 matter content. (No such field
   exists in the retained matter cluster, but its construction would
   change the uniqueness argument.)
2. A demonstrated alternative isospin-singlet × Lorentz-scalar
   composite on the L_L × H × e_R trilinear with normalization
   different from `Z² = 2`.
3. A correction to the doubled-hypercharge bookkeeping that changes
   which monomial is gauge-allowed.

## 7. What this note does NOT claim

- A `y_τ` Ward identity on the framework surface.
- A Lane 6 closure.
- A prediction of `m_τ`, `m_e`, `m_μ`, or any Yukawa eigenvalue.
- A falsification of the
  `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10` no-go.
- An analog of D12 (SU(N_c) color Fierz) on the (2,1) block.
- An analog of D16 (tree-level Feynman-rule completeness) on the (2,1)
  block.

## 8. Cross-references

- YT D17 (Q_L block): `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` §6 row D17
- YT D9 / scalar singlet derivation: `docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`
- YT class-5 non-Q_L analysis: `docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md`
- Combined no-go citing M5-a: `docs/CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- Direct Ward free Yukawa no-go (gauge-allowed monomial bookkeeping):
  `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
- LH doublet eigenvalue work on (2,1) and (2,3): `docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md`
- Minimal axioms substrate: `docs/MINIMAL_AXIOMS_2026-05-03.md`

## 9. Boundary

This is a narrow positive structural theorem on the lepton (2,1) block.
It closes one of the three named research-level routes' prerequisites
(M5-a) at the partial level. It does **not** unblock the surviving
research-level routes (M1, M5-a complete, M5-c) — those still require
either Koide flagship Q + δ closure or further structural content
(D12-prime + D16-prime + integration argument).

A class-A runner accompanies this note
(`scripts/frontier_lepton_block_scalar_singlet_composite_uniqueness.py`).
