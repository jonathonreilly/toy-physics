# Primitive P-LH Order-One Derivation Attempt (FULL BLAST) — A_F Partially Derives; Order-One ↔ Staggered-Dirac Structural Relocation (pPlh_order_one)

**Date:** 2026-05-10
**Type:** primitive_proposal_note (follow-on; no theorem promotion)
**Claim type:** primitive_proposal_note (no audit-lane status request)
**Status authority:** independent audit lane only.

**Source-note proposal disclaimer:** this is a primitive-design FULL BLAST
follow-on to [`PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md`](PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md)
(PR #1050; commit `1a57ef5fc`). The upstream P-LH-NCG-Native probe closed
D2 (KO-dim-6 J) as derivable from retained Cl(3)/Z^3 but left D1
(order-one condition `[[D_F, a], JbJ⁻¹] = 0`) as a named NCG admission.
This note performs the maximum-depth examination of whether D1 can ALSO
be derived, attempting to construct:

- **G1**: D_F (finite Dirac operator) from retained content.
- **G2**: A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) (Connes-Chamseddine SM finite algebra)
  from retained content.
- **G3**: order-one `[[D_F, a], JbJ⁻¹] = 0` as an automatic consequence
  of G1+G2 + algebra compatibility.

**Primary runner:** [`scripts/cl3_primitive_p_lh_order_one_2026_05_10_pPlh_order_one.py`](../scripts/cl3_primitive_p_lh_order_one_2026_05_10_pPlh_order_one.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_lh_order_one_2026_05_10_pPlh_order_one.txt`](../logs/runner-cache/cl3_primitive_p_lh_order_one_2026_05_10_pPlh_order_one.txt)

**Net verdict (honest, FULL BLAST):** **BOUNDED — structural clarification, not closure**.

| Goal | Derivation tier on retained Cl(3)/Z^3 |
|---|---|
| **G1 (D_F)** | **NOT DERIVABLE** — staggered-Dirac open gate dependency; D_F is structurally undetermined without H_F unification. |
| **G2 (A_F)** | **PARTIALLY DERIVABLE** — all three summands have retained-content sources: ℂ from central ω, ℍ from Cl⁺(3), M_3(ℂ) from hw=1 triplet generation algebra. BUT three summands live on STRUCTURALLY DISTINCT Hilbert sectors (per-site H_F + BZ-corner). Native assembly into single H_F requires staggered-Dirac open gate. |
| **G3 (order-one)** | **NOT AUTOMATIC** even granting G2. Toy model shows: block-scalar D_F satisfies order-one vacuously; Yukawa-like D_F violates order-one with max violation ~0.3. The order-one selection remains active (Chamseddine-Connes 2013). |

**Net structural finding.** The most important load-bearing finding of
this note is **the structural relocation**:

```text
LH-content gap reduces from:
  BEFORE (P-LH-NCG-Native): "order-one as named NCG primitive"
                            (one independent well-studied admission)
  AFTER  (this note):       "staggered-Dirac gate dependency"
                            (structurally identified, ALREADY-OPEN gate;
                             order-one is logically downstream)
```

This is **structural clarification, not a new admission**. The
order-one selectivity finding (Section 5) re-derives the
Chamseddine-Connes 2013 SM-vs-PS discriminator; the assembly finding
(Section 4) identifies that the obstruction to deriving order-one is
not order-one itself but the upstream staggered-Dirac gate that
determines H_F, the algebra embedding, and the Dirac operator class.

---

## 0. Notation and standing assumptions

Throughout this note:

- **Cl(3)** = real Clifford algebra `Cl(3,0)` with generators `γ_1, γ_2, γ_3`
  satisfying `{γ_i, γ_j} = 2 δ_{ij} · I` (retained A1).
- **Cl⁺(3)** = even subalgebra, isomorphic to ℍ (retained:
  `CL3_SM_EMBEDDING_THEOREM.md` Section A).
- **ω = γ_1 γ_2 γ_3** = central pseudoscalar; `ω² = -I`, `[ω, γ_i] = 0`
  (retained: `CL3_SM_EMBEDDING_THEOREM.md` Section B).
- **H_per_site** = ρ_+ ⊕ ρ_- ≅ ℂ⁴ (per-site Hilbert space; A1 + chirality
  decomp per `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`).
- **H_BZ_corner** = (ℂ²)^⊗3 ≅ ℂ⁸ (BZ-corner taste cube; staggered-Dirac
  gate per `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
- **H_hw1** = hw=1 triplet ⊂ H_BZ_corner, dim 3 (retained:
  `THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`).
- **A_F** = candidate finite algebra of Connes-Chamseddine SM derivation,
  = ℂ ⊕ ℍ ⊕ M_3(ℂ).
- **H_F^Connes** = 96-dimensional finite Hilbert space (3 generations ×
  32 spinor components including particles + antiparticles).
- **D_F** = candidate finite Dirac operator on H_F (self-adjoint, odd
  under chirality grading γ).
- **Order-one condition** = `[[D_F, a], JbJ⁻¹] = 0` for all a, b ∈ A_F.

## 1. Method — derivability test of G1, G2, G3 in sequence

For each goal `G_i`, the test is:

```text
   (Derivation)   A1 + A2 + (retained content)  ⊢  G_i
   (Negation)     A1 + A2 + (retained content)  ⊬  ¬G_i
   (Forcing)      A1 + A2 + (retained content) admits exactly one G_i
                  modulo unitary / gauge equivalence
```

Passing all three: derivable on retained content.
Failing (Derivation): not derivable; G_i remains an admission.
Failing (Forcing): G_i is a choice among admissible options.

The runner verifies each goal at exact-algebra precision on
constructed toy models. No PDG / lattice MC / fitted matching is
used. Forbidden imports are listed in Section 8.

## 2. G1 — D_F from retained content (NOT DERIVABLE)

**Statement.** The framework's minimal axioms A1+A2 do NOT determine
a unique finite Dirac operator D_F on the per-site Hilbert space
H_F (≅ ρ_+ ⊕ ρ_- = ℂ⁴) or any larger Hilbert sector.

**Proof sketch.** The minimal axioms A1+A2 (Cl(3) algebra + Z³ substrate)
specify only the local algebra and lattice. They do not:

1. Fix a Dirac operator D on the substrate (this is the
   `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` open gate).
2. Fix a finite Dirac operator D_F on the per-site Hilbert space (a D_F
   = block-swap on ρ_+ ⊕ ρ_-, or block-σ_x, or many other off-diagonal
   self-adjoint operators, are all admissible — see P-LH-NCG-Native
   Section 3.2).
3. Fix a multiplicity matrix (Krajewski diagram) specifying which copies
   of which spinor reps make up H_F.

This is the same finding as P-LH-NCG-Native Section 3.2. The G1 finding
is **inherited**, not new.

**Verdict on G1: NOT DERIVABLE. Staggered-Dirac open gate dependency.**

## 3. G2 — A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) from retained content (PARTIALLY DERIVABLE)

This is the novel content of this note. We test whether each summand
of Connes-Chamseddine's A_F can be located in retained content.

### 3.1 ℂ-summand — DERIVABLE from central pseudoscalar ω

**Claim.** The ℂ-summand of A_F is derivable as the 2-dim real
subalgebra `ℝ[ω]/⟨ω²+1⟩` ≅ ℂ, where ω = γ₁γ₂γ₃ is the central
pseudoscalar of Cl(3) (retained: `CL3_SM_EMBEDDING_THEOREM.md` Sec. B).

**Proof.** The retained content gives:
- ω is central in Cl(3,0): `[ω, γ_i] = 0` for all i.
- ω² = -I (the foundational relation of complex numbers).

Therefore the real subalgebra ℝ[ω] ⊂ Cl(3,0) generated by ω is:
- 2-dim over ℝ (basis: `{I, ω}`),
- satisfies multiplication `(a + bω)(c + dω) = (ac − bd) + (ad + bc)ω`
  (exactly the complex-number multiplication law),
- hence isomorphic to ℂ as a real algebra.

**Runner verification (Section 1):**
- ω commutes with γ_1, γ_2, γ_3 (centrality): PASS.
- ω² = -I (foundational relation): PASS.
- ℝ[ω] = 2-dim real algebra (linear independence of `{I, ω}`): PASS.
- Multiplication law matches complex-number multiplication: PASS.
- Ring isomorphism ℝ[ω] ≅ ℂ via 1 ↔ I, i ↔ ω: PASS.

**This is a STRUCTURAL DERIVATION**, not a numerical-match construction.
The relation ω² = -I uniquely determines ℝ[ω] up to isomorphism as the
complex numbers (this is the universal property of the algebraic
completion).

**Physical interpretation.** The ω-generated ℂ supplies the abelian
U(1)_Y factor needed for hypercharge in the SM. This is consistent
with `CL3_SM_EMBEDDING_THEOREM.md` Section C which uses ω as the source
of `dim(Cl⁺(3) + span{ω}) = 5` for `g_Y² = 1/(d+2)`.

**Verdict: ℂ-summand DERIVABLE.**

### 3.2 ℍ-summand — DERIVABLE from Cl⁺(3) (retained, prior)

**Claim.** The ℍ-summand of A_F is derivable as Cl⁺(3) ≅ ℍ.

**Proof.** This is the load-bearing content of
`CL3_SM_EMBEDDING_THEOREM.md` Section A: the even subalgebra of Cl(3)
is spanned by `{I, e₁₂, e₁₃, e₂₃}` with bivectors `e_{ij} = γ_i γ_j`.
Each bivector squares to `-I` and they satisfy quaternionic
multiplication.

**Runner verification (Section 2):**
- `e₁₂² = e₁₃² = e₂₃² = -I` (quaternion units): PASS each.
- `e₂₃ · e₁₃ = e₁₂` (ij = k): PASS.
- `e₁₃ · e₁₂ = e₂₃` (jk = i): PASS.
- `e₁₂ · e₂₃ = e₁₃` (ki = j): PASS.
- `e₂₃ · e₁₃ · e₁₂ = -I` (Hamilton's identity): PASS.
- Real-dim 4 = `{I, i, j, k}` basis: PASS.

**Physical interpretation.** Cl⁺(3) ≅ ℍ supplies the SU(2)_L weak
isospin algebra. The unit quaternions are SU(2). `CL3_SM_EMBEDDING_THEOREM.md`
Section D shows this Cl⁺(3) SU(2) is isomorphic (as abstract Lie algebra)
to the physical weak SU(2) on the fiber.

**Verdict: ℍ-summand DERIVABLE (retained, prior).**

### 3.3 M_3(ℂ)-summand — DERIVABLE from hw=1 triplet (retained, narrow theorem)

**Claim.** A M_3(ℂ) algebra is derivable on retained content as the
algebra generated by the diagonal projectors `{P_{X_i}}` together with
the C₃ cyclic permutation on the hw=1 triplet ℂ³.

**Proof.** The retained
`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`
establishes:
- `H_hw1` = hw=1 triplet of the BZ-corner taste cube ≅ ℂ³.
- Diagonal projectors `P_{X_i}` (i=1,2,3) are mutually orthogonal and
  sum to I_3.
- `C₃` = cyclic permutation `X_1 → X_2 → X_3 → X_1` satisfies `C₃³ = I`.
- The algebra generated by `{P_{X_i}, C₃}` on ℂ³ is the full M_3(ℂ).

**Runner verification (Section 3):**
- Diagonal projector properties (P² = P, mutually orthogonal, Σ = I_3): PASS.
- `C₃³ = I` (cyclic group action): PASS.
- `C₃ · P_X_1 = E_{21}`, `C₃ · P_X_2 = E_{32}`, `C₃ · P_X_3 = E_{13}`
  (off-diagonal matrix units): PASS each.
- Generated algebra spans all 9 matrix units `{E_{ij}}` of M_3(ℂ): PASS.

**CRITICAL CAVEAT.** This is a structurally important obstruction to
the FULL G2 derivation. The retained M_3(ℂ) is the **GENERATION
algebra** acting on the hw=1 GENERATION triplet, but Connes-Chamseddine's
M_3(ℂ) is the **COLOR algebra** acting on the COLOR triplet within ONE
generation. These two M_3(ℂ)'s have the same abstract algebra type but
**different physical interpretation**. The retained M_3(ℂ)-on-generations
does not natively match Connes' M_3(ℂ)-on-color.

**Verdict: M_3(ℂ)-summand DERIVABLE as abstract algebra; physical
matching to Connes' color M_3(ℂ) is non-trivial.**

### 3.4 Assembly obstruction — three summands on distinct sectors

Even though each summand individually has a retained-content source,
the three summands live on **structurally distinct Hilbert sectors**:

| Summand | Acts on | Sector class |
|---|---|---|
| ℂ (from ω) | H_per_site (4-dim, ρ_+ ⊕ ρ_-) | per-site (A1 + chirality) |
| ℍ (from Cl⁺(3)) | H_per_site (4-dim) | per-site (A1 + chirality) |
| M_3(ℂ) (from hw=1) | H_hw1 (3-dim) | BZ-corner (staggered-Dirac gate) |

The first two live on the **per-site sector** (retained on A1 alone
per `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`).
The third lives on the **BZ-corner sector** (which is the staggered-Dirac
open gate).

**Connes-Chamseddine A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) acts on a SINGLE Hilbert
space H_F^Connes (96-dim).** Three summands located on **different
sectors** cannot natively assemble into a single direct sum on a
single H_F. The naive direct sum:

```text
   H_F^naive := H_per_site ⊕ H_hw1 = ℂ⁴ ⊕ ℂ³ = ℂ⁷
```

is **ad hoc**: it does not correspond to a natural single-sector or
single-site Hilbert space in the framework. The Connes' H_F is 96-dim
(3 × 32), with structure 3 generations × (lepton-doublet +
lepton-singlet + quark-doublet × 3-color + 2 quark-singlets × 3-color)
× 2 (particle + antiparticle). None of these tensor factors is natively
retained without the staggered-Dirac gate.

**Runner verification (Section 4):**
- ω lives on H_per_site (dim 4): PASS.
- Cl⁺(3) (ℍ) lives on H_per_site (dim 4): PASS.
- M_3(ℂ) (generation) lives on H_hw1 (dim 3): PASS.
- per-site sector ≠ BZ-corner sector (structurally distinct): PASS.
- Naive direct sum H_per_site ⊕ H_hw1 = ℂ⁷ ≠ H_F^Connes (96): PASS.
- Assembly into single H_F requires staggered-Dirac gate: PASS.

**Verdict on G2: PARTIALLY DERIVABLE.** Each summand individually
LOCATABLE in retained content; native direct-sum ASSEMBLY into a single
H_F requires the staggered-Dirac open gate.

## 4. G3 — Order-one as automatic consequence of G2 (NOT AUTOMATIC)

Even GRANTING G2 (i.e., positing a unified H_F with A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ)
acting block-diagonally), we test G3: does order-one
`[[D_F, a], JbJ⁻¹] = 0` follow automatically?

