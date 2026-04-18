# Generation-Hierarchy Primitive Retention Analysis Note

**Date:** 2026-04-18 (amended 2026-04-18 with Fourier-basis spectrum correction)
**Status:** framework-native retention analysis. **Outcome D refined (retained
narrow no-go + retained positive Fourier-basis circulant mechanism flagged):**
the original Outcome D is narrow-technically correct about the POSITION-BASIS
diagonal content of C_3-commuting operators (every diagonal entry is equal by
cyclic symmetry), but the broader framing "no retained mechanism for generation
hierarchy" was too strong. The retained C_3-commuting operators — circulants
`H = a·I + b·C + b̄·C²` — have THREE DISTINCT Fourier-basis eigenvalues
`λ_k = a + 2|b| cos(arg(b) + 2πk/3)`, which IS a generation-labeled spectrum.
See **§0 Correction** below for the revised picture and cross-reference to
`codex/science-workspace-2026-04-18`'s Koide circulant character-theoretic
derivation, which uses this Fourier-basis mechanism to derive Koide Q = 2/3
exactly (modulo two non-retained ingredients A1 and P1). The original Path A
closure on `(1, -1/2, -1/2)` real-parts-of-characters weights is narrow-correct
but represents only one operator in the 2-parameter circulant family.
**Primary runner:** `scripts/frontier_yt_generation_hierarchy_primitive.py`
**Log:** `logs/retained/yt_generation_hierarchy_primitive_2026-04-18.log`

---

## §0 Correction (amendment 2026-04-18)

**This note's original outcome-framing was overly strong and is corrected
here.** The original abstract concluded "Outcome D retained no-go: the retained
three-generation observable theorem does NOT supply absolute
generation-dependent Yukawa weights at M_Pl." This is narrow-technically
correct about the POSITION-BASIS DIAGONAL CONTENT of C_3-commuting operators,
but it MISSED the complementary path via the FOURIER-BASIS EIGENVALUE SPECTRUM
of the retained circulant family.

### What the original analysis correctly established

The cyclic-symmetry theorem of §2.5: any operator H on H_hw=1 commuting with
C_{3[111]} satisfies `H_{11} = H_{22} = H_{33}` in the generation (position)
basis. The full retained algebra `R = M_3(C)` has 1-dim commutant (scalars
only). These results are correct and unchanged. The Path A candidate of §2.2,
which identifies weights with real parts of C_3 characters on position-basis
vectors (giving `(1, -1/2, -1/2)` with two negative entries), correctly
concludes that this specific candidate is unphysical.

### What the original framing missed

The physical generation labels are the FOURIER-BASIS EIGENVECTOR INDICES, not
the position-basis diagonal entries. The retained circulants in the centralizer
of C_{3[111]} (a 3-dim subalgebra of M_3(C) larger than the 1-dim commutant of
the full algebra) are

```
    H = a·I + b·C + b̄·C²,     a ∈ ℝ, b ∈ ℂ
```

and have three **distinct Fourier-basis eigenvalues**

```
    λ_k = a + 2|b| cos(arg(b) + 2πk/3),    k ∈ {0, 1, 2}.
```

For generic `(a, b)`, the three eigenvalues are distinct — this IS a
generation-label-dependent spectrum (= three distinct real positive eigenvalues
for a > √2|b|). The Path A real-parts-of-characters weights `(1, -1/2, -1/2)`
are a specific operator `Re(C_3) = (C_3 + C_3^†)/2` within this 2-parameter
family, not the generic case.

Path A's test — "identify w_i with Re(ω^{i-1}) on POSITION-BASIS vectors X_i" —
confuses the (1-dim-per-basis-vector) diagonal data with the (3-dim) Fourier
eigenvalue data. Fourier-basis eigenvalues are NOT diagonal entries of the
operator in the position basis; they are the eigenvalues of the operator,
which for circulants live naturally in the Fourier basis.

### External cross-reference (in-flight, not modified)

The `codex/science-workspace-2026-04-18` branch's
`docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` uses the
retained circulant family to derive the charged-lepton Koide relation Q = 2/3
as a character-theoretic consequence of this Fourier-basis spectrum,
conditional on:

- **A1 Frobenius equipartition** `3a² = 6|b|²` → `|b| = a/√2` → √2 coefficient
- **P1 √m identification** `λ_k = √m_k` (phenomenological)

Both A1 and P1 are flagged in that note as NON-RETAINED (structural assumption
+ phenomenological identification). Crucially, A1 and P1 are the MISSING
PRIMITIVES not addressed by Paths A/B/C/D of the present note; Path A's
closure is correct but does not rule out the A1+P1 path.

### Revised outcome for Class #2 (Generation-hierarchy primitive)

- The **narrow-technical claim** of §2.5 (cyclic-symmetry theorem forbidding
  generation-asymmetric DIAGONAL content of C_3-commuting operators) remains
  correct and is unchanged.
- The **broader interpretation** "no retained mechanism for generation
  hierarchy" is corrected. The retained circulant family in the centralizer of
  C_{3[111]} DOES provide distinct Fourier-basis eigenvalues. The retention
  gaps are the two non-retained ingredients A1 and P1 listed above, NOT the
  algebraic structure itself.
- Class #2's correct status: **retained narrow no-go on generation-ASYMMETRIC
  POSITION-BASIS DIAGONAL content + retained positive Fourier-basis
  circulant-spectrum mechanism with 2 named non-retained primitives (A1, P1)**.
  The 9-pin observational requirement stated in the original Outcome D is
  refined to "2 named primitives (equipartition, √m-identification) +
  1 overall-scale + 1 phase (δ → rad) remain non-retained for the charged-lepton
  Koide sector; circulant algebraic structure is retained."
