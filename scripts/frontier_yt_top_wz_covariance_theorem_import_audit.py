#!/usr/bin/env python3
"""
PR #230 top/W covariance-theorem import audit.

This runner closes a narrow W/Z shortcut after the marginal, native-label
factorization, and deterministic-W covariance gates: can an existing current
branch artifact already be imported as the strict same-surface product-measure,
conditional-independence, or closed-covariance theorem needed to avoid matched
top/W rows?

Current answer: no.  The current PR230 artifacts are builders, gates, scout
schemas, support theorems, or no-go certificates.  None is a production/theorem
surface that fixes cov_dE_top_dM_W on the same top/W source surface.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_top_wz_covariance_theorem_import_audit_2026-05-05.json"
FUTURE_THEOREM = ROOT / "outputs" / "yt_top_wz_closed_covariance_theorem_2026-05-05.json"

PARENTS = {
    "top_wz_covariance_marginal_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_factorization_independence_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_wz_deterministic_response_covariance_gate": "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
}

SCOUT_OR_SHORTCUT_OUTPUTS = {
    "factorization_scout": "outputs/yt_top_wz_factorization_independence_gate_scout_certificate_2026-05-05.json",
    "deterministic_scout": "outputs/yt_top_wz_deterministic_response_covariance_gate_scout_certificate_2026-05-05.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_observed_WZ_masses_as_selector",
    "used_observed_g2_as_selector",
    "used_H_unit_or_Ward_authority",
    "used_alpha_lm_plaquette_or_u0",
    "used_c2_or_zmatch_equal_one",
    "used_kappa_or_cos_theta_by_fiat",
    "synthesized_matched_response_rows",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def path_ref_ok(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(("docs/", "outputs/", "scripts/")) and (ROOT / value).exists()


def validate_theorem(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "failed_checks": ["closed covariance theorem artifact absent"],
            "checks": {},
        }

    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    certificates = candidate.get("certificates", {}) if isinstance(candidate.get("certificates"), dict) else {}
    mechanisms = {
        "product_measure_factorization": candidate.get("product_measure_factorization_proved") is True,
        "conditional_independence": candidate.get("conditional_independence_proved") is True,
        "closed_covariance_formula": candidate.get("closed_covariance_formula_proved") is True
        and finite(candidate.get("cov_dE_top_dM_W")),
    }
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "top_wz_joint_covariance_theorem",
        "phase_supported": candidate.get("phase") in {"theorem", "production"},
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "three_spatial_plus_derived_time": candidate.get("three_spatial_plus_derived_time") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "same_surface_top_w_scope": candidate.get("same_surface_top_w_scope") is True,
        "one_joint_covariance_mechanism": any(mechanisms.values()),
        "finite_covariance_if_formula": (
            finite(candidate.get("cov_dE_top_dM_W"))
            if candidate.get("closed_covariance_formula_proved") is True
            else True
        ),
        "top_response_identity_ref": path_ref_ok(certificates.get("top_response_identity_certificate")),
        "w_response_or_mass_fit_ref": path_ref_ok(certificates.get("w_response_or_mass_fit_certificate")),
        "same_source_ew_action_ref": path_ref_ok(certificates.get("same_source_ew_action_certificate")),
        "sector_or_canonical_higgs_ref": path_ref_ok(
            certificates.get("sector_or_canonical_higgs_identity_certificate")
        ),
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    checks.update({f"forbidden_{field}_false": firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS})
    failed = [name for name, ok in checks.items() if not ok]
    return {
        "present": True,
        "valid": not failed,
        "checks": checks,
        "mechanisms": mechanisms,
        "failed_checks": failed,
    }


def candidate_rows(parents: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "id": "matched_covariance_builder",
            "path": PARENTS["top_wz_matched_covariance_builder"],
            "classification": "builder / open",
            "importable_as_joint_covariance_theorem": False,
            "reason": "strict matched top/W response rows are absent; builder writes no production covariance certificate",
        },
        {
            "id": "marginal_covariance_no_go",
            "path": PARENTS["top_wz_covariance_marginal_no_go"],
            "classification": "exact negative boundary",
            "importable_as_joint_covariance_theorem": False,
            "reason": "proves covariance is not derivable from separate top and W marginals",
        },
        {
            "id": "factorization_independence_gate",
            "path": PARENTS["top_wz_factorization_independence_gate"],
            "classification": "exact negative boundary / absent theorem gate",
            "importable_as_joint_covariance_theorem": False,
            "reason": "current mode finds no production product-measure, conditional-independence, or closed covariance theorem",
        },
        {
            "id": "factorization_independence_scout_certificate",
            "path": SCOUT_OR_SHORTCUT_OUTPUTS["factorization_scout"],
            "classification": "scout schema",
            "importable_as_joint_covariance_theorem": False,
            "reason": "synthetic scout certificate validates schema only and is not production/theorem authority",
        },
        {
            "id": "deterministic_response_covariance_gate",
            "path": PARENTS["top_wz_deterministic_response_covariance_gate"],
            "classification": "exact negative boundary / absent certificate gate",
            "importable_as_joint_covariance_theorem": False,
            "reason": "deterministic W response alone does not fix top/W covariance",
        },
        {
            "id": "deterministic_response_scout_certificate",
            "path": SCOUT_OR_SHORTCUT_OUTPUTS["deterministic_scout"],
            "classification": "scout schema",
            "importable_as_joint_covariance_theorem": False,
            "reason": "synthetic scout certificate is not a production covariance theorem",
        },
        {
            "id": "same_source_top_response_builder",
            "path": PARENTS["same_source_top_response_builder"],
            "classification": "builder / open",
            "importable_as_joint_covariance_theorem": False,
            "reason": "top-response support is not paired top/W covariance authority",
        },
        {
            "id": "same_source_w_decomposition",
            "path": PARENTS["same_source_w_response_decomposition"],
            "classification": "exact support / W decomposition",
            "importable_as_joint_covariance_theorem": False,
            "reason": "W-response decomposition does not determine the joint top/W law",
        },
        {
            "id": "same_source_w_row_builder",
            "path": PARENTS["same_source_w_response_row_builder"],
            "classification": "builder / open",
            "importable_as_joint_covariance_theorem": False,
            "reason": "strict W rows and paired top/W rows are absent",
        },
        {
            "id": "same_source_ew_action_gate",
            "path": PARENTS["wz_same_source_ew_action_gate"],
            "classification": "exact negative boundary",
            "importable_as_joint_covariance_theorem": False,
            "reason": "same-source EW action is absent on the current PR230 surface",
        },
        {
            "id": "sector_overlap_obstruction",
            "path": PARENTS["same_source_sector_overlap"],
            "classification": "obstruction",
            "importable_as_joint_covariance_theorem": False,
            "reason": "sector-overlap identity remains open and cannot fix top/W covariance",
        },
    ]
    for row in rows:
        cert = load_rel(str(row["path"]))
        row["path_exists"] = bool(cert) or (ROOT / str(row["path"])).exists()
        row["actual_current_surface_status"] = status(cert)
    return rows


def main() -> int:
    print("PR #230 top/W covariance-theorem import audit")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}
    future_candidate = load_json(FUTURE_THEOREM)
    validation = validate_theorem(future_candidate)
    rows = candidate_rows(parents)

    marginal_no_go_loaded = (
        "matched top-W covariance not derivable from marginal response support"
        in statuses["top_wz_covariance_marginal_no_go"]
        and parents["top_wz_covariance_marginal_no_go"].get("marginal_derivation_no_go_passed") is True
    )
    factorization_gate_blocks = (
        "same-source top-W factorization not derived"
        in statuses["top_wz_factorization_independence_gate"]
        and parents["top_wz_factorization_independence_gate"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False
    )
    deterministic_gate_blocks = (
        "deterministic W response covariance shortcut not derived"
        in statuses["top_wz_deterministic_response_covariance_gate"]
        and parents["top_wz_deterministic_response_covariance_gate"].get(
            "strict_deterministic_response_covariance_gate_passed"
        )
        is False
    )
    matched_builder_open = (
        "matched top-W" in statuses["top_wz_matched_covariance_builder"]
        and parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    no_importable_candidate = not [row for row in rows if row["importable_as_joint_covariance_theorem"]]
    future_theorem_absent = not FUTURE_THEOREM.exists()
    import_audit_passed = (
        not missing
        and not proposal_allowed
        and marginal_no_go_loaded
        and factorization_gate_blocks
        and deterministic_gate_blocks
        and matched_builder_open
        and no_importable_candidate
        and future_theorem_absent
        and not validation["valid"]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("marginal-covariance-no-go-loaded", marginal_no_go_loaded, statuses["top_wz_covariance_marginal_no_go"])
    report("factorization-independence-gate-blocks", factorization_gate_blocks, statuses["top_wz_factorization_independence_gate"])
    report("deterministic-response-gate-blocks", deterministic_gate_blocks, statuses["top_wz_deterministic_response_covariance_gate"])
    report("matched-covariance-builder-open", matched_builder_open, statuses["top_wz_matched_covariance_builder"])
    report("future-closed-covariance-theorem-absent", future_theorem_absent, display(FUTURE_THEOREM))
    report("future-theorem-validation-not-passing", not validation["valid"], f"failed={validation['failed_checks']}")
    report("candidate-surfaces-classified", len(rows) >= 8, f"candidates={len(rows)}")
    report("no-importable-current-covariance-theorem", no_importable_candidate, "all candidates classified as support/gate/scout/no-go/open")
    report("covariance-theorem-import-audit-passed", import_audit_passed, "current branch has no admissible joint covariance theorem")

    result = {
        "actual_current_surface_status": "exact negative boundary / no importable same-surface top-W covariance theorem on current PR230 surface",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current branch contains W/Z support builders, gates, scout schemas, "
            "and no-go certificates, but no production/theorem artifact that proves "
            "product-measure factorization, conditional independence, or a closed "
            "same-surface cov_dE_top_dM_W formula."
        ),
        "bare_retained_allowed": False,
        "covariance_theorem_import_audit_passed": import_audit_passed,
        "future_closed_covariance_theorem": display(FUTURE_THEOREM),
        "future_closed_covariance_theorem_present": FUTURE_THEOREM.exists(),
        "future_theorem_validation": validation,
        "candidate_surfaces": rows,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not create matched top/W response rows",
            "does not convert scout certificates into production theorem authority",
            "does not use observed W/Z/top/y_t/g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, c2=1, Z_match=1, kappa_s=1, or cos(theta)=1",
            "does not package or rerun chunk MC",
        ],
        "exact_next_action": (
            "Supply a real same-surface top/W joint covariance theorem at "
            "outputs/yt_top_wz_closed_covariance_theorem_2026-05-05.json, "
            "or supply measured matched top/W response rows.  Do not import "
            "builders, scout schemas, support-only W decompositions, or no-go "
            "gates as covariance authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
