# LHCM Chain Audit Map Synthesis Meta Note

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the transitive upstream closure of the
LHCM family — `left_handed_charge_matching_note` plus the four
`lhcm_*` and `higgs_y_from_lhcm_*` rows that share the same
load-bearing graph-first surface — and the audit-status distribution
across that closure. Documents the finding so future automated
audit-backlog or retained-promotion campaigns target the right
frontier rows and use the recorded repair classes when wiring
follow-on cycles.
**Companion to:**
- [`docs/audit/README.md`](audit/README.md) (audit-lane policy:
  retained-grade dependencies, repair classes, terminal verdicts)
- [`AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)
  (campaign-level template for backward-looking synthesis notes
  citing already-applied audit data)
- [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
  (six-item LHCM repair atlas consolidating cycles 1-3 + PR #253 +
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS)
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  (parent LHCM source note)
- [`THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md)
  (sibling dep-chain audit template)
**Primary runner:** [`scripts/frontier_lhcm_chain_audit_map_synthesis.py`](../scripts/frontier_lhcm_chain_audit_map_synthesis.py)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note is
backward-looking: it cites already-recorded audit verdicts in
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json) and
synthesises the structural shape of the LHCM upstream closure. It does
not promote theorems, does not modify retained content, does not
propose new derivations, and does not reclassify any audit row. No new
vocabulary, claim type, or framing is introduced. All terminal-verdict
language used here (`audited_clean`, `audited_conditional`,
`unaudited`, `effective_status`, `retained_bounded`, `retained_no_go`,
`open_gate`, `meta`, `missing_dependency_edge`,
`runner_artifact_issue`, `dependency_not_retained`,
`scope_too_broad`, `missing_bridge_theorem`) is repo-canonical and
matches the audit lane's existing field values per
[`docs/audit/README.md`](audit/README.md).

## Naming

Throughout this note:
- **"the LHCM family"** = the five-row cluster on the live ledger:
  - **the parent** =
    [`docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) —
    claim_id `left_handed_charge_matching_note`
  - **the matter-assignment row** =
    [`docs/LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) —
    claim_id `lhcm_matter_assignment_from_su3_representation_note_2026-05-02`
  - **the Y-normalization row** =
    [`docs/LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md) —
    claim_id `lhcm_y_normalization_from_anomaly_and_convention_note_2026-05-02`
  - **the consolidation atlas** =
    [`docs/LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md) —
    claim_id `lhcm_repair_atlas_consolidation_note_2026-05-02`
  - **the Higgs-Y row** =
    [`docs/HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`](HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md) —
    claim_id `higgs_y_from_lhcm_and_yukawa_structure_note_2026-05-02`
- **"the parent core upstream"** = the five-row transitive upstream
  closure of the parent (the parent's tightest dep chain, listed
  explicitly in §3 below)
- **"the family upstream closure"** = the union of the transitive
  upstream closures of the five LHCM-family rows above (132 rows on
  the live ledger as of 2026-05-10)
- **"frontier row"** = a row in the upstream closure whose
  `audit_status` is `unaudited` or `audited_conditional` (i.e.,
  not yet `audited_clean`)
- **"chain root"** = the parent row `left_handed_charge_matching_note`
  itself — the row on which the LHCM ledger position is anchored
- **"repair class"** = the audit-lane field tagging the kind of work
  that would close a row's audit verdict, per
  [`docs/audit/README.md`](audit/README.md) §"Workflow audited_conditional
  repair-class prefix" (`runner_artifact_issue`,
  `dependency_not_retained`, `missing_dependency_edge`,
  `missing_bridge_theorem`, `scope_too_broad`, `compute_required`,
  `other`)

## Scope

This note synthesises three pieces of audit-graph data that the
ledger already carries:

1. The **parent core upstream**: a small five-row chain rooted in the
   two retained-bounded graph-first authorities, the open
   staggered-Dirac realization gate, the `MINIMAL_AXIOMS_2026-05-03`
   meta row, and the LH-doublet narrow ratio theorem (currently
   `unaudited`).
2. The **family upstream closure**: a 132-row transitive upstream
   for the LHCM-family cluster, picked up via the broader hypercharge
   uniqueness and anomaly-cancellation references that the
   matter-assignment, Y-normalization, consolidation atlas, and
   Higgs-Y rows additionally cite.
