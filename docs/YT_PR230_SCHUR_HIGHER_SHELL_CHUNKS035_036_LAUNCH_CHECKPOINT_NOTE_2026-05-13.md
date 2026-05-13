# PR230 Higher-Shell Chunks035-036 Launch Checkpoint

**Status:** run-control support / higher-shell Schur scalar-LSZ chunks035-036
launched; completed higher-shell prefix remains 34/63 until completed-mode
checkpoints pass; no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: run-control support / higher-shell Schur scalar-LSZ chunks035-036 launched; completed prefix remains 34/63
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The next non-colliding higher-shell support wave was launched under the
two-worker cap:

- chunk035: pid `68837`, seed `2026057035`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk035_20260513T185737Z.log`
- chunk036: pid `68838`, seed `2026057036`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk036_20260513T185737Z.log`

The launcher verified both workers alive after the verification interval. The
production output roots are distinct:

- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk035/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk036/`

No `--resume` rerun is used. Completed outputs are not overwritten.

## Boundary

Chunks035-036 are active run-control only until their row JSONs, volume
artifacts, and completed-mode chunk checkpoint certificates exist and pass.
Active processes, logs, pid files, partial output directories, and launcher
state are not completed row evidence.

This launch does not supply a complete higher-shell packet, canonical `O_H`,
strict `C_sH/C_HH` pole rows, Schur A/B/C kernel rows, scalar-LSZ/FV/IR
authority, W/Z response, physical `kappa_s`, retained closure, or
`proposed_retained` closure.

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
  --max-concurrent 2 --chunk-indices 35-36 --launch --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0; launched chunks035-036 pids 68837,68838

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
```

No retained or `proposed_retained` closure is authorized.
