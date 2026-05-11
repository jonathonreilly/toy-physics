#!/usr/bin/env python3
"""Bounded no-go runner for the top-quark QFP attractor route.

This runner tests whether generic UV values of y_t(M_Pl) flow under a
standard one-loop SM top-Yukawa RGE to a top mass near the external target,
using the current framework electroweak-scale coupling packet. It does not
use the lattice Ward boundary as input.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from canonical_plaquette_surface import (  # noqa: E402
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (D)" if "external" in label.lower() or "target" in label.lower() else "PASS (C)"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def beta_1loop(_t: float, y: np.ndarray) -> list[float]:
    g1, g2, g3, yt = y
    fac = 1.0 / (16.0 * math.pi**2)
    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0
    beta_g1 = b1 * g1**3
    beta_g2 = b2 * g2**3
    beta_g3 = b3 * g3**3
    beta_yt = yt * (
        9.0 / 2.0 * yt**2
        - 8.0 * g3**2
        - 9.0 / 4.0 * g2**2
        - 17.0 / 20.0 * g1**2
    )
    return [fac * beta_g1, fac * beta_g2, fac * beta_g3, fac * beta_yt]


def evolve(y0: list[float], t0: float, t1: float) -> np.ndarray:
    sol = solve_ivp(
        beta_1loop,
        (t0, t1),
        y0,
        method="RK45",
        rtol=1e-9,
        atol=1e-11,
        max_step=0.5,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1]


def main() -> int:
    print("Top-quark QFP attractor route no-go")

    # Framework-side coupling packet.
    m_pl = 1.2209e19
    alpha_s_v = CANONICAL_ALPHA_S_V
    alpha_lm = CANONICAL_ALPHA_LM
    v_ew = m_pl * (7.0 / 8.0) ** 0.25 * alpha_lm**16
    g3_v = math.sqrt(4.0 * math.pi * alpha_s_v)

    # Standard electroweak coupling inputs used only for this bounded RGE probe.
    m_z = 91.1876
    alpha_em_mz = 1.0 / 127.951
    sin2_tw_mz = 0.23122
    alpha_1_mz_gut = (5.0 / 3.0) * alpha_em_mz / (1.0 - sin2_tw_mz)
    alpha_2_mz = alpha_em_mz / sin2_tw_mz
    t_v = math.log(v_ew)
    t_z = math.log(m_z)
    inv_a1_v = 1.0 / alpha_1_mz_gut + (-41.0 / 10.0) / (2.0 * math.pi) * (t_v - t_z)
    inv_a2_v = 1.0 / alpha_2_mz + (19.0 / 6.0) / (2.0 * math.pi) * (t_v - t_z)
    g1_v = math.sqrt(4.0 * math.pi / inv_a1_v)
    g2_v = math.sqrt(4.0 * math.pi / inv_a2_v)

    t_pl = math.log(m_pl)
    target_mt = 172.69  # external comparator, not derivation input

    print(f"canonical plaquette={CANONICAL_PLAQUETTE:.6f}, u0={CANONICAL_U0:.6f}")
    print(f"alpha_bare={CANONICAL_ALPHA_BARE:.9f}, alpha_s(v)={alpha_s_v:.9f}")
    print(f"v_ew={v_ew:.6f} GeV, g1(v)={g1_v:.6f}, g2(v)={g2_v:.6f}, g3(v)={g3_v:.6f}")

    y_qfp_bracket = math.sqrt(
        (8.0 * g3_v**2 + 9.0 / 4.0 * g2_v**2 + 17.0 / 20.0 * g1_v**2)
        / (9.0 / 2.0)
    )
    mt_qfp_bracket = y_qfp_bracket * v_ew / math.sqrt(2.0)
    check(
        "QFP sign/bracket structure exists",
        y_qfp_bracket > 1.0,
        f"instantaneous bracket y_qfp={y_qfp_bracket:.4f}, mt={mt_qfp_bracket:.2f} GeV",
    )

    # Run gauge couplings up to M_Pl once; 1-loop gauge beta is independent of yt.
    g_pl = evolve([g1_v, g2_v, g3_v, 1.0], t_v, t_pl)[:3]
    uv_grid = np.array([0.5, 0.7, 1.0, 2.0, 5.0, 10.0])
    rows: list[tuple[float, float, float, float]] = []
    for yt_pl in uv_grid:
        y_v = evolve([float(g_pl[0]), float(g_pl[1]), float(g_pl[2]), float(yt_pl)], t_pl, t_v)
        yt_v = float(y_v[3])
        mt = yt_v * v_ew / math.sqrt(2.0)
        rel = (mt - target_mt) / target_mt
        rows.append((float(yt_pl), yt_v, mt, rel))

    for yt_pl, yt_v, mt, rel in rows:
        print(f"scan yt_pl={yt_pl:5.2f} -> yt_v={yt_v:.6f}, mt={mt:.2f} GeV, rel={rel:+.2%}")

    high_rows = [r for r in rows if r[0] >= 1.0]
    high_mt_min = min(r[2] for r in high_rows)
    high_mt_max = max(r[2] for r in high_rows)
    high_rel_min = min(abs(r[3]) for r in high_rows)
    check(
        "generic high-UV QFP band misses external top-mass target by more than 5%",
        high_rel_min > 0.05,
        f"mt range={high_mt_min:.2f}..{high_mt_max:.2f} GeV, closest_rel={high_rel_min:.2%}",
    )

    uv_span = max(uv_grid) / min(uv_grid)
    ir_values = np.array([r[1] for r in rows])
    ir_span = float(ir_values.max() / ir_values.min())
    check(
        "QFP focusing exists but does not imply correct location",
        uv_span / ir_span > 5.0,
        f"UV factor={uv_span:.2f}, IR factor={ir_span:.3f}, compression={uv_span/ir_span:.2f}",
    )

    special = min(rows, key=lambda r: abs(r[2] - target_mt))
    check(
        "near-target scan point is a selected UV boundary, not generic attraction",
        special[0] == 0.5 and abs(special[3]) < 0.05,
        f"best yt_pl={special[0]:.2f}, mt={special[2]:.2f} GeV, rel={special[3]:+.2%}",
    )

    # Exact no-go conclusion for the route as posed.
    route_fails = high_rel_min > 0.05 and special[0] == 0.5
    check(
        "no-go: generic QFP-attractor route cannot replace a derived UV boundary",
        route_fails,
        "large-UV attractor is misplaced; successful point requires UV selection",
    )

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
