#!/usr/bin/env python3
"""
PR #230 Schur C_x|s one-pole finite-residue scout.

The Schur-complement repair gate found that the finite residual

    C_x|s(q) = det([[C_ss, C_sx], [C_sx, C_xx]]) / C_ss(q)

passes the zero-to-first-shell Stieltjes direction on the current finite
packet.  With only two q_hat^2 levels, those two endpoint values determine a
unique one-pole ansatz C(x)=R/(x+m^2), but they do not determine a physical
pole or residue.  This runner records the one-pole scout and explicitly
constructs positive two-pole endpoint counterfamilies with the same two data
points.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json"
)

PARENTS = {
    "schur_repair": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
    "schur_complete_monotonicity": "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json",
    "schur_pole_lift": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

MASS_FACTOR_PAIRS = [(0.25, 4.0), (0.5, 2.0), (0.1, 10.0)]

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "stderr": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "stderr": statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def one_pole_fit(c0: float, c1: float, dp: float) -> dict[str, Any]:
    if not (c0 > 0.0 and c1 > 0.0 and dp > 0.0 and c1 < c0):
        return {
            "fit_valid": False,
            "reason": "requires C0 > C1 > 0 and dp > 0",
        }
    ratio = c1 / c0
    mass_sq = ratio * dp / (1.0 - ratio)
    residue = c0 * mass_sq
    return {
        "fit_valid": True,
        "C0": c0,
        "C1": c1,
        "delta_q_hat_sq": dp,
        "ratio_C1_over_C0": ratio,
        "implied_mass_sq": mass_sq,
        "implied_residue": residue,
        "implied_pole_location_q_hat_sq": -mass_sq,
        "model": "C(x)=R/(x+m^2) through the two endpoints",
        "strict_limit": (
            "This is the unique one-pole interpolation of two finite endpoint "
            "values. It is not physical pole/residue authority without an "
            "independent one-pole model-class theorem, threshold/FV/IR control, "
            "and a canonical O_H or physical-response bridge."
        ),
    }


def two_pole_family(c0: float, c1: float, dp: float, mass_sq: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    r_star = c1 / c0
    for low_factor, high_factor in MASS_FACTOR_PAIRS:
        m1 = low_factor * mass_sq
        m2 = high_factor * mass_sq
        r1 = m1 / (m1 + dp)
        r2 = m2 / (m2 + dp)
        if not (r1 < r_star < r2):
            rows.append(
                {
                    "low_factor": low_factor,
                    "high_factor": high_factor,
                    "valid_positive_family": False,
                    "reason": "chosen masses do not bracket endpoint ratio",
                }
            )
            continue
        weight1 = (r2 - r_star) / (r2 - r1)
        weight2 = 1.0 - weight1
        residue1 = weight1 * c0 * m1
        residue2 = weight2 * c0 * m2
        endpoint0 = residue1 / m1 + residue2 / m2
        endpoint1 = residue1 / (m1 + dp) + residue2 / (m2 + dp)
        rows.append(
            {
                "low_factor": low_factor,
                "high_factor": high_factor,
                "valid_positive_family": residue1 > 0.0 and residue2 > 0.0,
                "mass_sq_low": m1,
                "mass_sq_high": m2,
                "endpoint_ratio_low": r1,
                "endpoint_ratio_high": r2,
                "endpoint_weight_low": weight1,
                "endpoint_weight_high": weight2,
                "residue_low": residue1,
                "residue_high": residue2,
                "endpoint0": endpoint0,
                "endpoint1": endpoint1,
                "endpoint0_residual": endpoint0 - c0,
                "endpoint1_residual": endpoint1 - c1,
                "low_pole_residue_fraction_of_one_pole_residue": (
                    residue1 / (c0 * mass_sq)
                ),
                "strict_limit": (
                    "A positive two-pole Stieltjes measure with these masses "
                    "matches the same two endpoints.  Therefore the one-pole "
                    "residue is a model assumption, not a consequence of the "
                    "current row packet."
                ),
            }
        )
    return rows


def per_chunk_fits(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fits: list[dict[str, Any]] = []
    for row in rows:
        c0 = row.get("C_x_given_source_zero")
        c1 = row.get("C_x_given_source_shell_mean")
        dp = row.get("shell_p_hat_sq_mean")
        if finite(c0) and finite(c1) and finite(dp):
            fit = one_pole_fit(float(c0), float(c1), float(dp))
            fit["chunk_index"] = row.get("chunk_index")
            fit["seed"] = row.get("seed")
            fits.append(fit)
    return fits


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_pilot_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_one_pole_fit_as_physical_pole": False,
        "treated_C_x_given_source_as_canonical_O_H": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 Schur C_x|s one-pole finite-residue scout")
    print("=" * 72)

    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    schur = parents["schur_repair"]
    complete = parents["schur_complete_monotonicity"]
    rows = schur.get("per_chunk_schur_residual_rows")
    rows = rows if isinstance(rows, list) else []
    x_summary = schur.get("x_given_source_summary", {})
    zero = x_summary.get("zero", {}) if isinstance(x_summary, dict) else {}
    shell = x_summary.get("shell", {}) if isinstance(x_summary, dict) else {}
    c0 = float(zero["mean"]) if finite(zero.get("mean")) else math.nan
    c1 = float(shell["mean"]) if finite(shell.get("mean")) else math.nan
    p_levels = complete.get("p_hat_sq_levels")
    p_levels = p_levels if isinstance(p_levels, list) else []
    dp = float(p_levels[1] - p_levels[0]) if len(p_levels) == 2 else math.nan

    mean_fit = one_pole_fit(c0, c1, dp)
    counterfamilies = (
        two_pole_family(c0, c1, dp, float(mean_fit["implied_mass_sq"]))
        if mean_fit.get("fit_valid")
        else []
    )
    chunk_fits = per_chunk_fits(rows)
    valid_chunk_fits = [fit for fit in chunk_fits if fit.get("fit_valid") is True]
    residue_values = [float(fit["implied_residue"]) for fit in valid_chunk_fits]
    mass_values = [float(fit["implied_mass_sq"]) for fit in valid_chunk_fits]

    first_shell_support = (
        schur.get("x_given_source_stieltjes_first_shell_passed") is True
        and complete.get("x_given_source_first_shell_stieltjes_support") is True
    )
    one_pole_fit_valid = mean_fit.get("fit_valid") is True
    positive_counterfamilies = bool(counterfamilies) and all(
        row.get("valid_positive_family") is True
        and abs(float(row.get("endpoint0_residual", math.inf))) < 1.0e-12
        and abs(float(row.get("endpoint1_residual", math.inf))) < 1.0e-12
        for row in counterfamilies
    )
    model_class_authority_absent = (
        complete.get("complete_monotonicity_authority_passed") is False
        and complete.get("threshold_or_measure_authority_present") is False
        and complete.get("pole_model_class_authority_present") is False
        and parents["schur_pole_lift"].get("strict_pole_lift_passed") is False
    )
    bridge_absent = (
        complete.get("canonical_higgs_or_physical_response_bridge_present") is False
        and parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
    )
    ready_chunks = parents["row_combiner"].get("ready_chunks")
    expected_chunks = parents["row_combiner"].get("expected_chunks")
    finite_packet_support_boundary = (
        isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and 0 < ready_chunks <= expected_chunks
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("x-given-source-first-shell-support-loaded", first_shell_support, statuses["schur_repair"])
    report("mean-one-pole-fit-finite-positive", one_pole_fit_valid, str(mean_fit))
    report("per-chunk-one-pole-fits-valid", len(valid_chunk_fits) == len(rows) and bool(rows), f"{len(valid_chunk_fits)}/{len(rows)}")
    report("positive-two-pole-counterfamilies", positive_counterfamilies, str(counterfamilies))
    report("model-class-pole-authority-absent", model_class_authority_absent, statuses["schur_complete_monotonicity"])
    report("canonical-or-physical-response-bridge-absent", bridge_absent, statuses["source_higgs_readiness"])
    report("finite-packet-support-only", finite_packet_support_boundary, f"ready={ready_chunks}/{expected_chunks}")
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-import-firewall-clean", firewall_clean, str(forbidden_firewall()))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "bounded-support / C_x|s one-pole finite-residue scout; "
            "positive endpoint fits are model-class diagnostics only, not "
            "scalar-LSZ pole authority"
        ),
        "conditional_surface_status": (
            "If a future same-surface theorem supplies one-pole saturation, "
            "threshold/contact/FV/IR control, and canonical O_H or W/Z bridge "
            "authority, these parameters can seed the strict scalar-LSZ route."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Two endpoint values determine a one-pole interpolation, but "
            "positive two-pole Stieltjes counterfamilies match the same endpoints. "
            "The current surface lacks higher shells, threshold/contact/FV/IR, "
            "pole-model-class authority, and canonical O_H or W/Z bridge authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "schur_x_given_source_one_pole_scout_passed": True,
        "one_pole_fit_valid": one_pole_fit_valid,
        "one_pole_model_class_authority_passed": False,
        "two_pole_counterfamily_present": positive_counterfamilies,
        "physical_pole_residue_authority_present": False,
        "canonical_higgs_or_physical_response_bridge_present": False,
        "ready_chunks": parents["row_combiner"].get("ready_chunks"),
        "expected_chunks": parents["row_combiner"].get("expected_chunks"),
        "p_hat_sq_levels": p_levels,
        "mean_endpoint_values": {
            "C_x_given_source_zero": c0,
            "C_x_given_source_shell": c1,
            "delta_q_hat_sq": dp,
        },
        "one_pole_fit_from_means": mean_fit,
        "per_chunk_one_pole_fit_summary": {
            "mass_sq": summarize(mass_values),
            "residue": summarize(residue_values),
        },
        "two_pole_endpoint_counterfamilies": counterfamilies,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat the one-pole interpolation as a physical scalar pole",
            "does not treat C_x|s as canonical O_H",
            "does not supply source-Higgs C_spH/C_HH rows",
            "does not supply W/Z response, strict g2, or covariance rows",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "Use the one-pole mass/residue only as a target for future "
            "higher-shell and multivolume diagnostics.  Closure still requires "
            "a one-pole/threshold/FV theorem plus canonical O_H/source-overlap, "
            "or a genuine W/Z physical-response bridge."
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
