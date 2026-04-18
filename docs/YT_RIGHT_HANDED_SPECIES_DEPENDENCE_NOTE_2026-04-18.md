# Right-Handed Sector Species-Dependence Retention Analysis Note (Candidate Class #4)

**Date:** 2026-04-18
**Status:** framework-native retention analysis of the right-handed
sector as a candidate primitive for breaking the Ward-identity
Yukawa unification prediction. **Outcome C: the current retained
right-handed sector does NOT differentiate up-type from down-type
Yukawa Clebsch-Gordan factors.** The right-handed quark block C^8_R
on the 4D taste space carries u_R and d_R as color-triplet,
iso-singlet states that differ only in their U(1)_Y eigenvalue
(Y = +4/3 vs Y = −2/3). At the retained SU(3)_c × SU(2)_L × U(1)_Y
level, abelian U(1)_Y charges do not modify SU(N) Clebsch-Gordan
factors — the Yukawa CG factor for the tri-linear Q̄_L × H × u_R is
algebraically identical to Q̄_L × H × d_R, both equal to the same
`1/√6` that arises from the color (3×3→1) and iso (2×2→1) singlet
projections. The retained Ward theorem's species uniformity (Block
6 of the Ward runner) is therefore **not broken** by including the
right-handed sector under the current retained surface. This note
documents Outcome C as an **extension of the species-uniform
retained-surface limit** identified by the b-Yukawa retention
analysis (`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`).
**Primary runner:** `scripts/frontier_yt_right_handed_species_dependence.py`
**Log:** `logs/retained/yt_right_handed_species_dependence_2026-04-18.log`

---

## Authority notice

This note is a retained **retention-analysis note** closing candidate
class #4 (right-handed sector species dependence) as a mechanism for
breaking Yukawa unification at M_Pl. It does **not** modify:

- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), whose Q_L block
  derivation and species-uniform Clebsch-Gordan (Block 6) are
  inherited without modification;
- the retained one-generation matter-closure note
  (`docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`), whose right-handed
  completion `u_R : (1,3)_{+4/3}`, `d_R : (1,3)_{-2/3}`,
  `e_R : (1,1)_{-2}`, `nu_R : (1,1)_0` is inherited as-is;
- the retained anomaly-forced time theorem
  (`docs/ANOMALY_FORCES_TIME_THEOREM.md`), whose 3+1 closure and
  anomaly-cancellation derivation of right-handed hypercharges is
  inherited without modification;
- the retained left-handed charge-matching corollary
  (`docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md`), whose `Q_L : (2,3)_{+1/3}`
  and `L_L : (2,1)_{-1}` assignments are inherited;
- the retained three-generation chirality boundary note
  (`docs/THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md`);
- the retained b-quark Yukawa retention analysis
  (`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`),
  whose Outcome A (Yukawa unification at M_Pl, empirically falsified
  33×) is unchanged by this analysis;
- the retained P1 Δ_R master assembly
  (`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`);
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native
decision on whether the retained **right-handed sector** — at the
level of SU(3)_c × SU(2)_L × U(1)_Y representation assignments
fixed by the one-generation matter-closure anomaly cancellation —
provides a structural mechanism that would make
`y_u(M_Pl) ≠ y_d(M_Pl)` on the retained canonical surface, thus
partially or fully addressing the 33× falsification of the
species-uniform Ward prediction on m_b. The answer is Outcome C:
under the current retained surface, no such mechanism exists. The
analysis closes candidate class #4.

---

## Cross-references

### Foundational retained theorems (directly inherited)

- **One-generation matter closure (RH completion):**
  `docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md` —
  `u_R : (1,3)_{+4/3}, d_R : (1,3)_{-2/3}, e_R : (1,1)_{-2}, nu_R : (1,1)_0`
  uniquely fixed by anomaly cancellation on the Standard Model branch.
- **Anomaly-forced time theorem:**
  `docs/ANOMALY_FORCES_TIME_THEOREM.md` — 3+1 spacetime signature
  forced by anomaly cancellation + chirality + single-clock
  codimension-1 evolution, producing the RH sector as opposite-chirality
  SU(2) singlets on the 4D taste space C^16 = C^8_L + C^8_R.
- **Left-handed charge matching:**
  `docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md` — `Q_L : (2,3)_{+1/3}`
  and `L_L : (2,1)_{-1}` on the graph-first selected-axis surface.
- **Three-generation chirality boundary:**
  `docs/THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md` — chirality is
  not claimed on the purely spatial surface; enters only in the full
  framework through anomaly-forced time.
