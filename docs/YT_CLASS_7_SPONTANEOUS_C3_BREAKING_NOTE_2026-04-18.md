# YT Class #7 — Spontaneous C_{3[111]} Breaking Retention Analysis Note

**Date:** 2026-04-18
**Status:** framework-native retention analysis of Class #7 (spontaneous
breaking of the retained cyclic C_{3[111]} symmetry on the hw=1 generation
triplet). **Outcome D (retained no-go):** the retained `Cl(3)/Z^3` action
surface contains **no** framework-native composite operator whose vacuum
expectation value (a) carries a non-trivial generation label on H_hw=1 and
(b) can break the retained C_{3[111]} cyclic symmetry. The composite Higgs
`H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` sums over color and weak-isospin
indices with **no generation index in its D9 definition**; its VEV is
structurally generation-scalar and therefore C_{3[111]}-invariant. No other
retained bilinear on the Q_L block carries a generation label with Z² = 6
(D17 uniqueness), so no flavor-Higgs candidate with C_3-breaking VEV exists
on the retained surface. The taste-staircase hierarchy (D3: 2³ = 8 taste
doublers reducing to 1 physical species via α_LM^16) is a mechanism on the
**taste cube** C^8, not on the generation triplet H_hw=1; the two are
structurally independent (C_{3[111]} lives on the hw=1 triplet with
ordinary cyclic action, while the taste staircase compresses hw=0, hw=1,
hw=2, hw=3 sectors in a generation-symmetric manner). The promoted CKM
phase `δ_std = arctan(√5) = 65.905°` traces to the **explicit** Z_3 source
at the electroweak 1+2 split, not to spontaneous breaking of a larger
flavor symmetry. Class #7 therefore closes as a retained no-go,
complementing the Class #6 explicit-breaking no-go
(`YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`, Outcome D).
Together the two notes establish that **neither explicit nor spontaneous
generation-C_3 breaking is available on the current retained surface**; the
C_{3[111]} symmetry is exact both at the Lagrangian level and on every
retained vacuum state.
**Primary runner:** `scripts/frontier_yt_class_7_spontaneous_c3.py`
**Log:** `logs/retained/yt_class_7_spontaneous_c3_2026-04-18.log`

---

## Authority notice

This note is a **retention-analysis note** on the Class #7 candidate
primitive (spontaneous C_{3[111]} breaking) for species differentiation.
It does **not** modify:

- the retained three-generation observable theorem
  (`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`), whose M_3(C)
  algebra on H_hw=1 is inherited as-is;
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), whose D9 composite
  Higgs `phi = (1/N_c) ψ̄_a ψ_a` definition and D17 uniqueness of
  `H_unit` on the Q_L block are inherited without modification;
- the retained hierarchy theorem / observable principle from the axiom
  (`docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`), whose EW scale
  `v = M_Pl · (7/8)^(1/4) · α_LM^16` is inherited as-is;
- the retained strong-CP θ = 0 closure
  (`docs/STRONG_CP_THETA_ZERO_NOTE.md`), whose θ_eff = 0 on the retained
  action surface and the weak-only Z_3 source discipline are inherited
  without modification;
- the promoted CKM atlas/axiom package
  (`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`), whose
  `δ_std = arctan(√5) = 65.905°` phase derivation from the Z_3 source at
  the 1+2 EWSB split is inherited as-is;
- the retained S_3 taste-cube decomposition
  (`docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`), whose
  C^8 ~= 4 A_1 + 2 E decomposition is inherited as-is;
- the retained generation-hierarchy primitive analysis
  (`docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`),
  Class #6 Outcome D (no explicit C_3 breaking on the retained surface);
- the retained H_unit flavor-column decomposition analysis
  (`docs/YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`),
  Class #1 Outcome C (no flavor-column decomposition on the retained
  surface);
- the retained taste-staircase transport
  (`docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`), whose
  per-rung Ward ratio is generation-symmetric at every staircase step;
- any publication-surface file. No publication table is modified.

What this note adds is narrow and decisive: a framework-native decision on
whether the retained surface contains a **spontaneous** breaking mechanism
for the cyclic C_{3[111]} symmetry on H_hw=1. The answer is NO. Together
with the Class #6 explicit-breaking no-go, this closes the **combined**
C_3-breaking primitive question on the current retained surface.

---

## Cross-references

### Foundational retained theorems (directly inherited)

- **Three-generation observable theorem:**
  `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — irreducible M_3(C)
  algebra on H_hw=1, C_{3[111]} cyclic generator.
- **Ward identity D9 (composite Higgs):**
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` D9 — the framework's
  composite Higgs `phi = (1/N_c) ψ̄_a ψ_a` sums over COLOR index only
  (no generation index); extended in D17 to `H_unit = (1/√6) Σ_{α,a}
  ψ̄_{α,a} ψ_{α,a}` summing over color AND weak-isospin, still no
  generation label.
- **Hierarchy theorem:**
  `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` —
  `v = M_Pl · (7/8)^(1/4) · α_LM^16`, electroweak scale via 16 taste
  decouplings.
- **Strong-CP θ = 0 closure:**
  `docs/STRONG_CP_THETA_ZERO_NOTE.md` — θ_eff = 0 on the retained action
  surface; Z_3 source is weak-only, not strong-sector.
