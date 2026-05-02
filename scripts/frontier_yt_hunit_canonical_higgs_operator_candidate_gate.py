#!/usr/bin/env python3
"""
PR #230 H_unit canonical-Higgs operator candidate gate.

The new O_H/C_sH/C_HH route naturally tempts the old shortcut: use H_unit as
the canonical-Higgs operator.  This runner checks whether that is allowed on
the current surface.  It treats H_unit as a candidate only if the required
LSZ/purity/canonical-normalization certificates are present; it never uses the
old H_unit matrix-element definition as authority.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json"

TEXTS = {
    "ward_physical_readout_repair": "docs/YT_WARD_PHYSICAL_READOUT_REPAIR_AUDIT_NOTE_2026-05-01.md",
    "global_proof_audit": "docs/YT_PR230_GLOBAL_YT_PROOF_AUDIT_NOTE_2026-05-01.md",
    "class5_hunit": "docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md",
    "d17_closure_attempt": "docs/YT_D17_SOURCE_POLE_IDENTITY_CLOSURE_ATTEMPT_NOTE_2026-05-02.md",
}

CERTS = {
    "global_proof_audit": "outputs/yt_pr230_global_proof_audit_2026-05-01.json",
    "ward_physical_readout_repair": "outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json",
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_higgs_cross_correlator_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_higgs_operator_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "higgs_pole_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def read_text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def hunit_readout_witness() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    fixed_hunit_top_readout = 1.0
    for theta in (0.0, 0.35, 0.7):
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        y_chi = 0.4
        y_h = (fixed_hunit_top_readout - y_chi * sin_t) / cos_t
        rows.append(
            {
                "theta": theta,
                "cos_theta": cos_t,
                "sin_theta": sin_t,
                "hunit_unit_norm": cos_t * cos_t + sin_t * sin_t,
                "orthogonal_top_coupling_y_chi": y_chi,
                "fixed_hunit_top_readout": fixed_hunit_top_readout,
                "canonical_higgs_yukawa_y_h": y_h,
                "csh_purity_required": 1.0 if theta == 0.0 else 0.0,
            }
        )
    return rows


def main() -> int:
    print("PR #230 H_unit canonical-Higgs operator candidate gate")
    print("=" * 72)

    texts = {name: read_text(path) for name, path in TEXTS.items()}
    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    joined = "\n".join(texts.values())
    hunit_candidate_named = "H_unit" in joined and "(1,1)" in joined and "D17" in joined
    hunit_matrix_readout_forbidden = (
        "`H_unit`-to-top matrix element" in texts["ward_physical_readout_repair"]
        and "old `H_unit` matrix-element identification" in texts["global_proof_audit"]
    )
    hunit_docs_are_not_lsz_operator = (
        "source operator overlap" in texts["d17_closure_attempt"]
        and "inverse-propagator derivative" in texts["d17_closure_attempt"]
        and "canonical kinetic metric" in texts["d17_closure_attempt"]
    )

    global_audit_blocks = certs["global_proof_audit"].get("retained_y_t_rows") == {}
    ward_repair_blocks = certs["ward_physical_readout_repair"].get("closure_allowed") is False
    d17_blocks = (
        "D17 source-pole identity closure attempt blocked" in status(certs["d17_source_pole_identity"])
        and certs["d17_source_pole_identity"].get("theorem_closed") is False
    )
    mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in status(certs["source_pole_canonical_higgs_mixing"])
        and certs["source_pole_canonical_higgs_mixing"].get("source_pole_canonical_identity_gate_passed")
        is False
    )
    cross_import_blocks = (
        "source-Higgs cross-correlator import audit"
        in status(certs["source_higgs_cross_correlator_import"])
        and certs["source_higgs_cross_correlator_import"].get(
            "source_higgs_cross_correlator_authority_found"
        )
        is False
    )
    gram_blocks = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    operator_gate_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in status(certs["canonical_higgs_operator_realization"])
        and certs["canonical_higgs_operator_realization"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
    )
    latest_blocker_blocks = (
        "latest Higgs-pole identity blocker certificate"
        in status(certs["higgs_pole_identity_latest_blocker"])
        and certs["higgs_pole_identity_latest_blocker"].get("identity_closed") is False
    )

    witness_rows = hunit_readout_witness()
    fixed_readouts = {round(row["fixed_hunit_top_readout"], 12) for row in witness_rows}
    hunit_norms = {round(row["hunit_unit_norm"], 12) for row in witness_rows}
    canonical_y_values = {round(row["canonical_higgs_yukawa_y_h"], 12) for row in witness_rows}

    hunit_gate_passed = (
        not missing_texts
        and not missing_certs
        and not proposal_allowed
        and not global_audit_blocks
        and not ward_repair_blocks
        and not d17_blocks
        and not mixing_blocks
        and not cross_import_blocks
        and not gram_blocks
        and not operator_gate_blocks
        and not latest_blocker_blocks
    )

    report("text-authorities-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("hunit-candidate-named", hunit_candidate_named, "H_unit/D17 text surface exists")
    report("hunit-matrix-readout-forbidden", hunit_matrix_readout_forbidden, "old readout is the audited objection")
    report("hunit-docs-not-lsz-operator", hunit_docs_are_not_lsz_operator, "D17 note leaves overlap/residue/D'(pole) open")
    report("global-audit-blocks-hidden-proof", global_audit_blocks, status(certs["global_proof_audit"]))
    report("ward-repair-still-open", ward_repair_blocks, f"closure_allowed={certs['ward_physical_readout_repair'].get('closure_allowed')}")
    report("d17-source-pole-identity-blocks", d17_blocks, status(certs["d17_source_pole_identity"]))
    report("source-pole-mixing-blocks", mixing_blocks, status(certs["source_pole_canonical_higgs_mixing"]))
    report("csh-import-blocks", cross_import_blocks, status(certs["source_higgs_cross_correlator_import"]))
    report("gram-purity-blocks", gram_blocks, status(certs["source_higgs_gram_purity"]))
    report("canonical-operator-gate-blocks", operator_gate_blocks, status(certs["canonical_higgs_operator_realization"]))
    report("latest-higgs-pole-blocker-still-open", latest_blocker_blocks, status(certs["higgs_pole_identity_latest_blocker"]))
    report("witness-keeps-hunit-readout-fixed", len(fixed_readouts) == 1, f"fixed_readouts={sorted(fixed_readouts)}")
    report("witness-keeps-hunit-unit-norm-fixed", len(hunit_norms) == 1, f"hunit_norms={sorted(hunit_norms)}")
    report("witness-varies-canonical-y", len(canonical_y_values) == len(witness_rows), f"canonical_y={sorted(canonical_y_values)}")
    report("hunit-canonical-higgs-operator-gate-not-passed", not hunit_gate_passed, f"hunit_gate_passed={hunit_gate_passed}")

    result = {
        "actual_current_surface_status": "exact negative boundary / H_unit not canonical-Higgs operator realization",
        "verdict": (
            "H_unit remains a named substrate/D17 bilinear candidate, but it is "
            "not a certified canonical-Higgs operator for PR #230.  The current "
            "audited objection is precisely the H_unit matrix-element readout, "
            "and D17 carrier support leaves the source overlap, pole residue, "
            "inverse-propagator derivative, and canonical kinetic metric open.  "
            "The witness keeps H_unit unit norm and H_unit top readout fixed "
            "while the canonical-Higgs Yukawa varies through an orthogonal "
            "neutral scalar admixture.  Therefore H_unit can enter a future "
            "C_sH/C_HH route only after the same purity and canonical-normalization "
            "certificates required of any O_H candidate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "H_unit lacks the current-surface LSZ/purity/canonical-Higgs identity certificates required for O_H.",
        "hunit_canonical_higgs_operator_gate_passed": hunit_gate_passed,
        "parent_certificates": CERTS,
        "text_authorities": TEXTS,
        "witness_rows": witness_rows,
        "acceptance_requirements": [
            "do not use H_unit matrix-element readout as y_t authority",
            "derive or measure source-pole purity / cos(theta)=1",
            "derive C_HH and C_sH pole residues with a canonical-Higgs identity certificate",
            "derive source overlap or D'(pole), not only D17 carrier uniqueness",
            "pass retained-route and campaign certificates with proposal_allowed true before any proposed_retained wording",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity, observed top mass, observed y_t, observed W/Z masses, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1, cos(theta)=1, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "If using H_unit as O_H, first supply C_HH/C_sH pole residues and "
            "a purity/canonical-Higgs identity certificate.  Otherwise pivot "
            "to W/Z response with identity certificates or seed-controlled "
            "FH/LSZ chunk processing."
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
