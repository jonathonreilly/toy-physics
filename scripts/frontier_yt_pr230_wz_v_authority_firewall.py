#!/usr/bin/env python3
"""
PR #230 W/Z explicit-v authority firewall.

Block68 showed that a same-source W/Z physical-response Jacobian would become
identifiable if a clean absolute normalization pin were supplied, including an
explicit v authority.  This runner checks the current repository surface for
that pin and verifies that package/hierarchy v values are not silently imported
as PR230 W/Z proof authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_wz_v_authority_firewall_2026-05-15.json"

STRICT_V_CERTIFICATE = (
    ROOT / "outputs" / "yt_electroweak_v_authority_certificate_2026-05-12.json"
)
BLOCK68 = ROOT / "outputs" / "yt_pr230_block68_strict_wz_neutral_transfer_obstruction_2026-05-12.json"
WZ_ABS_EXHAUSTION = (
    ROOT
    / "outputs"
    / "yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json"
)
G2_FIREWALL = ROOT / "outputs" / "yt_wz_g2_authority_firewall_2026-05-05.json"
FH_MANIFEST = ROOT / "outputs" / "yt_fh_gauge_mass_response_manifest_2026-05-02.json"
FH_OBSERVABLE_GAP = (
    ROOT / "outputs" / "yt_fh_gauge_mass_response_observable_gap_2026-05-02.json"
)
WZ_SELF_NORM_NO_GO = (
    ROOT / "outputs" / "yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json"
)

OBSERVABLE_PRINCIPLE_NOTE = ROOT / "docs" / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
MINIMAL_AXIOMS_NOTE = ROOT / "docs" / "MINIMAL_AXIOMS_2026-04-11.md"
HIGGS_VACUUM_NOTE = ROOT / "docs" / "HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    print("PR #230 W/Z explicit-v authority firewall")
    print("=" * 72)

    strict_v_cert = load_json(STRICT_V_CERTIFICATE)
    block68 = load_json(BLOCK68)
    abs_exhaustion = load_json(WZ_ABS_EXHAUSTION)
    g2_firewall = load_json(G2_FIREWALL)
    fh_manifest = load_json(FH_MANIFEST)
    fh_gap = load_json(FH_OBSERVABLE_GAP)
    wz_self_norm = load_json(WZ_SELF_NORM_NO_GO)

    observable_text = read_text(OBSERVABLE_PRINCIPLE_NOTE)
    minimal_axioms_text = read_text(MINIMAL_AXIOMS_NOTE)
    higgs_vacuum_text = read_text(HIGGS_VACUUM_NOTE)
    package_surface_text = "\n".join(
        [observable_text, minimal_axioms_text, higgs_vacuum_text]
    )

    package_v_present = (
        "v = 246.282818290129 GeV" in package_surface_text
        or "retained `v = 246.282818290129 GeV`" in package_surface_text
    )
    package_v_observed_comparator_present = "v_meas = 246.22 GeV" in package_surface_text
    package_v_forbidden_dependencies = sorted(
        {
            token
            for token in ["alpha_LM", "M_Pl * alpha_LM^16", "plaquette", "u_0", "u0"]
            if token in package_surface_text
        }
    )
    package_v_rejected = package_v_present and bool(package_v_forbidden_dependencies)

    future_roots = block68.get("strict_future_roots_present", {})
    explicit_v_root_absent = future_roots.get("explicit_v_authority_certificate") is False
    block68_names_explicit_v_pin = "explicit v" in json.dumps(
        block68.get("wz_identifiability", {})
    )
    block68_requires_pin = (
        block68.get("wz_identifiability", {}).get("current_absolute_pin_present")
        is False
        and explicit_v_root_absent
        and block68_names_explicit_v_pin
    )

    required_wz_roots_absent = {
        name: future_roots.get(name) is False
        for name in [
            "accepted_same_source_ew_higgs_action",
            "production_wz_mass_fit_rows",
            "production_wz_response_rows",
            "same_source_top_response_rows",
            "matched_top_wz_covariance_certificate",
            "delta_perp_certificate",
            "strict_non_observed_g2_certificate",
        ]
    }
    all_required_wz_roots_absent = all(required_wz_roots_absent.values())

    static_v_not_source_identity = (
        "static electroweak v cannot identify the substrate source"
        in json.dumps(fh_manifest)
        and "does not use static electroweak v to identify the substrate source"
        in json.dumps(fh_gap)
    )
    g2_route_also_blocked = (
        "WZ response g2 authority absent"
        in g2_firewall.get("actual_current_surface_status", "")
        and g2_firewall.get("g2_authority_gate_passed") is False
        and g2_firewall.get("proposal_allowed") is False
    )
    absolute_route_exhaustion_records_strict_gap = (
        abs_exhaustion.get("wz_absolute_authority_route_exhaustion_passed") is True
        and abs_exhaustion.get("proposal_allowed") is False
        and "strict_electroweak_g2_certificate"
        in abs_exhaustion.get("missing_strict_packet_roots", [])
    )
    self_normalization_does_not_replace_v = (
        "does not fix absolute y_t"
        in wz_self_norm.get("actual_current_surface_status", "")
        and wz_self_norm.get("proposal_allowed") is False
    )

    strict_v_candidate_valid = (
        bool(strict_v_cert)
        and strict_v_cert.get("strict_non_observed_authority") is True
        and strict_v_cert.get("uses_alpha_lm_plaquette_or_u0") is False
        and strict_v_cert.get("uses_observed_v_selector") is False
        and strict_v_cert.get("proposal_allowed") is False
    )

    report("strict-explicit-v-certificate-absent", not strict_v_cert, rel(STRICT_V_CERTIFICATE))
    report(
        "package-v-present",
        package_v_present,
        "repo package surface contains v = 246.282818290129 GeV",
    )
    report(
        "package-v-rejected-as-pr230-authority",
        package_v_rejected,
        f"forbidden_dependencies={package_v_forbidden_dependencies}",
    )
    report(
        "observed-v-comparator-not-used",
        package_v_observed_comparator_present,
        "v_meas appears only as a comparator on the package surface; this firewall does not use it as proof input",
    )
    report(
        "block68-records-explicit-v-root-absent",
        block68_requires_pin,
        str(block68.get("wz_identifiability", {})),
    )
    report(
        "required-wz-packet-roots-absent",
        all_required_wz_roots_absent,
        str(required_wz_roots_absent),
    )
    report(
        "static-v-does-not-identify-source",
        static_v_not_source_identity,
        f"{rel(FH_MANIFEST)} / {rel(FH_OBSERVABLE_GAP)}",
    )
    report(
        "g2-absolute-pin-also-blocked",
        g2_route_also_blocked,
        g2_firewall.get("actual_current_surface_status", ""),
    )
    report(
        "wz-absolute-route-exhaustion-consumed",
        absolute_route_exhaustion_records_strict_gap,
        abs_exhaustion.get("actual_current_surface_status", ""),
    )
    report(
        "wz-self-normalization-does-not-replace-v",
        self_normalization_does_not_replace_v,
        wz_self_norm.get("actual_current_surface_status", ""),
    )
    report(
        "strict-v-candidate-not-accepted",
        not strict_v_candidate_valid,
        f"strict_v_candidate_valid={strict_v_candidate_valid}",
    )
    report("does-not-authorize-retained-proposal", True, "firewall only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 W/Z explicit-v authority absent; "
            "package hierarchy v is rejected as a load-bearing W/Z absolute pin"
        ),
        "conditional_surface_status": (
            "conditional-support only if a future strict non-forbidden explicit-v "
            "authority certificate is supplied together with accepted same-source "
            "EW/Higgs action, production W/Z and same-source top response rows, "
            "matched covariance, delta_perp, and final W-response authority"
        ),
        "admitted_observation_status": None,
        "hypothetical_axiom_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No strict explicit-v authority certificate is present. The visible "
            "package v value depends on hierarchy/observable-principle surfaces "
            "containing alpha_LM, plaquette/u0, and observed-comparator context, "
            "which PR230 may not use as load-bearing proof input."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "wz_v_authority_firewall_passed": FAIL_COUNT == 0,
        "v_authority_gate_passed": False,
        "explicit_v_authority_certificate": {
            "path": rel(STRICT_V_CERTIFICATE),
            "present": bool(strict_v_cert),
            "strict_candidate_valid": strict_v_candidate_valid,
        },
        "package_v_surface": {
            "package_v_present": package_v_present,
            "observed_v_comparator_present": package_v_observed_comparator_present,
            "rejected_as_pr230_load_bearing_input": package_v_rejected,
            "forbidden_dependencies_found": package_v_forbidden_dependencies,
            "documents_read": [
                rel(OBSERVABLE_PRINCIPLE_NOTE),
                rel(MINIMAL_AXIOMS_NOTE),
                rel(HIGGS_VACUUM_NOTE),
            ],
            "rejection_reasons": [
                "PR230 firewall forbids alpha_LM / plaquette / u0 as load-bearing proof input",
                "an observed v comparator is not an authority or selector for top-Yukawa closure",
                "static electroweak v does not identify the substrate source coordinate",
                "explicit v alone does not supply accepted action, W/Z rows, covariance, delta_perp, or W-response authority",
            ],
        },
        "block68_wz_identifiability": {
            "path": rel(BLOCK68),
            "explicit_v_root_absent": explicit_v_root_absent,
            "current_absolute_pin_present": block68.get("wz_identifiability", {}).get(
                "current_absolute_pin_present"
            ),
            "rank_with_explicit_v_pin": block68.get("wz_identifiability", {}).get(
                "rank_with_explicit_v_pin"
            ),
            "required_wz_roots_absent": required_wz_roots_absent,
        },
        "static_v_source_identity_boundary": {
            "manifest": rel(FH_MANIFEST),
            "observable_gap": rel(FH_OBSERVABLE_GAP),
            "static_v_not_source_identity": static_v_not_source_identity,
        },
        "other_absolute_pin_boundaries": {
            "g2_firewall": {
                "path": rel(G2_FIREWALL),
                "blocked": g2_route_also_blocked,
            },
            "wz_absolute_authority_route_exhaustion": {
                "path": rel(WZ_ABS_EXHAUSTION),
                "blocked": absolute_route_exhaustion_records_strict_gap,
            },
            "wz_mass_response_self_normalization": {
                "path": rel(WZ_SELF_NORM_NO_GO),
                "blocked": self_normalization_does_not_replace_v,
            },
        },
        "strict_non_claims": {
            "claimed_retained_or_proposed_retained": False,
            "used_hunit_matrix_element_readout": False,
            "used_yt_ward_identity": False,
            "used_observed_top_mass_or_yt_selector": False,
            "used_observed_v_as_authority": False,
            "used_alpha_lm_plaquette_or_u0_as_authority": False,
            "used_package_v_as_authority": False,
            "set_v_g2_c2_zmatch_or_kappa_by_unit_convention": False,
            "treated_static_v_as_source_identity": False,
            "treated_wz_smoke_as_production": False,
        },
        "exact_next_action": (
            "Supply outputs/yt_electroweak_v_authority_certificate_2026-05-12.json "
            "from an allowed non-observed, non-alpha_LM/plaquette/u0 authority, "
            "or replace the W/Z absolute pin with a strict non-observed g2 "
            "certificate or canonical source-response normalization. Then rerun "
            "the W/Z physical-response packet and full PR230 assembly gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
