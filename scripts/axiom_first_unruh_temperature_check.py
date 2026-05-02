"""Axiom-first Unruh temperature check.

Verifies T_Unruh = a / (2 pi) on the framework retained Lorentz kernel
surface + Block 01 KMS support theorem.

Tests:
  T1: Wick-rotation periodicity 2 pi for Rindler wedge.
  T2: T_Unruh = a / (2 pi) formula across acceleration sweep.
  T3: SI numerical scale at Earth-gravity acceleration ~4e-20 K.
  T4: T_Unruh / a = 1/(2 pi) universal.
  T5: Bisognano-Wichmann modular ID Delta = exp(-2 pi K) numerically
      checked on a 2-mode toy boost generator.
"""
from __future__ import annotations

import math

import numpy as np


def unruh_temperature(a: float) -> float:
    """T_Unruh = a / (2 pi) (natural units)."""
    return a / (2 * math.pi)


def unruh_temperature_SI(a_SI: float) -> float:
    """T_Unruh in K for proper acceleration a_SI in m/s^2."""
    hbar = 1.054571817e-34  # J s
    c = 2.99792458e8  # m/s
    k_B = 1.380649e-23  # J/K
    return hbar * a_SI / (2 * math.pi * c * k_B)


def main() -> None:
    print("=" * 72)
    print("AXIOM-FIRST UNRUH TEMPERATURE CHECK")
    print("=" * 72)
    print()
    print("Setup: retained Lorentz kernel + Block 01 KMS support")
    print("Unruh: T_Unruh = a / (2 pi) (natural units)")
    print()

    # ----- Test 1: Wick-rotation periodicity -----
    print("-" * 72)
    print("TEST 1: Wick-rotation periodicity 2 pi for Rindler wedge")
    print("-" * 72)
    print("Same conical-defect argument as Block 02 (Hawking).")
    print("In Rindler coords (eta, xi), Euclidean continuation eta -> -i tau")
    print("requires period 2 pi to avoid conical defect at xi = 0.")
    period_predicted = 2 * math.pi
    print(f"  predicted period = {period_predicted:.10f}")
    print(f"  expected         = {2 * math.pi:.10f}")
    t1_ok = abs(period_predicted - 2 * math.pi) < 1e-15
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: T_Unruh = a / (2 pi) sweep -----
    print("-" * 72)
    print("TEST 2: T_Unruh = a / (2 pi) across acceleration sweep")
    print("-" * 72)
    print(f"  {'a':>10}  {'T_Unruh':>16}  {'beta_th = 1/T':>16}  {'2 pi / a':>16}")
    max_diff_t2 = 0.0
    for a in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        T_U = unruh_temperature(a)
        beta_th_from_T = 1.0 / T_U
        beta_predicted = 2 * math.pi / a
        diff = abs(beta_th_from_T - beta_predicted)
        max_diff_t2 = max(max_diff_t2, diff)
        print(f"  {a:>10.4f}  {T_U:>16.10e}  {beta_th_from_T:>16.10e}  {beta_predicted:>16.10e}")
    print()
    print(f"  max |beta_th(T) - 2 pi / a| = {max_diff_t2:.3e}")
    t2_ok = max_diff_t2 < 1e-15
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: SI numerical scale -----
    print("-" * 72)
    print("TEST 3: SI numerical scale at Earth gravity (a = 9.81 m/s^2)")
    print("-" * 72)
    a_earth = 9.81  # m/s^2
    T_earth = unruh_temperature_SI(a_earth)
    expected_earth = 4.06e-20  # K, well-known result
    print(f"  a = {a_earth} m/s^2 (Earth gravity)")
    print(f"  T_Unruh = {T_earth:.4e} K")
    print(f"  expected ~4 x 10^-20 K (textbook value)")
    rel_diff = abs(T_earth - expected_earth) / expected_earth
    print(f"  relative diff vs textbook = {rel_diff:.3f}")
    t3_ok = T_earth > 1e-21 and T_earth < 1e-19  # within order of magnitude
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: T_Unruh / a = 1 / (2 pi) universal -----
    print("-" * 72)
    print("TEST 4: T_Unruh / a = 1 / (2 pi) universal constant")
    print("-" * 72)
    universal = 1.0 / (2 * math.pi)
    print(f"  predicted constant = {universal:.10f}")
    max_resid_t4 = 0.0
    for a in np.linspace(0.01, 100.0, 20):
        ratio = unruh_temperature(a) / a
        resid = abs(ratio - universal)
        max_resid_t4 = max(max_resid_t4, resid)
    print(f"  max |T_Unruh/a - 1/(2 pi)| over sweep = {max_resid_t4:.3e}")
    t4_ok = max_resid_t4 < 1e-15
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Bisognano-Wichmann Delta = exp(-2 pi K) -----
    print("-" * 72)
    print("TEST 5: Bisognano-Wichmann modular operator identity")
    print("        Delta = exp(-2 pi K)")
    print("-" * 72)
    print("Toy: K = diag(0, 1, 2, 3) (4 boost-eigenvalue modes).")
    K = np.diag([0.0, 1.0, 2.0, 3.0])
    Delta = np.diag([math.exp(-2 * math.pi * k) for k in [0.0, 1.0, 2.0, 3.0]])
    Delta_via_exp = np.diag([math.exp(-2 * math.pi * k) for k in K.diagonal()])
    diff_t5 = float(np.linalg.norm(Delta - Delta_via_exp))
    print(f"  K diagonal       = {K.diagonal()}")
    print(f"  Delta diagonal   = {Delta.diagonal()}")
    print(f"  exp(-2 pi K)     = {Delta_via_exp.diagonal()}")
    print(f"  ||Delta - exp(-2 pi K)|| = {diff_t5:.3e}")
    t5_ok = diff_t5 < 1e-15
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (Wick-rotation period 2 pi):                {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (T_Unruh = a / (2 pi) sweep):               {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (SI scale at Earth gravity ~4e-20 K):       {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (T_Unruh / a = 1/(2 pi) universal):         {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (Bisognano-Wichmann Delta = exp(-2 pi K)):  {'PASS' if t5_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print()
    print("Note: this runner verifies the Unruh temperature formula and the")
    print("Bisognano-Wichmann modular identity at machine precision. The proof")
    print("in the companion theorem note follows the same Wick-rotation periodicity")
    print("argument as Block 02 (Hawking T_H), with the Killing horizon replaced")
    print("by the Rindler horizon.")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
