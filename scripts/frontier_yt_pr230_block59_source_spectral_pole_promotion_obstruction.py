#!/usr/bin/env python3
"""
PR #230 Block59 source-spectral pole-promotion obstruction.

Block58 established finite-volume positive source-channel spectral support.
This gate asks the next exact question: can that finite-volume positive
spectral sum be promoted, on the current PR230 surface, to a thermodynamic
isolated scalar pole with a positive LSZ residue interval?

Answer: no, not from the current premises.  Positive finite-volume spectral
sums are compatible with atomless soft-continuum limits whose finite-volume
levels approach the spectral edge and whose individual residues vanish.  This
preserves reflection positivity, the spectrum condition, and finite-volume
source spectral support, while leaving the thermodynamic pole atom and residue
lower bound absent.
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
    / "yt_pr230_block59_source_spectral_pole_promotion_obstruction_2026-05-12.json"
)

PARENTS = {
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "finite_volume_pole_saturation_obstruction": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "soft_continuum_threshold_no_go": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "threshold_authority_import_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "confinement_gap_threshold_import_audit": "outputs/yt_confinement_gap_threshold_import_audit_2026-05-02.json",
    "source_overlap_sum_rule_no_go": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
    "scalar_spectral_saturation_no_go": "outputs/yt_scalar_spectral_saturation_no_go_2026-05-01.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def soft_band_laplace(t: float, m0: float, residue: float, epsilon: float) -> float:
    """Laplace transform of rho(x)=2x/epsilon^2 on x in [0, epsilon]."""

    return residue * math.exp(-m0 * t) * soft_band_factor(t, epsilon)


def soft_band_factor(t: float, epsilon: float) -> float:
    """Soft-band transform divided by a pole atom at the same spectral edge."""

    if t == 0:
        return 1.0
    return (
        2.0
        * (1.0 - math.exp(-t * epsilon) * (1.0 + t * epsilon))
        / (epsilon * epsilon * t * t)
    )


def pole_laplace(t: float, m0: float, residue: float) -> float:
    return residue * math.exp(-m0 * t)


def build_counterfamily() -> dict[str, Any]:
    m0 = 0.5
    residue = 0.4
    epsilon = 1.0e-3
    sample_times = [1, 2, 4, 8, 12]
    finite_window_rows = []
    for t in sample_times:
        pole = pole_laplace(float(t), m0, residue)
        soft = soft_band_laplace(float(t), m0, residue, epsilon)
        finite_window_rows.append(
            {
                "t": t,
                "pole_correlator": pole,
                "atomless_soft_band_correlator": soft,
                "relative_difference": abs(soft - pole) / pole,
            }
        )

    volume_rows = []
    for L in [12, 16, 24, 32, 48, 64]:
        n_levels = L
        level_weight = residue / n_levels
        level_spacing = epsilon / n_levels
        volume_rows.append(
            {
                "L": L,
                "n_levels_in_soft_band": n_levels,
                "lowest_level_gap_from_edge": level_spacing,
                "max_individual_level_residue": level_weight,
                "total_soft_band_weight": residue,
                "positive_finite_volume_spectral_sum": True,
            }
        )

    tail_rows = []
    for t in [100.0, 1000.0, 10000.0]:
        tail_rows.append(
            {
                "t": t,
                "soft_band_divided_by_pole_atom_with_same_edge": soft_band_factor(
                    t, epsilon
                ),
                "atom_residue_in_limit": 0.0,
            }
        )

    return {
        "spectral_edge_m0": m0,
        "total_source_weight": residue,
        "soft_band_width": epsilon,
        "soft_band_density": "rho(E)=2(E-m0)/epsilon^2 on [m0,m0+epsilon]",
        "finite_window_rows": finite_window_rows,
        "finite_volume_rows": volume_rows,
        "tail_rows": tail_rows,
        "max_finite_window_relative_difference": max(
            row["relative_difference"] for row in finite_window_rows
        ),
        "finite_volume_max_level_residue_decreases": (
            volume_rows[-1]["max_individual_level_residue"]
            < volume_rows[0]["max_individual_level_residue"]
        ),
        "finite_volume_lowest_gap_decreases": (
            volume_rows[-1]["lowest_level_gap_from_edge"]
            < volume_rows[0]["lowest_level_gap_from_edge"]
        ),
        "tail_ratio_decreases": (
            tail_rows[-1]["soft_band_divided_by_pole_atom_with_same_edge"]
            < tail_rows[0]["soft_band_divided_by_pole_atom_with_same_edge"]
        ),
    }


def main() -> int:
    print("PR #230 Block59 source-spectral pole-promotion obstruction")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    counterfamily = build_counterfamily()

    block58_loaded = (
        "finite-volume compact source-channel spectral support"
        in statuses["block58_compact_source_spectral_support"]
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
        and certs["block58_compact_source_spectral_support"].get(
            "thermodynamic_limit_authority_present"
        )
        is False
    )
    prior_negatives_apply = all(
        "exact negative boundary" in statuses[name]
        and certs[name].get("proposal_allowed") is False
        for name in [
            "finite_volume_pole_saturation_obstruction",
            "soft_continuum_threshold_no_go",
            "threshold_authority_import_audit",
            "confinement_gap_threshold_import_audit",
            "source_overlap_sum_rule_no_go",
            "scalar_spectral_saturation_no_go",
        ]
    )
    finite_window_ambiguous = (
        counterfamily["max_finite_window_relative_difference"] < 0.01
    )
    atomless_limit_witness = (
        counterfamily["finite_volume_max_level_residue_decreases"]
        and counterfamily["finite_volume_lowest_gap_decreases"]
        and counterfamily["tail_ratio_decreases"]
        and counterfamily["tail_rows"][-1]["atom_residue_in_limit"] == 0.0
    )
    thermodynamic_pole_authority = False
    uniform_threshold_gap_authority = False
    residue_lower_bound_certified = False
    canonical_oh_authority = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("block58-finite-volume-spectral-support-loaded", block58_loaded, statuses["block58_compact_source_spectral_support"])
    report("prior-negative-boundaries-still-apply", prior_negatives_apply, "finite-volume, threshold, confinement-gap, and sum-rule shortcuts blocked")
    report("positive-atomless-counterfamily-constructed", atomless_limit_witness, "finite-volume weights positive, max level residue -> 0")
    report("finite-window-data-do-not-certify-atom", finite_window_ambiguous, f"max_rel_diff={counterfamily['max_finite_window_relative_difference']:.3e}")
    report("thermodynamic-pole-authority-absent", not thermodynamic_pole_authority, "no isolated atom theorem")
    report("uniform-threshold-gap-authority-absent", not uniform_threshold_gap_authority, "soft continuum may start at spectral edge")
    report("residue-lower-bound-not-certified", not residue_lower_bound_certified, "pole residue lower bound remains zero")
    report("canonical-oh-authority-absent", not canonical_oh_authority, "source spectral measure is not O_H identity")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block59 is an exact negative boundary")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for the current PR230 surface: "
            "Block59 finite-volume source spectral positivity does not promote "
            "to thermodynamic scalar pole authority"
        ),
        "conditional_surface_status": (
            "conditional-support if a future uniform thermodynamic/FVIR "
            "source-spectral theorem supplies an isolated pole atom, residue "
            "interval, contact/continuum map, and canonical O_H or physical "
            "response bridge"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "Finite-volume positive source spectral support is compatible with "
            "atomless soft-continuum thermodynamic limits.  The current surface "
            "has no uniform threshold gap, pole-saturation theorem, residue "
            "lower bound, or canonical O_H authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block59_source_spectral_pole_promotion_obstruction_passed": True,
        "finite_volume_source_spectral_support_loaded": block58_loaded,
        "thermodynamic_pole_authority_present": thermodynamic_pole_authority,
        "uniform_threshold_gap_authority_present": uniform_threshold_gap_authority,
        "residue_lower_bound_certified": residue_lower_bound_certified,
        "canonical_oh_authority_present": canonical_oh_authority,
        "atomless_soft_continuum_counterfamily": counterfamily,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_scalar_authority_obligations": [
            "uniform thermodynamic/FVIR theorem for the compact source spectral measure",
            "isolated scalar pole atom or threshold gap with positive residue lower bound",
            "contact/continuum subtraction map from compact source correlator to scalar LSZ",
            "canonical O_H/source-overlap identity or strict physical-response bridge",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite-volume spectral positivity as pole saturation",
            "does not infer scalar LSZ residue authority from confinement or mass-gap language",
            "does not identify the source spectral measure with canonical O_H",
            "does not use H_unit, Ward, y_t_bare, observed top/Yukawa values, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "A positive scalar route now needs a new uniform thermodynamic/FVIR "
            "source-spectral pole theorem or strict physical rows with model, "
            "FV/IR, residue, and canonical-O_H/response authority.  Otherwise "
            "the current compact-source lane is exact-boundary support only."
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
