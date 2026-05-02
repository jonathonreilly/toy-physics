#!/usr/bin/env python3
"""
PR #230 canonical-Higgs operator realization gate.

The C_sH / Gram-purity route needs a concrete canonical-Higgs operator H on
the same Cl(3)/Z3 source surface as the PR scalar source.  Existing EW notes
use a canonical Higgs doublet after it is supplied; that is not the same as a
substrate operator realization that can produce C_sH and C_HH pole residues.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_realization_gate_2026-05-02.json"

EW_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
EW_RUNNER = ROOT / "scripts" / "frontier_ew_higgs_gauge_mass_diagonalization.py"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"

CERTS = {
    "source_higgs_cross_correlator_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "effective_potential_hessian": "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json",
    "brst_nielsen_higgs_identity": "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json",
    "neutral_scalar_rank_one_purity": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    print("PR #230 canonical-Higgs operator realization gate")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    ew_note_text = text(EW_NOTE)
    ew_runner_text = text(EW_RUNNER)
    harness_text = text(PRODUCTION_HARNESS)

    ew_assumes_canonical_h = (
        "Assume a neutral Higgs vacuum" in ew_note_text
        and "Higgs doublet" in ew_note_text
        and "M_W = g_2 v / 2" in ew_note_text
    )
    ew_runner_object_level = (
        "Object-level verifier for the EW Higgs gauge-mass diagonalization theorem" in ew_runner_text
        and "one-doublet tree-level" in ew_runner_text
        and "does not use numerical electroweak pole masses" in ew_runner_text
    )
    harness_has_scalar_source = (
        "--scalar-source-shifts" in harness_text
        and "scalar_source_response_analysis" in harness_text
    )
    harness_has_canonical_h_operator = any(
        token in harness_text
        for token in ("canonical_higgs_operator", "source_higgs_cross_correlator", "C_sH")
    )
    cross_import_blocks = (
        "source-Higgs cross-correlator import audit"
        in status(certs["source_higgs_cross_correlator_import"])
        and certs["source_higgs_cross_correlator_import"].get(
            "source_higgs_cross_correlator_authority_found"
        )
        is False
    )
    gram_gate_blocks = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    canonical_import_blocks = (
        "canonical scalar normalization import audit"
        in status(certs["canonical_scalar_import"])
        and certs["canonical_scalar_import"].get("proposal_allowed") is False
    )
    hessian_blocks = (
        "effective-potential Hessian not source-overlap identity"
        in status(certs["effective_potential_hessian"])
    )
    brst_blocks = "BRST-Nielsen identities not Higgs-pole identity" in status(
        certs["brst_nielsen_higgs_identity"]
    )
    rank_one_blocks = (
        "neutral scalar rank-one purity gate not passed" in status(certs["neutral_scalar_rank_one_purity"])
        and certs["neutral_scalar_rank_one_purity"].get(
            "neutral_scalar_rank_one_purity_gate_passed"
        )
        is False
    )

    acceptance_schema = {
        "canonical_higgs_operator": "explicit same-surface operator O_H or H_radial on Cl(3)/Z3 fields",
        "normalization": "canonical kinetic/LSZ normalization certificate for H",
        "correlators": ["C_HH pole residue", "C_sH cross residue", "C_ss same-source residue"],
        "purity_gate": "Res(C_sH)^2 = Res(C_ss) Res(C_HH) at isolated pole",
        "forbidden_substitutes": [
            "static electroweak v",
            "observed W/Z masses",
            "EW gauge-mass algebra after canonical H is assumed",
            "H_unit matrix-element readout",
            "D17 carrier support without source overlap",
        ],
    }
    gate_passed = (
        not missing
        and not proposal_allowed
        and harness_has_canonical_h_operator
        and not cross_import_blocks
        and not gram_gate_blocks
        and not canonical_import_blocks
        and not rank_one_blocks
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("ew-note-assumes-canonical-h", ew_assumes_canonical_h, str(EW_NOTE.relative_to(ROOT)))
    report("ew-runner-is-object-level-after-h-supplied", ew_runner_object_level, str(EW_RUNNER.relative_to(ROOT)))
    report("harness-has-pr-scalar-source", harness_has_scalar_source, str(PRODUCTION_HARNESS.relative_to(ROOT)))
    report("harness-lacks-canonical-h-operator", not harness_has_canonical_h_operator, "no C_sH/O_H path")
    report("cross-correlator-import-blocks", cross_import_blocks, status(certs["source_higgs_cross_correlator_import"]))
    report("gram-purity-gate-blocks", gram_gate_blocks, status(certs["source_higgs_gram_purity"]))
    report("canonical-scalar-import-blocks", canonical_import_blocks, status(certs["canonical_scalar_import"]))
    report("hessian-shortcut-blocks", hessian_blocks, status(certs["effective_potential_hessian"]))
    report("brst-nielsen-shortcut-blocks", brst_blocks, status(certs["brst_nielsen_higgs_identity"]))
    report("rank-one-purity-gate-blocks", rank_one_blocks, status(certs["neutral_scalar_rank_one_purity"]))
    report("canonical-higgs-operator-realization-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / canonical-Higgs operator realization gate not passed",
        "verdict": (
            "The C_sH / Gram-purity route needs a concrete same-surface "
            "canonical-Higgs operator.  Current EW Higgs gauge-mass artifacts "
            "assume canonical H and derive object-level mass algebra after "
            "that assumption; they do not realize O_H on the PR #230 Cl(3)/Z3 "
            "source surface.  The production harness has scalar-source "
            "response and C_ss support, but no C_sH or C_HH operator path."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No same-surface canonical-Higgs operator or C_sH/C_HH residue certificate exists.",
        "canonical_higgs_operator_realization_gate_passed": gate_passed,
        "acceptance_schema": acceptance_schema,
        "parent_certificates": CERTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat EW gauge-mass algebra as source-Higgs operator realization",
            "does not use observed W/Z masses, static v, H_unit, or yt_ward_identity",
            "does not set kappa_s = 1 or cos(theta)=1",
        ],
        "exact_next_action": (
            "Construct a same-surface canonical-Higgs operator with C_HH and "
            "C_sH residues, derive rank-one purity, implement W/Z response "
            "with identity certificates, or continue seed-controlled FH/LSZ production."
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