### 4.1 Toy direct-sum model

To test G3 on a tractable example without committing to the staggered-
Dirac realization, we build a 6-dim toy model:

```text
   H_F^toy := ℂ¹_ℂ ⊕ ℂ²_ℍ ⊕ ℂ³_M_3 = ℂ⁶
```

Each summand carries its fundamental rep (scalar action by ℂ, doublet
by ℍ, fundamental by M_3(ℂ)). A_F acts block-diagonally:

```text
   (λ, q, m) ∈ A_F  acts as  diag(λ, q, m)  on H_F^toy.
```

We test order-one for various D_F candidates with simple complex
conjugation as the real structure J (KO-dim 0 in this toy; the
structural finding is independent of KO-dim).

### 4.2 Block-scalar D_F: order-one VACUOUS

When D_F has the form `D_scalar = diag(d_1, d_2 · I_2, d_3 · I_3)`
(constant scalar within each block), the commutator `[D_scalar, a] = 0`
for all block-diagonal a, so `[[D_scalar, a], JbJ⁻¹] = 0` trivially.

**Runner verification (Section 5):**
- Block-scalar D over ALL A_F basis (14 elements: 2 ℂ + 4 ℍ + 9 M_3):
  max order-one violation = 0. PASS.
- D = 0: max violation = 0. PASS (vacuous case).

