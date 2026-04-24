#!/usr/bin/env python3
"""
Memory lane fixed-protocol size sweep.

Background.
  The active-queue item "memory lane: protocol- and geometry-stable
  observable remains open" is currently backed by two conflicting
  observations in `docs/MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md`:

    - scaled geometry: memory signal decays with N (positions scale, fewer
      wavepacket overlaps at larger ring).
    - fixed geometry (pos_a=15, pos_b=45, source_pos=30): memory signal
      *strengthens* with N (from +0.02 at N=61 to +2.58 at N=121).

  The existing mu^2 / size sweep runner hard-codes `steps = max(60, n)`,
  so the evolution window itself scales with N. That conflates three
  effects at larger N:

    (i) longer pulse, (ii) longer post-pulse window, (iii) different ring
    spectrum.

What this runner adds.
  Fix the protocol completely: `steps = 60` (constant), pulse window
  `[10, 20]` (constant), positions `(source=30, pos_a=15, pos_b=45)`
  (constant). Sweep only N in {61, 81, 101, 121}. Everything else is
  identical to the retained ring-memory dynamics
  (scripts/frontier_memory_mu2_size_sweep.py).

  Three claims:

    (B.1) fixed-protocol memory signal is size-stable: spread across
          N values < 30% of the median.
    (B.2) control (pulse_amplitude = 0) is approximately zero at every N,
          so the observable is not contaminated by background drift.
    (B.3) sign consistency: memory signal has the same sign across all N
          (no sign flips under the fixed protocol).

  If all three pass, the memory observable IS protocol-stable at fixed
  geometry and the open-queue item has a positive answer for this
  parameter choice.

What this runner does NOT close.
  A single protocol choice passing three checks is necessary but not
  sufficient to promote the memory lane. Multi-parameter stability
  (pulse amplitude, pulse window, damping) is the next step. The lane
  stays OPEN regardless of this run's verdict.

Falsifier.
  - Spread across N > 30% (would refute fixed-protocol stability).
  - Control drift > 10% of median signal (would refute signal quality).
  - Sign flip at any N (would refute observable robustness).
"""

from __future__ import annotations

import importlib.util
import sys
import time

import numpy as np
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve


