#!/usr/bin/env python3
"""Direct lattice contact-propagator computation for a Coulomb/free pair.

This lane answers the specific review objection that the DM work had only
compared continuum Sommerfeld/Gamow formulas without building and inverting
the discrete Hamiltonians.

What this script computes:
  - a radial finite-difference Hamiltonian H_free
  - a radial finite-difference Hamiltonian H_Coulomb
  - the literal contact resolvent element G(0,0; E) from
      (E + i eta - H)^{-1}
  - a driven s-wave contact-amplitude proxy with the same matrices

What it does NOT claim:
  - exact continuum equality with the Sommerfeld factor
  - full Omega_DM/Omega_b closure
  - a freeze-out derivation from graph axioms alone

The strongest honest claim supported by the code is that the direct finite-
lattice contact response is a real observable and that the attractive Coulomb
channel enhances the driven contact amplitude relative to the free case on the
same discretization. The contact resolvent ratio is also well-defined, but it is
scheme/boundary sensitive and should be treated as a diagnostic, not a closure.
"""

from __future__ import annotations

import math
import time

import numpy as np

try:
    from scipy.sparse import csc_matrix, diags, identity
    from scipy.sparse.linalg import spsolve
    HAS_SCIPY = True
except ImportError:  # pragma: no cover
    HAS_SCIPY = False


LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-dm_contact_propagator.txt"

results: list[str] = []


def log(msg: str = "") -> None:
    results.append(msg)
    print(msg)


PI = math.pi
MU = 0.5
C_F = 4.0 / 3.0
ALPHA_S = 0.092
ALPHA_EFF = C_F * ALPHA_S
X_F = 25.0
V_REL = 2.0 / math.sqrt(X_F)
K_ON_SHELL = MU * V_REL
E_ON_SHELL = K_ON_SHELL * K_ON_SHELL / (2.0 * MU)
ETA = 1e-3
R_BOX = 20.0
SCANS = [0.20, 0.10, 0.05]


def sommerfeld_target(alpha_eff: float, v_rel: float) -> float:
    zeta = alpha_eff / v_rel
    if abs(zeta) < 1e-14:
        return 1.0
    return (PI * zeta) / (1.0 - np.exp(-PI * zeta))


def build_radial_hamiltonian(n_sites: int, a: float, alpha_eff: float) -> csc_matrix:
    """Build the s-wave radial Hamiltonian on interior sites r_i = i*a.

    The grid has Dirichlet boundary conditions at r=0 and r=R=n_sites*a.
    Unknowns live on i=1..n_sites-1.
    """
    n_int = n_sites - 1
    if n_int < 2:
        raise ValueError("Need at least three radial sites")

    r = np.arange(1, n_sites, dtype=float) * a
    kinetic_diag = np.full(n_int, 1.0 / (MU * a * a))
    kinetic_off = np.full(n_int - 1, -1.0 / (2.0 * MU * a * a))
    potential = np.zeros(n_int)
    if alpha_eff != 0.0:
        potential = -alpha_eff / r

    return diags(
        [kinetic_off, kinetic_diag + potential, kinetic_off],
        offsets=[-1, 0, 1],
        format="csc",
    )


def direct_contact_resolvent_ratio(a: float, alpha_eff: float) -> tuple[complex, complex]:
    """Return G_C(0,0;E) and G_F(0,0;E) on the finite lattice."""
    n_sites = int(round(R_BOX / a))
    if abs(n_sites * a - R_BOX) > 1e-12:
        raise ValueError("R_BOX must be an integer multiple of the lattice spacing")

    h_free = build_radial_hamiltonian(n_sites, a, 0.0)
    h_coul = build_radial_hamiltonian(n_sites, a, alpha_eff)
    n_int = n_sites - 1
    eye = identity(n_int, format="csc", dtype=complex)
    rhs = np.zeros(n_int, dtype=complex)
    rhs[0] = 1.0

    g_free = spsolve((E_ON_SHELL + 1j * ETA) * eye - h_free, rhs)
    g_coul = spsolve((E_ON_SHELL + 1j * ETA) * eye - h_coul, rhs)
    return g_coul[0], g_free[0]


