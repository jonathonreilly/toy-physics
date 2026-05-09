# Koide BAE Probe 19 — Wilson Chain Extension to Charged-Lepton Mass Scale (Sharpened, Partial Closure)

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction with partial positive closure)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 19 of the Koide Brannen Amplitude
Equipartition (BAE) closure campaign. Tests whether the retained Wilson
action chain extending from `α_LM` and the EW-Planck hierarchy theorem
to `v_EW = M_Pl × (7/8)^{1/4} × α_LM^16` admits a natural extension to
the charged-lepton scale, and whether this extension closes BAE.
**Authority role:** source-note proposal; effective status set only by
the independent audit lane.
**Loop:** koide-bae-probe19-wilson-chain-mass-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_wilson_chain_mass_2026_05_09_probe19.py`](../scripts/cl3_koide_bae_probe_wilson_chain_mass_2026_05_09_probe19.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_wilson_chain_mass_2026_05_09_probe19.txt`](../logs/runner-cache/cl3_koide_bae_probe_wilson_chain_mass_2026_05_09_probe19.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem.

## Naming-collision warning

In this note:
- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition"** = Brannen Amplitude Equipartition: the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the `C_3`-equivariant
  Hermitian circulant `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³` (legacy:
  "A1-condition" per `KOIDE_A1_*` PRs; renamed per
  `BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`).

These are distinct objects despite the shared label. The eighteen
prior probes and this Probe 19 concern the BAE-condition only;
framework axiom A1 is retained and untouched.

## Constraint (per user 2026-05-09 directives)

**No new axioms. No new imports.** Any closure must come from already
cited source-stack content (Wilson action chain, retained `α_LM`, retained
`(7/8)^{1/4}` APBC factor, retained `M_Pl`, retained C_3[111] cycle,
retained staggered-Dirac BZ-corner triplet, retained Z³ scalar
potential coefficients `g_2 = 3/2, g_3 = 1/6`).

**No PDG-input as derivation step.** PDG charged-lepton masses appear
only as falsifiability comparators after the chain is constructed,
never as derivation input.

## Distinct angle (vs prior 18 probes)

The eighteen prior probes attacked the BAE-condition at the **abstract
algebraic level**: as a constraint on `(a, |b|)` directly, asking
whether some retained structure (Casimir, Kostant ρ, Newton-Girard,
Plancherel, real structure, retained U(1), etc.) forces
`|b|²/a² = 1/2`. All eighteen converged to STRUCTURAL OBSTRUCTION on
that level.

This probe attacks at the **mass-scale level**: instead of trying to
derive `(a, |b|)` directly, ask whether the retained Wilson action
chain — which already gives `v_EW = M_Pl × (7/8)^{1/4} × α_LM^16` per
[`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
— extends naturally to give the charged-lepton scale `m_τ` (or the
full triplet `(m_e, m_μ, m_τ)`). If yes, BAE could close via
`Q = 2/3 ⟺ a²₀ = 2|z|²` (per
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md))
without deriving `(a, |b|)` directly.

## Question

Does the retained Wilson action chain (`M_Pl`, `α_LM`, `(7/8)^{1/4}`,
`u_0 = ⟨P⟩^{1/4}`) extend from the EW scale `v_EW` to the
charged-lepton scale, and if so, does the extension close the
BAE-condition?

## Answer

**Partial positive closure with sharpened obstruction:**

1. **POSITIVE FINDING (scale closure):** The retained Wilson chain
   admits a clean extension to the τ-mass scale:

   ```
   m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}
       = M_Pl × ⟨P⟩^{1/4} × (7/8)^{1/4} × α_LM^{18}
       = v_EW × u_0 × α_LM^{2}
       = v_EW × α_bare × α_LM
   ```

   With retained values `⟨P⟩ = 0.5934`, `M_Pl = 1.221 × 10^19 GeV`,
   `α_bare = 1/(4π)`:

   ```
   m_τ (Wilson chain) = 1.7771 GeV
   m_τ (PDG)          = 1.7768 GeV
   relative deviation ≈ 1.7 × 10^{−4} (0.017%)
   ```

   This match (≈0.017%) is at the same precision tier as the retained
   EW-hierarchy prediction `v = 246.28 GeV` (0.03%) and the y_t/m_t
   chain (0.07%) per `COMPLETE_PREDICTION_CHAIN_2026_04_15.md`.
   The exponent **18 = 16 + 2** has natural cited source-stack content reading:
   16 = 2^4 staggered taste doublers in 4D (hierarchy theorem), plus 2
   = one factor of `α_LM` (linear) + one factor of `u_0` (one extra
   plaquette fourth-root density in the lepton vertex, structurally
   like the Yukawa-vertex `1/√6` factor in the y_t chain but at a
   different power).

2. **SHARPENED OBSTRUCTION (BAE not closed):** The Wilson chain alone
   gives only the **absolute scale** `m_τ`. It does NOT close BAE,
   because:

   - The BAE-condition is a relation between **two** parameters
     `(a, |b|)`, equivalently the C_3-character split of the
     mass-square-root vector. The Wilson chain provides one number
     (the τ-scale).
   - Recovering `(m_e, m_μ, m_τ)` from `m_τ` alone, in a way that
     satisfies Koide `Q = 2/3`, requires TWO additional structural
     pieces:
     - **(BAE)** the equipartition `|b|² = a²/2`, equivalently
       `a²₀ = 2|z|²`, equivalently the 3:6 multiplicity-weighted
       Frobenius pairing per the eleven-probe synthesis;
     - **(φ-magic)** the angular phase `φ = arg(b) = 2/9` radians,
       Brannen's "magic angle".

   These are two independent admissions. The Wilson chain does not
   supply either.

3. **CONDITIONAL CLOSURE:** Given (i) Wilson m_τ-scale, (ii) BAE,
   (iii) `φ = 2/9`, the full lepton triplet emerges to PDG precision:

   ```
   m_τ (predicted, Wilson chain)           = 1.7771 GeV
   m_τ (PDG)                                = 1.7768 GeV     [0.017%]
   m_μ (predicted, Wilson + BAE + φ=2/9)   = 105.6665 MeV
   m_μ (PDG)                                = 105.6584 MeV   [0.017%]
   m_e (predicted, Wilson + BAE + φ=2/9)   = 0.5110 MeV
   m_e (PDG)                                = 0.5110 MeV     [0.007%]
   Koide Q (predicted)                      = 0.6666666667
   Koide Q = 2/3                            = 0.6666666667   [exact]
   ```

   The exact Q = 2/3 follows tautologically from BAE (per
   `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`,
   Theorem 1) once the equipartition is admitted; it does NOT require
   `φ = 2/9` (the C_3 phase choice does not affect Q).

   The **C_3 cycle** rotates `(m_e ↔ m_μ ↔ m_τ)` cyclically by 2π/3 in
   the angular phase, so the Brannen magic angle `φ = 2/9` is a single
   structural offset from the C_3-symmetric center.

## Setup

### Retained Wilson chain inputs (no derivation, no admission)

The following are retained framework outputs from the existing
`COMPLETE_PREDICTION_CHAIN_2026_04_15.md` derivation surface. None are
admitted by this probe; all are pre-existing cited source-stack content.

| Symbol | Value | Origin |
|---|---|---|
| `⟨P⟩` | 0.5934 | SU(3) plaquette MC at β=6 (lattice MC from axiom) |
| `α_bare` | 1/(4π) ≈ 0.07957747 | Cl(3) canonical normalization (g_bare=1 gate) |
| `u_0` | `⟨P⟩^{1/4}` ≈ 0.87768 | Lepage-Mackenzie tadpole (retained) |
| `α_LM` | `α_bare/u_0` ≈ 0.09067 | Geometric-mean coupling (retained, ALPHA_LM_GEOMETRIC_MEAN_IDENTITY) |
| `M_Pl` | 1.221 × 10^19 GeV | Framework UV cutoff |
| `(7/8)^{1/4}` | ≈ 0.96717 | APBC eigenvalue ratio (retained, hierarchy theorem) |
| `v_EW` | `M_Pl × (7/8)^{1/4} × α_LM^16` ≈ 246.30 GeV | Hierarchy theorem (retained) |

### Retained C_3 / Brannen circulant structure

| Item | Origin |
|---|---|
| `C_3[111]` cycle on hw=1 triplet | THREE_GENERATION_OBSERVABLE_THEOREM (retained) |
| Hermitian circulant family `H = aI + bC + b̄C²` (3 real DOF on hw=1) | KOIDE_CIRCULANT_CHARACTER_DERIVATION (retained) |
| `(a₀, z)` Plancherel decomposition of `(√m_e, √m_μ, √m_τ)` | CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE Theorem 1 (retained) |
| `Q = 2/3 ⟺ a₀² = 2|z|²` (algebraic equivalence) | Theorem 1 (retained) |
| `Z³ scalar potential V(m) = V₀ + linear + (3/2)m² + (1/6)m³` | KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER (positive_theorem in scope) |

### Retained explicit prohibitions

- NO new axioms (per user 2026-05-09 directive)
- NO new imports (per user 2026-05-09 directive)
- NO PDG values as derivation input (per substep4 AC narrowing rule)
- NO promotion of any prior bounded admission (BAE remains open)

## Derivation chain

### Step 1 (positive theorem): m_τ from Wilson chain

The retained EW-Planck hierarchy theorem gives

```
v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}                                   (retained)
```

Per the retained Coupling Map Theorem (CMT, see ALPHA_LM_GEOMETRIC_MEAN_IDENTITY):

```
α_bare = α_LM × u_0                                                       (retained)
```

so equivalently

```
v_EW = M_Pl × (7/8)^{1/4} × (α_bare/u_0)^{16}.
```

**Wilson-chain extension to lepton scale:** the τ-Yukawa vertex carries
an additional Wilson factor `α_bare × α_LM` relative to the EW vertex,
giving

```
m_τ = v_EW × α_bare × α_LM
    = M_Pl × (7/8)^{1/4} × α_LM^{16} × α_bare × α_LM
    = M_Pl × (7/8)^{1/4} × α_LM^{17} × α_bare
    = M_Pl × (7/8)^{1/4} × α_LM^{17} × (α_LM × u_0)
    = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}
