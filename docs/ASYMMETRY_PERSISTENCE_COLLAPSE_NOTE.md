# Asymmetry Persistence + Collapse Note

**Date:** 2026-04-02  
**Status:** bounded pilot complete

**Audit-conditional perimeter (2026-04-30, relabel 2026-05-06):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing
step class `C`. The audit chain-closure explanation is exact: "The
primary runner is registered, but it did not complete within the 60s
audit-loop runtime budget during re-audit. Until the runner is
optimized, marked as intentionally slow with a reason, or replaced by a
bounded proof artifact, the frozen replay cannot be checked in the
standard audit loop." The audit-stated repair target is
`compute_required: rerun within compute budget or supply cached
completed artifact.` This rigorization edit only sharpens the boundary
of the conditional perimeter; nothing here promotes audit status, and
no audit JSON is modified.

## Cited authority chain

The primary runner registered against this row is
`scripts/asymmetry_persistence_collapse_pilot.py`
(`runner_sha256 = e39f93682f3659b7a5343d0b24e228be936c0fe492dfd68697de0939ba5887d2`,
audit-window cache: `status: timeout, exit_code: None, elapsed_sec: 120.01`
at the standard `120 s` audit budget, deposited at
[`logs/runner-cache/asymmetry_persistence_collapse_pilot.txt`](../logs/runner-cache/asymmetry_persistence_collapse_pilot.txt)).
The pilot is genuinely slow because it sweeps:

- dense generated 3D graphs at `N=80, npl=50` and `N=100, npl=60`,
- three thresholds `0.0 / 0.10 / 0.20`,
- `8` matched seeds,
- `10` Monte Carlo collapse realizations at `p=0.2`,
- both linear and per-layer-normalization propagation lanes,

and the row tables below quote the deterministic stdout of that sweep.

Shared infrastructure imports inside the runner:

- `scripts/gap_topological_asymmetry_layernorm_combo.py`
  (admitted-context input; provides the layernorm-regulated propagator
  and asymmetry-persistence pruning rule used by all rows of the
  asymmetry-persistence cluster).

Closure of the regulated-propagator + pruning-rule step lives on the
admitted-context bracket of that import, not this row.

## Question

Does the generated asymmetry-persistence geometry remain useful when we add
stochastic collapse?

This pilot compares, on the same dense 3D generated graphs:

- baseline generated geometry
- asymmetry persistence only
- collapse only
- asymmetry persistence + collapse

When feasible, it also compares linear propagation against per-layer
normalization.

Script:
[scripts/asymmetry_persistence_collapse_pilot.py](../scripts/asymmetry_persistence_collapse_pilot.py)

Log:
[logs/2026-04-02-asymmetry-persistence-collapse-pilot.txt](../logs/2026-04-02-asymmetry-persistence-collapse-pilot.txt)
(historical frozen log path; the live audit-window cache deposit is
`logs/runner-cache/asymmetry_persistence_collapse_pilot.txt`, see
"Cited authority chain" above for status).

## Setup

- dense generated 3D graphs
- `N=80` with `npl=50`
- `N=100` with `npl=60`
- thresholds `0.00, 0.10, 0.20`
- `8` matched seeds
- collapse probability `p=0.2`
- `10` Monte Carlo realizations

## Strongest retained rows

### Unitary rows report `pur_min`

| N | threshold | baseline `pur_min` | persistence `pur_min` | layernorm persistence `pur_min` | keep% |
|---|---:|---:|---:|---:|---:|
| 80 | 0.10 | 0.998 | 0.981 | 0.889 | 97.4% |
| 80 | 0.20 | 0.998 | 0.981 | 0.881 | 97.2% |
| 100 | 0.10 | 0.989 | 0.947 | 0.869 | 98.0% |
| 100 | 0.20 | 0.989 | 0.953 | 0.860 | 97.7% |

### Collapse rows report averaged detector purity

| N | threshold | baseline collapse purity | persistence collapse purity | layernorm collapse purity | persistence+collapse LN |
|---|---:|---:|---:|---:|---:|
| 80 | 0.10 | 0.272 | 0.292 | 0.218 | 0.232 |
| 80 | 0.20 | 0.272 | 0.289 | 0.218 | 0.233 |
| 100 | 0.10 | 0.249 | 0.269 | 0.221 | 0.205 |
| 100 | 0.20 | 0.249 | 0.265 | 0.221 | 0.216 |

## Narrow conclusion

The generated asymmetry-persistence geometry remains useful in the unitary
lane: it lowers `pur_min`, and layernorm stacks on top of it at both
`N=80` and `N=100`.

On the collapse side, the same geometry is not a broad win. In the linear
collapse rows it slightly raises detector purity, so it does not clearly
improve decoherence. The only retained collapse-side pocket is narrow:
at `N=100`, `threshold=0.10`, layernorm plus persistence+collapse lowers
collapse purity to `0.205`, below the layernorm-only baseline `0.221`.

So the safe summary is:

- persistence is a real unitary decoherence aid
- collapse is not generically helped by persistence
- there is one narrow `N=100` layernorm-assisted pocket worth keeping
  alive, but not a scalable collapse rescue

## What is closed inside the audited scope (class-C conditional citation)

- The "Strongest retained rows" tables are deterministic stdout of the
  registered runner `scripts/asymmetry_persistence_collapse_pilot.py`
  at the configuration in the Setup block above.
- The narrow conclusion that asymmetry-persistence is a unitary aid
  but not a generic collapse-rescue is supported directly by those
  rows and is wider in scope than any single seed.

## What remains open (named missing bridge)

- The registered runner does not finish within the standard `120 s`
  audit-loop runtime budget; the audit-window cache currently records
  `status: timeout`. The audit verdict's repair target is
  `compute_required: rerun within compute budget or supply cached
  completed artifact.` Closing this row at the audit lane requires
  either a faster harness, a wider compute window declared as the
  intentionally-slow reason, or a bounded proof artifact replacing the
  full sweep.

## Boundary

This note does not modify the audit ledger, does not promote audit
status, does not assert a generic collapse rescue, and does not assert
that asymmetry-persistence + collapse closes the broader collapse
lane. It only records the audit verdict, cites the registered primary
runner and its frozen audit-window cache, and names the
admitted-context imports the row depends on.