def driven_contact_amplitude_ratio(a: float, alpha_eff: float) -> tuple[float, float]:
    """Solve the boundary-driven radial system and return contact enhancement.

    The same finite-difference Hamiltonian is used for the free and Coulomb
    cases.  The right boundary is fixed to the free outgoing s-wave
    normalization u(R) = sin(k R); the contact enhancement is measured from
    the first few lattice sites near r = 0.
    """
    n_sites = int(round(R_BOX / a))
    n_int = n_sites - 1
    r = np.arange(1, n_sites, dtype=float) * a
    k = K_ON_SHELL

    def solve(alpha: float) -> np.ndarray:
        h = build_radial_hamiltonian(n_sites, a, alpha)
        a_mat = h - E_ON_SHELL * identity(n_int, format="csc", dtype=complex)
        b = np.zeros(n_int, dtype=complex)
        b[-1] = (1.0 / (2.0 * MU * a * a)) * math.sin(k * R_BOX)
        return spsolve(a_mat, b)

    u_free = solve(0.0)
    u_coul = solve(alpha_eff)

    # Average the first few interior points to reduce site-level jitter.
    w = slice(0, min(5, n_int))
    amp_free = np.mean(np.abs(u_free[w]) ** 2)
    amp_coul = np.mean(np.abs(u_coul[w]) ** 2)
    return float(amp_coul / amp_free), float(np.abs(u_coul[0] / u_free[0]))


def main() -> int:
    if not HAS_SCIPY:
        log("scipy is required for the direct matrix inversion lane")
        return 1

    log("=" * 78)
    log("DM DIRECT CONTACT-PROPAGATOR COMPUTATION")
    log("=" * 78)
    log(f"alpha_s = {ALPHA_S:.6f}")
    log(f"alpha_eff = C_F * alpha_s = {ALPHA_EFF:.6f}")
    log(f"x_F = {X_F:.1f}")
    log(f"v_rel = 2/sqrt(x_F) = {V_REL:.6f}")
    log(f"Sommerfeld target for this benchmark = {sommerfeld_target(ALPHA_EFF, V_REL):.6f}")
    log()
    log("We now invert the finite-lattice Hamiltonians directly.")
    log("The radial discretization is the s-wave contact channel of the 3D Coulomb problem.")
    log()

    log(f"{'a':>8s} {'N':>6s} {'|G_C/G_F|':>12s} {'contact amp ratio':>18s} {'|u_C/u_F|_0':>12s}")
    log("-" * 70)

    ratios = []
    for a in SCANS:
        n_sites = int(round(R_BOX / a))
        g_c, g_f = direct_contact_resolvent_ratio(a, ALPHA_EFF)
        contact_ratio, site_ratio = driven_contact_amplitude_ratio(a, ALPHA_EFF)
        ratios.append((a, n_sites, abs(g_c / g_f), contact_ratio, site_ratio))
        log(f"{a:8.3f} {n_sites:6d} {abs(g_c / g_f):12.6f} {contact_ratio:18.6f} {site_ratio:12.6f}")

    log("-" * 70)
    log()
    log("Interpretation:")
    log("  - |G_C/G_F| is the literal contact resolvent ratio on the finite lattice.")
    log("  - The boundary-driven contact amplitude is the stronger physical proxy.")
    log("  - The Coulomb channel enhances the contact response relative to free.")
    log("  - The exact continuum Sommerfeld equality is not yet proven by this script.")
    log("  - Freeze-out and the full Omega_DM/Omega_B chain remain separate work.")
    log()

    try:
        import os
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        log(f"Log saved to {LOG_FILE}")
    except Exception as exc:  # pragma: no cover
        log(f"Could not save log: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
