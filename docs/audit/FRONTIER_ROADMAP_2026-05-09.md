# Frontier Roadmap — Non-Retained Roots Inventory

**Date:** 2026-05-09
**Status:** navigation artifact for the audit-strategy lane. Maps the
355 non-retained roots with `transitive_descendants ≥ 100`, ordered
by leverage and grouped by tractability + thematic cluster, so the
next campaign can pick the highest-yield attack target without
re-deriving the leverage map each session.
**Lane:** audit-strategy. No physics claim added or removed.

---

## 0. Purpose

The 2026-05-08 leverage refresh showed that most of the audit-graph
leverage now sits in **two large interconnected families**: the
axiom-first foundations cluster (gated by the staggered-Dirac
realization gate) and the matter-content cluster (LHCM, three-
generation, neutrino, CKM, Koide). This doc maps those families plus
the smaller sectors so the audit-strategy lane has a current
inventory.

The 2026-05-08 staggered-Dirac campaign (PRs #797, #802, plus 16
fresh-context Claude audits applied via `apply_audit.py`) delivered
the cycle break for the gate's substep 1 chain:

- `axiom_first_cl3_per_site_uniqueness` → `retained` (cross-confirmed + judicial)
- `axiom_first_spin_statistics` → `retained`

The remaining gate cascade (substeps 1–4 + parent retag) is
mechanical — see `STAGGERED_DIRAC_GATE_UNTYING_PLAN_2026-05-08.md`.
This roadmap addresses **everything else**.

## 1. Inventory snapshot (2026-05-09)

`docs/audit/data/audit_ledger.json` snapshot:

| effective_status | count |
|---|---:|
| `unaudited` | 863 |
| `audited_conditional` | 414 |
| `retained_bounded` | 237 |
| `retained_no_go` | 122 |
| `retained` | 69 |
| `meta` | 49 |
| `audited_renaming` | 25 |
| `audited_numerical_match` | 20 |
| `open_gate` | 11 |
| `audited_failed` | 8 |
| `retained_pending_chain` | 2 |

**355 non-retained-grade rows have `transitive_descendants ≥ 100`** —
those are the rows whose retention would meaningfully cascade.

By audit_status:

| audit_status | count |
|---|---:|
| `unaudited` | 239 |
| `audited_conditional` | 94 |
| `audited_renaming` | 14 |
| `audited_numerical_match` | 6 |
| `audited_clean` | 1 (open_gate) |
| `audited_failed` | 1 |

Among the conditional rows, the auditor-stamped repair-class
distribution is:

| repair class | count |
|---|---:|
| `dependency_not_retained` | 30 |
| `missing_bridge_theorem` | 27 |
| `missing_dependency_edge` | 26 |
| `other` | 8 |
| (empty) | 2 |
| `runner_artifact_issue` | 1 |

## 2. Top-20 single-row leverage points

Ranked by **direct in-degree** (number of non-retained rows that cite
this row as a one-hop dep). Direct in-degree captures "if this one
row retains, how many descendants get a chance to retain in the next
audit pass." This is the cheapest cascade-trigger metric.