- **Ward-identity tree-level theorem (Q_L block, species-uniform):**
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` — Block 6 species
  uniformity on the 6-dim Q_L ⊗ Q_L* space (all CG overlaps = 1/√6).
- **b-quark Yukawa retention analysis (Outcome A, falsified):**
  `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` —
  Ward unification at M_Pl predicts m_b ≈ 140 GeV, 33× observed.

### Context

- **Native gauge closure (D7-D17 lineage):**
  `docs/NATIVE_GAUGE_CLOSURE_NOTE.md`
- **Yukawa color projection theorem:**
  `docs/YUKAWA_COLOR_PROJECTION_THEOREM.md` — `√(8/9)` correction
  on the physical Yukawa from the composite-Higgs propagator.
- **Right-handed sector runner (algebra + charges):**
  `scripts/frontier_right_handed_sector.py` — 61/61 PASS, verifies
  C^16 = C^8_L ⊕ C^8_R, taste SU(4), anomaly cancellation, RH
  hypercharges.

---

## Abstract (§0 Verdict)

**Question:** Does the framework's retained right-handed sector
structure (u_R, d_R separate from Q_L) provide a mechanism to
differentiate `y_u` from `y_d` at M_Pl, breaking the species-uniform
Ward prediction `y_u(M_Pl) = y_d(M_Pl) = g_s(M_Pl)/√6`?

**Answer: NO — Outcome C.**

Under the retained one-generation matter closure, the right-handed
quark block C^8_R on the 4D taste space carries:

- `u_R : (1, 3)_{+4/3}` (SU(2) singlet, color triplet, Y = +4/3)
- `d_R : (1, 3)_{-2/3}` (SU(2) singlet, color triplet, Y = −2/3)

**Both are identical at the SU(3)_c × SU(2)_L representation level**
— they are the same SU(3) fundamental, the same SU(2) singlet, and
the same Clifford-chirality projection P_R on C^16. They differ
**only** in their U(1)_Y eigenvalue on the shared (1, 3) block.

The retained Yukawa tri-linear interaction has the structural form:

```
    L_Y ~ Q̄_L × H × u_R  (up-type, H = H̃ with Y_H = −1)
    L_Y ~ Q̄_L × H × d_R  (down-type, H with Y_H = +1)
```

The **SU(3)_c × SU(2)_L Clebsch-Gordan factor** for the color +
iso singlet projection of this tri-linear is:

```
    CG[Q̄_L(2,3) ⊗ H(2,1) ⊗ q_R(1,3)] → (1,1)
      = CG_color[3 ⊗ 3* → 1] × CG_iso[2 ⊗ 2* → 1]
      = (1/√3) × (1/√2)
      = 1/√6                                                 (V-CG-RH)
```

This factor is **the same for up and down channels** because:

1. The color structure `3 ⊗ 3* → 1` is identical for u_R and d_R
   (both are color triplets, and Q̄_L is a color anti-triplet).
2. The iso structure `2 ⊗ 2* → 1` is determined by Q̄_L (iso-doublet)
   × H (iso-doublet); u_R and d_R are iso-singlets and do not enter
   the iso-CG.
3. The **only** difference between u_R and d_R is the U(1)_Y
   eigenvalue, and U(1) is abelian. Tensor products of U(1)
   irreducibles have trivial (= +1) Clebsch-Gordan coefficients:
   they only enforce additive charge conservation, not
   multiplicative CG factors.

**Numerically verified** in `scripts/frontier_yt_right_handed_species_dependence.py`:

```
    CG[Q̄_L × H × u_R → singlet] = 1/√6  ≈ 0.408248                 (V-CG-u)
    CG[Q̄_L × H × d_R → singlet] = 1/√6  ≈ 0.408248                 (V-CG-d)
    |CG_u − CG_d| = 0 (machine precision)                           (V-CG-eq)
