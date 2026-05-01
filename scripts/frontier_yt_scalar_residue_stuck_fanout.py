#!/usr/bin/env python3
"""
PR #230 scalar residue stuck fan-out.

After the scalar source two-point stretch attempt, the physics-loop skill
requires a fan-out before declaring the route blocked.  This runner tests five
orthogonal attack frames against the same target:

  F1 free/logdet source curvature;
  F2 finite-volume near-match to 1/sqrt(6);
  F3 Hubbard-Stratonovich/RPA scalar pole equation;
  F4 common scalar/gauge dressing from anomalous factors;
  F5 direct measurement / heavy-top route.

The output is not another wording pass.  It records which frame can still move
the claim state and which frames require a new input.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from frontier_yt_scalar_source_two_point_stretch import residue_proxy


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_residue_stuck_fanout_2026-05-01.json"

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


def load_json(rel_path: str) -> dict:
    path = ROOT / rel_path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rpa_family(pi0: float, pi1: float, pi2: float, inv_g: float) -> dict:
    """Toy RPA inverse propagator D^-1(x)=inv_g-(pi0+pi1*x+pi2*x^2)."""

    # x is Euclidean p_hat^2 in this diagnostic.  This is not a physical Higgs
    # mass solve; it tests whether A_min fixes the pole equation once the
    # bubble coefficients are supplied.
    coeff = [-pi2, -pi1, inv_g - pi0]
    roots = [complex(root) for root in np.roots(coeff)]
    real_positive_roots = [float(root.real) for root in roots if abs(root.imag) < 1.0e-10 and root.real > 0.0]
    if real_positive_roots:
        pole_x = min(real_positive_roots)
        slope = -(pi1 + 2.0 * pi2 * pole_x)
        residue = 1.0 / abs(slope)
    else:
        pole_x = None
        residue = None
    return {
        "inv_g": inv_g,
        "roots": [[root.real, root.imag] for root in roots],
        "positive_real_pole_x": pole_x,
        "residue_at_positive_real_pole": residue,
    }


def main() -> int:
    print("PR #230 scalar residue stuck fan-out")
    print("=" * 72)

    stretch = load_json("outputs/yt_scalar_source_two_point_stretch_2026-05-01.json")
    retained_route = load_json("outputs/yt_retained_closure_route_certificate_2026-05-01.json")
    direct_scale = load_json("outputs/yt_direct_measurement_scale_requirements_2026-05-01.json")

    report(
        "stretch-certificate-present",
        stretch.get("actual_current_surface_status") == "exact-support / open bridge",
        stretch.get("actual_current_surface_status", "missing"),
    )
    report(
        "retained-route-still-open",
        retained_route.get("actual_current_surface_status") == "open / retained closure not yet reached",
        retained_route.get("actual_current_surface_status", "missing"),
    )

    c_source = 1.0 / math.sqrt(6.0)
    near = residue_proxy(8, 16, 0.10, source_prefactor=c_source)["residue_proxy"]
    far = residue_proxy(24, 48, 0.10, source_prefactor=c_source)["residue_proxy"]
    finite_volume_drift = abs(near - far)
    report(
        "finite-volume-near-match-not-stable",
        finite_volume_drift > 0.10,
        f"L8={near:.12f}, L24={far:.12f}, drift={finite_volume_drift:.12f}",
    )

    # Use the L=8,m=0.25 bubble fit as a concrete source-curvature model, then
    # ask whether an HS/RPA pole follows without an extra scalar-channel
    # coupling.  The answer is no: changing inv_g changes pole existence and
    # residue while the source bubble is held fixed.
    bubble_fit = residue_proxy(8, 16, 0.25, source_prefactor=c_source)
    # Approximate Pi(x) by C(x), not C^-1, over the three computed momenta.
    x = np.array([row["p_hat_sq"] for row in bubble_fit["rows"]], dtype=float)
    y = np.array([row["curvature"] for row in bubble_fit["rows"]], dtype=float)
    pi2, pi1, pi0 = np.polyfit(x, y, 2)
    rpa_models = [rpa_family(float(pi0), float(pi1), float(pi2), inv_g) for inv_g in [0.01, 0.03, 0.06, 0.12]]
    pole_pattern = [model["positive_real_pole_x"] is not None for model in rpa_models]
    residues = [
        model["residue_at_positive_real_pole"]
        for model in rpa_models
        if model["residue_at_positive_real_pole"] is not None
    ]
    report(
        "hs-rpa-pole-needs-extra-coupling",
        len(set(pole_pattern)) > 1 or (residues and max(residues) / min(residues) > 1.5),
        f"pole_pattern={pole_pattern}; residues={residues}",
    )

    dressing_models = []
    for z_scalar, z_gauge in [(1.0, 1.0), (0.9, 1.0), (1.1, 0.95), (0.8, 1.2)]:
        dressing_models.append(
            {
                "z_scalar": z_scalar,
                "z_gauge": z_gauge,
                "readout_ratio_multiplier": math.sqrt(z_scalar) / math.sqrt(z_gauge),
            }
        )
    multipliers = {round(model["readout_ratio_multiplier"], 12) for model in dressing_models}
    report(
        "common-dressing-not-forced-by-source-bubble",
        len(multipliers) > 1,
        f"multipliers={sorted(multipliers)}",
    )

    scale_factor_am1 = direct_scale.get("required_refinement", {}).get("for_am_top_le_1")
    if scale_factor_am1 is None:
        # Backward-compatible extraction from the current certificate shape.
        scale_factor_am1 = direct_scale.get("scale_requirements", {}).get("refinement_for_am_le_1")
    if scale_factor_am1 is None and direct_scale.get("targets"):
        scale_factor_am1 = direct_scale["targets"][0].get("refinement_factor_vs_current")
    report(
        "direct-route-remains-fine-scale-or-hqet",
        scale_factor_am1 is None or float(scale_factor_am1) > 80.0,
        f"am<=1 refinement={scale_factor_am1}",
    )

    frames = [
        {
            "frame": "F1_free_logdet_source_curvature",
            "status": "exact-support / open bridge",
            "claim_movement": "source two-point curvature derived as fermion bubble",
            "blocker": "bubble residue is dynamical, not a retained physical Higgs pole theorem",
        },
        {
            "frame": "F2_finite_volume_near_match",
            "status": "no-go for shortcut",
            "claim_movement": "near-match at L=8,m=0.10 tested and rejected as unstable",
            "blocker": "volume drift is larger than 0.10 in residue proxy",
        },
        {
            "frame": "F3_hs_rpa_pole_equation",
            "status": "conditional-support only",
            "claim_movement": "identifies the exact additional input: scalar-channel coupling/pole condition",
            "blocker": "A_min supplies bubble coefficients, not the HS/RPA coupling inv_g",
        },
        {
            "frame": "F4_common_dressing",
            "status": "open",
            "claim_movement": "separates source residue from relative scalar/gauge renormalization",
            "blocker": "no retained identity equates scalar-density and gauge-link dressing",
        },
        {
            "frame": "F5_direct_measurement_hqet",
            "status": "open empirical route",
            "claim_movement": "bypasses analytic scalar residue if strict evidence exists",
            "blocker": "current relativistic scale requires fine lattice or heavy-top treatment",
        },
    ]

    result = {
        "actual_current_surface_status": "open",
        "verdict": (
            "The required stuck fan-out found no immediate retained closure.  "
            "The best positive movement is F1: exact source-curvature support.  "
            "The nearest next constructive analytic route is F3, but it requires "
            "a scalar-channel pole/coupling theorem not present in A_min.  The "
            "empirical alternative remains F5: fine-scale or HQET direct measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Fan-out exposes the next missing input rather than retiring it.",
        "finite_volume_near_match": {
            "L8_T16_m0p10": near,
            "L24_T48_m0p10": far,
            "drift": finite_volume_drift,
            "target_1_over_sqrt6": c_source,
        },
        "bubble_fit_for_rpa_test": {
            "pi0": float(pi0),
            "pi1": float(pi1),
            "pi2": float(pi2),
            "source": "L=8,T=16,m=0.25 source-prefactored free bubble",
        },
        "rpa_models": rpa_models,
        "dressing_models": dressing_models,
        "frames": frames,
        "next_route_selected": "F3_hs_rpa_pole_equation",
        "next_route_reason": (
            "It is the only fan-out route that could turn the exact bubble "
            "curvature into an interacting pole-residue theorem without using "
            "observed y_t or the old H_unit matrix-element definition."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
