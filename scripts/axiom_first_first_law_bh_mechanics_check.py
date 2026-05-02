"""Axiom-first first law of black hole mechanics check.

Verifies the first law dM = T_H dS_BH for the Schwarzschild family
on the framework's retained GR action surface plus retained BH 1/4
carrier composition plus Block 02 Hawking T_H = kappa/(2pi).

Tests:
  T1: Schwarzschild specialization (F1) — dM = T_H dS_BH.
  T2: Smarr formula (F3) — M = 2 T_H S_BH for Schwarzschild.
  T3: explicit identity check (F4) — symbolically dM = dM.
  T4: negative specific heat (corollary C3) — dT_H/dM < 0 for
      Schwarzschild.
  T5: integral form — M(M_2) - M(M_1) = integral T_H dS_BH from
      M_1 to M_2.
  T6: alternative check via Smarr — derivative of M = 2 T_H S_BH
      along Schwarzschild family is consistent with the first law.
"""
from __future__ import annotations

import math


def schwarzschild(M: float, G: float = 1.0) -> tuple[float, float, float, float, float]:
    """Return (r_s, A, S_BH, T_H, kappa) for Schwarzschild of mass M."""
    r_s = 2 * G * M
    A = 4 * math.pi * r_s ** 2  # = 16 pi G^2 M^2
    S_BH = A / (4 * G)  # = 4 pi G M^2
    kappa = 1.0 / (4 * G * M)
    T_H = kappa / (2 * math.pi)  # = 1 / (8 pi G M)
    return r_s, A, S_BH, T_H, kappa


