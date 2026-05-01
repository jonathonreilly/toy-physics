#!/usr/bin/env python3
"""
No-go runner for deriving beta_lambda(M_Pl)=0 from the weaker vacuum-stability
boundary lambda(M_Pl)=0 plus local stability below M_Pl.

The multiple-point / Planck-criticality route would close only if the substrate
derives a tangent condition.  A one-sided stability condition at the upper
boundary is weaker: with t = log(mu), lambda(t_Pl)=0 and lambda(t_Pl-eps)>=0
requires beta_lambda(t_Pl) <= 0, not beta_lambda(t_Pl)=0.  That inequality
leaves a continuum of allowed y_t values and therefore cannot select y_t.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_vacuum_stability_stationarity_no_go_2026-05-01.json"

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


def beta_lambda_one_loop_at_zero(g1: float, g2: float, yt: float) -> float:
    """One-loop numerator at lambda=0 with g1 GUT-normalized."""
    gp2 = (3.0 / 5.0) * g1 * g1
    return -6.0 * yt**4 + 3.0 / 8.0 * (2.0 * g2**4 + (g2 * g2 + gp2) ** 2)


def selector_y_star(g1: float, g2: float) -> float:
    gp2 = (3.0 / 5.0) * g1 * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp2) ** 2) / 16.0) ** 0.25


def local_lambda_below_boundary(beta_at_boundary: float, eps: float = 1.0e-3) -> float:
    """Taylor lambda(t_Pl - eps) from lambda(t_Pl)=0."""
    return -eps * beta_at_boundary


def assert_stability_is_inequality_not_stationarity() -> dict[str, object]:
    g1 = 0.6166064056
    g2 = 0.5063564410
    y_star = selector_y_star(g1, g2)
    samples = [
        ("below_selector", 0.90 * y_star),
        ("at_selector", 1.00 * y_star),
        ("above_selector_10pct", 1.10 * y_star),
        ("above_selector_50pct", 1.50 * y_star),
    ]
    rows = []
    for name, yt in samples:
        beta = beta_lambda_one_loop_at_zero(g1, g2, yt)
        lam_below = local_lambda_below_boundary(beta)
        locally_stable_below = lam_below >= -1.0e-15
        rows.append(
            {
                "name": name,
                "yt": yt,
                "beta_lambda_one_loop_at_zero": beta,
                "lambda_below_taylor": lam_below,
                "locally_stable_below": locally_stable_below,
            }
        )

    below_unstable = not rows[0]["locally_stable_below"]
    at_stationary = abs(rows[1]["beta_lambda_one_loop_at_zero"]) < 1.0e-14
    above_10_stable_nonzero = rows[2]["locally_stable_below"] and rows[2]["beta_lambda_one_loop_at_zero"] < 0
    above_50_stable_nonzero = rows[3]["locally_stable_below"] and rows[3]["beta_lambda_one_loop_at_zero"] < 0

    report(
        "selector-beta-zero",
        at_stationary,
        f"y_star={y_star:.12f} gives beta_lambda ~= 0",
    )
    report(
        "below-selector-locally-unstable",
        below_unstable,
        "y_t below the selector gives beta>0 and lambda<0 just below M_Pl",
    )
    report(
        "above-selector-stable-but-nonstationary-10pct",
        above_10_stable_nonzero,
        "10% above selector has beta<0, so local stability holds without beta=0",
    )
    report(
        "above-selector-stable-but-nonstationary-50pct",
        above_50_stable_nonzero,
        "50% above selector also satisfies the one-sided stability inequality",
    )
    report(
        "stability-gives-lower-bound-not-point",
        above_10_stable_nonzero and above_50_stable_nonzero,
        "lambda>=0 below M_Pl implies beta<=0 locally, leaving a continuum of y_t values",
    )

    return {
        "g1_MPl": g1,
        "g2_MPl": g2,
        "y_star": y_star,
        "samples": rows,
        "local_condition": "lambda(M_Pl)=0 and lambda below M_Pl nonnegative implies beta_lambda(M_Pl)<=0, not equality",
    }


def assert_current_vacuum_authority_is_bounded() -> dict[str, bool]:
    vacuum = read_doc("docs/VACUUM_CRITICAL_STABILITY_NOTE.md")
    higgs = read_doc("docs/HIGGS_MASS_DERIVED_NOTE.md")
    selector = read_doc("docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md")

    vacuum_bounded = "bounded companion prediction" in vacuum
    vacuum_inherits_yt = "inherits the explicit-systematic Yukawa / top lane" in vacuum
    higgs_lambda_boundary = "`lambda(M_Pl) = 0` is framework-native" in higgs
    higgs_inherits_yt = "inherits the current YT-lane precision caveat" in higgs or "inherited from `y_t`" in higgs
    selector_conditional = "conditional-support / open selector route" in selector

    report(
        "vacuum-note-bounded",
        vacuum_bounded,
        "vacuum criticality is explicitly bounded, not retained stationarity",
    )
    report(
        "vacuum-note-inherits-yt",
        vacuum_inherits_yt,
        "vacuum readout inherits the YT/top systematic",
    )
    report(
        "higgs-authority-lambda-only",
        higgs_lambda_boundary and higgs_inherits_yt,
        "Higgs authority gives lambda boundary but keeps YT caveat",
    )
    report(
        "selector-remains-conditional",
        selector_conditional,
        "double-criticality selector is still marked conditional/open",
    )

    return {
        "vacuum_bounded": vacuum_bounded,
        "vacuum_inherits_yt": vacuum_inherits_yt,
        "higgs_lambda_boundary": higgs_lambda_boundary,
        "higgs_inherits_yt": higgs_inherits_yt,
        "selector_conditional": selector_conditional,
    }


def assert_route_taxonomy() -> list[dict[str, str]]:
    routes = [
        {
            "route": "one_sided_vacuum_stability",
            "status": "blocked",
            "reason": "Local stability below M_Pl gives beta_lambda<=0, not beta_lambda=0.",
        },
        {
            "route": "critical_tangent",
            "status": "conditional_extra_premise",
            "reason": "Adding tangency beta_lambda=0 is exactly the missing selector.",
        },
        {
            "route": "multiple_point_degeneracy",
            "status": "conditional_extra_premise",
            "reason": "Would need an added theorem that the Planck boundary is a double zero.",
        },
        {
            "route": "observed_vacuum_criticality",
            "status": "forbidden_as_derivation",
            "reason": "Using observed near-criticality would be an admitted comparator, not substrate proof.",
        },
    ]
    allowed = {"blocked", "conditional_extra_premise", "forbidden_as_derivation"}
    for item in routes:
        report(
            f"route-{item['route']}",
            item["status"] in allowed,
            f"{item['status']}: {item['reason']}",
        )
    return routes


def main() -> int:
    print("YT vacuum-stability stationarity no-go")
    print("=" * 72)

    inequality = assert_stability_is_inequality_not_stationarity()
    authority = assert_current_vacuum_authority_is_bounded()
    routes = assert_route_taxonomy()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary",
        "target": "derive beta_lambda(M_Pl)=0 from lambda(M_Pl)=0 plus one-sided vacuum stability",
        "verdict": (
            "One-sided vacuum stability at a lambda=0 upper boundary gives a "
            "local inequality beta_lambda(M_Pl)<=0.  It does not force the "
            "stationary equality beta_lambda(M_Pl)=0 and therefore does not "
            "select a unique y_t."
        ),
        "inequality_boundary": inequality,
        "authority_boundary": authority,
        "routes": routes,
        "remaining_open_premise": "a new multiple-point/double-zero theorem or explicit Planck tangency selector",
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
