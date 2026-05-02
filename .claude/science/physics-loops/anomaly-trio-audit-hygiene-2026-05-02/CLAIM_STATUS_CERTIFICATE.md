# CLAIM STATUS CERTIFICATE — Iter 6: Anomaly trio (su2_witten / su3_cubic / lh_anomaly_trace_catalog) audit hygiene

**Iter:** 6 of 3plus1d-native-closure-2026-05-02 (parent loop pack)
**Date:** 2026-05-02
**Branch:** `physics-loop/anomaly-trio-audit-hygiene-2026-05-02`

## Per-row certificate

### Row 1 — `su2_witten_z2_anomaly_theorem_note_2026-04-24`

- `actual_current_surface_status`: bounded_theorem (parity arithmetic
  on assumed one-generation matter content)
- `target_claim_type`: bounded_theorem
- `conditional_surface_status`: NOT applicable as new-axiom or
  hypothetical surface — the matter-content premise is admitted external
  input from `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (currently
  `decoration_under_lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`,
  retained) and `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` (currently
  `audited_conditional`).
- `hypothetical_axiom_status`: null
- `admitted_observation_status`: null
- `claim_type_reason`: Standard Witten Z_2 parity arithmetic on the
  named matter table. Given the matter-content premise, the integer
  parity arithmetic
  `N_D(per gen) = N_c + 1 = 4`,
  `N_D(total) = 12`,
  `parity = 0`
  is exact. The runner verifies all parity-rule, extension, and
  Higgs-boundary corollaries (35 PASS, 0 FAIL).
- `audit_required_before_effective_retained`: true
- `bare_retained_allowed`: false
- `target_effective_status_on_clean_audit`: retained_bounded
- `audit_independence_required`: fresh_context_or_stronger
- `runner_check_breakdown`: A=8 (assert abs identity), B=0, C=0, D=0,
  total_pass=35
- `pre-existing-codex-verdict`: archived (note hash changed from the
  audited version; verdict moved to previous_audits)

### Row 2 — `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24`

- `actual_current_surface_status`: bounded_theorem (cubic-index
  arithmetic on assumed one-generation color-matter completion)
- `target_claim_type`: bounded_theorem
- `conditional_surface_status`: NOT applicable as new-axiom — the
  right-handed anti-triplet completion is admitted external input
  from `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` and
  `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`.
- `hypothetical_axiom_status`: null
- `admitted_observation_status`: null
- `claim_type_reason`: Standard SU(3) cubic-index arithmetic on the
  named matter table:
  `Q_L : 2 * A(3) = +2`, `u_R^c : A(3bar) = -1`, `d_R^c : A(3bar) = -1`,
  total `+2 - 1 - 1 = 0`. The runner verifies the index sum,
  extension scenarios, and the C-class numerical SU(3) symmetric
  tensor d_abc compute (33 PASS, 0 FAIL).
- `audit_required_before_effective_retained`: true
- `bare_retained_allowed`: false
- `target_effective_status_on_clean_audit`: retained_bounded
- `audit_independence_required`: fresh_context_or_stronger
- `runner_check_breakdown`: A=12 (assert abs identity), B=0, C=substantial
  via numpy.linalg / Lambda-matrix d-tensor compute, D=0, total_pass=33

### Row 3 — `lh_anomaly_trace_catalog_theorem_note_2026-04-25`

- `actual_current_surface_status`: bounded_theorem (exact rational/integer
  identity catalog on assumed LH content)
- `target_claim_type`: bounded_theorem (was `positive_theorem` per
  `claim_type_seed_hint` from legacy authoring; now author hint pin =
  bounded_theorem)
- `conditional_surface_status`: NOT applicable as new-axiom — LH-content
  premise is admitted from `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`
  (retained via decoration-under) and `HYPERCHARGE_IDENTIFICATION_NOTE.md`
  (audited_renaming).
- `hypothetical_axiom_status`: null
- `admitted_observation_status`: null
- `claim_type_reason`: Five exact `fractions.Fraction` identities
  (C1)-(C5) on the named LH content. Pure algebraic-identity (class A)
  arithmetic; no observation, no fitted parameter, no convention
  selector.
- `audit_required_before_effective_retained`: true
- `bare_retained_allowed`: false
- `target_effective_status_on_clean_audit`: retained_bounded
- `audit_independence_required`: fresh_context_or_stronger
- `runner_check_breakdown`: A=11 (assert abs identity), B=5 (auxiliary
  authority existence checks), C=0, D=0, total_pass=26
  Effect: classify_runner_passes now reports A-dominant
  (was B-dominant + decoration_candidate=True before).

## Open dependencies (cross-row)

- `lh_anomaly_trace_catalog_theorem_note_2026-04-25` cites the SU(2) Witten and
  SU(3) cubic siblings in cross-references but does NOT import their
  results. The sibling-link cleanup (markdown link -> plain text)
  removes the spurious dependency edges, so the catalog audit lane
  no longer needs those siblings to be cleared first.
- The catalog still depends on `hypercharge_identification_note` which
  is `audited_renaming` (rank 10 = same as audited_conditional). The
  audit lane will likely land the catalog at `audited_conditional`
  rather than `audited_clean` because the LH content's hypercharge
  normalization is admitted via a renaming. This is honest — the
  bounded scope says "given the LH content with `Y(Q_L) = 1/3`,
  `Y(L_L) = -1`, the identities (C1)-(C5) hold exactly."

## Net impact on `anomaly_forces_time_theorem`

`anomaly_forces_time_theorem` is currently `audited_clean / retained_bounded`
(deps=[]). It does not depend on these 3 anomaly rows for its retained-bounded
claim. However, the row's bounded scope cites the (LH+RH) anomaly arithmetic
as load-bearing, so the 3 anomaly rows are part of the broader anomaly-system
backbone the framework relies on for its anomaly-cancellation claims.

After this hygiene pass clears, the anomaly-system audit picture is:

- `anomaly_forces_time_theorem`: retained_bounded (stable)
- `su2_witten_z2_anomaly`: bounded_theorem, audit-ready (target retained_bounded)
- `su3_cubic_anomaly`: bounded_theorem, audit-ready (target retained_bounded)
- `lh_anomaly_trace_catalog`: bounded_theorem, audit-ready (target retained_bounded
  conditional on hypercharge_identification audited_renaming dep)

The path to retained-grade for the 3 rows is clear pending Codex audit
verdict pickup. PRs #382 and #383 (closing-derivation route) remain
the orthogonal upgrade path that, if landed, would lift
audit_status from audited_conditional/clean (bounded) to audited_clean
(positive_theorem) by replacing the admitted matter-content premise
with a derived theorem.

## Review-loop disposition

- self-review: pending after PR opens
- independent audit: pending (Codex GPT-5.5 audit lane)

## Independent audit handoff

After this PR opens, the audit lane should:
1. Re-run the citation graph build (auto in `run_pipeline.sh`).
2. Pick up the three rows from `audit_queue.json`. Both su2_witten and
   su3_cubic are now `ready=True`.
3. Apply Codex audit verdict via `apply_audit.py`.
4. Expected verdicts:
   - row 1 (`su2_witten`): `audited_clean` with `claim_type=bounded_theorem`
     -> `retained_bounded`. The audit prompt should focus on whether the
     bounded scope honestly excludes the matter-content derivation gap and
     whether the parity arithmetic is structurally correct given the named
     premise. The new Scope section explicitly draws this boundary.
   - row 2 (`su3_cubic`): same pattern -> `audited_clean` /
     `retained_bounded` on bounded scope.
   - row 3 (`lh_anomaly_trace_catalog`): `audited_clean` /
     `retained_bounded` on bounded scope, OR `audited_conditional` if
     the auditor decides the `audited_renaming` upstream of
     hypercharge_identification taints the catalog's bounded claim.
     Either landing is honest.