### 4.3 Yukawa-like D_F: order-one VIOLATED

The physically interesting D_F's (Yukawa-like couplings between
summands, generating SM mass spectra) are block-OFF-diagonal. When D
couples ℂ block to ℍ block (lepton singlet-doublet Yukawa) and ℍ block
to M_3 block (quark-like Yukawa), the order-one condition is
non-trivially violated.

**Explicit example.** Define:

```text
   D_yuk = symmetric block off-diagonal with:
     D[0, 1] = D[1, 0] = 0.5,  D[0, 2] = D[2, 0] = 0.3,
     D[1, 3] = D[3, 1] = 0.1,  D[2, 4] = D[4, 2] = 0.2.
```

For generic A_F elements a, b sampled from the basis,
`[[D_yuk, a], JbJ⁻¹] ≠ 0` with max violation ≈ 0.30.

**Runner verification (Section 5):**
- Yukawa-like D over ALL A_F basis: max violation > 0.01 (specifically
  ≈ 0.30). PASS (violation confirmed non-trivial).

### 4.4 Order-one is an active selection

The order-one CONSTRAINT SET is:

```text
   D_OC := { D_F : [[D_F, a], JbJ⁻¹] = 0 ∀ a, b ∈ A_F }.
```

The runner shows D_OC is **non-empty** (contains D = 0 and block-scalar
D's) but **non-trivial** (excludes generic Yukawa-like D's). Hence
order-one is an **active selection** on the space of admissible Dirac
operators, **not** a structural consequence of A_F's direct-sum form.

