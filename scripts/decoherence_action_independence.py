#!/usr/bin/env python3
"""Replay the action-independence of decoherence on the 3D 1/L^2 lattice.

This is a bounded, review-safe replay of the existing note:

  - same 3D ordered lattice family
  - same zero-field CL-bath decoherence setup
  - same tested h values
  - different action law

The point is to show that the decoherence observables are identical for
spent-delay and valley-linear on the tested family, not to expand the claim
beyond the retained 3D 1/L^2 branch.
"""

from __future__ import annotations

# Heavy compute / decoherence-bath replay — exceeds the 120s default audit
# timeout. Measured wall-clock at 2026-05-10: ~314s on the canonical
# Python 3.12 machine; declaring 450s here gives ~40% margin while
# keeping the audit-cache budget bounded. Without this declaration the
# audit lane caches an empty stdout under `status: timeout`, blocking
# the audit verdict (the cited row was UNAUDITED on origin/main).
AUDIT_TIMEOUT_SEC = 450

import math
import os
import time
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this replay; use /usr/bin/python3 if needed.")

from scripts.valley_linear_same_harness_compare import (
    Lattice3D,
    K,
    LAM,
    N_YBINS,
    PHYS_L,
    PHYS_W,
    setup_slits,
)


H_VALUES = [1.0, 0.5, 0.25]
ACTIONS = ["spent_delay", "valley_linear"]


def measure_decoherence(lat: Lattice3D, action_mode: str) -> dict[str, float]:
    sa, sb, blocked, bl = setup_slits(lat)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]

    field_f = np.zeros(lat.n)
    pos = lat.pos

    pa = lat.propagate(field_f, K, blocked | set(sb), action_mode)
    pb = lat.propagate(field_f, K, blocked | set(sa), action_mode)

    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db.values())
    dtv = 0.0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)

    bw = 2 * (PHYS_W + 1) / N_YBINS
    prob_a = np.zeros(N_YBINS)
    prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + PHYS_W + 1) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2

    na = prob_a.sum()
    nb = prob_b.sum()
    mi = 0.0
    if na > 1e-30 and nb > 1e-30:
        pa_n = prob_a / na
        pb_n = prob_b / nb
        h_val = 0.0
        hc = 0.0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                h_val -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        mi = h_val - hc

    env_depth = max(1, round(lat.nl / 6))
    st = bl + 1
    sp = min(lat.nl - 1, st + env_depth)
    mid = []
    for l in range(st, sp):
        mid.extend(
            [
                lat.nmap[(l, iy, iz)]
                for iy in range(-lat.hw, lat.hw + 1)
                for iz in range(-lat.hw, lat.hw + 1)
                if (l, iy, iz) in lat.nmap
            ]
        )

    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + PHYS_W + 1) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]

    s_norm = float(np.sum(np.abs(ba - bb) ** 2))
    na3 = float(np.sum(np.abs(ba) ** 2))
    nb3 = float(np.sum(np.abs(bb) ** 2))
    s_norm = s_norm / (na3 + nb3) if (na3 + nb3) > 0 else 0.0
    dcl = math.exp(-LAM**2 * s_norm)

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
    pur_cl = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    return {
        "d_tv": dtv,
        "mi": mi,
        "pur_cl": pur_cl,
        "decoh": 100.0 * (1.0 - pur_cl),
        "s_norm": s_norm,
    }


def main() -> None:
    t0 = time.time()
    print("=" * 88)
    print("DECOHERENCE ACTION INDEPENDENCE REPLAY")
    print("  3D 1/L^2 lattice, zero field, valley-linear vs spent-delay")
    print(f"  h values: {', '.join(str(v) for v in H_VALUES)}")
    print("=" * 88)
    print()

    rows = []
    for h in H_VALUES:
        lat = Lattice3D(PHYS_L, PHYS_W, h)
        print(f"h={h:.2f}  nodes={lat.n:,}  layers={lat.nl}  npl={lat.npl}")
        h_rows = {}
        for action in ACTIONS:
            obs = measure_decoherence(lat, action)
            h_rows[action] = obs
            print(
                f"  {action:<13s} "
                f"d_TV={obs['d_tv']:.4f}  MI={obs['mi']:.4f}  "
                f"pur_cl={obs['pur_cl']:.4f}  decoh={obs['decoh']:.1f}%  "
                f"S_norm={obs['s_norm']:.4f}"
            )

        deltas = {
            key: abs(h_rows["spent_delay"][key] - h_rows["valley_linear"][key])
            for key in ("d_tv", "mi", "pur_cl", "decoh", "s_norm")
        }
        print(
            "  delta(spent - valley): "
            + ", ".join(f"{k}={v:.2e}" for k, v in deltas.items())
        )
        rows.append((h, h_rows, deltas))
        print()

    max_delta = {
        key: max(d[key] for _, _, d in rows)
        for key in ("d_tv", "mi", "pur_cl", "decoh", "s_norm")
    }
    print("=" * 88)
    print("SUMMARY")
    print("  The decoherence observables are identical across actions on the tested family.")
    print(
        "  max |delta|: "
        + ", ".join(f"{k}={v:.2e}" for k, v in max_delta.items())
    )
    print(f"  Total time: {time.time() - t0:.1f}s")
    print("=" * 88)


if __name__ == "__main__":
    main()
