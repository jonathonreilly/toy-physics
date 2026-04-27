# Lane 1 Workstream Status: Three-Cycle Consolidation

**Date:** 2026-04-27
**Status:** retained branch-local consolidation note on
`frontier/hadron-mass-program-20260427`. Single read-first Lane 1
status surface synthesizing the three-cycle workstream output for the
post-workstream review-and-integration pipeline.
**Lane:** 1 — Hadron mass program
**Workstream:** `hadron-mass-program-20260427`

---

## 0. Headline

Before this workstream, Lane 1 was framed as five derivation targets
(3A `m_pi` via GMOR; 3B `m_p` ab initio; 3C spectroscopy; 3D form
factors; 3E `sqrt(sigma)` retained promotion) without a clear
dependency map.

After this workstream, Lane 1's near-term productive moves are
sharply mapped:

> - **3E `sqrt(sigma)` retention** reduces to **a single load-bearing
>   residual `(B2)`** (quenched → dynamical screening at `beta = 6.0`,
>   `N_f = 2+1`); closing `(B2)` plus declaring `(B1)` and `(B5)`
>   delivers a YT-lane-style retained-with-budget statement.
> - **3A `m_pi` via GMOR** decomposes into three retentions:
>   `(m_u + m_d)` from Lane 3 (essential), `Sigma`, and `f_pi`. The
>   Banks-Casher route to `Sigma` is **audit-empty on current
>   framework content** (R7 audit-no-go, Cycle 3) — opening it
>   requires either a large-volume lattice run or a new structural
>   identity.
> - **3B `m_p` / 3C spectroscopy / 3D form factors** all gated on
>   Lane 3 full closure plus standard lattice-QCD methodology
>   declared as admitted-convention bridge.

The cleanest single Lane-3 sub-target (for Lane 1's benefit) is
**retain `m_u + m_d` as a combined sum** — this alone unblocks 3A
once `Sigma` and `f_pi` are addressed. Other Lane-1-internal
near-term work is `(B2)` closure (would require an off-workstream
lattice calculation).

## 1. The retained gauge-sector stack used

All three cycles rest on the following retained items already on
`origin/main`. No cycle imports a quark mass or hadron mass observable
as a derivation input.

| Identity | Authority |
|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` |
| `T = 0` confinement of graph-first SU(3) | `CONFINEMENT_STRING_TENSION_NOTE.md` |
| `alpha_s(M_Z) = 0.1181` retained quantitative | `ALPHA_S_DERIVED_NOTE.md` |
| Graph-first SU(3) integration | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` |
| Retained `y_t / g_s = 1/sqrt(6)` Ward identity (analog template) | YT theorem cluster |
| Retained `m_t (pole) = 172.57 GeV` (precedent for retained quantum-mass closure) | YT/top transport lane |
| Bounded `sqrt(sigma) ≈ 465 MeV` (5.6% above PDG `440 ± 20 MeV`) | `CONFINEMENT_STRING_TENSION_NOTE.md` (bounded) |
| Lattice scan of `rho(0)` etc. at `L = 4, 6` | `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` |

## 2. Three-cycle output map

### Cycle 1 — Lane 3 dependency audit + Lane 1 theorem plan (R2)

**Artifact:** `docs/HADRON_MASS_LANE1_THEOREM_PLAN_NOTE_2026-04-27.md`
(no runner — structural plan).

**Claim:** Lane 1 closure is phase-ordered:

- **Phase 1** (now, parallel to Lane 3): 3E `sqrt(sigma)` retained
  promotion + Lane-1-internal `Sigma` / `f_pi` structural attempts.
- **Phase 2** (after Lane 3 retains `m_u + m_d`): 3A `m_pi` via GMOR.
- **Phase 3** (after Lane 3 full closure): 3B `m_p` ab initio + 3C
  spectroscopy + 3D form factors.

**Lane 1 contribution:** the lane file's explicit "first parallel-
worker target" landed branch-locally.

### Cycle 2 — `sqrt(sigma)` retention gate audit (R6)

**Artifact:**
`docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_NOTE_2026-04-27.md`
(no runner — EFT-bridge decomposition).

**Claim:** the 5.6% gap between bounded `sqrt(sigma) ≈ 465 MeV` and
PDG `440 ± 20 MeV` decomposes into 5 explicit EFT-bridge
contributions:

- (B1) `alpha_s(M_Z)` precision propagation: `~1%` — retained-input
  residual.
- **(B2) Quenched → dynamical screening: `~5%` — load-bearing.**
- (B3) `Lambda^(3)` two-loop matching: absorbed via Sommer-scale
  Method 2.
- (B4) Method 1 vs Method 2 disagreement: resolved by Method-2
  selection once `(B2)` closes.
- (B5) Framework SU(3) ↔ standard SU(3) YM identification:
  structural; needs volume-scaling / asymptotic Wilson-loop
  verification path.

**Lane 1 contribution:** `(B2)` isolated as the single load-bearing
open item. Closing it via a proper `N_f = 2+1` lattice calculation
at `beta = 6.0` (replacing the rough `×0.96` factor) plus declaring
`(B1)`, `(B5)` delivers retained-with-budget.

### Cycle 3 — Chiral condensate `Sigma` Banks-Casher scoping (R7)

**Artifact:**
`docs/HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_NOTE_2026-04-27.md`
(no runner — audit-no-go).

**Claim:** no clean Lane-1-internal structural retention route for
`Sigma` exists on current framework content. Two failure modes:

- (V1) Existing `L = 4, 6` lattice data is in finite-volume
  lattice-free regime; Banks-Casher requires `L >= 12-16` with
  chiral-thermodynamic ordering.
- (V2) No structural identity pinning `rho_Dirac(0)` from `Cl(3)/Z^3`
  action parameters. chRMT gives universal small-eigenvalue
  *shape* but not *scale* `Sigma`.

Two hypothetical opening paths named:

- (P1) Large-volume `N_f = 2+1` dynamical lattice at `beta = 6.0`,
  `L >= 16` — off-workstream-budget; delivers measured `Sigma` paired
  with `(B5)` framework identification.
- (P2) New structural identity (analog of YT-lane Ward) — no active
  route.

**Lane 1 contribution:** R7 class-bounding negative; mirrors
hubble-h0 (C3)-class audit-no-go pattern.

## 3. What the workstream did and did not retire

| Cycle | Retired imports | Clarified | Open |
|---|---|---|---|
| 1 | none | Lane 3 dependency map; phase ordering; cleanest Lane-3 sub-target = `m_u + m_d` | all 5 derivation targets |
| 2 | none | `sqrt(sigma)` decomposition; `(B2)` load-bearing | `(B2)` closure |
| 3 | none | Banks-Casher route audit-empty; `(P1)`, `(P2)` named | `Sigma` retention |

**Net retired imports: zero.** The workstream is structural —
classifies what Lane 1 closure requires, isolates load-bearing items,
and audits the visible Lane-1-internal routes.

## 4. Lane 1 closure pathway (post-workstream)

Combining Cycles 1-3, Lane 1 closure now reads:

```text
Phase 1 (parallel to Lane 3):
  - 3E sqrt(sigma) retained-with-budget
       requires: closing (B2) via off-workstream lattice run
                 + declaring (B1) and (B5) explicitly
  - Lane-1-internal Sigma retention
       requires: (P1) large-volume lattice run, OR
                 (P2) new structural identity (no active route)
  - Lane-1-internal f_pi retention
       (companion to Sigma; chiral-SB-pattern derivation)

Phase 2 (after Lane 3 retains m_u + m_d):
  - 3A m_pi via GMOR
       requires: (m_u + m_d) from Lane 3 + Sigma + f_pi
                 + GMOR identity (admitted convention)

Phase 3 (after Lane 3 full closure + lattice-QCD bridge):
  - 3B m_p ab initio
  - 3C spectroscopy systematic extension
  - 3D form factors
```

**Single highest-leverage Lane-3 sub-target:** retain `m_u + m_d` as
a combined sum (unblocks 3A).

**Single highest-leverage Lane-1-internal target:** close `(B2)`
quenched → dynamical screening at `beta = 6.0` (delivers
`sqrt(sigma)` retained-with-budget).

## 5. Manuscript-surface weaves (NOT applied — for post-workstream
integration)

