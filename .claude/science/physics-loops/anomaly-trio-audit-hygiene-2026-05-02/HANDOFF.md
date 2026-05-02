# HANDOFF — Iter 6: Anomaly trio audit-readiness hygiene

**Branch:** `physics-loop/anomaly-trio-audit-hygiene-2026-05-02`
**Parent loop:** `3plus1d-native-closure-2026-05-02`
**Date:** 2026-05-02

## Commits

1. `[physics-loop][science][hygiene] su2_witten Z2 anomaly: narrow scope to bounded_theorem`
2. `[physics-loop][science][hygiene] su3_cubic anomaly: narrow scope to bounded_theorem`
3. `[physics-loop][science][hygiene] lh_anomaly_trace_catalog: align as bounded_theorem A-dominant`
4. `[physics-loop][science][hygiene] lh_anomaly: separate load-bearing inputs from logical siblings + run pipeline`

## Effect on the audit ledger

| row | before | after |
| --- | --- | --- |
| `su2_witten_z2_anomaly_theorem_note_2026-04-24` | claim_type=positive_theorem, audit_status=audited_conditional, runner_path=None | claim_type=bounded_theorem, audit_status=unaudited (re-audit pending), runner_path=scripts/frontier_su2_witten_z2_anomaly.py, ready=True |
| `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | claim_type=positive_theorem, audit_status=audited_conditional, runner_path=None | claim_type=bounded_theorem, audit_status=unaudited (re-audit pending), runner_path=scripts/frontier_su3_cubic_anomaly_cancellation.py, ready=True |
| `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | claim_type=positive_theorem (seed hint), audit_status=unaudited, runner B-dominant + decoration_candidate=True, deps=6 | claim_type=bounded_theorem (author hint), audit_status=unaudited, runner A-dominant, deps=4 (siblings removed) |

## What this PR does NOT do

- It does not promote any row to `audited_clean` or `retained_bounded`.
  Independent Codex audit is still required.
- It does not derive the matter-content premises (Q_L/L_L doublet
  multiplicities, RH-singlet completion, u_R^c/d_R^c anti-triplet
  completion). Those are admitted external inputs. The closing
  derivation is pursued in:
  - PR #382 — `physics-loop/su3-anomaly-forced-3bar-completion-derivation-2026-05-02`
  - PR #383 — `physics-loop/su2-witten-doublet-count-derivation-2026-05-02`
  - PR #390 — `physics-loop/sm-hypercharge-no-nu-r-derivation-2026-05-02`
  These are orthogonal to this PR and pursue the upstream route.
- It does not fix the broader `audited_renaming` -> `retained_bounded`
  promotion path for `hypercharge_identification_note` (which keeps
  `lh_anomaly_trace_catalog` at `ready=False`). That is a separate
  upstream lane.

## Proposed weaving (to be picked up by review-integration lane, not by this PR)

- None outside the audit pipeline ledger updates that flow automatically.

## Verification commands

```bash
python3 scripts/frontier_su2_witten_z2_anomaly.py
python3 scripts/frontier_su3_cubic_anomaly_cancellation.py
python3 scripts/frontier_lh_anomaly_trace_catalog.py
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py
```

Expected:
- runners: PASS=35 / 33 / 26 (FAIL=0)
- pipeline: 1697 rows, 49 warnings (legacy backfills), 0 errors

## Net impact on parent loop

`anomaly_forces_time_theorem` is already `audited_clean / retained_bounded`
on the actual surface (deps=[]); these 3 anomaly rows are not gating the
parent. However, the broader anomaly-cancellation backbone of the framework
benefits from the 3 rows clearing to `retained_bounded`. Once Codex
ratifies the bounded scopes, the anomaly system will read:

- anomaly_forces_time = retained_bounded (stable)
- su2_witten_z2_anomaly = retained_bounded (after audit)
- su3_cubic_anomaly = retained_bounded (after audit)
- lh_anomaly_trace_catalog = retained_bounded or audited_conditional
  (after audit; depends on auditor judgment of the audited_renaming
  hypercharge dep)

## Open campaign-level coordination

- Iter 5 (Lorentz boost-covariance + angular kernel) is in flight on
  `claude/lorentz-boost-cov-and-angular-kernel-elevate-2026-05-02`. No
  overlap with this iteration's files.
- PRs #382, #383, #390 (closing-derivation route for matter content)
  are in flight from a separate worker. This iteration's bounded-scope
  hygiene is COMPLEMENTARY: if those PRs land at retained-grade, the
  bounded rows here can be re-audited to upgrade scope.
