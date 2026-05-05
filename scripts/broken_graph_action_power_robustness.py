#!/usr/bin/env python3
"""Broken-graph action-power robustness replay on the retained 3D family.

This is a bounded follow-up to the inverse-problem note.

Question:
  Under bounded graph damage, is the weak-field-linear phase valley
  (p = 1) structurally more robust than neighboring action powers?

Scope:
  - retained 3D ordered-lattice family
  - small damage ladder
  - action family S = L(1 - f^p)
  - bounded comparison only; not a universal graph theorem

The script reports:
  - Born on each damaged graph
  - gravity sign / magnitude at a fixed probe point
  - TOWARD count on a small source-distance ladder
  - local F~M exponent from a small strength ladder
  - retention relative to the undamaged baseline for each p

The honest read is whatever the bounded ladder says. If p=1 is not the most
robust action on this family, the script says so.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import math
import os
import random
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this probe. On this machine use /usr/bin/python3."
    ) from exc

from scripts.action_universality_probe import (  # noqa: E402
    BETA,
    K,
    Lattice3D,
    action_value,
    fit_power,
)


H = 0.5
PHYS_W = 8
PHYS_L = 12
MAX_D_PHYS = 3
STRENGTH = 5e-5
MASS_STRENGTHS = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
PROBE_Z = 3
SOURCE_ZS = tuple(range(2, 9))
ACTION_POWERS = (0.5, 1.0, 2.0)


@dataclass(frozen=True)
class DamageCase:
    name: str
    offset_keep: frozenset[tuple[int, int]]
    pos_jitter: float = 0.0
    seed: int = 0


@dataclass
class Row:
    damage: str
    p: float
    born: float
    grav_z3: float
    grav_sign: str
    toward_count: int
    fm_alpha: float
    tail_slope: float | None
    tail_r2: float | None
    baseline_grav_z3: float
    grav_retention: float


def detector(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def setup_slits(lat: Lattice3D) -> tuple[list[int], list[int], set[int], int]:
    bl = lat.nl // 3
    barrier = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                barrier.append(idx)
    sa = [i for i in barrier if lat.pos[i, 1] >= 0.5]
    sb = [i for i in barrier if lat.pos[i, 1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return sa, sb, blocked, bl


def make_field(pos: np.ndarray, lat: Lattice3D, z_mass_phys: float, strength: float) -> np.ndarray:
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n)
    mx, my, mz = pos[mi]
    r = np.sqrt((pos[:, 0] - mx) ** 2 + (pos[:, 1] - my) ** 2 + (pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


def jitter_positions(lat: Lattice3D, jitter: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pos = lat.pos.copy()
    pos[:, 1:] += rng.uniform(-jitter, jitter, size=(lat.n, 2))
    return pos


def keep_fraction_offsets(lat: Lattice3D, keep_frac: float, seed: int) -> frozenset[tuple[int, int]]:
    offsets = [(dy, dz) for dy, dz, _, _ in lat._off]
    rng = random.Random(seed)
    if keep_frac >= 1.0:
        return frozenset(offsets)
    keep_n = max(1, round(len(offsets) * keep_frac))
    kept = rng.sample(offsets, keep_n)
    return frozenset(kept)


def offset_mask(name: str, lat: Lattice3D) -> frozenset[tuple[int, int]]:
    offsets = [(dy, dz) for dy, dz, _, _ in lat._off]
    if name == "baseline":
        return frozenset(offsets)
    if name == "asymmetric":
        return frozenset((dy, dz) for dy, dz in offsets if dz <= 0)
    if name == "sparse_nn":
        return frozenset((dy, dz) for dy, dz in offsets if max(abs(dy), abs(dz)) <= 1)
    raise ValueError(f"unknown deterministic mask name={name}")


def propagate_damaged(
    lat: Lattice3D,
    pos: np.ndarray,
    field: np.ndarray,
    k: float,
    blocked_set: set[int],
    action_mode: str,
    offset_keep: frozenset[tuple[int, int]],
) -> np.ndarray:
    amps = np.zeros(lat.n, dtype=np.complex128)
    amps[lat.nmap[(0, 0, 0)]] = 1.0

    blocked = np.zeros(lat.n, dtype=bool)
    for b in blocked_set:
        blocked[b] = True

    for layer in range(lat.nl - 1):
        ls = lat._ls[layer]
        ld = lat._ls[layer + 1]

        sa = amps[ls:ls + lat.npl].copy()
        sa[blocked[ls:ls + lat.npl]] = 0
        if np.max(np.abs(sa)) < 1e-30:
            continue

        sf = field[ls:ls + lat.npl]
        df = field[ld:ld + lat.npl]
        db = blocked[ld:ld + lat.npl]

        for dy, dz, _, _ in lat._off:
            if (dy, dz) not in offset_keep:
                continue

            ym = max(0, -dy)
            yM = min(lat._nw, lat._nw - dy)
            zm = max(0, -dz)
            zM = min(lat._nw, lat._nw - dz)
            if ym >= yM or zm >= zM:
                continue

            yr = np.arange(ym, yM)
            zr = np.arange(zm, zM)
            siy, siz = np.meshgrid(yr, zr, indexing="ij")
            si = siy.ravel() * lat._nw + siz.ravel()
            di = (siy.ravel() + dy) * lat._nw + (siz.ravel() + dz)

            a = sa[si]
            nz = np.abs(a) > 1e-30
            if not np.any(nz):
                continue

            src_idx = ls + si[nz]
            dst_idx = ld + di[nz]
            delta = pos[dst_idx] - pos[src_idx]
            dx = delta[:, 0]
            dyv = delta[:, 1]
            dzv = delta[:, 2]
            L = np.sqrt(dx * dx + dyv * dyv + dzv * dzv)
            if np.max(L) < 1e-30:
                continue

            lf = 0.5 * (sf[si[nz]] + df[di[nz]])
            act = action_value(L, lf, action_mode)
            theta = np.arctan2(np.sqrt(dyv * dyv + dzv * dzv), np.maximum(dx, 1e-10))
            c = a[nz] * np.exp(1j * k * act) * np.exp(-BETA * theta * theta) * lat._hm / (L * L)
            c[db[di[nz]]] = 0
            np.add.at(amps[ld:ld + lat.npl], di[nz], c)

    return amps


def born_value(lat: Lattice3D, pos: np.ndarray, offset_keep: frozenset[tuple[int, int]]) -> float:
    _, _, blocked, _ = setup_slits(lat)
    det = detector(lat)
    field_f = np.zeros(lat.n)
    barrier_nodes = {
        lat.nmap[(lat.nl // 3, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl // 3, iy, iz) in lat.nmap
    }
    upper = sorted([i for i in barrier_nodes if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in barrier_nodes if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in barrier_nodes if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    if not (upper and lower and middle):
        return float("nan")

    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = barrier_nodes - all_s
    probs: dict[str, np.ndarray] = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(s_a + s_b)),
        ("ac", set(s_a + s_c)),
        ("bc", set(s_b + s_c)),
        ("a", set(s_a)),
        ("b", set(s_b)),
        ("c", set(s_c)),
    ]:
        bl2 = other | (all_s - open_set)
        amps = propagate_damaged(
            lat,
            pos,
            field_f,
            K,
            bl2,
            "valley_linear",
            offset_keep,
        )
        probs[key] = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)

    i3_sum = 0.0
    p_sum = 0.0
    for di in range(len(det)):
        i3 = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        i3_sum += abs(i3)
        p_sum += probs["abc"][di]
    return i3_sum / p_sum if p_sum > 1e-30 else float("nan")


def measure_case(
    lat: Lattice3D,
    pos: np.ndarray,
    offset_keep: frozenset[tuple[int, int]],
    action_mode: str,
) -> Row:
    det = detector(lat)
    _, _, blocked, _ = setup_slits(lat)
    field_f = np.zeros(lat.n)

    free = propagate_damaged(lat, pos, field_f, K, blocked, action_mode, offset_keep)
    z_free = float(np.sum(np.array([abs(free[d]) ** 2 for d in det]) * pos[det, 2]) / max(sum(abs(free[d]) ** 2 for d in det), 1e-30))

    born = born_value(lat, pos, offset_keep)

    field_m = make_field(pos, lat, PROBE_Z, STRENGTH)
    mass = propagate_damaged(lat, pos, field_m, K, blocked, action_mode, offset_keep)
    z_mass = float(np.sum(np.array([abs(mass[d]) ** 2 for d in det]) * pos[det, 2]) / max(sum(abs(mass[d]) ** 2 for d in det), 1e-30))
    grav = z_mass - z_free
    grav_sign = "TOWARD" if grav > 0 else "AWAY"

    fm_x: list[float] = []
    fm_y: list[float] = []
    for s in MASS_STRENGTHS:
        amps = propagate_damaged(lat, pos, make_field(pos, lat, PROBE_Z, s), K, blocked, action_mode, offset_keep)
        z_mass_s = float(np.sum(np.array([abs(amps[d]) ** 2 for d in det]) * pos[det, 2]) / max(sum(abs(amps[d]) ** 2 for d in det), 1e-30))
        delta = z_mass_s - z_free
        if delta > 0:
            fm_x.append(s)
            fm_y.append(delta)
    fm_alpha = float("nan")
    sl, _ = fit_power(fm_x, fm_y)
    if sl is not None:
        fm_alpha = sl

    b_data: list[float] = []
    d_data: list[float] = []
    for z_mass_phys in SOURCE_ZS:
        amps = propagate_damaged(
            lat,
            pos,
            make_field(pos, lat, z_mass_phys, STRENGTH),
            K,
            blocked,
            action_mode,
            offset_keep,
        )
        z_mass_s = float(np.sum(np.array([abs(amps[d]) ** 2 for d in det]) * pos[det, 2]) / max(sum(abs(amps[d]) ** 2 for d in det), 1e-30))
        delta = z_mass_s - z_free
        if delta > 0:
            b_data.append(z_mass_phys)
            d_data.append(delta)

    tail_slope = None
    tail_r2 = None
    if len(b_data) >= 3:
        peak_i = int(np.argmax(d_data))
        if len(b_data) - peak_i >= 3:
            slope, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
            tail_slope = slope
            tail_r2 = r2

    toward_count = sum(1 for d in d_data if d > 0)
    return Row(
        damage="",
        p=0.0,
        born=born,
        grav_z3=grav,
        grav_sign=grav_sign,
        toward_count=toward_count,
        fm_alpha=fm_alpha,
        tail_slope=tail_slope,
        tail_r2=tail_r2,
        baseline_grav_z3=grav,
        grav_retention=1.0,
    )


def fmt(x: float | None, places: int = 3) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x:.{places}f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stochastic-seed",
        type=int,
        default=13,
        help="Seed for randomized graph damage masks.",
    )
    args = parser.parse_args()

    lat = Lattice3D(PHYS_L, PHYS_W, H)
    base_pos = lat.pos
    det = detector(lat)
    _, _, blocked, _ = setup_slits(lat)

    cases: list[tuple[str, np.ndarray, frozenset[tuple[int, int]]]] = []
    cases.append(("baseline", base_pos, frozenset((dy, dz) for dy, dz, _, _ in lat._off)))
    cases.append(("delete_30", base_pos, keep_fraction_offsets(lat, 0.70, args.stochastic_seed)))
    cases.append(("delete_50", base_pos, keep_fraction_offsets(lat, 0.50, args.stochastic_seed + 1)))
    cases.append(("delete_70", base_pos, keep_fraction_offsets(lat, 0.30, args.stochastic_seed + 2)))
    cases.append(("asymmetric", base_pos, offset_mask("asymmetric", lat)))
    jitter_pos = jitter_positions(lat, 0.5 * lat.h, args.stochastic_seed + 3)
    cases.append(("jitter_0.5h", jitter_pos, frozenset((dy, dz) for dy, dz, _, _ in lat._off)))
    cases.append(("sparse_nn", base_pos, offset_mask("sparse_nn", lat)))

    print("=" * 100)
    print("BROKEN-GRAPH ACTION-POWER ROBUSTNESS")
    print("  Retained 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}")
    print("  Action family: S = L(1-f^p)")
    print("  Damage ladder: baseline, offset deletion, asymmetry, jitter, sparse NN")
    print("  Goal: check whether p=1 is structurally more robust than neighboring p values")
    print("=" * 100)
    print()

    all_rows: list[tuple[str, float, Row]] = []
    for case_name, pos, keep_offsets in cases:
        print(f"[damage={case_name}]")
        print(f"{'p':>5s} {'Born':>10s} {'Grav(z=3)':>12s} {'TOWARD':>8s} {'F~M':>8s} {'Tail':>14s}")
        for p in ACTION_POWERS:
            row = measure_case(lat, pos, keep_offsets, f"power:{p}")
            row.damage = case_name
            row.p = p
            all_rows.append((case_name, p, row))
            tail = "n/a"
            if row.tail_slope is not None and row.tail_r2 is not None:
                tail = f"b^({row.tail_slope:+.2f}),R²={row.tail_r2:.3f}"
            print(
                f"{p:5.2f} {row.born:10.2e} {row.grav_z3:+12.6f} "
                f"{row.grav_sign:>8s} {fmt(row.fm_alpha, 2):>8s} {tail:>14s}"
            )
        print()

    by_power: dict[float, list[Row]] = {p: [] for p in ACTION_POWERS}
    for _, p, row in all_rows:
        by_power[p].append(row)

    baseline_by_power = {p: next(r for _, pp, r in all_rows if pp == p and r.damage == "baseline") for p in ACTION_POWERS}

    print("ROBUSTNESS SUMMARY")
    print(f"{'p':>5s} {'base Grav':>12s} {'toward/6':>10s} {'mean Grav':>12s} {'mean |Grav|':>12s} {'mean |F~M-p|':>14s}")
    for p in ACTION_POWERS:
        base = baseline_by_power[p]
        damaged = [r for r in by_power[p] if r.damage != "baseline"]
        toward = sum(1 for r in damaged if r.grav_z3 > 0)
        mean_grav = float(np.nanmean([r.grav_z3 for r in damaged])) if damaged else float("nan")
        mean_abs_grav = float(np.nanmean([abs(r.grav_z3) for r in damaged])) if damaged else float("nan")
        mean_dev = float(np.nanmean([abs(r.fm_alpha - p) for r in damaged if math.isfinite(r.fm_alpha)])) if damaged else float("nan")
        print(
            f"{p:5.2f} {base.grav_z3:+12.6f} {toward:10d} "
            f"{mean_grav:+12.6f} {mean_abs_grav:12.6f} {mean_dev:14.3f}"
        )

    print()
    print("SAFE READ")
    print("  - This is a bounded graph-damage replay on one retained 3D family.")
    print("  - The graph controls precision and retention, not whether gravity exists.")
    print("  - p=1 is the Newtonian candidate; p!=1 are the neighboring comparison actions.")
    print("  - Read p=1 as structurally more robust only if it keeps the best retention and the smallest drift across the ladder.")
    print("  - If the summary does not favor p=1, the honest result is that the robustness claim weakens on this family.")


if __name__ == "__main__":
    main()