- The four paths A/B/C/D closed in §5.1 were all analyzed in the POSITION
  basis. The Fourier-basis eigenvalue path through retained circulants is
  outside those four paths and provides the positive mechanism.
- Five "missing primitives" (§5.3) are still sharply-posed; however Primitive
  1 (C_{3[111]}-breaking retained operator) is no longer the ONLY candidate —
  the Fourier-basis eigenvalue spectrum through C_3-COMMUTING circulants
  supplies distinct real eigenvalues without breaking C_3 on the operator
  algebra.

### Confidence on the amendment

HIGH on all points above. The position-basis cyclic-symmetry theorem of §2.5
is correct. The Fourier-basis eigenvalue split of circulants is standard linear
algebra (the discrete Fourier transform diagonalizes the cyclic shift matrix;
circulants diagonalize jointly in the Fourier basis). The retained circulants
live in a 3-dim centralizer already implicitly noted by §2.5 (as the space of
C_3-commuting operators). The Koide branch's retention stack (A1, P1) is
explicit about what's non-retained.

**The rest of this note (§1-§9) is the ORIGINAL retained-no-go analysis of
position-basis diagonal content, preserved unchanged.** It remains correct at
the stated narrow scope (position-basis diagonal entries of C_3-commuting
operators); the corrected interpretation above supersedes the original
"no generation hierarchy" framing for the broader Fourier-basis eigenvalue
spectrum.

---

## Authority notice

This note is a **retention-analysis note** on the generation-hierarchy primitive question. It does **not** modify:

- the retained three-generation observable theorem
  (`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`), whose M_3(C)
  algebra on H_hw=1 is inherited as-is;
- the retained three-generation matter structure note
  (`docs/THREE_GENERATION_STRUCTURE_NOTE.md`), whose 8 = 1 + 1 + 3 + 3
  orbit decomposition is inherited as-is;
- the retained S_3 taste-cube decomposition note
  (`docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`), whose
  C^8 ~= 4 A_1 + 2 E decomposition is inherited as-is;
- the retained site-phase / cube-shift intertwiner note
  (`docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`);
- the retained Z_2 hw=1 mass-matrix parametrization
  (`docs/Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`);
- the charged-lepton bounded review
  (`docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`),
  whose 19 runners / 518 PASS status and Theorem 7 observational-pin
  closure are inherited as-is;
- the retained structural no-go survey
  (`docs/STRUCTURAL_NO_GO_SURVEY_NOTE.md`), whose six charged-lepton
  no-gos are now explicitly shown to generalize across sectors;
- the bottom-Yukawa retention analysis note
  (`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`),
  whose Outcome A (Yukawa unification empirically falsified) is the
  starting point of this analysis;
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native decision on whether the retained three-generation structure supplies ABSOLUTE generation-dependent Yukawa weights at M_Pl capable of rescuing the fermion mass hierarchy. The answer is NO: the retained C_{3[111]} cyclic structure is symmetric, the retained algebra on H_hw=1 is the full M_3(C) with no canonical scale selector, and any generation-resolved hierarchy must come from content OUTSIDE the current retained surface.

---

## Cross-references

### Foundational retained theorems (directly inherited, not modified)

- **Three-generation observable no-proper-quotient theorem:**
  `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` —
  retained translation projectors {P_1, P_2, P_3} + C_{3[111]} cycle
  generate M_3(C) irreducibly on H_hw=1.
- **Three-generation matter structure:**
  `docs/THREE_GENERATION_STRUCTURE_NOTE.md` —
  orbit algebra 8 = 1 + 1 + 3 + 3, physical-lattice necessity.
- **S_3 taste-cube decomposition:**
  `docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md` —
  C^8 ~= 4 A_1 + 2 E (no sign irrep A_2).
- **Site-phase / cube-shift intertwiner:**
  `docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md` —
  exact bridge between C^8 taste cube and BZ-corner subspace.
- **Z_2 hw=1 mass-matrix parametrization:**
  `docs/Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md` —
  5-real-parameter Hermitian family once S_3 → Z_2.
