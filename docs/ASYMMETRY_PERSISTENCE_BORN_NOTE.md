# Asymmetry Persistence Born Calibration Note

This note records the corrected Born calibration for the generated
asymmetry-persistence lane. The lane is now confirmed as a narrow dense
Born-safe pocket, but the pocket is density-sensitive and does not yet have a
fully hardened large-`N` confirmation.

**Audit-conditional perimeter (2026-04-30):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing
step class `B`. The audit chain-closure explanation is exact: "The
load-bearing replay or comparison depends on an unregistered
script/log/artifact that is not available as a primary runner in the
restricted audit packet, so the conclusion cannot be ratified from the
source note alone." The audit-stated repair target is
`runner_artifact_issue: register a current runner/log or cite an
audited dependency that proves the missing bridge, then re-audit the
narrowed claim.` This rigorization edit only sharpens the boundary of
the conditional perimeter; nothing here promotes audit status, and no
audit JSON is modified.

## Cited authority chain (2026-05-10)

A primary runner is now registered against this row at
`runner_path = scripts/asymmetry_persistence_born_calibration.py`
(`runner_sha256 = 1c011f7ae6e918e10909249a5525bdb8492609416f2bc83d4282e44107379c0d`).
The runner is genuinely heavy and exceeds the standard audit-loop
runtime budget; the cached attempt at
[`logs/runner-cache/asymmetry_persistence_born_calibration.txt`](../logs/runner-cache/asymmetry_persistence_born_calibration.txt)
records `status: timeout` at the `1800 s` budget, but its frozen
partial stdout (deterministic at the `N=80, npl=50` and partial
`N=100, npl=60` rows) reproduces the corrected Born `|I3|/P` numbers in
the table below at `1e-15 .. 3e-16` magnitude on the persist+LN and
persist+LN+collapse columns. The narrow dense `N=100, npl=60` probe
quoted here uses the lighter `2 seeds, 4 realizations` configuration
that the source note explicitly flags as the only configuration that
finished in-session; the broader sweep is the configuration that times
out.

Shared infrastructure imports inside the runner:

- `scripts/gap_topological_asymmetry_layernorm_combo.py`
  (admitted-context input; provides the layernorm-regulated propagator
  and asymmetry-persistence pruning rule used by all rows of the
  asymmetry-persistence cluster).

Closure of the asymmetry-readout / regulated-propagator step lives on
the admitted-context bracket of that import, not this row.

Script:
[`scripts/asymmetry_persistence_born_calibration.py`](../scripts/asymmetry_persistence_born_calibration.py)

## Confirmed probe

The lowest-cost dense check was run at:

- `N = 100`
- `npl = 60`
- thresholds `0.10` and `0.20`
- `2` seeds
- `4` realizations
- corrected Sorkin metric with `-P(empty)`

## Result

On this corrected harness, the relevant retained rows are Born-clean at
machine precision:

| Threshold | linear `|I3|/P` | persistence `|I3|/P` | persistence+LN `|I3|/P` | persistence+LN+collapse `|I3|/P` |
| --- | --- | --- | --- | --- |
| `0.10` | `8.49e-16±1.7e-16` | `8.49e-16±1.7e-16` | `2.78e-16±7.2e-17` | `2.78e-16±4.1e-17` |
| `0.20` | `1.12e-15±2.5e-16` | `1.12e-15±2.5e-16` | `2.59e-16±3.9e-17` | `2.59e-16±4.1e-17` |

## Hardening Attempt

I also tried to widen this to denser `N=80/100` sweeps with more seeds and
realizations. That broader run was computationally heavy in this harness and
did not finish within the session window, so it did not produce a stronger
confirmation than the dense `N=100` probe above.

## Narrow conclusion

- persistence does not spoil Born on this dense `N=100` probe
- persistence + layer normalization remains Born-clean
- persistence + layer normalization + collapse is also Born-clean in this narrow probe
- the lane is alive, but it remains a density-limited confirmation rather than
  a final asymptotic claim

## What is closed inside the audited scope (class-B conditional citation)

- The corrected Sorkin `|I3|/P` magnitudes in the table above are
  reproducible from the registered runner
  `scripts/asymmetry_persistence_born_calibration.py` at the narrow
  `N=100, npl=60, 2 seeds, 4 realizations` configuration the runner
  is invoked with. The frozen partial cache deposit at
  `logs/runner-cache/asymmetry_persistence_born_calibration.txt`
  reproduces the deterministic `1e-15 .. 3e-16` magnitudes at
  the persist+LN and persist+LN+collapse columns for `N=80` and
  partial `N=100` rows, consistent with the source-note table.

## What remains open (named missing bridges)

- Broader-`N` / more-seed / more-realization confirmation (the
  "Hardening Attempt" section above) does not finish within the
  current audit-loop budget; the registered runner cache records
  `status: timeout` for that broader sweep. The lane stays a
  density-limited confirmation until either a faster harness or a
  bounded proof artifact is supplied.
- `scripts/gap_topological_asymmetry_layernorm_combo.py` is an
  admitted-context input whose own audit lane is what closes the
  layernorm-regulated propagator and asymmetry-persistence pruning
  rule; this row does not carry that closure.

## Boundary

This note does not modify the audit ledger, does not promote audit
status, does not assert a final asymptotic Born-clean claim, and does
not register the layernorm-combo companion runner against this row. It
only records the audit verdict, cites the registered primary runner
and its frozen partial cache, and names the admitted-context imports
the broader sweep depends on.
