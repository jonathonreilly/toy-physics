#!/usr/bin/env python3
"""
PR #230 W/Z Goldstone-equivalence source-identity no-go.

This runner closes a narrow W/Z shortcut: treating longitudinal gauge-boson /
Goldstone-equivalence structure as the missing PR230 source-to-canonical-Higgs
identity.  The equivalence theorem constrains the gauge/Higgs sector after the
canonical Higgs direction is known; it does not identify the scalar source
coordinate used by the top FH/LSZ response.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json"

PARENTS = {
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "one_higgs_completeness_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
    "brst_nielsen_higgs_identity_no_go": "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json",
    "sm_one_higgs_oh_import_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def rounded_values(rows: list[dict[str, Any]], path: tuple[str, ...]) -> set[float]:
    values = []
    for row in rows:
        value: Any = row
        for key in path:
            value = value[key]
        values.append(round(float(value), 12))
    return set(values)


def source_rotation_family() -> dict[str, Any]:
    g2 = 0.64
    gy = 0.36
    vev = 1.0
    yh = 0.91
    yx = -0.22
    m_chi = 1.35
    rows = []
    for theta in (0.0, 0.25, 0.65, 1.05):
        c = math.cos(theta)
        s = math.sin(theta)
        gauge_equivalence_signature = {
            "m_w": g2 * vev / 2.0,
            "m_z": math.sqrt(g2 * g2 + gy * gy) * vev / 2.0,
            "longitudinal_equivalence_residual": 0.0,
            "goldstone_radial_coupling_proxy": g2 * vev / 2.0,
        }
        top_slope = (yh * c + yx * s) / math.sqrt(2.0)
        w_slope = g2 * c / 2.0
        w_readout = g2 * top_slope / (math.sqrt(2.0) * w_slope)
        rows.append(
            {
                "theta": theta,
                "source_direction": {
                    "canonical_higgs_component": c,
                    "orthogonal_neutral_component": s,
                    "orthogonal_neutral_pole_mass": m_chi,
                },
                "gauge_equivalence_signature": gauge_equivalence_signature,
                "same_source_responses": {
                    "dE_top_ds": top_slope,
                    "dM_W_ds": w_slope,
                    "w_normalized_readout": w_readout,
                    "orthogonal_correction": yx * s / c,
                },
            }
        )
    gauge_signatures = [row["gauge_equivalence_signature"] for row in rows]
    return {
        "fixed_inputs": {
            "g2_symbolic_role": "kept fixed only inside the algebraic witness",
            "canonical_vev": vev,
            "canonical_top_yukawa": yh,
            "orthogonal_neutral_top_coupling": yx,
            "orthogonal_neutral_pole_mass": m_chi,
        },
        "rows": rows,
        "checks": {
            "gauge_equivalence_signature_fixed": all(
                signature == gauge_signatures[0] for signature in gauge_signatures
            ),
            "source_overlap_span": max(
                row["source_direction"]["canonical_higgs_component"] for row in rows
            )
            - min(row["source_direction"]["canonical_higgs_component"] for row in rows),
            "top_response_span": max(
                row["same_source_responses"]["dE_top_ds"] for row in rows
            )
            - min(row["same_source_responses"]["dE_top_ds"] for row in rows),
            "w_response_span": max(
                row["same_source_responses"]["dM_W_ds"] for row in rows
            )
            - min(row["same_source_responses"]["dM_W_ds"] for row in rows),
            "w_readout_span": max(
                row["same_source_responses"]["w_normalized_readout"] for row in rows
            )
            - min(row["same_source_responses"]["w_normalized_readout"] for row in rows),
        },
    }


def main() -> int:
    print("PR #230 W/Z Goldstone-equivalence source-identity no-go")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = source_rotation_family()
    checks = family["checks"]

    ew_action_absent = (
        "same-source EW action not defined" in status(parents["wz_same_source_ew_action_gate"])
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    source_transport_rejected = (
        "source-coordinate transport shortcut rejected"
        in status(parents["wz_source_coordinate_transport_no_go"])
        and parents["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
    )
    w_decomposition_loaded = (
        "same-source W-response decomposition theorem"
        in status(parents["same_source_w_response_decomposition"])
        and parents["same_source_w_response_decomposition"].get(
            "same_source_w_response_decomposition_theorem_passed"
        )
        is True
    )
    correction_gate_open = (
        parents["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False
    )
    one_higgs_premise_absent = (
        parents["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_gate_passed"
        )
        is False
    )
    brst_boundary_loaded = (
        "BRST-Nielsen identities not Higgs-pole identity"
        in status(parents["brst_nielsen_higgs_identity_no_go"])
        and parents["brst_nielsen_higgs_identity_no_go"].get("proposal_allowed") is False
    )
    sm_one_higgs_not_identity = (
        parents["sm_one_higgs_oh_import_boundary"].get("sm_one_higgs_import_closes_pr230")
        is False
    )
    canonical_identity_stretch_blocked = (
        parents["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
    )
    retained_route_open = (
        "retained closure not yet reached" in status(parents["retained_route"])
        and parents["retained_route"].get("proposal_allowed") is False
    )
    fixed_equivalence = checks["gauge_equivalence_signature_fixed"]
    source_overlap_varies = checks["source_overlap_span"] > 0.35
    responses_vary = (
        checks["top_response_span"] > 0.10
        and checks["w_response_span"] > 0.10
        and checks["w_readout_span"] > 0.05
    )
    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and ew_action_absent
        and source_transport_rejected
        and w_decomposition_loaded
        and correction_gate_open
        and one_higgs_premise_absent
        and brst_boundary_loaded
        and sm_one_higgs_not_identity
        and canonical_identity_stretch_blocked
        and retained_route_open
        and fixed_equivalence
        and source_overlap_varies
        and responses_vary
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-source-ew-action-absent", ew_action_absent, status(parents["wz_same_source_ew_action_gate"]))
    report("source-coordinate-transport-shortcut-rejected", source_transport_rejected, status(parents["wz_source_coordinate_transport_no_go"]))
    report("w-response-decomposition-loaded", w_decomposition_loaded, status(parents["same_source_w_response_decomposition"]))
    report("orthogonal-correction-gate-open", correction_gate_open, status(parents["same_source_w_response_orthogonal_correction"]))
    report("one-higgs-completeness-premise-absent", one_higgs_premise_absent, status(parents["one_higgs_completeness_orthogonal_null"]))
    report("brst-nielsen-boundary-loaded", brst_boundary_loaded, status(parents["brst_nielsen_higgs_identity_no_go"]))
    report("sm-one-higgs-not-source-identity", sm_one_higgs_not_identity, status(parents["sm_one_higgs_oh_import_boundary"]))
    report("canonical-identity-stretch-blocked", canonical_identity_stretch_blocked, status(parents["canonical_oh_premise_stretch"]))
    report("goldstone-equivalence-signature-held-fixed", fixed_equivalence, str(sorted(rounded_values(family["rows"], ("gauge_equivalence_signature", "m_w")))))
    report("source-overlap-varies", source_overlap_varies, f"span={checks['source_overlap_span']:.6g}")
    report("same-source-responses-vary", responses_vary, f"readout_span={checks['w_readout_span']:.6g}")
    report("retained-route-still-open", retained_route_open, status(parents["retained_route"]))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "equivalence structure does not identify the PR230 source")

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ Goldstone equivalence does not identify PR230 source coordinate",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Longitudinal gauge-boson / Goldstone-equivalence structure fixes "
            "gauge-sector relations after the canonical Higgs direction is known, "
            "but it does not certify that the PR230 scalar source is that direction."
        ),
        "bare_retained_allowed": False,
        "goldstone_equivalence_source_identity_no_go_passed": exact_negative_boundary_passed,
        "parent_certificates": PARENTS,
        "source_rotation_family": family,
        "theorem_statement": (
            "A family of source rotations can keep the longitudinal-equivalence "
            "and gauge-mass signature fixed while changing the source overlap "
            "with the canonical Higgs radial mode.  The same-source top and W "
            "responses then change, so equivalence structure alone cannot replace "
            "a same-surface source-identity, transport, one-Higgs completeness, "
            "or correction certificate."
        ),
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write W/Z measurement rows",
            "does not set the source-to-Higgs overlap by convention",
            "does not use external numerical selectors or user-banned shortcut authorities",
            "does not package or rerun chunk MC",
        ],
        "exact_next_action": (
            "Do not use longitudinal-equivalence or Goldstone bookkeeping as "
            "source-coordinate authority.  Continue only through real same-source "
            "W/Z rows plus identity/correction certificates, certified source-Higgs "
            "pole rows, Schur kernel rows, neutral irreducibility, or scalar-LSZ "
            "moment/threshold/FV authority."
        ),
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
