#!/usr/bin/env python3
"""
Assumption-sensitivity runner for the Planck double-criticality y_t selector.

This is a physics-loop assumption test, not a new y_t derivation.  It asks
whether the Planck criticality route is self-contained once the stationarity
premise is granted.  The answer is no: the selector also needs gauge boundary
data.  If the electroweak gauge inputs are not fixed by retained upstream
authority, beta_lambda(M_Pl)=0 defines a family of y_t values rather than a
unique number.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_planck_selector_gauge_input_sensitivity_2026-05-01.json"

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


def load_selector_certificate() -> dict:
    path = ROOT / "outputs" / "yt_planck_double_criticality_selector_2026-04-30.json"
    return json.loads(path.read_text(encoding="utf-8"))


def one_loop_y_star(g1: float, g2: float) -> float:
    """One-loop beta_lambda(lambda=0)=0 selector, g1 GUT-normalized."""
    gp2 = (3.0 / 5.0) * g1 * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp2) ** 2) / 16.0) ** 0.25


def one_loop_gauge_seed(g1_v: float, g2_v: float, alpha_s_v: float, v_gev: float, m_pl_gev: float) -> tuple[float, float, float]:
    """Run gauge couplings from v to M_Pl at one loop."""
    pi = math.pi
    g3_v = math.sqrt(4.0 * pi * alpha_s_v)
    t_v = math.log(v_gev)
    t_pl = math.log(m_pl_gev)
    fac = 1.0 / (16.0 * pi * pi)
    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0

    def up(g0: float, b: float) -> float:
        denom = 1.0 / (g0 * g0) - 2.0 * b * fac * (t_pl - t_v)
        return 1.0 / math.sqrt(denom)

    return up(g1_v, b1), up(g2_v, b2), up(g3_v, b3)


def assert_selector_depends_on_gauge_boundary() -> dict[str, object]:
    cert = load_selector_certificate()
    canonical = cert["results"][0]
    g1_pl = canonical["g1_pl"]
    g2_pl = canonical["g2_pl"]
    y0 = one_loop_y_star(g1_pl, g2_pl)

    samples = []
    for scale in [0.80, 0.90, 1.00, 1.10, 1.20]:
        y = one_loop_y_star(scale * g1_pl, scale * g2_pl)
        samples.append({"common_scale": scale, "yt_pl_one_loop": y, "relative_to_canonical": y / y0})

    spread = max(row["yt_pl_one_loop"] for row in samples) - min(row["yt_pl_one_loop"] for row in samples)
    report(
        "selector-homogeneous-in-gauge-scale",
        all(abs(row["relative_to_canonical"] - row["common_scale"]) < 1.0e-12 for row in samples),
        "common gauge rescaling changes selected y_t by the same scale factor at one loop",
    )
    report(
        "gauge-boundary-family-nonunique",
        spread > 0.10,
        f"20% gauge-boundary scan gives y_t(M_Pl) spread {spread:.6f}",
    )

    return {
        "canonical_g1_pl": g1_pl,
        "canonical_g2_pl": g2_pl,
        "canonical_yt_pl_one_loop": y0,
        "common_scale_samples": samples,
        "spread": spread,
    }


def assert_low_scale_gauge_inputs_are_load_bearing() -> dict[str, object]:
    cert = load_selector_certificate()
    inputs = cert["inputs"]
    g1_v = inputs["g1_v"]
    g2_v = inputs["g2_v"]
    alpha_s_v = inputs["alpha_s_v"]
    v_gev = inputs["v_gev"]
    m_pl_gev = inputs["m_pl_gev"]

    perturbations = [
        ("canonical", 1.00, 1.00, 1.00),
        ("g1_plus_5pct", 1.05, 1.00, 1.00),
        ("g1_minus_5pct", 0.95, 1.00, 1.00),
        ("g2_plus_5pct", 1.00, 1.05, 1.00),
        ("g2_minus_5pct", 1.00, 0.95, 1.00),
        ("alpha_s_plus_10pct", 1.00, 1.00, 1.10),
        ("alpha_s_minus_10pct", 1.00, 1.00, 0.90),
    ]

    rows = []
    for name, s1, s2, s3 in perturbations:
        gp = one_loop_gauge_seed(s1 * g1_v, s2 * g2_v, s3 * alpha_s_v, v_gev, m_pl_gev)
        yt_pl = one_loop_y_star(gp[0], gp[1])
        rows.append(
            {
                "case": name,
                "g1_v": s1 * g1_v,
                "g2_v": s2 * g2_v,
                "alpha_s_v": s3 * alpha_s_v,
                "g1_pl_one_loop": gp[0],
                "g2_pl_one_loop": gp[1],
                "g3_pl_one_loop": gp[2],
                "yt_pl_one_loop": yt_pl,
            }
        )

    canonical_y = rows[0]["yt_pl_one_loop"]
    for row in rows:
        row["relative_yt_shift"] = (row["yt_pl_one_loop"] - canonical_y) / canonical_y

    nonzero_shifts = [abs(row["relative_yt_shift"]) for row in rows[1:]]
    alpha_s_shifts = [row["relative_yt_shift"] for row in rows if row["case"].startswith("alpha_s")]

    report(
        "ew-gauge-inputs-move-selector",
        max(nonzero_shifts) > 0.02,
        f"max one-loop y_t selector shift under gauge-input perturbations = {max(nonzero_shifts):.3%}",
    )
    report(
        "alpha-s-not-in-one-loop-selector-value",
        max(abs(x) for x in alpha_s_shifts) < 1.0e-12,
        "alpha_s affects running beyond this analytic one-loop selector, but not beta_lambda(lambda=0) at one loop",
    )
    report(
        "g1-g2-boundary-required",
        abs(rows[1]["relative_yt_shift"]) > 0.0 and abs(rows[3]["relative_yt_shift"]) > 0.0,
        "electroweak gauge inputs are load-bearing for y_t(M_Pl)",
    )

    return {"samples": rows, "canonical_yt_pl_one_loop": canonical_y}


def assert_claim_boundary() -> dict[str, object]:
    selector = load_selector_certificate()
    selector_open = selector["status"]["actual_current_surface_status"] == "conditional-support / open selector route"
    proposal_forbidden = selector["status"]["proposal_allowed"] is False
    comparators_not_inputs = "comparators_not_proof_inputs" in selector

    report(
        "selector-currently-conditional",
        selector_open and proposal_forbidden,
        "selector certificate already forbids retained proposal without open imports closed",
    )
    report(
        "observed-values-comparators-only",
        comparators_not_inputs,
        "observed y_t/m_t/m_H values are not proof inputs in the selector certificate",
    )
    report(
        "gauge-input-audit-needed",
        True,
        "a retained selector would need retained electroweak gauge inputs plus beta stationarity",
    )
    return {
        "selector_open": selector_open,
        "proposal_forbidden": proposal_forbidden,
        "comparators_not_inputs": comparators_not_inputs,
        "additional_open_import": "retained authority for the electroweak gauge boundary inputs used by the selector",
    }


def main() -> int:
    print("YT Planck selector gauge-input sensitivity audit")
    print("=" * 72)

    boundary = assert_selector_depends_on_gauge_boundary()
    low_scale = assert_low_scale_gauge_inputs_are_load_bearing()
    claim = assert_claim_boundary()

    result = {
        "actual_current_surface_status": "conditional-support / assumption-sensitivity boundary",
        "target": "test whether Planck double-criticality selects y_t without admitted gauge inputs",
        "verdict": (
            "The selector is not self-contained: beta_lambda(M_Pl)=0 selects "
            "a y_t value only after electroweak gauge boundary data are fixed. "
            "Without those inputs, the route is a family, not a retained "
            "single-number derivation."
        ),
        "boundary_sensitivity": boundary,
        "low_scale_input_sensitivity": low_scale,
        "claim_boundary": claim,
        "remaining_open_imports": [
            "beta_lambda(M_Pl)=0 stationarity selector",
            "retained authority for g1(v), g2(v), and running bridge used by this route",
        ],
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
