#!/usr/bin/env python3
"""
PR #230 physics-loop campaign status certificate.

This runner summarizes the current 12h-campaign work package.  It does not
claim retained closure.  It verifies that the live analytic shortcuts have been
classified and that the remaining closure routes require either production
evidence or a genuinely new theorem/observable.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_campaign_status_certificate_2026-05-01.json"

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
    print("PR #230 campaign status certificate")
    print("=" * 72)

    certificates = {
        "key_blocker": load("outputs/yt_key_blocker_closure_attempt_2026-05-01.json"),
        "source_two_point": load("outputs/yt_scalar_source_two_point_stretch_2026-05-01.json"),
        "hs_rpa": load("outputs/yt_hs_rpa_pole_condition_attempt_2026-05-01.json"),
        "ladder_scout": load("outputs/yt_scalar_ladder_kernel_scout_2026-05-01.json"),
        "ladder_input": load("outputs/yt_scalar_ladder_kernel_input_audit_2026-05-01.json"),
        "projector_norm": load("outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json"),
        "hqet": load("outputs/yt_hqet_direct_route_requirements_2026-05-01.json"),
        "static_mass": load("outputs/yt_static_mass_matching_obstruction_2026-05-01.json"),
        "legendre": load("outputs/yt_legendre_kappa_gauge_freedom_2026-05-01.json"),
        "free_bubble": load("outputs/yt_free_scalar_two_point_pole_absence_2026-05-01.json"),
        "same_1pi": load("outputs/yt_same_1pi_scalar_pole_boundary_2026-05-01.json"),
        "lsz_norm": load("outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json"),
        "feshbach_response": load("outputs/yt_feshbach_operator_response_boundary_2026-05-01.json"),
        "bridge_stack": load("outputs/yt_bridge_stack_import_audit_2026-05-01.json"),
        "spectral_saturation": load("outputs/yt_scalar_spectral_saturation_no_go_2026-05-01.json"),
        "ladder_ir_zero_mode": load("outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json"),
        "heavy_kinetic": load("outputs/yt_heavy_kinetic_mass_route_2026-05-01.json"),
        "nonzero_momentum": load("outputs/yt_nonzero_momentum_correlator_scout_2026-05-01.json"),
        "momentum_harness": load("outputs/yt_momentum_harness_extension_certificate_2026-05-01.json"),
        "heavy_matching": load("outputs/yt_heavy_kinetic_matching_obstruction_2026-05-01.json"),
        "momentum_pilot": load("outputs/yt_momentum_pilot_scaling_certificate_2026-05-01.json"),
        "assumption_stress": load("outputs/yt_pr230_assumption_import_stress_2026-05-01.json"),
        "free_kinetic": load("outputs/yt_free_staggered_kinetic_coefficient_2026-05-01.json"),
        "interacting_kinetic": load("outputs/yt_interacting_kinetic_background_sensitivity_2026-05-01.json"),
        "direct_scale": load("outputs/yt_direct_measurement_scale_requirements_2026-05-01.json"),
    }

    all_present = all(isinstance(cert, dict) for cert in certificates.values())
    all_no_fail = all(int(cert.get("fail_count", 0)) == 0 for cert in certificates.values())
    proposal_allowed = [
        name for name, cert in certificates.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: cert.get("actual_current_surface_status") for name, cert in certificates.items()}

    report("campaign-certificates-present", all_present, f"count={len(certificates)}")
    report("campaign-runners-have-no-fails", all_no_fail, "all loaded certificates have FAIL=0")
    report("no-retained-proposal-authorized", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "direct-route-needs-scale-or-heavy-treatment",
        "scale requirement" in str(statuses["direct_scale"]),
        statuses["direct_scale"],
    )
    report(
        "hqet-route-needs-matching",
        "HQET" in str(statuses["hqet"]) or "route requirement" in str(statuses["hqet"]),
        statuses["hqet"],
    )
    report(
        "legendre-route-needs-residue",
        "Legendre" in str(statuses["legendre"]) or "normalization freedom" in str(statuses["legendre"]),
        statuses["legendre"],
    )
    report(
        "free-bubble-route-needs-interaction",
        "free source pole absence" in str(statuses["free_bubble"]),
        statuses["free_bubble"],
    )
    report(
        "same-1pi-route-needs-lsz",
        "same-1PI" in str(statuses["same_1pi"]),
        statuses["same_1pi"],
    )
    report(
        "lsz-normalization-cancellation-still-needs-kernel",
        "LSZ normalization cancellation" in str(statuses["lsz_norm"])
        or "conditional-support" in str(statuses["lsz_norm"]),
        statuses["lsz_norm"],
    )
    report(
        "feshbach-response-not-common-dressing",
        "Feshbach response boundary" in str(statuses["feshbach_response"])
        or "exact support" in str(statuses["feshbach_response"]),
        statuses["feshbach_response"],
    )
    report(
        "bridge-stack-not-pr230-closure",
        "bridge stack not PR230 closure" in str(statuses["bridge_stack"]),
        statuses["bridge_stack"],
    )
    report(
        "spectral-positivity-needs-saturation-theorem",
        "spectral saturation no-go" in str(statuses["spectral_saturation"]),
        statuses["spectral_saturation"],
    )
    report(
        "finite-ladder-route-needs-ir-limit",
        "zero-mode" in str(statuses["ladder_ir_zero_mode"]),
        statuses["ladder_ir_zero_mode"],
    )
    report(
        "heavy-kinetic-route-needs-data-and-matching",
        "heavy kinetic" in str(statuses["heavy_kinetic"])
        or "bounded-support" in str(statuses["heavy_kinetic"]),
        statuses["heavy_kinetic"],
    )
    report(
        "nonzero-momentum-scout-needs-production-and-matching",
        "nonzero-momentum" in str(statuses["nonzero_momentum"])
        or "bounded-support" in str(statuses["nonzero_momentum"]),
        statuses["nonzero_momentum"],
    )
    report(
        "momentum-harness-extension-needs-production",
        "momentum harness" in str(statuses["momentum_harness"])
        or "bounded-support" in str(statuses["momentum_harness"]),
        statuses["momentum_harness"],
    )
    report(
        "heavy-kinetic-route-needs-matching-theorem",
        "matching" in str(statuses["heavy_matching"]),
        statuses["heavy_matching"],
    )
    report(
        "momentum-pilot-needs-production",
        "momentum pilot" in str(statuses["momentum_pilot"])
        or "bounded-support" in str(statuses["momentum_pilot"]),
        statuses["momentum_pilot"],
    )
    report(
        "assumption-stress-no-shortcuts",
        "assumption-import" in str(statuses["assumption_stress"]),
        statuses["assumption_stress"],
    )
    report(
        "free-kinetic-support-not-interacting-closure",
        "free staggered kinetic coefficient" in str(statuses["free_kinetic"]),
        statuses["free_kinetic"],
    )
    report(
        "interacting-kinetic-needs-ensemble-or-theorem",
        "interacting kinetic" in str(statuses["interacting_kinetic"]),
        statuses["interacting_kinetic"],
    )

    remaining_routes = [
        {
            "route": "strict production direct measurement",
            "needed": "fine-scale relativistic top campaign or validated heavy-quark treatment with matching",
        },
        {
            "route": "new scalar LSZ/canonical normalization theorem",
            "needed": "interacting scalar two-point denominator, isolated pole/canonical kinetic term, residue kappa_H",
        },
        {
            "route": "new heavy-matching observable/theorem",
            "needed": "nonzero-momentum kinetic-mass correlators plus lattice-HQET/NRQCD-to-SM top mass matching without observed top calibration",
        },
    ]

    result = {
        "actual_current_surface_status": "open / campaign exhausted for current analytic shortcuts",
        "verdict": (
            "The current PR #230 physics-loop campaign did not reach retained "
            "top-Yukawa closure.  It did retire the visible shortcut routes: "
            "Ward/H_unit, R_conn-only LSZ, Legendre normalization, free logdet "
            "bubble, contact HS/RPA, simplified ladder projector, same-1PI, "
            "finite ladder IR/zero-mode shortcut, and static/HQET without "
            "matching.  It also isolates a constructive heavy kinetic-mass "
            "route, a tiny nonzero-momentum correlator scout, and production "
            "harness momentum fields.  A bounded two-volume pilot has large "
            "finite-volume drift, so that route still needs production data "
            "and a derived matching theorem.  The free staggered action fixes "
            "its kinetic coefficient, but interacting renormalization remains "
            "open and is gauge-background sensitive.  A covariant scalar LSZ "
            "normalization model shows source scaling can cancel only if the "
            "interacting denominator and residue are derived together.  Exact "
            "Feshbach response preservation removes crossover distortion as the "
            "blocker but does not equate scalar and gauge residues.  The "
            "axiom-first bridge stack is bounded transport support with endpoint "
            "imports, not a missed PR #230 proof.  Spectral positivity and "
            "low-order curvature moments do not fix the isolated pole residue "
            "without saturation/continuum control.  Remaining "
            "closure requires production "
            "evidence or a genuinely new scalar LSZ/heavy-matching theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Open imports remain across every non-production shortcut route.",
        "certificate_statuses": statuses,
        "remaining_routes": remaining_routes,
        "strict_non_claims": [
            "does not claim retained closure",
            "does not demote PR230's scout/proposed evidence",
            "does not use observed top mass or y_t as proof input",
            "does not allow H_unit matrix-element definition as y_t readout",
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
