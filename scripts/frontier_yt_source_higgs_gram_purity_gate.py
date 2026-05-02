#!/usr/bin/env python3
"""
PR #230 source-Higgs Gram purity gate.

This runner records the exact acceptance gate for a future source-Higgs
cross-correlator route.  If a canonical Higgs radial operator H is supplied on
the same surface, then pole-level C_ss, C_sH, and C_HH residues can certify
source-pole purity through the normalized Gram determinant.  The current PR
surface does not have C_sH or C_HH, so this is an open gate, not evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_gram_purity_gate_2026-05-02.json"

CERTS = {
    "source_pole_purity_gate": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "source_higgs_cross_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "higgs_pole_identity_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def purity_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    examples = [
        ("pure_same_pole", 4.0, 9.0, 6.0),
        ("mixed_source_pole", 4.0, 9.0, 3.0),
    ]
    for name, c_ss, c_hh, c_sh in examples:
        determinant = c_ss * c_hh - c_sh * c_sh
        rho = c_sh / math.sqrt(c_ss * c_hh)
        rows.append(
            {
                "name": name,
                "C_ss_pole_residue": c_ss,
                "C_HH_pole_residue": c_hh,
                "C_sH_pole_cross_residue": c_sh,
                "gram_determinant": determinant,
                "normalized_overlap_rho_sH": rho,
                "purity_certified": abs(1.0 - abs(rho)) < 1.0e-12 and abs(determinant) < 1.0e-12,
            }
        )
    return rows


def main() -> int:
    print("PR #230 source-Higgs Gram purity gate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    rows = purity_rows()
    pure_row = next(row for row in rows if row["name"] == "pure_same_pole")
    mixed_row = next(row for row in rows if row["name"] == "mixed_source_pole")

    source_pole_purity_open = (
        "source-pole purity cross-correlator gate not passed"
        in status(certs["source_pole_purity_gate"])
        and certs["source_pole_purity_gate"].get("source_pole_purity_gate_passed") is False
    )
    csh_import_missing = (
        "source-Higgs cross-correlator import audit" in status(certs["source_higgs_cross_import"])
        and certs["source_higgs_cross_import"].get("source_higgs_cross_correlator_authority_found") is False
    )
    source_to_higgs_open = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    latest_identity_open = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_pole_identity_blocker"])
        and certs["higgs_pole_identity_blocker"].get("identity_closed") is False
    )
    gate_theorem_valid = (
        pure_row["purity_certified"] is True
        and mixed_row["purity_certified"] is False
        and mixed_row["gram_determinant"] > 0.0
    )
    current_data_has_required_residues = False
    gate_passed = gate_theorem_valid and current_data_has_required_residues

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-pole-purity-open", source_pole_purity_open, status(certs["source_pole_purity_gate"]))
    report("csh-import-missing", csh_import_missing, status(certs["source_higgs_cross_import"]))
    report("source-to-higgs-lsz-open", source_to_higgs_open, status(certs["source_to_higgs_lsz"]))
    report("latest-higgs-pole-identity-open", latest_identity_open, status(certs["higgs_pole_identity_blocker"]))
    report("gram-purity-theorem-checks", gate_theorem_valid, f"rows={rows}")
    report("required-residues-absent-on-current-surface", not current_data_has_required_residues, "C_sH and C_HH absent")
    report("source-higgs-gram-purity-gate-not-passed", not gate_passed, "future acceptance gate only")

    result = {
        "actual_current_surface_status": "open / source-Higgs Gram purity gate not passed",
        "verdict": (
            "A future canonical-Higgs cross-correlator route has a sharp "
            "acceptance condition: at the isolated pole, C_sH^2 must equal "
            "C_ss C_HH, equivalently |rho_sH| = 1, after a canonical H operator "
            "has been derived on the same surface.  That condition certifies "
            "source-pole purity; a positive Gram determinant detects an "
            "orthogonal component.  The current PR surface lacks C_sH, C_HH, "
            "and the canonical-Higgs source operator, so this gate is not "
            "passed and does not authorize retained/proposed-retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The Gram purity theorem is an acceptance gate only; required C_sH/C_HH pole residues are absent.",
        "source_higgs_gram_purity_gate_passed": gate_passed,
        "current_data_has_required_residues": current_data_has_required_residues,
        "parent_certificates": CERTS,
        "acceptance_formula": {
            "gram_determinant": "Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2",
            "normalized_overlap": "rho_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))",
            "purity_condition": "Delta = 0 and |rho_sH| = 1 at the isolated pole",
        },
        "examples": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define canonical H by fiat",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat missing C_sH/C_HH data as evidence",
        ],
        "exact_next_action": (
            "Implement or derive the canonical-Higgs operator and C_sH/C_HH "
            "pole-residue measurements, or pivot to same-source W/Z response, "
            "sector-overlap equality, or production FH/LSZ chunk processing."
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
