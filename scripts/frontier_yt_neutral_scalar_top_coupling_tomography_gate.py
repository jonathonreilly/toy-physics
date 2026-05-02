#!/usr/bin/env python3
"""
PR #230 neutral-scalar top-coupling tomography gate.

Complete source-spectrum data identify the source overlap vector, and
dE_top/ds gives one linear functional of the neutral-scalar top-coupling
vector.  This runner checks the rank condition needed to recover the canonical
Higgs component.  On the current PR surface the rank condition is not passed.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json"

PARENTS = {
    "complete_source_spectrum_identity": "outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json",
    "neutral_scalar_rank_one_purity": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "neutral_scalar_dynamical_rank_one": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_wz_response": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "source_higgs_harness_absence": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
    "wz_response_harness_absence": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
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


def dot(lhs: list[float], rhs: list[float]) -> float:
    return sum(a * b for a, b in zip(lhs, rhs))


def rank_2x2(rows: list[list[float]]) -> int:
    if not rows:
        return 0
    if len(rows) == 1:
        return 0 if all(abs(x) < 1.0e-14 for x in rows[0]) else 1
    det = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
    return 2 if abs(det) > 1.0e-12 else 1


def tomography_witness() -> dict[str, Any]:
    source_row = [0.8, 0.6]
    null_row = [source_row[1], -source_row[0]]
    response = 0.8
    particular = [response * source_row[0], response * source_row[1]]
    lambdas = [-0.75, -0.25, 0.15, 0.35]

    rows: list[dict[str, Any]] = []
    for lam in lambdas:
        coupling = [particular[0] + lam * null_row[0], particular[1] + lam * null_row[1]]
        rows.append(
            {
                "lambda": lam,
                "coupling_vector_basis_h_chi": coupling,
                "canonical_higgs_y_t": coupling[0],
                "orthogonal_scalar_top_coupling": coupling[1],
                "source_response": dot(source_row, coupling),
            }
        )

    responses = [float(row["source_response"]) for row in rows]
    y_values = [float(row["canonical_higgs_y_t"]) for row in rows]
    chi_values = [float(row["orthogonal_scalar_top_coupling"]) for row in rows]
    current_rank = rank_2x2([source_row])
    hypothetical_wz_rank = rank_2x2([source_row, [1.0, 0.0]])
    hypothetical_ch_rank = rank_2x2([source_row, [1.0, 0.0]])
    return {
        "neutral_scalar_basis": ["h_canonical", "chi_orthogonal"],
        "source_overlap_row_from_complete_C_ss": source_row,
        "current_response_matrix_rank": current_rank,
        "required_rank_for_two_component_top_coupling": 2,
        "null_direction": null_row,
        "rows": rows,
        "checks": {
            "null_direction_annihilates_source_row": abs(dot(source_row, null_row)) < 1.0e-14,
            "same_source_response_identical": max(responses) - min(responses) < 1.0e-14,
            "canonical_higgs_y_span_factor": max(y_values) / min(y_values),
            "orthogonal_couplings_finite_positive": all(math.isfinite(value) and value > 0.0 for value in chi_values),
            "current_rank_insufficient": current_rank < 2,
            "hypothetical_wz_or_ch_row_would_close_rank": hypothetical_wz_rank == 2 and hypothetical_ch_rank == 2,
        },
        "hypothetical_rank_repairs": [
            {
                "repair": "canonical-Higgs row from O_H/C_sH/C_HH purity",
                "response_matrix_rank_if_present": hypothetical_ch_rank,
                "current_surface_present": False,
            },
            {
                "repair": "independent W/Z response row with sector-overlap identity",
                "response_matrix_rank_if_present": hypothetical_wz_rank,
                "current_surface_present": False,
            },
            {
                "repair": "rank-one neutral-scalar theorem",
                "effective_required_rank_if_derived": 1,
                "current_surface_present": False,
            },
        ],
    }


def main() -> int:
    print("PR #230 neutral-scalar top-coupling tomography gate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = tomography_witness()
    checks = witness["checks"]

    complete_source_blocked = (
        "complete source spectrum not canonical-Higgs closure"
        in status(parents["complete_source_spectrum_identity"])
        and parents["complete_source_spectrum_identity"].get("proposal_allowed") is False
    )
    rank_one_not_passed = (
        "neutral scalar rank-one purity gate not passed" in status(parents["neutral_scalar_rank_one_purity"])
        and parents["neutral_scalar_rank_one_purity"].get("neutral_scalar_rank_one_purity_gate_passed") is False
        and "dynamical rank-one neutral scalar theorem not derived"
        in status(parents["neutral_scalar_dynamical_rank_one"])
    )
    no_selection_rule = (
        "no-orthogonal-top-coupling selection rule not derived"
        in status(parents["no_orthogonal_top_coupling_selection"])
        and parents["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    ch_rows_absent = (
        "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity"])
        and "source-Higgs harness absence guard" in status(parents["source_higgs_harness_absence"])
    )
    wz_rows_absent = (
        "same-source WZ response certificate gate not passed" in status(parents["same_source_wz_response"])
        and "WZ response harness absence guard" in status(parents["wz_response_harness_absence"])
    )

    gate_passed = (
        not missing
        and not proposal_allowed
        and witness["current_response_matrix_rank"] >= witness["required_rank_for_two_component_top_coupling"]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("complete-source-spectrum-route-blocked", complete_source_blocked, status(parents["complete_source_spectrum_identity"]))
    report("rank-one-neutral-scalar-theorem-not-passed", rank_one_not_passed, status(parents["neutral_scalar_rank_one_purity"]))
    report("no-orthogonal-top-coupling-not-derived", no_selection_rule, status(parents["no_orthogonal_top_coupling_selection"]))
    report("source-higgs-rank-row-absent", ch_rows_absent, "O_H/C_sH/C_HH rank row absent")
    report("wz-rank-row-absent", wz_rows_absent, "W/Z response rank row absent")
    report("null-direction-annihilates-source-row", checks["null_direction_annihilates_source_row"], str(witness["null_direction"]))
    report("same-source-response-held-fixed", checks["same_source_response_identical"], "rank-one source row only")
    report(
        "canonical-higgs-component-varies",
        checks["canonical_higgs_y_span_factor"] > 4.0,
        f"span={checks['canonical_higgs_y_span_factor']:.6g}",
    )
    report("orthogonal-couplings-finite-positive", checks["orthogonal_couplings_finite_positive"], "witness stays finite/positive")
    report("current-response-rank-insufficient", checks["current_rank_insufficient"], f"rank={witness['current_response_matrix_rank']}")
    report("non-source-rank-row-would-be-repair", checks["hypothetical_wz_or_ch_row_would_close_rank"], "rank would be 2 if present")
    report("tomography-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / neutral scalar top-coupling tomography gate not passed",
        "verdict": (
            "Complete source-spectrum data provide a source-overlap row, and "
            "dE_top/ds supplies one scalar response equation.  For a two-component "
            "neutral scalar sector this leaves a null direction in the top-coupling "
            "vector, so the canonical-Higgs component can vary while all source-only "
            "rows stay fixed.  Closure needs a rank-one neutral-scalar theorem, a "
            "no-orthogonal-top-coupling theorem, same-surface O_H/C_sH/C_HH data, "
            "or an independent W/Z response row with identity certificates."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The response matrix has rank one on the current surface; the canonical-Higgs top-coupling component is not determined.",
        "tomography_witness": witness,
        "gate_passed": gate_passed,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set cos(theta) = 1",
            "does not set orthogonal scalar top coupling to zero",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Add an independent non-source response row: same-surface "
            "O_H/C_sH/C_HH Gram-purity data, W/Z response with sector-overlap "
            "identity certificates, or a rank-one/no-orthogonal-coupling theorem."
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