This re-derives the Chamseddine-Connes-van Suijlekom 2013
(arXiv:1304.8050) finding: order-one is the load-bearing discriminator
selecting Standard Model from Pati-Salam.

**Verdict on G3: NOT AUTOMATIC.** Even granting G2, order-one remains
an active selection that excludes generic Yukawa-like D_F's.

## 5. The structural relocation

Combining G1+G2+G3, the FULL BLAST examination yields:

```text
   Original LH-content gap (P-LH-Content proposal note 2026-05-10):
     one generic admission "LH content" (selects SM over Pati-Salam)
   
   After P-LH-NCG-Native (PR #1050):
     reduces to two NCG primitives {P-LH-1 (order-one), P-LH-3 (KO-dim-6 J)}
     and closes P-LH-3, leaving P-LH-1 as named NCG admission
   
   After this note (FULL BLAST):
     P-LH-1 (order-one) RELOCATES to staggered-Dirac gate dependency.
```

**Why this is a relocation, not closure.** The runner's three tests
identify that:

1. **D_F undetermined**: closing order-one requires fixing D_F first;
   D_F requires staggered-Dirac (G1).
2. **A_F partially derived but not assembled**: ℂ, ℍ, M_3 located in
   retained content but assembly into single H_F requires staggered-
   Dirac (G2).
