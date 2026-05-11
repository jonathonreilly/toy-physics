# Source-Resolved Transverse Propagating Green

**Date:** 2026-04-05  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/source-resolved-green-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/source-resolved-green-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale source-resolved Green runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `source_resolved_transverse_propagating_green_note`):**

> Issue: The note's load-bearing positive transverse correction is stale relative to scripts/source_resolved_transverse_propagating_green.py. Current output gives transverse - same = -2.30e-05, -4.60e-05, -9.23e-05, -1.86e-04, not the positive values frozen in the note; support-fraction delta is 0.000e+00; and the printed trans/same column is actually trans_delta / inst_delta, with true trans/same about 0.990. Why this blocks: the candidate retained-grade claim depends on transverse transport being a detectable positive correction relative to same-site memory, but the current executable artifact shows a small negative centroid correction and no support-fraction broadening. Repair target: update or fix the runner/note pair, compute true trans/same and trans/inst separately, add assertion gates for the intended centroid/support observable, and rerun from the exact artifact that produced the frozen rows if they are meant to be retained. Claim boundary until fixed: it is safe to claim only that the current runner preserves zero-source reduction, 4/4 TOWARD sign, and F~M exponent 1.00 while producing a small negative transverse-minus-same centroid shift and unchanged support fraction; it is not safe to claim a retained positive transverse-transport pocket.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Artifact chain

- [`scripts/source_resolved_transverse_propagating_green.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_transverse_propagating_green.py)

## Question

Does the exact-lattice Green pocket change in a meaningful way if the field
gets one minimal transverse-transport step, instead of only same-site memory?

This probe stays narrow:

- one compact exact lattice family at `h = 0.25`
- one source-resolved Green control
- one same-site-memory baseline
- one transverse-smoothing candidate
- one reduction check: zero source must recover free propagation exactly
- one observable: detector support localization relative to same-site memory

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- same-site memory `mix = 0.9`
- transverse smoothing `mix = 0.25`

Reduction check:

- zero-source same-site shift: `+0.000000e+00`
- zero-source transverse shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | same-site deflection | transverse deflection | transverse/same | transverse - same |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.438000e-03` | `+1.873000e-03` | `+1.904000e-03` | `1.017` | `+3.100000e-05` |
| `0.0020` | `+2.878000e-03` | `+3.746000e-03` | `+3.808000e-03` | `1.017` | `+6.200000e-05` |
| `0.0040` | `+5.756000e-03` | `+7.492000e-03` | `+7.616000e-03` | `1.017` | `+1.240000e-04` |
| `0.0080` | `+1.151000e-02` | `+1.498000e-02` | `+1.523000e-02` | `1.017` | `+2.500000e-04` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- same-site memory `F~M`: `1.00`
- transverse `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the transverse-smoothed field keeps the weak-field `TOWARD` sign on the
  compact exact lattice
- the mass-scaling class stays essentially linear
- the transverse transport only nudges the detector centroid relative to the
  same-site memory control at the few-per-mille level

## Honest limitation

This is still a minimal pocket, not a full propagating field theory.

- the transverse step is one local smoothing update, not a full dynamical wave
  equation
- the source cluster is now interior, so this is a cleaner exact-lattice test
  than the boundary-clipped pocket
- the observable difference between same-site and transverse transport is
  small, so the result is best read as a controlled perturbation rather than a
  dramatic architectural shift

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- transverse transport is detectable, but only as a small correction to the
  same-site-memory control
- the generated-family bottleneck is therefore not fixed by this minimal step
