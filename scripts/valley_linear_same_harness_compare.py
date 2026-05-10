#!/usr/bin/env python3
"""Same-harness spent-delay vs valley-linear core comparison on the 3D 1/L^2 family.

This is a bounded action-fork comparison, not a promoted flagship harness.

It keeps fixed:
  - the 3D ordered dense lattice family
  - the 1/L^2 kernel with h^2 measure
  - the slit geometry
  - the detector readout

It changes only the action law:
  - spent-delay: S = dl - sqrt(dl^2 - L^2)
  - valley-linear: S = L * (1 - f)

Measured here:
  - Born
  - k=0
  - F~M alpha
  - gravity sign at z=3
  - distance tail

The heavier MI / decoherence / multi-L checks stay in the full action-specific
card scripts and are not replayed here.
"""

from __future__ import annotations

# Heavy compute / lattice-sweep runner — exceeds the 120s default audit
# timeout. Measured wall-clock at 2026-05-10: ~229s on the canonical
# Python 3.12 machine; declaring 300s here gives a comfortable margin.
# Without this declaration the audit lane caches an empty stdout under
# `status: timeout`, blocking the audit verdict.
AUDIT_TIMEOUT_SEC = 300

import math
import time
from dataclasses import dataclass

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc


BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 10
PHYS_L = 12
H = 0.25
MAX_D_PHYS = 3
STRENGTH = 5e-5


@dataclass
class Result:
    name: str
    born: float
    k0: float
    fm_alpha: float
    grav: float
    toward_count: int
    tail_slope: float
    tail_r2: float
    peak_z: int


class Lattice3D:
    def __init__(self, phys_l: int, phys_w: int, h: float):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw**2
        self.n = self.nl * self.npl
        self._hm = h * h
        self._nw = nw

        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
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
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int], action_mode: str) -> np.ndarray:
        amps = np.zeros(self.n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0

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
                if action_mode == "spent_delay":
                    dl = L * (1 + lf)
                    ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
                    act = dl - ret
                elif action_mode == "valley_linear":
                    act = L * (1 - lf)
                else:  # pragma: no cover - internal guard
                    raise ValueError(f"unknown action_mode={action_mode}")

                c = a[nz] * np.exp(1j * k * act) * w * self._hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)

        return amps


