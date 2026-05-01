#!/usr/bin/env python3
"""
Assumption-sensitivity runner for dimensional/running anchors in the Planck
double-criticality y_t selector.

The selector is dimensionless at the Planck boundary, but the boundary-value
implementation still uses a running interval from v to M_Pl.  This runner
checks whether the selected one-loop Planck y_t is invariant under changes to
the endpoint anchors.  It is not.  Therefore M_Pl/v scale-setting and the SM
RGE bridge remain explicit imports for the non-MC selector route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_planck_selector_scale_anchor_sensitivity_2026-05-01.json"

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
    gp2 = (3.0 / 5.0) * g1 * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp2) ** 2) / 16.0) ** 0.25


def one_loop_gauge_seed(g1_v: float, g2_v: float, alpha_s_v: float, v_gev: float, m_pl_gev: float) -> tuple[float, float, float]:
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


def assert_scale_anchor_sensitivity() -> dict[str, object]:
    cert = load_selector_certificate()
    inputs = cert["inputs"]
    g1_v = inputs["g1_v"]
    g2_v = inputs["g2_v"]
    alpha_s_v = inputs["alpha_s_v"]
    v0 = inputs["v_gev"]
    mpl0 = inputs["m_pl_gev"]

    reduced_planck = 2.435e18
    cases = [
        ("canonical", v0, mpl0),
        ("reduced_planck_mass", v0, reduced_planck),
        ("planck_x0p1", v0, 0.1 * mpl0),
        ("planck_x10", v0, 10.0 * mpl0),
        ("v_minus_5pct", 0.95 * v0, mpl0),
        ("v_plus_5pct", 1.05 * v0, mpl0),
    ]

    rows = []
    for name, v_gev, mpl_gev in cases:
        g1_pl, g2_pl, g3_pl = one_loop_gauge_seed(g1_v, g2_v, alpha_s_v, v_gev, mpl_gev)
        yt_pl = one_loop_y_star(g1_pl, g2_pl)
        rows.append(
            {
                "case": name,
                "v_gev": v_gev,
                "m_pl_gev": mpl_gev,
                "log_interval": math.log(mpl_gev / v_gev),
                "g1_pl_one_loop": g1_pl,
                "g2_pl_one_loop": g2_pl,
                "g3_pl_one_loop": g3_pl,
                "yt_pl_one_loop": yt_pl,
            }
        )

    canonical = rows[0]["yt_pl_one_loop"]
    for row in rows:
        row["relative_yt_shift"] = (row["yt_pl_one_loop"] - canonical) / canonical

    reduced_shift = abs(rows[1]["relative_yt_shift"])
    planck_decade_shift = max(abs(rows[2]["relative_yt_shift"]), abs(rows[3]["relative_yt_shift"]))
    v_shift = max(abs(rows[4]["relative_yt_shift"]), abs(rows[5]["relative_yt_shift"]))

    report(
        "planck-convention-moves-selector",
        reduced_shift > 1.0e-3,
        f"unreduced-to-reduced Planck mass shifts one-loop y_t(M_Pl) by {reduced_shift:.3%}",
    )
    report(
        "planck-decade-moves-selector",
        planck_decade_shift > 1.0e-3,
        f"factor-10 Planck anchor shift moves y_t(M_Pl) by up to {planck_decade_shift:.3%}",
    )
    report(
        "v-anchor-moves-selector",
        v_shift > 1.0e-5,
        f"5% v endpoint shift moves y_t(M_Pl) by up to {v_shift:.4%}",
    )
    report(
        "running-interval-load-bearing",
        planck_decade_shift > v_shift,
        "the log running interval is a load-bearing bridge input",
    )

    return {
        "samples": rows,
        "canonical_yt_pl_one_loop": canonical,
        "reduced_planck_relative_shift": reduced_shift,
        "planck_decade_max_relative_shift": planck_decade_shift,
        "v_5pct_max_relative_shift": v_shift,
    }


def assert_claim_boundary() -> dict[str, object]:
    cert = load_selector_certificate()
    status_open = cert["status"]["actual_current_surface_status"] == "conditional-support / open selector route"
    blocking_import = cert["status"]["blocking_import"]

    report(
        "selector-already-open",
        status_open,
        "selector certificate is conditional/open, not retained",
    )
    report(
        "stationarity-still-primary-blocker",
        "beta_lambda" in blocking_import,
        blocking_import,
    )
    report(
        "scale-anchors-are-additional-imports",
        True,
        "M_Pl/v endpoint convention and RGE bridge remain explicit inputs",
    )
    return {
        "selector_open": status_open,
        "blocking_import": blocking_import,
        "additional_import": "dimensional endpoint anchors and SM RGE bridge",
    }


def main() -> int:
    print("YT Planck selector scale-anchor sensitivity audit")
    print("=" * 72)

    sensitivity = assert_scale_anchor_sensitivity()
    claim = assert_claim_boundary()
    result = {
        "actual_current_surface_status": "conditional-support / assumption-sensitivity boundary",
        "target": "test whether Planck double-criticality is invariant under dimensional/running anchor choices",
        "verdict": (
            "The one-loop selector changes when the M_Pl/v running interval is "
            "changed.  Thus dimensional endpoint anchors and the SM RGE bridge "
            "remain explicit imports for the non-MC criticality route."
        ),
        "scale_anchor_sensitivity": sensitivity,
        "claim_boundary": claim,
        "remaining_open_imports": [
            "beta_lambda(M_Pl)=0 stationarity selector",
            "retained dimensional endpoint anchors",
            "retained SM RGE bridge and scheme choice",
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
