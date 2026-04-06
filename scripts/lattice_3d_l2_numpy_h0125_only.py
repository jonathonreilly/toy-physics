#!/usr/bin/env python3
"""Focused replay for the decisive wide-family h=0.125 bridge test.

This is narrower than the full bridge wrapper and narrower than the full
``run_card`` path. The bridge decision only needs the observables that control
the retained claim surface:

- `k = 0` null
- Born
- gravity sign at the retained weak-field point
- weak-field `F~M`

At `h = 0.125` the current dense-family row is fully connected layer-to-layer,
so this harness uses a per-layer dense matrix update instead of materializing
the full multi-layer edge list. That keeps the test aimed at the scientific
decision instead of paying for metrics the reopen audit does not need.
"""

from __future__ import annotations

import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

BETA = 0.8
K = 5.0


def build_dense_family(phys_l: int, phys_w: int, h: float) -> dict[str, object]:
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    ys = np.arange(-hw, hw + 1, dtype=np.float64) * h
    zs = np.arange(-hw, hw + 1, dtype=np.float64) * h
    yy, zz = np.meshgrid(ys, zs, indexing="ij")
    yz = np.stack([yy.ravel(), zz.ravel()], axis=1)
    npl = yz.shape[0]

    # At h=0.125 on this family, max_d == hw, so every layer transition is
    # dense over the full yz slab. Build that fixed geometry once.
    dy = yz[:, 0][None, :] - yz[:, 0][:, None]
    dz = yz[:, 1][None, :] - yz[:, 1][:, None]
    transverse = np.sqrt(dy * dy + dz * dz)
    L = np.sqrt(h * h + transverse * transverse)
    base_kernel = np.exp(-BETA * np.arctan2(transverse, h) ** 2) / (L * L)
    free_phase = np.exp(1j * K * L) * base_kernel

    src_idx = int(np.argmin(np.sum(yz * yz, axis=1)))
    bl = nl // 3
    gl = 2 * nl // 3

    default_open = np.abs(yz[:, 0]) >= 0.5
    upper = np.where(yz[:, 0] > 1.0)[0]
    lower = np.where(yz[:, 0] < -1.0)[0]
    middle = np.where((np.abs(yz[:, 0]) <= 1.0) & (np.abs(yz[:, 1]) <= 1.0))[0]

    return {
        "h": h,
        "nl": nl,
        "hw": hw,
        "npl": npl,
        "n": nl * npl,
        "edges": (nl - 1) * npl * npl,
        "yz": yz,
        "L": L,
        "base_kernel": base_kernel,
        "free_phase": free_phase,
        "src_idx": src_idx,
        "bl": bl,
        "gl": gl,
        "default_open": default_open,
        "born_upper": upper,
        "born_lower": lower,
        "born_middle": middle,
    }


def make_field_layers(lat: dict[str, object], z_mass_phys: float, strength: float) -> np.ndarray:
    nl = int(lat["nl"])
    yz = lat["yz"]
    h = float(lat["h"])
    gl = int(lat["gl"])
    x = (np.arange(nl, dtype=np.float64) * h)[:, None]
    y = yz[:, 0][None, :]
    z = yz[:, 1][None, :]
    z_mass = round(z_mass_phys / h) * h
    r = np.sqrt((x - gl * h) ** 2 + y * y + (z - z_mass) ** 2) + 0.1
    return strength / r


def free_prefix_to_barrier(lat: dict[str, object]) -> tuple[np.ndarray, np.ndarray]:
    nl = int(lat["nl"])
    bl = int(lat["bl"])
    npl = int(lat["npl"])
    src_idx = int(lat["src_idx"])
    phase = lat["free_phase"]

    amps = np.zeros(npl, dtype=np.complex128)
    amps[src_idx] = 1.0
    for _layer in range(bl - 1):
        amps = amps @ phase

    barrier_in = amps @ phase
    return amps, barrier_in


def propagate_free_from_barrier(
    lat: dict[str, object], barrier_state: np.ndarray, open_mask: np.ndarray
) -> np.ndarray:
    nl = int(lat["nl"])
    bl = int(lat["bl"])
    phase = lat["free_phase"]
    amps = barrier_state.copy()
    amps[~open_mask] = 0.0
    for _layer in range(bl, nl - 1):
        amps = amps @ phase
    return amps


def propagate_field(lat: dict[str, object], field_layers: np.ndarray, open_mask: np.ndarray, k: float) -> np.ndarray:
    nl = int(lat["nl"])
    npl = int(lat["npl"])
    src_idx = int(lat["src_idx"])
    bl = int(lat["bl"])
    L = lat["L"]
    base_kernel = lat["base_kernel"]

    amps = np.zeros(npl, dtype=np.complex128)
    amps[src_idx] = 1.0
    for layer in range(nl - 1):
        a = 1.0 + 0.5 * (field_layers[layer][:, None] + field_layers[layer + 1][None, :])
        ret = np.sqrt(np.maximum(a * a - 1.0, 0.0))
        act = L * (a - ret)
        phase = np.exp(1j * k * act) * base_kernel
        amps = amps @ phase
        if layer + 1 == bl:
            amps = amps.copy()
            amps[~open_mask] = 0.0
    return amps


