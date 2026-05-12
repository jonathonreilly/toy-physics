# PR230 Higher-Shell Schur/LSZ Wave Launcher

Status: run-control / higher-shell Schur scalar-LSZ chunks001-002 active;
not row evidence and not top-Yukawa closure

Runner:
`scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`

Pending/completed chunk checkpoint runner:
`scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py`

Certificate:
`outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`

```yaml
actual_current_surface_status: run-control / higher-shell Schur scalar-LSZ wave launcher status; active or launched jobs are not physics evidence
proposal_allowed: false
bare_retained_allowed: false
wave_launcher_passed: true
max_concurrent: 2
active_chunk_indices: [1, 2]
```

After the four-mode packet reached `ready=63/63`, the higher-shell production
contract allowed a separate non-colliding higher-shell campaign.  This block
launched only chunks001-002 under the separate roots:

- `outputs/yt_pr230_schur_higher_shell_rows/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`

The launcher/status runner verifies the production contract, the 63-command
preview, no-resume higher-shell commands, fixed seeds `2026057001` and
`2026057002`, active-process non-collision, no blocking partial output dirs,
and a conservative two-worker cap.

The chunk checkpoint runner also records active-pending certificates for the
two running chunks.  These pending certificates pass only as run control:

- `outputs/yt_pr230_schur_higher_shell_chunk001_pending_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk002_pending_checkpoint_2026-05-12.json`

This block does not claim retained or `proposed_retained` closure.  Active
workers, logs, pid files, empty directories, partial directories, launch
status, and uncheckpointed row outputs are run-control state only.  They do
not supply complete monotonicity, scalar pole authority, threshold/FV/IR
authority, canonical `O_H`, source-overlap, W/Z physical response, `kappa_s`,
or top-Yukawa closure.

Verification:

```bash
python3 -m py_compile scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0
python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py --chunk-index 1 --allow-pending-active --output outputs/yt_pr230_schur_higher_shell_chunk001_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0
python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py --chunk-index 2 --allow-pending-active --output outputs/yt_pr230_schur_higher_shell_chunk002_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=369 FAIL=0
```

Next action: monitor chunks001-002.  When completed row JSON exists, run a
completed-mode higher-shell chunk checkpoint before combining rows or making
any scalar-LSZ/Schur authority claim.
