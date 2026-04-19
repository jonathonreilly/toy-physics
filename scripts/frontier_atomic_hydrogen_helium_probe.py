#!/usr/bin/env python3
"""Atomic hydrogen and helium probe --- standard-QM scaffold lane.

==========================================================================
PURPOSE: Open a lane on the atomic-scale gap in the CL3 lattice framework
by building a minimal, self-contained numerical solver that reproduces the
hydrogen spectrum and a variational helium ground state from STANDARD
quantum mechanics, in physical units.

This is a SCAFFOLD probe, not a retained framework derivation:

  - the inputs are textbook (m_e, e, hbar, 4*pi*epsilon_0, Z=1 / Z=2)
  - the Hamiltonian is the textbook nonrelativistic atomic Hamiltonian
  - no Cl(3)-on-Z^3 input is used anywhere in this script
  - the framework-internal route to these inputs (electron mass in MeV,
    Coulomb coupling in physical units, single-particle Schrodinger from
    the discrete-wave / path-sum surface) is exactly what the open
    matter / inertia / electromagnetism gaps would have to deliver

The lane's role is therefore twofold:

  1. confirm that standard numerics with standard inputs give the right
     hydrogen spectrum on this codebase --- so future framework-derived
     inputs can be substituted into the same harness without re-deriving
     the eigensolver
  2. record the helium baseline (independent-electron and one-parameter
     variational) as the next-step three-body discriminator any
     framework-internal atomic capability would have to beat

Hydrogen: the radial Schrodinger equation is solved by direct
diagonalization of the discrete radial Hamiltonian on a uniform grid
in r, for l = 0, 1, 2. The first five eigenvalues per channel are
compared to the analytic Bohr spectrum E_n = -13.6057 eV / n^2.

Helium: the closed-form solution is impossible (three-body), so we
report two reference levels --- (a) the independent-electron baseline
(2 * E_1s with Z=2, no electron-electron repulsion), and (b) the
single-parameter variational ground state with effective nuclear charge
Z_eff = 27/16 = 1.6875, which is the textbook minimum of
E(Z_eff) = Z_eff^2 - 2 Z Z_eff + (5/8) Z_eff in Hartree atomic units.
Both are compared to the experimental ground-state energy
-79.005 eV (NIST).

BOUNDED CLAIMS --- only what the numerics can support.
NO claim that the framework derives any of this.
PStack experiment: frontier-atomic-hydrogen-helium-probe
==========================================================================
"""

from __future__ import annotations

import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import eigsh
except ImportError:
    print("ERROR: scipy required.  pip install scipy")
    sys.exit(1)


# =========================================================================
# Physical constants (CODATA-style, eV / angstrom units)
# =========================================================================

HARTREE_EV = 27.211386245988
BOHR_ANG = 0.529177210903
RYDBERG_EV = HARTREE_EV / 2.0  # 13.6056931... eV


def analytic_hydrogen_energy(n: int) -> float:
    """Analytic Bohr level E_n = -RYDBERG_EV / n^2, in eV."""
    return -RYDBERG_EV / (n * n)


# =========================================================================
# Hydrogen: radial Schrodinger by direct diagonalization
# =========================================================================
#
# In Hartree atomic units (hbar = m_e = e = 1, 4*pi*eps_0 = 1) the
# radial equation for u(r) = r * R(r) is
#
#   [ -1/2 d^2/dr^2 + l(l+1)/(2 r^2) - Z/r ] u = E u
#
# with u(0) = 0 and u(r_max) = 0 (Dirichlet box).  We discretize on a
# uniform grid r_i = i * dr, i = 1..N, drop r=0 (singular), and use the
# standard 3-point Laplacian.  Eigenvalues are returned in eV.
# =========================================================================

def hydrogen_radial_eigenvalues(
    Z: int,
    l: int,
    n_grid: int = 8000,
    r_max: float = 200.0,
    n_states: int = 5,
) -> np.ndarray:
    """Return the n_states lowest eigenvalues of the radial H atom in eV.

    r_max is in Bohr.  n_grid is the number of interior grid points.
    """
    dr = r_max / (n_grid + 1)
    r = np.arange(1, n_grid + 1) * dr  # r_i, i=1..n_grid

    # -1/2 d^2/dr^2  ->  tridiag with diag = 1/dr^2, off-diag = -1/(2 dr^2)
    diag_kin = np.full(n_grid, 1.0 / (dr * dr))
    off_kin = np.full(n_grid - 1, -0.5 / (dr * dr))

    # Centrifugal + Coulomb potential, in Hartree
    v_centrifugal = 0.5 * l * (l + 1) / (r * r)
    v_coulomb = -Z / r
    diag_pot = v_centrifugal + v_coulomb

    diag = diag_kin + diag_pot
    H = sparse.diags(
        [off_kin, diag, off_kin],
        offsets=[-1, 0, 1],
        format='csr',
    )

    # Smallest algebraic eigenvalues = lowest energies (most negative).
    eigvals = eigsh(H, k=n_states, which='SA', return_eigenvectors=False)
    eigvals.sort()
    return eigvals * HARTREE_EV  # Hartree -> eV


def hydrogen_table(
    n_grid: int = 8000,
    r_max: float = 200.0,
) -> dict:
    """Build the hydrogen comparison table for l = 0, 1, 2."""
    rows = []
    for l in (0, 1, 2):
        e_numerical = hydrogen_radial_eigenvalues(
            Z=1, l=l, n_grid=n_grid, r_max=r_max, n_states=5,
        )
        # principal quantum numbers accessible at angular momentum l are
        # n = l+1, l+2, l+3, ...
        for k, e_num in enumerate(e_numerical):
            n = l + 1 + k
            e_exact = analytic_hydrogen_energy(n)
            rows.append({
                'l': l,
                'n': n,
                'E_numerical_eV': float(e_num),
                'E_analytic_eV': float(e_exact),
                'abs_error_eV': float(e_num - e_exact),
                'rel_error': float((e_num - e_exact) / e_exact),
            })
    return {
        'n_grid': n_grid,
        'r_max_bohr': r_max,
        'rows': rows,
    }


