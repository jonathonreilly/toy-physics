#!/usr/bin/env python3
"""Map the Lorentzian stability window: at which k values does the
phase-weighted metric have Lorentzian signature, and why?

BACKGROUND:
  frontier_phase_metric.py found Lorentzian (-,+,+,+) at k=3 and k=10
  in 3+1D, but Euclidean at k=0.5, 1, 5, 8. The signature oscillates
  with k. This script maps the full k-dependence at fine resolution
  to understand the structure.

KEY PHYSICS QUESTION:
  The phase factor is Re(exp(i*k*L)) = cos(k*L). For the forward edge
  (dy=dz=dw=0), L = h, so the phase is cos(k*h). For diagonal edges,
  L = h*sqrt(1+n^2*h^2). The signature flips when the causal-direction
  phase becomes negative while spatial phases stay positive (or vice
  versa). This happens when k*h crosses pi/2 + n*pi for the forward
  edge but NOT for the diagonal edges.

  The NATURAL k where Lorentzian signature is most stable should be
  where cos(k*h) < 0 (forward edge has negative phase) while
  cos(k*L_diagonal) > 0 (spatial edges have positive phase). This
  window is: pi/(2h) < k < pi/(2*L_min_diagonal).

EXPERIMENT:
  1. Fine k sweep (0.1 to 15.0, step 0.1) in 3+1D: plot the causal
     eigenvalue as a function of k. Identify Lorentzian windows.
  2. Compare the causal eigenvalue to cos(k*h) to verify the mechanism.
  3. Check whether the window depends on h (lattice spacing).
  4. Compute the effective "light cone angle" in Lorentzian windows.
"""

from __future__ import annotations
import math
import numpy as np


def compute_phase_metric(dims, h, max_d_phys, k, weight_fn, p):
    """Compute phase-weighted metric tensor in arbitrary dimensions.

    dims = 3 for 2+1D (x,y,z), dims = 4 for 3+1D (x,y,z,w).
    """
    d_spatial = dims - 1
    max_d = max(1, round(max_d_phys / h))
    metric = np.zeros((dims, dims))
    norm = 0.0

    # Generate all offset combinations for d_spatial transverse dims
    from itertools import product
    offsets = list(product(range(-max_d, max_d + 1), repeat=d_spatial))

    for off in offsets:
        dx_vec = np.array([h] + [o * h for o in off])
        L = np.linalg.norm(dx_vec)
        r_trans = np.linalg.norm(dx_vec[1:])
        theta = math.atan2(r_trans, h)
        w = weight_fn(theta)

        S = L  # free-space valley-linear
        phase_factor = math.cos(k * S)

        measure = h ** d_spatial
        contribution = phase_factor * w * measure / (L ** p)
        metric += contribution * np.outer(dx_vec, dx_vec) / (L ** 2)
        norm += abs(contribution)

    if norm > 1e-30:
        metric /= norm

    return metric


