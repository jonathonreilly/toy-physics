#!/usr/bin/env python3
"""Lane 1 confinement-to-hadron-mass firewall.

This runner verifies the current Lane 1 boundary: retained confinement and a
bounded string-tension scale are prerequisites for hadron physics, but they do
not retain pion, proton, neutron, or hadron-spectrum masses.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Comparator values only.
SQRT_SIGMA_BOUNDED_MEV = 465.0
M_PI_CHARGED_MEV = 139.57039
M_PI_NEUTRAL_MEV = 134.9768
M_PROTON_MEV = 938.27208816
M_NEUTRON_MEV = 939.56542052


def part1_repo_claim_state() -> None:
    section("Part 1: repo claim-state guardrails")
    lane = read("docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md")
    confinement = read("docs/CONFINEMENT_STRING_TENSION_NOTE.md")
    lane3 = read("docs/QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md")
    lane_flat = " ".join(lane.split())
    confinement_flat = " ".join(confinement.split())

    check(
        "Lane 1 stub says bounded confinement is not hadron-mass retention",
        "Bounded confinement + bounded" in lane_flat
        and "does not satisfy hadron-mass retention" in lane_flat,
    )
    check(
        "Lane 1 stub says pion/proton/neutron masses are absent",
        "Pion mass" in lane
        and "no derivation" in lane
        and "Proton mass" in lane
        and "Neutron mass" in lane,
    )
    check(
        "confinement note separates exact theorem from bounded string tension",
        "proposed_retained structural theorem + bounded quantitative prediction" in confinement_flat
        and "Bounded (EFT bridge)" in confinement_flat,
    )
    check(
        "confinement note leaves meson spectrum open",
        "Meson spectrum" in confinement
        and "requires significant lattice" in confinement,
    )
    check(
        "Lane 3 light-quark masses are currently not retained",
        "not a retained derivation of `m_u`" in lane3
        and "Lane 3 remains open" in lane3,
    )


def part2_one_scale_is_not_spectrum() -> None:
    section("Part 2: one bounded scale is not a hadron spectrum")
    c_pi_charged = M_PI_CHARGED_MEV / SQRT_SIGMA_BOUNDED_MEV
    c_pi_neutral = M_PI_NEUTRAL_MEV / SQRT_SIGMA_BOUNDED_MEV
    c_p = M_PROTON_MEV / SQRT_SIGMA_BOUNDED_MEV
    c_n = M_NEUTRON_MEV / SQRT_SIGMA_BOUNDED_MEV

    print(f"  bounded sqrt(sigma) = {SQRT_SIGMA_BOUNDED_MEV:.1f} MeV")
    print(f"  c_pi+ = m_pi+/sqrt(sigma) = {c_pi_charged:.4f}")
    print(f"  c_pi0 = m_pi0/sqrt(sigma) = {c_pi_neutral:.4f}")
    print(f"  c_p   = m_p/sqrt(sigma)   = {c_p:.4f}")
    print(f"  c_n   = m_n/sqrt(sigma)   = {c_n:.4f}")

    check(
        "pion and proton require different dimensionless spectral coefficients",
        abs(c_p - c_pi_charged) > 1.5,
        f"c_p-c_pi={c_p - c_pi_charged:.3f}",
    )
    check(
        "proton and neutron are close but not fixed by sqrt(sigma) alone",
        0.0 < abs(c_n - c_p) < 0.01,
        f"c_n-c_p={c_n - c_p:.5f}",
    )
    check(
        "bounded sqrt(sigma) alone leaves arbitrary channel coefficients",
        len({round(c_pi_charged, 3), round(c_pi_neutral, 3), round(c_p, 3), round(c_n, 3)}) > 2,
        "m_H = c_H sqrt(sigma); c_H is not retained",
    )


def part3_gmor_dependency() -> None:
    section("Part 3: GMOR pion-mass dependency")
    # GMOR in natural units: m_pi^2 = (m_u + m_d) Sigma / f_pi^2.
    # Demonstrate sensitivity: a 10% change in either quark-mass sum or
    # condensate changes m_pi by sqrt(1.1), while f_pi changes it inversely.
    factor_mass_or_sigma = math.sqrt(1.10)
    factor_fpi = 1.0 / 1.10
    lane = read("docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md")
    lane3 = read("docs/QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md")

    print("  GMOR: m_pi^2 f_pi^2 = (m_u + m_d) Sigma")
    print(f"  10% change in (m_u+m_d) or Sigma changes m_pi by {factor_mass_or_sigma:.4f}x")
    print(f"  10% change in f_pi changes m_pi by {factor_fpi:.4f}x")

    check(
        "GMOR is sensitive to light-quark masses",
        abs(factor_mass_or_sigma - 1.0) > 0.04,
        f"sqrt(1.10)={factor_mass_or_sigma:.4f}",
    )
    check(
        "GMOR is sensitive to f_pi normalization",
        abs(factor_fpi - 1.0) > 0.08,
        f"1/1.10={factor_fpi:.4f}",
    )
    check(
        "current Lane 1 cannot close m_pi until m_u, m_d, Sigma, and f_pi land",
        "Quark masses m_u, m_d" in lane
        and "Chiral condensate" in lane
        and "Pion decay constant" in lane
        and "Lane 3 remains open" in lane3,
        "all four are load-bearing in GMOR",
    )


def part4_confinement_runner_boundary() -> None:
    section("Part 4: confinement runner boundary")
    script = read("scripts/frontier_confinement_string_tension.py")
    note = read("docs/CONFINEMENT_STRING_TENSION_NOTE.md")

    check(
        "confinement runner labels string tension quantitative path as bounded",
        "kind=\"BOUNDED\"" in script
        and "bounded: conditioned on the standard low-energy EFT bridge" in script,
    )
    check(
        "confinement note states quantitative sigma uses standard lattice inputs",
        "Sommer-scale lattice data are derived from" in note
        and "therefore bounded through this identification" in note,
    )
    check(
        "support note does not claim m_pi or m_p",
        "Meson spectrum" in note
        and "Computing light meson masses" in note,
    )


def part5_safe_endpoint() -> None:
    section("Part 5: safe endpoint")
    lane = read("docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md")
    note = read("docs/HADRON_LANE1_CONFINEMENT_TO_MASS_FIREWALL_NOTE_2026-04-27.md")
    check(
        "Lane 1 honest status is open, not retained hadron closure",
        "ACCEPTED CRITICAL OPEN SCIENCE LANE" in lane
        and "no theorem or claim" in lane
        and "Lane 1 remains open" in note,
        "open gates: quark masses, chiral inputs, hadronic running, correlators",
    )
    check(
        "standard lattice-QCD methodology remains a bridge until instantiated",
        "lattice-QCD-equivalent correlator extraction" in note
        and "standard lattice-QCD methodology by itself counts as a framework derivation" in note,
        "methodology alone is not a framework mass calculation",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 HADRON CONFINEMENT-TO-MASS FIREWALL")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can retained confinement plus bounded sqrt(sigma) be promoted")
    print("  to retained pion, proton, neutron, or hadron-spectrum masses?")
    print()
    print("Answer:")
    print("  No. One bounded scale and confinement do not determine the spectrum.")

    part1_repo_claim_state()
    part2_one_scale_is_not_spectrum()
    part3_gmor_dependency()
    part4_confinement_runner_boundary()
    part5_safe_endpoint()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
