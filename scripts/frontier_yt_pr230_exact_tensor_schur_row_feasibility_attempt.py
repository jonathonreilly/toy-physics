#!/usr/bin/env python3
"""
PR #230 exact tensor/PEPS Schur-row feasibility attempt.

Exact tensor contraction is a good outside-math tool once the contracted object
is fully specified.  This runner asks the narrower current-surface question:
can an exact tensor/PEPS contraction of the existing PR230 source functional
produce the missing same-surface Schur A/B/C kernel rows without first adding a
neutral scalar kernel partition, source/orthogonal projector, and row
definitions?

The answer on the current surface is no.  Exact contraction can evaluate
defined tensor networks; it cannot define the missing Schur row labels.  The
source-only scalar marginal remains compatible with inequivalent A/B/C row
families unless the neutral kernel basis and source/orthogonal partition are
supplied as same-surface data.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_exact_tensor_schur_row_feasibility_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "schur_compressed_bootstrap": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "neutral_primitive_stretch": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "scalar_lsz_holonomic_attempt": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_ROW_FILES = {
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "schur_scalar_kernel_rows": "outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "exact_tensor_schur_kernel_rows": "outputs/yt_exact_tensor_schur_kernel_rows_2026-05-05.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "reduced cold pilots as production evidence",
    "c2 = 1, Z_match = 1, or kappa_s = 1 by convention",
    "PSLQ/value recognition as row selector",
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ROW_FILES.items()}


def exact_tensor_row_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_source_functional",
            "required": "PR230 source functional or finite tensor network for the source-only scalar marginal",
            "current_satisfied": True,
            "comment": "The source-only object can be simulated or tensorized in principle.",
        },
        {
            "id": "neutral_scalar_kernel_basis",
            "required": "same-surface neutral scalar kernel basis containing source and orthogonal directions",
            "current_satisfied": False,
        },
        {
            "id": "source_orthogonal_projector",
            "required": "projector and normalization selecting the source block and orthogonal complement",
            "current_satisfied": False,
        },
        {
            "id": "schur_abc_row_definitions",
            "required": "definitions of A(q), B(q), C(q), or equivalent precontracted matrix Schur rows",
            "current_satisfied": False,
        },
        {
            "id": "contact_threshold_fv_ir_conventions",
            "required": "contact/subtraction, threshold, FV/IR, and limiting-order conventions for row use at the pole",
            "current_satisfied": False,
        },
        {
            "id": "canonical_bridge_or_neutral_irreducibility",
            "required": "O_H/source-Higgs identity, same-source W/Z identity, or neutral irreducibility authority that makes the rows physical",
            "current_satisfied": False,
        },
        {
            "id": "exact_contraction_certificate",
            "required": "actual exact tensor/PEPS contraction or certified numerical tensor contraction of the defined row network",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "reject H_unit, Ward, observed selectors, alpha/plaquette/u0, reduced pilots, unit c2/Z_match/kappa_s, and PSLQ selectors",
            "current_satisfied": True,
        },
    ]


def schur_eff(a: float, b: float, c: float) -> float:
    return a - b * b / c


def make_partition(
    *,
    label: str,
    pole: float,
    slope: float,
    b0: float,
    b1: float,
    c0: float,
    c1: float,
) -> dict[str, Any]:
    def target_d(x: float) -> float:
        dx = x - pole
        return slope * dx + 0.11 * dx * dx

    def b_of(x: float) -> float:
        return b0 + b1 * (x - pole)

    def c_of(x: float) -> float:
        return c0 + c1 * (x - pole)

    def a_of(x: float) -> float:
        b = b_of(x)
        c = c_of(x)
        return target_d(x) + b * b / c

    rows = {
        "A_at_pole": a_of(pole),
        "B_at_pole": b0,
        "C_at_pole": c0,
        "A_prime_at_pole": slope + (2.0 * b0 * b1) / c0 - (b0 * b0 * c1) / (c0 * c0),
        "B_prime_at_pole": b1,
        "C_prime_at_pole": c1,
    }
    return {
        "id": label,
        "rows": rows,
        "functions": {
            "A": a_of,
            "B": b_of,
            "C": c_of,
            "D_eff": lambda x: schur_eff(a_of(x), b_of(x), c_of(x)),
            "target_D_eff": target_d,
        },
    }


def max_abs(values: list[float]) -> float:
    return max((abs(value) for value in values), default=0.0)


def evaluate_row_definition_gauge(
    first: dict[str, Any],
    second: dict[str, Any],
    sample_points: list[float],
) -> dict[str, Any]:
    def fn(partition: dict[str, Any], name: str) -> Callable[[float], float]:
        return partition["functions"][name]

    first_d = [fn(first, "D_eff")(x) for x in sample_points]
    second_d = [fn(second, "D_eff")(x) for x in sample_points]
    target_d = [fn(first, "target_D_eff")(x) for x in sample_points]
    same_source_marginal = max_abs([a - b for a, b in zip(first_d, second_d)]) < 1.0e-12
    both_match_tensor_marginal = (
        max_abs([a - b for a, b in zip(first_d, target_d)]) < 1.0e-12
        and max_abs([a - b for a, b in zip(second_d, target_d)]) < 1.0e-12
    )
    rows_differ = any(
        abs(first["rows"][key] - second["rows"][key]) > 1.0e-12
        for key in first["rows"]
    )
    c_nonzero = all(
        abs(fn(partition, "C")(x)) > 1.0e-9
        for partition in (first, second)
        for x in sample_points
    )
    finite_rows = all(
        math.isfinite(fn(partition, name)(x))
        for partition in (first, second)
        for name in ("A", "B", "C", "D_eff")
        for x in sample_points
    )
    return {
        "sample_points": sample_points,
        "first_source_marginal_samples": first_d,
        "second_source_marginal_samples": second_d,
        "exact_tensor_source_marginal_samples": target_d,
        "same_source_marginal_on_grid": same_source_marginal,
        "both_match_exact_tensor_source_marginal": both_match_tensor_marginal,
        "abc_rows_differ": rows_differ,
        "orthogonal_block_nonzero_on_grid": c_nonzero,
        "rows_finite_on_grid": finite_rows,
        "interpretation": (
            "An exact source-only tensor marginal does not select the Schur "
            "source/orthogonal row partition.  Distinct A/B/C rows can share "
            "the same source marginal until the row network itself is defined."
        ),
    }


def main() -> int:
    print("PR #230 exact tensor/PEPS Schur-row feasibility attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    future_rows_present = [name for name, present in future_present.items() if present]
    contract = exact_tensor_row_contract()
    missing_contract = [
        row["id"]
        for row in contract
        if row["id"] != "same_surface_source_functional" and not row["current_satisfied"]
    ]

    selected = parents["clean_source_higgs_math_selector"].get("selected_clean_route", {})
    stage_2_tools = selected.get("stage_2", {}).get("candidate_tools", [])
    selector_marks_exact_tensor_future = (
        "future-only" in str(selected.get("current_status", ""))
        and any("exact tensor" in str(tool) for tool in stage_2_tools)
    )
    schur_contract_not_passed = (
        parents["schur_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_contract"].get("current_closure_gate_passed") is False
    )
    row_absence_loaded = (
        parents["schur_absence_guard"].get("schur_kprime_row_absence_guard_passed") is True
        and parents["schur_absence_guard"].get("current_schur_kernel_rows_present") is False
    )
    compressed_no_go_loaded = (
        parents["schur_compressed_bootstrap"].get("bootstrap_no_go_passed") is True
        and parents["schur_compressed_bootstrap"].get("proposal_allowed") is False
    )
    invariant_oh_blocker_loaded = (
        parents["invariant_ring_oh_attempt"].get("invariant_ring_certificate_passed") is False
        and parents["invariant_ring_oh_attempt"].get("proposal_allowed") is False
    )
    primitive_blocker_loaded = (
        parents["neutral_primitive_stretch"].get("primitive_cone_stretch_no_go_passed")
        is True
    )
    holonomic_blocker_loaded = (
        parents["scalar_lsz_holonomic_attempt"].get("holonomic_exact_authority_passed")
        is False
    )

    pole = 0.0
    slope = 0.73
    first = make_partition(
        label="exact_tensor_row_definition_A",
        pole=pole,
        slope=slope,
        b0=0.21,
        b1=-0.03,
        c0=1.35,
        c1=0.09,
    )
    second = make_partition(
        label="exact_tensor_row_definition_B",
        pole=pole,
        slope=slope,
        b0=-0.47,
        b1=0.14,
        c0=2.25,
        c1=-0.16,
    )
    sample_points = [-0.31, -0.12, 0.0, 0.19, 0.44]
    row_gauge = evaluate_row_definition_gauge(first, second, sample_points)
    forbidden_firewall_clean = True
    exact_tensor_schur_row_feasibility_passed = False
    schur_rows_written = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-marks-exact-tensor-future-only", selector_marks_exact_tensor_future, str(selected.get("stage_2", {})))
    report("schur-contract-still-not-passed", schur_contract_not_passed, statuses["schur_contract"])
    report("schur-row-absence-guard-loaded", row_absence_loaded, statuses["schur_absence_guard"])
    report("compressed-denominator-no-go-loaded", compressed_no_go_loaded, statuses["schur_compressed_bootstrap"])
    report("invariant-oh-blocker-loaded", invariant_oh_blocker_loaded, statuses["invariant_ring_oh_attempt"])
    report("neutral-primitive-blocker-loaded", primitive_blocker_loaded, statuses["neutral_primitive_stretch"])
    report("scalar-lsz-holonomic-blocker-loaded", holonomic_blocker_loaded, statuses["scalar_lsz_holonomic_attempt"])
    report("future-schur-row-files-absent", not future_rows_present, f"present={future_rows_present}")
    report("tensor-row-contract-missing-definitions", len(missing_contract) == 6, f"missing={missing_contract}")
    report("same-source-marginal-counterfamily", row_gauge["same_source_marginal_on_grid"], "two row definitions share the exact source marginal")
    report("counterfamily-matches-tensor-marginal", row_gauge["both_match_exact_tensor_source_marginal"], "both match the same source-only tensor output")
    report("counterfamily-abc-rows-differ", row_gauge["abc_rows_differ"], "A/B/C rows are not unique")
    report("counterfamily-rows-finite", row_gauge["rows_finite_on_grid"], "finite nondegenerate rows on the grid")
    report("forbidden-firewall-clean", forbidden_firewall_clean, ", ".join(FORBIDDEN_INPUTS))
    report("no-schur-rows-written", not schur_rows_written, f"future_file_presence={future_present}")
    report("exact-tensor-feasibility-not-passed", not exact_tensor_schur_row_feasibility_passed, "method name is not row authority")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / exact tensor Schur A/B/C row feasibility "
            "blocked on current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface neutral scalar kernel "
            "basis, source/orthogonal projector, A/B/C row definitions, and "
            "certified exact tensor contraction are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Exact tensor/PEPS contraction can evaluate a defined finite tensor "
            "network, but the current PR230 surface does not define the neutral "
            "scalar kernel basis, source/orthogonal partition, or A/B/C row "
            "operators.  The same source-only marginal is compatible with "
            "inequivalent Schur row definitions."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_tensor_schur_row_feasibility_passed": exact_tensor_schur_row_feasibility_passed,
        "schur_rows_written": schur_rows_written,
        "future_file_presence": future_present,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_tensor_row_contract": contract,
        "missing_future_tensor_row_contract": missing_contract,
        "row_definition_gauge_counterfamily": {
            "shared_pole": pole,
            "shared_D_eff_prime_at_pole": slope,
            "partition_A_rows": first["rows"],
            "partition_B_rows": second["rows"],
            "checks": row_gauge,
        },
        "strict_non_claims": [
            "does not produce Schur A/B/C rows",
            "does not write a future Schur row file",
            "does not claim retained or proposed_retained PR230 closure",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, unit c2/Z_match/kappa_s, or PSLQ selectors",
            "does not treat exact tensor/PEPS as authority before the row network is defined",
        ],
        "exact_next_action": (
            "Define a same-surface neutral scalar kernel basis and source/"
            "orthogonal projector, then emit A/B/C or precontracted matrix "
            "Schur rows from a certified exact tensor/PEPS contraction.  If "
            "that cannot be supplied, pivot to O_H/C_sH/C_HH pole rows, "
            "same-source W/Z response rows with g2 and identity authority, "
            "strict scalar-LSZ moment/threshold/FV authority, or a "
            "neutral-sector irreducibility certificate."
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
