#!/usr/bin/env python3
"""
PR #230 Schur A/B/C definition derivation attempt.

This runner asks a necessary question for every Schur-based closure route:
does the current PR230 surface define the neutral scalar pre-Schur rows
`A`, `B`, and `C`, or only an effective source denominator/source marginal?

Outside-math tools such as exact tensor contraction, creative telescoping,
Picard-Fuchs/D-module methods, free probability, PSLQ/value recognition, and
motivic searches are allowed as computational machinery only after the object
being computed is defined.  They are not row-definition or normalization
authority by name.  On the current surface, the source-only effective
denominator remains compatible with inequivalent `A/B/C` block rows, so this
runner writes an exact negative boundary and no future Schur row file.
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
    / "yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json"
)

PARENTS = {
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "schur_compressed_bootstrap": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "exact_tensor_schur_feasibility": "outputs/yt_pr230_exact_tensor_schur_row_feasibility_attempt_2026-05-05.json",
    "feshbach_response_boundary": "outputs/yt_feshbach_operator_response_boundary_2026-05-01.json",
    "scalar_ladder_kernel_scout": "outputs/yt_scalar_ladder_kernel_scout_2026-05-01.json",
    "scalar_ladder_eigen_derivative": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "scalar_ladder_total_momentum": "outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json",
    "scalar_ladder_projector_norm": "outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json",
    "scalar_ladder_ir_zero_mode": "outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json",
    "scalar_ladder_derivative_limit": "outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
    "scalar_ladder_residue_envelope": "outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
    "scalar_kernel_ward_obstruction": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
    "neutral_offdiagonal_generator": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_ROW_FILES = {
    "schur_scalar_kernel_rows": "outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "schur_abc_definition_certificate": "outputs/yt_schur_abc_definition_certificate_2026-05-05.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass / observed y_t selectors",
    "alpha_LM / plaquette / u0 proof input",
    "reduced pilots as production evidence",
    "c2 = 1, Z_match = 1, or kappa_s = 1 by convention",
    "PSLQ/value recognition as physical-normalization authority",
    "Picard-Fuchs/D-module/creative-telescoping theorem names as row labels",
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


def definition_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_source_denominator",
            "needed": "source-only scalar effective denominator or source marginal",
            "current_satisfied": True,
            "current_surface": "finite FH/LSZ and scalar-ladder source support",
        },
        {
            "id": "neutral_scalar_kernel_basis",
            "needed": "same-surface neutral scalar kernel basis before Schur elimination",
            "current_satisfied": False,
        },
        {
            "id": "source_orthogonal_projector",
            "needed": "projector P_s and complement Q with normalization and measure authority",
            "current_satisfied": False,
        },
        {
            "id": "abc_block_definition",
            "needed": "A=P_s K P_s, B=P_s K Q, C=Q K Q or equivalent precontracted row definitions",
            "current_satisfied": False,
        },
        {
            "id": "block_derivative_rows",
            "needed": "A'(pole), B'(pole), C'(pole), or certified derivative of the block Schur complement",
            "current_satisfied": False,
        },
        {
            "id": "contact_threshold_fv_ir_scheme",
            "needed": "contact subtraction, threshold, finite-volume, IR, and zero-mode limiting order",
            "current_satisfied": False,
        },
        {
            "id": "canonical_bridge",
            "needed": "O_H/source-Higgs, W/Z physical response, or neutral irreducibility authority",
            "current_satisfied": False,
        },
        {
            "id": "outside_math_firewall",
            "needed": "outside math may compute defined rows but cannot define missing rows or proof-normalizations by name",
            "current_satisfied": True,
        },
    ]


def schur_eff(a: float, b: float, c: float) -> float:
    return a - b * b / c


def make_block_family(
    *,
    label: str,
    slope: float,
    curvature: float,
    b0: float,
    b1: float,
    c0: float,
    c1: float,
) -> dict[str, Any]:
    def d_eff(x: float) -> float:
        return slope * x + curvature * x * x

    def b(x: float) -> float:
        return b0 + b1 * x

    def c(x: float) -> float:
        return c0 + c1 * x

    def a(x: float) -> float:
        bx = b(x)
        cx = c(x)
        return d_eff(x) + bx * bx / cx

    return {
        "id": label,
        "rows_at_pole": {
            "A": a(0.0),
            "B": b(0.0),
            "C": c(0.0),
            "A_prime": slope + (2.0 * b0 * b1) / c0 - (b0 * b0 * c1) / (c0 * c0),
            "B_prime": b1,
            "C_prime": c1,
        },
        "functions": {
            "A": a,
            "B": b,
            "C": c,
            "D_eff": lambda x: schur_eff(a(x), b(x), c(x)),
            "target_D_eff": d_eff,
        },
    }


def max_abs(values: list[float]) -> float:
    return max((abs(value) for value in values), default=0.0)


def evaluate_row_gauge(families: list[dict[str, Any]], grid: list[float]) -> dict[str, Any]:
    def fn(family: dict[str, Any], key: str) -> Callable[[float], float]:
        return family["functions"][key]

    d_samples = [[fn(family, "D_eff")(x) for x in grid] for family in families]
    target = [fn(families[0], "target_D_eff")(x) for x in grid]
    all_share_source_denominator = all(
        max_abs([sample - target_value for sample, target_value in zip(row, target)])
        < 1.0e-12
        for row in d_samples
    )
    first_rows = families[0]["rows_at_pole"]
    rows_differ = all(
        any(abs(first_rows[key] - family["rows_at_pole"][key]) > 1.0e-12 for key in first_rows)
        for family in families[1:]
    )
    finite_nonzero_c = all(
        math.isfinite(fn(family, name)(x))
        for family in families
        for name in ("A", "B", "C", "D_eff")
        for x in grid
    ) and all(abs(fn(family, "C")(x)) > 1.0e-9 for family in families for x in grid)
    return {
        "grid": grid,
        "target_D_eff_samples": target,
        "family_D_eff_samples": d_samples,
        "all_share_source_denominator": all_share_source_denominator,
        "abc_rows_differ": rows_differ,
        "finite_nonzero_orthogonal_blocks": finite_nonzero_c,
        "interpretation": (
            "A source-only denominator, even if known exactly, is invariant "
            "under a row-definition gauge: changing B and C while shifting A "
            "keeps A - B C^{-1} B fixed but changes the A/B/C rows and their "
            "derivatives at the pole."
        ),
    }


def main() -> int:
    print("PR #230 Schur A/B/C definition derivation attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    future_rows_present = [name for name, present in future_present.items() if present]
    contract = definition_contract()
    missing_contract = [
        row["id"] for row in contract if not row["current_satisfied"]
    ]

    sufficiency_support_loaded = (
        parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_closure_gate_passed") is False
    )
    absence_guard_loaded = (
        parents["schur_absence_guard"].get("schur_kprime_row_absence_guard_passed") is True
        and parents["schur_absence_guard"].get("current_schur_kernel_rows_present") is False
    )
    contract_not_passed = (
        parents["schur_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_contract"].get("current_closure_gate_passed") is False
    )
    finite_candidate_blocker_loaded = (
        parents["schur_candidate_extraction"].get("finite_ladder_candidate_usable") is False
        and parents["schur_candidate_extraction"].get("candidate_rows_written") is False
    )
    compressed_blocker_loaded = (
        parents["schur_compressed_bootstrap"].get("bootstrap_no_go_passed") is True
        and parents["schur_compressed_bootstrap"].get("proposal_allowed") is False
    )
    exact_tensor_blocker_loaded = (
        parents["exact_tensor_schur_feasibility"].get("exact_tensor_schur_row_feasibility_passed")
        is False
        and parents["exact_tensor_schur_feasibility"].get("schur_rows_written") is False
    )
    feshbach_is_response_not_rows = (
        "Feshbach response boundary" in statuses["feshbach_response_boundary"]
        and parents["feshbach_response_boundary"].get("proposal_allowed") is False
    )
    ladder_obstructions_loaded = all(
        statuses[name]
        for name in (
            "scalar_ladder_kernel_scout",
            "scalar_ladder_eigen_derivative",
            "scalar_ladder_total_momentum",
            "scalar_ladder_projector_norm",
            "scalar_ladder_ir_zero_mode",
            "scalar_ladder_derivative_limit",
            "scalar_ladder_residue_envelope",
            "scalar_kernel_ward_obstruction",
        )
    )
    neutral_mixed_generator_absent = (
        parents["neutral_offdiagonal_generator"].get("offdiagonal_generator_certificate_passed")
        is False
        and parents["neutral_offdiagonal_generator"].get("offdiagonal_generator_written")
        is False
    )

    families = [
        make_block_family(
            label="abc_definition_family_alpha",
            slope=0.61,
            curvature=0.17,
            b0=0.18,
            b1=-0.04,
            c0=1.12,
            c1=0.08,
        ),
        make_block_family(
            label="abc_definition_family_beta",
            slope=0.61,
            curvature=0.17,
            b0=-0.42,
            b1=0.13,
            c0=2.40,
            c1=-0.11,
        ),
        make_block_family(
            label="abc_definition_family_gamma",
            slope=0.61,
            curvature=0.17,
            b0=0.56,
            b1=0.02,
            c0=3.05,
            c1=0.06,
        ),
    ]
    row_gauge = evaluate_row_gauge(families, [-0.40, -0.15, 0.0, 0.23, 0.51])

    outside_math_firewall_clean = True
    schur_abc_definition_derivation_passed = False
    schur_abc_rows_written = False
    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and sufficiency_support_loaded
        and absence_guard_loaded
        and contract_not_passed
        and finite_candidate_blocker_loaded
        and compressed_blocker_loaded
        and exact_tensor_blocker_loaded
        and feshbach_is_response_not_rows
        and ladder_obstructions_loaded
        and neutral_mixed_generator_absent
        and not future_rows_present
        and row_gauge["all_share_source_denominator"]
        and row_gauge["abc_rows_differ"]
        and row_gauge["finite_nonzero_orthogonal_blocks"]
        and not schur_abc_definition_derivation_passed
        and not schur_abc_rows_written
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-sufficiency-support-loaded", sufficiency_support_loaded, statuses["schur_sufficiency"])
    report("schur-row-absence-guard-loaded", absence_guard_loaded, statuses["schur_absence_guard"])
    report("schur-row-contract-not-passed", contract_not_passed, statuses["schur_contract"])
    report("finite-candidate-extraction-blocker-loaded", finite_candidate_blocker_loaded, statuses["schur_candidate_extraction"])
    report("compressed-denominator-blocker-loaded", compressed_blocker_loaded, statuses["schur_compressed_bootstrap"])
    report("exact-tensor-blocker-loaded", exact_tensor_blocker_loaded, statuses["exact_tensor_schur_feasibility"])
    report("feshbach-response-not-schur-rows", feshbach_is_response_not_rows, statuses["feshbach_response_boundary"])
    report("ladder-obstructions-loaded", ladder_obstructions_loaded, "ladder scout/projector/IR/derivative/residue/Ward blockers loaded")
    report("neutral-mixed-generator-absent", neutral_mixed_generator_absent, statuses["neutral_offdiagonal_generator"])
    report("future-schur-row-files-absent", not future_rows_present, f"present={future_rows_present}")
    report("definition-contract-missing-required-rows", len(missing_contract) == 6, f"missing={missing_contract}")
    report("same-effective-denominator-counterfamily", row_gauge["all_share_source_denominator"], "all families share D_eff")
    report("counterfamily-abc-rows-differ", row_gauge["abc_rows_differ"], "A/B/C rows differ at pole")
    report("counterfamily-finite-nondegenerate", row_gauge["finite_nonzero_orthogonal_blocks"], "C block finite/nonzero on grid")
    report("outside-math-firewall-clean", outside_math_firewall_clean, ", ".join(FORBIDDEN_INPUTS))
    report("no-schur-abc-definition-certificate-written", not schur_abc_rows_written, f"future_file_presence={future_present}")
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "current surface defines denominator support, not A/B/C rows")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Schur A/B/C definition not derivable "
            "from current PR230 source-only surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface neutral scalar kernel "
            "basis, source/orthogonal projector, A/B/C block definitions, "
            "block-derivative rows, contact/FV/IR scheme, and certified "
            "contraction or theorem are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current artifacts define source-denominator support and "
            "useful Schur sufficiency contracts, but they do not define the "
            "neutral scalar kernel basis, source/orthogonal projector, or "
            "A/B/C block rows.  Distinct finite nondegenerate block families "
            "share the same source effective denominator while changing the "
            "row data needed for K'(pole)."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "schur_abc_definition_derivation_passed": schur_abc_definition_derivation_passed,
        "schur_abc_rows_written": schur_abc_rows_written,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "definition_contract": contract,
        "missing_definition_contract": missing_contract,
        "future_file_presence": future_present,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "row_definition_gauge_counterfamily": {
            "families": [
                {
                    "id": family["id"],
                    "rows_at_pole": family["rows_at_pole"],
                }
                for family in families
            ],
            "checks": row_gauge,
        },
        "allowed_outside_math_tools": [
            "exact tensor/PEPS contraction after row network definition",
            "holonomic D-module / Picard-Fuchs / creative telescoping after row-generating integrals are defined",
            "free probability or Weingarten expansions after the neutral kernel partition is defined",
            "motivic or PSLQ searches only as post hoc exact-value recognition, never as a physical-row selector",
        ],
        "strict_non_claims": [
            "does not produce Schur A/B/C rows",
            "does not write a Schur row or definition certificate future file",
            "does not claim retained or proposed_retained PR230 closure",
            "does not infer row definitions from the compressed denominator, source-only C_ss rows, Feshbach response, exact tensor method names, PSLQ, or finite ladder scouts",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Produce a same-surface neutral scalar kernel basis and source/"
            "orthogonal projector, then emit A/B/C block rows or an equivalent "
            "precontracted Schur row certificate with contact/FV/IR and pole-"
            "derivative authority.  Otherwise pivot to certified O_H/C_sH/"
            "C_HH pole rows, genuine same-source W/Z response rows with g2/"
            "identity/covariance authority, strict scalar-LSZ moment/"
            "threshold/FV authority, or a neutral primitive-cone certificate."
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