3. The **frontier breakdown**: the audit-status distribution across
   the family upstream closure, sorted by repair class as recorded in
   [`docs/audit/data/repair_class_backfill_log.json`](audit/data/repair_class_backfill_log.json).

This is the dep-chain map analog for LHCM of the
`THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md` packet
that closed the dep-chain-status review for that lane. It does not
produce a closure proposal: closure work for the LHCM repair items
already exists in the consolidation atlas and the recently-shipped
proof-walk note suite (see §6 below). This synthesis localises which
upstream row is the structurally cheapest target for downstream
retained-promotion attempts.

## 1. The chain root

`left_handed_charge_matching_note` — current ledger row (read live from
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json)):

- `claim_type`: `bounded_theorem`
- `audit_status`: `unaudited`
- `effective_status`: `unaudited`
- `criticality`: `critical`
- `transitive_descendants`: 715 (was 713 before this PR adds the
  chain-map synthesis meta note + the matter-assignment block
  proof-walk note as downstream descendants)
- `direct_in_degree`: 37 (was 36 before this PR adds the matter-
  assignment block proof-walk note as a direct citing row)
- `load_bearing_score`: 27.984 (recomputed by the pipeline after
  this PR; was 27.48 prior)
- `deps`: [
    `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`,
    `graph_first_selector_derivation_note`,
    `graph_first_su3_integration_note`
  ]

The chain root has the highest `load_bearing_score` of any
critical-criticality row in the LHCM family. Its three direct deps
split as:

- **two retained-bounded graph-first authorities** —
  `graph_first_selector_derivation_note` and
  `graph_first_su3_integration_note`, both `audited_clean` with
  `effective_status = retained_bounded` per the live ledger;
- **one critical-criticality unaudited bounded narrow theorem** —
  `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`.

