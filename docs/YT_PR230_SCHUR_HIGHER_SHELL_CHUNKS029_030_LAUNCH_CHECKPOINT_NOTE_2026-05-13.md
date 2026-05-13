# PR230 Higher-Shell Chunks029-030 Launch Checkpoint

**Status:** run-control / higher-shell Schur scalar-LSZ chunks029-030
launched; active workers are not row evidence; no closure

**Runner:**

- `scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py`

**Certificate:**

- `outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json`

```yaml
actual_current_surface_status: run-control / higher-shell Schur scalar-LSZ chunks029-030 launched; active workers are not row evidence
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Result

The Block62 package left the higher-shell support prefix at 28/63 completed,
with no active workers and the next planned wave `[29,30]`. This launch block
started exactly that next non-colliding wave under the two-worker cap:

- chunk029: pid `32764`, seed `2026057029`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk029_20260513T120309Z.log`;
- chunk030: pid `32765`, seed `2026057030`, log
  `outputs/yt_pr230_schur_higher_shell_rows/logs/L12_T24_chunk030_20260513T120309Z.log`.

The launcher verified both processes alive after the verification interval and
kept `proposal_allowed=false`. The launch certificate is restricted to the
chunks029-030 action surface: it records launched pids, output paths, and
seeds. It does not count active processes, logs, empty directories, partial
directories, or launch status as completed row evidence.

## Boundary

Chunks029-030 are run-control only until completed-mode chunk checkpoints pass.
The completed higher-shell support prefix remains the previously packaged
28/63. This launch block does not supply canonical `O_H`, strict
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

python3 scripts/frontier_yt_pr230_schur_higher_shell_wave_launcher.py \
  --max-concurrent 2 \
  --chunk-indices 29-30 \
  --launch \
  --verify-seconds 5
# SUMMARY: PASS=11 FAIL=0; launched chunks029-030 pids 32764,32765

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

ps -p 32764,32765 -o pid,ppid,etime,command
# both chunk workers active after launch packaging began
```

No retained or `proposed_retained` closure is authorized.
