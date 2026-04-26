# Critical Open Science Lanes

**Date:** 2026-04-26
**Status:** ACCEPTED OPEN SCIENCE LANE PACKAGE on `main`. Not retained,
not bounded, and not on the manuscript surface. This package records five
missing science lanes that need active work.

## Why this package exists

The project's [CLAIMS_TABLE.md](../../publication/ci3_z3/CLAIMS_TABLE.md) currently
lists "Open Flagship Lane" entries that reflect the project's own audit
priorities:

- Cross-sector Koide/CKM `V_cb` bridge
- Charged-lepton Koide (`Q = 2/3`, `δ = 2/9`)
- Plus several CKM-side support bridges for the Koide question

These are real and worth closing. But they are **project-internal scoping**,
not the full missing-science surface of the repo. The bounded-companion and
scaffold-lane categories absorb significant content that still needs direct
derivation work.

This package accepts **six critical open science lanes** on `main`, each with
explicit derivation targets, existing scaffolding, and recommended attack
approaches. **It does not promote any claim or close any theorem.** It only
records the work that still needs to be done.

## The six lanes

| # | Lane | Science priority | Approachability | Status today |
|---|---|---|---|---|
| 1 | Hadron mass program (m_p, m_π, hadron spectroscopy) | HIGHEST | Tier B-C | confinement T=0 retained; √σ ≈ 465 MeV bounded; m_p, m_π not derived |
| 2 | Atomic-scale predictions (Rydberg, Lamb shift, fine structure) | HIGH-VISCERAL | Tier A (post-Koide) / B (pre-Koide) | scaffold uses textbook inputs |
| 3 | Quark masses retention (5 quark masses) | HIGHEST | Tier B-C | bounded companion via threshold-local + up-type extension |
| 4 | Neutrino quantitative closure (m_ν, Δm², Majorana phases) | HIGH | Tier B-C | "different carriers"; bounded |
| 5 | Hubble constant H_0 derivation (cosmology matter bridge) | HIGH | Tier B | external input; structural identities retained |
| 6 | Charged-lepton mass retention (full closure: ratios + V_0) | HIGHEST | Tier A-B | Koide flagship lane in flight (ratios); V_0 absolute scale separately open |

Per-lane open-lane documents:

- [`01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`](./01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md)
- [`02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md`](./02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md)
- [`03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md`](./03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md)
- [`04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`](./04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md)
- [`05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`](./05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md)
- [`06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md`](./06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md)

Each lane stub is intended to be a parallel-worker handoff surface. The top
metadata block names the primary closure targets, the first worker target, and
the non-claim boundary. The body preserves the current retained/bounded/scaffold
state, derivation targets, scaffolding, and recommended attack path.

Lane 6 (charged-lepton mass retention) was added 2026-04-26 to close the gap
where Tier 1 missing-science item #2 had no dedicated active lane. The Koide
flagship lane (in `ACTIVE_WORKING_LANES_2026-04-26.md`) covers the ratios
sub-target; Lane 6 holds the full charged-lepton mass retention scope
including the V_0 absolute scale. Lane 6 is a parent surface for the Koide
flagship work, not a duplicate of it.

## Common scoping principles for all six lanes

Each open-lane document follows the same structural template:

1. **Missing-science framing.** What the repo still cannot derive in this
   sector.
2. **Current state of repo content.** What's retained, bounded, scaffold-only,
   or absent — pulled from the live `origin/main` package.
3. **Derivation targets.** Specific named theorems / identities the lane would
   need to retain to close the lane.
4. **Existing scaffolding to build on.** Concrete file references to retained
   theorem notes that provide ingredients for the derivation targets.
5. **Approachability rating.** Tier A (1–4 weeks), Tier B (1–4 months),
   Tier C (4+ months / research program).
6. **Recommended attack approach.** Concrete sequence of theorem steps.
7. **Out-of-scope / will not claim.** What the lane explicitly does NOT propose
   to close, to keep scope honest.
8. **Cross-references.** Connections to other lanes and to the manuscript surface.

## Full Missing-Science Inventory