| rank | in-deg | td | crit | audit_status | claim_id | tractability |
|---:|---:|---:|---|---|---|---|
| 1 | 46 | 399 | critical | conditional | `observable_principle_from_axiom_note` | research-grade (`missing_bridge_theorem`) |
| 2 | 36 | 541 | critical | clean (open_gate) | `staggered_dirac_realization_gate_note_2026-05-03` | mechanical retag once substeps 1-4 land (campaign in flight) |
| 3 | 35 | 357 | critical | conditional | `alpha_s_derived_note` | research-grade (waits on `plaquette_self_consistency`) |
| 4 | 34 | 89 | critical | unaudited | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | **moderate (just audit it)** |
| 5 | 32 | 89 | critical | unaudited | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | **moderate (just audit it)** |
| 6 | 31 | 145 | critical | unaudited | `yt_ward_identity_derivation_theorem` | **moderate (just audit it)** |
| 7 | 27 | 231 | critical | unaudited | `three_generation_observable_theorem_note` | **moderate (just audit it)** |
| 8 | 26 | 514 | critical | unaudited | `anomaly_forces_time_theorem` | research-grade (citation cycle, see §5) |
| 9 | 26 | 70 | critical | unaudited | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | **moderate (just audit it)** |
| 10 | 26 | 200 | critical | conditional | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | research-grade |
| 11 | 25 | 423 | critical | unaudited | `left_handed_charge_matching_note` | research-grade (self-conditional, see §4.2) |
| 12 | 24 | 356 | critical | unaudited | `one_generation_matter_closure_note` | **moderate (just audit it)** |
| 13 | 23 | 370 | critical | unaudited | `three_generation_structure_note` | **moderate (just audit it)** |
| 14 | 22 | 396 | critical | conditional | `plaquette_self_consistency_note` | research-grade (`missing_bridge_theorem`) |
| 15 | 22 | 202 | critical | conditional | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | research-grade |
| 16 | 21 | 213 | critical | unaudited | `ckm_atlas_axiom_closure_note` | **moderate (just audit it)** |
| 17 | 21 | 190 | critical | conditional | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | research-grade |
| 18 | 20 | 149 | critical | unaudited | `universal_gr_discrete_global_closure_note` | **moderate (just audit it)** |
| 19 | 18 | 123 | critical | unaudited | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | **moderate (just audit it)** |
| 20 | 17 | 84 | critical | unaudited | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | **moderate (just audit it)** |

**Key observation:** 13 of the top-20 leverage points are *unaudited
critical rows* — they may simply land `audited_clean` on a
fresh-context audit pass without any new physics. Those are the
cheapest wins on the frontier and dominate the next campaign's
attention budget.

## 3. Tractability cohorts

### 3.1 Cohort A — fresh-context audit only (highest ROI)

13 of the top-20 leverage rows are `unaudited` critical with
runners. Each is a candidate for a single fresh-context audit pass
followed by cross-confirmation (critical-row policy). Per the
2026-05-08 staggered-Dirac campaign experience, ~70% of these will
land `audited_conditional` on first audit because of upstream
dependency state, but those that have only retained-grade upstream
deps will land `audited_clean` directly.

Candidates ordered by descending in-degree (and by td as tiebreaker):

```
ckm_cp_phase_structural_identity_theorem_note_2026-04-24    in-deg=34  td=89
wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24  in-deg=32  td=89
yt_ward_identity_derivation_theorem                          in-deg=31  td=145
three_generation_observable_theorem_note                     in-deg=27  td=231
anomaly_forces_time_theorem                                  in-deg=26  td=514  (SEE §5 cycle)
ckm_magnitudes_structural_counts_theorem_note_2026-04-25     in-deg=26  td=70
left_handed_charge_matching_note                             in-deg=25  td=423  (SEE §4.2)
one_generation_matter_closure_note                           in-deg=24  td=356
three_generation_structure_note                              in-deg=23  td=370
ckm_atlas_axiom_closure_note                                 in-deg=21  td=213
universal_gr_discrete_global_closure_note                    in-deg=20  td=149
standard_model_hypercharge_uniqueness_theorem_note_2026-04-24 in-deg=18  td=123
ckm_atlas_triangle_right_angle_theorem_note_2026-04-24       in-deg=17  td=84
```

**Recommended sequence** (audit in this order; each first-audit pass
takes ~60–90 sec of agent time):

1. `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` first; it's depended on by many CKM rows and has small td so its conditional-vs-clean determination is fast.
2. `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` second.
3. `ckm_magnitudes_structural_counts_theorem_note_2026-04-25`, `ckm_atlas_axiom_closure_note`, `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` form a CKM cluster — audit together.
4. `three_generation_observable_theorem_note`, `three_generation_structure_note`, `one_generation_matter_closure_note` form a matter-content cluster.
5. `universal_gr_discrete_global_closure_note`, `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` are independent.
6. `yt_ward_identity_derivation_theorem`: gauge-sector independent.
7. `left_handed_charge_matching_note` and `anomaly_forces_time_theorem` last; they have known citation cycles (§5).

