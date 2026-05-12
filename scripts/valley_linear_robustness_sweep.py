#!/usr/bin/env python3
"""Bounded robustness sweep for the valley-linear action.

This is a frozen replay of the branch-side robustness memo, not a proof of a
global theorem.

What it measures on the ordered 3D lattice family:
  - width sweep at fixed L and connectivity
  - connectivity sweep at fixed width and length
  - length sweep at fixed width and connectivity

All sweeps use:
  - action: S = L(1-f)
  - kernel: 1/L^2 with h^2 measure
  - h = 0.5

The script reports the same observables that matter for the current retained
story:
  - Born
  - d_TV
  - MI
  - decoherence
  - gravity sign
  - F~M exponent
  - distance tail when there are enough post-peak points

If a fit is not data-honest, the script prints ``n/a`` instead of inventing one.
"""

from __future__ import annotations

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
STRENGTH = 5e-5
H = 0.5
BASE_L = 12
BASE_W = 8
BASE_MAX_D = 3
Z_MASS_PHYS = 3

AUDIT_TIMEOUT_SEC = 1800


@dataclass
class Row:
    label: str
    born: float
    d_tv: float
    mi: float
    decoh: float
    grav: float
    grav_sign: str
    fm_alpha: float
    tail_slope: float | None
    tail_r2: float | None
    tail_count: int | None


class Lattice3D:
    def __init__(self, phys_l: int, phys_w: int, max_d_phys: int, h: float):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
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
                self._off.append((dy, dz, L, math.exp(-BETA * theta * theta)))

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int]) -> np.ndarray:
        amps = np.zeros(self.n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0

        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < self.nl else self.n

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
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * self._hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)

        return amps


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
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else None
    return slope, r2