- **Ward identity tree-level theorem:**
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` —
  Block 6 species-uniform Clebsch-Gordan (all six basis components
  of (1,1) singlet = 1/√6).

### Context (retention analyses upstream of this note)

- **Bottom-Yukawa retention:**
  `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` —
  Yukawa unification at M_Pl implied by Block 6 species uniformity;
  empirically falsified on m_b by 33×.
- **Charged-lepton bounded review:**
  `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` —
  Koide Q = 2/3 on hw=1 triplet is algebraically equivalent to
  equal-character-weight condition; hierarchy requires observational
  pin.
- **Structural no-go survey:**
  `docs/STRUCTURAL_NO_GO_SURVEY_NOTE.md` — six no-gos on the
  charged-lepton hw=1 mass mechanism.

---

## Abstract (Verdict)

**Outcome D (retained no-go):** the retained three-generation structure — whether read through (A) the C_{3[111]} cycle from translation projectors, (B) the orbit algebra 8 = 1 + 1 + 3 + 3, (C) the hw-grading — does NOT supply framework-derived, absolute generation-dependent Yukawa weights at M_Pl capable of breaking the Block-6 species uniformity. Each candidate path fails for the same deep reason: the retained surface has a cyclic Z_3 symmetry (from C_{3[111]}) under which the three hw=1 basis vectors X_1, X_2, X_3 are equivalent, so any retained operator that commutes with the full M_3(C) algebra acts as a scalar multiple of I_3 on generations.

**Path A (C_{3[111]} cycle).** The retained cyclic operator C_{3[111]} permutes generations X_1 → X_2 → X_3 → X_1 with equal amplitude on each. The three generations are cyclically equivalent under the retained algebra. No retained scalar selector distinguishes a specific generation. **Closed negatively.**

**Path B (orbit algebra 8 = 1 + 1 + 3 + 3).** Each triplet (hw=1 and hw=2) is an irreducible 3-dimensional permutation carrier of the C_{3[111]} action; it decomposes as A_1 ⊕ E under S_3 (S_3 taste-cube decomposition note). The three basis states within a triplet are permuted by S_3, not distinguished by magnitude. The "3" in the orbit is a symmetric triplet, not a hierarchy. **Closed negatively.**

**Path C (hw-grading).** The three hw=1 generations sit at a SINGLE Hamming-weight level (hw=1), not at three different hw values. The Wilson mass m(p) = Σ_μ (1 − cos p_μ) is constant (= 2) across the hw=1 triplet by construction. The three other hw sectors (hw=0, hw=2, hw=3) exist but do NOT correspond to light-species generations — hw=0 is the single trivial state, hw=2 is another three-cyclic-equivalent triplet (not the same species family), hw=3 is a single state. Using hw as a generation label requires identifying generations 1/2/3 with distinct hw values, which violates the 3-in-hw=1 interpretation of the three-species theorem. **Closed negatively.**

**Path D (retained no-go).** The three-generation observable theorem is a statement ABOUT the retained surface being generationally SYMMETRIC (the exact algebra is M_3(C) generated by symmetric cyclic and permutation operations). Absolute generation-dependent content requires breaking the cyclic symmetry, which cannot occur from retained algebra alone (any operator-algebra-invariant selector is a scalar). The shape theorem of the charged-lepton review supplies three independent weight slots, but those weights must be SUPPLIED externally — they are not framework-derived on the current retained surface. **This is the outcome.**

**Numerical consequence.** If a generation-hierarchy primitive existed with framework-derived weights (w_1, w_2, w_3), the retained Yukawa unification BC would generalize to

```
    y_{species, gen}(M_Pl) / g_s(M_Pl) = w_{gen} / √6                  (D-Y)
```

Five concrete retained-surface candidates for (w_1, w_2, w_3) were tested in the runner, each derivable from retained content by construction:

| Candidate | Source | (w_1, w_2, w_3) | Predicted Q | Match to observed leptons Q = 2/3 |
|---|---|---|---|---|
| Uniform (null) | trivial | (1, 1, 1) | 1/3 | miss by 100% |
| C_{3[111]} powers (real part) | ω^0, ω^1, ω^2 | (1, -1/2, -1/2) | — | non-physical (negative mass²) |
| Hamming weights on hw=1 | w = Σ components | (1, 1, 1) | 1/3 | miss (triply degenerate) |
| Joint translation characters | χ(T_μ) products | (-1, -1, -1) | — | non-physical |
| S_3 dimension weights | dim(A_1) = 1, dim(E) = 2 | (1, 2, 2) | 0.3411 | miss by 49% |

None of the five retained candidates reproduces the observed mass hierarchies — not even approximately — because the retained cyclic symmetry forbids the factor-of-~10^5 scale spread observed across generations.

**Observed mass hierarchies (context):**

```
    Up-type:    m_u : m_c : m_t   ≈  2.16e-3 : 1.27    : 172.69
                ratio m_c/m_u  ≈ 590,   ratio m_t/m_c  ≈ 136.
    Down-type:  m_d : m_s : m_b   ≈  4.67e-3 : 0.0934  : 4.18
                ratio m_s/m_d  ≈ 20,    ratio m_b/m_s  ≈ 45.
    Leptons:    m_e : m_μ : m_τ   ≈  0.511e-3 : 0.1057 : 1.777
                ratio m_μ/m_e  ≈ 207,   ratio m_τ/m_μ  ≈ 17.
```

The span from lightest to heaviest quark/lepton is ~10^5 (u to t), ~10^3 (d to b), ~3500 (e to τ). The retained C_{3[111]} cycle on H_hw=1 permutes generations with magnitude 1 — it cannot produce a spread of order 10^5.

**Retention verdict:** this is a **retained no-go**: the absolute generation-dependent Yukawa weights at M_Pl are NOT derivable from the current retained surface. A new primitive beyond the current retained core is required. Candidate primitives (none retained) are sharpened in §5. The charged-lepton bounded package's observational-pin structure is confirmed to extend uniformly to the quark sector.

**Confidence:**
- HIGH on the Path A C_{3[111]} cyclic-equivalence argument (algebraic,
  follows immediately from X_1 → X_2 → X_3 → X_1 being a unitary
  permutation);
- HIGH on the Path B orbit-algebra S_3-permutation argument
  (representation-theoretic, 3 = 1 ⊕ 2 under S_3 within the triplet, no
  magnitude-distinguishing content);
- HIGH on the Path C hw-grading argument (the 3 in 1+1+3+3 sits at a
  single hw value, not at three distinct values);
- HIGH on the Outcome D verdict (all three candidate paths close
  negatively by independent structural arguments);
- HIGH on extending the charged-lepton bounded result across sectors
  (quarks and leptons both sit on the same hw=1 cyclic triplet
  surface).

---

## 1. Retained foundations (inherited)

We work on the retained `Cl(3)/Z^3` framework surface.

### 1.1 Three-generation observable theorem on H_hw=1

From `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, the retained `hw=1` triplet T_1 = span{X_1, X_2, X_3} carries an irreducible M_3(C) algebra generated by:

