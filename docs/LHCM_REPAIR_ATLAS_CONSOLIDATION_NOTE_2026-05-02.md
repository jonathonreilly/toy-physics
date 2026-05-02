# LHCM Repair Atlas Consolidation: Cycles 1–3 + RH Uniqueness as a Single Authority Surface

**Date:** 2026-05-02
**Status:** exact-support batch theorem on retained graph-first surface
modulo SM-definition conventions. NOT proposed_retained — see
CLAIM_STATUS_CERTIFICATE.md. This note consolidates the audit-backlog
campaign cycles 1-3 (PRs #254, #255, #256) plus PR #253 plus
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` into a single
LHCM atlas, identifying the unique remaining residual as the
SM-definition-convention reclassification under audit policy.
**Primary runner:** `scripts/frontier_lhcm_repair_atlas_consolidation.py`
**Authority role:** support-batch atlas / consolidation theorem providing a
single audit-graph entry for the LHCM repair chain.

## 0. Summary

[`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) was flagged as `audited_conditional`
with three named verdict-residuals (matter assignment, U(1)_Y normalization,
anomaly-complete chiral completion). The audit-backlog campaign's cycles
1–5, together with PR #253 and `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS`,
together cover all five named LHCM repair items as exact-support theorems
on the retained graph-first surface, modulo two admitted SM-definition
conventions:

- `Q_e = −1` in elementary charge units (overall scale fixing)
- color-charged ↔ quark / color-singlet ↔ lepton (matter labelling)

Both are admitted naming conventions in SM, not derivations from physics.
Once the audit ledger explicitly classifies these as "narrow non-derivation
labelling context", LHCM can lift to retained.

## 1. The LHCM repair chain

