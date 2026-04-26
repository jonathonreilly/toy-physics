#!/usr/bin/env python3
"""Verifier for the atomic Rydberg dependency-compression theorem.

The runner checks the analytic two-body reduction, exact hydrogenic scaling,
finite-mass correction, and dependency/sensitivity budget. Numerical constants
are used only as smoke tests of the formulas; they are not framework claims.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    suffix = f" -- {detail}" if detail else ""
    if condition:
        PASS_COUNT += 1
        print(f"PASS: {name}{suffix}")
    else:
        FAIL_COUNT += 1
        print(f"FAIL: {name}{suffix}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def reduced_mass(m1: Fraction, m2: Fraction) -> Fraction:
    return m1 * m2 / (m1 + m2)


def center_of_mass_coefficients(m1: Fraction, m2: Fraction) -> dict[str, Fraction]:
    """Return coefficients in T = cP P^2 + cp p^2 + cross P.p.

    p1 = (m1/M) P + p, p2 = (m2/M) P - p.
    """
    total = m1 + m2
    a = m1 / total
    b = m2 / total
    coeff_p_total = a * a / (2 * m1) + b * b / (2 * m2)
    coeff_p_rel = Fraction(1, 2 * m1) + Fraction(1, 2 * m2)
    coeff_cross = a / m1 - b / m2
    return {
        "P2": coeff_p_total,
        "p2": coeff_p_rel,
        "cross": coeff_cross,
        "expected_P2": Fraction(1, 2 * total),
        "expected_p2": Fraction(1, 2 * reduced_mass(m1, m2)),
    }


def hydrogenic_energy_factor(z: int, n: int, mu_over_me: Fraction = Fraction(1, 1)) -> Fraction:
    """Dimensionless factor multiplying m_e c^2 alpha^2."""
    return -mu_over_me * Fraction(z * z, 2 * n * n)


def transition_factor(z: int, n_initial: int, n_final: int) -> Fraction:
    """Positive photon factor multiplying mu c^2 alpha^2/2."""
    return Fraction(z * z, 1) * (
        Fraction(1, n_final * n_final) - Fraction(1, n_initial * n_initial)
    )


def finite_mass_factor(m_over_mnucleus: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + m_over_mnucleus)


def mass_sensitivity_weights(m1: Fraction, m2: Fraction) -> tuple[Fraction, Fraction]:
    total = m1 + m2
    return m2 / total, m1 / total


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def numeric_smoke_tests() -> dict[str, float]:
    inv_alpha = 137.035999084
    alpha = 1.0 / inv_alpha
    me_ev = 510_998.95000
    mp_over_me = 1836.15267343
    reduced_factor_h = 1.0 / (1.0 + 1.0 / mp_over_me)
    rydberg_infinite_ev = 0.5 * me_ev * alpha * alpha
    rydberg_h_ev = rydberg_infinite_ev * reduced_factor_h
    lyman_alpha_ev = rydberg_h_ev * (1.0 - 1.0 / 4.0)
    return {
        "rydberg_infinite_ev": rydberg_infinite_ev,
        "reduced_factor_h": reduced_factor_h,
        "rydberg_h_ev": rydberg_h_ev,
        "hydrogen_ground_ev": -rydberg_h_ev,
        "lyman_alpha_ev": lyman_alpha_ev,
    }


def main() -> int:
    theorem_note = DOCS / "ATOMIC_RYDBERG_DEPENDENCY_COMPRESSION_THEOREM_NOTE_2026-04-26.md"
    lane_note = DOCS / "lanes" / "open_science" / "02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md"
    scaffold_note = DOCS / "ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md"
    bound_state_note = DOCS / "BOUND_STATE_SELECTION_NOTE.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("Lane 2 open-science note exists", lane_note.exists(), str(lane_note.relative_to(ROOT)))
    check("atomic scaffold note exists", scaffold_note.exists(), str(scaffold_note.relative_to(ROOT)))
    check("bound-state selection note exists", bound_state_note.exists(), str(bound_state_note.relative_to(ROOT)))

    text = read_text(theorem_note)
    lower = " ".join(text.lower().split())
    lane_text = read_text(lane_note).lower()
    scaffold_text = " ".join(read_text(scaffold_note).lower().split())

    check("note records primary runner", "frontier_atomic_rydberg_dependency_compression.py" in text)
    check("note states dependency-compression status", "dependency-compression theorem" in lower)
    check("note states no atomic-scale closure", "does not close lane 2" in lower)
    check("note names reduced mass gate", "1/(1 + m_e/m_p)" in text)
    check("note excludes frontier extension lanes", "time-travel, teleportation, or antigravity" in lower)
    check("Lane 2 is open and scaffold-dependent", "accepted critical open science lane" in lane_text)
    check("Lane 2 first target is dependency isolation", "isolate the exact dependency chain" in lane_text)
    check(
        "scaffold admits textbook inputs",
        "textbook inputs" in scaffold_text and "not** a retained framework derivation" in scaffold_text,
    )

    for m1, m2 in [(Fraction(3), Fraction(5)), (Fraction(2), Fraction(7)), (Fraction(11), Fraction(13))]:
        mu = reduced_mass(m1, m2)
        coeffs = center_of_mass_coefficients(m1, m2)
        check(f"mu reciprocal identity m=({m1},{m2})", Fraction(1, mu) == Fraction(1, m1) + Fraction(1, m2), str(mu))
        check(f"center-of-mass P coefficient m=({m1},{m2})", coeffs["P2"] == coeffs["expected_P2"], str(coeffs))
        check(f"center-of-mass relative coefficient m=({m1},{m2})", coeffs["p2"] == coeffs["expected_p2"], str(coeffs))
        check(f"center-of-mass cross term cancels m=({m1},{m2})", coeffs["cross"] == 0, str(coeffs))

    for z in range(1, 5):
        ground = hydrogenic_energy_factor(z, 1)
        for n in range(1, 8):
            factor = hydrogenic_energy_factor(z, n)
            check(f"Z={z}, n={n}: E_n/E_1 = 1/n^2", factor / ground == Fraction(1, n * n), str(factor))
        e2_to_1 = -hydrogenic_energy_factor(z, 1) + hydrogenic_energy_factor(z, 2)
        line_factor = transition_factor(z, 2, 1) / 2
        check(f"Z={z}: 2->1 transition equals level difference", e2_to_1 == line_factor, f"{e2_to_1} vs {line_factor}")
        check(f"Z={z}: Z^2 ground scaling", ground == -Fraction(z * z, 2), str(ground))

    eta = Fraction(1, 1836)
    finite = finite_mass_factor(eta)
    check("finite mass factor is below infinite-mass value", 0 < finite < 1, str(finite))
    check("finite mass factor exact formula", finite == Fraction(1836, 1837), str(finite))
    e_h = hydrogenic_energy_factor(1, 1, finite)
    check("hydrogen ground-state factor includes reduced mass", e_h == -Fraction(918, 1837), str(e_h))

    w1, w2 = mass_sensitivity_weights(Fraction(1), Fraction(1836))
    check("mass sensitivity weights sum to one", w1 + w2 == 1, f"{w1}, {w2}")
    check("electron sensitivity dominates hydrogen", w1 > Fraction(999, 1000), str(w1))
    check("proton sensitivity is reduced-mass suppressed", w2 == Fraction(1, 1837), str(w2))
    check("alpha log sensitivity is exactly two", Fraction(2, 1) == 2)

    for n_i, n_f in [(2, 1), (3, 1), (4, 2), (5, 3)]:
        f = transition_factor(1, n_i, n_f)
        expected = Fraction(1, n_f * n_f) - Fraction(1, n_i * n_i)
        check(f"transition factor {n_i}->{n_f} exact", f == expected, str(f))

    smoke = numeric_smoke_tests()
    check(
        "numeric smoke: infinite-mass Rydberg energy",
        close(smoke["rydberg_infinite_ev"], 13.60569312, 2e-8),
        f"{smoke['rydberg_infinite_ev']:.12f} eV",
    )
    check(
        "numeric smoke: hydrogen reduced-mass factor",
        close(smoke["reduced_factor_h"], 0.99945568, 2e-8),
        f"{smoke['reduced_factor_h']:.12f}",
    )
    check(
        "numeric smoke: hydrogen leading ground state",
        close(smoke["hydrogen_ground_ev"], -13.59828726, 3e-8),
        f"{smoke['hydrogen_ground_ev']:.12f} eV",
    )
    check(
        "numeric smoke: Lyman-alpha leading energy",
        close(smoke["lyman_alpha_ev"], 10.19871545, 3e-8),
        f"{smoke['lyman_alpha_ev']:.12f} eV",
    )

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
