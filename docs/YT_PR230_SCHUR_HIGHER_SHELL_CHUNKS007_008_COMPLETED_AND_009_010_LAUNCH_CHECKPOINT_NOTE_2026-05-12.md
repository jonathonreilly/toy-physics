# PR230 Higher-Shell Chunks007-008 Completed And Chunks009-010 Launch Checkpoint

**Status:** bounded-support / higher-shell Schur scalar-LSZ chunks007-008
completed-mode checkpoints passed; chunks009-010 launched as run-control only;
no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py`
- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_chunk007_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk008_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / higher-shell Schur scalar-LSZ chunks007-008 completed-mode checkpoints passed; chunks009-010 launched as run-control only
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

Higher-shell chunks007-008 completed under the separate non-colliding roots:

- `outputs/yt_pr230_schur_higher_shell_rows/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`

The completed-mode chunk checkpoints verify, for both chunks:

- production run-control metadata on `L12xT24`;
- fixed seeds `2026057007` and `2026057008`;
- `numba_gauge_seed_v1` seed control;
- selected-mass-only FH/LSZ policy at mass `0.75`;
- preserved three-mass top scan at `0.45,0.75,1.05`;
- eleven higher-shell `C_ss` time-series rows;
- eleven taste-radial `C_sx/C_xx` source-cross rows;
- no use of `H_unit`, `yt_ward_identity`, observed selectors,
  `alpha_LM`, plaquette, or `u0`;
- no `kappa_s=1`, `c2=1`, or `Z_match=1` assumption.

The row JSON metadata records:

- chunk007: `created_utc=2026-05-12T12:48:45Z`,
  `runtime_seconds=7609.597`, seed `2026057007`;
- chunk008: `created_utc=2026-05-12T12:48:41Z`,
  `runtime_seconds=7605.274`, seed `2026057008`.

After completed-mode checkpointing, the wave launcher was run in launch mode
with `--max-concurrent 2` and launched the next non-colliding support wave:

- chunk009: pid `39242`, seed `2026057009`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk009_20260512T125038Z.log`;
- chunk010: pid `39243`, seed `2026057010`,
  log `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk010_20260512T125038Z.log`.

The launcher verified both new workers alive after the verification interval.
Those launched jobs are run-control state only until their completed row JSONs
and completed-mode chunk checkpoints exist.

## Boundary

Chunks007-008 are higher-shell support rows only.  Chunks009-010 are launched
run-control only.  Neither state is a complete higher-shell packet, Schur
A/B/C kernel row evidence, complete monotonicity, scalar-pole or
threshold/FV/IR authority, canonical `O_H`, strict canonical `C_sH/C_HH` pole
rows, W/Z response, physical `kappa_s`, retained closure, or
`proposed_retained` closure.

The source-cross rows remain under the taste-radial second-source certificate.
They remain `C_sx/C_xx` support unless a separate canonical `O_H`
identity/source-overlap bridge lands.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  scripts/frontier_yt_pr230_campaign_status_certificate.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# OK

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 7 \
  --output outputs/yt_pr230_schur_higher_shell_chunk007_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 8 \
  --output outputs/yt_pr230_schur_higher_shell_chunk008_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0; completed_chunk_indices=[1,2,3,4,5,6,7,8]

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --launch --max-concurrent 2 --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0; launched chunks009-010

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=403 FAIL=0
```

Full final gates remain to be run after chunks009-010 complete and are
checkpointed.
