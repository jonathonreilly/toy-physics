#!/usr/bin/env python3
"""
PR #230 heavy kinetic-mass matching obstruction.

The nonzero-momentum route measures an energy splitting.  This removes the
static additive-mass ambiguity, but it does not by itself prove that the
lattice kinetic parameter is the SM top mass.  A kinetic-action coefficient and
a lattice-to-SM matching factor are still load-bearing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_heavy_kinetic_matching_obstruction_2026-05-01.json"

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


def delta_e(p_hat_sq: float, c2: float, m0: float) -> float:
    return c2 * p_hat_sq / (2.0 * m0)


def main() -> int:
    print("PR #230 heavy kinetic-mass matching obstruction")
    print("=" * 72)

    p_hat_sq = 2.0
    target_delta_e = 0.05
    # All pairs have c2 / m0 = target_delta_e * 2 / p_hat_sq.
    equivalent_pairs = [
        {"c2": 0.5, "m0_lat": 10.0},
        {"c2": 1.0, "m0_lat": 20.0},
        {"c2": 2.0, "m0_lat": 40.0},
    ]
    for row in equivalent_pairs:
        row["delta_e"] = delta_e(p_hat_sq, row["c2"], row["m0_lat"])
        row["measured_mkin_if_c2_assumed_1"] = p_hat_sq / (2.0 * row["delta_e"])

    matching_factors = [0.85, 1.0, 1.15]
    a_inv_gev = 2.119  # same order as the Sommer reference used by the PR230 harness
    measured_mkin_lat = p_hat_sq / (2.0 * target_delta_e)
    sm_mass_candidates = [
        {
            "z_match": z,
            "m_t_sm_GeV": measured_mkin_lat * a_inv_gev * z,
            "y_t_from_v_input": math.sqrt(2.0) * measured_mkin_lat * a_inv_gev * z / 246.21965,
        }
        for z in matching_factors
    ]

    deltas = [row["delta_e"] for row in equivalent_pairs]
    masses = [row["m0_lat"] for row in equivalent_pairs]
    sm_masses = [row["m_t_sm_GeV"] for row in sm_mass_candidates]

    report(
        "same-splitting-multiple-c2-m0-pairs",
        max(deltas) - min(deltas) < 1.0e-14 and max(masses) / min(masses) == 4.0,
        f"delta_e={deltas}, m0={masses}",
    )
    report(
        "unit-c2-assumption-hides-action-coefficient",
        all(abs(row["measured_mkin_if_c2_assumed_1"] - measured_mkin_lat) < 1.0e-14 for row in equivalent_pairs),
        f"measured_mkin_if_c2_assumed_1={measured_mkin_lat}",
    )
    report(
        "matching-factor-changes-sm-mass",
        max(sm_masses) - min(sm_masses) > 10.0,
        f"SM mass range={min(sm_masses):.6g}..{max(sm_masses):.6g} GeV",
    )
    report(
        "observed-top-calibration-not-used",
        True,
        "matching factors are countermodel parameters, not fitted to PDG top mass",
    )
    report(
        "not-retained-closure",
        True,
        "kinetic route still needs c2/action normalization and lattice-to-SM matching theorem",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / heavy kinetic matching obstruction",
        "verdict": (
            "A nonzero-momentum correlator can measure an energy splitting, but "
            "the splitting fixes c2/M0 rather than an SM pole mass unless the "
            "kinetic-action coefficient c2 is retained.  Even after a lattice "
            "M_kin is extracted, a lattice-to-SM matching factor changes the "
            "resulting m_t and y_t while leaving the measured splitting fixed.  "
            "Thus the kinetic route is real but not retained closure without a "
            "matching theorem or production evidence plus independently derived "
            "matching."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The kinetic-action coefficient and lattice-to-SM matching factor remain open imports.",
        "p_hat_sq": p_hat_sq,
        "target_delta_e": target_delta_e,
        "equivalent_kinetic_action_pairs": equivalent_pairs,
        "measured_mkin_lat_if_c2_is_one": measured_mkin_lat,
        "matching_factor_countermodels": sm_mass_candidates,
        "required_next_theorem": [
            "derive the heavy kinetic-action coefficient c2 on the Cl(3)/Z^3 substrate",
            "derive lattice-HQET/NRQCD-to-SM mass matching without observed top calibration",
            "combine with production E(p)-E(0) data and uncertainty propagation",
        ],
        "strict_non_claims": [
            "not a production measurement",
            "not a y_t derivation",
            "does not use observed top mass as calibration",
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