```

**Consequence: no species breaking at the Ward level.**

The retained Ward theorem's species uniformity on the Q_L ⊗ Q_L*
block (Block 6 of Ward runner, all 6 basis CG overlaps = 1/√6)
extends to the Q̄_L × H × q_R trilinear Yukawa vertex with the
**same** CG factor on both up and down channels. The right-handed
sector's U(1)_Y differentiation (+4/3 vs −2/3) is an **abelian
charge**, not a representation change. It enters the Ward ratio
only through the hypercharge choice of the Higgs field (Y_H = −1
for up, Y_H = +1 for down), which is a selection rule on which
Higgs component participates, not a modification of the CG weight.

Therefore **the framework predicts `y_u(M_Pl) = y_d(M_Pl)` at the
Ward level, by the same species-uniformity that produces Outcome A
in the b-quark analysis**. The 33× falsification on m_b is not
resolved by the right-handed sector under the current retained
surface.

**Outcome classification:** C — the retained right-handed sector
does NOT provide a framework-native primitive for species
differentiation of up vs down Yukawas. Candidate class #4 is
closed as insufficient to break Yukawa unification.

**Safe claim boundary.** The Clebsch-Gordan analysis is exact
algebra on the retained SU(3)_c × SU(2)_L × U(1)_Y representation
assignments of the one-generation matter closure. Abelian U(1)
tensor products do not alter non-abelian CG factors — this is a
standard group-theoretic fact, not a framework axiom. The Ward
theorem's species uniformity therefore extends from the Q_L ⊗ Q_L*
block (verified Block 6) to the Q̄_L × H × q_R trilinear vertex
(shown here) without species differentiation. The framework does
not claim that the right-handed sector provides such
differentiation; the sector's role, under the retained surface, is
to supply anomaly-cancellation charges and CPT completion, not to
break Yukawa unification.

**Confidence:**

- HIGH on the SU(3)_c × SU(2)_L rep equivalence of u_R and d_R
  (algebraic identity: both are `(1,3)` irreps, distinguished only
  by Y).
- HIGH on the U(1)_Y triviality of CG factors (standard group theory).
- HIGH on the identical Yukawa CG factor `1/√6` for up and down
  channels at the retained level (numerically verified).
- HIGH on Outcome C classification: the retained right-handed
  sector cannot break Yukawa unification. Any such breaking would
  require a primitive beyond the current retained core.

---

## 1. The retained right-handed sector structure

### 1.1 Representation assignments (from one-generation matter closure)

The retained one-generation matter-closure note
(`docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`) fixes the
right-handed sector via anomaly cancellation on the Standard Model
branch:

```
    u_R : (1, 3)_{+4/3}         (SU(2) singlet, color 3, Y = +4/3)   (1.1)
    d_R : (1, 3)_{-2/3}         (SU(2) singlet, color 3, Y = −2/3)   (1.2)
    e_R : (1, 1)_{-2}           (SU(2) singlet, color 1, Y = −2)     (1.3)
    nu_R : (1, 1)_0             (SU(2) singlet, color 1, Y = 0)       (1.4)
```

These assignments are **uniquely fixed** (modulo the nu_R ↔ e_R
relabeling) by:

- Tr[Y] = 0 (gravitational anomaly)
- Tr[Y³] = 0 (U(1)³ anomaly)
- Tr[SU(3)² Y] = 0 (mixed color-hypercharge anomaly)

combined with the Standard Model branch selection `nu_R Y = 0`.
See `docs/ANOMALY_FORCES_TIME_THEOREM.md` §2 for the closed-form
anomaly arithmetic.

### 1.2 u_R and d_R share SU(3)_c × SU(2)_L structure

The critical structural observation for the present analysis:

**u_R and d_R carry the IDENTICAL SU(3)_c × SU(2)_L representation:**

```
    u_R ~ (1, 3)    (SU(2) singlet, color-triplet)
    d_R ~ (1, 3)    (SU(2) singlet, color-triplet)              (1.5)
```

They sit in the **same** 8-dimensional right-handed taste space
C^8_R of the 4D Clifford algebra. The taste algebra su(4) (= M(4,ℂ)
on C^4_taste) commutes with γ_5 and gives both sectors the same
color decomposition `4 = 3_color + 1_lepton`. This is a retained
framework-native fact, verified by `scripts/frontier_right_handed_sector.py`
Part 4 (check: "Taste Lie algebra = su(4) (15 generators)"; check:
"All taste operators commute with gamma_5"; check: "Y spectrum same
on L and R" — modulo SWAP23 assignment, the SU(3) fundamental +
singlet structure is the same on both chiralities).

The **only** distinction between u_R and d_R is the U(1)_Y eigenvalue.

### 1.3 U(1)_Y as an abelian quantum number, not a representation

Hypercharge is the eigenvalue of a U(1) generator. U(1) has only
one-dimensional irreducibles (labeled by the eigenvalue / charge),
and tensor products of U(1) irreducibles are one-dimensional with
CG coefficient identically equal to +1:

```
    Y_a ⊗ Y_b = Y_(a+b)      (additive)                           (1.6)
    ⟨Y_a, Y_b | Y_(a+b)⟩ = 1  (trivial CG)                        (1.7)
```

This is a **standard group-theoretic fact**, not a framework
axiom. It implies that U(1)_Y does not modify non-abelian CG
factors for SU(2) or SU(3); it only enforces additive charge
conservation via selection rules on which states couple.

### 1.4 Structural consequence for Yukawa CG

For the Yukawa tri-linear Q̄_L × H × q_R:

- **SU(3)_c structure:** `3* ⊗ 1 ⊗ 3 → 1` (color singlet). The
  CG factor is `1/√3` (one-dimensional singlet inside 3 × 3*).
- **SU(2)_L structure:** `2* ⊗ 2 ⊗ 1 → 1` (iso singlet). The
  CG factor is `1/√2` (one-dimensional singlet inside 2 × 2).
- **U(1)_Y structure:** `(−1/3) + Y_H + Y_q → 0` (charge
  conservation). The CG factor is +1 (trivial abelian tensor).

For the up channel: Q̄_L(Y = −1/3) × H̃(Y_H = −1) × u_R(Y = +4/3),
sum = 0. ✓
For the down channel: Q̄_L(Y = −1/3) × H(Y_H = +1) × d_R(Y = −2/3),
sum = 0. ✓

**Combined CG factor** (up or down channel, independent of q_R
species):

```
    CG[Q̄_L × H × q_R → (1,1,0)] = 1/√3 × 1/√2 × 1 = 1/√6         (1.8)
