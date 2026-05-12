# PR230 Higher-Shell Chunks017-018 Launch Checkpoint

**Status:** run-control / higher-shell Schur scalar-LSZ chunks017-018
launched; active workers are not row evidence; no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: run-control / higher-shell Schur scalar-LSZ chunks017-018 launched; active workers are not row evidence
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The next non-colliding higher-shell support wave was launched after completed
chunks015-016 were packaged:

- chunk017: pid `46609`, seed `2026057017`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk017_20260512T221412Z.log`;
- chunk018: pid `46610`, seed `2026057018`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk018_20260512T221412Z.log`.

The launcher ran with `--max-concurrent 2 --chunk-indices 17-18 --launch
--verify-seconds 5` and verified both workers alive after the verification
interval.

The campaign status runner was extended to recognize the restricted
chunks017-018 launch-state as run-control support only. In this restricted
launch certificate, `completed_chunk_indices=[]` and
`active_or_completed_chunk_indices=[]` are allowed because the launch command
intentionally scoped discovery to the requested next wave. The durable
completed prefix before launch remains chunks001-016, recorded in the prior
Block50 package.

## Boundary

Chunks017-018 are active run-control only until completed-mode checkpoints
pass. Active processes, logs, pid files, partial directories, and launch-state
certificates are not completed row evidence.

This block does not supply canonical `O_H`, strict `C_sH/C_HH` pole rows,
Schur A/B/C kernel rows, scalar-LSZ moment/FV/IR authority, W/Z response rows,
physical `kappa_s`, retained closure, or `proposed_retained` closure.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_campaign_status_certificate.py \
  scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py
# OK

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 --chunk-indices 17-18 --launch --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=415 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=194 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=319 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=73 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK: no errors; 5 existing warnings

python3 docs/audit/scripts/audit_lint.py --strict
# OK: no errors; 5 existing warnings

git diff --check
# OK
```

No retained or `proposed_retained` closure is authorized.