def main():
    print("=" * 72)
    print("LORENTZIAN STABILITY WINDOW")
    print("=" * 72)
    print()

    kernels = [
        ("cos^2(theta)", lambda t: math.cos(t) ** 2),
        ("exp(-0.8t^2)", lambda t: math.exp(-0.8 * t * t)),
    ]

    # ==================================================================
    # Part 1: Fine k sweep in 3+1D
    # ==================================================================
    print("PART 1: Fine k sweep in 3+1D (h=1.0)")
    print("  Tracking causal eigenvalue (should be negative for Lorentzian)")
    print()

    h = 1.0
    max_d_phys = 2
    p = 3  # 1/L^3 for 3 spatial dims

    # Compute L values for reference
    L_forward = h  # pure causal edge
    L_diag1 = math.sqrt(h**2 + h**2)  # one transverse step
    L_diag2 = math.sqrt(h**2 + 2*h**2)  # two transverse steps
    print(f"  Edge lengths: forward={L_forward:.3f}, diag1={L_diag1:.3f}, diag2={L_diag2:.3f}")
    print(f"  cos(k*L_fwd)=0 at k = pi/(2*{L_forward:.3f}) = {math.pi/(2*L_forward):.3f}")
    print(f"  cos(k*L_d1)=0  at k = pi/(2*{L_diag1:.3f}) = {math.pi/(2*L_diag1):.3f}")
    print()

    k_values = np.arange(0.1, 15.01, 0.1)

    for name, wfn in kernels:
        print(f"  Kernel: {name}")
        print(f"  {'k':>6} | {'eig_causal':>12} | {'eig_spat':>12} | {'cos(kh)':>10} | {'signature':>15}")
        print(f"  {'-'*65}")

        lorentz_windows = []
        prev_sig = None

        for kk in k_values:
            g = compute_phase_metric(4, h, max_d_phys, kk, wfn, p)
            evals = np.sort(np.linalg.eigvalsh(g))
            # Causal eigenvalue: the one associated with the x-direction
            # In our convention, the causal direction gets the largest
            # or smallest eigenvalue depending on the kernel
            eig_causal = evals[0]  # smallest eigenvalue
            eig_spatial = evals[1]  # next (spatial should be degenerate)

            cos_kh = math.cos(kk * h)

            n_neg = sum(1 for e in evals if e < -1e-10)
            n_pos = sum(1 for e in evals if e > 1e-10)
            if n_neg == 1 and n_pos == 3:
                sig = "LORENTZIAN"
            elif n_neg == 0:
                sig = "Euclidean"
            elif n_neg == 3 and n_pos == 1:
                sig = "anti-Lorentz"
            else:
                sig = f"mixed({n_neg}-,{n_pos}+)"

            # Track Lorentzian windows
            if sig == "LORENTZIAN" and prev_sig != "LORENTZIAN":
                lorentz_windows.append({"start": kk, "end": kk})
            elif sig == "LORENTZIAN" and prev_sig == "LORENTZIAN":
                lorentz_windows[-1]["end"] = kk
            prev_sig = sig

            # Print at coarser intervals + all transitions
            if abs(kk % 1.0) < 0.05 or sig != prev_sig:
                print(f"  {kk:>6.2f} | {eig_causal:>+12.6f} | {eig_spatial:>+12.6f} | "
                      f"{cos_kh:>+10.4f} | {sig:>15}")

        print()
        if lorentz_windows:
            print(f"  Lorentzian windows:")
            for w in lorentz_windows:
                width = w["end"] - w["start"]
                center = (w["start"] + w["end"]) / 2
                print(f"    k = {w['start']:.2f} to {w['end']:.2f} "
                      f"(center={center:.2f}, width={width:.2f})")

            # Check if windows are periodic
            if len(lorentz_windows) >= 2:
                centers = [(w["start"] + w["end"]) / 2 for w in lorentz_windows]
                periods = [centers[i+1] - centers[i] for i in range(len(centers)-1)]
                if periods:
                    mean_period = sum(periods) / len(periods)
                    print(f"    Mean period between windows: {mean_period:.2f}")
                    print(f"    pi/h = {math.pi/h:.4f}")
                    print(f"    Ratio period/(pi/h): {mean_period/(math.pi/h):.4f}")
        else:
            print(f"  No Lorentzian windows found")
        print()

    # ==================================================================
    # Part 2: Mechanism analysis — cos(k*L) for different edge types
    # ==================================================================
    print("\n" + "=" * 72)
    print("PART 2: Phase mechanism — cos(k*L) for different edge types")
    print("=" * 72)
    print()
    print("  The forward (causal) edge has L = h.")
    print("  Diagonal edges have L = h*sqrt(1 + n^2) where n = transverse steps.")
    print("  Lorentzian signature requires cos(k*h) to have different sign")
    print("  from the weighted average of cos(k*L_diagonal).")
    print()

    # Show cos(k*L) for several edge types
    print(f"  {'k':>6} | {'cos(k*h)':>10} | {'cos(k*L1)':>10} | {'cos(k*L2)':>10} | {'cos(k*L3)':>10}")
    L1 = math.sqrt(h**2 + h**2)
    L2 = math.sqrt(h**2 + 2*h**2)
    L3 = math.sqrt(h**2 + 3*h**2)
    print(f"  {'':>6} | {'L=1.000':>10} | {'L=1.414':>10} | {'L=1.732':>10} | {'L=2.000':>10}")
    print(f"  {'-'*60}")
    for kk in np.arange(0.5, 15.01, 0.5):
        c0 = math.cos(kk * h)
        c1 = math.cos(kk * L1)
        c2 = math.cos(kk * L2)
        c3 = math.cos(kk * L3)
        # Mark where causal is negative but diagonals are positive
        marker = ""
        if c0 < 0 and (c1 > 0 or c2 > 0):
            marker = " <-- LORENTZIAN CANDIDATE"
        print(f"  {kk:>6.1f} | {c0:>+10.4f} | {c1:>+10.4f} | {c2:>+10.4f} | {c3:>+10.4f}{marker}")

    # ==================================================================
    # Part 3: h-dependence — does the Lorentzian window scale?
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("PART 3: Does the Lorentzian window scale with h?")
    print("=" * 72)
    print()
    print("  If the window is at k ~ pi/(2h), it's a lattice artifact.")
    print("  If it's at k ~ constant (independent of h), it's physical.")
    print()

    wfn = lambda t: math.cos(t) ** 2  # cos^2

    for h_test in [2.0, 1.0, 0.5, 0.25]:
        max_d_test = max(1, round(2 / h_test))
        p_test = 3  # 3+1D

        # Find first Lorentzian window
        first_lorentz_k = None
        for kk in np.arange(0.1, 30.01, 0.05):
            g = compute_phase_metric(4, h_test, 2, kk, wfn, p_test)
            evals = np.sort(np.linalg.eigvalsh(g))
            n_neg = sum(1 for e in evals if e < -1e-10)
            n_pos = sum(1 for e in evals if e > 1e-10)
            if n_neg == 1 and n_pos == 3:
                first_lorentz_k = kk
                break

        pi_over_2h = math.pi / (2 * h_test)
        if first_lorentz_k is not None:
            ratio = first_lorentz_k / pi_over_2h
            print(f"  h={h_test:.2f}: first Lorentzian at k={first_lorentz_k:.2f}, "
                  f"pi/(2h)={pi_over_2h:.2f}, ratio={ratio:.3f}")
        else:
            print(f"  h={h_test:.2f}: no Lorentzian window found in k=[0.1, 30.0]")

    # ==================================================================
    # Part 4: Effective light cone angle in Lorentzian windows
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("PART 4: Effective light cone in Lorentzian windows")
    print("=" * 72)
    print()
    print("  In Lorentzian signature (-,+,+,+), the light cone is defined by")
    print("  ds^2 = 0: g_00*dt^2 + g_11*(dx^2+dy^2+dz^2) = 0")
    print("  => c_eff = sqrt(-g_00/g_11) = signal speed")
    print()

    wfn = lambda t: math.cos(t) ** 2
    h_test = 1.0

    for kk in [3.0, 10.0]:
        g = compute_phase_metric(4, h_test, 2, kk, wfn, 3)
        evals = np.sort(np.linalg.eigvalsh(g))
        n_neg = sum(1 for e in evals if e < -1e-10)
        n_pos = sum(1 for e in evals if e > 1e-10)

        if n_neg == 1 and n_pos >= 1:
            g_causal = evals[0]  # negative
            g_spatial = evals[1]  # positive (degenerate)
            c_eff = math.sqrt(-g_causal / g_spatial) if g_spatial > 0 else float('inf')
            cone_angle = math.atan(1 / c_eff) * 180 / math.pi if c_eff > 0 else 90
            print(f"  k={kk:.1f}: g_causal={g_causal:+.6f}, g_spatial={g_spatial:+.6f}")
            print(f"    c_eff = sqrt({-g_causal:.6f}/{g_spatial:.6f}) = {c_eff:.4f}")
            print(f"    Light cone half-angle = {cone_angle:.1f} degrees")
            print(f"    (45 deg = standard light cone with c=1)")
        else:
            print(f"  k={kk:.1f}: not Lorentzian at this k")

    # ==================================================================
    # VERDICT
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)
    print()
    print("  Check the results above for:")
    print("  1. Whether Lorentzian windows are periodic (phase aliasing)")
    print("  2. Whether first Lorentzian k scales as pi/(2h) (lattice artifact)")
    print("     or is h-independent (physical)")
    print("  3. What the effective light cone speed is in Lorentzian windows")
    print()


if __name__ == "__main__":
    main()
