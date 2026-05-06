#!/usr/bin/env python3
"""
PR #230 source-sector pattern transfer gate.

This runner answers a narrow question:

    Does the SU(3) plaquette source-sector / exponent-shift / holonomic
    approach transfer to the PR #230 top-Yukawa bridge?

The answer is deliberately split.  The method transfers as a way to compute
same-surface source rows after the physical source operators are defined.  It
does not transfer as a direct y_t derivation from source-only data, because
PR #230 still lacks a current-surface canonical Higgs coordinate or an
equivalent rank-one neutral-scalar theorem.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json"

PARENTS = {
    "holonomic_source_response": (
        "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
    ),
    "source_functional_lsz": (
        "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
    ),
    "clean_math_tool_selector": (
        "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json"
    ),
    "derived_rank_one_attempt": (
        "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json"
    ),
    "fresh_artifact_review": (
        "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json"
    ),
    "retained_route": (
        "outputs/yt_retained_closure_route_certificate_2026-05-01.json"
    ),
}

TEXTS = {
    "holonomic_source_response": (
        "docs/YT_PR230_HOLONOMIC_SOURCE_RESPONSE_FEASIBILITY_GATE_NOTE_2026-05-05.md"
    ),
    "source_functional_lsz": (
        "docs/YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md"
    ),
    "clean_math_tool_selector": (
        "docs/YT_PR230_CLEAN_SOURCE_HIGGS_MATH_TOOL_ROUTE_SELECTOR_NOTE_2026-05-05.md"
    ),
    "derived_rank_one_attempt": (
        "docs/YT_PR230_DERIVED_BRIDGE_RANK_ONE_CLOSURE_ATTEMPT_NOTE_2026-05-05.md"
    ),
}

FUTURE_ARTIFACTS = {
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "same_source_wz_rows": (
        "outputs/yt_top_wz_matched_response_rows_2026-05-04.json"
    ),
    "neutral_rank_one_certificate": (
        "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-05.json"
    ),
    "neutral_primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def transfer_map() -> list[dict[str, Any]]:
    return [
        {
            "su3_pattern": "finite compact source functional first, observable as log-Z derivative",
            "pr230_translation": "build Z(beta, s, h) and compute C_ss, C_sH, C_HH as derivatives",
            "current_status": "relevant but blocked until h/O_H is a same-surface object",
        },
        {
            "su3_pattern": "source-sector exponent/resummation correction changes rho_R",
            "pr230_translation": "possible source-coordinate normalization kappa_s or scalar pole residue",
            "current_status": "cannot be inferred from source-only C_ss because source rescalings leave the physical overlap undetermined",
        },
        {
            "su3_pattern": "Schwinger-Dyson/character equations constrain a closed gauge source sector",
            "pr230_translation": "neutral scalar SD equations could prove primitive/rank-one pole dominance",
            "current_status": "positive route only if a neutral off-diagonal generator or primitive cone is derived",
        },
        {
            "su3_pattern": "outside math tools certify rows after the integrand is fixed",
            "pr230_translation": "holonomic/D-module/tensor tools can compute source-Higgs rows after O_H is defined",
            "current_status": "math tool names are not proof authority by themselves",
        },
    ]


def source_only_counterfamily() -> list[dict[str, float | bool | str]]:
    rows: list[dict[str, float | bool | str]] = []
    for rho in (1.0, 0.8, 0.35, 0.0, -0.35):
        rows.append(
            {
                "source_only_log_Z": "0.5*s^2",
                "C_ss": 1.0,
                "C_sH": rho,
                "C_HH": 1.0,
                "gram_det": 1.0 - rho * rho,
                "source_higgs_purity": abs(1.0 - rho * rho) < 1e-15,
            }
        )
    return rows


def firewall() -> dict[str, bool]:
    return {
        "uses_plaquette_value_as_yukawa_input": False,
        "uses_su3_exponent_shift_as_yukawa_value": False,
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_or_yukawa_targets": False,
        "sets_kappa_s_equal_one": False,
        "identifies_source_only_Os_with_canonical_OH": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 source-sector pattern transfer gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    texts = {name: read_rel(path) for name, path in TEXTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}
    counterfamily = source_only_counterfamily()
    clean_firewall = all(value is False for value in firewall().values())

    holonomic_relevance_recorded = (
        "PR541-style holonomic source-response route is relevant"
        in parent_statuses["holonomic_source_response"]
        or "PR541-style holonomic source-response route is relevant"
        in texts["holonomic_source_response"]
    )
    source_only_boundary_recorded = (
        "source-only pole data do not determine the overlap"
        in texts["source_functional_lsz"]
    )
    clean_route_selector_points_to_oh_rows = (
        "O_H/C_sH/C_HH" in texts["clean_math_tool_selector"]
        and "same-surface" in texts["clean_math_tool_selector"]
    )
    derived_rank_one_not_closed = (
        "derived rank-one bridge not closed" in parent_statuses["derived_rank_one_attempt"]
        and parents["derived_rank_one_attempt"].get("proposal_allowed") is False
    )
    retained_route_still_open = (
        parents["retained_route"].get("proposal_allowed") is False
    )
    no_future_physical_bridge_artifact = not any(future_presence.values())
    counterfamily_blocks_source_only = (
        len({row["C_sH"] for row in counterfamily}) > 1
        and len({row["source_only_log_Z"] for row in counterfamily}) == 1
        and any(row["source_higgs_purity"] for row in counterfamily)
        and any(not row["source_higgs_purity"] for row in counterfamily)
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("holonomic-relevance-recorded", holonomic_relevance_recorded, parent_statuses["holonomic_source_response"])
    report("source-only-boundary-recorded", source_only_boundary_recorded, parent_statuses["source_functional_lsz"])
    report("clean-route-selector-points-to-oh-rows", clean_route_selector_points_to_oh_rows, "O_H/C_sH/C_HH route selected")
    report("derived-rank-one-not-closed", derived_rank_one_not_closed, parent_statuses["derived_rank_one_attempt"])
    report("retained-route-still-open", retained_route_still_open, parent_statuses["retained_route"])
    report("no-future-physical-bridge-artifact-present", no_future_physical_bridge_artifact, str(future_presence))
    report("source-only-counterfamily-blocks-transfer", counterfamily_blocks_source_only, "same Z(s,0), different overlap")
    report("forbidden-firewall-clean", clean_firewall, str(firewall()))

    approach_relevant = (
        holonomic_relevance_recorded
        and source_only_boundary_recorded
        and clean_route_selector_points_to_oh_rows
        and counterfamily_blocks_source_only
        and clean_firewall
    )
    direct_closure_available = (
        not no_future_physical_bridge_artifact
        and not derived_rank_one_not_closed
        and not retained_route_still_open
        and clean_firewall
    )
    bounded_support_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and approach_relevant
        and not direct_closure_available
        and derived_rank_one_not_closed
        and retained_route_still_open
        and no_future_physical_bridge_artifact
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / SU3 source-sector pattern is relevant to PR230 "
            "as a bridge-computation method, not as source-only y_t closure"
        ),
        "conditional_surface_status": (
            "If a same-surface O_H/h source, C_sH/C_HH rows, W/Z response rows, "
            "or a neutral primitive/rank-one theorem is supplied, the source-sector "
            "holonomic/SD/tensor pattern becomes a viable exact-computation route."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The transfer exposes the right positive contract but does not supply "
            "the physical Higgs coordinate, source-Higgs overlap, or neutral "
            "rank-one theorem needed for y_t."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "approach_relevant": approach_relevant,
        "direct_closure_available": direct_closure_available,
        "bounded_support_passed": bounded_support_passed,
        "transfer_map": transfer_map(),
        "source_only_counterfamily": counterfamily,
        "future_artifact_presence": future_presence,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": firewall(),
        "strict_non_claims": [
            "does not work the SU3 plaquette SD problem",
            "does not import the plaquette value or exponent shift into y_t",
            "does not define y_t_bare or use H_unit matrix-element readout",
            "does not identify source-only O_s with canonical O_H",
            "does not set kappa_s = 1",
            "does not claim retained or proposed_retained closure",
        ],
        "exact_next_action": (
            "Use the transferred method only after creating a current-surface "
            "bridge object: canonical O_H/h plus C_sH/C_HH rows, same-source "
            "W/Z response rows, or a neutral primitive-cone/rank-one theorem. "
            "Do not spend effort deriving SU3 plaquette constants for PR230."
        ),
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
