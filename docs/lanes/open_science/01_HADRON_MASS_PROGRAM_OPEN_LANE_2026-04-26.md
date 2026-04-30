# Lane 1 — Hadron Mass Program

**Date:** 2026-04-26
**Status:** ACCEPTED CRITICAL OPEN SCIENCE LANE on `main`; no theorem or claim
promotion
**Science priority:** HIGHEST. Bounded confinement + bounded √σ does not
satisfy hadron-mass retention.
**Approachability:** Tier B-C (1–6 months for first results; full closure 6–18 months)
**Primary closure targets:** retained `m_p`, `m_n`, `m_pi`, hadron spectroscopy,
and form-factor derivation paths.
**First parallel-worker target:** complete. The lane now has a support
roadmap, a `sqrt(sigma)` retention-gate audit, and a Banks-Casher `Sigma`
scoping no-go.
**Current highest-leverage targets:** (i) close the repaired `(B2)` gate for
`sqrt(sigma)` at `beta=6.0`, `N_f=2+1`: first define the full-QCD dynamical
observable, then import or compute its value with a residual budget; (ii) have
Lane 3 retain the combined `m_u + m_d` light-quark sum, which is the shortest
unblocker for the GMOR pion route once `Sigma` and `f_pi` are addressed.
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

### Support landed 2026-04-28

- [HADRON_MASS_LANE1_THEOREM_PLAN_SUPPORT_NOTE_2026-04-27.md](../../HADRON_MASS_LANE1_THEOREM_PLAN_SUPPORT_NOTE_2026-04-27.md)
  maps the lane into phase-ordered dependencies: `sqrt(sigma)` gate work
  can proceed in parallel; `m_pi` via GMOR needs Lane 3 `m_u + m_d` plus
  `Sigma` and `f_pi`; proton/spectroscopy/form factors wait on broader
  quark-mass and lattice-QCD bridges.
- [HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md](../../HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md)
  decomposes the bounded `sqrt(sigma)` readout into the `(B1)`-`(B5)`
  residual budget and isolates `(B2)` quenched-to-dynamical screening as
  the dominant numerical gate.
- [HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md](../../HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md)
  records the Banks-Casher `Sigma` no-active-route result on current
  framework content: existing `L=4,6` data is finite-volume/lattice-free,
  and no structural identity currently pins `rho_Dirac(0)`.

### Support landed 2026-04-30

- [HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md](../../HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md)
  repairs the `(B2)` target: the rough x0.96 screening factor cannot promote
  `sqrt(sigma)`, a PDG backsolve is circular, and a literal asymptotic
  full-QCD string tension is underdefined because full QCD strings break.
  The gate is now split into `(B2a)` observable definition and `(B2b)` bridge
  value plus residual budget.
- [HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md](../../HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md)
  tests modern full-QCD static-energy inputs. The bridge is materially stronger
  than rough x0.96, but still bounded: `r0`/`r1` are the cleanest `N_f=2+1`
  force-scale observables, while finite-window `sigma` carries a
  static-potential convention split and the `(B5)` framework link remains open.

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

**Phase 1 (now, in parallel with Lane 3):**

1. **`sqrt(sigma)` retained-with-budget gate (3E)** — close repaired `(B2)`:
   define the full-QCD observable first (pre-breaking effective tension,
   static-force scale, or static-energy fit window), then import or compute
   the `N_f=2+1` value with an uncertainty budget. Keep `(B5)`
   framework-to-standard-YM identification as an explicit residual until
   large-volume Wilson-loop/Creutz-ratio checks close it.
2. **`Sigma` / `f_pi` support work** — Banks-Casher is currently a no-active
   route without large-volume lattice data or a new structural identity; `f_pi`
   remains a companion chiral-SB normalization target.
3. **Lane 3 coordination** — prioritize retained `m_u + m_d` as the combined
   quark-mass sum that first unlocks 3A.

**Phase 2 (after Lane 3 retains `m_u + m_d` and `Sigma`, `f_pi` are addressed):**

4. **Pion mass via GMOR** — close 3A first; this is the lightest hadron and
   has the cleanest chiral-SB structure.

**Phase 3 (after Lane 3 full quark-mass closure + lattice-QCD bridge):**

5. **Proton/neutron mass ab initio** — close 3B. This is the highest-visibility
   hadron observable.
6. **Kaon, ρ, ω masses and broader spectroscopy** — extend 3A/3B methodology.
7. **Hadron form factors** — phenomenology lane.

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
