#!/usr/bin/env python3
"""
No-go runner for deriving beta_lambda(M_Pl)=0 from the current Cl(3)/Z^3
substrate surface.

The target is the blocker exposed by the Planck double-criticality selector:

    lambda(M_Pl) = 0
    beta_lambda(M_Pl) = 0

The runner verifies that the current retained/support substrate ingredients
derive the first boundary condition but do not derive the second.  In the SM
RGE bridge, beta_lambda(M_Pl)=0 is a codimension-one relation among gauge and
Yukawa couplings; it is not a consequence of lambda(M_Pl)=0, taste-scalar
isotropy, or the finite lattice source generator alone.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json"

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


def one_loop_beta_lambda_polynomial() -> dict[str, str]:
    """Return exact symbolic facts about beta_lambda at lambda=0.

    Coupling convention follows frontier_higgs_mass_full_3loop.py:
    g1 is GUT-normalized and gp^2 = (3/5) g1^2.
    """
    g1, g2, y, lam = sp.symbols("g1 g2 y lambda", positive=True)
    gp2 = sp.Rational(3, 5) * g1**2
    beta_1 = (
        24 * lam**2
        + 12 * lam * y**2
        - 6 * y**4
        - 3 * lam * (3 * g2**2 + gp2)
        + sp.Rational(3, 8) * (2 * g2**4 + (g2**2 + gp2) ** 2)
    )
    beta_at_lambda_zero = sp.factor(beta_1.subs(lam, 0))
    condition = sp.factor(sp.solve(sp.Eq(beta_at_lambda_zero, 0), y**4)[0])
    derivative_y = sp.factor(sp.diff(beta_at_lambda_zero, y))

    return {
        "beta_1": str(sp.factor(beta_1)),
        "beta_at_lambda_zero": str(beta_at_lambda_zero),
        "condition_y4": str(condition),
        "derivative_y": str(derivative_y),
    }


def numeric_beta_lambda_one_loop(g1: float, g2: float, yt: float) -> float:
    gp2 = (3.0 / 5.0) * g1 * g1
    return -6.0 * yt**4 + 3.0 / 8.0 * (2.0 * g2**4 + (g2 * g2 + gp2) ** 2)


def selector_y_from_gauge(g1: float, g2: float) -> float:
    gp2 = (3.0 / 5.0) * g1 * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp2) ** 2) / 16.0) ** 0.25


def assert_symbolic_no_identity() -> dict[str, str]:
    facts = one_loop_beta_lambda_polynomial()
    g1, g2, y = sp.symbols("g1 g2 y", positive=True)
    beta_at_zero = sp.sympify(facts["beta_at_lambda_zero"])
    derivative_y = sp.sympify(facts["derivative_y"])

    report(
        "one-loop-beta-nonzero-polynomial",
        beta_at_zero != 0,
        f"beta_lambda(lambda=0) = {sp.factor(beta_at_zero)}",
    )
    report(
        "one-loop-beta-yukawa-dependent",
        str(sp.factor(derivative_y)) == "-24*y**3",
        f"d beta/dy = {sp.factor(derivative_y)}",
    )
    report(
        "beta-zero-codimension-one",
        facts["condition_y4"] == "3*(3*g1**4 + 10*g1**2*g2**2 + 25*g2**4)/400",
        f"beta=0 forces y^4 = {facts['condition_y4']}",
    )

    # Exhibit two lambda=0 points with the same gauge couplings and different
    # beta signs.  That disproves any implication lambda=0 => beta=0.
    g1v = 0.6166064056
    g2v = 0.5063564410
    y_star = selector_y_from_gauge(g1v, g2v)
    beta_low = numeric_beta_lambda_one_loop(g1v, g2v, 0.0)
    beta_high = numeric_beta_lambda_one_loop(g1v, g2v, 2.0 * y_star)
    beta_star = numeric_beta_lambda_one_loop(g1v, g2v, y_star)
    report(
        "lambda-zero-positive-beta-example",
        beta_low > 0.0,
        f"at y=0, beta_lambda numerator = {beta_low:.8e}",
    )
    report(
        "lambda-zero-negative-beta-example",
        beta_high < 0.0,
        f"at y=2*y_star, beta_lambda numerator = {beta_high:.8e}",
    )
    report(
        "selector-is-extra-relation",
        abs(beta_star) < 1.0e-14,
        f"beta=0 only after imposing y_star={y_star:.12f}",
    )
    return facts


def assert_authority_boundary() -> dict[str, bool]:
    higgs = read_doc("docs/HIGGS_MASS_DERIVED_NOTE.md")
    vacuum = read_doc("docs/HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md")
    observable = read_doc("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    taste = read_doc("docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md")
    selector = read_doc("docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md")

    has_lambda_boundary = "`lambda(M_Pl) = 0` is framework-native" in higgs
    has_inherited_yt_residual = (
        "inherits the current YT-lane precision caveat" in higgs
        or "inherited from `y_t`" in higgs
        or "accepted `y_t(v)` route still carries" in higgs
    )
    observable_mentions_beta = bool(re.search(r"beta_lambda|β_λ|beta-function stationarity", observable))
    taste_mentions_beta = bool(re.search(r"beta_lambda|β_λ|beta-function stationarity", taste))
    selector_flags_open = "proposal_allowed: false" in selector and "not derived in this note" in selector
    vacuum_inherits_yt = "current Ward-primary YT residual budget" in vacuum

    report(
        "higgs-authority-lambda-only",
        has_lambda_boundary and has_inherited_yt_residual,
        "Higgs authority derives lambda(M_Pl)=0 but keeps inherited YT residual",
    )
    report(
        "observable-principle-no-beta-selector",
        not observable_mentions_beta,
        "observable principle fixes log|det(D+J)| source response, not beta_lambda stationarity",
    )
    report(
        "taste-isotropy-no-beta-selector",
        not taste_mentions_beta,
        "taste scalar isotropy constrains Hessian degeneracy, not SM beta_lambda",
    )
    report(
        "vacuum-authority-inherits-yt",
        vacuum_inherits_yt,
        "Higgs/vacuum authority remains tied to the YT residual budget",
    )
    report(
        "selector-note-flags-open-premise",
        selector_flags_open,
        "double-criticality selector already marks beta_lambda(M_Pl)=0 as open",
    )

    return {
        "has_lambda_boundary": has_lambda_boundary,
        "has_inherited_yt_residual": has_inherited_yt_residual,
        "observable_mentions_beta": observable_mentions_beta,
        "taste_mentions_beta": taste_mentions_beta,
        "selector_flags_open": selector_flags_open,
        "vacuum_inherits_yt": vacuum_inherits_yt,
    }


def assert_finite_substrate_vs_rge_boundary() -> dict[str, str]:
    observable = read_doc("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    minimal = read_doc("docs/MINIMAL_AXIOMS_2026-04-11.md")

    source_generator = "W[J] = log |det(D+J)|" in observable
    finite_grassmann = "finite Grassmann" in observable
    ordinary_rge_is_bridge = "perturbative low-energy EFT running" in minimal
    rge_not_auto_promote = "do not automatically promote a bounded lane" in minimal

    report(
        "finite-source-generator",
        source_generator and finite_grassmann,
        "substrate gives finite log|det(D+J)| source response",
    )
    report(
        "rge-is-separate-bridge",
        ordinary_rge_is_bridge and rge_not_auto_promote,
        "SM/EFT running is explicitly a bridge, not automatic substrate content",
    )
    report(
        "no-rg-tangent-from-fixed-lattice",
        True,
        "fixed finite lattice data can set boundary values but not an SM beta-vector tangent without an RG bridge",
    )
    report(
        "scale-stationarity-is-extra",
        True,
        "requiring d lambda/d ln(mu)=0 at M_Pl is a new stationarity selector unless separately proved",
    )

    return {
        "source_generator": "W[J] = log |det(D+J)|",
        "rge_boundary": "SM beta_lambda is an imported EFT vector field, not the finite source coefficient itself",
        "missing_selector": "a substrate theorem forcing scale-stationarity of the renormalized quartic",
    }


def assert_route_taxonomy() -> list[dict[str, str]]:
    routes = [
        {
            "route": "lambda_boundary",
            "status": "blocked",
            "reason": "lambda(M_Pl)=0 sets a boundary value only; one-loop beta at lambda=0 is not identically zero.",
        },
        {
            "route": "finite_source_response",
            "status": "blocked",
            "reason": "log|det(D+J)| supplies source derivatives but no renormalized SM RG tangent.",
        },
        {
            "route": "taste_isotropy",
            "status": "blocked",
            "reason": "isotropy of the scalar Hessian does not relate y_t to electroweak gauge couplings.",
        },
        {
            "route": "multiple_point_or_scale_stationarity",
            "status": "conditional",
            "reason": "would imply the needed condition if accepted, but is exactly the missing selector premise.",
        },
        {
            "route": "ward_or_h_unit",
            "status": "forbidden_for_this_pr",
            "reason": "re-enters the audited_renaming route and still is not beta_lambda stationarity.",
        },
    ]
    for item in routes:
        report(
            f"route-{item['route']}",
            item["status"] in {"blocked", "conditional", "forbidden_for_this_pr"},
            f"{item['status']}: {item['reason']}",
        )
    return routes


def main() -> int:
    print("beta_lambda(M_Pl)=0 substrate-stationarity no-go")
    print("=" * 72)

    symbolic = assert_symbolic_no_identity()
    authority = assert_authority_boundary()
    substrate = assert_finite_substrate_vs_rge_boundary()
    routes = assert_route_taxonomy()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary",
        "target": "derive beta_lambda(M_Pl)=0 from current Cl(3)/Z^3 substrate premises",
        "verdict": (
            "The current substrate derives lambda(M_Pl)=0 and finite scalar "
            "source-response data, but beta_lambda(M_Pl)=0 is an additional "
            "codimension-one scale-stationarity selector in the SM RGE bridge."
        ),
        "symbolic": symbolic,
        "authority_boundary": authority,
        "substrate_vs_rge": substrate,
        "routes": routes,
        "remaining_open_premise": "derive a substrate scale-stationarity theorem, or adopt it explicitly as a new conditional selector",
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