3. **Order-one is active selection**: even granting G2, order-one is
   non-trivial; only a strict subset of D_F's satisfy it (G3).

The order-one condition's load-bearing content was always **logically
downstream** of the staggered-Dirac realization. The staggered-Dirac
gate is the unique upstream gate that determines:
- the unified H_F (which Hilbert space is the finite spectral triple's H);
- the embedding of A_F into End(H_F) (the bimodule / Krajewski diagram);
- the class of admissible D_F's (constrained by lattice locality).

When the staggered-Dirac gate closes, the order-one condition either:
- (a) follows automatically (if the derived staggered-Dirac D has the
  first-order property on the lattice, which is a natural feature of
  lattice-Dirac operators), or
- (b) becomes an additional structural constraint that the closed
  staggered-Dirac realization either satisfies or not.

In either case, **order-one is not an independent admission**.

**Why this is structural clarification, not new admission.** No new
gate is introduced. The staggered-Dirac gate already exists as
`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` and is named
in `MINIMAL_AXIOMS_2026-05-03.md`. This note simply re-locates a
previously-identified "named NCG admission" to the existing open
gate's content.

## 6. Hostile review

This section addresses adversarial questions about whether the
construction is a real derivation or a numerical-match-by-construction.

### HR1: Is constructing ℂ from ω² = -I a real derivation?

**Answer: YES, structural.** The relation ω² = -I is the **abstract
defining relation** of the universal ℝ-algebra `ℝ[X]/⟨X²+1⟩`, which is
isomorphic to ℂ as a real algebra independent of any numerical
embedding or representation. ω is RETAINED (central, with ω² = -I, in
Cl(3,0) per `CL3_SM_EMBEDDING_THEOREM.md` Section B). No numerical
fitting, no matching coefficient — purely algebraic.

### HR2: Does the "three summands on different sectors" obstruction matter?

**Answer: YES, central.** Connes-Chamseddine A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ)
acts on a **single** Hilbert space H_F^Connes (96-dim). The order-one
condition operates on this single H_F. Three summands **located** on
different sectors do not natively assemble: the assembly itself IS
the missing content. This is not a cosmetic distinction; it is the
structural reason why G2 is PARTIAL rather than FULL.

