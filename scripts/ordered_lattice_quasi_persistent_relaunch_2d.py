#!/usr/bin/env python3
"""2D ordered-lattice quasi-persistent relaunch control.

This is the cheapest cross-family sanity check for the relaunch-packet idea.
It mirrors the retained 3D relaunch control, but on the retained 2D ordered
lattice from the continuum-distance lane.

Question:
  If we build a compact packet surrogate on the 2D ordered lattice, can we
  re-identify it after a free propagation segment and relaunch it without
  destroying the profile?

What it measures:
  - free packet centroid and spread at the detector
  - top-k re-identification capture fraction
  - carry overlap between the free packet and the relaunch surrogate
  - field-induced centroid shift after relaunch

This is a diagnostic only. It does not claim a persistent-mass theorem.
"""

from __future__ import annotations

import math
import os
import sys
import time

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
FIELD_STRENGTHS = (2e-5, 5e-5, 1e-4)
TOPK_REIDENTIFY = 5
ACTIONS = ("valley_linear", "spent_delay")


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
    if norm < 1e-30:
        return weights
    return {iy: w / norm for iy, w in weights.items()}


def source_field(
    pos: list[tuple[float, float]],
    nmap: dict[tuple[int, int], int],
    nl: int,
    h: float,
    z_phys: float,
    strength: float,
) -> np.ndarray:
    gl = 2 * nl // 3
    iy = round(z_phys / h)
    mi = nmap.get((gl, iy))
    if mi is None:
        return np.zeros(len(pos), dtype=float)
    mx, my = pos[mi]
    field = np.zeros(len(pos), dtype=float)
    for i, (x, y) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2) + 0.1
        field[i] = strength / r
    return field


def source_packet(
    n: int,
    nmap: dict[tuple[int, int], int],
    weights: dict[int, float],
) -> np.ndarray:
    init = np.zeros(n, dtype=np.complex128)
    norm = math.sqrt(sum(w * w for w in weights.values()))
    if norm < 1e-30:
        return init
    for iy, w in weights.items():
        init[nmap[(0, iy)]] = w / norm
    return init


def y_profile(
    amps: np.ndarray,
    det: list[int],
    pos: list[tuple[float, float]],
    h: float,
) -> dict[int, float]:
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


def overlap(profile_a: dict[int, float], profile_b: dict[int, float]) -> float:
    keys = set(profile_a) | set(profile_b)
    return sum(math.sqrt(profile_a.get(k, 0.0) * profile_b.get(k, 0.0)) for k in keys)


def topk_reidentify(profile: dict[int, float], k: int) -> tuple[dict[int, float], float]:
    if not profile:
        return {}, 0.0
    items = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    selected = items[: min(k, len(items))]
    capture = sum(p for _, p in selected)
    total = sum(p for _, p in selected)
    if total <= 0:
        return {}, 0.0
    return {iy: p / total for iy, p in selected}, capture


def packet_from_profile(
    n: int,
    nmap: dict[tuple[int, int], int],
    profile: dict[int, float],
) -> np.ndarray:
    init = np.zeros(n, dtype=np.complex128)
    norm = math.sqrt(sum(p for p in profile.values()))
    if norm <= 0:
        return init
    for iy, p in profile.items():
        init[nmap[(0, iy)]] = math.sqrt(p) / norm
    return init


