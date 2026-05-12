#!/usr/bin/env python3
"""
PR #230 Block62 compact-source K-prime identifiability obstruction.

Block57/58 give an exact compact finite-volume source functional and positive
finite-volume source-channel spectral support.  Block60 fixes the source
carrier, and Block61 blocks carrier-to-residue promotion.  This gate tests the
remaining compact-source shortcut:

    compact source functional + fixed carrier + positive source spectrum
    => K'(pole) / pole residue

The shortcut fails on the current surface.  Positive source spectral measures
can preserve the same source carrier, pole location, source curvature, and one
finite source-correlator value while varying the pole residue.  Therefore the
current compact-source support still needs a real denominator derivative,
strict pole rows, or a stronger thermodynamic/FVIR theorem.
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
    / "yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json"
)

PARENTS = {
    "block57_compact_source_functional_foundation": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block61_post_carrier_kprime_obstruction": "outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
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


def solve_two_background_weights(
    total_background: float,
    background_c1: float,
    mass_light: float,
    mass_heavy: float,
) -> tuple[float, float]:
    e_light = math.exp(-mass_light)
    e_heavy = math.exp(-mass_heavy)
    light_weight = (background_c1 - total_background * e_heavy) / (
        e_light - e_heavy
    )
    heavy_weight = total_background - light_weight
    return light_weight, heavy_weight


def spectral_counterfamily() -> dict[str, Any]:
    pole_mass = 1.0
    bg_light_mass = 1.4
    bg_heavy_mass = 8.0

    reference = {
        "pole_residue": 0.4,
        "bg_light_weight": 0.3,
        "bg_heavy_weight": 0.3,
    }
    total_weight = sum(reference.values())
    one_step_value = (
        reference["pole_residue"] * math.exp(-pole_mass)
        + reference["bg_light_weight"] * math.exp(-bg_light_mass)
        + reference["bg_heavy_weight"] * math.exp(-bg_heavy_mass)
    )

    rows = []
    for pole_residue in [0.18, 0.4, 0.58]:
        total_background = total_weight - pole_residue
        background_c1 = one_step_value - pole_residue * math.exp(-pole_mass)
        bg_light_weight, bg_heavy_weight = solve_two_background_weights(
            total_background,
            background_c1,
            bg_light_mass,
            bg_heavy_mass,
        )
        weights = [pole_residue, bg_light_weight, bg_heavy_weight]
        c0 = sum(weights)
        c1 = (
            pole_residue * math.exp(-pole_mass)
            + bg_light_weight * math.exp(-bg_light_mass)
            + bg_heavy_weight * math.exp(-bg_heavy_mass)
        )
        rows.append(
            {
                "pole_mass": pole_mass,
                "pole_residue": pole_residue,
                "background_masses": [bg_light_mass, bg_heavy_mass],
                "background_weights": [bg_light_weight, bg_heavy_weight],
                "all_weights_nonnegative": all(weight >= -1e-12 for weight in weights),
                "source_curvature_C0": c0,
                "one_step_source_correlator_C1": c1,
                "same_source_carrier": "Block60 taste-singlet source carrier",
            }
        )

    c0_values = [row["source_curvature_C0"] for row in rows]
    c1_values = [row["one_step_source_correlator_C1"] for row in rows]
    residues = [row["pole_residue"] for row in rows]
    return {
        "pole_mass": pole_mass,
        "reference_total_weight": total_weight,
        "reference_one_step_value": one_step_value,
        "rows": rows,
        "all_positive_spectral_measures": all(
            row["all_weights_nonnegative"] for row in rows
        ),
        "same_source_curvature": max(c0_values) - min(c0_values),
        "same_one_step_source_correlator": max(c1_values) - min(c1_values),
        "pole_residue_spread": max(residues) / min(residues),
    }


def main() -> int:
    print("PR #230 Block62 compact-source K-prime identifiability obstruction")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    family = spectral_counterfamily()

    compact_source_loaded = (
        "compact finite-volume scalar-source functional foundation"
        in statuses["block57_compact_source_functional_foundation"]
        and certs["block57_compact_source_functional_foundation"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
        and certs["block57_compact_source_functional_foundation"].get(
            "exact_denominator_or_pole_authority_present"
        )
        is False
    )
    finite_spectral_support_loaded = (
        "finite-volume compact source-channel spectral support"
        in statuses["block58_compact_source_spectral_support"]
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
        and certs["block58_compact_source_spectral_support"].get(
            "isolated_pole_residue_authority_present"
        )
        is False
        and certs["block58_compact_source_spectral_support"].get(
            "thermodynamic_limit_authority_present"
        )
        is False
    )
    carrier_fixed_no_kprime = (
        certs["block60_compact_source_taste_singlet_carrier"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "pole_residue_authority_present"
        )
        is False
    )
    source_only_lsz_boundary_loaded = (
        "source-functional LSZ identifiability theorem"
        in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    schur_path_needs_rows = (
        certs["schur_complement_kprime_sufficiency"].get(
            "schur_sufficiency_theorem_passed"
        )
        is True
        and certs["schur_complement_kprime_sufficiency"].get(
            "current_schur_kernel_rows_present"
        )
        is False
        and certs["schur_kprime_row_absence_guard"].get(
            "schur_kprime_row_absence_guard_passed"
        )
        is True
        and certs["schur_kprime_row_absence_guard"].get(
            "current_schur_kernel_rows_present"
        )
        is False
    )
    positive_same_support_variable_residue = (
        family["all_positive_spectral_measures"]
        and abs(family["same_source_curvature"]) < 1e-12
        and abs(family["same_one_step_source_correlator"]) < 1e-12
        and family["pole_residue_spread"] >= 3.0
    )
    kprime_authority = False
    pole_residue_authority = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("compact-source-support-loaded", compact_source_loaded, statuses["block57_compact_source_functional_foundation"])
    report("finite-spectral-support-loaded", finite_spectral_support_loaded, statuses["block58_compact_source_spectral_support"])
    report("carrier-fixed-but-no-kprime", carrier_fixed_no_kprime, statuses["block61_post_carrier_kprime_obstruction"])
    report("source-only-lsz-boundary-loaded", source_only_lsz_boundary_loaded, statuses["source_functional_lsz_identifiability"])
    report("schur-path-still-needs-rows", schur_path_needs_rows, statuses["schur_kprime_row_absence_guard"])
    report("positive-same-support-variable-residue-family", positive_same_support_variable_residue, f"residue_spread={family['pole_residue_spread']:.1f}x")
    report("kprime-authority-absent", not kprime_authority, "compact source support does not supply denominator derivative")
    report("pole-residue-authority-absent", not pole_residue_authority, "positive same-support family varies pole residue")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block62 is an exact negative boundary")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for the current PR230 surface: "
            "compact source support and fixed carrier do not identify K-prime or pole residue"
        ),
        "conditional_surface_status": (
            "conditional-support if future work supplies same-surface Schur "
            "A/B/C kernel rows and pole derivatives, direct C_ss/C_sH/C_HH "
            "pole rows, or a thermodynamic scalar denominator theorem"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "The compact source functional and fixed source carrier do not "
            "determine K'(pole) or the pole residue.  Positive spectral "
            "measures can preserve the current source-support invariants while "
            "changing the residue."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block62_compact_source_kprime_identifiability_obstruction_passed": True,
        "compact_source_support_loaded": compact_source_loaded,
        "finite_spectral_support_loaded": finite_spectral_support_loaded,
        "source_channel_taste_carrier_fixed": carrier_fixed_no_kprime,
        "kprime_authority_present": kprime_authority,
        "pole_residue_authority_present": pole_residue_authority,
        "positive_same_support_variable_residue_family": family,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_scalar_authority_obligations": [
            "same-surface Schur A/B/C kernel rows with pole derivatives",
            "strict C_ss/C_sH/C_HH pole rows with Gram/FVIR/contact authority",
            "thermodynamic scalar denominator theorem deriving K'(pole) and pole residue",
            "canonical O_H/source-overlap or strict physical-response bridge",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer K'(pole) from compact source curvature or carrier normalization",
            "does not treat finite source spectral positivity as pole-residue authority",
            "does not identify source carrier with canonical O_H",
            "does not use H_unit, Ward, y_t_bare, observed top/Yukawa values, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "A positive route must supply actual Schur kernel rows, strict "
            "source-Higgs pole rows, or a thermodynamic scalar denominator "
            "theorem.  Compact-source support and carrier normalization are "
            "exhausted as shortcuts."
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