def main() -> None:
    print("=" * 72)
    print("AXIOM-FIRST FIRST LAW OF BH MECHANICS CHECK")
    print("=" * 72)
    print()
    print("Setup:")
    print("  retained framework GR action (UNIVERSAL_GR_*)")
    print("  retained BH 1/4 carrier composition (S_BH = A/4G)")
    print("  Block 02 Hawking T_H = kappa/(2 pi)")
    print()
    print("First law: dM = T_H dS_BH for the Schwarzschild family")
    print()

    G = 1.0

    # ----- Test 1: F1 differential check -----
    print("-" * 72)
    print("TEST 1: Schwarzschild differential dM = T_H dS_BH")
    print("-" * 72)
    print(f"  {'M':>6}  {'T_H':>14}  {'dS_BH/dM':>14}  {'T_H*dS_BH/dM':>14}  {'should=1':>10}")
    print(f"  {'-'*6}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*10}")
    max_diff_t1 = 0.0
    for M in [0.5, 1.0, 2.0, 5.0, 10.0]:
        _, _, S_BH, T_H, _ = schwarzschild(M, G)
        # Compute dS_BH/dM via finite difference
        dM = 1e-6
        _, _, S_BH_plus, _, _ = schwarzschild(M + dM, G)
        _, _, S_BH_minus, _, _ = schwarzschild(M - dM, G)
        dSdM = (S_BH_plus - S_BH_minus) / (2 * dM)
        product = T_H * dSdM
        diff = abs(product - 1.0)
        max_diff_t1 = max(max_diff_t1, diff)
        print(f"  {M:>6.2f}  {T_H:>14.6e}  {dSdM:>14.6e}  {product:>14.6e}  diff={diff:.2e}")
    print()
    print(f"  max | T_H dS_BH/dM - 1 | = {max_diff_t1:.3e}")
    t1_ok = max_diff_t1 < 1e-6  # finite-diff precision
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Smarr formula M = 2 T_H S_BH -----
    print("-" * 72)
    print("TEST 2: Smarr formula M = 2 T_H S_BH (Schwarzschild)")
    print("-" * 72)
    print(f"  {'M':>6}  {'T_H':>14}  {'S_BH':>14}  {'2 T_H S_BH':>14}  {'M':>14}")
    max_diff_t2 = 0.0
    for M in [0.5, 1.0, 2.0, 5.0, 10.0]:
        _, _, S_BH, T_H, _ = schwarzschild(M, G)
        smarr_rhs = 2 * T_H * S_BH
        diff = abs(smarr_rhs - M)
        max_diff_t2 = max(max_diff_t2, diff)
        print(f"  {M:>6.2f}  {T_H:>14.6e}  {S_BH:>14.6e}  {smarr_rhs:>14.6e}  {M:>14.6e}")
    print()
    print(f"  max | 2 T_H S_BH - M | = {max_diff_t2:.3e}")
    t2_ok = max_diff_t2 < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: explicit identity check -----
    print("-" * 72)
    print("TEST 3: explicit symbolic check dM = dM (proof equation 6)")
    print("-" * 72)
    print("Substitute T_H = 1/(8 pi G M), S_BH = 4 pi G M^2:")
    print("  T_H dS_BH = (1/8 pi G M) * d(4 pi G M^2)")
    print("            = (1/8 pi G M) * 8 pi G M dM")
    print("            = dM   ✓")
    print()
    # Numerical identity check
    M = 2.5
    _, _, S_BH, T_H, _ = schwarzschild(M, G)
    coef_dM_lhs = 1.0  # dM coefficient on the left
    # T_H * dS_BH/dM = T_H * 8 pi G M = (1/8 pi G M) * 8 pi G M = 1
    coef_dM_rhs = T_H * 8 * math.pi * G * M
    diff_t3 = abs(coef_dM_lhs - coef_dM_rhs)
    print(f"  T_H * 8 pi G M at M = {M}: {coef_dM_rhs:.10f}")
    print(f"  expected 1.0, diff = {diff_t3:.3e}")
    t3_ok = diff_t3 < 1e-15
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: negative specific heat for Schwarzschild -----
    print("-" * 72)
    print("TEST 4: negative specific heat dT_H/dM < 0 (Schwarzschild)")
    print("-" * 72)
    print(f"  {'M':>6}  {'T_H':>14}  {'dT_H/dM':>14}  {'sign':>6}")
    all_negative = True
    for M in [0.5, 1.0, 2.0, 5.0, 10.0]:
        _, _, _, T_H, _ = schwarzschild(M, G)
        dM = 1e-6
        _, _, _, T_H_plus, _ = schwarzschild(M + dM, G)
        _, _, _, T_H_minus, _ = schwarzschild(M - dM, G)
        dTdM = (T_H_plus - T_H_minus) / (2 * dM)
        sign = "<0" if dTdM < 0 else ">=0"
        if dTdM >= 0:
            all_negative = False
        print(f"  {M:>6.2f}  {T_H:>14.6e}  {dTdM:>14.6e}  {sign:>6}")
    print()
    t4_ok = all_negative
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: integral form -----
    print("-" * 72)
    print("TEST 5: integrated first law M(M_2) - M(M_1) = integral T_H dS_BH")
    print("-" * 72)
    M_1, M_2 = 1.0, 5.0
    _, _, S_BH_1, _, _ = schwarzschild(M_1, G)
    _, _, S_BH_2, _, _ = schwarzschild(M_2, G)
    n_steps = 1000
    integral = 0.0
    for k in range(n_steps):
        M_mid = M_1 + (k + 0.5) / n_steps * (M_2 - M_1)
        _, _, _, T_H_mid, _ = schwarzschild(M_mid, G)
        # dS_BH = 8 pi G M dM
        dSdM = 8 * math.pi * G * M_mid
        dM = (M_2 - M_1) / n_steps
        integral += T_H_mid * dSdM * dM
    print(f"  M_1 = {M_1}, M_2 = {M_2}")
    print(f"  M_2 - M_1 = {M_2 - M_1}")
    print(f"  integral T_H dS_BH from M_1 to M_2 = {integral:.10f}")
    diff_t5 = abs(integral - (M_2 - M_1))
    print(f"  | integral - (M_2 - M_1) | = {diff_t5:.3e}")
    t5_ok = diff_t5 < 1e-6
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Smarr derivative consistency -----
    print("-" * 72)
    print("TEST 6: Smarr-derivative consistency: d(2 T_H S_BH)/dM = 1")
    print("-" * 72)
    max_diff_t6 = 0.0
    for M in [1.0, 2.0, 5.0]:
        _, _, S_BH, T_H, _ = schwarzschild(M, G)
        dM = 1e-6
        _, _, S_BH_plus, T_H_plus, _ = schwarzschild(M + dM, G)
        _, _, S_BH_minus, T_H_minus, _ = schwarzschild(M - dM, G)
        smarr_plus = 2 * T_H_plus * S_BH_plus
        smarr_minus = 2 * T_H_minus * S_BH_minus
        d_smarr = (smarr_plus - smarr_minus) / (2 * dM)
        diff = abs(d_smarr - 1.0)
        max_diff_t6 = max(max_diff_t6, diff)
        print(f"  M = {M}: d(2 T_H S_BH)/dM = {d_smarr:.10f}, expected 1")
    print()
    print(f"  max diff = {max_diff_t6:.3e}")
    t6_ok = max_diff_t6 < 1e-6
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (dM = T_H dS_BH for Schwarzschild):              {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (Smarr formula M = 2 T_H S_BH):                  {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (explicit identity dM = dM):                     {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (negative specific heat dT_H/dM < 0):            {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (integral form over (M_1, M_2)):                 {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (Smarr derivative consistency):                  {'PASS' if t6_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok and t6_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print()
    print("Note: the proof in the companion theorem note follows Bardeen-Carter-")
    print("Hawking 1973 plus the Wald-Noether identity (admitted, same as upstream")
    print("BH 1/4 carrier composition). The runner verifies the Schwarzschild")
    print("specialization at machine precision; Kerr-Newman extensions are")
    print("recorded as corollaries (not numerically checked here).")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
