#!/usr/bin/env python3
"""Bounded edge-deletion boundary sweep on the retained 3D valley-linear family.

This is the follow-up to the graph-requirements harness and the edge-deletion
boundary note.

Question:
  Around the transition between roughly 90% and 80% retained connectivity,
  how stable is the gravity sign across seeds?

The sweep keeps the family fixed and only varies:
  - keep fraction
  - seed

The output is intentionally narrow:
  - TOWARD fraction across seeds
  - mean gravity delta
  - optional representative controls if they are cheap

This is a boundary probe, not a universal graph theorem.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.inverse_problem_graph_requirements import (  # noqa: E402
    GraphLattice3D,
    H,
    MASS_Z,
    MAX_D_PHYS,
    PHYS_L,
    PHYS_W,
    STRENGTH,
    K,
    born_ratio,
    make_field,
)


KEEP_FRACTIONS = (1.00, 0.95, 0.90, 0.85, 0.80, 0.75)
SEEDS = tuple(20260404 + i for i in range(12))
CONTROL_SEED = SEEDS[0]
DELTA_EPS = 1e-12


@dataclass(frozen=True)
class Result:
    keep_fraction: float
    toward_count: int
    total: int
    mean_delta: float
    std_delta: float


def gravity_delta(lat: GraphLattice3D, field: np.ndarray, k: float) -> float:
    det = lat.detector_indices()
    _, _, _, blocked = _slits(lat)
    free = lat.propagate(np.zeros(lat.n, dtype=float), k, blocked)
    grav = lat.propagate(field, k, blocked)
    z_free = _centroid_z(free, det, lat.pos)
    z_grav = _centroid_z(grav, det, lat.pos)
    if not (np.isfinite(z_free) and np.isfinite(z_grav)):
        return float("nan")
    return z_grav - z_free


def _slits(lat: GraphLattice3D) -> tuple[list[int], list[int], list[int], set[int]]:
    barrier = lat.barrier_indices()
    upper = [i for i in barrier if lat.grid_pos[i, 1] > 1]
    lower = [i for i in barrier if lat.grid_pos[i, 1] < -1]
    middle = [i for i in barrier if abs(lat.grid_pos[i, 1]) <= 1 and abs(lat.grid_pos[i, 2]) <= 1]
    blocked = set(barrier) - set(upper + lower + middle)
    return upper, lower, middle, blocked


def _centroid_z(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return float("nan")
    return float(np.dot(probs, pos[det, 2]) / total)


def measure_fraction(keep_fraction: float, seed: int) -> float:
    edge_delete_prob = max(0.0, 1.0 - keep_fraction)
    lat = GraphLattice3D(
        PHYS_L,
        PHYS_W,
        H,
        MAX_D_PHYS,
        edge_delete_prob=edge_delete_prob,
        seed=seed,
    )
    field = make_field(lat, MASS_Z, STRENGTH)
    return gravity_delta(lat, field, K)


def representative_controls() -> dict[str, float]:
    # Cheap representative checks on the 100% and 80% cases using one seed.
    controls: dict[str, float] = {}
    for keep_fraction, label in ((1.00, "100%"), (0.80, "80%")):
        edge_delete_prob = max(0.0, 1.0 - keep_fraction)
        lat = GraphLattice3D(
            PHYS_L,
            PHYS_W,
            H,
            MAX_D_PHYS,
            edge_delete_prob=edge_delete_prob,
            seed=CONTROL_SEED,
        )
        controls[f"{label}_born"] = born_ratio(lat)
        field = make_field(lat, MASS_Z, STRENGTH)
        controls[f"{label}_k0"] = gravity_delta(lat, field, 0.0)
        controls[f"{label}_nofield"] = gravity_delta(lat, np.zeros(lat.n, dtype=float), K)
    return controls


def summarize(keep_fraction: float, values: list[float]) -> Result:
    arr = np.array(values, dtype=float)
    toward = int(np.sum(arr > DELTA_EPS))
    return Result(
        keep_fraction=keep_fraction,
        toward_count=toward,
        total=len(values),
        mean_delta=float(np.mean(arr)),
        std_delta=float(np.std(arr, ddof=0)) if len(values) > 1 else 0.0,
    )


def main() -> None:
    print("=" * 100)
    print("EDGE DELETION BOUNDARY SWEEP")
    print("  Retained 3D valley-linear family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={MAX_D_PHYS}")
    print(f"  keep fractions: {', '.join(f'{k:.2f}' for k in KEEP_FRACTIONS)}")
    print(f"  seeds: {len(SEEDS)} ({SEEDS[0]}..{SEEDS[-1]})")
    print("  Goal: harden the 80%-90% retention transition on the same family")
    print("=" * 100)
    print()

    rows: list[Result] = []
    for keep_fraction in KEEP_FRACTIONS:
        deltas = [measure_fraction(keep_fraction, seed) for seed in SEEDS]
        rows.append(summarize(keep_fraction, deltas))

    print(f"{'keep':>6s} {'TOWARD':>12s} {'mean_delta':>14s} {'std_delta':>12s}")
    print("-" * 54)
    for row in rows:
        print(
            f"{row.keep_fraction:>6.2f} "
            f"{row.toward_count:>2d}/{row.total:<9d} "
            f"{row.mean_delta:+14.6e} "
            f"{row.std_delta:>12.6e}"
        )

    controls = representative_controls()
    print()
    print("REPRESENTATIVE CONTROLS (seed=first seed)")
    print(f"  100%  Born={controls['100%_born']:.2e}  k=0={controls['100%_k0']:+.3e}  no-field={controls['100%_nofield']:+.3e}")
    print(f"  80%   Born={controls['80%_born']:.2e}  k=0={controls['80%_k0']:+.3e}  no-field={controls['80%_nofield']:+.3e}")

    print()
    print("SAFE READ")
    best = max(rows, key=lambda r: r.keep_fraction)
    worst = min(rows, key=lambda r: r.keep_fraction)
    print("  - Use the keep-fraction rows to locate the transition region, not as a universal theorem.")
    print("  - If 90% stays mostly TOWARD and 80% becomes coin-flip or AWAY-dominated, the boundary is real.")
    print("  - If the transition wanders seed-to-seed, the graph boundary is forgiving but not precise.")
    print("  - The representative controls are only sanity checks; the sweep rows are the main result.")
    print(f"  - endpoints: best={best.keep_fraction:.2f}, worst={worst.keep_fraction:.2f}")


if __name__ == "__main__":
    main()
