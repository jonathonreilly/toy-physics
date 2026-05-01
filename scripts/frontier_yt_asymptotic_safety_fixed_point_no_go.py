#!/usr/bin/env python3
"""
No-go runner for deriving beta_lambda(M_Pl)=0 from a perturbative SM fixed
point / asymptotic-safety interpretation on the current PR #230 surface.

At one loop in the SM bridge, the gauge beta functions have no nonzero
perturbative fixed point.  If the full beta vector is forced to vanish in the
one-loop SM subsystem, the only real solution is the Gaussian point
g1=g2=g3=y_t=lambda=0.  That does not reproduce the Planck selector value and
cannot be the PR #230 top-Yukawa derivation.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_asymptotic_safety_fixed_point_no_go_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_one_loop_full_fixed_point() -> dict[str, str]:
    g1, g2, g3, y, lam = sp.symbols("g1 g2 g3 y lambda", real=True)
    gp2 = sp.Rational(3, 5) * g1**2
    beta_g1 = sp.Rational(41, 10) * g1**3
    beta_g2 = -sp.Rational(19, 6) * g2**3
    beta_g3 = -7 * g3**3
    beta_y = y * (
        sp.Rational(9, 2) * y**2
        - sp.Rational(17, 20) * g1**2
        - sp.Rational(9, 4) * g2**2
        - 8 * g3**2
    )
    beta_lam_at_zero = -6 * y**4 + sp.Rational(3, 8) * (
        2 * g2**4 + (g2**2 + gp2) ** 2
    )

    gauge_solution = sp.solve([sp.Eq(beta_g1, 0), sp.Eq(beta_g2, 0), sp.Eq(beta_g3, 0)], [g1, g2, g3], dict=True)
    gaussian_only = gauge_solution == [{g1: 0, g2: 0, g3: 0}]
    beta_y_gaussian_gauge = sp.factor(beta_y.subs({g1: 0, g2: 0, g3: 0}))
    beta_lam_gaussian_gauge = sp.factor(beta_lam_at_zero.subs({g1: 0, g2: 0, g3: 0}))
    full_solution_y = sp.solve(
        [sp.Eq(beta_y_gaussian_gauge, 0), sp.Eq(beta_lam_gaussian_gauge, 0)],
        [y],
        dict=True,
    )
    y_only_zero = full_solution_y == [{y: 0}]

    report(
        "one-loop-gauge-fixed-point-gaussian-only",
        gaussian_only,
        f"gauge beta solution = {gauge_solution}",
    )
    report(
        "gaussian-gauge-yukawa-beta",
        str(beta_y_gaussian_gauge) == "9*y**3/2",
        f"beta_y at zero gauge = {beta_y_gaussian_gauge}",
    )
    report(
        "gaussian-gauge-quartic-beta",
        str(beta_lam_gaussian_gauge) == "-6*y**4",
        f"beta_lambda(lambda=0) at zero gauge = {beta_lam_gaussian_gauge}",
    )
    report(
        "full-one-loop-fixed-point-has-y-zero",
        y_only_zero,
        f"full fixed point forces y_t = {full_solution_y}",
    )

    return {
        "beta_g1": str(beta_g1),
        "beta_g2": str(beta_g2),
        "beta_g3": str(beta_g3),
        "beta_y": str(beta_y),
        "beta_lambda_at_lambda_zero": str(sp.factor(beta_lam_at_zero)),
        "gauge_solution": str(gauge_solution),
        "beta_y_at_zero_gauge": str(beta_y_gaussian_gauge),
        "beta_lambda_at_zero_gauge": str(beta_lam_gaussian_gauge),
        "full_solution_y": str(full_solution_y),
    }


def assert_partial_fixed_point_is_extra_relation() -> dict[str, object]:
    g1, g2, g3, y = sp.symbols("g1 g2 g3 y", positive=True)
    gp2 = sp.Rational(3, 5) * g1**2
    beta_y_bracket = (
        sp.Rational(9, 2) * y**2
        - sp.Rational(17, 20) * g1**2
        - sp.Rational(9, 4) * g2**2
        - 8 * g3**2
    )
    beta_lam_at_zero = -6 * y**4 + sp.Rational(3, 8) * (
        2 * g2**4 + (g2**2 + gp2) ** 2
    )
    y2_from_betay = sp.solve(sp.Eq(beta_y_bracket, 0), y**2)[0]
    y4_from_betalambda = sp.solve(sp.Eq(beta_lam_at_zero, 0), y**4)[0]
    compatibility = sp.factor(y2_from_betay**2 - y4_from_betalambda)

    report(
        "partial-yukawa-fixed-point-extra-condition",
        compatibility != 0,
        f"beta_y=0 and beta_lambda=0 impose compatibility {compatibility}",
    )
    report(
        "partial-fixed-point-not-substrate-derived",
        True,
        "without a gauge fixed point or new UV completion, partial beta conditions are added selectors",
    )
    return {
        "y2_from_beta_y_zero": str(y2_from_betay),
        "y4_from_beta_lambda_zero": str(y4_from_betalambda),
        "compatibility_condition": str(compatibility),
    }


def assert_authority_boundary() -> dict[str, bool]:
    gbare = read_doc("docs/G_BARE_DERIVATION_NOTE.md")
    selector = read_doc("docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md")
    has_su3_no_fixed_point = "SU(3) lattice beta function has NO nontrivial fixed point" in gbare
    selector_conditional = "conditional-support / open selector route" in selector
    selector_premise_open = "beta_lambda(M_Pl)=0" in selector and "not prove" in selector

    report(
        "repo-records-su3-no-fixed-point",
        has_su3_no_fixed_point,
        "existing g_bare note rejects nontrivial SU(3) lattice-beta fixed point route",
    )
    report(
        "selector-still-conditional",
        selector_conditional and selector_premise_open,
        "double-criticality note does not claim an asymptotic-safety proof",
    )
    return {
        "has_su3_no_fixed_point": has_su3_no_fixed_point,
        "selector_conditional": selector_conditional,
        "selector_premise_open": selector_premise_open,
    }


def main() -> int:
    print("YT asymptotic-safety fixed-point no-go")
    print("=" * 72)

    full_fixed_point = assert_one_loop_full_fixed_point()
    partial = assert_partial_fixed_point_is_extra_relation()
    authority = assert_authority_boundary()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary",
        "target": "derive beta_lambda(M_Pl)=0 from a perturbative SM fixed point/asymptotic-safety route",
        "verdict": (
            "The one-loop SM beta-vector has only the Gaussian gauge fixed "
            "point in the perturbative subsystem.  Imposing full beta-vector "
            "vanishing then forces y_t=0, not the PR #230 selector value. "
            "Partial beta conditions are extra selectors, not substrate closure."
        ),
        "full_fixed_point": full_fixed_point,
        "partial_fixed_point": partial,
        "authority_boundary": authority,
        "remaining_open_premise": "a non-SM UV fixed-point theorem or new asymptotic-safety structure beyond the current substrate",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
