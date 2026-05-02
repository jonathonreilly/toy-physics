#!/usr/bin/env python3
"""
PR #230 taste-corner scalar-carrier import audit.

The finite ladder crossings that survived color-singlet q=0 removal are
dominated by non-origin Brillouin-zone taste corners.  This runner checks
whether any current retained/audit-clean authority lets PR #230 treat those
corners as the physical scalar carrier and use the crossing as LSZ evidence.

The answer is no.  Existing taste and staggered-PT surfaces are useful support
or formula layers, but they do not derive the scalar carrier/projector and
inverse-propagator derivative needed for retained top-Yukawa closure.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
LADDER_INPUT = ROOT / "outputs" / "yt_scalar_ladder_kernel_input_audit_2026-05-01.json"
TASTE_CORNER = ROOT / "outputs" / "yt_taste_corner_ladder_pole_obstruction_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_taste_carrier_import_audit_2026-05-01.json"

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


def load_ledger_rows() -> dict[str, dict[str, object]]:
    payload = json.loads(AUDIT_LEDGER.read_text(encoding="utf-8"))
    return payload["rows"]


def row_summary(row: dict[str, object]) -> dict[str, object]:
    return {
        "current_status_raw": row.get("current_status_raw"),
        "audit_status": row.get("audit_status"),
        "effective_status": row.get("effective_status"),
        "chain_closes": row.get("chain_closes"),
        "runner_path": row.get("runner_path"),
        "chain_closure_explanation": row.get("chain_closure_explanation"),
        "verdict_rationale": row.get("verdict_rationale"),
    }


def main() -> int:
    print("PR #230 taste-corner scalar-carrier import audit")
    print("=" * 72)

    rows = load_ledger_rows()
    required_ids = [
        "cl3_taste_generation_theorem",
        "taste_scalar_isotropy_theorem_note",
        "yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18",
    ]
    candidates = {claim_id: rows.get(claim_id, {}) for claim_id in required_ids}
    ladder_input = json.loads(LADDER_INPUT.read_text(encoding="utf-8"))
    taste_corner = json.loads(TASTE_CORNER.read_text(encoding="utf-8"))

    missing = [claim_id for claim_id, row in candidates.items() if not row]
    taste_generation = candidates["cl3_taste_generation_theorem"]
    taste_isotropy = candidates["taste_scalar_isotropy_theorem_note"]
    staggered_pt = candidates["yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18"]

    taste_generation_not_carrier = (
        taste_generation.get("effective_status") == "audited_renaming"
        and taste_generation.get("chain_closes") is False
        and "identification of algebraic orbit labels" in str(taste_generation.get("verdict_rationale", ""))
    )
    taste_isotropy_not_carrier = (
        taste_isotropy.get("effective_status") == "audited_conditional"
        and taste_isotropy.get("chain_closes") is False
        and "scalar-spectrum" in str(taste_isotropy.get("verdict_rationale", ""))
    )
    staggered_pt_not_carrier = (
        taste_isotropy.get("chain_closes") is False
        and staggered_pt.get("effective_status") == "audited_conditional"
        and staggered_pt.get("chain_closes") is False
        and "H_UNIT" in str(staggered_pt.get("verdict_rationale", "")).upper()
    )
    ladder_projector_still_missing = (
        ladder_input.get("proposal_allowed") is False
        and "scalar color/taste/spin projector independent of H_unit readout"
        in ladder_input.get("still_missing", [])
    )
    taste_corner_blocks_finite_witness = (
        taste_corner.get("proposal_allowed") is False
        and "taste-corner pole-witness obstruction" in str(taste_corner.get("actual_current_surface_status", ""))
    )
    retained_authorities = [
        claim_id
        for claim_id, row in candidates.items()
        if row.get("effective_status") == "retained" and row.get("chain_closes") is True
    ]

    report("candidate-ledger-rows-present", not missing, f"missing={missing}")
    report(
        "cl3-taste-generation-not-scalar-carrier-authority",
        taste_generation_not_carrier,
        f"effective={taste_generation.get('effective_status')}, chain_closes={taste_generation.get('chain_closes')}",
    )
    report(
        "taste-scalar-isotropy-not-carrier-projector",
        taste_isotropy_not_carrier,
        f"effective={taste_isotropy.get('effective_status')}, chain_closes={taste_isotropy.get('chain_closes')}",
    )
    report(
        "full-staggered-pt-not-pr230-carrier-closure",
        staggered_pt_not_carrier,
        f"effective={staggered_pt.get('effective_status')}, chain_closes={staggered_pt.get('chain_closes')}",
    )
    report(
        "scalar-ladder-input-audit-still-missing-projector",
        ladder_projector_still_missing,
        str(ladder_input.get("still_missing", [])),
    )
    report(
        "taste-corner-finite-witness-block-loaded",
        taste_corner_blocks_finite_witness,
        str(taste_corner.get("actual_current_surface_status")),
    )
    report(
        "no-retained-taste-corner-scalar-carrier-authority",
        not retained_authorities,
        f"retained_authorities={retained_authorities}",
    )
    report(
        "not-retained-closure",
        True,
        "non-origin taste corners remain an open scalar-carrier import, not LSZ evidence",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / taste-corner scalar-carrier import audit",
        "verdict": (
            "No current retained/audit-clean authority lets PR #230 use the "
            "non-origin Brillouin-zone taste corners that dominate the finite "
            "ladder crossings as the physical scalar carrier.  The CL3 taste "
            "generation row is audited as a physical-identification/renaming "
            "boundary, the taste-scalar isotropy row is conditional for scalar "
            "spectrum consequences, and the full staggered-PT row is "
            "conditional and imports non-clean H_unit/normalization surfaces.  "
            "The ladder input audit still lists the scalar color/taste/spin "
            "projector as missing.  Therefore the finite taste-corner "
            "crossings cannot be used as retained scalar pole or LSZ evidence "
            "without a new taste/scalar-carrier theorem or production pole "
            "data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The taste-corner scalar-carrier/projector authority is not retained on the current surface.",
        "candidate_rows": {claim_id: row_summary(row) for claim_id, row in candidates.items()},
        "ladder_input_certificate": str(LADDER_INPUT.relative_to(ROOT)),
        "taste_corner_certificate": str(TASTE_CORNER.relative_to(ROOT)),
        "retained_authorities": retained_authorities,
        "remaining_blockers": [
            "derive a retained taste/scalar-carrier theorem for non-origin BZ corners, or exclude them in the continuum scalar denominator",
            "derive the scalar color/taste/spin projector independent of H_unit readout",
            "derive or measure the interacting inverse-propagator derivative at the scalar pole",
            "run production same-source FH/LSZ pole data if the theorem route remains blocked",
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
