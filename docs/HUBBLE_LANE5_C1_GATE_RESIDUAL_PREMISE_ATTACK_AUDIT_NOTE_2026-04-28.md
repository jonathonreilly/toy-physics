# Lane 5 `(C1)` Absolute-Scale Gate — Residual-Premise Attack Audit

**Type:** open_gate

**Date:** 2026-04-28
**Status:** open_gate — branch-local attack-audit note enumerating
surviving research-level attack candidates on the (G1 edge-statistics
principle + G2 action-unit metrology) coupled residual premise on
`P_A H_cell`. Cycle 1 of the (C1) gate loop. Builds on the 2026-04-26
`(C1)` gate audit which isolated this single residual premise. This
audit identifies which attack candidates are single-cycle attemptable
vs. research-level distant; no attack is closed here, so the gate
remains open.
**Lane:** 5 — Hubble constant `H_0` derivation
**Loop:** `hubble-c1-absolute-scale-gate-20260428`

---

## 0. Context

The 2026-04-26 `(C1)` gate audit
(`HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`) established:

- Three Planck-lane targets (Target 1 gravity/action unit-map; Target 2
  horizon-entropy `1/4` carrier; Target 3 information/action bridge)
  collapse to a **single coupled residual premise**: the metric-
  compatible primitive Clifford/CAR coframe response on the rank-four
  primitive boundary block `P_A H_cell ⊆ H_cell`.
- Coupled decomposition:
  - **(G1) Edge-statistics principle:** force CAR semantics on
    `P_A H_cell` (vs. non-CAR ququart / two-qubit semantics that
    rank-4 alone admits).
  - **(G2) Action-unit metrology:** break the `(S, κ) → (λS, λκ)`
    rescaling degeneracy that the Hilbert-only stack leaves intact.
- (G1) and (G2) are not independent: per the conditional Clifford
  phase bridge, deriving the Clifford coframe response on `P_A H_cell`
  + adopting natural phase/action units gives both `c_Widom = 1/4`
  and `G_Newton,lat = 1`, yielding `a/l_P = 1`.

**Result of (C1) closure (per 2026-04-26 audit):** closed-gate `a/l_P
= 1`, hence `a^{-1} = M_Pl` derived numerically; conditional Clifford
phase bridge marked closed in that audit; `R_Λ` numerical
retention chain unlocked; (C1) half of two-gate Hubble dependency
closed.

This audit (Cycle 1) goes one step further: enumerates **surviving
research-level attack candidates on (G1+G2)** so that future
single-cycle stretch attempts are well-targeted.

## 1. Six candidate attack frames on (G1+G2)

### A1 — Direct A_min derivation of CAR from Z³ + Cl(3) substrate

**Premise:** the minimal axiom stack `A_min` (`MINIMAL_AXIOMS_2026-04-11.md`)
specifies local Cl(3) + Z³ substrate + finite local Grassmann/staggered-
Dirac partition. The Grassmann partition functor on lattice fermions
is **canonically anticommutative** by definition.

**Mechanism:** show that the rank-four primitive boundary block
`P_A H_cell` inherits the Grassmann anticommutation from the bulk
finite local Grassmann/staggered-Dirac partition (axiom 3), forcing
CAR semantics rather than ququart/two-qubit alternatives.

**Constraint count:** Grassmann anticommutation on the bulk; need
to verify the boundary projection P_A preserves the anticommutation
structure (i.e., P_A is a Clifford-module morphism, not an arbitrary
projection).

**Status:** **HIGH** promise; single-cycle attemptable. Direct
derivation from axiom 3 (Grassmann partition) closing (G1) on the
`P_A` boundary block.

### A2 — Action-unit metrology via retained `g_bare = 1` axiom

**Premise:** axiom 4 of `A_min` retains `g_bare = 1` as the gauge-
coupling normalization. This is a **dimensionful constraint** that
fixes the action-unit scale on the bulk.

**Mechanism:** show that retained `g_bare = 1` plus retained Cl(3)
bivector → SU(2) gauge structure plus admitted lattice unit `a`
fixes the action-unit scale on `P_A H_cell` to natural units, breaking
the `(S, κ)` rescaling degeneracy.

