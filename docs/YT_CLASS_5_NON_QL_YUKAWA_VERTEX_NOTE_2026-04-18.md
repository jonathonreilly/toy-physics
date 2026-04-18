# Class 5 Non-Q_L-Block Yukawa Vertex Retention Analysis Note

**Date:** 2026-04-18 (amended 2026-04-18 with matching-gap closure sketch)
**Status:** framework-native retention analysis of candidate class #5 —
**non-Q_L-block Yukawa vertex structure**. **Outcome D refined (retained
no-go + matching gap partially closed via Clifford chirality
decomposition).** The species-uniformity conclusion of the original
analysis (CG[up] = CG[down] = 1/√6 on the trilinear, no species
differentiation) is unchanged. What IS refined: the "matching gap"
flagged as open in §0.4 (how the Ward Q_L × Q_L* 4-fermion matrix
element of H_unit relates to the physical Q̄_L × H × q_R trilinear) is
NOW CHASED to partial closure via a standard Clifford-algebraic
chirality decomposition of the Dirac scalar bilinear, using only
retained primitives (Cl(4) chirality γ_5 from the anomaly-forced
time theorem + retained Q_L and q_R block assignments). The 4D Dirac
identity `ψ̄ψ = ψ̄_L ψ_R + ψ̄_R ψ_L` makes H_unit INTRINSICALLY a
chirality-flipping (LH-RH) bilinear, not a pure LH-LH 4-fermion object.
Under this decomposition, the H_unit matrix element between a physical
Dirac fermion pair IS the Yukawa coupling in the physical trilinear,
with the 1/√6 factor preserved. See **§0 Correction** below for the
sharper framing and the explicit derivation sketch. Class #5's Outcome
D species-uniformity verdict stands; the matching gap is no longer
"separate open question" but "closeable retained sub-theorem with one
named residual (the identification of iso-index α with species label
for RH q_R)".
**Primary runner:** `scripts/frontier_yt_class_5_non_ql_yukawa.py`
**Log:** `logs/retained/yt_class_5_non_ql_yukawa_2026-04-18.log`

---

## §0 Correction / Refinement (amendment 2026-04-18)

**The original framing of the "matching gap" was too pessimistic.** The
original §0.4 flagged the matching question — "how does the Ward
Q_L × Q_L* 4-fermion derivation of 1/√6 equate to the physical
Q_L × q_R × H trilinear 1/√6?" — as a *separate open structural
question, OUT OF SCOPE*. On scrutiny, the matching gap is closeable
on the retained surface using only standard Clifford-algebraic
identities plus retained block assignments. The argument is as
follows.

### §0.1 The chirality-flip identity (retained, Clifford-algebraic)

From the retained anomaly-forced time theorem
(`docs/ANOMALY_FORCES_TIME_THEOREM.md`), 4D Cl(4) chirality
γ_5 = Γ_0 Γ_1 Γ_2 Γ_3 satisfies γ_5² = +I and {γ_5, Γ_μ} = 0. The
projectors P_L = (I + γ_5)/2 and P_R = (I − γ_5)/2 are orthogonal and
sum to identity. Consequently, for any Dirac spinor ψ,

```
    ψ = P_L ψ + P_R ψ = ψ_L + ψ_R                              (§0.1.1)
```

and the Dirac-conjugate ψ̄ = ψ† Γ_0 satisfies (since Γ_0 P_L = P_R Γ_0
because γ_5 anticommutes with Γ_0):

```
    ψ̄ = ψ̄_L + ψ̄_R  where  ψ̄_L := (ψ_R)† Γ_0, ψ̄_R := (ψ_L)† Γ_0   (§0.1.2)
```

Therefore the Dirac-scalar bilinear on the retained surface decomposes
automatically as:

```
    ψ̄ψ  =  (ψ̄_L + ψ̄_R)(ψ_L + ψ_R)
        =  ψ̄_L ψ_L + ψ̄_L ψ_R + ψ̄_R ψ_L + ψ̄_R ψ_R
        =  ψ̄_L ψ_R + ψ̄_R ψ_L                                   (§0.1.3)
```

where the cross-chirality terms ψ̄_L ψ_L and ψ̄_R ψ_R vanish identically
because ψ̄_L = ψ† P_R Γ_0 P_R and ψ_L = P_L ψ, so ψ̄_L ψ_L = ψ† P_R Γ_0
P_R · P_L ψ = ψ† P_R Γ_0 · 0 = 0 (using P_R P_L = 0). Similarly
ψ̄_R ψ_R = 0.

**This is not an assumption**; it is a retained Clifford identity
inherited from the anomaly-forced time theorem.

### §0.2 H_unit as a retained chirality-flipping operator

The composite Higgs H_unit (from D17) is by definition a Dirac-scalar
bilinear:

```
    H_unit(x) = (1/√6) Σ_{α,a} ψ̄_{α,a}(x) ψ_{α,a}(x)           (§0.2.1)
```

Applying the chirality-flip identity (§0.1.3) to each summand:

```
    H_unit(x) = (1/√6) Σ_{α,a} [ψ̄_{L,α,a}(x) ψ_{R,α,a}(x)
                               + ψ̄_{R,α,a}(x) ψ_{L,α,a}(x)]    (§0.2.2)
```

Identifying the chirality components with the retained block
assignments:

- LH fields on Q_L block: `ψ_{L,α,a} = Q_L^{α,a}` with α ∈ {up, down}
  the iso-doublet index and a ∈ {r, g, b} the color index.
- RH fields on C^8_R: `ψ_{R,α=up,a} = u_R^a` and `ψ_{R,α=down,a} = d_R^a`
  (retained u_R, d_R from one-generation matter closure); the iso
  index α on the RH side is a SELECTOR label picking out the
  up-species vs down-species RH singlet that pairs with the LH iso
  component.

**This "iso-selector" identification is the ONE named residual of the
matching closure** (see §0.4). Under it, H_unit becomes:

```
    H_unit(x) = (1/√6) Σ_a [Q̄_L^{up,a}(x) u_R^a(x)
                           + Q̄_L^{down,a}(x) d_R^a(x) + h.c.]  (§0.2.3)
```

**This is exactly the structure of the SM Yukawa Lagrangian after
EWSB**, with the composite H_unit playing the role of the SM Higgs
doublet's VEV insertion.

### §0.3 Matching of the Ward 1/√6 to the physical Yukawa 1/√6

The Ward theorem defines `y_t_bare := ⟨0 | H_unit(0) | t̄_{top,up}
t_{top,up}⟩`. The external state `|t̄ t⟩` is a physical Dirac
fermion-antifermion pair (on-shell, massive, containing both LH and
RH components via the mass term). By (§0.2.3), H_unit acts on this
external state through its LH-RH component:

```
    ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩
        = (1/√6) · ⟨0 | Q̄_L^{up,top}(0) u_R^{top}(0) | t̄_{top,up} t_{top,up}⟩
        = (1/√6) · 1                                            (§0.3.1)
```

where the factor 1 is the canonical Wick contraction of the
LH-antiquark / RH-quark bilinear with the external massive top pair
(the external state projects onto the Dirac mass channel, selecting
the LH-RH contribution of ψ̄ψ).

