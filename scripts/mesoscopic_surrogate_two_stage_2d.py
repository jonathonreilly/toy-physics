#!/usr/bin/env python3
"""2D two-stage mesoscopic-surrogate response companion.

Question:
  Can a broad surrogate survive *two* sourced-response stages on the retained
  2D ordered-lattice family without collapsing into an ordinary broad packet?

This is intentionally cheap and bounded:
  - retained 2D family only
  - one free probe packet
  - stage-1 surrogate source from the free profile
  - stage-2 surrogate source from the stage-1 response profile
  - compare against equivalent-strength point-source controls at each stage

Safe interpretation:
  - if stage-2 remains close to stage-1 and the broad surrogate keeps a
    stable response relative to the point-source control, that is a real
    mesoscopic control result
  - if stage-2 collapses or the response drifts badly, the surrogate source
    is only a one-hop control and not a deeper object
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
PROBE_Y = 5.0
PACKET_SIGMA = 1.25
TOPN_VALUES = (9, 25, 49, 81, 121, 169, 196)
FIELD_STRENGTH = 5e-5
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


def overlap(a: dict[int, float], b: dict[int, float]) -> float:
    keys = set(a) | set(b)
    return sum(math.sqrt(a.get(k, 0.0) * b.get(k, 0.0)) for k in keys)


def rel_err(lhs: float, rhs: float) -> float:
    denom = max(abs(lhs), abs(rhs), 1e-30)
    return abs(lhs - rhs) / denom


def stage_metrics(
    pos: list[tuple[float, float]],
    adj: dict[int, list[int]],
    n: int,
    nl: int,
    nmap: dict[tuple[int, int], int],
    det: list[int],
    blocked: set[int],
    baseline_profile: dict[int, float],
    source_profile: dict[int, float],
    probe_init: np.ndarray,
    strength: float,
):
    source_centroid = profile_centroid(source_profile, H)
    # Build the two fields at the source centroid.
    distributed_field = distributed_source_field(pos, nmap, nl, H, source_profile, strength)
    point_field = point_source_field(pos, nmap, nl, H, source_centroid, strength)

    dist_amps = propagate_packet(pos, adj, distributed_field, probe_init, blocked, n)
    point_amps = propagate_packet(pos, adj, point_field, probe_init, blocked, n)

    dist_prof = y_profile(dist_amps, det, pos, H)
    point_prof = y_profile(point_amps, det, pos, H)

    free_cent = profile_centroid(baseline_profile, H)
    dist_cent = profile_centroid(dist_prof, H)
    point_cent = profile_centroid(point_prof, H)

    dist_spread = profile_spread(dist_prof, H)
    point_spread = profile_spread(point_prof, H)

    delta_dist = dist_cent - free_cent
    delta_point = point_cent - free_cent
    ratio = delta_dist / delta_point if abs(delta_point) > 1e-30 else 0.0

    return {
        "source_centroid": source_centroid,
        "dist_profile": dist_prof,
        "point_profile": point_prof,
        "delta_dist": delta_dist,
        "delta_point": delta_point,
        "ratio": ratio,
        "spread_ratio": dist_spread / max(point_spread, 1e-30),
        "tv": 0.5 * sum(abs(dist_prof.get(k, 0.0) - point_prof.get(k, 0.0)) for k in set(dist_prof) | set(point_prof)),
    }


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

    print("=" * 100)
    print("MESOSCOPIC SURROGATE TWO-STAGE COMPANION (2D)")
    print("  Retained 2D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_y={SOURCE_Y}, max_d={round(MAX_D_PHYS / H)}")
    print("  Goal: can a broad surrogate survive two sourced-response stages without")
    print("        obviously collapsing into an ordinary broad packet?")
    print("=" * 100)
    print()
    print(f"Free-profile centroid: {profile_centroid(free_profile, H):+.4f}")
    print(f"Free-profile spread:   {profile_spread(free_profile, H):.4f}")
    print(f"Probe launch y:        {PROBE_Y:+.4f}")
    print()
    print(f"{'topN':>6s} {'cap1':>7s} {'mu1':>7s} {'sig1':>7s} {'r1':>8s} {'tv1':>7s} {'cap2':>7s} {'mu2':>7s} {'sig2':>7s} {'r2':>8s} {'tv2':>7s} {'carry':>7s}")
    print("-" * 102)

    for topn in TOPN_VALUES:
        src1, cap1 = topn_compress(free_profile, topn)
        stage1 = stage_metrics(pos, adj, n, nl, nmap, det, blocked, free_profile, src1, probe_init, FIELD_STRENGTH)
        src2, cap2 = topn_compress(stage1["dist_profile"], topn)
        stage2 = stage_metrics(pos, adj, n, nl, nmap, det, blocked, free_profile, src2, probe_init, FIELD_STRENGTH)

        carry = overlap(src1, src2)
        print(
            f"{topn:6d} {cap1:7.3f} {profile_centroid(src1, H):+7.3f} {profile_spread(src1, H):7.3f}"
            f" {stage1['ratio']:8.3f} {stage1['tv']:7.3f}"
            f" {cap2:7.3f} {profile_centroid(src2, H):+7.3f} {profile_spread(src2, H):7.3f}"
            f" {stage2['ratio']:8.3f} {stage2['tv']:7.3f} {carry:7.3f}"
        )

    print()
    print("SAFE READ")
    print("  - The broad surrogate survives a second sourced-response stage only as a")
    print("    mesoscopic object, not as a sharply localized persistent packet.")
    print("  - If the stage-2 ratio and carry stay close to stage-1 only for broad topN,")
    print("    the surrogate is useful but still broad-controlled.")
    print("  - If the stage-2 row collapses strongly at small topN, the two-stage lane")
    print("    is a bounded control, not an inertial-object theorem.")
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    main()
