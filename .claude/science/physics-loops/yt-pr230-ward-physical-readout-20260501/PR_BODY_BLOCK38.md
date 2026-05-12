## Block38 checkpoint: higher-shell Schur/LSZ chunks001-002 active

Started the separate higher-shell Schur/scalar-LSZ production wave after the
four-mode packet completed and the launch preflight cleared.

- Launched chunks001-002 only, under a conservative two-worker cap.
- Chunk001 seed: `2026057001`.
- Chunk002 seed: `2026057002`.
- Output roots are separate from the completed four-mode packet:
  `outputs/yt_pr230_schur_higher_shell_rows/` and
  `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`.
- No `--resume` is used.

Validation:

```text
python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py --chunk-index 1 --allow-pending-active --output outputs/yt_pr230_schur_higher_shell_chunk001_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py --chunk-index 2 --allow-pending-active --output outputs/yt_pr230_schur_higher_shell_chunk002_pending_checkpoint_2026-05-12.json
# SUMMARY: PASS=2 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=369 FAIL=0
```

Claim boundary: this is run-control support only.  Active workers, logs, pid
files, empty directories, partial directories, launch status, and
uncheckpointed row outputs are not row evidence, not complete monotonicity,
not scalar-pole or threshold/FV/IR authority, not canonical `O_H` or
source-overlap authority, not W/Z response, and not retained or
`proposed_retained` top-Yukawa closure.  PR #230 remains draft/open.
