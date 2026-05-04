# PR #230 FH/LSZ Paired Variance Calibration Orchestrator

**Status:** bounded-support / paired x8/x16 variance calibration orchestration  
**Runner:** `scripts/frontier_yt_fh_lsz_paired_variance_calibration_orchestrator.py`  
**Status output:** `outputs/yt_fh_lsz_paired_variance_calibration_orchestrator_status_2026-05-04.json`

## Purpose

This runner keeps the future eight-mode scalar-pole calibration separate from
the current four-mode FH/LSZ chunk stream.  It reads the paired x8/x16
variance-calibration manifest, detects completed or running calibration jobs,
optionally launches missing x8/x16 jobs, and reruns the paired variance gates
after outputs land.

The orchestrator respects a global production-job cap.  With the current
chunks047-052 wave saturating six production jobs, dry-run status shows no
launch slots and prevents accidental overcommit.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_paired_variance_calibration_orchestrator.py
python3 scripts/frontier_yt_fh_lsz_paired_variance_calibration_orchestrator.py --dry-run
# poll=1 completed=[] running=[] missing=['x16', 'x8'] all_jobs=6 launch_slots=0
```

## Claim Boundary

This is run control only.  It does not claim retained or proposed-retained
`y_t`, does not treat variance calibration as scalar LSZ normalization, and
does not mix the eight-mode calibration stream with the four-mode production
chunks as one homogeneous physical readout.
