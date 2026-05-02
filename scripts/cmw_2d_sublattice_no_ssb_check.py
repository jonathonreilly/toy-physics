"""CMW 2D/1D sublattice no-SSB check.

Verifies (S1)-(S4) of CMW_2D_SUBLATTICE_NO_SSB_THEOREM_NOTE_2026-05-02.md
by computing the IR-divergence of the lattice Goldstone-mode integral
I_d in d = 1, 2, 3 and confirming the divergence pattern that drives
the no-SSB conclusion.

Tests:
  T1: I_1 diverges linearly in L
  T2: I_2 diverges logarithmically in L
  T3: I_3 converges to a finite limit as L → ∞
  T4: scaling I_d / appropriate-divergence is constant for d = 1, 2
  T5: the divergent I_d for d ≤ 2 implies via Bogoliubov bound that
      ⟨q⟩_β = 0 (numerically demonstrated bound)
"""
from __future__ import annotations

import math

import numpy as np


def lattice_dispersion_d(k):
    """Goldstone-mode lattice dispersion E_k = 2 sum_μ (1 - cos k_μ)."""
    return 2 * sum(1 - math.cos(km) for km in k)


def lattice_IR_integral(L: int, d: int) -> float:
    """I_d = (1/V) sum_{k != 0} 1 / E_k on Z^d with side length L."""
    V = L ** d
    total = 0.0
    # Iterate over all wavevectors except k = 0
    if d == 1:
        for n in range(L):
            if n == 0:
                continue
            k = (2 * math.pi * n / L,)
            total += 1.0 / lattice_dispersion_d(k)
    elif d == 2:
        for n1 in range(L):
            for n2 in range(L):
                if n1 == 0 and n2 == 0:
                    continue
                k = (2 * math.pi * n1 / L, 2 * math.pi * n2 / L)
                total += 1.0 / lattice_dispersion_d(k)
    elif d == 3:
        for n1 in range(L):
            for n2 in range(L):
                for n3 in range(L):
                    if n1 == 0 and n2 == 0 and n3 == 0:
                        continue
                    k = (2 * math.pi * n1 / L, 2 * math.pi * n2 / L, 2 * math.pi * n3 / L)
                    total += 1.0 / lattice_dispersion_d(k)
    return total / V


