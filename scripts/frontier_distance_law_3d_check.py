"""Frontier #1b: 3D distance law verification.

The distance-law analytic theorem predicts:
- Valley-linear (S = L(1-f)) on a 3D lattice with f = s/r gives delta ~ 1/b
- Spent-delay (S ~ sqrt(f)) gives delta ~ 1/sqrt(b)

In 2D, the logarithmic Green's function prevents 1/b scaling for ANY action.
This script verifies that 3D is different: the Coulomb 1/r field should
recover Newtonian gravity with the valley-linear action.

Approach: solve Poisson equation on a 3D grid, compute ray deflection
at various impact parameters for both action modes.
"""

import math
import numpy as np
from scipy.optimize import curve_fit


def solve_laplacian_field_3d(
    nx: int, ny: int, nz: int,
    mass_pos: tuple[int, int, int],
    mass_strength: float = 1.0,
    max_iter: int = 3000,
    tol: float = 1e-7,
) -> np.ndarray:
    """Solve 3D Laplacian field with point source and Dirichlet BC."""
    field = np.zeros((nx, ny, nz))
    source = np.zeros((nx, ny, nz))
    mx, my, mz = mass_pos
    source[mx, my, mz] = mass_strength

    for iteration in range(max_iter):
        old = field.copy()
        # Interior points only (Dirichlet BC = 0 on boundary)
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                for k in range(1, nz - 1):
                    field[i, j, k] = (
                        field[i+1, j, k] + field[i-1, j, k] +
                        field[i, j+1, k] + field[i, j-1, k] +
                        field[i, j, k+1] + field[i, j, k-1] +
                        source[i, j, k]
                    ) / 6.0
        max_change = np.max(np.abs(field - old))
        if max_change < tol:
            print(f"  3D field converged in {iteration+1} iterations (max_change={max_change:.2e})")
            break
    else:
        print(f"  3D field: max_iter reached (max_change={max_change:.2e})")

    return field


def compute_ray_deflection_3d(
    field: np.ndarray,
    b: int,
    k: float,
    action_mode: str,
    mass_y: int,
    mass_z: int,
) -> float:
    """Compute deflection of a ray at impact parameter b in the y-direction.

    Ray propagates along x at (y = mass_y + b, z = mass_z).
    Returns dPhi/db via finite difference.
    """
    nx = field.shape[0]
    z = mass_z
    y_b = mass_y + b
    y_b1 = mass_y + b + 1

    if y_b < 0 or y_b1 >= field.shape[1] or z < 0 or z >= field.shape[2]:
        return 0.0

    phase_b = 0.0
    phase_b1 = 0.0

    for x in range(1, nx - 1):
        f_b = field[x, y_b, z]
        f_b1 = field[x, y_b1, z]

        if action_mode == "valley_linear":
            phase_b += k * (1.0 - f_b)
            phase_b1 += k * (1.0 - f_b1)
        elif action_mode == "spent_delay":
            s_b = (1.0 + f_b) - math.sqrt(max(2 * f_b + f_b * f_b, 0.0))
            s_b1 = (1.0 + f_b1) - math.sqrt(max(2 * f_b1 + f_b1 * f_b1, 0.0))
            phase_b += k * s_b
            phase_b1 += k * s_b1

    return phase_b1 - phase_b


def power_law(x, a, alpha):
    return a / (x ** alpha)


