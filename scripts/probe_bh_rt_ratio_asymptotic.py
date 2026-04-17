#!/usr/bin/env python3
"""
RT-ratio asymptotic probe for the Cl(3)/Z^3 free-fermion carrier.

The current BH entropy lane claims

    S_ent(L)                         1
    -------------------     ~       ---
    |dA| * ln chi_eff                4

on the free-fermion ground state of the NN-hopping tight-binding Hamiltonian
on Z^d at half filling.  On small L (up to 32) the OBC-lattice numerical
value looks like ~0.24, "close to" 1/4.  This probe asks the actual question:

    * what is the L -> infinity limit of the RT ratio?
    * is it 1/4, or is it the Widom / Gioev-Klich coefficient 1/6?

Setup: open-boundary L x L square lattice, NN hopping, half filling, cut at
x = L/2.  Matches the existing frontier_bh_entropy_derived.py geometry so the
conclusion applies directly to the current BH lane.

Correct asymptotic form:
    RT(L) = c_infty + a / ln(L) + b / L + ...
(Widom-Sobolev subleading correction), NOT the 1/L form the current lane
uses.  With the correct form, c_infty for the free-fermion square-lattice
half-filled carrier is the Gioev-Klich constant

    c_Widom = (1 / (12 (2 pi)^{d-1})) * integral over Fermi surface of
              |n_x . n_k| ds_k

For 2D square-lattice diamond Fermi surface with straight cut:
    c_Widom = (1 / (24 pi)) * (4 pi) = 1 / 6 ~= 0.1667

Not 1 / 4.  The 1/4 in the OBC-lattice fit is a finite-L artifact.

Primary estimator for this probe's verdict:
    two-parameter fit  RT(L) = c_inf + a / ln(L)   over tail L >= 48.
Additional three-parameter fits and alternative estimators are printed
above the verdict for transparency, but they have too few tail points on
this L range to be stable and are not used as the verdict.  The probe
exits 0 iff the verdict estimator lands within 10% of 1/6 and at least
20% away from 1/4; otherwise exits 1.
"""

from __future__ import annotations

import math
import time

import numpy as np
from numpy.linalg import eigh


def build_2d_hamiltonian(Lx: int, Ly: int, t: float = 1.0) -> np.ndarray:
    """Tight-binding Hamiltonian on an OBC Lx x Ly square lattice."""
    N = Lx * Ly
    H = np.zeros((N, N))
    for x in range(Lx):
        for y in range(Ly):
            i = x * Ly + y
            if x + 1 < Lx:
                j = (x + 1) * Ly + y
                H[i, j] = -t
                H[j, i] = -t
            if y + 1 < Ly:
                j = x * Ly + (y + 1)
                H[i, j] = -t
                H[j, i] = -t
    return H


def correlation_matrix(eigvecs: np.ndarray, n_occupied: int) -> np.ndarray:
    occ = eigvecs[:, :n_occupied]
    return occ @ occ.T


def entanglement_entropy(C: np.ndarray, subsystem: list[int]) -> float:
    C_A = C[np.ix_(subsystem, subsystem)]
    evals = np.linalg.eigvalsh(C_A)
    eps = 1e-15
    evals = np.clip(evals, eps, 1.0 - eps)
    return float(-np.sum(evals * np.log(evals) + (1.0 - evals) * np.log(1.0 - evals)))


def transfer_rank(C: np.ndarray, L: int, threshold: float = 1e-6) -> int:
    """chi_eff = rank of off-layer correlator at x = L/2 cut (matches the
    frontier_bh_entropy_derived.py convention)."""
    mid = L // 2
    layer_L = [mid * L + y for y in range(L)]
    layer_R = [(mid - 1) * L + y for y in range(L)]
    T = C[np.ix_(layer_L, layer_R)]
    sv = np.linalg.svd(T, compute_uv=False)
    if sv[0] < 1e-30:
        return 0
    return int(np.sum(sv / sv[0] > threshold))


