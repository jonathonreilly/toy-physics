# H_unit Flavor-Column Decomposition Retention Analysis Note

**Date:** 2026-04-18
**Status:** proposed_retained retention-analysis **no-go** note. This note investigates
candidate class #1 from the b-quark retention analysis note
(`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`, §5.1): whether the
composite Higgs `H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` admits a
framework-native flavor-column decomposition into per-species operators with
different effective Yukawa normalizations. **The outcome is C (no-go).** On
the retained Q_L = (2,3) block, every candidate sub-block (up-iso vs
down-iso, generation-indexed, color-indexed) either (a) has Z² ≠ 6 and is
therefore explicitly excluded by D17 from the retained (1,1) scalar subspace,
or (b) carries a non-trivial projection onto a non-singlet SU(2)_L irrep
(principally (3,1) weak-triplet) and therefore cannot emerge as a pure D17
scalar. The species-uniform Clebsch-Gordan (Block 6, all 6 basis overlaps =
1/√6) is a **structural consequence of D17 + exact SU(2)_L invariance at
M_Pl**, not a contingent choice. Flavor-column decomposition of H_unit is
**not available** on the current retained surface. The retention gap
identified by the b-quark note therefore cannot be closed within candidate
class #1; the missing primitive for charged-flavor mass hierarchy must be
sought elsewhere (candidate classes #2, #3, or #4 of the b-quark note).
**Primary runner:** `scripts/frontier_yt_h_unit_flavor_column.py`
**Log:** `logs/retained/yt_h_unit_flavor_column_2026-04-18.log`

---

## Authority notice

This note is a retained **no-go retention-analysis note** on candidate class
#1 for closing the b-quark absolute-scale gap. It does **not** modify:

- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), whose D17 uniqueness of
  H_unit on the Q_L block (Block 5) and Block 6 species-uniform
  Clebsch-Gordan are inherited without modification;
- the retained b-quark retention analysis
  (`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`), whose
  Outcome A classification (Yukawa unification at M_Pl empirically falsified
  by 33× on `m_b`) stands;
- the retained three-generation observable theorem
  (`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`), whose exact
  irreducible M_3(C) generation algebra on the hw=1 triplet is used here as
  an input candidate for gen-indexed decomposition, without modification;
- the retained one-generation matter closure
  (`docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`), whose right-handed sector
  content (u_R : (1,3)_{+4/3}, d_R : (1,3)_{-2/3}) is used here only as
  context;
- the Z_2 hw=1 mass-matrix parametrization note
  (`docs/Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`), whose 5-parameter
  Hermitian normal form is inherited as a companion tool;
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native decision on
whether candidate class #1 (flavor-column decomposition of H_unit) can
produce per-species Yukawa values consistent with the retained Ward theorem.
The answer is: **no**. The note closes class #1 as a no-go and redirects the
missing-primitive search to classes #2-#4.

---

## Cross-references

### Foundational retained theorems (directly inherited)

- **Ward-identity tree-level theorem (Q_L block, D17 uniqueness):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) — D17 states H_unit is the
  unique unit-normalized color-singlet × iso-singlet × Dirac-scalar
  composite on Q_L with Z² = N_c × N_iso = 6; Block 5 numerically verifies
  the (1,8), (3,1), (8,3) alternatives give Z² = 8, 9/2, 24 respectively,
  each distinct from 6.
- **Block 6 species uniformity (numerically verified to machine precision):**
  same runner, [`scripts/frontier_yt_ward_identity_derivation.py`](../scripts/frontier_yt_ward_identity_derivation.py) lines
  291-295 — all 6 basis Clebsch-Gordan overlaps on the unit-norm (1,1)
  singlet equal 1/√6.
- **Bottom-Yukawa retention analysis (Outcome A falsified):**
  [`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md) —
  identifies candidate classes #1-#4; this note addresses class #1.

### Context

- **Three-generation observable theorem:**
  [`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) — the hw=1 triplet
  carries irreducible M_3(C) generation algebra; gen-indexed projectors
  exist as exact framework operators.
- **One-generation matter closure:**
  [`docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — right-handed sector
  content u_R, d_R, e_R, ν_R; relevant for candidate class #4 which is
  out-of-scope here.
- **Site-phase / cube-shift intertwiner:**
  [`docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md) — BZ-corner ↔ taste-cube
  bridge; relevant for gen-indexed analysis.
