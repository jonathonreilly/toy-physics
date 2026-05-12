#!/usr/bin/env python3
"""
PR #230 two-source taste-radial Schur finite-to-pole lift gate.

The finite Schur A/B/C row certificate computes inverse-block rows at the
zero mode and first nonzero shell.  This runner checks whether those finite
rows can be promoted to strict neutral-kernel A/B/C pole-row authority.

Even under the favorable assumption that the zero-mode point is the pole,
two endpoint values do not determine the pole derivative: adding
lambda * x * (x - dp) preserves both endpoint values but changes f'(0).
Therefore finite A_f/B_f/C_f rows remain bounded support until a model class,
isolated pole, FV/IR limiting order, and neutral-kernel row contract supply
derivative authority.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json"
)

PARENTS = {
    "finite_abc_rows": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
    "schur_kernel_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FINITE_KEYS = (
    ("A", "A_finite_K_ss_zero", "A_finite_K_ss_shell_mean"),
    ("B", "B_finite_K_sx_zero", "B_finite_K_sx_shell_mean"),
    ("C", "C_finite_K_xx_zero", "C_finite_K_xx_shell_mean"),
)

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


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def mean_shell_dp(chunks: list[dict[str, Any]]) -> float | None:
    values = [
        float(chunk["shell_p_hat_sq_mean"])
        for chunk in chunks
        if finite(chunk.get("shell_p_hat_sq_mean"))
    ]
    if not values:
        return None
    return statistics.fmean(values)


def interpolation_witness(summary: dict[str, Any], dp: float) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, zero_key, shell_key in FINITE_KEYS:
        y0 = float(summary[zero_key]["mean"])
        y1 = float(summary[shell_key]["mean"])
        secant = (y1 - y0) / dp
        variants = []
        for lam in (0.0, 1.0):
            def f(x: float, *, lam: float = lam, y0: float = y0, secant: float = secant) -> float:
                return y0 + secant * x + lam * x * (x - dp)

            variants.append(
                {
                    "lambda": lam,
                    "f_zero": f(0.0),
                    "f_shell": f(dp),
                    "endpoint_residual_max": max(abs(f(0.0) - y0), abs(f(dp) - y1)),
                    "derivative_at_zero_if_zero_is_pole": secant - lam * dp,
                }
            )
        rows[label] = {
            "zero_value": y0,
            "shell_value": y1,
            "shell_minus_zero_over_dp": secant,
            "endpoint_preserving_variants": variants,
            "derivative_spread": abs(
                variants[1]["derivative_at_zero_if_zero_is_pole"]
                - variants[0]["derivative_at_zero_if_zero_is_pole"]
            ),
        }
    return {
        "assumption_for_strongest_possible_current_lift": (
            "Treat the zero-mode point as if it were the pole.  The derivative "
            "is still not fixed by two endpoint values without a model class."
        ),
        "p_hat_sq_zero": 0.0,
        "p_hat_sq_shell_mean": dp,
        "rows": rows,
    }


def strict_blockers(
    finite_abc: dict[str, Any],
    schur_contract: dict[str, Any],
    witness: dict[str, Any],
) -> dict[str, bool]:
    return {
        "complete_63_of_63_packet_support_only": (
            finite_abc.get("ready_chunks") == finite_abc.get("expected_chunks")
            and finite_abc.get("expected_chunks") == 63
        ),
        "finite_combined_rows_are_not_strict_kernel_rows": True,
        "strict_schur_contract_gate_not_passed": schur_contract.get(
            "schur_kernel_row_contract_gate_passed"
        )
        is not True,
        "strict_neutral_kernel_abc_rows_absent": finite_abc.get(
            "strict_schur_abc_kernel_rows_written"
        )
        is not True,
        "isolated_pole_derivative_rows_absent": finite_abc.get(
            "pole_location_or_derivative_rows_present"
        )
        is not True,
        "fv_ir_zero_mode_authority_absent": finite_abc.get(
            "fv_ir_zero_mode_authority_present"
        )
        is not True,
        "canonical_higgs_identity_absent": finite_abc.get(
            "canonical_higgs_operator_identity_passed"
        )
        is not True,
        "endpoint_values_do_not_fix_derivative": all(
            row.get("derivative_spread", 0.0) > 0.0
            for row in witness.get("rows", {}).values()
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_endpoint_secant_as_kprime_pole": False,
        "treated_finite_abc_rows_as_strict_pole_rows": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 two-source taste-radial Schur finite-to-pole lift gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    finite_abc = parents["finite_abc_rows"]
    chunks = finite_abc.get("chunk_finite_schur_abc_rows")
    chunks = chunks if isinstance(chunks, list) else []
    summary = finite_abc.get("finite_shell_summary")
    summary = summary if isinstance(summary, dict) else {}
    dp = mean_shell_dp([chunk for chunk in chunks if isinstance(chunk, dict)])
    summary_complete = all(
        key in summary and finite(summary[key].get("mean"))
        for _, zero_key, shell_key in FINITE_KEYS
        for key in (zero_key, shell_key)
    )
    witness = interpolation_witness(summary, dp) if dp and dp > 0.0 and summary_complete else {}
    blockers = strict_blockers(finite_abc, parents["schur_kernel_contract"], witness)

    finite_abc_loaded = (
        finite_abc.get("two_source_taste_radial_schur_abc_finite_rows_passed") is True
        and finite_abc.get("finite_schur_abc_rows_written") is True
        and finite_abc.get("proposal_allowed") is False
    )
    schur_contract_open = (
        parents["schur_kernel_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_kernel_contract"].get("candidate_rows_present") is False
    )
    schur_sufficiency_loaded = (
        parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_schur_kernel_rows_present") is False
    )
    route_still_open = parents["schur_route_completion"].get("proposal_allowed") is False
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    endpoint_witness_passed = (
        bool(witness)
        and all(
            variant.get("endpoint_residual_max", 1.0) < 1.0e-12
            for row in witness["rows"].values()
            for variant in row["endpoint_preserving_variants"]
        )
        and all(row["derivative_spread"] > 0.0 for row in witness["rows"].values())
    )
    strict_lift_passed = False
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("finite-abc-rows-loaded", finite_abc_loaded, statuses["finite_abc_rows"])
    report("schur-contract-still-open", schur_contract_open, statuses["schur_kernel_contract"])
    report("schur-sufficiency-loaded", schur_sufficiency_loaded, statuses["schur_sufficiency"])
    report("finite-shell-summary-complete", summary_complete and bool(dp), f"dp={dp}")
    report("endpoint-derivative-nonidentifiability-witness", endpoint_witness_passed, str(witness))
    report("strict-blockers-present", all(blockers.values()), str(blockers))
    report("strict-pole-lift-not-passed", not strict_lift_passed, f"strict_lift_passed={strict_lift_passed}")
    report("schur-route-still-open", route_still_open, statuses["schur_route_completion"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    passed = (
        not missing
        and not proposals
        and finite_abc_loaded
        and schur_contract_open
        and schur_sufficiency_loaded
        and summary_complete
        and bool(dp)
        and endpoint_witness_passed
        and all(blockers.values())
        and not strict_lift_passed
        and route_still_open
        and retained_open
        and campaign_open
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / finite Schur A/B/C rows do not lift to "
            "strict pole-row authority without model-class, pole, and FV/IR authority"
        ),
        "conditional_surface_status": (
            "conditional-support only after complete combined rows, a certified "
            "neutral scalar kernel basis, isolated-pole derivative rows or an "
            "accepted model class, FV/IR zero-mode limiting order, and canonical "
            "O_H/source-overlap or same-source W/Z response authority are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Finite inverse rows are endpoint data.  The interpolation witness "
            "keeps the endpoint rows fixed while changing the derivative, so the "
            "strict K'(pole)/A'B'C' authority is not present on the current surface."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "two_source_taste_radial_schur_pole_lift_gate_passed": passed,
        "strict_pole_lift_passed": strict_lift_passed,
        "endpoint_derivative_nonidentifiability_witness_passed": endpoint_witness_passed,
        "strict_blockers": blockers,
        "interpolation_witness": witness,
        "ready_chunks": finite_abc.get("ready_chunks"),
        "expected_chunks": finite_abc.get("expected_chunks"),
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite A_f/B_f/C_f rows as strict pole rows",
            "does not treat endpoint secants as K'(pole)",
            "does not provide FV/IR or scalar threshold authority",
            "does not identify taste-radial x with canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Use the complete finite packet only as staging support, then supply either an accepted "
            "model-class/pole-derivative theorem with FV/IR control or direct "
            "strict neutral-kernel A/B/C pole rows.  Without that, pivot to "
            "O_H/C_sH/C_HH rows or same-source W/Z response."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
