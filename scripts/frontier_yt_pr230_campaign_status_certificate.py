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
        "large_nc": load("outputs/yt_large_nc_pole_dominance_boundary_2026-05-01.json"),
        "production_resource": load("outputs/yt_production_resource_projection_2026-05-01.json"),
        "feynman_hellmann": load("outputs/yt_feynman_hellmann_source_response_route_2026-05-01.json"),
        "mass_response": load("outputs/yt_mass_response_bracket_certificate_2026-05-01.json"),
        "source_reparametrization": load("outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json"),
        "canonical_scalar_import": load("outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json"),
        "source_to_higgs_lsz": load("outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json"),
        "cl3_source_unit": load("outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json"),
        "scalar_source_response_harness": load("outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json"),
        "fh_production_protocol": load("outputs/yt_fh_production_protocol_certificate_2026-05-01.json"),
        "same_source_scalar_two_point": load("outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json"),
        "bs_kernel_residue_degeneracy": load("outputs/yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json"),
        "scalar_two_point_harness": load("outputs/yt_scalar_two_point_harness_certificate_2026-05-01.json"),
        "fh_lsz_joint_harness": load("outputs/yt_fh_lsz_joint_harness_certificate_2026-05-01.json"),
        "fh_lsz_joint_resource": load("outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json"),
        "fh_lsz_production_manifest": load("outputs/yt_fh_lsz_production_manifest_2026-05-01.json"),
        "fh_lsz_invariant_readout": load("outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"),
        "scalar_pole_determinant_gate": load("outputs/yt_scalar_pole_determinant_gate_2026-05-01.json"),
        "scalar_ladder_eigen_derivative": load("outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json"),
        "scalar_ladder_total_momentum_derivative": load("outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json"),
        "scalar_ladder_derivative_limit": load("outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json"),
        "scalar_ladder_residue_envelope": load("outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json"),
        "scalar_kernel_ward_identity": load("outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json"),
        "scalar_zero_mode_limit_order": load("outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json"),
        "zero_mode_prescription_import": load("outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json"),
        "flat_toron_denominator": load("outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json"),
        "flat_toron_washout": load("outputs/yt_flat_toron_thermodynamic_washout_2026-05-01.json"),
        "color_singlet_zero_mode": load("outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json"),
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
        "retained_closure_route": load("outputs/yt_retained_closure_route_certificate_2026-05-01.json"),
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
        "large-nc-pole-dominance-needs-finite-nc-bound",
        "large-Nc pole dominance" in str(statuses["large_nc"]),
        statuses["large_nc"],
    )
    report(
        "production-resource-projection-not-evidence",
        "production resource projection" in str(statuses["production_resource"]),
        statuses["production_resource"],
    )
    report(
        "feynman-hellmann-still-needs-source-normalization",
        "Feynman-Hellmann" in str(statuses["feynman_hellmann"])
        or "source-response" in str(statuses["feynman_hellmann"]),
        statuses["feynman_hellmann"],
    )
    report(
        "mass-response-bracket-is-bare-source-only",
        "mass-response" in str(statuses["mass_response"]),
        statuses["mass_response"],
    )
    report(
        "source-reparametrization-gauge-blocks-source-only-closure",
        "source reparametrization" in str(statuses["source_reparametrization"]),
        statuses["source_reparametrization"],
    )
    report(
        "canonical-scalar-normalization-not-hidden-proof",
        "canonical scalar normalization" in str(statuses["canonical_scalar_import"]),
        statuses["canonical_scalar_import"],
    )
    report(
        "source-to-higgs-lsz-closure-still-open",
        "source-to-Higgs" in str(statuses["source_to_higgs_lsz"])
        or "LSZ closure attempt" in str(statuses["source_to_higgs_lsz"]),
        statuses["source_to_higgs_lsz"],
    )
    report(
        "cl3-source-unit-does-not-fix-kappa",
        "Cl3 source-unit" in str(statuses["cl3_source_unit"])
        or "source-unit normalization no-go" in str(statuses["cl3_source_unit"]),
        statuses["cl3_source_unit"],
    )
    report(
        "scalar-source-response-harness-needs-kappa",
        "scalar source response harness" in str(statuses["scalar_source_response_harness"])
        or "bounded-support" in str(statuses["scalar_source_response_harness"]),
        statuses["scalar_source_response_harness"],
    )
    report(
        "fh-production-protocol-needs-production-and-kappa",
        "Feynman-Hellmann production protocol" in str(statuses["fh_production_protocol"])
        or "bounded-support" in str(statuses["fh_production_protocol"]),
        statuses["fh_production_protocol"],
    )
    report(
        "same-source-scalar-two-point-needs-pole-and-continuum",
        "same-source scalar two-point" in str(statuses["same_source_scalar_two_point"])
        or "bounded-support" in str(statuses["same_source_scalar_two_point"]),
        statuses["same_source_scalar_two_point"],
    )
    report(
        "bs-kernel-residue-degeneracy-needs-denominator-theorem",
        "Bethe-Salpeter" in str(statuses["bs_kernel_residue_degeneracy"])
        or "pole-residue degeneracy" in str(statuses["bs_kernel_residue_degeneracy"]),
        statuses["bs_kernel_residue_degeneracy"],
    )
    report(
        "scalar-two-point-harness-needs-production-and-lsz",
        "scalar two-point production-harness" in str(statuses["scalar_two_point_harness"])
        or "bounded-support" in str(statuses["scalar_two_point_harness"]),
        statuses["scalar_two_point_harness"],
    )
    report(
        "fh-lsz-joint-harness-needs-production-and-kappa",
        "Feynman-Hellmann scalar-LSZ" in str(statuses["fh_lsz_joint_harness"])
        or "bounded-support" in str(statuses["fh_lsz_joint_harness"]),
        statuses["fh_lsz_joint_harness"],
    )
    report(
        "fh-lsz-joint-resource-projection-not-evidence",
        "resource projection" in str(statuses["fh_lsz_joint_resource"])
        or "bounded-support" in str(statuses["fh_lsz_joint_resource"]),
        statuses["fh_lsz_joint_resource"],
    )
    report(
        "fh-lsz-production-manifest-not-evidence",
        "production manifest" in str(statuses["fh_lsz_production_manifest"])
        or "bounded-support" in str(statuses["fh_lsz_production_manifest"]),
        statuses["fh_lsz_production_manifest"],
    )
    report(
        "fh-lsz-invariant-readout-still-needs-pole-data",
        "invariant readout formula" in str(statuses["fh_lsz_invariant_readout"])
        or "exact-support" in str(statuses["fh_lsz_invariant_readout"]),
        statuses["fh_lsz_invariant_readout"],
    )
    report(
        "scalar-pole-determinant-gate-still-needs-kernel",
        "determinant gate" in str(statuses["scalar_pole_determinant_gate"])
        or "exact-support" in str(statuses["scalar_pole_determinant_gate"]),
        statuses["scalar_pole_determinant_gate"],
    )
    report(
        "scalar-ladder-eigen-derivative-gate-still-needs-momentum-kernel",
        "eigen-derivative gate" in str(statuses["scalar_ladder_eigen_derivative"])
        or "exact-support" in str(statuses["scalar_ladder_eigen_derivative"]),
        statuses["scalar_ladder_eigen_derivative"],
    )
    report(
        "scalar-ladder-total-momentum-derivative-scout-not-limit",
        "total-momentum derivative scout" in str(statuses["scalar_ladder_total_momentum_derivative"])
        or "bounded-support" in str(statuses["scalar_ladder_total_momentum_derivative"]),
        statuses["scalar_ladder_total_momentum_derivative"],
    )
    report(
        "scalar-ladder-derivative-limit-needs-zero-mode-theorem",
        "limiting-order obstruction" in str(statuses["scalar_ladder_derivative_limit"])
        or "exact negative boundary" in str(statuses["scalar_ladder_derivative_limit"]),
        statuses["scalar_ladder_derivative_limit"],
    )
    report(
        "scalar-ladder-residue-envelope-not-lsz-bound",
        "residue-envelope obstruction" in str(statuses["scalar_ladder_residue_envelope"])
        or "exact negative boundary" in str(statuses["scalar_ladder_residue_envelope"]),
        statuses["scalar_ladder_residue_envelope"],
    )
    report(
        "scalar-kernel-ward-identity-not-k-prime-theorem",
        "Ward-identity obstruction" in str(statuses["scalar_kernel_ward_identity"])
        or "exact negative boundary" in str(statuses["scalar_kernel_ward_identity"]),
        statuses["scalar_kernel_ward_identity"],
    )
    report(
        "scalar-zero-mode-limit-order-needs-prescription",
        "zero-mode limit-order theorem" in str(statuses["scalar_zero_mode_limit_order"])
        or "exact negative boundary" in str(statuses["scalar_zero_mode_limit_order"]),
        statuses["scalar_zero_mode_limit_order"],
    )
    report(
        "zero-mode-prescription-import-audit-not-closure",
        "zero-mode prescription import audit" in str(statuses["zero_mode_prescription_import"])
        or "exact negative boundary" in str(statuses["zero_mode_prescription_import"]),
        statuses["zero_mode_prescription_import"],
    )
    report(
        "flat-toron-sectors-change-scalar-denominator",
        "flat toron scalar-denominator obstruction" in str(statuses["flat_toron_denominator"])
        or "exact negative boundary" in str(statuses["flat_toron_denominator"]),
        statuses["flat_toron_denominator"],
    )
    report(
        "flat-toron-thermodynamic-washout-not-closure",
        "flat toron thermodynamic washout" in str(statuses["flat_toron_washout"])
        or "exact-support" in str(statuses["flat_toron_washout"]),
        statuses["flat_toron_washout"],
    )
    report(
        "color-singlet-zero-mode-cancellation-not-closure",
        "color-singlet gauge-zero-mode cancellation" in str(statuses["color_singlet_zero_mode"])
        or "exact-support" in str(statuses["color_singlet_zero_mode"]),
        statuses["color_singlet_zero_mode"],
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
    report(
        "retained-closure-route-certificate-still-open",
        "retained closure not yet reached" in str(statuses["retained_closure_route"]),
        statuses["retained_closure_route"],
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
        {
            "route": "Feynman-Hellmann source-response measurement",
            "needed": "production dE/ds data plus scalar LSZ/canonical-Higgs normalization kappa_s and response matching",
        },
    ]

    result = {
        "actual_current_surface_status": "open / active campaign continuing after current shortcut blocks",
        "verdict": (
            "The current PR #230 physics-loop checkpoint has not reached "
            "retained top-Yukawa closure.  It did retire the visible shortcut "
            "routes: "
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
            "without saturation/continuum control; large-Nc pole dominance is "
            "not a finite-Nc proof at N_c=3.  The production resource "
            "projection makes the strict direct route concrete as a multi-day "
            "single-worker job, but it is not measurement evidence.  A "
            "Feynman-Hellmann top-energy response can remove additive rest "
            "mass, but still needs scalar source-to-Higgs normalization and "
            "production response data; the reduced mass-bracket response is "
            "bare-source support only.  The source-reparametrization gauge "
            "boundary shows source-only analytic routes cannot close without "
            "canonical scalar normalization, and the strongest existing "
            "EW/Higgs structural notes do not supply that hidden proof.  "
            "The explicit source-to-Higgs LSZ closure attempt finds no allowed "
            "premise that fixes kappa_s.  The harness now supports explicit "
            "uniform scalar-source shifts and emits dE/ds response analysis, "
            "which advances the Feynman-Hellmann measurement route but still "
            "does not convert to physical dE/dh without kappa_s.  Remaining "
            "closure requires production evidence or a genuinely new scalar "
            "LSZ/heavy-matching theorem.  The production Feynman-Hellmann "
            "protocol is now specified: common-ensemble symmetric source "
            "shifts, correlated dE/ds fits, and a separate scalar two-point "
            "LSZ measurement to determine kappa_s.  The same-source scalar "
            "two-point object C_ss(q) is now executable on a tiny exact lattice, "
            "but the reduced primitive has no controlled pole/continuum limit "
            "and its finite residue proxy is mass-dependent.  A finite "
            "Wilson-exchange scalar ladder total-momentum derivative can be "
            "computed, but the derivative magnitude is strongly "
            "prescription-sensitive and is not a retained limiting theorem.  "
            "A direct IR-limiting scout shows why: keeping the gauge zero mode "
            "makes the derivative grow and changes the pole-test crossing, "
            "while removing it gives a different stable surface.  The Cl(3)/Z3 "
            "source unit fixes the additive source coordinate but not the "
            "canonical Higgs field normalization.  The joint FH/LSZ production "
            "path now has exact launch commands, but the manifest is not "
            "production evidence.  The refreshed retained-closure route "
            "certificate still authorizes no proposed-retained wording.  A "
            "pole-tuned finite ladder residue envelope also fails to select a "
            "unique LSZ input across current zero-mode, projector, and volume "
            "choices.  Existing Ward/gauge/Feshbach surfaces also do not fix "
            "the scalar kernel derivative K'(x_pole)."
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
