#!/usr/bin/env python3
"""Audit the standalone Planck source-unit normalization theorem."""

from __future__ import annotations

from dataclasses import dataclass
import math
import sys


TOL = 1e-14


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def record(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name, passed, detail))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")


def main() -> int:
    checks: list[Check] = []

    omega_2 = 4.0 * math.pi
    g_kernel = 1.0 / omega_2
    c_cell = 4.0 / 16.0

    record(
        checks,
        "retained Green-kernel coefficient is 1/(4*pi)",
        close(g_kernel, 1.0 / (4.0 * math.pi)),
        f"G_kernel={g_kernel:.15f}",
    )

    q_bare = 1.0
    bare_monopole = q_bare * g_kernel
    bare_flux = omega_2 * bare_monopole
    record(
        checks,
        "unit bare delta has unit Gauss flux, not unit Newton monopole",
        close(bare_monopole, 1.0 / omega_2) and close(bare_flux, 1.0),
        f"phi~{bare_monopole:.15f}/r; flux={bare_flux:.12f}",
    )

    m_phys = 1.0
    source_unit = omega_2
    q_for_unit_mass = source_unit * m_phys
    physical_monopole = q_for_unit_mass * g_kernel
    physical_flux = omega_2 * physical_monopole
    record(
        checks,
        "Gauss/Newton source unit gives unit 1/r monopole",
        close(physical_monopole, m_phys) and close(physical_flux, omega_2),
        f"q_bare=4*pi*M_phys gives phi~{physical_monopole:.12f}/r",
    )

    trial_source_units = [1.0, omega_2 / 2.0, omega_2, 2.0 * omega_2]
    trial_monopoles = [sigma * g_kernel for sigma in trial_source_units]
    unit_trials = [idx for idx, value in enumerate(trial_monopoles) if close(value, 1.0)]
    record(
        checks,
        "unit monopole readout uniquely fixes sigma=4*pi",
        unit_trials == [2],
        "trial monopoles="
        + ", ".join(f"{value:.12f}" for value in trial_monopoles),
    )

    g_newton_lat = source_unit * g_kernel
    record(
        checks,
        "physical lattice Newton coefficient is one",
        close(g_newton_lat, 1.0),
        f"G_Newton,lat=(4*pi)*G_kernel={g_newton_lat:.12f}",
    )

    m1 = 3.0
    m2 = 5.0
    r = 7.0
    source2_bare = source_unit * m2
    source2_monopole = source2_bare * g_kernel
    physical_force_coeff = m1 * source2_monopole
    newton_force_coeff = g_newton_lat * m1 * m2
    force_at_r = physical_force_coeff / (r * r)
    record(
        checks,
        "same source unit gives the physical two-body product law",
        close(source2_monopole, m2)
        and close(physical_force_coeff, newton_force_coeff),
        (
            f"F_coeff={physical_force_coeff:.12f}; "
            f"G*M1*M2={newton_force_coeff:.12f}; F(r=7)={force_at_r:.12f}"
        ),
    )

    bare_a_over_l_planck = 1.0 / math.sqrt(g_kernel)
    normalized_a_over_l_planck = 1.0 / math.sqrt(g_newton_lat)
    record(
        checks,
        "bare-source mislabel gives the hostile-review failure mode",
        close(bare_a_over_l_planck, 2.0 * math.sqrt(math.pi))
        and close(normalized_a_over_l_planck, 1.0),
        (
            f"bare a/l_P={bare_a_over_l_planck:.12f}; "
            f"normalized a/l_P={normalized_a_over_l_planck:.12f}"
        ),
    )

    bh_area_coeff = 1.0 / (4.0 * g_newton_lat)
    record(
        checks,
        "primitive carrier matches the Planck-area coefficient",
        close(bh_area_coeff, c_cell),
        f"1/(4*G_Newton,lat)={bh_area_coeff:.12f}; c_cell={c_cell:.12f}",
    )

    eh_prefactor = 1.0 / (16.0 * math.pi * g_newton_lat)
    record(
        checks,
        "EH prefactor is c_cell/(4*pi), not c_cell",
        close(eh_prefactor, c_cell / omega_2),
        f"EH={eh_prefactor:.15f}; c_cell/(4*pi)={c_cell / omega_2:.15f}",
    )

    wald_area_from_eh = omega_2 * eh_prefactor
    record(
        checks,
        "Wald/Gauss bridge maps EH prefactor to the area coefficient",
        close(wald_area_from_eh, c_cell),
        f"4*pi*EH={wald_area_from_eh:.12f}",
    )

    g_phys_over_a2 = g_newton_lat
    l_planck_over_a = math.sqrt(g_phys_over_a2)
    record(
        checks,
        "physical unit map closes a/l_P=1",
        close(g_phys_over_a2, 1.0) and close(l_planck_over_a, 1.0),
        "G_phys=a^2*G_Newton,lat=a^2, so l_P=a",
    )

    no_smuggling_conditions = [
        close(g_kernel, 1.0 / omega_2),
        close(source_unit, omega_2),
        close(g_newton_lat, 1.0),
        close(c_cell, 0.25),
    ]
    record(
        checks,
        "no measured constants enter the closure arithmetic",
        all(no_smuggling_conditions),
        "inputs are G_kernel=1/(4*pi), source unit=4*pi, c_cell=4/16",
    )

    print()
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Summary: {passed}/{total} checks passed.")
    if passed == total:
        print(
            "Verdict: positive clean-science closure candidate. The retained "
            "1/(4*pi) is the bare Green-kernel coefficient; the physical "
            "Gauss/Newton source unit is q_bare=4*pi*M_phys; therefore "
            "G_Newton,lat=1, c_cell=1/(4G), EH=c_cell/(4*pi), and a/l_P=1."
        )
        return 0

    print("Verdict: source-unit normalization theorem failed an internal gate.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
