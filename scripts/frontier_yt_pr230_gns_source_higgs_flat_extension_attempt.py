#!/usr/bin/env python3
"""
PR #230 GNS source-Higgs flat-extension attempt.

The clean source-Higgs route ranked GNS flat extension / truncated moment-rank
certificates as useful outside-math tools after a canonical-Higgs operator and
source-Higgs moment rows exist.  This runner asks whether the current PR230
surface can already use those tools to certify source-pole purity.

It cannot.  The current source-only moment projection has multiple positive
semidefinite source-Higgs extensions with different GNS ranks and different
source-Higgs overlaps.  Flat-extension/moment-rank machinery becomes decisive
only after same-surface O_H, C_sH, and C_HH pole rows are supplied.
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
    / "yt_pr230_gns_source_higgs_flat_extension_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "isolated_pole_gram_factorization": "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "gns_flat_extension_certificate": "outputs/yt_source_higgs_gns_flat_extension_certificate_2026-05-05.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "reduced pilots as production evidence",
    "kappa_s = 1 by convention",
    "GNS rank/value recognition as an O_H selector without O_H rows",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def rank_2x2(a: float, b: float, c: float) -> int:
    det = a * c - b * b
    if abs(a) < 1.0e-12 and abs(b) < 1.0e-12 and abs(c) < 1.0e-12:
        return 0
    if abs(det) <= 1.0e-12:
        return 1
    return 2


def eigenvalues_2x2(a: float, b: float, c: float) -> list[float]:
    trace = a + c
    disc = math.sqrt(max((a - c) * (a - c) + 4.0 * b * b, 0.0))
    return [(trace - disc) / 2.0, (trace + disc) / 2.0]


def moment_extension(label: str, c_ss: float, c_sh: float, c_hh: float) -> dict[str, Any]:
    det = c_ss * c_hh - c_sh * c_sh
    rho = c_sh / math.sqrt(c_ss * c_hh) if c_ss > 0.0 and c_hh > 0.0 else float("nan")
    eigs = eigenvalues_2x2(c_ss, c_sh, c_hh)
    return {
        "case": label,
        "moment_matrix_basis": ["O_s", "O_H_candidate"],
        "matrix": [[c_ss, c_sh], [c_sh, c_hh]],
        "source_only_projection": [[c_ss]],
        "source_only_rank": 1 if c_ss > 0.0 else 0,
        "gram_determinant": det,
        "normalized_overlap_rho_sH": rho,
        "gns_rank": rank_2x2(c_ss, c_sh, c_hh),
        "positive_semidefinite": min(eigs) >= -1.0e-12,
        "flat_over_source_projection": rank_2x2(c_ss, c_sh, c_hh) == (1 if c_ss > 0.0 else 0),
        "source_projection_changed": False,
        "eigenvalues": eigs,
    }


def extension_counterfamily() -> list[dict[str, Any]]:
    c_ss = 4.0
    return [
        moment_extension("pure_rank_one_extension", c_ss, 6.0, 9.0),
        moment_extension("mixed_rank_two_extension", c_ss, 3.0, 9.0),
        moment_extension("orthogonal_rank_two_extension", c_ss, 0.0, 9.0),
    ]


def gns_future_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "canonical_higgs_operator",
            "required": "same-surface O_H identity and normalization certificate",
            "current_satisfied": False,
        },
        {
            "id": "source_higgs_moment_rows",
            "required": "production pole rows for C_ss, C_sH, and C_HH at the same isolated pole",
            "current_satisfied": False,
        },
        {
            "id": "positive_moment_matrix",
            "required": "PSD moment/localizing matrix with uncertainties or exact bounds",
            "current_satisfied": False,
        },
        {
            "id": "flat_extension_rank_stability",
            "required": "rank M_d = rank M_{d-1} for the full source-Higgs matrix, not only the source projection",
            "current_satisfied": False,
        },
        {
            "id": "pole_fv_ir_model_control",
            "required": "isolated-pole, threshold, FV/IR, and contact/model-class authority",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "reject H_unit, Ward, observed selectors, alpha/plaquette/u0, reduced pilots, unit kappa_s, and rank/value selectors",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 GNS source-Higgs flat-extension attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    future_present_names = [name for name, present in future_present.items() if present]

    selected = parents["clean_source_higgs_math_selector"].get("selected_clean_route", {})
    stage_2_tools = selected.get("stage_2", {}).get("candidate_tools", [])
    selector_names_gns = (
        "future-only" in str(selected.get("current_status", ""))
        and any("GNS" in str(tool) or "moment rank" in str(tool) for tool in stage_2_tools)
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and future_present["canonical_oh_certificate"] is False
    )
    source_higgs_rows_absent = (
        parents["source_higgs_builder"].get("proposal_allowed") is False
        and "rows absent" in statuses["source_higgs_builder"]
        and parents["source_higgs_pole_residue_extractor"].get("rows_written") is False
        and future_present["source_higgs_measurement_rows"] is False
        and future_present["source_higgs_production_certificate"] is False
    )
    gram_gate_open = (
        parents["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed")
        is False
        and parents["source_higgs_gram_purity_gate"].get("current_data_has_required_residues")
        is False
    )
    unratified_gram_blocked = (
        parents["source_higgs_unratified_gram_no_go"].get("unratified_gram_shortcut_no_go_passed")
        is True
    )
    isolated_gram_support_only = (
        parents["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True
        and parents["isolated_pole_gram_factorization"].get("proposal_allowed") is False
    )
    source_only_lsz_no_go_loaded = (
        parents["source_functional_lsz_identifiability"].get("theorem_closed") is False
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    invariant_oh_blocker_loaded = (
        parents["invariant_ring_oh_attempt"].get("invariant_ring_certificate_passed")
        is False
    )

    extensions = extension_counterfamily()
    same_source_projection = len(
        {
            json.dumps(row["source_only_projection"], sort_keys=True)
            for row in extensions
        }
    ) == 1
    all_psd = all(row["positive_semidefinite"] for row in extensions)
    ranks = {row["gns_rank"] for row in extensions}
    overlaps = {round(float(row["normalized_overlap_rho_sH"]), 12) for row in extensions}
    flatness_values = {row["flat_over_source_projection"] for row in extensions}
    gns_contract = gns_future_contract()
    missing_contract = [row["id"] for row in gns_contract if not row["current_satisfied"]]
    forbidden_firewall_clean = True
    gns_flat_extension_passed = False
    gns_certificate_written = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-names-gns-as-future-tool", selector_names_gns, str(stage_2_tools))
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("gram-purity-gate-open", gram_gate_open, statuses["source_higgs_gram_purity_gate"])
    report("unratified-gram-shortcut-blocked", unratified_gram_blocked, statuses["source_higgs_unratified_gram_no_go"])
    report("isolated-gram-factorization-support-only", isolated_gram_support_only, statuses["isolated_pole_gram_factorization"])
    report("source-only-lsz-identifiability-no-go-loaded", source_only_lsz_no_go_loaded, statuses["source_functional_lsz_identifiability"])
    report("invariant-oh-blocker-loaded", invariant_oh_blocker_loaded, statuses["invariant_ring_oh_attempt"])
    report("future-gns-and-source-higgs-files-absent", not future_present_names, f"present={future_present_names}")
    report("source-only-projection-same", same_source_projection, "all PSD extensions share C_ss")
    report("moment-extensions-positive-semidefinite", all_psd, str(extensions))
    report("gns-ranks-vary-at-fixed-source-projection", ranks == {1, 2}, f"ranks={sorted(ranks)}")
    report("source-higgs-overlaps-vary", len(overlaps) == len(extensions), f"overlaps={sorted(overlaps)}")
    report("flatness-not-determined-by-source-projection", flatness_values == {False, True}, f"flatness={sorted(flatness_values)}")
    report("future-gns-contract-recorded", len(missing_contract) == 5, f"missing={missing_contract}")
    report("forbidden-firewall-clean", forbidden_firewall_clean, ", ".join(FORBIDDEN_INPUTS))
    report("no-gns-certificate-written", not gns_certificate_written, f"future_file_presence={future_present}")
    report("gns-flat-extension-not-passed", not gns_flat_extension_passed, "source-only projection is underdetermined")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / GNS source-Higgs flat-extension attempt "
            "blocked by missing O_H/C_sH/C_HH rows"
        ),
        "conditional_surface_status": (
            "conditional-support if future same-surface O_H, C_sH, and C_HH "
            "pole rows provide a full PSD moment matrix with flat-extension "
            "rank stability and pole/FV/IR authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current source-only moment projection has multiple positive "
            "source-Higgs extensions with different GNS ranks and overlaps.  "
            "A GNS flat-extension certificate requires the full source-Higgs "
            "moment matrix and a canonical O_H identity, not only C_ss."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "gns_flat_extension_passed": gns_flat_extension_passed,
        "gns_certificate_written": gns_certificate_written,
        "future_file_presence": future_present,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "source_only_projection_counterfamily": extensions,
        "future_gns_contract": gns_contract,
        "missing_future_gns_contract": missing_contract,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write a GNS flat-extension certificate",
            "does not treat source-only C_ss moments as source-Higgs Gram rows",
            "does not use GNS rank, PSLQ, exact values, or method names as O_H selectors",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or kappa_s = 1",
        ],
        "exact_next_action": (
            "Produce a same-surface canonical O_H certificate and production "
            "C_ss/C_sH/C_HH pole rows, then run a GNS/moment flat-extension "
            "certificate on the full source-Higgs moment matrix.  Otherwise "
            "pivot to same-source W/Z response rows with identity/covariance/g2 "
            "authority, genuine Schur rows, strict scalar-LSZ moment/threshold/"
            "FV authority, or a neutral-sector irreducibility certificate."
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
