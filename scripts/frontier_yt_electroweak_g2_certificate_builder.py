#!/usr/bin/env python3
"""
PR #230 electroweak g2 certificate builder gate.

The same-source W/Z route needs a strict non-observed g2 certificate at
outputs/yt_electroweak_g2_certificate_2026-05-04.json.  This builder does not
mint that certificate on the current surface.  It audits the available
candidate authorities and records why none is load-bearing for PR #230 under
the active claim firewall.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_electroweak_g2_certificate_builder_2026-05-05.json"
STRICT_CERT = ROOT / "outputs" / "yt_electroweak_g2_certificate_2026-05-04.json"

USABLE_INDEX = ROOT / "docs" / "publication" / "ci3_z3" / "USABLE_DERIVED_VALUES_INDEX.md"
EW_COLOR_NOTE = ROOT / "docs" / "YT_EW_COLOR_PROJECTION_THEOREM.md"
EW_DELTA_R_NOTE = ROOT / "docs" / "YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md"
W_MASS_NOTE = ROOT / "docs" / "W_MASS_DERIVED_NOTE.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "AUDIT_LEDGER.md"

PARENTS = {
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
}

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
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


def contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def main() -> int:
    print("PR #230 electroweak g2 certificate builder gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    usable_text = read_text(USABLE_INDEX)
    ew_color_text = read_text(EW_COLOR_NOTE)
    ew_delta_text = read_text(EW_DELTA_R_NOTE)
    w_mass_text = read_text(W_MASS_NOTE)
    audit_text = read_text(AUDIT_LEDGER)
    strict_cert = json.loads(STRICT_CERT.read_text(encoding="utf-8")) if STRICT_CERT.exists() else {}

    package_g2_present = bool(re.search(r"`g_2\(v\)`\s*\|\s*`0\.6480`", usable_text))
    package_uses_forbidden_pr230_inputs = contains_any(
        usable_text + ew_color_text + ew_delta_text,
        ("plaquette", "u_0", "R_conn", "observed", "Observed", "PDG", "alpha_EM"),
    )
    bare_g2_present = "g_2^2" in ew_color_text and "1/4" in ew_color_text
    bare_to_v_bridge_uses_forbidden_inputs = contains_any(
        ew_color_text + ew_delta_text,
        ("taste staircase", "plaquette", "u_0", "R_conn", "observed", "Observed"),
    )
    w_mass_route_uses_existing_g2_or_observed_context = (
        "g_2(v)" in w_mass_text and contains_any(w_mass_text, ("observed", "PDG", "CDF", "ATLAS", "CMS", "LHCb"))
    )
    audit_blocks_silent_import = contains_any(
        audit_text,
        (
            "not safe to claim the retained physical EW couplings are independently derived",
            "not safe to claim a retained EW-coupling derivation",
            "EW coupling authority caveats",
        ),
    )
    response_self_normalization_blocked = (
        "WZ response-only g2 self-normalization no-go"
        in parents["wz_g2_response_self_normalization_no_go"].get(
            "actual_current_surface_status", ""
        )
        and parents["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
    )
    row_builder_requires_strict_cert = (
        "electroweak g2 certificate absent"
        in parents["wz_mass_fit_response_row_builder"].get("g2_validation", {}).get(
            "failed_checks", []
        )
    )

    candidates = [
        {
            "name": "strict_certificate_file",
            "path": rel(STRICT_CERT),
            "present": bool(strict_cert),
            "accepted": False,
            "rejection": "strict certificate file is absent",
        },
        {
            "name": "repo_package_g2_v",
            "path": rel(USABLE_INDEX),
            "present": package_g2_present,
            "accepted": False,
            "rejection": "package g_2(v) is tied to plaquette/R_conn/running/observed-comparison authority forbidden as PR230 proof input",
        },
        {
            "name": "bare_geometry_g2_squared_one_quarter",
            "path": rel(EW_COLOR_NOTE),
            "present": bare_g2_present,
            "accepted": False,
            "rejection": "bare g2^2=1/4 does not by itself certify the PR230 low-scale physical g2 without an allowed running/matching bridge",
        },
        {
            "name": "w_mass_same_surface_probe",
            "path": rel(W_MASS_NOTE),
            "present": "g_2(v)" in w_mass_text,
            "accepted": False,
            "rejection": "W-mass companion reuses the existing EW g2 lane and observed-context comparisons; it is not independent g2 authority",
        },
        {
            "name": "response_only_self_normalization",
            "path": PARENTS["wz_g2_response_self_normalization_no_go"],
            "present": response_self_normalization_blocked,
            "accepted": False,
            "rejection": "response-only top/W/Z rows determine ratios, not absolute g2",
        },
    ]
    accepted_candidates = [candidate for candidate in candidates if candidate["accepted"]]

    strict_candidate_valid = (
        bool(strict_cert)
        and strict_cert.get("proposal_allowed") is False
        and strict_cert.get("used_observed_g2_as_selector") is False
        and strict_cert.get("uses_alpha_lm_or_plaquette_or_u0") is False
        and strict_cert.get("strict_electroweak_g2_certificate_passed") is True
    )
    builder_passed = bool(accepted_candidates) and strict_candidate_valid

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("strict-g2-certificate-absent", not strict_cert, rel(STRICT_CERT))
    report("wz-row-builder-requires-strict-g2-cert", row_builder_requires_strict_cert, PARENTS["wz_mass_fit_response_row_builder"])
    report("package-g2-present", package_g2_present, rel(USABLE_INDEX))
    report("package-g2-rejected-for-pr230-firewall", package_uses_forbidden_pr230_inputs and audit_blocks_silent_import, "forbidden package dependencies/audit caveats")
    report("bare-g2-present-but-not-low-scale-cert", bare_g2_present and bare_to_v_bridge_uses_forbidden_inputs, rel(EW_COLOR_NOTE))
    report("w-mass-probe-not-independent-g2-authority", w_mass_route_uses_existing_g2_or_observed_context, rel(W_MASS_NOTE))
    report("response-only-self-normalization-blocked", response_self_normalization_blocked, PARENTS["wz_g2_response_self_normalization_no_go"])
    report("no-accepted-g2-candidate", not accepted_candidates, f"accepted={accepted_candidates}")
    report("strict-electroweak-g2-certificate-not-built", not builder_passed, f"builder_passed={builder_passed}")
    report("does-not-authorize-retained-proposal", True, "builder gate only")

    result = {
        "actual_current_surface_status": "open / electroweak g2 certificate builder inputs absent",
        "proposal_allowed": False,
        "proposal_allowed_reason": "No accepted non-observed, non-forbidden PR230 g2 authority candidate is present.",
        "bare_retained_allowed": False,
        "strict_electroweak_g2_certificate_passed": False,
        "strict_certificate_output": rel(STRICT_CERT),
        "strict_certificate_written": False,
        "parent_certificates": PARENTS,
        "candidate_authorities": candidates,
        "accepted_candidates": accepted_candidates,
        "rejected_shortcuts": [
            "observed g2 or observed W/Z/top/y_t selectors",
            "repo package g_2(v) when its load-bearing path uses plaquette/u0/R_conn or audit-caveated EW authority",
            "bare g2^2=1/4 without an allowed PR230 low-scale running/matching bridge",
            "W-mass companion rows that reuse the existing EW g2 lane",
            "response-only W/Z self-normalization",
        ],
        "required_future_certificate_fields": [
            "g2",
            "phase",
            "strict_electroweak_g2_certificate_passed=true",
            "used_observed_g2_as_selector=false",
            "uses_alpha_lm_or_plaquette_or_u0=false",
            "uses_package_g2_without_new_authority=false",
            "authority_path",
            "uncertainty_or_exact_status",
            "proposal_allowed=false",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write the strict g2 certificate",
            "does not import observed g2, observed W/Z, observed top mass, or observed y_t",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use alpha_LM, plaquette, u0, or the package g2 as proof authority",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Build a real allowed authority path for g2, e.g. a non-plaquette "
            "absolute EW normalization theorem or a strict measurement/certificate "
            "that satisfies the required future fields, then rerun the W/Z mass-fit "
            "response-row builder and full PR230 assembly gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
