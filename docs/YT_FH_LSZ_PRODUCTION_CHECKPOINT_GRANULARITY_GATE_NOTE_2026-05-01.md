# PR #230 FH/LSZ Production Checkpoint Granularity Gate

**Status:** open / FH-LSZ production checkpoint granularity gate blocks
foreground launch

## Question

The joint FH/LSZ manifest now contains production-targeted `--resume`
commands.  Before launching under a 12-hour foreground campaign, the route
needs one more check:

```text
Does --resume create safely checkpointed production progress inside the
campaign window?
```

## Result

No.  The harness currently resumes only completed per-volume artifacts:

```text
outputs/yt_direct_lattice_correlator_production/L*/ensemble_measurement.json
```

Those artifacts are written after `run_volume(...)` returns.  There is no
detected mid-volume configuration checkpoint for gauge state, RNG state, and
accumulated FH/LSZ measurements.

The smallest projected joint shard is:

```text
L12_T24 joint mass-scaled hours: 180.069033057
campaign foreground window: 12h
```

Therefore a foreground launch would be a partial compute job with no
completed production output and no retained-grade evidence.

## Claim Boundary

This block does not weaken the production route.  It defines the launch
precondition:

```text
production route requires either chunk-level checkpoint/resume support
or an external scheduler/walltime budget long enough to finish at least
the smallest shard.
```

The manifest remains launch planning only.  Partial logs or interrupted runs
must not be used as production evidence.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_production_checkpoint_granularity_gate.py
python3 scripts/frontier_yt_fh_lsz_production_checkpoint_granularity_gate.py
# SUMMARY: PASS=9 FAIL=0
```

## Next Action

Either add per-configuration or bounded-chunk checkpoint/resume support for
the FH/LSZ harness, run the manifest under a scheduler that can finish the
smallest shard, or continue the analytic scalar-denominator/residue theorem
route.