**Constraint count:** retained `g_bare = 1` directly constrains the
action density. The question is whether this constrains the boundary-
block action-unit metrology.

**Status:** **MEDIUM-HIGH** promise; needs sharper audit of how
`g_bare = 1` projects onto the P_A boundary block. Likely single-
cycle attemptable if axiom 4 alone closes (G2).

### A3 — Combined A1 + A2: A_min closes coupled (G1+G2)

**Premise:** if A1 closes (G1) and A2 closes (G2), then `A_min`
alone closes the coupled (G1+G2) residual premise — exactly what
the 2026-04-26 audit flagged as the closure pathway.

**Mechanism:** combine the Grassmann-from-axiom-3 derivation (A1)
with the action-unit-from-axiom-4 derivation (A2).

**Status:** depends on A1 and A2 separately. If both land single-
cycle, this is a **direct (C1) closure on `A_min` alone**. Highest-
leverage outcome if achievable.

### A4 — Edge-statistics from primitive parity-gate carrier theorem

**Premise:** the retained
`AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`
establishes a primitive parity-gate carrier on the rank-four block.
Parity-gate structure may force CAR (vs. non-CAR) semantics
without needing to invoke the bulk Grassmann partition.

**Mechanism:** parity-gate structure on `P_A H_cell` + Clifford
module identification ⟹ CAR semantics (alternative to A1).

**Status:** **MEDIUM** promise; needs audit of whether parity-gate
+ rank-4 force CAR specifically.

### A5 — Carrier-axiom compatibility audit (Phase-2 fallback)

**Premise:** if A1+A2+A3+A4 all fail to close (G1+G2) on `A_min`
alone, identify the **minimal carrier axiom** that would close the
gate without violating the framework's no-fitted-parameter posture
or the methodology of single-axiom retention.

**Mechanism:** enumerate carrier-axiom candidates (minimal CAR
posit, minimal action-unit posit, minimal Clifford coframe posit),
audit each for compatibility with the existing framework surface.

**Status:** **fallback** route; would represent "honest stop on
A_min closure of (C1); minimal-carrier-axiom extension required".
Audit-grade Phase-2.

### A6 — Cross-lane impact via landed spectral-gap identity

**Premise:** retained `Λ = 3/R_Λ²` plus retained `H_inf = c/R_Λ`
plus closed (C1) gate ⟹ retained absolute `R_Λ` ⟹ retained `H_inf`.
This is the **outcome** of (C1) closure, not an attack on (G1+G2);
included for completeness.

**Status:** outcome only; not an attack frame on (G1+G2). Mentioned
for cross-lane chain documentation.

## 2. Synthesis

| Candidate | Promise | Single-cycle? | Dependencies |
|---|---|---|---|
| **A1 Grassmann-from-axiom-3 ⇒ CAR (G1)** | **HIGH** | **yes** | axiom 3 verification on P_A boundary |
| **A2 g_bare=1 ⇒ action-unit (G2)** | **MEDIUM-HIGH** | likely yes | axiom 4 projection onto P_A |
| **A3 A1+A2 combined ⇒ (G1+G2) closed** | **HIGHEST if A1+A2 land** | yes (sequential) | A1, A2 |
| A4 Parity-gate ⇒ CAR (G1) | medium | needs audit | retained parity-gate theorem |
| A5 Minimal-carrier-axiom audit | fallback | yes (audit-grade) | A1-A4 fail |
| A6 Spectral-gap chain (outcome) | not an attack | n/a | (C1) already closed |

**Recommended Cycle 2:** **A1 stretch attempt** — derive CAR
semantics on `P_A H_cell` from axiom 3 (finite local Grassmann/
staggered-Dirac partition). This is the cleanest single-cycle
attack frame on (G1) and would either close (G1) or honestly
identify the structural obstruction.

**Recommended Cycle 3:** if A1 lands, **A2 stretch attempt** —
derive action-unit metrology on `P_A H_cell` from axiom 4
(`g_bare = 1`). Closure of A2 plus A1 closes A3 (the full coupled
(G1+G2) residual premise on `A_min` alone).

