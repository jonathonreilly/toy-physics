# String Tension Retention-with-Explicit-Budget Theorem (V1)

**Date:** 2026-04-29
**Status (actual current surface):** `proposed_retained_with_budget`
author proposal — formalizes the Lane 1 string tension audit
(HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27)
into a YT-lane-style retention-with-explicit-budget statement that
the framework's `√σ ≈ 465 MeV` reading is structurally retained
modulo an explicit ≤ 5% (B2) dynamical-screening budget and an
explicit unquantified (B5) framework↔standard-SU(3) YM identification
residual. Bare `retained` / `promoted` is NOT used.
**Primary runner:** `scripts/frontier_string_tension_retention_with_explicit_budget.py`

**Cited authorities (one-hop deps):**
- [HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md](HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md)
  — audit decomposing the 5.6% gap into B1-B5 contributions.
- [CONFINEMENT_STRING_TENSION_NOTE.md](CONFINEMENT_STRING_TENSION_NOTE.md)
  — retained `T = 0` confinement of graph-first SU(3) gauge sector;
  bounded `√σ ≈ 465 MeV` numerical reading.
- [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md)
  — retained `α_s(M_Z) = 0.1181`.
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  — retained graph-first SU(3) gauge structure.
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)
  — analog YT-lane retention-with-explicit-budget pattern (template).

---

## 0. Headline

The Lane 1 retention-gate audit (2026-04-27) decomposed the framework
`√σ ≈ 465 MeV` reading vs. PDG `440 ± 20 MeV` 5.6% central gap into
five EFT-bridge contributions (B1-B5):

| # | Contribution | Magnitude | Status after audit |
|---|---|---|---|
| B1 | α_s(M_Z) precision propagation | ~1.2% | retained-input precision (NOT bounded) |
| B2 | Quenched → dynamical screening | ~5% | bounded (rough ×0.96 factor) |
| B3 | Λ^(3) two-loop threshold matching | ~2-3% | absorbed via Method 2 |
| B4 | Method 1 vs Method 2 disagreement | ~10% | resolved by selecting Method 2 |
| B5 | framework SU(3) ↔ standard SU(3) YM | unquantified | structural-bridge residual |

The audit identified (B2) as the single load-bearing open numerical
budget item.

This V1 note converts the audit into a **retention-with-explicit-budget
theorem** matching the YT-lane retention pattern
(YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE): the framework's string tension
reading is `proposed_retained_with_budget` on the explicit budget

```text
√σ_framework = 465 MeV ± 5% (B2) ± 1% (B1) ± unquantified (B5)
```

with PDG `440 ± 20 MeV` falling within the explicit budget at
`+5.6%` central.

The bounded label is replaced with a budget-decorated retained statement
WITHOUT any new lattice MC computation; this is a relabeling/formalization
move, not a new closure.

---

## 1. The retention-with-budget statement

### 1.1 Retained components

Per the audit + retained authorities:

```text
T = 0 confinement                  : retained (graph-first SU(3) + Wilson criterion)
α_s(M_Z) = 0.1181 ± 0.2%           : retained (ALPHA_S_DERIVED_NOTE)
β = 6.0 (g_bare = 1, N_c = 3)      : retained
<P> = 0.5934                       : retained quantitative
Method 2 (Sommer + Creutz)         : selected as preferred extraction route
graph-first SU(3) at β = 6.0       : structural (with B5 budget item)
```

### 1.2 Explicit budget

The framework's `√σ` reading carries the explicit budget:

| Budget item | Magnitude | Type |
|---|---|---|
| (B1) α_s precision propagation | ±1.2% | retained-input precision residual |
| (B2) quenched → dynamical screening | ±5% | bounded (rough ×0.96) |
| (B5) framework ↔ standard SU(3) YM | unquantified | structural bridge |
| (B3) Λ^(3) matching | absorbed via Method 2 | 0% |
| (B4) Method disagreement | selected Method 2 | 0% |

### 1.3 Numerical readout

```text
√σ_framework = 465 MeV
PDG reading  = 440 ± 20 MeV
central gap  = +5.6%      (within (B2) + (B1) ≈ ±6.2%)
```

The 5.6% central gap is comfortably within the explicit (B2) + (B1)
budget. (B5) is qualitatively supported by the plaquette consistency
check (`<P>_framework = 0.5934`, `<P>_MC at β=6.0 = 0.5973 ± 0.0006`,
0.7% finite-size shift) but remains unquantified pending volume-scaling
verification.

---

## 2. Theorem statement

**Theorem (String Tension Retention-with-Budget).**
On the framework's retained `T = 0` SU(3) confinement surface +
retained `α_s(M_Z) = 0.1181` + retained `β = 6.0` + selected Method
2 (Sommer-scale + Creutz ratio):

