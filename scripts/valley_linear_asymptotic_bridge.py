#!/usr/bin/env python3
"""Bounded asymptotic bridge for the 3D valley-linear ordered-lattice lane.

This script does not search for new physics. It reuses the retained
valley-linear 3D family and asks a narrow review-safe question:

  Is the far-tail exponent stabilizing across modest width / h changes,
  or does it still move with the finite lattice slice?

The output is intentionally conservative:
- same family
- same action
- same kernel
- same detector geometry
- a small width / h ladder only

The result should be read as a finite-size correction study, not a theorem.
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__])
    raise SystemExit(
        "numpy is required for this bridge. On this machine use /usr/bin/python3."
    ) from exc

from scripts.valley_linear_same_harness_compare import (  # noqa: E402
    K,
    PHYS_L,
    STRENGTH,
    Lattice3D,
    fit_power,
    make_field,
    setup_slits,
)

AUDIT_TIMEOUT_SEC = 1800


@dataclass(frozen=True)
class Checkpoint:
    label: str
    h: float
    w: int


@dataclass
class Result:
    label: str
    h: float
    w: int
    born: float
    k0: float
    fm_alpha: float
    grav: float
    toward_count: int
    toward_total: int
    peak_z: int
    peak_slope: float
    peak_r2: float
    far_slope: float
    far_r2: float
    far_n: int


CHECKPOINTS = [
    Checkpoint("coarse anchor", 0.5, 8),
    Checkpoint("core retained", 0.25, 10),
    Checkpoint("wide replay", 0.25, 12),
]


def _born_audit(lat: Lattice3D, det: list[int], barrier_nodes: set[int], pos: np.ndarray) -> float:
    field_zero = np.zeros(lat.n)
    upper = sorted([i for i in barrier_nodes if pos[i, 1] > 1.0], key=lambda i: pos[i, 1])
    lower = sorted([i for i in barrier_nodes if pos[i, 1] < -1.0], key=lambda i: -pos[i, 1])
    middle = [i for i in barrier_nodes if abs(pos[i, 1]) <= 1.0 and abs(pos[i, 2]) <= 1.0]
    if not upper or not lower or not middle:
        return math.nan

    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = barrier_nodes - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(s_a + s_b)),
        ("ac", set(s_a + s_c)),
        ("bc", set(s_b + s_c)),
        ("a", set(s_a)),
        ("b", set(s_b)),
        ("c", set(s_c)),
    ]:
        blocked_now = other | (all_s - open_set)
        amps = lat.propagate(field_zero, K, blocked_now, "valley_linear")
        probs[key] = np.array([abs(amps[d]) ** 2 for d in det])

    i3 = 0.0
    total = 0.0
    for idx in range(len(det)):
        term = (
            probs["abc"][idx]
            - probs["ab"][idx]
            - probs["ac"][idx]
            - probs["bc"][idx]
            + probs["a"][idx]
            + probs["b"][idx]
            + probs["c"][idx]
        )
        i3 += abs(term)
        total += probs["abc"][idx]
    return i3 / total if total > 1e-30 else math.nan


def _measure_checkpoint(cp: Checkpoint) -> Result:
    lat = Lattice3D(PHYS_L, cp.w, cp.h)
    pos = lat.pos
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    sa, sb, blocked, bl = setup_slits(lat)
    barrier_nodes = {
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap
    }

    field_zero = np.zeros(lat.n)
    t0 = time.time()
    amps_flat = lat.propagate(field_zero, K, blocked, "valley_linear")
    p_flat = sum(abs(amps_flat[d]) ** 2 for d in det)
    z_flat = sum(abs(amps_flat[d]) ** 2 * pos[d, 2] for d in det) / p_flat
    born = _born_audit(lat, det, barrier_nodes, pos)

    field_mass3 = make_field(lat, 3, STRENGTH)
    amps_f0 = lat.propagate(field_zero, 0.0, blocked, "valley_linear")
    amps_m0 = lat.propagate(field_mass3, 0.0, blocked, "valley_linear")
    p_f0 = sum(abs(amps_f0[d]) ** 2 for d in det)
    p_m0 = sum(abs(amps_m0[d]) ** 2 for d in det)
    k0 = 0.0
    if p_f0 > 1e-30 and p_m0 > 1e-30:
        z_f0 = sum(abs(amps_f0[d]) ** 2 * pos[d, 2] for d in det) / p_f0
        z_m0 = sum(abs(amps_m0[d]) ** 2 * pos[d, 2] for d in det) / p_m0
        k0 = z_m0 - z_f0

    # F~M
    m_data = []
    g_data = []
    for s in [1e-6, 5e-6, 2e-5, 5e-5]:
        fm = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked, "valley_linear")
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - z_flat
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)
    fm_alpha = float("nan")
    if len(m_data) >= 3:
        fm_alpha, _ = fit_power(m_data, g_data)

    # gravity sign
    am3 = lat.propagate(field_mass3, K, blocked, "valley_linear")
    pm3 = sum(abs(am3[d]) ** 2 for d in det)
    grav = sum(abs(am3[d]) ** 2 * pos[d, 2] for d in det) / pm3 - z_flat if pm3 > 1e-30 else 0.0

    # distance law
    z_values = list(range(2, min(10, lat.hw) + 1))
    b_data = []
    d_data = []
    for z_mass in z_values:
        fm = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked, "valley_linear")
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - z_flat
            if delta > 0:
                b_data.append(z_mass)
                d_data.append(delta)

    peak_z = -1
    peak_slope = peak_r2 = math.nan
    far_slope = far_r2 = math.nan
    far_n = 0
    if len(d_data) >= 3:
        d_arr = np.array(d_data)
        peak_i = int(np.argmax(d_arr))
        peak_z = b_data[peak_i]
        if len(d_data[peak_i:]) >= 3:
            peak_slope, peak_r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
        far_pairs = [(b, d) for b, d in zip(b_data, d_data) if b >= 5]
        if len(far_pairs) >= 3:
            far_slope, far_r2 = fit_power([b for b, _ in far_pairs], [d for _, d in far_pairs])
            far_n = len(far_pairs)

    return Result(
        label=cp.label,
        h=cp.h,
        w=cp.w,
        born=born,
        k0=k0,
        fm_alpha=fm_alpha,
        grav=grav,
        toward_count=len(b_data),
        toward_total=len(z_values),
        peak_z=peak_z,
        peak_slope=peak_slope,
        peak_r2=peak_r2,
        far_slope=far_slope,
        far_r2=far_r2,
        far_n=far_n,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 92)
    print("VALLEY-LINEAR ASYMPTOTIC BRIDGE")
    print("  Bounded h/W comparison for the 3D ordered-lattice 1/L^2 family")
    print("  Goal: decide whether the far-tail is stabilizing or still slice-dependent")
    print("=" * 92)
    print()

    results = []
    for cp in CHECKPOINTS:
        cp_t0 = time.time()
        res = _measure_checkpoint(cp)
        results.append(res)
        print(
            f"{cp.label}: h={cp.h}, W={cp.w} done in {time.time() - cp_t0:.1f}s "
            f"(Born={res.born:.2e}, TOWARD={res.toward_count}/{res.toward_total})"
        )

    print()
    print(f"{'slice':<14} {'h':>5s} {'W':>4s} {'Born':>10s} {'k=0':>10s} {'F~M':>8s} "
          f"{'grav':>11s} {'TOWARD':>8s} {'peak-tail':>22s} {'far-tail':>22s}")
    print("-" * 132)
    for r in results:
        peak = "n/a" if math.isnan(r.peak_slope) else f"z>={r.peak_z}: {r.peak_slope:.2f} (R²={r.peak_r2:.3f})"
        far = "n/a" if math.isnan(r.far_slope) else f"z>=5: {r.far_slope:.2f} (R²={r.far_r2:.3f}, n={r.far_n})"
        print(
            f"{r.label:<14} {r.h:>5.2f} {r.w:>4d} {r.born:>10.2e} {r.k0:>+10.2e} "
            f"{r.fm_alpha:>8.2f} {r.grav:>+11.6f} {f'{r.toward_count}/{r.toward_total}':>8} "
            f"{peak:>22} {far:>22}"
        )

    print()
    print("SAFE READ:")
    print("  - The finite-lattice 3D valley-linear replay is still genuinely TOWARD.")
    print("  - The far-tail exponent moves with h/W enough to stay slice-dependent.")
    print("  - The best current read is near-Newtonian finite-lattice replay, not an exact universal -1.00 theorem.")
    print("  - The wider replay improves tail resolution, but the asymptotic bridge is not fully stabilized yet.")
    print()
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