**Reject:** A6 as not an attack frame; A5 as fallback only.

## 3. Phase ordering

### Phase 1 (this loop)

1. **Cycle 1 (this audit):** enumerate attack candidates A1-A6.
2. **Cycle 2:** A1 stretch attempt — Grassmann-from-axiom-3
   ⇒ CAR on P_A boundary block (closes G1).
3. **Cycle 3:** A2 stretch attempt — `g_bare = 1` ⇒ action-unit
   metrology on P_A boundary block (closes G2).
4. **Cycle 4 (if A1+A2 both land):** A3 consolidation — combined
   theorem closing (G1+G2) on `A_min` alone, retaining (C1) gate.

### Phase 2 (cross-lane impact if Phase 1 succeeds)

5. **Conditional Clifford phase bridge promotion** to retained.
6. **Targets 1, 2, 3 closure** per 2026-04-26 (C1) audit §3.
7. **Hubble two-gate dependency** half-closure: (C1) closed;
   (C2)/(C3) gate becomes the remaining bottleneck.
8. **Lane 4F-β follow-on:** with bounded `h` (still requires
   (C2)/(C3) closure for full retention), Σm_ν bounded interval
   becomes attemptable.

### Phase 2 fallback (if A1, A2 fail)

5'. **Cycle 4:** stuck fan-out for alternate (G1+G2) closure
   mechanisms (A4 parity-gate route + A5 minimal-carrier-axiom
   audit).
6'. **Cycle 5:** A5 audit-grade output identifying minimal carrier-
   axiom extension as honest research-level Phase-2 candidate.
7'. **Honest stop** on the (C1) loop with the audit-attack inventory
   landed; flag `A_min`-closure-of-(C1) as research-level distant.

## 4. What this audit closes and does not close

**Closes:**

- Inventory of six candidate attack frames A1-A6 on (G1+G2)
  coupled residual premise.
- Identification that A1+A2 = A3 represents the **highest-leverage
  single-cycle attack pathway** to closing (C1) on `A_min` alone.
- Phase ordering for Cycles 2-4 (Phase 1) plus fallback Phase
  2 ordering.
- Cross-lane chain documentation for outcome of (C1) closure.

**Does not close:**

- (C1) gate itself.
- (G1) edge-statistics principle.
- (G2) action-unit metrology.
- Any A1-A6 attack frame.

## 5. Cross-references

- 2026-04-26 (C1) gate audit (primary anchor):
  `docs/HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`.
- 2026-04-26 (C2) gate audit (companion):
  `docs/HUBBLE_LANE5_ETA_RETIREMENT_GATE_AUDIT_NOTE_2026-04-26.md`.
- 2026-04-27 two-gate dependency firewall:
  `docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`.
- A_min foundation:
  `docs/MINIMAL_AXIOMS_2026-04-11.md`.
- 2026-04-25 area-law CAR semantics tightening:
  `docs/AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md`.
- 2026-04-25 primitive parity-gate carrier (A4 candidate anchor):
  `docs/AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md`.
- 2026-04-25 primitive-CAR edge identification:
  `docs/AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md`.
- Conditional Clifford phase bridge:
  `docs/PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`
  (referenced from 2026-04-26 (C1) audit §0).
- 4F-loop fan-out (cross-lane motivation):
  `docs/NEUTRINO_LANE4_4F_PHASE2_ATTACK_FRAME_FANOUT_NOTE_2026-04-28.md`
  (F1 → this loop).
- Loop pack:
  `.claude/science/physics-loops/hubble-c1-absolute-scale-gate-20260428/`.

## 6. Boundary

This is an audit / theorem-plan note. It does not retain (G1) or
(G2), does not close (C1), does not promote any conditional theorem
to retained. It produces the **attack inventory** for surviving
research-level routes on the coupled (G1+G2) residual premise and
recommends Cycles 2-3 as the highest-leverage stretch-attempt
sequence (A1 then A2, both targeting `A_min`-only closure).

A runner is not authored.
