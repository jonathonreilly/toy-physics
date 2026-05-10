# Lane 4 Neutrino Theorem Plan: Closure Roadmap with Phase Ordering

---

**This is a planning / roadmap note. It does not establish any retained claim.**
For retained claims on Lane 4 components, see the per-claim notes
referenced from the `## Audit scope` block below.

---

**Date:** 2026-04-28
**Status:** support / planning record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / planning record only — does not propagate retained-grade
**Audit status:** audited_conditional (per audit ledger)
**Propagates retained-grade:** no
**Proposes new claims:** no

Roadmap only, no claim promotion. Reduces Lane 4 (neutrino
quantitative closure) to a sharp closure roadmap using current
PMNS/Majorana/Dirac content, `N_eff`, and the DM-closed-package
`delta_CP`/`theta_23` forecast. Identifies Phase-1 priorities and the
cleanest stretch-attempt entry.

**Lane:** 4 — Neutrino quantitative closure
**Loop:** `neutrino-quantitative-20260428`

## Audit scope (relabel 2026-05-10)

This file is a **planning / closure-roadmap note** for Lane 4
(neutrino quantitative closure). It is **not** a single retained
theorem and **must not** be audited as one. The audit ledger row for
`neutrino_lane4_theorem_plan_note_2026-04-28` classified this source
as conditional/open_gate with auditor's repair target:

> missing_dependency_edge: register the actual one-hop authorities and
> separately audit the 4D globalization, 4E mass mechanism, and
> downstream arithmetic targets.

The minimal-scope response in this PR is to **relabel** this document
as a planning record rather than to materialize the missing one-hop
authority edges or to separately audit the 4D/4E/downstream targets
here. Those steps belong in dedicated review-loop or per-target
audit passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The seven derivation targets (4A-4G), tier classifications,
  approachability assessments, phase ordering, and stretch-attempt
  candidate lists below are **historical planning memory only**.