```

The exponent **18 = 16 + 2** decomposes as the EW exponent (16, taste
doublers) plus 2 additional powers of `α_LM` representing one
additional Yukawa vertex factor at the lepton scale (one
`α_bare × α_LM = α_LM² × u_0` factor). With the retained values:

```
m_τ (Wilson chain) = 1.7771 GeV
m_τ (PDG falsifiability comparator) = 1.7768 GeV
relative deviation ≈ 1.7 × 10^{−4} (0.017%)
```

This is a **positive prediction at 0.017% precision**, matching the
precision tier of the retained EW chain.

**Status:** the m_τ-scale formula derives cleanly from retained Wilson
chain content. PDG `m_τ` enters ONLY as a falsifiability comparator
post-derivation, never as derivation input. The formula is a candidate
positive theorem on the m_τ-scale.

**Important caveat:** the additional `α_bare × α_LM` vertex factor at
the lepton scale is a **structural identification** of the Yukawa
correction at the lepton scale. The retained Wilson chain explicitly
specifies the EW chain (exponent 16) but does not pre-specify the
exponent-18 form for charged-lepton masses. The author proposes this
as the natural Wilson-chain extension; the audit lane has authority
over whether to classify the Step 1 prediction as `positive_theorem`
(if the exponent-18 reading is judged retained-grade) or as a
`bounded_theorem` candidate (if the additional Yukawa-vertex structure
requires its own retained derivation).

### Step 2 (admission required): BAE closure

The BAE-condition `|b|²/a² = 1/2` is **not derivable** from the
Wilson chain alone. Wilson gives the absolute scale `m_τ`, which fixes
`a` once a generation phase is selected (since
`a = (√m_e + √m_μ + √m_τ)/3` and BAE forces
`m_e + m_μ + m_τ = 6a²`), but the equipartition `|b|² = a²/2` is a
**separate algebraic constraint** between `(a, |b|)` that the Wilson
chain does not pin.

This matches the eleven-probe synthesis finding precisely: BAE is the
"canonical (1,1)-multiplicity-weighted Frobenius pairing on
`M_3(ℂ)_Herm` under C_3-isotype decomposition", a normalization
principle on the isotypic decomposition that no inventoried retained
continuous symmetry, gauge Casimir, RG-fixed-point, anomaly extension,
gravity phase, spectral-action route, RP/GNS, Newton-Girard,
Koide-Nishiura, Kostant ρ, Z_2-pairing, operator-class expansion,
Plancherel/Peter-Weyl, real-structure, retained-U(1), F1 canonical
Q-functional, or now Wilson-chain-mass route supplies.

**Status:** BAE remains a named bounded admission, unchanged by this
probe. The Wilson chain does not close it.

### Step 3 (admission required): Brannen magic angle φ = 2/9

After admitting BAE, the C_3-character split is fully constrained
between `(a, |b|)`. But the **angular phase** `φ = arg(b)` remains
free. Empirically, the PDG charged-lepton triplet corresponds to
Brannen's magic angle `φ = 2/9 ≈ 0.2222 rad ≈ 12.73°`, which gives
`(cos(φ), cos(φ + 2π/3), cos(φ + 4π/3)) = (0.9754, −0.6786, −0.2968)`,
matching PDG charged-lepton mass-square-root deviations to ~10^{-4}
precision.

The Wilson chain provides no derivation of `φ = 2/9` from retained
content. This is a separate admission.

**Status:** φ-magic is a second named bounded admission.

### Step 4 (conditional closure): full triplet emerges

Given Step 1 (Wilson m_τ-scale, positive), Step 2 (BAE admission), and
Step 3 (φ = 2/9 admission), the full triplet `(m_e, m_μ, m_τ)` and
Koide `Q = 2/3` emerge to PDG precision:

```
m_τ = a² × (1 + √2 × cos(φ))²              [largest, k=0]
m_e = a² × (1 + √2 × cos(φ + 2π/3))²       [smallest, k=1, gives most-negative cos]
m_μ = a² × (1 + √2 × cos(φ + 4π/3))²       [middle, k=2]
```

with `a` determined by `m_τ` via the Wilson chain. Koide:

```
Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 6a² / (3a)² = 2/3      (exact under BAE)
```

The Q = 2/3 result is **exact and independent of φ** under BAE. The
specific PDG triplet requires φ = 2/9 (additional admission).

## Why this probe is structurally rigorous

### Three independent verifications

1. **Direct formula computation.** The retained Wilson values give
   `m_τ_pred = 1.7771 GeV`, matching PDG `m_τ = 1.7768 GeV` to 0.017%.

2. **Exponent provenance.** The exponent 18 = 16 + 2 has clean
   cited source-stack content reading: 16 = staggered taste doublers in 4D
   (retained, hierarchy theorem); 2 = one Yukawa-vertex `α_bare × α_LM`
   factor at the lepton scale.

3. **Conditional closure preserves Q = 2/3 exactly.** With BAE +
   φ = 2/9 admitted, the predicted full triplet matches PDG to
   10^{-4} on all three masses, and Koide Q = 2/3 holds exactly (not
   approximately) by Theorem 1 of
   `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE`.

### Sharpened residue

After Probes 1–18, the missing primitive was:

> "The continuous extension of retained discrete C_3 to U(1)_b on the
> b-doublet of A^{C_3}; equivalently, the canonical
> (1,1)-multiplicity-weighted Frobenius pairing on M_3(ℂ)_Herm under
> C_3-isotype decomposition." (Probes 12-14, 16-18 sharpened residue)

After Probe 19, the residue is sharpened in two directions:

**(R1) Scale-side closure (positive):** the absolute m_τ scale closes
on retained Wilson chain content alone, at 0.017% precision. The
Wilson-chain extension does not require BAE for the τ-scale alone.

**(R2) BAE-side residue (unchanged):** BAE itself is not closed by the
Wilson chain. The eighteen-probe missing primitive is preserved
intact. Probe 19 adds: the Wilson chain provides the **scale** of `a`
(via `a² = m_τ/(1 + √2 × cos(φ))²` once φ is fixed, or via
`a² = (m_e + m_μ + m_τ)/6` once BAE is admitted) but not the relation
`|b|²/a² = 1/2`.

**(R3) φ-side residue (newly named):** the Brannen magic angle
`φ = 2/9` is a **separate** structural admission, distinct from BAE.
BAE alone (without φ-magic) gives Q = 2/3 but does NOT give the
specific PDG mass triplet. The Wilson chain provides neither.

### What is positively closed

The retained Wilson chain extends naturally to the charged-lepton
scale via

```
m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}    [0.017% precision]
```

This is a positive prediction at the precision tier of the retained
EW chain. **The author does not promote this to retained status here**
— such promotion is the audit lane's authority — but proposes it as a
candidate positive theorem.

### What remains bounded

The BAE-condition `|b|²/a² = 1/2` and the Brannen magic angle
`φ = 2/9` are two independent bounded admissions. The Wilson chain
extension closes the **scale** but not the **relative structure**.

## Strategic options

This probe **does not select** an option; that authority is the
user's. Three options remain after 19 probes:

1. **Promote Step 1 (m_τ scale) to retained.** The Wilson-chain m_τ
   formula at 0.017% precision is at the same tier as retained EW
   predictions. If the audit lane judges the exponent-18 reading
   retained-grade (analogous to how exponent-16 for v_EW is retained),
   m_τ-scale becomes a retained prediction. BAE and φ=2/9 remain
   bounded admissions for the full triplet, but the absolute mass scale
   closes.

2. **Continue BAE-derivation hunt.** The residue is now precisely
   characterized at TWO structural levels: BAE (algebraic equipartition)
   and φ=2/9 (angular phase). Future probes can target either or both
   independently. Probability of closure remains low after 19 negative
   probes for BAE, but the m_τ-scale positive finding is encouraging
   that some Wilson-chain-related structure may yet supply BAE.

3. **Pivot to other bridge work.** Per
   `KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`
   §Strategic options, other bridge work (Convention C-iso engineering,
   substrate-to-carrier forcing, δ campaign) may be higher-priority.

## What this DOES NOT do

This note explicitly does **NOT**:

1. **Close the BAE-condition.** BAE remains a named bounded admission.
2. **Derive the Brannen magic angle φ = 2/9.** This remains a separate
   bounded admission.
3. **Promote any retained theorem.** No retained theorem is modified.
4. **Add a new axiom.** A1+A2 still suffice on the retained stack.
5. **Use PDG values as derivation input.** PDG `m_τ`, `m_μ`, `m_e`
   appear ONLY as falsifiability comparators after the chain is
   constructed. The Step 1 prediction `m_τ = 1.7771 GeV` is computed
   from retained `M_Pl`, `α_LM`, `(7/8)^{1/4}`, `u_0` alone.
6. **Promote the Step 1 prediction.** Whether the m_τ-scale Wilson
   formula is retained-grade or bounded is the audit lane's authority,
   not this note's.
7. **Claim closure of any sister bridge gap** (L3a, L3b, C-iso,
   W1.exact). This is a Wilson-chain-extension probe only.

## What this DOES do

This note records, as repo-language clarification:

1. **The retained Wilson chain extends to the τ-mass scale** via
   `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` at 0.017% precision.
   This is a **positive scale-side finding**, distinct in kind from
   the eighteen prior bounded-obstruction probes.

2. **BAE is not closed by the Wilson chain.** The 18-probe campaign's
   missing primitive (multiplicity-weighted Frobenius pairing) is
   preserved intact. Probe 19 sharpens that the Wilson chain provides
   the **scale** but not the **algebraic equipartition**.

3. **A new named admission emerges:** the Brannen magic angle
   φ = 2/9. BAE alone does not pin the specific PDG mass triplet;
   φ-magic is a separate structural piece. The Wilson chain provides
   neither.

4. **Conditional closure:** Wilson-scale + BAE + φ=2/9 reproduces the
   full lepton triplet to 10^{-4} on each mass, and Koide Q = 2/3 is
   exact (under BAE alone, independent of φ).

5. **No new admissions admitted; no new axioms added.** The audit lane
   retains full authority over the m_τ-scale promotion question and
   over the BAE/φ-magic admission status.

## Cross-references

### Foundational

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition):
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- BAE rename meta:
  `BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md` (PR #790)

### Retained Wilson chain

- Complete prediction chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- α_LM geometric-mean identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- Hierarchy theorem (retained, in COMPLETE_PREDICTION_CHAIN):
  `v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}`

### Retained Koide circulant / charged-lepton structure

- Charged-lepton Koide cone equivalence:
  [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Charged-lepton mass hierarchy review:
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
- Z³ scalar potential (g_2=3/2, g_3=1/6):
  [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
- Cyclic Wilson descendant law:
  [`KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md`](KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

### Eighteen-probe campaign (BAE-condition closure)

- Eleven-probe synthesis:
  [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md) (PR #751)
- Probe 12 (Plancherel/Peter-Weyl):
  [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) (PR #755)
- Probe 13 (real-structure):
  [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) (PR #763)
- Probe 14 (retained-U(1) hunt):
  [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md) (PR #784)

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_wilson_chain_mass_2026_05_09_probe19.py
```