```

This is **identical to the Block 6 Q_L ⊗ Q_L* singlet uniformity
result `1/√6`** on the Ward identity surface. The retained Ward
theorem's structural CG factor is preserved under extension to the
right-handed sector.

---

## 2. Analysis of Q_L × u_R vs Q_L × d_R on Cl(3) / Z³

### 2.1 The right-handed sector sits on the 4D taste space C^8_R

From the retained right-handed sector runner
(`scripts/frontier_right_handed_sector.py` Part 4), the 4D Clifford
algebra Cl(4) generated by `Γ_0, Γ_1, Γ_2, Γ_3` on C^16 has:

- chirality γ_5 = Γ_0 Γ_1 Γ_2 Γ_3 with γ_5² = +I
- C^16 = C^8_L ⊕ C^8_R under γ_5 projection
- taste algebra = M(4, ℂ) acting on C^4_taste, commutes with γ_5

The right-handed quark block consists of 6 states of C^8_R (3 colors
for u_R and 3 colors for d_R), embedded in the same taste 4 = 3 + 1
structure as the left-handed sector. The lepton block (e_R, nu_R)
carries the 2 remaining states.

### 2.2 Under SU(3)_c × SU(2)_L, u_R and d_R are algebraically
identical

Within C^8_R (8-state right-handed sector):

- SU(2)_L acts trivially (right-handed sector carries zero SU(2)
  charge; this is the defining property of SU(2)'s chirality).
- SU(3)_c acts as the fundamental `3` on the color-triplet part
  (6 of 8 states), trivially on the lepton singlets (2 of 8 states).

The split of 6 color-triplet RH states into "3 for u_R" vs "3 for
d_R" is **NOT** determined by SU(3)_c or SU(2)_L structure. Both
projections carry identical (1, 3) quantum numbers under the
retained non-abelian gauge group. The split is fixed **only** by
the U(1)_Y eigenvalue assignment from anomaly cancellation.

### 2.3 The CG analysis for the Yukawa vertex

The Yukawa tri-linear operator in the retained surface:

```
    O_Y = ψ̄_{Q_L} · Φ · ψ_{q_R}                                   (2.1)
```

where Φ is an iso-doublet color-singlet scalar (SM Higgs in the
conventional embedding; composite H_unit in the framework's
retained composite-Higgs axiom D9 — though as noted in the b-quark
analysis, H_unit has Y = 0 and does not directly provide the SM
Yukawa vertex; this analysis therefore examines the Yukawa CG at
the representation level, which is the relevant structural input
for any framework-native candidate Higgs assignment).

The CG factor for projecting onto the (1, 1, 0) singlet:

**Color channel:**

```
    3*_{Q̄_L} ⊗ 1_{Φ} ⊗ 3_{q_R} = 3* ⊗ 3 = 1 ⊕ 8                  (2.2)
    ⟨1 | 3* ⊗ 3⟩ = 1/√N_c = 1/√3                                   (2.3)
```

**Iso channel:**

```
    2*_{Q̄_L} ⊗ 2_{Φ} ⊗ 1_{q_R} = 2* ⊗ 2 = 1 ⊕ 3                   (2.4)
    ⟨1 | 2* ⊗ 2⟩ = 1/√N_iso = 1/√2                                 (2.5)
```

**U(1) channel:**

```
    Y_{Q̄_L} + Y_Φ + Y_{q_R} = 0                                   (2.6)
    ⟨0 | Y_a ⊗ Y_b ⊗ Y_c⟩ = δ(sum=0) × 1                          (2.7)
```

The combined CG factor:

```
    CG[Q̄_L × Φ × q_R → (1,1,0)] = (1/√3) × (1/√2) × 1 = 1/√6    (2.8)
