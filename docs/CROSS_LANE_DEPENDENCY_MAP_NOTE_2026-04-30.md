# Cross-Lane Dependency Map for the Six Critical Open Science Lanes

**Date:** 2026-04-30
**Status:** support-only synthesis; no claim promotion. This note is a
navigation/firewall artifact that consolidates the existing per-lane
dependency firewalls into a single dependency graph. It does **not** prove
any new lane closure and does **not** retire any open primitive.
**Script:** `scripts/frontier_cross_lane_dependency_map.py`
**Lanes:** 1, 2, 3, 4, 5, 6 (six critical open science lanes per
`docs/lanes/open_science/README.md`).

---

## 0. Why this note exists

The 2026-04-27 firewall packet landed five per-lane dependency firewalls plus
the 2026-04-30 atomic Lane 2 QED running firewall (this campaign's Block 1).
Each firewall names its load-bearing primitives in isolation. The cross-lane
implications are scattered across six separate notes.

This note consolidates those firewalls into one dependency graph so a worker
on any lane can see immediately which other lanes (or admitted observational
imports) must close first. It also exposes the **transitive blockers** —
primitives that reach into multiple lanes simultaneously — so closure
ordering can be planned strategically rather than per-lane.

The result is honest: the framework cannot reach atomic Lane 2 without
Lanes 1, 3, **and** 6 closing first; cannot reach Lane 1 without Lane 3
plus chiral inputs; and cannot reach Lane 5 numerical `H_0` without both a
`(C1)` absolute-scale primitive and a cosmic-`L` primitive.

## 1. Per-lane firewall summary

For each Tier-1 critical open lane, the **direct** load-bearing primitives
that block retained-grade closure:

| lane | direct blockers | firewall reference |
|---|---|---|
| 1 hadron | quark masses (Lane 3); chiral inputs (`Sigma`, `f_pi`); `(B5)` framework large-volume Wilson/Creutz primitive; `(B2)` quenched-to-dynamical screening | [HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27](./HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md), [HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30](./HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md) |
| 2 atomic | `m_e` (Lane 6); `alpha(0)` via QED running primitive (R-Lep, R-Q-Heavy, R-Had-NP); physical-unit nonrelativistic Schrodinger limit | [ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27](./ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md), [ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30](./ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md) |
| 3 quark | retained denominator/readout primitive for each of `m_u, m_d, m_s, m_c, m_b`; mass-ratio support is not retention | [QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27](./QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md) |
| 4 neutrino | `(C2-X)` charge-2 primitive class exhaustion or admitted Majorana/Dirac activation law; `mu_current = 0` plus `y_nu^eff` are not one closure surface | [NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27](./NEUTRINO_LANE4_DIRAC_SEESAW_FORK_NO_GO_NOTE_2026-04-27.md), [NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28](./NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md) |
| 5 Hubble | `(C1)` absolute-scale gate (currently blocked at active-block selector + carrier-to-metrology map); `(C2)/(C3)` cosmic-`L` gate | [HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27](./HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md), [HUBBLE_LANE5_C1_CARRIER_METROLOGY_AXIOM_AUDIT_NOTE_2026-04-29](./HUBBLE_LANE5_C1_CARRIER_METROLOGY_AXIOM_AUDIT_NOTE_2026-04-29.md) |
| 6 charged-lepton | `y_tau` Ward identity (research-level distant after Cycle 5 of `charged-lepton-pickup-20260428`); `V_0` absolute-scale closure once Koide ratios + Ward identity land; gauge-anchor routes (g_2, g_1) closed | [`docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md`](./lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md), [CHARGED_LEPTON_Y_TAU_M3_PREMISE_SELF_CORRECTION_NOTE_2026-04-28](./CHARGED_LEPTON_Y_TAU_M3_PREMISE_SELF_CORRECTION_NOTE_2026-04-28.md) |

## 2. Forward-edge dependency graph

A directed edge `X -> Y` reads "Lane Y depends on Lane X being closed first
or admitting a comparator import":

```text
                            QED loop primitive
                            (textbook input)
                                   |
                                   v
   Lane 6  --(R-Lep)-->  Lane 2 --(R-Q-Heavy)-->  Lane 3
   (m_e, m_mu, m_tau)  (alpha-running)            (m_u..m_b)
       |                        |                      |
       v                        v                      v
   y_tau Ward identity   admit-or-derive R(s)    chiral inputs
   (research-level)       --(R-Had-NP)-->           Sigma, f_pi
                                                       |
                                                       v
                                                  Lane 1 (m_pi, m_p)
                                                       ^
                                                       |
                                       Lane 1 (B5) framework large-volume
                                       Wilson/Creutz primitive
                                       (compute-budget gate)


   Lane 4 (neutrino) --(C2-X)--> Lane 4 closure
                          |
                          v
   admit Majorana/Dirac activation OR
   prove (SR-1)/(SR-2)/(SR-3)


   Lane 5 (Hubble) --(C1)--> Lane 5 numerical H_0
                       \--(C2)/(C3)--> Lane 5 numerical H_0
                       (BOTH gates required)
                          |
                          v
   active-block selector + carrier-to-metrology map
   (C1 sub-residual after 2026-04-29 packet)
```

The graph has **three disjoint connected components** at the framework
substrate level:

1. **Matter-mass component** (Lanes 1, 2, 3, 6) plus auxiliary chiral inputs
   and the QED loop primitive. Closure is sequential: Lane 6 first
   (charged-lepton ratios + V_0), Lane 3 (quark masses), Lane 1
   (hadron spectrum + chiral inputs), then Lane 2 substitution.
2. **Neutrino component** (Lane 4). Closure depends on `(C2-X)` charge-2
   primitive class exhaustion or an admitted activation law. Independent of
   the matter-mass component except through three-generation structure.
3. **Cosmology component** (Lane 5). Closure requires both `(C1)` and one of
   `(C2)/(C3)`. Independent of the matter-mass and neutrino components for
   numerical `H_0`, though shares retained `Lambda`, `m_g^2`, and `R_base`
   with the broader framework.

## 3. Transitive blockers

A **transitive blocker** is a primitive whose retention unblocks more than
one lane. The current list:

| primitive | unblocks | priority justification |
|---|---|---|
| Lane 6 closure (`m_e, m_mu, m_tau` retained) | Lane 2 R-Lep; Lane 6; partially Lane 3 (via cross-sector Koide bridges) | highest leverage in matter-mass component |
| Lane 3 closure (`m_q` for `c, b` retained) | Lane 1 (chiral inputs feed into GMOR-style closure); Lane 2 R-Q-Heavy | second-highest in matter-mass component |
| Lane 1 substrate `R(s)` retention | Lane 2 R-Had-NP; Lane 1 itself for hadron-spectroscopy | shared between Lane 1 and Lane 2 atomic R-Had-NP |
| `(C2-X)` exhaustion or admitted neutrino activation law | Lane 4 4D Dirac global lift unconditional | unblocks the entire neutrino component |
| `(C1)` absolute-scale carrier-to-metrology map | Lane 5 numerical `H_0` (with cosmic-`L` gate also closing) | half of the numerical `H_0` closure |
| QED loop primitive on framework substrate | Lane 2 running primitive at all orders; partially Lane 4 (vacuum-polarization analogs) | shared QFT-on-framework infrastructure |

**Highest-leverage transitive blocker:** Lane 6 closure. Closing Lane 6 alone
unblocks (i) Lane 2 R-Lep, (ii) Lane 6 itself, and (iii) opens cross-sector
Koide bridges into Lane 3. Lane 3 then unblocks Lane 1 chiral inputs and
Lane 2 R-Q-Heavy.

**Highest-leverage compute primitive:** Lane 1 substrate `R(s)` retention.
Closing it unblocks Lane 2 R-Had-NP without admitting external R-ratio
data.

**Highest-leverage structural primitive:** the QED loop primitive on the
framework substrate. It is implicit in retained `alpha_EM(M_Z)` but is
not itself retained as a derivation — only the value at one scale. A retained
loop primitive would enable all-orders running for both Lane 2 and Lane 4
analogs.

## 4. Closure-ordering implications

The dependency graph implies the following honest ordering for matter-mass
component closure:

```text
1. Lane 6 (charged-lepton) — closes m_e, m_mu, m_tau
   |
   v
2. Lane 3 (quark mass) — closes m_u, m_d, m_s, m_c, m_b
   |
   +--> 2a. (R-Lep) closes; partial Lane 2 progress
   v
3. Lane 1 (hadron mass) — chiral inputs + B5 + GMOR closure
   |
   +--> 3a. (R-Q-Heavy) closes; further Lane 2 progress
   v
4. Lane 2 substitution — Rydberg + atomic spectrum
   (also requires QED loop primitive retention, independent of 1-3)
   |
   +--> 4a. (R-Had-NP) closes via Lane 1 R(s)
```

Lane 4 and Lane 5 are independent and can proceed in parallel with the
matter-mass chain.

This ordering supersedes the recommended priority in
[`docs/lanes/open_science/README.md`](./lanes/open_science/README.md) §
"Recommended priority order" only for **dependency-driven** scheduling. The
README's recommendation includes a tactical Lane 5 parallel path because
"recent structural-identity landings make this materially closer." Both
recommendations agree on Lane 6 first; this map adds the explicit
post-Lane-6 chain via Lanes 3 and 1.

## 5. What this note retires

This note retires four tempting cross-lane shortcuts that the per-lane
firewalls do not individually rule out:

1. **"Closing Lane 6 closes the matter-mass program."** False.
   Lane 6 closure unblocks Lane 2 R-Lep but does not close R-Q-Heavy
   (Lane 3) or R-Had-NP (Lane 1). Atomic Lane 2 still requires
   Lanes 3 and 1.

2. **"Closing Lane 3 closes Lane 1."** False. Quark masses are necessary
   but not sufficient: Lane 1 also needs chiral inputs (`Sigma`, `f_pi`),
   `(B5)` framework large-volume Wilson/Creutz primitive, and `(B2)`
   quenched-to-dynamical screening (or an honest scope reduction).

3. **"Closing Lane 4 (neutrino) requires Lane 6 first."** False. Lane 4
   `(C2-X)` is independent of Lane 6 closure. Both can proceed in parallel.

4. **"Closing Lane 5 numerical `H_0` requires only the C1 gate."** False.
   The 2026-04-27 two-gate firewall says BOTH gates needed; either alone
   leaves a one-parameter family.

## 6. What remains open

The note does **not** retire any of the named load-bearing primitives. It
records them in one place and shows their interdependencies. Each primitive
remains an open lane closure target:

- `y_tau` Ward identity (Lane 6) — research-level distant after 5-cycle
  charged-lepton loop with all single-cycle gauge-anchor routes excluded
- denominator/readout primitive for each non-top quark (Lane 3) — bounded
  companion only
- `(B5)` framework-side large-volume Wilson/Creutz primitive (Lane 1) —
  compute-budget gated at L=8,12,16
- chiral inputs `Sigma`, `f_pi` from framework substrate (Lane 1)
- substrate hadronic R-ratio `R(s)` (Lane 1) — feeds Lane 2 R-Had-NP
- QED loop primitive on framework substrate (Lane 2)
- `(C2-X)` charge-2 primitive class exhaustion (Lane 4) — pending (SR-1),
  (SR-2), or (SR-3) closure
- `(C1)` active-block selector + carrier-to-metrology map (Lane 5)
- `(C2)/(C3)` cosmic-`L` gate (Lane 5)

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_cross_lane_dependency_map.py
```

The runner verifies:

1. All six firewall notes referenced in §1 exist on the current branch
   (Block-1's atomic running firewall is included).
2. Each firewall is named with the appropriate `proposed_retained` /
   `support` / `exact-reduction-theorem` status; no bare `retained`.
3. The dependency graph in §2 is internally consistent — every edge has
   a citation in the per-lane firewall body.
4. The transitive blockers in §3 each have at least two distinct lane
   destinations recorded.
5. The closure-ordering chain in §4 is acyclic.
6. The four retired shortcuts in §5 each cite a concrete firewall as
   evidence they are false.

## 8. Inputs and import roles

| Input | Role | Import class | Source |
|---|---|---|---|
| 5 existing firewall notes (2026-04-27 + 2026-04-29 + 2026-04-30) | source for direct-blocker rows | repo authority surface | per-note citations in §1 |
| Block 1 atomic-running firewall | source for atomic Lane 2 sub-residuals | repo authority surface (this branch) | `docs/ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md` |
| `docs/lanes/open_science/README.md` recommended priority order | comparator for §4 ordering claim | repo authority surface | per-lane open-lane README |

**No new physical claims; no new numerical comparators; no new admitted observations are introduced by this note.**
It is pure synthesis of existing firewall content.

## 9. Safe wording

**Can claim:**

- "Cross-lane dependency map of the six critical open lanes."
- "Synthesis of existing per-lane firewalls into one dependency graph."
- "Transitive blockers identified and prioritized."
- "Closure-ordering implications for matter-mass component."

**Cannot claim:**

- bare `retained` / `promoted` on this artifact.
- "This closes any lane." (it doesn't)
- "This retires any open primitive." (it doesn't — it consolidates them)
- "New physical content." (it has none — pure synthesis)

## 10. Cross-references

- **Block 1 (this campaign):** [ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30](./ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md)
- **2026-04-27 firewall packet:** five per-lane firewalls listed in §1
- **2026-04-29 Hubble C1 packet:** six C1 obstruction/boundary notes
- **2026-04-30 hadron Lane 1 work:** B2 gate-repair, B2 static-energy bridge,
  B5 framework-link audit, B5 ladder budget
- **Open lane index:** [`docs/lanes/open_science/README.md`](./lanes/open_science/README.md)
- **Active lane table:** [`docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md`](./lanes/ACTIVE_WORKING_LANES_2026-04-26.md)