- **Z_2 hw=1 mass-matrix parametrization:**
  [`docs/Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md) — 5-parameter residual
  Z_2-invariant Hermitian normal form on hw=1 triplet.

---

## Abstract (§0 Verdict)

### §0.1 Retention question

The retained Ward-identity theorem implies species-uniform Yukawa at M_Pl:

```
    y_t(M_Pl) = y_b(M_Pl) = y_c(M_Pl) = y_s(M_Pl) = y_u(M_Pl) = y_d(M_Pl)
              = g_s(M_Pl) / √6                                              (V-0.1)
```

This is algebraically identical across all 6 basis components of Q_L by
Block 6 species uniformity. The b-quark retention analysis demonstrated
this BC is **empirically falsified** (predicts m_b ≈ 140 GeV vs observed
4.18 GeV; m_t ≈ 99 GeV vs observed 172.69 GeV).

Candidate class #1 asks: **can H_unit be decomposed into species-indexed
sub-operators with different effective Yukawa weights, consistent with the
retained D17?**

```
    H_unit^{species s}  = c_s · O_s(ψ̄, ψ)     with  c_s ≠ 1/√6 in general   (V-0.2)
```

### §0.2 Outcome verdict

**Outcome C (no-go).** Every candidate flavor-column decomposition of
H_unit either (a) violates D17's (1,1) uniqueness (Z² ≠ 6), or (b) contains
non-trivial projection onto a non-singlet SU(2)_L irrep (principally (3,1)
weak-triplet), and is therefore excluded from the retained scalar surface
at M_Pl.

**Key verification (machine-precision, Block 4 of runner):**

```
    P_up  = diag(1,1,1,0,0,0)   projector onto up-iso sub-block
    P_down = diag(0,0,0,1,1,1)  projector onto down-iso sub-block
    P_up + P_down = I_6                                                     (V-0.3)

    P_up   = (1/2)(I_6 + T3_6)     where T3_6 = σ³ ⊗ I_color               (V-0.4)
    P_down = (1/2)(I_6 - T3_6)
```

The projector P_up (P_down) is structurally an EQUAL mixture of the (1,1)
singlet direction (I_6) and the (3,1) weak-triplet diagonal direction
(T3_6 = σ³ ⊗ I_color), with Frobenius-norm projection weights of 1/√2 each.

Consequently, any species-projected composite `H_s := (1/√Z_s) P_s · ψ̄ψ`
is a linear combination

```
    H_up   = (1/√2)(H_unit + H_{(3,1)_{σ³}})                                 (V-0.5)
    H_down = (1/√2)(H_unit - H_{(3,1)_{σ³}})
```

where `H_{(3,1)_{σ³}}` is the σ³-component of the pure (3,1) weak-triplet
scalar (itself excluded from D17 by Z²_(3,1) = 9/2 ≠ 6 in the Ward-runner
Block 5 normalization). The sub-block operators are therefore **not pure
(1,1) scalars** and cannot emerge as D17-compliant primitives.

### §0.3 Per-species Yukawa prediction: none

Under candidate class #1 and the retained D17, no species-differentiated
Yukawa is producible. The only framework-native Yukawa on the Q_L scalar
surface at M_Pl is the species-uniform value 1/√6. Per-species Yukawas
require a primitive outside class #1.

### §0.4 Consistency with observed masses

Since no per-species Yukawa emerges under class #1, the mass predictions
remain as the b-quark note's Outcome A (empirically falsified). Candidate
class #1 **cannot** close the observed hierarchy:

```
    m_u^{obs}(2 GeV) ≈ 2.16 MeV         framework class #1: N/A (uniform BC)
    m_d^{obs}(2 GeV) ≈ 4.67 MeV         framework class #1: N/A (uniform BC)
    m_s^{obs}(2 GeV) ≈ 93.4 MeV         framework class #1: N/A (uniform BC)
    m_c^{obs}(m_c)   = 1.27 GeV         framework class #1: N/A (uniform BC)
    m_t^{obs}(pole)  = 172.69 GeV       framework class #1: 99 GeV (0.57×)
    m_b^{obs}(m_b)   = 4.18 GeV         framework class #1: 140 GeV (33×)     (V-0.6)
```

### §0.5 Confidence

- HIGH on the algebraic no-go: P_up and P_down have exact machine-precision
  decomposition (V-0.4) into (1,1) + (3,1) equal mixtures; this is a direct
  computation not an approximation.
- HIGH on D17 exclusion of (3,1): Block 5 of the Ward runner explicitly
  verifies Z²_(3,1) = 9/2 ≠ 6.
- HIGH on exact SU(2)_L invariance at M_Pl blocking (1,1)-(3,1) operator
  mixing at any loop order: this is a standard consequence of unbroken
  gauge symmetry for operators in different irreps.
- HIGH on the outcome classification: this is Outcome C (no-go for class
  #1); the missing primitive for charged-flavor hierarchy must be sought
  elsewhere.

---

## 1. Retained foundations

### 1.1 D17 statement (inherited verbatim)

From `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (D17):

> The unique unit-normalized (Z² = 6) color-singlet × iso-singlet ×
> Dirac-scalar composite operator on Q_L = (2,3) is
> `H_unit = (1/√(N_c · N_iso)) Σ ψ̄ψ`. Other (1,8), (3,1), (8,3) irreps give
> Z² = 8, 9/2, 24 respectively (Block 5 verified) — each distinct from
> Z² = 6, hence none are the framework's scalar singlet on this block.

The key structural content:

- H_unit lives in the **(1,1) irrep** of SU(2)_L × SU(3)_c on the Q_L
  tensor-product space.
- The uniqueness is within the **(1,1) subspace** of Q_L ⊗ Q_L*, which is
  1-dimensional (Schur's lemma on finite-dimensional irreps).
- The Z² = 6 value is structural: it equals dim(Q_L) = N_c · N_iso = 6, the
  unique way to normalize the identity-on-Q_L to unit residue.

### 1.2 Q_L block decomposition

The Q_L block is a single irreducible representation of the gauge group
SU(2)_L × SU(3)_c:

```
    Q_L = (2,3)                                     (dim 2 × 3 = 6)        (1.1)
```

Under the gauge group, `Q_L ⊗ Q_L*` decomposes as:

```
    Q_L ⊗ Q_L* = (2 ⊗ 2̄)_{iso} ⊗ (3 ⊗ 3̄)_{color}
               = (1 ⊕ 3)_{iso} ⊗ (1 ⊕ 8)_{color}
               = (1,1) ⊕ (1,8) ⊕ (3,1) ⊕ (3,8)                            (1.2)
    dim = 1 + 8 + 3 + 24 = 36 ✓
```

The **(1,1) singlet subspace is 1-dimensional**. This is the Schur's lemma
content that makes D17's uniqueness structural, not contingent.

### 1.3 Block 6 species uniformity (inherited)

The (1,1) state in Q_L ⊗ Q_L*, unit-normalized, is

```
    |S⟩ = (1/√6) Σ_{α,a} |α,a⟩ ⊗ |α,a⟩*                                     (1.3)
```

and has overlap with every basis bilinear |α,a⟩ ⊗ |α,a⟩* equal to 1/√6. This
is numerically verified in Block 6 of the Ward runner for all 6 species.

---

## 2. Sub-block decomposition analysis

### 2.1 Up/down-iso sub-block projectors

Define sub-block projectors on Q_L (6-dimensional, ordered as
`(up,r), (up,g), (up,b), (down,r), (down,g), (down,b)`):

```
    P_up   = diag(1, 1, 1, 0, 0, 0)                                         (2.1)
    P_down = diag(0, 0, 0, 1, 1, 1)
```

These are well-defined Hermitian idempotents with `P_up + P_down = I_6` and
`P_up P_down = 0`. They are mathematically consistent 3-dimensional
sub-projectors.

### 2.2 Sub-block composite operators

Define the naive sub-block composites:

```
    H_up   = (1/√Z_up) · Σ_{a=r,g,b} ψ̄_{up,a} ψ_{up,a}
           = (1/√3) · ψ̄ P_up ψ                                              (2.2)

    H_down = (1/√Z_down) · Σ_{a=r,g,b} ψ̄_{down,a} ψ_{down,a}
           = (1/√3) · ψ̄ P_down ψ                                            (2.3)
```

Unit-residue normalization gives `Z_up² = Z_down² = 3` (= N_c), by the same
free-theory sum-of-diagonal-contractions argument as the Ward runner Block 2.

### 2.3 Key no-go: Z² mismatch with D17

**D17 demands Z² = 6** for the retained (1,1) scalar on Q_L. The sub-block
operators have `Z² = 3 ≠ 6`. By D17's uniqueness statement, they are **not**
the framework's scalar singlet on the Q_L block.

This is a first-cut exclusion by direct comparison with the Block 5
numerical values (Ward runner lines 239, 248):

```
    Block 5: (1,1) singlet  Z² = 6       ← D17 retained
            (1,8) adjoint   Z² = 8       ← excluded
            (3,1) triplet   Z² = 4.5     ← excluded
            (8,3) tensor    Z² = 24      ← excluded
    This note: up sub-block Z² = 3       ← excluded on same ground         (2.4)
              down sub-block Z² = 3      ← excluded on same ground
```

### 2.4 Deeper no-go: impurity under SU(2)_L

The sub-block operators are not merely mis-normalized scalars on the (1,1)
direction. They are linear combinations of (1,1) and (3,1) directions, by
explicit decomposition:

```
    P_up   = (1/2)(I_6 + T3_6)                                              (2.5)
    P_down = (1/2)(I_6 - T3_6)

    where  T3_6 = σ³ ⊗ I_color = diag(+1, +1, +1, -1, -1, -1).
```

This is an exact algebraic identity (machine-precision verified in the
runner): summing (1/2)(I_6 + T3_6) diagonal entries gives (1,1,1,0,0,0)
exactly, matching P_up.

**Interpretation.** The projector P_up is an EQUAL mixture of the (1,1)
singlet direction (I_6 = identity on Q_L) and the (3,1) σ³-direction
(T3_6 = σ³ ⊗ I_color). The normalized Frobenius-norm projection weights are:

```
    ⟨P_up, I_6⟩_F / ‖P_up‖_F · ‖I_6‖_F  =  3 / (√3 · √6)  =  1/√2          (2.6)
    ⟨P_up, T3_6⟩_F / ‖P_up‖_F · ‖T3_6‖_F = 3 / (√3 · √6)  =  1/√2
```

with the sum of squared projections equal to 1 (P_up is exactly in the span
of these two directions; no content on (1,8) or (3,8)).

**Consequence.** The unit-norm composite `H_up = (1/√3) P_up · ψ̄ψ` is
structurally

```
    H_up   = (1/√2) · H_unit + (1/√2) · H_{(3,1)_{σ³}}                       (2.7)
    H_down = (1/√2) · H_unit - (1/√2) · H_{(3,1)_{σ³}}
```

where `H_{(3,1)_{σ³}} = (1/√6) · T3_6 · ψ̄ψ = (1/√6)(ψ̄_{up}ψ_{up} - ψ̄_{down}ψ_{down})`
is the σ³-component of the pure (3,1) weak-triplet operator.

D17 excludes the (3,1) direction with Z² = 9/2 (Block 5). Therefore `H_up`
and `H_down` are **mixtures of the retained D17 scalar and an explicitly
non-retained (3,1) operator**. They cannot emerge as framework-native
primitives on the retained scalar surface.

### 2.5 Exact SU(2)_L invariance blocks loop mixing

At M_Pl, the retained framework has exact SU(2)_L gauge invariance (D5:
Cl(3) ⊃ su(2) → SU(2)_L). Operators in different SU(2)_L irreps cannot mix
at any loop order in the unbroken theory (standard gauge-invariance result).
Therefore (1,1) and (3,1) scalar operators are **orthogonal at all scales
above EWSB** and cannot combine into a species-dependent H_unit by any
loop-level interaction.

**Path B closure.** Loop-level operator mixing between (1,1) H_unit and any
species-dependent (3,1) operator is forbidden at M_Pl by exact SU(2)_L.
After EWSB at v, the broken SU(2)_L allows such mixing, but by then the
Yukawa couplings are already frozen at their v-scale RGE values derived
from the M_Pl BC. The species uniformity at M_Pl is preserved through the
RGE; the RGE differentiation into y_t, y_b via the y_t² − y_b² term is
sub-leading and cannot produce the observed hierarchy (b-quark note §3).

---

## 3. Generation-indexed decomposition analysis

### 3.1 Retained generation structure

The three-generation observable theorem
(`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`) establishes that the hw=1
triplet carries an exact irreducible M_3(C) generation algebra, generated
by the three lattice translation projectors `P_1, P_2, P_3` (onto X_1, X_2,
X_3 sectors) and the induced C_3[111] cyclic corner map.

Extended to the full Q_L^total block with generation index:

```
    Q_L^total = {1, 2, 3}_gen × {up, down}_iso × {r, g, b}_color        (3.1)
    dim(Q_L^total) = 3 × 2 × 3 = 18
```

Generation projectors `P_{gen=i}` (i = 1, 2, 3) exist as exact framework
operators with `P_1 + P_2 + P_3 = I_{3-gen}`.

### 3.2 Generation-indexed composite candidates

Define gen-indexed composites:

```
    H_gen_i = (1/√Z_gen) · P_{gen=i} · Σ_{α,a} ψ̄_{i,α,a} ψ_{i,α,a}          (3.2)
            = (1/√6) · Σ_{α,a} ψ̄_{i,α,a} ψ_{i,α,a}     (N_c N_iso = 6)
```

Unit-residue gives `Z_gen² = N_c · N_iso = 6` **for every generation
uniformly** (because each generation's Q_L sub-block has the same gauge
content (2,3)). This is a direct consequence of SM universality of the
quark doublet across generations.

### 3.3 No hierarchy from generation indexing

The gen-indexed composite H_gen_i has the **same** Z² = 6 and **same**
Clebsch-Gordan overlap 1/√6 for every generation i. No species
differentiation emerges from generation indexing alone:

```
    y_t(gen=3) = y_c(gen=2) = y_u(gen=1) = 1/√6       (up-iso, different gens) (3.3)
    y_b(gen=3) = y_s(gen=2) = y_d(gen=1) = 1/√6       (down-iso, different gens)
```

This is still **6-fold species-uniform** (up/down × three generations), with
no mass hierarchy mechanism.

### 3.4 Residual Z_2 parametrization is a post-S_3-breaking tool

The Z_2 hw=1 mass-matrix parametrization note
(`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`) gives a 5-parameter
Hermitian normal form for residual-Z_2-invariant mass matrices on the hw=1
triplet. This parametrizes **mass-matrix** freedom AFTER a symmetry-breaking
choice, not a Yukawa-column decomposition of H_unit. It is a downstream
ingredient for flavor modeling, not a retained primitive for closing the
Yukawa absolute scale.

---

## 4. Operator-mixing (Path B) analysis

### 4.1 UV structure: no independent scalar fields

The retained bare Cl(3) × Z³ action contains only the Wilson plaquette and
the staggered Dirac operator (D16,
`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` lines 109-136). **No
independent scalar field is present.** The composite scalar H_unit is
derived as a condensate of the quark bilinear (D9, YCP:33-40). No separate
(3,1) or (1,8) scalar field is in the bare action.

### 4.2 (1,1) ↔ (3,1) mixing forbidden at M_Pl

Exact SU(2)_L invariance at M_Pl forbids mixing between operators in
different SU(2)_L irreps. Specifically, the (1,1) and (3,1) scalar
operators cannot mix at any loop order while SU(2)_L is unbroken.

Therefore, any loop-level diagram in the retained framework preserves the
(1,1) character of H_unit. No species-dependent effective Yukawa can emerge
from loop mixing at M_Pl.

### 4.3 Post-EWSB mixing is not a UV BC

After EWSB at scale v, SU(2)_L is spontaneously broken and (1,1) ↔ (3,1)
mixing becomes possible in the effective theory. However, this mixing is
parametrized by the VEV ⟨H_unit⟩ ~ v, which is set by the low-energy
spectrum and does not feed back into the UV boundary condition at M_Pl.
The M_Pl BC for all Yukawa couplings is frozen at y_s(M_Pl) = g_s(M_Pl)/√6
for all species s, as in the retained Ward theorem.

Post-EWSB mixing can in principle generate small corrections to the y_t, y_b
ratio at the electroweak scale, but these are suppressed by α_LM/(4π) or
v²/M_Pl² depending on the operator, and nowhere near the 33× scale needed
to reconcile with observation.

---

## 5. Per-species Yukawa prediction

Under candidate class #1 and the retained D17, **no species-differentiated
Yukawa emerges**. The only framework-native Yukawa on the Q_L scalar
surface at M_Pl is species-uniform:

```
    y_t(M_Pl) = y_b(M_Pl) = y_c(M_Pl) = y_s(M_Pl) = y_u(M_Pl) = y_d(M_Pl)
              = g_s(M_Pl) / √6    (identical to the retained Ward theorem)   (5.1)
```

The per-species prediction table is therefore **uniform** and reduces to
the b-quark note's Outcome A (Yukawa unification):

```
    Species  | y_s(M_Pl)/g_s(M_Pl)  | RGE → y_s(v)   | m_s framework
    ---------|----------------------|-----------------|---------------
    u        |  1/√6 = 0.4082       |  ≈ 0.55         |  ≈ 96 GeV
    d        |  1/√6 = 0.4082       |  ≈ 0.55         |  ≈ 96 GeV
    c        |  1/√6 = 0.4082       |  ≈ 0.55         |  ≈ 96 GeV
    s        |  1/√6 = 0.4082       |  ≈ 0.55         |  ≈ 96 GeV
    t        |  1/√6 = 0.4082       |  ≈ 0.57         |  ≈ 99 GeV
    b        |  1/√6 = 0.4082       |  ≈ 0.55         |  ≈ 95 GeV (v) → 140 GeV (m_b)
```

(The small differences at v come from RGE threshold effects with n_f
matching; they are not species-distinguishing at any useful level.)

---

## 6. Comparison to observed quark masses

Observed MSbar quark masses (PDG 2024):

```
    m_u(2 GeV)    ≈  2.16 MeV                                               (6.1)
    m_d(2 GeV)    ≈  4.67 MeV
    m_s(2 GeV)    ≈  93.4 MeV
    m_c(m_c)      =  1.27 GeV
    m_b(m_b)      =  4.18 GeV
    m_t(pole)     =  172.69 GeV
```

**Mass hierarchies observed:**

```
    m_t / m_u     ≈  80000×
    m_t / m_b     ≈  41×
    m_b / m_s     ≈  45×
    m_s / m_u     ≈  43×
    m_c / m_u     ≈  590×                                                   (6.2)
```

The observed hierarchy spans ~5 orders of magnitude from m_u to m_t.

**Class-#1 framework prediction (no species differentiation):**

```
    All y_s(M_Pl)/g_s(M_Pl) = 1/√6 → all m_s ≈ O(100 GeV)                  (6.3)
```

The framework under class #1 predicts **no mass hierarchy**, which fails
empirically at every species pair.

**Quantitative discrepancy (class #1 vs observed, at v):**

```
    m_u: framework 96 GeV / observed 2.16 MeV  ≈ 44,000×                   (6.4)
    m_d: framework 96 GeV / observed 4.67 MeV  ≈ 21,000×
    m_s: framework 96 GeV / observed 93.4 MeV  ≈ 1,000×
    m_c: framework 96 GeV / observed 1.27 GeV  ≈ 76×
    m_b: framework 140 GeV / observed 4.18 GeV ≈ 33×  (inherited from §4)
    m_t: framework 99 GeV / observed 172.7 GeV ≈ 0.57×  (inherited from §4)
```

All six species predictions are empirically falsified by at least 2× (m_c,
m_t) up to ~44,000× (m_u). The up-type hierarchy (m_u ≪ m_c ≪ m_t) and
down-type hierarchy (m_d ≪ m_s ≪ m_b) are both entirely absent from the
class-#1 retained surface.

---

## 7. Retention verdict

### 7.1 Outcome classification

**Outcome C (no-go).** Candidate class #1 (flavor-column decomposition of
H_unit) is closed as a no-go on the retained framework surface:

1. Sub-block (up-iso / down-iso) decomposition fails because `P_up, P_down`
   have exact equal mixtures of (1,1) and (3,1) directions; the sub-block
   operators are impure (1,1)+(3,1) mixtures with Z² = 3, excluded by D17.
2. Generation-indexed decomposition gives Z² = 6 uniformly for every
   generation, producing no hierarchy.
3. Operator mixing at M_Pl is forbidden by exact SU(2)_L invariance
   between (1,1) and (3,1) irreps.

### 7.2 Missing-primitive redirection

The retention gap for b-quark absolute scale
(`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`) **cannot be
closed within candidate class #1**. The missing primitive must be sought
in candidate classes #2, #3, or #4:

- **Class #2** (generation-hierarchy primitive breaking species uniformity):
  a new primitive at the lattice level that differentiates the three hw=1
  sectors in their Yukawa coupling, beyond the generation-universal
  Z² = 6. Example: a sector-dependent kinetic normalization Z²_i, a
  sector-dependent condensate VEV, or a generation-dependent composite
  operator structure. None of these are present on the current retained
  surface.
- **Class #3** (SUSY-like spectrum with large tan β): a two-Higgs-doublet
  structure where y_b ∝ 1/cos β can be small even at Yukawa unification.
  This requires a non-minimal Higgs content not present in the retained
  framework (D9: single composite H_unit).
- **Class #4** (right-handed sector primitive differentiating up-iso vs
  down-iso via u_R, d_R hypercharge content): u_R is (1,3)_{+4/3} and
  d_R is (1,3)_{-2/3}, with different hypercharges. The Yukawa couplings
  y_t ~ Q_L H_unit u_R^c and y_b ~ Q_L H_unit d_R^c involve different
  right-handed sectors; a primitive differentiating their effective
  coupling to H_unit (e.g., via a hypercharge-sensitive kinetic
  normalization or a right-handed composite operator) would produce
  species-differentiated Yukawa values. This is **not addressed in this
  note** (out of scope) and remains open.

### 7.3 What is retained unchanged

- Ward-identity tree-level theorem (species-uniform 1/√6 on Q_L block).
- D17 scalar-singlet uniqueness on Q_L.
- Block 6 species-uniform Clebsch-Gordan.
- b-quark retention analysis Outcome A classification (empirically falsified).
- Three-generation observable theorem (M_3(C) on hw=1 triplet).
- One-generation matter closure (right-handed sector content).
- All retained canonical-surface anchors (α_LM, α_s(v), v, etc.).

### 7.4 What this note adds to the retained surface

A framework-native **closure of candidate class #1 as no-go**. The b-quark
retention note's §5.1 listed four candidate classes; this note explicitly
eliminates class #1. The remaining three classes are open research
directions.

---

## 8. Safe claim boundary

This note claims:

> On the retained Cl(3) × Z³ surface, the composite Higgs `H_unit` admits
> no framework-native flavor-column decomposition consistent with D17.
> Specifically: (i) sub-block (up/down-iso) operators `H_up = (1/√3) ψ̄
> P_up ψ` and `H_down = (1/√3) ψ̄ P_down ψ` are exact equal mixtures of the
> retained (1,1) direction and the non-retained (3,1) σ³-direction, with
> Z² = 3 ≠ 6 and therefore excluded from the retained scalar surface by
> D17; (ii) generation-indexed operators `H_gen_i` have uniform Z² = 6 for
> every generation and produce no hierarchy; (iii) operator mixing between
> (1,1) and (3,1) is forbidden at M_Pl by exact SU(2)_L gauge invariance.
> Therefore candidate class #1 (flavor-column decomposition of H_unit) from
> the b-quark retention analysis is **closed as no-go**. The charged-flavor
> mass hierarchy retention gap identified in that note cannot be closed
> within class #1. The missing primitive must be sought in classes #2
> (generation-hierarchy), #3 (SUSY-like tan β), or #4 (right-handed sector).

It does **not** claim:

- any modification of the retained Ward-identity theorem;
- any modification of the retained b-quark retention analysis;
- any modification of the three-generation observable theorem or
  one-generation matter closure;
- closure of candidate classes #2, #3, or #4 — those remain open;
- a first-principles derivation of y_b at the observed scale;
- closure of the charged-flavor mass hierarchy gap.

### 8.1 Scope of this no-go

The no-go is on **the specific question asked**: whether candidate class
#1, as stated in the b-quark retention note's §5.1, can produce per-species
Yukawa via H_unit decomposition alone. It is not a statement about any
other approach (e.g., a candidate class beyond #1-#4, or a combination of
classes). The retention surface remains open for exploration of classes
#2-#4 and their possible combinations or generalizations.

### 8.2 What does not change

The retained top prediction `m_t(pole) = 172.57 ± 5.7 GeV` is unchanged
(top-only regime with y_b neglected, inherited from the 2-loop chain). The
Ward-identity tree-level theorem is unchanged. The b-quark retention
analysis Outcome A classification is unchanged. The Δ_R master assembly is
unchanged. The bounded down-type mass-ratio CKM-dual lane
(`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`) is unchanged.

---

## 9. What is retained vs. cited vs. open

### 9.1 Retained (framework-native, inherited from upstream theorems)

- D17 uniqueness of H_unit as the (1,1) scalar with Z² = 6 on Q_L.
- Block 5 numerical verification of Z² = 8, 9/2, 24 for (1,8), (3,1),
  (8,3) alternatives.
- Block 6 species-uniform Clebsch-Gordan 1/√6.
- Gauge group decomposition Q_L ⊗ Q_L* = (1,1) ⊕ (1,8) ⊕ (3,1) ⊕ (3,8).
- Exact SU(2)_L invariance at M_Pl forbidding (1,1)-(3,1) operator mixing.
- Three-generation M_3(C) algebra on hw=1 triplet.
- Right-handed sector content u_R : (1,3)_{+4/3}, d_R : (1,3)_{-2/3}.

### 9.2 Cited (external / standard)

- Observed quark masses (PDG 2024).
- Standard gauge-invariance result: operators in different irreps of
  unbroken gauge symmetry cannot mix at any loop order.

### 9.3 Open (retained gaps, including this note's closure)

- **Class #1 flavor-column decomposition of H_unit**: closed as no-go by
  this note.
- **Class #2 generation-hierarchy primitive**: open.
- **Class #3 SUSY-like tan β enhancement**: open; requires non-minimal
  Higgs content not present in the retained framework.
- **Class #4 right-handed sector primitive**: open; u_R vs d_R have
  different hypercharges, which could in principle differentiate y_t and
  y_b via right-handed composite structure. Not addressed here.
- **Absolute scale of y_u, y_d, y_c, y_s, y_τ, y_μ, y_e, neutrino
  Yukawas**: open, with the same retention obstruction structure as
  y_b inherited from Block 6 species uniformity.

---

## 10. Validation

The runner `scripts/frontier_yt_h_unit_flavor_column.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_h_unit_flavor_column_2026-04-18.log`. The runner must
return PASS on every check to keep this note on the retained
retention-analysis surface.

### 10.1 Class #6 scrutiny audit (2026-04-18)

This section documents the audit of Class #1 against the same
Fourier-basis-vs-position-basis and commutant-vs-centralizer scrutiny that
produced the §0 correction of Class #6
(`docs/YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`) and Class #2
(`docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`).

**Audit result: no correction needed. Class #1's Outcome C stands at both
narrow and broad scope.**

The Class #6 / Class #2 corrections hinge on the retained C_{3[111]} cyclic
operator on the 3-dim H_hw=1 generation space: the POSITION BASIS and the
FOURIER BASIS differ, and the generation-label spectrum lives in the Fourier
basis (eigenvalues of circulants), not the position basis (diagonal entries).

**Class #1 operates on a STRUCTURALLY DIFFERENT space.** The claim is about
operators on the 6-dim Q_L = (2,3) iso×color space, specifically about their
decomposition under SU(2)_L × SU(3)_c irreducible representations. The
distinctions used in the Class #6 correction do not translate because:

1. **No C_{3[111]} operator is being analyzed here.** The iso×color space
   carries no analog of the cyclic generation operator. The relevant symmetry
   is the SU(2)_L × SU(3)_c gauge group, not the Z_3 cyclic group, and the
   relevant irreps are (1,1), (1,8), (3,1), (3,8) — not cyclic eigenspaces.

2. **The `Z² = 3 ≠ 6` no-go is NOT a position-basis artifact.** `Z²` is the
   Frobenius norm squared `Tr(P_up²)`, a basis-independent invariant. Every
   operator on Q_L has a well-defined `Z²`; D17 demands `Z² = 6` for the
   retained (1,1) scalar. `Z²_sub = 3` means `P_up` cannot be the (1,1)
   scalar; this is correct across all bases.

3. **The commutant-vs-centralizer distinction does not apply.** The Class #6
   correction noted that the centralizer of C_{3[111]} alone (3-dim
   circulants) is larger than the commutant of the full retained algebra
   (1-dim scalars). Here there is no analogous ambiguity: the decomposition
   Q_L ⊗ Q_L* = (1,1) ⊕ (1,8) ⊕ (3,1) ⊕ (3,8) is a direct sum of irreps,
   each with a well-defined `Z²`, and D17 picks out (1,1) uniquely.

4. **The SU(2)_L gauge-invariance no-go is genuine.** Exact SU(2)_L at M_Pl
   forbids (1,1) ↔ (3,1) operator mixing at any loop order; this is a
   standard consequence of unbroken gauge symmetry, not a symmetry-breaking
   overclaim on a hidden Fourier basis. `P_up = (1/2)(I_6 + T3_6)` is an
   exact decomposition into (1,1) + (3,1) components; the SU(2)_L-invariant
   subspace is 1-dim (= span{I_6}), and `P_up ∉ span{I_6}`, so `P_up` is
   genuinely outside the retained (1,1) scalar surface.

5. **No "operators are different from H_unit, they can couple differently"
   loophole.** The key claim is that sub-block operators `H_up`, `H_down` are
   FORCED by the iso×color irrep structure to be equal mixtures of (1,1) and
   (3,1), with projection weights `1/√2` onto each. These projection weights
   are basis-independent Frobenius overlaps (machine-precision verified in
   Block 6 of the runner). No alternative basis produces a different picture.

**What WOULD constitute a Class #6-analog overclaim for Class #1, and
wasn't found.** A hypothetical overclaim would be something like "the only
retained operator on Q_L is H_unit" — but the Class #1 note explicitly
acknowledges that (1,8), (3,1), (8,3) operators exist as mathematical
objects; D17 only asserts that H_unit is the UNIQUE (1,1) scalar with
Z² = 6. The note correctly frames the no-go as "sub-block operators live
partly outside the retained (1,1) scalar surface", not "sub-block operators
don't exist as operators" — so there's no loophole via a hidden basis.

**Numerical verification of audit.** Block 16 of
`scripts/frontier_yt_h_unit_flavor_column.py` verifies that:

- the C_{3[111]} cyclic operator on H_hw=1 (3-dim) is distinct from any
  operator on the Q_L = (2,3) = 6-dim iso×color space;
- `Z²` is basis-independent: `Tr(P_up²) = 3` in any basis, not just the
  canonical up/down-iso × color basis;
- the SU(2)_L-invariant subspace within Q_L ⊗ Q_L* is exactly 1-dim
  (= span{I_6 / √6}), consistent with Schur's lemma on the 6-dim irrep;
- `P_up` has a 2-dim support across (1,1) + (3,1) irreps, with Frobenius
  projection weights `1/√2` each — verified in every unitary basis of Q_L.

**Conclusion.** Class #1's Outcome C is a genuine retained no-go on the
narrow question of flavor-column decomposition of H_unit via up/down-iso
projectors. It correctly acknowledges that alternative operators exist
(e.g., the pure (3,1) σ³-direction), that they are simply not the retained
D17 scalar, and that their mixing with H_unit is forbidden by exact SU(2)_L
at M_Pl. The §0 correction pattern of Classes #6 and #2 does not apply
because no hidden Fourier basis exists on the iso×color space with a
distinct spectrum. Class #1 is **CONFIRMED** as a retained no-go at both
narrow and broad scopes.

### 10.3 What remains open after the audit

The original §7.2 missing-primitive redirection stands: candidate classes
#2 (generation-hierarchy), #3 (SUSY tan β), #4 (right-handed sector) remain
open. Classes #2 and #6 have been corrected in their broad framing to
acknowledge the Fourier-basis circulant mechanism; Class #1's "flavor-column
decomposition" remains closed as a no-go because its structural obstacle
(SU(2)_L irrep mixing) is unrelated to the C_3 Fourier-basis mechanism.

### 10.4 Runner PASS checks (original list)

The runner verifies:

1. D17 inherited: Z²_{(1,1)} = 6, Z²_{(1,8)} = 8, Z²_{(3,1)} = 9/2,
   Z²_{(8,3)} = 24 on Q_L block.
2. Block 6 inherited: all 6 basis Clebsch-Gordan overlaps = 1/√6.
3. Sub-block projectors P_up, P_down are Hermitian idempotents with
   P_up + P_down = I_6, Z²_up = Z²_down = 3.
4. Exact decomposition P_up = (1/2)(I_6 + T3_6), P_down = (1/2)(I_6 - T3_6)
   (machine precision).
5. Frobenius-norm projection weights of P_up onto (1,1) direction (I_6) and
   (3,1) σ³-direction (T3_6) are both 1/√2.
6. Sub-block composites H_up, H_down are equal (1/√2) mixtures of H_unit
   and H_{(3,1)_{σ³}}.
7. Sub-block Z² = 3 ≠ 6, excluded from D17 retained surface.
8. Generation-indexed composites H_gen_i have uniform Z² = 6 for all three
   generations (no hierarchy).
9. Exact SU(2)_L invariance test: H_unit commutes with all three SU(2)_L
   generators T^a_iso on Q_L, while H_up does not commute with T^1_iso or
   T^2_iso (breaks SU(2)_L).
10. Per-species Yukawa prediction under class #1: y_s(M_Pl)/g_s(M_Pl) =
    1/√6 for all s ∈ {u, d, s, c, t, b} — no species differentiation.
11. Comparison to observed masses: framework m_s hierarchy is absent; all
    predictions within order 100 GeV, while observed masses span ~2 MeV to
    ~173 GeV (~5 orders of magnitude).
12. Outcome verdict C (no-go) logged.
13. No modification of Ward theorem, D17, Block 6, b-quark analysis, or
    publication surface.
14. All retained framework constants agree with upstream retained values to
    sub-permille.