This is the **complete** list of missing-science items captured in this pass,
ranked by scientific impact and approachability. The six active lanes above
are the top six by priority × approachability product. The remaining items are
deferred to follow-on lanes — they remain open but are either lower priority,
lower approachability on the current scaffolding, or already addressed by
non-active-lane mechanisms in the framework.

The status labels in this inventory are tracking shorthand only. They do not
create new authority, upgrade support notes, or supersede the canonical claim
ledger and theorem notes. If this inventory conflicts with a retained/support
status elsewhere, the canonical theorem surface wins.

### Tier 1 — Highest-priority missing science

| # | Item | Status | In active package? |
|---|---|---|---|
| 1 | **Quark masses (m_u, m_d, m_s, m_c, m_b)** | bounded companion only | **Active — Lane 3** |
| 2 | **Charged-lepton masses (m_e, m_μ, m_τ)** | bounded via 3-real PDG pin; Koide closure in flight | **Active — Lane 6** (parent lane covering ratios + V_0); Koide flagship lane is the ratios dependency |
| 3 | **Proton / hadron masses (m_p, m_π, m_K, etc.)** | bounded via confinement only | **Active — Lane 1** |
| 4 | **Atomic-scale predictions (Rydberg / -13.6 eV)** | scaffold uses textbook inputs | **Active — Lane 2** |
| 5 | **Neutrino sector quantitative (m_ν, Δm², Majorana phases)** | "different carriers" / bounded | **Active — Lane 4** |

### Tier 2 — HIGH science priority

| # | Item | Status | In active package? |
|---|---|---|---|
| 6 | **Hubble constant H_0** | external input | **Active — Lane 5** |
| 7 | **Inflation mechanism** | bounded primordial spectrum only | **Deferred — Lane 5E (folded)** |
| 8 | **Muon g-2 prediction** | absent | **Deferred — Lane 2D follow-on** |
| 9 | **Strong-field gravity continuum** | perturbative only (adversarial review §1) | **Deferred — separate research lane** |
| 10 | **Higgs mass m_H retention** | derived budget at 0.1% | **Deferred — Phase 2 of matter mass program** |
| 11 | **W boson mass M_W retention** | bounded companion at 0.23% | **Deferred — Phase 2 of matter mass program** |
| 12 | **BBN abundance ratio derivation** | absent | **Deferred — separate cosmology lane** |
| 13 | **CMB anisotropy spectrum quantitative comparison** | bounded primordial only | **Deferred — separate cosmology lane** |
| 14 | **Dark matter particle / detection mechanism** | DM relic ratio R = 5.48 retained, but not particle ID | **Deferred — DM closed package follow-on** |
| 15 | **Lattice scale ⟨P⟩ = 0.5934 dependence on action choice** | computed via Monte Carlo | **Deferred — methodology audit lane** |

### Tier 3 — MEDIUM science priority

| # | Item | Status | In active package? |
|---|---|---|---|
| 16 | **Black hole interior physics / singularities** | no quantitative | **Deferred — strong-field gravity research lane** |
| 17 | **Hawking radiation quantitative** | no quantitative | **Deferred — same lane as 16** |
| 18 | **Information paradox** | no statement | **Deferred — same lane as 16** |
| 19 | **BMS / asymptotic symmetries** | open | **Active separately — Pate co-author P4 paper target** |
| 20 | **Decoherence law universal** | bounded | **Deferred — Gate A in older review-hardening backlog** |
| 21 | **Galaxy rotation curves / DM detection cross-section** | absent | **Deferred — DM follow-on** |
| 22 | **Hierarchy stability under quantum corrections** | implicitly retained via v derivation | **Argued retained** (the v derivation is not just tree-level) |
| 23 | **Vacuum stability quantitative** | qualitative result only | **Deferred — Phase 2 matter mass** |
| 24 | **Form factors (B → π, K → π, etc.)** | absent | **Deferred — Lane 1 follow-on** |
| 25 | **Hadron spectroscopy (excited states)** | absent | **Deferred — Lane 1 follow-on** |

### Tier 4 — LOW-MEDIUM science priority / specialist concerns

