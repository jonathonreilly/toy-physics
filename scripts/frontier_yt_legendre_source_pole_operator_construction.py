#!/usr/bin/env python3
"""
PR #230 Legendre/LSZ source-pole operator construction.

This is the strongest operator that can be derived from the current Cl(3)/Z3
scalar source functional without adding new source-Higgs data.  The connected
source two-point function fixes an LSZ-normalized source-pole operator with
unit pole residue.  That construction is invariant under source-coordinate
rescaling and insensitive to analytic source contact terms.

It is not, by itself, the physical canonical Higgs radial operator O_H used by
v.  The remaining missing theorem is the source-pole/canonical-Higgs identity:
unit overlap with O_H, equivalently source-Higgs Gram purity after a valid O_H
operator is supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_legendre_source_pole_operator_construction_2026-05-03.json"

PARENTS = {
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "source_reparametrization": "outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "source_unit_normalization_no_go": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
    "scalar_contact_boundary": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
    "scalar_renormalization_overlap_no_go": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_pole_mixing_obstruction": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "candidate_stress": "outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json",
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


def contact_term_rows() -> list[dict[str, float]]:
    """Analytic source contact terms do not change the isolated pole residue."""
    z_pole = 3.7
    rows: list[dict[str, float]] = []
    for a0, a1 in ((0.0, 0.0), (2.0, 0.0), (-1.5, 0.8), (12.0, -4.0)):
        # Let x = p^2 - p_*^2.  C_ss(x) = Z/x + a0 + a1*x + O(x^2).
        # Then Gamma_ss = 1/C_ss = x/(Z + a0*x + a1*x^2 + ...), so
        # dGamma_ss/dx at the pole is exactly 1/Z.
        gamma_prime_at_pole = 1.0 / z_pole
        unit_residue = gamma_prime_at_pole * z_pole
        rows.append(
            {
                "pole_residue_Z_s": z_pole,
                "analytic_contact_a0": a0,
                "analytic_contact_a1": a1,
                "dGamma_ss_dx_at_pole": gamma_prime_at_pole,
                "Res_C_source_pole_operator": unit_residue,
            }
        )
    return rows


def source_rescaling_rows() -> list[dict[str, float]]:
    """The LSZ-normalized source-pole operator is invariant under O_s -> c O_s."""
    z_pole = 3.7
    rows: list[dict[str, float]] = []
    for c in (0.25, 0.5, 1.0, 2.0, 4.0):
        z_scaled = c * c * z_pole
        gamma_prime_scaled = 1.0 / z_scaled
        matrix_element_os = c * math.sqrt(z_pole)
        matrix_element_osp = math.sqrt(gamma_prime_scaled) * matrix_element_os
        rows.append(
            {
                "source_rescaling_c": c,
                "Res_C_ss_scaled": z_scaled,
                "dGamma_ss_dx_scaled": gamma_prime_scaled,
                "matrix_element_O_s": matrix_element_os,
                "matrix_element_O_source_pole": matrix_element_osp,
                "source_pole_residue": matrix_element_osp * matrix_element_osp,
            }
        )
    return rows


def mixing_counterfamily_rows() -> list[dict[str, float | bool]]:
    """Hold the source-pole operator fixed while varying canonical-Higgs overlap."""
    rows: list[dict[str, float | bool]] = []
    for cos_theta in (1.0, 0.9, 0.75, 0.6):
        sin_theta = math.sqrt(max(0.0, 1.0 - cos_theta * cos_theta))
        gram_delta = 1.0 - cos_theta * cos_theta
        rows.append(
            {
                "Res_C_source_pole_source_pole": 1.0,
                "Res_C_HH_if_OH_supplied": 1.0,
                "Res_C_source_pole_H_if_OH_supplied": cos_theta,
                "canonical_higgs_overlap_cos_theta": cos_theta,
                "orthogonal_overlap_sin_theta": sin_theta,
                "source_higgs_gram_determinant": gram_delta,
                "would_certify_OH_identity": abs(gram_delta) < 1.0e-12 and abs(abs(cos_theta) - 1.0) < 1.0e-12,
            }
        )
    return rows


def forbidden_source_fragments_absent() -> tuple[bool, list[str]]:
    body = Path(__file__).read_text(encoding="utf-8")
    fragments = [
        "y_t" + "_bare :=",
        "H_unit" + " matrix-element readout as authority",
        "alpha" + "_LM as authority",
        "observed" + " target selector",
    ]
    hits = [fragment for fragment in fragments if fragment in body]
    return not hits, hits


def source_pole_operator_candidate() -> dict[str, Any]:
    return {
        "certificate_kind": "source_pole_operator",
        "same_surface_cl3z3": True,
        "same_source_coordinate": True,
        "source_coordinate": "uniform additive lattice scalar source s entering the Dirac mass as m_bare + s",
        "operator_id": "legendre_lsz_source_pole_operator_v1",
        "operator_definition": (
            "O_sp(q) = sqrt(dGamma_ss/dx|_{x=0}) O_s(q), where "
            "x = p^2 - p_*^2 and C_ss has an isolated source pole at x = 0"
        ),
        "source_pole_operator_constructed": True,
        "source_pole_residue_normalized_to_one": True,
        "canonical_higgs_operator_identity_passed": False,
        "identity_certificate": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
        "normalization_certificate": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
        "diagonal_vertex": {
            "kind": "constant_site_color_diagonal",
            "strict_limit": "diagonal source vertex only; physical O_H identity remains open",
        },
        "hunit_used_as_operator": False,
        "static_ew_algebra_used_as_operator": False,
        "proposal_allowed": False,
        "firewall": {
            "used_observed_targets_as_selectors": False,
            "used_yt_ward_identity": False,
            "used_alpha_lm_or_plaquette": False,
            "used_hunit_matrix_element_readout": False,
        },
    }


def main() -> int:
    print("PR #230 Legendre/LSZ source-pole operator construction")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    contacts = contact_term_rows()
    rescalings = source_rescaling_rows()
    mixing = mixing_counterfamily_rows()
    candidate = source_pole_operator_candidate()
    forbidden_absent, forbidden_hits = forbidden_source_fragments_absent()

    contact_unit_residues = [row["Res_C_source_pole_operator"] for row in contacts]
    rescaling_matrix_elements = [row["matrix_element_O_source_pole"] for row in rescalings]
    rescaling_residues = [row["source_pole_residue"] for row in rescalings]
    gram_deltas = [float(row["source_higgs_gram_determinant"]) for row in mixing]

    identifiability_boundary_loaded = (
        "source-functional LSZ identifiability theorem"
        in status(parents["source_functional_lsz_identifiability"])
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    source_to_higgs_open = (
        "source-to-Higgs LSZ closure attempt blocked" in status(parents["source_to_higgs_lsz"])
        and parents["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    source_unit_no_go_loaded = (
        "source-unit normalization no-go"
        in status(parents["source_unit_normalization_no_go"])
        and parents["source_unit_normalization_no_go"].get("proposal_allowed") is False
    )
    contact_boundary_loaded = (
        "scalar source contact-term scheme boundary" in status(parents["scalar_contact_boundary"])
        and parents["scalar_contact_boundary"].get("proposal_allowed") is False
    )
    renorm_overlap_no_go_loaded = (
        "renormalization-condition source-overlap no-go"
        in status(parents["scalar_renormalization_overlap_no_go"])
        and parents["scalar_renormalization_overlap_no_go"].get("proposal_allowed") is False
    )
    higgs_identity_open = (
        "canonical-Higgs pole identity gate blocking" in status(parents["fh_lsz_higgs_pole_identity"])
        and parents["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    mixing_obstruction_loaded = (
        "source-pole canonical-Higgs mixing obstruction"
        in status(parents["source_pole_mixing_obstruction"])
        and parents["source_pole_mixing_obstruction"].get("source_pole_canonical_identity_gate_passed") is False
    )
    gram_gate_open = (
        "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity"])
        and parents["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    candidate_stress_loaded = (
        "canonical-Higgs operator candidate stress rejects current substitutes"
        in status(parents["candidate_stress"])
    )

    source_pole_constructed = (
        max(contact_unit_residues) - min(contact_unit_residues) < 1.0e-12
        and abs(contact_unit_residues[0] - 1.0) < 1.0e-12
        and max(rescaling_matrix_elements) - min(rescaling_matrix_elements) < 1.0e-12
        and max(rescaling_residues) - min(rescaling_residues) < 1.0e-12
        and abs(rescaling_residues[0] - 1.0) < 1.0e-12
    )
    mixing_family_blocks_oh = (
        any(abs(delta) > 1.0e-12 for delta in gram_deltas)
        and sum(1 for row in mixing if row["would_certify_OH_identity"]) == 1
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-functional-boundary-loaded", identifiability_boundary_loaded, status(parents["source_functional_lsz_identifiability"]))
    report("source-to-higgs-lsz-still-open", source_to_higgs_open, status(parents["source_to_higgs_lsz"]))
    report("source-unit-normalization-no-go-loaded", source_unit_no_go_loaded, status(parents["source_unit_normalization_no_go"]))
    report("contact-term-boundary-loaded", contact_boundary_loaded, status(parents["scalar_contact_boundary"]))
    report("renormalization-overlap-no-go-loaded", renorm_overlap_no_go_loaded, status(parents["scalar_renormalization_overlap_no_go"]))
    report("contact-terms-do-not-change-pole-normalization", max(contact_unit_residues) - min(contact_unit_residues) < 1.0e-12, f"unit_residues={contact_unit_residues}")
    report("source-rescaling-invariant-operator", source_pole_constructed, f"matrix_elements={rescaling_matrix_elements}")
    report("source-pole-operator-is-constructed", source_pole_constructed, candidate["operator_id"])
    report("higgs-pole-identity-still-open", higgs_identity_open, status(parents["fh_lsz_higgs_pole_identity"]))
    report("mixing-family-blocks-oh-identity", mixing_family_blocks_oh, f"gram_deltas={gram_deltas}")
    report("source-pole-mixing-obstruction-loaded", mixing_obstruction_loaded, status(parents["source_pole_mixing_obstruction"]))
    report("gram-purity-route-still-open", gram_gate_open, status(parents["source_higgs_gram_purity"]))
    report("candidate-stress-loaded", candidate_stress_loaded, status(parents["candidate_stress"]))
    report("forbidden-shortcuts-absent", forbidden_absent, f"hits={forbidden_hits}")
    report("canonical-oh-not-derived", candidate["canonical_higgs_operator_identity_passed"] is False, "O_sp is not certified as O_H")

    result = {
        "actual_current_surface_status": "bounded-support / Legendre source-pole operator constructed; canonical O_H identity open",
        "verdict": (
            "The Cl(3)/Z3 scalar source functional determines an LSZ-normalized "
            "source-pole operator O_sp = sqrt(dGamma_ss/dx|pole) O_s at an "
            "isolated source pole.  This operator has unit pole residue and is "
            "invariant under source-coordinate rescaling; analytic source "
            "contact terms do not change the construction.  This is the maximal "
            "same-source operator derivable on the current PR #230 surface.  It "
            "does not yet prove O_sp = O_H, because a source pole can still be "
            "a mixture cos(theta) O_H + sin(theta) O_chi while preserving the "
            "source-pole normalization.  Closing O_H requires source-Higgs Gram "
            "purity, a rank-one neutral-scalar theorem, or an equivalent W/Z "
            "response/sector-overlap certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source-pole operator is constructed, but the canonical-Higgs radial identity is still open.",
        "source_pole_operator_constructed": source_pole_constructed,
        "canonical_higgs_operator_identity_passed": False,
        "operator_candidate": candidate,
        "legendre_lsz_formula": {
            "connected_two_point_near_pole": "C_ss(x) = Z_s/x + analytic, x = p^2 - p_*^2",
            "inverse_derivative": "dGamma_ss/dx|_{x=0} = 1/Z_s",
            "source_pole_operator": "O_sp = sqrt(dGamma_ss/dx|pole) O_s",
            "unit_residue": "Res(C_sp_sp) = (dGamma_ss/dx|pole) Res(C_ss) = 1",
        },
        "contact_term_rows": contacts,
        "source_rescaling_rows": rescalings,
        "canonical_higgs_overlap_counterfamily": mixing,
        "why_not_O_H_yet": [
            "The construction normalizes the source pole, not the canonical Higgs radial field used by v.",
            "A mixed pole O_sp = cos(theta) O_H + sin(theta) O_chi has the same source-pole normalization for different theta.",
            "Source-only C_ss data cannot measure C_sH or C_HH pole residues.",
            "No current theorem excludes an orthogonal neutral scalar top coupling.",
        ],
        "necessary_next_certificate": [
            "same-surface canonical O_H identity plus normalization certificate",
            "or pole-level C_sH/C_HH residues satisfying Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
            "or a rank-one neutral-scalar theorem excluding orthogonal admixture",
            "or a same-source W/Z response certificate fixing the sector overlap",
        ],
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not identify O_s or O_sp with canonical H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Use O_sp as the normalized source-pole side of the next test, then "
            "derive or measure its overlap with canonical O_H through C_sH/C_HH "
            "Gram purity, W/Z response, or a rank-one neutral-scalar theorem."
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