# =========================================================================
# Helium: independent-electron baseline + one-parameter variational
# =========================================================================
#
# Helium has no closed-form solution.  We report two standard textbook
# benchmarks, both in Hartree atomic units.
#
# (1) Independent-electron baseline (no e-e repulsion):
#     E0 = 2 * E_1s(Z=2) = 2 * (-Z^2/2) = -4 Hartree = -108.85 eV
#
# (2) Single-parameter variational ground state with trial wavefunction
#     psi(r1, r2) = exp(-Z_eff r1) exp(-Z_eff r2):
#         E(Z_eff) = Z_eff^2 - 2 Z Z_eff + (5/8) Z_eff   (Hartree)
#     Minimizing in Z_eff gives Z_eff* = Z - 5/16 = 27/16 for Z=2 and
#         E_var = -(Z - 5/16)^2 = -(27/16)^2 Hartree = -2.8477 Hartree
#               = -77.49 eV
#
# Experimental helium ground state (NIST):  E_exp = -79.0052 eV.
# =========================================================================

def helium_independent_electron_energy(Z: int = 2) -> float:
    """Two non-interacting 1s electrons, in eV."""
    return 2.0 * (-0.5 * Z * Z) * HARTREE_EV


def helium_variational_energy(Z: int = 2) -> tuple[float, float]:
    """One-parameter variational helium ground state.

    Returns (Z_eff_optimal, E_min_in_eV).
    """
    # E(Z_eff) = Z_eff^2 - 2 Z Z_eff + (5/8) Z_eff   (Hartree)
    # dE/dZ_eff = 2 Z_eff - 2 Z + 5/8 = 0
    # => Z_eff* = Z - 5/16
    z_eff = Z - 5.0 / 16.0
    e_min_hartree = z_eff * z_eff - 2.0 * Z * z_eff + (5.0 / 8.0) * z_eff
    return z_eff, e_min_hartree * HARTREE_EV


HELIUM_EXPERIMENTAL_EV = -79.0052  # NIST ground-state energy


def helium_table() -> dict:
    e_indep = helium_independent_electron_energy(Z=2)
    z_eff, e_var = helium_variational_energy(Z=2)
    return {
        'experimental_eV': HELIUM_EXPERIMENTAL_EV,
        'independent_electron_eV': e_indep,
        'independent_electron_error_eV': e_indep - HELIUM_EXPERIMENTAL_EV,
        'variational_Z_eff': z_eff,
        'variational_eV': e_var,
        'variational_error_eV': e_var - HELIUM_EXPERIMENTAL_EV,
        'variational_relative_error': (
            (e_var - HELIUM_EXPERIMENTAL_EV) / HELIUM_EXPERIMENTAL_EV
        ),
    }


# =========================================================================
# Reporting
# =========================================================================

def print_hydrogen(table: dict) -> None:
    print("=" * 78)
    print("HYDROGEN  (Z = 1)")
    print(f"  grid: n_grid = {table['n_grid']}, "
          f"r_max = {table['r_max_bohr']} Bohr")
    print(f"  reference: E_n = -{RYDBERG_EV:.6f} eV / n^2 (analytic Bohr)")
    print("-" * 78)
    print(f"  {'l':>2} {'n':>3}  "
          f"{'E_num [eV]':>14} {'E_exact [eV]':>14} "
          f"{'|err| [eV]':>12} {'rel_err':>10}")
    for row in table['rows']:
        print(
            f"  {row['l']:>2} {row['n']:>3}  "
            f"{row['E_numerical_eV']:>14.6f} "
            f"{row['E_analytic_eV']:>14.6f} "
            f"{abs(row['abs_error_eV']):>12.2e} "
            f"{row['rel_error']:>10.2e}"
        )
    max_rel = max(abs(r['rel_error']) for r in table['rows'])
    print("-" * 78)
    print(f"  worst relative error vs analytic: {max_rel:.2e}")


def print_helium(table: dict) -> None:
    print("=" * 78)
    print("HELIUM  (Z = 2)  [no closed-form: three-body]")
    print(f"  reference (NIST experimental): "
          f"E_exp = {table['experimental_eV']:.4f} eV")
    print("-" * 78)
    print(f"  independent-electron baseline   "
          f"= {table['independent_electron_eV']:>10.4f} eV  "
          f"(err {table['independent_electron_error_eV']:+.4f} eV)")
    print(f"  one-parameter variational       "
          f"= {table['variational_eV']:>10.4f} eV  "
          f"(err {table['variational_error_eV']:+.4f} eV, "
          f"rel {table['variational_relative_error']:+.2%})")
    print(f"  optimal Z_eff                   "
          f"= {table['variational_Z_eff']:.4f}  (= 27/16)")


def main() -> int:
    h_table = hydrogen_table(n_grid=8000, r_max=200.0)
    he_table = helium_table()
    print_hydrogen(h_table)
    print()
    print_helium(he_table)
    print()
    print("=" * 78)
    print("STATUS: bounded exploratory scaffold lane.")
    print("This script uses STANDARD quantum mechanics with TEXTBOOK inputs.")
    print("It does NOT use any Cl(3)-on-Z^3 framework input.")
    print("See docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md for scope and gap map.")
    print("=" * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
