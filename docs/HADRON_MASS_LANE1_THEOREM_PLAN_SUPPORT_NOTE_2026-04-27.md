# Lane 1 Hadron Mass Theorem Plan: Lane-3 Dependency Audit and Closure Roadmap

**Date:** 2026-04-27
**Status:** support / open-lane planning note on `main`; no theorem or
claim promotion. Reduces Lane 1 (hadron mass program) to a sharp
pion/proton mass roadmap using current confinement, `alpha_s` running,
and Lane 3 quark-mass dependencies. Identifies Lane-1-internal work
that proceeds in parallel with Lane 3.
**Lane:** 1 — Hadron mass program
**Source workstream:** `hadron-mass-program-20260427`

---

## 0. Statement

Lane 1 closure (retained `m_p, m_n, m_pi`, hadron spectroscopy, form
factors) requires retaining each target via an explicit derivation
chain on the framework substrate. Per the lane file, the **five
derivation targets** are:

- **3A** pion mass via Gell-Mann-Oakes-Renner (GMOR);
- **3B** proton/neutron mass ab initio via lattice-QCD methodology;
- **3C** hadron spectroscopy (kaon, ρ, ω, B/D mesons, baryon
  octet/decuplet);
- **3D** hadron form factors;
- **3E** retained promotion of `sqrt(sigma)` (string tension; bounded
  at `~465 MeV`, ~5.6% above PDG `440 ± 20 MeV`).

This plan organizes the targets by **Lane-3 dependency**:

- Phase-1 Lane-3-blocked: **3A** (needs `m_u + m_d`).
- Phase-2 Lane-3-blocked: **3B** (needs all five quark masses).
- Phase-3 Lane-3-blocked: **3C, 3D**.
- Phase-1 Lane-1-internal (parallel to Lane 3): **3E**, plus an
  optional Lane-1-internal route to chiral condensate `Sigma` retention
  (which would partially unblock 3A even before Lane 3 closure of
  light-quark masses).

The plan does not derive a hadron mass; it produces the structural
roadmap.

## 1. Retained framework structure used

| Identity | Authority | Role in plan |
|---|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` | substrate |
| `T = 0` confinement of graph-first SU(3) | `CONFINEMENT_STRING_TENSION_NOTE.md` | qualitative gate-keeper for hadron spectrum existence |
| `alpha_s(M_Z) = 0.1181` retained | `ALPHA_S_DERIVED_NOTE.md` | running input for hadronic-scale `alpha_s` |
| Graph-first SU(3) integration | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` | gauge sector retained |
| Retained `y_t / g_s = 1/sqrt(6)` Ward identity | YT theorem cluster | analog template for any framework-side hadron-Ward derivation |
| Retained `m_t(pole) = 172.57 GeV` | YT/top transport lane | precedent for retained quantum-mass closure |
| Standard plaquette / `u_0` surface | minimal-axioms canonical normalization | lattice-action layer |

The framework already supplies:

- gauge-sector quantum closure (anomaly-free, asymptotic-freedom-
  preserving, anomaly cancellations);
- a substrate (Cl(3)/Z³) that supports both Wilson and staggered
  fermion lattice actions natively;
- a precedent (top sector) for retained quantum-mass closure via a
  framework-internal Ward identity.

It does not yet supply:

- numerical light-quark masses (Lane 3 open);
- chiral condensate `Sigma` (Lane-1-internal possible);
- pion decay constant `f_pi` (Lane-1-internal possible);
- any retained hadron-mass numerical prediction.

## 2. The five derivation targets

### 2.1 Target 3A — Pion mass via GMOR

**Identity (standard chiral perturbation theory):**

```text
m_pi^2 f_pi^2  =  (m_u + m_d) * Sigma                              (GMOR)
```

valid in the chiral limit; corrections are `O(m_q)` higher in chiral
counting.

**What needs to be retained:**

- `m_u + m_d` (light-quark mass sum) — Lane 3 dependency;
- `Sigma` (chiral condensate, `Sigma = -<u-bar u> = -<d-bar d>` in
  isospin limit) — Lane-1-internal candidate;
- `f_pi` (pion decay constant, ≈ 92.4 MeV) — Lane-1-internal candidate.

**Closure status table:**

| Quantity | Retained on `main`? | Lane | Notes |
|---|---|---|---|
| `m_u + m_d` | no | 3 | bounded scaffold |
| `Sigma` | no | 1 (internal) | derivable from staggered-Dirac partition? |
| `f_pi` | no | 1 (internal) | derivable from chiral SB pattern? |
| `m_pi` (output) | no | 1 (this target) | conditional on the above |

**Approachability:** Tier B once Lane 3 lands `m_u + m_d`. If
Lane-1-internal routes for `Sigma` and `f_pi` succeed earlier, 3A can
land conditionally on Lane-3 light-quark-mass-sum closure alone.

### 2.2 Target 3B — Proton / neutron mass ab initio