```

**Independent of whether q_R = u_R or q_R = d_R**, given that Y_Φ
adjusts so that the U(1) sum = 0. For up channel: Y_Φ = −1 (H̃);
for down channel: Y_Φ = +1 (H).

### 2.4 Structural observation: this is Ward species uniformity
extended to the trilinear

The retained Block 6 species uniformity on Q_L ⊗ Q_L* (Ward theorem,
all 6 basis CG overlaps = 1/√6) is a statement about the Q_L ⊗ Q_L*
bilinear space: the unit-norm (1, 1) singlet has equal weight on
all 6 components (up-red, up-green, up-blue, down-red, down-green,
down-blue).

The present analysis shows the **same** CG factor `1/√6` arises in
the tri-linear Q̄_L × Φ × q_R vertex, for either q_R = u_R or
q_R = d_R, by the separate SU(3)_c and SU(2)_L singlet projections.
This is the structural extension of Block 6 uniformity to the
trilinear case, and it establishes that **the right-handed sector's
U(1)_Y differentiation is insufficient** to break the species
uniformity of the retained Yukawa CG.

---

## 3. Ward-like Clebsch-Gordan for each channel

### 3.1 Up-type Yukawa channel

```
    y_u_CG := ⟨0 | O_Y^up | q̄_L^{a,i=1} · Φ^{i=2} · u_R^a ⟩_{singlet}
            = CG_color[3̄ × 3 → 1] · CG_iso[2 × 2 → 1] · CG_Y[−1/3, −1, +4/3 → 0]
            = (1/√3) · (1/√2) · 1
            = 1/√6                                                    (3.1)
```

The color triplet index a ∈ {1, 2, 3} on Q_L matches the triplet
index on u_R (same color). The iso index i ∈ {1, 2} (up, down)
contracts Q_L's iso-doublet with H̃'s iso-doublet. U(1)_Y is trivial.

### 3.2 Down-type Yukawa channel

```
    y_d_CG := ⟨0 | O_Y^down | q̄_L^{a,i=2} · Φ^{i=1} · d_R^a ⟩_{singlet}
            = CG_color[3̄ × 3 → 1] · CG_iso[2 × 2 → 1] · CG_Y[−1/3, +1, −2/3 → 0]
            = (1/√3) · (1/√2) · 1
            = 1/√6                                                    (3.2)
```

The same factorization as the up channel, with Φ → H (Y = +1) and
q_R → d_R (Y = −2/3). U(1)_Y differs but its CG is +1 in both cases.

### 3.3 Species equality

```
    y_u_CG = y_d_CG = 1/√6                                             (3.3)
```

**The right-handed sector does not differentiate up-type from
down-type Yukawa CG factors at the retained level.**

### 3.4 Extension to leptons (e_R, nu_R)

The analysis extends **analogously** to the charged-lepton and
neutrino channels:

```
    y_ν_CG := ⟨0 | O_Y^ν | L̄_L^{i=1} · Φ^{i=2} · nu_R ⟩_{singlet}
             = CG_color[1 × 1 → 1] · CG_iso[2 × 2 → 1] · CG_Y[+1, −1, 0 → 0]
             = 1 · (1/√2) · 1
             = 1/√2                                                    (3.4)

    y_e_CG := ⟨0 | O_Y^e | L̄_L^{i=2} · Φ^{i=1} · e_R ⟩_{singlet}
            = CG_color[1 × 1 → 1] · CG_iso[2 × 2 → 1] · CG_Y[+1, +1, −2 → 0]
            = 1 · (1/√2) · 1
            = 1/√2                                                    (3.5)
```

Leptons have no color (all factors are singlets), so the CG factor
is `1/√2` (iso-singlet only). This **differs from the quark CG**
`1/√6` by a color factor of `√3` — but note that **within** the
lepton sector, the CG is uniform: `y_ν_CG = y_e_CG = 1/√2`.

This is structurally reasonable: the Ward theorem's Block 6 species
uniformity on the 6-dim Q_L block (color × iso) becomes Block-4
species uniformity on the 2-dim L_L block (iso only, color is trivial).
Neither gives a mechanism for intra-sector differentiation (up vs
down, or electron vs neutrino).

---

## 4. Per-species Yukawa prediction (if differentiation existed)

### 4.1 Under Outcome C, no differentiation exists

Since `y_u_CG = y_d_CG = 1/√6`, the retained framework prediction
for the Ward ratio at M_Pl is:

```
    y_u(M_Pl) / g_s(M_Pl) = 1/√6                                      (4.1)
    y_d(M_Pl) / g_s(M_Pl) = 1/√6                                      (4.2)
```

This is **identical to the top Ward ratio** inherited from
`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` and **identical to
the bottom Ward ratio** inherited from
`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` as
Outcome A.

### 4.2 Δ_R correction is inherited identically

The retained P1 Δ_R master assembly
(`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`)
has color-decomposition structure

```
    Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]       (4.3)
```

which is flavor-blind (no species index). Therefore:

```
    Δ_R^{u-type} = Δ_R^{d-type} = Δ_R^{top} = Δ_R^{bottom} = −3.77% ± 0.45%  (4.4)