| # | Item | Status | In active package? |
|---|---|---|---|
| 26 | **Lamb shift / fine structure / hyperfine** | absent | **Deferred — Lane 2 follow-on** |
| 27 | **Heavy-quark effective theory expansions** | absent | **Deferred — Lane 1/3 follow-on** |
| 28 | **Tetraquarks / pentaquarks / glueballs** | absent | **Deferred — Lane 1 follow-on** |
| 29 | **Sterile neutrino / eV-scale anomalies** | absent | **Deferred — Lane 4 follow-on** |
| 30 | **0νββ rates** | absent (depends on Majorana confirmation) | **Deferred — Lane 4 follow-on** |
| 31 | **Strongly correlated systems** | absent | **Deferred — Lane 2 follow-on** |
| 32 | **Modified gravity tests (solar-system PPN)** | implicitly in retained GR | **Argued retained** |
| 33 | **Gravitational-wave templates beyond linear** | absent | **Deferred — strong-field gravity research lane** |
| 34 | **Axions / dark sector beyond DM relic** | absent | **Deferred — separate dark-sector lane** |
| 35 | **Quantitative leptogenesis baryon asymmetry** | DM closed package gives δ_CP forecast | **Argued partial via DM closed package** |

### Tier 5 — Items the framework already retains or argues away

These are items where the framework either has retained content or has argued
the item away structurally (acknowledged for completeness):

| # | Item | Resolution |
|---|---|---|
| 36 | Why 3 generations | DERIVED (April 24-25 anomaly cluster) |
| 37 | Why 3+1 dimensional spacetime | DERIVED (anomaly-forced 3+1) |
| 38 | Why SM gauge group SU(3)×SU(2)×U(1) | DERIVED (April 24-25 anomaly cluster + native SU(2) + graph-first SU(3)) |
| 39 | Hierarchy problem | DERIVED (v = M_Pl × (7/8)^(1/4) × α_LM^16) |
| 40 | Strong CP θ-angle = 0 | RETAINED (universal θ-EDM vanishing) |
| 41 | CP violation in flavor | RETAINED (full CKM atlas/axiom closure in α_s + rationals) |
| 42 | Dark energy w = -1 | RETAINED (exactly) |
| 43 | Cosmological constant Λ value | RETAINED structural identity (m_g² = 2Λ) |
| 44 | Dark matter abundance ratio R = Ω_DM/Ω_b | RETAINED (5.48 from group theory, 0.2%) |
| 45 | Born rule / I_3 = 0 | DERIVED |
| 46 | CPT | EXACT |
| 47 | Bell inequality violation | DERIVED |
| 48 | Emergent Lorentz at low energy | DERIVED + exact 1+1D and 3+1D continuum boost-covariance |
| 49 | Discrete-to-continuum gravity | RETAINED on canonical textbook target |
| 50 | Top quark mass m_t | RETAINED (172.57 GeV at 0.07%) |

### Why these specific six lanes are active

The six active lanes are selected by:

> A lane is **included as active** if and only if (a) it is a top-priority
> open science question, AND (b) closing it produces meaningful change in the
> framework's defensibility as a TOE candidate, AND (c) closing it is
> approachable on a months-to-year timescale given existing repo scaffolding.

All five Tier 1 items now have active-lane coverage:
- Tier 1 item 1 (quark masses) → Lane 3
- Tier 1 item 2 (charged-lepton masses) → **Lane 6** (added 2026-04-26;
  parent lane with Koide flagship as the ratios dependency)
- Tier 1 item 3 (hadron masses) → Lane 1
- Tier 1 item 4 (atomic-scale) → Lane 2
- Tier 1 item 5 (neutrino sector) → Lane 4
- Tier 2 item 6 (H_0) → Lane 5

All other Tier 2-4 items are deferred — they remain open and should be tracked
as such. Any deferred item can be moved into active status if priorities change
or if a worker finds a tractable attack path.

The Tier 5 items are listed for completeness — they show what the framework
has already retained or argued away from the missing-science inventory, so the
total picture is honest rather than only listing the open items.

## Recommended priority order (subject to review)

