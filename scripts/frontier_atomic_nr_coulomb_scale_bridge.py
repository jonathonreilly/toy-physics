#!/usr/bin/env python3
"""Lane 2 atomic nonrelativistic Coulomb scale bridge.

This runner tests the exact scaling bridge between the repo's dimensionless
lattice Coulomb companion

    H_g = -Delta_x - g / |x|

and the physical nonrelativistic Coulomb Hamiltonian in natural units,

    H_phys = -(1 / 2 mu) Delta_r - Z alpha / r.

It is not a retained Rydberg calculation.  The point is to separate the
conditional Schrodinger/Coulomb scale map from the still-open physical inputs:
mu (electron/reduced mass), alpha(0), and the physical unit map.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]

# Comparator constants already used by the repo's scaffold/firewall surfaces.
# They are printed only as a comparator check, not used in the theorem tests.
ALPHA0_INV_COMPARATOR = 137.035999084
M_E_EV_COMPARATOR = 510_998.95000
HARTREE_EV_SCAFFOLD = 27.211386245988


@dataclass
class CheckLog:
    passed: int = 0
    failed: int = 0

    def check(self, condition: bool, message: str, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"  [PASS] {message}")
        else:
            self.failed += 1
            print(f"  [FAIL] {message}")
            if detail:
                print(f"         {detail}")


def dimless_coulomb_energy(g: float, n: int) -> float:
    """Continuum scaled spectrum of -Delta_x - g/r: lambda_n = -g^2/(4 n^2)."""
    return -(g * g) / (4.0 * n * n)


def bohr_radius_scale(mu_ev: float, alpha: float, z: float, g: float) -> float:
    """Physical lattice spacing a, in eV^-1, required by g = 2 mu a Z alpha."""
    return g / (2.0 * mu_ev * z * alpha)


def physical_energy_from_dimless(lambda_dimless: float, mu_ev: float, a_evinv: float) -> float:
    """Convert dimensionless lambda to eV via E = lambda / (2 mu a^2)."""
    return lambda_dimless / (2.0 * mu_ev * a_evinv * a_evinv)


def bohr_energy(mu_ev: float, alpha: float, z: float, n: int) -> float:
    """Physical Coulomb spectrum E_n = -mu (Z alpha)^2 / (2 n^2), in eV."""
    return -mu_ev * (z * alpha) ** 2 / (2.0 * n * n)


def almost_equal(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def assert_repo_surfaces(log: CheckLog) -> None:
    print("Part 1: repo surfaces used for the bridge")
    paths = [
        "docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md",
        "docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md",
        "docs/work_history/atomic/HYDROGEN_HELIUM_ATOMIC_COMPANION_NOTE_2026-04-18.md",
        "scripts/frontier_atomic_hydrogen_lattice_companion.py",
    ]
    for rel in paths:
        log.check((REPO_ROOT / rel).exists(), f"required surface exists: {rel}")

    companion = (REPO_ROOT / "scripts/frontier_atomic_hydrogen_lattice_companion.py").read_text(
        encoding="utf-8"
    )
    log.check("H_g" in companion and "V_g(r)" in companion, "lattice companion names H_g")
    log.check("Absolute energies in eV still require the electron-mass lane" in companion,
              "lattice companion keeps absolute eV blocked")
    log.check("Level ratios" in companion and "1/n" in companion,
              "lattice companion records Rydberg ratio target")
    print()


def test_dimensionless_scaling(log: CheckLog) -> None:
    print("Part 2: dimensionless Coulomb scaling")
    for g in (0.25, 1.0, 2.5):
        e1 = dimless_coulomb_energy(g, 1)
        for n in range(1, 7):
            en = dimless_coulomb_energy(g, n)
            expected_ratio = 1.0 / (n * n)
            got_ratio = en / e1
            log.check(
                almost_equal(got_ratio, expected_ratio),
                f"g={g:g} gives E_{n}/E_1 = 1/{n*n}",
                f"got {got_ratio}, expected {expected_ratio}",
            )
    print()


def test_physical_scale_identity(log: CheckLog) -> None:
    print("Part 3: exact physical-unit scale identity")
    samples = [
        # Synthetic values keep the theorem independent of observed hydrogen.
        (3.0, 0.2, 1.0, 0.4),
        (17.0, 0.03, 2.0, 1.3),
        (511_000.0, 1.0 / 137.0, 1.0, 2.0),
    ]
    for mu_ev, alpha, z, g in samples:
        a = bohr_radius_scale(mu_ev, alpha, z, g)
        for n in range(1, 5):
            lam = dimless_coulomb_energy(g, n)
            mapped = physical_energy_from_dimless(lam, mu_ev, a)
            exact = bohr_energy(mu_ev, alpha, z, n)
            log.check(
                almost_equal(mapped, exact, rel=1e-12, abs_tol=1e-9),
                f"scale map cancels arbitrary g={g:g} for n={n}",
                f"mapped={mapped:.16e}, exact={exact:.16e}",
            )

    mu_ev, alpha, z, n = 511_000.0, 1.0 / 137.0, 1.0, 1
    energies = []
    for g in (0.2, 1.0, 5.0):
        a = bohr_radius_scale(mu_ev, alpha, z, g)
        energies.append(physical_energy_from_dimless(dimless_coulomb_energy(g, n), mu_ev, a))
    log.check(
        max(energies) - min(energies) < 1e-12,
        "physical energy is independent of arbitrary dimensionless g once a is mapped",
        f"energies={energies}",
    )
    print()


def test_missing_unit_map_no_go(log: CheckLog) -> None:
    print("Part 4: missing physical unit map remains an underdetermination")
    mu_ev = 1.0
    g = 1.0
    lam = dimless_coulomb_energy(g, 1)
    a_values = [0.5, 1.0, 2.0]
    energies = [physical_energy_from_dimless(lam, mu_ev, a) for a in a_values]
    print("  Same dimensionless lambda_1 = -g^2/4 with mu=1 and different a:")
    for a, energy in zip(a_values, energies):
        print(f"    a={a:4.1f} eV^-1 -> E={energy: .6f} eV")
    log.check(
        almost_equal(energies[0] / energies[1], 4.0),
        "energy scales as 1/a^2 when the physical lattice spacing is free",
    )
    log.check(
        almost_equal(energies[1] / energies[2], 4.0),
        "changing a without the bridge changes the absolute eV scale",
    )
    log.check(
        len({round(e, 12) for e in energies}) == len(energies),
        "same dimensionless lattice spectrum does not determine one absolute energy",
    )
    print()


def comparator_hydrogen_check(log: CheckLog) -> None:
    print("Part 5: hydrogen comparator, not a proof input")
    alpha = 1.0 / ALPHA0_INV_COMPARATOR
    e1 = bohr_energy(M_E_EV_COMPARATOR, alpha, 1.0, 1)
    rydberg_scaffold = HARTREE_EV_SCAFFOLD / 2.0
    print(f"  comparator 1/alpha(0) = {ALPHA0_INV_COMPARATOR}")
    print(f"  comparator m_e c^2    = {M_E_EV_COMPARATOR:.5f} eV")
    print(f"  -m_e alpha(0)^2/2     = {e1:.9f} eV")
    print(f"  scaffold Hartree/2    = {-rydberg_scaffold:.9f} eV")
    log.check(
        abs(e1 + rydberg_scaffold) < 2.0e-5,
        "comparator constants reproduce the scaffold Rydberg scale",
        f"delta={e1 + rydberg_scaffold:.6e} eV",
    )
    print()


def main() -> int:
    print("=" * 78)
    print("LANE 2 ATOMIC NR COULOMB SCALE BRIDGE")
    print("=" * 78)
    print("Question:")
    print("  Does the existing dimensionless lattice Coulomb companion supply a")
    print("  physical-unit nonrelativistic Coulomb bridge by itself?")
    print("Answer:")
    print("  No. It supplies an exact conditional scale bridge. Absolute eV output")
    print("  still needs mu/m_e, alpha(0), and the physical unit map.")
    print()

    log = CheckLog()
    assert_repo_surfaces(log)
    test_dimensionless_scaling(log)
    test_physical_scale_identity(log)
    test_missing_unit_map_no_go(log)
    comparator_hydrogen_check(log)

    print("=" * 78)
    print(f"SUMMARY: PASS={log.passed} FAIL={log.failed}")
    print("STATUS: exact conditional support plus underdetermination boundary.")
    print("NOT CLAIMED: retained alpha(0), retained m_e, retained Rydberg closure,")
    print("or framework-derived physical lattice spacing.")
    print("=" * 78)
    return 0 if log.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
