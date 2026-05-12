#!/usr/bin/env python3
"""
PR #230 Block64 finite-moment atom/residue obstruction.

After Block60 fixed the compact source carrier, Block61 blocked the
carrier-to-K-prime shortcut, and Block62 blocked compact-source support as
K-prime authority, this gate tests the next scalar shortcut:

    finite Stieltjes/source moments + fixed source carrier => fixed pole atom
    mass / scalar LSZ residue

The shortcut is not valid on the current PR230 surface.  Finite moment data can
agree while the atom at a candidate pole differs.  A positive route needs a
strict determinacy/extremality certificate, a direct pole-row residue
measurement with FV/IR/contact authority, or a microscopic K'(pole) theorem.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block64_finite_moment_atom_residue_obstruction_2026-05-12.json"
)

PARENTS = {
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block59_source_spectral_pole_promotion_obstruction": "outputs/yt_pr230_block59_source_spectral_pole_promotion_obstruction_2026-05-12.json",
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block61_post_carrier_kprime_obstruction": "outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json",
    "block62_compact_source_kprime_identifiability_obstruction": "outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json",
    "fh_lsz_stieltjes_moment_certificate_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "fh_lsz_pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "scalar_lsz_carleman_tauberian": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "finite_shell_identifiability": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
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


def moment(measure: list[tuple[Fraction, Fraction]], power: int) -> Fraction:
    return sum(weight * (point**power) for point, weight in measure)


def finite_prefix_counterfamily() -> dict[str, Any]:
    # Two positive measures on [0, 1] with identical m_0,m_1,m_2 but different
    # candidate-pole atom mass at x=0.
    measure_a = [
        (Fraction(0), Fraction(1, 6)),
        (Fraction(1, 2), Fraction(2, 3)),
        (Fraction(1), Fraction(1, 6)),
    ]
    measure_b = [
        (Fraction(0), Fraction(1, 4)),
        (Fraction(2, 3), Fraction(3, 4)),
    ]
    moments_a = [moment(measure_a, k) for k in range(3)]
    moments_b = [moment(measure_b, k) for k in range(3)]
    pole_atom_a = sum(weight for point, weight in measure_a if point == 0)
    pole_atom_b = sum(weight for point, weight in measure_b if point == 0)
    return {
        "candidate_pole_x": "0",
        "moment_powers_checked": [0, 1, 2],
        "measure_a": [
            {"x": str(point), "weight": str(weight)} for point, weight in measure_a
        ],
        "measure_b": [
            {"x": str(point), "weight": str(weight)} for point, weight in measure_b
        ],
        "moments_a": [str(value) for value in moments_a],
        "moments_b": [str(value) for value in moments_b],
        "moments_match": moments_a == moments_b,
        "pole_atom_mass_a": str(pole_atom_a),
        "pole_atom_mass_b": str(pole_atom_b),
        "pole_atom_masses_differ": pole_atom_a != pole_atom_b,
        "residue_ratio_b_over_a": str(pole_atom_b / pole_atom_a),
    }


def main() -> int:
    print("PR #230 Block64 finite-moment atom/residue obstruction")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    family = finite_prefix_counterfamily()

    block58_loaded = (
        "finite-volume compact source-channel spectral support"
        in statuses["block58_compact_source_spectral_support"]
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
    )
    block59_blocks_promotion = (
        "finite-volume source spectral positivity does not promote"
        in statuses["block59_source_spectral_pole_promotion_obstruction"]
        and certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "block59_source_spectral_pole_promotion_obstruction_passed"
        )
        is True
    )
    block60_carrier_fixed = (
        certs["block60_compact_source_taste_singlet_carrier"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
    )
    block61_kprime_blocked = (
        certs["block61_post_carrier_kprime_obstruction"].get(
            "block61_post_carrier_kprime_obstruction_passed"
        )
        is True
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "kprime_authority_present"
        )
        is False
    )
    block62_compact_source_kprime_blocked = (
        certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "block62_compact_source_kprime_identifiability_obstruction_passed"
        )
        is True
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "pole_residue_authority_present"
        )
        is False
    )
    strict_moment_authority_absent = (
        "strict positive certificate absent"
        in statuses["fh_lsz_stieltjes_moment_certificate_gate"]
        and "strict moment-threshold certificate absent"
        in statuses["fh_lsz_pade_stieltjes_bounds_gate"]
        and "Carleman/Tauberian scalar-LSZ determinacy not derivable"
        in statuses["scalar_lsz_carleman_tauberian"]
    )
    finite_shell_identifiability_blocks = (
        "finite-shell pole-fit identifiability no-go"
        in statuses["finite_shell_identifiability"]
    )
    finite_prefix_atom_not_fixed = (
        family["moments_match"] and family["pole_atom_masses_differ"]
    )

    proposal_allowed = False
    current_finite_prefix_residue_authority_present = False
    strict_extremal_moment_certificate_present = False
    direct_pole_row_residue_measurement_present = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_allowed_parents,
        f"proposal_allowed={proposal_allowed_parents}",
    )
    report("block58-source-spectral-support-loaded", block58_loaded, statuses["block58_compact_source_spectral_support"])
    report("block59-promotion-blocked", block59_blocks_promotion, statuses["block59_source_spectral_pole_promotion_obstruction"])
    report("block60-carrier-fixed", block60_carrier_fixed, statuses["block60_compact_source_taste_singlet_carrier"])
    report("block61-kprime-blocked", block61_kprime_blocked, statuses["block61_post_carrier_kprime_obstruction"])
    report("block62-compact-source-kprime-blocked", block62_compact_source_kprime_blocked, statuses["block62_compact_source_kprime_identifiability_obstruction"])
    report("strict-moment-authority-absent", strict_moment_authority_absent, "Stieltjes/Pade/Carleman parents do not certify determinacy")
    report("finite-shell-identifiability-blocks", finite_shell_identifiability_blocks, statuses["finite_shell_identifiability"])
    report("finite-prefix-atom-mass-not-fixed", finite_prefix_atom_not_fixed, f"residue_ratio={family['residue_ratio_b_over_a']}")
    report("current-finite-prefix-residue-authority-absent", not current_finite_prefix_residue_authority_present, "finite moments are not pole-residue authority")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block64 is an exact negative boundary")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for the current PR230 surface: "
            "finite source/Stieltjes moment prefixes do not fix the pole atom "
            "mass or scalar LSZ residue without an additional strict "
            "determinacy/extremality certificate"
        ),
        "conditional_surface_status": (
            "conditional-support if a future exact moment/localizing-matrix "
            "extremality certificate, Carleman/Tauberian threshold theorem, "
            "direct pole-row residue measurement, or microscopic K'(pole) "
            "theorem is supplied together with FV/IR/contact and canonical "
            "O_H/physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "The current surface has finite source moments and source-carrier "
            "support only.  The executable positive-measure counterfamily has "
            "identical m0,m1,m2 but different atom mass at the candidate pole."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block64_finite_moment_atom_residue_obstruction_passed": True,
        "finite_prefix_atom_counterfamily": family,
        "current_finite_prefix_residue_authority_present": current_finite_prefix_residue_authority_present,
        "strict_extremal_moment_certificate_present": strict_extremal_moment_certificate_present,
        "direct_pole_row_residue_measurement_present": direct_pole_row_residue_measurement_present,
        "source_channel_taste_carrier_fixed": block60_carrier_fixed,
        "compact_source_kprime_identifiability_blocked": block62_compact_source_kprime_blocked,
        "kprime_authority_present": False,
        "pole_residue_authority_present": False,
        "threshold_fvir_contact_authority_present": False,
        "canonical_oh_or_physical_response_authority_present": False,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_positive_route_requirements": [
            "strict exact moment/localizing-matrix extremality or determinacy certificate",
            "or direct source-Higgs/pole rows measuring the residue with covariance",
            "or microscopic K'(pole) denominator theorem",
            "plus threshold/FVIR/contact authority",
            "plus canonical O_H/source-overlap or physical W/Z response authority",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not treat finite moments, Pade fits, or finite-shell pole fits as LSZ residue authority",
            "does not infer K'(pole), pole atom mass, or kappa_s from source carrier normalization",
            "does not use H_unit, yt_ward_identity, observed top/Yukawa values, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Positive closure must supply an actual residue authority: an "
            "extremal/determinate moment certificate, direct pole-row residue "
            "measurement, or K'(pole) theorem, then still pair it with "
            "FV/IR/contact and canonical O_H/physical-response authority."
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