The narrow ratio theorem itself has four upstream deps
(`staggered_dirac_realization_gate_note_2026-05-03`,
`graph_first_su3_integration_note`,
`graph_first_selector_derivation_note`,
`minimal_axioms_2026-05-03`) — the staggered-Dirac realization gate
appears as an `admitted_context_input`, not a load-bearing premise of
the ratio algebra (see the recently-shipped
[`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md)
for the explicit demonstration that the ratio's load-bearing chain
does not consume staggered-Dirac realization machinery).

## 2. The five-row parent core upstream

The parent's transitive upstream closure on the live ledger is exactly
five rows. All five are recorded in
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json):

| claim_id | claim_type | audit_status | effective_status | criticality |
|---|---|---|---|---|
| `graph_first_selector_derivation_note` | `bounded_theorem` | `audited_clean` | `retained_bounded` | `critical` |
| `graph_first_su3_integration_note` | `bounded_theorem` | `audited_clean` | `retained_bounded` | `critical` |
| `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | `bounded_theorem` | `unaudited` | `unaudited` | `critical` |
| `minimal_axioms_2026-05-03` | `meta` | `unaudited` | `meta` | `critical` |
| `staggered_dirac_realization_gate_note_2026-05-03` | `open_gate` | `audited_clean` | `open_gate` | `critical` |

Two of the five are retained-bounded; one is `audited_clean` open-gate
(realization gate); one is `meta`; one is the `unaudited` narrow
ratio theorem.

The structural shape: the parent core upstream is **dominated by a
single unaudited critical row** — the LH-doublet narrow ratio theorem.
Audit-ratifying that one row would clean the parent's core upstream up
to the named open gate (which is audit-clean and an explicit
admitted-context input under the
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) framing,
not a load-bearing premise).

## 3. The 132-row family upstream closure

The four additional LHCM-family rows
(`lhcm_matter_assignment_from_su3_representation_note_2026-05-02`,
`lhcm_y_normalization_from_anomaly_and_convention_note_2026-05-02`,
`lhcm_repair_atlas_consolidation_note_2026-05-02`,
`higgs_y_from_lhcm_and_yukawa_structure_note_2026-05-02`) cite the
broader hypercharge / anomaly cancellation surface as well. Their
union of transitive upstream closures (the family upstream closure)
is 132 rows. Distribution of `audit_status` across that 132-row
closure as recorded in the live ledger:

| audit_status | count |
|---|---|
| `unaudited` | 93 |
| `audited_clean` | 27 |
| `audited_conditional` | 12 |

By `claim_type`:

| claim_type | count |
|---|---|
| `positive_theorem` | 60 |
| `bounded_theorem` | 49 |
| `no_go` | 16 |
| `open_gate` | 4 |
| `meta` | 3 |

By `effective_status`:

| effective_status | count |
|---|---|
| `unaudited` | 90 |
| `retained_bounded` | 13 |
| `audited_conditional` | 12 |
| `retained_no_go` | 10 |
| `retained` | 3 |
| `meta` | 3 |
| `open_gate` | 1 |

Of the 132 rows, **27 are `audited_clean`** and **27 carry retained-grade
`effective_status`** (`retained` 3 + `retained_bounded` 13 +
`retained_no_go` 10 + `open_gate` 1 = 27, matching the audited-clean
count modulo the meta row). The remaining 105 rows are frontier rows
in the §0 sense.

## 4. Frontier rows by structural class

The 105 frontier rows split into structurally distinct groups by the
shape of their position in the LHCM family upstream:

### 4.1 The LHCM family itself (5 rows)

All five LHCM-family rows are themselves `unaudited`:

- `left_handed_charge_matching_note` — chain root, parent
- `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` —
  Sym²/Anti² ↔ Q_L/L_L matter-assignment row (cycle 2 of the audit-
  backlog campaign)
- `lhcm_y_normalization_from_anomaly_and_convention_note_2026-05-02` —
  α = +1 from Q_e = -1 convention (cycle 3)
- `lhcm_repair_atlas_consolidation_note_2026-05-02` — six-item
  consolidation atlas
- `higgs_y_from_lhcm_and_yukawa_structure_note_2026-05-02` — Y_H = +1
  from all four Yukawa couplings

Sister anomaly / hypercharge rows that LHCM family directly cites:
- `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`
  (the narrow ratio packet)
- `lh_doublet_su2_squared_hypercharge_anomaly_cancellation_note_2026-05-01`
  (PR #253 — SU(2)²×Y for LH doublets)
- `rh_sector_anomaly_cancellation_identities_note_2026-05-02` (cycle 1
  — R-A,B,C identities)
- `lh_anomaly_trace_catalog_theorem_note_2026-04-25` (full trace
  catalog)
- `hypercharge_identification_note` (audited_renaming sister)
- `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24`
  (RH hypercharge uniqueness)
- `su2_witten_z2_anomaly_theorem_note_2026-04-24`
- `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24`
- `one_generation_matter_closure_note`
- `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02`
- `three_generation_structure_note`
- `hopping_bilinear_hermiticity_theorem_note_2026-05-02`

These rows are the closest extension of the LHCM family — they pull
in via the Y-normalization, atlas, and Higgs-Y rows. None of them
carry retained-grade `effective_status` yet.

### 4.2 Graph-first / single-axiom upstream (retained, not frontier)

The retained-bounded graph-first authorities and the few rows that
already cleared:
- `graph_first_su3_integration_note` (retained_bounded)
- `graph_first_selector_derivation_note` (retained_bounded)
- `i3_zero_exact_theorem_note` (retained)
- `site_phase_cube_shift_intertwiner_note` (retained)
- `z2_hw1_mass_matrix_parametrization_note` (retained)
- `staggered_dirac_realization_gate_note_2026-05-03` (open_gate)
- `physical_lattice_necessity_note` (retained_no_go)
- a few axiom-first retained-bounded rows
  (`action_normalization_note`, `oh_schur_boundary_action_note`,
  `restricted_strong_field_closure_note`, `boundary_law_robustness_note_2026-04-11`,
  `holographic_probe_note_2026-04-11`,
  `cluster_decomposition_mass_gap_bridge_theorem_note_2026-05-09`,
  `gravity_full_self_consistency_note`,
  `self_consistency_forces_poisson_note`,
  `native_gauge_closure_note`,
  `quark_route2_exact_time_coupling_note_2026-04-19`,
  `universal_gr_polarization_frame_bundle_blocker_note`,
  `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` (retained_no_go),
  etc.)

These 27 rows carry retained-grade `effective_status` and are NOT
frontier rows. They are the parts of the LHCM family upstream that
already cleared the audit lane.

### 4.3 Universal-GR / Planck / area-law / single-clock chains (~80 rows)

The bulk of the 105-row frontier is composed of universal-GR,
Planck-scale, area-law, axiom-first, Lorentz/microcausality,
S3-spacetime, and related single-clock chains that the LHCM family's
matter-assignment, atlas, and Higgs-Y rows cite indirectly via
`hypercharge_identification_note`,
`one_generation_matter_closure_note`,
`hopping_bilinear_hermiticity_theorem_note_2026-05-02`, and the
broader axiom-first cluster.

These chains do not block LHCM at the algebra layer (the parent core
upstream is only 5 rows). They appear in the family upstream closure
because the consolidation atlas and Higgs-Y rows carry the broader
hypercharge / anomaly references. Their audit status is mostly
`unaudited` with a sub-cluster of `audited_conditional` rows
(notably `axiom_first_cluster_decomposition_theorem_note_2026-04-29`,
`axiom_first_lattice_noether_theorem_note_2026-04-29`,
`observable_principle_from_axiom_note`,
`physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30`,
`source_driven_field_recovery_sweep_note`,
`s3_boundary_link_theorem_note`, `s3_cap_uniqueness_note`,
`staggered_fermion_card_2026-04-11`,
`universal_gr_isotropic_glue_operator_note`,
`universal_gr_lorentzian_global_atlas_closure_note`,
`universal_gr_tensor_action_blocker_note`,
`quark_route2_source_domain_bridge_no_go_note_2026-04-28`).

These are downstream of broader Cl(3) / Z³ axiom-first work; their
repair-class breakdown matches the universal-GR / Planck campaign's
own scope, not LHCM-specific work. They are listed here for
completeness so the chain map captures the full closure, but
LHCM-specific repair work does not need to clear them — closing the
parent core's narrow ratio row plus the matter-assignment and
Y-normalization rows is sufficient for the LHCM ledger position.

## 5. Repair-class distribution

The audit lane records repair classes for `audited_conditional`
verdicts in
[`docs/audit/data/repair_class_backfill_log.json`](audit/data/repair_class_backfill_log.json).
Distribution across the live log (216 entries):

| repair_class | count |
|---|---|
| `runner_artifact_issue` | 119 |
| `other` | 43 |
| `dependency_not_retained` | 18 |
| `scope_too_broad` | 16 |
| `missing_dependency_edge` | 11 |
| `missing_bridge_theorem` | 7 |
| `compute_required` | 2 |

The LHCM-family rows themselves are `unaudited` and carry no recorded
repair class. The audit-conditional rows in the family upstream
closure (the 12 in §3) are part of the broader axiom-first and
universal-GR campaigns and are not LHCM-specific repair targets.

## 6. Existing closure work referenced

The LHCM repair chain has substantial existing closure work that
forms the structural baseline for any retained-promotion campaign on
the chain root:

- [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md):
  six-item LHCM repair atlas consolidating cycles 1-3 + PR #253 +
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS, with the unique remaining
  residual identified as governance reclassification of two
  SM-definition conventions (`Q_e = -1` and quark/lepton naming).
- [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md):
  exact-support theorem for repair item (1) (Sym²/Anti² ↔ Q_L/L_L).
- [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md):
  exact-support theorem for repair item (2) (α = +1 from Q_e = -1).
- [`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md):
  bounded proof-walk demonstrating the LH-doublet 1:(-3) ratio's
  load-bearing chain does not consume staggered-Dirac realization
  machinery.
- [`HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md`](HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md):
  hypercharge identification proof-walk under the lattice-independence
  bounded scope.
- [`ANOMALY_CANCELLATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md`](ANOMALY_CANCELLATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md):
  anomaly cancellation (E1)-(E4) proof-walks demonstrating their
  load-bearing chains do not consume lattice-action machinery.
- [`SU5_DECOMPOSITION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md`](SU5_DECOMPOSITION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md):
  SU(5) decomposition proof-walk.
- [`SIN2THETAW_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md`](SIN2THETAW_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08.md):
  sin²θ_W^GUT = 3/8 proof-walk.

Of the LHCM-family closure work, only the consolidation atlas (PR #262)
and the four cycles 1-3 + 15-19 narrow exact-support theorems are
shipped on `main`; the consolidation atlas explicitly disclaims
retained promotion (`proposal_allowed: false` per its CLAIM_STATUS_CERTIFICATE).

## 7. The structurally cheapest LHCM frontier target

Per §1-2, the parent core upstream has exactly one `unaudited`
critical row in its load-bearing chain:
`lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`.

Audit-ratifying that one row to `audited_clean` would clean the
parent's core upstream up to the named open realization gate (which
is audit-clean and an explicit admitted-context input, not a
load-bearing premise of the ratio algebra; see
[`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md)
for the explicit demonstration). After that, the parent's
`effective_status` becomes the chain-bounded retention target the
consolidation atlas already maps; the remaining work is governance
classification of the two SM-definition conventions
(`Q_e = -1` and quark/lepton naming) per
[`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md).

This synthesis identifies the narrow ratio row as the single
structurally cheapest frontier target on the LHCM chain. It does
NOT propose audit-status changes for that row — the audit lane
remains the sole authority. It only records the structural
observation so future automated campaigns target the correct row.

## Status

```yaml
claim_type: meta
proposal_allowed: false
proposal_allowed_reason: |
  This note is a backward-looking synthesis citing already-applied
  audit verdicts and live-ledger structural data. It does not propose
  any new derivation, theorem, or admission. It only records the
  transitive upstream closure shape of the LHCM family and the
  audit-status / repair-class distribution across that closure. The
  audit lane remains the sole authority for changing any row's
  audit_status or effective_status.
authority_chain:
  - left_handed_charge_matching_note (chain root, unaudited, td=715
    after this PR, was 713 prior)
  - lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02
    (single unaudited critical row in parent core upstream)
  - graph_first_su3_integration_note + graph_first_selector_derivation_note
    (retained-bounded graph-first authorities)
  - staggered_dirac_realization_gate_note_2026-05-03
    (audit-clean open gate; admitted-context input per
     MINIMAL_AXIOMS_2026-05-03)
```

## What this note does NOT do

1. Promote any LHCM-family row to retained.
2. Demote any row from its recorded audit verdict.
3. Reclassify any LHCM-family row, dep, or downstream descendant.
4. Propose a new theorem, derivation, or repair mechanism.
5. Rename, retag, or introduce new vocabulary for any row.
6. Modify any retained content.
7. Open or close any audit row.
8. Set or predict any audit verdict.
9. Make any claim about the staggered-Dirac realization gate's
   closure status — the gate's audit verdict (`audited_clean` /
   `effective_status: open_gate`) is recorded by the audit lane and
   not modified by this synthesis.

## Recommendation for future campaigns

Concrete operational recommendation for automated audit-backlog
campaigns and retained-promotion campaigns that target LHCM:

1. **The structurally cheapest single frontier target on the LHCM
   chain root's core upstream is the LH-doublet narrow ratio row**
   (`lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`).
   It is the only `unaudited` critical row in the parent's five-row
   core upstream, and a recently-shipped proof-walk
   ([`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md))
   already demonstrates its load-bearing chain does not consume
   staggered-Dirac realization machinery.
