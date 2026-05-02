#!/usr/bin/env python3
"""
PR #230 confinement-gap threshold import audit.

This runner checks a tempting scalar-denominator shortcut: whether qualitative
confinement or mass-gap statements on the Cl(3)/Z^3 substrate can supply the
uniform same-source scalar continuum threshold required by the FH/LSZ
pole-residue gate.  They cannot.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_confinement_gap_threshold_import_audit_2026-05-02.json"
SUBSTRATE_NOTE = ROOT / "docs" / "YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md"

CERTS = {
    "threshold_authority": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "uniform_gap": "outputs/yt_fh_lsz_uniform_gap_self_certification_no_go_2026-05-02.json",
    "soft_continuum": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "finite_volume": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "scalar_denominator": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "higgs_pole_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def build_sector_gap_witness() -> dict[str, Any]:
    colored_confinement_gap = 1.0
    scalar_pole_x = 0.25
    rows = []
    for epsilon in (1.0e-1, 1.0e-3, 1.0e-6):
        rows.append(
            {
                "colored_confinement_gap": colored_confinement_gap,
                "scalar_pole_x": scalar_pole_x,
                "same_source_scalar_continuum_start_x": scalar_pole_x + epsilon,
                "same_source_scalar_threshold_gap": epsilon,
                "confinement_gap_unchanged": colored_confinement_gap,
            }
        )
    scalar_gaps = [row["same_source_scalar_threshold_gap"] for row in rows]
    return {
        "interpretation": (
            "A qualitative colored-sector confinement gap is not the same as a "
            "uniform lower bound on same-source color-singlet scalar spectral "
            "weight above the isolated Higgs pole."
        ),
        "rows": rows,
        "checks": {
            "confinement_gap_fixed": len({row["colored_confinement_gap"] for row in rows}) == 1,
            "scalar_threshold_gap_can_approach_zero": min(scalar_gaps) <= 1.0e-6,
            "gap_ratio_span": max(scalar_gaps) / min(scalar_gaps),
        },
    }


def main() -> int:
    print("PR #230 confinement-gap threshold import audit")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    note_text = SUBSTRATE_NOTE.read_text(encoding="utf-8") if SUBSTRATE_NOTE.exists() else ""
    witness = build_sector_gap_witness()
    checks = witness["checks"]

    substrate_mentions_mass_gap = "mass gap" in note_text and "confinement" in note_text
    substrate_denies_numeric_pin = (
        "but not the value" in note_text
        and "NOT pin the dimensionful mass" in note_text
        and "gauge symmetry does NOT constrain the Yukawa coupling coefficients" in note_text
    )
    threshold_import_absent = (
        "threshold-authority import audit" in status(certs["threshold_authority"])
        and certs["threshold_authority"].get("proposal_allowed") is False
    )
    uniform_gap_not_self_certified = (
        "uniform-gap self-certification no-go" in status(certs["uniform_gap"])
        and certs["uniform_gap"].get("proposal_allowed") is False
    )
    soft_continuum_blocks_ir_upgrade = (
        "soft-continuum threshold no-go" in status(certs["soft_continuum"])
        and certs["soft_continuum"].get("proposal_allowed") is False
    )
    finite_volume_blocks_discreteness = (
        "finite-volume pole-saturation obstruction" in status(certs["finite_volume"])
        and certs["finite_volume"].get("proposal_allowed") is False
    )
    scalar_denominator_open = (
        "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator"])
        and certs["scalar_denominator"].get("theorem_closed") is False
    )
    higgs_identity_open = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_pole_blocker"])
        and certs["higgs_pole_blocker"].get("identity_closed") is False
    )
    threshold_closed = (
        not missing
        and not proposal_allowed
        and substrate_mentions_mass_gap
        and not any(
            [
                substrate_denies_numeric_pin,
                threshold_import_absent,
                uniform_gap_not_self_certified,
                soft_continuum_blocks_ir_upgrade,
                finite_volume_blocks_discreteness,
                scalar_denominator_open,
                higgs_identity_open,
            ]
        )
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("substrate-note-mentions-confinement-gap", substrate_mentions_mass_gap, str(SUBSTRATE_NOTE.relative_to(ROOT)))
    report("substrate-note-denies-numeric-yukawa-pin", substrate_denies_numeric_pin, "qualitative gap is not scalar LSZ threshold")
    report("threshold-authority-still-absent", threshold_import_absent, status(certs["threshold_authority"]))
    report("uniform-gap-not-self-certified", uniform_gap_not_self_certified, status(certs["uniform_gap"]))
    report("soft-continuum-blocks-ir-upgrade", soft_continuum_blocks_ir_upgrade, status(certs["soft_continuum"]))
    report("finite-volume-discreteness-not-threshold", finite_volume_blocks_discreteness, status(certs["finite_volume"]))
    report("scalar-denominator-still-open", scalar_denominator_open, status(certs["scalar_denominator"]))
    report("higgs-pole-identity-still-open", higgs_identity_open, status(certs["higgs_pole_blocker"]))
    report("witness-keeps-confinement-gap-fixed", checks["confinement_gap_fixed"], f"gap_span={checks['gap_ratio_span']:.6g}")
    report("scalar-threshold-can-approach-pole", checks["scalar_threshold_gap_can_approach_zero"], f"min_gap={min(row['same_source_scalar_threshold_gap'] for row in witness['rows']):.3e}")
    report("confinement-gap-not-scalar-threshold-closure", not threshold_closed, f"threshold_closed={threshold_closed}")

    result = {
        "actual_current_surface_status": "exact negative boundary / confinement gap not scalar LSZ threshold",
        "verdict": (
            "Qualitative confinement or mass-gap statements on the Cl(3)/Z^3 "
            "substrate do not supply the uniform same-source scalar continuum "
            "threshold required by the FH/LSZ pole-residue gate.  The substrate "
            "note itself limits topology/anomaly arguments to qualitative "
            "spectrum and representation constraints, not numerical Yukawa or "
            "scalar-pole normalization.  The existing threshold-authority, "
            "uniform-gap, soft-continuum, finite-volume, scalar-denominator, "
            "and Higgs-pole identity gates all remain blocking."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No current-surface confinement/mass-gap statement derives the same-source scalar spectral threshold or pole residue.",
        "threshold_closed": threshold_closed,
        "parent_certificates": CERTS,
        "substrate_note": str(SUBSTRATE_NOTE.relative_to(ROOT)),
        "sector_gap_witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer scalar pole saturation from confinement",
            "does not use observed top mass, observed y_t, observed hadron masses, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit or yt_ward_identity as authority",
        ],
        "exact_next_action": (
            "Continue seed-controlled production chunks or derive a genuine "
            "same-source scalar denominator/threshold theorem; do not use "
            "generic confinement-gap language as the FH/LSZ threshold premise."
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