- The retained-status surface for any Lane 4 sub-claim is the audit
  ledger (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim notes
  cited under "Retained framework structure used" in §1, **not** this
  plan.
- Retained-grade does **NOT** propagate from this plan to any 4A-4G
  sub-target, theorem object, or successor cycle.

### Per-claim pointers

The framework-structure inputs cited under §1 each have dedicated
notes where the live audit-clean status, if any, lives. The plan
quotes those notes by filename; the live status is whatever the
audit-ledger row for each linked note says today, not what this plan
records.

For any retained claim on Lane 4 closure status, audit the
corresponding dedicated note (e.g. `NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`,
`NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`, etc.) and its
runner as a separate scoped claim — not this roadmap plan.

---

## 0. Statement

Lane 4 closure (retained `m_lightest`, `Delta m^2_21`, `Delta m^2_31`,
Majorana phases if applicable, seesaw spectrum) requires retaining
each target via an explicit derivation chain on the framework
substrate. Per the lane file, the **seven derivation targets** are:

- **4A** absolute mass scale `m_lightest`;
- **4B** solar mass-squared difference `Delta m^2_21`;
- **4C** atmospheric mass-squared difference `Delta m^2_31`;
- **4D** Dirac vs Majorana global lift;
- **4E** seesaw mass spectrum quantitative closure;
- **4F** cosmological `Sigma m_nu` constraint;
- **4G** cross-validation with retained `delta_CP ≈ -81°` and
  `theta_23 ≥ 0.5410`.

This plan organizes targets by **dependency on current retained
content**:

- **Phase 1 (now, Lane-4-internal):** 4D Dirac global lift (Tier B;
  current-stack zero law + mass-reduction-to-Dirac retained as
  scaffolding); 4E seesaw spectrum partial→retained (Tier B-C; Phase 4
  of mass-spectrum derived note is partial).
- **Phase 2 (after 4D + 4E):** 4B `Delta m^2_21` and 4C `Delta m^2_31`
  derived from the seesaw spectrum (Tier B-C; arithmetic once Phase 1
  lands).
- **Phase 3 (after Phase 2):** 4A `m_lightest` absolute scale (Tier C;
  hardest sub-target).
- **Cross-cycle:** 4F `Sigma m_nu` connects to Lane 5 retained
  cosmology surface; 4G internal consistency check (Tier A; runs
  whenever 4D-4E land).

The plan does not derive any neutrino mass or splitting; it produces
the structural roadmap.

## 1. Retained framework structure used

| Identity | Authority | Role in plan |
|---|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` | substrate |
| Anomaly-forced 3+1 + retained three-generation structure | three-generation cluster | mass-spectrum dimensionality |
| Exact PMNS selector / current-stack zero law | `PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md` | local constraint on mixing structure |
| Exact Majorana zero law on current stack | `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` | local witness for Dirac lane (Phase 1) |
| Neutrino mass reduction to Dirac lane | `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` | structural carrier identity |
| Retained neutrino observable bounds | `NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md` | validation scaffolding |
| Retained two-amplitude last-mile reduction | `NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md` | reduces remaining open object |
| `delta_CP ≈ -81°` (DM closed package; falsifiable) | DM closed package | 4G consistency comparator |
| `theta_23 ≥ 0.5410` upper octant | DM closed package | 4G consistency comparator |
| `N_eff = 3.046` from three generations | `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` | 4F cosmology bridge |
| Hubble-h0 loop's matter-bridge identity + structural lock theorems | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`, `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` | 4F upstream cosmology |

## 2. The seven derivation targets

### 2.1 Target 4D — Dirac vs Majorana global lift

**Statement to attempt:** **Theorem (Global Dirac).** On the retained
`Cl(3)/Z^3` framework with three generations and the retained
current-stack Majorana zero law plus Majorana no-go cluster (Native-
Gaussian, Finite-Normal-Grammar, Lower-Level-Pairing), neutrinos are
globally Dirac.

**Closure status:**

| Component | Retained on `main`? | Notes |
|---|---|---|
| Current-stack Majorana zero law | yes | local witness |
| Mass reduction to Dirac | yes | structural carrier |
| Majorana construction no-gos | yes | obstruction inventory |
| Globalization step | no | the open theorem object |
| `m_ββ` falsifier scaffold | bounded | from KamLAND-Zen comparator |

**Approachability:** Tier B. Existing scaffolding is real; the open
work is the globalization step.

**Falsifier (if landed):** any positive 0νββ signal up to experimental
precision falsifies Global Dirac. Predicts no Majorana phases
`alpha_21`, `alpha_31`.

### 2.2 Target 4E — Seesaw mass spectrum quantitative closure

**Identity (type-I seesaw):**

```text
m_nu  =  -m_D^T M_R^-1 m_D                                       (seesaw)
```

where `m_D` is the Dirac mass matrix (from neutrino Yukawa `Y_nu` × `v`)
and `M_R` is the right-handed Majorana mass matrix.

**What needs to be retained:**

- `M_R = diag(M_R1, M_R2, M_R3)` numerical spectrum (Phase 4 of
  `MASS_SPECTRUM_DERIVED_NOTE.md` is partial);
- Neutrino Yukawa structure `Y_nu` (analog of charged-lepton Koide on
  the neutrino carrier; lane file flags as "different carrier").

**Note:** if 4D lands as Global Dirac, type-I seesaw with Majorana M_R
is **excluded** (Dirac neutrinos have no right-handed Majorana mass).
The active mass spectrum then comes directly from `m_D = Y_nu * v`
without seesaw suppression. This forces an alternative mass-mechanism
question: how does the framework explain the smallness of `m_nu`
without a seesaw?

**Approachability:** Tier B-C. Highly dependent on 4D outcome.

### 2.3 Targets 4B, 4C — Mass-squared splittings

Once 4E (or its Dirac alternative) lands the active mass spectrum
`(m_1, m_2, m_3)`, the splittings follow by arithmetic:

```text
Delta m^2_21  =  m_2^2 - m_1^2
Delta m^2_31  =  m_3^2 - m_1^2
```

**Approachability:** Tier B-C; arithmetic once mass spectrum lands.

### 2.4 Target 4A — Absolute mass scale `m_lightest`

The hardest sub-target. Requires:
- the active mass spectrum from 4E (relative scale);
- an absolute-scale anchor (similar to how charged-lepton retention
  needs the absolute lepton scale `V_0` per Lane 6).

**Approachability:** Tier C. Likely needs a structural identity
analogous to YT-lane `y_t / g_s = 1/sqrt(6)` Ward identity, on the
neutrino carrier. The lane file flags "different carriers" — the
neutrino-side identity has not been articulated.

### 2.5 Target 4F — `Sigma m_nu` cosmological

Once `(m_1, m_2, m_3)` lands, `Sigma m_nu = m_1 + m_2 + m_3` is
arithmetic. Cross-checks against:
- retained `N_eff = 3.046` (3+0.046 thermal correction, from three
  generations);
- the hubble-h0 loop's structural-lock surface (no late-time
  modifications);
- the cosmological Σm_ν observational bound (`< 0.12 eV` from Planck +
  BAO; comparator only).

**Approachability:** Tier B. Mostly downstream arithmetic.

### 2.6 Target 4G — Cross-validation with retained δ_CP and θ_23

