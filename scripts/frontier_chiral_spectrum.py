#!/usr/bin/env python3
"""
frontier_chiral_spectrum.py
===========================
Spectral analysis of the chiral quantum walk in a box.

HYPOTHESIS: The chiral walk's unitary transfer matrix has eigenphases
that match particle-in-a-box energy levels E_n ~ n^2.

FALSIFICATION: Spectrum is flat or doesn't scale as 1/W^2 with box size.
"""

import numpy as np


def build_chiral_unitary(n_y, theta):
    """Build the 2n_y x 2n_y unitary for a chiral walk with reflecting boundaries.

    Internal DOF: index 2*y = right-mover (+), 2*y+1 = left-mover (-).
    U = S @ C where C is the coin and S is the shift with reflection at walls.
    """
    dim = 2 * n_y

    # Coin matrix (block diagonal rotation by theta at each site)
    C = np.zeros((dim, dim), dtype=complex)
    for y in range(n_y):
        ip, im = 2 * y, 2 * y + 1
        C[ip, ip] = np.cos(theta)
        C[ip, im] = -np.sin(theta)
        C[im, ip] = np.sin(theta)
        C[im, im] = np.cos(theta)

    # Shift matrix with reflecting boundaries
    S = np.zeros((dim, dim), dtype=complex)
    for y in range(n_y):
        # Right-mover (+) shifts right; reflects at right wall
        if y + 1 < n_y:
            S[2 * (y + 1), 2 * y] = 1      # + at y -> + at y+1
        else:
            S[2 * y + 1, 2 * y] = 1         # reflect: + at wall -> -

        # Left-mover (-) shifts left; reflects at left wall
        if y - 1 >= 0:
            S[2 * (y - 1) + 1, 2 * y + 1] = 1  # - at y -> - at y-1
        else:
            S[2 * y, 2 * y + 1] = 1             # reflect: - at wall -> +

    return S @ C


def verify_unitarity(U, label=""):
    """Check that U is unitary: U^dagger U = I."""
    I = np.eye(U.shape[0])
    err = np.max(np.abs(U @ U.conj().T - I))
    return err


def extract_spectrum(U):
    """Extract sorted eigenphases from unitary matrix."""
    eigenvalues = np.linalg.eigvals(U)

    # Verify all eigenvalues on unit circle
    radii = np.abs(eigenvalues)
    radius_err = np.max(np.abs(radii - 1.0))

    phases = np.angle(eigenvalues)
    # Sort by absolute phase (energy magnitude)
    idx = np.argsort(np.abs(phases))
    phases_sorted = phases[idx]

    return phases_sorted, radius_err


