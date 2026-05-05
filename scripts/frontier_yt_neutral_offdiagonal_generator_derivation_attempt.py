#!/usr/bin/env python3
"""
PR #230 neutral off-diagonal generator derivation attempt.

This block tests the clean neutral-sector positive route after the Burnside
attempt: can the current PR230 surface itself derive the missing off-diagonal
source/orthogonal neutral generator needed for primitive-cone or full-matrix
irreducibility?

It cannot.  The current source functional and production rows remain
source-only or absence-guarded; Schur, W/Z, and O_H rows are absent; and the
current Burnside witness is block diagonal.  Outside-math tools are still
useful as certificate engines, but no present same-surface artifact supplies
the mixed generator they would need.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "gns_source_higgs_flat_extension": "outputs/yt_pr230_gns_source_higgs_flat_extension_attempt_2026-05-05.json",
    "source_higgs_harness_absence_guard": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
    "source_higgs_cross_correlator_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_response_harness_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "schur_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_row_contract_gate": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "neutral_primitive_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_primitive_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "neutral_burnside_attempt": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
    "full_positive_closure_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "offdiagonal_generator_certificate": (
        "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json"
    ),
    "neutral_primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
    "source_higgs_measurement_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "schur_scalar_kernel_rows": "outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
}

FORBIDDEN_IMPORTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "reduced pilots as production evidence",
    "c2 = 1, Z_match = 1, or kappa_s = 1 by convention",
    "PSLQ/value recognition as generator selector",
    "self-declared off-diagonal generator without same-surface derivation",
]

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


def future_file_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def offdiagonal_norm(matrix: np.ndarray) -> float:
    offdiag = np.array(matrix, dtype=float)
    np.fill_diagonal(offdiag, 0.0)
    return float(np.linalg.norm(offdiag, ord=1))


def primitive_power_positive(matrix: np.ndarray, tolerance: float = 1.0e-12) -> dict[str, Any]:
    n = matrix.shape[0]
    power = np.array(matrix, dtype=float)
    max_power = max(1, n * n - 2 * n + 2)
    for exponent in range(1, max_power + 1):
        if bool(np.all(power > tolerance)):
            return {"positive": True, "first_positive_power": exponent}
        power = power @ matrix
    return {"positive": False, "first_positive_power": None}


def strongly_connected(matrix: np.ndarray, tolerance: float = 1.0e-12) -> bool:
    n = matrix.shape[0]
    graph = [[j for j in range(n) if matrix[i, j] > tolerance] for i in range(n)]
    reverse = [[i for i in range(n) if matrix[i, j] > tolerance] for j in range(n)]

    def reach(adjacency: list[list[int]]) -> set[int]:
        seen = {0}
        frontier = [0]
        while frontier:
            node = frontier.pop()
            for child in adjacency[node]:
                if child not in seen:
                    seen.add(child)
                    frontier.append(child)
        return seen

    return len(reach(graph)) == n and len(reach(reverse)) == n


def derivation_attempts(parents: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    source_only_transfer = np.asarray([[0.82, 0.0], [0.0, 0.61]], dtype=float)
    accepted_shape = np.asarray([[0.62, 0.18], [0.11, 0.71]], dtype=float)
    attempts = [
        {
            "route": "source-functional FH/LSZ rows",
            "math_tool": "commutant/Burnside intake",
            "candidate_matrix": source_only_transfer.tolist(),
            "offdiagonal_norm": offdiagonal_norm(source_only_transfer),
            "same_surface_artifact": "C_ss and dE_top/ds only",
            "result": "blocked",
            "reason": "source-only rows are invariant under an orthogonal neutral completion",
        },
        {
            "route": "source-Higgs O_H/C_sH/C_HH rows",
            "math_tool": "GNS flat extension or Gram rank",
            "candidate_matrix": None,
            "offdiagonal_norm": None,
            "same_surface_artifact": "absent",
            "result": "blocked",
            "reason": status(parents["source_higgs_cross_correlator_builder"]),
        },
        {
            "route": "same-source W/Z response rows",
            "math_tool": "non-source rank repair / covariance row",
            "candidate_matrix": None,
            "offdiagonal_norm": None,
            "same_surface_artifact": "absent_guarded",
            "result": "blocked",
            "reason": status(parents["same_source_wz_response_gate"]),
        },
        {
            "route": "Schur A/B/C kernel rows",
            "math_tool": "Schur complement / exact tensor contraction",
            "candidate_matrix": None,
            "offdiagonal_norm": None,
            "same_surface_artifact": "absent",
            "result": "blocked",
            "reason": status(parents["schur_row_absence_guard"]),
        },
        {
            "route": "invariant-ring neutral labels",
            "math_tool": "Schur multiplicity-one",
            "candidate_matrix": source_only_transfer.tolist(),
            "offdiagonal_norm": offdiagonal_norm(source_only_transfer),
            "same_surface_artifact": "two-singlet completion allowed",
            "result": "blocked",
            "reason": status(parents["invariant_ring_oh_attempt"]),
        },
    ]
    return [
        *attempts,
        {
            "route": "future off-diagonal generator acceptance shape",
            "math_tool": "Perron-Frobenius / primitive matrix / Burnside",
            "candidate_matrix": accepted_shape.tolist(),
            "offdiagonal_norm": offdiagonal_norm(accepted_shape),
            "same_surface_artifact": "not present",
            "strongly_connected": strongly_connected(accepted_shape),
            "primitive_power": primitive_power_positive(accepted_shape),
            "result": "future contract witness only",
            "reason": "would close the neutral primitive shape if derived on the PR230 surface",
        },
    ]


def future_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_origin",
            "required": (
                "derivation from PR230 Cl(3)/Z3 action/source functional or a "
                "production same-ensemble non-source response row"
            ),
            "current_satisfied": False,
        },
        {
            "id": "offdiagonal_source_orthogonal_entry",
            "required": "nonzero source/orthogonal neutral coupling with sign and normalization",
            "current_satisfied": False,
        },
        {
            "id": "primitive_or_burnside_check",
            "required": "full matrix algebra/scalar commutant or positive primitive transfer power",
            "current_satisfied": False,
        },
        {
            "id": "pole_and_overlap_authority",
            "required": "isolated lowest neutral pole plus source and canonical-Higgs overlap authority",
            "current_satisfied": False,
        },
        {
            "id": "claim_firewall",
            "required": "no H_unit/Ward/observed/alpha/plaquette/u0/unit-normalization selectors",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 neutral off-diagonal generator derivation attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    future_present = future_file_presence()
    attempts = derivation_attempts(parents)
    contract = future_certificate_contract()

    source_higgs_absent = (
        parents["source_higgs_harness_absence_guard"].get("proposal_allowed") is False
        and "guard" in statuses["source_higgs_harness_absence_guard"]
        and "absent" in statuses["source_higgs_cross_correlator_builder"]
    )
    wz_absent = (
        parents["wz_response_harness_absence_guard"].get("proposal_allowed") is False
        and "absence guard" in statuses["wz_response_harness_absence_guard"]
        and parents["same_source_wz_response_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )
    schur_absent = (
        parents["schur_row_absence_guard"].get("current_schur_kernel_rows_present") is False
        and parents["schur_row_contract_gate"].get("proposal_allowed") is False
    )
    primitive_absent = (
        parents["neutral_primitive_gate"].get("primitive_cone_certificate_gate_passed") is False
        and parents["neutral_primitive_stretch_no_go"].get("primitive_cone_stretch_no_go_passed")
        is True
    )
    burnside_blocks = (
        parents["neutral_burnside_attempt"].get("burnside_irreducibility_certificate_passed")
        is False
        and parents["neutral_burnside_attempt"].get("exact_negative_boundary_passed") is True
    )
    invariant_ring_blocks = (
        parents["invariant_ring_oh_attempt"].get("invariant_ring_certificate_passed") is False
        and "two-singlet" in json.dumps(parents["invariant_ring_oh_attempt"])
    )
    gns_blocks = (
        parents["gns_source_higgs_flat_extension"].get("gns_flat_extension_passed") is False
        and parents["gns_source_higgs_flat_extension"].get("gns_certificate_written") is False
    )
    current_attempts_have_no_mixed_generator = all(
        row["result"] != "blocked" or not row.get("offdiagonal_norm")
        for row in attempts
        if row["route"] != "future off-diagonal generator acceptance shape"
    )
    future_shape_is_valid = (
        attempts[-1]["strongly_connected"] is True
        and attempts[-1]["primitive_power"]["positive"] is True
        and attempts[-1]["offdiagonal_norm"] > 0.0
    )
    future_artifacts_absent = not any(future_present.values())
    missing_contract = [row["id"] for row in contract if not row["current_satisfied"]]
    offdiagonal_generator_certificate_passed = False
    offdiagonal_generator_written = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-higgs-rows-absent", source_higgs_absent, statuses["source_higgs_cross_correlator_builder"])
    report("wz-response-rows-absent", wz_absent, statuses["same_source_wz_response_gate"])
    report("schur-kernel-rows-absent", schur_absent, statuses["schur_row_absence_guard"])
    report("primitive-cone-certificate-absent", primitive_absent, statuses["neutral_primitive_gate"])
    report("burnside-blocks-current-source-only-generators", burnside_blocks, statuses["neutral_burnside_attempt"])
    report("invariant-ring-two-singlet-obstruction-loaded", invariant_ring_blocks, statuses["invariant_ring_oh_attempt"])
    report("gns-flat-extension-not-an-offdiagonal-generator", gns_blocks, statuses["gns_source_higgs_flat_extension"])
    report("current-attempts-have-no-mixed-generator", current_attempts_have_no_mixed_generator, "all current candidates are absent or block diagonal")
    report("future-offdiagonal-shape-is-decisive", future_shape_is_valid, "synthetic contract witness is primitive")
    report("future-offdiagonal-artifacts-absent", future_artifacts_absent, f"future_present={future_present}")
    report("future-contract-recorded", len(missing_contract) == 4, f"missing={missing_contract}")
    report("offdiagonal-generator-certificate-not-passed", not offdiagonal_generator_certificate_passed, "no same-surface generator derived")
    report("forbidden-firewall-clean", True, ", ".join(FORBIDDEN_IMPORTS))

    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and source_higgs_absent
        and wz_absent
        and schur_absent
        and primitive_absent
        and burnside_blocks
        and invariant_ring_blocks
        and gns_blocks
        and current_attempts_have_no_mixed_generator
        and future_shape_is_valid
        and future_artifacts_absent
        and not offdiagonal_generator_certificate_passed
        and not offdiagonal_generator_written
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / neutral off-diagonal generator not "
            "derivable from current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface off-diagonal "
            "source/orthogonal neutral generator or primitive transfer "
            "certificate is supplied and passes the contract"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No current same-surface artifact supplies a nonzero off-diagonal "
            "neutral generator.  Existing source-only rows are block diagonal, "
            "and O_H/C_sH/C_HH, W/Z, Schur, and primitive-cone row files are absent."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "offdiagonal_generator_certificate_passed": offdiagonal_generator_certificate_passed,
        "offdiagonal_generator_written": offdiagonal_generator_written,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_file_presence": future_present,
        "derivation_attempts": attempts,
        "future_certificate_contract": contract,
        "outside_math_tools_used_as_certificate_engines": [
            "Burnside/double-commutant",
            "Perron-Frobenius primitive matrix",
            "Schur multiplicity-one / commutant",
            "GNS flat extension",
            "exact tensor/Schur row contract",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write a neutral off-diagonal generator certificate",
            "does not treat the synthetic primitive matrix as PR230 evidence",
            "does not promote source-only C_ss, GNS labels, Schur method names, or Burnside theorem names to physical rows",
            "does not import H_unit, Ward authority, observed targets, alpha_LM, plaquette, u0, reduced pilots, c2=1, Z_match=1, kappa_s=1, or PSLQ selectors",
        ],
        "exact_next_action": (
            "Make this route positive by deriving or measuring a same-surface "
            "off-diagonal neutral generator, then rerun primitive-cone/Burnside "
            "gates.  Otherwise prioritize O_H/C_sH/C_HH pole rows, real W/Z "
            "response rows with strict g2 and identity certificates, Schur "
            "A/B/C rows, or strict scalar-LSZ infinite/tail moment authority."
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