- three lattice translations T_x = diag(−1, +1, +1), T_y = diag(+1, −1, +1), T_z = diag(+1, +1, −1);
- induced cyclic operator C_{3[111]}: X_1 → X_2 → X_3 → X_1.

Rank-1 projectors P_1, P_2, P_3 onto X_1, X_2, X_3 are generated by the translation characters. Every matrix unit E_{ij} is expressible as P_i C_3^k P_j, so the retained algebra is all of M_3(C).

### 1.2 Orbit algebra 8 = 1 + 1 + 3 + 3

From `docs/THREE_GENERATION_STRUCTURE_NOTE.md`, the taste cube C^8 = (C^2)^{⊗3} decomposes under Hamming weight as:

| Sector | hw | dim | content |
|---|---|---|---|
| O_0 | 0 | 1 | trivial state (0,0,0) |
| T_1 | 1 | 3 | hw=1 triplet {X_1, X_2, X_3} |
| T_2 | 2 | 3 | hw=2 triplet {(1,1,0), (1,0,1), (0,1,1)} |
| O_3 | 3 | 1 | singleton (1,1,1) |

Total dimension 8 = 1 + 3 + 3 + 1, rewritten as 1 + 1 + 3 + 3 in the orbit-algebra reading.

### 1.3 S_3 taste-cube decomposition

From `docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`, under the S_3 axis-permutation action:

- hw=0 sector: 1 × A_1 (trivial);
- hw=1 sector: A_1 ⊕ E (one trivial + 2-dim standard representation);
- hw=2 sector: A_1 ⊕ E (identical structure);
- hw=3 sector: 1 × A_1 (trivial).

Total: C^8 ~= 4 A_1 ⊕ 2 E. The sign irrep A_2 does NOT appear.

**Key structural fact**: within the hw=1 triplet, the three generations X_1, X_2, X_3 are NOT S_3-invariant individually — they are permuted by S_3. The S_3-invariant direction is the 1-dim A_1 sub-block, which is (X_1 + X_2 + X_3)/√3 (equal-weight combination, NOT a generation basis state).

### 1.4 Ward identity Block 6 species uniformity

From `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, the unit-norm (1,1) singlet on Q_L ⊗ Q_L* carries Clebsch-Gordan weight 1/√6 on every one of the 6 basis components (3 colors × 2 iso-indices). This Block 6 uniformity implies Yukawa unification at M_Pl:

```
    y_t(M_Pl) / g_s(M_Pl) = y_b(M_Pl) / g_s(M_Pl) = 1/√6              (1.4)
```

When generalized to the three-generation framework, the same argument applied to each generation would require an analog Clebsch-Gordan on the generation label.

---

## 2. Generation weight structure analysis

### 2.1 Structural question

**The question.** Given the retained three-generation observable theorem's irreducible M_3(C) algebra on H_hw=1, is there a framework-derived mechanism that assigns DISTINCT weights (w_1, w_2, w_3) to the three generations, producing a generation-hierarchy prediction:

```
    y_{species, gen}(M_Pl) = w_{gen} · g_s(M_Pl) / √6                    (2.1)
```

**The answer.** NO. Any retained operator that can be constructed from {P_1, P_2, P_3, C_{3[111]}} is subject to the following symmetry constraint: under C_{3[111]} conjugation, P_1 → P_2, P_2 → P_3, P_3 → P_1. Therefore any retained Hermitian operator H satisfying [H, C_{3[111]}] = 0 has equal diagonal entries in the generation basis:

```
    H_{11} = H_{22} = H_{33}.                                            (2.2)
```

Any operator that "sees" different generations via different weights must BREAK the C_{3[111]} cyclic symmetry. No such operator exists on the retained surface alone — the retained surface IS the symmetric M_3(C) algebra.

### 2.2 Path A: C_{3[111]} cycle weights

**Candidate weights.** The cyclic operator C_{3[111]} has eigenvalues {1, ω, ω²} on the three eigenvectors

- e_+ = (1, 1, 1)/√3 (trivial, eigenvalue 1);
- e_ω = (1, ω, ω²)/√3 (eigenvalue ω);
- e_{ω²} = (1, ω², ω)/√3 (eigenvalue ω²).

**Test.** Identify (w_1, w_2, w_3) with the real parts of the cycle eigenvalues on (X_1, X_2, X_3). Since C_{3[111]} permutes the computational basis, each X_i has character 0 under each power of C_3 (as a representation-basis vector):

```
    Tr(P_1 · C_{3[111]}^k) = δ_{k mod 3 = 0}                              (2.3)
```

so the cyclic character projection on (X_1, X_2, X_3) gives (1, 0, 0) — uninformative (it trivially separates basis vectors but gives no graded weight).

Alternatively, identify w_i = Re(ω^{i-1}) = {1, −1/2, −1/2}. This yields two equal generations and one distinct, but two weights are negative (non-physical for a Yukawa weight), and the resulting "Koide" value

```
    Q_candidate = (1 − 1/2 − 1/2) / (1 + √(−1/2) + √(−1/2))²            (2.4)
```

is complex-valued and unphysical.

**Verdict.** Path A does NOT supply real positive absolute weights. Closed negatively.

### 2.3 Path B: Orbit-algebra hierarchy

**Candidate weights.** Within the hw=1 triplet, the S_3 decomposition is A_1 ⊕ E. If we assign weights by S_3 irrep dimension:

```
    w_{A_1} = dim(A_1) = 1                                                (2.5)
    w_{E}   = dim(E)   = 2                                                (2.6)