**Methodology:** standard lattice-QCD correlator analysis on the
`Cl(3)/Z³` substrate's Wilson or staggered fermion action, with
hadronic-scale `alpha_s` from SM running of retained `alpha_s(M_Z)`,
and quark masses from Lane 3.

**What needs to be retained:**

- All five quark masses `m_u, m_d, m_s, m_c, m_b` — Lane 3 full closure.
- `alpha_s` at hadronic scale (~1 GeV) — running bridge from retained
  `alpha_s(M_Z) = 0.1181`. Standard SM running; admitted convention.
- Lattice-action equivalence: declaration that the framework's
  staggered-Dirac partition matches the standard lattice-QCD action up
  to controlled lattice artifacts. This may need a separate retained
  bridge note (similar to YT-lane `1.21%` and `0.755%` bridge budgets).
- Standard lattice-QCD correlator-analysis methodology (admitted
  convention).

**Closure status:**

| Component | Retained on `main`? | Notes |
|---|---|---|
| All five quark masses | no | Lane 3 — Phase 2 / Phase 3 |
| Hadronic `alpha_s` | bridge, no | SM running from `alpha_s(M_Z)` |
| Lattice-action equivalence | not declared | possible Lane-1-internal bridge |
| Methodology | admitted | textbook |
| `m_p`, `m_n` (output) | no | conditional on the above |

**Approachability:** Tier C. Substantial computational work but
well-understood methodology.

### 2.3 Target 3C — Hadron spectroscopy

**Methodology:** systematic extension of 3A/3B framework to kaon,
ρ, ω, B/D, baryon octet/decuplet.

**What needs to be retained:** all of 3A and 3B prerequisites, plus
heavy-quark sector retentions (m_c, m_b from Lane 3).

**Approachability:** Tier C. Routine lattice-QCD once 3A and 3B land.

### 2.4 Target 3D — Hadron form factors

**Methodology:** lattice computation of B → π, K → π, nucleon EM, π
EM form factors.

**What needs to be retained:** 3A/3B/3C plus standard
form-factor-extraction methodology.

**Approachability:** Tier C. Standard lattice methodology.

### 2.5 Target 3E — `sqrt(sigma)` retained promotion