- **CKM atlas/axiom package:**
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` — `δ_std = arctan(√5) = 65.905°`
  from Z_3 source phase 2π/3 on the 1+5 projector.

### Context (complementary retention analyses)

- **Class #6 explicit C_3 breaking (no-go):**
  `docs/YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md`
  Outcome D — no retained operator on H_hw=1 breaks C_{3[111]} explicitly;
  the retained algebra is generationally symmetric.
- **Class #1 flavor-column decomposition (no-go):**
  `docs/YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md`
  Outcome C — no flavor-column decomposition of `H_unit` with distinct
  per-species CG weights.
- **Bottom-Yukawa retention analysis:**
  `docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`
  Outcome A — Yukawa unification at M_Pl empirically falsified on m_b.
- **Structural no-go survey (six lepton no-gos):**
  `docs/STRUCTURAL_NO_GO_SURVEY_NOTE.md`.

---

## Abstract (Verdict)

### 0.1 Retention question

The retained Ward-identity theorem implies **species-uniform** Yukawa at
M_Pl (Block 6 species uniformity: every basis CG on the unit-norm (1,1)
singlet equals 1/√6). The bottom-Yukawa retention analysis (Outcome A)
shows this boundary condition is empirically falsified on m_b by 33×. The
Class #6 analysis (explicit C_3 breaking) closed as a retained no-go: no
retained operator on H_hw=1 breaks C_{3[111]} explicitly. Class #7 asks the
complementary question:

> Can the retained C_{3[111]} cyclic symmetry on the generation triplet be
> broken **spontaneously** — preserved at the action level but broken by
> a retained vacuum state — by a framework-native condensate?

### 0.2 Standard SSB criterion

Spontaneous symmetry breaking requires:

1. **Action invariance.** S[ψ, A] is invariant under a group G.
2. **Vacuum non-invariance.** There exists a local composite operator
   `O(x)` such that the vacuum expectation value `⟨O⟩ ≠ 0` and `⟨O⟩` is
   not invariant under G (i.e., `G · ⟨O⟩ ≠ ⟨O⟩`).
3. **Goldstone counting (optional).** In continuous-group SSB, each
   broken generator gives a massless Goldstone; for discrete groups
   (Z_n), no Goldstone modes appear — the SSB is purely structural.

For Class #7, G = C_{3[111]} (a Z_3 cyclic group on H_hw=1), so the
criterion reduces to: **does the retained surface contain a composite
operator O with ⟨O⟩ non-invariant under C_{3[111]}?**

### 0.3 Outcome verdict

**Outcome D (retained no-go).** The retained surface contains NO composite
operator whose VEV can spontaneously break C_{3[111]}. The analysis traces
through five structural paths:

**Path A (H_unit VEV on the generation label).** The D9 composite
`phi = (1/N_c) ψ̄_a ψ_a` and its D17 extension
`H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` sum ONLY over color (N_c = 3)
and weak-isospin (N_iso = 2). **Neither carries a generation index.** The
VEV `⟨H_unit⟩ = v/√2 ≈ 174.15 GeV` is a single complex scalar on the Q_L
block; its action on H_hw=1 is structurally trivial (scalar multiple of
I_3 on generations). **Closed negatively.**

**Path B (generation-triplet bilinear condensate).** Any candidate
⟨ψ̄_i ψ_j⟩ bilinear with generation labels i, j ∈ {1, 2, 3} must respect
D17 uniqueness on the Q_L block — only the (1,1) scalar at Z² = 6 is
retained. All generation-resolved bilinears ⟨X_i X_j⟩ either (a) have
Z² ≠ 6 (excluded by D17 as non-retained composite), or (b) are pure (1,1)
scalars that by Block 6 species uniformity sum symmetrically over all
three generations — giving ⟨X_1⟩ = ⟨X_2⟩ = ⟨X_3⟩ uniformly, which
**preserves** C_{3[111]} rather than breaking it. **Closed negatively.**

**Path C (loop-level tadpole breaking C_3).** A one-loop tadpole for a
C_3-breaking composite requires a bare source term that breaks C_3. The
retained action `S_ret = S_Wilson + ψ̄(D + m)ψ` contains only gauge and
Dirac content; the mass term `m I` is generation-uniform (real scalar
multiple of the identity in the generation basis), commuting with
C_{3[111]}. No C_3-breaking bare source exists, hence no C_3-breaking
tadpole is radiatively generated. Vafa-Witten-like arguments on the
retained determinant positivity (`det(D + m) > 0`, Strong-CP leg A) block
radiative generation of CP-odd operators, and the parallel structural
argument blocks radiative generation of C_3-odd operators: `D + m`
commutes with C_{3[111]}, so `ln det(D + m)` is C_{3[111]}-invariant on
every gauge background, giving a C_{3[111]}-symmetric effective action
after fermion integration. **Closed negatively.**

**Path D (generation-triplet flavor Higgs).** A BSM-style flavor Higgs
scalar `Φ_ij` (an independent field on H_hw=1 × H_hw=1*) would break
C_{3[111]} if its VEV selected a specific generation direction. But D9's
composite-Higgs structural axiom **forbids** independent fundamental
scalar fields on the retained surface: the framework's only scalar is
the composite quark-antiquark bilinear. Adding a generation-triplet Higgs
would require a new axiom (not retained). **Closed negatively —
non-retained.**

**Path E (spontaneous CKM phase breaking).** The promoted CKM phase
δ_std = arctan(√5) = 65.905° traces through the promoted CKM atlas/axiom package
to the **explicit** Z_3 source at the electroweak 1+2 split (CKM atlas
note, §Exact Constants). This is a **discrete explicit** CP source acting
on the mass-basis mixing matrix, not the spontaneous breaking of a larger
continuous flavor symmetry. No retained operator that is Z_3-symmetric at
the action level develops a C_3-asymmetric VEV. The CKM phase is
retained-side explicit, not emergent from vacuum choice. **No hidden
spontaneous breaking; closed negatively.**

### 0.4 Retention verdict (Outcome D)

The retained `Cl(3)/Z^3` surface does NOT contain a spontaneous
C_{3[111]}-breaking mechanism. Combined with the Class #6 explicit no-go
(no operator breaks C_3 explicitly), the **full** primitive question
closes: C_{3[111]} is **exact** on both the Lagrangian and every retained
vacuum state.

### 0.5 Implication for species hierarchy

The Class #7 no-go reinforces the Class #6 no-go and extends the
charged-lepton bounded observational-pin requirement
(3 pins → 9 pins as documented in Class #6). No spontaneous rescue exists
for the Outcome A falsification of Yukawa unification; the observed
5-order-of-magnitude mass spread on up-type quarks cannot be produced by
any retained vacuum mechanism.

### 0.6 Confidence

- HIGH on Path A (H_unit definition D9 is **generation-free** by
  inspection; verified numerically in Block 2 of the runner).
- HIGH on Path B (D17 uniqueness Z² = 6 forces generation-symmetric
  bilinear content; the only retained (1,1) scalar on Q_L is H_unit,
  and Block 6 species uniformity makes its VEV generation-symmetric).
- HIGH on Path C (structural: `D + m` commutes with C_{3[111]} on every
  gauge background, making `det(D + m)` C_{3[111]}-invariant pointwise,
  blocking any radiative tadpole).
- HIGH on Path D (non-retained: adding a flavor Higgs requires a new
  axiom violating D9).
- HIGH on Path E (CKM phase is explicit via the Z_3 source, not
  spontaneous).
- HIGH on Outcome D: all five paths close negatively by independent
  structural arguments anchored in retained theorems.

---

## 1. Retained foundations (inherited)

### 1.1 Retained action surface

From the strong-CP closure note (§Leg C), the retained action class is:

```
    S_ret[U, ψ, ψ̄]  =  S_Wilson[U]  +  ψ̄ (D[U] + m) ψ         (1.1)
