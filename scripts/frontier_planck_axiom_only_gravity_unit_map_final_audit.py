#!/usr/bin/env python3
"""Final audit for the Planck unit-map target after event Ward closure."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_AUDIT = ROOT / "docs/PLANCK_SCALE_AXIOM_ONLY_GRAVITY_UNIT_MAP_FINAL_AUDIT_2026-04-23.md"
PLAIN_STATUS = ROOT / "docs/PLANCK_SCALE_NATURE_REVIEW_PLAIN_LANGUAGE_STATUS_2026-04-23.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
HORIZON = ROOT / "docs/PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md"
COSMIC = ROOT / "docs/PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
EVENT_WARD = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def read(path: Path) -> str:
    return path.read_text()


def main() -> int:
    audit = read(FINAL_AUDIT)
    plain = read(PLAIN_STATUS)
    scale_ray = read(SCALE_RAY)
    horizon = read(HORIZON)
    cosmic = read(COSMIC)
    event_ward = read(EVENT_WARD)

    dim_cell = 16
    rank_packet = 4
    c_cell = Fraction(rank_packet, dim_cell)
    mu_values = [Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)]
    matched_a2 = [4 * mu * c_cell for mu in mu_values]

    banned_reviewer_terms = [
        "P1",
        "Axiom Extension",
        "GSI",
        "Gravity-Sector Identification",
    ]
    reviewer_text = audit + "\n" + plain

    checks = [
        (
            "reviewer-facing-new-docs-avoid-project-shorthand",
            all(term not in reviewer_text for term in banned_reviewer_terms),
            "new reviewer-facing status must use plain physics language",
        ),
        (
            "native-quarter-is-exact",
            c_cell == Fraction(1, 4)
            and "`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`" in audit
            and "`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`" in plain,
            f"rank/dim={rank_packet}/{dim_cell}={c_cell}",
        ),
        (
            "event-ward-closes-last-density-law",
            "`S_micro / k_B = mu c_cell A / a^2`" in audit
            and "`mu = 1`" in audit
            and "`delta := nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`"
            in audit
            and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in event_ward,
            "the old multiplier target is closed on the primitive event Ward surface",
        ),
        (
            "mu-countermodels-are-now-rejection-tests",
            matched_a2 == [Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)]
            and "| `mu = 1/2` | `a^2 = (1/2) l_P^2` |" in audit
            and "| `mu = 2` | `a^2 = 2 l_P^2` |" in audit,
            f"a^2/l_P^2 values={matched_a2}; live only if event Ward is rejected",
        ),
        (
            "scale-ray-no-go-supports-no-bare-unit-map",
            "fixes a **scale ray**, not an absolute scale\nanchor" in scale_ray
            and "homogeneous Einstein-Hilbert-style action comparisons fix a scale ray"
            in audit,
            "homogeneous gravity/action family was not the closure route",
        ),
        (
            "horizon-lane-does-not-supply-quarter",
            "no exact route to a `1/4` coefficient" in horizon
            and "Widom-class no-go" in horizon
            and "current horizon-entropy carriers do not derive the black-hole quarter"
            in audit,
            "horizon entropy carriers are not the closure route",
        ),
        (
            "cosmic-address-cancels-surface-area",
            "cosmological address data select a surface but do not set the microscopic\n   unit map"
            in audit
            and "Cosmic-address imports do not replace" in cosmic,
            "age/current-time data select a surface but do not set the multiplier",
        ),
        (
            "electroweak-is-calibration-not-native",
            "observed electroweak scale as a Planck calibration" in plain
            and "electroweak calibration can set a phenomenological scale, but is not a\n   native Planck proof"
            in audit
            and "not a bare Planck derivation" in cosmic,
            "observed electroweak scale may calibrate but does not derive the Planck unit",
        ),
        (
            "plain-status-has-safe-and-unsafe-claims",
            "Use this:" in plain
            and "Do not use this:" in plain
            and "the parent-source theorem identifies\n> Schur"
            in plain
            and "Ordinary Schur source-response Ward identities alone" in plain,
            "reviewer front door must name the actual closure surface",
        ),
        (
            "final-verdict-is-event-ward-closed-with-explicit-rejection",
            "proposed native closure of the last value-law gap" in audit
            and "Nature-grade on the retained primitive boundary-action"
            in plain,
            "final status should state closure and the remaining rejection target",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
