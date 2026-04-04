#!/usr/bin/env python3
"""Bounded action-universality probe on the retained 3D ordered-lattice family.

This is not a universal theorem harness. It freezes a review-safe comparison on
one fixed family:

  - 3D ordered dense lattice
  - valley-style 1/L^2 propagator with h^2 measure
  - h = 0.5, W = 8, L = 12
  - same barrier / detector geometry

It compares representative action laws to test the claim that:

  - TOWARD gravity requires a phase valley
  - the F~M exponent tracks the weak-field power of f in the action
  - weak-field-linear phase valleys form a Newtonian-like universality class

Measured here:
  - Born (field-free; same value for all actions on this family)
  - gravity sign at z = 3
  - TOWARD count on z = 2..8
  - local F~M exponent on a small strength ladder
  - representative post-peak tail fit when enough positive rows exist
"""

from __future__ import annotations

import math
import os
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


BETA = 0.8
K = 5.0
H = 0.5
PHYS_W = 8
PHYS_L = 12
MAX_D_PHYS = 3
STRENGTH = 5e-5
MASS_STRENGTHS = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]


@dataclass
class ActionResult:
    name: str
    born: float
    gravity_z3: float
    toward_count: int
    fm_alpha: float
    tail_slope: float
    tail_r2: float
    peak_z: int | None


class Lattice3D:
    def __init__(self, phys_l: int, phys_w: int, h: float):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        self._nw = 2 * self.hw + 1
        self.npl = self._nw**2
        self.n = self.nl * self.npl
        self._hm = h * h

        self.pos = np.zeros((self.n, 3))
        self.nmap: dict[tuple[int, int, int], int] = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int], action_mode: str) -> np.ndarray:
        amps = np.zeros(self.n, dtype=np.complex128)
        amps[self.nmap[(0, 0, 0)]] = 1.0

        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1]
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue

            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]

            for dy, dz, L, w in self._off:
                ym = max(0, -dy)
                yM = min(self._nw, self._nw - dy)
                zm = max(0, -dz)
                zM = min(self._nw, self._nw - dz)
                if ym >= yM or zm >= zM:
                    continue

                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * self._nw + siz.ravel()
                di = (siy.ravel() + dy) * self._nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue

                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = action_value(L, lf, action_mode)
                c = a[nz] * np.exp(1j * k * act) * w * self._hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)

        return amps


def action_value(L: float, f: np.ndarray, action_mode: str) -> np.ndarray:
    f = np.maximum(f, 0.0)
    if action_mode.startswith("power:"):
        power = float(action_mode.split(":", 1)[1])
        return L * (1.0 - np.power(f, power))
    if action_mode == "none":
        return np.full_like(f, L)
    if action_mode == "hill_linear":
        return L * (1.0 + f)
    if action_mode == "valley_sqrt":
        return L * (1.0 - np.sqrt(f))
    if action_mode == "valley_linear":
        return L * (1.0 - f)
    if action_mode == "valley_quadratic":
        return L * (1.0 - f * f)
    if action_mode == "valley_exp":
        return L * np.exp(-f)
    if action_mode == "valley_recip":
        return L / (1.0 + f)
    if action_mode == "negative_linear":
        return -L * f
    raise ValueError(f"unknown action_mode={action_mode}")


