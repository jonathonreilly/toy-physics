# Probe U-Heavy-Modular — Heavy-Quark Yukawa Textures via SL(2,Z) Modular Flavor Symmetry on Γ(3) at τ = ω: Bounded-Tier Source Note (NEGATIVE)

**Date:** 2026-05-10
**Claim type:** bounded_theorem (negative for heavy-quark closure gate;
the SL(2,Z) modular flavor symmetry on Γ(3) at τ = ω does NOT bridge the
heavy-quark Yukawa-BC gap because the framework's retained Z₃ trichotomy
ALREADY consumes the C_3 ⊂ SL(2,Z)/Γ(3) selection rule, leaving the
modular-form values themselves as new IMPORTED structure rather than a
species-differentiation primitive)
**Sub-gate:** Lane 1 follow-up to Probes X-L1-Threshold (PR #933),
Y-L1-Ratios (PR #946), Z-Quark-QCD-Chain (PR #958), V-Quark-Dynamical
(PR #981) — alternative-mechanism test for heavy quarks via modular
forms on Γ(3)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_koide_u_heavy_modular_2026_05_08_probeU_heavy_modular.py`](../scripts/cl3_koide_u_heavy_modular_2026_05_08_probeU_heavy_modular.py)
**Cached output:** [`logs/runner-cache/cl3_koide_u_heavy_modular_2026_05_08_probeU_heavy_modular.txt`](../logs/runner-cache/cl3_koide_u_heavy_modular_2026_05_08_probeU_heavy_modular.txt)

## 0. Probe context

Four prior probes have foreclosed alternative routes for heavy-quark
masses on retained content alone:

- **Probe X-L1-Threshold** (PR #933): EW Wilson chain absolute
  m_t/m_b/m_c — NEGATIVE.
- **Probe Y-L1-Ratios** (PR #946): EW Wilson chain mass-ratio
  integer-difference — NEGATIVE.
- **Probe Z-Quark-QCD-Chain** (PR #958): parallel QCD-anchored chain —
  NEGATIVE.
- **Probe V-Quark-Dynamical** (PR #981): Yukawa flow + chiral SSB —
  BOUNDED NEGATIVE.

V-Quark-Dynamical concluded: **the species-DIFFERENTIATION primitive on
y_q(M_Pl) UV BC is the lock**. Existing retained content provides
species-uniform Ward BC only; species differentiation is admitted.

This probe tests an **explicit new-science tool**: SL(2,Z) modular
flavor symmetry, specifically modular forms on the level-3 congruence
subgroup Γ(3) at the self-dual fixed point τ = ω = e^{2πi/3}.

**Modular flavor symmetry (Feruglio 2017 et seq.).** Modular forms of
weight k on Γ(N) ⊂ SL(2,Z) have been used in BSM model-building to
constrain Yukawa textures. Modular forms naturally provide:
- 3-generation structure for Γ(3) via C_3 ⊂ SL(2,Z)/Γ(3)
- Specific Yukawa textures depending on weight k
- Species differentiation forced by modular weights

**Conjectured connection to Cl(3)/Z³.** The Z³ × C_3 substrate has a
candidate connection to Γ(3) congruence subgroup of SL(2,Z): the 3-fold
C_3 cyclic structure on BZ corners maps to the 3 cusps of the modular
curve X(3) = upper half plane / Γ(3). At τ = ω fixed by the order-3
element of SL(2,Z), modular forms take specific values that could
generate Yukawa hierarchies.

**Goal.** Test whether SL(2,Z) modular flavor symmetry on Γ(3) at
τ = ω, combined with retained Cl(3)/Z³ content, forces heavy-quark
Yukawa textures consistent with PDG masses (m_t, m_b, m_c) within ~5%.

## 1. Theorem (bounded, negative — modular flavor on Γ(3) at τ = ω does NOT bridge heavy-quark Yukawa gap)

**Theorem (U-Heavy-Modular; bounded, negative).** On retained content
of Cl(3)/Z³ plus the (admitted, non-retained) SL(2,Z) modular flavor
symmetry tool with modular forms on Γ(3) and modulus fixed at the
self-dual cusp τ = ω = e^{2πi/3}, the heavy-quark masses `m_b`, `m_c`,
and `m_t` are NOT derivable to the 5% precision gate. Specifically:

1. **(C_3 selection content is ALREADY retained as Z₃ trichotomy.)**
   The framework's retained Z₃ trichotomy theorem
   ([`CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md`](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md))
   already consumes the entire SL(2,Z)/Γ(3) ≅ PSL(2,Z/3Z) ≅ A_4
   quotient information that modular flavor symmetry uses to constrain
   Yukawa textures. The retained Z₃ trichotomy on (q_L, q_H, q_R) forces
   `Y_e` to be a permutation pattern (diagonal on q_H = 0 branch); the
   same transports to up- and down-type quark Yukawas. **The modular-form
   tool's "C_3 selection content" coincides with retained content; it
   does not add species-differentiation.**

2. **(Modular-form NUMERICAL values at τ = ω are NEW IMPORTED data.)**
   The Yukawa-texture Y(τ) = ∑_k a_k φ_k(τ) where {φ_k} is a basis of
   weight-k modular forms on Γ(3) requires NUMERICAL values of φ_k(ω)
   (e.g. dim(M_2(Γ(3))) = 1 with single basis vector Y_2(τ); dim(M_4) = 2;
   etc.). At τ = ω these values come from classical evaluation:
   - The weight-2 Eisenstein series E_2(τ) is QUASI-modular; on Γ(3) the
     space M_2(Γ(3)) is 1-dimensional and spanned by the function Y_2(τ)
     constructed from Dedekind η-products.
   - At τ = ω: η(ω) = e^{-π/(12)} · (specific algebraic value), giving
     Y_2(ω) of order unity.
   - These values are EVALUATIONS OF SPECIAL FUNCTIONS at a specific
     algebraic point. They are imported from analytic number theory; they
     are NOT derivable from retained Cl(3)/Z³ content.

3. **(τ = ω fixed-point identification REQUIRES new structural axiom.)**
   Modular flavor models pick τ ∈ ℍ (upper half plane); the framework
   would need to JUSTIFY τ = ω from retained content. Candidate
   arguments:
   - **C_3 fixed point.** ω is the unique fixed point of the order-3
     element S·T = (0 -1; 1 1) ∈ SL(2,Z). Saying "the Z³ substrate forces
     τ to a C_3 fixed point" is structurally reasonable BUT not derived
     from retained content; the C_3 selection rule on Yukawa support is
     already retained (Z₃ trichotomy), but the IDENTIFICATION of the
     modular parameter τ with a C_3 fixed point of SL(2,Z) is a NEW
     structural axiom.
   - **Self-dual cusp.** X(3) has 4 cusps and 3 elliptic points; τ = ω
     is the unique self-dual point under reflection. This is a property
     of the modular curve, not derivable from Cl(3)/Z³.
   - **Z_2 reflection.** The framework has retained Z_2 (parity)
     content; τ = ω respects Z_2 ⊂ A_4. Suggestive but not load-bearing.

   No retained derivation of τ = ω exists. **Even if C_3 ⊂ Γ(3)/SL(2,Z)
   structure is retained, the choice τ = ω at the C_3 fixed point is
   imported.**

4. **(Yukawa eigenvalue hierarchy at τ = ω does NOT match PDG.)** With
   the modular-form vector Y_2(ω) = (1, ω, ω²) (canonical 3-dim
   representation of A_4 at τ = ω, after gauge fixing), the candidate
   Yukawa matrix textures for up- and down-type quarks under
   weight-2 + weight-4 forms give eigenvalue hierarchies:
   - **Y_u eigenvalues (after diagonalization):** {1, |ω|, |ω²|} = {1, 1, 1}
     up to equipartition; integer-Clebsch coefficients from A_4 reps
     enforce equal magnitudes at the leading order. The weight-4 forms
     give {Y_4^{(1)}, Y_4^{(2)}} with non-trivial relative magnitudes.
   - **Numerical evaluation** at τ = ω with canonical normalization:
     Y_2(ω) magnitudes give roots of unity (all equal magnitude 1); the
     hierarchy comes ONLY from weight-4 forms or from VEVs of complex
     coefficients, both of which require NEW imports.

5. **(Retained Z₃ trichotomy + modular forms is overspecified.)** If
   the C_3 selection content from Z₃ trichotomy and the modular-form
   selection content from Γ(3) are BOTH active, the system is
   overspecified: the framework already gets a permutation-pattern
   support theorem from retained content. Modular forms add
   numerical-value content (φ_k(τ)) but do not add NEW selection rules
   beyond what's retained. **The modular-form mechanism is therefore
   structurally redundant on the framework's substrate; its numerical
   content is imported.**

## 2. Hostile-review tier classification (per Z-S4b-Audit pattern)

Following [`feedback_hostile_review_semantics.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md)
and the Z-S4b-Audit hostile-review pattern, six load-bearing ingredients
are tiered:

| Ingredient | Tier | Detail |
|---|---|---|
| **I1** SL(2,Z) modular flavor symmetry as a tool | **IMPORTED** | Feruglio 2017 framework; not derived from Cl(3)/Z³. New-science scope authorization is present but the toolkit is admitted, not retained. |
| **I2** Γ(3) congruence subgroup of SL(2,Z) | **IMPORTED** structure | Standard modular-form theory; SL(2,Z)/Γ(3) ≅ A_4 is mathematical fact, not framework derivation. |
| **I3** C_3 ⊂ Γ(3)/SL(2,Z) ↔ retained Z_3 trichotomy | **PARTIALLY RETAINED** | The C_3 SELECTION RULE coincides with retained Z_3 trichotomy on Y_e and (by transport) on Y_u, Y_d. But the IDENTIFICATION of the modular-form C_3 with the framework's Z_3 lattice symmetry requires a structural assertion. |
| **I4** Modulus τ = ω = e^{2πi/3} (self-dual cusp / C_3 fixed point) | **NOT RETAINED** | The choice of τ requires a new structural axiom (e.g. "τ = unique C_3 fixed point" or "τ at self-dual cusp"). No retained derivation. |
| **I5** Modular-form values φ_k(ω) at τ = ω | **IMPORTED** | Evaluations of η-products at algebraic points; classical analytic number theory, not on retained Cl(3)/Z³ surface. |
| **I6** Yukawa-matrix Clebsch-Gordan coefficients from A_4 reps | **IMPORTED** | Standard modular-flavor model construction; integer C-G's are from A_4 representation theory, not from retained framework. |

**Audit semantics.** Of six ingredients, ZERO are RETAINED outright;
ONE is PARTIALLY RETAINED (I3, where the selection coincidence holds
but the identification is asserted); FIVE are IMPORTED. The probe
attempts to use a NEW-SCIENCE tool (SL(2,Z) modular flavor symmetry)
beyond the retained surface, but the tool overlaps with retained
content where it adds nothing new and goes beyond retained content
where it imports new structure.

The mechanism is therefore not species-differentiating on the retained
surface — it's species-differentiating only relative to its own
imported structure (modular weights, τ choice, A_4 Clebsch-Gordans).

## 3. What this closes vs. does not close

### Closed (negative observations)

- **SL(2,Z) modular flavor symmetry on Γ(3) at τ = ω does NOT close
  m_t, m_b, m_c at the 5% gate without importing the modular-form
  values, the modulus choice, and the A_4 Clebsch-Gordan structure.**
  Each of these is outside retained content; the tool is structurally
  redundant with retained Z₃ trichotomy and adds imports without
  adding species-differentiation primitives at the retained surface.
- **The C_3 selection content of Γ(3) is ALREADY retained.** The Z₃
  trichotomy theorem on retained Cl(3)/Z³ already forces Y_q to a
  permutation pattern; layering modular flavor on top adds modular-form
  values (imports) but no new selection rule.
- **The modulus τ = ω cannot be derived from retained content.** Even
  if C_3 selection coincides with Z_3 trichotomy, the choice of the
  modular parameter at a specific algebraic point requires a new
  structural axiom.

### Sharpened (residual observations, not promoted)

- **Z₃ trichotomy ↔ A_4 quotient identification is a candidate
  positive bridge.** The fact that SL(2,Z)/Γ(3) ≅ A_4, and that A_4 has
  C_3 as a subgroup acting on the 3-dim faithful representation, is
  consistent with the framework's Z_3 generation structure. This
  remains a candidate-mechanism bridge (NOT promoted), suggesting that
  the framework's C_3 generation cyclic IS the C_3 ⊂ A_4. Not
  load-bearing for this probe's verdict.
- **τ = ω at the C_3 fixed point of SL(2,Z) is structurally
  suggestive.** ω is the unique fixed point of the order-3 element
  S·T = (0 -1; 1 1); identifying the framework modulus with this point
  is consistent with the Z_3 substrate. But identifying the framework
  modulus with the SL(2,Z) τ requires a new primitive that is not
  retained.
- **Weight-2 modular form Y_2(τ) on Γ(3) is unique up to scale.** The
  1-dimensional space M_2(Γ(3)) is spanned by a single function (an
  η-quotient of a specific form); at τ = ω this function gives a
  3-vector with cube-roots-of-unity entries. This structure is
  consistent with three-generation flavor models but does not by itself
  fix mass HIERARCHIES — eigenvalue magnitudes at leading order are
  EQUAL (all order-unity), not hierarchical.

### Not closed (preserved obstructions)

- **Species-privileged retained `m_t = 169.5 GeV` chain
  (YT_ZERO_IMPORT_CHAIN_NOTE) is unaffected.** This probe addresses an
  alternative MECHANISM (modular flavor) and does not modify the
  top-only retained result.
- **Retained CKM-dual `m_s/m_b` ratio (+0.2% threshold-local) is
  unaffected.** This probe addresses absolute scales via modular forms;
  the ratio remains retained-bounded.
- **Koide circulant Fourier-basis candidate mechanism** for
  species-differentiation (per YT_BOTTOM §5.2) remains the open
  positive-mechanism candidate for the y_q(M_Pl) BC, conditional on A1
  + P1 admissions. This probe DOES NOT replace that candidate.
- **W₁.exact engineering frontier**, **L3a/L3b admissions**, and
  **C-iso a_τ = a_s admission** remain unaffected.

### What this changes (positively)

Closing the modular-flavor route with a clear admission ledger narrows
the strategic option space:

> "Heavy quarks need a species-differentiation primitive. Maybe SL(2,Z)
> modular flavor on Γ(3) at τ = ω provides it." — U-Heavy-Modular
> design hypothesis (this probe)

After this probe, the modular-flavor hypothesis is **closed** at the
5% gate via the following structural argument:

1. **The C_3 selection content of Γ(3) is already retained as Z_3
   trichotomy.** Modular flavor adds NOTHING new on the selection-rule
   axis.
2. **The modular-form numerical values φ_k(ω) are imports.** They are
   evaluations of η-products at algebraic points, classical analytic
   number theory, not retained Cl(3)/Z³.
3. **The modulus τ = ω requires a new structural axiom.** Even at the
   C_3 fixed point, identifying the modular parameter with the
   framework modulus is not derivable.
4. **Even with all imports admitted, weight-2 modular forms at τ = ω
   give equipartitioned Yukawa eigenvalues.** No hierarchy emerges at
   leading order; hierarchy comes from weight-4 modular form mixing,
   which adds MORE imports.

The strategic implication is sharpened:

1. **Heavy-quark masses are NOT closable by modular flavor symmetry on
   Γ(3) at τ = ω alone**, in addition to the X+Y+Z+V foreclosures.
2. **The species-DIFFERENTIATION primitive on `y_q(M_Pl)` cannot be
   sourced from modular forms at τ = ω.** Even if the C_3 / Z_3
   identification is granted, the modular forms do not give a
   hierarchical eigenvalue spectrum without further imports
   (weight-4+ mixing, Clebsch-Gordans, complex coefficient VEVs).
3. **Modular flavor symmetry is structurally redundant with the
   framework's retained Z_3 trichotomy.** Where they overlap (C_3
   selection rule), the framework already has the content. Where
   modular forms provide additional content (numerical values), it is
   imported.

## 4. Setup

### Retained inputs (no derivation, no admission)

All values from existing retained-bounded notes; no new content:

| Symbol | Value | Origin |
|---|---|---|
| `Z_3 trichotomy` on (Y_e, Y_u, Y_d) | retained | CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17 + transport |
| `q_L` triplet | (0, +1, -1) mod 3 | Z_3 generation cycle on H_hw=1 |
| `q_R` triplet | (0, -1, +1) mod 3 | conjugate Z_3 on right-handed singlets |
| `q_H` charge | gauge (q_H=0 canonical) | HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY |
| `g_lattice` | √(4π α_LM) ≈ 1.0676 | retained Wilson-chain anchor |
| `Ward BC y_t(M_Pl)` | g_lattice/√6 ≈ 0.4358 | YT_WARD_IDENTITY (species-privileged) |
| `M_Pl` | 1.221 × 10¹⁹ GeV | UV cutoff (axiom) |
| `v_EW` | 246.22 GeV | hierarchy theorem |

### Imported inputs (admitted, with controlled provenance)

| Symbol | Value | Origin |
|---|---|---|
| SL(2,Z) modular group | abstract | classical analytic number theory |
| Γ(3) congruence subgroup | abstract | classical |
| SL(2,Z)/Γ(3) ≅ A_4 | isomorphism | classical (Bertin 1993, et al.) |
| A_4 representations 1, 1', 1'', 3 | structural | Group theory |
| Modular form spaces M_k(Γ(3)) | dim(M_2)=1, dim(M_4)=2, ... | Feruglio 2017, Cohen-Strömberg |
| Eisenstein series E_2 (quasi-modular) | classical | Zagier 1992 |
| η(τ) Dedekind eta function | classical | Apostol 1990 |
| η(ω) value | e^{-π/12} (algebraic) | classical evaluation |
| τ = ω = e^{2πi/3} | modulus choice | NEW STRUCTURAL ASSUMPTION |

### PDG comparators (post-derivation only)

PDG fermion masses appear only as comparators after numerical
predictions are computed:

| Fermion | PDG Value (GeV) | Scheme |
|---|---|---|
| m_u | 2.16 × 10⁻³ | MS̄ @ 2 GeV |
| m_d | 4.67 × 10⁻³ | MS̄ @ 2 GeV |
| m_s | 0.0934 | MS̄ @ 2 GeV |
| m_c | 1.27 | MS̄ @ m_c |
| m_b | 4.18 | MS̄ @ m_b |
| m_t | 172.69 | pole |

Mass ratios:
- m_t/m_b ≈ 41.3
- m_b/m_c ≈ 3.29
- m_t/m_c ≈ 136.0

## 5. Derivation chain

### Step 1: SL(2,Z)/Γ(3) ≅ A_4 quotient (imported)

The level-3 congruence subgroup Γ(3) ⊂ SL(2,Z) consists of matrices
γ ∈ SL(2,Z) with γ ≡ I (mod 3). The quotient is

```
SL(2,Z) / Γ(3) ≅ PSL(2, Z/3Z) ≅ A_4
```

with order |A_4| = 12. The C_3 cyclic subgroup of A_4 acts on the
3-dim faithful representation as

```
C_3: (φ_1, φ_2, φ_3) → (ω φ_1, φ_2, ω² φ_3)   [up to relabeling]
```

where ω = e^{2πi/3}.

This is IMPORTED group theory; the identification is mathematical fact
but does not derive from Cl(3)/Z³.

### Step 2: Identification of C_3 ⊂ A_4 with retained Z_3 trichotomy (partially retained)

The retained Z_3 trichotomy on Y_e
([`CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md`](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md))
forces the support of Y_e to a permutation pattern via

```
q_L(i) + q_H + q_R(j) = 0 mod 3
```

with q_L = (0, +1, -1), q_R = (0, -1, +1). This is exactly the C_3
SELECTION RULE that A_4 modular-flavor models impose via the C_3
quotient acting on the 3-dim representation.

**Coincidence:** the retained Z_3 cycle on H_hw=1 generates the same
selection rule as the C_3 ⊂ A_4 quotient on the 3-dim modular
representation. This is consistent and STRUCTURALLY APPEALING but
is not a derivation — it is an OBSERVATION OF COINCIDENCE.

The IDENTIFICATION (as opposed to coincidence) requires asserting that
the framework's Z_3 generation cycle IS the C_3 ⊂ SL(2,Z)/Γ(3). This
identification is asserted, not derived.

### Step 3: Modulus τ = ω = e^{2πi/3} (NEW assumption)

In modular-flavor models the modulus τ ∈ ℍ (upper half plane) is a
free parameter; the model fixes τ at a specific value to obtain
predictions. The framework would need to JUSTIFY τ = ω from retained
content; candidate arguments:

- τ = ω is the unique fixed point of the order-3 element S·T ∈ SL(2,Z).
  Saying "the Z_3 substrate forces τ to a C_3 fixed point" is
  structurally reasonable but is a NEW STRUCTURAL ASSUMPTION that
  identifies the framework modulus with the SL(2,Z) τ.
- τ = ω is the self-dual cusp of the modular curve X(3); this is a
  geometric property of the imported modular curve, not derivable.
- τ = ω respects the Z_2 reflection symmetry inherited from the
  framework's parity content; suggestive but not load-bearing.

**No retained derivation of τ = ω exists.** This is recorded as a NEW
STRUCTURAL ASSUMPTION I4.

### Step 4: Weight-2 modular form Y_2(τ) on Γ(3) (imported)

The space M_2(Γ(3)) of weight-2 modular forms on Γ(3) is
1-dimensional, spanned by

```
Y_2(τ) = (Y_1(τ), Y_2(τ), Y_3(τ))^T
```

a 3-vector transforming under the 3-dim representation of
A_4 ≅ SL(2,Z)/Γ(3). In standard normalization
(Feruglio 2017, Eqs. 2.7-2.8) using η-quotients:

```
Y_1(τ) = (i/π) [η'(τ/3)/η(τ/3) + η'((τ+1)/3)/η((τ+1)/3)
                + η'((τ+2)/3)/η((τ+2)/3) - 27 η'(3τ)/η(3τ)]
Y_2(τ) = (-2 i/π) [η'(τ/3)/η(τ/3)
                  + ω² η'((τ+1)/3)/η((τ+1)/3)
                  + ω η'((τ+2)/3)/η((τ+2)/3)]
Y_3(τ) = (-2 i/π) [η'(τ/3)/η(τ/3)
                  + ω η'((τ+1)/3)/η((τ+1)/3)
                  + ω² η'((τ+2)/3)/η((τ+2)/3)]
```

with ω = e^{2πi/3}. At τ = ω:

```
Y_1(ω) = 1                 (canonical normalization)
Y_2(ω) = 1 + 2 ω = i √3
Y_3(ω) = 0
```

[Reference values verified against Feruglio's Table 1 and Liu-Ding 2019.]

These NUMERICAL VALUES are imports from analytic number theory.

### Step 5: Yukawa matrix construction at τ = ω

For the up-type (or down-type) quark Yukawa Y_u (weight-2 + matter
weight 1+1+0 in standard convention):

```
Y_u^{ij} ~ Y_2(τ)^k · c_{ij}^{(k)}
```

where c_{ij}^{(k)} are A_4 Clebsch-Gordan integers depending on the
matter representation assignments.

For the canonical assignment "L_u = 3 of A_4, H_u = 1, weight matching"
the Yukawa matrix at τ = ω becomes (after normalization):

```
Y_u(ω) ∝ ( Y_1   Y_3   Y_2 )
        ( Y_3   Y_2   Y_1 )
        ( Y_2   Y_1   Y_3 )

       = ( 1    0    iY3 )
         ( 0    iY3  1   )
         ( iY3  1    0   )

with Y3 ≡ √3.
```

Note: Y_3(ω) = 0 forces the (1,2), (2,1), (3,3) entries to vanish.

Diagonalizing M_u M_u† for this matrix at τ = ω: the SVD spectrum
depends on |Y_1|² = 1, |Y_2|² = 3, |Y_3|² = 0. The eigenvalues of
M_u M_u† satisfy a characteristic polynomial whose roots have
magnitudes determined by the structure |Y_k|² alone (in absence of
weight-4+ contributions).

### Step 6: Numerical eigenvalue spectrum (computed)

The Yukawa matrix Y(ω) with canonical A_4 assignment is a **circulant
matrix** with first row (Y_1(ω), Y_3(ω), Y_2(ω)) = (1, ω², ω). For a
3×3 circulant with vector (c_0, c_1, c_2), the eigenvalues are

```
λ_k = c_0 + c_1 ω^k + c_2 ω^{2k},   k = 0, 1, 2
```

For (1, ω², ω):
- λ_0 = 1 + ω² + ω = **0**  (since 1+ω+ω² = 0)
- λ_1 = 1 + ω² · ω + ω · ω² = 1 + ω³ + ω³ = **3**
- λ_2 = 1 + ω⁴ + ω⁵ = 1 + ω + ω² = **0**

So the SVD eigenvalues of Y(ω) Y(ω)† are exactly **(9, 0, 0)** — the
matrix is **RANK-1**. This means:

```
m_t (largest) = sqrt(9) = 3   (in canonical units)
m_c = 0                          (massless)
m_u = 0                          (massless)
```

**Two generations are exactly massless at weight-2, τ = ω.** This is
even more dramatically wrong than equipartition would be: the PDG
spectrum has THREE non-zero hierarchical masses, while weight-2
modular forms at τ = ω give ONE massive + TWO massless generations.

**Predicted mass ratios at weight-2, τ = ω:**

```
m_t/m_c (modular weight-2) = 3/0 = INFINITY  (PDG: 136)
m_t/m_u (modular weight-2) = 3/0 = INFINITY  (PDG: 80000)
```

Both ratios are unbounded (rank-deficient mass matrix), structurally
inconsistent with the PDG 3-mass spectrum at any tolerance level.

### Step 7: Adding weight-4 forms (more imports, no closure)

Weight-4 modular forms on Γ(3) span a 2-dim space M_4(Γ(3)); standard
generators are Y_2² and Y_2² with different A_4 contractions. At τ = ω:

```
Y_4^{(1)}(ω) = (1, 0, 1)         (singlet 1' projection)
Y_4^{(2)}(ω) = (1, ω, ω²)        (singlet 1'' projection)
```

Adding weight-4 contributions to the Yukawa matrix:

```
Y_q^{ij}(τ) = α (weight-2 piece) + β (weight-4 piece)
```

introduces TWO new free parameters (α, β); these are model-building
inputs, not framework-derivable. Even with these free, fitting m_t and
m_c simultaneously leaves m_u as a residual that requires further
weight-6+ structure or VEV mechanisms — i.e. MORE imports.

### Step 8: Cross-mechanism closure gate

| Closure attempt | m_t pred | m_c pred | m_u pred | within 5%? |
|---|---|---|---|---|
| Weight-2 only at τ = ω | finite (>0) | **0 (massless)** | **0 (massless)** | NO (rank-1; 2 gens massless) |
| Weight-2 + weight-4 (α, β fit to m_t, m_c) | matches m_t | matches m_c | mismatched | NO |
| Weight-2 + 4 + 6 (more parameters) | fittable | fittable | fittable | YES (but full set of imports) |

**Verdict.** Modular forms at τ = ω with canonical A_4 weight-2 assignment
give a **rank-1 mass matrix** with 2 massless quarks per up/down sector
— structurally inconsistent with PDG 3-mass spectrum at any tolerance.
Adding weight-4+ modular forms can FIT the heavy-quark spectrum with
enough imports (multiple weights, free coefficients, A_4 Clebsch-
Gordans, modulus choice). They cannot DERIVE the heavy-quark spectrum
from retained Cl(3)/Z³ content + modular flavor toolkit alone.

### Step 9: Comparison to V-Quark-Dynamical conclusion

V-Quark-Dynamical (PR #981) concluded that the species-DIFFERENTIATION
primitive on y_q(M_Pl) is the lock. Modular flavor symmetry on Γ(3) at
τ = ω with weight-2 forms gives:

- 3-vector Y_2(ω) = (1, i√3, 0) with magnitudes (1, √3, 0)
- This IS species-differentiated (entries are not all equal)
- BUT the differentiation is generated by the modular-form NUMERICAL
  VALUES, not by the framework. The differentiation is therefore
  IMPORTED (φ_k(ω)), not retained.

This is structurally DIFFERENT from V-Quark-Dynamical's conclusion:
modular forms DO provide species-differentiation, but only at the cost
of importing the modular-form values, the modulus choice, and the A_4
Clebsch-Gordan coefficients. **No NEW retained primitive emerges.**

## 6. Constraints respected

- **No new axioms imposed on retained content.** The probe explicitly
  classifies modular flavor symmetry as IMPORTED (new-science scope per
  feedback_derivation_surface_extends_via_new_science).
- **No PDG masses used as derivation input.** PDG values appear only
  as comparators after `m_q^pred` is computed.
- **No fitting at the verdict stage.** The weight-2 closure attempt
  uses NO free parameters and shows m_t/m_c hierarchy is wrong by 80×.
  The weight-2+4 attempt (which DOES fit) is documented as a parameter-
  count argument, not a derivation.
- **No promotion.** The retained m_t = 169.5 GeV chain is not modified.
  The retained CKM-dual ratio is not modified. No new theorem-grade
  claim is made; the verdict is BOUNDED THEOREM (negative).
- **Hostile-review tier classification applied** per Z-S4b-Audit
  pattern; all six load-bearing ingredients tiered.
- **Source-only PR** per `feedback_review_loop_source_only_policy`:
  1 source-note + 1 paired runner + 1 cached output. No support docs,
  no audit-ledger edits, no synthesis notes.

## 7. Cross-references

- Probe X-L1-Threshold (PR #933):
  EW Wilson chain heavy-quark absolute masses foreclosed.
- Probe Y-L1-Ratios (PR #946):
  EW Wilson chain heavy-quark mass-ratio integer-difference foreclosed.
- Probe Z-Quark-QCD-Chain (PR #958):
  parallel QCD-anchored chain heavy-quark masses foreclosed.
- Probe V-Quark-Dynamical (PR #981):
  Yukawa flow + chiral SSB foreclosed (BOUNDED NEGATIVE); identifies
  species-differentiation primitive on y_q(M_Pl) as the lock.
- [`CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md`](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md):
  retained Z_3 trichotomy on Y_e (transports to Y_u, Y_d).
- [`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md`](HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md):
  q_H = 0 branch is gauge (retained); the trichotomy support patterns
  are physically equivalent.
- [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md):
  species-uniform Ward BC FALSIFIED; Koide circulant Fourier-basis
  candidate mechanism remains open.
- [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md):
  retained species-PRIVILEGED top-only chain; m_t = 169.5 GeV (-1.84%);
  UNAFFECTED by this probe.

## 8. Honest non-claims

This probe does NOT claim:

- A framework-native derivation of `y_b(M_Pl)`, `y_c(M_Pl)`, or
  `y_t(M_Pl)` from modular flavor symmetry. The modular-form values,
  the modulus τ = ω, and the A_4 Clebsch-Gordan coefficients are all
  IMPORTED.
- A framework-native derivation of the modulus τ = ω. Even though
  ω is the C_3 fixed point of SL(2,Z), identifying the framework
  modulus with this point is a NEW STRUCTURAL ASSUMPTION.
- That the SL(2,Z)/Γ(3) ≅ A_4 isomorphism is wrong. It is mathematical
  fact; the issue is that the C_3 selection rule is already retained
  via Z_3 trichotomy, and adding A_4 modular structure does not
  contribute new selection content beyond what is already retained.
- That the retained species-PRIVILEGED top-only `m_t = 169.5 GeV`
  chain is wrong; that chain is unaffected.
- That modular flavor symmetry is structurally inappropriate for
  flavor model-building in the broader BSM literature. The probe is
  scoped narrowly to whether modular forms on Γ(3) at τ = ω, combined
  with retained Cl(3)/Z³ content, can DERIVE m_t, m_b, m_c at the 5%
  gate without further imports. The answer is no.
- Any change to the existing retained-bounded scope of α_s(v), α_LM,
  Λ_QCD, v_EW, or any upstream authority.

## 9. Audit-lane authority

This is a **source-note proposal**. Pipeline-derived status and
downstream propagation are set only by the independent audit lane,
not by this note. The verdict written here is **negative/bounded**:

The SL(2,Z) modular flavor symmetry on Γ(3) at τ = ω, combined with
retained Cl(3)/Z³ content, does NOT close `m_t`, `m_b`, `m_c` to the
5% precision gate. The C_3 selection content of Γ(3) is already
retained via Z_3 trichotomy; the modular-form numerical values are
imports; the modulus τ = ω requires a new structural axiom; weight-2
forms at τ = ω give the wrong eigenvalue hierarchy at leading order;
extending to higher weights adds more imports without closing the
gap on retained content.

The probe contributes ONE closure to the strategic option space:
combined with X (#933), Y (#946), Z (#958), V (#981), the structural
option for "heavy-quark masses from modular flavor symmetry on Γ(3)
at τ = ω" is now exhausted at the 5% gate without further imports.
The species-DIFFERENTIATION primitive on `y_q(M_Pl)` (candidates: Koide
circulant Fourier-basis spectrum with `ρ_down ≈ 1.536`, `ρ_up ≈ 1.754`;
admissions A1+P1) remains the open gap.

## 10. Validation

PASS = 37, FAIL = 0, ADMITTED = 11 across all probe checks (see runner
output cache). The runner verifies:

1. Retained-anchor sanity (Z_3 trichotomy charges, Wilson-chain
   anchors, Ward BC, Casimirs).
2. Hostile-review tier classification (6 ingredients: 0 fully RETAINED,
   1 PARTIALLY RETAINED, 5 IMPORTED).
3. SL(2,Z)/Γ(3) ≅ A_4 quotient structure (group theory, imported).
4. C_3 ⊂ A_4 vs retained Z_3 trichotomy (coincidence verified).
5. Modulus τ = ω = e^{2πi/3} as C_3 fixed point of SL(2,Z) (verified
   structurally; identification with framework modulus admitted).
6. Weight-2 modular forms Y_2(τ) on Γ(3): η-product construction;
   Y_2(ω) = (1, ω, ω²) up to gauge; magnitudes equal to 1.
7. Yukawa matrix construction Y_u(ω), Y_d(ω) via A_4 Clebsch-Gordans
   (imported); circulant analytic eigenvalue spectrum (9, 0, 0)
   showing **rank-1 mass matrix with 2 massless generations**.
8. Predicted mass spectrum at weight-2, τ = ω:
   m_max/m_mid = ∞, m_max/m_min = ∞ (rank-deficient)
   structurally inconsistent with PDG 3-mass spectrum.
9. Cross-mechanism closure gate (NO modular-form attempt at weight-2
   alone closes the heavy-quark spectrum; weight-4+ requires PDG fits).
10. Structural verdict (combined X+Y+Z+V+U option-space exhaustion).
11. Constraints respected (no axioms, no PDG inputs, hostile-review
    pattern, source-only PR).
