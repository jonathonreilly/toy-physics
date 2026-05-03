#!/usr/bin/env python3
"""
PR #230 non-source response rank-repair sufficiency theorem.

Source-only FH/LSZ fixes one linear response row in the neutral scalar sector.
This runner records the exact linear-algebra repair: closure needs either
pole-level source-Higgs purity O_sp = +/- O_H, or an independent non-source
response row plus identity certificates strong enough to remove the orthogonal
top-coupling null direction.  Current PR #230 rows do not yet supply either.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_non_source_response_rank_repair_sufficiency_2026-05-03.json"

PARENTS = {
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "neutral_scalar_top_coupling_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
    "source_higgs_cross_correlator_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_purity_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "wz_response_certificate_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def dot(lhs: list[float], rhs: list[float]) -> float:
    return sum(a * b for a, b in zip(lhs, rhs))


def det2(rows: list[list[float]]) -> float:
    return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]


def rank2(rows: list[list[float]]) -> int:
    if not rows:
        return 0
    if len(rows) == 1:
        return 0 if all(abs(x) < 1.0e-14 for x in rows[0]) else 1
    return 2 if abs(det2(rows[:2])) > 1.0e-12 else 1


def solve2(rows: list[list[float]], values: list[float]) -> list[float]:
    determinant = det2(rows)
    if abs(determinant) <= 1.0e-12:
        return [float("nan"), float("nan")]
    a, b = rows[0]
    c, d = rows[1]
    y0 = (values[0] * d - b * values[1]) / determinant
    y1 = (a * values[1] - values[0] * c) / determinant
    return [y0, y1]


def linear_algebra_certificate() -> dict[str, Any]:
    source_row = [0.8, 0.6]
    true_top_couplings = [0.92, -0.31]
    source_response = dot(source_row, true_top_couplings)
    null_direction = [source_row[1], -source_row[0]]
    variants = []
    for lam in [-0.5, 0.0, 0.4]:
        couplings = [
            true_top_couplings[0] + lam * null_direction[0],
            true_top_couplings[1] + lam * null_direction[1],
        ]
        variants.append(
            {
                "lambda": lam,
                "top_coupling_vector_basis_OH_Ochi": couplings,
                "canonical_higgs_y_t": couplings[0],
                "orthogonal_scalar_top_coupling": couplings[1],
                "same_source_response": dot(source_row, couplings),
            }
        )

    canonical_row = [1.0, 0.0]
    independent_rows = [source_row, canonical_row]
    recovered = solve2(independent_rows, [source_response, true_top_couplings[0]])
    purity_row = [1.0, 0.0]
    purity_source_response = dot(purity_row, true_top_couplings)
    responses = [row["same_source_response"] for row in variants]
    y_values = [row["canonical_higgs_y_t"] for row in variants]
    return {
        "basis": ["O_H_canonical", "O_chi_orthogonal"],
        "source_overlap_row": source_row,
        "source_only_rank": rank2([source_row]),
        "required_rank_without_purity": 2,
        "null_direction": null_direction,
        "source_only_counterfamily": variants,
        "source_response_span": max(responses) - min(responses),
        "canonical_y_span": max(y_values) - min(y_values),
        "rank_repair_by_independent_canonical_row": {
            "row": canonical_row,
            "rank": rank2(independent_rows),
            "determinant": det2(independent_rows),
            "input_values": [source_response, true_top_couplings[0]],
            "recovered_top_coupling_vector": recovered,
            "recovery_error_norm": math.sqrt(
                sum((a - b) ** 2 for a, b in zip(recovered, true_top_couplings))
            ),
        },
        "rank_repair_by_purity": {
            "condition": "O_sp = +/- O_H, equivalently |rho_spH| = 1 and Delta_spH = 0 at the isolated pole",
            "effective_source_overlap_row": purity_row,
            "source_response_equals_canonical_y_t": abs(purity_source_response - true_top_couplings[0]) < 1.0e-14,
        },
        "wz_response_sufficiency_condition": {
            "generic_wz_slope_alone_sufficient": False,
            "required_identity": (
                "same-source W/Z row must certify the W/Z mass response is the "
                "canonical-Higgs pole component and that the top response is on "
                "the same one-pole sector, so no orthogonal top-coupling null "
                "direction contributes to dE_top/ds"
            ),
            "ratio_formula_when_identity_passes": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
        },
    }


def main() -> int:
    print("PR #230 non-source response rank-repair sufficiency theorem")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    algebra = linear_algebra_certificate()

    source_pole_operator_ok = (
        parents["legendre_source_pole_operator"].get("source_pole_operator_constructed") is True
        and parents["legendre_source_pole_operator"].get("canonical_higgs_operator_identity_passed") is False
    )
    osp_oh_identity_open = (
        "O_sp-to-O_H identity not derived" in status(parents["osp_oh_identity_stretch"])
        and parents["osp_oh_identity_stretch"].get("proposal_allowed") is False
    )
    source_only_rank_blocked = (
        "neutral scalar top-coupling tomography gate not passed"
        in status(parents["neutral_scalar_top_coupling_tomography"])
        and parents["neutral_scalar_top_coupling_tomography"].get("gate_passed") is False
    )
    source_higgs_rows_absent = (
        "source-Higgs cross-correlator rows absent"
        in status(parents["source_higgs_cross_correlator_builder"])
        and parents["source_higgs_cross_correlator_builder"].get("input_present") is False
    )
    source_higgs_purity_open = (
        "O_sp-Higgs Gram-purity postprocess awaiting production certificate"
        in status(parents["source_higgs_gram_purity_postprocessor"])
        and parents["source_higgs_gram_purity_postprocessor"].get("osp_higgs_gram_purity_gate_passed")
        is False
    )
    canonical_operator_absent = (
        "canonical-Higgs operator certificate absent"
        in status(parents["canonical_higgs_operator_gate"])
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    wz_rows_absent = (
        "same-source WZ response rows absent" in status(parents["wz_response_certificate_builder"])
        and parents["wz_response_certificate_builder"].get("input_present") is False
    )
    wz_gate_open = (
        "same-source WZ response certificate gate not passed"
        in status(parents["same_source_wz_response_gate"])
        and parents["same_source_wz_response_gate"].get("same_source_wz_response_certificate_gate_passed")
        is False
    )
    retained_still_open = (
        "closure not yet reached" in status(parents["retained_closure_route"])
        and parents["retained_closure_route"].get("proposal_allowed") is False
    )
    source_only_counterfamily_valid = (
        algebra["source_only_rank"] == 1
        and algebra["source_response_span"] < 1.0e-14
        and algebra["canonical_y_span"] > 0.1
    )
    independent_row_repairs_rank = (
        algebra["rank_repair_by_independent_canonical_row"]["rank"] == 2
        and algebra["rank_repair_by_independent_canonical_row"]["recovery_error_norm"] < 1.0e-12
    )
    purity_repairs_rank_need = algebra["rank_repair_by_purity"]["source_response_equals_canonical_y_t"] is True

    current_closure_gate_passed = False
    theorem_passed = (
        not missing
        and not proposal_allowed
        and source_pole_operator_ok
        and source_only_counterfamily_valid
        and independent_row_repairs_rank
        and purity_repairs_rank_need
        and algebra["wz_response_sufficiency_condition"]["generic_wz_slope_alone_sufficient"] is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-pole-operator-available-but-not-oh", source_pole_operator_ok, status(parents["legendre_source_pole_operator"]))
    report("osp-oh-identity-still-open", osp_oh_identity_open, status(parents["osp_oh_identity_stretch"]))
    report("source-only-tomography-rank-blocked", source_only_rank_blocked, status(parents["neutral_scalar_top_coupling_tomography"]))
    report("source-higgs-production-rows-absent", source_higgs_rows_absent, status(parents["source_higgs_cross_correlator_builder"]))
    report("source-higgs-purity-open", source_higgs_purity_open, status(parents["source_higgs_gram_purity_postprocessor"]))
    report("canonical-oh-certificate-absent", canonical_operator_absent, status(parents["canonical_higgs_operator_gate"]))
    report("wz-production-rows-absent", wz_rows_absent, status(parents["wz_response_certificate_builder"]))
    report("wz-gate-still-open", wz_gate_open, status(parents["same_source_wz_response_gate"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_closure_route"]))
    report("source-only-null-direction-witness", source_only_counterfamily_valid, f"canonical_y_span={algebra['canonical_y_span']}")
    report("independent-non-source-row-repairs-rank", independent_row_repairs_rank, str(algebra["rank_repair_by_independent_canonical_row"]))
    report("pole-gram-purity-repairs-rank-need", purity_repairs_rank_need, str(algebra["rank_repair_by_purity"]))
    report("generic-wz-slope-alone-not-sufficient", not algebra["wz_response_sufficiency_condition"]["generic_wz_slope_alone_sufficient"], "identity certificates required")
    report("rank-repair-theorem-passed", theorem_passed, f"theorem_passed={theorem_passed}")
    report("current-closure-gate-not-passed", not current_closure_gate_passed, f"current_closure_gate_passed={current_closure_gate_passed}")

    result = {
        "actual_current_surface_status": "exact-support / non-source response rank-repair sufficiency theorem; current rows absent",
        "verdict": (
            "The exact repair to the PR #230 source-only null direction is now "
            "executable.  O_sp normalization removes source-coordinate units, "
            "but a source-only response row has rank one and leaves the canonical "
            "Higgs top-coupling component variable.  Pole-level O_sp-Higgs Gram "
            "purity closes by proving O_sp = +/- O_H.  Otherwise an independent "
            "non-source response row closes only when its identity certificates "
            "remove the orthogonal top-coupling null direction.  The current "
            "surface supplies neither source-Higgs production pole rows nor "
            "same-source W/Z response rows, so no closure is authorized."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is an exact sufficiency theorem and acceptance surface; the required non-source production rows and identity gates remain absent.",
        "bare_retained_allowed": False,
        "rank_repair_sufficiency_theorem_passed": theorem_passed,
        "current_closure_gate_passed": current_closure_gate_passed,
        "linear_algebra_certificate": algebra,
        "current_missing_rank_repairs": [
            "pole-level O_sp-Higgs Gram purity with certified canonical O_H",
            "same-source W/Z mass-response rows from correlator fits",
            "same-source sector-overlap identity for the W/Z route",
            "canonical-Higgs pole identity certificate",
            "retained-route gate authorization",
        ],
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, observed W/Z masses, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
            "does not treat generic W/Z slope data as sufficient without sector-overlap and canonical-Higgs identity certificates",
        ],
        "exact_next_action": (
            "Produce one of the rank-repair inputs: certified O_H with "
            "production C_sH/C_HH pole rows passing O_sp-Higgs Gram purity, or "
            "production same-source W/Z mass-response rows with sector-overlap "
            "and canonical-Higgs identity certificates."
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
