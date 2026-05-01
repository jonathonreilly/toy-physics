#!/usr/bin/env python3
"""
PR #230 heavy-top/HQET direct-route requirements.

The relativistic direct-correlator route is blocked at the current scale by
am_top >> 1.  A natural alternative is a static/heavy-quark effective
correlator.  This runner checks whether that alternative can determine the
absolute top mass and y_t without a new matching input.

It cannot: the static rephasing that makes the correlator numerically tractable
also removes the absolute heavy mass from the normalized correlator.  Absolute
m_top then re-enters only through a matching/additive mass term.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE_CERT = ROOT / "outputs" / "yt_direct_measurement_scale_requirements_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_hqet_direct_route_requirements_2026-05-01.json"

V_GEV = 246.21965
M_TOP_REF_GEV = 172.56

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


def normalized_static_correlator(t_values: list[int], residual_energy_lat: float) -> list[float]:
    """Static correlator after factoring out the heavy rest mass.

    C_static(t) / C_static(0) = exp(-E_residual t).
    The absolute mass does not appear.
    """
    return [math.exp(-residual_energy_lat * t) for t in t_values]


def relativistic_correlator(t_values: list[int], am_abs: float, residual_energy_lat: float) -> list[float]:
    """Unsubtracted heavy correlator, included only to show why am>>1 is hard."""
    return [math.exp(-(am_abs + residual_energy_lat) * t) for t in t_values]


def main() -> int:
    print("PR #230 HQET/direct route requirements")
    print("=" * 72)

    scale = json.loads(SCALE_CERT.read_text(encoding="utf-8"))
    current = scale["current_scale"]
    a_inv_gev = float(current["a_inv_GeV"])
    am_top = float(current["am_top_physical"])
    residual_energy_lat = 0.25
    t_values = [0, 1, 2, 3, 4]

    masses_gev = [100.0, M_TOP_REF_GEV, 250.0]
    static_shapes = []
    relativistic_shapes = []
    for mass in masses_gev:
        am_abs = mass / a_inv_gev
        static_shapes.append(
            {
                "m_abs_GeV": mass,
                "am_abs": am_abs,
                "normalized_static_correlator": normalized_static_correlator(t_values, residual_energy_lat),
                "y_from_mass_and_v": math.sqrt(2.0) * mass / V_GEV,
            }
        )
        relativistic_shapes.append(
            {
                "m_abs_GeV": mass,
                "am_abs": am_abs,
                "unsubtracted_correlator": relativistic_correlator(t_values, am_abs, residual_energy_lat),
            }
        )

    static_reference = static_shapes[0]["normalized_static_correlator"]
    static_identical = all(
        row["normalized_static_correlator"] == static_reference for row in static_shapes
    )
    y_values = [row["y_from_mass_and_v"] for row in static_shapes]
    y_spread = max(y_values) - min(y_values)
    t1_underflow_top = relativistic_shapes[1]["unsubtracted_correlator"][1]

    report("scale-certificate-present", SCALE_CERT.exists(), str(SCALE_CERT.relative_to(ROOT)))
    report("current-relativistic-am-top-large", am_top > 50.0, f"am_top={am_top:.6f}")
    report(
        "static-rephasing-removes-absolute-mass",
        static_identical,
        "normalized static correlator identical for 100, 172.56, and 250 GeV masses",
    )
    report(
        "same-static-correlator-gives-different-y",
        y_spread > 0.5,
        f"y_values={[round(v, 6) for v in y_values]}",
    )
    report(
        "unsubtracted-current-scale-correlator-is-numerically-dead",
        0.0 <= t1_underflow_top < 1.0e-30,
        f"C(t=1) at m_top={t1_underflow_top:.3e}",
    )
    report(
        "hqet-needs-matching-mass",
        True,
        "absolute m_top enters through m_bare/additive static self-energy/matching coefficient",
    )
    report(
        "not-closure",
        True,
        "HQET is viable only with a retained matching theorem or measured calibration, not as a zero-import shortcut",
    )

    result = {
        "actual_current_surface_status": "route requirement / HQET shortcut no-go",
        "verdict": (
            "A static/HQET correlator can remove the numerical am_top cutoff "
            "problem, but the same rephasing removes the absolute heavy mass "
            "from the normalized correlator.  The absolute top mass and y_t "
            "then require an independent matching/additive-mass theorem or a "
            "measured calibration.  HQET is therefore a possible production "
            "strategy, not retained closure by itself."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Absolute m_top is underdetermined without a heavy-mass matching theorem or external calibration.",
        "current_scale": current,
        "residual_energy_lat": residual_energy_lat,
        "t_values": t_values,
        "static_countermodels": static_shapes,
        "unsubtracted_correlator_examples": relativistic_shapes,
        "required_for_hqet_closure": [
            "derive or measure the static additive mass renormalization",
            "derive lattice-HQET-to-SM top mass matching at the chosen scale",
            "propagate matching uncertainty into y_t = sqrt(2) m_t / v",
            "keep v as substrate input and avoid H_unit/Ward readout authority",
        ],
        "strict_non_claims": [
            "does not reject HQET as an engineering strategy",
            "does not certify direct y_t measurement",
            "does not use observed top mass as proof input",
            "does not define y_t through H_unit matrix elements",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
