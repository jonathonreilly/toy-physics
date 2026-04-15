#!/usr/bin/env python3
"""
Canonical synthesis runner for COMPLETE_PREDICTION_CHAIN_2026_04_15.md.

This script is intentionally package-level rather than route-level. It
collects the final promoted quantitative rows that survived the review pass and
prints the single reviewer-facing prediction card on `main`.

Subcomponent provenance:
  - plaquette/u0/alpha_LM/alpha_s(v)/v: hierarchy + zero-import chain
  - R_conn, g_1(v), g_2(v), sin^2(theta_W), 1/alpha_EM: color projection stack
  - y_t(v), m_t(pole): Ward + color-singlet projection stack
  - m_H (2-loop): corrected-y_t stability boundary
  - m_H (full 3-loop): Buttazzo full-3-loop boundary calibration with derived inputs
  - vacuum stability: corrected-y_t stability-boundary route
"""

from __future__ import annotations

import math

PI = math.pi
M_PL = 1.2209e19
PLAQ = 0.5934
R_CONN = 8.0 / 9.0

U0 = PLAQ ** 0.25
ALPHA_BARE = 1.0 / (4.0 * PI)
ALPHA_LM = ALPHA_BARE / U0
ALPHA_S_V = ALPHA_BARE / (U0 ** 2)
V = M_PL * ((7.0 / 8.0) ** 0.25) * (ALPHA_LM ** 16)
TASTE_WEIGHT = (7.0 / 8.0) * 0.5 * R_CONN

# Final promoted EW package values from the reviewed complete chain.
SIN2_MZ = 0.23061
INV_ALPHA_EM_MZ = 127.665
G1_V = 0.464376
G2_V = 0.648031

# Final promoted Yukawa / top package values.
YT_WARD_V = 0.973220
YT_PHYSICAL_V = YT_WARD_V * math.sqrt(R_CONN)
MT_POLE_2L = 172.57
MT_POLE_3L = 173.10

# Final promoted Higgs / vacuum package values.
MH_2L = 119.77
MH_3L = 129.70
VACUUM_STABLE = True


def pct(pred: float, obs: float) -> float:
    return 100.0 * (pred - obs) / obs


def main() -> None:
    print("==============================================================================")
    print("COMPLETE PREDICTION CHAIN: CANONICAL PACKAGE SYNTHESIS")
    print("==============================================================================")
    print()
    print("Framework inputs")
    print(f"  <P>             = {PLAQ:.4f}")
    print(f"  u_0             = {U0:.6f}")
    print(f"  alpha_LM        = {ALPHA_LM:.6f}")
    print(f"  alpha_s(v)      = {ALPHA_S_V:.6f}")
    print(f"  v               = {V:.2f} GeV")
    print(f"  R_conn          = {R_CONN:.6f}")
    print(f"  taste_weight    = {TASTE_WEIGHT:.6f} (= 7/18)")
    print()
    print("Promoted quantitative package")
    rows = [
        ("v [GeV]", V, 246.22),
        ("alpha_s(M_Z)", 0.118066, 0.1179),
        ("sin^2(theta_W)(M_Z)", SIN2_MZ, 0.23122),
        ("1/alpha_EM(M_Z)", INV_ALPHA_EM_MZ, 127.951),
        ("g_1(v)", G1_V, 0.463986),
        ("g_2(v)", G2_V, 0.646288),
        ("y_t(v)", YT_PHYSICAL_V, 0.9170),
        ("m_t(pole, 2-loop) [GeV]", MT_POLE_2L, 172.69),
        ("m_t(pole, 3-loop) [GeV]", MT_POLE_3L, 172.69),
        ("m_H(2-loop) [GeV]", MH_2L, 125.25),
        ("m_H(full 3-loop) [GeV]", MH_3L, 125.25),
    ]
    for label, pred, obs in rows:
        print(f"  {label:<28} {pred:>10.4f}   obs {obs:>10.4f}   dev {pct(pred, obs):>+7.3f}%")
    print(
        "  Vacuum stability".ljust(28)
        + ("Absolutely stable" if VACUUM_STABLE else "Not stable")
        + "   comparator SM metastability"
    )
    print()
    print("Primary support stack")
    print("  COMPLETE_PREDICTION_CHAIN_2026_04_15.md")
    print("  RCONN_DERIVED_NOTE.md")
    print("  YT_EW_COLOR_PROJECTION_THEOREM.md")
    print("  YT_COLOR_PROJECTION_CORRECTION_NOTE.md")
    print("  YT_QFP_INSENSITIVITY_THEOREM.md")
    print("  HIGGS_MASS_FROM_AXIOM_NOTE.md")
    print()
    print("Status: promoted package on main")


if __name__ == "__main__":
    main()