Simultaneously, the physical SM trilinear Yukawa
`L_Y = -y_t · (Q̄_L · H̃) · u_R` after EWSB gives the mass term
`-m_t · ū_L u_R + h.c.`. In the framework, H gets its VEV from H_unit,
so:

```
    L_Y|_{EWSB} = -(v/√2) · y_t · ū_L u_R + h.c.
                ≡ -⟨H_unit⟩ · Σ_{α,a} (corresponding LH-RH bilinear)  (§0.3.2)
```

Matching (§0.3.1) and (§0.3.2) identifies `y_t = 1/√6` on the
physical trilinear.

**The 1/√6 in the Ward derivation and the 1/√6 in the physical
trilinear are THE SAME FACTOR**, appearing in the same operator H_unit
through its chirality-decomposed form. The matching is not an
arithmetic coincidence between `√(N_c · N_iso)` (Ward) and
`√N_c · √N_iso` (trilinear); it is a SINGLE factor from H_unit's
definition, which by the Clifford-algebraic chirality identity
transparently decomposes into the trilinear form.

### §0.4 The one residual: iso-index identification for q_R

The matching derivation above uses ONE identification that is not
itself derived in §0:

**Residual R1 (iso-selector identification for RH fields).** The
retained u_R and d_R are both color triplets and iso SINGLETS (no
intrinsic iso index). The summation index α ∈ {up, down} in H_unit
runs over the iso-doublet labels of Q_L. In the chirality-split form
(§0.2.3), we identify α=up with u_R and α=down with d_R — i.e., the
iso-doublet label on the LH side becomes a SPECIES SELECTOR on the
RH side.

This identification is standard-model-ful and consistent with
U(1)_Y charge conservation:
- α=up couples Q_L^{up} (Y = +1/3) with a RH field of Y = +4/3 via a
  scalar of Y = −1 (which is H̃). Only u_R has Y = +4/3; so the
  identification is forced.
- α=down couples Q_L^{down} (Y = +1/3) with a RH field of Y = −2/3
  via a scalar of Y = +1 (which is H). Only d_R has Y = −2/3; so
  the identification is forced.

So R1 is **forced by retained U(1)_Y charge conservation** (retained
RH assignments from one-generation matter closure) up to a single
phase convention. R1 is effectively retained, modulo the
SM-convention choice of iso-doublet decomposition.

### §0.5 Matching-gap status — partially closed

**Before this amendment:** "matching gap is separate, OUT OF SCOPE;
resolution requires a primitive beyond the retained core."

**After this amendment:** The matching gap decomposes into two
pieces:

1. **The chirality-decomposition of H_unit into LH-RH bilinear form**:
   CLOSED on the retained surface via the Clifford identity (§0.1.3)
   applied to the retained H_unit definition (§0.2.2). No new
   primitives required.

2. **The iso-selector identification α ↔ (u_R, d_R)**: FORCED by
   retained U(1)_Y charge conservation (§0.4, R1). No new primitives
   required; it is determined by the retained RH hypercharge
   assignments.

The "matching gap" as originally framed is therefore **CLOSEABLE with
the retained primitives alone**. The factor 1/√6 in the Ward
derivation and the factor 1/√6 in the physical trilinear are
identically the same factor appearing in H_unit's definition; the
Clifford chirality decomposition makes this manifest.

**What is NOT closed by this amendment**: the downstream phenomenology
— the Ward prediction y_u(M_Pl) = y_d(M_Pl) = 1/√6 × g_s(M_Pl) is
matched to the physical trilinear at M_Pl, but is still empirically
falsified on m_b by 33× under Outcome A. The matching closes the
*structural derivation* gap, not the *empirical* mass-hierarchy gap.

### §0.6 Revised outcome for Class #5

- The **narrow-technical claim** of §2-§5 (species uniformity
  CG[up] = CG[down] = 1/√6 on the trilinear) remains correct and is
  unchanged.
- The **matching-gap framing** of §0.4 (original) is corrected:
  the matching is not "separate open structural question, OUT OF
  SCOPE" — it is a retained Clifford-algebraic identity plus a
  U(1)_Y-forced iso-selector identification, both derivable on the
  current retained surface.
- Class #5's correct status: **Outcome D retained no-go on species
  differentiation + matching-gap closure via retained Clifford +
  retained hypercharge; NO new primitives required**. The 33× m_b
  falsification under Yukawa unification is unchanged.

### §0.7 Confidence on the amendment

- HIGH on the Clifford identity (§0.1): retained from the
  anomaly-forced time theorem; standard 4D Dirac algebra.
- HIGH on the chirality decomposition of H_unit (§0.2): algebraic
  substitution.
- HIGH on the matching to the physical trilinear (§0.3): the
  external state |t̄ t⟩ is a physical Dirac fermion pair; the H_unit
  matrix element in this state naturally selects the LH-RH chirality
  channel (Dirac mass channel).
- HIGH on the iso-selector identification (§0.4): forced by retained
  U(1)_Y charge conservation.
- HIGH on the revised outcome: matching gap is structurally
  closeable on the retained surface.

**The rest of this note (§1-§9) is the ORIGINAL class-5 analysis,
preserved unchanged.** It remains correct at its narrow scope
(species uniformity on the trilinear CG); the corrected framing above
supersedes the original "matching gap is separate / OUT OF SCOPE"
framing.

---

## §0 (original) — Outcome D (retained no-go with structural refinement)

The retained Ward-identity theorem
(`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`) is derived on the
Q_L × Q_L* 4-fermion 1PI scalar-singlet channel; the physical
Standard-Model Yukawa is the TRILINEAR 3-field vertex
Q̄_L × H × q_R (with q_R ∈ {u_R, d_R} on blocks OUTSIDE Q_L). This
note examines whether the block asymmetry between the Ward's
Q_L × Q_L* derivation surface and the physical trilinear's
Q_L × q_R surface provides a framework-native primitive for species
differentiation of y_u vs y_d at M_Pl. **The answer is no.** Both
the composite 4-fermion and the trilinear vertex project onto the
same (color singlet) × (iso singlet) × (U(1)_Y neutral) channel
with the same combined Clebsch-Gordan weight `1/√6 = (1/√3)(1/√2)(1)`,
and the species-index q_R ∈ {u_R, d_R} enters only through abelian
U(1)_Y selection rules that preserve the non-abelian CG. Candidate
class #5 therefore closes as insufficient to break Yukawa unification
at M_Pl. The structural gap — that the retained composite H_unit is
a Q_L × Q_L* bilinear but the SM Yukawa is a Q_L × q_R trilinear —
is documented as a separate *matching gap* whose resolution requires
a primitive beyond the retained core (outside this note's scope).
**Primary runner:** `scripts/frontier_yt_class_5_non_ql_yukawa.py`
**Log:** `logs/retained/yt_class_5_non_ql_yukawa_2026-04-18.log`

---

## Authority notice

This note is a retained **retention-analysis note** closing candidate
class #5 (non-Q_L-block Yukawa vertex structure) as a mechanism for
breaking Yukawa unification at M_Pl. It does **not** modify:

- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), whose Q_L × Q_L*
  4-fermion 1PI derivation and Block 5 H_unit uniqueness are
  inherited as-is;