```

The A_1 direction is e_+ = (1, 1, 1)/√3; the E direction is the 2-dim subspace orthogonal to e_+. But the three generations (X_1, X_2, X_3) are NOT eigenvectors of the irrep decomposition — they are linear combinations of A_1 and E content:

```
    X_i  =  (1/√3) e_+  +  (2-dim E-component)                            (2.7)
```

Assigning (w_1, w_2, w_3) to the three X_i vectors therefore requires assigning a single real weight to each X_i, but the S_3 orbit content gives no such distinguishing structure. The natural "flat" assignment is (w_1, w_2, w_3) = (1, 1, 1) — triply degenerate.

Alternative: assign weights to the two separately (A_1 vs. E). This gives only 2 distinct values for 3 generations, which cannot reproduce a 3-level hierarchy.

**Verdict.** Path B does NOT supply three distinct absolute weights on the three generations. Closed negatively.

### 2.4 Path C: hw-grading hierarchy

**Candidate identification.** Could the three generations sit at three different Hamming weights, with the mass scale set by hw?

**No.** The retained three-species theorem (`docs/THREE_GENERATION_STRUCTURE_NOTE.md`) identifies the three generations with the 3-dim hw=1 triplet — all three sit at the SAME Hamming weight (= 1). The Wilson mass at hw=1 is m(p) = 3 · 1 = 2 (using m = Σ(1 − cos p_μ) with each p_μ ∈ {0, π}), identical across all three generations.

Alternative: split generations across hw=1 and hw=2 sectors. But the hw=2 triplet is structurally equivalent to hw=1 (both are permutation representations of S_3 decomposing as A_1 ⊕ E); assigning one generation to hw=1 and another to hw=2 breaks the retained three-species interpretation at the foundational level.

Alternative: use hw as a generation *label* for three of the four Hamming-weight levels {0, 1, 2, 3}, picking three of the four. But this requires discarding one of the four sectors arbitrarily, and it does not match the retained identification of the hw=1 triplet as the three generations.

**Verdict.** Path C does NOT supply a hw-based generation hierarchy consistent with the retained framework. Closed negatively.

### 2.5 Path D: Retained no-go (the outcome)

**Theorem (retained generation-hierarchy no-go).** Any retained operator H on H_hw=1 that is a polynomial in {P_1, P_2, P_3, C_{3[111]}} and that commutes with C_{3[111]} satisfies H_{11} = H_{22} = H_{33} in the generation basis.

*Proof.* Let V = C_{3[111]} denote the generator of the cyclic group action X_1 → X_2 → X_3 → X_1. In the generation basis, V is the cyclic permutation matrix

```
    V = [[0, 0, 1],
         [1, 0, 0],
         [0, 1, 0]].                                                       (2.8)
```

Any operator H commuting with V satisfies V H V^† = H, i.e., H is cyclic-symmetric. A matrix is cyclic-symmetric iff its entries satisfy H_{ij} = H_{(i+k) mod 3, (j+k) mod 3} for all k ∈ {0, 1, 2}. In particular, H_{11} = H_{22} = H_{33}. □

**Consequence.** Any retained attempt to produce generation-resolved hierarchy on H_hw=1 must BREAK the C_{3[111]} symmetry. But the C_{3[111]} symmetry is part of the retained operator algebra. No retained mechanism exists.

**This is Outcome D.**

---

## 3. Per-generation Yukawa prediction (candidate structures, all closed)

### 3.1 Flat (Yukawa unification) candidate

Under Block 6 species uniformity (Ward theorem), the flat weights (w_1, w_2, w_3) = (1, 1, 1) give the Yukawa unification BC already analyzed in `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`:

```
    y_t(M_Pl) = y_c(M_Pl) = y_u(M_Pl) = y_b(M_Pl) = y_s(M_Pl)
              = y_d(M_Pl) = y_τ(M_Pl) = y_μ(M_Pl) = y_e(M_Pl)
              = g_s(M_Pl) / √6  ≈ 0.436.                                   (3.1)
```

Running forward through 2-loop SM RGE with 9 simultaneous Yukawas all at g_s(M_Pl)/√6 gives a worse quasi-fixed point than the 2-Yukawa case (more Yukawa pulling). This is the worst-case empirical prediction: all masses are O(100 GeV) at v, which fails for every generation except possibly m_t.

### 3.2 Character-assigned weights

Assigning (w_1, w_2, w_3) to the real parts of the C_{3[111]} characters on X_i gives (w_1, w_2, w_3) = (1, -1/2, -1/2), which has negative entries — non-physical for a squared coupling.

### 3.3 S_3 irrep-dimension weights

Assigning (w_1, w_2, w_3) = (1, 2, 2) from A_1 ⊕ E multiplicity gives Koide Q = (1 + 2 + 2)/(1 + √2 + √2)² = 5/(1 + 2√2)² ≈ 0.3411, which differs from the observed charged-lepton Q_ℓ = 2/3 by 49% (too flat — Q = 1/3 is the fully-degenerate limit, and (1,2,2) is close to that limit).

For the b-quark under this weighting:

```
    y_b(M_Pl) / g_s(M_Pl) = w_3 / √6 = 2/√6 ≈ 0.816                       (3.2)
```

This is larger than the flat BC (= 0.408), which makes the m_b prediction WORSE (not better). The (1, 2, 2) weighting also fails to produce the observed ~10^3 spread between m_d and m_b.

### 3.4 Geometric/exponential candidates

Exponential weights (1, e, e²) or (1, ε, ε²) with tunable ε could reproduce the observed geometric hierarchy (e.g., for charged leptons ε ≈ 0.058 gives ratios (1 : ε : ε²) = (1 : 0.058 : 0.0034) matching m_τ : m_μ : m_e ≈ 1 : 0.060 : 0.00029 with one-order-of-magnitude slack). But "ε" is NOT framework-derived — it is a free parameter that would need to be fixed by observation, which returns us to the observational-pin closure already documented for charged leptons.

Moreover, the geometric scales differ across species:

```
    Lepton  ε_ℓ ≈ 0.058 (using m_τ as base)
    Down    ε_d ≈ 0.022 (using m_b as base)
    Up      ε_u ≈ 7e-3 (using m_t as base)
