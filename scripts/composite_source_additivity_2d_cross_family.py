#!/usr/bin/env python3
"""Bounded second-family additivity probe on the retained 2D ordered lattice.

This is the smallest cross-family check for the new valley-linear additivity
story. It reuses the existing 2D ordered-lattice geometry from the continuum
distance lane and asks whether the same weak-field source-additivity story
survives beyond the fixed 3D ordered family.

The probe is intentionally narrow:

- same-site source-strength additivity
- disjoint-source field additivity
- same two actions: valley-linear vs spent-delay

It is a test-particle response probe only. It does not derive persistent-pattern
inertial mass.
"""

from __future__ import annotations

import math
import os
import sys

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    )

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.lattice_2d_continuum_distance import BETA, K, generate


H = 0.5
PHYS_L = 40
PHYS_W = 20
MAX_D_PHYS = 5
SOURCE_Y = 5.0
PAIR_STRENGTHS = [(1e-5, 2e-5), (1e-5, 5e-5), (2e-5, 5e-5)]
DISJOINT_Y_PAIRS = [((3.0, 7.0), 2e-5), ((4.0, 9.0), 2e-5)]
ACTIONS = ("valley_linear", "spent_delay")


def detector(nl: int, hw: int, nmap: dict[tuple[int, int], int]) -> list[int]:
    return [
        nmap[(nl - 1, iy)]
        for iy in range(-hw, hw + 1)
        if (nl - 1, iy) in nmap
    ]


def centroid(amps: np.ndarray, det: list[int], pos: list[tuple[float, float]]) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, np.array([pos[d][1] for d in det], dtype=float)) / total)


def propagate(
    pos: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: np.ndarray,
    k: float,
    blocked: set[int],
    n: int,
    action_mode: str,
) -> np.ndarray:
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = np.zeros(n, dtype=np.complex128)
    src = next(i for i, p in enumerate(pos) if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action_mode == "spent_delay":
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
            elif action_mode == "valley_linear":
                act = L * (1 - lf)
            else:  # pragma: no cover - internal guard
                raise ValueError(f"unknown action_mode={action_mode}")
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * np.exp(1j * k * act) * w / L
    return amps


def rel_err(lhs: float, rhs: float) -> float:
    denom = max(abs(lhs), abs(rhs), 1e-30)
    return abs(lhs - rhs) / denom


def make_field(pos, nmap, nl, h, z_phys, strength):
    gl = 2 * nl // 3
    iy = round(z_phys / h)
    mi = nmap.get((gl, iy))
    if mi is None:
        return np.zeros(len(pos)), None
    mx, my = pos[mi]
    field = np.zeros(len(pos), dtype=float)
    for i, (x, y) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2) + 0.1
        field[i] = strength / r
    return field, mi


def main() -> None:
    pos, adj, nl, hw, nmap = generate(PHYS_L, PHYS_W, MAX_D_PHYS, H)
    n = len(pos)
    det = detector(nl, hw, nmap)

    print("=" * 88)
    print("COMPOSITE-SOURCE ADDITIVITY CROSS-FAMILY PROBE")
    print("  2D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_y={SOURCE_Y}")
    print("  Goal: bound whether the valley-linear additivity story survives beyond the fixed 3D family")
    print("=" * 88)

    for action in ACTIONS:
        print(f"\nACTION: {action}")
        print("  Same-site strength additivity:")
        print(f"    {'s1':>8s} {'s2':>8s} {'delta(s1+s2)':>14s} {'delta1+delta2':>14s} {'rel_err':>10s}")
        af = propagate(pos, adj, np.zeros(n), K, set(), n, action)
        for s1, s2 in PAIR_STRENGTHS:
            f1, _ = make_field(pos, nmap, nl, H, SOURCE_Y, s1)
            f2, _ = make_field(pos, nmap, nl, H, SOURCE_Y, s2)
            f12, _ = make_field(pos, nmap, nl, H, SOURCE_Y, s1 + s2)
            a1 = propagate(pos, adj, f1, K, set(), n, action)
            a2 = propagate(pos, adj, f2, K, set(), n, action)
            a12 = propagate(pos, adj, f12, K, set(), n, action)
            d1 = centroid(a1, det, pos) - centroid(af, det, pos)
            d2 = centroid(a2, det, pos) - centroid(af, det, pos)
            d12 = centroid(a12, det, pos) - centroid(af, det, pos)
            err = rel_err(d12, d1 + d2)
            print(f"    {s1:8.0e} {s2:8.0e} {d12:+14.8e} {d1 + d2:+14.8e} {err:10.2%}")

        print("  Disjoint-source field additivity:")
        print(f"    {'yA,yB':>12s} {'s':>8s} {'delta(A+B)':>14s} {'deltaA+deltaB':>14s} {'rel_err':>10s}")
        for (y_a, y_b), s in DISJOINT_Y_PAIRS:
            f_a, _ = make_field(pos, nmap, nl, H, y_a, s)
            f_b, _ = make_field(pos, nmap, nl, H, y_b, s)
            a_a = propagate(pos, adj, f_a, K, set(), n, action)
            a_b = propagate(pos, adj, f_b, K, set(), n, action)
            a_ab = propagate(pos, adj, f_a + f_b, K, set(), n, action)
            d_a = centroid(a_a, det, pos) - centroid(af, det, pos)
            d_b = centroid(a_b, det, pos) - centroid(af, det, pos)
            d_ab = centroid(a_ab, det, pos) - centroid(af, det, pos)
            err = rel_err(d_ab, d_a + d_b)
            print(f"    ({y_a:.0f},{y_b:.0f}) {s:8.0e} {d_ab:+14.8e} {d_a + d_b:+14.8e} {err:10.2%}")

    print("\nSAFE READ")
    print("  - This is a second-family cross-check on the retained 2D ordered lattice.")
    print("  - Valley-linear should remain additive on this weak-field test-particle family if the lane generalizes.")
    print("  - Spent-delay is expected to deviate because the action is nonlinear in the field.")
    print("  - Even if valley-linear is additive here, that still only supports a test-particle response law,")
    print("    not a persistent-pattern inertial-mass theorem.")


if __name__ == "__main__":
    main()
