#!/usr/bin/env python3
"""
PR #230 completed-L12 chunk compute status.

This runner consumes the completed four-mode/x16 and eight-mode/x8 L12 FH/LSZ
chunk summaries.  It records what the compute campaign has genuinely produced
without promoting finite-volume source-response proxies into physical top mass
or Yukawa closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_l12_chunk_compute_status_2026-05-06.json"

PARENTS = {
    "four_mode_combiner": "outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json",
    "four_mode_combined": "outputs/yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json",
    "polefit8x8_combiner": "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json",
    "polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
    "polefit8x8_combined": "outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json",
    "stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "complete_bernstein_inverse_diagnostic": "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json",
    "positive_closure_completion_audit": "outputs/yt_pr230_positive_closure_completion_audit_2026-05-05.json",
    "genuine_source_pole_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status") or cert.get("verdict") or "")


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def response_summary(combined: dict[str, Any]) -> dict[str, float]:
    row = combined.get("source_response_summary", {})
    if not isinstance(row, dict):
        return {}
    return {
        "mean": float(row.get("mean")),
        "stderr": float(row.get("stderr")),
    }


def mode_rows(combined: dict[str, Any]) -> list[dict[str, Any]]:
    rows = (
        combined.get("combined_lsz_summary", {})
        .get("mode_rows", {})
    )
    if not isinstance(rows, dict):
        return []
    out = []
    for key, row in rows.items():
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "mode_key": key,
                "momentum_mode": row.get("momentum_mode"),
                "p_hat_sq": float(row.get("p_hat_sq")),
                "C_ss_real_weighted": float(row.get("C_ss_real_weighted")),
                "C_ss_real_weighted_stderr": float(row.get("C_ss_real_weighted_stderr")),
                "Gamma_ss_real_proxy": float(row.get("Gamma_ss_real_proxy")),
            }
        )
    return sorted(out, key=lambda r: (r["p_hat_sq"], str(r["mode_key"])))


def monotonicity_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    shell_rows = []
    for row in rows:
        shell_rows.append(
            {
                "mode_key": row["mode_key"],
                "p_hat_sq": row["p_hat_sq"],
                "C_ss_real_weighted": row["C_ss_real_weighted"],
                "Gamma_ss_real_proxy": row["Gamma_ss_real_proxy"],
            }
        )
    c_increase = []
    gamma_decrease = []
    for a, b in zip(shell_rows, shell_rows[1:]):
        if b["C_ss_real_weighted"] > a["C_ss_real_weighted"]:
            c_increase.append([a["mode_key"], b["mode_key"]])
        if b["Gamma_ss_real_proxy"] < a["Gamma_ss_real_proxy"]:
            gamma_decrease.append([a["mode_key"], b["mode_key"]])
    return {
        "rows": shell_rows,
        "C_ss_increases_with_p_hat_sq_pairs": c_increase,
        "Gamma_ss_decreases_with_p_hat_sq_pairs": gamma_decrease,
        "stieltjes_proxy_shortcut_blocked": bool(c_increase),
        "complete_bernstein_inverse_shortcut_blocked": bool(gamma_decrease),
    }


def source_response_consistency(a: dict[str, float], b: dict[str, float]) -> dict[str, Any]:
    delta = b["mean"] - a["mean"]
    sigma = math.sqrt(a["stderr"] ** 2 + b["stderr"] ** 2)
    z = abs(delta) / sigma if sigma > 0 else math.inf
    return {
        "four_mode_mean": a["mean"],
        "four_mode_stderr": a["stderr"],
        "polefit8x8_mean": b["mean"],
        "polefit8x8_stderr": b["stderr"],
        "delta": delta,
        "combined_stderr": sigma,
        "z_score": z,
        "consistent_within_one_sigma": z <= 1.0,
    }


def main() -> int:
    print("PR #230 completed-L12 chunk compute status")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    four = certs["four_mode_combined"]
    pole = certs["polefit8x8_combined"]
    four_resp = response_summary(four)
    pole_resp = response_summary(pole)
    response_consistency = (
        source_response_consistency(four_resp, pole_resp) if four_resp and pole_resp else {}
    )
    four_modes = mode_rows(four)
    pole_modes = mode_rows(pole)
    pole_monotonicity = monotonicity_summary(pole_modes)

    four_complete = (
        certs["four_mode_combiner"].get("proposal_allowed") is False
        and certs["four_mode_combiner"].get("combined_summary", {}).get("chunk_count") == 63
        and four.get("metadata", {}).get("saved_configurations") == 1008
    )
    pole_complete = (
        certs["polefit8x8_combiner"].get("proposal_allowed") is False
        and certs["polefit8x8_combiner"].get("combined_summary", {}).get("chunk_count") == 63
        and pole.get("metadata", {}).get("saved_configurations") == 1008
    )
    source_data_real = (
        four_complete
        and pole_complete
        and len(four_modes) == 4
        and len(pole_modes) == 8
        and bool(response_consistency)
        and response_consistency.get("consistent_within_one_sigma") is True
    )
    scalar_lsz_shortcut_blocked = (
        certs["stieltjes_proxy_diagnostic"].get("stieltjes_proxy_certificate_passed") is False
        and certs["complete_bernstein_inverse_diagnostic"].get(
            "complete_bernstein_inverse_certificate_passed"
        )
        is False
        and pole_monotonicity["stieltjes_proxy_shortcut_blocked"]
        and pole_monotonicity["complete_bernstein_inverse_shortcut_blocked"]
    )
    source_pole_genuine = (
        certs["genuine_source_pole_intake"].get(
            "artifact_is_genuine_current_surface_support"
        )
        is True
        and certs["genuine_source_pole_intake"].get("artifact_is_physics_closure")
        is False
    )
    aggregate_closure_barred = (
        certs["positive_closure_completion_audit"].get("closure_achieved") is False
        and certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    consumed_evidence = {
        "four_response": four_resp,
        "pole_response": pole_resp,
        "four_modes": four_modes,
        "pole_modes": pole_modes,
        "response_consistency": response_consistency,
        "pole_monotonicity": pole_monotonicity,
    }
    forbidden_inputs_absent = all(
        banned not in json.dumps(consumed_evidence, sort_keys=True)
        for banned in (
            "y_t_bare",
            "H_unit-to-top matrix element identification",
            "observed top mass as selector",
        )
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("four-mode-l12-stream-complete", four_complete, f"chunks={len(four.get('chunk_indices', []))} saved={four.get('metadata', {}).get('saved_configurations')}")
    report("polefit8x8-l12-stream-complete", pole_complete, f"chunks={len(pole.get('chunk_indices', []))} saved={pole.get('metadata', {}).get('saved_configurations')}")
    report("four-mode-shape-recorded", len(four_modes) == 4, f"modes={len(four_modes)}")
    report("polefit8x8-shape-recorded", len(pole_modes) == 8, f"modes={len(pole_modes)}")
    report(
        "source-response-consistent-across-streams",
        response_consistency.get("consistent_within_one_sigma") is True,
        f"z={response_consistency.get('z_score')}",
    )
    report(
        "source-data-real-current-surface-support",
        source_data_real,
        "completed L12 source-response support exists",
    )
    report(
        "stieltjes-shortcut-blocked-by-data",
        pole_monotonicity["stieltjes_proxy_shortcut_blocked"],
        f"pairs={len(pole_monotonicity['C_ss_increases_with_p_hat_sq_pairs'])}",
    )
    report(
        "complete-bernstein-shortcut-blocked-by-data",
        pole_monotonicity["complete_bernstein_inverse_shortcut_blocked"],
        f"pairs={len(pole_monotonicity['Gamma_ss_decreases_with_p_hat_sq_pairs'])}",
    )
    report("scalar-lsz-current-proxy-blocked", scalar_lsz_shortcut_blocked, "finite-shell proxy is not an LSZ denominator certificate")
    report("source-pole-artifact-genuine-but-not-closure", source_pole_genuine, status(certs["genuine_source_pole_intake"]))
    report("aggregate-closure-still-barred", aggregate_closure_barred, "closure_achieved=false and proposal_allowed=false")
    report("forbidden-input-firewall-clean", forbidden_inputs_absent, "no banned proof selectors in this status gate")

    result = {
        "actual_current_surface_status": (
            "bounded-support / completed L12 same-source chunk compute status; "
            "physical y_t closure still open"
        ),
        "verdict": (
            "The completed chunk campaign provides real, internally consistent "
            "L12 same-source FH/LSZ support data.  The four-mode/x16 and "
            "eight-mode/x8 source responses agree within one sigma.  The same "
            "data also block the tempting finite-shell scalar-LSZ shortcut: "
            "the polefit8x8 C_ss proxy increases with p_hat^2 and its inverse "
            "Gamma_ss decreases with p_hat^2, so it is not a strict Stieltjes "
            "or complete-Bernstein denominator certificate.  This artifact is "
            "therefore compute support, not m_t/y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Only L12 finite-volume source-response support is present; L16/L24, "
            "FV/IR/threshold authority, scalar-LSZ denominator authority, "
            "canonical O_H/source overlap, and matching/running closure remain open."
        ),
        "source_response_consistency": response_consistency,
        "four_mode_summary": {
            "combined_path": PARENTS["four_mode_combined"],
            "chunk_count": len(four.get("chunk_indices", [])),
            "saved_configurations": four.get("metadata", {}).get("saved_configurations"),
            "mode_count": len(four_modes),
            "source_response": four_resp,
        },
        "polefit8x8_summary": {
            "combined_path": PARENTS["polefit8x8_combined"],
            "chunk_count": len(pole.get("chunk_indices", [])),
            "saved_configurations": pole.get("metadata", {}).get("saved_configurations"),
            "mode_count": len(pole_modes),
            "source_response": pole_resp,
            "monotonicity_summary": pole_monotonicity,
        },
        "strict_closure_blockers": {
            "single_volume_only": True,
            "finite_shell_only": True,
            "scalar_lsz_denominator_certificate_absent": True,
            "canonical_oh_or_source_higgs_overlap_absent": True,
            "matching_running_bridge_absent": True,
            "aggregate_proposal_allowed": False,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not compute m_t(pole) or y_t(v)",
            "does not define y_t_bare",
            "does not identify O_sp with O_H",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat L12 finite-shell rows as strict scalar-LSZ or FV/IR evidence",
        ],
        "parent_certificates": PARENTS,
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
