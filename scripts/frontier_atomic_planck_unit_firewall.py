#!/usr/bin/env python3
"""Lane 2 atomic Planck-unit map firewall.

Question:
  Does the current Planck/source-unit package close the Lane 2
  physical-unit nonrelativistic Coulomb map?

Answer:
  No.  The Planck/source-unit package can supply a gravitational lattice
  length anchor on its conditional carrier surface.  The atomic Coulomb
  Hamiltonian still needs an effective dimensionless coupling

      g_atomic = 2 * mu * a_lat * Z * alpha(0)

  and the kinetic mass/reduced-mass and low-energy Coulomb coupling entering
  that expression are still open Lane 2 imports.  Setting the finite-box
  companion's convenient g=1 equal to the Planck-lattice coupling is a
  different, false map.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude/science/physics-loops/lane2-atomic-scale-20260428"


# Comparator/package-pin values already present in repo surfaces.  These are
# not proof inputs for the synthetic tests below.
M_PLANCK_GEV_COMPARATOR = 1.2209e19
M_E_EV_COMPARATOR = 510_998.95000
ALPHA0_INV_COMPARATOR = 137.035999084
RYDBERG_EV_COMPARATOR = 13.605693122994


@dataclass
class CheckLog:
    passed: int = 0
    failed: int = 0

    def check(self, condition: bool, name: str, detail: str = "") -> None:
        if condition:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] {name}{suffix}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def dimless_lambda(g: float, n: int) -> float:
    """Continuum scaled spectrum for H_g = -Delta_x - g/r."""
    return -(g * g) / (4.0 * n * n)


def physical_energy(lambda_n: float, mu: float, a_lat: float) -> float:
    """Energy from dimensionless lambda when r_phys = a_lat * x."""
    return lambda_n / (2.0 * mu * a_lat * a_lat)


def bohr_energy(mu: float, alpha: float, z: float, n: int) -> float:
    """Nonrelativistic Coulomb spectrum in natural units."""
    return -mu * (z * alpha) ** 2 / (2.0 * n * n)


def matched_g(mu: float, alpha: float, z: float, a_lat: float) -> float:
    """Dimensionless lattice coupling required by the physical Coulomb map."""
    return 2.0 * mu * a_lat * z * alpha


def almost_equal(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def part1_repo_grounding(log: CheckLog) -> None:
    section("Part 1: repo grounding")
    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    planck_status = read("docs/PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md")
    planck_source = read("docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md")
    atomic_companion = read("docs/work_history/atomic/HYDROGEN_HELIUM_ATOMIC_COMPANION_NOTE_2026-04-18.md")
    atomic_lattice_script = read("scripts/frontier_atomic_hydrogen_lattice_companion.py")
    assumptions = (PACK / "ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")
    prior_scale = (
        PACK
        / "notes"
        / "ATOMIC_NR_COULOMB_SCALE_BRIDGE_STRETCH_NOTE_2026-05-01.md"
    ).read_text(encoding="utf-8")

    paths = [
        "docs/PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md",
        "docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md",
        "scripts/frontier_planck_source_unit_normalization_support_theorem.py",
        "scripts/frontier_atomic_nr_coulomb_scale_bridge.py",
        "scripts/frontier_atomic_rydberg_gate_factorization_fanout.py",
    ]
    for rel in paths:
        log.check((ROOT / rel).exists(), f"required surface exists: {rel}")

    log.check(
        "a^(-1) = M_Pl" in planck_status
        and (
            "fallback package pin remains active" in planck_status
            or "explicit package pin" in planck_status
        )
        and "conditional" in planck_status,
        "Planck status keeps absolute a^(-1)=M_Pl as package pin / conditional program",
    )
    log.check(
        "not a standalone minimal-stack closure" in planck_source
        and "G_Newton,lat = 1" in planck_source,
        "source-unit theorem is conditional support, not a generic atomic unit map",
    )
    log.check(
        "m_e" in lane2
        and "alpha(0)" in lane2
        and "Schrodinger/Coulomb limit" in lane2,
        "Lane 2 still names mass, alpha(0), and physical-unit Coulomb gates",
    )
    log.check(
        "coupling-relative units" in atomic_companion
        and "treats g as a free coupling" in atomic_lattice_script
        and "Absolute energies in eV still require the electron-mass lane" in atomic_lattice_script,
        "atomic lattice companion keeps g free and absolute eV scale blocked",
    )
    log.check(
        "Physical length map" in assumptions and "framework-native unit map" in assumptions,
        "loop assumption ledger keeps the atomic unit map open",
    )
    log.check(
        "g = 2 mu a Z alpha" in prior_scale
        and "kinetic\n   prefactor" in prior_scale,
        "prior scale bridge already isolated the admitted map",
    )


def part2_synthetic_planck_length_split(log: CheckLog) -> None:
    section("Part 2: synthetic Planck-length split")

    samples = [
        # mu, alpha, Z, inverse lattice length M = 1/a_lat, n
        (3.0, 0.20, 1.0, 17.0, 1),
        (11.0, 0.07, 2.0, 101.0, 2),
        (29.0, 0.011, 3.0, 509.0, 3),
    ]
    for mu, alpha, z, m_lat, n in samples:
        a_lat = 1.0 / m_lat
        g = matched_g(mu, alpha, z, a_lat)
        mapped = physical_energy(dimless_lambda(g, n), mu, a_lat)
        exact = bohr_energy(mu, alpha, z, n)
        log.check(
            almost_equal(mapped, exact, rel=1e-12, abs_tol=1e-12),
            f"matched g reproduces Coulomb energy for synthetic M={m_lat:g}, n={n}",
            f"g={g:.6e}",
        )

    mu, alpha, z, m_lat = 7.0, 0.13, 1.0, 97.0
    a_lat = 1.0 / m_lat
    base_g = matched_g(mu, alpha, z, a_lat)
    for factor in (0.5, 2.0, 3.0):
        g_mu = matched_g(factor * mu, alpha, z, a_lat)
        g_alpha = matched_g(mu, factor * alpha, z, a_lat)
        log.check(
            almost_equal(g_mu / base_g, factor),
            f"dimensionless atomic g is linear in mu at factor {factor:g}",
        )
        log.check(
            almost_equal(g_alpha / base_g, factor),
            f"dimensionless atomic g is linear in alpha at factor {factor:g}",
        )

    # With fixed a_lat and mu, g=1 selects an alpha value; it is not supplied
    # by the Planck/source-unit theorem.
    implied_alpha = 1.0 / (2.0 * mu * a_lat * z)
    direct_energy = physical_energy(dimless_lambda(1.0, 1), mu, a_lat)
    matched_energy = bohr_energy(mu, alpha, z, 1)
    log.check(
        implied_alpha > 1.0,
        "setting g=1 at the synthetic short lattice scale imposes a new alpha selector",
        f"alpha_implied={implied_alpha:.6f}",
    )
    log.check(
        abs(direct_energy / matched_energy) > 1.0e3,
        "direct g=1 at fixed lattice scale is not the matched atomic map",
        f"E_g1/E_matched={direct_energy / matched_energy:.3e}",
    )


def part3_planck_package_does_not_select_atomic_g(log: CheckLog) -> None:
    section("Part 3: Planck source-unit support does not select atomic g")

    c_cell = 4.0 / 16.0
    lambda_selected = 4.0 * c_cell
    g_newton_lat = 1.0 / lambda_selected
    log.check(
        almost_equal(c_cell, 0.25) and almost_equal(g_newton_lat, 1.0),
        "Planck source-unit algebra selects G_Newton,lat=1 on its carrier surface",
    )

    mu, alpha, z = 5.0, 0.1, 1.0
    m_lat_values = [10.0, 100.0, 1000.0]
    g_values = [matched_g(mu, alpha, z, 1.0 / m_lat) for m_lat in m_lat_values]
    print("  same synthetic mu and alpha with different absolute lattice anchors:")
    for m_lat, g in zip(m_lat_values, g_values):
        print(f"    M_lat={m_lat:8.1f} -> g_atomic={g:.6e}")
    log.check(
        g_values[0] > g_values[1] > g_values[2],
        "absolute lattice anchor changes g_atomic unless mu and alpha are supplied",
    )
    log.check(
        almost_equal(g_values[0] / g_values[1], 10.0)
        and almost_equal(g_values[1] / g_values[2], 10.0),
        "g_atomic scales as 1/M_lat, not as a pure Planck-source constant",
    )

    # A source-unit Newton coefficient and an electromagnetic Coulomb coupling
    # live in different sectors.  Equality would be an extra cross-sector law.
    alpha_from_newton_if_g1 = 1.0 / (2.0 * mu * (1.0 / 100.0) * z)
    log.check(
        not almost_equal(alpha_from_newton_if_g1, alpha, rel=1e-9),
        "G_Newton,lat=1 does not imply the electromagnetic g_atomic=1 map",
        f"alpha_from_g1={alpha_from_newton_if_g1:.6f}, supplied alpha={alpha:.6f}",
    )


def part4_comparator_falsifier(log: CheckLog) -> None:
    section("Part 4: comparator-only hydrogen/Planck scale check")
    m_planck_ev = M_PLANCK_GEV_COMPARATOR * 1.0e9
    alpha0 = 1.0 / ALPHA0_INV_COMPARATOR
    a_planck_evinv = 1.0 / m_planck_ev
    g_atomic = matched_g(M_E_EV_COMPARATOR, alpha0, 1.0, a_planck_evinv)
    r0_sites = 2.0 / g_atomic
    e_matched = physical_energy(dimless_lambda(g_atomic, 1), M_E_EV_COMPARATOR, a_planck_evinv)
    e_bohr = bohr_energy(M_E_EV_COMPARATOR, alpha0, 1.0, 1)
    e_g1 = physical_energy(dimless_lambda(1.0, 1), M_E_EV_COMPARATOR, a_planck_evinv)
    alpha_implied_g1 = 1.0 / (2.0 * M_E_EV_COMPARATOR * a_planck_evinv)

    print(f"  comparator M_Pl              = {M_PLANCK_GEV_COMPARATOR:.4e} GeV")
    print(f"  comparator m_e               = {M_E_EV_COMPARATOR:.5f} eV")
    print(f"  comparator 1/alpha(0)        = {ALPHA0_INV_COMPARATOR:.9f}")
    print(f"  matched Planck-lattice g     = {g_atomic:.6e}")
    print(f"  Bohr radius in lattice sites = {r0_sites:.6e}")
    print(f"  matched E_1                  = {e_matched:.9f} eV")
    print(f"  direct g=1 at Planck spacing = {e_g1:.6e} eV")
    print(f"  alpha implied by g=1         = {alpha_implied_g1:.6e}")

    log.check(
        almost_equal(e_matched, e_bohr, rel=1e-12, abs_tol=1e-9),
        "if comparator m_e and alpha(0) are supplied, tiny g reproduces Bohr energy",
    )
    log.check(
        abs(abs(e_bohr) - RYDBERG_EV_COMPARATOR) / RYDBERG_EV_COMPARATOR < 1e-10,
        "comparator constants reproduce the Rydberg scale",
    )
    log.check(
        g_atomic < 1.0e-20 and r0_sites > 1.0e20,
        "Planck lattice anchor implies an enormous atomic radius in lattice sites",
        f"g={g_atomic:.3e}, r0_sites={r0_sites:.3e}",
    )
    log.check(
        abs(e_g1) / RYDBERG_EV_COMPARATOR > 1.0e40,
        "direct g=1 at Planck spacing is catastrophically non-atomic",
        f"|E_g1|/Rydberg={abs(e_g1) / RYDBERG_EV_COMPARATOR:.3e}",
    )
    log.check(
        alpha_implied_g1 > 1.0e20,
        "g=1 at Planck spacing would require a non-atomic low-energy coupling",
        f"alpha_implied={alpha_implied_g1:.3e}",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 2 ATOMIC PLANCK-UNIT MAP FIREWALL")
    print("=" * 88)
    print("Question:")
    print("  Does the current Planck/source-unit package close the atomic")
    print("  physical-unit Coulomb/Schrodinger map?")
    print("Answer:")
    print("  No. It supplies at most a gravitational lattice length/source unit on")
    print("  its conditional carrier surface. Atomic closure still needs")
    print("  mu/reduced mass, alpha(0), and the effective low-energy coupling map.")

    log = CheckLog()
    part1_repo_grounding(log)
    part2_synthetic_planck_length_split(log)
    part3_planck_package_does_not_select_atomic_g(log)
    part4_comparator_falsifier(log)

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={log.passed} FAIL={log.failed}")
    print("STATUS: exact negative boundary / conditional-support firewall.")
    print("NOT CLAIMED: retained m_e, retained alpha(0), retained Rydberg closure,")
    print("or a framework-native atomic kinetic/unit-map theorem.")
    print("=" * 88)
    return 0 if log.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
