# Lane 1 — Hadron Mass Program

**Date:** 2026-04-26
**Status:** ACCEPTED CRITICAL OPEN SCIENCE LANE on `main`; no theorem or claim
promotion
**Science priority:** HIGHEST. Bounded confinement + bounded √σ does not
satisfy hadron-mass retention.
**Approachability:** Tier B-C (1–6 months for first results; full closure 6–18 months)
**Primary closure targets:** retained `m_p`, `m_n`, `m_pi`, hadron spectroscopy,
and form-factor derivation paths.
**First parallel-worker target:** reduce the lane to a retained pion/proton
mass theorem plan using current confinement, α_s running, and Lane 3 quark-mass
dependencies.
**Non-claim boundary:** this file opens the lane only; it does not derive any
hadron mass.

## 2026-04-27 Dependency Firewall

The [Hadron Lane 1 confinement-to-mass firewall](../../HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md)
records the current no-go boundary for this lane. Retained `T = 0`
confinement and the bounded `sqrt(sigma)` readout are prerequisites for
hadron physics, not retained mass-spectrum closure.

The firewall blocks any upgrade of `sqrt(sigma)` into `m_pi`, `m_p`, `m_n`, or
hadron spectroscopy unless a branch also supplies the missing light-quark
masses, chiral inputs such as GMOR data, hadronic running/matching, and
dimensionless spectral coefficients or an ab-initio lattice-QCD-equivalent
computation.

## 1. Missing-science framing

The framework still needs direct answers to:

- "What does the framework predict for the proton mass?"
- "What about the pion mass and chiral symmetry breaking?"
- "What is the K, ρ, B-meson mass spectrum?"
- "What are the form factors for B → π, B → D*, kaon decays?"

**The current package has confinement T=0 retained as a structural theorem and
√σ ≈ 465 MeV as a bounded numerical readout. This does NOT constitute
"hadron physics derived."**

This is a direct missing-science lane for a TOE claim. Quantitative hadron
observables have to be retained or the QCD sector remains incomplete.

## 2. Current state of repo content

### Retained

- `T = 0` confinement of the graph-first SU(3) gauge sector
  ([CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md))
- α_s(M_Z) = 0.1181 (retained quantitative)
- Quark-lepton anomaly cancellation (recent SM gauge cluster)

### Bounded

- √σ ≈ 465 MeV (5.6% above PDG 440 ± 20 MeV) via low-energy EFT bridge +
  screening corrections
- BH entropy / RT ratio companion (with retained Widom no-go)

### Scaffold-only or absent

- Pion mass m_π — no derivation
- Proton mass m_p — no derivation
- Neutron mass m_n — no derivation
- Kaon, ρ, B-meson masses — no derivations
- Hadron form factors — no derivations
- Hadron spectroscopy — no quantitative results

## 3. Derivation targets

### 3A. Pion mass via Gell-Mann-Oakes-Renner (chiral SB)

The standard relation is:

```
m_π² f_π² = (m_u + m_d) Σ
```

where Σ is the chiral condensate and f_π is the pion decay constant.

**What the framework needs to retain:**
- Quark masses m_u, m_d (depends on Lane 3 — quark mass retention)
- Chiral condensate Σ — derivable from staggered-Dirac partition on Cl(3)/Z³
- Pion decay constant f_π — derivable from chiral symmetry breaking pattern

**Approachability:** Tier B once Lane 3 lands. Standard lattice chiral perturbation
theory applies.

### 3B. Proton / neutron mass via ab initio QCD

Standard lattice QCD methodology gives m_p, m_n from quark masses + α_s + lattice
infrastructure.

**What the framework needs to retain:**
- Quark masses (Lane 3)
- α_s at the relevant hadronic scale (already retained at M_Z; needs running to
  hadronic scale)
- Lattice action equivalence / matching to standard lattice QCD
- Standard hadron-mass extraction methodology (correlator analysis)

**Approachability:** Tier C. Substantial computational work but well-understood
methodology.

### 3C. Hadron spectroscopy

Following 3A and 3B, systematically extend to:
- Kaon masses (K, K*, K_1)
- ρ, ω mesons
- B and D mesons
- Baryon octet and decuplet
- Excited states

**Approachability:** Tier C. Routine lattice QCD once 3A and 3B land.

### 3D. Hadron form factors

Following 3C:
- B → π form factor
- K → π form factor
- Nucleon EM form factors
- Pion EM form factor

**Approachability:** Tier C. Standard lattice methodology.

### 3E. √σ retained promotion

**What the framework needs:** tighten the EFT bridge + screening corrections to
move √σ from bounded (5.6%) to retained (sub-percent or with explicit retention
budget like the YT/top transport lane has).

**Approachability:** Tier B. Incremental tightening of existing bounded content.

## 4. Existing scaffolding to build on

- [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) — confinement T=0 + bounded √σ
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — graph-first SU(3) closure
- [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) — α_s(M_Z) retained
- [QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md](../../QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md) — Lane 3 entry point
- Standard lattice QCD methodology (Wilson / staggered actions are explicitly
  in the framework's substrate language)

## 5. Recommended attack approach

**Phase 1 (after Lane 3 lands quark masses):**

1. **Pion mass via GMOR** — close 3A first; this is the lightest hadron and
   has the cleanest chiral-SB structure.
2. **√σ retained promotion (3E)** — incremental tightening; can run in parallel.

**Phase 2 (after Phase 1):**

3. **Proton mass ab initio** — close 3B. This is the highest-visibility hadron
   observable.
4. **Kaon, ρ, ω masses** — extend 3A methodology.

**Phase 3 (after Phase 2):**

5. **Baryon octet / decuplet** — systematic extension.
6. **Hadron form factors** — phenomenology lane.

## 6. Out of scope / will not claim

- This lane does NOT propose to derive QCD from scratch — the gauge sector is
  already retained.
- This lane does NOT propose to compete with PDG precision on every hadron
  mass — only to retain the major observables to standard lattice-QCD
  precision (1–5%).
- This lane does NOT address exotic hadrons (tetraquarks, pentaquarks,
  glueballs) in the initial scope.
- This lane does NOT address heavy-quark effective theory or NRQCD-style
  expansions in the initial scope.

## 7. Cross-references

- Depends on: Lane 3 (quark mass retention)
- Enables: Lane 4 (neutrino sector, indirectly via hadron-physics consistency
  checks like the kaon ε_K Jarlskog decomposition already retained)
- Enables: Lane 2 (atomic-scale, indirectly — atomic mass precision needs
  hadron scale precision via nuclear masses)
- Independent of: Lane 5 (Hubble constant), Planck pin, Koide closure

## 8. Reviewer questions

1. Should we attempt to retain m_p directly via existing lattice QCD methodology
   adapted to the framework substrate, or is there a shorter path through the
   framework's structural identities?
2. Is the GMOR-based pion mass route the right entry point, or should we
   attempt the proton mass first?
3. What hadron-mass precision target should we set as "retained" — 1%? 5%?
   PDG precision?
4. Should hadron-physics retention be a single lane or split into chiral-SB,
   ab-initio-QCD, spectroscopy, and form-factor sub-lanes?
