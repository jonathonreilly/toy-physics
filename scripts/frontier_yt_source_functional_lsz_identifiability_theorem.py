#!/usr/bin/env python3
"""
PR #230 source-functional LSZ identifiability theorem.

This route-1 block asks exactly what can be derived from the Cl(3)/Z3 scalar
source functional when the source has an isolated scalar pole.  The answer is
useful but not closing: same-source LSZ data identify a source-pole coupling,
while the physical top Yukawa still needs the source-pole/canonical-Higgs
overlap or an equivalent same-surface response certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"

PARENTS = {
    "assumption_stress": "outputs/yt_pr230_assumption_import_stress_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "source_reparametrization": "outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json",
    "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_cross_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "same_source_wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def source_rescaling_rows() -> list[dict[str, float]]:
    """Same-source LSZ invariant under O_s -> c O_s."""
    base_dE_ds = 0.19
    base_dgamma_dp2 = 7.0
    rows: list[dict[str, float]] = []
    for c in (0.2, 0.5, 1.0, 2.0, 5.0):
        dE_ds = c * base_dE_ds
        dgamma_dp2 = base_dgamma_dp2 / (c * c)
        rows.append(
            {
                "source_rescaling_c": c,
                "dE_top_ds": dE_ds,
                "dGamma_ss_dp2_at_pole": dgamma_dp2,
                "same_source_lsz_readout": dE_ds * math.sqrt(dgamma_dp2),
                "forbidden_kappa_s_equals_one_readout": dE_ds,
            }
        )
    return rows


def orthogonal_overlap_rows() -> list[dict[str, float]]:
    """Hold source-only pole data fixed while changing canonical-Higgs overlap."""
    source_lsz_y = 0.91
    rows: list[dict[str, float]] = []
    for cos_theta in (1.0, 0.9, 0.75, 0.6):
        sin_theta = math.sqrt(max(0.0, 1.0 - cos_theta * cos_theta))
        rows.append(
            {
                "Res_Css": 1.0,
                "dGamma_ss_dp2_at_pole": 1.0,
                "same_source_lsz_readout": source_lsz_y,
                "canonical_higgs_overlap_cos_theta": cos_theta,
                "orthogonal_overlap_sin_theta": sin_theta,
                "canonical_y_t_if_orthogonal_top_coupling_zero": source_lsz_y / cos_theta,
                "Res_CsH_if_OH_available": cos_theta,
                "Gram_rho_sH_if_OH_available": cos_theta,
            }
        )
    return rows


def general_two_coupling_rows() -> list[dict[str, float]]:
    """Show that even y_chi=0 is an extra premise, not source-functional data."""
    cos_theta = 0.8
    sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
    source_y = 0.91
    rows: list[dict[str, float]] = []
    for y_chi in (-0.4, 0.0, 0.4):
        y_h = (source_y - sin_theta * y_chi) / cos_theta
        rows.append(
            {
                "same_source_lsz_readout": source_y,
                "canonical_higgs_overlap_cos_theta": cos_theta,
                "orthogonal_overlap_sin_theta": sin_theta,
                "orthogonal_top_coupling_y_chi": y_chi,
                "canonical_higgs_y_t": y_h,
            }
        )
    return rows


def main() -> int:
    print("PR #230 source-functional LSZ identifiability theorem")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    rescaling = source_rescaling_rows()
    overlaps = orthogonal_overlap_rows()
    two_coupling = general_two_coupling_rows()

    invariant_values = [row["same_source_lsz_readout"] for row in rescaling]
    forbidden_values = [row["forbidden_kappa_s_equals_one_readout"] for row in rescaling]
    invariant_spread = max(invariant_values) - min(invariant_values)
    forbidden_spread = max(forbidden_values) - min(forbidden_values)

    canonical_y_values = [row["canonical_y_t_if_orthogonal_top_coupling_zero"] for row in overlaps]
    source_only_fixed = {
        (
            round(row["Res_Css"], 12),
            round(row["dGamma_ss_dp2_at_pole"], 12),
            round(row["same_source_lsz_readout"], 12),
        )
        for row in overlaps
    }
    two_coupling_y_values = [row["canonical_higgs_y_t"] for row in two_coupling]

    assumption_firewall_passed = parents["assumption_stress"].get("fail_count") == 0
    source_to_higgs_open = (
        "source-to-Higgs LSZ closure attempt blocked" in status(parents["source_to_higgs_lsz"])
        and parents["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    source_reparam_boundary = (
        "source reparametrization gauge" in status(parents["source_reparametrization"])
        and parents["source_reparametrization"].get("proposal_allowed") is False
    )
    same_source_gate_open = (
        "same-source pole-data sufficiency gate not passed"
        in status(parents["same_source_pole_data_sufficiency"])
        and parents["same_source_pole_data_sufficiency"].get("gate_passed") is False
    )
    mixing_obstruction_loaded = (
        "source-pole canonical-Higgs mixing obstruction"
        in status(parents["source_pole_canonical_higgs_mixing"])
        and parents["source_pole_canonical_higgs_mixing"].get(
            "source_pole_canonical_identity_gate_passed"
        )
        is False
    )
    gram_gate_open = (
        "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity"])
        and parents["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    csh_missing = (
        "source-Higgs cross-correlator import audit" in status(parents["source_higgs_cross_import"])
        and parents["source_higgs_cross_import"].get("source_higgs_cross_correlator_authority_found")
        is False
    )
    wz_gate_open = (
        "same-source WZ response certificate gate not passed" in status(parents["same_source_wz_gate"])
        and parents["same_source_wz_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("assumption-firewall-passed", assumption_firewall_passed, PARENTS["assumption_stress"])
    report("source-to-higgs-lsz-still-open", source_to_higgs_open, status(parents["source_to_higgs_lsz"]))
    report("source-reparametrization-boundary-loaded", source_reparam_boundary, status(parents["source_reparametrization"]))
    report("same-source-lsz-rescaling-invariant", invariant_spread < 1.0e-12, f"spread={invariant_spread:.3e}")
    report("kappa-one-readout-rejected", forbidden_spread > 0.5, f"spread={forbidden_spread:.6g}")
    report("source-only-pole-data-do-not-fix-overlap", len(source_only_fixed) == 1 and max(canonical_y_values) - min(canonical_y_values) > 0.4, f"canonical_y={canonical_y_values}")
    report("orthogonal-top-coupling-is-independent-premise", max(two_coupling_y_values) - min(two_coupling_y_values) > 0.5, f"canonical_y={two_coupling_y_values}")
    report("same-source-pole-data-gate-remains-open", same_source_gate_open, status(parents["same_source_pole_data_sufficiency"]))
    report("source-pole-canonical-mixing-obstruction-loaded", mixing_obstruction_loaded, status(parents["source_pole_canonical_higgs_mixing"]))
    report("gram-purity-route-is-exact-target-but-absent", gram_gate_open and csh_missing, "C_sH/C_HH not on current surface")
    report("wz-response-route-still-needs-real-response", wz_gate_open, status(parents["same_source_wz_gate"]))

    theorem_closed = False
    result = {
        "actual_current_surface_status": "exact negative boundary / source-functional LSZ identifiability theorem",
        "verdict": (
            "From the current Cl(3)/Z3 scalar source functional, an isolated "
            "source pole plus same-source FH/LSZ data can identify a "
            "source-pole coupling through (dE_top/ds)*sqrt(dGamma_ss/dp2). "
            "That product is invariant under source-coordinate rescaling, so "
            "the blocker is not the forbidden shortcut kappa_s=1.  The blocker "
            "is identifiability: source-only pole data do not determine the "
            "overlap between the measured source pole and the canonical Higgs "
            "radial mode used by v, nor do they set the top coupling of an "
            "orthogonal neutral scalar to zero.  Therefore route 1 cannot close "
            "from source-functional data alone.  The exact missing data are a "
            "same-surface source-Higgs Gram purity measurement/theorem, an "
            "equivalent canonical-Higgs source identity, or a real W/Z response "
            "certificate that fixes the same sector overlap."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source-functional LSZ theorem identifies the missing overlap; it does not derive it on the current surface.",
        "theorem_closed": theorem_closed,
        "same_source_lsz_rescaling_rows": rescaling,
        "orthogonal_overlap_counterfamily": overlaps,
        "general_two_coupling_counterfamily": two_coupling,
        "necessary_and_sufficient_extra_data": [
            "C_sH and C_HH pole residues with Gram purity Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
            "a same-surface canonical-Higgs operator O_H and source-pole identity theorem",
            "a W/Z mass-response certificate measuring dM_W/ds or dM_Z/ds plus sector-overlap identity",
            "a microscopic rank-one neutral-scalar theorem excluding orthogonal source-pole admixture and orthogonal top coupling",
        ],
        "forbidden_shortcuts_checked": [
            "H_unit matrix-element readout",
            "yt_ward_identity as authority",
            "observed top mass / observed y_t as proof selectors",
            "alpha_LM / plaquette / u0 as load-bearing proof input",
            "reduced cold pilots as production evidence",
            "c2 = 1 unless derived",
            "Z_match = 1 unless derived",
            "kappa_s = 1 unless derived by scalar LSZ/canonical normalization",
        ],
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not identify O_s with canonical H",
            "does not set cos(theta) = 1",
            "does not set orthogonal neutral top coupling to zero",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, c2 = 1, Z_match = 1, or reduced pilots as proof input",
        ],
        "exact_next_action": (
            "Implement or derive same-surface C_sH/C_HH pole-residue rows, "
            "or implement a production W/Z mass-response observable with a "
            "sector-overlap certificate; source-only LSZ data are insufficient."
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