### 3.2 Cohort B — research-grade, gated by named obstructions

7 of the top-20 leverage rows are `audited_conditional` or
`audited_renaming` with auditor-stamped science-grade gaps:

| claim_id | repair_class | named obstruction |
|---|---|---|
| `observable_principle_from_axiom_note` | `missing_bridge_theorem` | derive scalar additivity, CPT-even phase blindness, continuity/regularity, normalization selection from retained primitives |
| `alpha_s_derived_note` | `dependency_not_retained` | waits on `plaquette_self_consistency` retain (§3.2 row 3) and the low-energy running bridge |
| `plaquette_self_consistency_note` | `missing_bridge_theorem` | runner hard-codes `PLAQ_REFERENCE = 0.5934`; needs first-principles compute or explicit retention as imported MC constant |
| `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | conditional | dm-neutrino cluster |
| `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | conditional | dm-neutrino cluster |
| `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | conditional | dm-neutrino cluster |
| `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | `scope_too_broad` | imports Hastings-Koma as literature black-box; needs derivation or scope narrow to L1/L3/L4 |

These rows need **substantive new physics work** — typically a
science-loop campaign per row. The science-fix loop
(`scripts/science_fix_loop.py`) is the autonomous chip-tool for
these; see `MISSING_DERIVATION_PROMPTS.md` cohorts.

### 3.3 Cohort C — audited_renaming / audited_numerical_match cohort

20 rows in the top-355 carry these terminal verdicts. Repair = either
write the missing derivation OR demote to bounded/decoration. See
`MISSING_DERIVATION_PROMPTS.md` `audited_renaming` (34 total) and
`audited_numerical_match` (22 total) sections — those are already
queued for `science_fix_loop.py`.

## 4. Thematic clusters

### 4.1 Axiom-first foundations cluster (gate campaign in flight)

State as of 2026-05-08:

```
axiom_first_cl3_per_site_uniqueness            retained (this session)
axiom_first_spin_statistics                     retained (this session)
staggered_dirac_realization_gate_note_2026-05-03  audited_clean / open_gate (parent)
  substep 1 (Grassmann forcing)                 audited_conditional → re-audit ready
  substep 2 (Kawamoto-Smit)                     unaudited → audit when substep 1 retains
  substep 3 (BZ-corner)                         unaudited → audit when substep 2 retains
  substep 4 (Physical species)                  unaudited → audit when substep 3 retains
  Phase 5: parent gate retag open_gate → positive_theorem
```