2. **Do NOT** spawn campaign cycles that attempt to close the
   broader 105-row frontier (universal-GR, Planck, area-law, S3-spacetime,
   axiom-first chains) as part of LHCM-specific work. Those rows
   appear in the family upstream closure via the consolidation atlas
   and Higgs-Y rows' broader hypercharge references, not as
   load-bearing inputs of the LHCM ratio algebra. Their repair work
   belongs to their own campaigns, not to LHCM.
3. **Do NOT** propose to demote the staggered-Dirac realization gate
   from its `audited_clean / open_gate` recorded status. Its
   admitted-context-input role per MINIMAL_AXIOMS_2026-05-03 is the
   correct repo-canonical handling of a critical open gate; the LHCM
   ratio's load-bearing chain bypasses it as already demonstrated by
   the recent proof-walk note.
4. **Do NOT** introduce new vocabulary, new tags, new claim_types, or
   new framings on the LHCM family. The audit lane's existing
   language for repair classes (`runner_artifact_issue`,
   `dependency_not_retained`, `missing_dependency_edge`,
   `missing_bridge_theorem`, `scope_too_broad`, `compute_required`,
   `other`) plus the existing ratio-and-multiplicities authority chain
   is sufficient.
5. The remaining substantive Nature-grade target (governance
   classification of the two SM-definition conventions per
   [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md))
   is an audit-ledger governance decision, not a derivation task; it
   does not reduce to a small bounded source note and is outside
   campaign-style 1-identity-at-a-time work.

