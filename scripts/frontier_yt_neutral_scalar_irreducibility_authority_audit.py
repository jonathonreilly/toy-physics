#!/usr/bin/env python3
"""
PR #230 neutral-scalar irreducibility authority audit.

This runner asks whether the current repository surface already contains the
missing neutral-sector irreducibility / primitive-cone certificate needed to
turn the conditional positivity-improving rank-one support theorem into an
actual PR #230 closure route.

It deliberately does not prove a new physics theorem.  It is the route-level
authority audit after the direct positivity-improving stretch attempt: if a
current certificate exists, the runner must find it by exact key; if not, the
rank-one route remains blocked until a same-surface theorem or non-source row
is supplied.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json"
)

PARENTS = {
    "positivity_improving_neutral_scalar_rank_one": (
        "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
    ),
    "neutral_scalar_positivity_improving_direct_closure": (
        "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"
    ),
    "gauge_perron_neutral_scalar_rank_one_import": (
        "outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json"
    ),
    "reflection_positivity_lsz_shortcut": (
        "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"
    ),
    "neutral_scalar_rank_one_purity_gate": (
        "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json"
    ),
    "neutral_scalar_commutant_rank_no_go": (
        "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"
    ),
    "neutral_scalar_dynamical_rank_one_closure": (
        "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"
    ),
    "neutral_scalar_top_coupling_tomography_gate": (
        "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json"
    ),
    "non_source_response_rank_repair_sufficiency": (
        "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json"
    ),
    "osp_oh_assumption_route_audit": (
        "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json"
    ),
}

EXACT_POSITIVE_KEYS = {
    "neutral_scalar_irreducibility_certificate_present": True,
    "neutral_scalar_irreducibility_theorem_passed": True,
    "primitive_cone_irreducibility_theorem_passed": True,
    "positivity_improving_certificate_present": True,
    "direct_positivity_improving_theorem_derived": True,
}

FORBIDDEN_SHORTCUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity readout",
    "observed m_t or y_t selector",
    "alpha_LM / plaquette / u0 normalization import",
    "static EW algebra as an O_H certificate",
    "reflection positivity alone",
    "gauge-vacuum Perron uniqueness imported into the neutral scalar sector",
    "finite source-only C_ss rows as Schur A/B/C rows",
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


def iter_repo_json() -> list[Path]:
    roots = [ROOT / "outputs", ROOT / ".claude" / "science" / "physics-loops"]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*.json") if path.is_file())
            files.extend(path for path in root.rglob("*.yaml") if path.is_file())
    return sorted(files)


def find_exact_positive_authority() -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in iter_repo_json():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for key, value in EXACT_POSITIVE_KEYS.items():
            json_pattern = f'"{key}": {str(value).lower()}'
            yaml_pattern = f"{key}: {str(value).lower()}"
            if json_pattern in text or yaml_pattern in text:
                hits.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "key": key,
                        "value": str(value),
                    }
                )
    return hits


def minimal_premise_contract() -> dict[str, Any]:
    return {
        "needed_certificate": "same-surface neutral scalar irreducibility / primitive-cone positivity improvement",
        "must_prove": [
            "the neutral scalar transfer sector is a single primitive cone after gauge, fermion, scalar-source, and O_H construction",
            "the source pole and certified canonical-Higgs radial operator overlap the unique lowest isolated neutral scalar pole",
            "no finite orthogonal neutral top-coupled direction survives with the same source-only rows",
            "the theorem is stated on the PR230 Cl(3)/Z3 Wilson-staggered surface, not imported from a gauge-only Perron theorem",
        ],
        "current_substitutes_rejected": FORBIDDEN_SHORTCUTS,
    }


def route_table(parents: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "candidate": "Perron-Frobenius rank-one support",
            "status": status(parents["positivity_improving_neutral_scalar_rank_one"]),
            "blocker": "conditional theorem has no positivity-improving neutral-sector certificate",
        },
        {
            "candidate": "direct positivity-improving theorem",
            "status": status(parents["neutral_scalar_positivity_improving_direct_closure"]),
            "blocker": "reducible positive neutral transfer witness remains admissible",
        },
        {
            "candidate": "gauge Perron import",
            "status": status(parents["gauge_perron_neutral_scalar_rank_one_import"]),
            "blocker": "gauge-vacuum uniqueness does not control the neutral scalar response block",
        },
        {
            "candidate": "reflection positivity / OS positivity",
            "status": status(parents["reflection_positivity_lsz_shortcut"]),
            "blocker": "positive spectral weights do not force primitive-cone irreducibility",
        },
        {
            "candidate": "commutant / symmetry labels",
            "status": status(parents["neutral_scalar_commutant_rank_no_go"]),
            "blocker": "rank-two neutral response families preserve the labels",
        },
        {
            "candidate": "source-only tomography",
            "status": status(parents["neutral_scalar_top_coupling_tomography_gate"]),
            "blocker": "current response matrix has rank one and leaves a null direction",
        },
        {
            "candidate": "non-source rank repair",
            "status": status(parents["non_source_response_rank_repair_sufficiency"]),
            "blocker": "sufficiency is exact support; O_H/C_sH/C_HH or W/Z rows remain absent",
        },
    ]


def main() -> int:
    print("PR #230 neutral-scalar irreducibility authority audit")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    exact_positive_hits = find_exact_positive_authority()
    contract = minimal_premise_contract()
    routes = route_table(parents)

    conditional_support_loaded = (
        "positivity-improving neutral-scalar rank-one theorem"
        in status(parents["positivity_improving_neutral_scalar_rank_one"])
        and parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False
    )
    direct_attempt_blocks = (
        "neutral-scalar positivity-improving direct theorem not derived"
        in status(parents["neutral_scalar_positivity_improving_direct_closure"])
        and parents["neutral_scalar_positivity_improving_direct_closure"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and parents["neutral_scalar_positivity_improving_direct_closure"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
    )
    gauge_perron_blocks = (
        parents["gauge_perron_neutral_scalar_rank_one_import"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and parents["gauge_perron_neutral_scalar_rank_one_import"].get(
            "gauge_perron_import_closes_neutral_rank_one"
        )
        is False
    )
    tomography_blocks = (
        parents["neutral_scalar_top_coupling_tomography_gate"].get("gate_passed")
        is False
        and parents["neutral_scalar_top_coupling_tomography_gate"]
        .get("tomography_witness", {})
        .get("checks", {})
        .get("current_rank_insufficient")
        is True
    )
    assumption_audit_loaded = (
        parents["osp_oh_assumption_route_audit"].get("assumption_route_audit_passed")
        is True
        and parents["osp_oh_assumption_route_audit"].get("proposal_allowed") is False
    )
    no_exact_positive_authority = exact_positive_hits == []
    all_routes_have_blockers = all(row["blocker"] for row in routes)
    current_closure_gate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "conditional-rank-one-support-loaded",
        conditional_support_loaded,
        status(parents["positivity_improving_neutral_scalar_rank_one"]),
    )
    report(
        "direct-positivity-improvement-attempt-blocks",
        direct_attempt_blocks,
        status(parents["neutral_scalar_positivity_improving_direct_closure"]),
    )
    report(
        "gauge-perron-import-blocks",
        gauge_perron_blocks,
        status(parents["gauge_perron_neutral_scalar_rank_one_import"]),
    )
    report(
        "source-only-tomography-rank-insufficient",
        tomography_blocks,
        status(parents["neutral_scalar_top_coupling_tomography_gate"]),
    )
    report("assumption-route-audit-loaded", assumption_audit_loaded, status(parents["osp_oh_assumption_route_audit"]))
    report("exact-positive-authority-absent", no_exact_positive_authority, f"hits={exact_positive_hits}")
    report("route-table-has-explicit-blockers", all_routes_have_blockers, f"routes={len(routes)}")
    report(
        "future-premise-contract-names-irreducibility",
        "primitive-cone positivity improvement" in contract["needed_certificate"],
        contract["needed_certificate"],
    )
    report(
        "neutral-scalar-irreducibility-not-current-closure",
        not current_closure_gate_passed,
        f"current_closure_gate_passed={current_closure_gate_passed}",
    )

    authority_audit_passed = (
        not missing
        and not proposal_allowed
        and conditional_support_loaded
        and direct_attempt_blocks
        and gauge_perron_blocks
        and tomography_blocks
        and assumption_audit_loaded
        and no_exact_positive_authority
        and all_routes_have_blockers
        and not current_closure_gate_passed
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / neutral-scalar irreducibility authority absent on current PR230 surface"
        ),
        "verdict": (
            "The repo does not currently contain a same-surface neutral scalar "
            "irreducibility or primitive-cone positivity-improvement certificate. "
            "The rank-one/Perron route remains conditional support only; the "
            "direct positivity-improvement attempt, gauge-Perron import, "
            "reflection-positivity shortcut, commutant route, and source-only "
            "tomography route all leave an admissible orthogonal neutral sector."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No exact positive authority key or parent certificate proves neutral "
            "scalar irreducibility on the current PR230 surface."
        ),
        "bare_retained_allowed": False,
        "authority_audit_passed": authority_audit_passed,
        "neutral_scalar_irreducibility_certificate_present": False,
        "neutral_scalar_irreducibility_theorem_passed": False,
        "current_closure_gate_passed": current_closure_gate_passed,
        "exact_positive_authority_hits": exact_positive_hits,
        "minimal_premise_contract": contract,
        "route_table": routes,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not prove a new irreducibility theorem",
            "does not infer positivity improvement from reflection positivity, gauge Perron, symmetry labels, or source-only data",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not manufacture O_H, C_sH/C_HH rows, W/Z rows, or Schur A/B/C rows",
        ],
        "exact_next_action": (
            "Do not continue source-only rank-one loops.  Positive closure now "
            "requires one real missing input: a same-surface neutral scalar "
            "irreducibility theorem, certified O_H with C_sH/C_HH pole rows, "
            "same-source W/Z response rows with identity certificates, or Schur "
            "A/B/C kernel rows."
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
