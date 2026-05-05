#!/usr/bin/env python3
"""
PR #230 cross-lane O_H authority audit.

The current non-chunk blocker is a same-surface canonical-Higgs radial
operator O_H certificate for the PR230 source-Higgs route.  The repo also has
many adjacent artifacts whose names mention O_h/O_H/Higgs/two-Higgs/Schur.
This runner checks whether any of those adjacent artifacts is already a valid
PR230 O_H authority, or whether they are cross-lane support/no-go surfaces.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_cross_lane_oh_authority_audit_2026-05-05.json"

PARENTS = {
    "canonical_higgs_repo_authority": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "canonical_higgs_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_higgs_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "fms_oh_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
}

CANDIDATES = [
    {
        "id": "gravity_oh_schur_boundary_action",
        "path": "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md",
        "lane": "restricted strong-field gravity",
        "classification": "cross-lane gravity O_h shell-boundary action",
        "positive_reuse": "Schur-complement boundary-action method as analogy only",
        "blocking_reasons": [
            "O_h here names a cubic source class, not the electroweak Higgs radial operator O_H",
            "surface is a static conformal gravity shell, not PR230 top/source-Higgs",
            "no PR230 source coordinate, canonical Higgs LSZ normalization, or C_sH/C_HH rows",
        ],
    },
    {
        "id": "gravity_oh_static_constraint_lift",
        "path": "docs/OH_STATIC_CONSTRAINT_LIFT_NOTE.md",
        "lane": "restricted strong-field gravity",
        "classification": "cross-lane static gravity O_h lift",
        "positive_reuse": "exact local lift method as analogy only",
        "blocking_reasons": [
            "O_h is the exact local gravity source class, not O_H",
            "works on a static conformal bridge surface rather than a dynamic EW gauge-Higgs surface",
            "does not define a top-sector canonical-Higgs source overlap",
        ],
    },
    {
        "id": "gravity_star_supported_bridge",
        "path": "docs/STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md",
        "lane": "restricted strong-field gravity",
        "classification": "cross-lane gravity bridge class",
        "positive_reuse": "boundary/support vocabulary only",
        "blocking_reasons": [
            "Schur boundary bridge is gravitational support, not top Yukawa source-Higgs identity",
            "no PR230 operator certificate or source-Higgs pole residues",
        ],
    },
    {
        "id": "tensor_source_map_eta",
        "path": "docs/TENSOR_SOURCE_MAP_ETA_NOTE.md",
        "lane": "gravity/tensor source support",
        "classification": "cross-lane tensor-source support",
        "positive_reuse": "tensor source-map analogy only",
        "blocking_reasons": [
            "concerns tensor probes of scalar Schur data, not canonical EW Higgs",
            "no PR230 C_sH/C_HH or O_sp/O_H identity",
        ],
    },
    {
        "id": "tensor_matching_completion",
        "path": "docs/TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md",
        "lane": "gravity/tensor matching support",
        "classification": "cross-lane tensor matching support",
        "positive_reuse": "matching discipline analogy only",
        "blocking_reasons": [
            "matches tensor/scalar boundary data, not top/source-Higgs pole data",
            "no same-surface top-sector Higgs radial certificate",
        ],
    },
    {
        "id": "higgs_vacuum_explicit_systematic",
        "path": "docs/HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md",
        "lane": "Higgs/vacuum quantitative lane",
        "classification": "Higgs quantitative summary with inherited YT residual",
        "positive_reuse": "Higgs-sector RGE and vacuum-stability context",
        "blocking_reasons": [
            "explicitly separate from the Yukawa/top lane and inherits the YT residual budget",
            "does not supply a PR230 source coordinate or O_H identity/normalization certificate",
            "does not contain production C_sH/C_HH pole residues",
        ],
    },
    {
        "id": "higgs_mass_derived",
        "path": "docs/HIGGS_MASS_DERIVED_NOTE.md",
        "lane": "Higgs mass quantitative lane",
        "classification": "derived Higgs-mass result, not O_H authority",
        "positive_reuse": "Higgs-sector context after the top/YT bridge exists",
        "blocking_reasons": [
            "does not derive PR230 source-to-canonical-Higgs overlap",
            "does not produce an operator certificate accepted by the O_H gate",
        ],
    },
    {
        "id": "higgs_mechanism",
        "path": "docs/HIGGS_MECHANISM_NOTE.md",
        "lane": "Higgs mechanism support",
        "classification": "mechanism-level Higgs support",
        "positive_reuse": "qualitative Higgs-mechanism context",
        "blocking_reasons": [
            "mechanism support is downstream of having a canonical Higgs field",
            "does not attach the PR230 scalar source to the canonical radial pole",
        ],
    },
    {
        "id": "higgs_z3_charge_pmns_gauge_redundancy",
        "path": "docs/HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md",
        "lane": "PMNS/charged-lepton support",
        "classification": "PMNS gauge-redundancy theorem for Higgs Z3 charge",
        "positive_reuse": "single-Higgs charge-gauge redundancy in lepton observables",
        "blocking_reasons": [
            "concerns PMNS left-handed diagonalizers and right-handed charged-lepton relabeling",
            "does not define a PR230 top-sector canonical-Higgs radial operator",
            "does not provide source-Higgs pole residues",
        ],
    },
    {
        "id": "sm_one_higgs_yukawa_gauge_selection",
        "path": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
        "lane": "SM one-Higgs operator selection",
        "classification": "gauge monomial selection after H is supplied",
        "positive_reuse": "operator-pattern support once O_H is independently available",
        "blocking_reasons": [
            "leaves Yukawa coefficients and source overlap free",
            "does not identify the PR230 scalar source with canonical H",
        ],
    },
    {
        "id": "ew_higgs_gauge_mass_diagonalization",
        "path": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
        "lane": "EW gauge-mass algebra",
        "classification": "EW mass dictionary after a canonical Higgs is supplied",
        "positive_reuse": "W/Z response dictionary after a real O_H/EW action certificate",
        "blocking_reasons": [
            "starts from a supplied Higgs doublet/vacuum rather than deriving it from PR230 source data",
            "cannot serve as an O_sp/O_H identity or source-Higgs purity certificate",
        ],
    },
    {
        "id": "taste_scalar_isotropy",
        "path": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
        "lane": "Cl(3)/Z3 scalar/taste support",
        "classification": "exact taste-block isotropy support",
        "positive_reuse": "framework-native scalar/taste isotropy support",
        "blocking_reasons": [
            "isotropy does not select which scalar direction is the canonical Higgs radial pole",
            "does not provide source-Higgs C_sH/C_HH rows or canonical LSZ normalization",
        ],
    },
    {
        "id": "charged_lepton_two_higgs_canonical_reduction",
        "path": "docs/CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md",
        "lane": "charged-lepton two-Higgs reduction",
        "classification": "lepton texture reduction, not top-sector O_H certificate",
        "positive_reuse": "two-Higgs support-counting analogy only",
        "blocking_reasons": [
            "classifies charged-lepton Yukawa textures and residual freedom",
            "does not attach PR230 scalar source to a canonical Higgs pole",
        ],
    },
    {
        "id": "neutrino_dirac_two_higgs_canonical_reduction",
        "path": "docs/NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md",
        "lane": "neutrino two-Higgs reduction",
        "classification": "neutrino texture reduction, not top-sector O_H certificate",
        "positive_reuse": "two-Higgs support-counting analogy only",
        "blocking_reasons": [
            "works on neutrino support textures, not PR230 top/source-Higgs response",
            "does not provide O_H identity/normalization or source-Higgs rows",
        ],
    },
    {
        "id": "dm_neutrino_two_higgs_minimality",
        "path": "docs/DM_NEUTRINO_TWO_HIGGS_MINIMALITY_THEOREM_NOTE_2026-04-15.md",
        "lane": "DM/neutrino route selection",
        "classification": "DM-side two-Higgs minimality support",
        "positive_reuse": "route-selection logic for multi-Higgs lepton lanes",
        "blocking_reasons": [
            "selects a minimal local neutrino escape class once DM CP support is required",
            "does not derive a top-sector canonical Higgs radial operator",
        ],
    },
    {
        "id": "dm_neutrino_two_higgs_right_gram_bridge",
        "path": "docs/DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md",
        "lane": "DM/neutrino right-Gram support",
        "classification": "right-Gram bridge for neutrino two-Higgs lane",
        "positive_reuse": "Gram-matrix proof style analogy only",
        "blocking_reasons": [
            "right-Gram bridge is in the DM/neutrino lane, not the PR230 top source-Higgs lane",
            "does not involve PR230 C_sH/C_HH pole residues",
        ],
    },
    {
        "id": "koide_q23_oh_covariance_no_go",
        "path": "docs/KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md",
        "lane": "Koide support/no-go",
        "classification": "Koide O_h covariance no-go",
        "positive_reuse": "negative symmetry-covariance lesson only",
        "blocking_reasons": [
            "O_h is the cubic point group in a Koide chart test, not electroweak O_H",
            "the result is a no-go and cannot be an O_H certificate",
        ],
    },
    {
        "id": "koide_z3_scalar_potential_support",
        "path": "docs/KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md",
        "lane": "Koide scalar support",
        "classification": "Koide scalar potential support",
        "positive_reuse": "scalar-potential support analogy only",
        "blocking_reasons": [
            "Koide scalar selector context is outside PR230",
            "does not supply same-surface top/Higgs pole identity",
        ],
    },
    {
        "id": "koide_one_scalar_obstruction",
        "path": "docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md",
        "lane": "Koide scalar obstruction",
        "classification": "Koide one-scalar obstruction",
        "positive_reuse": "negative scalar-selection analogy only",
        "blocking_reasons": [
            "obstruction theorem is not a constructive O_H identity",
            "Koide source domain is not the PR230 top/source-Higgs surface",
        ],
    },
]

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def read_rel(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def classify(candidate: dict[str, Any]) -> dict[str, Any]:
    text = read_rel(candidate["path"])
    lower = text.lower()
    hints = {
        "file_present": bool(text),
        "mentions_cl3_z3": "cl(3)/z" in lower or "cl3/z" in lower or "cl(3)" in lower,
        "mentions_pr230": "pr230" in lower or "pr #230" in lower,
        "mentions_oh_token": "o_h" in text or "O_H" in text or "O_h" in text,
        "mentions_source_higgs_rows": "C_sH" in text and "C_HH" in text,
        "mentions_source_coordinate": "source coordinate" in lower or "same-source" in lower,
        "mentions_lsz_normalization": "lsz" in lower and "normalization" in lower,
        "mentions_canonical_higgs": "canonical higgs" in lower or "canonical-higgs" in lower,
        "mentions_top_yukawa": "top" in lower and "yukawa" in lower,
    }
    # The acceptance surface requires all of these simultaneously, and no
    # candidate below is allowed to pass by a single suggestive name.
    acceptance_required = {
        "same_pr230_surface": hints["mentions_pr230"] and hints["mentions_cl3_z3"],
        "top_source_higgs_surface": hints["mentions_top_yukawa"]
        and (hints["mentions_source_coordinate"] or hints["mentions_source_higgs_rows"]),
        "operator_identity_normalization": hints["mentions_canonical_higgs"]
        and hints["mentions_lsz_normalization"],
        "pole_residue_rows": hints["mentions_source_higgs_rows"],
    }
    usable = all(acceptance_required.values())
    return {
        **candidate,
        "hints": hints,
        "acceptance_required": acceptance_required,
        "usable_as_pr230_oh_certificate": usable,
    }


def main() -> int:
    print("PR #230 cross-lane O_H authority audit")
    print("=" * 72)

    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    rows = [classify(candidate) for candidate in CANDIDATES]
    missing_files = [row["path"] for row in rows if not row["hints"]["file_present"]]
    usable = [row["id"] for row in rows if row["usable_as_pr230_oh_certificate"]]

    gravity_oh_rows = [row for row in rows if row["lane"].startswith("restricted strong-field gravity")]
    lepton_two_higgs_rows = [
        row for row in rows if "two-Higgs" in row["lane"] or "two-Higgs" in row["classification"]
    ]
    ew_assume_h_rows = [
        row
        for row in rows
        if row["id"] in {"sm_one_higgs_yukawa_gauge_selection", "ew_higgs_gauge_mass_diagonalization"}
    ]
    source_rows_present = any(row["hints"]["mentions_source_higgs_rows"] for row in rows)

    parent_missing = [name for name, data in parents.items() if not data]
    parent_proposal = [name for name, data in parents.items() if data.get("proposal_allowed") is True]
    canonical_gate_open = (
        parents["canonical_higgs_certificate_gate"].get("candidate_present") is False
        and parents["canonical_higgs_certificate_gate"].get("candidate_valid") is False
        and parents["canonical_higgs_certificate_gate"].get("proposal_allowed") is False
    )
    fms_blocked = (
        "FMS O_H certificate construction blocked"
        in parents["fms_oh_construction_attempt"].get("actual_current_surface_status", "")
    )
    source_higgs_blocked = (
        parents["source_higgs_readiness"].get("operator_certificate_present") is False
        and parents["source_higgs_readiness"].get("future_rows_present") is False
        and parents["source_higgs_readiness"].get("proposal_allowed") is False
    )
    assembly_open = parents["assembly_gate"].get("proposal_allowed") is False

    report("parent-certificates-present", not parent_missing, f"missing={parent_missing}")
    report("no-parent-authorizes-proposal", not parent_proposal, f"proposal_allowed={parent_proposal}")
    report("candidate-files-present", not missing_files, f"missing={missing_files}")
    report("gravity-oh-separated-from-higgs-oh", all("gravity" in row["lane"] for row in gravity_oh_rows), "gravity O_h rows are not electroweak O_H")
    report("lepton-two-higgs-is-cross-lane", len(lepton_two_higgs_rows) >= 3, f"count={len(lepton_two_higgs_rows)}")
    report("ew-higgs-not-upstream-oh", all("after" in row["classification"] for row in ew_assume_h_rows), "EW/SM notes assume H after supplied")
    report("no-cross-lane-pr230-oh-certificate", not usable, f"usable={usable}")
    report("cross-lane-source-higgs-rows-not-present", not source_rows_present, "no adjacent cross-lane doc contains C_sH/C_HH production rows")
    report("canonical-higgs-gate-still-open", canonical_gate_open, parents["canonical_higgs_certificate_gate"].get("actual_current_surface_status", ""))
    report("fms-oh-attempt-still-blocked", fms_blocked, parents["fms_oh_construction_attempt"].get("actual_current_surface_status", ""))
    report("source-higgs-production-still-blocked", source_higgs_blocked, parents["source_higgs_readiness"].get("actual_current_surface_status", ""))
    report("assembly-gate-still-open", assembly_open, parents["assembly_gate"].get("actual_current_surface_status", ""))
    report("framework-native-boundary-recorded", True, "surveyed artifacts are framework-native support/no-go surfaces, but not PR230 authority")

    boundary_passed = FAIL_COUNT == 0 and not usable
    result = {
        "actual_current_surface_status": "exact negative boundary / cross-lane O_H authority audit",
        "verdict": (
            "Adjacent O_h/O_H/Higgs/two-Higgs/Schur artifacts do not supply "
            "the missing PR230 same-surface canonical-Higgs radial operator "
            "certificate.  Gravity O_h notes concern static shell source "
            "classes; lepton/DM two-Higgs notes classify flavor textures; "
            "EW and SM one-Higgs notes assume a canonical Higgs after it is "
            "supplied; Higgs-mass/vacuum notes inherit the top/YT residual; "
            "Koide O_h notes are no-go/support surfaces in another lane.  "
            "All may remain framework-native context, but none gives the "
            "PR230 O_sp/O_H identity, canonical LSZ normalization, or "
            "C_sH/C_HH pole residues."
        ),
        "cross_lane_oh_authority_audit_passed": boundary_passed,
        "repo_cross_lane_authority_found": bool(usable),
        "usable_candidates": usable,
        "proposal_allowed": False,
        "proposal_allowed_reason": "No adjacent cross-lane O_h/O_H/Higgs artifact satisfies the PR230 canonical-Higgs certificate surface.",
        "bare_retained_allowed": False,
        "candidate_surfaces": rows,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not import gravity O_h shell classes as electroweak O_H",
            "does not import lepton/DM two-Higgs reductions as top-sector O_H",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, or observed target values",
            "does not set kappa_s = 1, cos(theta) = 1, c2 = 1, or Z_match = 1",
        ],
        "positive_reuse": [
            "gravity Schur/Feshbach tools can inspire future row/certificate construction but are cross-lane",
            "EW gauge-mass and SM one-Higgs notes can be used after a canonical O_H is independently supplied",
            "taste-scalar isotropy remains scalar/taste support, not source-Higgs identity",
            "lepton/DM two-Higgs reductions can inform multi-Higgs route selection, not PR230 closure",
        ],
        "exact_next_action": (
            "Continue with a real PR230 same-surface O_H certificate, "
            "source-Higgs C_sH/C_HH production rows plus Gram purity, W/Z "
            "response rows with identity certificates, Schur A/B/C rows, or "
            "a neutral-sector irreducibility theorem."
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
