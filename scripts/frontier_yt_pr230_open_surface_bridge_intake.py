#!/usr/bin/env python3
"""
PR #230 open-surface bridge intake.

This runner deliberately widens the search beyond the current repo surface.
It does not import external literature as proof authority.  Instead it records
which outside physics/math surfaces could supply the missing PR230 bridge:
canonical O_H, production C_ss/C_sH/C_HH pole rows with Gram flatness, a
neutral rank-one theorem, or a strict W/Z physical-response packet.

The result is route intake only: bounded support, proposal_allowed=false.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_open_surface_bridge_intake_2026-05-07.json"

PARENTS = {
    "canonical_oh_hard_residual": (
        "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json"
    ),
    "source_higgs_aperture": (
        "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json"
    ),
    "source_higgs_time_kernel_manifest": (
        "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json"
    ),
    "neutral_h3h4_aperture": (
        "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
    ),
    "wz_response_intake": (
        "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json"
    ),
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_yt_ward_identity": False,
    "used_hunit_matrix_element_or_hunit_operator": False,
    "used_y_t_bare": False,
    "used_observed_y_t_or_top_mass": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "aliased_c_sx_to_c_sh_before_canonical_oh": False,
    "treated_literature_as_proof_authority": False,
    "touched_live_chunk_worker": False,
}

SOURCES = [
    {
        "id": "fms_1981",
        "title": "Higgs phenomenon without symmetry breaking order parameter",
        "authors": "Froehlich, Morchio, Strocchi",
        "surface": "gauge-invariant BEH/FMS operator language",
        "url": "https://archives.ihes.fr/document/P_81_12.pdf",
        "use_in_pr230": "route guidance for defining physical gauge-invariant Higgs operators; not proof of the PR230 source overlap",
    },
    {
        "id": "fms_observable_spectrum_2017",
        "title": "On the observable spectrum of theories with a Brout-Englert-Higgs effect",
        "authors": "Maas, Sondenheimer, Toerek",
        "surface": "FMS/gauge-invariant spectrum",
        "url": "https://arxiv.org/abs/1709.07477",
        "use_in_pr230": "evidence that FMS supplies a known gauge-invariant composite-to-elementary mapping in suitable BEH regimes",
    },
    {
        "id": "su3_fundamental_higgs_spectrum_2018",
        "title": "The spectrum of an SU(3) gauge theory with a fundamental Higgs field",
        "authors": "Maas, Toerek",
        "surface": "lattice gauge-Higgs spectroscopy",
        "url": "https://arxiv.org/abs/1804.04453",
        "use_in_pr230": "method precedent for lattice spectroscopy of gauge-invariant Higgs composites",
    },
    {
        "id": "lattice_higgs_yukawa_2010",
        "title": "Upper and lower Higgs boson mass bounds from a chirally invariant lattice Higgs-Yukawa model",
        "authors": "Gerhold",
        "surface": "nonperturbative lattice Higgs-Yukawa top/bottom sector",
        "url": "https://arxiv.org/abs/1002.2569",
        "use_in_pr230": "method precedent for lattice Higgs-top-bottom Yukawa simulations; not a derivation of y_t without an accepted bridge",
    },
    {
        "id": "fradkin_shenker_1979",
        "title": "Phase diagrams of lattice gauge theories with Higgs fields",
        "authors": "Fradkin, Shenker",
        "surface": "lattice gauge-Higgs analytic-continuity structure",
        "url": "https://doi.org/10.1103/PhysRevD.19.3682",
        "use_in_pr230": "route guidance for admissible gauge-Higgs surface extensions; not an overlap selector",
    },
    {
        "id": "osterwalder_schrader_1973",
        "title": "Axioms for Euclidean Green's functions",
        "authors": "Osterwalder, Schrader",
        "surface": "Euclidean reconstruction / reflection positivity",
        "url": "https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-31/issue-2/Axioms-for-Euclidean-Greens-functions/cmp/1103858969.pdf",
        "use_in_pr230": "justifies transfer/Hilbert-space reconstruction from valid Euclidean correlators; does not by itself identify O_sp with O_H",
    },
    {
        "id": "luscher_transfer_1977",
        "title": "Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories",
        "authors": "Luescher",
        "surface": "lattice transfer matrix positivity",
        "url": "https://doi.org/10.1007/bf01614090",
        "use_in_pr230": "supports the transfer-kernel route once the correct gauge-invariant operators are supplied",
    },
    {
        "id": "complex_cones_pf_2010",
        "title": "Cones and gauges in complex spaces: Spectral gaps and complex Perron-Frobenius theory",
        "authors": "Rugh",
        "surface": "positive/complex cone spectral gap methods",
        "url": "https://annals.math.princeton.edu/2010/171-3/p07",
        "use_in_pr230": "candidate math toolkit for a neutral primitive/rank-one theorem; requires a PR230 physical transfer kernel first",
    },
    {
        "id": "sm_criticality_1995",
        "title": "Standard Model Criticality Prediction: Top mass 173 +/- 5 GeV and Higgs mass 135 +/- 9 GeV",
        "authors": "Froggatt, Nielsen",
        "surface": "multiple-point / Planck-criticality top-mass route",
        "url": "https://arxiv.org/abs/hep-ph/9511371",
        "use_in_pr230": "possible external axiom route; not current-surface derivation and not enough for PR230 retention",
    },
    {
        "id": "mpcp_gravity_tension_2014",
        "title": "Gravitational effects on vanishing Higgs potential at the Planck scale",
        "authors": "Haba, Kaneta, Takahashi, Yamaguchi",
        "surface": "MPCP/beta_lambda Planck boundary tension",
        "url": "https://arxiv.org/abs/1408.5548",
        "use_in_pr230": "negative/constraint context for criticality route; warns that beta_lambda(M_Pl)=0 is not automatically SM closure",
    },
]

ROUTES = [
    {
        "rank": 1,
        "route_id": "fms_gauge_invariant_higgs_operator_rows",
        "external_surface": "FMS + lattice gauge-Higgs spectroscopy",
        "repo_disjunct_supplied_if_successful": "certified O_H plus C_ss/C_sH/C_HH pole rows",
        "positive_candidate": True,
        "audit_posture": "open-surface candidate; would need accepted same-surface EW/Higgs action or derivation from Cl(3)/Z^3 before proof use",
        "why_relevant": (
            "FMS gives the right language for a gauge-invariant physical Higgs "
            "operator.  If PR230 can build O_H as a same-surface composite and "
            "measure source-Higgs time-kernel rows, this directly attacks the "
            "O_sp/O_H overlap residual without Ward/H_unit renaming."
        ),
        "immediate_target": (
            "Promote the existing source-Higgs time-kernel manifest into a pilot "
            "that consumes an explicit candidate gauge-invariant O_H definition, "
            "then require Gram flatness rather than setting overlap factors to one."
        ),
        "source_ids": [
            "fms_1981",
            "fms_observable_spectrum_2017",
            "su3_fundamental_higgs_spectrum_2018",
            "fradkin_shenker_1979",
        ],
    },
    {
        "rank": 2,
        "route_id": "os_transfer_matrix_pole_row_reconstruction",
        "external_surface": "OS reconstruction + lattice transfer matrix positivity",
        "repo_disjunct_supplied_if_successful": "production pole rows and Gram flatness for a certified operator basis",
        "positive_candidate": True,
        "audit_posture": "method bridge only; valid after actual Euclidean time rows and operator certificate exist",
        "why_relevant": (
            "The current finite static rows are underdetermined.  OS/transfer "
            "machinery says the right object is a time-ordered correlator kernel "
            "and spectral/pole residue extraction, not equal-time aliasing."
        ),
        "immediate_target": (
            "Run a tiny source-Higgs time-kernel scout after an explicit O_H "
            "candidate is supplied; require C_ss(t), C_sH(t), C_HH(t), GEVP pole "
            "residue, covariance, and FV/IR gates."
        ),
        "source_ids": ["osterwalder_schrader_1973", "luscher_transfer_1977"],
    },
    {
        "rank": 3,
        "route_id": "neutral_primitive_positive_cone_theorem",
        "external_surface": "Krein-Rutman/Jentzsch/Perron-Frobenius style cone theory",
        "repo_disjunct_supplied_if_successful": "same-surface neutral scalar rank-one/flat-extension theorem",
        "positive_candidate": True,
        "audit_posture": "hard theorem route; blocked until PR230 supplies a physical positivity-improving transfer kernel",
        "why_relevant": (
            "Block07 reduced the obstruction to PSD flatness Delta_spH=0.  A "
            "genuine positivity-improving transfer theorem could force rank one "
            "in the neutral scalar channel, but reflection positivity alone is "
            "insufficient."
        ),
        "immediate_target": (
            "Formulate H3/H4 as a concrete positive-kernel problem: operator "
            "space, cone, compactness, irreducibility, and source/Higgs coupling "
            "functional.  Do not claim rank one from PSD bounds alone."
        ),
        "source_ids": ["complex_cones_pf_2010", "luscher_transfer_1977"],
    },
    {
        "rank": 4,
        "route_id": "lattice_higgs_yukawa_targeted_compute",
        "external_surface": "chirally invariant lattice Higgs-Yukawa simulations",
        "repo_disjunct_supplied_if_successful": "direct top/Higgs sector measurement route",
        "positive_candidate": False,
        "audit_posture": "compute/method route; Yukawa must not be an input tuned to the answer",
        "why_relevant": (
            "This is the nearest established nonperturbative compute route for "
            "the top/bottom/Higgs sector.  It can benchmark PR230 methodology, "
            "but it does not avoid the bridge if y_t is merely a scanned input."
        ),
        "immediate_target": (
            "Use only as a validation template for operator construction, "
            "correlator fitting, and uncertainty accounting; do not count as "
            "derived y_t unless m_t is predicted from substrate data."
        ),
        "source_ids": ["lattice_higgs_yukawa_2010"],
    },
    {
        "rank": 5,
        "route_id": "planck_criticality_beta_lambda_route",
        "external_surface": "multiple-point/Planck criticality",
        "repo_disjunct_supplied_if_successful": "external boundary condition on y_t via SM RGE",
        "positive_candidate": False,
        "audit_posture": "new principle/import unless beta_lambda(M_Pl)=0 is derived from Cl(3)/Z^3",
        "why_relevant": (
            "Criticality can numerically point at top mass, but it is not the "
            "PR230 physical-observable source-Higgs bridge.  It remains a "
            "separate axiom/derivation problem and has known SM tension."
        ),
        "immediate_target": (
            "Keep as an independent lane only if the Planck boundary condition "
            "is derived natively; do not use it to patch PR230 O_H closure."
        ),
        "source_ids": ["sm_criticality_1995", "mpcp_gravity_tension_2014"],
    },
]

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


def main() -> int:
    print("PR #230 open-surface bridge intake")
    print("=" * 72)

    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    source_ids = {source["id"] for source in SOURCES}
    route_source_errors = [
        route["route_id"]
        for route in ROUTES
        if not set(route["source_ids"]).issubset(source_ids)
    ]
    current_surface_only = False
    proof_authority_imported = any(FORBIDDEN_FIREWALL.values())
    positive_routes = [route for route in ROUTES if route["positive_candidate"]]
    routes_by_disjunct = {
        route["repo_disjunct_supplied_if_successful"] for route in ROUTES
    }

    report("parents_present", not missing_parents, f"missing={missing_parents}")
    report("literature_scope_widened", len(SOURCES) >= 8, f"sources={len(SOURCES)}")
    report("route_count", len(ROUTES) >= 5, f"routes={len(ROUTES)}")
    report("route_sources_resolve", not route_source_errors, f"errors={route_source_errors}")
    report(
        "not_current_surface_limited",
        not current_surface_only,
        "survey includes FMS, lattice gauge-Higgs, OS transfer, cone theory, and criticality surfaces",
    )
    report(
        "positive_candidates_present",
        len(positive_routes) >= 3,
        f"positive_candidate_routes={[r['route_id'] for r in positive_routes]}",
    )
    report(
        "bridge_disjunct_coverage",
        len(routes_by_disjunct) >= 4,
        f"covered={sorted(routes_by_disjunct)}",
    )
    report(
        "external_sources_not_proof_authority",
        not proof_authority_imported,
        "literature is route guidance only; no y_t proof imports are activated",
    )
    report("proposal_firewall", True, "proposal_allowed=false; PR230 remains open")
    report(
        "top_route_has_engineering_target",
        bool(ROUTES[0]["immediate_target"]),
        ROUTES[0]["route_id"],
    )
    report(
        "ward_trap_firewall",
        not (
            FORBIDDEN_FIREWALL["used_yt_ward_identity"]
            or FORBIDDEN_FIREWALL["used_hunit_matrix_element_or_hunit_operator"]
            or FORBIDDEN_FIREWALL["used_y_t_bare"]
        ),
        "Ward/H_unit/y_t_bare not used",
    )
    report(
        "observed_value_firewall",
        not (
            FORBIDDEN_FIREWALL["used_observed_y_t_or_top_mass"]
            or FORBIDDEN_FIREWALL["used_observed_wz_or_g2"]
        ),
        "observed targets not used as selectors",
    )

    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "actual_current_surface_status": (
            "bounded-support / open-surface bridge intake; no current PR230 closure"
        ),
        "conditional_surface_status": (
            "exact support if a future accepted route supplies certified O_H plus "
            "production C_ss/C_sH/C_HH pole rows with Gram flatness, or a physical "
            "neutral rank-one theorem, or a strict W/Z physical-response packet "
            "without forbidden imports"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The artifact surveys external/open surfaces as route guidance only. "
            "It imports no proof authority and supplies no certified O_H, pole rows, "
            "rank-one theorem, accepted W/Z action, production W/Z rows, covariance, "
            "strict g2 certificate, or production top response."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "open_surface_search_not_current_repo_limited": True,
        "sources": SOURCES,
        "ranked_routes": ROUTES,
        "recommended_next_non_chunk_route": ROUTES[0],
        "fallback_next_route": ROUTES[1],
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "parents": PARENTS,
        "parent_statuses": {
            name: cert.get("actual_current_surface_status", "") if cert else "missing"
            for name, cert in parents.items()
        },
        "checks": {"pass": PASS_COUNT, "fail": FAIL_COUNT},
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