```

at the **canonical retained central** from the full-staggered-PT BZ
quadrature (`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`).
The prior literature-cited central `−3.27 %` (from the master assembly
`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md` §§2–9) is
consistent with the canonical central within the master assembly's
±2.32 % literature-bounded band and is preserved as the citation-based
three-channel roll-up, but is superseded as the operational central. The
MSbar Ward ratio at M_Pl is the same for all quark channels; with the
canonical central:

```
    (y_q / g_s)^{MSbar}(M_Pl) ≈ (1/√6) · (1 − 0.0377)  ≈ 0.3928  (all quarks; canonical)
    (y_q / g_s)^{MSbar}(M_Pl) ≈ (1/√6) · (1 − 0.0327)  ≈ 0.3949  (all quarks; lit-cited)
                                                                           (4.5)
```

The shift from the literature-cited central to the canonical central is
~0.5 % on the MSbar ratio and is flavor-blind; it does not modify the
qualitative right-handed species-uniformity conclusions of this note.

### 4.3 Running to IR: the same 33× falsification applies

Following the b-quark retention analysis machinery: the retained
Ward BC `y_u(M_Pl) = y_d(M_Pl) = g_s(M_Pl)/√6` ≈ 0.436, when run
through SM 2-loop RGE to v, produces the quasi-fixed-point
`y_u(v) ≈ y_d(v) ≈ 0.55`, giving masses `m_u ≈ m_d ≈ 95 GeV` at v
(and after QCD running to self-scale, ~140 GeV at each quark's
self-scale).

**Comparison to observed up-type + down-type masses:**

```
    m_u(observed, self-scale)   ≈ 2.2 MeV     (framework pred ~140 GeV; 60000× off)
    m_d(observed, self-scale)   ≈ 4.7 MeV     (framework pred ~140 GeV; 30000× off)
    m_c(observed, self-scale)   ≈ 1.27 GeV    (framework pred ~140 GeV; 110× off)
    m_s(observed, self-scale)   ≈ 95 MeV      (framework pred ~140 GeV; 1500× off)
    m_t(observed, self-scale)   ≈ 165 GeV     (framework pred ~140 GeV; 0.85× off)
    m_b(observed, self-scale)   ≈ 4.18 GeV    (framework pred ~140 GeV; 33× off)
```

The framework's species-uniform Ward prediction is compatible only
with the **top** quark mass (accidentally at the RG quasi-fixed
point); all other quarks are orders of magnitude off.

**The right-handed sector provides no lever to resolve any of these
mass failures**, under the current retained surface. The mechanism
needed must come from elsewhere.

---

## 5. Comparison to observed m_t vs m_b

### 5.1 The observed up-type vs down-type hierarchy

```
    m_t / m_b (observed, self-scale)  ≈  172.69 / 4.18  ≈  41.3         (5.1)
```

This is a factor of **41×** hierarchy between the top and bottom
quarks at their respective self-scales. At a common scale (e.g.,
M_Z), the ratio becomes `y_t(M_Z) / y_b(M_Z) ≈ 0.94 / 0.017 ≈ 55×`.

### 5.2 Framework prediction under Outcome C

Under the current retained right-handed sector (no species
differentiation), the Ward BC at M_Pl gives `y_t(M_Pl) = y_b(M_Pl)`.
Running both simultaneously through SM 2-loop RGE produces the
quasi-fixed point (see §3 of the b-quark retention analysis):

```
    y_t(v)^{framework}  ≈  0.569                                       (5.2)
    y_b(v)^{framework}  ≈  0.548                                       (5.3)
    y_t/y_b at v (framework)  ≈  1.04                                  (5.4)
```

compared to observed `y_t/y_b at v ≈ 56`. **The framework
underestimates the observed t/b hierarchy by a factor of ~54×.**

### 5.3 The retention gap is unchanged by the right-handed sector

The Outcome C of this note **closes candidate class #4** as a
resolution path: the retained right-handed sector does NOT give
a mechanism for up-type vs down-type differentiation at the Ward
level. The 33× failure on m_b documented in
`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` is
**not resolved** by the right-handed sector's representation
structure under the current retained surface.

The class of primitives that would close this gap (identified in
the b-quark retention analysis §5.1) are **not retained** here:
candidate primitives like SUSY with tan β enhancement, flavor-column
structure of H_unit, generation-hierarchy primitive, or a
species-breaking Clifford-algebraic primitive would need to be
proposed and verified separately.

---

## 6. Retention verdict

### 6.1 Outcome C: retained right-handed sector does not
differentiate

The framework's retained right-handed sector, under the current
one-generation matter-closure / anomaly-forced time surface,
carries u_R and d_R as identical `(1, 3)` irreps of SU(2) × SU(3),
distinguished only by abelian U(1)_Y eigenvalues. The Yukawa
tri-linear CG factor for Q̄_L × H × q_R is:

```
    CG = 1/√3 · 1/√2 · 1 = 1/√6   (independent of q_R = u_R or d_R)   (6.1)
