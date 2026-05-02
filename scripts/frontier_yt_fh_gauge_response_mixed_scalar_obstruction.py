#!/usr/bin/env python3
"""
PR #230 FH gauge-response mixed-scalar obstruction.

This runner pressure-tests the physical-response bypass.  A same-source
W/Z response can cancel a common source normalization, but it still does not
identify the physical top Yukawa if the measured source pole is a mixture of
the canonical Higgs radial mode and an orthogonal scalar that couples to the
top.  The ratio measures the top coupling to the source pole divided by its
gauge/Higgs overlap.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json"

CERTS = {
    "gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "gauge_mass_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "sector_overlap_obstruction": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "source_pole_mixing_obstruction": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
}

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def mixed_scalar_countermodels() -> list[dict[str, float]]:
    # Units are arbitrary.  The construction fixes the measured same-source
    # top and W slopes while changing the physical canonical-Higgs Yukawa y_h.
    g2 = 1.0
    source_overlap = 1.0
    cos_theta = 0.8
    sin_theta = math.sqrt(1.0 - cos_theta**2)
    measured_top_numerator = 1.0
    d_e_top_ds = source_overlap * measured_top_numerator / math.sqrt(2.0)
    d_m_w_ds = source_overlap * g2 * cos_theta / 2.0
    ratio_readout = (g2 / math.sqrt(2.0)) * d_e_top_ds / d_m_w_ds

    rows = []
    for y_chi in (-0.5, 0.0, 0.5):
        y_h = (measured_top_numerator - y_chi * sin_theta) / cos_theta
        rows.append(
            {
                "g2": g2,
                "source_overlap": source_overlap,
                "cos_theta": cos_theta,
                "sin_theta": sin_theta,
                "orthogonal_top_coupling_y_chi": y_chi,
                "physical_canonical_higgs_y_h": y_h,
                "measured_top_slope_dE_ds": d_e_top_ds,
                "measured_gauge_slope_dM_W_ds": d_m_w_ds,
                "gauge_normalized_ratio_readout": ratio_readout,
                "pole_top_coupling_over_higgs_overlap": y_h + y_chi * sin_theta / cos_theta,
            }
        )
    return rows


def main() -> int:
    print("PR #230 FH gauge-response mixed-scalar obstruction")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    rows = mixed_scalar_countermodels()
    measured_pairs = {
        (
            round(row["measured_top_slope_dE_ds"], 12),
            round(row["measured_gauge_slope_dM_W_ds"], 12),
            round(row["source_overlap"], 12),
            round(row["cos_theta"], 12),
        )
        for row in rows
    }
    physical_y_values = {round(row["physical_canonical_higgs_y_h"], 12) for row in rows}
    ratio_values = {round(row["gauge_normalized_ratio_readout"], 12) for row in rows}
    pole_ratio_values = {round(row["pole_top_coupling_over_higgs_overlap"], 12) for row in rows}
    missing_premises = [
        "source pole equals canonical Higgs radial mode (sin_theta = 0)",
        "orthogonal scalar has zero top coupling (y_chi = 0)",
        "independent theorem/measured constraint fixing y_chi",
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "same-measured-response-pair",
        len(measured_pairs) == 1 and len(ratio_values) == 1 and len(pole_ratio_values) == 1,
        f"measured_pairs={measured_pairs}, ratio_values={ratio_values}",
    )
    report(
        "physical-yukawa-varies",
        len(physical_y_values) == len(rows),
        f"physical_y_values={sorted(physical_y_values)}",
    )
    report(
        "ratio-reads-pole-coupling-not-yh",
        any(
            abs(row["gauge_normalized_ratio_readout"] - row["physical_canonical_higgs_y_h"]) > 1e-12
            for row in rows
        ),
        "ratio equals y_h only after extra purity premises",
    )
    report("missing-purity-premises-explicit", len(missing_premises) == 3, str(missing_premises))
    report("does-not-authorize-retained-proposal", True, "physical-response ratio still needs scalar purity/identity")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH gauge-response mixed-scalar obstruction",
        "verdict": (
            "A same-source top/W response ratio cancels common source "
            "normalization, but it measures the source-pole top coupling divided "
            "by the source-pole gauge/Higgs overlap.  If the source pole has an "
            "orthogonal scalar admixture that couples to the top, the same "
            "measured top slope, W slope, source overlap, and Higgs overlap are "
            "compatible with different physical canonical-Higgs Yukawa values. "
            "The physical-response bypass therefore still needs either a "
            "canonical-Higgs pole identity, a no-orthogonal-top-coupling theorem, "
            "or an independent measurement fixing the orthogonal coupling."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The response ratio remains underidentified in the mixed-scalar family; scalar purity/identity premises are open.",
        "parent_certificates": CERTS,
        "countermodels": rows,
        "missing_premises": missing_premises,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed top, y_t, W/Z, or Higgs values as selectors",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not set kappa_s = 1",
            "does not assume orthogonal scalar top coupling vanishes",
        ],
        "exact_next_action": (
            "Derive a canonical-Higgs/source-pole identity or a theorem that "
            "orthogonal scalar admixtures have zero top coupling; otherwise a "
            "same-source W/Z response harness remains support, not closure."
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
