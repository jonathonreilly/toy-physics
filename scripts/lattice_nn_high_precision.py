#!/usr/bin/env python3
"""High-precision raw nearest-neighbor lattice continuation.

This script re-runs the raw nearest-neighbor lattice kernel from
`scripts/lattice_nn_continuum.py` using arbitrary-precision arithmetic.

The goal is intentionally narrow:
- keep the raw kernel unchanged
- keep the same observables
- try one more refinement step to `h = 0.125` without any rescaling trick

The safe interpretation is not "continuum proven" but:
- does the Born-clean refinement trend through `h = 0.25` extend one step
  further in a raw high-precision implementation?
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import mpmath as mp
except ImportError as exc:  # pragma: no cover - helpful runtime message
    raise SystemExit(
        "mpmath is required for the high-precision continuation. "
        "Create a local virtualenv and install mpmath there."
    ) from exc


BETA_STR = "0.8"
K_PHYS_STR = "5.0"
LAM_STR = "10.0"
N_YBINS = 8
PHYS_W_STR = "20.0"
PHYS_L_STR = "40.0"
SLIT_Y_STR = "3.0"
MASS_Y_STR = "8.0"


def generate_nn_lattice(spacing: mp.mpf):
    """Lattice with exactly 3 nearest-neighbor forward edges per node."""
    phys_l = mp.mpf(PHYS_L_STR)
    phys_w = mp.mpf(PHYS_W_STR)
    nl = int(mp.floor(phys_l / spacing)) + 1
    hw = int(mp.floor(phys_w / spacing))
    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(nl):
        x = mp.mpf(layer) * spacing
        for iy in range(-hw, hw + 1):
            y = mp.mpf(iy) * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx

    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for diy in (-1, 0, 1):
                iyn = iy + diy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)

    order = list(range(len(pos)))
    order.sort(key=lambda i: pos[i][0])
    return pos, dict(adj), nl, hw, nmap, order


def propagate(pos, adj, field, k, blocked, n, order):
    beta = mp.mpf(BETA_STR)
    amps = [mp.mpc(0)] * n
    src = next(
        i for i, (x, y) in enumerate(pos)
        if abs(x) < mp.mpf("1e-40") and abs(y) < mp.mpf("1e-40")
    )
    amps[src] = mp.mpc(1)

    for i in order:
        if abs(amps[i]) < mp.mpf("1e-80") or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx = x2 - x1
            dy = y2 - y1
            L = mp.sqrt(dx * dx + dy * dy)
            if L < mp.mpf("1e-40"):
                continue
            lf = mp.mpf("0.5") * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = mp.sqrt(max(dl * dl - L * L, mp.mpf("0")))
            act = dl - ret
            theta = mp.atan2(abs(dy), max(dx, mp.mpf("1e-40")))
            w = mp.e ** (-beta * theta * theta)
            ea = mp.e ** (1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_full(spacing, dps):
    with mp.workdps(dps):
        k_phys = mp.mpf(K_PHYS_STR)
        lam = mp.mpf(LAM_STR)
        phys_w = mp.mpf(PHYS_W_STR)
        slit_y = mp.mpf(SLIT_Y_STR)
        mass_y = mp.mpf(MASS_Y_STR)
        spacing = mp.mpf(str(spacing))
        pos, adj, nl, hw, nmap, order = generate_nn_lattice(spacing)
        n = len(pos)
        det_layer = nl - 1
        det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1)
               if (det_layer, iy) in nmap]
        bl = nl // 3
        gl = 2 * nl // 3

        slit_iy = max(1, int(mp.nint(slit_y / spacing)))
        bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
        sa_range = range(slit_iy, min(slit_iy + max(2, int(mp.nint(2 / spacing))), hw + 1))
        sb_range = range(-min(slit_iy + max(1, int(mp.nint(1 / spacing))), hw), -slit_iy + 1)
        sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
        sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
        if not sa or not sb:
            return None
        blocked = set(bi) - set(sa + sb)
        field_f = [mp.mpf("0")] * n

        mass_iy = int(mp.nint(mass_y / spacing))
        mass_idx = nmap.get((gl, mass_iy))
        if mass_idx is None:
            return None
        phys_strength = mp.mpf("0.0005")
        field_m = [mp.mpf("0")] * n
        mx, my = pos[mass_idx]
        for i in range(n):
            ix, iy = pos[i]
            r = mp.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + mp.mpf("0.1")
            field_m[i] = phys_strength / r

        af = propagate(pos, adj, field_f, k_phys, blocked, n, order)
        am = propagate(pos, adj, field_m, k_phys, blocked, n, order)
        pf = mp.fsum(abs(af[d]) ** 2 for d in det)
        pm = mp.fsum(abs(am[d]) ** 2 for d in det)
        if pf < mp.mpf("1e-80") or pm < mp.mpf("1e-80"):
            return None
        yf = mp.fsum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
        ym = mp.fsum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
        gravity = ym - yf

        am0 = propagate(pos, adj, field_m, mp.mpf("0"), blocked, n, order)
        af0 = propagate(pos, adj, field_f, mp.mpf("0"), blocked, n, order)
        pm0 = mp.fsum(abs(am0[d]) ** 2 for d in det)
        pf0 = mp.fsum(abs(af0[d]) ** 2 for d in det)
        gk0 = mp.mpf("0")
        if pm0 > mp.mpf("1e-80") and pf0 > mp.mpf("1e-80"):
            gk0 = (
                mp.fsum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
                - mp.fsum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0
            )

        pa = propagate(pos, adj, field_f, k_phys, blocked | set(sb), n, order)
        pb = propagate(pos, adj, field_f, k_phys, blocked | set(sa), n, order)
        bw = mp.mpf("2") * (phys_w + spacing) / N_YBINS
        prob_a = [mp.mpf("0")] * N_YBINS
        prob_b = [mp.mpf("0")] * N_YBINS
        for d in det:
            b2 = max(
                0,
                min(N_YBINS - 1, int((pos[d][1] + phys_w + spacing) / bw)),
            )
            prob_a[b2] += abs(pa[d]) ** 2
            prob_b[b2] += abs(pb[d]) ** 2
        na = mp.fsum(prob_a)
        nb = mp.fsum(prob_b)
        MI = mp.mpf("0")
        if na > mp.mpf("1e-80") and nb > mp.mpf("1e-80"):
            pa_n = [p / na for p in prob_a]
            pb_n = [p / nb for p in prob_b]
            H = mp.mpf("0")
            Hc = mp.mpf("0")
            for b3 in range(N_YBINS):
                pm2 = mp.mpf("0.5") * pa_n[b3] + mp.mpf("0.5") * pb_n[b3]
                if pm2 > mp.mpf("1e-80"):
                    H -= pm2 * mp.log(pm2, 2)
                if pa_n[b3] > mp.mpf("1e-80"):
                    Hc -= mp.mpf("0.5") * pa_n[b3] * mp.log(pa_n[b3], 2)
                if pb_n[b3] > mp.mpf("1e-80"):
                    Hc -= mp.mpf("0.5") * pb_n[b3] * mp.log(pb_n[b3], 2)
            MI = H - Hc

        env_depth = max(1, int(mp.nint(nl / 6)))
        st = bl + 1
        sp = min(nl - 1, st + env_depth)
        mid = []
        for l in range(st, sp):
            mid.extend([nmap[(l, iy)] for iy in range(-hw, hw + 1) if (l, iy) in nmap])
        ba = [mp.mpf("0")] * N_YBINS
        bb = [mp.mpf("0")] * N_YBINS
        for m in mid:
            b2 = max(
                0,
                min(N_YBINS - 1, int((pos[m][1] + phys_w + spacing) / bw)),
            )
            ba[b2] += pa[m]
            bb[b2] += pb[m]
        S = mp.fsum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = mp.fsum(abs(a) ** 2 for a in ba)
        NB = mp.fsum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > mp.mpf("0") else mp.mpf("0")
        Dcl = mp.e ** (-lam ** 2 * Sn)
        rho = {}
        for d1 in det:
            for d2 in det:
                rho[(d1, d2)] = (
                    pa[d1].conjugate() * pa[d2]
                    + pb[d1].conjugate() * pb[d2]
                    + Dcl * pa[d1].conjugate() * pb[d2]
                    + Dcl * pb[d1].conjugate() * pa[d2]
                )
        tr = mp.fsum(rho[(d, d)] for d in det).real
        pur_cl = mp.mpf("1")
        if tr > mp.mpf("1e-80"):
            for key in rho:
                rho[key] /= tr
            pur_cl = mp.fsum(abs(v) ** 2 for v in rho.values()).real

        da = {d: abs(pa[d]) ** 2 for d in det}
        db = {d: abs(pb[d]) ** 2 for d in det}
        na2 = mp.fsum(da.values())
        nb2 = mp.fsum(db.values())
        dtv = mp.mpf("0")
        if na2 > mp.mpf("1e-80") and nb2 > mp.mpf("1e-80"):
            dtv = mp.mpf("0.5") * mp.fsum(
                abs(da[d] / na2 - db[d] / nb2) for d in det
            )

        born = mp.nan
        upper = sorted([i for i in bi if pos[i][1] > spacing], key=lambda i: pos[i][1])
        lower = sorted([i for i in bi if pos[i][1] < -spacing], key=lambda i: -pos[i][1])
        middle = [i for i in bi if abs(pos[i][1]) <= spacing]
        if upper and lower and middle:
            s_a = [upper[0]]
            s_b = [lower[0]]
            s_c = [middle[0]]
            all_s = set(s_a + s_b + s_c)
            other = set(bi) - all_s
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
                bl2 = other | (all_s - open_set)
                a = propagate(pos, adj, field_f, k_phys, bl2, n, order)
                probs[key] = [abs(a[d]) ** 2 for d in det]
            I3 = mp.mpf("0")
            P = mp.mpf("0")
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
            born = I3 / P if P > mp.mpf("1e-80") else mp.nan

        return {
            "h": spacing,
            "n": n,
            "nl": nl,
            "npl": 2 * hw + 1,
            "gravity": gravity,
            "gk0": gk0,
            "MI": MI,
            "pur_cl": pur_cl,
            "dtv": dtv,
            "born": born,
        }


def fmt(x, digits=6):
    if x is None:
        return "None"
    if isinstance(x, str):
        return x
    try:
        if mp.isnan(x):
            return "nan"
    except Exception:
        pass
    try:
        if mp.isinf(x):
            return str(x)
    except Exception:
        pass
    try:
        return mp.nstr(x, digits)
    except Exception:
        return str(x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=120)
    parser.add_argument("--spacings", nargs="*", type=float, default=[0.25, 0.125])
    args = parser.parse_args()

    print("=" * 95)
    print("HIGH-PRECISION NEAREST-NEIGHBOR LATTICE CONTINUATION")
    print(f"  raw kernel, mpmath dps={args.dps}")
    print(f"  physical: W={PHYS_W_STR}, L={PHYS_L_STR}, k={K_PHYS_STR}, field_strength=0.0005")
    print("=" * 95)
    print()

    header = [
        "h", "nodes", "layers", "gravity", "MI", "1-pur", "d_TV", "Born", "k=0"
    ]
    print("\t".join(header))
    print("-" * 95)
    for spacing in args.spacings:
        row = measure_full(spacing, args.dps)
        if row is None:
            print(f"{spacing}\tNO_RESULT")
            continue
        one_minus_pur = mp.mpf("1") - row["pur_cl"]
        print(
            "\t".join(
                [
                    fmt(row["h"], 6),
                    str(row["n"]),
                    str(row["nl"]),
                    fmt(row["gravity"], 6),
                    fmt(row["MI"], 6),
                    fmt(one_minus_pur, 6),
                    fmt(row["dtv"], 6),
                    fmt(row["born"], 6),
                    fmt(row["gk0"], 6),
                ]
            )
        )


if __name__ == "__main__":
    main()