def detector_probability(amps: np.ndarray) -> np.ndarray:
    return np.abs(amps) ** 2


def centroid_z(lat: dict[str, object], amps: np.ndarray) -> tuple[float, float]:
    probs = detector_probability(amps)
    total = float(probs.sum())
    if total <= 1e-30:
        return 0.0, 0.0
    z = lat["yz"][:, 1]
    return float((probs * z).sum() / total), total


def born_ratio(lat: dict[str, object], barrier_in: np.ndarray) -> float:
    upper = lat["born_upper"]
    lower = lat["born_lower"]
    middle = lat["born_middle"]
    npl = int(lat["npl"])
    if len(upper) == 0 or len(lower) == 0 or len(middle) == 0:
        return float("nan")

    s_a = int(upper[0])
    s_b = int(lower[0])
    s_c = int(middle[0])

    masks = {}
    for key, open_nodes in {
        "abc": {s_a, s_b, s_c},
        "ab": {s_a, s_b},
        "ac": {s_a, s_c},
        "bc": {s_b, s_c},
        "a": {s_a},
        "b": {s_b},
        "c": {s_c},
    }.items():
        open_mask = np.zeros(npl, dtype=bool)
        for idx in open_nodes:
            open_mask[idx] = True
        final = propagate_free_from_barrier(lat, barrier_in, open_mask)
        masks[key] = detector_probability(final)

    i3 = masks["abc"] - masks["ab"] - masks["ac"] - masks["bc"] + masks["a"] + masks["b"] + masks["c"]
    total = float(masks["abc"].sum())
    return float(np.abs(i3).sum() / total) if total > 1e-30 else float("nan")


def main() -> None:
    phys_l = 6
    phys_w = 3
    strength = 5e-5
    h = 0.125

    t0 = time.time()
    lat = build_dense_family(phys_l, phys_w, h)
    t_build = time.time() - t0

    print("=" * 84)
    print("3D 1/L^2 + h^2 NUMPY H=0.125 SINGLE-ROW DECISION TEST")
    print(f"  fixed family: phys_l={phys_l}, phys_w={phys_w}, max_d_phys=3")
    print(f"  source strength={strength:.0e}")
    print("  goal: decide whether the decisive h=0.125 row can be retained")
    print("=" * 84)
    print()
    print(f"  {lat['n']} nodes, {lat['nl']} layers, {lat['edges']} dense edges")
    print(f"  Built dense layer geometry in {t_build:.1f}s")

    t1 = time.time()
    _prefix, barrier_in = free_prefix_to_barrier(lat)
    free_final = propagate_free_from_barrier(lat, barrier_in, lat["default_open"])
    z_free, p_free = centroid_z(lat, free_final)
    print(f"  Free propagation: {time.time() - t1:.1f}s (P_det={p_free:.3e})")

    t1 = time.time()
    born = born_ratio(lat, barrier_in)
    print(f"  1. Born |I3|/P = {born:.2e}  [{'PASS' if born < 1e-10 else 'FAIL'}] ({time.time() - t1:.1f}s)")

    field_z3 = make_field_layers(lat, 3.0, strength)

    t1 = time.time()
    null_final = propagate_field(lat, field_z3, lat["default_open"], 0.0)
    z_null, _p_null = centroid_z(lat, null_final)
    print(f"  2. k=0 = {z_null - z_free:+.6f} ({time.time() - t1:.1f}s)")

    t1 = time.time()
    grav_final = propagate_field(lat, field_z3, lat["default_open"], K)
    z_grav, p_grav = centroid_z(lat, grav_final)
    grav = z_grav - z_free
    print(f"  3. Gravity z=3 = {grav:+.6f} ({'TOWARD' if grav > 0 else 'AWAY'}) ({time.time() - t1:.1f}s, P_det={p_grav:.3e})")

    t1 = time.time()
    m_data = []
    g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        field = make_field_layers(lat, 3.0, s)
        final = propagate_field(lat, field, lat["default_open"], K)
        z_m, _p_m = centroid_z(lat, final)
        delta = z_m - z_free
        if delta > 0:
            m_data.append(s)
            g_data.append(delta)
    if len(m_data) >= 3:
        lx = [math.log(v) for v in m_data]
        ly = [math.log(v) for v in g_data]
        mx = sum(lx) / len(lx)
        my = sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
        alpha = sxy / sxx if sxx > 1e-12 else float("nan")
        print(f"  4. F~M alpha = {alpha:.3f} ({time.time() - t1:.1f}s)")
    else:
        print(f"  4. F~M: too few TOWARD points ({len(m_data)}) ({time.time() - t1:.1f}s)")


if __name__ == "__main__":
    main()
