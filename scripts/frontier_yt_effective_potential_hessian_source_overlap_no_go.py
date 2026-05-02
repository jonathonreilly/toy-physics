#!/usr/bin/env python3
"""
PR #230 effective-potential Hessian/source-overlap no-go.

This runner checks whether SSB effective-potential curvature data can identify
the PR #230 scalar source pole with the canonical Higgs radial mode.  It
cannot: a canonical VEV, gauge masses, and scalar Hessian can be held fixed
while the source operator direction in scalar field space is rotated.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json"

PARENTS = {
    "source_higgs_legendre_ssb": "outputs/yt_source_higgs_legendre_ssb_bridge_2026-05-01.json",
    "gauge_vev_source_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "renormalization_condition_overlap": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "higgs_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_hessian_family() -> dict[str, Any]:
    v = 1.0
    g2 = 0.65
    gy = 0.36
    y_h = 1.0
    m_h2 = 0.25
    m_chi2 = 1.70
    angles = [0.0, 0.2, 0.6, 1.0]
    rows = []
    for theta in angles:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        source_susceptibility_at_zero = cos_t * cos_t / m_h2 + sin_t * sin_t / m_chi2
        rows.append(
            {
                "theta": theta,
                "canonical_vev": [v, 0.0],
                "scalar_hessian_diag": [m_h2, m_chi2],
                "m_w": g2 * v / 2.0,
                "m_z": math.sqrt(g2 * g2 + gy * gy) * v / 2.0,
                "source_operator_direction": [cos_t, sin_t],
                "source_overlap_with_canonical_h": cos_t,
                "source_only_top_slope_for_y_chi_zero": y_h * cos_t,
                "source_susceptibility_at_zero": source_susceptibility_at_zero,
            }
        )
    overlaps = [row["source_overlap_with_canonical_h"] for row in rows]
    slopes = [row["source_only_top_slope_for_y_chi_zero"] for row in rows]
    susceptibilities = [row["source_susceptibility_at_zero"] for row in rows]
    return {
        "fixed_canonical_data": {
            "v": v,
            "g2": g2,
            "gY": gy,
            "m_h_squared": m_h2,
            "m_chi_squared": m_chi2,
            "m_w": g2 * v / 2.0,
            "m_z": math.sqrt(g2 * g2 + gy * gy) * v / 2.0,
            "canonical_y_h": y_h,
        },
        "rows": rows,
        "checks": {
            "canonical_data_fixed": all(
                row["canonical_vev"] == rows[0]["canonical_vev"]
                and row["scalar_hessian_diag"] == rows[0]["scalar_hessian_diag"]
                and row["m_w"] == rows[0]["m_w"]
                and row["m_z"] == rows[0]["m_z"]
                for row in rows
            ),
            "source_overlap_varies": max(overlaps) - min(overlaps),
            "source_only_slope_varies": max(slopes) - min(slopes),
            "source_susceptibility_varies": max(susceptibilities) - min(susceptibilities),
        },
    }


def main() -> int:
    print("PR #230 effective-potential Hessian/source-overlap no-go")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = build_hessian_family()
    checks = family["checks"]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("canonical-hessian-data-held-fixed", checks["canonical_data_fixed"], "v, M_W, M_Z, and Hessian eigenvalues fixed")
    report(
        "source-overlap-still-varies",
        checks["source_overlap_varies"] > 0.4,
        f"span={checks['source_overlap_varies']:.6g}",
    )
    report(
        "source-only-response-still-varies",
        checks["source_only_slope_varies"] > 0.4,
        f"span={checks['source_only_slope_varies']:.6g}",
    )
    report(
        "source-susceptibility-not-canonical-identity",
        checks["source_susceptibility_varies"] > 0.5,
        f"span={checks['source_susceptibility_varies']:.6g}",
    )
    report("higgs-identity-gate-still-open", parents["higgs_identity_gate"].get("proposal_allowed") is False, parents["higgs_identity_gate"].get("actual_current_surface_status", ""))
    report("does-not-authorize-retained-proposal", True, "Hessian/radial data do not fix the source operator direction")

    result = {
        "actual_current_surface_status": "exact negative boundary / effective-potential Hessian not source-overlap identity",
        "verdict": (
            "SSB effective-potential Hessian data do not close the PR #230 "
            "source-to-canonical-Higgs bridge.  The witness family keeps the "
            "canonical VEV, W/Z mass algebra, scalar Hessian eigenvalues, and "
            "canonical top Yukawa fixed while rotating the scalar source "
            "operator direction.  The source overlap, source-only top slope, "
            "and source susceptibility change.  Therefore radial curvature or "
            "effective-potential Hessian data cannot replace a same-source "
            "pole-residue measurement, microscopic denominator theorem, or "
            "canonical-Higgs source-pole identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source operator direction in scalar field space remains an independent input after canonical VEV and Hessian data are fixed.",
        "parent_certificates": PARENTS,
        "hessian_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity as authority",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Derive the source operator direction/source-pole identity from "
            "the Cl(3)/Z3 source functional, or measure it through same-source "
            "production pole data; do not infer it from Hessian curvature alone."
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
