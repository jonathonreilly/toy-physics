#!/usr/bin/env python3
"""
PR #230 neutral primitive H3/H4 aperture checkpoint.

After block09 the source-Higgs bridge remains open.  This checkpoint pivots to
the next ranked primitive/rank-one route and asks whether the current
same-surface Z3 support plus the completed two-source taste-radial rows can
now supply the missing H3/H4 physical-transfer premises.

The result is bounded support plus an exact boundary.  H1/H2 algebraic support
is real, and the completed C_sx/C_xx chunk prefix is useful staging evidence,
but the current surface still lacks a physical neutral transfer/off-diagonal
generator and a coupling to the PR230 source/canonical-Higgs sector.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
)

PARENTS = {
    "neutral_primitive_route_completion": (
        "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
    ),
    "z3_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "z3_h2_positive_cone_support": (
        "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
    ),
    "same_surface_neutral_multiplicity_candidate": (
        "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json"
    ),
    "two_source_primitive_transfer_candidate": (
        "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json"
    ),
    "two_source_row_combiner": (
        "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
    ),
    "source_higgs_bridge_aperture": (
        "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json"
    ),
    "wz_accepted_action_root": (
        "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json"
    ),
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "neutral_primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
    "neutral_offdiagonal_generator_certificate": (
        "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json"
    ),
    "neutral_scalar_rank_one_purity_certificate": (
        "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-03.json"
    ),
    "neutral_scalar_irreducibility_certificate": (
        "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json"
    ),
    "canonical_higgs_operator_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_measurement_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "source_higgs_production_certificate": (
        "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
    ),
    "accepted_same_source_ew_action": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "wz_correlator_mass_fit_rows": (
        "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json"
    ),
    "wz_response_ratio_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "top_wz_matched_covariance_certificate": (
        "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json"
    ),
    "strict_electroweak_g2_certificate": (
        "outputs/yt_electroweak_g2_certificate_2026-05-04.json"
    ),
}

FORBIDDEN_FIREWALL = {
    "used_positivity_without_irreducibility": False,
    "used_commutant_rank_as_rank_one_purity": False,
    "used_source_only_or_c_sx_rows_as_neutral_transfer": False,
    "aliased_c_sx_to_c_sh_before_canonical_oh": False,
    "identified_taste_radial_x_as_canonical_oh": False,
    "used_hunit_matrix_element_or_hunit_operator": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_y_t_or_top_mass": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "assumed_k_top_equals_k_gauge": False,
    "touched_live_chunk_worker": False,
    "claimed_retained_or_proposed_retained": False,
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def row_diagnostics(combiner: dict[str, Any]) -> dict[str, Any]:
    diagnostics = combiner.get("partial_mode_diagnostics", {})
    if not isinstance(diagnostics, dict):
        diagnostics = {}
    determinants: list[float] = []
    abs_rhos: list[float] = []
    counts: set[int] = set()
    for row in diagnostics.values():
        if not isinstance(row, dict):
            continue
        det = row.get("finite_row_gram_determinant_real", {})
        rho = row.get("rho_sx_real", {})
        if isinstance(det, dict) and isinstance(det.get("mean"), (int, float)):
            determinants.append(float(det["mean"]))
        if isinstance(rho, dict) and isinstance(rho.get("mean"), (int, float)):
            abs_rhos.append(abs(float(rho["mean"])))
        if isinstance(det, dict) and isinstance(det.get("count"), int):
            counts.add(int(det["count"]))
    return {
        "mode_count": len(diagnostics),
        "determinant_min": min(determinants) if determinants else None,
        "determinant_max": max(determinants) if determinants else None,
        "max_abs_rho_sx": max(abs_rhos) if abs_rhos else None,
        "chunk_counts_seen": sorted(counts),
        "finite_rows_rank_one_flat": bool(determinants)
        and all(abs(value) <= 1.0e-12 for value in determinants),
    }


def h3_h4_aperture_table(
    certs: dict[str, dict[str, Any]], futures: dict[str, bool]
) -> list[dict[str, Any]]:
    combiner = certs["two_source_row_combiner"]
    diagnostics = row_diagnostics(combiner)
    return [
        {
            "gate": "H1 same-surface Z3 taste-triplet action",
            "current_status": "support loaded",
            "evidence": PARENTS["z3_conditional_primitive"],
            "blocks_closure": False,
        },
        {
            "gate": "H2 positive-cone equal-magnitude support",
            "current_status": "support loaded",
            "evidence": PARENTS["z3_h2_positive_cone_support"],
            "blocks_closure": False,
        },
        {
            "gate": "H3 physical neutral transfer/off-diagonal generator",
            "current_status": "absent",
            "evidence": FUTURE_ARTIFACTS["neutral_offdiagonal_generator_certificate"],
            "blocks_closure": not futures["neutral_offdiagonal_generator_certificate"],
        },
        {
            "gate": "H3 primitive-cone/irreducibility certificate",
            "current_status": "absent",
            "evidence": FUTURE_ARTIFACTS["neutral_primitive_cone_certificate"],
            "blocks_closure": not futures["neutral_primitive_cone_certificate"],
        },
        {
            "gate": "H4 coupling to PR230 source/canonical-Higgs sector",
            "current_status": "absent",
            "evidence": FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"],
            "blocks_closure": not futures["canonical_higgs_operator_certificate"],
        },
        {
            "gate": "finite C_sx/C_xx row staging",
            "current_status": (
                f"bounded support: {combiner.get('ready_chunks')}/"
                f"{combiner.get('expected_chunks')} chunks, "
                f"min finite Gram determinant={diagnostics['determinant_min']}"
            ),
            "evidence": PARENTS["two_source_row_combiner"],
            "blocks_closure": True,
        },
        {
            "gate": "source-Higgs disjunct",
            "current_status": status(certs["source_higgs_bridge_aperture"]),
            "evidence": PARENTS["source_higgs_bridge_aperture"],
            "blocks_closure": certs["source_higgs_bridge_aperture"].get(
                "current_surface_closure_satisfied"
            )
            is not True,
        },
        {
            "gate": "W/Z physical-response disjunct",
            "current_status": status(certs["wz_accepted_action_root"]),
            "evidence": PARENTS["wz_accepted_action_root"],
            "blocks_closure": certs["wz_accepted_action_root"].get(
                "current_route_blocked"
            )
            is True,
        },
    ]


def main() -> int:
    print("PR #230 neutral primitive H3/H4 aperture checkpoint")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()
    combiner = certs["two_source_row_combiner"]
    diagnostics = row_diagnostics(combiner)
    aperture = h3_h4_aperture_table(certs, futures)
    open_gates = [row["gate"] for row in aperture if row["blocks_closure"]]

    neutral_completion = certs["neutral_primitive_route_completion"]
    conditional_z3 = certs["z3_conditional_primitive"]
    z3_h2 = certs["z3_h2_positive_cone_support"]
    multiplicity = certs["same_surface_neutral_multiplicity_candidate"]
    two_source_gate = certs["two_source_primitive_transfer_candidate"]
    source_higgs = certs["source_higgs_bridge_aperture"]
    wz_root = certs["wz_accepted_action_root"]
    campaign = certs["campaign_status"]

    h1_h2_loaded = (
        neutral_completion.get("conditional_z3_remaining_unsupplied_premises") == ["H3", "H4"]
        and conditional_z3.get("h2_positive_cone_support_supplied") is True
        and z3_h2.get("z3_triplet_positive_cone_h2_support_passed") is True
        and neutral_completion.get("proposal_allowed") is False
        and conditional_z3.get("proposal_allowed") is False
        and z3_h2.get("proposal_allowed") is False
    )
    expected_chunks = combiner.get("expected_chunks")
    ready_chunks = combiner.get("ready_chunks")
    present_chunks = combiner.get("present_chunks")
    missing_chunk_indices = combiner.get("missing_chunk_indices", [])
    first_missing = missing_chunk_indices[0] if missing_chunk_indices else None
    ready_prefix_is_current = (
        isinstance(expected_chunks, int)
        and isinstance(ready_chunks, int)
        and isinstance(present_chunks, int)
        and ready_chunks == present_chunks
        and ready_chunks >= 44
        and (first_missing == ready_chunks + 1 or ready_chunks == expected_chunks)
    )
    two_source_combiner_boundary = (
        isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and (
            (
                combiner.get("combined_rows_written") is False
                and ready_chunks < expected_chunks
            )
            or (
                combiner.get("combined_rows_written") is True
                and ready_chunks == expected_chunks == 63
            )
        )
    )
    two_source_rows_current_prefix = (
        expected_chunks == 63
        and ready_prefix_is_current
        and two_source_combiner_boundary
    )
    finite_rows_not_rank_one_transfer = (
        diagnostics["mode_count"] >= 4
        and diagnostics["chunk_counts_seen"] == [ready_chunks]
        and isinstance(diagnostics["determinant_min"], float)
        and diagnostics["determinant_min"] > 0.0
        and diagnostics["finite_rows_rank_one_flat"] is False
        and two_source_gate.get("proposal_allowed") is False
        and "finite C_sx rows do not certify a physical primitive neutral transfer"
        in status(two_source_gate)
    )
    h3_h4_absent = (
        neutral_completion.get("h3_physical_transfer_or_offdiagonal_generator_absent")
        is True
        and neutral_completion.get("h4_source_canonical_higgs_coupling_absent")
        is True
        and multiplicity.get("candidate_accepted") is False
        and not futures["neutral_offdiagonal_generator_certificate"]
        and not futures["neutral_primitive_cone_certificate"]
        and not futures["canonical_higgs_operator_certificate"]
    )
    route_disjuncts_still_open = (
        source_higgs.get("current_surface_closure_satisfied") is False
        and source_higgs.get("proposal_allowed") is False
        and wz_root.get("current_route_blocked") is True
        and wz_root.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    future_files_absent = not any(futures.values())
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("h1-h2-support-loaded", h1_h2_loaded, "conditional Z3 H1/H2 support loaded; H3/H4 remain listed")
    report("two-source-rows-current-prefix", two_source_rows_current_prefix, f"{combiner.get('ready_chunks')}/63 ready")
    report("finite-csx-rows-not-rank-one-transfer", finite_rows_not_rank_one_transfer, str(diagnostics))
    report("h3-h4-physical-premises-absent", h3_h4_absent, str(neutral_completion.get("conditional_z3_remaining_unsupplied_premises")))
    report("source-higgs-and-wz-disjuncts-open", route_disjuncts_still_open, "source-Higgs and W/Z parent routes still open")
    report("future-artifacts-absent", future_files_absent, str(futures))
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    passed = (
        not missing
        and not proposal_parents
        and h1_h2_loaded
        and two_source_rows_current_prefix
        and finite_rows_not_rank_one_transfer
        and h3_h4_absent
        and route_disjuncts_still_open
        and future_files_absent
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / neutral primitive H3/H4 aperture checkpoint; "
            f"H1/H2 support and {ready_chunks} C_sx/C_xx chunks do not supply physical "
            "neutral transfer or source-canonical-Higgs coupling"
        ),
        "claim_type": "open_gate",
        "conditional_surface_status": (
            "exact support if a future same-surface primitive neutral transfer "
            "or off-diagonal generator certificate supplies H3 and a canonical "
            "O_H/source-Higgs or W/Z physical-response packet supplies H4 without "
            "forbidden imports"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The block only loads H1/H2 algebraic support and current finite "
            "C_sx/C_xx staging rows.  H3 physical transfer/off-diagonal dynamics, "
            "H4 source/canonical-Higgs coupling, production C_sH/C_HH rows, and "
            "W/Z accepted-response rows are absent."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "neutral_primitive_h3h4_aperture_checkpoint_passed": passed,
        "current_surface_closure_satisfied": False,
        "h1_h2_support_loaded": h1_h2_loaded,
        "h3_physical_transfer_or_offdiagonal_generator_absent": h3_h4_absent,
        "h4_source_canonical_higgs_coupling_absent": h3_h4_absent,
        "two_source_rows": {
            "expected_chunks": combiner.get("expected_chunks"),
            "ready_chunks": combiner.get("ready_chunks"),
            "present_chunks": combiner.get("present_chunks"),
            "combined_rows_written": combiner.get("combined_rows_written"),
            "strict_limit": (
                "These are finite C_sx/C_xx covariance rows on a "
                "two-source taste-radial packet. They are not physical transfer "
                "matrices, primitive-cone certificates, canonical O_H, or "
                "C_sH/C_HH pole rows."
            ),
            "diagnostics": diagnostics,
        },
        "open_aperture_gates": open_gates,
        "h3_h4_aperture_table": aperture,
        "future_artifact_presence": futures,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not promote H1/H2 algebraic Z3 support into a physical transfer",
            "does not treat finite C_sx/C_xx covariance rows as H3 physical transfer",
            "does not relabel C_sx/C_xx as C_sH/C_HH before canonical O_H",
            "does not identify taste-radial x as canonical O_H",
            "does not set kappa_s, c2, Z_match, g2, or overlaps to one",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, or u0",
            "does not touch or relaunch the live chunk worker",
        ],
        "exact_next_action": (
            "Pivot to a real missing artifact: W/Z physical-response rows with "
            "accepted action, sector-overlap, matched covariance, and strict "
            "non-observed g2; or a fresh same-surface canonical O_H plus "
            "production C_ss/C_sH/C_HH Gram-flat row packet.  Do not reopen the "
            "neutral primitive route without a same-surface H3/H4 certificate."
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
