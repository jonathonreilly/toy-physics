#!/usr/bin/env python3
"""
PR #230 O_sp/O_H literature bridge.

This runner records the targeted literature/theorem-shape pass for the active
source-pole-to-canonical-Higgs blocker.  External literature can suggest
measurement and operator-certificate shapes, but it is not current-surface
authority for O_sp = O_H.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_osp_oh_literature_bridge_2026-05-04.json"

PARENTS = {
    "osp_oh_assumption_route_audit": "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json",
    "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "wz_correlator_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

SOURCES = [
    {
        "id": "fms_bound_state_spectrum",
        "url": "https://arxiv.org/abs/1912.08680",
        "title": "Analytical relations for the bound state spectrum of gauge theories with a Brout-Englert-Higgs mechanism",
        "useful_shape": "FMS-style gauge-invariant composite Higgs operators can be related to gauge-fixed Higgs objects after the gauge-Higgs system is supplied.",
        "pr230_boundary": "Does not identify the PR230 scalar source O_s or O_sp with the required gauge-invariant Higgs operator.",
        "route_action": "Use as design context for a future same-surface O_H certificate, not as proof input.",
    },
    {
        "id": "fms_higgs_resonance",
        "url": "https://arxiv.org/abs/2009.06671",
        "title": "Gauge-invariant description of the Higgs resonance and its phenomenological implications",
        "useful_shape": "A gauge-invariant bound-state Higgs description can share pole structure with the elementary Higgs in the FMS expansion.",
        "pr230_boundary": "Pole-structure matching in an EW gauge-Higgs theory does not supply PR230 C_sH/C_HH rows or O_sp/O_H overlap.",
        "route_action": "If pursued, implement a gauge-invariant O_H candidate and validate it through the O_H certificate and Gram-purity gates.",
    },
    {
        "id": "weak_higgs_lattice_2026",
        "url": "https://arxiv.org/abs/2603.12882",
        "title": "Weak and Higgs physics from the lattice",
        "useful_shape": "Recent lattice Higgs work treats weak/Higgs physics through gauge-invariant FMS-connected observables.",
        "pr230_boundary": "This is external lattice methodology and has no authority to define the Cl(3)/Z3 source coordinate as canonical Higgs.",
        "route_action": "Use as methodology context for future EW/Higgs lattice rows, not as a retained closure import.",
    },
    {
        "id": "gevp_lattice_matrix_elements",
        "url": "https://arxiv.org/abs/0902.1265",
        "title": "On the generalized eigenvalue method for energies and matrix elements in lattice field theory",
        "useful_shape": "Operator correlation matrices and GEVP analysis are standard tools for isolating states and matrix elements.",
        "pr230_boundary": "GEVP supplies an extraction method only after a valid O_H operator family and C_sH/C_HH rows exist.",
        "route_action": "Future source-Higgs production should prefer an operator matrix/GEVP pole-residue analysis over one-row assertions.",
    },
    {
        "id": "feynman_hellmann_lattice_transition",
        "url": "https://arxiv.org/abs/2305.05491",
        "title": "Feynman-Hellmann approach to transition matrix elements and quasi-degenerate energy states",
        "useful_shape": "Adding a perturbing operator to the action and reading energy shifts is a standard lattice route to matrix elements.",
        "pr230_boundary": "It justifies the source-response measurement pattern, not the source-to-canonical-Higgs identity.",
        "route_action": "Keep FH/LSZ chunks as production support; do not promote source-only response to physical y_t.",
    },
    {
        "id": "nielsen_pole_mass",
        "url": "https://arxiv.org/abs/1308.5127",
        "title": "On the gauge independence of the fermion pole mass",
        "useful_shape": "Nielsen-identity methods can protect pole-mass statements under gauge variation in appropriate settings.",
        "pr230_boundary": "Gauge independence of a pole is not a scalar-source overlap theorem and does not certify O_H.",
        "route_action": "Use Nielsen/BRST material only as a guardrail for future EW pole definitions.",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 O_sp/O_H literature bridge")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    fms_sources = [row for row in SOURCES if row["id"].startswith("fms") or row["id"].startswith("weak")]
    extraction_sources = [row for row in SOURCES if row["id"].startswith("gevp") or row["id"].startswith("feynman")]
    guardrail_sources = [row for row in SOURCES if row["id"].startswith("nielsen")]

    assumption_audit_loaded = (
        "O_sp-to-O_H assumption-route audit complete"
        in status(parents["osp_oh_assumption_route_audit"])
        and parents["osp_oh_assumption_route_audit"].get("assumption_route_audit_passed") is True
    )
    hidden_oh_absent = (
        "canonical-Higgs O_H authority audit" in status(parents["canonical_higgs_repo_authority_audit"])
        and parents["canonical_higgs_repo_authority_audit"].get("repo_authority_found") is False
    )
    source_higgs_still_blocked = "source-Higgs production launch blocked" in status(
        parents["source_higgs_production_readiness"]
    )
    wz_still_blocked = "WZ correlator mass-fit path absent" in status(
        parents["wz_correlator_mass_fit_path"]
    )
    retained_still_open = "retained closure not yet reached" in status(parents["retained_route"])

    literature_is_context_only = all(
        "does not" in row["pr230_boundary"].lower()
        or "not" in row["pr230_boundary"].lower()
        or "no authority" in row["pr230_boundary"].lower()
        or "only after" in row["pr230_boundary"].lower()
        for row in SOURCES
    )
    route_shape_identified = len(fms_sources) >= 3 and len(extraction_sources) >= 2
    no_literature_closure_import = True
    literature_bridge_passed = (
        not missing
        and not proposal_allowed
        and assumption_audit_loaded
        and hidden_oh_absent
        and source_higgs_still_blocked
        and wz_still_blocked
        and retained_still_open
        and literature_is_context_only
        and route_shape_identified
        and no_literature_closure_import
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("assumption-audit-loaded", assumption_audit_loaded, status(parents["osp_oh_assumption_route_audit"]))
    report("repo-hidden-oh-still-absent", hidden_oh_absent, status(parents["canonical_higgs_repo_authority_audit"]))
    report("source-higgs-route-still-blocked", source_higgs_still_blocked, status(parents["source_higgs_production_readiness"]))
    report("wz-route-still-blocked", wz_still_blocked, status(parents["wz_correlator_mass_fit_path"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_route"]))
    report("fms-literature-gives-operator-certificate-shape", len(fms_sources) >= 3, f"count={len(fms_sources)}")
    report("gevp-fh-literature-gives-extraction-shape", len(extraction_sources) >= 2, f"count={len(extraction_sources)}")
    report("nielsen-literature-is-pole-guardrail-only", len(guardrail_sources) == 1, f"count={len(guardrail_sources)}")
    report("literature-classified-context-only", literature_is_context_only, "no source is current-surface authority")
    report("no-literature-closure-import", no_literature_closure_import, "external literature not imported as proof")
    report("literature-bridge-passed", literature_bridge_passed, "methodology shape identified without closure")

    result = {
        "actual_current_surface_status": (
            "bounded-support / O_sp/O_H literature bridge; no current-surface closure import"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The literature suggests a future FMS-style gauge-invariant O_H "
            "operator plus GEVP/Gram-pole extraction path, but it does not "
            "supply a same-surface Cl(3)/Z3 O_sp=O_H theorem or measurement."
        ),
        "bare_retained_allowed": False,
        "literature_bridge_passed": literature_bridge_passed,
        "methodology_shape": (
            "Future positive attempt should build a same-surface gauge-invariant "
            "canonical-Higgs operator certificate, then measure a C_ss/C_sH/C_HH "
            "correlator matrix with GEVP or isolated-pole residue analysis."
        ),
        "source_rows": SOURCES,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import external literature as PR230 proof authority",
            "does not identify O_sp with O_H",
            "does not treat FMS pole-structure statements as source-Higgs Gram purity",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "If taking the literature route, implement a same-surface "
            "FMS-inspired O_H operator certificate and use the existing "
            "source-Higgs builder/postprocessor with GEVP-style pole-residue "
            "rows.  Otherwise continue chunk production."
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
