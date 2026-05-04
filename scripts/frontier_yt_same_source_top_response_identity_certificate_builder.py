#!/usr/bin/env python3
"""
PR #230 same-source top-response identity certificate builder.

The top-response certificate needs one identity object that says the measured
same-source top response is allowed to be treated as the canonical-Higgs/top
response used by the W/Z route.  This runner makes that identity contract
explicit.  On the current surface it stays open because the sector-overlap,
canonical-Higgs pole identity, no-orthogonal-top-coupling, and retained-route
premises remain blocked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IDENTITY_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_identity_certificate_2026-05-04.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_identity_certificate_builder_2026-05-04.json"
SCOUT_IDENTITY_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_identity_certificate_builder_scout_certificate_2026-05-04.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_identity_certificate_builder_scout_2026-05-04.json"

PARENTS = {
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "higgs_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "neutral_scalar_rank_one_purity": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "same_source_wz_response": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FIREWALL_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_observed_WZ_masses_as_selector",
    "used_H_unit_or_Ward_authority",
    "used_alpha_lm_plaquette_or_u0",
    "used_c2_or_zmatch_equal_one",
    "used_kappa_or_cos_theta_by_fiat",
)

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


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def parent_statuses(parents: dict[str, dict[str, Any]]) -> dict[str, str]:
    return {name: status(cert) for name, cert in parents.items()}


def evaluate_current_identity(parents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    sector = parents["same_source_sector_overlap"]
    higgs_gate = parents["fh_lsz_higgs_pole_identity"]
    latest = parents["higgs_identity_latest_blocker"]
    mixing = parents["source_pole_canonical_higgs_mixing"]
    no_orthogonal = parents["no_orthogonal_top_coupling_selection"]
    gram = parents["source_higgs_gram_purity"]
    rank_one = parents["neutral_scalar_rank_one_purity"]
    wz = parents["same_source_wz_response"]
    retained = parents["retained_route"]

    positive_checks = {
        "same_source_sector_overlap_identity_passed": sector.get("sector_overlap_identity_gate_passed") is True,
        "canonical_higgs_pole_identity_passed": (
            higgs_gate.get("higgs_pole_identity_gate_passed") is True
            and latest.get("identity_closed") is True
        ),
        "source_pole_canonical_identity_passed": (
            mixing.get("source_pole_canonical_identity_gate_passed") is True
        ),
        "no_orthogonal_top_coupling_or_measured_component_passed": (
            no_orthogonal.get("no_orthogonal_top_coupling_selection_rule_gate_passed") is True
        ),
        "source_higgs_gram_purity_passed": gram.get("source_higgs_gram_purity_gate_passed") is True,
        "neutral_scalar_rank_one_purity_passed": (
            rank_one.get("neutral_scalar_rank_one_purity_gate_passed") is True
        ),
        "same_source_wz_response_certificate_passed": (
            wz.get("same_source_wz_response_certificate_gate_passed") is True
        ),
        "retained_route_or_proposal_gate_passed": retained.get("proposal_allowed") is True,
    }
    accepted_identity_routes = {
        "direct_higgs_pole_identity": (
            positive_checks["canonical_higgs_pole_identity_passed"]
            and positive_checks["source_pole_canonical_identity_passed"]
            and positive_checks["no_orthogonal_top_coupling_or_measured_component_passed"]
        ),
        "source_higgs_gram_purity": positive_checks["source_higgs_gram_purity_passed"],
        "neutral_scalar_rank_one_purity": positive_checks["neutral_scalar_rank_one_purity_passed"],
        "same_source_wz_response": (
            positive_checks["same_source_wz_response_certificate_passed"]
            and positive_checks["same_source_sector_overlap_identity_passed"]
        ),
    }
    any_identity_route = any(accepted_identity_routes.values())
    identity_passed = (
        any_identity_route
        and positive_checks["same_source_sector_overlap_identity_passed"]
        and positive_checks["canonical_higgs_pole_identity_passed"]
        and positive_checks["retained_route_or_proposal_gate_passed"]
    )
    failed_positive_checks = [key for key, ok in positive_checks.items() if not ok]
    return {
        "identity_passed": identity_passed,
        "positive_checks": positive_checks,
        "failed_positive_checks": failed_positive_checks,
        "accepted_identity_routes": accepted_identity_routes,
        "any_identity_route": any_identity_route,
    }


def blocked_checks(parents: dict[str, dict[str, Any]]) -> dict[str, bool]:
    return {
        "sector_overlap_identity_blocked": (
            "sector-overlap identity obstruction" in status(parents["same_source_sector_overlap"])
            and parents["same_source_sector_overlap"].get("sector_overlap_identity_gate_passed") is False
            and parents["same_source_sector_overlap"].get("proposal_allowed") is False
        ),
        "higgs_identity_blocked": (
            "canonical-Higgs pole identity gate blocking" in status(parents["fh_lsz_higgs_pole_identity"])
            and parents["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
            and parents["higgs_identity_latest_blocker"].get("identity_closed") is False
        ),
        "source_pole_mixing_blocked": (
            "source-pole canonical-Higgs mixing" in status(parents["source_pole_canonical_higgs_mixing"])
            and parents["source_pole_canonical_higgs_mixing"].get(
                "source_pole_canonical_identity_gate_passed"
            )
            is False
        ),
        "no_orthogonal_top_coupling_blocked": (
            "no-orthogonal-top-coupling selection rule not derived"
            in status(parents["no_orthogonal_top_coupling_selection"])
            and parents["no_orthogonal_top_coupling_selection"].get(
                "no_orthogonal_top_coupling_selection_rule_gate_passed"
            )
            is False
        ),
        "source_higgs_gram_purity_blocked": (
            "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity"])
            and parents["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
        ),
        "neutral_rank_one_blocked": (
            "neutral scalar rank-one purity gate not passed"
            in status(parents["neutral_scalar_rank_one_purity"])
            and parents["neutral_scalar_rank_one_purity"].get(
                "neutral_scalar_rank_one_purity_gate_passed"
            )
            is False
        ),
        "wz_response_identity_route_blocked": (
            "same-source WZ response certificate gate not passed"
            in status(parents["same_source_wz_response"])
            and parents["same_source_wz_response"].get("same_source_wz_response_certificate_gate_passed")
            is False
        ),
        "retained_route_not_authorized": (
            "retained closure not yet reached" in status(parents["retained_route"])
            and parents["retained_route"].get("proposal_allowed") is False
        ),
    }


def build_identity_certificate(*, phase: str, source_coordinate: str) -> dict[str, Any]:
    return {
        "certificate_kind": "same_source_top_response_identity",
        "phase": phase,
        "same_source_coordinate": True,
        "source_coordinate": source_coordinate,
        "same_source_sector_overlap_identity_passed": True,
        "canonical_higgs_pole_identity_passed": True,
        "retained_route_or_proposal_gate_passed": True,
        "identity_route": "scout schema witness" if phase == "scout" else "strict accepted identity route",
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s=1, cos(theta)=1, or k_top/k_gauge=1 by fiat",
            "does not use H_unit, yt_ward_identity, observed top/y_t/WZ selectors, alpha_LM, plaquette, or u0",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--identity-output", type=Path, default=DEFAULT_IDENTITY_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    identity_output = (
        SCOUT_IDENTITY_OUTPUT
        if args.scout and args.identity_output == DEFAULT_IDENTITY_OUTPUT
        else args.identity_output
    )

    print("PR #230 same-source top-response identity certificate builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    statuses = parent_statuses(parents)
    evaluation = evaluate_current_identity(parents) if not missing_parents else {
        "identity_passed": False,
        "positive_checks": {},
        "failed_positive_checks": ["parent certificates absent"],
        "accepted_identity_routes": {},
        "any_identity_route": False,
    }
    blockers = blocked_checks(parents) if not missing_parents else {}

    scout_gate_passed = args.scout and not missing_parents and not proposal_allowed_parents
    strict_gate_passed = args.strict and evaluation["identity_passed"] and not proposal_allowed_parents
    current_gate_passed = (not args.scout) and (not args.strict) and evaluation["identity_passed"]
    identity_written = False
    identity_certificate: dict[str, Any] = {}
    if scout_gate_passed or strict_gate_passed or current_gate_passed:
        identity_certificate = build_identity_certificate(
            phase="scout" if args.scout else "production",
            source_coordinate="same scalar source coordinate used by top FH/LSZ and W/Z response",
        )
        identity_output.parent.mkdir(parents=True, exist_ok=True)
        identity_output.write_text(
            json.dumps(identity_certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        identity_written = True

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    if args.scout:
        report("scout-identity-schema-parent-surface-loaded", scout_gate_passed, "schema witness only")
        report("scout-identity-certificate-written", identity_written, display(identity_output))
        report("strict-identity-certificate-not-claimed", not strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")
    elif args.strict:
        report("strict-sector-overlap-identity-passed", evaluation["positive_checks"].get("same_source_sector_overlap_identity_passed") is True, statuses.get("same_source_sector_overlap", ""))
        report("strict-canonical-higgs-identity-passed", evaluation["positive_checks"].get("canonical_higgs_pole_identity_passed") is True, statuses.get("higgs_identity_latest_blocker", ""))
        report("strict-identity-route-accepted", evaluation["any_identity_route"] is True, str(evaluation["accepted_identity_routes"]))
        report("strict-retained-route-or-proposal-gate-passed", evaluation["positive_checks"].get("retained_route_or_proposal_gate_passed") is True, statuses.get("retained_route", ""))
        report("strict-identity-certificate-written", identity_written, display(identity_output))
    else:
        report("sector-overlap-identity-currently-blocked", blockers.get("sector_overlap_identity_blocked") is True, statuses.get("same_source_sector_overlap", ""))
        report("higgs-pole-identity-currently-blocked", blockers.get("higgs_identity_blocked") is True, statuses.get("higgs_identity_latest_blocker", ""))
        report("source-pole-mixing-currently-blocked", blockers.get("source_pole_mixing_blocked") is True, statuses.get("source_pole_canonical_higgs_mixing", ""))
        report("no-orthogonal-top-coupling-currently-blocked", blockers.get("no_orthogonal_top_coupling_blocked") is True, statuses.get("no_orthogonal_top_coupling_selection", ""))
        report("source-higgs-gram-purity-currently-blocked", blockers.get("source_higgs_gram_purity_blocked") is True, statuses.get("source_higgs_gram_purity", ""))
        report("neutral-rank-one-currently-blocked", blockers.get("neutral_rank_one_blocked") is True, statuses.get("neutral_scalar_rank_one_purity", ""))
        report("wz-response-identity-route-currently-blocked", blockers.get("wz_response_identity_route_blocked") is True, statuses.get("same_source_wz_response", ""))
        report("retained-route-not-authorized", blockers.get("retained_route_not_authorized") is True, statuses.get("retained_route", ""))
        report("current-mode-does-not-write-identity-certificate", not identity_written, display(DEFAULT_IDENTITY_OUTPUT))
        report("strict-identity-certificate-not-claimed", not strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / same-source top-response identity certificate schema"
            if scout_gate_passed
            else "strict-pass / same-source top-response identity certificate built"
            if strict_gate_passed
            else "support / same-source top-response identity certificate built"
            if current_gate_passed
            else "open / same-source top-response identity blockers remain"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The builder emits the production identity certificate only after a "
            "sector-overlap identity, canonical-Higgs pole identity, one accepted "
            "identity route, and retained-route authorization exist."
        ),
        "bare_retained_allowed": False,
        "same_source_top_response_identity_builder_passed": scout_gate_passed
        or strict_gate_passed
        or current_gate_passed,
        "strict_same_source_top_response_identity_builder_passed": strict_gate_passed,
        "identity_certificate_written": identity_written,
        "identity_certificate_output": display(identity_output),
        "identity_evaluation": evaluation,
        "blocker_checks": blockers,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "identity_certificate": identity_certificate,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s=1, cos(theta)=1, k_top/k_gauge=1, c2=1, or Z_match=1",
            "does not use H_unit, yt_ward_identity, observed top/y_t/WZ selectors, alpha_LM, plaquette, or u0",
            "does not treat a same-source label as a sector-overlap or canonical-Higgs identity",
        ],
        "exact_next_action": (
            "Close one accepted identity route: source-Higgs Gram purity with "
            "C_sH/C_HH pole residues, a same-source W/Z response certificate "
            "with sector-overlap identity, a neutral-scalar rank-one theorem, "
            "or a direct canonical-Higgs pole identity.  Then rerun this builder "
            f"to emit {display(DEFAULT_IDENTITY_OUTPUT)}."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if identity_written:
        print(f"Wrote identity certificate: {display(identity_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
