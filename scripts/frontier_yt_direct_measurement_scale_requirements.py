#!/usr/bin/env python3
"""
Scale requirements for retained direct top-correlator closure.

The current pilot/mass-bracket route used the Sommer-scale conversion present
in the certificates, where one lattice mass unit is about 2.12 GeV.  A physical
top at that scale has am_t about 81, which is outside a useful relativistic
staggered-correlator extraction.  This runner computes the refinement required
for a direct physical top measurement and records the heavy-quark alternative.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASS_BRACKET = ROOT / "outputs" / "yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_direct_measurement_scale_requirements_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0

HBARC_GEV_FM = 0.1973269804
M_TOP_GEV = 172.56


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def main() -> int:
    print("YT direct measurement scale requirements")
    print("=" * 72)

    data = json.loads(MASS_BRACKET.read_text(encoding="utf-8"))
    conversion = data.get("scale_setting", {}).get("lattice_mass_unit_GeV")
    if conversion is None:
        # The mass-bracket certificate also records proxy GeV values in the
        # per-mass measurements.  Keep this fallback explicit.
        conversion = 2.119291769496

    current_a_inv_gev = float(conversion)
    current_a_fm = HBARC_GEV_FM / current_a_inv_gev
    current_am_top = M_TOP_GEV / current_a_inv_gev

    targets = []
    for am_target in [1.0, 0.5, 0.25]:
        required_a_inv = M_TOP_GEV / am_target
        required_a_fm = HBARC_GEV_FM / required_a_inv
        refinement = required_a_inv / current_a_inv_gev
        targets.append(
            {
                "target_am_top": am_target,
                "required_a_inv_GeV": required_a_inv,
                "required_a_fm": required_a_fm,
                "refinement_factor_vs_current": refinement,
                "physical_extent_fm_L12": 12 * required_a_fm,
                "physical_extent_fm_L16": 16 * required_a_fm,
                "physical_extent_fm_L24": 24 * required_a_fm,
            }
        )

    report("mass-bracket-certificate-present", MASS_BRACKET.exists(), str(MASS_BRACKET.relative_to(ROOT)))
    report("current-scale-conversion-positive", current_a_inv_gev > 0, f"a^-1={current_a_inv_gev:.12f} GeV")
    report("current-am-top-large", current_am_top > 50.0, f"am_top={current_am_top:.6f}")
    report("am-leq-one-needs-80x-refinement", targets[0]["refinement_factor_vs_current"] > 80.0, f"factor={targets[0]['refinement_factor_vs_current']:.3f}")
    report("am-leq-half-needs-160x-refinement", targets[1]["refinement_factor_vs_current"] > 160.0, f"factor={targets[1]['refinement_factor_vs_current']:.3f}")
    report("strict-current-scale-production-not-next", True, "production at current scale would certify cutoff obstruction, not physical top")
    report("retained-direct-route-requires-fine-scale-or-hqet", True, "need much finer lattice or heavy-quark/top-integrated effective treatment")

    result = {
        "actual_current_surface_status": "scale requirement / direct measurement route open",
        "verdict": (
            "At the current certificate scale, a physical top corresponds to "
            f"am_t = {current_am_top:.3f}.  A relativistic direct correlator with "
            "am_t <= 1 requires about an 81x finer inverse lattice spacing; "
            "am_t <= 0.5 requires about 163x.  Therefore the retained direct "
            "measurement route needs a fine-scale campaign or a heavy-quark/top-"
            "integrated effective treatment before strict production is meaningful."
        ),
        "current_scale": {
            "a_inv_GeV": current_a_inv_gev,
            "a_fm": current_a_fm,
            "am_top_physical": current_am_top,
        },
        "targets": targets,
        "closure_recommendation": [
            "do not spend production compute at the current scale for retained top closure",
            "choose fine-scale direct measurement if the framework allows scale variation/matching",
            "or build a heavy-top effective correlator/matching theorem and strict certificate",
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
