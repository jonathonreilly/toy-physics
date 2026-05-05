#!/usr/bin/env python3
"""
PR #230 W/Z g2 bare-to-low-scale running bridge attempt.

The W/Z physical-response route needs a strict non-observed low-scale
electroweak g2 certificate.  Existing gates reject observed values, package
g2(v), SU(2) generator/Casimir normalization, and response-only
self-normalization.  This runner tests the remaining natural idea: can the
current PR230 surface turn a bare/structural SU(2) coupling into the required
low-scale g2 by beta-function running without importing forbidden scale,
threshold, matching, or EW-action normalizations?

On the current surface the answer is no.  One-loop running is a formula after
the gauge action, scheme, threshold content, and scale ratio are supplied; it
does not supply those premises.  Varying the unprovided scale ratio or finite
matching shift changes the low-scale g2 while leaving the current PR230
structural inputs fixed.
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
    / "yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json"
)
STRICT_G2_CERT = ROOT / "outputs" / "yt_electroweak_g2_certificate_2026-05-04.json"

DOCS = {
    "su2_beta": "docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md",
    "ew_color": "docs/YT_EW_COLOR_PROJECTION_THEOREM.md",
    "ew_higgs_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
}

PARENTS = {
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_generator_casimir_no_go": "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "matching_running_bridge": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FORBIDDEN_INPUTS = [
    "observed g2, observed W/Z mass, observed top mass, or observed y_t",
    "alpha_LM / plaquette / u0 / R_conn package coupling authority",
    "H_unit matrix-element readout",
    "yt_ward_identity",
    "response-only self-normalization",
    "SU(2) generator/Casimir normalization as physical g2",
    "unit c2, Z_match, or kappa_s",
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def one_loop_g2_from_inverse_shift(g0_sq: float, inv_shift: float) -> float:
    inv = 1.0 / g0_sq + inv_shift
    if inv <= 0.0:
        return float("nan")
    return math.sqrt(1.0 / inv)


def running_counterfamily() -> dict[str, Any]:
    # Convention-independent use: the exact coefficient is not load-bearing
    # here.  The point is that any nonzero coefficient leaves g2 dependent on
    # a missing log scale ratio and finite matching/scheme shift.
    g0_sq = 0.25
    beta_abs = 19.0 / 6.0
    coeff = beta_abs / (8.0 * math.pi * math.pi)
    scale_rows = []
    for log_scale_ratio in (-8.0, -2.0, 0.0, 3.0, 8.0):
        inv_shift = coeff * log_scale_ratio
        scale_rows.append(
            {
                "log_scale_ratio": log_scale_ratio,
                "inverse_coupling_shift": inv_shift,
                "g2_low_scale": one_loop_g2_from_inverse_shift(g0_sq, inv_shift),
            }
        )
    scheme_rows = []
    for finite_matching_shift in (-0.08, -0.03, 0.0, 0.04, 0.10):
        scheme_rows.append(
            {
                "finite_matching_shift_in_inverse_g2": finite_matching_shift,
                "g2_low_scale": one_loop_g2_from_inverse_shift(g0_sq, finite_matching_shift),
            }
        )
    g2_values = [row["g2_low_scale"] for row in scale_rows + scheme_rows]
    finite_values = [value for value in g2_values if math.isfinite(value)]
    return {
        "bare_g2_squared": g0_sq,
        "beta_abs_coefficient_used_for_counterfamily": beta_abs,
        "scale_ratio_family": scale_rows,
        "finite_matching_scheme_family": scheme_rows,
        "g2_min": min(finite_values),
        "g2_max": max(finite_values),
        "g2_spread": max(finite_values) - min(finite_values),
        "counterfamily_interpretation": (
            "The same structural bare coupling and one-loop beta coefficient "
            "produce different low-scale g2 values when the unprovided scale "
            "ratio or finite matching shift is changed."
        ),
    }


def bridge_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_source_ew_action",
            "required": "same-source SU(2)xU(1)/Higgs lattice action with gauge kinetic normalization",
            "current_satisfied": False,
        },
        {
            "id": "bare_coupling_boundary_condition",
            "required": "accepted bare electroweak coupling boundary condition in that action",
            "current_satisfied": False,
        },
        {
            "id": "scale_ratio",
            "required": "same-surface relation between lattice cutoff/renormalization scale and the physical readout scale",
            "current_satisfied": False,
        },
        {
            "id": "threshold_content",
            "required": "field content and threshold ordering for running from the bare scale to readout scale",
            "current_satisfied": False,
        },
        {
            "id": "finite_matching_scheme",
            "required": "scheme and finite matching constants for converting action coupling to g2(v)",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "no observed values, package alpha/plaquette/u0/R_conn, H_unit, Ward, or unit normalizations",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 W/Z g2 bare-to-low-scale running bridge attempt")
    print("=" * 72)

    docs = {name: read_rel(path) for name, path in DOCS.items()}
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_docs = [name for name, text in docs.items() if not text]
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    contract = bridge_contract()
    missing_contract = [row["id"] for row in contract if not row["current_satisfied"]]
    counter = running_counterfamily()

    su2_beta_structural_only = (
        "1-loop" in docs["su2_beta"]
        and ("does NOT claim" in docs["su2_beta"] or "open Science Lane" in docs["su2_beta"])
    )
    bare_g2_candidate_present = "g_2^2" in docs["ew_color"] and "1/4" in docs["ew_color"]
    ew_mass_static_dictionary = (
        "M_W = g_2 v / 2" in docs["ew_higgs_mass"]
        and "Assume a neutral Higgs vacuum" in docs["ew_higgs_mass"]
    )
    minimal_axioms_not_ew_action = (
        "g_bare = 1" in docs["minimal_axioms"]
        and "staggered-Dirac partition" in docs["minimal_axioms"]
    )
    strict_cert_absent = not STRICT_G2_CERT.exists()
    g2_builder_rejects_bare_route = any(
        candidate.get("name") == "bare_geometry_g2_squared_one_quarter"
        and candidate.get("accepted") is False
        for candidate in parents["electroweak_g2_builder"].get("candidate_authorities", [])
    )
    g2_firewall_open = (
        "WZ response g2 authority absent" in status(parents["wz_g2_authority_firewall"])
        and parents["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False
    )
    same_source_ew_action_absent = (
        "same-source EW action not defined" in status(parents["wz_same_source_ew_action_gate"])
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    matching_running_open = (
        "matching-running bridge awaits certified physical input"
        in status(parents["matching_running_bridge"])
        and parents["matching_running_bridge"].get("matching_running_bridge_passed") is False
    )
    response_self_normalization_blocked = (
        parents["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
    )
    generator_casimir_blocked = (
        parents["wz_g2_generator_casimir_no_go"].get("g2_generator_casimir_no_go_passed")
        is True
    )
    row_builder_g2_absent = (
        "electroweak g2 certificate absent"
        in parents["wz_mass_fit_response_row_builder"].get("g2_validation", {}).get(
            "failed_checks", []
        )
    )
    counterfamily_passed = counter["g2_spread"] > 1.0e-3
    wz_g2_bare_running_bridge_passed = False
    strict_certificate_written = False
    exact_negative_boundary_passed = (
        not missing_docs
        and not missing_parents
        and not proposal_allowed
        and su2_beta_structural_only
        and bare_g2_candidate_present
        and ew_mass_static_dictionary
        and minimal_axioms_not_ew_action
        and strict_cert_absent
        and g2_builder_rejects_bare_route
        and g2_firewall_open
        and same_source_ew_action_absent
        and matching_running_open
        and response_self_normalization_blocked
        and generator_casimir_blocked
        and row_builder_g2_absent
        and counterfamily_passed
        and not wz_g2_bare_running_bridge_passed
        and not strict_certificate_written
    )

    report("support-documents-present", not missing_docs, f"missing={missing_docs}")
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("su2-beta-note-structural-only", su2_beta_structural_only, DOCS["su2_beta"])
    report("bare-g2-candidate-present", bare_g2_candidate_present, DOCS["ew_color"])
    report("ew-mass-note-static-dictionary", ew_mass_static_dictionary, DOCS["ew_higgs_mass"])
    report("minimal-axioms-not-ew-action", minimal_axioms_not_ew_action, DOCS["minimal_axioms"])
    report("strict-g2-certificate-absent", strict_cert_absent, str(STRICT_G2_CERT.relative_to(ROOT)))
    report("g2-builder-rejects-bare-route", g2_builder_rejects_bare_route, status(parents["electroweak_g2_builder"]))
    report("g2-authority-firewall-open", g2_firewall_open, status(parents["wz_g2_authority_firewall"]))
    report("same-source-ew-action-absent", same_source_ew_action_absent, status(parents["wz_same_source_ew_action_gate"]))
    report("matching-running-bridge-open", matching_running_open, status(parents["matching_running_bridge"]))
    report("response-self-normalization-blocked", response_self_normalization_blocked, status(parents["wz_g2_response_self_normalization_no_go"]))
    report("generator-casimir-normalization-blocked", generator_casimir_blocked, status(parents["wz_g2_generator_casimir_no_go"]))
    report("wz-row-builder-still-needs-g2", row_builder_g2_absent, status(parents["wz_mass_fit_response_row_builder"]))
    report("bridge-contract-missing-load-bearing-inputs", len(missing_contract) == 5, f"missing={missing_contract}")
    report("running-counterfamily-varies-g2", counterfamily_passed, f"spread={counter['g2_spread']}")
    report("strict-certificate-not-written", not strict_certificate_written, "no g2 certificate emitted")
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "bare-to-low-scale bridge not derivable on current surface")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / WZ g2 bare-to-low-scale running bridge "
            "not derivable on current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-source EW action, accepted "
            "bare coupling boundary condition, scale ratio, threshold content, "
            "finite matching scheme, and forbidden-import firewall certificate "
            "are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current PR230 surface has structural SU(2) beta-function and "
            "bare-coupling candidates, but no same-source EW action, scale "
            "ratio, threshold/matching scheme, or strict g2 certificate.  The "
            "low-scale g2 changes under unprovided running and finite-matching "
            "data."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "wz_g2_bare_running_bridge_passed": wz_g2_bare_running_bridge_passed,
        "strict_electroweak_g2_certificate_written": strict_certificate_written,
        "strict_electroweak_g2_certificate_path": str(STRICT_G2_CERT.relative_to(ROOT)),
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "bridge_contract": contract,
        "missing_bridge_contract": missing_contract,
        "running_and_matching_counterfamily": counter,
        "parent_certificates": PARENTS,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "support_documents": DOCS,
        "forbidden_inputs_checked": FORBIDDEN_INPUTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write the strict electroweak g2 certificate",
            "does not import observed g2, W/Z/top/y_t values, alpha_LM, plaquette, u0, R_conn, H_unit, or Ward authority",
            "does not treat g2^2=1/4, beta-function names, SU2 Casimir data, or package g2(v) as proof authority",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Supply a same-source EW action and strict non-observed g2 running/"
            "matching certificate with scale ratio, threshold content, finite "
            "matching scheme, and firewall fields, then rerun the electroweak "
            "g2 builder, W/Z mass-fit row builder, assembly, retained-route, "
            "and campaign gates."
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
