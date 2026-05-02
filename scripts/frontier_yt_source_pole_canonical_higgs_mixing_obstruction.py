#!/usr/bin/env python3
"""
PR #230 source-pole/canonical-Higgs mixing obstruction.

The same-source FH/LSZ readout can determine the top coupling to the scalar
pole created by the substrate source.  It becomes physical y_t only after that
source pole is identified with the canonical Higgs radial mode used by v.  This
runner records the remaining mixing obstruction.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json"

CERTS = {
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "same_source_scalar_two_point": "outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json",
    "fh_lsz_invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "gauge_vev_source_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "scalar_denominator": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "kprime": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def mixing_family() -> list[dict[str, float]]:
    source_pole_y_readout = 0.93
    g2 = 0.65
    v = 1.0
    rows = []
    for theta in (0.0, 0.35, 0.7):
        canonical_overlap = math.cos(theta)
        orthogonal_overlap = math.sin(theta)
        canonical_y_t = source_pole_y_readout / canonical_overlap
        rows.append(
            {
                "theta_rad": theta,
                "source_pole_residue": 1.0,
                "canonical_higgs_overlap_cos_theta": canonical_overlap,
                "orthogonal_scalar_overlap_sin_theta": orthogonal_overlap,
                "same_source_fh_lsz_y_readout": source_pole_y_readout,
                "canonical_y_t_if_top_couples_only_to_h": canonical_y_t,
                "static_v": v,
                "static_M_W": g2 * v / 2.0,
                "g2": g2,
            }
        )
    return rows


def main() -> int:
    print("PR #230 source-pole/canonical-Higgs mixing obstruction")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    rows = mixing_family()

    same_source_support = (
        "invariant readout" in status(certs["fh_lsz_invariant_readout"])
        and certs["fh_lsz_invariant_readout"].get("proposal_allowed") is False
        and "same-source scalar two-point" in status(certs["same_source_scalar_two_point"])
    )
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(certs["fh_lsz_higgs_pole_identity"])
        and certs["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    sector_identity_blocked = (
        "sector-overlap identity obstruction" in status(certs["same_source_sector_overlap_identity"])
        and certs["same_source_sector_overlap_identity"].get("sector_overlap_identity_gate_passed") is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    canonical_import_blocked = (
        "canonical scalar normalization import audit" in status(certs["canonical_scalar_import"])
        and certs["canonical_scalar_import"].get("proposal_allowed") is False
    )
    static_vev_shortcut_blocked = (
        "gauge-VEV source-overlap no-go" in status(certs["gauge_vev_source_overlap"])
        and certs["gauge_vev_source_overlap"].get("proposal_allowed") is False
    )
    denominator_stack_open = (
        "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator"])
        and "K-prime closure attempt blocked" in status(certs["kprime"])
    )

    y_values = [row["canonical_y_t_if_top_couples_only_to_h"] for row in rows]
    readouts = {round(row["same_source_fh_lsz_y_readout"], 12) for row in rows}
    static_w_values = {round(row["static_M_W"], 12) for row in rows}
    mixing_changes_canonical_y = len(readouts) == 1 and len(static_w_values) == 1 and max(y_values) - min(y_values) > 0.25
    identity_gate_passed = False

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-source-pole-readout-support-present", same_source_support, "FH/LSZ invariant and C_ss primitive loaded")
    report("higgs-pole-identity-still-blocked", higgs_identity_blocked, status(certs["fh_lsz_higgs_pole_identity"]))
    report("sector-overlap-identity-still-blocked", sector_identity_blocked, status(certs["same_source_sector_overlap_identity"]))
    report("source-to-higgs-and-canonical-imports-blocked", source_to_higgs_blocked and canonical_import_blocked, "source bridge remains open")
    report("static-vev-shortcut-blocked", static_vev_shortcut_blocked, status(certs["gauge_vev_source_overlap"]))
    report("denominator-stack-still-open", denominator_stack_open, "D'(pole) and K'(pole) not closed")
    report("mixing-family-underdetermines-canonical-y", mixing_changes_canonical_y, f"canonical_y_values={y_values}")
    report("source-pole-canonical-identity-not-derived", not identity_gate_passed, "cos(theta)=1 not derived")
    report("mixing-obstruction-not-closure", True, "no retained proposal allowed")

    result = {
        "actual_current_surface_status": "exact negative boundary / source-pole canonical-Higgs mixing obstruction",
        "verdict": (
            "A same-source FH/LSZ measurement can determine the top coupling to "
            "the scalar pole created by the substrate source.  It still does "
            "not prove that this source pole is the canonical Higgs radial mode "
            "whose VEV defines v.  In a two-scalar mixing family, the source "
            "pole residue and same-source y readout can be held fixed while the "
            "canonical Higgs overlap cos(theta) changes; the canonical y_t then "
            "changes as y_source/cos(theta).  Therefore the current route needs "
            "a source-pole-to-canonical-Higgs identity theorem, an equivalent "
            "sector-overlap measurement, or direct production evidence with a "
            "certified pole identity."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source scalar pole is not certified as the canonical Higgs radial mode.",
        "source_pole_canonical_identity_gate_passed": identity_gate_passed,
        "mixing_family": rows,
        "parent_certificates": CERTS,
        "required_identity": [
            "prove the source pole has unit overlap with the canonical Higgs radial mode",
            "exclude or measure orthogonal scalar admixture in the source pole",
            "derive the same identity from the Cl(3)/Z3 source functional or a production response certificate",
            "combine it with the isolated-pole derivative D'(pole) without forbidden normalization imports",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set cos(theta) = 1",
            "does not set kappa_s = 1",
            "does not use static v, observed top mass, observed y_t, or observed W/Z masses as proof selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Derive or measure the source-pole-to-canonical-Higgs identity "
            "cos(theta)=1, or continue seed-controlled FH/LSZ production plus "
            "a pole-identity acceptance gate; a same-source pole residue alone "
            "is not enough."
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