The following weaves are recorded for the post-workstream review-
and-integration pipeline. They are not applied on
`frontier/hadron-mass-program-20260427` per skill science-only
delivery policy.

- `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  §4 scaffolding list: add the four new branch-local artifacts
  (theorem plan, sqrt(sigma) gate audit, Sigma scoping, this
  consolidation).
- `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  §5 phase ordering: incorporate the `(B2)` load-bearing isolation
  and the R7 audit-no-go.
- `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md` Lane 1 status
  line: update from "critical open science lane" to
  "critical open science lane; closure path mapped; (B2) and Lane 3
  m_u + m_d retention identified as highest-leverage open items".
- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §6 (bounded
  rows) update for `sqrt(sigma)` to reflect the explicit (B1-B5)
  budget decomposition.
- Lane 3 lane file cross-reference: mark the `m_u + m_d` combined
  retention as the highest-leverage Lane-3 sub-target for Lane 1's
  benefit.

## 6. Cross-references

### Workstream artifacts (this branch)

- Cycle 1: `HADRON_MASS_LANE1_THEOREM_PLAN_NOTE_2026-04-27.md`
- Cycle 2: `HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_NOTE_2026-04-27.md`
- Cycle 3: `HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_NOTE_2026-04-27.md`

### Workstream pack (this branch)

- `.claude/science/frontier-workstreams/hadron-mass-program-20260427/`
  — pack scaffold (9 files: STATE.yaml, GOAL.md,
  ASSUMPTIONS_AND_IMPORTS.md, NO_GO_LEDGER.md, ROUTE_PORTFOLIO.md,
  ARTIFACT_PLAN.md, LITERATURE_BRIDGES.md, REVIEW_HISTORY.md,
  HANDOFF.md).

### Adjacent open lanes

- Lane 3 (quark mass retention) — primary blocker for 3A/3B/3C/3D.
- Off-workstream lattice-QCD calculation — required to close `(B2)`
  for `sqrt(sigma)` and to deliver measured `Sigma` for 3A.

## 7. Boundary

This is a consolidation/status note, not a new theorem. It does
not retire any input, does not promote any cycle's claim to a
new tier, and does not change the closure pathway taxonomy. It
synthesizes the three-cycle workstream output into a single
read-first surface for the post-workstream review pipeline.

A runner is not authored: the consolidation is editorial /
navigational content over the existing branch-local artifacts.
