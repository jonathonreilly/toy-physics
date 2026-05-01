#!/usr/bin/env python3
"""
PR #230 retained-closure route certificate.

This runner answers the operational question: what is the shortest honest path
from the current PR #230 state to retained top-Yukawa closure?  It does not
claim closure.  It verifies that all non-MC shortcuts currently tested are
blocked or conditional, then records the only remaining closure routes.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_retained_closure_route_certificate_2026-05-01.json"

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


def load_json(path: str) -> dict:
    full = ROOT / path
    if not full.exists():
        return {}
    return json.loads(full.read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 retained-closure route certificate")
    print("=" * 72)

    required_certificates = {
        "global_proof_audit": "outputs/yt_pr230_global_proof_audit_2026-05-01.json",
        "direct_cutoff_obstruction": "outputs/yt_top_mass_cutoff_obstruction_2026-05-01.json",
        "beta_lambda_no_go": "outputs/yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json",
        "queue_exhaustion": "outputs/yt_pr230_queue_exhaustion_certificate_2026-05-01.json",
        "ward_repair_audit": "outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json",
        "scalar_pole_residue_no_go": "outputs/yt_scalar_pole_residue_current_surface_no_go_2026-05-01.json",
    }
    certificates = {name: load_json(path) for name, path in required_certificates.items()}

    direct_certificates = [
        "outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_plus_certificate_2026-05-01.json",
        "outputs/yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json",
    ]
    direct_meta = []
    for path in direct_certificates:
        data = load_json(path)
        metadata = data.get("metadata", {})
        direct_meta.append(
            {
                "path": path,
                "exists": bool(data),
                "phase": metadata.get("phase") or data.get("phase"),
                "strict_pass": data.get("strict_pass") or data.get("strict_validation", {}).get("pass"),
            }
        )

    missing = [name for name, data in certificates.items() if not data]
    no_hidden_proof = certificates["global_proof_audit"].get("retained_y_t_rows") == {}
    direct_strict_pass = any(item.get("phase") == "production" and item.get("strict_pass") is True for item in direct_meta)
    ward_open = certificates["ward_repair_audit"].get("closure_allowed") is False
    scalar_residue_blocked = (
        certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status")
        == "exact negative boundary / retained closure unavailable on current analytic surface"
    )
    beta_blocked = "no-go" in certificates["beta_lambda_no_go"].get("actual_current_surface_status", "")
    queue_text = (
        certificates["queue_exhaustion"].get("actual_current_surface_status", "")
        + " "
        + certificates["queue_exhaustion"].get("verdict", "")
    ).lower()
    queue_open = "queue exhausted" in queue_text and "no retained" in queue_text

    report("required-certificates-present", not missing, f"missing={missing}")
    report("no-hidden-retained-yt-proof", no_hidden_proof, "global audit retained_y_t_rows empty")
    report("direct-strict-production-not-yet-passed", not direct_strict_pass, f"direct_meta={direct_meta}")
    report("ward-repair-still-open", ward_open, f"closure_allowed={certificates['ward_repair_audit'].get('closure_allowed')}")
    report("scalar-pole-residue-blocked-on-current-surface", scalar_residue_blocked, certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status", ""))
    report("planck-beta-route-blocked-on-current-surface", beta_blocked, certificates["beta_lambda_no_go"].get("actual_current_surface_status", ""))
    report("prior-route-queue-exhausted", queue_open, "queue exhaustion certificate says no full retained closure")

    closure_routes = [
        {
            "route": "direct_measurement",
            "retained_closure_condition": (
                "run strict production correlator evidence on a physically suitable "
                "scale/heavy-quark treatment, produce a production certificate, and "
                "pass scripts/frontier_yt_direct_lattice_correlator.py"
            ),
            "why_shortest": "It bypasses Ward/H_unit and scalar-pole analytic normalization.",
            "current_blocker": "existing certificates are reduced-scope/pilot; mass-bracket shows current scale cutoff obstruction",
        },
        {
            "route": "analytic_scalar_residue",
            "retained_closure_condition": (
                "derive scalar source two-point pole residue, scalar carrier map, "
                "and common scalar/gauge dressing from retained dynamics, then "
                "re-run the Ward physical-readout repair audit"
            ),
            "why_shortest": "It directly repairs the audit's physical-readout objection.",
            "current_blocker": "current algebraic surface underdetermines pole residue and dressing",
        },
        {
            "route": "new_selector_or_axiom",
            "retained_closure_condition": (
                "derive beta_lambda(M_Pl)=0 or explicitly add a new selector/premise; "
                "the latter is not retained closure under the current one-axiom surface"
            ),
            "why_shortest": "It can reproduce numerical y_t if the selector is accepted.",
            "current_blocker": "all current stationarity shortcuts are no-go/conditional",
        },
    ]

    result = {
        "actual_current_surface_status": "open / retained closure not yet reached",
        "verdict": (
            "The current PR #230 surface has no retained top-Yukawa closure.  "
            "All tested non-MC shortcuts are blocked or conditional.  The shortest "
            "honest retained routes are: strict direct physical measurement, a new "
            "scalar pole-residue/common-dressing theorem, or a newly derived "
            "Planck stationarity selector.  The first two preserve the current "
            "claim posture; the third requires a new theorem and cannot be merely "
            "assumed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No route currently satisfies retained-proposal conditions.",
        "direct_certificates": direct_meta,
        "required_certificates": required_certificates,
        "closure_routes": closure_routes,
        "exact_next_action": (
            "Do not run more small pilot MC for closure.  Either implement a "
            "physically suitable strict measurement plan, or start the scalar "
            "two-point residue theorem from the retained action and expect that "
            "it may require real correlator data."
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