```

with Wilson plaquette gauge action and staggered Dirac operator. **There is
no bare Higgs field, no bare Yukawa coupling, and no bare mass splitting
between generations.** The mass term `m I` is diagonal in the generation
basis with equal entries (generation-uniform), consistent with both the
retained three-gen observable theorem (M_3(C) irreducible) and the Ward
identity Block 6 species uniformity.

### 1.2 Retained composite Higgs D9

From `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (D9):

```
    phi(x)  =  (1 / N_c) · Σ_a ψ̄_a(x) ψ_a(x)                   (1.2)
```

summed over color index a ∈ {1, 2, 3}. Extended in D17 to the Q_L block:

```
    H_unit(x)  =  (1 / √(N_c · N_iso)) · Σ_{α,a} ψ̄_{α,a}(x) ψ_{α,a}(x)
              =  (1 / √6) · (ψ̄ψ)_{(1,1)}(x)                    (1.3)
```

summed over weak-isospin α ∈ {up, down} AND color a ∈ {1, 2, 3}. **No
generation index appears** in either (1.2) or (1.3).

### 1.3 EWSB and H_unit VEV

The composite Higgs VEV breaks SU(2)_L spontaneously:

```
    ⟨H_unit⟩  =  v / √2  ≈  174.15 GeV                         (1.4)
```

with `v = M_Pl · (7/8)^(1/4) · α_LM^16 ≈ 246.28 GeV` from the hierarchy
theorem. This is the framework's retained spontaneous SU(2)_L breaking:
the scalar `H_unit` develops a non-zero VEV picking out a specific
direction in SU(2)_L × U(1)_Y space.

### 1.4 Retained three-generation observable theorem on H_hw=1

From `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, the retained
hw=1 triplet T_1 = span{X_1, X_2, X_3} carries an irreducible M_3(C)
algebra generated by three lattice translations and the C_{3[111]}
cyclic operator. The three generations are cyclically equivalent under
C_{3[111]}.

### 1.5 Retained S_3 taste-cube decomposition

From `docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`:

```
    C^8  ~=  4 A_1  +  2 E                                     (1.5)
```

with no sign irrep A_2. The hw=1 and hw=2 triplets each decompose as
A_1 ⊕ E.

### 1.6 Retained Z_3 source (weak-only)

From `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` and
`docs/STRONG_CP_THETA_ZERO_NOTE.md`, the retained Z_3 source acts through
the electroweak 1+2 split and produces the explicit CKM phase:

```
    δ_source  =  2π/3                                         (1.6)
    δ_std  =  arccos(1/√6)  =  arctan(√5)  =  65.905°         (1.7)
