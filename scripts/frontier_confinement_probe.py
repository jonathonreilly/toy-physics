#!/usr/bin/env python3
"""
Confinement Probe: String Tension from Parity-Coupled Staggered Fermion
========================================================================
Tests whether the parity-coupled staggered fermion produces linear
confinement (string tension) between two opposite-sign sources.

Protocol:
  1. On a 2D periodic lattice (side=12), place two point sources:
       rho_A[node] = +G   at position (3, 6)
       rho_B[node] = -G   at position (9, 6)
  2. Solve combined potential: (L + mu^2) Phi = rho_A + rho_B
  3. Evolve staggered wavepacket under this combined potential
  4. Measure total energy E(r) as function of source separation r
     for r = 2, 3, 4, 5, 6, 7, 8
  5. Fit E(r) to:
       Coulomb: E = a/r + b
       Linear:  E = sigma*r + c
       Cornell: E = a/r + sigma*r + c
  6. If sigma > 0 in linear or Cornell fit, there is string tension
  7. Measure flux tube: |Phi(x,y)| along line connecting sources

Parameters: MASS=0.30, MU2=0.22, DT=0.12, G=5.0, N_STEPS=30
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
SIDE = 12
MASS = 0.30
MU2 = 0.22
DT = 0.12
G = 5.0
N_STEPS = 30
SEPARATIONS = [2, 3, 4, 5, 6, 7, 8]

# ---------------------------------------------------------------------------
# Lattice infrastructure
# ---------------------------------------------------------------------------

def idx2(x, y, n):
    return (x % n) * n + (y % n)


def build_2d_laplacian(n):
    """Graph Laplacian for 2D periodic square lattice."""
    N = n * n
    L = lil_matrix((N, N), dtype=float)
    for x in range(n):
        for y in range(n):
            i = idx2(x, y, n)
            neighbors = [
                idx2(x + 1, y, n), idx2(x - 1, y, n),
                idx2(x, y + 1, n), idx2(x, y - 1, n),
            ]
            for j in neighbors:
                L[i, j] -= 1.0
                L[i, i] += 1.0
    return L.tocsr()


def parity_2d(n):
    """Staggered parity epsilon(x) = (-1)^(x+y)."""
    N = n * n
    par = np.zeros(N)
    for x in range(n):
        for y in range(n):
            par[idx2(x, y, n)] = (-1) ** (x + y)
    return par


def build_H_staggered_2d(n, mass, phi, par):
    """2D staggered Dirac Hamiltonian with parity coupling.

    H = hopping + (mass + phi) * parity
    """
    N = n * n
    H = lil_matrix((N, N), dtype=complex)

    # Diagonal: parity-coupled mass + potential
    H.setdiag((mass + phi) * par)

    # Hopping: eta_mu phases
    for x in range(n):
        for y in range(n):
            i = idx2(x, y, n)

            # x-direction: eta_1 = 1
            j_fwd = idx2(x + 1, y, n)
            j_bwd = idx2(x - 1, y, n)
            H[i, j_fwd] += -0.5j
            H[i, j_bwd] += 0.5j

            # y-direction: eta_2 = (-1)^x
            eta2 = (-1) ** x
            j_fwd = idx2(x, y + 1, n)
            j_bwd = idx2(x, y - 1, n)
            H[i, j_fwd] += eta2 * (-0.5j)
            H[i, j_bwd] += eta2 * 0.5j

    return H.tocsr()


def evolve_cn(H, N, dt, n_steps, psi0):
    """Crank-Nicolson evolution: i dpsi/dt = H psi."""
    Ap = (speye(N) + 0.5j * dt * H).tocsc()
    Am = speye(N) - 0.5j * dt * H
    psi = psi0.copy()
    for _ in range(n_steps):
        psi = spsolve(Ap, Am.dot(psi))
    return psi


# ---------------------------------------------------------------------------
# Energy measurement
# ---------------------------------------------------------------------------

def measure_energy(psi, H):
    """<psi|H|psi> / <psi|psi>."""
    Hpsi = H.dot(psi)
    return np.real(np.vdot(psi, Hpsi) / np.vdot(psi, psi))


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_confinement_probe():
    print("=" * 70)
    print("CONFINEMENT PROBE: String Tension from Parity-Coupled Staggered Fermion")
    print("=" * 70)
    print(f"  Lattice: {SIDE}x{SIDE} periodic")
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, G={G}, N_STEPS={N_STEPS}")
    print()

    n = SIDE
    N = n * n
    par = parity_2d(n)
    L = build_2d_laplacian(n)
    op = (L + MU2 * speye(N)).tocsc()

    # Source A fixed at (3, 6)
    src_a = idx2(3, 6, n)

    # Initial wavepacket: Gaussian centered at (6, 6) — midpoint
    psi0 = np.zeros(N, dtype=complex)
    cx, cy = 6, 6
    sigma = 1.5
    for x in range(n):
        for y in range(n):
            dx = min(abs(x - cx), n - abs(x - cx))
            dy = min(abs(y - cy), n - abs(y - cy))
            psi0[idx2(x, y, n)] = np.exp(-(dx**2 + dy**2) / (2 * sigma**2))
    psi0 /= np.linalg.norm(psi0)

    # -----------------------------------------------------------------------
    # Sweep over separations
    # -----------------------------------------------------------------------
    print("-" * 70)
    print(f"  {'r':>4s}  {'src_B pos':>12s}  {'E(r)':>12s}  {'|psi| norm':>12s}")
    print("-" * 70)

    energies = []
    for r in SEPARATIONS:
        # Source B at (3+r, 6) with opposite sign
        bx = (3 + r) % n
        src_b = idx2(bx, 6, n)

        # Combined charge density
        rho = np.zeros(N)
        rho[src_a] = +G
        rho[src_b] = -G

        # Solve for potential
        phi = spsolve(op, rho)

        # Build Hamiltonian with this potential
        H = build_H_staggered_2d(n, MASS, phi, par)

        # Evolve wavepacket
        psi = evolve_cn(H, N, DT, N_STEPS, psi0)
        norm = np.linalg.norm(psi)

        # Measure energy
        E = measure_energy(psi, H)
        energies.append(E)

        print(f"  {r:4d}  ({bx:2d}, 6)       {E:12.6f}  {norm:12.6f}")

    r_arr = np.array(SEPARATIONS, dtype=float)
    E_arr = np.array(energies)

    # -----------------------------------------------------------------------
    # Fits
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("FIT RESULTS")
    print("=" * 70)

    # Coulomb: E = a/r + b
    def coulomb(r, a, b):
        return a / r + b

    # Linear: E = sigma*r + c
    def linear(r, sigma, c):
        return sigma * r + c

    # Cornell: E = a/r + sigma*r + c
    def cornell(r, a, sigma, c):
        return a / r + sigma * r + c

    # Coulomb fit
    try:
        popt_c, pcov_c = curve_fit(coulomb, r_arr, E_arr)
        E_pred_c = coulomb(r_arr, *popt_c)
        resid_c = np.sqrt(np.mean((E_arr - E_pred_c)**2))
        print(f"\n  Coulomb fit:  E = {popt_c[0]:.6f}/r + {popt_c[1]:.6f}")
        print(f"    RMS residual: {resid_c:.6e}")
    except Exception as e:
        print(f"\n  Coulomb fit FAILED: {e}")
        popt_c = None
        resid_c = float('inf')

    # Linear fit
    try:
        popt_l, pcov_l = curve_fit(linear, r_arr, E_arr)
        E_pred_l = linear(r_arr, *popt_l)
        resid_l = np.sqrt(np.mean((E_arr - E_pred_l)**2))
        sigma_l = popt_l[0]
        print(f"\n  Linear fit:   E = {sigma_l:.6f}*r + {popt_l[1]:.6f}")
        print(f"    String tension sigma = {sigma_l:.6f}")
        print(f"    RMS residual: {resid_l:.6e}")
        if sigma_l > 0:
            print(f"    --> POSITIVE string tension: confining potential!")
        else:
            print(f"    --> Negative sigma: no confinement")
    except Exception as e:
        print(f"\n  Linear fit FAILED: {e}")
        popt_l = None
        resid_l = float('inf')
        sigma_l = 0.0

    # Cornell fit
    try:
        p0 = [popt_c[0] if popt_c is not None else 0.1,
              sigma_l if popt_l is not None else 0.01,
              0.0]
        popt_cr, pcov_cr = curve_fit(cornell, r_arr, E_arr, p0=p0, maxfev=5000)
        E_pred_cr = cornell(r_arr, *popt_cr)
        resid_cr = np.sqrt(np.mean((E_arr - E_pred_cr)**2))
        sigma_cr = popt_cr[1]
        print(f"\n  Cornell fit:  E = {popt_cr[0]:.6f}/r + {sigma_cr:.6f}*r + {popt_cr[2]:.6f}")
        print(f"    Coulomb coeff a = {popt_cr[0]:.6f}")
        print(f"    String tension sigma = {sigma_cr:.6f}")
        print(f"    Constant c = {popt_cr[2]:.6f}")
        print(f"    RMS residual: {resid_cr:.6e}")
        if sigma_cr > 0:
            print(f"    --> POSITIVE string tension in Cornell fit!")
        else:
            print(f"    --> No confinement in Cornell fit")
    except Exception as e:
        print(f"\n  Cornell fit FAILED: {e}")
        popt_cr = None
        resid_cr = float('inf')
        sigma_cr = 0.0

    # Best fit comparison
    print(f"\n  Best fit (lowest RMS):")
    fits = [("Coulomb", resid_c), ("Linear", resid_l), ("Cornell", resid_cr)]
    fits.sort(key=lambda x: x[1])
    for name, r in fits:
        print(f"    {name:10s}: RMS = {r:.6e}")

    # -----------------------------------------------------------------------
    # Flux tube measurement
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("FLUX TUBE PROFILE")
    print("=" * 70)

    # Use the r=6 case (sources at (3,6) and (9,6))
    r_flux = 6
    bx_flux = (3 + r_flux) % n
    src_b_flux = idx2(bx_flux, 6, n)
    rho_flux = np.zeros(N)
    rho_flux[src_a] = +G
    rho_flux[src_b_flux] = -G
    phi_flux = spsolve(op, rho_flux)

    # Along the source axis (y=6, varying x)
    print(f"\n  |Phi| along y=6 (source axis), sources at x=3 and x={bx_flux}:")
    print(f"  {'x':>4s}  {'|Phi|':>12s}  {'profile':>30s}")
    print(f"  {'-'*4}  {'-'*12}  {'-'*30}")

    phi_axis = []
    for x in range(n):
        val = abs(phi_flux[idx2(x, 6, n)])
        phi_axis.append(val)

    max_phi = max(phi_axis) if max(phi_axis) > 0 else 1.0
    for x in range(n):
        val = phi_axis[x]
        bar_len = int(28 * val / max_phi)
        bar = "#" * bar_len
        marker = ""
        if x == 3:
            marker = " <-- source A (+G)"
        elif x == bx_flux:
            marker = " <-- source B (-G)"
        print(f"  {x:4d}  {val:12.6f}  {bar}{marker}")

    # Transverse profile at midpoint x=6
    print(f"\n  |Phi| transverse at x=6 (midpoint between sources):")
    print(f"  {'y':>4s}  {'|Phi|':>12s}  {'profile':>30s}")
    print(f"  {'-'*4}  {'-'*12}  {'-'*30}")

    phi_trans = []
    for y in range(n):
        val = abs(phi_flux[idx2(6, y, n)])
        phi_trans.append(val)

    max_phi_t = max(phi_trans) if max(phi_trans) > 0 else 1.0
    for y in range(n):
        val = phi_trans[y]
        bar_len = int(28 * val / max_phi_t)
        bar = "#" * bar_len
        print(f"  {y:4d}  {val:12.6f}  {bar}")

    # Flux tube width: ratio of on-axis to off-axis field
    on_axis = abs(phi_flux[idx2(6, 6, n)])
    off_axis_1 = abs(phi_flux[idx2(6, 4, n)])
    off_axis_2 = abs(phi_flux[idx2(6, 8, n)])
    off_axis_avg = (off_axis_1 + off_axis_2) / 2

    print(f"\n  Flux tube concentration:")
    print(f"    On-axis |Phi(6,6)|  = {on_axis:.6f}")
    print(f"    Off-axis avg |Phi| = {off_axis_avg:.6f}")
    if off_axis_avg > 0:
        ratio = on_axis / off_axis_avg
        print(f"    Concentration ratio = {ratio:.3f}")
        if ratio > 2.0:
            print(f"    --> Field concentrated into tube (ratio > 2)")
        else:
            print(f"    --> Field spreads like Coulomb (ratio ~ 1)")
    else:
        print(f"    Off-axis field is zero — trivially concentrated")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\n  E(r) values:")
    for r, E in zip(SEPARATIONS, energies):
        print(f"    r={r}: E={E:.6f}")

    has_confinement = (sigma_l > 0) or (sigma_cr > 0)
    print(f"\n  String tension (linear fit):  sigma = {sigma_l:.6f}")
    if popt_cr is not None:
        print(f"  String tension (Cornell fit): sigma = {sigma_cr:.6f}")
    print(f"\n  Confinement detected: {'YES' if has_confinement else 'NO'}")

    if has_confinement:
        print(f"\n  REMARKABLE: The parity-coupled staggered fermion produces")
        print(f"  linear confinement between opposite-sign sources.")
        print(f"  Same mechanism as gravity generates string tension.")
    else:
        print(f"\n  No linear confinement detected. The potential between")
        print(f"  opposite-sign sources does not grow linearly with separation.")


if __name__ == "__main__":
    run_confinement_probe()
