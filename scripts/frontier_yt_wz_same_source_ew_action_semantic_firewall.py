#!/usr/bin/env python3
"""
PR #230 same-source EW action semantic firewall.

This stress-tests the future W/Z same-source EW action certificate builder.
A syntactically filled action candidate must not be able to smuggle in static
EW algebra, the current QCD/top harness, observed selectors, H_unit/Ward
authority, or self-declared certificate references as a same-source
SU(2)xU(1)/Higgs production action.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUILDER_SCRIPT = ROOT / "scripts" / "frontier_yt_wz_same_source_ew_action_certificate_builder.py"
BUILDER_OUTPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json"
ACTION_GATE_OUTPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_gate_2026-05-04.json"
OUTPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json"

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


def load_builder_module() -> Any:
    spec = importlib.util.spec_from_file_location("wz_action_builder", BUILDER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load W/Z same-source EW action builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def base_candidate() -> dict[str, Any]:
    return {
        "certificate_kind": "same_source_ew_action",
        "phase": "production_design",
        "same_surface_cl3_z3": True,
        "same_source_coordinate": True,
        "source_coordinate": "s_top_fh_lsz",
        "fields": {
            "su2_link_field": True,
            "u1_link_field": True,
            "dynamic_higgs_doublet": True,
            "higgs_radial_mode": "O_H_radial",
        },
        "action_terms": {
            "su2_wilson_action": True,
            "u1_gauge_action": True,
            "gauge_covariant_higgs_kinetic": True,
            "higgs_potential": True,
        },
        "source_coupling": {
            "couples_to": "centered_phi_dagger_phi",
            "operator_centered": True,
            "matches_top_fh_lsz_source_coordinate": True,
        },
        "observables": {
            "wz_two_point_correlators": True,
            "wz_mass_fit_method": "future production W/Z correlator effective-mass fit",
        },
        "certificates": {
            "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
            "higgs_mass_source_action_bridge_kind": "higgs_mass_source_action_bridge",
            "canonical_higgs_operator_certificate": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
            "canonical_higgs_operator_certificate_kind": "canonical_higgs_identity_theorem",
            "same_source_sector_overlap_certificate": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
            "same_source_sector_overlap_certificate_kind": "same_source_sector_overlap_identity",
            "wz_correlator_mass_fit_path_certificate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
            "wz_correlator_mass_fit_path_certificate_kind": "production_wz_correlator_mass_fit_path",
        },
        "proposal_allowed": False,
        "firewall": {
            "used_hunit_matrix_element_readout": False,
            "used_hunit_as_operator": False,
            "used_yt_ward_identity": False,
            "used_observed_masses_or_couplings_as_selectors": False,
            "used_static_ew_algebra_as_measurement": False,
            "used_alpha_lm_or_plaquette_u0": False,
            "set_kappa_s_equal_one": False,
            "set_cos_theta_equal_one": False,
            "set_c2_equal_one": False,
            "set_z_match_equal_one": False,
        },
    }


def reject_case(name: str, candidate: dict[str, Any], builder: Any) -> dict[str, Any]:
    validation = builder.validate_action_certificate(candidate)
    failed_checks = list(validation.get("reasons", []))
    rejected = validation.get("valid") is False and bool(failed_checks)
    report(name, rejected, f"failed_checks={failed_checks}")
    return {
        "case": name,
        "rejected": rejected,
        "failed_checks": failed_checks,
    }


def main() -> int:
    print("PR #230 same-source EW action semantic firewall")
    print("=" * 72)

    builder = load_builder_module()
    builder_output = load_json(BUILDER_OUTPUT)
    action_gate_output = load_json(ACTION_GATE_OUTPUT)
    check_names = set(builder.validate_action_certificate(base_candidate()).get("checks", {}))
    stronger_schema = all(
        key in check_names
        for key in (
            "canonical_higgs_certificate_not_shortcut",
            "canonical_higgs_certificate_kind_allowed",
            "higgs_mass_source_action_bridge_reference",
            "higgs_mass_source_action_bridge_kind_allowed",
            "sector_overlap_certificate_not_shortcut",
            "sector_overlap_certificate_kind_allowed",
            "wz_mass_fit_path_certificate_not_shortcut",
            "wz_mass_fit_path_certificate_kind_allowed",
        )
    )
    current_builder_open = (
        "same-source EW action certificate absent"
        in builder_output.get("actual_current_surface_status", "")
        and builder_output.get("proposal_allowed") is False
        and builder_output.get("same_source_ew_action_certificate_valid") is False
    )
    current_action_gate_open = (
        "same-source EW action not defined" in action_gate_output.get("actual_current_surface_status", "")
        and action_gate_output.get("proposal_allowed") is False
        and action_gate_output.get("same_source_ew_action_ready") is False
    )

    report("builder-module-loaded", True, str(BUILDER_SCRIPT.relative_to(ROOT)))
    report("current-builder-output-open", current_builder_open, str(BUILDER_OUTPUT.relative_to(ROOT)))
    report("current-action-gate-open", current_action_gate_open, str(ACTION_GATE_OUTPUT.relative_to(ROOT)))
    report("stronger-schema-checks-present", stronger_schema, "semantic non-shortcut checks in validate_action_certificate")

    cases: list[dict[str, Any]] = []
    cases.append(reject_case("reject-static-ew-canonical-higgs-reference", base_candidate(), builder))

    qcd_harness = base_candidate()
    qcd_harness["certificates"]["wz_correlator_mass_fit_path_certificate"] = "scripts/yt_direct_lattice_correlator_production.py"
    cases.append(reject_case("reject-current-qcd-top-harness-reference", qcd_harness, builder))

    obstruction_refs = base_candidate()
    obstruction_refs["certificates"]["canonical_higgs_operator_certificate"] = (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    )
    cases.append(reject_case("reject-gate-output-as-identity-certificate", obstruction_refs, builder))

    observed_selector = base_candidate()
    observed_selector["firewall"]["used_observed_masses_or_couplings_as_selectors"] = True
    cases.append(reject_case("reject-observed-mass-coupling-selector", observed_selector, builder))

    ward_hunit = base_candidate()
    ward_hunit["firewall"]["used_hunit_as_operator"] = True
    ward_hunit["firewall"]["used_yt_ward_identity"] = True
    cases.append(reject_case("reject-hunit-ward-authority", ward_hunit, builder))

    self_declared = base_candidate()
    self_declared["certificates"]["canonical_higgs_operator_certificate_kind"] = "self_declared_boolean"
    self_declared["certificates"]["same_source_sector_overlap_certificate_kind"] = "self_declared_boolean"
    self_declared["certificates"]["wz_correlator_mass_fit_path_certificate_kind"] = "self_declared_boolean"
    cases.append(reject_case("reject-self-declared-certificate-kinds", self_declared, builder))

    proposal_candidate = base_candidate()
    proposal_candidate["proposal_allowed"] = True
    cases.append(reject_case("reject-candidate-local-proposal-authorization", proposal_candidate, builder))

    all_spoofs_rejected = all(row["rejected"] for row in cases)
    report("all-spoof-candidates-rejected", all_spoofs_rejected, f"cases={len(cases)}")

    result = {
        "actual_current_surface_status": "bounded-support / same-source EW action semantic firewall passed",
        "verdict": (
            "The same-source EW action certificate builder now rejects semantic "
            "spoof candidates that try to use static EW algebra, the current "
            "QCD/top harness, gate/obstruction outputs, observed selectors, "
            "H_unit/Ward authority, self-declared certificate kinds, or "
            "candidate-local proposal authorization.  This is overclaim "
            "protection only; no EW action block or W/Z row is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The firewall hardens a future W/Z same-source action contract; it "
            "does not provide same-source EW dynamics, W/Z correlator rows, "
            "sector-overlap identity, canonical-Higgs identity, or retained y_t closure."
        ),
        "bare_retained_allowed": False,
        "builder_output": str(BUILDER_OUTPUT.relative_to(ROOT)),
        "action_gate_output": str(ACTION_GATE_OUTPUT.relative_to(ROOT)),
        "current_builder_open": current_builder_open,
        "current_action_gate_open": current_action_gate_open,
        "stronger_schema": stronger_schema,
        "spoof_cases": cases,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not provide a same-source EW action certificate",
            "does not synthesize W/Z measurement rows",
            "does not treat static EW algebra as dM_W/ds or dM_Z/ds",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            "A future W/Z bypass must supply a real same-source EW action "
            "certificate with non-shortcut identity references, then production "
            "W/Z correlator mass-fit rows, sector-overlap identity, canonical-Higgs "
            "identity, and retained-route approval."
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