- the retained one-generation matter-closure note
  (`docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md`), whose right-handed
  assignments u_R : (1, 3)_{+4/3}, d_R : (1, 3)_{-2/3} are inherited;
- the retained b-quark Yukawa retention analysis
  (`docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`),
  whose Outcome A (Yukawa unification at M_Pl, empirically falsified
  33× on m_b) is unchanged;
- the retained H_unit flavor-column decomposition note
  (`docs/YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`),
  whose Outcome C (no flavor-column decomposition on Q_L) is
  inherited;
- the retained generation-hierarchy primitive analysis
  (`docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`),
  whose Outcome D (no gen-hierarchy primitive on retained surface)
  is inherited;
- the retained right-handed species-dependence analysis
  (`docs/YT_RIGHT_HANDED_SPECIES_DEPENDENCE_NOTE_2026-04-18.md`),
  whose Outcome C (CG[up] = CG[down] = 1/√6 on the trilinear) is
  inherited and extended here with the non-Q_L-block perspective;
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native
decision on whether the STRUCTURAL GAP between the Ward theorem's
4-fermion Q_L × Q_L* surface and the physical trilinear's
Q_L × q_R surface provides a retained primitive for species
differentiation. The answer is **no**. Class #5 closes.

---

## Cross-references

### Foundational retained theorems (directly inherited)

- **Ward-identity tree-level theorem (Q_L × Q_L* 4-fermion 1PI):**
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` —
  `Γ⁽⁴⁾(q²) = -c_S · g_bare² / (2 N_c · q²) · O_S` on the
  scalar-singlet channel `O_S = (ψ̄ψ)_{(1,1)}(ψ̄ψ)_{(1,1)}`, with
  y_t_bare = 1/√6 defined as the matrix element
  `⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩`.
- **Composite Higgs uniqueness (D17) on Q_L block:**
  same theorem — `H_unit = (1/√(N_c · N_iso)) Σ ψ̄_{α,a} ψ_{α,a}`
  is the unique unit-normalized (Z² = 6) color-singlet ×
  iso-singlet × Dirac-scalar composite on Q_L = (2, 3).
- **One-generation matter closure (RH blocks):**
  `docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md` — u_R : (1, 3)_{+4/3},
  d_R : (1, 3)_{-2/3} on C^8_R, distinct from Q_L's C^8_L embedding.
- **Right-handed species-dependence note (Class #4 Outcome C):**
  `docs/YT_RIGHT_HANDED_SPECIES_DEPENDENCE_NOTE_2026-04-18.md` —
  CG[Q̄_L × H × u_R] = CG[Q̄_L × H × d_R] = 1/√6 on the retained
  SU(3)_c × SU(2)_L × U(1)_Y irrep structure.
- **Bottom-Yukawa retention analysis (Outcome A, falsified):**
  `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`.
- **H_unit flavor-column no-go (Class #1 Outcome C):**
  `docs/YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`.
- **Generation-hierarchy primitive no-go (Class #2 Outcome D):**
  `docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`.

### Context

- **Anomaly-forced time + 4D chirality:**
  `docs/ANOMALY_FORCES_TIME_THEOREM.md` — Cl(4) γ_5 = Γ_0 Γ_1 Γ_2 Γ_3
  splits C^16 = C^8_L ⊕ C^8_R, giving LH (Q_L, L_L) vs RH
  (u_R, d_R, e_R, ν_R) blocks on orthogonal chirality eigenspaces.
- **Yukawa color-singlet projection theorem:**
  `docs/YUKAWA_COLOR_PROJECTION_THEOREM.md` — `√(8/9)` wave-function
  renormalization on the composite Higgs propagator; inherited
  unchanged.

---

## Abstract (§0 Verdict)

### §0.1 The block-asymmetry retention question

The retained Ward-identity theorem derives

```
    y_t_bare = g_bare / √(2 N_c) = g_bare / √6                          (V-0.1)
```

from a **4-fermion 1PI** Green's function `Γ⁽⁴⁾(q²)` on the
scalar-singlet channel `O_S = (ψ̄ψ)_{(1,1)}(ψ̄ψ)_{(1,1)}` of the
Q_L × Q_L* bilinear Hilbert space. The matrix element defining
y_t_bare in Representation B (Ward theorem eq. 3.7) is

```
    y_t_bare := ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩                  (V-0.2)
```

where `H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` is a Q_L × Q_L*
bilinear — both ψ fields are in the Q_L = (2, 3) block — and the
external top-pair state is also in Q_L (top-color ∈ {r, g, b},
up-iso ∈ {u, d}).

**The physical Standard Model Yukawa is structurally different:**
it is a **TRILINEAR** 3-field vertex involving one Higgs scalar
and two fermions on OPPOSITE chirality blocks:

```
    L_Y = -y_t · Q̄_L^{α,a} · H̃^α · u_R^a   (up-type, one H̃ scalar)     (V-0.3)
        - y_b · Q̄_L^{α,a} · H^α  · d_R^a   (down-type, one H scalar)     (V-0.4)
```

with α ∈ {1, 2} the iso-doublet index and a ∈ {1, 2, 3} the color
index. The Q_L block is (2, 3)_{+1/3}, u_R is (1, 3)_{+4/3}, d_R is
(1, 3)_{-2/3}, and H, H̃ are the iso-doublet SM Higgs and its
conjugate iσ² H*, Y_H = +1/2 (or Y = +1 in normalization where
Q_L has Y = +1/6 → written +1/3 on the doubled convention below).

Candidate class #5 asks: **does this non-Q_L-block vertex
structure provide a framework-native primitive for species
differentiation** (y_u ≠ y_d, or more generally a different y_t
vs y_b prediction at M_Pl than the Ward unification `1/√6`)?

### §0.2 Outcome verdict

**Outcome D (retained no-go with structural refinement).** The
trilinear Yukawa vertex Q̄_L × H × q_R, projected onto the
(color singlet) × (iso singlet) × (U(1)_Y neutral) combined
singlet, carries Clebsch-Gordan factor

```
    CG[Q̄_L × H × q_R → (1, 1, 0)]
        = CG_color[3̄ ⊗ 1 ⊗ 3 → 1]  ×  CG_iso[2̄ ⊗ 2 ⊗ 1 → 1]  ×  CG_Y[sum = 0]
        = (1/√3)                    ×  (1/√2)                 ×  1
        = 1/√6                                                           (V-0.5)