| LHCM item | Closure | Status | Authority |
|-----|---|---|---|
| (1) matter assignment Sym²(3) ↔ Q_L, Anti²(1) ↔ L_L | cycle 2 (PR #255) | exact-support modulo SM-definition labels | [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) |
| (2) U(1)_Y normalization α = +1 | cycle 3 (PR #256) | exact-support modulo Q_e = −1 convention | [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md) |
| (3) anomaly LH SU(2)²×U(1)_Y | PR #253 | exact-support | [`LH_DOUBLET_SU2_SQUARED_HYPERCHARGE_ANOMALY_CANCELLATION_NOTE_2026-05-01.md`](LH_DOUBLET_SU2_SQUARED_HYPERCHARGE_ANOMALY_CANCELLATION_NOTE_2026-05-01.md) (open PR) |
| (3) anomaly R-A SU(3)²×Y | cycle 1 (PR #254) | exact-support | [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md) |
| (3) anomaly R-B Y³ | cycle 1 (PR #254) | exact-support | (same) |
| (3) anomaly R-C grav²×Y | cycle 1 (PR #254) | exact-support | (same) |
| RH hypercharge uniqueness from (R-A,B,C) + Y(ν_R)=0 + Q(u_R)>0 | `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` | proposed_retained / unaudited | (same) |

## 2. Authority chain

```
graph_first_su3_integration_note (RETAINED, td=312)
  │
  ├─→ Sym²(3) ⊕ Anti²(1) split under residual permutation τ on 4-point base
  │     (canonical commutant gl(3)⊕gl(1))
  │
  ├─→ unique traceless abelian generator with eigenvalue ratio 1:(−3)
  │     on Sym²:Anti² (free overall scale α)
  │
  └─→ (Cycle 2 / PR #255): Sym²(3) carries SU(3) fundamental, Anti²(1)
        carries SU(3) trivial; matter assignment forced by SU(3) rep content
        modulo SM-definition labels (color-charged ↔ quark, color-singlet ↔ lepton).

  +
  graph_first_selector_derivation_note (RETAINED, td=311)
  +
  PR #253 (open): SU(2)²×U(1)_Y anomaly cancellation for LH doublets
  +
  PR #254 / cycle 1: (R-A) SU(3)²×Y, (R-B) Y³, (R-C) grav²×Y identities
        as exact rational arithmetic on the full one-generation content
        (parametric in α).

  +
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS (proposed_retained, unaudited):
    given LH content + neutral ν_R + Q(u_R)>0 + (R-A,B,C) anomaly
    cancellation, RH content uniquely (4α/3, −2α/3, −2α, 0).
    Solves cubic 9x²−6x−8 = 0 with rational roots {4/3, −2/3}.

  =
  PR #256 / cycle 3: SM-definition convention Q_e = −1 (= −α via Q = T_3 + Y/2
    on SU(2) singlets) fixes α = +1 uniquely, yielding all 6 SM Y values:
      Y(Q_L)=+1/3, Y(L_L)=−1, Y(u_R)=+4/3, Y(d_R)=−2/3, Y(e_R)=−2, Y(ν_R)=0.
```

## 3. The single remaining residual

The full LHCM closure depends on **two SM-definition conventions**:

1. **Q_e = −1**: the elementary charge unit, fixed by the SM convention that
   the electron has charge −1. This is a NAMING convention.

2. **color-charged ↔ quark, color-singlet ↔ lepton**: the SM naming of
   fermion species by their SU(3) representation. This is a labeling convention.

Neither is a physics derivation. Both are SM-definition labelings.

For LHCM to lift to retained, the audit ledger must **explicitly classify
these conventions as "narrow non-derivation labelling context"** under
Criterion 3 of the retained-proposal certificate. This is a governance
decision, not a derivation task.

The deeper Nature-grade target — derivation of the SM photon
`Q = T_3 + Y/2` from graph-first surface — would close the SM convention
input but is significantly harder (electroweak symmetry breaking +
identification of the unbroken U(1)_em on graph-first surface).

## 4. What this consolidation atlas does

- **Provides a single audit-graph entry** that summarizes the LHCM repair
  chain across 6 source notes (PR #253, cycles 1-3, SM hypercharge
  uniqueness, plus the parent LHCM note).
- **Identifies the unique remaining residual** as governance/policy
  classification of SM-definition conventions, not a derivation gap.
- **Provides a clear path to LHCM retention**: explicit Criterion-3
  classification, audit ratification of cycles 1-3 + PR #253, and audit of
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS.

## 5. What this consolidation atlas does NOT do

- It does **not** promote LHCM to retained. That requires audit ledger
  decisions on (a) SM-definition convention classification and (b)
  ratification of cycles 1-3 + PR #253.
- It does **not** derive the SM-definition conventions from physics. They
  are naming conventions.
- It does **not** derive the SM photon `Q = T_3 + Y/2` from graph-first
  surface. That is a deeper Nature-grade target.

## 6. Validation

- primary runner:
  [`scripts/frontier_lhcm_repair_atlas_consolidation.py`](../scripts/frontier_lhcm_repair_atlas_consolidation.py)
  — verifies (a) note structure, (b) all 6 LHCM repair items are mapped to
  closure authorities, (c) the parametric-α structure connecting the cycles
  is consistent at exact Fraction precision, (d) the two SM-definition
  conventions are explicitly listed.

## 7. Authority surface

```yaml
actual_current_surface_status: exact-support batch
conditional_surface_status: |
  consolidation atlas of cycles 1-3 + PR #253 + STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
  modulo two SM-definition conventions:
    1. Q_e = -1 (elementary charge unit, naming)
    2. color-charged ↔ quark, color-singlet ↔ lepton (matter naming)
hypothetical_axiom_status: null
admitted_observation_status: |
  Q_e = -1 (cycle 3)
  SM-definition matter labelling (cycle 2)
proposal_allowed: false
proposal_allowed_reason: |
  Criterion 3 fails — SM-definition conventions are load-bearing for the
  cumulative LHCM closure. Reclassification of these conventions as
  "narrow non-derivation labelling context" requires audit-ledger
  governance decision, not a derivation.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 8. Cross-references

### Closure chain

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — parent (audited_conditional)
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained primitive (td=312)
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md) — retained primitive (td=311)
- [`LH_DOUBLET_SU2_SQUARED_HYPERCHARGE_ANOMALY_CANCELLATION_NOTE_2026-05-01.md`](LH_DOUBLET_SU2_SQUARED_HYPERCHARGE_ANOMALY_CANCELLATION_NOTE_2026-05-01.md) — PR #253 (open)
- [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md) — PR #254 (cycle 1)
- [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) — PR #255 (cycle 2)
- [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md) — PR #256 (cycle 3)
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — proposed_retained, unaudited (sister)

### Audit chain

- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) — audited_renaming (sister algebra)
- [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) — audited_conditional
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md) — audited_conditional
- [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md) — audited_conditional
