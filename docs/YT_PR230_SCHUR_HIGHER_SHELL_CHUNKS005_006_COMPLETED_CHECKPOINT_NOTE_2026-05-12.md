# PR230 Higher-Shell Chunks005-006 Completed Checkpoint

**Status:** bounded-support / higher-shell Schur scalar-LSZ chunks005-006
completed-mode checkpoints passed; no closure

**Runners:**

- `scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py`
- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`
- `scripts/frontier_yt_pr230_assumption_import_stress.py`
- `scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py`
- `scripts/frontier_yt_retained_closure_route_certificate.py`
- `scripts/frontier_yt_pr230_positive_closure_completion_audit.py`

**Certificates:**

- `outputs/yt_pr230_schur_higher_shell_chunk005_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_chunk006_checkpoint_2026-05-12.json`
- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / higher-shell Schur scalar-LSZ chunks005-006 completed-mode checkpoints passed
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

Higher-shell chunks005-006 completed under the separate non-colliding roots:

- `outputs/yt_pr230_schur_higher_shell_rows/`
- `outputs/yt_direct_lattice_correlator_production_schur_higher_shell_rows/`

The completed-mode chunk checkpoints verify, for both chunks:

- production run-control metadata on `L12xT24`;
- fixed seeds `2026057005` and `2026057006`;
- `numba_gauge_seed_v1` seed control;
- selected-mass-only FH/LSZ policy at mass `0.75`;
- preserved three-mass top scan at `0.45,0.75,1.05`;
- eleven higher-shell `C_ss` time-series rows;
- eleven taste-radial `C_sx/C_xx` source-cross rows;
- no use of `H_unit`, `yt_ward_identity`, observed selectors,
  `alpha_LM`, plaquette, or `u0`;
- no `kappa_s=1`, `c2=1`, or `Z_match=1` assumption.

The row JSON metadata records:

- chunk005: `created_utc=2026-05-12T10:21:08Z`,
  `runtime_seconds=7358.061`, seed `2026057005`;
- chunk006: `created_utc=2026-05-12T10:21:18Z`,
  `runtime_seconds=7368.229`, seed `2026057006`.

The wave-launcher status now records no active higher-shell workers,
`completed_chunk_indices=[1,2,3,4,5,6]`, and
`planned_launch_chunk_indices=[7,8]`.  It does not launch successor chunks in
this block.

## Boundary

These rows are higher-shell support only.  They are not a complete
higher-shell packet, not Schur A/B/C kernel rows, not complete monotonicity,
not a scalar-pole or threshold/FV/IR authority certificate, not canonical
`O_H`, not strict canonical `C_sH/C_HH` pole rows, not W/Z response, and not
physical `kappa_s`.

The source-cross rows are still emitted under the taste-radial second-source
certificate.  They remain `C_sx/C_xx` support unless a separate canonical
`O_H` identity/source-overlap bridge lands.

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
  --chunk-index 5 \
  --output outputs/yt_pr230_schur_higher_shell_chunk005_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_chunk_checkpoint.py \
  --chunk-index 6 \
  --output outputs/yt_pr230_schur_higher_shell_chunk006_checkpoint_2026-05-12.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py --max-concurrent 2
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=400 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=190 FAIL=0

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

No retained or `proposed_retained` top-Yukawa closure is authorized.
