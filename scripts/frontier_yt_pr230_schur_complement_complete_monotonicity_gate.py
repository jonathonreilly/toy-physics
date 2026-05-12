#!/usr/bin/env python3
"""
PR #230 Schur-complement complete-monotonicity / threshold authority gate.

The first Schur repair gate found one useful finite diagnostic:

    C_x|s(q) = det([[C_ss, C_sx], [C_sx, C_xx]]) / C_ss(q)

decreases from the zero mode to the first shell, while raw C_ss and C_s|x
fail the same necessary Stieltjes direction.  This runner asks the next
stricter question: can the current C_x|s packet be promoted to strict
scalar-LSZ moment/threshold/FV authority?

It cannot on the current surface.  The packet has only zero and first-shell
momenta, no complete 63/63 packet yet, no pole/model-class row, no threshold
measure, no FV/IR/multivolume limit, and no canonical O_H/source-overlap.
The first-shell decrease is therefore bounded support only.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json"
)

PARENTS = {
    "schur_repair": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "schur_abc": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
    "schur_kprime": "outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json",
    "schur_pole_lift": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def distinct_p_levels(rows: list[dict[str, Any]]) -> list[float]:
    levels: set[float] = set()
    for chunk in rows:
        modes = chunk.get("mode_rows")
        if not isinstance(modes, dict):
            continue
        for row in modes.values():
            if isinstance(row, dict) and finite(row.get("p_hat_sq")):
                levels.add(round(float(row["p_hat_sq"]), 15))
    return sorted(levels)


def finite_difference_requirements() -> list[dict[str, Any]]:
    return [
        {
            "id": "stieltjes_first_difference",
            "required": "C(x2) - C(x1) <= 0 for x2 > x1",
            "current_C_x_given_source": "passed on zero-to-first shell",
            "sufficient_for_authority": False,
        },
        {
            "id": "complete_monotonicity_higher_differences",
            "required": "alternating finite-difference signs across at least three ordered q_hat^2 levels, or an analytic moment theorem",
            "current_C_x_given_source": "not testable: current rows have only zero and first-shell momenta",
            "sufficient_for_authority": False,
        },
        {
            "id": "threshold_or_measure_certificate",
            "required": "positive spectral measure / threshold support with contact-subtraction convention",
            "current_C_x_given_source": "absent",
            "sufficient_for_authority": False,
        },
        {
            "id": "pole_and_residue_certificate",
            "required": "isolated pole location, derivative/residue, and model-class authority",
            "current_C_x_given_source": "absent",
            "sufficient_for_authority": False,
        },
        {
            "id": "fv_ir_limiting_order",
            "required": "multivolume FV/IR/zero-mode limiting order",
            "current_C_x_given_source": "absent: current packet is single volume L12xT24",
            "sufficient_for_authority": False,
        },
        {
            "id": "canonical_source_bridge",
            "required": "canonical O_H/source-overlap or W/Z physical-response bridge",
            "current_C_x_given_source": "absent",
            "sufficient_for_authority": False,
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_pilot_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_C_x_given_source_as_canonical_O_H": False,
        "treated_first_shell_check_as_scalar_lsz_authority": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 Schur-complement complete-monotonicity authority gate")
    print("=" * 78)

    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    schur = parents["schur_repair"]
    rows = schur.get("per_chunk_schur_residual_rows")
    rows = rows if isinstance(rows, list) else []
    p_levels = distinct_p_levels(rows)
    x_summary = schur.get("x_given_source_summary", {})
    x_diff = x_summary.get("shell_minus_zero", {}) if isinstance(x_summary, dict) else {}
    x_z = x_summary.get("shell_minus_zero_z_score_from_chunk_scatter") if isinstance(x_summary, dict) else None

    first_shell_support = (
        schur.get("x_given_source_stieltjes_first_shell_passed") is True
        and isinstance(x_diff, dict)
        and finite(x_diff.get("mean"))
        and float(x_diff["mean"]) < 0.0
    )
    source_given_x_rejected = schur.get("source_given_x_stieltjes_first_shell_failed") is True
    ready_count = parents["row_combiner"].get("ready_chunks")
    expected_count = parents["row_combiner"].get("expected_chunks")
    finite_packet_support_boundary = (
        isinstance(ready_count, int)
        and isinstance(expected_count, int)
        and 0 < ready_count <= expected_count
    )
    only_two_p_levels = len(p_levels) == 2
    higher_differences_unavailable = only_two_p_levels
    pole_authority_absent = (
        parents["schur_pole_lift"].get("strict_pole_lift_passed") is False
        and parents["schur_pole_lift"].get("proposal_allowed") is False
        and "finite Schur A/B/C rows do not lift to strict pole-row authority"
        in status(parents["schur_pole_lift"])
    )
    finite_schur_not_strict = (
        parents["schur_abc"].get("finite_schur_abc_rows_written") is True
        and parents["schur_abc"].get("strict_schur_abc_kernel_rows_written") is False
    )
    kprime_not_authority = (
        parents["schur_kprime"].get("finite_shell_schur_kprime_scout_passed") is True
        and parents["schur_kprime"].get("strict_schur_kprime_authority_passed") is False
    )
    strict_scalar_lsz_absent = (
        parents["strict_scalar_lsz"].get("strict_scalar_lsz_moment_fv_authority_present") is False
        and parents["strict_scalar_lsz"].get("proposal_allowed") is False
    )
    source_higgs_bridge_absent = (
        parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and parents["source_higgs_readiness"].get("proposal_allowed") is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("x-given-source-first-shell-support", first_shell_support, f"diff={x_diff.get('mean')} z={x_z}")
    report("source-given-x-first-shell-rejected", source_given_x_rejected, statuses["schur_repair"])
    report("finite-row-packet-support-only", finite_packet_support_boundary, f"ready={ready_count}/{expected_count}")
    report("only-zero-and-first-shell-momenta", only_two_p_levels, f"p_levels={p_levels}")
    report("higher-complete-monotonicity-unavailable", higher_differences_unavailable, "need at least three ordered q_hat^2 levels or analytic theorem")
    report("finite-schur-abc-not-strict-kernel-rows", finite_schur_not_strict, statuses["schur_abc"])
    report("finite-kprime-scout-not-authority", kprime_not_authority, statuses["schur_kprime"])
    report("pole-model-class-authority-absent", pole_authority_absent, statuses["schur_pole_lift"])
    report("strict-scalar-lsz-authority-absent", strict_scalar_lsz_absent, statuses["strict_scalar_lsz"])
    report("source-higgs-or-physical-response-bridge-absent", source_higgs_bridge_absent, statuses["source_higgs_readiness"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-proposal-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-import-firewall-clean", firewall_clean, str(forbidden_firewall()))

    result = {
        "actual_current_surface_status": (
            "bounded support plus exact boundary / C_x|s Schur residual passes "
            "the necessary first-shell Stieltjes direction but lacks complete "
            "monotonicity, threshold, pole, FV/IR, and source-bridge authority"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A zero-to-first-shell decrease is only a necessary Stieltjes check. "
            "The current packet has two q_hat^2 levels, no "
            "pole/model-class rows, no spectral threshold theorem, no multivolume "
            "FV/IR limit, and no canonical O_H or W/Z bridge."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "schur_complement_complete_monotonicity_gate_passed": True,
        "x_given_source_first_shell_stieltjes_support": first_shell_support,
        "complete_monotonicity_authority_passed": False,
        "higher_momentum_shells_present": len(p_levels) >= 3,
        "threshold_or_measure_authority_present": False,
        "pole_model_class_authority_present": False,
        "fv_ir_multivolume_authority_present": False,
        "canonical_higgs_or_physical_response_bridge_present": False,
        "ready_chunks": ready_count,
        "expected_chunks": expected_count,
        "p_hat_sq_levels": p_levels,
        "x_given_source_summary": x_summary,
        "finite_difference_requirements": finite_difference_requirements(),
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat C_x|s as canonical O_H",
            "does not treat a first-shell Stieltjes check as scalar-LSZ authority",
            "does not supply C_spH/C_HH pole rows",
            "does not supply a W/Z physical-response bridge",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "Use C_x|s as a targeted diagnostic while the 63-chunk row packet "
            "is complete finite support, but for closure add higher-shell/multivolume Schur rows "
            "plus a pole/threshold theorem, or supply canonical O_H/C_spH/C_HH "
            "rows or a genuine W/Z response bridge."
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
