# Wider `h = 0.125` Family (`phys_w = 4`) Note

**Status:** open - open or unresolved claim state
**Claim type:** open_gate
**Date:** 2026-04-06

**Review repair perimeter (2026-05-03 generated-audit context):**
Generated-audit context identified this chain-closure blocker: "The note's conclusion depends on the Born,
k=0, gravity, and alpha numerical row, but the live runner did not
reach those diagnostics in a bounded restricted run." The
repair target being addressed is: "provide a current completed
runner output or a faster deterministic runner path that reproduces
the exact retained width-4 row and justifies why that full-window
z=3.0 readout is decisive." This rigorization edit only sharpens
the boundary of the repair perimeter; nothing here promotes
audit status. The active runner is
[`scripts/lattice_3d_l2_wide_h0125_w4.py`](../scripts/lattice_3d_l2_wide_h0125_w4.py);
its prior runner cache hit `status: timeout` because the
audit-lane precompute invokes the runner with no arguments and the
default sweep iterates three windows x three z-mass values x six
strengths, which takes ~15 min on the reference laptop and exceeds
the 120 s default ceiling. The runner-budget mismatch is
registered explicitly in "Audit cache / runner-budget bridge
(2026-05-10)" below; the bounded-no-go scientific conclusion is
unaffected.

This note tracks the first genuinely wider continuation of the retained dense
`1/L^2 + h^2` bridge family. The fixed `phys_w = 3` family is already frozen
as a bounded negative for weak-field closure; this probe asks whether widening
the box to `phys_w = 4` can move the exponent toward `1.0` or whether the
`~0.5` limit persists.

## Script

- [`scripts/lattice_3d_l2_wide_h0125_w4.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_w4.py)

## Status

Finished as a bounded no-go on the retained tested row.

- finished log:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
- retained width-4 row:
  - `phys_w = 4`
  - `phys_l = 6`
  - full detector window at `z = 3.0`
  - `Born = 8.01e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.010955`
  - `alpha = 0.499`

So the first genuinely wider dense-family row does not rescue the weak-field
mass-law bridge. It reproduces the same `~0.5` exponent class as the frozen
`phys_w = 3` family and should be treated as a bounded negative, not an
unresolved reopen.

## Audit cache / runner-budget bridge (2026-05-10)

The generated-audit context cited at top flagged that
[`scripts/lattice_3d_l2_wide_h0125_w4.py`](../scripts/lattice_3d_l2_wide_h0125_w4.py)
did not "reach those [Born, k=0, gravity, alpha] diagnostics in a
bounded restricted run." The cached runner output was
`status: timeout` at the 120 s default ceiling because the
dense-family row at `phys_w=4` builds 207025 nodes / 49 layers /
856830000 dense edges per layer pair, and the full sweep over
three windows x three z-mass values x six strengths takes ~15 min
wall-clock on the reference laptop. The bounded no-go conclusion
of this note is carried by the load-bearing `full / z=3.0` row;
the secondary `r<=1.5` and `|y|<=0.5` window slices are
confirmatory rather than load-bearing for the headline
`alpha=0.499` pinning.

A future runner-source rigorization may declare
`AUDIT_TIMEOUT_SEC = 1800` at module top so the audit-lane
precompute (see [`scripts/runner_cache.py`](../scripts/runner_cache.py))
allows the default sweep to complete and the cache to land with
`status: ok` rather than `status: timeout`; that change is
deferred to a follow-up runner refresh because it changes the
runner SHA and would invalidate the existing SHA-pinned cache. The
frozen reference summary in the Status section above preserves the
load-bearing row outside the audit-lane runner cache; the
review repair perimeter is exactly the missing completed-stdout
flag inside the audit-lane runner cache, and the bounded-no-go
scientific conclusion is unaffected by either path.