**Goal:** tighten EFT bridge + screening corrections to move bounded
`sqrt(sigma) ≈ 465 MeV` (5.6% above PDG `440 ± 20 MeV`) to retained
sub-percent or with explicit retention budget (analog of YT/top
transport lane's `1.21%` / `0.755%` bridge budget).

**What needs to be retained:**

- Existing `sqrt(sigma)` bounded derivation (already in
  `CONFINEMENT_STRING_TENSION_NOTE.md`);
- Tightened EFT bridge (currently bounded);
- Screening-correction budget (currently bounded);
- Possibly a separate retained bridge note that fixes the residual
  bounded numerics.

**Closure status:**

| Component | Retained on `main`? | Notes |
|---|---|---|
| `T = 0` confinement | yes | retained structural theorem |
| `sqrt(sigma) ≈ 465 MeV` numerical | bounded | 5.6% above PDG |
| EFT bridge | bounded | needs tightening |
| Screening corrections | bounded | needs tightening |

**Approachability:** Tier B. **No Lane-3 dependency**; runs in
parallel.

## 3. Lane-3 dependency map

Lane 3 (quark mass retention) has the following current state per its
lane file:

- `m_t (pole) = 172.57 GeV` retained via `y_t / g_s = 1/sqrt(6)` Ward
  identity (analog template).
- All five non-top quark masses (`m_u, m_d, m_s, m_c, m_b`) bounded /
  scaffolded.

Lane-3 retentions unblock Lane-1 targets in this dependency order:

```text
Lane 3 retains m_u + m_d  →  Lane 1 unblocks 3A pion mass (3E unaffected)
Lane 3 retains all five    →  Lane 1 unblocks 3B proton/neutron mass
Lane 3 + 3A + 3B retained  →  Lane 1 unblocks 3C spectroscopy + 3D form factors
```

The cleanest first sub-target on the Lane-3 side (for Lane 1's
benefit) is `m_u + m_d` — a single combined retention that unblocks
3A. This is Lane 3's call; Lane 1 records it as the strongest
priority dependency.

## 4. Lane-1-internal routes (parallel to Lane 3)

Two Lane-1-internal routes can run independently of Lane 3:

### 4.1 Route 3E — `sqrt(sigma)` retained promotion (`R1` in workstream portfolio)

Sketch: tighten the existing bounded `sqrt(sigma)` via:

1. EFT bridge audit: identify the precise EFT operators that contribute
   to the residual 5.6% gap.
2. Screening-correction budget: produce a retention budget analogous to
   YT-lane's `1.21%` / `0.755%` budget.
3. If the retention budget closes sub-percent: promote `sqrt(sigma)`
   to retained.
4. If a residual remains: produce a retained-with-explicit-budget
   statement (the YT-lane analog).

This route does not depend on Lane 3 and is the cleanest Lane-1-
internal Tier-B target.

### 4.2 Route — chiral condensate `Sigma` structural derivation (`R7` in workstream portfolio)

Sketch: investigate whether the retained finite local
Grassmann/staggered-Dirac partition on `Cl(3)/Z³` delivers a retained
`Sigma` directly via:

1. The Banks-Casher relation `Sigma = pi * rho_eigen(0)` (eigenvalue
   density of the Dirac operator at zero) — standard chiral SB
   identity.
2. Framework's substrate already supplies the staggered-Dirac
   eigenvalue structure on `Z³`.
3. If the small-eigenvalue density is retainable from framework
   structure, `Sigma` lands on `main`.

This route is Tier B-C, depending on whether a clean structural path
emerges. Note that landing `Sigma` plus retaining `f_pi` would let 3A
land conditionally on Lane-3 closure of `m_u + m_d` only (rather than
on `m_u + m_d + Sigma + f_pi`).

### 4.3 Route — pion decay constant `f_pi` derivation

Sketch: derive `f_pi` from the framework's chiral SB pattern on
`Cl(3)/Z³`. This is a structural pion-current normalization that
should be available once `Sigma` is retained (the two are
intertwined in the chiral-SB pattern).

Not separately scored as a workstream route — would naturally be a
companion or follow-on to the `Sigma` route.

## 5. Phase ordering

Per the lane file §5 with Lane-3 dependency map:

### Phase 1 (now, parallel to Lane 3 progress)

- **3E** `sqrt(sigma)` retention-gate work (Lane-1-internal; no Lane-3
  blocker).
- **`Sigma` / `f_pi` structural attempt** (Lane-1-internal; partial
  unblock for 3A even before Lane 3 closure of light-quark masses).
- Lane-3 dependency monitoring: as soon as Lane 3 retains `m_u + m_d`,
  Phase-2 begins.

### Phase 2 (after Lane 3 retains `m_u + m_d`)

- **3A** pion mass via GMOR. Combines retained `m_u + m_d` (Lane 3) +
  retained `Sigma` (Phase 1, if landed) + retained `f_pi` (Phase 1,
  if landed) + GMOR identity (admitted convention).

### Phase 3 (after Lane 3 retains all five quark masses)

- **3B** proton/neutron mass ab initio.
- **3C** hadron spectroscopy systematic extension.
- **3D** hadron form factors.

## 6. What this plan closes and does not close

**Closes (claim-state movement):**

- A sharp Lane-3 dependency map: which Lane-3 retentions unblock
  which Lane-1 targets.
- A phase-ordered closure roadmap (Phase 1: 3E + `Sigma`/`f_pi`;
  Phase 2: 3A; Phase 3: 3B/3C/3D).
- An explicit list of Lane-1-internal routes that proceed in parallel
  with Lane 3.
- An explicit identification of the cleanest first sub-target on the
  Lane-3 side (`m_u + m_d` retention).

**Does not close:**

- Any hadron mass numerically.
- Any Lane-3 retention.
- The specific structural derivation of `Sigma`, `f_pi`, or hadronic
  `alpha_s`.
- The lattice-action equivalence bridge for 3B.

## 7. Falsifier

The plan is structural; it does not predict a value. It is falsified
if:

- a Phase-2 derivation succeeds without retaining one of the listed
  prerequisites (indicating a missed dependency in the map);
- a Lane-1 target lands via an entirely different methodology not
  enumerated here (indicating an unscored route).

Either outcome is a positive update to the plan, not a defeat.

## 8. Cross-references

- `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  — Lane 1 lane file (primary authority for the five derivation
  targets).
- `docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md`
  — Lane 3 lane file (primary dependency).
- `docs/CONFINEMENT_STRING_TENSION_NOTE.md` — retained `T = 0`
  confinement; bounded `sqrt(sigma) ≈ 465 MeV`.
- `docs/ALPHA_S_DERIVED_NOTE.md` — retained `alpha_s(M_Z) = 0.1181`.
- `docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` — graph-first SU(3)
  closure.
- `docs/QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md` — Lane 3 entry
  point.
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — minimal accepted axiom stack.
## 9. Boundary

This is a structural plan, not a theorem. It does not retire any
input, does not introduce a numerical claim, and does not promote
any cycle of work to retained status. It produces the workstream's
roadmap so subsequent cycles target the right object.

A runner is not authored: the plan is editorial / structural; no
new symbolic or numerical content is introduced.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [lanes.open_science.01_hadron_mass_program_open_lane_2026-04-26](lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md)
- [lanes.open_science.03_quark_mass_retention_open_lane_2026-04-26](lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md)
- [confinement_string_tension_note](CONFINEMENT_STRING_TENSION_NOTE.md)
- [alpha_s_derived_note](ALPHA_S_DERIVED_NOTE.md)
- [graph_first_su3_integration_note](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- [quark_mass_ratio_review_packet_2026-04-18](QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md)
- [minimal_axioms_2026-04-11](MINIMAL_AXIOMS_2026-04-11.md)