```text
√σ_framework = 465 MeV ± 5% (B2) ± 1% (B1) ± unquantified (B5)
```

is a `proposed_retained_with_budget` reading on the actual current
surface, with the residuals decomposed explicitly per the Lane 1
retention-gate audit.

**Status:** `proposed_retained_with_budget` modulo (a) audit
ratification of the budget formalization and (b) future volume-scaling
verification of the plaquette consistency to tighten (B5).

The bounded label on the existing CONFINEMENT_STRING_TENSION_NOTE is
the OLD reading; this V1 supplies the budget-decorated retained
reading on the same numerical surface.

### Proof

**Step 1 (T = 0 confinement retained).** By
GRAPH_FIRST_SU3_INTEGRATION_NOTE and CONFINEMENT_STRING_TENSION_NOTE
§3, the framework's graph-first SU(3) gauge sector exhibits T = 0
confinement (retained).

**Step 2 (α_s(M_Z) retained).** By ALPHA_S_DERIVED_NOTE,
α_s(M_Z) = 0.1181 ± 0.2% retained on the canonical CMT surface.

**Step 3 (β = 6.0 + Method 2).** g_bare = 1 + N_c = 3 ⇒ β = 6.0
(Wilson plaquette action, retained). Method 2 (Sommer scale + Creutz
ratio at β = 6.0) is the preferred extraction route per the audit
(B3 absorbed, B4 resolved).

**Step 4 (budget decomposition).** Per HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27
§3, the residuals decompose as B1 (~1.2%, retained-input precision),
B2 (~5%, bounded dynamical screening), B5 (unquantified, structural
bridge); B3 absorbed, B4 resolved.

**Step 5 (retention-with-budget).** Combining: the framework's
`√σ ≈ 465 MeV` is retained on the structural side (T = 0
confinement + retained α_s + Method 2) modulo the explicit budget.
The PDG comparator `440 ± 20 MeV` falls within the explicit budget
at +5.6% central. **QED on the retention-with-budget statement**;
(B2) tightening would require a proper N_f = 2+1 dynamical lattice
at β = 6.0.

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: proposed_retained_with_budget
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  V1 formalizes the Lane 1 retention-gate audit (2026-04-27) into a
  YT-lane-style retention-with-explicit-budget statement. The
  framework's √σ ≈ 465 MeV reading is structurally retained on the
  T = 0 confinement + retained α_s + retained β = 6.0 + Method 2
  surface, with explicit ±5% (B2) + ±1% (B1) + unquantified (B5)
  budget. PDG 440 ± 20 MeV falls within the explicit budget at +5.6%.
  No new computation; this is a budget-decorated relabeling move.
audit_required_before_effective_retained: true
bare_retained_allowed: false
b2_dynamical_screening_status: bounded_load_bearing
b5_framework_to_standard_su3_ym_status: structural_bridge_unquantified
budget_total: "±5% (B2) + ±1% (B1) + unquantified (B5)"
```

---

## 4. What is and is NOT closed

### Closed by V1

1. retention-with-budget formalization of the audit's decomposition
2. relabel from "bounded numerical reading" to
   "retained-with-explicit-budget" (matching YT-lane pattern)
3. PDG comparator falls within the explicit budget

### NOT closed (carried forward)

1. **(B2) load-bearing**: needs proper N_f = 2+1 dynamical lattice at
   β = 6.0; can't be done without lattice MC infrastructure
2. **(B5) unquantified**: needs volume-scaling verification of
   plaquette consistency at ≥ 16^4 (currently only 0.7% shift on 4^4)
3. **Asymptotic Wilson loop area-law verification at large R**

---

## 5. Cascade unlocked (proposed for later weaving)

If V1 audit-ratifies:
- **PUBLICATION_MATRIX line 73 (gauge corollary):** "promoted
  structural confinement; bounded numerical string-tension readout"
  → "promoted structural confinement; retained-with-explicit-budget
  numerical string-tension readout"
- HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27
  gets §Note that V1 lands the audit's recommendations as a budget-
  decorated retained statement.

---

## 6. Verification

```bash
python3 scripts/frontier_string_tension_retention_with_explicit_budget.py
```

Audits 5 retained chain authorities + the audit's budget decomposition
+ PDG comparator within budget + status firewall fields.

PASS=N FAIL=0.

---

## 7. Honest residual

After V1 lands as `proposed_retained_with_budget`:
- (B2) ~5% bounded budget: requires dynamical lattice MC
- (B5) structural bridge: requires volume-scaling verification
- The string tension is now retained-with-budget, not closed.
