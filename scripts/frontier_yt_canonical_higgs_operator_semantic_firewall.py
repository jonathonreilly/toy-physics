#!/usr/bin/env python3
"""
PR #230 canonical-Higgs operator semantic firewall.

This runner stress-tests the O_H certificate gate against future spoof
candidates.  It exists because the O_H bridge is now a high-leverage non-chunk
closure route: a syntactically filled candidate must not be able to smuggle in
static EW algebra, H_unit, Ward readout, observed selectors, or a self-declared
identity as a canonical-Higgs operator certificate.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json"
GATE_SCRIPT = ROOT / "scripts" / "frontier_yt_canonical_higgs_operator_certificate_gate.py"
GATE_OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"

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
    spec = importlib.util.spec_from_file_location("oh_gate", GATE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load canonical-Higgs gate module")
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
        "certificate_kind": "canonical_higgs_operator",
        "same_surface_cl3z3": True,
        "same_source_coordinate": True,
        "source_coordinate": "s",
        "operator_id": "O_H_future",
        "operator_definition": "future same-surface gauge-invariant canonical Higgs radial operator",
        "canonical_higgs_operator_identity_passed": True,
        "canonical_higgs_operator_normalization_passed": True,
        "identity_certificate": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
        "identity_certificate_kind": "canonical_higgs_identity_theorem",
        "normalization_certificate": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
        "normalization_certificate_kind": "canonical_higgs_lsz_normalization",
        "source_overlap_closure_mode": "source_higgs_gram_purity",
        "forbidden_shortcut_audit_passed": True,
        "diagonal_vertex": {"kind": "site_color_diagonal_values"},
        "hunit_used_as_operator": False,
        "static_ew_algebra_used_as_operator": False,
        "proposal_allowed": False,
        "firewall": {
            "used_observed_targets_as_selectors": False,
            "used_yt_ward_identity": False,
            "used_alpha_lm_or_plaquette": False,
            "used_hunit_matrix_element_readout": False,
        },
    }


def reject_case(name: str, candidate: dict[str, Any], gate: Any) -> dict[str, Any]:
    checks = gate.validate_candidate(candidate)
    failed_checks = [key for key, ok in checks.items() if not ok]
    rejected = bool(failed_checks)
    report(name, rejected, f"failed_checks={failed_checks}")
    return {
        "case": name,
        "rejected": rejected,
        "failed_checks": failed_checks,
    }


def main() -> int:
    print("PR #230 canonical-Higgs operator semantic firewall")
    print("=" * 72)

    gate = load_gate_module()
    gate_output = load_json(GATE_OUTPUT)
    gate_has_stronger_schema = all(
        token in gate.validate_candidate(base_candidate())
        for token in (
            "identity_certificate_not_shortcut",
            "identity_certificate_kind_allowed",
            "normalization_certificate_not_shortcut",
            "normalization_certificate_kind_allowed",
            "canonical_normalization_passed",
            "source_overlap_closure_mode_allowed",
            "forbidden_shortcut_audit_passed",
        )
    )
    current_gate_open = (
        gate_output.get("actual_current_surface_status") == "open / canonical-Higgs operator certificate absent"
        and gate_output.get("proposal_allowed") is False
    )

    cases: list[dict[str, Any]] = []
    report("gate-module-loaded", True, str(GATE_SCRIPT.relative_to(ROOT)))
    report("current-gate-output-open", current_gate_open, str(GATE_OUTPUT.relative_to(ROOT)))
    report("stronger-schema-checks-present", gate_has_stronger_schema, "semantic checks in validate_candidate")

    static_ew = base_candidate()
    cases.append(reject_case("reject-static-ew-reference", static_ew, gate))

    hunit = base_candidate()
    hunit["identity_certificate"] = "docs/YT_HUNIT_CANONICAL_HIGGS_OPERATOR_CANDIDATE_GATE_NOTE_2026-05-02.md"
    hunit["hunit_used_as_operator"] = True
    cases.append(reject_case("reject-hunit-substitute", hunit, gate))

    ward = base_candidate()
    ward["identity_certificate"] = "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
    ward["firewall"]["used_yt_ward_identity"] = True
    cases.append(reject_case("reject-ward-identity-import", ward, gate))

    self_declared = base_candidate()
    self_declared["identity_certificate_kind"] = "self_declared_boolean"
    self_declared["normalization_certificate_kind"] = "self_declared_boolean"
    self_declared["forbidden_shortcut_audit_passed"] = False
    cases.append(reject_case("reject-self-declared-identity", self_declared, gate))

    observed_selector = base_candidate()
    observed_selector["firewall"]["used_observed_targets_as_selectors"] = True
    cases.append(reject_case("reject-observed-target-selector", observed_selector, gate))

    proposal_candidate = base_candidate()
    proposal_candidate["proposal_allowed"] = True
    cases.append(reject_case("reject-candidate-authorized-proposal", proposal_candidate, gate))

    all_spoofs_rejected = all(row["rejected"] for row in cases)
    report("all-spoof-candidates-rejected", all_spoofs_rejected, f"cases={len(cases)}")

    result = {
        "actual_current_surface_status": "bounded-support / canonical-Higgs operator semantic firewall passed",
        "verdict": (
            "The canonical-Higgs O_H certificate gate now rejects semantic spoof "
            "candidates that would have tried to use static EW algebra, H_unit, "
            "Ward identity, observed selectors, self-declared identity classes, "
            "or candidate-local proposal authorization.  This is overclaim "
            "protection only; no O_H certificate is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The firewall hardens a future O_H gate; it does not provide O_H, C_sH/C_HH rows, or retained y_t closure.",
        "bare_retained_allowed": False,
        "gate_output": str(GATE_OUTPUT.relative_to(ROOT)),
        "gate_has_stronger_schema": gate_has_stronger_schema,
        "current_gate_open": current_gate_open,
        "spoof_cases": cases,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not provide a canonical-Higgs operator certificate",
            "does not treat static EW algebra, H_unit, Ward, or observed selectors as O_H",
            "does not use y_t_bare, alpha_LM, plaquette/u0, kappa_s=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            "Any future O_H certificate must pass the hardened gate with a real "
            "identity certificate kind, normalization certificate kind, source-"
            "overlap closure mode, non-shortcut references, and forbidden-"
            "shortcut audit.  Then source-Higgs C_sH/C_HH production rows can "
            "be launched."
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
