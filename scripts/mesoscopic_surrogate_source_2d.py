#!/usr/bin/env python3
"""2D mesoscopic-surrogate source companion check.

Question:
  If a broad relaunch surrogate is treated as a distributed source on the
  retained 2D ordered-lattice family, does it behave like a soft point source
  or does the distributed support materially change the downstream response?

This is intentionally narrow:
  - 2D ordered lattice only
  - one broad surrogate family extracted from the free packet profile
  - compare against an equivalent-strength point source at the same centroid
  - compare the downstream test-particle response on the detector layer

Safe interpretation:
  - if the broad surrogate and point source agree closely, the surrogate is a
    usable soft-source control
  - if agreement requires a very broad support or fails at compression, the
    surrogate remains mesoscopic and not mass-like
"""

from __future__ import annotations

import math
import os
import sys
import time
import cmath

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

from scripts.lattice_2d_continuum_distance import BETA, K, generate


H = 0.5
PHYS_L = 20
PHYS_W = 12
MAX_D_PHYS = 5
SOURCE_Y = 5.0
PACKET_SIGMA = 1.25
PROBE_Y = 5.0
TOPN_VALUES = (9, 25, 49, 81, 121, 169, 196)
FIELD_STRENGTHS = (2e-5, 5e-5, 1e-4)


def detector(nl: int, hw: int, nmap: dict[tuple[int, int], int]) -> list[int]:
    return [
        nmap[(nl - 1, iy)]
        for iy in range(-hw, hw + 1)
        if (nl - 1, iy) in nmap
    ]


def gaussian_packet(hw: int, h: float, sigma: float = PACKET_SIGMA) -> dict[int, float]:
    weights: dict[int, float] = {}
    for iy in range(-hw, hw + 1):
        y = iy * h
        weights[iy] = math.exp(-0.5 * (y * y) / (sigma * sigma))
    norm = math.sqrt(sum(w * w for w in weights.values()))
    return {iy: w / norm for iy, w in weights.items()} if norm > 1e-30 else weights


def source_packet(n: int, nmap: dict[tuple[int, int], int], weights: dict[int, float]) -> np.ndarray:
    init = np.zeros(n, dtype=np.complex128)
    norm = math.sqrt(sum(w * w for w in weights.values()))
    if norm <= 0:
        return init
    for iy, w in weights.items():
        init[nmap[(0, iy)]] = w / norm
    return init


def point_packet(n: int, nmap: dict[tuple[int, int], int], y_phys: float) -> np.ndarray:
    init = np.zeros(n, dtype=np.complex128)
    iy = round(y_phys / H)
    init[nmap[(0, iy)]] = 1.0
    return init


def y_profile(amps: np.ndarray, det: list[int], pos: list[tuple[float, float]], h: float) -> dict[int, float]:
    profile: dict[int, float] = {}
    for d in det:
        iy = int(round(pos[d][1] / h))
        profile[iy] = profile.get(iy, 0.0) + float(abs(amps[d]) ** 2)
    total = sum(profile.values())
    if total > 0:
        profile = {k: v / total for k, v in profile.items()}
    return dict(sorted(profile.items()))


def profile_centroid(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total <= 0:
        return 0.0
    return sum((iy * h) * p for iy, p in profile.items()) / total


def profile_spread(profile: dict[int, float], h: float) -> float:
    total = sum(profile.values())
    if total <= 0:
        return 0.0
    mu = profile_centroid(profile, h)
    return math.sqrt(sum((((iy * h) - mu) ** 2) * p for iy, p in profile.items()) / total)


def topn_compress(profile: dict[int, float], n: int) -> tuple[dict[int, float], float]:
    if not profile:
        return {}, 0.0
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    selected = items[: min(n, len(items))]
    capture = sum(p for _, p in selected)
    total = sum(p for _, p in selected)
    if total <= 0:
        return {}, 0.0
    return {iy: p / total for iy, p in selected}, capture


def point_source_field(
    pos: list[tuple[float, float]],
    nmap: dict[tuple[int, int], int],
    nl: int,
    h: float,
    y_phys: float,
    strength: float,
) -> np.ndarray:
    gl = 2 * nl // 3
    iy = round(y_phys / h)
    mi = nmap.get((gl, iy))
    if mi is None:
        return np.zeros(len(pos), dtype=float)
    mx, my = pos[mi]
    field = np.zeros(len(pos), dtype=float)
    for i, (x, y) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2) + 0.1
        field[i] = strength / r
    return field