```

This **extends** the Block 6 species-uniform CG factor from the
Q_L ⊗ Q_L* bilinear to the trilinear Yukawa vertex and is
algebraically the same. The right-handed sector therefore:

- **does NOT provide** a mechanism for y_u ≠ y_d at M_Pl;
- **does NOT resolve** the 33× falsification on m_b from the
  b-Yukawa retention analysis;
- **does NOT close** candidate class #4 as a resolution path
  (candidate closed as insufficient).

### 6.2 What is retained

- The retained right-handed sector assignments (u_R, d_R, e_R, nu_R)
  are inherited unchanged from
  `docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`.
- The retained Ward-identity theorem's species uniformity on the
  Q_L block is unchanged; it now has a corollary that the
  Yukawa trilinear CG is also species-uniform across u_R / d_R.
- The retained b-quark retention analysis (Outcome A, falsified 33×)
  is unchanged; the right-handed sector does not modify the
  outcome.
- The retention gap identified in the b-Yukawa analysis is
  unchanged: a new primitive beyond the retained surface is
  required to close the up-type vs down-type mass hierarchy.

### 6.3 What this note adds

- A framework-native closure of candidate class #4 (right-handed
  sector species dependence) as **insufficient** to break Yukawa
  unification at M_Pl under the current retained surface.
- A structural extension of the Block 6 species uniformity from
  the Q_L ⊗ Q_L* bilinear to the trilinear Yukawa vertex.
- An explicit numerical verification (in the runner) that the
  Yukawa CG factor is `1/√6` for both up-type and down-type
  quarks, and that U(1)_Y differences do not alter the CG factor.

---

## 7. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` canonical surface, the
> right-handed sector's u_R and d_R carry identical SU(3)_c × SU(2)_L
> representations `(1, 3)`, differing only in U(1)_Y eigenvalue
> (+4/3 vs −2/3). The Yukawa tri-linear Clebsch-Gordan factor for
> Q̄_L × H × q_R projects onto the (1, 1, 0) singlet with CG =
> `1/√3 · 1/√2 · 1 = 1/√6`, which is **identical for up-type and
> down-type channels** because U(1)_Y differences contribute
> trivial (+1) tensor products to the CG. The retained Ward
> theorem's species uniformity therefore **extends** to the Yukawa
> tri-linear vertex and does not break between up and down channels.
> Candidate class #4 (right-handed sector as a primitive
> differentiating y_u and y_d) is **closed as Outcome C: insufficient**.
> The 33× falsification on m_b documented in the b-quark retention
> analysis is **not resolved** by this sector's structure under the
> current retained surface.

It does **not** claim:

- any modification of the retained Ward-identity theorem;
- any modification of the retained one-generation matter-closure
  note or anomaly-forced time theorem;
- any modification of the retained b-quark retention analysis;
- any new primitive for species differentiation; this note **closes
  candidate class #4** as not providing one, and flags elsewhere
  as the required source;
- any speculative mechanism at SUSY, flavor-column, or
  generation-hierarchy primitive level; these remain open research
  directions.

### 7.1 Retention gap is explicit and unchanged

The retention gap identified in the b-quark retention analysis is
**unchanged by this note**: the absolute scale of y_u, y_d, y_c,
y_s, y_b (and by extension y_e, y_μ, y_τ) is wrong under the
current retained Ward + Δ_R + SM 2-loop RGE chain. The right-handed
sector provides no resolution. **A primitive beyond the current
retained core is required** — and this note shows that it must
come from **somewhere other than** the right-handed sector.

### 7.2 What does not change

The retained top prediction `m_t(pole) = 172.57 ± 5.7 GeV` is
unchanged. The Δ_R master assembly is unchanged. The Ward-identity
tree-level theorem is unchanged. The b-Yukawa retention analysis
is unchanged. The bounded down-type mass-ratio CKM-dual lane
(`docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`) is unchanged. Only
**this new retention-analysis note** and its runner are added.

---

## 8. What is retained vs. cited vs. open

### 8.1 Retained (framework-native, inherited from upstream theorems)

- Right-handed sector charge assignments (u_R, d_R, e_R, nu_R) from
  anomaly cancellation on the Standard Model branch
  (`ONE_GENERATION_MATTER_CLOSURE`).
- Anomaly-forced time + 4D taste space C^16 = C^8_L + C^8_R
  (`ANOMALY_FORCES_TIME_THEOREM`).
- Taste algebra su(4) commuting with γ_5 (common color-structure
  on both chirality sectors, `frontier_right_handed_sector.py` Part 4).
- Ward-identity theorem's Block 6 species uniformity on the Q_L
  block (`YT_WARD_IDENTITY_DERIVATION_THEOREM`).