def import_mu2_helpers():
    spec = importlib.util.spec_from_file_location(
        "mu2", "scripts/frontier_memory_mu2_size_sweep.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FIXED_STEPS = 60
FIXED_PULSE_START = 10
FIXED_PULSE_END = 20
FIXED_SOURCE_POS = 30
FIXED_POS_A = 15
FIXED_POS_B = 45
MU2 = 0.22


def run_fixed_protocol(mod, n: int, pulse_amplitude: float) -> dict:
    """Reimplements run_memory_sim with steps fixed at 60 and fixed pulse
    window, overriding the hard-coded `steps = max(60, n)` in the original.
    """
    par = mod.parity_vector(n)
    L = mod.build_ring_laplacian(n)
    field_op = -mod.C_SPEED ** 2 * (L + MU2 * speye(n, format="csr"))

    phi = np.zeros(n)
    pi_field = np.zeros(n)

    source_profile = np.zeros(n)
    source_profile[FIXED_SOURCE_POS] = 1.0

    psi_a = mod.make_wavepacket(FIXED_POS_A, n)
    psi_b = mod.make_wavepacket(FIXED_POS_B, n)

    sep_history = []
    for step in range(FIXED_STEPS):
        ca = mod.ring_centroid(psi_a, n)
        cb = mod.ring_centroid(psi_b, n)
        sep_history.append(mod.ring_distance(ca, cb, n))

        pulse_active = FIXED_PULSE_START <= step < FIXED_PULSE_END
        for _ in range(mod.N_FIELD_SUBSTEPS):
            source = (
                mod.BETA * pulse_amplitude * source_profile
                if pulse_active
                else np.zeros(n)
            )
            acc = field_op.dot(phi) - mod.GAMMA * pi_field + source
            pi_field += 0.5 * mod.DT_FIELD * acc
            phi += mod.DT_FIELD * pi_field
            acc = field_op.dot(phi) - mod.GAMMA * pi_field + source
            pi_field += 0.5 * mod.DT_FIELD * acc

        H = mod.build_ring_hamiltonian(n, phi, par)
        psi_a = mod.cn_step(H, psi_a, mod.DT_MATTER)
        psi_b = mod.cn_step(H, psi_b, mod.DT_MATTER)

    ca = mod.ring_centroid(psi_a, n)
    cb = mod.ring_centroid(psi_b, n)
    sep_history.append(mod.ring_distance(ca, cb, n))

    return {
        "steps": FIXED_STEPS,
        "sep_history": np.array(sep_history),
        "sep_initial": sep_history[0],
        "sep_final": float(sep_history[-1]),
        "memory_shift": float(sep_history[-1] - sep_history[0]),
    }


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def main() -> int:
    t0 = time.time()
    mod = import_mu2_helpers()

    N_VALUES = [61, 81, 101, 121]

    print("=" * 82)
    print("MEMORY LANE FIXED-PROTOCOL SIZE SWEEP")
    print("=" * 82)
    print(f"N_VALUES={N_VALUES}")
    print(f"steps={FIXED_STEPS}, pulse_window=[{FIXED_PULSE_START}, {FIXED_PULSE_END}]")
    print(f"source={FIXED_SOURCE_POS}, pos_a={FIXED_POS_A}, pos_b={FIXED_POS_B}")
    print(f"mu^2={MU2}")
    print()

    print(f"{'N':>5s}  {'ctrl':>12s}  {'memory_shift':>14s}  {'sep_init':>10s}  {'sep_final':>11s}")
    rows = []
    for n in N_VALUES:
        ctrl = run_fixed_protocol(mod, n, pulse_amplitude=0.0)
        live = run_fixed_protocol(mod, n, pulse_amplitude=1.0)
        memory = live["memory_shift"] - ctrl["memory_shift"]
        row = {
            "n": n,
            "ctrl_drift": ctrl["memory_shift"],
            "live_shift": live["memory_shift"],
            "memory": memory,
            "sep_init": live["sep_initial"],
            "sep_final": live["sep_final"],
        }
        rows.append(row)
        print(
            f"  {n:>3d}  {row['ctrl_drift']:+.4e}  {row['memory']:+.4e}  "
            f"{row['sep_init']:>10.6f}  {row['sep_final']:>11.6f}"
        )
    print()

    # B.1 size stability: spread / median < 30%
    memories = np.array([r["memory"] for r in rows])
    median = float(np.median(memories))
    spread = float(memories.max() - memories.min())
    rel_spread = spread / abs(median) if abs(median) > 0 else float("inf")
    record(
        "B.1 fixed-protocol memory signal is size-stable (spread/median < 30%)",
        rel_spread < 0.30,
        f"memories = {[f'{m:+.4e}' for m in memories]}\n"
        f"median = {median:+.4e}, spread = {spread:.4e}, "
        f"rel_spread = {rel_spread*100:.1f}%",
    )

    # B.2 control drift is small (< 10% of median signal)
    ctrl_drifts = np.array([r["ctrl_drift"] for r in rows])
    max_ctrl = float(np.max(np.abs(ctrl_drifts)))
    ctrl_ratio = max_ctrl / abs(median) if abs(median) > 0 else float("inf")
    record(
        "B.2 control (pulse=0) drift is small (< 10% of memory signal at any N)",
        ctrl_ratio < 0.10,
        f"max|ctrl_drift| = {max_ctrl:.4e}, memory median = {abs(median):.4e}\n"
        f"ratio = {ctrl_ratio*100:.1f}%",
    )

    # B.3 sign consistency
    signs = np.sign(memories)
    all_same_sign = (np.abs(np.sum(signs)) == len(signs)) and (signs[0] != 0)
    record(
        "B.3 memory signal has consistent sign across all N",
        all_same_sign,
        f"signs = {signs.tolist()}",
    )

    # Sanity: each run's sep_init should be approximately 30 (the initial
    # separation on a ring with markers at 15 and 45). Memory should be
    # small compared to sep_init.
    sep_inits = [r["sep_init"] for r in rows]
    record(
        "C.1 initial separation is ~30 on every ring (markers 15 / 45)",
        all(abs(s - 30) < 3.0 for s in sep_inits),
        f"sep_init values: {[f'{s:.3f}' for s in sep_inits]}",
    )

    # Honest open boundary
    record(
        "D.1 memory lane remains OPEN; single protocol choice does not close it",
        True,
        "A single-point size-stability PASS (at fixed mu^2, fixed pulse\n"
        "amplitude, fixed window, fixed damping) is necessary but not\n"
        "sufficient to promote the lane. Multi-parameter stability is the\n"
        "next step.",
    )

    # Summary
    print()
    print("=" * 82)
    print("SUMMARY")
    print("=" * 82)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}   wallclock: {time.time() - t0:.1f}s")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    # Load-bearing: B.1 + B.2 + B.3 + C.1 + D.1.
    load_bearing = all(ok for _, ok, _ in PASSES)

    print()
    if load_bearing:
        print("VERDICT (fixed-protocol memory is size-stable): under the fixed")
        print(f"protocol (steps={FIXED_STEPS}, pulse=[{FIXED_PULSE_START},{FIXED_PULSE_END}], "
              f"source={FIXED_SOURCE_POS},")
        print(f"pos_a={FIXED_POS_A}, pos_b={FIXED_POS_B}, mu^2={MU2}), the memory signal is")
        print("size-stable across N in {61, 81, 101, 121} with spread/median < 30%,")
        print("control drift < 10% of signal, and consistent sign. The memory lane")
        print("still remains OPEN; multi-parameter stability is the next step.")
    else:
        print("VERDICT: fixed-protocol size-stability failed on at least one check.")
        print("This characterizes the open-lane failure mode more sharply.")
    return 0 if load_bearing else 1


if __name__ == "__main__":
    sys.exit(main())
