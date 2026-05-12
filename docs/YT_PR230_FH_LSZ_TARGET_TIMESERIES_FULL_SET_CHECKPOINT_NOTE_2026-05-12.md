# PR230 FH/LSZ Target-Timeseries Full-Set Checkpoint

Status: bounded-support / full L12 FH/LSZ target-timeseries packet packaged;
not scalar-LSZ or top-Yukawa closure

Runner:
`scripts/frontier_yt_fh_lsz_target_timeseries_full_set_checkpoint.py`

Certificate:
`outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json`

```yaml
actual_current_surface_status: bounded-support / FH-LSZ full L12 target-timeseries packet checkpoint
proposal_allowed: false
bare_retained_allowed: false
checked_chunks: 63
replacement_queue: []
```

The FH/LSZ target-timeseries replacement campaign is complete for the current
L12 ready set.  The refreshed combiner reports `present=63`, `ready=63`,
`missing=0`, and `1008` saved configurations against the `1000` target.  The
autocorrelation/target-timeseries gate reports `complete_count=63`,
`complete_for_all_ready_chunks=true`, and no incomplete ready chunks.

The dated full-set checkpoint checks every chunk artifact and generic
target-timeseries checkpoint.  It verifies `numba_gauge_seed_v1` seed control,
63 distinct seeds, production target mode, per-configuration source effective
energies and slopes, and scalar `C_ss_timeseries` rows for the four target
modes.  Some chunks predate the selected-mass/normal-cache optimization, so
the checkpoint records that optimization split explicitly rather than treating
it as a schema failure.

Validation:

```bash
python3 -m py_compile \
  scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py \
  scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py \
  scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py \
  scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py \
  scripts/frontier_yt_fh_lsz_target_timeseries_full_set_checkpoint.py

python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_timeseries_full_set_checkpoint.py
# SUMMARY: PASS=9 FAIL=0
```

Claim boundary: this closes only the target-timeseries replacement queue.  It
does not derive `kappa_s`, identify the scalar source pole with canonical
`O_H`, provide `C_sH/C_HH` pole rows, provide same-source W/Z response rows or
strict `g2` authority, prove scalar-pole derivative/model-class/FV/IR
control, or authorize retained or `proposed_retained` top-Yukawa closure.

The separate higher-shell Schur/scalar-LSZ chunks001-002 are still live
run-control state until completed row JSON exists and completed-mode
checkpoints pass.
