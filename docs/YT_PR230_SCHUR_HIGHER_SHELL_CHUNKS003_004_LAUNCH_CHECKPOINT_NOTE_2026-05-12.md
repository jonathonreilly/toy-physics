# PR230 Higher-Shell Chunks003-004 Launch Checkpoint

**Status:** run-control / higher-shell Schur scalar-LSZ chunks003-004 active
pending; no row evidence and no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk003_pending_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk004_pending_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: run-control / higher-shell Schur scalar-LSZ chunks003-004 active pending
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The next non-colliding higher-shell wave was launched under the separate
higher-shell roots with the same two-worker cap:

- chunk003: seed `2026057003`, pid `84017`
- chunk004: seed `2026057004`, pid `84018`

The launcher uses the fixed higher-shell production contract, no `--resume`,
and writes only under:

- `outputs/yt_pr230_schur_higher_shell_rows/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`

The status certificate now records `completed_chunk_indices=[1,2]`,
`active_chunk_indices=[3,4]`, and
`active_or_completed_chunk_indices=[1,2,3,4]`.

## Boundary

Chunks003-004 are active-pending run-control only.  The pending checkpoint
certificates prove only that a single active worker owns each chunk and that
the launch state does not authorize retained or `proposed_retained` wording.
Logs, pids, active processes, partial directories, and pending checkpoints are
not row evidence.

This block does not claim complete higher-shell rows, complete monotonicity,
Schur A/B/C kernel rows, scalar pole/FV/IR authority, canonical `O_H`,
canonical `C_sH/C_HH`, W/Z response, physical `kappa_s`, retained, or
`proposed_retained` top-Yukawa closure.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  scripts/frontier_yt_pr230_campaign_status_certificate.py

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 --chunk-indices 3-4 --launch --verify-seconds 2
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 3 --allow-pending-active \
  --output outputs/yt_pr230_schur_higher_shell_chunk003_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 4 --allow-pending-active \
  --output outputs/yt_pr230_schur_higher_shell_chunk004_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=386 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=177 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=319 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=73 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK, 5 known warnings; newly seeded=1; re-audit required=0

python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings

git diff --check
# OK
```

No closure statement: PR #230 remains draft/open and no retained or
`proposed_retained` top-Yukawa closure is authorized.
