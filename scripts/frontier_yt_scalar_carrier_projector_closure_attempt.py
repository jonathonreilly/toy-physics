#!/usr/bin/env python3
"""
PR #230 scalar carrier/projector closure attempt.

This runner asks whether the current color-singlet and taste/projector
artifacts identify a physical scalar carrier and normalized source projector
strong enough to support the FH/LSZ scalar-pole residue route.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_carrier_projector_closure_attempt_2026-05-02.json"

CERTS = {
    "color_singlet_zero_mode": "outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json",
    "color_singlet_finite_q_ir": "outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json",
    "zero_mode_removed_ladder": "outputs/yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json",
    "taste_corner_obstruction": "outputs/yt_taste_corner_ladder_pole_obstruction_2026-05-01.json",
    "taste_carrier_import": "outputs/yt_taste_carrier_import_audit_2026-05-01.json",
    "taste_singlet_normalization": "outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json",
    "taste_projector_attempt": "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json",
    "unit_projector_threshold": "outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json",
    "kernel_enhancement_import": "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json",
    "fitted_kernel_selector": "outputs/yt_fitted_kernel_residue_selector_no_go_2026-05-01.json",
    "scalar_denominator_closure": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "soft_continuum_threshold": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
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


def main() -> int:
    print("PR #230 scalar carrier/projector closure attempt")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    support_rows = [
        {
            "premise": "color-singlet q=0 cancellation",
            "certificate": CERTS["color_singlet_zero_mode"],
            "available": "zero-mode cancellation" in status(certs["color_singlet_zero_mode"]),
        },
        {
            "premise": "finite-q IR regularity",
            "certificate": CERTS["color_singlet_finite_q_ir"],
            "available": "finite-q IR regularity" in status(certs["color_singlet_finite_q_ir"]),
        },
        {
            "premise": "unit taste-singlet algebra",
            "certificate": CERTS["taste_projector_attempt"],
            "available": "scalar taste-projector normalization theorem attempt blocked" in status(certs["taste_projector_attempt"]),
        },
    ]
    blockers = [
        {
            "premise": "non-origin taste corners are admitted as the physical scalar carrier",
            "certificate": CERTS["taste_carrier_import"],
            "blocked": "taste-corner scalar-carrier import audit" in status(certs["taste_carrier_import"]),
        },
        {
            "premise": "normalized taste-singlet projector preserves finite crossings",
            "certificate": CERTS["taste_singlet_normalization"],
            "blocked": "taste-singlet" in status(certs["taste_singlet_normalization"]),
        },
        {
            "premise": "physical scalar carrier/source projector is fixed by current source functional",
            "certificate": CERTS["taste_projector_attempt"],
            "blocked": certs["taste_projector_attempt"].get("proposal_allowed") is False,
        },
        {
            "premise": "unit-projector finite ladder crosses without underived kernel multiplier",
            "certificate": CERTS["unit_projector_threshold"],
            "blocked": "unit-projector" in status(certs["unit_projector_threshold"]),
        },
        {
            "premise": "scalar-kernel enhancement or K'(pole) is derived",
            "certificate": CERTS["kernel_enhancement_import"],
            "blocked": "scalar-kernel enhancement import audit" in status(certs["kernel_enhancement_import"]),
        },
        {
            "premise": "fitted multiplier is a physical selector rather than an import",
            "certificate": CERTS["fitted_kernel_selector"],
            "blocked": "fitted scalar-kernel residue selector no-go" in status(certs["fitted_kernel_selector"]),
        },
        {
            "premise": "threshold/denominator stack supplies the remaining carrier-independent LSZ premise",
            "certificate": f"{CERTS['scalar_denominator_closure']}; {CERTS['soft_continuum_threshold']}",
            "blocked": (
                "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator_closure"])
                and "soft-continuum threshold no-go" in status(certs["soft_continuum_threshold"])
            ),
        },
    ]
    support_available = [row for row in support_rows if row["available"]]
    blocked_rows = [row for row in blockers if row["blocked"]]
    theorem_closed = not missing and not proposal_allowed and len(blocked_rows) == 0

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("support-premises-available", len(support_available) == len(support_rows), f"support={len(support_available)}/{len(support_rows)}")
    report("taste-carrier-import-still-blocking", blockers[0]["blocked"], CERTS["taste_carrier_import"])
    report("taste-singlet-normalization-still-blocking", blockers[1]["blocked"], CERTS["taste_singlet_normalization"])
    report("unit-projector-threshold-still-blocking", blockers[3]["blocked"], CERTS["unit_projector_threshold"])
    report("kernel-enhancement-still-blocking", blockers[4]["blocked"], CERTS["kernel_enhancement_import"])
    report("fitted-kernel-selector-still-blocking", blockers[5]["blocked"], CERTS["fitted_kernel_selector"])
    report("scalar-carrier-projector-theorem-not-closed", not theorem_closed, f"blocker_count={len(blocked_rows)}")

    result = {
        "actual_current_surface_status": "open / scalar carrier-projector closure attempt blocked",
        "verdict": (
            "The current PR #230 artifacts do not identify a physical scalar "
            "carrier/projector strongly enough for retained FH/LSZ closure.  "
            "Color-singlet zero-mode cancellation, finite-q IR regularity, and "
            "unit taste-singlet algebra are support.  The route remains blocked "
            "because non-origin taste corners lack authority as the physical "
            "carrier, normalized taste-singlet weighting removes finite "
            "crossings, unit-projector finite ladders need an underived kernel "
            "multiplier, fitted multipliers import the missing normalization, "
            "and the scalar denominator/threshold stack remains open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Physical scalar carrier/projector and K'(pole) remain open imports; finite witnesses are not retained LSZ residue evidence.",
        "parent_certificates": CERTS,
        "support_rows": support_rows,
        "blocker_rows": blockers,
        "support_count": len(support_available),
        "blocking_count": len(blocked_rows),
        "theorem_closed": theorem_closed,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not count non-origin taste corners without retained authority",
            "does not fit a scalar-kernel multiplier as a proof input",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Either derive the physical scalar carrier/projector and K'(pole) "
            "from retained dynamics, or continue seed-controlled FH/LSZ "
            "production toward a direct same-source pole derivative."
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