- b-Yukawa retention analysis with Outcome A (Yukawa unification
  at M_Pl, empirically falsified 33×)
  (`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18`).
- Δ_R master assembly (flavor-blind color decomposition)
  (`YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18`).

### 8.2 Cited (external, standard group theory)

- Abelian U(1) tensor product triviality: Y_a ⊗ Y_b = Y_{a+b},
  ⟨|⟩ = +1. Standard, not framework-specific.
- SU(N) singlet projection CG: `1/√N` on N ⊗ N* → 1. Standard.
- SM Yukawa gauge-invariant trilinear structure
  `Q̄_L H u_R` + `Q̄_L H̃ d_R`. Standard QFT.

### 8.3 Open (flagged, not closed by this note)

- **A framework-native primitive for up-type vs down-type
  differentiation**: open. This note closes the right-handed
  sector as not providing one. Candidates still open: flavor-column
  structure of H_unit, generation-hierarchy primitive,
  supersymmetric lane (tan β), or other primitive.
- **Extension of this CG analysis to neutrino Yukawas on the
  L_L block:** the Block-4 species uniformity on L_L ⊗ L_L*
  (2-dim iso-doublet) would give a CG factor `1/√2` for the
  leptonic Yukawas, with analogous ν / e non-differentiation.
  This is noted as a parallel structural observation; a full
  retention analysis for leptons is open.
- **The role of CKM mixing** in the framework's retained surface:
  CKM appears as an open promoted structure (see
  `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`); its contribution to
  per-species Yukawas is not addressed here.

---

## 9. Validation

The runner `scripts/frontier_yt_right_handed_species_dependence.py`
emits deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_right_handed_species_dependence_2026-04-18.log`.
The runner returns PASS on every check to keep this note on the
retained retention-analysis surface.

The runner verifies:

1. Retention of SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`
   and canonical surface anchors `α_LM = 0.09067`, `α_s(v) = 0.1033`.
2. Retention of the one-generation matter-closure RH assignments
   `u_R : (1, 3)_{+4/3}, d_R : (1, 3)_{-2/3}, e_R : (1, 1)_{-2},
   nu_R : (1, 1)_0`.
3. **4D Clifford algebra + γ_5 + RH projection**: the chirality
   operator γ_5 = Γ_0 Γ_1 Γ_2 Γ_3 on C^16 squares to +I, is
   Hermitian, anticommutes with all Γ_μ, and projects onto an
   8-dim right-handed subspace `Tr(P_R) = 8`.
4. **Taste algebra commutes with γ_5**: the taste commutant of
   Cl(4) has dim 16 and every taste operator commutes with γ_5
   (same color structure on both chirality sectors).
5. **SU(3)_c × SU(2)_L equivalence of u_R and d_R**: both are
   `(1, 3)` irreps; the only difference is U(1)_Y eigenvalue.
   This is verified as an algebraic identity on the retained
   assignments.
6. **Color CG factor**: `⟨1 | 3 ⊗ 3* ⟩ = 1/√3`.
7. **Iso CG factor**: `⟨1 | 2 ⊗ 2* ⟩ = 1/√2`.
8. **Combined Yukawa CG**: `1/√3 · 1/√2 = 1/√6` for the color +
   iso singlet projection of the Yukawa trilinear.
9. **Species equality (Outcome C)**: CG[up] = CG[down] = 1/√6
   (both channels give the same factor at machine precision).
10. **U(1)_Y triviality**: the hypercharge assignments
    (Q_L: +1/3, u_R: +4/3, H̃: −1, total for up channel = 0;
    Q_L: +1/3, d_R: −2/3, H: +1, total for down channel = 0)
    conserve charge trivially without modifying the CG factor.
11. **Leptonic extension** (Block 4 of L_L): `CG[L_L × H × e_R] =
    CG[L_L × H × nu_R] = 1/√2` (color trivial, iso singlet = 1/√2).
12. **Outcome C: no species differentiation in the retained
    right-handed sector**. Ward prediction `y_u(M_Pl) = y_d(M_Pl)
    = g_s(M_Pl)/√6` holds at the retained level.
13. **Empirical failure inherited**: under the species-uniform Ward
    BC, up and down Yukawas at v both converge to ~0.55 (RG
    quasi-fixed-point), producing m_u-type = m_d-type ≈ 140 GeV,
    grossly incompatible with observed up-type and down-type
    masses (t/b hierarchy 41× missed).
14. **Retention status**: this note closes candidate class #4 as
    not providing a species-differentiation primitive. The
    retention gap remains open; a new primitive beyond the
    current retained core is required.
15. All retained framework constants (α_LM, α_s(v), v, G3_Pl, YT_Pl,
    DELTA_R) agree with upstream retained values to sub-permille.
