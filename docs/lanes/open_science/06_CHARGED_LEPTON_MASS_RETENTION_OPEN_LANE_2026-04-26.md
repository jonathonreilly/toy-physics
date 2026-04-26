# Lane 6 — Charged-Lepton Mass Retention (Full Closure)

**Date:** 2026-04-26
**Status:** ACCEPTED CRITICAL OPEN SCIENCE LANE on `main`; no theorem or claim
promotion
**Science priority:** HIGHEST. Tier 1 missing-science item #2 (charged-lepton
masses). Currently the only Tier 1 critical-open item without a dedicated
active lane; the Koide flagship lane covers ratios but not absolute scale.
**Approachability:** Tier A–B (Koide ratios in flight; V_0 absolute scale is
1–3 months of focused work on existing Ward-identity scaffolding).
**Primary closure targets:** retained absolute `m_e`, `m_μ`, `m_τ` derived
from one axiom — no PDG observational pin.
**First parallel-worker target:** construct the y_τ Ward identity on the
charged-lepton carrier (analog of the retained `y_t(M_Pl)/g_s(M_Pl) = 1/√6`
top-quark Ward identity). With the Koide ratios closure in flight providing
m_e/m_μ/m_τ ratios, a y_τ Ward identity pins the absolute lepton scale V_0
and chains to all three charged-lepton masses retained.
**Non-claim boundary:** this file opens the lane only; it does not derive any
charged-lepton mass.

## 1. Missing-science framing

The framework still needs direct answers to:

- "What does the framework predict for the electron mass?"
- "What about the muon and tau masses?"
- "Are the three charged-lepton masses derived from one axiom, or imported
  from PDG?"
- "What sets the absolute lepton mass scale?"

**The current package has the Koide flagship lane (Q = 2/3, δ = 2/9) in flight,
which addresses the ratio structure of the charged-lepton mass-square-root
vector v = (√m_e, √m_μ, √m_τ). But the overall lepton scale V_0 is separately
open, and without it the framework cannot retain absolute m_e, m_μ, m_τ
values — only the dimensionless ratios.**

The currently-active charged-lepton bounded package
([CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md))
imports a **3-real PDG observational pin** to fix all three masses absolutely.
This is the single most lethal "you import PDG numbers" attack in Tier 1.

This is a direct missing-science lane for a TOE claim. Lepton mass retention
is what an external particle physicist will ask about first, before any of
the other sectors.

## 2. Current state of repo content

### Retained

- y_t(M_Pl)/g_s(M_Pl) = 1/√6 exact lattice-scale Ward identity (top-quark
  template for generation-stratified Ward identities)
- Three-generation matter structure (anomaly-forced + hw=1 observable theorem)
- v = 246.283 GeV electroweak hierarchy (the ambient EW scale)
- Cl(3) bivector → SU(2) native gauge structure
- Generation-color and EW A4 bridges (recent landing 2026-04-25)
- α_LM geometric-mean identity

### In flight (Koide flagship lane)

The [Charged-lepton Koide / Brannen bridge open support lane](../ACTIVE_WORKING_LANES_2026-04-26.md)
addresses:

- Q = 2/3 closure (source-domain selector theorem target)
- δ = 2/9 closure (period convention / Euclidean rotation interpretation)

These together pin v's direction in R³ modulo overall scale. **Closure of the
Koide flagship lane retains the dimensionless ratios m_e/m_μ and m_μ/m_τ.**
It does NOT retain the absolute scale.

### Bounded

- Charged-lepton mass-hierarchy observational-pin closure
  ([CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md))
  — bounded package on a 3-real PDG observational pin
- Compatibility with Koide Q = 2/3 (algebraic equivalence retained on the
  hw=1 triplet, structural cone-forcing not retained)

### Absent

- Overall lepton scale V_0 derivation (the "lepton-scale" item separately
  flagged as open in the Koide flagship lane CLAIMS_TABLE entry)
- y_τ Ward identity (analog of the retained y_t Ward identity, for the τ
  generation)
- Generation-stratified Yukawa structure for charged leptons (y_e, y_μ, y_τ
  individually)
- Absolute m_e from framework first principles
- Absolute m_μ from framework first principles
- Absolute m_τ from framework first principles

## 3. Derivation targets

### 6A. Koide ratios closure (in flight via flagship lane)

**Target:** retain Q = 2/3 and δ = 2/9 via the existing flagship-lane work
(source-domain selector theorem for Q; Euclidean rotation interpretation for
δ).

**Status:** in flight. Tracked in the [Charged-lepton Koide / Brannen bridge
open support lane](../ACTIVE_WORKING_LANES_2026-04-26.md). This lane is a
**dependency** of the present Lane 6, not duplicated work.

**Approachability:** Tier A–B for δ via rotation angle; Tier B for Q via
source-domain selector.

### 6B. y_τ Ward identity construction

**Target:** construct a τ-generation Ward identity analogous to the retained
top-quark Ward identity y_t(M_Pl)/g_s(M_Pl) = 1/√6, fixing the τ Yukawa at
the lattice scale.

**What the framework needs:**
- Lift the YT Ward derivation
  ([YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md))
  to the third generation of the charged-lepton sector
- Use the retained hw=1 triplet structure + Cl(3) bivector → SU(2) native
  gauge content to construct the analogous Ward identity for the τ
- Identify the structural rational analog of `1/√6` for the τ generation