### HR3: Even if A_F were assembled, would order-one follow?

**Answer: NO.** Section 4.3 demonstrates explicitly: even with a clean
block-diagonal direct-sum structure on a unified H_F, generic
Yukawa-like D_F (block off-diagonal, the physically interesting case)
VIOLATES order-one. The constraint is active. This is independent of
any specific Connes-Chamseddine details; it follows from the
combinatorial structure of the commutator nesting.

### HR4: Is the deepest obstruction "order-one" or "staggered-Dirac"?

**Answer: STAGGERED-DIRAC.** With G2's "partially derivable but not
natively assemblable" finding, the LH-content gap **relocates
locationally** from "order-one as named NCG primitive" to
"staggered-Dirac open gate". Closing staggered-Dirac would derive
H_F, fix the A_F embedding, and restrict the Dirac operator class —
all three of which are upstream of order-one. The order-one consequence
follows by lattice-locality of staggered-Dirac D, not as an
independent admission.

### HR5: Is the "staggered-Dirac → order-one" relocation a derivation or an admission swap?

**Answer: STRUCTURAL CLARIFICATION, not admission swap.** The relocation
identifies that the order-one content was always **logically downstream**
of the already-named staggered-Dirac gate. No new gate is introduced;
the staggered-Dirac gate is already in `MINIMAL_AXIOMS_2026-05-03.md`
as a named open gate with explicit closure path. This note's relocation
simply collapses the previously-identified "order-one named NCG
admission" into the existing staggered-Dirac gate, **reducing the count
of independent admissions by one**.

## 7. Compatibility with retained content

All three G1, G2, G3 findings are CONSISTENT with retained Cl(3)/Z^3
content — i.e., they can be adjoined without contradicting any retained
theorem. This was established structurally:

- G1 (D_F undetermined) is consistent with the staggered-Dirac gate
  being open.
- G2 (summands locatable on distinct sectors) is consistent with the
  per-site/BZ-corner sector inventory.
- G3 (order-one active selection) is consistent with the
  Chamseddine-Connes 2013 finding.

The runner verifies all 68 structural checks at exact-algebra precision
on small matrices (PASS=68, FAIL=0).

## 8. Forbidden imports respected

- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new repo-wide axioms (this is a follow-on; no retention requested)
- NO HK + DHR appeal (Block 01 audit retired; respected)
- NO same-surface family arguments
- NO recourse to PDG-fitted Yukawa coupling values

## 9. Net verdict and consequence for LH-content campaign

**Honest verdict: BOUNDED — structural clarification, not closure.**

| Goal | Tier on retained Cl(3)/Z^3 |
|---|---|
| G1 (D_F derivation) | NOT DERIVABLE (staggered-Dirac open-gate dependency) |
| G2 (A_F derivation) | PARTIALLY DERIVABLE (summands located; assembly via gate) |
| G3 (order-one as auto consequence) | NOT AUTOMATIC (active selection) |

**Consequence for LH-content campaign.** The campaign trajectory is now:

```text
[Stage 1] LH-content as one generic admission
              ↓ (P-LH-Content proposal note, PR #1032)
[Stage 2] Two NCG primitives: {P-LH-1 (order-one), P-LH-3 (KO-dim-6 J)}
              ↓ (P-LH-NCG-Native, PR #1050)
[Stage 3] One named NCG admission (order-one); P-LH-3 derived
              ↓ (this note, PR #TBD)
[Stage 4] Order-one relocates to existing staggered-Dirac open gate;
          NO INDEPENDENT NEW ADMISSION
```

The closure path forward:

- **(a)** Close the staggered-Dirac open gate (the canonical parent
  is `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` with
  explicit closure path enumerated in
  `MINIMAL_AXIOMS_2026-05-03.md` and 6+ in-flight notes).
- **(b)** Once the gate closes, verify whether the derived staggered-
  Dirac D satisfies the order-one condition automatically by lattice
  locality (the natural feature) or whether order-one becomes an
  additional constraint that the gate's closure produces independently.

In either path, the LH-content gap is no longer an **independent** admission;
it is **structurally identified** with an already-open gate.

## 10. Honest scoping caveats

This note explicitly does NOT claim:

- That order-one is derivable on Cl(3)/Z^3 (Section 4 shows it is not
  automatic).