```

Three distinct geometric parameters ε_ℓ, ε_d, ε_u would be required — no single retained generation-hierarchy primitive supplies all three.

### 3.5 Summary table

| Candidate | (w_1, w_2, w_3) | y_b(M_Pl)/g_s | Koide Q | Matches observed m_b? |
|---|---|---|---|---|
| Flat (unification) | (1, 1, 1) | 1/√6 ≈ 0.408 | 1/3 | NO (m_b ≈ 140, 33× over) |
| C_{3[111]} real parts | (1, -1/2, -1/2) | non-physical | complex | NO |
| Hamming on hw=1 | (1, 1, 1) | 1/√6 | 1/3 | NO (same as flat) |
| Joint-char product | (-1, -1, -1) | non-physical | — | NO |
| S_3 dim | (1, 2, 2) | 2/√6 ≈ 0.816 | 0.3411 | NO (worse than flat) |
| Geometric ε = 0.06 | (1, 0.06, 0.0036) | 0.0036/√6 ≈ 0.0015 | tuneable | YES, but ε not derived |

Only the tuned geometric candidate approaches the observed hierarchy, and its parameter ε is NOT framework-derived — it is equivalent to an observational pin. The charged-lepton bounded package's conclusion (hierarchy requires observational pin) extends to the full fermion mass-spectrum problem.

---

## 4. Comparison to observed mass hierarchies

### 4.1 Observed hierarchies

PDG 2024 values at natural scales (context, not derivation):

```
    Up-type:    m_u = 2.16e-3 GeV, m_c = 1.27 GeV, m_t = 172.69 GeV
                spread  m_t/m_u  =  8.00e4   (~10^5)
    Down-type:  m_d = 4.67e-3 GeV, m_s = 0.0934 GeV, m_b = 4.18 GeV
                spread  m_b/m_d  =  8.95e2   (~10^3)
    Leptons:    m_e = 5.11e-4 GeV, m_μ = 0.1057 GeV, m_τ = 1.777 GeV
                spread  m_τ/m_e  =  3.48e3   (~3500)
```

All three spreads exceed 10^3, with up-type reaching ~10^5.

### 4.2 Scale spread from retained surface

The retained algebra on H_hw=1 is M_3(C) generated by unitary operators (translations, C_{3[111]}, their products). Unitary operators preserve norms; the only way to produce mass scales that differ by factors of 10^3 to 10^5 is through non-unitary content (e.g., propagator resolvents evaluated at specific energies, or EWSB-scale ratios).

**Retained candidate.** The retained shape theorem (charged-lepton review §3) supplies a second-order-return operator with diagonal (w_{O_0}, w_a, w_b). But these three weights are SUPPLIED by the intermediate propagator's values at three distinct Cl(3) states, NOT derived from the retained algebra alone. The values of w_{O_0}, w_a, w_b are free parameters on the retained surface, pinned only by observation.

For the b-quark, the analog weights would be (w_{O_0}^{b}, w_a^{b}, w_b^{b}) on the down-iso channel, similarly free. Without a generation-hierarchy primitive supplying these weights at M_Pl, the predicted hierarchy is flat (Outcome A of the b-Yukawa retention) and empirically falsified.

### 4.3 Quantitative check

If a retained primitive existed producing weights (w_1, w_2, w_3) with ratios matching observation, it would need to produce:

```
    Up channel:    w_u/w_t ~ 10^{-4.9}, w_c/w_t ~ 10^{-2.1}
    Down channel:  w_d/w_b ~ 10^{-2.95}, w_s/w_b ~ 10^{-1.65}
    Lepton channel: w_e/w_τ ~ 10^{-3.54}, w_μ/w_τ ~ 10^{-1.23}
