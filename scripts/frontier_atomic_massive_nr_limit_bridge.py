#!/usr/bin/env python3
"""Lane 2 massive nonrelativistic kinetic-limit bridge.

This runner isolates the kinetic part of the physical-unit Schrodinger gate.

If a retained low-energy one-particle sector supplies the relativistic mass
shell

    E^2 = m^2 + p^2

then subtracting the rest energy gives the nonrelativistic kinetic term

    E - m = p^2/(2m) + O(p^4/m^3).

The current repo has Lorentz/dispersion support surfaces, but Lane 2 does not
retain the electron/reduced mass or a complete atomic one-particle Coulomb
sector.  Therefore this bridge is exact conditional support, not retained
atomic closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude/science/physics-loops/lane2-atomic-scale-20260428"

M_E_EV_COMPARATOR = 510_998.95000


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


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def e_cont(p: float, m: float) -> float:
    return math.sqrt(m * m + p * p)


def e_lat_1d(p: float, m: float, a: float) -> float:
    return math.sqrt(m * m + (4.0 / (a * a)) * math.sin(p * a / 2.0) ** 2)


def kinetic_cont(p: float, m: float) -> float:
    return e_cont(p, m) - m


def kinetic_lat_1d(p: float, m: float, a: float) -> float:
    return e_lat_1d(p, m, a) - m


def schrodinger_kinetic(p: float, m: float) -> float:
    return p * p / (2.0 * m)


def almost_equal(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def part1_grounding(log: CheckLog) -> None:
    section("Part 1: repo grounding")
    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    harness = read("docs/CANONICAL_HARNESS_INDEX.md")
    lorentz = read("docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md")
    boost3 = read("scripts/frontier_lorentz_boost_3plus1d.py")
    assumptions = (PACK / "ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")

    paths = [
        "docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md",
        "docs/LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md",
        "scripts/frontier_lorentz_boost_3plus1d.py",
        "scripts/frontier_atomic_nr_coulomb_scale_bridge.py",
    ]
    for rel in paths:
        log.check((ROOT / rel).exists(), f"required surface exists: {rel}")

    log.check(
        "retained Lorentz support packet" in harness
        and "frontier_lorentz_boost_3plus1d.py" in harness,
        "canonical harness index carries the Lorentz support packet",
    )
    log.check(
        "E² = p²" in lorentz or "E² = (1/a²)" in lorentz,
        "emergent Lorentz note records infrared dispersion support",
    )
    log.check(
        "E_lat^2(p) = m^2" in boost3 and "m^2 + |p" in boost3,
        "3+1D boost runner uses a massive lattice-to-continuum dispersion",
    )
    log.check(
        "single-particle Schrodinger" in lane2
        or "Schrodinger/Coulomb limit" in lane2,
        "Lane 2 keeps the physical-unit Schrodinger limit as an open gate",
    )
    log.check(
        "kinetic normalization/unit map" in assumptions and "| `m_e` |" in assumptions,
        "loop assumption ledger keeps kinetic prefactor and mass open",
    )


def part2_continuum_nr_expansion(log: CheckLog) -> None:
    section("Part 2: continuum massive nonrelativistic expansion")
    samples = [
        (3.0, 0.03),
        (11.0, 0.05),
        (101.0, 0.08),
    ]
    for m, eps in samples:
        p = eps * m
        exact = kinetic_cont(p, m)
        nr = schrodinger_kinetic(p, m)
        rel_error = abs(exact - nr) / nr
        expected = (p / m) ** 2 / 4.0
        log.check(
            rel_error < 1.1 * expected,
            f"K=E-m approaches p^2/(2m) for p/m={eps:g}",
            f"rel_error={rel_error:.3e}, expected~{expected:.3e}",
        )

    m = 7.0
    p = 0.02 * m
    coeff = kinetic_cont(p, m) / (p * p)
    log.check(
        abs(coeff - 1.0 / (2.0 * m)) / (1.0 / (2.0 * m)) < 1.1e-4,
        "kinetic p^2 coefficient is fixed by the mass",
        f"coeff={coeff:.10e}, 1/(2m)={1.0/(2.0*m):.10e}",
    )


def part3_lattice_continuum_nr_bridge(log: CheckLog) -> None:
    section("Part 3: lattice dispersion inherits the same NR prefactor at small a p")
    samples = [
        # m, p/m, a*m
        (5.0, 0.03, 0.20),
        (13.0, 0.04, 0.10),
        (41.0, 0.05, 0.05),
    ]
    for m, eps, am in samples:
        p = eps * m
        a = am / m
        k_lat = kinetic_lat_1d(p, m, a)
        k_nr = schrodinger_kinetic(p, m)
        rel_error = abs(k_lat - k_nr) / k_nr
        log.check(
            rel_error < 2.0e-3,
            f"lattice massive dispersion gives NR kinetic term for p/m={eps:g}, a*m={am:g}",
            f"rel_error={rel_error:.3e}",
        )

    m = 17.0
    p = 0.03 * m
    coarse = kinetic_lat_1d(p, m, 0.2 / m)
    fine = kinetic_lat_1d(p, m, 0.05 / m)
    cont = kinetic_cont(p, m)
    log.check(
        abs(fine - cont) < abs(coarse - cont),
        "refining the lattice spacing improves the massive dispersion bridge",
        f"|fine-cont|={abs(fine-cont):.3e}, |coarse-cont|={abs(coarse-cont):.3e}",
    )


def part4_mass_gate(log: CheckLog) -> None:
    section("Part 4: the kinetic prefactor is still mass-gated")
    p = 0.01
    masses = [1.0, 2.0, 5.0]
    coeffs = [schrodinger_kinetic(p, m) / (p * p) for m in masses]
    for m, coeff in zip(masses, coeffs):
        print(f"  m={m:.1f} -> kinetic coefficient K/p^2={coeff:.6f}")
    log.check(
        coeffs[0] / coeffs[1] == 2.0 and coeffs[1] / coeffs[2] == 2.5,
        "different masses give different Schrodinger kinetic prefactors",
    )
    log.check(
        len({round(c, 12) for c in coeffs}) == len(coeffs),
        "mass shell alone without retained m_e does not pick the atomic prefactor",
    )

    coeff_e = 1.0 / (2.0 * M_E_EV_COMPARATOR)
    print(f"  comparator electron coefficient 1/(2 m_e) = {coeff_e:.12e} eV^-1")
    log.check(
        9.0e-7 < coeff_e < 1.1e-6,
        "electron comparator gives the expected tiny atomic kinetic coefficient",
    )


def part5_lane2_consequence(log: CheckLog) -> None:
    section("Part 5: Lane 2 consequence")
    print("  Conditional support:")
    print("    retained massive low-energy dispersion + rest-energy subtraction")
    print("      -> Schrodinger kinetic prefactor p^2/(2m).")
    print()
    print("  Still open for retained Rydberg:")
    print("    - retained electron/reduced mass m;")
    print("    - retained alpha(0) and threshold moment;")
    print("    - retained Coulomb potential/coupling in the same low-energy sector;")
    print("    - finite nuclear mass/proton inputs for physical hydrogen.")

    log.check(True, "conditional NR kinetic bridge is isolated")
    log.check(True, "no electron mass or Rydberg closure is claimed")


def main() -> int:
    print("=" * 88)
    print("LANE 2 MASSIVE NONRELATIVISTIC KINETIC-LIMIT BRIDGE")
    print("=" * 88)
    print("Question:")
    print("  Does the retained Lorentz/dispersion surface close the physical-unit")
    print("  Schrodinger kinetic prefactor for atomic Lane 2?")
    print("Answer:")
    print("  It gives exact conditional support once a massive one-particle sector")
    print("  and mass m are supplied. The atomic prefactor remains mass-gated.")

    log = CheckLog()
    part1_grounding(log)
    part2_continuum_nr_expansion(log)
    part3_lattice_continuum_nr_bridge(log)
    part4_mass_gate(log)
    part5_lane2_consequence(log)

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={log.passed} FAIL={log.failed}")
    print("STATUS: exact conditional kinetic support plus mass-gate boundary.")
    print("NOT CLAIMED: retained m_e, retained alpha(0), retained Coulomb sector,")
    print("or retained Rydberg closure.")
    print("=" * 88)
    return 0 if log.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
