# PR230 Higher-Shell Chunks051-052 Launch Checkpoint

**Status:** run-control support / higher-shell Schur scalar-LSZ chunks051-052
launched; completed higher-shell support prefix remains 50/63 until completed
row artifacts pass chunk checkpoints; no closure

**Runner:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`

**Certificate:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`

```yaml
actual_current_surface_status: run-control support / higher-shell Schur scalar-LSZ chunks051-052 launched; completed prefix remains 50/63
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

After Block84 packaged completed chunks049-050 and left the wave launcher with
active `[]` and planned `[51,52]`, the launcher was run with:

```bash
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 \
  --chunk-indices 51-52 \
  --launch \
  --verify-seconds 5
```

The launch-mode certificate reports `PASS=11 FAIL=0` and records:

- chunk051: pid `79756`, seed `2026057051`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk051_20260514T124922Z.log`,
  output target
  `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk051_2026-05-07.json`,
  production root
  `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk051`;
- chunk052: pid `79757`, seed `2026057052`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk052_20260514T124922Z.log`,
  output target
  `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk052_2026-05-07.json`,
  production root
  `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk052`.

A direct `ps` check after launch showed both workers alive and CPU-active:

```text
79756 Rs 00:17 ~100% CPU
79757 Rs 00:17 ~100% CPU
```

The launch command scopes the launcher certificate to chunks051-052, so its
launch-mode `completed_chunk_indices` are not used as a full-prefix census.
The durable completed prefix remains the Block84 completed-mode prefix
`[1..50]` until chunks051-052 write row JSONs and completed-mode chunk
checkpoints pass.

## Boundary

This checkpoint is run-control support only. Active processes, logs, pids,
partial output directories, and launch-state certificates are not completed
row evidence. Chunks051-052 do not count toward the higher-shell completed
prefix until the row JSONs and volume artifacts exist and completed-mode chunk
checkpoints pass.

No canonical `O_H`, strict `C_sH/C_HH` pole rows, Schur A/B/C kernel rows,
scalar-LSZ/FV/IR authority, W/Z response rows, physical `kappa_s`, retained
closure, or `proposed_retained` closure is supplied by this launch.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  scripts/frontier_yt_pr230_campaign_status_certificate.py \
  scripts/frontier_yt_pr230_assumption_import_stress.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py \
  scripts/frontier_yt_retained_closure_route_certificate.py
# OK

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 \
  --chunk-indices 51-52 \
  --launch \
  --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0

ps -p 79756,79757 -o pid=,stat=,etime=,pcpu=,pmem=,command=
# both workers alive and CPU-active

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=421 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=194 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=319 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=73 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK, 5 known warnings

python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings

git diff --check
# OK
```

No retained or `proposed_retained` closure is authorized.