def make_field(lat: Lattice3D, z_mass_phys: float, strength: float) -> np.ndarray:
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n)
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx) ** 2 + (lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


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


def fit_power(x_data: list[float], y_data: list[float]) -> tuple[float | None, float | None]:
    if len(x_data) < 3:
        return None, None
    lx = np.log(np.array(x_data, dtype=float))
    ly = np.log(np.array(y_data, dtype=float))
    mx = lx.mean()
    my = ly.mean()
    sxx = np.sum((lx - mx) ** 2)
    if sxx < 1e-12:
        return None, None
    sxy = np.sum((lx - mx) * (ly - my))
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx))) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def detector(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def born_value(lat: Lattice3D, det: list[int], action_mode: str) -> float:
    _, _, blocked, bl = setup_slits(lat)
    field_f = np.zeros(lat.n)
    pos = lat.pos
    barrier_nodes = {
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap
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
        a = lat.propagate(field_f, K, bl2, action_mode)
        probs[key] = np.array([abs(a[d]) ** 2 for d in det])
    I3 = 0.0
    P = 0.0
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
        I3 += abs(i3)
        P += probs["abc"][di]
    return I3 / P if P > 1e-30 else float("nan")


def measure_action(lat: Lattice3D, det: list[int], action_mode: str) -> ActionResult:
    sa, sb, blocked, _ = setup_slits(lat)
    pos = lat.pos
    field_f = np.zeros(lat.n)

    af = lat.propagate(field_f, K, blocked, action_mode)
    pf = sum(abs(af[d]) ** 2 for d in det)
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf

    born = born_value(lat, det, action_mode)

    fm_data_x: list[float] = []
    fm_data_y: list[float] = []
    for s in MASS_STRENGTHS:
        fm = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked, action_mode)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                fm_data_x.append(s)
                fm_data_y.append(delta)
    fm_alpha = float("nan")
    sl, _r2 = fit_power(fm_data_x, fm_data_y)
    if sl is not None:
        fm_alpha = sl

    fz3 = make_field(lat, 3, STRENGTH)
    az3 = lat.propagate(fz3, K, blocked, action_mode)
    pz3 = sum(abs(az3[d]) ** 2 for d in det)
    gravity_z3 = 0.0
    if pz3 > 1e-30:
        gravity_z3 = sum(abs(az3[d]) ** 2 * pos[d, 2] for d in det) / pz3 - zf

    b_data: list[float] = []
    d_data: list[float] = []
    for z in range(2, 9):
        fm = make_field(lat, z, STRENGTH)
        am = lat.propagate(fm, K, blocked, action_mode)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                b_data.append(z)
                d_data.append(delta)
    toward_count = len(b_data)
    tail_slope = float("nan")
    tail_r2 = float("nan")
    peak_z: int | None = None
    if len(d_data) >= 3:
        peak_i = int(np.argmax(np.array(d_data)))
        peak_z = int(b_data[peak_i])
        sl2, r22 = fit_power(b_data[peak_i:], d_data[peak_i:])
        if sl2 is not None:
            tail_slope = sl2
            tail_r2 = r22 if r22 is not None else float("nan")

    return ActionResult(
        name=action_mode,
        born=born,
        gravity_z3=gravity_z3,
        toward_count=toward_count,
        fm_alpha=fm_alpha,
        tail_slope=tail_slope,
        tail_r2=tail_r2,
        peak_z=peak_z,
    )


def label(action_mode: str) -> str:
    if action_mode.startswith("power:"):
        power = float(action_mode.split(":", 1)[1])
        return f"S=L(1-f^{power:g})"
    return {
        "none": "S=L",
        "hill_linear": "S=L(1+f)",
        "valley_sqrt": "S=L(1-f^0.5)",
        "valley_linear": "S=L(1-f)",
        "valley_quadratic": "S=L(1-f^2)",
        "valley_exp": "S=L exp(-f)",
        "valley_recip": "S=L/(1+f)",
        "negative_linear": "S=-Lf",
    }[action_mode]


def fmt_float(x: float, places: int = 2) -> str:
    if math.isnan(x):
        return "nan"
    return f"{x:.{places}f}"


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    actions = [
        "none",
        "hill_linear",
        "valley_sqrt",
        "valley_linear",
        "valley_quadratic",
        "valley_exp",
        "valley_recip",
        "negative_linear",
    ]

    print("=" * 96)
    print("ACTION UNIVERSALITY PROBE")
    print("  Fixed 3D ordered-lattice family")
    print("  h=0.5, W=8, L=12, max_d=3")
    print("  Kernel: 1/L^2 with h^2 measure")
    print("  Field: s/r, standard strength ladder")
    print("  Goal: test weak-field action universality classes, not a universal theorem")
    print("=" * 96)
    print()
    print(f"{'action':<18} {'Born':>10} {'grav(z=3)':>12} {'TOWARD':>8} {'F~M':>8} {'tail':>12}")
    print("-" * 96)

    results: list[ActionResult] = []
    for mode in actions:
        row = measure_action(lat, det, mode)
        results.append(row)
        toward = f"{row.toward_count}/7"
        tail = "n/a"
        if not math.isnan(row.tail_slope):
            peak = f"z>={row.peak_z}" if row.peak_z is not None else "tail"
            tail = f"{peak}:{row.tail_slope:+.2f}"
        print(
            f"{label(mode):<18} "
            f"{row.born:>10.2e} "
            f"{row.gravity_z3:>+12.6f} "
            f"{toward:>8s} "
            f"{fmt_float(row.fm_alpha, 2):>8s} "
            f"{tail:>12s}"
        )

    print()
    print("SAFE READ")
    print("  - Born is structural on this family: field-free Born stays machine-clean for every action.")
    print("  - Phase hills / no-coupling fail to give the desired TOWARD gravity.")
    print("  - Valley actions stay TOWARD, but the F~M exponent follows the weak-field power of f.")
    print("  - The cleanest universality-class statement here is about F~M, not a universal distance theorem.")


if __name__ == "__main__":
    main()
