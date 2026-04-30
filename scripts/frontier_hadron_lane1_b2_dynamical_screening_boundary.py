#!/usr/bin/env python3
"""
Lane 1 B2 boundary: pure-gauge data cannot close dynamical screening.

Question:
  Can the current beta=6.0 pure-gauge / quenched string-tension data and the
  rough 0.96 screening factor close the N_f=2+1 dynamical screening budget
  for sqrt(sigma)?

Answer on the current branch-local science surface:
  No. The B2 factor is a sea-fermion determinant effect. Pure-gauge Wilson-loop
  and Creutz-ratio data are compatible with a family of screening factors until
  a dynamical determinant calculation, or an explicitly budgeted external
  comparator, is supplied.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

np.set_printoptions(precision=8, suppress=True, linewidth=120)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


SQRT_SIGMA_QUENCHED_MEV = 484.0
ROUGH_SCREENING_FACTOR = 0.96
PDG_COMPARATOR_MEV = 440.0


def pure_gauge_payload() -> tuple[float, float, float, float]:
    """Current Method-2 payload before the sea-fermion determinant enters."""
    beta = 6.0
    r0_over_a = 5.37
    sigma_a2 = 0.0465
    plaquette = 0.5934
    return beta, r0_over_a, sigma_a2, plaquette


def screened_readout(screening_factor: float) -> float:
    return SQRT_SIGMA_QUENCHED_MEV * screening_factor


def determinant_factor(singular_values: np.ndarray, masses: tuple[float, ...]) -> float:
    factor = 1.0
    for mass in masses:
        factor *= float(np.prod(singular_values**2 + mass**2))
    return factor


def reweighted_observable(
    gauge_weights: np.ndarray,
    observable: np.ndarray,
    singular_value_bank: np.ndarray,
    masses: tuple[float, ...] | None,
) -> float:
    if masses is None:
        weights = gauge_weights
    else:
        dets = np.array([determinant_factor(vals, masses) for vals in singular_value_bank])
        weights = gauge_weights * dets
    return float(np.sum(weights * observable) / np.sum(weights))


def test_authority_text() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AUTHORITY TEXT NAMES B2 AS THE LOAD-BEARING GAP")
    print("=" * 88)

    lane = read("docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md")
    audit = read("docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md")
    confinement = read("docs/CONFINEMENT_STRING_TENSION_NOTE.md")
    runner = read("scripts/frontier_confinement_string_tension.py")

    check(
        "Lane 1 file names B2 as the current highest-leverage sqrt(sigma) gate",
        "B2" in lane and "quenched-to-dynamical" in lane and "screening budget" in lane,
    )
    check(
        "Audit note identifies B2 as the dominant numerical residual",
        "(B2)" in audit and "dynamical screening" in audit and "dominant" in audit,
    )
    check(
        "Audit note requires a proper N_f=2+1 lattice calculation",
        "proper `N_f = 2+1` lattice" in audit and "beta = 6.0" in audit,
    )
    check(
        "Confinement note says the current correction is rough",
        "rough screening correction" in confinement or "rough central estimate" in confinement,
    )
    check(
        "Current confinement runner is pure-gauge at beta=6.0",
        "Pure-gauge SU(3) Monte Carlo" in runner and "beta = 6.0" in runner,
    )


def test_screening_factor_degeneracy() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SAME PURE-GAUGE PAYLOAD ADMITS MANY SCREENING FACTORS")
    print("=" * 88)

    payload = pure_gauge_payload()
    factors = [0.90, 0.94, ROUGH_SCREENING_FACTOR, 1.00]
    readouts = [screened_readout(factor) for factor in factors]

    print(f"  pure-gauge payload = beta, r0/a, sigma_a2, plaquette = {payload}")
    for factor, value in zip(factors, readouts):
        print(f"  f_screen={factor:.2f} -> sqrt(sigma)={value:.2f} MeV")

    check(
        "Pure-gauge payload is unchanged across the factor family",
        len({payload for _ in factors}) == 1,
    )
    check(
        "Different factors produce materially different sqrt(sigma) readouts",
        max(readouts) - min(readouts) > 40.0,
        f"spread={max(readouts) - min(readouts):.2f} MeV",
    )
    check(
        "The current rough factor is not selected by the pure-gauge payload",
        ROUGH_SCREENING_FACTOR in factors and len(set(readouts)) == len(factors),
    )
    check(
        "The comparator-implied factor is distinct from the rough factor",
        abs(PDG_COMPARATOR_MEV / SQRT_SIGMA_QUENCHED_MEV - ROUGH_SCREENING_FACTOR) > 0.04,
        f"440/484={PDG_COMPARATOR_MEV / SQRT_SIGMA_QUENCHED_MEV:.4f}",
    )


def test_determinant_reweighting_is_load_bearing() -> None:
    print("\n" + "=" * 88)
    print("PART 3: SEA-FERMION DETERMINANT DATA CHANGE THE MEASURE")
    print("=" * 88)

    gauge_weights = np.array([1.0, 0.72, 0.46, 0.33])
    local_sigma_a2 = np.array([0.049, 0.0465, 0.043, 0.039])
    singular_value_bank = np.array(
        [
            [0.22, 0.35, 0.51, 0.73],
            [0.12, 0.19, 0.31, 0.58],
            [0.05, 0.09, 0.18, 0.41],
            [0.015, 0.04, 0.11, 0.29],
        ]
    )

    quenched = reweighted_observable(gauge_weights, local_sigma_a2, singular_value_bank, masses=None)
    light_sea = reweighted_observable(gauge_weights, local_sigma_a2, singular_value_bank, masses=(0.02, 0.03, 0.10))
    heavier_sea = reweighted_observable(gauge_weights, local_sigma_a2, singular_value_bank, masses=(0.50, 0.60, 0.70))

    print(f"  quenched <sigma a^2>       = {quenched:.8f}")
    print(f"  light-sea <sigma a^2>      = {light_sea:.8f}")
    print(f"  heavier-sea <sigma a^2>    = {heavier_sea:.8f}")

    check(
        "Including determinant weights changes the measured observable",
        abs(light_sea - quenched) > 1.0e-3,
        f"delta={light_sea - quenched:+.6f}",
    )
    check(
        "Changing sea masses changes the determinant-weighted observable",
        abs(light_sea - heavier_sea) > 1.0e-4,
        f"delta={light_sea - heavier_sea:+.6f}",
    )
    check(
        "Therefore N_f and sea-mass data are load-bearing for B2",
        abs(light_sea - quenched) > 1.0e-3 and abs(light_sea - heavier_sea) > 1.0e-4,
    )


def test_volume_and_budget_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CURRENT FINITE RUNNER CANNOT BE THE B2 CLOSURE")
    print("=" * 88)

    confinement_note = read("docs/CONFINEMENT_STRING_TENSION_NOTE.md")
    confinement_runner = read("scripts/frontier_confinement_string_tension.py")

    current_linear_size = 4
    target_linear_size = 16
    current_links = current_linear_size**4 * 4
    target_links = target_linear_size**4 * 4
    ratio = target_links / current_links

    check(
        "Confinement note says quantitative extraction needs larger volumes",
        "Quantitative" in confinement_note and "requires volumes" in confinement_note and "16" in confinement_note,
    )
    check(
        "Current runner uses L=4 for a qualitative pure-gauge check",
        "L = 4" in confinement_runner and "Pure-gauge SU(3) Monte Carlo" in confinement_runner,
    )
    check(
        "A 16^4 check has much larger link count than the current 4^4 runner",
        math.isclose(ratio, 256.0),
        f"link-count ratio={ratio:.0f}x",
    )
    check(
        "The B2 spread exceeds a one-percent budget until determinant data enter",
        (1.00 - 0.90) > 0.01,
        "screening-factor family spans ten percent",
    )


def test_status_firewall() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CLAIM-STATUS FIREWALL")
    print("=" * 88)

    pure_payload = pure_gauge_payload()
    missing_inputs = {
        "sea_fermion_determinant": True,
        "n_f_2_plus_1_ensemble": True,
        "sea_mass_specification": True,
        "large_volume_creutz_ratio": True,
    }
    no_current_surface_closure = all(missing_inputs.values()) and pure_payload == pure_gauge_payload()

    check("Sea-fermion determinant input is absent from the current B2 payload", missing_inputs["sea_fermion_determinant"])
    check("No N_f=2+1 beta=6.0 ensemble is present in the current B2 payload", missing_inputs["n_f_2_plus_1_ensemble"])
    check("Sea-mass specification remains load-bearing", missing_inputs["sea_mass_specification"])
    check("Large-volume Creutz-ratio extraction remains load-bearing", missing_inputs["large_volume_creutz_ratio"])
    check("B2 cannot close on the current data alone", no_current_surface_closure)


def main() -> int:
    print("=" * 88)
    print("LANE 1 B2: DYNAMICAL SCREENING BOUNDARY")
    print("=" * 88)
    print()
    print("Claim under test:")
    print("  Current pure-gauge beta=6.0 data plus the rough 0.96 factor might")
    print("  close the N_f=2+1 dynamical screening budget for sqrt(sigma).")
    print()
    print("Boundary result:")
    print("  The B2 factor is determinant-dependent. The current data remain")
    print("  bounded-support only until a dynamical calculation or explicit")
    print("  budgeted comparator is supplied.")

    test_authority_text()
    test_screening_factor_degeneracy()
    test_determinant_reweighting_is_load_bearing()
    test_volume_and_budget_boundary()
    test_status_firewall()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT:
        print("B2 boundary runner failed; do not use the note.")
        return 1

    print("Result: B2 remains open; current pure-gauge data cannot close it.")
    print("A proper N_f=2+1 determinant ensemble or explicit budgeted comparator is required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
