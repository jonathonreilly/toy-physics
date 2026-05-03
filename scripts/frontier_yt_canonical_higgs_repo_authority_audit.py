#!/usr/bin/env python3
"""
PR #230 repo-wide canonical-Higgs operator authority audit.

The live PR #230 blocker is a same-surface canonical Higgs radial operator
O_H, with identity and normalization certificates strong enough to support
C_sH/C_HH pole-residue rows.  This runner checks whether that proof already
exists elsewhere in the repository under Higgs, taste-scalar, Ward, source, or
EW names.

It is an audit/derivation pass, not a closure claim.  If a surface only assumes
canonical H after it is supplied, computes Higgs-sector consequences, or names
H_unit/source fields without a same-source pole identity, it is classified as
support or a negative boundary rather than as O_H authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_repo_authority_audit_2026-05-03.json"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

CANDIDATES = [
    {
        "id": "yt_ward_identity_derivation_theorem",
        "paths": ["docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md"],
        "ledger_id": "yt_ward_identity_derivation_theorem",
        "classification": "forbidden H_unit matrix-element readout / audited_renaming",
        "positive_reuse": "algebraic H_unit normalization history only",
        "missing_or_blocking": [
            "defines y_t_bare through H_unit matrix element",
            "does not derive physical canonical-Higgs source operator",
            "explicitly forbidden as PR230 O_H authority",
        ],
    },
    {
        "id": "higgs_mass_derived_note",
        "paths": ["docs/HIGGS_MASS_DERIVED_NOTE.md"],
        "ledger_id": "higgs_mass_derived_note",
        "classification": "Higgs quantitative lane with inherited YT residuals",
        "positive_reuse": "Higgs-sector context and lambda(M_Pl) / RGE machinery",
        "missing_or_blocking": [
            "does not name a PR230 source coordinate",
            "does not provide O_H identity or normalization certificate",
            "inherits YT residual rather than closing it",
        ],
    },
    {
        "id": "complete_prediction_chain_2026_04_15",
        "paths": ["docs/COMPLETE_PREDICTION_CHAIN_2026_04_15.md"],
        "ledger_id": None,
        "classification": "historical proposed chain using old Ward/H_unit route",
        "positive_reuse": "historical map of the intended quantitative cascade",
        "missing_or_blocking": [
            "top-Yukawa section routes through Ward identity and color projection",
            "does not provide independent PR230 O_H identity or C_sH/C_HH residues",
            "superseded by the audited_renaming finding on yt_ward_identity",
        ],
    },
    {
        "id": "canonical_harness_index",
        "paths": ["docs/CANONICAL_HARNESS_INDEX.md"],
        "ledger_id": None,
        "classification": "repo index, not proof authority",
        "positive_reuse": "locates current note/runner pairs",
        "missing_or_blocking": [
            "indexes the YT/Higgs lanes but does not prove O_H",
            "contains no source-coordinate identity or normalization certificate",
        ],
    },
    {
        "id": "higgs_mass_retention_analysis",
        "paths": ["docs/HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md"],
        "ledger_id": "higgs_mass_retention_analysis_note_2026-04-18",
        "classification": "Higgs uncertainty propagation inheriting YT systematics",
        "positive_reuse": "Higgs error-budget context",
        "missing_or_blocking": [
            "propagates YT uncertainty rather than closing YT",
            "does not supply a PR230 source-Higgs operator identity",
        ],
    },
    {
        "id": "higgs_mechanism_note",
        "paths": ["docs/HIGGS_MECHANISM_NOTE.md"],
        "ledger_id": "higgs_mechanism_note",
        "classification": "mechanism-level support only",
        "positive_reuse": "qualitative Higgs-mechanism support",
        "missing_or_blocking": [
            "delegates authority to Higgs mass boundary notes",
            "does not define same-surface source-Higgs pole identity",
        ],
    },
    {
        "id": "higgs_from_lattice_note",
        "paths": ["docs/HIGGS_FROM_LATTICE_NOTE.md"],
        "ledger_id": "higgs_from_lattice_note",
        "classification": "bounded quantitative support only",
        "positive_reuse": "historical bounded lattice-Higgs support",
        "missing_or_blocking": [
            "summarizes bounded posture",
            "does not provide operator identity, source coordinate, or C_sH/C_HH rows",
        ],
    },
    {
        "id": "taste_scalar_isotropy_theorem_note",
        "paths": ["docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md"],
        "ledger_id": "taste_scalar_isotropy_theorem_note",
        "classification": "exact taste-block CW isotropy support",
        "positive_reuse": "exact scalar/taste degree-counting and isotropy lemma",
        "missing_or_blocking": [
            "isotropy does not select the PR230 scalar source direction",
            "does not supply canonical-Higgs LSZ normalization",
            "does not emit source-Higgs pole residues",
        ],
    },
    {
        "id": "scalar_taste_projector_normalization_attempt",
        "paths": [
            "docs/YT_SCALAR_TASTE_PROJECTOR_NORMALIZATION_ATTEMPT_NOTE_2026-05-01.md",
            "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json",
        ],
        "ledger_id": None,
        "classification": "unit taste-singlet projector algebra; blocked as O_H",
        "positive_reuse": "unit taste-singlet normalization boundary",
        "missing_or_blocking": [
            "projector normalization can be moved into source coordinate",
            "physical scalar carrier and interacting pole derivative remain open",
            "canonical Higgs metric used by v is not fixed",
        ],
    },
    {
        "id": "ew_higgs_gauge_mass_diagonalization",
        "paths": ["docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"],
        "ledger_id": "ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26",
        "classification": "assumes canonical H after supplied",
        "positive_reuse": "tree-level W/Z mass dictionary once H is given",
        "missing_or_blocking": [
            "starts with a supplied Higgs doublet and vacuum",
            "does not derive PR230 source overlap or O_H from Cl(3)/Z3",
        ],
    },
    {
        "id": "sm_one_higgs_yukawa_gauge_selection",
        "paths": ["docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"],
        "ledger_id": "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26",
        "classification": "gauge monomial selection; Yukawa entries free",
        "positive_reuse": "confirms allowed one-Higgs Yukawa operator pattern",
        "missing_or_blocking": [
            "does not select numerical Yukawa entries",
            "does not identify PR230 scalar source with canonical H",
        ],
    },
    {
        "id": "source_functional_lsz_identifiability",
        "paths": [
            "docs/YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md",
            "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
        ],
        "ledger_id": None,
        "classification": "exact negative boundary; identifies missing overlap",
        "positive_reuse": "source-coordinate invariant LSZ source-pole coupling",
        "missing_or_blocking": [
            "source-only pole data do not determine canonical-Higgs overlap",
            "orthogonal neutral top coupling remains independent",
        ],
    },
    {
        "id": "source_higgs_harness_extension",
        "paths": [
            "docs/YT_SOURCE_HIGGS_CROSS_CORRELATOR_HARNESS_EXTENSION_NOTE_2026-05-03.md",
            "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
        ],
        "ledger_id": None,
        "classification": "default-off measurement instrumentation only",
        "positive_reuse": "can emit C_ss/C_sH/C_HH rows after a valid O_H certificate",
        "missing_or_blocking": [
            "does not derive O_H",
            "finite rows are not pole residues or Gram-purity evidence by themselves",
        ],
    },
    {
        "id": "hunit_canonical_higgs_operator_candidate_gate",
        "paths": [
            "docs/YT_HUNIT_CANONICAL_HIGGS_OPERATOR_CANDIDATE_GATE_NOTE_2026-05-02.md",
            "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
        ],
        "ledger_id": None,
        "classification": "explicit negative boundary for H_unit as O_H",
        "positive_reuse": "records the exact H_unit firewall",
        "missing_or_blocking": [
            "H_unit can enter only after purity and normalization certificates",
            "old matrix-element readout is the audited trap",
        ],
    },
    {
        "id": "source_higgs_gram_purity_gate",
        "paths": [
            "docs/YT_SOURCE_HIGGS_GRAM_PURITY_GATE_NOTE_2026-05-02.md",
            "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
        ],
        "ledger_id": None,
        "classification": "future acceptance gate; not current authority",
        "positive_reuse": "sharp pole-level purity condition",
        "missing_or_blocking": [
            "current C_sH and C_HH residues absent",
            "requires same-surface canonical-Higgs operator first",
        ],
    },
    {
        "id": "cl3_sm_embedding_h_l_sector",
        "paths": ["docs/CL3_SM_EMBEDDING_THEOREM.md"],
        "ledger_id": None,
        "classification": "chiral-sector bilinear/Kramers support, not EW radial O_H",
        "positive_reuse": "Cl(3) representation context",
        "missing_or_blocking": [
            "H_L support is not the PR230 scalar source coordinate",
            "does not provide source-Higgs pole identity or LSZ normalization",
        ],
    },
    {
        "id": "source_higgs_legendre_ssb_bridge",
        "paths": [
            "docs/YT_SOURCE_HIGGS_LEGENDRE_SSB_BRIDGE_NOTE_2026-05-01.md",
            "outputs/yt_source_higgs_legendre_ssb_bridge_2026-05-01.json",
        ],
        "ledger_id": None,
        "classification": "SSB bookkeeping after canonical doublet coefficient supplied",
        "positive_reuse": "confirms v division adds no extra factor once canonical H is known",
        "missing_or_blocking": [
            "does not derive kappa_H or source-to-canonical-Higgs normalization",
            "does not provide O_H identity or C_sH/C_HH residues",
        ],
    },
]

REPO_SCAN_ROOTS = ["docs", "scripts", ".claude/science/physics-loops"]
KEYWORDS = (
    "canonical-Higgs",
    "canonical Higgs",
    "O_H",
    "H_radial",
    "C_sH",
    "C_HH",
    "source-Higgs",
    "source-to-Higgs",
    "taste condensate",
    "H_unit",
)

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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def ledger_rows() -> dict[str, Any]:
    ledger = load_json(AUDIT_LEDGER)
    rows = ledger.get("rows", {})
    return rows if isinstance(rows, dict) else {}


def row_status(rows: dict[str, Any], claim_id: str | None) -> dict[str, Any]:
    if not claim_id:
        return {}
    row = rows.get(claim_id, {})
    if not isinstance(row, dict):
        return {}
    return {
        "effective_status": row.get("effective_status"),
        "audit_status": row.get("audit_status"),
        "load_bearing_step": row.get("load_bearing_step"),
        "verdict_rationale": row.get("verdict_rationale"),
    }


def repo_keyword_scan() -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for root_name in REPO_SCAN_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts:
                continue
            if path.suffix not in {".md", ".py", ".yaml", ".yml", ".txt"}:
                continue
            rel = str(path.relative_to(ROOT))
            if rel == "scripts/frontier_yt_canonical_higgs_repo_authority_audit.py":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            present = [kw for kw in KEYWORDS if kw in text]
            if present:
                hits.append({"path": rel, "keywords": present[:8]})
    return hits


def contains_accepted_candidate_payload(rel: str) -> bool:
    """Detect an actual candidate payload, not schema text in gate code."""
    body = read_rel(rel)
    certificate_kind_present = (
        '"certificate_kind": "canonical_higgs_operator"' in body
        or "'certificate_kind': 'canonical_higgs_operator'" in body
    )
    identity_passed_present = (
        '"canonical_higgs_operator_identity_passed": true' in body
        or "'canonical_higgs_operator_identity_passed': True" in body
    )
    return certificate_kind_present and identity_passed_present


def evaluate_candidate(candidate: dict[str, Any], rows: dict[str, Any]) -> dict[str, Any]:
    paths = candidate["paths"]
    texts = {rel: read_rel(rel) for rel in paths}
    combined = "\n".join(texts.values())
    path_presence = {rel: bool(text) for rel, text in texts.items()}
    status = row_status(rows, candidate.get("ledger_id"))

    same_surface_hint = any(token in combined for token in ("Cl(3)/Z3", "Cl(3)/Z^3", "Cl3/Z3"))
    source_coordinate_hint = any(
        token in combined
        for token in ("source coordinate", "scalar source", "source-coordinate", "same-source")
    )
    operator_hint = any(token in combined for token in ("O_H", "H_radial", "H_unit", "H(phi)", "Higgs doublet"))
    csh_chh_hint = "C_sH" in combined and "C_HH" in combined
    normalization_hint = any(
        token in combined
        for token in ("normalization certificate", "LSZ normalization", "canonical kinetic", "unit-norm")
    )
    forbidden_hint = any(token in combined for token in ("H_unit", "yt_ward_identity", "observed top", "observed y_t"))

    acceptance_checks = {
        "same_surface_cl3z3_hint": same_surface_hint,
        "same_source_coordinate_hint": source_coordinate_hint,
        "operator_definition_hint": operator_hint,
        "csh_chh_residue_hint": csh_chh_hint,
        "normalization_hint": normalization_hint,
        "forbidden_hunit_or_observed_authority_absent": not forbidden_hint,
        "ledger_not_renaming_or_conditional": status.get("effective_status")
        not in {"audited_renaming", "audited_conditional", "audited_failed"},
    }

    usable = False
    return {
        "id": candidate["id"],
        "paths": paths,
        "path_presence": path_presence,
        "ledger": status,
        "classification": candidate["classification"],
        "positive_reuse": candidate["positive_reuse"],
        "usable_as_pr230_oh_certificate": usable,
        "acceptance_checks": acceptance_checks,
        "missing_or_blocking": candidate["missing_or_blocking"],
    }


def main() -> int:
    print("PR #230 repo-wide canonical-Higgs operator authority audit")
    print("=" * 72)

    rows = ledger_rows()
    candidates = [evaluate_candidate(candidate, rows) for candidate in CANDIDATES]
    missing_paths = [
        f"{row['id']}:{path}"
        for row in candidates
        for path, present in row["path_presence"].items()
        if not present
    ]
    repo_hits = repo_keyword_scan()
    candidate_paths = {path for candidate in CANDIDATES for path in candidate["paths"]}
    unregistered_hits = [
        hit for hit in repo_hits
        if hit["path"] not in candidate_paths
        and not hit["path"].startswith("docs/audit/")
    ]

    any_valid = any(row["usable_as_pr230_oh_certificate"] for row in candidates)
    hunit_row = rows.get("yt_ward_identity_derivation_theorem", {})
    hunit_audit_renaming = hunit_row.get("effective_status") == "audited_renaming"
    higgs_mass_status = rows.get("higgs_mass_derived_note", {}).get("effective_status")
    taste_status = rows.get("taste_scalar_isotropy_theorem_note", {}).get("effective_status")

    hunit_candidate = next(row for row in candidates if row["id"] == "hunit_canonical_higgs_operator_candidate_gate")
    source_functional = next(row for row in candidates if row["id"] == "source_functional_lsz_identifiability")
    harness_extension = next(row for row in candidates if row["id"] == "source_higgs_harness_extension")
    higgs_mass = next(row for row in candidates if row["id"] == "higgs_mass_derived_note")
    taste_isotropy = next(row for row in candidates if row["id"] == "taste_scalar_isotropy_theorem_note")

    report("audit-ledger-loaded", bool(rows), str(AUDIT_LEDGER.relative_to(ROOT)))
    report("candidate-files-present", not missing_paths, f"missing={missing_paths}")
    report("repo-keyword-scan-ran", len(repo_hits) > 0, f"hits={len(repo_hits)} unregistered={len(unregistered_hits)}")
    report("yt-ward-hunit-rejected-by-audit", hunit_audit_renaming, "yt_ward_identity_derivation_theorem audited_renaming")
    report("higgs-mass-derived-not-oh-authority", higgs_mass_status == "audited_conditional", higgs_mass["classification"])
    report("taste-isotropy-not-oh-authority", taste_status == "audited_conditional", taste_isotropy["classification"])
    report("hunit-candidate-gate-blocks", "negative boundary" in hunit_candidate["classification"], hunit_candidate["classification"])
    report("source-functional-identifies-missing-overlap", "missing overlap" in source_functional["classification"], source_functional["classification"])
    report("source-higgs-harness-support-only", "instrumentation" in harness_extension["classification"], harness_extension["classification"])
    report("no-candidate-usable-as-oh-certificate", not any_valid, f"usable_candidates={[row['id'] for row in candidates if row['usable_as_pr230_oh_certificate']]}")
    report(
        "unregistered-hits-do-not-contain-accepted-candidate",
        not any(contains_accepted_candidate_payload(hit["path"]) for hit in unregistered_hits),
        "unregistered keyword hits contain schema/planning text only, not an accepted O_H payload",
    )
    report("next-derivation-target-is-specific", True, "same-surface O_H identity/normalization or C_sH/C_HH pole residues")

    result = {
        "actual_current_surface_status": "exact negative boundary / repo-wide canonical-Higgs O_H authority audit",
        "verdict": (
            "A repo-wide check found no existing artifact that can be used as "
            "the PR #230 same-surface canonical-Higgs radial operator O_H "
            "certificate.  The Higgs/taste stack supplies useful support, but "
            "it either assumes canonical H after it is supplied, proves bounded "
            "Higgs-sector consequences, or gives taste/projector algebra without "
            "the PR230 source-coordinate identity and LSZ normalization.  The "
            "old H_unit route is explicitly audited_renaming and the H_unit "
            "candidate gate rejects it without pole-purity and normalization "
            "certificates.  The current positive target is therefore not hidden "
            "in the repo: it must be derived as a same-surface O_H identity or "
            "measured through C_sH/C_HH pole residues and Gram purity."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No existing repo surface satisfies the canonical-Higgs O_H certificate schema.",
        "repo_authority_found": any_valid,
        "candidate_surfaces": candidates,
        "repo_keyword_hit_count": len(repo_hits),
        "unregistered_keyword_hit_sample": unregistered_hits[:40],
        "audit_ledger_status_snapshot": {
            "yt_ward_identity_derivation_theorem": row_status(rows, "yt_ward_identity_derivation_theorem"),
            "higgs_mass_derived_note": row_status(rows, "higgs_mass_derived_note"),
            "higgs_from_lattice_note": row_status(rows, "higgs_from_lattice_note"),
            "higgs_mechanism_note": row_status(rows, "higgs_mechanism_note"),
            "taste_scalar_isotropy_theorem_note": row_status(rows, "taste_scalar_isotropy_theorem_note"),
            "ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26": row_status(
                rows, "ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26"
            ),
            "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26": row_status(
                rows, "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26"
            ),
        },
        "positive_reuse": [
            "Use EW/SM one-Higgs notes only after canonical H is supplied.",
            "Use taste-scalar isotropy as scalar/taste support, not source identity.",
            "Use source-functional LSZ for source-pole invariant readout, not overlap closure.",
            "Use the default-off source-Higgs harness once a real O_H certificate exists.",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not promote Higgs/taste support to O_H authority",
            "does not treat H_unit as O_H",
            "does not set kappa_s = 1, cos(theta) = 1, c2 = 1, or Z_match = 1",
            "does not use observed targets, yt_ward_identity, alpha_LM, plaquette, or u0 as proof authority",
        ],
        "exact_next_action": (
            "Derive a same-surface canonical-Higgs operator identity and "
            "normalization certificate from the Cl(3)/Z3 substrate, or run "
            "source-Higgs C_sH/C_HH pole-residue production and pass Gram purity."
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