1. **Lane 6 (charged-lepton mass retention)** first — Koide flagship is in
   flight; the y_τ Ward identity (the V_0 dependency) is the highest-leverage
   single derivation in flight on the matter-mass program. Closing 6 unlocks
   Lane 2 as a Tier A substitution exercise.
2. **Lane 2 (atomic-scale)** in parallel with 6 — once Lane 6 lands m_e,
   substituting into the existing H/He scaffold is a Tier A exercise.
   **Visceral defense against "you can't even do hydrogen" attack.**
3. **Lane 5 (Hubble)** in parallel — has the most recent structural-identity
   landings (single-ratio inverse reconstruction, FRW kinematic reduction,
   R_base = 31/9, N_eff, matter-radiation equality). Closer to closure than
   it looks.
4. **Lane 3 (quark masses)** — substantial, but the up-type amplitude
   shortlist (7/9, √(3/5), atan(√5)−√5/6, ...) is short and the down-type
   5/6 NP proof has a clear taste-staircase route.
5. **Lane 1 (hadron masses)** — depends on Lane 3. After quark masses retain,
   standard lattice-QCD methodology applies and m_π via chiral SB +
   m_p ab initio QCD become tractable.
6. **Lane 4 (neutrino)** — substantial structural extension, but the DM
   closed package gives δ_CP + θ_23 forecast as cross-validation. Likely
   the longest lane to close.

## Relationship to existing project lanes

This package does NOT replace or override the existing project Open Flagship
Lane scoping. Specifically:

- The Koide closure work (Q = 2/3 + δ = 2/9) remains a project priority.
  It is now formally the **ratios sub-target** of Lane 6 (charged-lepton
  mass retention). Closing the Koide flagship lane advances Lane 6, which
  in turn advances Lane 2 (atomic-scale, via m_e retention) and Lane 3
  absolute scales.
- The Planck pin completion work (a^(-1) = M_Pl unconditional) remains a
  project priority. It is orthogonal to these six lanes and addresses the
  claim-framing question rather than the matter-mass question.
- The frontier extension lanes (teleportation, chronology, signed gravity)
  are exploratory expansion lanes and remain separately scoped.

The relationship is additive: these six lanes are missing science that still
needs closing for a defensible TOE claim, on top of the internal lanes already
prioritized.

## Possible Manuscript-Surface Follow-Up

- Add a new section to [CLAIMS_TABLE.md](../../publication/ci3_z3/CLAIMS_TABLE.md)
  titled "Critical Open Science Lanes" listing these six lanes with status
  pointers to the per-lane open-lane documents.
- Update [WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](../../publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)
  to explicitly call out each of these six lanes as "currently bounded /
  open / scaffold-only" rather than implying they're already addressed by
  the bounded-companion category.
- Update [INPUTS_AND_QUALIFIERS_NOTE.md](../../publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md)
  to be explicit about which observables in each lane are framework-derived
  vs. external-input vs. scaffold-only.

Those publication-surface updates are deliberately deferred. This landing only
opens the critical open science lane package; it does not change the manuscript
claim surface.

## Open Review Questions

Future reviewers should evaluate:

1. **Are these the right six lanes?** Should others be substituted?
2. **Is the priority ordering right?** Should Hubble go first instead of atomic?
3. **Are the derivation targets correctly specified?** Are they the right
   theorems to attack?
4. **Are the approachability ratings calibrated?** Are any of these actually
   harder or easier than rated?
5. **Should any lane be promoted from open-lane tracking to a retained-grade
   lane-opening note after its first theorem target is scoped?**
6. **What should the manuscript-surface treatment be?** Add to CLAIMS_TABLE
   as "Critical Open Science Lanes," or keep this off the manuscript surface
   entirely until specific lane closures land?

## Honest framing

This open-lane package does not contain new physics. It contains scoping and
strategy. The six lanes are real missing-science lanes. Whether and how to
attack them is a separate question from whether they are correctly identified.

This is roughly a 6–18 month closure program. Each lane is months of focused
work, though lanes 2 and 5 are likely closer to single-month first closures.