```

The Z_3 source is **explicit** at the action level, not spontaneously
generated from vacuum dynamics.

### 1.7 Retained taste staircase (hierarchy mechanism)

From `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` and
`docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`, the EW scale is
compressed 17 decades below M_Pl by 16 successive taste doubler
decouplings:

```
    v / M_Pl  =  (7/8)^(1/4) · α_LM^16                        (1.8)
```

This is a hierarchy mechanism on the **taste cube** C^8 (8 → 1 physical
taste per decoupling step), acting symmetrically on all taste sectors.

---

## 2. Spontaneous C_3 breaking analysis

### 2.1 Standard SSB framework

For a retained symmetry group G acting on the Hilbert space of states, a
symmetry is spontaneously broken if there exists a composite operator
`O(x)` satisfying:

1. **Action invariance.** The retained action S_ret is G-invariant:
   for g ∈ G, `S_ret[g · ψ, g · U] = S_ret[ψ, U]`.
2. **Vacuum non-invariance.** The VEV is non-vanishing and non-invariant:
   `⟨O⟩ ≠ 0` AND `g · ⟨O⟩ ≠ ⟨O⟩` for some g ∈ G.
3. **Linear order parameter.** `O` transforms linearly under G (so that
   `⟨O⟩` is a non-trivial representation vector, not a singlet).

For G = C_{3[111]} = Z_3 acting on the hw=1 triplet H_hw=1, the only way
for `⟨O⟩` to be non-invariant under C_3 is for `O` to carry a **generation
index** i ∈ {1, 2, 3} and for `⟨O_i⟩` to not be cyclically symmetric
under i → i+1 mod 3.

### 2.2 Path A — H_unit VEV check

**Claim.** The composite Higgs VEV ⟨H_unit⟩ is a generation-scalar and
therefore C_{3[111]}-invariant on the retained surface.

**Proof.** From D17 (eq. 1.3 above), H_unit is defined by
```
    H_unit(x)  =  (1/√6) · Σ_{α ∈ {up, down}} Σ_{a ∈ {color}} ψ̄_{α,a}(x) ψ_{α,a}(x)
```
with the sum running over weak-isospin α and color a. The composite
H_unit **has no generation index**; its definition is identical across
all three generations by construction. Consequently, applied to the
hw=1 generation triplet, H_unit acts as a scalar multiple of I_3:
```
    (H_unit)|_{H_hw=1}  =  c · I_3                             (2.1)
```
with a single complex c (independent of generation label). Therefore the
VEV
```
    ⟨H_unit⟩|_{H_hw=1}  =  ⟨c⟩ · I_3  =  (v/√2) · I_3          (2.2)
```
is **generation-scalar** and hence C_{3[111]}-invariant:
```
    C_{3[111]} · ⟨H_unit⟩|_{H_hw=1} · C_{3[111]}^†
      =  C_{3[111]} · (v/√2) · I_3 · C_{3[111]}^†
      =  (v/√2) · I_3  =  ⟨H_unit⟩|_{H_hw=1}                   (2.3)
```

The H_unit VEV breaks SU(2)_L × U(1)_Y spontaneously (the retained EWSB
mechanism), but it does **NOT** break the generation-triplet
C_{3[111]}. **Path A closed negatively.**

### 2.3 Path B — generation-triplet bilinear condensate

**Question.** Is there any retained composite bilinear `⟨O_ij⟩` with
generation indices i, j ∈ {1, 2, 3} that can develop a C_3-asymmetric
VEV?

**Analysis.** The candidate operator would be of the form
```
    O_ij(x)  =  ψ̄_i(x) ψ_j(x)                                 (2.4)
```
where the indices i, j label the three X_1, X_2, X_3 basis states on
H_hw=1. For O_ij to be a **retained** composite, it must lie on the
scalar-singlet composite surface defined by D17. D17 uniqueness enforces
that the only unit-normalized (1,1) scalar composite on Q_L has
Z² = N_c · N_iso = 6; it does NOT include a generation factor in the
normalization. Consequently, the only retained scalar composite containing
ψ̄ψ content is H_unit itself, and H_unit has **no generation index**
(Path A).

If we attempt to define a generation-indexed composite
```
    H_ij(x)  =  (1/√6) · Σ_{α,a} ψ̄_{i,α,a}(x) ψ_{j,α,a}(x)    (2.5)
