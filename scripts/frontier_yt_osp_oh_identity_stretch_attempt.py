#!/usr/bin/env python3
"""
PR #230 O_sp/O_H identity stretch attempt.

This is the first-principles stretch required after deriving the Legendre/LSZ
source-pole operator O_sp.  It asks whether the current Cl(3)/Z3 surface can
promote O_sp to the canonical Higgs radial operator O_H without adding a new
source-Higgs row, W/Z response row, or rank-one neutral-scalar theorem.

The output is intentionally claim-firewalled.  If the current premise set
cannot force O_sp = O_H, the runner records the exact counterfamily rather
than authorizing retained/proposed-retained wording.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_osp_oh_identity_stretch_attempt_2026-05-03.json"

PARENTS = {
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "gauge_vev_source_overlap": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "neutral_scalar_commutant": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_dynamical_rank_one": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "neutral_scalar_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
    "no_orthogonal_top_coupling": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_wz_response": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "candidate_stress": "outputs/yt_canonical_higgs_operator_candidate_stress_2026-05-03.json",
}

DOCS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "ew_higgs_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
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


def read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def overlap_counterfamily() -> list[dict[str, float | bool]]:
    """Hold all source-only data fixed while changing O_sp/O_H overlap."""
    y_source = 0.82
    rows: list[dict[str, float | bool]] = []
    for cos_theta, y_h in ((1.0, 0.82), (0.9, 0.70), (0.75, 0.58), (0.6, 0.48)):
        sin_theta = math.sqrt(max(0.0, 1.0 - cos_theta * cos_theta))
        if sin_theta == 0.0:
            y_chi = 0.0
        else:
            y_chi = (y_source - cos_theta * y_h) / sin_theta
        gram_delta = 1.0 - cos_theta * cos_theta
        rows.append(
            {
                "Res_C_sp_sp": 1.0,
                "same_source_y_readout": y_source,
                "canonical_higgs_overlap_cos_theta": cos_theta,
                "orthogonal_overlap_sin_theta": sin_theta,
                "canonical_higgs_y_t": y_h,
                "orthogonal_neutral_top_coupling": y_chi,
                "source_readout_reconstructed": cos_theta * y_h + sin_theta * y_chi,
                "source_higgs_gram_determinant_if_measured": gram_delta,
                "would_certify_O_sp_equals_O_H": abs(gram_delta) < 1.0e-12 and abs(abs(cos_theta) - 1.0) < 1.0e-12,
            }
        )
    return rows


def attack_frame_rows(certs: dict[str, dict[str, Any]], docs: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "frame": "v_order_parameter_identity",
            "positive_target": "derive O_sp = O_H because v uses the same scalar direction",
            "current_surface_result": "blocked",
            "loaded_blocker": status(certs["gauge_vev_source_overlap"]),
            "reason": "static v or gauge masses do not fix the Cl(3)/Z3 additive source overlap",
        },
        {
            "frame": "taste_scalar_isotropy",
            "positive_target": "derive O_sp = O_H from exact taste-block scalar isotropy",
            "current_surface_result": "blocked",
            "loaded_blocker": "taste isotropy proves Hessian degeneracy, not PR230 source-axis selection",
            "evidence": "isotropic" in docs["taste_scalar_isotropy"].lower()
            and "does not select" in status(certs["canonical_higgs_repo_authority_audit"]),
            "reason": "an isotropic scalar block admits rotations; it does not set the source-Higgs angle",
        },
        {
            "frame": "one_higgs_gauge_selection",
            "positive_target": "derive no orthogonal neutral scalar top coupling from one-Higgs SM monomial selection",
            "current_surface_result": "blocked",
            "loaded_blocker": status(certs["no_orthogonal_top_coupling"]),
            "evidence": "leaves Yukawa values free" in status(certs["canonical_higgs_repo_authority_audit"])
            or "does not select the numerical entries" in docs["sm_one_higgs"],
            "reason": "SM monomial selection assumes canonical H after supplied; it is not a scalar source-pole purity theorem",
        },
        {
            "frame": "neutral_scalar_rank_one",
            "positive_target": "derive a rank-one neutral scalar response theorem",
            "current_surface_result": "blocked",
            "loaded_blocker": status(certs["neutral_scalar_dynamical_rank_one"]),
            "reason": "current dynamics permit a finite orthogonal neutral scalar pole witness",
        },
        {
            "frame": "observable_overlap_measurement",
            "positive_target": "measure or certify the O_sp/O_H overlap directly",
            "current_surface_result": "open",
            "loaded_blocker": status(certs["source_higgs_gram_purity"]),
            "reason": "C_sH/C_HH pole residues or same-source W/Z response are the exact next non-source rows, but they are absent",
        },
    ]


def forbidden_source_fragments_absent() -> tuple[bool, list[str]]:
    body = Path(__file__).read_text(encoding="utf-8")
    fragments = [
        "y_t" + "_bare :=",
        "H_unit" + " matrix-element readout as authority",
        "observed" + " target selector",
        "alpha" + "_LM as authority",
        "cos" + "(theta) = 1 by assumption",
    ]
    hits = [fragment for fragment in fragments if fragment in body]
    return not hits, hits


def main() -> int:
    print("PR #230 O_sp/O_H identity stretch attempt")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    docs = {name: read(rel) for name, rel in DOCS.items()}
    missing_certs = [name for name, cert in certs.items() if not cert]
    missing_docs = [name for name, text in docs.items() if not text]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    counterfamily = overlap_counterfamily()
    attack_frames = attack_frame_rows(certs, docs)
    forbidden_absent, forbidden_hits = forbidden_source_fragments_absent()

    y_values = [float(row["canonical_higgs_y_t"]) for row in counterfamily]
    source_values = [float(row["source_readout_reconstructed"]) for row in counterfamily]
    gram_deltas = [float(row["source_higgs_gram_determinant_if_measured"]) for row in counterfamily]
    finite_orthogonal = [
        float(row["orthogonal_neutral_top_coupling"])
        for row in counterfamily
        if float(row["orthogonal_overlap_sin_theta"]) > 0.0
    ]

    osp_constructed = (
        certs["legendre_source_pole_operator"].get("source_pole_operator_constructed") is True
        and certs["legendre_source_pole_operator"].get("canonical_higgs_operator_identity_passed") is False
    )
    repo_no_hidden_oh = (
        certs["canonical_higgs_repo_authority_audit"].get("repo_authority_found") is False
    )
    operator_gate_open = (
        certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and "certificate absent" in status(certs["canonical_higgs_operator_gate"])
    )
    source_functional_blocks = (
        "source-functional LSZ identifiability theorem"
        in status(certs["source_functional_lsz_identifiability"])
        and certs["source_functional_lsz_identifiability"].get("theorem_closed") is False
    )
    mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction" in status(certs["source_pole_mixing"])
        and certs["source_pole_mixing"].get("source_pole_canonical_identity_gate_passed") is False
    )
    rank_one_blocks = (
        "dynamical rank-one neutral scalar theorem not derived"
        in status(certs["neutral_scalar_dynamical_rank_one"])
        and certs["neutral_scalar_dynamical_rank_one"].get("proposal_allowed") is False
    )
    tomography_blocks = (
        certs["neutral_scalar_tomography"].get("gate_passed") is False
        and "tomography gate not passed" in status(certs["neutral_scalar_tomography"])
    )
    gram_open = (
        certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    wz_open = (
        certs["same_source_wz_response"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    candidates_rejected = (
        "candidate stress rejects current substitutes" in status(certs["candidate_stress"])
    )

    source_fixed = max(source_values) - min(source_values) < 1.0e-12
    canonical_varies = max(y_values) - min(y_values) > 0.25
    gram_would_distinguish = any(delta > 1.0e-12 for delta in gram_deltas)
    orthogonal_finite = all(math.isfinite(value) for value in finite_orthogonal)
    all_frames_accounted = len(attack_frames) == 5 and all(row["current_surface_result"] in {"blocked", "open"} for row in attack_frames)
    identity_derived = False
    proposal_now_allowed = False

    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("support-docs-present", not missing_docs, f"missing={missing_docs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("legendre-source-pole-operator-loaded", osp_constructed, status(certs["legendre_source_pole_operator"]))
    report("repo-authority-finds-no-hidden-oh", repo_no_hidden_oh, status(certs["canonical_higgs_repo_authority_audit"]))
    report("canonical-oh-certificate-gate-open", operator_gate_open, status(certs["canonical_higgs_operator_gate"]))
    report("source-functional-identifiability-blocks-source-only", source_functional_blocks, status(certs["source_functional_lsz_identifiability"]))
    report("source-pole-mixing-blocker-loaded", mixing_blocks, status(certs["source_pole_mixing"]))
    report("rank-one-dynamical-route-blocked", rank_one_blocks, status(certs["neutral_scalar_dynamical_rank_one"]))
    report("top-coupling-tomography-rank-blocked", tomography_blocks, status(certs["neutral_scalar_tomography"]))
    report("gram-purity-route-open-not-passed", gram_open, status(certs["source_higgs_gram_purity"]))
    report("wz-response-route-open-not-passed", wz_open, status(certs["same_source_wz_response"]))
    report("candidate-stress-rejects-substitutes", candidates_rejected, status(certs["candidate_stress"]))
    report("stuck-fanout-frames-recorded", all_frames_accounted, f"frames={len(attack_frames)}")
    report("counterfamily-holds-source-readout-fixed", source_fixed, f"source_values={source_values}")
    report("counterfamily-varies-canonical-y", canonical_varies, f"canonical_y={y_values}")
    report("orthogonal-couplings-remain-finite", orthogonal_finite, f"orthogonal={finite_orthogonal}")
    report("gram-row-would-distinguish-counterfamily", gram_would_distinguish, f"gram_deltas={gram_deltas}")
    report("forbidden-shortcuts-absent", forbidden_absent, f"hits={forbidden_hits}")
    report("osp-oh-identity-not-derived", not identity_derived, "no current-surface premise forces cos(theta)=1")
    report("retained-proposal-not-authorized", not proposal_now_allowed, "open non-source overlap row or rank-one theorem still required")

    result = {
        "actual_current_surface_status": "exact negative boundary / O_sp-to-O_H identity not derived on current surface",
        "conditional_surface_status": "conditional-support if a future C_sH/C_HH Gram-purity row, W/Z response row, or rank-one neutral-scalar theorem closes the overlap",
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_now_allowed,
        "proposal_allowed_reason": "The Legendre source-pole operator is derived, but no current-surface premise forces its overlap with canonical O_H to be unity.",
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "identity_derived": identity_derived,
        "minimal_allowed_premises_A_min": [
            "Cl(3)/Z3 substrate and uniform additive scalar source s",
            "Legendre/LSZ source-pole construction O_sp with unit pole residue",
            "existing canonical Higgs H/v surfaces only after H is supplied",
            "exact taste-scalar isotropy support",
            "existing one-Higgs gauge-monomial selection support",
            "no H_unit matrix-element readout, no yt_ward authority, no observed targets",
        ],
        "forbidden_imports": [
            "H_unit matrix-element readout",
            "yt_ward_identity as authority",
            "observed m_t or y_t selector",
            "alpha_LM, plaquette, u0",
            "kappa_s = 1, cos(theta) = 1, c2 = 1, Z_match = 1 by assumption",
        ],
        "stretch_attempt_frames": attack_frames,
        "counterfamily": counterfamily,
        "verdict": (
            "The first-principles stretch does not derive O_sp = O_H from the "
            "current PR #230 surface.  O_sp is a valid LSZ-normalized source-pole "
            "operator, but current Higgs/taste/EW support does not fix the "
            "source-pole/canonical-Higgs angle.  A positive counterfamily holds "
            "Res(C_sp,sp)=1 and the same-source top readout fixed while varying "
            "the canonical-Higgs component and a finite orthogonal neutral top "
            "coupling.  The family would be distinguished by C_sH/C_HH Gram "
            "purity, a same-source W/Z response row, or a genuine rank-one "
            "neutral-scalar theorem.  Those are absent, so retained or "
            "proposed_retained closure is not authorized."
        ),
        "exact_next_action": (
            "Stop trying source-only or static-Higgs shortcuts.  The next positive "
            "route must add one independent non-source row or theorem: source-Higgs "
            "C_sH/C_HH pole residues with Gram purity, same-source W/Z response "
            "with sector-overlap identity, or a dynamical rank-one neutral-scalar "
            "theorem that excludes O_chi."
        ),
        "parent_certificates": PARENTS,
        "support_docs": DOCS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not identify O_sp with O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
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