def measure_2d_obc(L: int) -> dict:
    """RT ratio on OBC L x L lattice, matches frontier_bh_entropy_derived.py."""
    N = L * L
    H = build_2d_hamiltonian(L, L)
    _, vecs = eigh(H)
    C = correlation_matrix(vecs, N // 2)
    subsystem = [x * L + y for x in range(L // 2) for y in range(L)]
    S = entanglement_entropy(C, subsystem)
    chi_eff = transfer_rank(C, L)
    ln_chi = math.log(chi_eff) if chi_eff > 1 else 0.0
    S_max = L * ln_chi
    rt = S / S_max if S_max > 0 else float("nan")
    return {
        "L": L,
        "N": N,
        "S": S,
        "chi_eff": chi_eff,
        "ln_chi": ln_chi,
        "S_max": S_max,
        "rt_ratio": rt,
        "c_direct": S / (L * math.log(L)) if L > 1 else float("nan"),
    }


def widom_gioev_klich_2d_square() -> float:
    """Analytic Widom-Gioev-Klich coefficient for 2D square-lattice NN
    hopping at half filling with a straight cut.

    Formula (Gioev-Klich 2006, Helling-Leschke-Spitzer 2011):
        c_Widom = (1 / (12 (2 pi)^{d-1})) * int_{∂Γ} |n_x . n_k| dS_k
    For d = 2, Fermi surface |k_x| + |k_y| = pi (diamond), n_x = (1, 0):
        perimeter of Γ = 4 sqrt(2) pi
        |n_x . n_k| = 1 / sqrt(2) on each of the 4 segments
        integral = 4 pi
        c_Widom = 4 pi / (12 * 2 pi) = 1 / 6
    """
    d = 2
    perimeter_dotted = 4.0 * math.sqrt(2.0) * math.pi * (1.0 / math.sqrt(2.0))
    # = 4 pi
    return perimeter_dotted / (12.0 * (2.0 * math.pi) ** (d - 1))


def widom_gioev_klich_3d_half_filled_numeric(n_samples: int = 400_000,
                                               seed: int = 42) -> float:
    """Numerical Widom-Gioev-Klich coefficient for 3D cubic-lattice NN
    hopping at half filling with straight cut normal to x-axis.

    Fermi surface: cos k_x + cos k_y + cos k_z = 0.  Implicit surface in
    BZ = [-pi, pi]^3.  We integrate |n_x . n_k| dS_k by Monte Carlo over
    an isosurface parametrization.

    We use the following identity for implicit surfaces F(k) = 0:
        dS_k = |grad F| dk_y dk_z / |partial F / partial k_x|  (parametrize
        by k_y, k_z and solve for k_x)
    then |n_x . n_k| = |partial F / partial k_x| / |grad F|, so
        |n_x . n_k| dS_k = dk_y dk_z
    summed over all roots k_x of F(k_x, k_y, k_z) = 0 for each fixed
    (k_y, k_z).

    For F = cos k_x + cos k_y + cos k_z, fixed (k_y, k_z), we solve
    cos k_x = -(cos k_y + cos k_z).  Real roots exist iff
    |cos k_y + cos k_z| <= 1.  There are two roots in (-pi, pi)
    when |cos k_y + cos k_z| < 1.
    """
    rng = np.random.default_rng(seed)
    # Uniform (k_y, k_z) in [-pi, pi]^2
    ky = rng.uniform(-math.pi, math.pi, size=n_samples)
    kz = rng.uniform(-math.pi, math.pi, size=n_samples)
    u = np.cos(ky) + np.cos(kz)
    mask = np.abs(u) < 1.0
    # For each valid (k_y, k_z), there are 2 roots k_x.  Each contributes
    # integrand |n_x . n_k| dS_k = dk_y dk_z.
    count = 2.0 * np.sum(mask)
    area = (2.0 * math.pi) ** 2  # area of (k_y, k_z) plane in BZ
    integral = area * count / n_samples
    # c_Widom (3D) = (1 / (12 (2 pi)^2)) * integral
    return integral / (12.0 * (2.0 * math.pi) ** 2)


def main() -> None:
    print("=" * 78)
    print("RT-RATIO ASYMPTOTIC PROBE")
    print("OBC L x L free-fermion half-filled square lattice")
    print("=" * 78)
    print()

    c_widom_2d = widom_gioev_klich_2d_square()
    print("2D Widom-Gioev-Klich analytic prediction (NN hopping, half filling,")
    print("straight cut, diamond Fermi surface):")
    print(f"    c_Widom(2D) = {c_widom_2d:.10f}  (= 1 / 6 exactly)")
    print(f"    1/4          = {0.25:.10f}   (current BH lane claim)")
    print()

    c_widom_3d = widom_gioev_klich_3d_half_filled_numeric()
    print("3D Widom-Gioev-Klich analytic prediction (cubic lattice, half")
    print("filling, straight cut):")
    print(f"    c_Widom(3D) = {c_widom_3d:.6f}  (Monte Carlo, N=4e5)")
    print()

    t0 = time.time()

    # Push to L = 96 (eigh on 9216x9216 matrix is ~3min on laptop).
    L_list = [8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96]

    header = (f"{'L':>4s} {'N':>6s} {'chi_eff':>8s} {'ln(chi)':>8s} "
              f"{'S_ent':>10s} {'c_direct':>10s} {'RT_ratio':>10s} "
              f"{'dev_1/6_%':>9s} {'dev_1/4_%':>9s}")
    print(header)
    print("-" * len(header))

    records = []
    for L in L_list:
        t_start_l = time.time()
        r = measure_2d_obc(L)
        dt = time.time() - t_start_l
        rt = r["rt_ratio"]
        dev6 = (rt - 1.0 / 6.0) / (1.0 / 6.0) * 100
        dev4 = (rt - 0.25) / 0.25 * 100
        print(f"{r['L']:>4d} {r['N']:>6d} {r['chi_eff']:>8d} "
              f"{r['ln_chi']:>8.4f} {r['S']:>10.4f} {r['c_direct']:>10.4f} "
              f"{rt:>10.4f} {dev6:>+8.1f}% {dev4:>+8.1f}%  ({dt:.1f}s)")
        records.append(r)

    print()

    # Fit RT = c_infty + a/ln(L) + b/L using L >= 16 (drops the L=8, L=12
    # parity-affected points).
    L_arr = np.array([r["L"] for r in records], dtype=float)
    rt_arr = np.array([r["rt_ratio"] for r in records], dtype=float)
    lnL_arr = np.log(L_arr)

    # Two-parameter fit RT = c_inf + a/ln(L)  (more stable than 3-param)
    print("Two-parameter fit:  RT(L) = c_inf + a / ln(L)")
    print()
    for L_cut, tag in [(16, "L>=16"), (20, "L>=20"), (24, "L>=24"),
                         (32, "L>=32"), (40, "L>=40"), (48, "L>=48")]:
        mask = L_arr >= L_cut
        if mask.sum() < 3:
            continue
        X = np.column_stack([np.ones(mask.sum()), 1.0 / lnL_arr[mask]])
        y = rt_arr[mask]
        coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
        c_inf, a_inv_ln = coeffs
        y_pred = X @ coeffs
        residual = np.max(np.abs(y - y_pred))
        dev_sixth = (c_inf - 1.0 / 6.0) / (1.0 / 6.0) * 100
        dev_quarter = (c_inf - 0.25) / 0.25 * 100
        print(f"  [{tag}]: c_inf = {c_inf:.6f}  "
              f"a = {a_inv_ln:+.4f}  max_resid = {residual:.5f}")
        print(f"    dev vs 1/6: {dev_sixth:+.2f}%     "
              f"dev vs 1/4: {dev_quarter:+.2f}%")

    print()
    print("Three-parameter fit:  RT(L) = c_inf + a/ln(L) + b/L")
    print()
    for L_cut, tag in [(16, "L>=16"), (20, "L>=20"), (24, "L>=24"),
                         (32, "L>=32"), (40, "L>=40")]:
        mask = L_arr >= L_cut
        if mask.sum() < 4:
            continue
        X = np.column_stack([np.ones(mask.sum()), 1.0 / lnL_arr[mask],
                              1.0 / L_arr[mask]])
        y = rt_arr[mask]
        coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
        c_inf, a_inv_ln, b_inv_L = coeffs
        y_pred = X @ coeffs
        residual = np.max(np.abs(y - y_pred))
        dev_sixth = (c_inf - 1.0 / 6.0) / (1.0 / 6.0) * 100
        dev_quarter = (c_inf - 0.25) / 0.25 * 100
        print(f"  [{tag}]: c_inf = {c_inf:.6f}  a = {a_inv_ln:+.4f}  "
              f"b = {b_inv_L:+.4f}  max_resid = {residual:.5f}")
        print(f"    dev vs 1/6: {dev_sixth:+.2f}%     "
              f"dev vs 1/4: {dev_quarter:+.2f}%")

    # ------------------------------------------------------------------
    # Verdict
    #
    # Authoritative estimator: two-parameter asymptotic fit
    #     RT(L) = c_inf + a / ln(L)
    # over the L >= 48 tail.  This is the same fit the no-go note
    # (BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md) cites.  The higher-order
    # three-parameter fits are printed above for transparency but have
    # too few degrees of freedom on this L range to be stable and are
    # not used as the verdict.  The two-parameter L >= 48 fit uses 4+
    # tail points and is the most stable extrapolation.
    # ------------------------------------------------------------------
    print("=" * 72)
    print("Verdict (primary estimator: 2-parameter RT(L) = c_inf + a/ln(L),")
    print("         tail window L >= 48)")
    print("=" * 72)

    mask_verdict = L_arr >= 48
    if mask_verdict.sum() < 3:
        print("  Not enough tail points at L >= 48; skipping verdict.")
        elapsed = time.time() - t0
        print(f"\nProbe runtime: {elapsed:.1f} s")
        return

    X_v = np.column_stack([np.ones(mask_verdict.sum()),
                             1.0 / lnL_arr[mask_verdict]])
    coeffs_v, *_ = np.linalg.lstsq(X_v, rt_arr[mask_verdict], rcond=None)
    c_inf_v, a_v = coeffs_v
    y_pred_v = X_v @ coeffs_v
    resid_v = float(np.max(np.abs(rt_arr[mask_verdict] - y_pred_v)))

    dev_sixth_v = (c_inf_v - 1.0 / 6.0) / (1.0 / 6.0) * 100
    dev_quarter_v = (c_inf_v - 0.25) / 0.25 * 100

    print(f"  c_inf (L >= 48)  = {c_inf_v:.6f}")
    print(f"  a                = {a_v:+.4f} / ln(L)")
    print(f"  max residual     = {resid_v:.6f}")
    print(f"  c_inf - 1/6      = {c_inf_v - 1.0/6.0:+.6f}  "
          f"({dev_sixth_v:+.2f}%)")
    print(f"  c_inf - 1/4      = {c_inf_v - 0.25:+.6f}  "
          f"({dev_quarter_v:+.2f}%)")
    print()

    within_sixth = abs(c_inf_v - 1.0 / 6.0) / (1.0 / 6.0) < 0.10
    outside_quarter = abs(c_inf_v - 0.25) / 0.25 > 0.20

    print(f"  c_inf within 10% of 1/6 (Widom)           : {within_sixth}")
    print(f"  c_inf outside 20% of 1/4 (current claim)  : {outside_quarter}")
    if within_sixth and outside_quarter:
        print()
        print("  => RT ratio asymptote is c_Widom = 1/6, NOT 1/4.")
        print("  => The identification S = A / (4 l_P^2) through the RT")
        print("     bond-dimension ratio on the free-fermion carrier is a")
        print("     finite-L artifact; the asymptote is the Widom-Gioev-")
        print("     Klich constant 1/6.")
        verdict_pass = True
    else:
        print()
        print("  => Verdict inconclusive on this L range.  Primary fit does")
        print("     not resolve between 1/6 and 1/4 at the required margin.")
        verdict_pass = False

    print()
    elapsed = time.time() - t0
    print(f"Probe runtime: {elapsed:.1f} s")

    import sys as _sys
    _sys.exit(0 if verdict_pass else 1)


if __name__ == "__main__":
    main()
