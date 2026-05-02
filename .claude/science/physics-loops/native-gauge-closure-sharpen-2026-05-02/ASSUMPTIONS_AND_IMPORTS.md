# Assumption / Import Ledger

## Inputs read

### Repo-internal authority surfaces (load-bearing)

- `docs/NATIVE_GAUGE_CLOSURE_NOTE.md` (target row, `retained_bounded`)
- `docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md` (dep, `retained_bounded`,
  cross-confirmed 2026-05-02)
- `docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` (dep, `retained_bounded`,
  cross-confirmed 2026-05-02)
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` (downstream consumer, current main)
- `docs/AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02.md`
  (PR #392 branch, the WZ theorem that uses NATIVE_GAUGE_CLOSURE at W4)
- `scripts/frontier_non_abelian_gauge.py` (primary runner, PASS=50 FAIL=0)
- `docs/audit/data/audit_ledger.json` (current state)
- `docs/audit/scripts/compute_effective_status.py` (claim_type → effective_status mapping)
- `docs/audit/scripts/audit_lint.py` (hash drift policy)
- `docs/audit/worker_lanes/02_native_gauge_runners.md` (legacy lane file
  describing the audit history)

### No external literature imports

This iteration is documentation-tightening. No new derivations.

## Forbidden imports

- bare `retained` / `promoted` wording in branch-local source notes
- claim_type promotion that would require upstream U(1)_Y
  anomaly-completion that does not exist on the current bank
- merging or modifying upstream deps (graph_first_*) — out of scope per
  campaign awareness rule (touch only NATIVE_GAUGE_CLOSURE and rows
  actually blocking it)

## What this iteration retires

Nothing. This iteration documents that NATIVE_GAUGE_CLOSURE's bounded
scope is INTRINSIC (the abelian factor identification is genuinely a
separate audit lane), not inherited overcaution.

## What this iteration exposes

- The next-blocker for sharpening NATIVE_GAUGE_CLOSURE from
  `retained_bounded` to `retained` is **anomaly-complete U(1)_Y
  identification on the bounded eigenvalue surface**. This is itself
  a candidate audit lane.
- The WZ theorem at W4 only needs the gauge sector to exist, not its
  anomaly-completeness; so `retained_bounded` is sufficient input to
  the WZ theorem.
- The anomaly_forces_time_theorem's overall claim_type stays
  `bounded_theorem` because it has its own admitted bridges (i)-(iv).
  Sharpening NATIVE_GAUGE_CLOSURE to `positive_theorem` would not
  flip anomaly_forces_time to `retained` because of those independent
  admitted bridges.
