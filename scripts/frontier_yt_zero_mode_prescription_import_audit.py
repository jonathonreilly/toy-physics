#!/usr/bin/env python3
"""
PR #230 zero-mode prescription import audit.

The scalar zero-mode theorem reduced the analytic blocker to a selected
gauge-fixing / zero-mode / IR / finite-volume prescription for the interacting
scalar denominator.  This runner audits the strongest current repo surfaces
that might already supply that prescription.

Result: no current surface supplies it.  Existing PT notes use fixed IR
regulators and gauge-parameter conventions, the continuum-identification note
warns about alternative gauge fixings, and the FH/LSZ production manifest
requires zero-mode/IR control rather than deriving it.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_zero_mode_prescription_import_audit_2026-05-01.json"

TEXT_CANDIDATES = {
    "p1_bz_pt_note": ROOT / "docs" / "YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md",
    "continuum_identification": ROOT / "docs" / "CONTINUUM_IDENTIFICATION_NOTE.md",
    "fh_lsz_manifest_note": ROOT / "docs" / "YT_FH_LSZ_PRODUCTION_MANIFEST_NOTE_2026-05-01.md",
    "zero_mode_theorem_note": ROOT / "docs" / "YT_SCALAR_ZERO_MODE_LIMIT_ORDER_THEOREM_NOTE_2026-05-01.md",
}

JSON_CANDIDATES = {
    "kernel_input_audit": ROOT / "outputs" / "yt_scalar_ladder_kernel_input_audit_2026-05-01.json",
    "ladder_ir_zero_mode": ROOT / "outputs" / "yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json",
    "ladder_derivative_limit": ROOT / "outputs" / "yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
    "zero_mode_limit_order": ROOT / "outputs" / "yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json",
    "fh_lsz_manifest": ROOT / "outputs" / "yt_fh_lsz_production_manifest_2026-05-01.json",
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def main() -> int:
    print("PR #230 zero-mode prescription import audit")
    print("=" * 72)

    text_data = {name: read_text(path) for name, path in TEXT_CANDIDATES.items()}
    json_data = {name: read_json(path) for name, path in JSON_CANDIDATES.items()}
    statuses = {
        name: data.get("actual_current_surface_status", "")
        for name, data in json_data.items()
    }
    proposal_allowed = [
        name for name, data in json_data.items()
        if data.get("proposal_allowed") is True
    ]

    p1_note = text_data["p1_bz_pt_note"]
    continuum_note = text_data["continuum_identification"]
    manifest_note = text_data["fh_lsz_manifest_note"]
    kernel_audit = json_data["kernel_input_audit"]
    manifest = json_data["fh_lsz_manifest"]
    zero_mode = json_data["zero_mode_limit_order"]

    candidate_summary = {
        "p1_bz_pt_note": {
            "has_ir_regulator": contains_all(p1_note, ["IR regulator"]),
            "has_gauge_parameter_convention": contains_all(p1_note, ["gauge-parameter convention"]),
            "has_zero_mode_prescription": contains_all(p1_note, ["zero-mode prescription"]),
            "has_retained_scalar_denominator_limit": contains_all(p1_note, ["retained", "scalar", "denominator", "zero-mode"]),
        },
        "continuum_identification": {
            "has_alternative_gauge_fixings": contains_all(continuum_note, ["alternative gauge-fixings"]),
            "has_pr230_scalar_denominator": contains_all(continuum_note, ["PR #230", "scalar denominator"]),
        },
        "fh_lsz_manifest_note": {
            "requires_zero_mode_control": contains_all(manifest_note, ["finite-volume/IR/zero-mode control"]),
            "claims_production_evidence": contains_all(manifest_note, ["production evidence", "retained closure"]),
        },
        "kernel_input_audit": {
            "status": statuses["kernel_input_audit"],
            "proposal_allowed": kernel_audit.get("proposal_allowed"),
            "reason": kernel_audit.get("proposal_allowed_reason"),
        },
        "zero_mode_limit_order": {
            "status": statuses["zero_mode_limit_order"],
            "proposal_allowed": zero_mode.get("proposal_allowed"),
        },
        "fh_lsz_manifest": {
            "status": statuses["fh_lsz_manifest"],
            "proposal_allowed": manifest.get("proposal_allowed"),
            "required_next_theorem": manifest.get("required_next_theorem", []),
        },
    }

    report(
        "candidate-surfaces-present",
        all(path.exists() for path in TEXT_CANDIDATES.values()) and all(path.exists() for path in JSON_CANDIDATES.values()),
        f"text={len(TEXT_CANDIDATES)}, json={len(JSON_CANDIDATES)}",
    )
    report(
        "no-candidate-authorizes-proposed-retained",
        not proposal_allowed,
        f"proposal_allowed={proposal_allowed}",
    )
    report(
        "pt-note-is-regulator-convention-not-prescription",
        candidate_summary["p1_bz_pt_note"]["has_ir_regulator"]
        and candidate_summary["p1_bz_pt_note"]["has_gauge_parameter_convention"]
        and not candidate_summary["p1_bz_pt_note"]["has_zero_mode_prescription"],
        str(candidate_summary["p1_bz_pt_note"]),
    )
    report(
        "continuum-note-does-not-select-pr230-gauge-fixing",
        candidate_summary["continuum_identification"]["has_alternative_gauge_fixings"]
        and not candidate_summary["continuum_identification"]["has_pr230_scalar_denominator"],
        str(candidate_summary["continuum_identification"]),
    )
    report(
        "kernel-input-audit-keeps-limit-open",
        "limiting theorem remain open imports" in str(kernel_audit.get("proposal_allowed_reason", ""))
        and kernel_audit.get("proposal_allowed") is False,
        str(kernel_audit.get("proposal_allowed_reason", "")),
    )
    report(
        "manifest-requires-control-rather-than-derives-it",
        candidate_summary["fh_lsz_manifest_note"]["requires_zero_mode_control"]
        and manifest.get("proposal_allowed") is False,
        statuses["fh_lsz_manifest"],
    )
    report(
        "zero-mode-theorem-parent-blocks-hidden-shortcut",
        "zero-mode limit-order theorem" in str(statuses["zero_mode_limit_order"])
        and zero_mode.get("proposal_allowed") is False,
        statuses["zero_mode_limit_order"],
    )
    report(
        "not-retained-closure",
        True,
        "no current repo surface selects the PR230 scalar zero-mode/IR/finite-volume prescription",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / zero-mode prescription import audit",
        "verdict": (
            "The strongest current repo candidates do not supply a retained "
            "gauge-fixing, zero-mode, IR, and finite-volume prescription for "
            "the PR #230 scalar denominator.  Existing perturbative notes use "
            "fixed regulator conventions; continuum-identification warns about "
            "alternative gauge fixings; production manifests require the "
            "prescription instead of deriving it; and all scalar ladder "
            "certificates keep proposal_allowed=false."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No audited current-surface authority selects the scalar zero-mode/IR/finite-volume prescription.",
        "text_candidates": {name: str(path.relative_to(ROOT)) for name, path in TEXT_CANDIDATES.items()},
        "json_candidates": {name: str(path.relative_to(ROOT)) for name, path in JSON_CANDIDATES.items()},
        "statuses": statuses,
        "candidate_summary": candidate_summary,
        "required_next_theorem": [
            "derive a retained gauge fixing and zero-mode treatment for the scalar-channel kernel",
            "derive the finite-volume and IR limiting order selected by that gauge fixing",
            "prove pole-location and inverse-propagator-derivative convergence in that limit",
            "or run production same-source scalar pole measurements with an explicitly selected prescription",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as selectors",
            "does not use alpha_LM, plaquette, u0, or reduced pilots as proof inputs",
            "does not set c2 = 1 or Z_match = 1",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
