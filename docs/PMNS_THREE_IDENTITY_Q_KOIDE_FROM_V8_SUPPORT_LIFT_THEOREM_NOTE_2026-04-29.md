# PMNS Three-Identity Q_Koide-from-V8 Support Lift Theorem (V1)

**Date:** 2026-04-29
**Status:** support: V8-derived chart-constant lift, conditional on V8 (Block 1) ratification; PMNS selector laws and broader gate remain open.
This support-grade lift composes V8 (Block 1, Q_Koide = 2/3 on A_min)
with the PMNS three-identity selector support (2026-04-21) to upgrade
the chart constant `Q_Koide = 2/3` from "imported numeric constant" to
"V8-derived structural value on A_min". The three open gaps in the
PMNS three-identity package (proposed selector laws, basin uniqueness,
broader PMNS/DM gate) are unchanged. Stronger headline tier language is
NOT used.
**Primary runner:** `scripts/frontier_pmns_three_identity_q_koide_from_v8_support_lift.py`

**Cited authorities (one-hop deps):**
- [KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md](KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md)
  — V8 (Block 1) Q_Koide = 2/3 on A_min, support/audit-pending.
- [PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md)
  — PMNS three-identity support proposal using Q_Koide = 2/3 +
  SELECTOR = √6/3 + chart constants gamma, E1, E2.

---

## 0. Headline

The PMNS three-identity support package (2026-04-21) uses Q_Koide = 2/3
as one of the chart constants on the affine Hermitian PMNS chart:

```text
gamma = 1/2
E1 = sqrt(8/3)
E2 = sqrt(8)/3
Q_Koide = 2/3      ← imported as numeric constant
SELECTOR = sqrt(6)/3
```

with the scalar identity `SELECTOR² = Q_Koide = 2/3`.

V8 (Block 1, 2026-04-29) now records Q_Koide = 2/3 on A_min as
support via the OP-locality structural chain, audit pending. This V1 note composes the two: the
PMNS chart constant `Q_Koide = 2/3` is no longer an imported numeric
constant; it is now a V8-derived structural value on A_min.

The composition:
- removes one import from the PMNS chart;
- ties the PMNS three-identity selector candidate laws structurally
  to the charged-lepton sector via V8;
- but does NOT close the three open gaps in the PMNS support
  proposal (proposed selector laws delta·q_+ = Q_Koide and det(H) =
  E2 are still proposed, basin uniqueness is still bounded multi-start,
  broader PMNS/DM gate still open).

V1 is support-grade, not closure.

---

## 1. The composition

### 1.1 V8 (Block 1) closure of Q_Koide

By V8 (Block 1):
```text
Q_Koide = (Σ √m_l)² / (Σ m_l) = 2/3
```
on the A_min surface, via OP-locality + canonical-descent + CRIT.
Status: support, audit-pending.

### 1.2 PMNS chart constant

By PMNS_SELECTOR_THREE_IDENTITY_SUPPORT, the PMNS chart constant
Q_Koide = 2/3 is imported as a numeric value into the affine
Hermitian chart H(m, δ, q_+). The scalar identity SELECTOR² = Q_Koide
ties SELECTOR = √6/3 to Q_Koide = 2/3.

### 1.3 Composed chart with V8-derived Q_Koide

Substituting V8's structural derivation into the PMNS chart:

```text
Q_Koide       = 2/3       (V8 / Block 1 on A_min)
SELECTOR      = √6/3      (= √Q_Koide, derived from V8)
SELECTOR²     = Q_Koide   (algebraic identity, retained)
gamma, E1, E2: chart constants on retained Hermitian chart
```

The PMNS chart constant Q_Koide is now V8-derived; the PMNS three-
identity system

```text
Tr(H)         = Q_Koide
delta · q_+   = Q_Koide      (proposed selector law)
det(H)        = E2           (proposed selector law)
```

now uses Q_Koide as a V8-derived structural value rather than an
imported numeric.

---

## 2. Theorem statement

**Theorem (PMNS Three-Identity Q_Koide-from-V8 Support Lift).**
On the A_min surface with V8 (Block 1) closure of Q_Koide = 2/3:

1. The PMNS three-identity chart constant Q_Koide is V8-derived.
2. The associated chart constant SELECTOR = √Q_Koide = √6/3 is
   V8-derived.
3. The three-identity numerical solution
   `(m_*, δ_*, q_+*) = (2/3, 0.9330..., 0.7145...)` and the resulting
   PMNS observables are unchanged; their interpretation is now
   V8-supported on the chart side.

**Status:** support. The three open PMNS gaps (proposed selector laws
not yet closed, basin uniqueness bounded multi-start, broader PMNS/DM
gate open) are unchanged.

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: support
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  V1 composes V8 (Block 1 support/audit-pending Q_Koide closure
  attempt) with the PMNS three-identity support package. The chart
  constant Q_Koide = 2/3 lifts from "imported numeric" to
  "V8-derived structural value". Three open PMNS gaps are unchanged,
  so the surface remains support.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposed_selector_laws_status: open
basin_uniqueness_status: bounded_multi_start
broader_pmns_dm_gate_status: open
```

---

## 4. What is and is NOT closed

### Support-tier lift recorded by V1
1. PMNS chart constant Q_Koide = 2/3 is now V8-derived
2. SELECTOR = √Q_Koide = √6/3 is V8-derived
3. PMNS three-identity numerical solution unchanged but
   structurally V8-supported

### NOT closed (carried forward, unchanged from PMNS support note)
1. Proposed selector law `delta · q_+ = Q_Koide` — still proposed
2. Proposed selector law `det(H) = E2` — still proposed
3. Basin uniqueness — bounded multi-start, not analytic uniqueness
4. Broader PMNS/DM gate — open

---

## 5. Integration boundary

This support-tier note does not change downstream publication rows.
Later weaving must wait for independent V8 ratification and must
continue to carry the open PMNS selector-law and broader-gate fields.

---

## 6. Verification

```bash
python3 scripts/frontier_pmns_three_identity_q_koide_from_v8_support_lift.py
```

Audits V8 + PMNS three-identity authorities + Q_Koide chain
substitution + status firewall fields. PASS=N FAIL=0.

---

## 7. Honest residual

PMNS three-identity remains support-grade; V1 only retires the chart-
constant import. The three open gaps from PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE
are unchanged.
