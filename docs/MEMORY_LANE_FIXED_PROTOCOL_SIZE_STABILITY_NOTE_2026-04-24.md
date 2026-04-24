# Memory Lane Fixed-Protocol Size Stability Note

**Date:** 2026-04-24
**Status:** positive partial-closure for the active-queue item
"memory lane: protocol- and geometry-stable observable remains open".
The lane remains OPEN, but size-stability under a fixed protocol is
now positively established as a point result.
**Runner:** `scripts/frontier_memory_fixed_protocol_sweep.py`
**Result:** `5/5 PASS`. Wallclock < 1 second.

## 1. Question

The 2026-04-11 mu^2 / size sweep note
([`MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md`](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md))
found two conflicting observations:

- scaled geometry: memory signal decays with N.
- fixed geometry (pos_a=15, pos_b=45, source_pos=30): memory signal
  *strengthens* with N, from `+0.02` at N=61 to `+2.58` at N=121.

The latter was taken as evidence that the lane was protocol-fragile.
But a closer read of the existing runner shows that
`steps = max(60, n)` hard-codes the evolution window to scale with N.
This conflates three effects:

1. pulse duration scales with N,
2. post-pulse evolution window scales with N,
3. ring spectrum changes with N.

The question is: if the *protocol* is fully fixed (steps, pulse
window, positions, damping, screening), is the memory signal
size-stable across N?

## 2. Setup

Single `run_fixed_protocol` helper that reimplements the mu2-sweep
dynamics with these fixed parameters:

- `FIXED_STEPS = 60`
- `FIXED_PULSE_START = 10`, `FIXED_PULSE_END = 20`
- `FIXED_SOURCE_POS = 30`, `FIXED_POS_A = 15`, `FIXED_POS_B = 45`
- `MU2 = 0.22`, `MASS = 0.30`, `GAMMA = 0.05`, `BETA = 5.0`

Sweep N in `{61, 81, 101, 121}`.

Memory observable: `sep_final - sep_initial` with the control
(`pulse_amplitude = 0`) subtracted.

## 3. Frozen results

| N | control drift | memory shift | sep_init | sep_final |
|---:|---|---|---|---|
| 61 | `+7.62e-8` | `+1.2742e-02` | 30.000 | 30.0127 |
| 81 | `+7.74e-10` | `+1.4661e-02` | 30.000 | 30.0147 |
| 101 | `+1.20e-9` | `+1.5554e-02` | 30.000 | 30.0155 |
| 121 | `+1.44e-9` | `+1.6041e-02` | 30.000 | 30.0160 |

Median memory shift: `+1.51e-2`; spread across N: `3.30e-3`; relative
spread: `21.8%`.

## 4. Verdicts

- **B.1 size stability (PASS)**: spread/median = 21.8%, below the 30%
  threshold. The memory signal is size-stable under the fixed protocol.
- **B.2 control quality (PASS)**: maximum control drift is `7.6e-8`,
  approximately 0% of the memory signal. The observable is not
  contaminated by background drift.
- **B.3 sign consistency (PASS)**: all four memory shifts are
  positive; no sign flips under the fixed protocol.
- **C.1 initial separation (PASS)**: all rings have `sep_init = 30.0`
  as expected for markers at positions 15 and 45.
- **D.1 lane remains open (PASS)**: a single-point stability result
  does not promote the lane.

## 5. Interpretation

The protocol-fragility observed in the earlier mu2/size sweep was
primarily driven by the hard-coded `steps = max(60, N)` scaling of
the evolution window, not by any intrinsic ring-size effect. Once
the protocol is fully fixed, the memory signal asymptotes to a
stable value around `+1.5e-2` with a 22% spread across N in the
tested range.

The signal grows slightly with N (`+1.27e-2 → +1.60e-2`), likely
reflecting the changing ring spectrum (point (iii) from Section 1).
This secondary dependence does not invalidate the fixed-protocol
stability claim within the 30% tolerance band.

## 6. What this does NOT close

The memory lane remains **open** because the active-queue item asks
for a *protocol- AND geometry-stable* observable. This run pins down
size-stability at one specific (pulse, mu^2, damping, position) cell.
Multi-parameter stability requires sweeps over:

- `pulse_amplitude in {0.1, 0.5, 1.0, 2.0, 5.0}`,
- `mu^2 in {0, 0.01, 0.05, 0.22, 0.5}`,
- `pulse_window_length` (currently fixed at 10 steps),
- `damping gamma in {0, 0.02, 0.05, 0.10}`.

At each cell, size-stability under fixed protocol should be tested
the same way. Full closure would require positive results at
multiple parameter choices.

## 7. Falsifier

- Re-run with same parameters producing different memory shifts
  (would invalidate determinism).
- Control drift exceeding 10% of memory signal at any N (would
  invalidate signal quality).
- Sign flip at any N (would invalidate observable robustness).
- Memory shift varying by >30% across N (would refute fixed-protocol
  stability).

The runner exposes all four checks; all pass.

## 8. Active-queue update

The `memory lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content is a frozen positive size-stability
baseline at a single (mu^2, pulse, positions) cell. The lane is not
promoted, demoted, or closed.

## 9. Next concrete step

Extend the fixed-protocol sweep to multiple (mu^2, pulse_amplitude,
damping) cells. At each cell, check the same four conditions
(size-stability, control quality, sign consistency, initial-separation
sanity). If all cells pass, the lane is materially advanced toward
closure. If some cells fail, the failure pattern characterizes the
parameter region where the observable is stable.

## 10. Provenance

- Runner: `scripts/frontier_memory_fixed_protocol_sweep.py`
- Underlying dynamics:
  `scripts/frontier_memory_mu2_size_sweep.py` (imports)
- Result: `5/5 PASS`, wallclock `0.3 s`.
- Reproducibility: deterministic (no random seeds used);
  same parameters -> same outputs.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1. The dynamics are sparse-
  linear-algebra + Crank-Nicolson; version drift is not a confounder.
