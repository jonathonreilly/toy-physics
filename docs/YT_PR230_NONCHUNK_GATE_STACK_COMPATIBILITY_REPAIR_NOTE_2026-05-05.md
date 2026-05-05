# PR230 Non-Chunk Gate Stack Compatibility Repair

**Status:** exact support / audit-gate compatibility repair only; positive closure remains open

**Updated runners:**

- `scripts/frontier_yt_pr230_nonchunk_current_surface_exhaustion_gate.py`
- `scripts/frontier_yt_pr230_nonchunk_terminal_route_exhaustion_gate.py`

**Refreshed certificates:**

- `outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json`
- `outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json`
- `outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json`
- `outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json`

## Purpose

After cycle 35, rerunning the older non-chunk gate stack exposed a stale
compatibility assumption.  The worklist now includes
`top_wz_closed_covariance_theorem`, while the cycle-8 exhaustion and terminal
gates still carried the older future-artifact key set.  The exhaustion gate
also expected the cycle-7 Schur closeout wording, even though the current
route-family audit now records the later, stricter
`no_current_surface_nonchunk_route` closeout.

## Result

The repair makes the gate stack accept both the legacy Schur closeout and the
current no-route closeout, and it expands the future-artifact key set to
include `top_wz_closed_covariance_theorem`.

This does not add a same-surface row, certificate, or theorem.  It only keeps
the stop/reopen gates rerunnable against the current PR230 surface.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_nonchunk_current_surface_exhaustion_gate.py \
  scripts/frontier_yt_pr230_nonchunk_future_artifact_intake_gate.py \
  scripts/frontier_yt_pr230_nonchunk_terminal_route_exhaustion_gate.py \
  scripts/frontier_yt_pr230_nonchunk_reopen_admissibility_gate.py

python3 scripts/frontier_yt_pr230_nonchunk_current_surface_exhaustion_gate.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_nonchunk_future_artifact_intake_gate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_pr230_nonchunk_terminal_route_exhaustion_gate.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_nonchunk_reopen_admissibility_gate.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

No retained or `proposed_retained` top-Yukawa closure is authorized.  The
admissible reopen condition is unchanged: a listed same-surface row,
certificate, or theorem must exist as a parseable claim-status artifact before
the non-chunk route surface can execute again.
