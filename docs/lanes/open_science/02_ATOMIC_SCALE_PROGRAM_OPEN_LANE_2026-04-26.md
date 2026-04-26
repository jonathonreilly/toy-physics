# Lane 2 — Atomic-Scale Predictions

**Date:** 2026-04-26
**Status:** ACCEPTED CRITICAL OPEN SCIENCE LANE on `main`; no theorem or claim
promotion
**Science priority:** HIGH. Hydrogen/Rydberg/fine-structure predictions are
basic quantitative checks once absolute charged-lepton scales are available.
**Approachability:** Tier A post-Koide (substitution exercise) / Tier B pre-Koide
**Primary closure targets:** retained Rydberg constant, hydrogen ground-state
energy, fine-structure corrections, and Lamb/hyperfine follow-ons.
**First parallel-worker target:** isolate the exact dependency chain from
`m_e`, α, and retained electroweak/QED inputs to the first Rydberg theorem.
**Non-claim boundary:** current atomic content remains scaffold-only until
those dependencies are retained.

## 1. Missing-science framing

The framework still needs direct answers to:

> "Does the framework reproduce the Rydberg constant from first principles?
> Does it predict -13.6 eV without textbook inputs?"

Plus follow-ups:

- "What about Lamb shift?"
- "Fine structure α²?"
- "Hyperfine structure of hydrogen?"
- "Helium ground state energy?"
- "Larger atoms — periodic table closure?"
- "Muon g-2 — current BSM-active observable?"

**The current package has [ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md](../../ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md)
as a bounded scaffold lane that uses TEXTBOOK INPUTS (m_e, e, ℏ) — explicitly
NOT framework-derived.** The lane exists specifically to scope the gap; it
does not close it.

## 2. Current state of repo content

### Retained (relevant to atomic scale)

- 1/α_EM(M_Z) = 127.67 (sub-percent agreement)
- v = 246.283 GeV (EW hierarchy retained)
- y_t Ward identity (top sector)

### Bounded / scaffold-only

- ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE — uses textbook m_e, e, ℏ; produces -13.6 eV
  via standard radial Schrödinger eigensolver but NOT from framework inputs

### Absent

- m_e from framework (depends on Koide closure + V_0 retention)
- Rydberg constant from framework first principles
- Lamb shift derivation
- Hyperfine structure
- Muon g-2 prediction
- Larger-atom predictions
- Molecular ground states

## 3. Derivation targets

### 2A. Substitute framework m_e into existing eigensolver

**Once Koide Q + δ + V_0 close, m_e is retained.** Substitute into the existing
H/He eigensolver harness and verify:
- Hydrogen ground state = -13.6 eV (Bohr formula)
- Hydrogen Lyman series energies
- Helium ground state ≈ -79 eV
- Ionization energies for H, He, Li, ..., periodic table sample

**Approachability:** Tier A (~1 week) once m_e retained. Pure substitution.

### 2B. Lamb shift via QED on framework substrate

Standard QED Lamb shift calculation requires:
- m_e (Lane 3 / Koide closure)
- α_EM (retained)
- QED self-energy / vacuum polarization corrections

**What the framework needs:** retain the QED machinery on the framework
substrate — this is mostly automatic given retained α_EM and m_e, but the
specific QED loop calculations need to be performed in the framework's
language.

**Approachability:** Tier B (1–3 months).

### 2C. Fine structure / hyperfine

Standard atomic physics with relativistic corrections + spin-orbit + magnetic
hyperfine. Requires m_e, m_p, α_EM, μ_p (proton magnetic moment).

**Depends on Lane 1 (proton magnetic moment) for hyperfine.**

**Approachability:** Tier B (after Lane 1 partial closure).

### 2D. Muon g-2 prediction

Standard hadronic vacuum polarization calculation requires:
- m_μ (Koide closure)
- α_EM
- Hadronic loop contributions (depends on Lane 1)

**This is a currently-active BSM search lane.** A clean prediction here would
be a major quantitative closure point.

**Approachability:** Tier B-C.

### 2E. Larger atoms + periodic table

Systematic extension of 2A using standard quantum chemistry methodology with
framework-derived constants.

**Approachability:** Tier B. Standard with framework inputs.

### 2F. Molecular ground states

H_2, HeH⁺, He_2, etc. via standard quantum chemistry.

**Approachability:** Tier B-C.

## 4. Existing scaffolding to build on

- [ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md](../../ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md) —
  existing eigensolver harness with textbook inputs
- [BOUND_STATE_SELECTION_NOTE.md](../../BOUND_STATE_SELECTION_NOTE.md) —
  Coulomb scaling as dimension-selection diagnostic
- α_EM retained (EW package)
- 1/α_EM(M_Z) = 127.67
- Standard QED machinery is implicit in the framework's gauge content

## 5. Recommended attack approach

**Phase 1 — Fast win (post-Koide):**

1. **2A: Substitute framework m_e into eigensolver.** Pure substitution
   exercise. Produces -13.6 eV from one axiom. **Visceral defense.**

**Phase 2 (after Lane 1 partial closure):**

2. **2B: Lamb shift via QED.**
3. **2C: Fine structure / hyperfine.**
4. **2D: Muon g-2 prediction.**

**Phase 3:**

5. **2E: Larger atoms.**
6. **2F: Molecular ground states.**

## 6. Out of scope / will not claim

- This lane does NOT propose to derive standard QM from scratch — the
  framework's quantum content is already retained (Born forced, CPT, Bell).
- This lane does NOT propose to compete with QED precision tests at 10⁻¹²
  — the framework will reproduce 1/α_EM at sub-percent, not at QED precision.
- This lane does NOT address strongly correlated systems (high-T_c
  superconductivity, quantum Hall, etc.) in initial scope.

## 7. Cross-references

- Depends on: Koide closure (for m_e); Lane 1 partial (for proton magnetic
  moment, hadronic vacuum polarization)
- Enables: defense against the "you can't even do hydrogen" attack
- Independent of: Lane 5 (Hubble), Planck pin

## 8. Reviewer questions

1. Should 2A be considered a fast-win Tier A target post-Koide, treated as
   a single substitution-and-verification theorem note?
2. What atomic-precision target should the lane target — sub-percent on
   Rydberg? QED-precision on Lamb shift? Standard atomic-physics precision?
3. Should muon g-2 be its own dedicated lane given current BSM-search
   context, or scoped within this atomic-scale lane?
4. Should the existing atomic-scaffold lane be folded into this open lane
   or remain as an exploratory scaffold?