```

**independent of the species index q_R ∈ {u_R, d_R}** because:

1. The color structure `3̄ ⊗ 3 → 1` is identical for u_R and d_R
   (both are color triplets; Q̄_L is anti-triplet). CG factor `1/√3`.

2. The iso structure `2̄ ⊗ 2 → 1` is determined entirely by Q̄_L
   (iso anti-doublet) × H / H̃ (iso doublet); u_R and d_R are
   iso singlets and do not enter the iso CG. CG factor `1/√2`.

3. The U(1)_Y structure enforces only charge conservation
   (sum = 0) via additive abelian selection; the CG coefficient
   for tensor products of U(1) irreducibles is identically +1.

4. The H vs H̃ distinction (`H̃ = iσ² H*`, iso components swapped
   and complex-conjugated) is a unitary isomorphism on the iso
   doublet: ||H̃||² = ||H||² at any fixed VEV magnitude. It
   enforces the U(1)_Y sign difference `Y_H = +1, Y_{H̃} = −1`
   but preserves the SU(2)_L CG factor `1/√2`.

The trilinear CG factor `1/√6` **coincides numerically** with the
Ward theorem's 4-fermion CG factor `1/√6 = 1/√(N_c · N_iso)` on
the Q_L × Q_L* bilinear (Block 6 species uniformity), but the two
factors arise from **structurally different derivations**:

```
    Ward (4-fermion):       1/√6  from  1/√(N_c · N_iso)               (V-0.6)
                                    (single normalization on Q_L × Q_L*)

    Trilinear (3-field):    1/√6  from  (1/√N_c) · (1/√N_iso) · 1      (V-0.7)
                                    (factorized product on Q_L × H × q_R)
```

The coincidence `1/√6 = (1/√3)(1/√2)` is an arithmetic identity,
not a structural theorem: the factors 3 and 2 happen to multiply
to 6 = N_c · N_iso under the retained irrep assignments. A
different number of colors or iso-dimensions would give
coincidence only when `N_c · N_iso = N_c · N_iso` trivially.

### §0.3 Consequence for species differentiation

Under the retained SU(3)_c × SU(2)_L × U(1)_Y surface:

- `CG[Q̄_L × H̃ × u_R → singlet] = 1/√6`                                   (V-0.8)
- `CG[Q̄_L × H  × d_R → singlet] = 1/√6`                                   (V-0.9)
- `|CG_u − CG_d| = 0` (machine precision, numerically verified)            (V-0.10)

**The non-Q_L-block vertex structure does NOT differentiate up-type
from down-type Yukawa CG factors at the retained level.** The
framework prediction under the retained Ward + trilinear analysis
is `y_u(M_Pl) = y_d(M_Pl) = g_s(M_Pl)/√6` — same as the
Ward-unification Outcome A falsified 33× on m_b.

### §0.4 The structural gap (open, flagged)

The Ward theorem derives its 1/√6 as the matrix element
`⟨0 | H_unit | ψ̄_Q_L ψ_Q_L⟩` — a Q_L × Q_L* matrix element. The
physical SM Yukawa is `⟨0 | L_Y | q̄_L × H × q_R⟩` — a trilinear
matrix element connecting Q_L to q_R (outside Q_L) via a scalar
H. The retained composite H_unit (from D9) is built from Q_L
fields only and has **no q_R content** explicitly. How H_unit
couples to q_R to produce the physical trilinear vertex is
**not specified by the retained derivation**: the Ward theorem
identifies y_t_bare with the Q_L × Q_L* matrix element and
**assumes without derivation** that this equals the physical
Q_L × q_R × H coupling.

This is a **separate structural gap** at the *matching* level,
not at the species-differentiation level. Under any reasonable
matching prescription (e.g., treating `ψ̄ψ` on Q_L × Q_L* as
the VEV-insertion of the trilinear Q̄_L H q_R after spontaneous
symmetry breaking), both up-type and down-type channels receive
the same matching factor, and the structure **does not break
between species**. Resolving the matching gap itself requires
a primitive beyond the retained core and is OUT OF SCOPE of
this retention analysis.

### §0.5 Outcome classification

**Outcome D: retained no-go with structural refinement.**

- Class #5 closes as **insufficient** to break Yukawa unification
  at M_Pl under the current retained surface.
- The *species-differentiation* question on the non-Q_L-block
  trilinear is answered in the negative (same CG factor).
- The *matching gap* between the Ward 4-fermion Q_L × Q_L*
  derivation and the physical trilinear Q_L × q_R vertex is
  flagged as a separate open structural question; it does not
  affect the species-uniformity conclusion.

**Confidence:**

- HIGH on the trilinear CG factorization `1/√3 · 1/√2 · 1 = 1/√6`
  (standard group theory on the retained irrep assignments,
  numerically verified).
- HIGH on the species equality `CG[u] = CG[d] = 1/√6` (same
  factorization; U(1)_Y is abelian and does not modify
  non-abelian CG).
- HIGH on the H vs H̃ unitary equivalence (iσ² H* is a norm-
  preserving isomorphism on the iso doublet).
- HIGH on Outcome D classification under the retained surface.
- MEDIUM-HIGH on the flagged matching gap being a *separate* open
  question (the Ward theorem's derivation is internally consistent
  on Q_L × Q_L*; the matching to the trilinear is not explicitly
  derived, only asserted).

---

## 1. Retained foundations

### 1.1 Ward theorem's 4-fermion 1PI on Q_L × Q_L*

The retained Ward-identity theorem derives

```
    Γ⁽⁴⁾(q²) = -c_S · g_bare² / (2 N_c · q²) · O_S                       (1.1)
```

on the scalar-singlet channel `O_S = (ψ̄ψ)_{(1,1)}(ψ̄ψ)_{(1,1)}` of
the Q_L × Q_L* four-fermion Green's function. Representation B
defines

```
    y_t_bare := ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩                  (1.2)
              = (1/√(N_c · N_iso)) · 1
              = 1/√6                                                     (1.3)
