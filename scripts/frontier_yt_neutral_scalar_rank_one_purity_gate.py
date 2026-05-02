#!/usr/bin/env python3
"""
PR #230 neutral-scalar rank-one purity gate.

A direct way to certify source-pole purity would be a retained theorem that the
current neutral scalar response space is rank one: every neutral scalar source
response is the canonical Higgs radial mode, with no orthogonal top-coupled
component.  This runner makes that premise executable and checks whether the
current PR surface supplies it.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json"

CERTS = {
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_pole_purity_cross_correlator": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "higgs_pole_identity_latest": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def rank_two_witness() -> dict[str, Any]:
    theta_values = [0.0, 0.35, 0.70]
    y_h = 0.93
    y_chi = -0.45
    rows = []
    for theta in theta_values:
        source_readout = math.cos(theta) * y_h + math.sin(theta) * y_chi
        rows.append(
            {
                "theta": theta,
                "canonical_higgs_y_t": y_h,
                "orthogonal_scalar_top_coupling": y_chi,
                "source_pole_readout": source_readout,
                "cos_theta": math.cos(theta),
                "sin_theta": math.sin(theta),
            }
        )
    return {
        "neutral_scalar_rank": 2,
        "same_listed_charges": True,
        "d17_carrier_label_preserved": True,
        "rows": rows,
        "readout_span": max(row["source_pole_readout"] for row in rows)
        - min(row["source_pole_readout"] for row in rows),
    }


def main() -> int:
    print("PR #230 neutral-scalar rank-one purity gate")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    witness = rank_two_witness()

    d17_support_not_identity = (
        "D17 source-pole identity closure attempt blocked" in status(certs["d17_source_pole_identity"])
        and certs["d17_source_pole_identity"].get("theorem_closed") is False
    )
    no_orthogonal_top_coupling_not_derived = (
        "no-orthogonal-top-coupling selection rule not derived"
        in status(certs["no_orthogonal_top_coupling_selection"])
        and certs["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    source_pole_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in status(certs["source_pole_canonical_higgs_mixing"])
        and certs["source_pole_canonical_higgs_mixing"].get(
            "source_pole_canonical_identity_gate_passed"
        )
        is False
    )
    source_only_purity_blocks = (
        "source-pole purity cross-correlator gate not passed"
        in status(certs["source_pole_purity_cross_correlator"])
        and certs["source_pole_purity_cross_correlator"].get("source_pole_purity_gate_passed")
        is False
    )
    gram_purity_not_passed = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    wz_response_not_passed = (
        "same-source WZ response certificate gate not passed"
        in status(certs["same_source_wz_response_gate"])
        and certs["same_source_wz_response_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )
    latest_blocker_open = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_pole_identity_latest"])
        and certs["higgs_pole_identity_latest"].get("identity_closed") is False
    )
    rank_one_certificate_present = False
    rank_two_witness_nontrivial = witness["neutral_scalar_rank"] == 2 and witness["readout_span"] > 0.1
    gate_passed = (
        not missing
        and not proposal_allowed
        and rank_one_certificate_present
        and not no_orthogonal_top_coupling_not_derived
        and not source_pole_mixing_blocks
        and not gram_purity_not_passed
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("d17-support-is-not-rank-one-identity", d17_support_not_identity, status(certs["d17_source_pole_identity"]))
    report("no-orthogonal-top-coupling-not-derived", no_orthogonal_top_coupling_not_derived, status(certs["no_orthogonal_top_coupling_selection"]))
    report("source-pole-mixing-still-blocks", source_pole_mixing_blocks, status(certs["source_pole_canonical_higgs_mixing"]))
    report("source-only-purity-still-blocks", source_only_purity_blocks, status(certs["source_pole_purity_cross_correlator"]))
    report("gram-purity-gate-not-passed", gram_purity_not_passed, status(certs["source_higgs_gram_purity"]))
    report("wz-response-gate-not-passed", wz_response_not_passed, status(certs["same_source_wz_response_gate"]))
    report("latest-higgs-pole-blocker-open", latest_blocker_open, status(certs["higgs_pole_identity_latest"]))
    report("rank-two-witness-nontrivial", rank_two_witness_nontrivial, f"readout_span={witness['readout_span']}")
    report("neutral-scalar-rank-one-certificate-absent", not rank_one_certificate_present, "no retained rank-one theorem")
    report("rank-one-purity-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / neutral scalar rank-one purity gate not passed",
        "verdict": (
            "A retained rank-one theorem for the neutral scalar response space "
            "would close a direct source-pole purity route, but the current PR "
            "surface does not supply it.  D17 carrier uniqueness is support, "
            "not a dynamical Hilbert-space rank theorem.  The current listed "
            "charges still allow an orthogonal neutral scalar with top coupling, "
            "source-only pole data do not fix source-Higgs overlap, and the "
            "C_sH/WZ identity gates are not passed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No retained rank-one neutral-scalar response theorem or equivalent purity measurement exists.",
        "neutral_scalar_rank_one_purity_gate_passed": gate_passed,
        "rank_one_certificate_present": rank_one_certificate_present,
        "rank_two_witness": witness,
        "acceptance_requirements": [
            "retained theorem that the neutral scalar response space is rank one",
            "or pole-level Gram purity Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
            "or same-source W/Z response certificate plus sector-overlap identity",
            "no orthogonal top-coupled scalar response component",
            "canonical-Higgs pole identity passed",
        ],
        "parent_certificates": CERTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat D17 carrier support as source-pole purity",
            "does not set cos(theta)=1 or kappa_s=1",
            "does not set orthogonal top coupling to zero",
            "does not use H_unit, yt_ward_identity, observed top/y_t, observed W/Z masses, alpha_LM, plaquette, u0, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Either derive the rank-one neutral-scalar response theorem, "
            "measure C_sH/C_HH Gram purity, implement the W/Z response "
            "certificate route, or continue seed-controlled FH/LSZ production."
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
