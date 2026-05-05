#!/usr/bin/env python3
"""
PR #230 missing-bridge literature and assumption exercises.

This is a physics-loop style artifact for the current top-Yukawa bridge:

    source pole O_s / O_sp  ->  canonical Higgs radial O_H
    source-only Z(s,0)      ->  two-source Z(s,h), C_sH, C_HH

The runner records two exercises:
  1. Targeted literature search, including math-heavy tools outside ordinary
     lattice-QCD practice.
  2. Assumption questioning against the exact missing bridge.

It is not a proof of y_t.  It classifies route families and keeps the claim
firewall explicit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_missing_bridge_literature_assumption_exercises_2026-05-05.json"
)

PARENT_CERTIFICATES = {
    "holonomic_source_response_gate": (
        "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
    ),
    "action_first_oh_artifact_attempt": (
        "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json"
    ),
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "source_functional_lsz_identifiability": (
        "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
    ),
    "source_higgs_gram_purity": (
        "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json"
    ),
    "same_source_sector_overlap": (
        "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json"
    ),
    "schur_abc_definition_attempt": (
        "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json"
    ),
    "neutral_primitive_cone_gate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
    ),
    "full_positive_closure_assembly_gate": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_closure_route": (
        "outputs/yt_retained_closure_route_certificate_2026-05-01.json"
    ),
}

TEXT_SURFACES = {
    "canonical_higgs_repo_authority_audit": (
        "docs/YT_CANONICAL_HIGGS_REPO_AUTHORITY_AUDIT_NOTE_2026-05-03.md"
    ),
    "source_functional_lsz_identifiability": (
        "docs/YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md"
    ),
    "holonomic_source_response_gate": (
        "docs/YT_PR230_HOLONOMIC_SOURCE_RESPONSE_FEASIBILITY_GATE_NOTE_2026-05-05.md"
    ),
    "fresh_artifact_literature_route_review": (
        "docs/YT_PR230_FRESH_ARTIFACT_LITERATURE_ROUTE_REVIEW_NOTE_2026-05-05.md"
    ),
    "schur_abc_definition_attempt": (
        "docs/YT_PR230_SCHUR_ABC_DEFINITION_DERIVATION_ATTEMPT_NOTE_2026-05-05.md"
    ),
}

FUTURE_ARTIFACTS = {
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "matrix_spectral_measure_rows": (
        "outputs/yt_pr230_matrix_spectral_source_higgs_rows_2026-05-05.json"
    ),
    "neutral_rank_one_certificate": (
        "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-05.json"
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


def literature_exercise() -> list[dict[str, Any]]:
    return [
        {
            "family": "FMS / gauge-invariant Higgs spectroscopy",
            "sources": [
                "Frohlich-Morchio-Strocchi 1981 IHES preprint: https://archives.ihes.fr/document/P_81_12.pdf",
                "Maas-Sondenheimer 2020: https://arxiv.org/abs/2009.06671",
                "Fradkin-Shenker 1979: https://www.osti.gov/biblio/6248890",
            ],
            "bridge_question": "Can gauge-invariant Higgs language identify current PR230 O_s with O_H?",
            "finding": (
                "Useful physical language, but conditional on an EW/Higgs action "
                "and a gauge-invariant composite operator. It does not supply "
                "the current PR230 h-source or source-overlap identity."
            ),
            "route_status": "conditional-support",
            "next_positive_artifact": "same-source EW/Higgs action certificate or canonical O_H certificate",
        },
        {
            "family": "Matrix-valued Herglotz / matrix moment problem",
            "sources": [
                "Gesztesy-Tsekanovskii matrix Herglotz functions: https://arxiv.org/abs/funct-an/9712004",
                "Lopez-Rodriguez matrix moment Nevanlinna parametrization: https://www.mscand.dk/article/view/14340",
            ],
            "bridge_question": "Does exact source spectral data determine C_sH/C_HH?",
            "finding": (
                "No. Source-only C_ss is one marginal entry of a matrix-valued "
                "spectral measure. Off-diagonal and HH entries require either "
                "the second operator or extra constraints."
            ),
            "route_status": "no-go for source-only; exact-support for future two-source rows",
            "next_positive_artifact": "2x2 matrix spectral measure rows for O_s and O_H",
        },
        {
            "family": "Minimal realization / Ho-Kalman system identification",
            "sources": [
                "Ho-Kalman 1966 NASA record: https://ntrs.nasa.gov/citations/19670049337",
            ],
            "bridge_question": "Can input-output data fix the hidden scalar coordinate?",
            "finding": (
                "Minimal realizations are coordinate-free up to similarity. "
                "This maps directly to the PR230 source-coordinate ambiguity: "
                "source-only transfer data can identify a realization class, "
                "not the canonical Higgs coordinate."
            ),
            "route_status": "no-go for coordinate identity; support for multi-output response route",
            "next_positive_artifact": "joint top/W/H response rows with observability/rank certificate",
        },
        {
            "family": "Phase retrieval / latent-variable identifiability",
            "sources": [
                "Grohs-Koppensteiner-Rathmair SIAM Review 2020: https://epubs.siam.org/doi/10.1137/19M1256865",
                "Allman-Matias-Rhodes latent identifiability: https://arxiv.org/abs/0809.5032",
            ],
            "bridge_question": "Can a hidden overlap be inferred from one class of marginal measurements?",
            "finding": (
                "Generally no. These literatures clarify the need for masks, "
                "views, or conditional-independence structure. The PR230 analog "
                "is a need for non-source rows such as C_sH/C_HH or W/Z output."
            ),
            "route_status": "assumption stress / experimental design guidance",
            "next_positive_artifact": "additional independent view: O_H, W/Z, or neutral projector row",
        },
        {
            "family": "Krein-Rutman / Perron-Frobenius for positive semigroups",
            "sources": [
                "Fonte Sanchez-Gabriel-Mischler 2023: https://arxiv.org/abs/2305.06652",
            ],
            "bridge_question": "Can uniqueness of the neutral scalar state remove the O_H overlap ambiguity?",
            "finding": (
                "Potentially the best derivation-preferred route. If a "
                "current-surface neutral scalar transfer operator is "
                "positivity improving on a certified cone, the first scalar "
                "eigenvector can be unique. Current PR230 lacks the cone, "
                "irreducibility, and primitive certificate."
            ),
            "route_status": "high-value open derivation route",
            "next_positive_artifact": "neutral scalar primitive-cone / positivity-improving certificate",
        },
        {
            "family": "Tannaka-Krein / Doplicher-Roberts reconstruction",
            "sources": [
                "Doplicher-Roberts Annals 1989: https://annals.math.princeton.edu/1989/130-1/p03",
                "Doplicher-Roberts compact group duality: https://link.springer.com/article/10.1007/BF01388849",
            ],
            "bridge_question": "Can charged field/Higgs structure be reconstructed from observables?",
            "finding": (
                "Conceptually relevant but too large for immediate PR230. "
                "It reconstructs symmetry/field structure from a rich observable "
                "category, not from current source-only scalar rows."
            ),
            "route_status": "long-horizon reconstruction route",
            "next_positive_artifact": "explicit current-surface tensor category/fiber functor data",
        },
        {
            "family": "Holonomic D-modules / Picard-Fuchs / creative telescoping",
            "sources": [
                "Zeilberger holonomic systems: https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimhtml/holonomic.html",
                "Mueller-Stach-Weinzierl-Zayadeh Picard-Fuchs: https://arxiv.org/abs/1212.4389",
            ],
            "bridge_question": "Can PR541-style exact math compute the bridge?",
            "finding": (
                "It can compute rows after Z(beta,s,h) is defined. It cannot "
                "define h, O_H, kappa_s, or the source-Higgs identity."
            ),
            "route_status": "tool after object definition; blocked now",
            "next_positive_artifact": "defined two-source finite-volume functional",
        },
        {
            "family": "Prony / sparse moment reconstruction",
            "sources": [
                "Kunis-Peter-Roemer-von der Ohe multivariate Prony: https://www.sciencedirect.com/science/article/pii/S0024379515006187",
            ],
            "bridge_question": "Can exact finite-shell moments identify pole data?",
            "finding": (
                "Can reconstruct a finite sparse measure if finite-support "
                "and separation assumptions are certified. Current PR230 has "
                "finite prefixes, not an exact finite-support theorem."
            ),
            "route_status": "conditional-support for scalar-LSZ only",
            "next_positive_artifact": "finite-rank Stieltjes/moment certificate or threshold theorem",
        },
    ]


def assumption_exercise() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "A same-source label fixes the physical Higgs coordinate.",
            "stress_result": "false on current surface",
            "why": "common source rescalings cancel, but sector-overlap ratios can still vary",
            "repair": "derive k_top/k_gauge=1 or measure a joint top-W/H response identity",
        },
        {
            "assumption": "Exact Z(s,0) or C_ss determines C_sH and C_HH.",
            "stress_result": "false",
            "why": "matrix spectral measures with identical ss marginal can have different off-diagonal entries",
            "repair": "define O_H and measure/derive the 2x2 matrix-valued spectral rows",
        },
        {
            "assumption": "FMS lets us write O_H without an EW/Higgs action on PR230.",
            "stress_result": "false",
            "why": "FMS is an operator expansion after a gauge-Higgs theory and composite are supplied",
            "repair": "same-source EW/Higgs action certificate or independent canonical O_H theorem",
        },
        {
            "assumption": "Holonomic/Picard-Fuchs methods can replace the missing operator definition.",
            "stress_result": "false",
            "why": "they compute derivatives of a defined functional; they do not choose the h source",
            "repair": "first define Z(beta,s,h), then use holonomic/tensor contraction",
        },
        {
            "assumption": "One neutral scalar pole is automatic from Cl(3)/Z3 symmetry.",
            "stress_result": "unproved",
            "why": "symmetry labels do not exclude orthogonal neutral scalar admixture or top coupling",
            "repair": "primitive cone / positivity-improving / rank-one neutral scalar theorem",
        },
        {
            "assumption": "The v input fixes the source-Higgs normalization.",
            "stress_result": "false",
            "why": "v is a substrate input for y_t computation, not a certificate that O_s=O_H",
            "repair": "source-Higgs Gram purity or W/Z gauge-normalized response",
        },
        {
            "assumption": "Invariant-ring uniqueness of H dagger H closes O_s=O_H.",
            "stress_result": "conditional only",
            "why": "unique invariant exists after a same-surface Higgs doublet is supplied",
            "repair": "derive the Higgs doublet/action from PR230 surface before using invariant theory",
        },
        {
            "assumption": "Tannaka/DR reconstruction can be used with current scalar rows.",
            "stress_result": "false now",
            "why": "reconstruction needs a rich observable tensor category, not one source marginal",
            "repair": "build category-level charge/intertwiner/fiber-functor data or drop this route",
        },
        {
            "assumption": "Finite moment prefixes are enough for scalar-LSZ determinacy.",
            "stress_result": "false",
            "why": "Prony/stieltjes routes need finite-rank, separation, or asymptotic authority",
            "repair": "finite-rank moment certificate or threshold/FV/IR theorem",
        },
        {
            "assumption": "A measured y_t-compatible number can select the bridge.",
            "stress_result": "forbidden",
            "why": "observed top/y_t targets would be fitted selectors, not derivation inputs",
            "repair": "only use rows derived/measured on the current Cl(3)/Z3 surface",
        },
    ]


def route_ranking() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "route": "multi-output physical response",
            "target": "top + W/Z or O_H rows on same ensemble",
            "why_best": "turns hidden overlap into an observed covariance/ratio instead of an assumed identity",
            "blocking_artifact": "production W/Z or source-Higgs rows",
        },
        {
            "rank": 2,
            "route": "positivity-improving neutral scalar rank-one theorem",
            "target": "primitive cone and irreducible transfer operator in neutral scalar sector",
            "why_best": "derivation-preferred path that could make source-only pole data sufficient",
            "blocking_artifact": "current-surface cone, positivity, irreducibility certificate",
        },
        {
            "rank": 3,
            "route": "same-source EW/Higgs action then invariant/FMS O_H",
            "target": "derive EW/Higgs action tied to the PR230 source coordinate",
            "why_best": "most direct O_H construction once the action is real",
            "blocking_artifact": "same-source EW action certificate",
        },
        {
            "rank": 4,
            "route": "matrix-valued spectral measure",
            "target": "2x2 Stieltjes/Herglotz rows for O_s and O_H",
            "why_best": "mathematically exact acceptance framework for C_sH/C_HH",
            "blocking_artifact": "O_H operator and h source",
        },
        {
            "rank": 5,
            "route": "Tannaka/DR reconstruction",
            "target": "reconstruct charged field/Higgs structure from observable category",
            "why_best": "deepest possible reconstruction route",
            "blocking_artifact": "far more category data than PR230 currently has",
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_alpha_lm_plaquette_u0_or_rconn": False,
        "set_kappa_s_equal_one": False,
        "defined_O_H_by_name_only": False,
        "treated_literature_as_bridge_proof": False,
        "claimed_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 missing bridge literature + assumption exercises")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENT_CERTIFICATES.items()}
    texts = {name: read_rel(path) for name, path in TEXT_SURFACES.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}
    literature = literature_exercise()
    assumptions = assumption_exercise()
    ranking = route_ranking()
    firewall = forbidden_firewall()

    no_forbidden_imports = all(value is False for value in firewall.values())
    current_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    current_two_source_absent = (
        parents["holonomic_source_response_gate"].get(
            "two_source_functional_current_surface_defined"
        )
        is False
        and future_presence["source_higgs_rows"] is False
    )
    source_only_blocked = (
        "source-only pole data do not determine" in texts[
            "source_functional_lsz_identifiability"
        ]
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    math_tools_are_post_definition = (
        "after the object being computed is defined" in texts["schur_abc_definition_attempt"]
        and parents["holonomic_source_response_gate"].get("proposal_allowed") is False
    )
    literature_has_nonphysics_math = {
        row["family"]
        for row in literature
        if any(
            key in row["family"]
            for key in (
                "Herglotz",
                "Ho-Kalman",
                "Phase retrieval",
                "Krein-Rutman",
                "Tannaka",
                "Holonomic",
                "Prony",
            )
        )
    }
    assumptions_all_have_repairs = all(row.get("repair") for row in assumptions)
    ranking_selects_physical_or_rank_one_first = (
        ranking[0]["route"] == "multi-output physical response"
        and ranking[1]["route"] == "positivity-improving neutral scalar rank-one theorem"
    )
    retained_route_open = parents["retained_closure_route"].get("proposal_allowed") is False
    assembly_gate_open = (
        parents["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("literature-exercise-has-eight-families", len(literature) == 8, str(len(literature)))
    report("nonphysics-math-covered", len(literature_has_nonphysics_math) >= 6, str(sorted(literature_has_nonphysics_math)))
    report("assumption-exercise-has-ten-tests", len(assumptions) == 10, str(len(assumptions)))
    report("assumptions-have-repair-targets", assumptions_all_have_repairs, "repair field populated")
    report("current-oh-absent", current_oh_absent, parent_statuses["canonical_higgs_operator_gate"])
    report("current-two-source-functional-absent", current_two_source_absent, parent_statuses["holonomic_source_response_gate"])
    report("source-only-bridge-blocked", source_only_blocked, parent_statuses["source_functional_lsz_identifiability"])
    report("math-tools-post-definition-only", math_tools_are_post_definition, parent_statuses["schur_abc_definition_attempt"])
    report("route-ranking-selects-response-and-rank-one", ranking_selects_physical_or_rank_one_first, str([row["route"] for row in ranking[:2]]))
    report("retained-route-still-open", retained_route_open, parent_statuses["retained_closure_route"])
    report("assembly-gate-still-open", assembly_gate_open, parent_statuses["full_positive_closure_assembly_gate"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    exercise_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and len(literature) == 8
        and len(literature_has_nonphysics_math) >= 6
        and len(assumptions) == 10
        and assumptions_all_have_repairs
        and current_oh_absent
        and current_two_source_absent
        and source_only_blocked
        and math_tools_are_post_definition
        and ranking_selects_physical_or_rank_one_first
        and retained_route_open
        and assembly_gate_open
        and no_forbidden_imports
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / targeted literature and assumption exercises "
            "complete; missing O_s/O_sp-to-O_H bridge remains open"
        ),
        "conditional_surface_status": (
            "The literature suggests two serious positive routes: measure "
            "multi-output same-source rows, or derive a positivity-improving "
            "rank-one neutral scalar theorem. Both require new current-surface artifacts."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The exercises identify route families and expose assumptions; they "
            "do not supply O_H, h-source, C_sH/C_HH, W/Z response rows, or a "
            "rank-one neutral scalar theorem."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exercise_passed": exercise_passed,
        "literature_exercise": literature,
        "assumption_questioning_exercise": assumptions,
        "route_ranking": ranking,
        "future_artifact_presence": future_presence,
        "parent_certificates": PARENT_CERTIFICATES,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define y_t_bare",
            "does not use H_unit or yt_ward_identity",
            "does not use observed y_t/top mass, alpha_LM, plaquette, u0, or R_conn",
            "does not identify O_s or O_sp with O_H",
            "does not treat any literature source as a current-surface bridge theorem",
        ],
        "exact_next_action": (
            "Pursue either the measured multi-output route (same-source W/Z or "
            "O_H rows with covariance/Gram purity) or the derivation-preferred "
            "rank-one route (primitive cone plus positivity-improving neutral "
            "scalar transfer theorem). Holonomic/D-module/tensor tools become "
            "useful only after Z(beta,s,h) or equivalent row definitions exist."
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
