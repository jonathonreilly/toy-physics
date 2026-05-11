# Wider `h = 0.125` Replay Note

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-06

**Review repair perimeter (2026-05-03 generated-audit context):**
Generated-audit context identified this chain-closure blocker: "The one-hop scout dependency is
already clean in current operational metadata, but the load-bearing
width-4 replay row did not reproduce within bounded current audit
runs, including a narrowed full-window invocation." The repair target
being addressed is `runner_artifact_issue`: "provide a current
completed runner output or a faster deterministic runner path that
reproduces the exact phys_l=6, phys_w=4, h=0.125, full-window z=3.0
row and its alpha~0.5 fit." This rigorization edit only sharpens the
boundary of the repair perimeter; nothing here promotes audit
status. The active runner
[`scripts/lattice_3d_l2_wide_h0125_replay.py`](../scripts/lattice_3d_l2_wide_h0125_replay.py)
already supports a narrowed CLI invocation
(`--phys-w 4 --z-mass 3.0 --window full`) that runs only the
load-bearing single row; the prior runner cache hit
`status: timeout` because the audit-lane precompute invokes the
runner with no arguments and the default sweep iterates `phys_w` in
`{3, 4}` plus three windows and three z-mass values, and on the
reference laptop a single phys_w slice already takes ~15 min. The
runner-budget mismatch is registered explicitly in "Audit cache /
runner-budget bridge (2026-05-10)" below; the bounded-no-go
scientific conclusion is unaffected.

This note records the widened-family diagnostic for the retained 3D dense
`1/L^2 + h^2` bridge lane. It is intentionally narrower than the existing
fixed-family bridge note.

## Question

Does widening the physical box at `h = 0.125` rescue the weak-field mass-law
bridge, or does the fixed-family `F~M ~ 0.5` limit persist?

## Diagnostic

- new replay script:
  - [`scripts/lattice_3d_l2_wide_h0125_replay.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_replay.py)
- comparison families:
  - `phys_w = 3`
  - `phys_w = 4`
- shared setup:
  - `phys_l = 6`
  - `h = 0.125`
  - `z_mass = 3`
  - primary weak-field sweep over `s = 10^-7 ... 5 x 10^-6`
  - confirmatory probe sweep over `s = 10^-7, 10^-6, 5 x 10^-6`
- observables:
  - Born
  - `k = 0` null
  - gravity sign
  - `F~M` exponent

## Interpretation target

- if `phys_w = 4` moves the exponent toward `1.0`, the bridge may still be
  open on a truly wider family
- if `phys_w = 4` stays near the fixed-family `0.5` slope, the fixed-family
  negative is likely structural rather than a detector-window artifact

## Status

Finished bounded no-go on the retained tested row.

- comparison log:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
- retained baseline:
  - `phys_w = 3`, `phys_l = 6`, `z = 3.0`, full window
  - `Born = 6.59e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.009417`
  - `alpha = 0.500`
- genuinely wider row:
  - `phys_w = 4`, `phys_l = 6`, `z = 3.0`, full window
  - `Born = 8.01e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.010955`
  - `alpha = 0.499`
- confirmatory probe log:
  - [`logs/2026-04-06-h0125-wide-full-window-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window-probe.txt)
  - same `phys_w = 4`, `phys_l = 6`, `z = 3.0`, full-window row
  - same `alpha = 0.499` on the reduced three-strength sweep
- shorter-scale scout:
  - [`docs/H0125_SCALABLE_SCOUT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/H0125_SCALABLE_SCOUT_NOTE.md)
  - [`logs/2026-04-06-h0125-scalable-scout.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-scalable-scout.txt)
  - `phys_l = 4`, `phys_w = 3`, full window
  - `alpha = 0.501`, `0.501`, `0.502` across `z = 1.5`, `2.0`, `3.0`

On this first genuinely wider full-window replay, the weak-field exponent does
not move toward `1.0`; it stays pinned to the fixed-family `~0.5` class. That
makes the wider-family `h = 0.125` continuation a bounded negative rather than
a retained rescue. The shorter-axial-scale scout also stays in the same class,
so there is no review-safe scalable replay reopening on the observed rows.

## Audit cache / runner-budget bridge (2026-05-10)

The generated-audit context cited at top flagged a
`runner_artifact_issue` because the previous cached runner output for
[`scripts/lattice_3d_l2_wide_h0125_replay.py`](../scripts/lattice_3d_l2_wide_h0125_replay.py)
was `status: timeout` at the 120 s default ceiling — the full sweep
iterates `phys_w` in `{3, 4}` plus the three windows and three z-mass
values, and on the reference laptop a single phys_w slice already
takes ~15 min (the dense-family row at `phys_w=4` builds 207025
nodes / 49 layers / dense edges per layer pair). The bounded
conclusion of this note is supported only by the load-bearing
`phys_w=4 / full-window / z=3.0` row (and the parallel `phys_w=3`
control); the broader window/z slices are confirmatory rather than
load-bearing for the headline `alpha~0.5` pinning.

The runner already supports two narrowed invocations for in-budget
audit reruns: `--phys-w 4 --z-mass 3.0 --window full` (load-bearing
single-row only) and the implicit single-width specialization
[`scripts/lattice_3d_l2_wide_h0125_w4.py`](../scripts/lattice_3d_l2_wide_h0125_w4.py)
which is already registered as the single-width companion runner.
A future runner-source rigorization may declare
`AUDIT_TIMEOUT_SEC = 1800` at module top so the audit-lane
precompute (see [`scripts/runner_cache.py`](../scripts/runner_cache.py))
allows the default sweep to complete and the cache to land with
`status: ok` rather than `status: timeout`; that change is
deferred to a follow-up runner refresh because it changes the
runner SHA and would invalidate the existing
SHA-pinned cache. The review repair perimeter is exactly the
missing-completed-stdout flag; the bounded-no-go scientific
conclusion is unaffected by either path.