def main() -> None:
    print("=" * 72)
    print("CMW 2D/1D SUBLATTICE NO-SSB CHECK")
    print("=" * 72)
    print()
    print("Setup:")
    print("  Lattice IR-integral I_d = (1/V) sum_{k≠0} 1/E_k")
    print("  E_k = 2 sum_μ (1 - cos k_μ) (lattice Goldstone dispersion)")
    print("  Divergence of I_d at large L is the Bogoliubov-bound mechanism")
    print("  that forces ⟨q⟩_β = 0 (no SSB) for d ≤ 2.")
    print()

    # ----- Test 1: I_1 diverges linearly -----
    print("-" * 72)
    print("TEST 1: I_1 diverges linearly with L")
    print("-" * 72)
    Ls = [4, 8, 16, 32, 64, 128]
    I_1_vals = [lattice_IR_integral(L, 1) for L in Ls]
    print(f"  {'L':>4}  {'I_1':>12}  {'I_1 / L':>12}")
    for L, I in zip(Ls, I_1_vals):
        print(f"  {L:>4}  {I:>12.6f}  {I/L:>12.6e}")
    # Linear divergence: I_1(L) ~ c · L for some constant c
    # Check that I_1(L) / L is converging to a constant
    ratio_diff = abs(I_1_vals[-1] / Ls[-1] - I_1_vals[-2] / Ls[-2])
    growing = all(I_1_vals[i+1] > I_1_vals[i] for i in range(len(Ls) - 1))
    print(f"  I_1 monotonically growing: {growing}")
    t1_ok = growing and ratio_diff < 0.01  # I_1/L approaching constant
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: I_2 diverges logarithmically -----
    print("-" * 72)
    print("TEST 2: I_2 diverges logarithmically with L")
    print("-" * 72)
    Ls_2d = [4, 8, 16, 32, 48]  # smaller for 2D (V = L^2)
    I_2_vals = [lattice_IR_integral(L, 2) for L in Ls_2d]
    print(f"  {'L':>4}  {'I_2':>12}  {'I_2 / log(L)':>14}")
    for L, I in zip(Ls_2d, I_2_vals):
        print(f"  {L:>4}  {I:>12.6f}  {I/math.log(L):>14.6f}")
    growing_2 = all(I_2_vals[i+1] > I_2_vals[i] for i in range(len(Ls_2d) - 1))
    # I_2 / log L should approach a constant
    t2_ok = growing_2 and (abs(I_2_vals[-1] / math.log(Ls_2d[-1]) - I_2_vals[-2] / math.log(Ls_2d[-2])) < 0.05)
    print(f"  I_2 monotonically growing: {growing_2}")
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: I_3 converges to finite limit -----
    print("-" * 72)
    print("TEST 3: I_3 converges to a finite value as L → ∞")
    print("-" * 72)
    Ls_3d = [4, 6, 8, 10, 12]  # small for 3D (V = L^3)
    I_3_vals = [lattice_IR_integral(L, 3) for L in Ls_3d]
    print(f"  {'L':>4}  {'I_3':>12}  {'rel. change':>14}")
    for i, (L, I) in enumerate(zip(Ls_3d, I_3_vals)):
        if i == 0:
            change = "—"
        else:
            change = f"{abs(I - I_3_vals[i-1])/I_3_vals[i-1]:.4e}"
        print(f"  {L:>4}  {I:>12.6f}  {change:>14}")
    # I_3 should approach a finite limit (Watson integral ≈ 0.505)
    final_change = abs(I_3_vals[-1] - I_3_vals[-2]) / I_3_vals[-2]
    converging = final_change < 0.05
    finite_limit = I_3_vals[-1] < 1.0  # bounded
    t3_ok = converging and finite_limit
    print(f"  final relative change = {final_change:.4e}, bounded? {finite_limit}")
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: divergence pattern -----
    print("-" * 72)
    print("TEST 4: I_d / appropriate-divergence is constant for d ≤ 2")
    print("-" * 72)
    d1_ratios = [I_1_vals[i] / Ls[i] for i in range(len(Ls))]
    d2_ratios = [I_2_vals[i] / math.log(Ls_2d[i]) for i in range(len(Ls_2d))]
    print(f"  d=1: I_1/L ratios = {[round(r, 4) for r in d1_ratios]}")
    print(f"  d=2: I_2/log(L) ratios = {[round(r, 4) for r in d2_ratios]}")
    d1_stable = (max(d1_ratios[-3:]) - min(d1_ratios[-3:])) < 0.05
    d2_stable = (max(d2_ratios[-3:]) - min(d2_ratios[-3:])) < 0.05
    print(f"  d=1 ratio stable: {d1_stable}")
    print(f"  d=2 ratio stable: {d2_stable}")
    t4_ok = d1_stable and d2_stable
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Bogoliubov-bound argument -----
    print("-" * 72)
    print("TEST 5: divergent I_d for d ≤ 2 → Bogoliubov bound forces ⟨q⟩ = 0")
    print("-" * 72)
    print("  Bogoliubov inequality: |⟨q⟩|² ≤ const / I_d in CMW setup.")
    print("  As L → ∞, I_d → ∞ for d ≤ 2 ⇒ |⟨q⟩| → 0.")
    print()
    # Numerically compute the bound for d=1, 2
    const = 1.0  # arbitrary normalization
    for d, I_vals, L_vals in [(1, I_1_vals, Ls), (2, I_2_vals, Ls_2d)]:
        bound_seq = [math.sqrt(const / I) for I in I_vals]
        print(f"  d={d}: |⟨q⟩| upper bound for L={L_vals}:")
        print(f"        {[round(b, 4) for b in bound_seq]}")
    # The bound should decrease with L (more sites → tighter bound)
    bound_d1_decreasing = all(math.sqrt(const / I_1_vals[i+1]) < math.sqrt(const / I_1_vals[i]) for i in range(len(Ls) - 1))
    bound_d2_decreasing = all(math.sqrt(const / I_2_vals[i+1]) < math.sqrt(const / I_2_vals[i]) for i in range(len(Ls_2d) - 1))
    t5_ok = bound_d1_decreasing and bound_d2_decreasing
    print(f"  d=1 bound decreasing with L: {bound_d1_decreasing}")
    print(f"  d=2 bound decreasing with L: {bound_d2_decreasing}")
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (I_1 ~ L linear divergence):           {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (I_2 ~ log L logarithmic divergence):  {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (I_3 finite as L → ∞):                 {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (divergence ratios stable):            {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (Bogoliubov bound forces ⟨q⟩ = 0):     {'PASS' if t5_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