def main():
    print("=" * 70)
    print("FRONTIER #1b: 3D Distance Law Verification")
    print("=" * 70)
    print()
    print("Prediction: In 3D, f(r) = s/r (Coulomb), so:")
    print("  Valley-linear: delta ~ 1/b (Newtonian)")
    print("  Spent-delay:   delta ~ 1/sqrt(b)")
    print()
    print("In 2D, f(r) ~ ln(r) prevents 1/b for ANY action.")
    print("This script tests whether 3D recovers the predicted scaling.")
    print()

    # 3D grid — smaller than 2D due to O(n^3) memory/time
    N = 31  # grid size per dimension
    mid = N // 2
    k = 4.0

    print(f"Grid: {N}x{N}x{N} = {N**3} nodes")
    print(f"Mass at center: ({mid}, {mid}, {mid})")
    print(f"Phase wavenumber k = {k}")
    print()

    print("Solving 3D Laplacian field...")
    field = solve_laplacian_field_3d(N, N, N, (mid, mid, mid), mass_strength=1.0)
    print(f"  Peak field: {field[mid, mid, mid]:.6f}")
    print(f"  Field at r=3: {field[mid, mid+3, mid]:.6f}")
    print(f"  Field at r=5: {field[mid, mid+5, mid]:.6f}")
    print()

    # Check field is 1/r in 3D
    print("-" * 70)
    print("3D FIELD PROFILE: f(r) vs 1/r and ln(r)")
    print("-" * 70)
    r_check = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    r_check = [r for r in r_check if mid + r < N - 1]
    f_check = [field[mid, mid + r, mid] for r in r_check]

    print(f"{'r':>4} | {'f(r)':>10} | {'f*r':>10} | {'f/ln(r)':>10}")
    print("-" * 50)
    for r, f in zip(r_check, f_check):
        print(f"{r:>4} | {f:>10.6f} | {f*r:>10.6f} | {f/math.log(r):>10.6f}")

    # Fit power law
    r_arr = np.array(r_check, dtype=float)
    f_arr = np.array(f_check)
    mask = f_arr > 0
    if mask.sum() >= 3:
        log_r = np.log(r_arr[mask])
        log_f = np.log(f_arr[mask])
        coeffs = np.polyfit(log_r, log_f, 1)
        print(f"\nPower law fit: f ~ r^{coeffs[0]:.3f}")
        print(f"  3D Coulomb predicts: f ~ r^(-1.0)")

        # Also fit logarithmic
        log_r_lin = np.log(r_arr[mask])
        coeffs_log = np.polyfit(log_r_lin, f_arr[mask], 1)
        f_pred_log = coeffs_log[0] * log_r_lin + coeffs_log[1]
        ss_res_log = np.sum((f_arr[mask] - f_pred_log) ** 2)
        ss_tot = np.sum((f_arr[mask] - np.mean(f_arr[mask])) ** 2)
        r2_log = 1.0 - ss_res_log / ss_tot if ss_tot > 0 else 0.0

        f_pred_pow = np.exp(coeffs[1]) * r_arr[mask] ** coeffs[0]
        ss_res_pow = np.sum((f_arr[mask] - f_pred_pow) ** 2)
        r2_pow = 1.0 - ss_res_pow / ss_tot if ss_tot > 0 else 0.0

        print(f"  Power-law R^2 = {r2_pow:.4f}")
        print(f"  Logarithmic R^2 = {r2_log:.4f}")
        if r2_pow > r2_log:
            print("  -> Power-law fits better (expected for 3D)")
        else:
            print("  -> Logarithmic fits better (unexpected for 3D)")

    # Impact parameters for deflection test
    b_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    b_values = [b for b in b_values if mid + b + 1 < N - 1]

    print()
    print("-" * 70)
    print("3D DEFLECTION vs IMPACT PARAMETER")
    print("-" * 70)
    print(f"{'b':>4} | {'VL defl':>12} | {'SD defl':>12}")
    print("-" * 35)

    vl_d = []
    sd_d = []
    for b in b_values:
        vl = abs(compute_ray_deflection_3d(field, b, k, "valley_linear", mid, mid))
        sd = abs(compute_ray_deflection_3d(field, b, k, "spent_delay", mid, mid))
        vl_d.append(vl)
        sd_d.append(sd)
        print(f"{b:>4} | {vl:>12.6f} | {sd:>12.6f}")

    # Fit power laws
    b_arr = np.array(b_values, dtype=float)

    print()
    print("-" * 70)
    print("POWER LAW FITS: delta(b) = A / b^alpha")
    print("-" * 70)

    vl_arr = np.array(vl_d)
    sd_arr = np.array(sd_d)

    for name, d_arr, expected in [("Valley-linear", vl_arr, 1.0), ("Spent-delay", sd_arr, 0.5)]:
        mask = d_arr > 0
        if mask.sum() >= 3:
            try:
                popt, _ = curve_fit(power_law, b_arr[mask], d_arr[mask], p0=[1.0, expected])
                pred = power_law(b_arr[mask], *popt)
                ss_res = np.sum((d_arr[mask] - pred) ** 2)
                ss_tot = np.sum((d_arr[mask] - np.mean(d_arr[mask])) ** 2)
                r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
                print(f"{name}: alpha = {popt[1]:.4f}  (theory: {expected})  R^2 = {r2:.4f}")
            except Exception as e:
                print(f"{name}: fit failed: {e}")
        else:
            print(f"{name}: insufficient data")

    # Mass scaling in 3D
    print()
    print("-" * 70)
    print("3D MASS SCALING: delta(M) at fixed b=4")
    print("-" * 70)

    mass_values = [0.5, 1.0, 2.0, 4.0, 8.0]
    b_test = 4
    vl_mass = []
    sd_mass = []

    for m in mass_values:
        f = solve_laplacian_field_3d(N, N, N, (mid, mid, mid), mass_strength=m)
        vl = abs(compute_ray_deflection_3d(f, b_test, k, "valley_linear", mid, mid))
        sd = abs(compute_ray_deflection_3d(f, b_test, k, "spent_delay", mid, mid))
        vl_mass.append(vl)
        sd_mass.append(sd)

    vl_ref = vl_mass[1] if vl_mass[1] > 0 else 1.0
    sd_ref = sd_mass[1] if sd_mass[1] > 0 else 1.0

    print(f"{'M':>6} | {'VL defl':>12} | {'SD defl':>12} | {'VL/VL(1)':>10} | {'SD/SD(1)':>10}")
    print("-" * 60)
    for i, m in enumerate(mass_values):
        print(f"{m:>6.1f} | {vl_mass[i]:>12.6f} | {sd_mass[i]:>12.6f} | "
              f"{vl_mass[i]/vl_ref:>10.4f} | {sd_mass[i]/sd_ref:>10.4f}")

    # Fit mass exponents
    m_arr = np.array(mass_values)
    for name, d_arr, expected in [("VL", np.array(vl_mass), 1.0), ("SD", np.array(sd_mass), 0.5)]:
        mask = d_arr > 0
        if mask.sum() >= 3:
            log_m = np.log(m_arr[mask])
            log_d = np.log(d_arr[mask])
            coeffs = np.polyfit(log_m, log_d, 1)
            print(f"\n{name} mass exponent: beta = {coeffs[0]:.4f}  (theory: {expected})")

    # Summary
    print()
    print("=" * 70)
    print("3D vs 2D COMPARISON")
    print("=" * 70)
    print("""
3D field is Coulomb (f ~ 1/r), not logarithmic.
The valley-linear action on a 3D field should give 1/b distance law.

If confirmed: the "distance law anomaly" was always a 2D artifact,
not a fundamental problem with the model. The physical 3D case should
work correctly with the valley-linear action.

If NOT confirmed: finite-grid boundary effects dominate even in 3D,
and larger grids are needed.
""")


if __name__ == "__main__":
    main()