```
explicitly projecting onto specific generation labels, then:
- for i = j (diagonal), by Block 6 species uniformity on the full Q_L block
  (which extends naturally to Q_L × H_hw=1), all three ⟨H_ii⟩ have
  identical structural weight (symmetric under C_{3[111]} cyclically);
- for i ≠ j (off-diagonal), the composite H_ij mixes different
  translation-character sectors X_i, X_j and by the character-orthogonality
  argument of the structural no-go survey §5.2 (pure-APBC curvature
  K_ij = 0 for i ≠ j via translation-character orthogonality),
  `⟨H_ij⟩ = 0` in the retained vacuum (no off-diagonal condensate).

Both cases therefore satisfy `C_{3[111]} · ⟨H⟩ · C_{3[111]}^† = ⟨H⟩`:
- diagonal ⟨H_ii⟩ = ⟨H_jj⟩ (cyclically symmetric);
- off-diagonal ⟨H_ij⟩ = 0 (vanishing).

The full VEV matrix on H_hw=1 is therefore ⟨H⟩|_{H_hw=1} = c · I_3 with
a single complex c, which is C_{3[111]}-invariant by the cyclic-symmetry
theorem of the Class #6 note.

**Path B closed negatively.**

### 2.4 Path C — loop-level tadpole breaking C_3

**Question.** Even if no tree-level C_3-breaking composite exists, could a
loop-level radiative effect generate a C_3-breaking tadpole?

**Analysis.** A radiative tadpole for a C_3-breaking operator requires at
least one Feynman diagram whose integrand is not C_3-invariant. The
retained action (1.1) contains only:
- Wilson plaquette (gauge kinetic, no fermion dependence);
- staggered Dirac `D + m` (kinetic + uniform mass).

The kinetic term `D + m` is C_{3[111]}-invariant on the hw=1 generation
triplet by the three-generation observable theorem (the translation
projectors P_1, P_2, P_3 and C_{3[111]} generate the full M_3(C) algebra;
the diagonal operator `D + m` restricted to H_hw=1 has equal diagonal
entries on (X_1, X_2, X_3), hence commutes with C_{3[111]}). Explicitly:
```
    (D + m) · C_{3[111]}  =  C_{3[111]} · (D + m)              (2.6)
```
pointwise on every gauge background (mass m is generation-uniform, kinetic
operator is diagonal with equal entries on hw=1 corners of equal Wilson
mass).

The exact fermion effective action from the strong-CP closure (§Leg C) is
```
    Γ_f[U]  =  − Tr ln(D[U] + m)                              (2.7)
```
By (2.6), `ln(D + m)` commutes with C_{3[111]} on every gauge background;
therefore `Γ_f[U]` is a C_{3[111]}-scalar function of U on H_hw=1. The
fermion effective action **cannot generate** any C_{3[111]}-odd operator
at any loop order because the fermion determinant is C_{3[111]}-even.

**Parallel to strong-CP.** The strong-CP closure uses the analogous
argument on CP parity: `det(D + m) > 0` and real, so no CP-odd radiative
effect is generated. The C_3 parallel is: `det(D + m)` is
C_{3[111]}-invariant, so no C_3-odd radiative effect is generated.

**Path C closed negatively.** No radiative tadpole breaks C_{3[111]}.

### 2.5 Path D — generation-triplet flavor Higgs

**Question.** BSM models often introduce a flavor Higgs scalar
`Φ_ij` (i, j ∈ {1, 2, 3}) whose VEV selects a specific generation or
generation-ordering direction, analogously to how ordinary Higgs selects
an SU(2)_L direction. Could the retained surface host such a field?

**Analysis.** The D9 composite-Higgs structural axiom explicitly **forbids**
independent fundamental scalar fields on the retained surface:

> D9: the framework's Higgs is the composite taste condensate
> `phi = (1/N_c) ψ̄_a ψ_a`, NOT an independent fundamental scalar field.

Adding a flavor Higgs Φ_ij would require a new axiom AX3 (or replacing
D9). This is **not retained**. Path D is therefore a non-retained
primitive: it could close Class #7 with a new axiom, but the current
retained surface does not supply it.

**Path D closed as non-retained.** (The note lists it as a candidate
missing primitive, parallel to the Class #6 note's §5.3 Primitive 4.)

### 2.6 Path E — spontaneous CKM phase breaking

**Question.** The promoted CKM phase `δ_std = 65.905°` is a non-trivial
CP-violating phase in the quark mass-basis mixing matrix. In BSM models
with spontaneous CP violation, the CKM phase can arise from a larger
discrete or continuous flavor symmetry broken spontaneously by
flavor-dependent condensates. Does this mechanism operate on the retained
surface?

**Analysis.** From the CKM atlas/axiom package note, the promoted phase
traces through:

```
    source phase  δ_source  =  2π/3                           (from Z_3)
    projector weights        1 + 5                            (on quark block)
    cos²(δ_std)              =  1/6                           (from 1/(1+5))
    δ_std                    =  arccos(1/√6)
                             =  arctan(√5)  =  65.905°        (2.8)