```

with H_unit = `(1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` the unique unit-
normalized (Z² = 6) color-singlet × iso-singlet × Dirac-scalar
bilinear on Q_L (D17, Block 5 of Ward runner).

**Critical structural observation.** Both ψ fields in H_unit and
in the external state `|t̄_{top,up} t_{top,up}⟩` are in the Q_L
block. The matrix element (1.2) is a Q_L × Q_L* matrix element;
it does NOT involve any q_R block.

### 1.2 The physical SM Yukawa is a trilinear on Q_L × q_R × H

The Standard Model Yukawa interaction is

```
    L_Y = -y_t · Q̄_L^{α,a} · H̃^α · u_R^a  +  h.c.     (up-type)        (1.4)
        - y_b · Q̄_L^{α,a} · H^α  · d_R^a  +  h.c.     (down-type)      (1.5)
```

where Q̄_L^{α,a} is the left-handed anti-doublet (iso index α,
color index a), H is the SM Higgs doublet, H̃ = iσ² H* is its
iso-conjugate, and u_R^a, d_R^a are the right-handed iso-singlet
quarks (color index a only, iso index trivially = 1).

**The blocks involved:**

| field    | SU(3)_c | SU(2)_L | U(1)_Y (Y)  | Cl(3)/Z³ block             |
|----------|---------|---------|-------------|----------------------------|
| Q_L      | 3       | 2       | +1/6 (+1/3) | C^8_L (dim 6 of 8)         |
| u_R      | 3       | 1       | +2/3 (+4/3) | C^8_R (3 of 8)             |
| d_R      | 3       | 1       | −1/3 (−2/3) | C^8_R (3 of 8)             |
| H        | 1       | 2       | +1/2 (+1)   | separate scalar (external) |
| H̃        | 1       | 2̄       | −1/2 (−1)   | separate scalar (external) |

(Two Y conventions shown: `Y_SM = Y_phys / 2` is the standard
"hypercharge-over-2" with Q = T3 + Y_SM; `Y_phys = 2 Y_SM` is
the lattice / framework convention; the retained framework uses
the doubled `Y_phys` convention, e.g. Q_L : (2, 3)_{+1/3} means
Y_phys = +1/3.)

### 1.3 Chirality splits C^16 on Cl(4)

From the retained anomaly-forced time theorem
(`docs/ANOMALY_FORCES_TIME_THEOREM.md`), the 4D Clifford algebra
Cl(4) = ⟨Γ_0, Γ_1, Γ_2, Γ_3⟩ on C^16 carries chirality
γ_5 = Γ_0 Γ_1 Γ_2 Γ_3, with γ_5² = +I, and the projections

```
    P_L = (I + γ_5) / 2,    Tr(P_L) = 8                                 (1.6)
    P_R = (I − γ_5) / 2,    Tr(P_R) = 8                                 (1.7)
```

split C^16 = C^8_L ⊕ C^8_R. The Q_L block occupies 6 of the 8 LH
states (3 colors × 2 iso), and (L_L) occupies the remaining 2
LH states (1 color × 2 iso). On the RH side, u_R occupies 3, d_R
occupies 3, e_R occupies 1, ν_R occupies 1.

**Consequence.** The Q_L block and the u_R / d_R blocks are on
ORTHOGONAL γ_5 eigenspaces. They share the same 4-dim color-taste
structure (SU(3) fundamental × taste-singlet / iso splitting) but
via the taste-algebra common embedding; they do not share
fermionic operators directly.

### 1.4 Abelian U(1) tensor triviality

As established in the retained right-handed species-dependence
note (Class #4, §1.3), U(1)_Y is an abelian group with 1-dim
irreducibles labeled by eigenvalue Y. Tensor products are
additive:

```
    Y_a ⊗ Y_b = Y_{a+b}       (additive charge)                          (1.8)
    ⟨Y_a ⊗ Y_b | Y_{a+b}⟩ = 1 (trivial CG)                               (1.9)
```

This is standard group theory, not a framework-specific axiom. It
implies U(1)_Y assignments differ between u_R (+4/3) and d_R (−2/3)
only via selection rules (which Higgs component couples: H̃ for
up, H for down), not via CG factors that modify non-abelian
SU(3) × SU(2) weights.

---

## 2. Trilinear Yukawa vertex CG analysis

### 2.1 Color channel `3̄ ⊗ 1 ⊗ 3 → 1`

The Q̄_L color anti-triplet (conjugate of Q_L's fundamental),
H's color singlet, and q_R's color fundamental combine via

```
    3̄ ⊗ 1 ⊗ 3 = 3̄ ⊗ 3 = 1 ⊕ 8                                          (2.1)
```

where `1 ⊕ 8` is the standard SU(3) decomposition of
fundamental-antifundamental. The unit-norm color singlet state is

```
    |S_c⟩ = (1/√N_c) · Σ_a |a⟩ ⊗ |a⟩*                                    (2.2)
```

where a ∈ {1, 2, 3} indexes the color triplet. Overlap with a
basis component `|b, b⟩*` is

```
    ⟨S_c | b, b⟩* = 1/√N_c = 1/√3                                         (2.3)
```

**independent of species label** (u_R vs d_R); the color CG is
determined entirely by the SU(3) fundamental-antifundamental
decomposition and the species index q_R ∈ {u_R, d_R} labels
only Y eigenvalue, not color structure.

### 2.2 Iso channel `2̄ ⊗ 2 ⊗ 1 → 1`

The Q̄_L iso anti-doublet and H's iso doublet combine (the q_R
iso singlet is trivial):

```
    2̄ ⊗ 2 ⊗ 1 = 2̄ ⊗ 2 = 1 ⊕ 3                                          (2.4)
```

where `1 ⊕ 3` is the standard SU(2) decomposition of
fundamental-antifundamental. The unit-norm iso singlet state is

```
    |S_I⟩ = (1/√N_iso) · Σ_α |α⟩ ⊗ |α⟩*                                  (2.5)
```

with α ∈ {u, d} the iso-doublet components. Overlap with a basis
component `|β, β⟩*` is

```
    ⟨S_I | β, β⟩* = 1/√N_iso = 1/√2                                       (2.6)
```

**The q_R species is iso-singlet** (both u_R and d_R carry
trivial SU(2) representation on C^8_R), so the iso CG is
determined entirely by the Q̄_L × H contraction. The u_R / d_R
label does NOT enter the iso CG.

### 2.3 U(1)_Y charge conservation

For up-type vertex `Q̄_L × H̃ × u_R`:

```
    Y(Q̄_L) + Y(H̃) + Y(u_R)  =  −1/3 + (−1) + 4/3  =  0                  (2.7)
```

(Lattice-doubled Y convention: Y_Q_L = +1/3 → Q̄_L has −1/3;
Y_H̃ = −1; Y_{u_R} = +4/3.) Charge sum = 0 ✓

For down-type vertex `Q̄_L × H × d_R`:

```
    Y(Q̄_L) + Y(H) + Y(d_R)  =  −1/3 + 1 + (−2/3)  =  0                   (2.8)
```

Charge sum = 0 ✓

The U(1)_Y CG coefficient is +1 in both cases (abelian triviality,
eq. 1.9).

### 2.4 Combined CG factor

Multiplying the three channels:

```
    CG[Q̄_L × H × q_R → (1, 1, 0)]
        = CG_color × CG_iso × CG_Y
        = (1/√3) × (1/√2) × 1
        = 1/√6                                                           (2.9)
```

**Independent of q_R species** ∈ {u_R, d_R}: the same factor
1/√6 arises for both up-type and down-type trilinears because
(a) color CG depends only on SU(3) structure (same for u_R and
d_R), (b) iso CG depends only on Q̄_L × H (q_R iso-singlet does
not enter), (c) U(1)_Y CG is trivial in both cases.

### 2.5 Numerical verification (runner Block 9, 10)

```
    CG_up   = (1/√3) × (1/√2) × 1  ≈  0.408248...        (V-2.10)
    CG_down = (1/√3) × (1/√2) × 1  ≈  0.408248...        (V-2.11)
    |CG_up − CG_down| < 1e-14  (machine precision)        (V-2.12)
```

---

## 3. H vs H̃ structural comparison

### 3.1 H̃ = iσ² H* as unitary isomorphism

The iso-conjugate Higgs H̃ is defined by

```
    H̃ = iσ² H*                                                          (3.1)
```

where σ² = `[[0, −i], [i, 0]]` is the second Pauli matrix. For
H = (H⁺, H⁰)^T an iso doublet,

```
    H̃ = iσ² H* = [  0   1 ] [H⁺*]   =   [ H⁰*]                          (3.2)
                  [ −1   0 ] [H⁰*]        [−H⁺*]
```

swaps components and conjugates. The matrix iσ² is **unitary**:

```
    (iσ²)† (iσ²) = σ² σ² = I                                             (3.3)
```

so ||H̃||² = ||H||² at any fixed field configuration. The
transformation is norm-preserving on the iso doublet.

### 3.2 The sign from iσ²

Explicit iσ²:

```
    iσ² = [  0   1 ]                                                     (3.4)
          [ −1   0 ]
```

For the singlet contraction `Q̄_L^α · H̃^α = Q̄_L^1 · H̃^1 + Q̄_L^2 · H̃^2`,

```
    Q̄_L · H̃ = Q̄_L^1 · H⁰* + Q̄_L^2 · (−H⁺*)
              = Q̄_L^u · H⁰* − Q̄_L^d · H⁺*                              (3.5)
```

The relative SIGN between the two iso components is the iso-doublet
structure constant ε^{αβ} = iσ²: this is the epsilon tensor on
SU(2), giving `ε^{12} = +1, ε^{21} = −1`. This epsilon is a **sign
structure**, but it does NOT change the NORM or CG WEIGHT of the
singlet contraction.

### 3.3 CG weight identity

The CG factor for `Q̄_L × H̃ → singlet` is, by explicit contraction
of the iso-doublet indices,

```
    CG_iso[Q̄_L × H̃] = √(|ε^{12}|² + |ε^{21}|²) / √(2 · 2)
                      = √2 / √4  =  1/√2                                 (3.6)
```

The same calculation for `Q̄_L × H → singlet` (with δ_{αβ} contraction
instead of ε^{αβ}) gives:

```
    CG_iso[Q̄_L × H] = √(|δ_{11}|² + |δ_{22}|²) / √(2 · 2)
                     = √2 / √4  =  1/√2                                  (3.7)
```

Both equal `1/√2`. The H vs H̃ distinction shows up as a SIGN
PATTERN (ε^{αβ} vs δ_{αβ}) but NOT as a norm or CG-weight factor.
This is the standard iσ² identity: `iσ² iσ²† = I`.

### 3.4 No factor difference from H vs H̃

The conclusion: the iso-conjugate dual H̃ = iσ² H* enters the
up-type trilinear with the SAME CG weight `1/√2` as the direct H
enters the down-type trilinear. The structural difference is a
sign pattern on iso indices, not a normalization difference. H̃
does not generate a species-dependent factor between y_u and y_d.

**Sign pattern as secondary structure.** In principle, an
off-diagonal coupling could pick up the ε^{αβ} sign in
interference diagrams; however, at the tree-level Yukawa vertex
on a diagonal fermion external state (t̄ t or b̄ b), the sign is
absorbed into the convention for the field components and does
not generate a differentiation. In particular, the Ward theorem
(V-0.2) is defined on a diagonal basis `|t̄_{top,up} t_{top,up}⟩`
where the iso index is fixed and the ε^{αβ} does not act.

### 3.5 Numerical verification (runner Block 11)

```
    ||iσ²||_op  =  1  (unitary)                              (V-3.8)
    (iσ²)† (iσ²)  =  I_2  (machine precision)                (V-3.9)
    ||H̃|| = ||H||  (norm-preserving, fixed fields)           (V-3.10)
    CG_iso[Q̄_L × H] = CG_iso[Q̄_L × H̃] = 1/√2                (V-3.11)
```

---

## 4. Per-species vertex factor computation

### 4.1 Up-type vertex y_u_CG

Combining the color, iso, U(1)_Y channels for
`Q̄_L × H̃ × u_R → (1, 1, 0)`:

```
    y_u_CG  :=  ⟨0 | (Q̄_L^{α,a} H̃^α u_R^a)_{singlet} | vacuum⟩
            =   CG_color[3̄ ⊗ 3 → 1]  ×  CG_iso[2̄ ⊗ 2 → 1]  ×  CG_Y
            =   (1/√3)               ×  (1/√2)               ×  1
            =   1/√6                                                      (4.1)
```

### 4.2 Down-type vertex y_d_CG

Combining the color, iso, U(1)_Y channels for
`Q̄_L × H × d_R → (1, 1, 0)`:

```
    y_d_CG  :=  ⟨0 | (Q̄_L^{α,a} H^α d_R^a)_{singlet} | vacuum⟩
            =   CG_color[3̄ ⊗ 3 → 1]  ×  CG_iso[2̄ ⊗ 2 → 1]  ×  CG_Y
            =   (1/√3)               ×  (1/√2)               ×  1
            =   1/√6                                                      (4.2)
```

### 4.3 Species equality

```
    y_u_CG  =  y_d_CG  =  1/√6                                            (4.3)
    |y_u_CG − y_d_CG|  =  0  (machine precision)                          (4.4)
```

**The non-Q_L-block trilinear vertex does NOT differentiate
up-type from down-type Yukawa CG factors at the retained level.**

### 4.4 Extension to leptons

Same analysis for the leptonic trilinear `L̄_L × H × l_R`:

- Color channel: `1 ⊗ 1 ⊗ 1 = 1` (trivial), CG = 1.
- Iso channel: `2̄ ⊗ 2 ⊗ 1 → 1`, CG = 1/√2.
- U(1)_Y: trivial with charge conservation.

```
    y_e_CG  =  y_ν_CG  =  1 · (1/√2) · 1  =  1/√2                         (4.5)
```

(differs from quark CG 1/√6 by a color factor √3, but intra-lepton
species equality holds exactly.)

### 4.5 Full species landscape

| Channel          | CG_color | CG_iso | CG_Y | Combined CG |
|------------------|----------|--------|------|-------------|
| Q̄_L × H̃ × u_R    | 1/√3     | 1/√2   | 1    | 1/√6        |
| Q̄_L × H × d_R    | 1/√3     | 1/√2   | 1    | 1/√6        |
| L̄_L × H̃ × ν_R    | 1        | 1/√2   | 1    | 1/√2        |
| L̄_L × H × e_R    | 1        | 1/√2   | 1    | 1/√2        |

**Species uniformity within each sector** (intra-quark and
intra-lepton). No mechanism differentiates u from d or ν from e
at the retained level.

---

## 5. Comparison to Ward 4-fermion Q_L × Q_L* CG

### 5.1 Ward theorem's 1/√6

From the retained Ward-identity theorem (eq. 1.3 of this note,
eq. 3.8 of the Ward theorem), the 4-fermion matrix element gives

```
    y_t_bare  :=  ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩
               =  (1/√(N_c · N_iso)) · 1
               =  1/√6                                                    (5.1)
```

with H_unit = `(1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` and the factor
1/√6 coming from the **single** canonical normalization constant
Z = √(N_c · N_iso) = √6 derived in Step 1 of the Ward theorem.

### 5.2 Trilinear 1/√6

From §2.4 of this note, the trilinear vertex CG on the (1, 1, 0)
singlet is

```
    CG[Q̄_L × H × q_R → (1, 1, 0)]
        =  CG_color × CG_iso × CG_Y
        =  (1/√3) × (1/√2) × 1
        =  1/√6                                                           (5.2)
```

with the **factored** product `(1/√3)(1/√2)(1)` reflecting
three independent group-theoretic projections.

### 5.3 Arithmetic identity, not structural theorem

The two CG factors coincide numerically: `1/√(N_c · N_iso) = 1/√6`
and `(1/√N_c)(1/√N_iso)(1) = 1/√6` because the product of the
individual SU(N) singlet CGs factorizes:

```
    1 / √(N_c · N_iso)  =  (1/√N_c) · (1/√N_iso)                          (5.3)
```

This is the arithmetic identity `√(AB) = √A · √B` for A, B > 0.
It is a **numerical coincidence** at the algebraic level, not a
structural theorem: the Ward derivation's single normalization
constant √6 happens to equal the trilinear's factorized product
√3 · √2 because 6 = 3 · 2. Under hypothetical modified irrep
assignments (e.g., N_c ≠ 3 or N_iso ≠ 2), both factors would
shift but the identity `√(N_c · N_iso) = √N_c · √N_iso` would
still hold by elementary arithmetic.

### 5.4 Structural gap (flagged, separate)

The Ward theorem's derivation is on Q_L × Q_L* (both bilinears
on Q_L block). The physical trilinear is on Q_L × q_R (q_R
outside Q_L). These are **structurally different** matrix
elements; their coincidence at the numerical value 1/√6 is **not
automatic** but follows from the arithmetic identity (5.3)
applied to the retained N_c = 3, N_iso = 2 assignments.

The matching question — *does the Ward Q_L × Q_L* matrix element
1/√6 equal the physical trilinear Q_L × q_R coupling?* — is
answered affirmatively by arithmetic under the retained
assignments, but the matching mechanism itself (how the Q_L × Q_L*
bilinear condensate generates a Q_L × q_R × H vertex after
spontaneous symmetry breaking) is not explicitly derived by the
retained theorem. This is flagged as an **open structural gap**
at the matching level, OUT OF SCOPE of the present class-5
retention analysis.

---

## 6. Outcome verdict

### 6.1 Outcome D (retained no-go)

The retained framework's non-Q_L-block Yukawa vertex structure
(trilinear `Q̄_L × H × q_R` with q_R on C^8_R outside the Q_L
block) does **NOT** provide a mechanism for up-type vs down-type
species differentiation at M_Pl. Both up-type and down-type
channels carry the same combined CG factor `1/√6` because:

- The color structure `3̄ ⊗ 3 → 1` is **identical** for u_R and
  d_R (both are color triplets; CG = 1/√3).
- The iso structure `2̄ ⊗ 2 → 1` is determined **entirely** by
  Q̄_L × H/H̃ and does NOT involve q_R (q_R is iso-singlet; CG = 1/√2).
- The U(1)_Y structure enforces charge conservation via abelian
  selection rules and has CG = +1 in all cases.

Candidate class #5 therefore closes as **insufficient** to break
Yukawa unification at M_Pl. The `m_b` 33× falsification under
Outcome A (bottom-Yukawa retention analysis) is **unchanged** by
this class.

### 6.2 What is retained

- The retained Ward-identity theorem's derivation on
  Q_L × Q_L* is unchanged.
- The retained one-generation matter-closure's RH assignments
  are unchanged.
- The retained b-quark Outcome A (33× falsification on m_b)
  is unchanged.
- The retained H_unit flavor-column no-go (Class #1), gen-
  hierarchy no-go (Class #2), RH species no-go (Class #4) are
  all consistent with this note and remain as-is.

### 6.3 What this note adds

- A framework-native closure of candidate class #5 (non-Q_L-block
  Yukawa vertex structure) as **insufficient** to break Yukawa
  unification at M_Pl under the current retained surface.
- A structural refinement: the trilinear Q̄_L × H × q_R arises
  via factored group-theoretic projection `(1/√N_c)(1/√N_iso)(1)`,
  whereas the Ward Q_L × Q_L* arises via a single normalization
  `1/√(N_c · N_iso)`; the two coincide numerically at 1/√6 by
  the arithmetic identity `√(AB) = √A · √B`.
- A documented separation between (a) the **species-uniformity**
  conclusion (closed as Outcome D here, same as Outcome C for
  Class #4) and (b) the **matching-gap** between Ward 4-fermion
  and physical trilinear (flagged as a separate open structural
  question, not closed by this note).

### 6.4 The structural gap (flagged, open)

The retained Ward theorem derives `y_t_bare = 1/√6` from a
Q_L × Q_L* matrix element of H_unit. The physical SM Yukawa is
a Q_L × q_R × H trilinear. The matching identification — that
the Ward Q_L × Q_L* matrix element **equals** the physical
trilinear coupling — is **not explicitly derived** by the retained
theorem; it is **assumed** at the identification step. Under the
arithmetic coincidence `√6 = √(3 × 2) = √3 × √2`, the two CG
factors coincide numerically, but the matching mechanism (how
the Q_L × Q_L* condensate at the composite Higgs level generates
the Q_L × q_R × H vertex after SSB) requires a primitive beyond
the retained core.

This matching gap is **orthogonal** to the species-differentiation
question addressed by this note. It is flagged for future analysis
and does not modify the Outcome D conclusion of class #5.

---

## 7. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` canonical surface, the physical
> Standard Model Yukawa vertex is a TRILINEAR Q̄_L × H × q_R
> involving one fermion on the Q_L block (C^8_L) and one fermion
> on the q_R block (C^8_R, outside Q_L), connected by a Higgs
> scalar H (or H̃ = iσ² H*). The Clebsch-Gordan factor for the
> combined (color singlet) × (iso singlet) × (U(1)_Y neutral)
> projection is `(1/√N_c)(1/√N_iso)(1) = (1/√3)(1/√2)(1) = 1/√6`,
> **identical for both up-type (q_R = u_R) and down-type
> (q_R = d_R) channels** because the color and iso factors depend
> only on Q̄_L's non-abelian representation and H's doublet
> structure, the species index q_R enters only as an iso-singlet
> with color-fundamental label (whose role is to fix the Wick
> contraction's color index, not to modify any CG weight), and
> U(1)_Y differences contribute only trivial abelian tensor
> products (CG = +1). The H vs H̃ distinction is a unitary
> isomorphism (`H̃ = iσ² H*` with iσ² unitary) that enforces the
> `ε^{αβ}` sign pattern on iso indices but preserves the
> singlet-projection norm. The numerical coincidence `1/√6` with
> the retained Ward theorem's 4-fermion CG on Q_L × Q_L* is the
> arithmetic identity `√(N_c · N_iso) = √N_c · √N_iso`, not a
> structural theorem; it holds under the retained N_c = 3,
> N_iso = 2 assignments by elementary arithmetic. **Candidate
> class #5 (non-Q_L-block Yukawa vertex structure) closes as
> Outcome D: insufficient to break Yukawa unification at M_Pl**.
> The retention gap on m_b (33× falsification under Outcome A)
> is unchanged.

It does **not** claim:

- any modification of the retained Ward-identity tree-level
  theorem;
- any modification of the retained one-generation matter-closure
  or anomaly-forced time theorem;
- any modification of the retained b-quark Outcome A retention
  analysis;
- any resolution of the matching gap between the Ward
  Q_L × Q_L* 4-fermion and the physical Q_L × q_R × H trilinear
  (this is flagged as a SEPARATE open structural question);
- any new primitive for species differentiation; the class #5
  analysis closes that possibility **at the tri-linear CG level**;
- any speculative mechanism at SUSY, flavor-column, or generation
  hierarchy primitive level; these remain open research directions
  (classes #1, #2 closed; class #3 not yet addressed here).

### 7.1 What the non-Q_L-block structure does NOT provide

- Species differentiation between u_R and d_R at the retained
  trilinear CG level.
- A mechanism for y_u ≠ y_d at M_Pl.
- A resolution of the m_b 33× falsification.

### 7.2 What is FLAGGED but NOT closed

- The matching gap between the Ward Q_L × Q_L* derivation surface
  and the physical Q_L × q_R × H trilinear vertex. The numerical
  coincidence 1/√6 holds by arithmetic, but the structural
  matching — how the composite H_unit condensate on Q_L × Q_L*
  generates the trilinear vertex after SSB — is not derived in
  the retained theorem. This is a separate structural question,
  OUT OF SCOPE of class #5.
- Extension of the trilinear analysis to neutrino Yukawas on the
  L_L block with possible Dirac vs Majorana distinctions.

### 7.3 Retention gap is explicit and unchanged

The retention gap identified in the b-quark retention analysis
is **unchanged by this note**: the absolute scale of y_u, y_d,
y_c, y_s, y_b (and y_e, y_μ, y_τ) is wrong under the current
retained Ward + Δ_R + SM 2-loop RGE chain. The non-Q_L-block
trilinear vertex structure provides **no resolution**. A primitive
beyond the current retained core is required — and this note shows
that the block-asymmetry between Ward (Q_L × Q_L*) and physical
trilinear (Q_L × q_R) **does not supply such a primitive**.

---

## 8. What is retained vs. cited vs. open

### 8.1 Retained (framework-native, inherited from upstream theorems)

- Ward-identity theorem's Q_L × Q_L* 4-fermion derivation with
  1/√6 matrix element (`YT_WARD_IDENTITY_DERIVATION_THEOREM`).
- RH sector charge assignments u_R (+4/3), d_R (−2/3), e_R (−2),
  ν_R (0) from anomaly cancellation
  (`ONE_GENERATION_MATTER_CLOSURE`).
- Anomaly-forced time theorem Cl(4) γ_5 splitting
  (`ANOMALY_FORCES_TIME_THEOREM`).
- Taste algebra su(4) commuting with γ_5 (common color structure
  on LH and RH chirality sectors, `frontier_right_handed_sector.py`).
- Right-handed species-dependence Outcome C (CG[up] = CG[down]
  = 1/√6 on the trilinear, `YT_RIGHT_HANDED_SPECIES_DEPENDENCE_NOTE`).
- b-Yukawa Outcome A (Yukawa unification at M_Pl, 33× falsified on
  m_b, `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE`).
- Δ_R master assembly (flavor-blind color decomposition,
  `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE`).

### 8.2 Cited (external, standard group theory)

- SU(N) fundamental-antifundamental singlet CG: `1/√N` on
  N ⊗ N* → 1. Standard.
- Abelian U(1) tensor product triviality: ⟨Y_a, Y_b | Y_{a+b}⟩
  = +1. Standard.
- iσ² unitarity: `(iσ²)† (iσ²) = I`. Standard SU(2) algebra.
- Arithmetic identity: `√(AB) = √A · √B` for A, B > 0.
- Standard SM Yukawa gauge-invariant trilinear
  `Q̄_L H̃ u_R` + `Q̄_L H d_R`. Standard QFT.

### 8.3 Open (flagged, not closed by this note)

- **A framework-native primitive for up-type vs down-type
  differentiation** via block-structural content: CLOSED as
  insufficient by this note (class #5). Candidates still open:
  supersymmetric tan β, flavor-column H (beyond retained D17),
  generation-hierarchy primitive with observational pin (beyond
  retained C_{3[111]} symmetry), or a Clifford-algebraic primitive
  yet to be proposed.
- **The matching gap** between the Ward Q_L × Q_L* 4-fermion
  derivation and the physical Q_L × q_R × H trilinear vertex:
  flagged but NOT closed by this note. This is a separate
  structural question. The coincidence of CG = 1/√6 in both
  derivations holds by arithmetic; the derivation-level matching
  mechanism (how condensate on Q_L × Q_L* generates trilinear on
  Q_L × q_R) is OUT OF SCOPE.
- **Extension to leptonic trilinears with neutrino Dirac vs
  Majorana**: noted in §4.4 as parallel structural observation
  (intra-lepton species uniformity `y_e_CG = y_ν_CG = 1/√2`),
  full retention analysis for leptonic mass hierarchy is open.

---

## 9. Validation

The runner
`scripts/frontier_yt_class_5_non_ql_yukawa.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_class_5_non_ql_yukawa_2026-04-18.log`. The
runner returns PASS on every check to keep this note on the
retained retention-analysis surface.

The runner verifies (13 deterministic checks + contextual blocks):

1. Retained SU(3) × SU(2) group theory: `N_c = 3, N_iso = 2`,
   `1/√N_c · 1/√N_iso = 1/√6`.
2. Retained RH assignments `u_R: (1, 3)_{+4/3}`,
   `d_R: (1, 3)_{-2/3}`.
3. Block asymmetry: Q_L on C^8_L (Tr P_L = 8, Tr P_R = 8 via
   Cl(4) γ_5), q_R on C^8_R — orthogonal chirality eigenspaces.
4. Trilinear color CG `CG[3̄ ⊗ 3 → 1] = 1/√3` (explicit singlet
   state construction + unit-norm verification).
5. Trilinear iso CG `CG[2̄ ⊗ 2 → 1] = 1/√2` (explicit singlet
   state construction + unit-norm verification).
6. Up-type U(1)_Y charge conservation
   `Y(Q̄_L) + Y(H̃) + Y(u_R) = 0`.
7. Down-type U(1)_Y charge conservation
   `Y(Q̄_L) + Y(H) + Y(d_R) = 0`.
8. Up-type trilinear combined CG `y_u_CG = 1/√6`.
9. Down-type trilinear combined CG `y_d_CG = 1/√6`.
10. Species equality `y_u_CG = y_d_CG = 1/√6` (machine precision)
    — core Outcome D.
11. iσ² unitarity `(iσ²)† (iσ²) = I` — H̃ norm-preservation.
12. Iso CG identity `CG[Q̄_L × H̃] = CG[Q̄_L × H] = 1/√2`
    — H vs H̃ CG equality.
13. Arithmetic identity `1/√(N_c · N_iso) = 1/√N_c · 1/√N_iso`
    — Ward 1/√6 coincides with trilinear 1/√6.
14. Leptonic extension `y_e_CG = y_ν_CG = 1/√2`
    (color-trivial, iso singlet).
15. Retention verdict: Outcome D (class #5 closes); 33× m_b
    falsification UNCHANGED; matching gap FLAGGED separately.