Estimated unblock count when gate retags: **~660 transitive
descendants** (per substeps 1–4 audit verdicts and the parent
gate's recompute).

The remaining steps are documented in
`STAGGERED_DIRAC_GATE_UNTYING_PLAN_2026-05-08.md`.

### 4.2 Matter-content cluster (LHCM + three-generation + Koide)

Top blockers in this cluster:

| claim_id | td | state |
|---|---:|---|
| `left_handed_charge_matching_note` (LHCM) | 423 | unaudited; **self-conditional** on Q = T_3 + Y/2 admission |
| `three_generation_observable_theorem_note` | 231 | unaudited; depends on staggered-Dirac gate |
| `three_generation_structure_note` | 370 | unaudited; depends on gate |
| `one_generation_matter_closure_note` | 356 | unaudited |
| `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | 123 | unaudited |
| `koide_brannen_phase_reduction_theorem_note_2026-04-20` | 107 | (cluster member) |

The 2026-05-02 audit-backlog campaign (cycles 1–19) already produced
exact-support derivations for LHCM items (1)–(3) on the graph-first
SU(3) surface. The Q = T_3 + Y/2 admission was identified as the
governance gate. After the staggered-Dirac gate retag (above), the
matter-content cluster has substantial flow potential.

**Recommended attack:** dispatch fresh-context audits on the 6
LHCM + three-generation + hypercharge unaudited rows in parallel
once the staggered-Dirac substep 1 lands clean. Most should land
audited_conditional pending substep 1 chain; once substep 1 retains,
run a re-audit pass over the cluster.

### 4.3 CKM atlas cluster

7 unaudited critical rows in the top-20 leverage list:

```
ckm_cp_phase_structural_identity_theorem_note_2026-04-24       td=89
wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24  td=89
ckm_magnitudes_structural_counts_theorem_note_2026-04-25       td=70
ckm_atlas_axiom_closure_note                                   td=213
ckm_atlas_triangle_right_angle_theorem_note_2026-04-24         td=84
ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25  (top-50)
```

These are tightly coupled and likely all audit together as a single
batch. Citation cycle 16 (`ckm_cp_phase_structural_identity` ↔
others) needs a cycle-break before retain propagation. See §5.

### 4.4 Dark-matter neutrino cluster

`dm_neutrino_*`: 65 rows with td≥100; mostly conditional on the
neutrino_majorana family + the staggered-Dirac gate. The neutrino_
majorana family (28 rows) is a **second leverage root** (per the
2026-05-01 leverage map: 733 transitive descendants). Closing
`neutrino_majorana_operator_axiom_first_note` would cascade through
the dm_neutrino + dm_leptogenesis + Majorana-Pfaffian families.

### 4.5 Universal QG / GR cluster

29 rows (universal_qg + universal_gr). `universal_gr_discrete_global_closure_note`
(td=149, in-deg=20) is the single biggest entry; it's unaudited.
`universal_gr_a1_invariant_section_note` is a citation-cycle break
target (cycle-0006).

### 4.6 Hadron / gauge-vacuum / yt clusters

`yt_p1` (12 rows), `yt_p2`, `gauge_vacuum` (13 rows), `yt_ward_identity_derivation_theorem`
(td=145, in-deg=31). Mostly unaudited; should batch audit.

## 5. Citation cycles (35 total)

`docs/audit/data/cycle_inventory.json` records 35 graph cycles. Each
cycle blocks every member from `retained` until one node is
re-audited with explicit cycle-break instructions or one cited edge
is stripped. Top 5 by max descendant td:

| cycle_id | length | max_desc | primary break target |
|---|---:|---:|---|
| `cycle-0001` | 2 | 501 | `angular_kernel_underdetermination_no_go_note` |
| `cycle-0002` | 7 | 501 | `anomaly_forces_time_theorem` |
| `cycle-0003` | 2 | 250 | `hypercharge_identification_note` |
| `cycle-0004` | 4 | 149 | `universal_gr_constraint_action_stationarity_note` |
| `cycle-0006` | 6 | 149 | `universal_gr_a1_invariant_section_note` |

Cycle-break is the cheap-but-not-free cascade unblocker: pick one
member, narrow its scope to drop the cycle-creating cite (the same
pattern as `cl3_per_site_uniqueness` ↔ substep 1 in this session),
and the whole cycle becomes orderable.

## 6. Recommended next-campaign attack order

Priority is descending leverage × ascending tractability:

### Phase A — Top-of-leverage Cohort A audit batch (8–12 hours of audit-agent time)

```
# Single fresh-context audit (then cross-confirm if critical):
wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24
ckm_cp_phase_structural_identity_theorem_note_2026-04-24
ckm_magnitudes_structural_counts_theorem_note_2026-04-25
ckm_atlas_axiom_closure_note
ckm_atlas_triangle_right_angle_theorem_note_2026-04-24
three_generation_observable_theorem_note
three_generation_structure_note
one_generation_matter_closure_note
universal_gr_discrete_global_closure_note
standard_model_hypercharge_uniqueness_theorem_note_2026-04-24
yt_ward_identity_derivation_theorem
```

Expect ~30–40% to land `audited_clean` directly (those whose only
deps are A1/A2 axioms, simple chirality content, or already-retained
primitives). The other ~60% will land `audited_conditional` with
auditor-stamped repair targets that feed Cohort B.

### Phase B — Resume staggered-Dirac gate cascade (mechanical)

Per `STAGGERED_DIRAC_GATE_UNTYING_PLAN_2026-05-08.md`:
- Re-audit `cl3_per_site_hilbert_dim_two` (just narrowed; should clean)
- Re-audit substep 1 once dim_two retains
- Audit substeps 2/3/4 in chain
- Retag parent gate

### Phase C — Tackle the remaining cycle-break targets

Pick `anomaly_forces_time_theorem` (cycle-0002, 501 descendants),
`hypercharge_identification_note` (cycle-0003, 250 desc), and
`universal_gr_constraint_action_stationarity_note` (cycles -0004,
-0005, -0007, 149 desc). For each, scope-narrow per the §5 break-
target column.

### Phase D — Research-grade Cohort B (multi-session campaigns)

Each row needs a science-loop pass:

- `observable_principle_from_axiom_note` — derive missing bridges (additivity, phase blindness, regularity)
- `plaquette_self_consistency_note` — first-principles `β = 6` derivation OR scope-restrict to imported MC constant
- `axiom_first_cluster_decomposition_theorem_note_2026-04-29` — Hastings-Koma assumption verification
- `neutrino_majorana_operator_axiom_first_note` — open the second leverage root (733 td)
- `g_bare` family — six notes; prior leverage map ranked it #1 with 1010 td

These should be queued for `scripts/science_fix_loop.py` per cohort
(`conditional_missing_bridge_theorem` already covers most).

### Phase E — `audited_renaming` / `audited_numerical_match` backlog

Already queued in `MISSING_DERIVATION_PROMPTS.md`. Run
`scripts/science_fix_loop.py --n 10 --category renaming` and
`--category numerical_match` to chip at it autonomously.

## 7. Estimated cascade impact

If Phase A clears (~12 of 13 candidates land), and the staggered-
Dirac gate retags via Phase B, conservative estimate:

- Direct retentions: 12 (Phase A) + 4 substeps + 1 gate parent = ~17 rows
- Cascade retentions: 660 (gate descendants) + 1500–2000 (Cohort A
  descendants, weighted by td) — but heavily overlapping
- Net unique: ~2000 rows become re-audit-eligible

Followed by a Phase D campaign on `observable_principle_from_axiom`
(in-deg 46) and `neutrino_majorana_operator_axiom_first_note` (the
733-descendant root from the prior leverage map), the audit ledger's
`unaudited` count would drop substantially below 500 (currently 863).

## 8. Maintenance

Regenerate this roadmap whenever the audit ledger advances
materially:

```bash
# Refresh the leverage data
python3 << 'PY'
import json
ledger = json.loads(open('docs/audit/data/audit_ledger.json').read())
# (use the inventory script in this doc's history; output to
#  /tmp/frontier_candidates.json)
PY
```

Treat this doc as a living artifact; the specific row counts and
in-degrees are point-in-time. The structural taxonomy (Cohorts A/B/C,
the 5 thematic clusters, the cycle-break targets) is more durable.

## 9. Cross-references

- `docs/audit/STAGGERED_DIRAC_GATE_UNTYING_PLAN_2026-05-08.md`
- `docs/AUDIT_LHF_LEVERAGE_MAP_FOR_RETAINED_PROMOTION_NOTE_2026-05-01.md` (prior leverage map)
- `docs/audit/MISSING_DERIVATION_PROMPTS.md` (per-cohort prompt queues)
- `docs/audit/data/audit_ledger.json` (source of truth)
- `docs/audit/data/cycle_inventory.json` (35 cycles)
- `docs/audit/data/audit_queue.json` (pending audit queue)
- `docs/audit/AUDIT_LEDGER.md` (rendered ledger)