def distributed_source_field(
    pos: list[tuple[float, float]],
    nmap: dict[tuple[int, int], int],
    nl: int,
    h: float,
    profile: dict[int, float],
    strength: float,
) -> np.ndarray:
    gl = 2 * nl // 3
    field = np.zeros(len(pos), dtype=float)
    for iy, p in profile.items():
        mi = nmap.get((gl, iy))
        if mi is None:
            continue
        mx, my = pos[mi]
        for i, (x, y) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2) + 0.1
            field[i] += strength * p / r
    return field


def propagate_packet(
    pos: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: np.ndarray,
    init: np.ndarray,
    blocked: set[int],
    n: int,
) -> np.ndarray:
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = np.zeros(n, dtype=np.complex128)
    amps[: len(init)] = init
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        x1, y1 = pos[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1 - lf)
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
    return amps


def main() -> None:
    t_total = time.time()
    pos, adj, nl, hw, nmap = generate(PHYS_L, PHYS_W, MAX_D_PHYS, H)
    n = len(pos)
    det = detector(nl, hw, nmap)

    bl = nl // 3
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    slit_iy = max(1, round(3.0 / H))
    sa = [nmap[(bl, iy)] for iy in range(slit_iy, hw + 1) if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in range(-hw, -slit_iy + 1) if (bl, iy) in nmap]
    blocked = set(bi) - set(sa + sb)

    probe_init = point_packet(n, nmap, PROBE_Y)
    free_amps = propagate_packet(pos, adj, np.zeros(n, dtype=float), probe_init, blocked, n)
    free_profile = y_profile(np.array(free_amps, dtype=np.complex128), det, pos, H)

    print("=" * 92)
    print("MESOSCOPIC SURROGATE SOURCE COMPANION (2D)")
    print("  Retained 2D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_y={SOURCE_Y}, max_d={round(MAX_D_PHYS / H)}")
    print("  Goal: ask whether a broad relaunch surrogate behaves like a soft point")
    print("        source for a stable test-particle response.")
    print("=" * 92)
    print()
    print(f"Free-profile centroid: {profile_centroid(free_profile, H):+.4f}")
    print(f"Free-profile spread:   {profile_spread(free_profile, H):.4f}")
    print(f"Probe launch y:        {PROBE_Y:+.4f}")
    print()

    # Use the free packet profile itself as the mesoscopic source surrogate.
    # Then compare its field against an equivalent-strength point source at the
    # same centroid.
    print(f"{'topN':>6s} {'capture':>8s} {'src_mu':>8s} {'src_sig':>8s} {'d_dist':>10s} {'d_point':>10s} {'ratio':>8s} {'spread×':>8s} {'TV':>8s}")
    print("-" * 74)

    for topn in TOPN_VALUES:
        surrogate, capture = topn_compress(free_profile, topn)
        mu = profile_centroid(surrogate, H)
        sig = profile_spread(surrogate, H)
        centroid_y = round(mu / H)

        for strength in FIELD_STRENGTHS:
            distrib_field = distributed_source_field(pos, nmap, nl, H, surrogate, strength)
            point_field = point_source_field(pos, nmap, nl, H, mu, strength)

            # Field-response comparison for the same test packet and same source strength.
            # We compare distributed-source response to point-source response.
            dist_amps = propagate_packet(pos, adj, distrib_field, probe_init, blocked, n)
            point_amps = propagate_packet(pos, adj, point_field, probe_init, blocked, n)

            free_cent = profile_centroid(free_profile, H)
            dist_prof = y_profile(np.array(dist_amps, dtype=np.complex128), det, pos, H)
            point_prof = y_profile(np.array(point_amps, dtype=np.complex128), det, pos, H)

            dist_cent = profile_centroid(dist_prof, H)
            point_cent = profile_centroid(point_prof, H)
            dist_spread = profile_spread(dist_prof, H)
            point_spread = profile_spread(point_prof, H)
            tv = 0.5 * sum(abs(dist_prof.get(k, 0.0) - point_prof.get(k, 0.0)) for k in set(dist_prof) | set(point_prof))
            delta_dist = dist_cent - free_cent
            delta_point = point_cent - free_cent
            ratio = delta_dist / delta_point if abs(delta_point) > 1e-30 else 0.0

            print(
                f"{topn:6d} {capture:8.3f} {mu:+8.3f} {sig:8.3f}"
                f" {delta_dist:+10.6f} {delta_point:+10.6f}"
                f" {ratio:8.3f} {dist_spread / max(point_spread, 1e-30):8.3f}"
                f" {tv:8.3f}"
            )

    print()
    print("SAFE READ")
    print("  - If the distributed surrogate and point source stay close, the surrogate")
    print("    acts like a soft source.")
    print("  - If agreement only appears for broad support, the surrogate remains mesoscopic.")
    print("  - This is a companion check, not a persistent-mass theorem.")
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    main()
