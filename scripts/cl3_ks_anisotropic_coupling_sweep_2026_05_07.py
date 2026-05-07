"""
Coupling sweep at xi=1 (isotropic Wilson) and xi=2 (mildly anisotropic)
on 2x2x2xLt geometry to compare with strong-coupling LO and KS literature.

Output: <P>_sp(g^2) for g^2 in [0.5, 4.0].
"""

from __future__ import annotations

import numpy as np
from cl3_ks_anisotropic_mc_2026_05_07 import run_anisotropic


if __name__ == "__main__":
    print("=" * 70)
    print("Coupling sweep: 2x2x2 spatial torus")
    print("=" * 70)
    print()
    print("S = -(beta_sigma/N_c) Sum_sp - (beta_tau/N_c) Sum_tau")
    print("Trotter dictionary: beta_sigma = beta_W/xi, beta_tau = beta_W*xi")
    print("where beta_W = 2*N_c/g^2 = 6/g^2 for SU(3).")
    print()

    print("[1] Isotropic xi=1 sweep on 2x2x2x16:")
    print(f"{'g^2':>6}  {'beta_W':>8}  {'P_sp':>8}  {'P_sp_LO=1/(24g^4)':>20}")
    for g2 in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]:
        beta_W = 6.0 / g2
        r = run_anisotropic(2, 2, 2, 16, beta_W, beta_W,
                              n_therm=300, n_meas=300, seed=42, eps=0.1,
                              verbose=False)
        LO = 1.0 / (24 * g2**2)
        print(f"{g2:>6.2f}  {beta_W:>8.2f}  {r['P_sp']:>8.4f}  {LO:>20.4f}")

    print()
    print("[2] Anisotropic xi=2 sweep on 2x2x2x32:")
    print(f"{'g^2':>6}  {'beta_sigma':>10}  {'beta_tau':>9}  {'P_sp':>8}")
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
        beta_W = 6.0 / g2
        r = run_anisotropic(2, 2, 2, 32, beta_W / 2.0, beta_W * 2.0,
                              n_therm=300, n_meas=300, seed=42, eps=0.1,
                              verbose=False)
        print(f"{g2:>6.2f}  {beta_W/2.0:>10.2f}  {beta_W*2.0:>9.2f}  "
              f"{r['P_sp']:>8.4f}")

    print()
    print("[3] More extreme anisotropic xi=4 (closer to Hamilton):")
    print(f"{'g^2':>6}  {'beta_sigma':>10}  {'beta_tau':>9}  {'P_sp':>8}")
    for g2 in [0.5, 1.0, 2.0]:
        beta_W = 6.0 / g2
        r = run_anisotropic(2, 2, 2, 64, beta_W / 4.0, beta_W * 4.0,
                              n_therm=300, n_meas=300, seed=42, eps=0.1,
                              verbose=False)
        print(f"{g2:>6.2f}  {beta_W/4.0:>10.2f}  {beta_W*4.0:>9.2f}  "
              f"{r['P_sp']:>8.4f}")

    print()
    print("Reference: at g^2=1, beta=6:")
    print("  KS literature P_sp ~ 0.55-0.60")
    print("  Wilson MC isotropic large vol: 0.5934")
    print("  Strong-coupling LO 1/(24*g^4) at g^2=1: 0.0417")
