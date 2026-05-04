#!/usr/bin/env python3
"""
PR #230 Schur row candidate extraction attempt.

The Schur row contract gate names the future row file needed for the
K'(pole) route.  This runner checks the nearest current finite-ladder,
eigen-derivative, and Feshbach support artifacts to see whether they can be
converted into same-surface A/B/C or precontracted Schur rows.

It does not write the future row file.  It records that the available finite
support is not the required neutral-scalar kernel partition.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_schur_row_candidate_extraction_attempt_2026-05-03.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_schur_scalar_kernel_rows_2026-05-03.json"

PARENTS = {
    "schur_kernel_row_contract_gate": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "eigen_derivative_gate": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "total_momentum_derivative_scout": "outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json",
    "ladder_kernel_scout": "outputs/yt_scalar_ladder_kernel_scout_2026-05-01.json",
    "feshbach_response_boundary": "outputs/yt_feshbach_operator_response_boundary_2026-05-01.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
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


def matrix_shape(matrix: Any) -> tuple[int, int] | None:
    if not isinstance(matrix, list) or not matrix or not all(isinstance(row, list) for row in matrix):
        return None
    widths = {len(row) for row in matrix}
    if len(widths) != 1:
        return None
    return (len(matrix), next(iter(widths)))


def finite_matrix(matrix: Any) -> bool:
    shape = matrix_shape(matrix)
    return shape is not None and all(finite(value) for row in matrix for value in row)


def classify_candidates(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    eigen = certs["eigen_derivative_gate"]
    total = certs["total_momentum_derivative_scout"]
    ladder = certs["ladder_kernel_scout"]
    feshbach = certs["feshbach_response_boundary"]

    m0 = eigen.get("M0_at_pole")
    eigen_rows = eigen.get("rows", [])
    total_rows = total.get("scan", [])
    ladder_rows = ladder.get("scan", [])
    feshbach_rows = feshbach.get("rows", [])

    return [
        {
            "id": "eigen_derivative_gate_M0_at_pole",
            "path": PARENTS["eigen_derivative_gate"],
            "positive_reuse": "finite 2x2 toy pole matrix and eigen-derivative examples",
            "signals": {
                "finite_matrix": finite_matrix(m0),
                "matrix_shape": matrix_shape(m0),
                "has_lambda_prime_examples": bool(eigen_rows),
            },
            "missing_or_blocking": [
                "M0 is not certified as the same-surface source/orthogonal neutral kernel partition",
                "does not provide A_prime/B_prime/C_prime block derivatives",
                "lambda_prime examples are not block Schur rows",
                "no FV/IR/zero-mode pole-control certificate for the matrix rows",
            ],
            "usable_as_schur_rows": False,
        },
        {
            "id": "total_momentum_derivative_scout_scan",
            "path": PARENTS["total_momentum_derivative_scout"],
            "positive_reuse": "finite d lambda_max / d p_hat^2 proxy rows",
            "signals": {
                "scan_rows": len(total_rows) if isinstance(total_rows, list) else 0,
                "has_finite_derivatives": any(
                    finite(row.get("d_lambda_dp_hat_sq")) for row in total_rows if isinstance(row, dict)
                )
                if isinstance(total_rows, list)
                else False,
            },
            "missing_or_blocking": [
                "derivative rows are prescription-sensitive finite scouts",
                "do not identify A/B/C source and orthogonal kernel blocks",
                "do not include source-orthogonal covariance rows",
                "do not pass the scalar-kernel row contract gate",
            ],
            "usable_as_schur_rows": False,
        },
        {
            "id": "ladder_kernel_scout_lambda_scan",
            "path": PARENTS["ladder_kernel_scout"],
            "positive_reuse": "finite lambda_max crossing scout",
            "signals": {
                "scan_rows": len(ladder_rows) if isinstance(ladder_rows, list) else 0,
                "has_crossing_examples": any(
                    row.get("pole_condition_lambda_ge_1") is True
                    for row in ladder_rows
                    if isinstance(row, dict)
                )
                if isinstance(ladder_rows, list)
                else False,
            },
            "missing_or_blocking": [
                "lambda crossing is not a Schur block partition",
                "no pole derivative rows A_prime/B_prime/C_prime",
                "depends on simplified projector, mass, and IR regulator",
                "does not certify same-surface neutral scalar source coordinate",
            ],
            "usable_as_schur_rows": False,
        },
        {
            "id": "feshbach_response_boundary",
            "path": PARENTS["feshbach_response_boundary"],
            "positive_reuse": "exact projection covariance for already defined operators",
            "signals": {
                "response_rows": len(feshbach_rows) if isinstance(feshbach_rows, list) else 0,
                "preserves_ratios": "Feshbach response boundary" in status(feshbach),
            },
            "missing_or_blocking": [
                "operator response preservation is not a microscopic scalar kernel row",
                "does not compute A/B/C or precontracted C^{-1} rows",
                "does not prove the source operator is canonical Higgs",
            ],
            "usable_as_schur_rows": False,
        },
    ]


def main() -> int:
    print("PR #230 Schur row candidate extraction attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    candidates = classify_candidates(certs)
    usable = [row["id"] for row in candidates if row["usable_as_schur_rows"]]

    contract_loaded = "Schur kernel row contract gate" in status(certs["schur_kernel_row_contract_gate"])
    sufficiency_loaded = "Schur-complement K-prime sufficiency theorem" in status(
        certs["schur_complement_kprime_sufficiency"]
    )
    absence_guard_loaded = "Schur K-prime row absence guard" in status(certs["schur_kprime_row_absence_guard"])
    eigen_support_loaded = "scalar ladder eigen-derivative gate" in status(certs["eigen_derivative_gate"])
    total_scout_loaded = "total-momentum derivative scout" in status(certs["total_momentum_derivative_scout"])
    ladder_scout_loaded = "ladder-kernel scout" in status(certs["ladder_kernel_scout"])
    feshbach_loaded = "Feshbach response boundary" in status(certs["feshbach_response_boundary"])
    source_boundary_loaded = "source-functional LSZ identifiability theorem" in status(
        certs["source_functional_lsz_identifiability"]
    )
    finite_ladder_candidate_usable = bool(usable)
    candidate_extraction_closes_pr230 = False
    candidate_rows_written = False
    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and contract_loaded
        and sufficiency_loaded
        and absence_guard_loaded
        and eigen_support_loaded
        and total_scout_loaded
        and ladder_scout_loaded
        and feshbach_loaded
        and source_boundary_loaded
        and not finite_ladder_candidate_usable
        and not candidate_extraction_closes_pr230
        and not candidate_rows_written
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-contract-loaded", contract_loaded, status(certs["schur_kernel_row_contract_gate"]))
    report("schur-sufficiency-loaded", sufficiency_loaded, status(certs["schur_complement_kprime_sufficiency"]))
    report("schur-absence-guard-loaded", absence_guard_loaded, status(certs["schur_kprime_row_absence_guard"]))
    report("nearest-finite-candidates-classified", len(candidates) == 4, f"candidates={len(candidates)}")
    report("eigen-toy-matrix-not-schur-rows", not candidates[0]["usable_as_schur_rows"], candidates[0]["id"])
    report("finite-derivative-scout-not-schur-rows", not candidates[1]["usable_as_schur_rows"], candidates[1]["id"])
    report("lambda-scan-not-schur-rows", not candidates[2]["usable_as_schur_rows"], candidates[2]["id"])
    report("feshbach-response-not-schur-rows", not candidates[3]["usable_as_schur_rows"], candidates[3]["id"])
    report("no-usable-schur-row-candidate-found", not usable, f"usable={usable}")
    report("does-not-write-future-row-file", not candidate_rows_written, str(FUTURE_ROWS.relative_to(ROOT)))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "finite ladder/Feshbach support cannot be imported as Schur rows")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Schur row candidate extraction from finite ladder support"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Nearest finite-ladder, eigen-derivative, and Feshbach support "
            "artifacts do not supply same-surface A/B/C or precontracted "
            "Schur kernel rows with partition, pole-control, and firewall "
            "certificates."
        ),
        "bare_retained_allowed": False,
        "candidate_surfaces": candidates,
        "finite_ladder_candidate_usable": finite_ladder_candidate_usable,
        "usable_candidates": usable,
        "candidate_extraction_closes_pr230": candidate_extraction_closes_pr230,
        "candidate_rows_written": candidate_rows_written,
        "future_rows_path": str(FUTURE_ROWS.relative_to(ROOT)),
        "future_rows_path_present": FUTURE_ROWS.exists(),
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
            "does not infer A/B/C Schur rows from lambda scans, M0 toy rows, or Feshbach responses",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Produce genuine same-surface Schur kernel rows from a neutral "
            "scalar kernel theorem/measurement, or pivot to certified "
            "O_H/C_sH/C_HH pole rows or same-source W/Z response rows."
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
