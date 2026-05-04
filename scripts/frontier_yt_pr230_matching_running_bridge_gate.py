#!/usr/bin/env python3
"""
PR #230 matching/running bridge gate.

This is a non-closure gate for the final lattice-scale -> physical-scale
conversion step.  It makes the required bridge certificate executable without
using observed top/yukawa values, H_unit/Ward authority, alpha_LM/plaquette
authority, or kappa/c2/Z_match shortcuts.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_matching_running_bridge_gate_2026-05-04.json"
CANDIDATE = ROOT / "outputs" / "yt_pr230_matching_running_bridge_certificate_2026-05-04.json"

REFERENCE_DOCS = {
    "k1": "docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md",
    "k2": "docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md",
    "k3": "docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md",
    "v_input": "docs/MINIMAL_AXIOMS_2026-04-11.md",
}

ALLOWED_READOUT_KINDS = {
    "direct_correlator_mass",
    "fh_lsz_source_pole",
    "source_higgs_gram",
    "same_source_wz_response",
}

FORBIDDEN_REFERENCE_FRAGMENTS = {
    "YT_WARD_IDENTITY_DERIVATION_THEOREM",
    "yt_ward_identity",
    "H_UNIT",
    "H_unit",
    "alpha_LM",
    "plaquette",
    "u0",
    "observed",
    "PDG",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def path_ref_ok(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if not value.startswith(("docs/", "outputs/", "scripts/")):
        return False
    return (ROOT / value).exists()


def non_shortcut_ref_ok(value: Any) -> bool:
    if not path_ref_ok(value):
        return False
    return not any(fragment in value for fragment in FORBIDDEN_REFERENCE_FRAGMENTS)


def validate_candidate(candidate: dict[str, Any]) -> dict[str, bool]:
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall", {}), dict) else {}
    uncertainty = (
        candidate.get("uncertainty_budget", {})
        if isinstance(candidate.get("uncertainty_budget", {}), dict)
        else {}
    )
    required_uncertainties = {
        "statistical",
        "finite_volume",
        "finite_spacing",
        "scale_setting",
        "running_bridge",
        "matching",
    }
    return {
        "certificate_kind": candidate.get("certificate_kind") == "pr230_matching_running_bridge",
        "readout_kind_allowed": candidate.get("readout_kind") in ALLOWED_READOUT_KINDS,
        "input_readout_reference": non_shortcut_ref_ok(candidate.get("input_readout_reference")),
        "physical_inputs_certified": candidate.get("physical_inputs_certified") is True,
        "scalar_lsz_or_direct_mass_certified": candidate.get("scalar_lsz_or_direct_mass_certified") is True,
        "source_overlap_or_direct_mass_certified": candidate.get("source_overlap_or_direct_mass_certified") is True,
        "scale_anchor_certified": candidate.get("scale_anchor_certified") is True,
        "v_input_declared_as_substrate": candidate.get("v_input_declared_as_substrate") is True,
        "sm_rge_loop_order": candidate.get("sm_rge_loop_order") in {4, 5},
        "msbar_to_pole_order": isinstance(candidate.get("msbar_to_pole_order"), int)
        and candidate.get("msbar_to_pole_order") >= 3,
        "scheme_conversion_reference": non_shortcut_ref_ok(candidate.get("scheme_conversion_reference")),
        "uncertainty_budget_complete": required_uncertainties.issubset(set(uncertainty)),
        "no_observed_target_selector": firewall.get("used_observed_targets_as_selectors") is False,
        "no_hunit_or_ward": firewall.get("used_hunit_or_ward_authority") is False,
        "no_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_kappa_c2_zmatch_shortcut": firewall.get("set_kappa_c2_zmatch_equal_one") is False,
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }


def sample_bridge_sanity() -> dict[str, float]:
    # Toy values only: this checks arithmetic shape, not PR230 evidence.
    m_msbar_v = 100.0
    alpha_s = 0.1
    a = alpha_s / math.pi
    v_input = 246.282818290129
    k1 = 4.0 / 3.0
    k2 = 10.9405
    k3 = 80.405
    pole_factor = 1.0 + k1 * a + k2 * a * a + k3 * a * a * a
    return {
        "sample_m_msbar_v_GeV": m_msbar_v,
        "sample_alpha_s": alpha_s,
        "sample_y_t_v": math.sqrt(2.0) * m_msbar_v / v_input,
        "sample_msbar_to_pole_factor_3loop": pole_factor,
        "sample_m_pole_GeV": m_msbar_v * pole_factor,
    }


def main() -> int:
    print("PR #230 matching/running bridge gate")
    print("=" * 72)

    candidate = load_json(CANDIDATE)
    candidate_checks = validate_candidate(candidate) if candidate else {}
    failed_candidate_checks = [key for key, ok in candidate_checks.items() if not ok]
    candidate_passes = bool(candidate) and not failed_candidate_checks
    sample = sample_bridge_sanity()
    references_present = {key: (ROOT / rel).exists() for key, rel in REFERENCE_DOCS.items()}

    report("reference-docs-present", all(references_present.values()), f"{references_present}")
    report(
        "sample-bridge-arithmetic-positive",
        sample["sample_y_t_v"] > 0.0 and sample["sample_msbar_to_pole_factor_3loop"] > 1.0,
        f"sample_y={sample['sample_y_t_v']:.6f}, pole_factor={sample['sample_msbar_to_pole_factor_3loop']:.6f}",
    )
    report("candidate-certificate-absent", not candidate, str(CANDIDATE.relative_to(ROOT)))
    if candidate:
        report("candidate-certificate-schema-valid", candidate_passes, f"failed={failed_candidate_checks}")
    report(
        "matching-running-bridge-not-currently-authorized",
        not candidate_passes,
        f"matching_running_bridge_passed={candidate_passes}",
    )
    report("does-not-authorize-retained-proposal", True, "bridge awaits certified physical inputs")

    result = {
        "actual_current_surface_status": "open / PR230 matching-running bridge awaits certified physical input",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No certified production readout with scalar-LSZ/direct-mass, "
            "source-overlap/direct-mass, scale-setting, and 4/5-loop running "
            "inputs has been supplied."
        ),
        "bare_retained_allowed": False,
        "bridge_contract_ready": True,
        "matching_running_bridge_passed": candidate_passes,
        "candidate_certificate": str(CANDIDATE.relative_to(ROOT)),
        "candidate_certificate_present": bool(candidate),
        "candidate_certificate_checks": candidate_checks,
        "candidate_certificate_failed_checks": failed_candidate_checks,
        "allowed_readout_kinds": sorted(ALLOWED_READOUT_KINDS),
        "required_candidate_fields": [
            "certificate_kind = pr230_matching_running_bridge",
            "input_readout_reference to certified physical readout",
            "physical_inputs_certified = true",
            "scalar_lsz_or_direct_mass_certified = true",
            "source_overlap_or_direct_mass_certified = true",
            "scale_anchor_certified = true",
            "v_input_declared_as_substrate = true",
            "sm_rge_loop_order in {4, 5}",
            "msbar_to_pole_order >= 3",
            "complete uncertainty budget",
            "shortcut firewall flags all false",
        ],
        "sample_arithmetic_sanity_not_evidence": sample,
        "parent_references": REFERENCE_DOCS,
        "strict_non_claims": [
            "does not run from observed m_t or observed y_t",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette, or u0 authority",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not claim current physical y_t or m_t",
        ],
        "exact_next_action": (
            "After production/LSZ/source-overlap or direct-mass gates pass, "
            "emit a PR230 matching-running bridge certificate with 4/5-loop "
            "SM running, MSbar-to-pole conversion, scale-setting and matching "
            "uncertainties, then rerun the full closure assembly gate."
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
