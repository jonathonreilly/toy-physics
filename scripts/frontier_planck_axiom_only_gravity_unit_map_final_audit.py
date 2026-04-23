#!/usr/bin/env python3
"""Final audit for the bare-axiom Planck unit-map target.

This runner checks the reviewer-facing result:
the native coefficient is exact, but the current axiom stack does not force the
remaining boundary unit-map multiplier to one.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_AUDIT = ROOT / "docs/PLANCK_SCALE_AXIOM_ONLY_GRAVITY_UNIT_MAP_FINAL_AUDIT_2026-04-23.md"
PLAIN_STATUS = ROOT / "docs/PLANCK_SCALE_NATURE_REVIEW_PLAIN_LANGUAGE_STATUS_2026-04-23.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
HORIZON = ROOT / "docs/PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md"
COSMIC = ROOT / "docs/PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"


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
            "last-multiplier-is-explicit",
            "`S_micro / k_B = mu c_cell A / a^2`" in audit
            and "`mu = 1`" in audit
            and "derive `mu = 1`" in audit,
            "the exact remaining target should be the boundary unit-map multiplier",
        ),
        (
            "mu-countermodels-change-planck-length",
            matched_a2 == [Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)]
            and "| `mu = 1/2` | `a^2 = (1/2) l_P^2` |" in audit
            and "| `mu = 2` | `a^2 = 2 l_P^2` |" in audit,
            f"a^2/l_P^2 values={matched_a2}",
        ),
        (
            "scale-ray-no-go-supports-no-bare-unit-map",
            "fixes a **scale ray**, not an absolute scale\nanchor" in scale_ray
            and "current action comparison does not force the\nboundary multiplier `mu`" in audit,
            "homogeneous gravity/action family cannot select the absolute unit map",
        ),
        (
            "horizon-lane-does-not-supply-quarter",
            "no exact route to a `1/4` coefficient" in horizon
            and "Widom-class no-go" in horizon
            and "not supplied by the current entanglement carrier class" in audit,
            "current horizon entropy carriers do not close the boundary multiplier",
        ),
        (
            "cosmic-address-cancels-surface-area",
            "Since `A_U > 0`, the area cancels" in audit
            and "Cosmic-address imports do not replace" in cosmic,
            "age/current-time data select a surface but do not set the multiplier",
        ),
        (
            "electroweak-is-calibration-not-native",
            "calibration use of observed data, not a bare Planck-length derivation"
            in plain
            and "not a bare Planck derivation" in cosmic,
            "observed electroweak scale may calibrate but does not derive the Planck unit",
        ),
        (
            "plain-status-has-safe-and-unsafe-claims",
            "Use this:" in plain
            and "Do not use this:" in plain
            and "Conditional on identifying the primitive one-step worldtube" in plain
            and "bare physical `Cl(3)` / `Z^3` axioms alone force" in plain,
            "reviewer front door must prevent the unconditional overclaim",
        ),
        (
            "final-verdict-is-conditional-not-unconditional",
            "does **not** yet prove the fully bare claim" in audit
            and "not yet Nature-grade as an unconditional bare-axiom derivation"
            in plain,
            "final status should be explicit under hostile review",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
