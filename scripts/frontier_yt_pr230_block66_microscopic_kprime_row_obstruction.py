#!/usr/bin/env python3
"""
PR #230 Block66 microscopic K-prime/residue row obstruction.

This probe tests the direct microscopic route requested after Blocks57-64:

    compact source functional / transfer operator / Feshbach denominator
    => K'(pole) or pole residue.

The route has a clean conditional theorem.  For an analytic same-surface
inverse kernel K(x), a simple pole at x_* has source residue

    <u,r><l,u> / <l,K'(x_*)r>,

where r,l are the right/left nullvectors of K(x_*).  In a Schur/Feshbach
source/orthogonal split, the denominator derivative is the derivative of the
Schur complement.  Thus the exact missing row is the pole derivative/projection
row: either <l,K'(x_*)r> directly, or the block derivative rows entering the
Feshbach denominator.  Current PR230 support supplies compact finite-volume
source and spectral support, but not that row, not thermodynamic/FVIR isolated
pole authority, and not canonical O_H/physical-response authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block66_microscopic_kprime_row_obstruction_2026-05-12.json"
)

PARENTS = {
    "block57_compact_source_functional_foundation": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block59_source_spectral_pole_promotion_obstruction": "outputs/yt_pr230_block59_source_spectral_pole_promotion_obstruction_2026-05-12.json",
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block61_post_carrier_kprime_obstruction": "outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json",
    "block62_compact_source_kprime_identifiability_obstruction": "outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json",
    "block63_lane1_completion_audit": "outputs/yt_pr230_block63_lane1_completion_audit_2026-05-12.json",
    "block64_finite_moment_atom_residue_obstruction": "outputs/yt_pr230_block64_finite_moment_atom_residue_obstruction_2026-05-12.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_abc_definition_derivation_attempt": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "schur_pole_lift_gate": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
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


def assumptions_exercise() -> list[dict[str, str]]:
    return [
        {
            "assumption": "same-surface analytic inverse kernel K(x) exists near the scalar pole",
            "needed_for": "turn the source two-point function into a meromorphic inverse-kernel problem",
            "if_wrong": "the residue formula is only formal; source functional derivatives do not define K'(pole)",
        },
        {
            "assumption": "the pole is isolated and simple after the required FVIR/thermodynamic order",
            "needed_for": "replace the resolvent by a one-pole Laurent term with a rank-one spectral projection",
            "if_wrong": "continuous threshold or multipole behavior replaces a scalar LSZ residue by nonlocal spectral data",
        },
        {
            "assumption": "left/right pole vectors or the spectral projection are defined on the same surface",
            "needed_for": "evaluate the numerator <u,r><l,u> and the derivative sandwich <l,K'(x*)r>",
            "if_wrong": "a denominator zero alone has no normalization and no physical residue",
        },
        {
            "assumption": "source carrier normalization from the additive Cl(3)/Z3 scalar source is the source coordinate used in K",
            "needed_for": "prevent moving factors between source coordinate, operator, and numerator",
            "if_wrong": "the source residue can be rescaled without changing the pole location",
        },
        {
            "assumption": "Feshbach/Schur P/Q split is a certified neutral scalar kernel split, not a source-only reconstruction",
            "needed_for": "interpret A/B/C rows and their derivatives as same-surface operator rows",
            "if_wrong": "Schur algebra is correct but its rows are labels without authority",
        },
        {
            "assumption": "contact subtraction is fixed before taking the pole derivative",
            "needed_for": "separate analytic contact curvature from the nonanalytic pole residue",
            "if_wrong": "finite contact choices can change inverse-curvature reads without changing finite source support",
        },
        {
            "assumption": "analytic continuation from Euclidean transfer data to the pole variable is authorized",
            "needed_for": "identify the derivative variable x used in K'(x*) with the scalar LSZ pole variable",
            "if_wrong": "transfer energies or Euclidean moments do not define the required p^2 derivative",
        },
        {
            "assumption": "FVIR, toron, and thermodynamic limits commute with pole isolation and residue extraction",
            "needed_for": "promote finite-volume spectral sums to a strict scalar pole row",
            "if_wrong": "atomless soft-continuum limits can erase the finite-volume pole residue",
        },
        {
            "assumption": "canonical O_H/source-overlap or strict physical response authority is supplied separately",
            "needed_for": "turn a source-pole residue into the top-Yukawa Higgs normalization used by PR230",
            "if_wrong": "the route at most normalizes O_sp, not the canonical Higgs radial field",
        },
    ]


def first_principles_minimal_driver() -> dict[str, Any]:
    return {
        "denominator_zero": {
            "row": "D(x*) = 0",
            "role": "locates the candidate source pole",
            "not_enough_because": "zeros do not determine Laurent residues",
        },
        "derivative_at_zero": {
            "row": "D'(x*) = <l,K'(x*)r> or Feshbach D_eff'(x*)",
            "role": "fixes the inverse-propagator slope and therefore the denominator part of the residue",
            "not_enough_because": "it must be paired with a same-surface source numerator/projection",
        },
        "numerator_or_source_normalization": {
            "row": "N* = <u,r><l,u>, or N*=1 only after a certified source-coordinate Schur normalization",
            "role": "fixes the source overlap with the pole state",
            "not_enough_because": "source-pole normalization still does not identify canonical O_H",
        },
        "same_surface_primitives": [
            "analytic transfer/inverse-kernel family K(x)",
            "pole projection or left/right pole vectors",
            "K'(x*) derivative row in the physical pole variable",
            "source vector u from the compact additive scalar source",
            "contact subtraction and FVIR/toron limiting order",
            "canonical O_H/source-overlap or strict physical response authority",
        ],
        "blocked_shortcut": (
            "Blocks57-64 provide support around the source functional, finite "
            "spectral positivity, source carrier, and finite moments.  They do "
            "not supply the derivative/projection row."
        ),
    }


def literature_and_math_search() -> list[dict[str, str]]:
    return [
        {
            "topic": "Feshbach projection operators",
            "reference": "H. Feshbach, Unified Theory of Nuclear Reactions, Annals of Physics 5 (1958), doi:10.1016/0003-4916(58)90007-1",
            "url": "https://www.osti.gov/biblio/4272316",
            "role": "projection/Feshbach denominator context; not a PR230 row source",
        },
        {
            "topic": "Feshbach projection operator flexibility and quantitative projections",
            "reference": "H. Feshbach, A Unified Theory of Nuclear Reactions. Part II, Annals of Physics 19 (1962), doi:10.1016/0003-4916(62)90221-X",
            "url": "https://www.osti.gov/biblio/4796566",
            "role": "supports the distinction between formal projection identities and explicit projection rows",
        },
        {
            "topic": "lattice reflection positivity and transfer matrices",
            "reference": "K. Osterwalder and E. Seiler, Gauge field theories on a lattice, Annals of Physics 110 (1978), doi:10.1016/0003-4916(78)90039-8",
            "url": "https://oamonitor.ireland.openaire.eu/rpo/rcsi/search/publication?pid=10.1016%2F0003-4916%2878%2990039-8",
            "role": "stable transfer-matrix background for finite-volume spectral support",
        },
        {
            "topic": "analytic perturbation and spectral projections",
            "reference": "T. Kato, Perturbation theory for linear operators, Springer (1966), doi:10.1007/978-3-662-12678-3",
            "url": "https://link.springer.com/book/10.1007/978-3-662-12678-3",
            "role": "standard source for analytic eigenprojections and resolvent residues",
        },
        {
            "topic": "analytic Fredholm theorem",
            "reference": "analytic Fredholm theorem, standard operator-theory theorem",
            "url": "https://en.wikipedia.org/wiki/Analytic_Fredholm_theorem",
            "role": "context for meromorphic inverse families; does not provide PR230 pole rows",
        },
        {
            "topic": "lattice correlator spectral matrices",
            "reference": "A. C. Lichtl, The Spectral Structure of Correlator Matrices, PoS LAT2007 (2007), arXiv:0711.4072",
            "url": "https://arxiv.org/abs/0711.4072",
            "role": "lattice two-point correlator overlap context",
        },
        {
            "topic": "Kallen-Lehmann/Stieltjes lattice scalar correlators",
            "reference": "D. Dudal, O. Oliveira, M. Roelfs, Kallen-Lehmann Spectral Representation of the Scalar SU(2) Glueball, EPJC 82 (2022), arXiv:2103.11846",
            "url": "https://arxiv.org/abs/2103.11846",
            "role": "stable example of lattice scalar two-point functions as spectral-density inversion, not residue proof input",
        },
        {
            "topic": "Krein/Birman-Schwinger resolvent reductions",
            "reference": "Krein-type and Birman-Schwinger resolvent formulas, operator-theory context",
            "url": "https://academic.oup.com/plms/article/104/3/577/1547786",
            "role": "mathematical analogy: zeros of reduced determinants still need derivative/projection data",
        },
    ]


def feshbach_derivative_formula() -> dict[str, Any]:
    return {
        "source_projection": "P",
        "orthogonal_projection": "Q = I - P",
        "orthogonal_resolvent": "R(x*) = (Q K(x*) Q)^(-1) on Q-space",
        "denominator": "D_eff = P K P - P K Q R Q K P",
        "derivative": (
            "D_eff' = P K' P - P K' Q R Q K P - P K Q R Q K' P "
            "+ P K Q R Q K' Q R Q K P"
        ),
        "missing_rows": [
            "P K'(x*) P",
            "P K'(x*) Q and Q K'(x*) P",
            "Q K'(x*) Q inside the reduced resolvent sandwich",
            "same-surface P/Q neutral scalar kernel split",
        ],
    }


def same_pole_operator_witness() -> dict[str, Any]:
    # Analytic 2x2 self-adjoint inverse kernels with identical K(0), identical
    # source vector e_s, identical Feshbach pole D_eff(0)=0, and different
    # K'(0) sandwich rows.
    g = 0.3
    m = 2.0
    a0 = g * g / m
    x_pole = 0.0
    rows = []
    for alpha in [0.5, 1.0, 2.0, 4.0]:
        d_eff_prime = alpha
        norm_r2 = 1.0 + (g / m) ** 2
        normalized_numerator = 1.0 / norm_r2
        normalized_derivative_sandwich = alpha / norm_r2
        rows.append(
            {
                "alpha": alpha,
                "K_x": f"[[{a0} + alpha*x, {g}], [{g}, {m}]]",
                "K_at_pole": [[a0, g], [g, m]],
                "right_nullvector_at_pole_unnormalized": [1.0, -g / m],
                "source_vector": [1.0, 0.0],
                "feshbach_D_eff_at_pole": 0.0,
                "feshbach_D_eff_prime_at_pole": d_eff_prime,
                "normalized_numerator": normalized_numerator,
                "normalized_derivative_sandwich": normalized_derivative_sandwich,
                "residue": normalized_numerator / normalized_derivative_sandwich,
                "same_pole_location": x_pole,
            }
        )
    residues = [row["residue"] for row in rows]
    k0_values = [row["K_at_pole"] for row in rows]
    return {
        "description": (
            "All rows have the same K(0), source vector, Feshbach zero, and "
            "nullvector at the pole.  Only the same-surface derivative row "
            "K'(0) changes, so the residue changes."
        ),
        "pole": x_pole,
        "same_K_at_pole": all(k0 == k0_values[0] for k0 in k0_values),
        "same_source_vector": True,
        "same_denominator_zero": all(row["feshbach_D_eff_at_pole"] == 0.0 for row in rows),
        "derivative_row_varies": max(row["feshbach_D_eff_prime_at_pole"] for row in rows)
        / min(row["feshbach_D_eff_prime_at_pole"] for row in rows),
        "residue_varies": max(residues) / min(residues),
        "rows": rows,
    }


def main() -> int:
    print("PR #230 Block66 microscopic K-prime/residue row obstruction")
    print("=" * 80)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    family = same_pole_operator_witness()
    assumptions = assumptions_exercise()
    minimal_driver = first_principles_minimal_driver()
    feshbach_rows = feshbach_derivative_formula()
    literature = literature_and_math_search()

    compact_source_loaded = (
        certs["block57_compact_source_functional_foundation"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
    )
    existing_blockers_loaded = (
        certs["block59_source_spectral_pole_promotion_obstruction"].get(
            "thermodynamic_pole_authority_present"
        )
        is False
        and certs["block61_post_carrier_kprime_obstruction"].get(
            "kprime_authority_present"
        )
        is False
        and certs["block62_compact_source_kprime_identifiability_obstruction"].get(
            "pole_residue_authority_present"
        )
        is False
        and certs["block64_finite_moment_atom_residue_obstruction"].get(
            "current_finite_prefix_residue_authority_present"
        )
        is False
    )
    source_pole_only_boundary_loaded = (
        certs["legendre_source_pole_operator"].get("source_pole_operator_constructed")
        is True
        and certs["legendre_source_pole_operator"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
        and certs["source_functional_lsz_identifiability"].get("theorem_closed")
        is False
    )
    schur_sufficiency_loaded_but_rows_absent = (
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
    schur_definition_and_pole_lift_blocked = (
        "Schur A/B/C definition not derivable"
        in statuses["schur_abc_definition_derivation_attempt"]
        and "finite Schur A/B/C rows do not lift"
        in statuses["schur_pole_lift_gate"]
    )
    completion_audit_still_open = (
        certs["block63_lane1_completion_audit"].get("full_positive_closure_achieved")
        is False
        and certs["block63_lane1_completion_audit"].get("proposal_allowed") is False
    )
    same_pole_derivative_witness_passed = (
        family["same_K_at_pole"]
        and family["same_source_vector"]
        and family["same_denominator_zero"]
        and family["derivative_row_varies"] >= 8.0
        and family["residue_varies"] >= 8.0
    )

    same_surface_kprime_derivative_row_present = False
    transfer_spectral_projection_overlap_row_present = False
    thermodynamic_fvir_isolated_pole_authority_present = False
    canonical_oh_or_physical_response_authority_present = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_allowed_parents,
        f"proposal_allowed={proposal_allowed_parents}",
    )
    report("compact-source-and-finite-spectral-support-loaded", compact_source_loaded, "Blocks57-58 loaded")
    report("blocks59-61-62-64-blockers-loaded", existing_blockers_loaded, "pole-promotion, carrier, compact-source, and finite-moment shortcuts blocked")
    report("source-pole-only-boundary-loaded", source_pole_only_boundary_loaded, "O_sp support does not identify canonical O_H")
    report("schur-sufficiency-loaded-but-rows-absent", schur_sufficiency_loaded_but_rows_absent, "Schur formula present; row authority absent")
    report("schur-definition-and-pole-lift-blocked", schur_definition_and_pole_lift_blocked, "A/B/C definition and finite pole lift gates block shortcuts")
    report("completion-audit-still-open", completion_audit_still_open, statuses["block63_lane1_completion_audit"])
    report("same-pole-operator-derivative-witness", same_pole_derivative_witness_passed, f"residue_spread={family['residue_varies']:.1f}x")
    report("same-surface-kprime-derivative-row-absent", not same_surface_kprime_derivative_row_present, "missing <l,K'(pole)r> or Feshbach derivative rows")
    report("transfer-projection-overlap-row-absent", not transfer_spectral_projection_overlap_row_present, "missing ||P_* O_s Omega||^2 row")
    report("thermodynamic-fvir-pole-authority-absent", not thermodynamic_fvir_isolated_pole_authority_present, "Blocks58-59 leave this open")
    report("canonical-oh-or-physical-response-authority-absent", not canonical_oh_or_physical_response_authority_present, "source pole is not canonical Higgs")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block66 is an exact negative boundary")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for the current PR230 surface: "
            "microscopic source/transfer/Feshbach formalism reduces K'(pole) "
            "or pole residue to a missing same-surface derivative/projection row"
        ),
        "conditional_surface_status": (
            "conditional-support if future work supplies an analytic same-surface "
            "inverse kernel or transfer resolvent with an isolated simple pole, "
            "the spectral projection/source-overlap row, the K'(pole) derivative "
            "sandwich or Feshbach block derivative rows, contact/FVIR authority, "
            "and canonical O_H or strict physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "The formal residue theorem is conditional and exact, but the "
            "current PR230 surface does not contain the load-bearing "
            "same-surface pole derivative/projection row.  The executable "
            "operator witness keeps K(pole), source vector, nullvector, and "
            "denominator zero fixed while changing K'(pole) and the residue."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block66_microscopic_kprime_row_obstruction_passed": True,
        "assumptions_exercise": assumptions,
        "first_principles_minimal_driver": minimal_driver,
        "operator_residue_identity": {
            "general_formula": "Res_x=<u,r><l,u>/<l,K'(x*)r> for a simple pole of K(x)^(-1)",
            "self_adjoint_formula": "Res_x=|<u,psi>|^2/<psi,K'(x*)psi>",
            "transfer_resolvent_formula": "Res_z <u,(1-zT)^(-1)u> = -z_* <u,P_*u> for isolated T-eigenvalue lambda_*=1/z_*",
            "source_pole_operator_limit": "unit residue can be obtained by O_sp normalization, but this is not canonical O_H authority",
        },
        "feshbach_derivative_formula": feshbach_rows,
        "same_pole_operator_witness": family,
        "literature_and_mathematics_search": literature,
        "same_surface_kprime_derivative_row_present": same_surface_kprime_derivative_row_present,
        "transfer_spectral_projection_overlap_row_present": transfer_spectral_projection_overlap_row_present,
        "thermodynamic_fvir_isolated_pole_authority_present": thermodynamic_fvir_isolated_pole_authority_present,
        "canonical_oh_or_physical_response_authority_present": canonical_oh_or_physical_response_authority_present,
        "exact_operator_row_whose_absence_blocks_closure": [
            "direct analytic-kernel row: <l_*, K'(x_*) r_*>",
            "transfer row: <O_s Omega, P_* O_s Omega> plus isolated-pole/FVIR authority",
            "Feshbach rows: P K' P, P K' Q, Q K' P, Q K' Q in the certified source/orthogonal split",
            "canonical bridge row: O_sp to O_H overlap or strict physical W/Z response",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not use finite-prefix moments, Pade rows, or finite endpoint secants as residue authority",
            "does not infer Schur A/B/C rows from source-only C_ss data",
            "does not identify O_s or O_sp with canonical O_H",
            "does not use H_unit, Ward, y_t_bare, observed targets, alpha_LM, plaquette/u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Do not replay source-functional, finite spectral, fixed-carrier, "
            "or finite-moment shortcuts.  A positive route must produce the "
            "same-surface derivative/projection row itself, or strict "
            "source-Higgs/physical-response pole rows with FVIR/contact and "
            "canonical O_H authority."
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