The DM closed package retains `delta_CP ≈ -81°` and
`theta_23 ≥ 0.5410` as falsifiable predictions. With the mass spectrum
landed (4A-4E), check:
- the predicted PMNS matrix structure with the retained zero law;
- consistency of `delta_CP` and `theta_23` with the retained two-
  amplitude last-mile reduction.

**Approachability:** Tier A. Internal consistency check.

## 3. Lane-3 / Lane-5 / Lane-6 dependency map

| Other lane | Affects which Lane-4 target? | How |
|---|---|---|
| Lane 3 (quark mass retention) | indirect | quark Yukawa structure may inform neutrino Yukawa structure (analog) |
| Lane 5 (Hubble H_0) | 4F | cosmological `Sigma m_nu` constraint cross-check |
| Lane 6 (charged-lepton mass retention) | 4A indirectly | absolute lepton scale `V_0` via tau Ward identity could inform `m_lightest` absolute scale by analogy |

Lane 4 is **largely independent** of Lanes 1, 2, 3 in primary closure
path (per lane file §7). It connects to Lane 5 via 4F and to Lane 6
via the absolute-scale analog for 4A.

## 4. Phase ordering

### Phase 1 (now)

1. **4D Dirac global lift.** Existing retained scaffolding (current-
   stack zero law + mass reduction to Dirac) makes this the most
   achievable Tier-B target. **Cycle 2 priority.**
2. **4E seesaw partial→retained, OR Dirac-alternative mass mechanism.**
   Conditional on 4D outcome. **Cycle 3 priority.**

### Phase 2 (after Phase 1)

3. **4B and 4C** arithmetic from 4E spectrum.
4. **4F** Σm_ν cosmological bridge to Lane 5.

### Phase 3 (after Phase 2)

5. **4A** absolute mass scale (hardest; needs structural identity on
   neutrino carrier).
6. **4G** cross-validation with retained δ_CP / θ_23.

## 5. Stretch-attempt candidates (per Deep Work Rules)

If the loop hits the audit-quota threshold (2 audit cycles in a row),
stretch-attempt candidates ordered by likely diagnostic value:

- **(SA1) 4A `m_lightest` from minimal axioms.** Hardest target. Even
  a partial result + named obstruction is valuable per Deep Work
  no-churn exception.
- **(SA2) 4D globalization step alone.** If Cycle 2 produces partial-
  lift only, the obstruction itself is the stretch target.
- **(SA3) Neutrino Yukawa structural identity attempt.** Analog of YT-
  lane `y_t / g_s = 1/sqrt(6)` for the neutrino carrier. May produce
  a no-go on the easy options + named structural premise needed.

## 6. What this plan closes and does not close

**Closes (claim-state movement):**

- Phase-ordered closure roadmap for Lane 4.
- Identification of 4D as the cleanest single-cycle Tier-B Phase-1
  target.
- Stretch-attempt candidate inventory for Deep Work Rules compliance.
- Cross-lane dependency map (Lane 5 for 4F; Lane 6 by analogy for 4A).

**Does not close:**

- Any neutrino mass or splitting numerically.
- 4D globalization step (open theorem object for Cycle 2).
- 4E seesaw spectrum / Dirac-alternative mass mechanism.
- Neutrino Yukawa structural identity.

## 7. Falsifier

The plan is structural; it does not predict values. It is falsified
if a Phase-2 derivation succeeds without retaining one of the listed
prerequisites (missed dependency) or if a Lane-4 target lands via an
entirely different methodology not enumerated here (unscored route).

Either outcome is a positive update to the plan.

## 8. Cross-references

- `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
  — Lane 4 lane file (primary authority).
- `docs/NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md` — neutrino
  retained boundary packet.
- `docs/NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md`
  — observable bounds.
- `docs/MASS_SPECTRUM_DERIVED_NOTE.md` Phase 4 — seesaw partial.
- `docs/NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` — Dirac carrier
  identity.
- `docs/NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` — local
  Majorana zero witness.
- `docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md` — PMNS local
  zero.
- `docs/NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md` — last-
  mile reduction.
- `docs/N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` — 4F
  upstream.
- `docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` and
  `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` —
  cosmology bridge for 4F (recently integrated upstream from the
  hubble-h0 loop).
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — `A_min`.
- DM closed package — δ_CP, θ_23 retained predictions for 4G.
- Loop pack at
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.

## 9. Boundary

This is a structural plan, not a theorem. It does not retire any
input, does not introduce a numerical claim, and does not promote
any cycle of work to retained status. It produces the loop's roadmap
so subsequent cycles target the right object.

A runner is not authored: the plan is editorial / structural; no new
symbolic or numerical content is introduced.