```

These three columns (up, down, lepton) are NOT proportional to each other: the ratios differ significantly across species. A single generation-hierarchy primitive with species-independent weights CANNOT reproduce all three columns simultaneously.

Any retained primitive must therefore be BOTH generation- AND species-dependent. But species-dependence on the Q_L = (2, 3) block is precisely what Block 6 species uniformity FORBIDS. The retained surface is structurally incapable of producing the observed hierarchy through a single Ward-type mechanism.

---

## 5. Retention verdict (Outcome D)

### 5.1 Summary of closures

All four paths close negatively on the retained surface:

1. **Path A (C_{3[111]} cycle)** — the cyclic operator permutes generations, producing either uniform weights (flat) or complex/negative weights (characters), neither of which gives a real positive hierarchy.
2. **Path B (orbit-algebra hierarchy)** — the 3 within 8 = 1 + 1 + 3 + 3 sits at a single S_3 permutation carrier (A_1 ⊕ E); it does NOT carry a 3-level hierarchy.
3. **Path C (hw-grading)** — the three generations sit at a single Hamming weight (hw = 1); hw-grading gives at most 4 levels total, not 3 generation levels with 5-order-of-magnitude spread.
4. **Path D (retained no-go)** — no retained operator on H_hw=1 commuting with C_{3[111]} distinguishes generations; the full retained algebra M_3(C) is cyclic-symmetric.

### 5.2 Retention-gap statement

The retained three-generation structure is generationally **SYMMETRIC** — the three generations X_1, X_2, X_3 are cyclically equivalent under the retained C_{3[111]} operator. The observed generation-resolved mass hierarchy is **ASYMMETRIC** (5 orders of magnitude spread for up-type, 3 orders for down-type, 3.5 orders for lepton). Any bridge between the retained symmetric structure and the observed asymmetric hierarchy requires a primitive that BREAKS the cyclic symmetry.

The current retained surface does not contain such a primitive.

This is a **retained obstruction**, identical in status to the charged-lepton bounded package's observational-pin requirement, now extended across all three species (up, down, lepton).

### 5.3 Named missing primitives (sharply posed, not retained)

If any of the following primitives is retained on a future framework extension, the generation-hierarchy closure would upgrade from observational-pin to sole-axiom for ALL THREE species simultaneously:

**Primitive 1 (C_{3[111]}-breaking retained operator).** A retained operator on H_hw=1 that commutes with translation structure but NOT with C_{3[111]}, and that carries framework-derived generation-dependent diagonal. Such an operator would select a preferred generation (or preferred ordering) from the retained content.

**Primitive 2 (propagator-resolvent primitive at a generation-specific scale).** A retained operator of the form (M_retained − λ I)^{−1} with λ a framework-derived scale (not free parameter), evaluated on H_hw=1 with λ dependent on generation label. This would require both (a) λ a framework-derived scale and (b) a generation-label dependence of λ, neither of which is present on the current retained surface.

**Primitive 3 (spontaneous symmetry breaking of C_3).** A retained mechanism that spontaneously breaks the C_{3[111]} cyclic symmetry down to a subgroup (Z_1 or Z_2), selecting a preferred generation ordering from vacuum-choice dynamics. The three-generation observable theorem explicitly FORBIDS proper quotients of the retained algebra, so any such spontaneous breaking must occur at the Hilbert-space level, not the operator-algebra level.

**Primitive 4 (flavor-column structure on the Higgs).** A retained decomposition of the Higgs singlet H_unit into generation-specific columns H_1, H_2, H_3, each carrying a distinct Clebsch-Gordan weight on the generation label. This would evade Block 6 species uniformity by moving from a single Higgs with uniform CG to a generation-column Higgs structure.

**Primitive 5 (non-Q_L-block Yukawa mechanism).** A retained Yukawa vertex NOT lying on the Q_L block, carrying a generation-label decoration that Block 6 uniformity does not constrain. The current retained Ward theorem derivation works on the full Q_L block; a vertex on a generation-split block (e.g., (2, 3) × (3, 1) with explicit generation indices) would have Clebsch-Gordan structure dependent on generation.

None of these five primitives is present on the current retained surface.

### 5.4 Cross-sector consistency

This result is structurally uniform across all three species:

| Species | Retained obstruction | Observational pin status |
|---|---|---|
| Up-type | generation hierarchy not derived; Block 6 uniformity applies | required, 3 pins (m_u, m_c, m_t) |
| Down-type | generation hierarchy not derived; Block 6 uniformity applies | required, 3 pins (m_d, m_s, m_b) |
| Lepton | generation hierarchy not derived; Block 6 uniformity applies | required, 3 pins (m_e, m_μ, m_τ) — documented in charged-lepton bounded |

Total: 9 observational pins (3 generations × 3 species) required to close the fermion mass matrix on the current retained surface. No sole-axiom prediction is available.

---

## 6. Safe claim boundary

This note claims:

> On the retained `Cl(3)/Z^3` framework, the three-generation observable theorem's irreducible M_3(C) algebra on H_hw=1 is **generationally symmetric** under the retained C_{3[111]} cyclic operator: the three generations X_1, X_2, X_3 are cyclically equivalent. Any retained operator commuting with the full M_3(C) algebra is a scalar multiple of the identity on generations; no retained scalar selector distinguishes one generation from another. Four candidate paths for deriving absolute generation-dependent Yukawa weights at M_Pl from the retained surface (C_{3[111]} cycle, orbit-algebra hierarchy, hw-grading, the retained algebra itself) each close negatively for the same deep structural reason: the retained algebra carries no C_{3[111]}-breaking content. The observed fermion mass hierarchy — 5 orders of magnitude spread for up-type, 3 orders for down-type, 3.5 orders for lepton — cannot be reproduced from the retained surface alone. This is **Outcome D (retained no-go)**, extending the charged-lepton bounded package's observational-pin requirement uniformly across all three species. Closing the hierarchy requires one of five sharply-posed missing primitives (C_{3[111]}-breaking retained operator; propagator-resolvent at framework-derived scale; spontaneous symmetry breaking of C_3; flavor-column Higgs structure; non-Q_L-block Yukawa), none of which is present on the current retained surface.

It does **not** claim:

- any modification of the retained three-generation observable theorem (the M_3(C) algebra on H_hw=1 is inherited as-is);
- any modification of the retained S_3 taste-cube decomposition (C^8 ~= 4 A_1 + 2 E);
- any modification of the retained orbit algebra (8 = 1 + 1 + 3 + 3);
- any modification of the retained Ward identity Block 6 species uniformity;
- any modification of the bottom-Yukawa retention analysis (Outcome A, Yukawa unification empirically falsified);
- any modification of the charged-lepton bounded package (19 runners / 518 PASS inherited as-is);
- any derivation of absolute generation-dependent Yukawa weights from the retained surface;
- that no derivation is conceivable — the five named missing primitives are explicit construction targets for future retention work;
- that the observed hierarchy has no explanation — the 9-pin observational-pin closure supplies the observed masses as comparators; this is not a derivation, it is a bounded accommodation.

### 6.1 Retention gap is explicit

The retention gap is: the absolute generation-dependent Yukawa weights (w_1^{species}, w_2^{species}, w_3^{species}) for species ∈ {up, down, lepton} are NOT derivable from the current retained surface. Nine observational pins are required (3 × 3) to close the fermion mass-spectrum problem. This is a specific, quantifiable gap — not a vague "framework doesn't address hierarchy" statement.

### 6.2 Consistency with charged-lepton bounded

The charged-lepton bounded package (`docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`) documents the observational-pin requirement for leptons with Theorem 7's 3-real pin on (m_e, m_μ, m_τ). This note demonstrates that the SAME structural reasoning applies to quarks, so the observational-pin requirement extends to (m_u, m_c, m_t, m_d, m_s, m_b). The charged-lepton bounded result is therefore a SPECIAL CASE of a uniform retained-surface limit; no quark-specific obstruction beyond the lepton-specific one exists.

### 6.3 Relation to b-Yukawa retention analysis (Outcome A)

The b-Yukawa retention analysis establishes Outcome A: under Block 6 species uniformity (no generation-hierarchy primitive), the Yukawa unification BC at M_Pl is empirically falsified by 33× on m_b. This note (Outcome D) establishes that NO retained generation-hierarchy primitive exists to rescue this BC. The two outcomes are complementary: the b-Yukawa retention identifies the EMPIRICAL FAILURE on the retained surface; the present note identifies the STRUCTURAL CAUSE (retained cyclic symmetry forbids generation-resolved content). Together, they establish the retained-surface limit on the fermion mass hierarchy as **both diagnosed and sharply bounded**.

---

## 7. What is retained vs. cited vs. open

### 7.1 Retained (framework-native, inherited from upstream theorems)

- Three-generation observable theorem's M_3(C) algebra on H_hw=1.
- Orbit algebra 8 = 1 + 1 + 3 + 3 taste decomposition.
- S_3 taste-cube decomposition C^8 ~= 4 A_1 + 2 E.
- Site-phase / cube-shift intertwiner bridge.
- C_{3[111]} cyclic operator on H_hw=1.
- Translation projectors P_1, P_2, P_3 on H_hw=1.
- Ward identity Block 6 species uniformity (6/6 = 1/√6).
- Z_2 mass-matrix 5-real-parameter family.
- The exact cyclic-symmetry argument: any operator commuting with C_{3[111]} has equal diagonal entries in the generation basis.

### 7.2 Cited (external, with controlled systematic)

- Observed fermion mass values (PDG 2024):
  - m_u, m_c, m_t = 2.16e-3, 1.27, 172.69 GeV;
  - m_d, m_s, m_b = 4.67e-3, 0.0934, 4.18 GeV;
  - m_e, m_μ, m_τ = 0.511e-3, 0.1057, 1.777 GeV.

### 7.3 Open

- **Absolute generation-dependent Yukawa weights from the retained surface**: not derivable. Nine observational pins required. A new primitive (one of five named in §5.3) would close this gap; none is currently retained.
- Analogous analyses for neutrino generations (m_ν1, m_ν2, m_ν3 absolute scales, beyond the retained mixing angles) are open and would likely show the same generation-symmetric obstruction on the retained neutrino surface.

---

## 8. Validation

The runner `scripts/frontier_yt_generation_hierarchy_primitive.py` emits deterministic PASS/FAIL lines and is logged under `logs/retained/yt_generation_hierarchy_primitive_2026-04-18.log`. It verifies:

1. Retention of the three-generation observable theorem's M_3(C) on H_hw=1 (translation projectors, C_{3[111]} cycle, matrix units).
2. C_{3[111]} unitarity and order 3.
3. Cyclic-symmetry theorem: any matrix H commuting with the cyclic permutation V satisfies H_{11} = H_{22} = H_{33}.
4. Path A closure: C_{3[111]} characters on (X_1, X_2, X_3) produce uniform or complex weights, not real positive hierarchy.
5. Path B closure: S_3 irrep-dim weights (A_1 = 1, E = 2) produce only 2 distinct values on 3 generations, triply degenerate on individual X_i.
6. Path C closure: all three hw=1 generations sit at single Hamming weight = 1; Wilson mass constant across the triplet.
7. Path D closure (retained no-go): explicit construction of the scalar selector on the retained M_3(C)-invariant content gives only scalar multiples of I_3.
8. Flat candidate (1, 1, 1) gives Yukawa unification BC as in b-Yukawa retention Outcome A (inherited as-is).
9. (1, 2, 2) S_3-dim candidate gives y_b/g_s = 2/√6 ≈ 0.816, WORSE than flat — predicted m_b further from observation.
10. Character (1, -1/2, -1/2) candidate is non-physical (two negative weights).
11. Observed mass spread: up ~10^5, down ~10^3, lepton ~10^{3.5} — all exceed what cyclic-symmetric retained operators can produce (which is factor 1, by cyclic equivalence).
12. Cross-species consistency: 9 observational pins (3 gen × 3 species) required on the retained surface.
13. Consistency with charged-lepton bounded Theorem 7 observational-pin closure (3-pin on the lepton row).
14. No modification of Ward theorem Block 6, three-gen observable theorem, charged-lepton bounded, bottom-Yukawa retention, publication surface.
15. Numerical consistency with retained framework constants.

---

## 9. Status

**RETAINED RETENTION-ANALYSIS NOTE** — Outcome D documented. The retained generation-hierarchy primitive does NOT exist on the current surface. Extension of the charged-lepton bounded observational-pin requirement to the full fermion sector.