```

The Z_3 source is a **discrete explicit** CP source at the action level,
acting on the quark block's 6-dimensional Hilbert space via the 1+5
projector structure. Key features:

1. **Z_3 symmetry is exact at the action level.** The Z_3 source enters
   the action explicitly; it is not a subgroup of a broken continuous
   flavor symmetry.
2. **Z_3 action is retained.** From the strong-CP closure (§Combined
   Result), the Z_3 eigenvalues are discrete cube roots of unity acting
   on the weak-sector structure; there is no spontaneous dynamical
   generation of this phase from vacuum choice.
3. **No hidden continuous flavor symmetry.** The retained gauge symmetry
   group is SU(3)_C × SU(2)_L × U(1)_Y; no additional continuous flavor
   symmetry is present in the retained action. Consequently, no broken
   continuous flavor symmetry can leave Z_3 as an unbroken discrete
   subgroup via spontaneous breaking.
4. **θ_eff = 0 on the retained surface.** The strong-CP closure explicitly
   shows that the Z_3 source does NOT leak into a strong-sector θ phase;
   it is confined to weak-sector phase structure.

Therefore the promoted CKM phase is **explicit** (from the Z_3 source
built into the action) rather than **emergent** (from spontaneous
breaking of a larger flavor symmetry). There is no hidden spontaneous
breaking mechanism on the retained surface producing δ = arctan(√5).

**Path E closed negatively.**

### 2.7 Path F (addendum) — taste-staircase impact on generation C_3

**Question.** The taste staircase is a retained hierarchy mechanism that
reduces 2³ = 8 taste doublers to 1 physical species over 16 α_LM
decouplings (hierarchy theorem, eq. 1.8). This IS a symmetry reduction
(S_8 taste symmetry → S_1 physical). Does the taste staircase also break
C_{3[111]} on the generation triplet?

**Analysis.** The taste staircase acts on the **taste cube** C^8 (the
Hamming-weight decomposition 1+3+3+1), not on the **generation triplet**
H_hw=1. Key distinctions:

1. **Taste cube ≠ generation triplet.** The three generations sit at
   hw=1 only (retained three-gen observable theorem); the taste staircase
   compresses hw=0, hw=1, hw=2, hw=3 sectors simultaneously and
   symmetrically.
2. **Per-rung Ward ratio is generation-symmetric.** From the P2 taste
   staircase transport note (§Outcome),
   `y_t(μ_k)_lattice / g_s(μ_k)_lattice = 1/√6` **at every rung** k ∈
   {0, ..., 16}, by Block 6 species uniformity applied rung-by-rung. The
   staircase preserves (does not break) Block 6 species uniformity, and
   therefore preserves C_{3[111]} on the generation triplet at every
   rung.
3. **Taste S_3 is not C_{3[111]} on hw=1.** The S_3 axis-permutation
   acts on the full C^8 taste cube (S3_TASTE_CUBE_DECOMPOSITION_NOTE),
   inducing A_1 ⊕ E on each hw=1 and hw=2 triplet. The C_{3[111]}
   cyclic operator on H_hw=1 is the **restriction** of the full
   taste-cube [111]-diagonal cyclic generator to the hw=1 eigenspace;
   it commutes with the taste-staircase decoupling at every rung (the
   decoupling sends 8 → 1 symmetrically across all taste sectors,
   preserving the hw=1 sector's internal C_3 action).
4. **Taste staircase is generation-blind.** The staircase parameter is
   α_LM, defined through Wilson plaquette structure (gauge sector). It
   acts multiplicatively on scales (v/M_Pl = α_LM^16 · constant) with no
   generation-dependent factor.

Therefore the taste staircase preserves C_{3[111]} on the generation
triplet. **Path F closed negatively.**

---

## 3. Per-species implication

Since neither Path A–F breaks C_{3[111]} spontaneously, the retained
surface preserves the full cyclic symmetry on H_hw=1 at both the
Lagrangian and vacuum levels. Consequently:

1. **Yukawa unification BC at M_Pl is NOT rescued by spontaneous C_3
   breaking.** The bottom-Yukawa Outcome A (33× over on m_b) remains
   empirically falsified.
2. **Observational pin count remains 9.** Three species (up, down,
   lepton) × three generations each require an observational pin, as
   established in the Class #6 note (§5.4 cross-sector consistency). No
   spontaneous mechanism reduces the pin count.
3. **Class #7 adds to the combined no-go package.** Together with Class
   #6 (explicit breaking no-go) and Class #1 (flavor-column decomposition
   no-go), the retained surface is now closed against three independent
   candidate primitives for species differentiation. Only Classes #3
   (propagator-resolvent at generation-dependent scale), #5 (non-Q_L
   block Yukawa with generation decoration), and the non-retained
   Class #7D (explicit flavor-Higgs axiom) remain sharply posed as
   missing primitives.

---

## 4. Summary table of paths

| Path | Candidate mechanism | Retained? | Breaks C_3? | Verdict |
|---|---|---|---|---|
| A | ⟨H_unit⟩ generation content | YES (D9 retained) | NO (generation-scalar) | Closed |
| B | ⟨X_i X_j⟩ gen-triplet bilinear | Only H_unit is retained; others fail D17 | NO (diagonal symmetric or off-diagonal zero) | Closed |
| C | Loop tadpole breaking C_3 | Radiative on retained action | NO (`det(D+m)` is C_3-invariant) | Closed |
| D | Flavor Higgs Φ_ij | NOT retained (violates D9) | would break C_3 if retained | Closed as non-retained |
| E | Spontaneous CKM phase | NO (CKM phase is explicit via Z_3 source) | NO (no hidden continuous flavor) | Closed |
| F | Taste-staircase impact on C_3 | YES (hierarchy mechanism retained) | NO (staircase is generation-blind) | Closed |

All six paths close. **Outcome D (retained no-go).**

---

## 5. Retention gap and missing primitives

### 5.1 Combined C_3-breaking closure

The retained surface contains NO mechanism — explicit (Class #6) or
spontaneous (Class #7) — to break the C_{3[111]} cyclic symmetry on the
generation triplet. The retention gap is **symmetric** in both classes:
C_{3[111]} is exact at both the Lagrangian and vacuum levels.

### 5.2 Named missing primitives (sharply posed, not retained)

The Class #6 note named five candidate missing primitives (§5.3 of that
note). The Class #7 analysis updates Primitive 3 to a sharper form:

**Primitive 3 (updated, spontaneous C_3 breaking via new composite).**
A retained mechanism supplying a composite operator `O(x)` on H_hw=1 that
carries a generation label AND satisfies D17-like uniqueness with Z² ≠ 6
(i.e., a new retained scalar composite with generation index). Currently,
D17 excludes all such candidates on the Q_L block; a new uniqueness
theorem on a different retained block (e.g., the hw=2 triplet, or the
joint hw=1 × hw=2 surface) would be required. No such theorem is
retained.

**Primitive 4 (updated, flavor-column Higgs axiom).** Replacing D9 with
an axiom permitting independent fundamental scalar fields on the
generation triplet. This would violate the current composite-Higgs
axiom; it is non-retained and would require a framework extension.

The remaining primitives (#1: C_3-breaking retained operator; #2:
propagator-resolvent at generation-specific scale; #5: non-Q_L block
Yukawa) retain their Class #6 framing.

---

## 6. Safe claim boundary

This note claims:

> On the retained `Cl(3)/Z^3` framework, the retained cyclic C_{3[111]}
> symmetry on the generation triplet H_hw=1 is **exact at both the
> Lagrangian level AND the vacuum level**. The retained composite Higgs
> VEV ⟨H_unit⟩ = v/√2 ≈ 174.15 GeV is a generation-scalar (no generation
> index in the D9/D17 definition, summing only over color and weak-isospin),
> hence C_{3[111]}-invariant on H_hw=1. No retained bilinear composite
> other than H_unit carries (1,1) scalar content on the Q_L block (D17
> uniqueness, Z² = 6), and the only such composite has a generation-symmetric
> VEV by Block 6 species uniformity. Radiative loop effects cannot generate
> a C_3-breaking tadpole because `D + m` commutes with C_{3[111]} on every
> gauge background, making `det(D + m)` pointwise C_3-invariant. Adding an
> independent flavor Higgs would violate D9 (composite-Higgs axiom) and is
> therefore non-retained. The promoted CKM phase δ_std = arctan(√5) = 65.905°
> traces to the **explicit** Z_3 source at the 1+2 EWSB split, not to
> spontaneous breaking of a larger flavor symmetry. The taste staircase
> (16 α_LM decouplings) acts generation-symmetrically at every rung and
> preserves C_{3[111]}. Each of the six structural paths (A: H_unit VEV;
> B: generation-triplet bilinear; C: radiative tadpole; D: flavor Higgs;
> E: spontaneous CKM; F: taste staircase) closes negatively. This is
> **Outcome D (retained no-go)**, complementing the Class #6 explicit
> C_3-breaking no-go and establishing the combined generation-C_3
> primitive question as closed against both explicit and spontaneous
> mechanisms on the current retained surface.

It does **not** claim:

- any modification of the retained three-generation observable theorem
  (the M_3(C) algebra on H_hw=1 is inherited as-is);
- any modification of the retained Ward identity Block 6 species uniformity;
- any modification of the retained composite-Higgs axiom D9 or D17
  uniqueness;
- any modification of the retained strong-CP θ = 0 closure;
- any modification of the promoted CKM atlas/axiom package;
- any modification of the bottom-Yukawa retention analysis (Outcome A,
  Yukawa unification empirically falsified);
- any modification of the Class #1 flavor-column or Class #6 explicit C_3
  breaking no-gos;
- any derivation of absolute generation-dependent Yukawa weights from the
  retained surface;
- that the observed hierarchy has no explanation — the 9-pin observational
  closure continues to supply the observed masses as comparators;
- that no framework extension is conceivable — the named missing
  primitives remain explicit construction targets for future retention
  work.

### 6.1 Retention gap is explicit

The retention gap from Class #7 combines with Class #6 to establish:
**C_{3[111]} is exact on the retained surface.** No explicit or
spontaneous breaking mechanism exists. Any species-hierarchy primitive
must be added via a new axiom (e.g., Primitive 4: flavor-Higgs; or
Primitive 5: non-Q_L-block Yukawa), or via a new retained scalar
composite with generation-dependent Z² (Primitive 3 updated).

### 6.2 Consistency with the strong-CP closure

The strong-CP θ = 0 closure (§Leg A: `det(D+m) > 0`, Leg C: real
effective action) uses **structurally identical** arguments to those
applied here in Path C. The parallel is:
- **Strong-CP:** `det(D + m)` is positive real, so no CP-odd effect
  is radiatively generated.
- **Class #7 Path C:** `det(D + m)` is C_{3[111]}-invariant on
  H_hw=1 (because `D + m` commutes with C_{3[111]}), so no C_3-odd
  effect is radiatively generated.

Both arguments rely on the fact that the retained action does not
contain bare symmetry-breaking content for the symmetry in question.

### 6.3 Class #6 × Class #7 combined closure

The two retention-analysis notes together establish:

- **Class #6 (explicit):** no retained operator on H_hw=1 breaks C_3
  at the Lagrangian level (any retained operator commuting with the
  M_3(C) algebra is a scalar multiple of I_3).
- **Class #7 (spontaneous):** no retained vacuum state breaks C_3 (all
  retained composite VEVs are generation-symmetric or generation-free).

Together, **C_{3[111]} is exact on the retained surface at both levels**.
The combined no-go is symmetric and exhaustive within the current
retained core.

---

## 7. What is retained vs. cited vs. open

### 7.1 Retained (framework-native, inherited from upstream theorems)

- Three-generation observable theorem's M_3(C) algebra on H_hw=1.
- Ward identity D9 composite Higgs + D17 uniqueness + Block 6 species
  uniformity.
- EWSB via ⟨H_unit⟩ = v/√2 (retained SU(2)_L × U(1)_Y breaking).
- Hierarchy theorem `v = M_Pl · (7/8)^(1/4) · α_LM^16`.
- Strong-CP θ = 0 closure (four legs: determinant positivity,
  axial/chiral non-generation, gauge-sector radiative non-generation,
  topological-sector positivity).
- Retained Z_3 source (weak-only, explicit; produces δ_std = arctan(√5)).
- Retained C_{3[111]} cyclic operator on H_hw=1.
- S_3 taste-cube decomposition C^8 ~= 4 A_1 + 2 E.
- Taste-staircase per-rung Ward ratio preservation.
- Retained D + m operator's C_{3[111]}-invariance on H_hw=1.

### 7.2 Cited (external, no role in derivation)

- Observed CKM parameters for consistency comparison (δ = 65.9° ± 3° from
  PDG).
- Observed fermion mass hierarchies as comparators to spread ratios
  (m_t/m_u ~ 10^5, etc., from PDG 2024).

### 7.3 Open

- **Absolute generation-dependent Yukawa weights:** still not derivable.
  Nine observational pins remain required (as established by Class #6);
  Class #7 confirms this is not rescued by spontaneous mechanisms.
- **Primitive 3 (new composite on a different retained block):** open —
  a retained scalar composite with Z² ≠ 6 on a non-Q_L block (e.g., the
  hw=2 triplet or on the full taste cube) could break Block 6 species
  uniformity in a C_3-asymmetric way, but no such composite is currently
  retained.
- **Primitive 4 (flavor-Higgs axiom):** non-retained; would require a
  framework extension beyond D9.

---

## 8. Validation

The runner `scripts/frontier_yt_class_7_spontaneous_c3.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_class_7_spontaneous_c3_2026-04-18.log`. It verifies:

1. H_unit generation symmetry: the retained D9/D17 definition has no
   generation index; its action on H_hw=1 is a scalar multiple of I_3.
2. H_unit VEV invariance under C_{3[111]}: explicit verification that
   C_3 ⟨H_unit⟩ C_3^† = ⟨H_unit⟩ on H_hw=1.
3. Absence of generation-resolved retained composite: no bilinear
   ⟨X_i X_j⟩ (i ≠ j) with Z² = 6 on the retained surface.
4. Off-diagonal bilinear vanishing: `P_i (D + m)^{-1} P_j = 0` for i ≠ j
   on H_hw=1 (translation-character orthogonality, structural no-go
   survey §5.2).
5. `D + m` commutes with C_{3[111]} on H_hw=1: generation-uniform mass +
   translation-invariant kinetic structure.
6. Radiative C_3-invariance: `det(D + m)` is C_3-invariant pointwise on
   gauge backgrounds, blocking radiative tadpole.
7. No independent flavor Higgs on retained surface: D9 structural axiom
   forbids it.
8. Retained CKM phase is explicit (Z_3 source), not spontaneous: verify
   the arctan(√5) value and its origin in the 1+5 projector on the quark
   block.
9. Z_3 source action is exact (cube-root eigenvalues), not from
   spontaneous breaking of a continuous flavor symmetry.
10. Taste staircase per-rung Ward ratio: `y/g_s = 1/√6` generation-
    symmetrically at each of 16 rungs.
11. Taste cube ≠ generation triplet: C^8 decomposition acts on hw=0,
    1, 2, 3 sectors simultaneously; C_{3[111]} restricts to hw=1.
12. Numerical consistency: `v/√2 = 174.15 GeV`, `δ_std = 65.905°`,
    `α_LM^16` hierarchy check.
13. Combined Class #6 × Class #7 closure: C_{3[111]} is exact at both
    Lagrangian and vacuum levels.
14. No modification of upstream retained notes (Ward D9/D17, three-gen
    observable, strong-CP θ = 0, CKM atlas, hierarchy theorem,
    Class #6, Class #1).
15. Outcome D verdict explicit: retained spontaneous C_3 breaking does
    NOT exist on the current surface.

---

## 9. Status

**RETAINED RETENTION-ANALYSIS NOTE** — Outcome D documented. The
retained `Cl(3)/Z^3` framework does NOT contain a spontaneous
C_{3[111]}-breaking mechanism on the generation triplet. Combined with
Class #6 (explicit C_3 breaking no-go), C_{3[111]} is exact at both the
Lagrangian and vacuum levels on the retained surface. The observational-
pin requirement established by Class #6 (9 pins: 3 species × 3
generations) is not reduced by spontaneous mechanisms.