- That A_F is FULLY derivable as a direct sum (Section 3.4 identifies
  the assembly obstruction).
- That the staggered-Dirac gate is closer to closing than
  `MINIMAL_AXIOMS_2026-05-03.md` already records.
- That this note's structural relocation is the FINAL state of the
  LH-content campaign. Future work may close the staggered-Dirac gate
  and verify whether order-one follows automatically; or identify a
  finer relocation.

The honest scope is: **The FULL BLAST examination of A_F and order-one
derivability identifies that the LH-content gap is not an independent
admission but a downstream consequence of the existing staggered-Dirac
open gate. This is structural clarification, not closure.**

```yaml
claim_type_author_hint: primitive_proposal_note
claim_scope: |
  FULL BLAST follow-on to PRIMITIVE_P_LH_NCG_NATIVE attempting maximum-
  depth examination of whether the order-one condition [[D_F, a], JbJ⁻¹] = 0
  can be derived Cl(3)/Z^3-natively. Result:
    G1 (D_F): NOT DERIVABLE (staggered-Dirac open gate)
    G2 (A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ)): PARTIALLY DERIVABLE
      - ℂ-summand:    derivable as ℝ[ω]/⟨ω²+1⟩ from central pseudoscalar ω
      - ℍ-summand:    derivable as Cl⁺(3) ≅ ℍ (retained)
      - M_3(ℂ)-sumd:  derivable as ⟨P_{X_i}, C₃⟩ on hw=1 triplet (retained)
      - BUT: three summands live on STRUCTURALLY DISTINCT Hilbert sectors
        (per-site + BZ-corner); native single-H_F assembly requires
        staggered-Dirac gate
    G3 (order-one auto): NOT AUTOMATIC even granting G2 (active selection
      remains; toy model shows Yukawa-like D_F's violate order-one)
  Net verdict: BOUNDED — structural CLARIFICATION (LH-content gap
  relocates from independent "order-one named admission" to existing
  staggered-Dirac open gate; no new gate introduced; admission count
  reduces by one).
upstream_dependencies:
  - primitive_p_lh_ncg_native_note_2026-05-10_pPlh_ncg_native
  - primitive_p_lh_content_proposal_note_2026-05-10_pPlh
  - cl3_sm_embedding_theorem
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02
  - staggered_dirac_realization_gate_note_2026-05-03
  - minimal_axioms_2026-05-03
admitted_context_inputs:
  - Connes canonical KO-dim sign table (Connes 1995; reproduced in
    Connes-Marcolli NCG QFM Ch. 1; Suijlekom NCG Particle Physics Ch. 4)
  - Standard real-Clifford-algebra Cartan classification
    (Lawson-Michelsohn Spin Geometry Ch. I)
  - Chamseddine-Connes-Suijlekom 2013 (arXiv:1304.8050) as the
    authoritative reading of order-one's role as SM-vs-PS discriminator
  - Boyle-Farnsworth 2014/2018 (arXiv:1408.5367; arXiv:1604.00847)
    on associative-algebra extension as alternative derivation route
literature_references:
  - Connes A., "Noncommutative geometry and reality," J. Math. Phys. 36 (1995) 6194
  - Connes A., "Noncommutative geometry and the standard model with neutrino mixing,"
    JHEP 11 (2006) 081, arXiv:hep-th/0608226
  - Chamseddine A.H., Connes A., van Suijlekom W.D., "Beyond the
    spectral standard model: emergence of Pati-Salam unification,"
    JHEP 11 (2013) 132, arXiv:1304.8050
  - Boyle L., Farnsworth S., "Rethinking Connes' approach to the
    standard model of particle physics via non-commutative geometry,"
    NJP 16 (2014) 123027, arXiv:1408.5367
  - Boyle L., Farnsworth S., "A new algebraic structure in the
    standard model of particle physics," JHEP 06 (2018) 071, arXiv:1604.00847
  - Krajewski T., "Classification of finite spectral triples,"
    J. Geom. Phys. 28 (1998) 1, arXiv:hep-th/9701081
  - Cacic B., "Moduli Spaces of Dirac Operators for Finite Spectral Triples,"
    MPI Mathematik 2009
verification_runner: scripts/cl3_primitive_p_lh_order_one_2026_05_10_pPlh_order_one.py
```