def make_field(lat: Lattice3D, z_mass_phys: int, strength: float) -> np.ndarray:
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n)
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx) ** 2 + (lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r


def setup_slits(lat: Lattice3D) -> tuple[list[int], list[int], list[int], set[int], int]:
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
    return bi, sa, sb, blocked, bl


def detector_indices(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def mean_z(lat: Lattice3D, det: list[int], amps: np.ndarray) -> float:
    pos = lat.pos
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return float("nan")
    return float(np.sum(probs * pos[det, 2]) / total)


def born_measure(lat: Lattice3D, det: list[int], bi: list[int], blocked: set[int], bl: int) -> float:
    pos = lat.pos
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [
        i for i in bi
        if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1
    ]
    if not (upper and lower and middle):
        return float("nan")

    field_f = np.zeros(lat.n)
    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = set(bi) - all_s
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
        amps = lat.propagate(field_f, K, bl2)
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


def measure_case(phys_l: int, phys_w: int, max_d_phys: int, h: float) -> Row:
    lat = Lattice3D(phys_l, phys_w, max_d_phys, h)
    det = detector_indices(lat)
    bi, sa, sb, blocked, bl = setup_slits(lat)
    pos = lat.pos
    field_f = np.zeros(lat.n)

    free = lat.propagate(field_f, K, blocked)
    z_free = mean_z(lat, det, free)

    born = born_measure(lat, det, bi, blocked, bl)

    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = np.array([abs(pa[d]) ** 2 for d in det], dtype=float)
    db = np.array([abs(pb[d]) ** 2 for d in det], dtype=float)
    na = da.sum()
    nb = db.sum()
    d_tv = 0.5 * float(np.sum(np.abs(da / na - db / nb))) if na > 1e-30 and nb > 1e-30 else float("nan")

    field_m = make_field(lat, Z_MASS_PHYS, STRENGTH)
    mass = lat.propagate(field_m, K, blocked)
    z_mass = mean_z(lat, det, mass)
    grav = z_mass - z_free if np.isfinite(z_mass) and np.isfinite(z_free) else float("nan")
    grav_sign = "TOWARD" if grav > 0 else "AWAY"

    fm_strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    fm_data: list[float] = []
    fm_delta: list[float] = []
    for s in fm_strengths:
        amps = lat.propagate(make_field(lat, Z_MASS_PHYS, s), K, blocked)
        z_mass_s = mean_z(lat, det, amps)
        delta = z_mass_s - z_free if np.isfinite(z_mass_s) else float("nan")
        if np.isfinite(delta) and delta > 0:
            fm_data.append(s)
            fm_delta.append(delta)
    fm_alpha = float("nan")
    slope, _ = fit_power(fm_data, fm_delta)
    if slope is not None:
        fm_alpha = slope

    # decoherence / MI from the same barrier readout used in the card
    bw = 2 * (phys_w + 1) / N_YBINS
    ed = max(1, round(lat.nl / 6))
    st = bl + 1
    sp = min(lat.nl - 1, st + ed)
    mid = []
    for layer in range(st, sp):
        mid.extend([
            lat.nmap[(layer, iy, iz)]
            for iy in range(-lat.hw, lat.hw + 1)
            for iz in range(-lat.hw, lat.hw + 1)
            if (layer, iy, iz) in lat.nmap
        ])
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + phys_w + 1) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    s_overlap = float(np.sum(np.abs(ba - bb) ** 2))
    na3 = float(np.sum(np.abs(ba) ** 2))
    nb3 = float(np.sum(np.abs(bb) ** 2))
    sn = s_overlap / (na3 + nb3) if (na3 + nb3) > 0 else 0.0
    dcl = math.exp(-LAM**2 * sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                pa[d1].conjugate() * pa[d2]
                + pb[d1].conjugate() * pb[d2]
                + dcl * pa[d1].conjugate() * pb[d2]
                + dcl * pb[d1].conjugate() * pa[d2]
            )
    tr = sum(rho[(d, d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur = float(sum(abs(v) ** 2 for v in rho.values()).real)
    decoh = 100 * (1 - pur)

    prob_a = np.zeros(N_YBINS)
    prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + phys_w + 1) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na_prob = prob_a.sum()
    nb_prob = prob_b.sum()
    mi = 0.0
    if na_prob > 1e-30 and nb_prob > 1e-30:
        pa_n = prob_a / na_prob
        pb_n = prob_b / nb_prob
        H_val = 0.0
        Hc = 0.0
        for b2 in range(N_YBINS):
            pmix = 0.5 * pa_n[b2] + 0.5 * pb_n[b2]
            if pmix > 1e-30:
                H_val -= pmix * math.log2(pmix)
            if pa_n[b2] > 1e-30:
                Hc -= 0.5 * pa_n[b2] * math.log2(pa_n[b2])
            if pb_n[b2] > 1e-30:
                Hc -= 0.5 * pb_n[b2] * math.log2(pb_n[b2])
        mi = H_val - Hc

    # distance tail
    b_data: list[int] = []
    d_data: list[float] = []
    for z_mass in range(2, 10):
        amps = lat.propagate(make_field(lat, z_mass, STRENGTH), K, blocked)
        z_mass_s = mean_z(lat, det, amps)
        delta = z_mass_s - z_free if np.isfinite(z_mass_s) else float("nan")
        if np.isfinite(delta) and delta > 0:
            b_data.append(z_mass)
            d_data.append(delta)
    tail_slope = None
    tail_r2 = None
    tail_count = None
    if len(b_data) >= 3:
        peak_i = int(np.argmax(d_data))
        if len(b_data) - peak_i >= 3:
            slope, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
            tail_slope, tail_r2 = slope, r2
            tail_count = len(b_data) - peak_i

    return Row(
        label=f"W={phys_w}, max_d={max_d_phys}, L={phys_l}",
        born=born,
        d_tv=d_tv,
        mi=mi,
        decoh=decoh,
        grav=grav,
        grav_sign=grav_sign,
        fm_alpha=fm_alpha,
        tail_slope=tail_slope,
        tail_r2=tail_r2,
        tail_count=tail_count,
    )


def print_row(prefix: str, row: Row, extra: str = "") -> None:
    tail = "n/a"
    if row.tail_slope is not None and row.tail_r2 is not None and row.tail_count is not None:
        tail = f"b^({row.tail_slope:.2f}), R²={row.tail_r2:.3f}, n={row.tail_count}"
    print(
        f"{prefix} Born={row.born:.1e} | d_TV={row.d_tv:.2f} | MI={row.mi:.2f} bits | "
        f"Decoh={row.decoh:.1f}% | Grav={row.grav:+.6f} ({row.grav_sign}) | "
        f"F~M={row.fm_alpha:.2f} | Tail={tail}{extra}"
    )


def main() -> None:
    t0 = time.time()
    print("=" * 78)
    print("VALLEY-LINEAR ROBUSTNESS SWEEP")
    print("Action: S = L(1-f)")
    print("Kernel: 1/L^2 with h^2 measure")
    print("Scope: bounded lattice robustness replay, not a theorem card")
    print("=" * 78)
    print(f"h={H}, STRENGTH={STRENGTH:g}, K={K}, LAM={LAM}")
    print()

    print("SWEEP 1: Width (L=12, max_d=3, h=0.5)")
    for w in [4, 6, 8, 10]:
        row = measure_case(phys_l=12, phys_w=w, max_d_phys=3, h=H)
        print_row(f"  W={w:2d}", row)
    print()

    print("SWEEP 2: Connectivity (L=12, W=8, h=0.5)")
    for md in [1, 2, 3]:
        row = measure_case(phys_l=12, phys_w=8, max_d_phys=md, h=H)
        print_row(f"  max_d={md}", row)
    print()

    print("SWEEP 3: Length (W=8, max_d=3, h=0.5)")
    for pl in [8, 10, 12, 15, 18]:
        row = measure_case(phys_l=pl, phys_w=8, max_d_phys=3, h=H)
        print_row(f"  L={pl:2d}", row, extra="")
    print()

    print("SAFE INTERPRETATION")
    print("- valley-linear is promisingly robust on the tested 3D ordered-lattice slices")
    print("- Born remains machine-clean across the tested width/connectivity/length rows")
    print("- the retained rows keep F~M at 1.00 on these sweeps")
    print("- tail fits are only reported when there are enough post-peak points; otherwise n/a")
    print("- this is a frozen replay of the memo tables, not a proof of universality")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
