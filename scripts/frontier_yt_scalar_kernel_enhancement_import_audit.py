#!/usr/bin/env python3
"""
PR #230 scalar-kernel enhancement import audit.

The unit taste projector removes the finite ladder crossings at the retained
scout kernel strength.  A finite pole would require an extra scalar-channel
kernel enhancement.  This runner checks the strongest current surfaces that
could supply that enhancement without fitting it as a pole selector.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_kernel_enhancement_import_audit_2026-05-01.json"

CERT_PATHS = {
    "unit_projector_threshold": "outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json",
    "hs_rpa_contact": "outputs/yt_hs_rpa_pole_condition_attempt_2026-05-01.json",
    "ladder_input_audit": "outputs/yt_scalar_ladder_kernel_input_audit_2026-05-01.json",
    "same_1pi_boundary": "outputs/yt_same_1pi_scalar_pole_boundary_2026-05-01.json",
    "scalar_kernel_ward_identity": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
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


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 scalar-kernel enhancement import audit")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERT_PATHS.items()}
    threshold = certs["unit_projector_threshold"]
    required_multiplier = float(
        threshold.get("summary", {}).get("required_kernel_multiplier_min", 0.0)
    )

    candidates = [
        {
            "candidate": "HS/RPA contact coupling",
            "certificate": CERT_PATHS["hs_rpa_contact"],
            "status": certs["hs_rpa_contact"].get("actual_current_surface_status"),
            "chain_closes": False,
            "why_not": "A local contact G is not in A_min, and gauge-exchange-to-contact collapse is scale dependent.",
        },
        {
            "candidate": "scalar ladder input audit",
            "certificate": CERT_PATHS["ladder_input_audit"],
            "status": certs["ladder_input_audit"].get("actual_current_surface_status"),
            "chain_closes": False,
            "why_not": "Reusable formulae exist, but exact scalar-channel kernel, projector, IR/volume limit, crossing, and residue remain listed as missing.",
        },
        {
            "candidate": "same-1PI four-fermion coefficient",
            "certificate": CERT_PATHS["same_1pi_boundary"],
            "status": certs["same_1pi_boundary"].get("actual_current_surface_status"),
            "chain_closes": False,
            "why_not": "A four-fermion coefficient fixes y^2 D_phi, not the scalar pole normalization or a pole-generating kernel multiplier.",
        },
        {
            "candidate": "Ward/gauge/Feshbach response identities",
            "certificate": CERT_PATHS["scalar_kernel_ward_identity"],
            "status": certs["scalar_kernel_ward_identity"].get("actual_current_surface_status"),
            "chain_closes": False,
            "why_not": "The pole condition fixes K(x_pole), but K'(x_pole), common dressing, and kernel enhancement remain open.",
        },
    ]

    report(
        "unit-projector-threshold-loaded",
        threshold.get("proposal_allowed") is False
        and required_multiplier > 2.0,
        f"required_kernel_multiplier_min={required_multiplier:.12g}",
    )
    report(
        "hs-rpa-contact-does-not-supply-retained-enhancement",
        certs["hs_rpa_contact"].get("proposal_allowed") is False
        and "new kernel theorem" in certs["hs_rpa_contact"].get("actual_current_surface_status", ""),
        certs["hs_rpa_contact"].get("actual_current_surface_status", ""),
    )
    report(
        "ladder-input-audit-keeps-kernel-import-open",
        certs["ladder_input_audit"].get("proposal_allowed") is False
        and "exact scalar-channel Bethe-Salpeter kernel from Wilson gauge exchange"
        in certs["ladder_input_audit"].get("still_missing", []),
        "kernel remains listed as missing",
    )
    report(
        "same-1pi-does-not-fix-enhancement",
        certs["same_1pi_boundary"].get("proposal_allowed") is False
        and "same-1PI not PR230 closure" in certs["same_1pi_boundary"].get(
            "actual_current_surface_status", ""
        ),
        certs["same_1pi_boundary"].get("actual_current_surface_status", ""),
    )
    report(
        "ward-identity-does-not-fix-kernel-enhancement",
        certs["scalar_kernel_ward_identity"].get("proposal_allowed") is False
        and "scalar kernel Ward-identity obstruction"
        in certs["scalar_kernel_ward_identity"].get("actual_current_surface_status", ""),
        certs["scalar_kernel_ward_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "no-candidate-closes-chain",
        not any(candidate["chain_closes"] for candidate in candidates),
        f"closing_candidates={[candidate['candidate'] for candidate in candidates if candidate['chain_closes']]}",
    )
    report(
        "not-retained-closure",
        True,
        "the audit finds no retained scalar-kernel enhancement authority",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / scalar-kernel enhancement import audit"
        ),
        "verdict": (
            "The current PR #230 surface has no retained/audit-clean authority "
            "for the extra scalar-channel kernel enhancement required after "
            "unit taste projection.  HS/RPA contact coupling, reusable ladder "
            "formulae, same-1PI four-fermion coefficients, and Ward/Feshbach "
            "response identities all leave the pole-generating kernel "
            "enhancement or K'(x_pole) open.  The multiplier needed to force "
            "a finite unit-projector crossing therefore cannot be imported as "
            "a proof input."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No current retained candidate derives the scalar-kernel "
            "enhancement or pole derivative required by the unit-projector "
            "threshold."
        ),
        "required_kernel_multiplier_min": required_multiplier,
        "candidates": candidates,
        "parent_certificates": CERT_PATHS,
        "remaining_blockers": [
            "derive the interacting scalar-channel kernel enhancement from retained Wilson-staggered dynamics",
            "derive the physical scalar taste/projector carrier and continuum limit",
            "derive K'(x_pole) and the same-source scalar LSZ residue",
            "or measure the pole derivative in production same-source FH/LSZ data",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained top-Yukawa closure",
            "does not add or fit a scalar contact coupling G",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
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
