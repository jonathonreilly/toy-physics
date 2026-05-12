# PR230 Higher-Shell Chunks015-016 Completed Checkpoint

**Status:** bounded-support / higher-shell Schur scalar-LSZ chunks015-016
completed-mode checkpoints passed; higher-shell support prefix now 16/63; no
closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py`
- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_chunk015_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk016_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / higher-shell Schur scalar-LSZ chunks015-016 completed-mode checkpoints passed; higher-shell support prefix 16/63
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

Higher-shell chunks015-016 completed under the separate non-colliding roots:

- `outputs/yt_pr230_schur_higher_shell_rows/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`

The completed-mode chunk checkpoints verify, for both chunks:

- production run-control metadata on `L12xT24`;
- fixed seeds `2026057015` and `2026057016`;
- `numba_gauge_seed_v1` seed control;
- selected-mass-only FH/LSZ policy at mass `0.75`;
- preserved three-mass top scan at `0.45,0.75,1.05`;
- eleven higher-shell `C_ss` time-series rows;
- eleven taste-radial `C_sx/C_xx` source-cross rows;
- no use of `H_unit`, `yt_ward_identity`, observed selectors,
  `alpha_LM`, plaquette, or `u0`;
- no `kappa_s=1`, `c2=1`, or `Z_match=1` assumption.

The row JSON metadata records:

- chunk015: `created_utc=2026-05-12T22:03:39Z`, seed `2026057015`,
  runtime `7268.026` seconds;
- chunk016: `created_utc=2026-05-12T22:03:30Z`, seed `2026057016`,
  runtime `7258.438` seconds.

After completed-mode checkpointing, the wave launcher was run without launch.
It records `completed_chunk_indices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]`,
no active higher-shell workers, and `planned_launch_chunk_indices=[17,18]` if
the support campaign continues.

## Boundary

Chunks015-016 are higher-shell support rows only. They extend the completed
higher-shell prefix to 16/63 planned chunks, but this is not a complete
higher-shell packet, not Schur A/B/C kernel row evidence, not complete
monotonicity, not scalar-pole or threshold/FV/IR authority, not canonical
`O_H`, not strict canonical `C_sH/C_HH` pole rows, not W/Z response, not
physical `kappa_s`, not retained closure, and not `proposed_retained` closure.

The source-cross rows remain under the taste-radial second-source certificate.
They remain `C_sx/C_xx` support unless a separate canonical `O_H`
identity/source-overlap bridge lands.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  scripts/frontier_yt_pr230_campaign_status_certificate.py \
  scripts/frontier_yt_pr230_assumption_import_stress.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py \
  scripts/frontier_yt_retained_closure_route_certificate.py
# OK

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 15 \
  --output outputs/yt_pr230_schur_higher_shell_chunk015_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 16 \
  --output outputs/yt_pr230_schur_higher_shell_chunk016_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0; completed_chunk_indices=[1..16]

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=414 FAIL=0

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