def propagate_packet(
    pos: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: np.ndarray,
    init: np.ndarray,
    blocked: set[int],
    n: int,
    action_mode: str,
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
            if action_mode == "spent_delay":
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
            elif action_mode == "valley_linear":
                act = L * (1 - lf)
            else:  # pragma: no cover - internal guard
                raise ValueError(f"unknown action_mode={action_mode}")
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * np.exp(1j * K * act) * w / L
    return amps


def relaunch_metrics(
    pos: list[tuple[float, float]],
    adj: dict[int, list[int]],
    nmap: dict[tuple[int, int], int],
    nl: int,
    hw: int,
    det: list[int],
    blocked: set[int],
    action: str,
    init: np.ndarray,
    free_field: np.ndarray,
    mass_field: np.ndarray,
) -> tuple[dict[int, float], dict[int, float], dict[int, float], float, float, float]:
    free_amps = propagate_packet(pos, adj, free_field, init, blocked, len(pos), action)
    mass_amps = propagate_packet(pos, adj, mass_field, init, blocked, len(pos), action)
    free_profile = y_profile(free_amps, det, pos, H)
    mass_profile = y_profile(mass_amps, det, pos, H)
    topk, capture = topk_reidentify(free_profile, TOPK_REIDENTIFY)
    relaunch = packet_from_profile(len(pos), nmap, topk if topk else free_profile)
    relaunch_free = propagate_packet(pos, adj, free_field, relaunch, blocked, len(pos), action)
    relaunch_mass = propagate_packet(pos, adj, mass_field, relaunch, blocked, len(pos), action)
    relaunch_free_profile = y_profile(relaunch_free, det, pos, H)
    relaunch_mass_profile = y_profile(relaunch_mass, det, pos, H)
    carry = overlap(free_profile, relaunch_free_profile)
    shift = profile_centroid(mass_profile, H) - profile_centroid(free_profile, H)
    relaunch_shift = profile_centroid(relaunch_mass_profile, H) - profile_centroid(relaunch_free_profile, H)
    spread_ratio = (
        profile_spread(mass_profile, H) / profile_spread(free_profile, H)
        if profile_spread(free_profile, H) > 1e-30
        else 0.0
    )
    return free_profile, mass_profile, relaunch_free_profile, capture, carry, shift, relaunch_shift, spread_ratio


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

    init = source_packet(n, nmap, gaussian_packet(hw, H))
    free_field = np.zeros(n, dtype=float)

    print("=" * 92)
    print("ORDERED-LATTICE QUASI-PERSISTENT RELAUNCH CONTROL (2D)")
    print("  Cross-family sanity check for the relaunch-packet idea")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={round(MAX_D_PHYS / H)}, source_y={SOURCE_Y}")
    print("  Goal: ask whether a compact packet surrogate stays recognizable enough")
    print("        to be relaunched on the retained 2D ordered family.")
    print("=" * 92)
    print()

    # Bounded numerical replay table. Each value is pinned by an assertion
    # below tied to docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md.
    # No acceptance threshold, packet-class, or invariance guarantee is being
    # claimed; the note's narrowed claim is only that this six-row table
    # reproduces deterministically.
    measured: dict[tuple[str, float], dict[str, float]] = {}

    for action in ACTIONS:
        print(f"ACTION: {action}")
        print(
            f"{'strength':>10s} {'capture':>8s} {'carry':>8s} "
            f"{'shift':>10s} {'relaunch':>10s} {'width×':>8s}"
        )
        print("-" * 68)

        for strength in FIELD_STRENGTHS:
            mass_field = source_field(pos, nmap, nl, H, SOURCE_Y, strength)
            (
                free_profile,
                mass_profile,
                relaunch_free_profile,
                capture,
                carry,
                shift,
                relaunch_shift,
                spread_ratio,
            ) = relaunch_metrics(
                pos,
                adj,
                nmap,
                nl,
                hw,
                det,
                blocked,
                action,
                init,
                free_field,
                mass_field,
            )
            measured[(action, strength)] = {
                "capture": capture,
                "carry": carry,
                "shift": shift,
                "relaunch": relaunch_shift,
                "width": spread_ratio,
            }
            print(
                f"{strength:10.0e} {capture:8.3f} {carry:8.3f} "
                f"{shift:+10.6f} {relaunch_shift:+10.6f} {spread_ratio:8.3f}"
            )
        print()

    # Bounded numerical-replay assertions (pinned to the note table).
    # Tolerance: 1e-3 absolute on rounded reported values; this is the
    # display precision used in the note table and the runner output.
    expected = {
        ("valley_linear", 2e-05): (0.344, 0.911, +0.000394, +0.000205, 1.000),
        ("valley_linear", 5e-05): (0.344, 0.911, +0.000985, +0.000512, 1.000),
        ("valley_linear", 1e-04): (0.344, 0.911, +0.001968, +0.001024, 1.000),
        ("spent_delay",   2e-05): (0.344, 0.911, +0.111785, +0.073447, 0.996),
        ("spent_delay",   5e-05): (0.344, 0.911, +0.174422, +0.115193, 0.993),
        ("spent_delay",   1e-04): (0.344, 0.911, +0.242946, +0.161549, 0.990),
    }
    tol = 1.0e-3
    for key, (cap_e, car_e, sh_e, rel_e, wid_e) in expected.items():
        m = measured[key]
        assert abs(m["capture"]  - cap_e) <= tol, f"{key} capture drift: got {m['capture']:.6f}, expected {cap_e}"
        assert abs(m["carry"]    - car_e) <= tol, f"{key} carry drift: got {m['carry']:.6f}, expected {car_e}"
        assert abs(m["shift"]    - sh_e ) <= tol, f"{key} shift drift: got {m['shift']:+.6f}, expected {sh_e:+.6f}"
        assert abs(m["relaunch"] - rel_e) <= tol, f"{key} relaunch drift: got {m['relaunch']:+.6f}, expected {rel_e:+.6f}"
        assert abs(m["width"]    - wid_e) <= tol, f"{key} width drift: got {m['width']:.6f}, expected {wid_e}"
    print("PASS: bounded numerical-replay table matches the narrowed note "
          "(six rows; capture/carry/shift/relaunch/width within +/-1e-3).")

    print("SAFE READ")
    print("  - This is a bounded numerical replay only. It is not a persistent-mass theorem.")
    print("  - It is not a family-generic claim; only the one fixed harness is tested.")
    print("  - The displayed values are pinned by the assertions above.")
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    main()