def main():
    sep = "=" * 70
    print(sep)
    print("FRONTIER: CHIRAL WALK SPECTRUM IN A BOX")
    print(sep)

    # ================================================================
    # TEST 0: Verify unitarity
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 0: UNITARITY VERIFICATION")
    print("=" * 70)

    for n_y in [11, 21, 31, 41]:
        U = build_chiral_unitary(n_y, 0.3)
        err = verify_unitarity(U)
        print(f"  n_y={n_y:3d}  dim={2*n_y:4d}  unitarity error = {err:.2e}")

    # ================================================================
    # TEST 1: Free-space spectrum -- E_n/E_1 vs n^2?
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 1: EIGENPHASE RATIOS vs n^2 (particle-in-a-box)")
    print("=" * 70)

    theta = 0.3
    for n_y in [21, 31, 41]:
        U = build_chiral_unitary(n_y, theta)
        phases, rad_err = extract_spectrum(U)

        # Take positive phases only, sorted ascending
        pos_phases = np.sort(phases[phases > 0])

        if len(pos_phases) < 6:
            print(f"\n  n_y={n_y}: Only {len(pos_phases)} positive phases -- skipping")
            continue

        E1 = pos_phases[0]
        print(f"\n  n_y={n_y} (W={n_y}), theta={theta:.1f}, radius_err={rad_err:.2e}")
        print(f"  E_1 = {E1:.6f}")
        print(f"  {'n':>4s}  {'E_n':>12s}  {'E_n/E_1':>12s}  {'n^2':>8s}  {'ratio/n^2':>10s}")
        print(f"  {'---':>4s}  {'---':>12s}  {'---':>12s}  {'---':>8s}  {'---':>10s}")

        for i in range(min(8, len(pos_phases))):
            n = i + 1
            En = pos_phases[i]
            ratio = En / E1
            n_sq = n * n
            deviation = ratio / n_sq
            print(f"  {n:4d}  {En:12.6f}  {ratio:12.4f}  {n_sq:8d}  {deviation:10.4f}")

    # ================================================================
    # TEST 2: Box-size scaling -- E_1 ~ 1/W^2?
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 2: BOX-SIZE SCALING -- E_1 vs 1/W^2")
    print("=" * 70)

    theta = 0.3
    widths = [15, 21, 31, 41, 51, 61, 81, 101]
    E1_values = []

    for n_y in widths:
        U = build_chiral_unitary(n_y, theta)
        phases, _ = extract_spectrum(U)
        pos_phases = np.sort(phases[phases > 0])
        if len(pos_phases) > 0:
            E1_values.append((n_y, pos_phases[0]))

    print(f"\n  theta = {theta}")
    print(f"  {'W':>6s}  {'E_1':>12s}  {'E_1*W^2':>12s}  {'E_1*W':>12s}")
    print(f"  {'---':>6s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")

    for W, E1 in E1_values:
        print(f"  {W:6d}  {E1:12.6f}  {E1 * W**2:12.4f}  {E1 * W:12.4f}")

    # Check which scaling holds: E_1*W^p = const for which p?
    if len(E1_values) >= 3:
        Ws = np.array([x[0] for x in E1_values], dtype=float)
        Es = np.array([x[1] for x in E1_values], dtype=float)
        # Log-log fit: log(E) = a + b*log(W), expect b = -2 for PIB
        coeffs = np.polyfit(np.log(Ws), np.log(Es), 1)
        print(f"\n  Log-log fit: E_1 ~ W^({coeffs[0]:.3f})")
        print(f"  Particle-in-a-box predicts exponent = -2.0")
        print(f"  Linear (massless) predicts exponent = -1.0")

    # ================================================================
    # TEST 3: Mass dependence -- E_1 vs theta
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 3: MASS DEPENDENCE -- E_1 vs theta at fixed W=31")
    print("=" * 70)

    n_y = 31
    thetas = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2]
    E1_theta = []

    for th in thetas:
        U = build_chiral_unitary(n_y, th)
        phases, _ = extract_spectrum(U)
        pos_phases = np.sort(phases[phases > 0])
        if len(pos_phases) > 0:
            E1_theta.append((th, pos_phases[0]))

    print(f"\n  W = {n_y}")
    print(f"  {'theta':>8s}  {'E_1':>12s}  {'E_1/theta':>12s}  {'E_1/theta^2':>12s}")
    print(f"  {'---':>8s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")

    for th, E1 in E1_theta:
        print(f"  {th:8.3f}  {E1:12.6f}  {E1/th:12.4f}  {E1/th**2:12.4f}")

    # Log-log fit for E_1 vs theta
    if len(E1_theta) >= 3:
        ths = np.array([x[0] for x in E1_theta], dtype=float)
        Es = np.array([x[1] for x in E1_theta], dtype=float)
        coeffs_th = np.polyfit(np.log(ths), np.log(Es), 1)
        print(f"\n  Log-log fit: E_1 ~ theta^({coeffs_th[0]:.3f})")
        print(f"  If m ~ theta, PIB predicts E ~ 1/m ~ theta^(-1) -> exponent = -1")
        print(f"  If E ~ theta (mass gap), exponent = +1")

    # ================================================================
    # TEST 4: Degeneracy structure
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 4: DEGENERACY STRUCTURE")
    print("=" * 70)

    theta = 0.3
    for n_y in [21, 31]:
        U = build_chiral_unitary(n_y, theta)
        phases, _ = extract_spectrum(U)

        # Check for phase pairs: +E and -E (parity symmetry)
        pos = np.sort(phases[phases > 1e-10])
        neg = np.sort(-phases[phases < -1e-10])

        print(f"\n  n_y={n_y}, theta={theta}")
        print(f"  Total eigenphases: {len(phases)}")
        print(f"  Positive phases: {len(pos)}")
        print(f"  Negative phases: {len(neg)}")

        # Check +/- pairing
        n_pairs = min(len(pos), len(neg))
        if n_pairs > 0:
            diffs = np.abs(pos[:n_pairs] - neg[:n_pairs])
            print(f"  +/- phase pairs (first {min(8, n_pairs)}):")
            for i in range(min(8, n_pairs)):
                print(f"    E_{i+1:2d}: +{pos[i]:.6f}  -{neg[i]:.6f}  diff={diffs[i]:.2e}")
            print(f"  Max pairing error: {np.max(diffs):.2e}")

        # Check for zero phases
        near_zero = np.sum(np.abs(phases) < 1e-8)
        near_pi = np.sum(np.abs(np.abs(phases) - np.pi) < 1e-8)
        print(f"  Phases near 0: {near_zero}")
        print(f"  Phases near +/-pi: {near_pi}")

    # ================================================================
    # TEST 5: Full spectrum visualization (print)
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 5: FULL SPECTRUM for n_y=21, theta=0.3")
    print("=" * 70)

    U = build_chiral_unitary(21, 0.3)
    phases, _ = extract_spectrum(U)
    all_sorted = np.sort(phases)

    print(f"\n  All {len(all_sorted)} eigenphases (sorted):")
    for i, ph in enumerate(all_sorted):
        print(f"    [{i:3d}] {ph:+.6f}")

    # ================================================================
    # TEST 6: Dispersion relation check
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 6: ANALYTIC vs NUMERICAL -- cos(E) = cos(theta)*cos(k)")
    print("=" * 70)

    theta = 0.3
    n_y = 101  # large box for good k-resolution
    U = build_chiral_unitary(n_y, theta)
    phases, _ = extract_spectrum(U)
    pos = np.sort(phases[phases > 1e-10])

    # For a box of width W with reflecting boundaries, k_n = n*pi/W
    # Dispersion: cos(E) = cos(theta)*cos(k)
    # So E_n = arccos(cos(theta)*cos(n*pi/W))

    print(f"\n  n_y={n_y}, theta={theta}")
    print(f"  {'n':>4s}  {'E_num':>12s}  {'E_analytic':>12s}  {'diff':>12s}")
    print(f"  {'---':>4s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")

    for n in range(1, min(11, len(pos) + 1)):
        k_n = n * np.pi / n_y
        arg = np.cos(theta) * np.cos(k_n)
        if abs(arg) <= 1:
            E_analytic = np.arccos(arg)
        else:
            E_analytic = float('nan')

        if n - 1 < len(pos):
            E_num = pos[n - 1]
            diff = abs(E_num - E_analytic)
            print(f"  {n:4d}  {E_num:12.6f}  {E_analytic:12.6f}  {diff:12.2e}")

    # ================================================================
    # TEST 7: Small-k expansion -- is E_n ~ theta + k^2/(2*sin(theta))?
    # ================================================================
    print("\n" + "=" * 70)
    print("TEST 7: SMALL-k EXPANSION -- E ~ theta + k^2/(2*sin(theta))")
    print("=" * 70)

    theta = 0.3
    n_y = 101

    U = build_chiral_unitary(n_y, theta)
    phases, _ = extract_spectrum(U)
    pos = np.sort(phases[phases > 1e-10])

    mass_gap = theta  # E(k=0) = arccos(cos(theta)) = theta for small theta
    eff_mass = np.sin(theta)  # from d^2E/dk^2 at k=0

    print(f"\n  theta={theta}, mass_gap(analytic)={mass_gap:.6f}")
    print(f"  effective mass = sin(theta) = {eff_mass:.6f}")
    print(f"  W={n_y}")
    print()
    print(f"  {'n':>4s}  {'E_n':>10s}  {'E_n-gap':>10s}  {'n^2*pi^2/(2mW^2)':>18s}  {'ratio':>8s}")
    print(f"  {'---':>4s}  {'---':>10s}  {'---':>10s}  {'---':>18s}  {'---':>8s}")

    for i in range(min(8, len(pos))):
        n = i + 1
        En = pos[i]
        kinetic = En - mass_gap
        predicted = n**2 * np.pi**2 / (2 * eff_mass * n_y**2)
        ratio = kinetic / predicted if abs(predicted) > 1e-15 else float('nan')
        print(f"  {n:4d}  {En:10.6f}  {kinetic:10.6f}  {predicted:18.6f}  {ratio:8.4f}")

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    # Recompute key results for summary
    # Box-size scaling
    if len(E1_values) >= 3:
        Ws = np.array([x[0] for x in E1_values], dtype=float)
        Es = np.array([x[1] for x in E1_values], dtype=float)
        coeffs = np.polyfit(np.log(Ws), np.log(Es), 1)
        print(f"\n  Box-size scaling: E_1 ~ W^({coeffs[0]:.3f})")

    if len(E1_theta) >= 3:
        ths = np.array([x[0] for x in E1_theta], dtype=float)
        Es = np.array([x[1] for x in E1_theta], dtype=float)
        coeffs_th = np.polyfit(np.log(ths), np.log(Es), 1)
        print(f"  Mass dependence: E_1 ~ theta^({coeffs_th[0]:.3f})")

    print(f"\n  HYPOTHESIS: E_n ~ n^2 (particle-in-a-box)")

    # Check: are the ratios E_n/E_1 close to n^2?
    U = build_chiral_unitary(41, 0.3)
    phases, _ = extract_spectrum(U)
    pos = np.sort(phases[phases > 1e-10])
    if len(pos) >= 5:
        ratios = [pos[i] / pos[0] for i in range(5)]
        n_sq = [1, 4, 9, 16, 25]
        max_dev = max(abs(ratios[i] / n_sq[i] - 1) for i in range(5))
        print(f"  Max deviation of E_n/E_1 from n^2 (n=1..5): {max_dev:.4f}")

        if max_dev < 0.1:
            verdict = "PASS -- spectrum is approximately n^2"
        else:
            verdict = "FAIL -- spectrum deviates significantly from n^2"
            # Check if it's linear instead
            n_lin = [1, 2, 3, 4, 5]
            max_dev_lin = max(abs(ratios[i] / n_lin[i] - 1) for i in range(5))
            if max_dev_lin < 0.1:
                verdict += f"\n  BUT: E_n/E_1 ~ n (linear, not quadratic!) max_dev_lin={max_dev_lin:.4f}"

        print(f"\n  VERDICT: {verdict}")

    # Final: what IS the correct dispersion?
    print(f"\n  The CORRECT dispersion is: cos(E) = cos(theta)*cos(k)")
    print(f"  For small k: E ~ theta + k^2/(2*sin(theta))")
    print(f"  This is particle-in-a-box WITH a mass gap theta.")
    print(f"  The kinetic part (E - theta) should scale as n^2.")

    # Check kinetic part scaling
    if len(pos) >= 5:
        kinetic = [pos[i] - theta for i in range(5)]
        if kinetic[0] > 1e-10:
            k_ratios = [kinetic[i] / kinetic[0] for i in range(5)]
            n_sq = [1, 4, 9, 16, 25]
            max_dev_k = max(abs(k_ratios[i] / n_sq[i] - 1) for i in range(5))
            print(f"  Max deviation of (E_n-theta)/(E_1-theta) from n^2: {max_dev_k:.4f}")

            if max_dev_k < 0.1:
                print(f"  --> KINETIC PART matches n^2: PARTICLE-IN-A-BOX CONFIRMED")
            else:
                print(f"  --> Kinetic part does NOT match n^2")
                # Print the actual ratios
                print(f"  Kinetic ratios: {[f'{r:.3f}' for r in k_ratios]}")
                print(f"  Expected n^2:   {n_sq}")


if __name__ == "__main__":
    main()