**Approachability:** Tier B (1–3 months). The y_t derivation is the
template; the lift uses retained content.

### 6C. V_0 absolute lepton scale from y_τ Ward identity

**Target:** derive the overall lepton scale V_0 such that m_τ = y_τ · V_0
where y_τ is fixed by 6B.

**What the framework needs:**
- y_τ retained (6B)
- Connection to the EW scale v = 246.283 GeV (already retained) via the
  Higgs Yukawa coupling structure, OR
- An independent V_0 anchor from generation-stratified Ward content

**Approachability:** Tier A–B. Automatic chain once 6B lands.

### 6D. Generation-stratified Yukawa structure for charged leptons

**Target:** retain y_e, y_μ, y_τ separately as ratios y_e/y_τ, y_μ/y_τ
chained off the y_τ Ward identity (6B) and the Koide ratios (6A).

**Approachability:** Tier A–B. Automatic from 6A + 6B.

### 6E. Absolute m_e, m_μ, m_τ retention

**Target:** chain absolute charged-lepton masses from 6B (y_τ), 6C (V_0),
and 6A (ratios).

```
m_τ = y_τ · V_0
m_μ = y_τ · V_0 · (m_μ/m_τ)   [from Koide ratios]
m_e = y_τ · V_0 · (m_e/m_τ)   [from Koide ratios]
```

**Approachability:** Tier A. Automatic chain once 6A + 6B + 6C land.

### 6F. Cross-validation against bounded charged-lepton package

**Target:** verify the now-retained absolute charged-lepton masses agree
with the existing bounded package
([CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md))
to PDG precision.

**Approachability:** Tier A. Internal consistency check.

## 4. Existing scaffolding to build on

- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
  — top-quark Ward identity template
- [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  — bounded charged-lepton compatibility package
- [KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md](../../KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md)
  — Koide flagship lane (in flight)
- [KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md](../../KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
  — Brannen geometry / 2-plane rotation interpretation
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](../../THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — three-generation hw=1 structure
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — v hierarchy retained
- [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — coupling-chain identity
- The retained Cl(3) bivector → SU(2) gauge structure

## 5. Recommended attack approach

**Phase 1 (parallel with Koide flagship closure):**

1. **6B: y_τ Ward identity construction.** Tier B, 1–3 months. Uses the
   y_t Ward template + retained three-generation structure. Independent
   of the Koide closure timing — can start immediately.

**Phase 2 (after Koide flagship closure + 6B):**

2. **6C: V_0 from y_τ Ward.** Tier A–B. Automatic chain.
3. **6D: Generation-stratified Yukawa structure.** Tier A–B. Automatic.
4. **6E: Absolute m_e, m_μ, m_τ retention.** Tier A. Automatic.

**Phase 3:**

5. **6F: Cross-validation against bounded package.** Tier A. Consistency check.

**Optional Phase 4 (post-closure):**

6. Promote the bounded charged-lepton compatibility package
   ([CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md))
   to retained status, removing the 3-real PDG observational pin from the
   bounded-companion list.

## 6. Out of scope / will not claim

- This lane does NOT propose to derive Koide ratios independently of the
  Koide flagship lane — it depends on that lane closing.
- This lane does NOT propose to derive PMNS angles or neutrino mixing
  from the charged-lepton sector.
- This lane does NOT address charged-lepton precision QED tests (Lamb
  shift, fine structure, hyperfine) — those are Lane 2 (atomic-scale).
- This lane does NOT address muon g-2 — that is a separate BSM-search
  observable downstream of Lane 1 (hadron) + Lane 2 (atomic-scale).

## 7. Cross-references

- **Depends on:** Koide flagship lane (for Q, δ ratios) — see
  [Charged-lepton Koide / Brannen bridge open support lane](../ACTIVE_WORKING_LANES_2026-04-26.md)
- **Enables:** Lane 2 (atomic-scale) — once m_e is retained, the H/He
  scaffold can substitute framework-derived m_e and the Rydberg constant
  + atomic spectra become Tier A substitution exercises
- **Connects to:** Lane 3 (quark mass retention) — the y_τ Ward identity
  construction is structurally analogous to the generation-stratified
  Yukawa Ward identities needed for quark masses (Lane 3 sub-target 3C)
- **Cross-validates:** the V_cb cross-sector bridge `Q_ℓ · α_s² = 4|V_cb|²`
  becomes a retained closure once Q is retained via the Koide flagship lane
- **Independent of:** Lanes 4 (neutrino), 5 (Hubble), Planck-scale absolute
  normalization

## 8. Reviewer questions

1. Is the y_τ Ward identity (6B) the right entry point for V_0 derivation,
   or is there a cleaner direct V_0 anchor through the EW scale v?
2. Should the Koide flagship lane be merged with this Lane 6, or kept as a
   dependency? (Current proposal: keep separate; Koide is the ratios
   sub-component, Lane 6 is the full closure including absolute scale.)
3. Is the y_τ Ward construction approach the right route, or should the
   framework attempt a direct generation-stratified Ward identity covering
   all three lepton generations simultaneously?
4. What precision target should "retained m_e, m_μ, m_τ" mean — sub-percent?
   PDG precision (10⁻⁸ for m_e)?
5. Should the bounded charged-lepton package be promoted to retained status
   in Phase 4, or kept as a separate "compatibility cross-check" surface?
