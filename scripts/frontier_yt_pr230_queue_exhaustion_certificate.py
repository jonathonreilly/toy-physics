#!/usr/bin/env python3
"""
Campaign queue-exhaustion certificate for the PR #230 y_t physics loop.

This is a process runner, not a physics theorem.  It checks that the current
PR branch has explicit artifacts for the main attempted non-MC routes, that
their paired runners passed, and that the claim-status firewall still blocks
retained closure.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / ".claude/science/physics-loops/yt-pr230-retained-closure-12h-20260501"
OUTPUT = ROOT / "outputs" / "yt_pr230_queue_exhaustion_certificate_2026-05-01.json"

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def assert_route_artifacts() -> dict[str, bool]:
    artifacts = {
        "direct_correlator_gate": "docs/YT_DIRECT_LATTICE_CORRELATOR_DERIVATION_THEOREM_NOTE_2026-04-30.md",
        "top_mass_pin_no_go": "docs/YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md",
        "ward_decomp_no_go": "docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md",
        "planck_selector": "docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md",
        "beta_lambda_no_go": "docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "scale_stationarity_no_go": "docs/YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md",
        "trace_anomaly_no_go": "docs/YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "vacuum_stability_no_go": "docs/YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "gauge_input_sensitivity": "docs/YT_PLANCK_SELECTOR_GAUGE_INPUT_SENSITIVITY_NOTE_2026-05-01.md",
        "scale_anchor_sensitivity": "docs/YT_PLANCK_SELECTOR_SCALE_ANCHOR_SENSITIVITY_NOTE_2026-05-01.md",
        "fixed_point_no_go": "docs/YT_ASYMPTOTIC_SAFETY_FIXED_POINT_NO_GO_NOTE_2026-05-01.md",
        "ward_ratio_no_go": "docs/YT_WARD_RATIO_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "qfp_no_go": "docs/YT_QFP_SELECTOR_NO_GO_NOTE_2026-05-01.md",
        "observed_inversion_no_go": "docs/YT_OBSERVED_MASS_INVERSION_NO_GO_NOTE_2026-05-01.md",
        "rge_only_no_go": "docs/YT_RGE_ONLY_SELECTOR_NO_GO_NOTE_2026-05-01.md",
    }
    results = {name: (ROOT / rel).exists() for name, rel in artifacts.items()}
    for name, ok in results.items():
        report(f"artifact-{name}", ok, artifacts[name])
    return results


def assert_runner_outputs() -> dict[str, dict[str, object]]:
    outputs = {
        "planck_selector": "outputs/yt_planck_double_criticality_selector_2026-04-30.json",
        "beta_lambda_no_go": "outputs/yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json",
        "scale_stationarity_no_go": "outputs/yt_scale_stationarity_substrate_no_go_2026-05-01.json",
        "trace_anomaly_no_go": "outputs/yt_trace_anomaly_stationarity_no_go_2026-05-01.json",
        "vacuum_stability_no_go": "outputs/yt_vacuum_stability_stationarity_no_go_2026-05-01.json",
        "assumption_audit": "outputs/yt_pr230_physics_loop_assumption_audit_2026-05-01.json",
        "gauge_input_sensitivity": "outputs/yt_planck_selector_gauge_input_sensitivity_2026-05-01.json",
        "scale_anchor_sensitivity": "outputs/yt_planck_selector_scale_anchor_sensitivity_2026-05-01.json",
        "fixed_point_no_go": "outputs/yt_asymptotic_safety_fixed_point_no_go_2026-05-01.json",
        "ward_ratio_no_go": "outputs/yt_ward_ratio_stationarity_no_go_2026-05-01.json",
        "qfp_no_go": "outputs/yt_qfp_selector_no_go_2026-05-01.json",
        "observed_inversion_no_go": "outputs/yt_observed_mass_inversion_no_go_2026-05-01.json",
        "rge_only_no_go": "outputs/yt_rge_only_selector_no_go_2026-05-01.json",
    }
    results: dict[str, dict[str, object]] = {}
    for name, rel in outputs.items():
        data = load_json(rel)
        ok = data.get("fail_count") == 0
        report(f"runner-{name}", ok, f"pass={data.get('pass_count')} fail={data.get('fail_count')}")
        results[name] = {
            "path": rel,
            "pass_count": data.get("pass_count"),
            "fail_count": data.get("fail_count"),
            "status": data.get("actual_current_surface_status") or data.get("status", {}).get("actual_current_surface_status"),
        }
    return results


def assert_claim_firewall() -> dict[str, object]:
    state = read(LOOP / "STATE.yaml")
    certificate = read(LOOP / "CLAIM_STATUS_CERTIFICATE.md")
    direct_cert = load_json("outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json")

    phase = direct_cert.get("metadata", {}).get("phase")
    open_status = "open / no full retained closure" in state
    proposal_blocked = "proposal_allowed: false" in certificate
    bare_retained_blocked = "bare_retained_allowed: false" in certificate and "bare_retained_allowed: false" in state
    direct_not_production = phase != "production"
    open_imports_recorded = "production correlator data" in certificate and "top-mass parameter pin" in certificate

    checks = {
        "state_open_status": open_status,
        "proposal_blocked": proposal_blocked,
        "bare_retained_blocked": bare_retained_blocked,
        "direct_certificate_not_production": direct_not_production,
        "open_imports_recorded": open_imports_recorded,
    }
    for tag, ok in checks.items():
        report(f"firewall-{tag}", ok, f"{tag}={ok}")

    return {
        "checks": checks,
        "direct_certificate_phase": phase,
    }


def main() -> int:
    print("PR #230 y_t physics-loop queue-exhaustion certificate")
    print("=" * 72)

    artifacts = assert_route_artifacts()
    runners = assert_runner_outputs()
    firewall = assert_claim_firewall()

    result = {
        "actual_current_surface_status": "open / queue exhausted for current non-MC PR230 routes",
        "verdict": (
            "The current PR #230 physics-loop queue has closed the explored "
            "non-MC shortcuts negatively or demoted them to conditional support. "
            "No retained y_t closure is available on the current surface.  The "
            "remaining positive routes are production correlator evidence plus "
            "an independent top-mass parameter pin, a new substrate theorem for "
            "Planck stationarity, or an explicit new selector premise."
        ),
        "artifacts": artifacts,
        "runners": runners,
        "claim_firewall": firewall,
        "remaining_positive_routes": [
            "complete production direct-correlator campaign and supply an independent heavy top-sector mass parameter pin",
            "derive beta_lambda(M_Pl)=0 from new substrate scale/trace boundary structure",
            "adopt beta_lambda(M_Pl)=0 as an explicit selector premise and keep the result conditional",
            "re-permit and independently re-audit the old Ward/H_unit route as a definition source rather than a derivation",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
