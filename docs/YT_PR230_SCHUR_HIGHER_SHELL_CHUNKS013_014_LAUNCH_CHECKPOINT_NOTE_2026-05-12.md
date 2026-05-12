# PR230 Higher-Shell Chunks013-014 Launch Checkpoint

Status: run-control support only.

This checkpoint launches the next non-colliding higher-shell Schur/scalar-LSZ
support wave after the completed chunks011-012 package advanced the prefix to
12/63.  The launch is infrastructure support only.  Active processes, logs,
pid files, partial directories, and launch-state certificates are not row
evidence and do not authorize retained or `proposed_retained` top-Yukawa
closure wording.

## Launch

Command:

```bash
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2 --chunk-indices 13-14 --launch --verify-seconds 5
```

Result:

- chunk013 launched with pid `40305`, seed `2026057013`, and log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk013_20260512T174550Z.log`;
- chunk014 launched with pid `40306`, seed `2026057014`, and log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk014_20260512T174550Z.log`;
- the launcher certificate records `PASS=11 FAIL=0` and both workers alive
  after the verification interval;
- the campaign-status runner now recognizes the restricted 13/14 launch-state
  as run-control support and passes `PASS=411 FAIL=0`.

The launched output paths are:

- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk013_2026-05-07.json`;
- `outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk014_2026-05-07.json`;
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk013`;
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/L12_T24_chunk014`.

Completed-mode checkpoints for chunks013-014 must be run only after those
workers exit and write row JSON plus volume artifacts.

## Validation

```bash
python3 -m py_compile scripts/frontier_yt_pr230_campaign_status_certificate.py scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py
# OK
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2 --chunk-indices 13-14 --launch --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=411 FAIL=0
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

## Claim Boundary

This block does not supply completed chunks013-014 row evidence.  It does not
provide a complete higher-shell packet, canonical `O_H`, strict `C_sH/C_HH`
pole rows, Schur A/B/C kernel rows, scalar-LSZ/FV/IR authority, W/Z response
rows, strict `g2`, matched covariance, physical `kappa_s`, retained closure,
or `proposed_retained` closure.  PR #230 remains draft/open.
