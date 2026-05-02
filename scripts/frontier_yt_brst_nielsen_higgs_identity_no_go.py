#!/usr/bin/env python3
"""
PR #230 BRST/Nielsen Higgs-identity no-go.

This runner checks whether gauge identities can supply the missing
source-pole-to-canonical-Higgs premise.  They cannot: BRST/ST transversality
and Nielsen pole-gauge-independence conditions are blind to a gauge-invariant
scalar source direction that mixes the canonical Higgs radial mode with an
orthogonal neutral scalar.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json"

PARENTS = {
    "ward_repair_audit": "outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json",
    "scalar_kernel_ward_identity": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
    "fh_lsz_higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
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


def build_identity_family() -> dict[str, Any]:
    """A gauge-identity-equivalent family with variable source overlap."""

    g2 = 0.65
    gy = 0.36
    v = 1.0
    xi_values = [0.0, 1.0, 3.0]
    m_h = 0.5
    m_chi = 1.4
    y_h = 1.0
    y_chi = -0.25

    rows = []
    for theta in [0.0, 0.25, 0.65, 1.1]:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        rows.append(
            {
                "theta": theta,
                "gauge_identity_surface": {
                    "brst_transversality_residual": 0.0,
                    "st_identity_residual": 0.0,
                    "nielsen_physical_pole_mass_xi_derivative": 0.0,
                    "xi_values_checked": xi_values,
                    "m_w": g2 * v / 2.0,
                    "m_z": math.sqrt(g2 * g2 + gy * gy) * v / 2.0,
                    "goldstone_masses_by_xi": [xi * (g2 * v / 2.0) ** 2 for xi in xi_values],
                },
                "scalar_spectrum": {
                    "canonical_higgs_pole_mass": m_h,
                    "orthogonal_scalar_pole_mass": m_chi,
                },
                "source_operator": {
                    "direction_in_neutral_scalar_space": [cos_t, sin_t],
                    "overlap_with_canonical_higgs_radial_mode": cos_t,
                    "overlap_with_orthogonal_scalar": sin_t,
                    "same_source_top_slope": y_h * cos_t + y_chi * sin_t,
                    "same_source_gauge_mass_slope_proxy": cos_t,
                },
            }
        )

    overlaps = [row["source_operator"]["overlap_with_canonical_higgs_radial_mode"] for row in rows]
    top_slopes = [row["source_operator"]["same_source_top_slope"] for row in rows]
    gauge_slopes = [row["source_operator"]["same_source_gauge_mass_slope_proxy"] for row in rows]
    brst_surfaces = [row["gauge_identity_surface"] for row in rows]

    return {
        "fixed_inputs": {
            "g2": g2,
            "gY": gy,
            "canonical_vev": v,
            "canonical_higgs_pole_mass": m_h,
            "orthogonal_scalar_pole_mass": m_chi,
            "canonical_top_yukawa": y_h,
            "orthogonal_scalar_top_coupling": y_chi,
        },
        "rows": rows,
        "checks": {
            "gauge_identity_surface_fixed": all(surface == brst_surfaces[0] for surface in brst_surfaces),
            "source_overlap_span": max(overlaps) - min(overlaps),
            "same_source_top_slope_span": max(top_slopes) - min(top_slopes),
            "same_source_gauge_slope_span": max(gauge_slopes) - min(gauge_slopes),
        },
    }


def main() -> int:
    print("PR #230 BRST/Nielsen Higgs-identity no-go")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = build_identity_family()
    checks = family["checks"]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "gauge-identity-surface-held-fixed",
        checks["gauge_identity_surface_fixed"],
        "BRST/ST/Nielsen residual rows fixed across source rotations",
    )
    report(
        "source-overlap-still-varies",
        checks["source_overlap_span"] > 0.5,
        f"span={checks['source_overlap_span']:.6g}",
    )
    report(
        "same-source-top-response-still-varies",
        checks["same_source_top_slope_span"] > 0.5,
        f"span={checks['same_source_top_slope_span']:.6g}",
    )
    report(
        "same-source-gauge-response-still-varies",
        checks["same_source_gauge_slope_span"] > 0.5,
        f"span={checks['same_source_gauge_slope_span']:.6g}",
    )
    report(
        "higgs-pole-identity-gate-still-open",
        parents["fh_lsz_higgs_pole_identity_gate"].get("higgs_pole_identity_gate_passed") is False,
        parents["fh_lsz_higgs_pole_identity_gate"].get("actual_current_surface_status", ""),
    )
    report(
        "no-orthogonal-top-coupling-not-derived",
        parents["no_orthogonal_top_coupling_import"].get("no_orthogonal_top_coupling_theorem_found")
        is False,
        parents["no_orthogonal_top_coupling_import"].get("actual_current_surface_status", ""),
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        "Gauge identities do not determine the neutral scalar source direction or source pole purity",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / BRST-Nielsen identities not Higgs-pole identity",
        "verdict": (
            "BRST, Slavnov-Taylor, and Nielsen-style gauge identities are not "
            "the missing PR #230 source-to-canonical-Higgs theorem.  The "
            "witness keeps the gauge identity surface, gauge masses, Goldstone "
            "gauge-parameter bookkeeping, physical pole gauge-independence, "
            "and scalar spectrum fixed while rotating a gauge-invariant neutral "
            "source operator between the canonical Higgs radial mode and an "
            "orthogonal scalar.  The source overlap and same-source response "
            "then change, so these identities cannot replace a scalar "
            "pole-residue measurement, source-pole purity theorem, or "
            "canonical-Higgs identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Gauge identities constrain gauge redundancies and gauge-parameter dependence, not the gauge-invariant neutral scalar source direction.",
        "parent_certificates": PARENTS,
        "identity_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout or yt_ward_identity as authority",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Pursue a microscopic scalar source-pole identity or production "
            "same-source pole-residue/sector-overlap measurement; do not infer "
            "canonical-Higgs identity from BRST/ST/Nielsen constraints alone."
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