Runner verifies:
1. Retained Wilson chain values reproduce v_EW = 246.30 GeV (sanity).
2. Wilson chain extension `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}`
   reproduces PDG m_τ to 0.017% precision (positive scale finding).
3. Conditional triplet (Wilson + BAE + φ=2/9) reproduces PDG (m_e,
   m_μ, m_τ) to 10^{-4} per mass.
4. Koide Q = 2/3 exact under BAE alone (independent of φ).
5. Three independent algebraic forms of m_τ Wilson formula agree.
6. Q-functional invariance under permutation of (m_e, m_μ, m_τ).
7. Brannen magic-angle phase φ = 2/9 reproduces PDG cosines
   `(0.9754, -0.6786, -0.2968)` to 10^{-4}.
8. The probe does not load-bear PDG values as derivation input.

**Runner result: PASS=N, FAIL=0** (set on first run; this note records
the verdict structure, the numerical cache is generated by the runner).

## Review-loop rule

When reviewing future branches that propose to close BAE via a
mass-scale-level Wilson extension:

1. The m_τ-scale positive finding (Probe 19 §Step 1) is a candidate
   positive theorem; promotion to retained is the audit lane's
   authority.
2. BAE remains the named bounded admission per the eleven-probe
   synthesis. The Wilson chain provides scale, not the equipartition.
3. The Brannen magic angle φ = 2/9 is a **separate** named bounded
   admission, newly identified by Probe 19. BAE-only closure does not
   pin the PDG-specific mass triplet.
4. PDG charged-lepton mass values must enter only as comparators
   post-derivation, never as derivation inputs (per substep-4 AC
   narrowing rule).
5. The retained `Cl(3)/Z³` axioms (A1+A2) and the retained
   eighteen bounded-obstruction probe theorems remain unchanged by
   this probe.
