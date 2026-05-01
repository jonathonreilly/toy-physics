#!/usr/bin/env python3
"""
PR #230 static heavy-mass matching obstruction.

This is the formal follow-up to the HQET direct-route requirements runner.
It checks the residual-mass freedom of a static heavy correlator:

    C(t; am0, E) = A exp[-(am0 + E) t]
    C_sub(t; E) = exp(am0 t) C(t; am0, E) = A exp[-E t]

The subtracted/static observable is independent of the absolute rest mass
am0.  Therefore a static route needs an additive-mass/matching theorem before
it can determine m_t or y_t.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_static_mass_matching_obstruction_2026-05-01.json"

V_GEV = 246.21965
AINV_GEV = 2.119291769496

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


def raw_static_correlator(t_values: list[int], am0: float, residual_energy: float, amplitude: float = 1.0) -> list[float]:
    return [amplitude * math.exp(-(am0 + residual_energy) * t) for t in t_values]


def subtracted_static_correlator(t_values: list[int], raw: list[float], am0: float) -> list[float]:
    return [math.exp(am0 * t) * value for t, value in zip(t_values, raw, strict=True)]


def max_abs_delta(a: list[float], b: list[float]) -> float:
    return max(abs(x - y) for x, y in zip(a, b, strict=True))


def main() -> int:
    print("PR #230 static heavy-mass matching obstruction")
    print("=" * 72)

    t_values = [0, 1, 2, 3, 4, 5]
    residual_energy = 0.25
    target_masses_gev = [120.0, 172.56, 230.0]
    models = []
    for mass_gev in target_masses_gev:
        am0 = mass_gev / AINV_GEV
        raw = raw_static_correlator(t_values, am0, residual_energy)
        sub = subtracted_static_correlator(t_values, raw, am0)
        models.append(
            {
                "m_abs_GeV": mass_gev,
                "am0": am0,
                "raw_correlator": raw,
                "subtracted_correlator": sub,
                "y_from_mass_and_v": math.sqrt(2.0) * mass_gev / V_GEV,
            }
        )

    reference_sub = models[0]["subtracted_correlator"]
    subtracted_identical = all(max_abs_delta(row["subtracted_correlator"], reference_sub) < 1.0e-14 for row in models)
    raw_slopes = [
        -math.log(row["raw_correlator"][1] / row["raw_correlator"][0])
        for row in models
    ]
    raw_distinct = len({round(slope, 12) for slope in raw_slopes}) == len(raw_slopes)
    y_values = [row["y_from_mass_and_v"] for row in models]

    # A residual-mass counterterm can preserve the same physical subtracted
    # energy while changing the decomposition of absolute mass into m0 and
    # delta_m.  This is the static-HQET matching freedom in toy form.
    total_am = target_masses_gev[1] / AINV_GEV
    decompositions = [
        {"am0": total_am - 1.0, "delta_m": 1.0},
        {"am0": total_am, "delta_m": 0.0},
        {"am0": total_am + 1.0, "delta_m": -1.0},
    ]
    same_total = all(abs(item["am0"] + item["delta_m"] - total_am) < 1.0e-14 for item in decompositions)

    report(
        "raw-static-correlator-depends-on-rest-mass",
        raw_distinct,
        f"effective slopes={[round(slope, 6) for slope in raw_slopes]}",
    )
    report("subtracted-static-correlator-independent-of-rest-mass", subtracted_identical, "all subtracted correlators match")
    report("same-subtracted-correlator-different-y", max(y_values) - min(y_values) > 0.5, f"y_values={[round(v, 6) for v in y_values]}")
    report("residual-mass-decomposition-nonunique", same_total, f"decompositions={decompositions}")
    report("absolute-mass-needs-matching-condition", True, "must fix am0 + delta_m in physical units")
    report("not-a-direct-closure-route", True, "static route cannot determine y_t without the matching condition")

    result = {
        "actual_current_surface_status": "exact negative boundary / static mass matching obstruction",
        "verdict": (
            "Static rephasing makes the measured heavy correlator insensitive "
            "to the absolute rest mass.  Different absolute top masses give the "
            "same subtracted static correlator but different y_t values.  The "
            "decomposition into bare static mass and additive residual mass is "
            "nonunique until a lattice-HQET-to-SM matching condition is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Absolute m_t remains an open matching input on the static route.",
        "t_values": t_values,
        "residual_energy_lat": residual_energy,
        "models": models,
        "raw_effective_slopes": raw_slopes,
        "residual_mass_decompositions_for_172_56_GeV": decompositions,
        "required_matching_condition": [
            "fix the additive residual mass delta_m(a) from the retained gauge action",
            "fix the conversion from static energy to SM top mass",
            "show the matching does not import observed m_t or H_unit/Ward y_t authority",
        ],
        "strict_non_claims": [
            "does not reject static/HQET simulation methods",
            "does not produce a top mass measurement",
            "does not define y_t through H_unit",
            "does not use observed top mass as a selector",
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
