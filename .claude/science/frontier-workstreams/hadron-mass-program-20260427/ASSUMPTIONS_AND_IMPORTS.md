# Hadron Mass Program — Assumptions and Imports Ledger

**Date:** 2026-04-27
**Workstream:** `hadron-mass-program-20260427`
**Purpose:** explicit pre-cycle inventory of what is taken as input,
what is already retained on the framework surface, and what bridge
layers are in play.

This ledger feeds the dramatic-step gate. New cycles must retire an
existing import or add exact support; silent re-imports fail the gate.

## 1. Retained framework structure (already on `main`)

Theorem-grade; no additional support needed before citing.

| Identity | Authority |
|---|---|
| `Cl(3)` on `Z^3` (one-axiom physical theory) | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| `T = 0` confinement of graph-first SU(3) gauge sector | `docs/CONFINEMENT_STRING_TENSION_NOTE.md` |
| `alpha_s(M_Z) = 0.1181` retained quantitative | `docs/ALPHA_S_DERIVED_NOTE.md` |
| Quark-lepton anomaly cancellation | recent SM gauge-anomaly cluster on `origin/main` |
| Graph-first SU(3) integration | `docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` |
| Standard plaquette / `u_0` surface | included in minimal-axioms canonical normalization |
| Retained electroweak hierarchy / `v = 246.282818290129 GeV` | `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` |
| Retained `y_t / g_s = 1/sqrt(6)` lattice-scale Ward identity (top sector) | YT theorem cluster on `origin/main` |
| Retained bare `alpha_3 / alpha_em = 9` dimension support | `docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md` (see hubble-h0 inputs ledger) |

## 2. Bounded / scaffold-only on `main`

| Item | Current status | Authority |
|---|---|---|
| `sqrt(sigma) ~= 465 MeV` (string tension readout) | bounded (5.6% above PDG 440 ± 20 MeV) via EFT bridge + screening | `docs/CONFINEMENT_STRING_TENSION_NOTE.md` |
| BH entropy / RT ratio | bounded companion with retained Widom no-go | `docs/BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md` |
| All five non-top quark masses (m_u, m_d, m_s, m_c, m_b) | bounded / scaffolded | Lane 3 (`docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md`) |

## 3. External inputs on the current paper surface

Explicit observational pins. Lane 1's job is to produce retained
hadron-mass predictions; in doing so, it must avoid silently importing
hadron-mass values rather than deriving them.

| Input | Value | Role | Retirement candidate? |
|---|---|---|---|
| PDG quark masses | `m_u, m_d, m_s, m_c, m_b` (PDG MS-bar values) | Lane 3 dependency; not Lane 1 retirement target | belongs to Lane 3 |
| Hadron mass observables | `m_p ≈ 938 MeV`, `m_n ≈ 940 MeV`, `m_pi ≈ 140 MeV`, etc. | comparators only | not derivation inputs; never an "import" |
| `alpha_s` at hadronic scale | derived by SM running from retained `alpha_s(M_Z)` | bridge layer | the running itself is a retained bridge |
| Standard lattice QCD methodology | textbook (Wilson/staggered actions; correlator analysis) | admitted convention | not retired in this lane; standard substrate |
| Chiral perturbation theory | textbook framework for GMOR-based m_pi extraction | admitted convention | not retired |

## 4. Bridge layers and admitted conventions

Not raw observational inputs but standard physics layers used between
the retained core and hadron-mass extraction. None of these is a
derivation input in its own right.

- Standard SM running of `alpha_s` from `M_Z` to hadronic scale (~1 GeV)
- Wilson / staggered fermion lattice action (substrate already in
  `Cl(3)/Z³` framework's microscopic dynamics layer)
- Standard lattice-QCD correlator analysis for hadron mass extraction
- Chiral perturbation theory for m_pi → quark mass relations
- Standard hadron-mass renormalon / scheme conventions (MS-bar etc.)

## 5. What Lane 1 has and does not have

**Has:**

- Retained gauge sector (T=0 confinement; α_s(M_Z); SM gauge-cluster
  retentions).
- Bounded √σ ≈ 465 MeV (5.6% above PDG); needs tightening for
  retained promotion (3E).
- The substrate to run standard lattice-QCD methodology (Wilson /
  staggered actions are explicitly in the framework's substrate).
- Top mass `m_t(pole) = 172.57 GeV` retained as a closed analog of
  what Lane 1 wants for the lighter quarks and hadrons.

**Does not have:**

- Retained `m_u`, `m_d`, `m_s`, `m_c`, `m_b` (Lane 3 open).
- Retained chiral condensate `Σ`.
- Retained pion decay constant `f_π`.
- Any retained hadron-mass numerical prediction.
- Retained α_s at hadronic scale (running bridge needed).

## 6. Workstream rule

A cycle that derives a hadron mass while silently importing a quark
mass or hadron-mass observable from PDG fails the dramatic-step gate.
Quark masses are explicitly Lane 3's retirement target; hadron masses
are explicitly Lane 1's retention target. Comparators are used in
runners' verification phase only.

## 7. Lane 3 dependency map

Per the lane file §3, Lane 1 closure of `m_pi` (via GMOR) requires:

```text
m_pi^2 f_pi^2 = (m_u + m_d) * Sigma
```

so `m_pi` retained needs:

- `m_u + m_d` retained (Lane 3 closure of light-quark mass sum)
- `Sigma` retained (chiral condensate; possible Lane-1-internal route)
- `f_pi` retained (pion decay constant; possible Lane-1-internal
  route)

Lane 1 closure of `m_p` (ab initio) requires:

- All quark masses retained (Lane 3 full closure)
- α_s at hadronic scale retained (running bridge)
- Standard lattice-QCD methodology adapted to framework substrate

The Lane-3 dependency is therefore **strictly required for 3A and 3B**
but not for 3E (√σ promotion). 3E is the cleanest single-cycle entry
target for this workstream.
