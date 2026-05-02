#!/usr/bin/env python3
"""
PR #230 orthogonal-neutral decoupling no-go.

After the dynamical rank-one attempt failed, a tempting shortcut is to treat a
finite/heavy orthogonal neutral pole as harmless.  This runner checks that
shortcut.  On the current surface, a mass gap by itself does not prove the
source pole is the canonical Higgs radial mode or that the top-coupled
orthogonal component vanishes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json"

CERTS = {
    "neutral_scalar_dynamical_rank_one": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "neutral_scalar_commutant_rank": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "latest_higgs_identity_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "confinement_gap_threshold": "outputs/yt_confinement_gap_threshold_import_audit_2026-05-02.json",
}

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def cert_status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def heavy_orthogonal_family() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_pole_mass_sq = 0.25
    source_pole_residue = 1.0
    canonical_overlap = 0.8
    for orthogonal_mass_sq in (2.0, 10.0, 100.0):
        rows.append(
            {
                "source_pole_mass_sq": source_pole_mass_sq,
                "source_pole_residue": source_pole_residue,
                "orthogonal_pole_mass_sq": orthogonal_mass_sq,
                "orthogonal_pole_gap_from_source": orthogonal_mass_sq - source_pole_mass_sq,
                "canonical_higgs_overlap_with_source_pole": canonical_overlap,
                "orthogonal_overlap_component": (1.0 - canonical_overlap * canonical_overlap) ** 0.5,
                "mass_gap_alone_sets_overlap_to_one": False,
                "requires_decoupling_scaling_theorem": True,
            }
        )
    return rows


def main() -> int:
    print("PR #230 orthogonal-neutral decoupling no-go")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    dynamic_rank_one_blocks = (
        "dynamical rank-one neutral scalar theorem not derived"
        in cert_status(certs["neutral_scalar_dynamical_rank_one"])
        and certs["neutral_scalar_dynamical_rank_one"].get("rank_one_dynamical_theorem_derived") is False
    )
    commutant_blocks = (
        "neutral scalar commutant does not force rank-one purity"
        in cert_status(certs["neutral_scalar_commutant_rank"])
        and certs["neutral_scalar_commutant_rank"].get("rank_one_theorem_derived") is False
    )
    source_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in cert_status(certs["source_pole_canonical_higgs_mixing"])
        and certs["source_pole_canonical_higgs_mixing"].get("proposal_allowed") is False
    )
    no_selection_blocks = (
        "no-orthogonal-top-coupling selection rule not derived"
        in cert_status(certs["no_orthogonal_top_coupling_selection"])
        and certs["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    gram_blocks = (
        "source-Higgs Gram purity gate not passed" in cert_status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    latest_identity_blocks = (
        "latest Higgs-pole identity blocker certificate" in cert_status(certs["latest_higgs_identity_blocker"])
        and certs["latest_higgs_identity_blocker"].get("identity_closed") is False
    )
    confinement_gap_not_enough = (
        "confinement gap not scalar LSZ threshold" in cert_status(certs["confinement_gap_threshold"])
        and certs["confinement_gap_threshold"].get("proposal_allowed") is False
    )

    rows = heavy_orthogonal_family()
    source_masses = {float(row["source_pole_mass_sq"]) for row in rows}
    source_residues = {float(row["source_pole_residue"]) for row in rows}
    orthogonal_masses = [float(row["orthogonal_pole_mass_sq"]) for row in rows]
    overlaps = {round(float(row["canonical_higgs_overlap_with_source_pole"]), 12) for row in rows}
    gaps_positive = all(float(row["orthogonal_pole_gap_from_source"]) > 0.0 for row in rows)
    decoupling_scaling_theorem_derived = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("dynamic-rank-one-still-blocks", dynamic_rank_one_blocks, cert_status(certs["neutral_scalar_dynamical_rank_one"]))
    report("commutant-rank-still-blocks", commutant_blocks, cert_status(certs["neutral_scalar_commutant_rank"]))
    report("source-pole-mixing-still-blocks", source_mixing_blocks, cert_status(certs["source_pole_canonical_higgs_mixing"]))
    report("no-orthogonal-selection-still-blocks", no_selection_blocks, cert_status(certs["no_orthogonal_top_coupling_selection"]))
    report("gram-purity-gate-still-blocks", gram_blocks, cert_status(certs["source_higgs_gram_purity"]))
    report("latest-identity-still-blocks", latest_identity_blocks, cert_status(certs["latest_higgs_identity_blocker"]))
    report("generic-gap-not-lsz-identity", confinement_gap_not_enough, cert_status(certs["confinement_gap_threshold"]))
    report("source-pole-mass-fixed", len(source_masses) == 1, f"source_masses={sorted(source_masses)}")
    report("source-pole-residue-fixed", len(source_residues) == 1, f"source_residues={sorted(source_residues)}")
    report("orthogonal-gap-positive", gaps_positive, f"orthogonal_masses={orthogonal_masses}")
    report("overlap-not-forced-to-one", overlaps == {0.8}, f"overlaps={sorted(overlaps)}")
    report(
        "decoupling-scaling-theorem-not-derived",
        not decoupling_scaling_theorem_derived,
        "no current certificate ties overlap/top coupling to inverse orthogonal mass",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / orthogonal neutral decoupling shortcut not derived",
        "verdict": (
            "A finite or heavy orthogonal neutral pole is not automatically "
            "harmless on the current surface.  The source pole mass and residue "
            "can remain fixed while the orthogonal mass is raised and the "
            "canonical-Higgs overlap stays below one.  Decoupling would require "
            "a theorem tying the overlap or orthogonal top coupling to the "
            "heavy mass limit, same-surface C_sH/C_HH Gram-purity data, or an "
            "accepted Higgs-identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No decoupling-scaling theorem or same-surface source-Higgs purity certificate is present.",
        "decoupling_scaling_theorem_derived": decoupling_scaling_theorem_derived,
        "heavy_orthogonal_counterfamily": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set cos(theta)=1 or kappa_s=1",
            "does not infer decoupling from a finite mass gap alone",
            "does not use observed masses, H_unit readout, yt_ward_identity authority, alpha_LM, plaquette, u0, or reduced pilots",
        ],
        "exact_next_action": (
            "Derive a decoupling-scaling theorem, measure C_sH/C_HH Gram purity, "
            "derive a stronger source-Higgs identity theorem, implement W/Z "
            "response with identity certificates, or process FH/LSZ chunks."
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
