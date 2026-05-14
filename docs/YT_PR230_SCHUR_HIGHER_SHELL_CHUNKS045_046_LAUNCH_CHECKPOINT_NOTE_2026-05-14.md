# PR230 Higher-Shell Chunks045-046 Launch Checkpoint

**Status:** run-control support / higher-shell Schur scalar-LSZ chunks045-046
launched; completed higher-shell support prefix remains 44/63; no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: run-control support / higher-shell Schur scalar-LSZ chunks045-046 launched; completed higher-shell support prefix remains 44/63
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The wave launcher started the next non-colliding support wave under the
two-worker cap:

- chunk045: pid `41577`, seed `2026057045`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk045_20260514T061330Z.log`
- chunk046: pid `41578`, seed `2026057046`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk046_20260514T061330Z.log`

The launched commands use distinct output paths:

- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk045_2026-05-07.json`
- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk046_2026-05-07.json`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk045`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk046`

The launcher verifies both workers alive after the verification interval. The
completed prefix remains 44/63 until row JSONs exist and completed-mode chunk
checkpoints pass.

## Boundary

Chunks045-046 are run-control only in this checkpoint. Active jobs, logs, pid
references, partial output directories, and launch-state certificates are not
completed row evidence and do not supply canonical `O_H`, strict `C_sH/C_HH`
pole rows, Schur A/B/C kernel rows, scalar-LSZ/FV/IR authority, W/Z response,
physical `kappa_s`, retained closure, or `proposed_retained` closure.

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
  --chunk-indices 45-46 \
  --launch \
  --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0

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