## Cross-references

- Audit-lane policy: [`docs/audit/README.md`](audit/README.md)
  (claim_type / audit_status / effective_status separation; repair
  classes; retained-grade dependency closure)
- Sibling dep-chain audit:
  [`THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md)
- Sibling terminal-block syntheses:
  [`QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md),
  [`DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md),
  [`CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md),
  [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Sibling synthesis-template authority:
  [`AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)
- Parent source note:
  [`docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
- Companion narrow theorem note (this PR):
  [`docs/LHCM_MATTER_ASSIGNMENT_BLOCK_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LHCM_MATTER_ASSIGNMENT_BLOCK_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md)
- Live ledger row data:
  [`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json)
- Citation graph data:
  [`docs/audit/data/citation_graph.json`](audit/data/citation_graph.json)
- Repair class backfill log:
  [`docs/audit/data/repair_class_backfill_log.json`](audit/data/repair_class_backfill_log.json)

## Validation

```bash
PYTHONPATH=scripts python3 scripts/frontier_lhcm_chain_audit_map_synthesis.py
```

Runner verifies (against the live audit ledger):

1. The parent `left_handed_charge_matching_note` exists with
   recorded `claim_type = bounded_theorem`,
   `audit_status = unaudited`, `criticality = critical`,
   `transitive_descendants = 713`, `direct_in_degree = 36`, and the
   three-row `deps` array listed in §1.
2. The five-row parent core upstream closure matches the table in
   §2 and contains exactly the listed rows with the recorded
   audit-status fields.
3. The four LHCM-family sibling rows
   (`lhcm_matter_assignment_from_su3_representation_note_2026-05-02`,
   `lhcm_y_normalization_from_anomaly_and_convention_note_2026-05-02`,
   `lhcm_repair_atlas_consolidation_note_2026-05-02`,
   `higgs_y_from_lhcm_and_yukawa_structure_note_2026-05-02`) exist
   on the live ledger.
4. The narrow ratio row
   `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`
   exists as the single `unaudited` critical row in the parent's
   core upstream.
5. The realization gate
   `staggered_dirac_realization_gate_note_2026-05-03` carries
   `audit_status = audited_clean` and
   `effective_status = open_gate`.
6. The two retained-bounded graph-first authorities carry
   `effective_status = retained_bounded`.
7. This note is `claim_type = meta` and does not declare pipeline
   status for any LHCM-family row.

If any of the recorded audit-ledger fields above changes, this
synthesis becomes stale and the runner FAILs — that signals a
re-evaluation is in order.

## Review-loop rule

Going forward:

1. The LHCM family chain map recorded here is the **structurally
   cheapest single frontier target** for downstream retained-promotion
   campaigns: the LH-doublet narrow ratio row. Closing that row's
   audit verdict (the audit lane's prerogative, not this synthesis's)
   is the cheapest unblocking action on the parent core upstream.
2. The 105-row frontier in the family upstream closure is mostly
   downstream of unrelated axiom-first / universal-GR campaigns. New
   audit-backlog or retained-promotion cycles on those frontier rows
   should target their own campaigns, not LHCM.
3. The remaining substantive Nature-grade work for full LHCM closure
   (governance reclassification of the two SM-definition conventions
   `Q_e = -1` and quark/lepton naming) is an audit-ledger governance
   decision, not a derivation task. It is outside campaign-style
   1-identity-at-a-time work.
4. If the audit lane records new verdicts on any LHCM-family row, or
   if the live-ledger transitive descendants / in-degree / load-
   bearing-score fields change for the chain root, this synthesis
   becomes stale — the runner will FAIL and the synthesis must be
   re-rendered.
