#!/usr/bin/env python3
"""
PR #230 FH/LSZ model-class semantic firewall.

This stress-tests the scalar-LSZ model-class gate so a future finite-shell
pole-fit certificate cannot promote chunk output with a shallow
model_class_gate_passed boolean, Ward/H_unit authority, observed selectors, or
implicit kappa/matching shortcuts.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATE_SCRIPT = ROOT / "scripts" / "frontier_yt_fh_lsz_pole_fit_model_class_gate.py"
GATE_OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json"

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


def load_gate_module() -> Any:
    spec = importlib.util.spec_from_file_location("model_gate", GATE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load FH/LSZ model-class gate module")
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
        "certificate_kind": "fh_lsz_pole_fit_model_class",
        "model_class_gate_passed": True,
        "model_class_certificate_kind": "analytic_continuation_theorem",
        "model_class_reference": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
        "finite_shell_deformations_excluded": True,
        "scalar_pole_isolated": True,
        "derivative_identifier": "dGamma_ss_dp_hat_sq_at_pole",
        "fv_ir_zero_mode_control_passed": True,
        "threshold_or_denominator_control_passed": True,
        "proposal_allowed": False,
        "firewall": {
            "used_observed_targets_as_selectors": False,
            "used_hunit_or_ward_authority": False,
            "used_alpha_lm_or_plaquette": False,
            "set_kappa_c2_zmatch_equal_one": False,
        },
    }


def reject_case(name: str, candidate: dict[str, Any], gate: Any) -> dict[str, Any]:
    checks = gate.validate_model_class_certificate(candidate)
    failed_checks = [key for key, ok in checks.items() if not ok]
    rejected = bool(failed_checks)
    report(name, rejected, f"failed_checks={failed_checks}")
    return {"case": name, "rejected": rejected, "failed_checks": failed_checks}


def main() -> int:
    print("PR #230 FH/LSZ model-class semantic firewall")
    print("=" * 72)

    gate = load_gate_module()
    gate_output = load_json(GATE_OUTPUT)
    gate_open = (
        "model-class gate blocks" in gate_output.get("actual_current_surface_status", "")
        and gate_output.get("proposal_allowed") is False
        and gate_output.get("model_class_gate_passed") is False
    )
    stronger_schema = all(
        key in gate.validate_model_class_certificate(base_candidate())
        for key in (
            "certificate_kind_allowed",
            "model_class_reference_not_shortcut",
            "finite_shell_deformations_excluded",
            "fv_ir_zero_mode_control_passed",
            "threshold_or_denominator_control_passed",
            "no_kappa_or_matching_shortcut",
        )
    )

    report("gate-module-loaded", True, str(GATE_SCRIPT.relative_to(ROOT)))
    report("current-model-class-gate-open", gate_open, str(GATE_OUTPUT.relative_to(ROOT)))
    report("stronger-schema-checks-present", stronger_schema, "semantic checks in validate_model_class_certificate")

    cases: list[dict[str, Any]] = []
    cases.append(reject_case("reject-static-ew-reference", base_candidate(), gate))

    ward = base_candidate()
    ward["model_class_reference"] = "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
    ward["firewall"]["used_hunit_or_ward_authority"] = True
    cases.append(reject_case("reject-ward-model-class-import", ward, gate))

    self_declared = base_candidate()
    self_declared["model_class_certificate_kind"] = "self_declared_boolean"
    self_declared["finite_shell_deformations_excluded"] = False
    cases.append(reject_case("reject-self-declared-model-class", self_declared, gate))

    no_fv_ir = base_candidate()
    no_fv_ir["fv_ir_zero_mode_control_passed"] = False
    no_fv_ir["threshold_or_denominator_control_passed"] = False
    cases.append(reject_case("reject-no-fv-ir-threshold-control", no_fv_ir, gate))

    target_selector = base_candidate()
    target_selector["firewall"]["used_observed_targets_as_selectors"] = True
    cases.append(reject_case("reject-observed-target-selector", target_selector, gate))

    shortcut = base_candidate()
    shortcut["firewall"]["set_kappa_c2_zmatch_equal_one"] = True
    cases.append(reject_case("reject-kappa-c2-zmatch-shortcut", shortcut, gate))

    proposal = base_candidate()
    proposal["proposal_allowed"] = True
    cases.append(reject_case("reject-candidate-authorized-proposal", proposal, gate))

    all_spoofs_rejected = all(row["rejected"] for row in cases)
    report("all-spoof-candidates-rejected", all_spoofs_rejected, f"cases={len(cases)}")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ model-class semantic firewall passed",
        "verdict": (
            "The FH/LSZ model-class gate now rejects semantic spoof candidates "
            "that try to promote finite-shell pole fits with static EW algebra, "
            "Ward/H_unit authority, self-declared model-class booleans, missing "
            "FV/IR/threshold control, observed selectors, or kappa/c2/Z_match "
            "shortcuts.  This is overclaim protection only; no scalar LSZ "
            "model-class certificate is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The firewall hardens a future scalar-LSZ model-class gate; it does not provide the missing scalar denominator or pole-saturation theorem.",
        "bare_retained_allowed": False,
        "gate_output": str(GATE_OUTPUT.relative_to(ROOT)),
        "gate_open": gate_open,
        "stronger_schema": stronger_schema,
        "spoof_cases": cases,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not provide scalar LSZ normalization",
            "does not accept finite-shell fits as physical pole residues",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette/u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "A future model-class certificate must provide a non-shortcut "
            "analytic-continuation, pole-saturation, continuum-threshold, or "
            "microscopic scalar-denominator theorem plus FV/IR/zero-mode control "
            "before chunk pole fits can be load-bearing."
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