def make_field(lat: Lattice3D, z_mass_phys: int, strength: float) -> np.ndarray:
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n)
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx) ** 2 + (lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


def setup_slits(lat: Lattice3D) -> tuple[list[int], list[int], set[int], int]:
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return sa, sb, blocked, bl


def fit_power(x_data: list[float], y_data: list[float]) -> tuple[float, float]:
    lx = np.log(np.array(x_data, dtype=float))
    ly = np.log(np.array(y_data, dtype=float))
    mx = lx.mean()
    my = ly.mean()
    sxx = np.sum((lx - mx) ** 2)
    sxy = np.sum((lx - mx) * (ly - my))
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx))) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def measure_action(lat: Lattice3D, action_mode: str) -> Result:
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    sa, sb, blocked, bl = setup_slits(lat)
    field_f = np.zeros(lat.n)
    pos = lat.pos

    af = lat.propagate(field_f, K, blocked, action_mode)
    pf = sum(abs(af[d]) ** 2 for d in det)
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf

    # Born
    upper = sorted(
        [lat.nmap[(bl, iy, iz)] for iy in range(-lat.hw, lat.hw + 1) for iz in range(-lat.hw, lat.hw + 1)
         if (bl, iy, iz) in lat.nmap and pos[lat.nmap[(bl, iy, iz)], 1] > 1],
        key=lambda i: pos[i, 1],
    )
    lower = sorted(
        [lat.nmap[(bl, iy, iz)] for iy in range(-lat.hw, lat.hw + 1) for iz in range(-lat.hw, lat.hw + 1)
         if (bl, iy, iz) in lat.nmap and pos[lat.nmap[(bl, iy, iz)], 1] < -1],
        key=lambda i: -pos[i, 1],
    )
    middle = [
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap and abs(pos[lat.nmap[(bl, iy, iz)], 1]) <= 1 and abs(pos[lat.nmap[(bl, iy, iz)], 2]) <= 1
    ]
    born = float("nan")
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        bi = set(sa + sb) | blocked
        # reconstruct barrier layer nodes
        barrier_nodes = {
            lat.nmap[(bl, iy, iz)]
            for iy in range(-lat.hw, lat.hw + 1)
            for iz in range(-lat.hw, lat.hw + 1)
            if (bl, iy, iz) in lat.nmap
        }
        all_s = set(s_a + s_b + s_c)
        other = barrier_nodes - all_s
        probs = {}
        for key, open_set in [("abc", all_s), ("ab", set(s_a + s_b)), ("ac", set(s_a + s_c)),
                              ("bc", set(s_b + s_c)), ("a", set(s_a)), ("b", set(s_b)), ("c", set(s_c))]:
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
        born = I3 / P if P > 1e-30 else float("nan")

    # k=0
    field_m3 = make_field(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked, action_mode)
    af0 = lat.propagate(field_f, 0.0, blocked, action_mode)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    k0 = (
        sum(abs(am0[d]) ** 2 * pos[d, 2] for d in det) / pm0
        - sum(abs(af0[d]) ** 2 * pos[d, 2] for d in det) / pf0
        if pm0 > 1e-30 and pf0 > 1e-30
        else 0.0
    )

    # F~M
    m_data = []
    g_data = []
    for s in [1e-6, 5e-6, 2e-5, 5e-5]:
        fm = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked, action_mode)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)
    fm_alpha = float("nan")
    if len(m_data) >= 3:
        fm_alpha, _ = fit_power(m_data, g_data)

    # gravity z=3
    am3 = lat.propagate(field_m3, K, blocked, action_mode)
    pm3 = sum(abs(am3[d]) ** 2 for d in det)
    grav = sum(abs(am3[d]) ** 2 * pos[d, 2] for d in det) / pm3 - zf if pm3 > 1e-30 else 0.0

    # distance tail
    b_data = []
    d_data = []
    for z_mass in range(2, 10):
        fm = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked, action_mode)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                b_data.append(z_mass)
                d_data.append(delta)
    d_arr = np.array(d_data)
    peak_i = int(np.argmax(d_arr))
    peak_z = b_data[peak_i]
    tail_slope, tail_r2 = fit_power(b_data[peak_i:], d_data[peak_i:])

    return Result(
        name=action_mode,
        born=born,
        k0=k0,
        fm_alpha=fm_alpha,
        grav=grav,
        toward_count=len(b_data),
        tail_slope=tail_slope,
        tail_r2=tail_r2,
        peak_z=peak_z,
    )


def main() -> None:
    started = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    print("=" * 88)
    print("SAME-HARNESS ACTION COMPARISON: spent-delay vs valley-linear")
    print("  fixed family: 3D ordered dense lattice, 1/L^2 kernel, h^2 measure")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}, nodes={lat.n:,}")
    print("=" * 88)
    print()

    results = []
    for mode in ["spent_delay", "valley_linear"]:
        t0 = time.time()
        res = measure_action(lat, mode)
        results.append(res)
        print(f"{mode}: done in {time.time() - t0:.1f}s")

    print()
    print(
        f"{'action':<16} {'Born':>10} {'k=0':>10} {'F~M':>8} "
        f"{'gravity':>10} {'TOWARD':>8} {'tail':>22}"
    )
    print("-" * 108)
    for r in results:
        label = "spent-delay" if r.name == "spent_delay" else "valley-linear"
        tail = f"z>={r.peak_z}: {r.tail_slope:.2f} (R²={r.tail_r2:.3f})"
        print(
            f"{label:<16} {r.born:>10.2e} {r.k0:>+10.2e} "
            f"{r.fm_alpha:>8.2f} {r.grav:>+10.6f} "
            f"{f'{r.toward_count}/8':>8} {tail:>22}"
        )

    print()
    print("READ:")
    print("  - This is a bounded same-family action-fork comparison.")
    print("  - If valley-linear wins here, that does not preserve any spent-delay flagship claim automatically.")
    print("  - Convergence under refinement still needs its own frozen artifact chain.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")


if __name__ == "__main__":
    main()
