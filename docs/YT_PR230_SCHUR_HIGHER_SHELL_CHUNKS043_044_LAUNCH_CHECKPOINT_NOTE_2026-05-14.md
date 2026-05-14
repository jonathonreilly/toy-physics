# PR230 Higher-Shell Chunks043-044 Launch Checkpoint

**Status:** run-control support / higher-shell Schur scalar-LSZ chunks043-044
launched; completed higher-shell support prefix remains 42/63; no closure

**Runner:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`

**Certificate:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`

```yaml
actual_current_surface_status: run-control support / higher-shell Schur scalar-LSZ chunks043-044 launched; completed prefix remains 42/63
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The wave launcher was run with an explicit launch request under the two-worker
cap:

```bash
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 \
  --chunk-indices 43-44 \
  --launch \
  --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0
```

It launched:

- chunk043: pid `31031`, seed `2026057043`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk043_20260514T040055Z.log`,
  output `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk043_2026-05-07.json`;
- chunk044: pid `31032`, seed `2026057044`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk044_20260514T040055Z.log`,
  output `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk044_2026-05-07.json`.

Both workers survived the verification interval and had distinct production
roots:

- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk043`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk044`

## Boundary

This block is run-control support only. Active jobs, logs, pid references,
partial directories, and launch certificates are not row evidence. Until the
workers write row JSONs and completed-mode chunk checkpoints pass,
chunks043-044 do not extend the completed higher-shell prefix beyond 42/63.

Even after completion, these rows remain higher-shell support unless a separate
physical bridge lands. The launch does not supply canonical `O_H`, strict
`C_sH/C_HH` pole rows, Schur A/B/C kernel rows, scalar-LSZ/FV/IR authority,
W/Z response, physical `kappa_s`, retained closure, or `proposed_retained`
closure.

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
