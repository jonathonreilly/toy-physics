#!/usr/bin/env python3
"""
PR #230 staggered logdet Hessian neutral-mixing attempt.

This runner tests a tempting determinant route:

    staggered log det with the PR230 mass/source coordinate
        => missing neutral O_H / off-diagonal generator

The attempt fails on the current surface.  A one-source logdet
`W(s,0)` can determine the source-source response tower, but it does not
define a second neutral source `h` or its mixed/source-Higgs Hessian rows.
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
    / "yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json"
)

PARENTS = {
    "det_positivity_intake": "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json",
    "reflection_det_primitive_upgrade": "outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json",
    "neutral_offdiagonal_attempt": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "effective_potential_hessian_no_go": "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json",
    "minimal_axioms_firewall": "outputs/yt_pr230_minimal_axioms_yukawa_summary_firewall_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def source_only_derivatives(max_order: int = 8) -> list[float]:
    # W(s,0)=log(1+s), so d^n W/ds^n at zero is (-1)^(n-1)(n-1)!.
    return [((-1.0) ** (n - 1)) * math.factorial(n - 1) for n in range(1, max_order + 1)]


def logdet_counterfamily() -> list[dict[str, Any]]:
    """
    A two-source neutral determinant toy model:

        D(s,h; eps) = [[1+s, eps h], [eps h, 1]]
        W_eps(s,h) = log det D = log(1+s - eps^2 h^2)

    For every eps, W_eps(s,0)=log(1+s) and the entire source-only derivative
    tower is identical.  The h-source Hessian and mixed source-Higgs rows vary
    with eps and therefore cannot be recovered from W(s,0).
    """
    rows = []
    for eps in [0.0, 0.25, 0.75]:
        det_at_small_sources = 1.0 + 0.1 - (eps**2) * (0.1**2)
        rows.append(
            {
                "epsilon": eps,
                "D_matrix_symbolic": [[1.0, "epsilon*h"], ["epsilon*h", 1.0]],
                "W_source_only": "log(1+s)",
                "source_derivatives_at_zero": source_only_derivatives(),
                "d_h_W_at_zero": 0.0,
                "d_s_d_h_W_at_zero": 0.0,
                "d_h_h_W_at_zero": -2.0 * eps**2,
                "d_s_d_h_h_W_at_zero": 2.0 * eps**2,
                "offdiagonal_generator_norm": eps,
                "det_positive_near_origin": det_at_small_sources > 0.0,
                "det_at_s_0p1_h_0p1": det_at_small_sources,
            }
        )
    return rows


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_minimal_axioms_yukawa_summary_as_proof": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_u0_or_rconn": False,
        "defines_yt_bare": False,
        "sets_source_higgs_overlap_to_one": False,
        "sets_c2_zmatch_or_kappa_to_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 staggered logdet Hessian neutral-mixing attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    statuses = {name: status(cert) for name, cert in certs.items()}
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    rows = logdet_counterfamily()
    firewall = forbidden_firewall()

    source_towers = {tuple(row["source_derivatives_at_zero"]) for row in rows}
    hh_values = {row["d_h_h_W_at_zero"] for row in rows}
    shh_values = {row["d_s_d_h_h_W_at_zero"] for row in rows}
    offdiag_values = {row["offdiagonal_generator_norm"] for row in rows}

    source_only_identical = len(source_towers) == 1
    neutral_hessian_varies = len(hh_values) == len(rows) and len(shh_values) == len(rows)
    offdiag_varies = len(offdiag_values) == len(rows)
    determinant_positive = all(row["det_positive_near_origin"] for row in rows)
    det_support_only = (
        certs["det_positivity_intake"].get("determinant_bridge_closes_pr230") is False
        and certs["det_positivity_intake"].get("proposal_allowed") is False
    )
    reflection_det_not_primitive = (
        certs["reflection_det_primitive_upgrade"].get("primitive_upgrade_passed") is False
        and certs["reflection_det_primitive_upgrade"].get("exact_negative_boundary_passed") is True
        and certs["reflection_det_primitive_upgrade"].get("proposal_allowed") is False
    )
    neutral_offdiag_absent = (
        certs["neutral_offdiagonal_attempt"].get("offdiagonal_generator_certificate_passed") is False
        and certs["neutral_offdiagonal_attempt"].get("offdiagonal_generator_written") is False
        and certs["neutral_offdiagonal_attempt"].get("exact_negative_boundary_passed") is True
        and certs["neutral_offdiagonal_attempt"].get("proposal_allowed") is False
    )
    source_only_lsz_boundary = (
        "source-functional LSZ identifiability" in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    effective_hessian_boundary = (
        "Hessian not source-overlap identity" in statuses["effective_potential_hessian_no_go"]
        and certs["effective_potential_hessian_no_go"].get("proposal_allowed") is False
    )
    minimal_axioms_not_authority = (
        "minimal-axioms Yukawa summary is not PR230 proof authority"
        in statuses["minimal_axioms_firewall"]
        and certs["minimal_axioms_firewall"].get("proposal_allowed") is False
    )
    assembly_open = certs["full_positive_assembly"].get("proposal_allowed") is False
    retained_route_open = certs["retained_route"].get("proposal_allowed") is False
    clean_firewall = all(value is False for value in firewall.values())

    logdet_hessian_bridge_closes = (
        source_only_identical
        and not neutral_hessian_varies
        and not offdiag_varies
        and neutral_offdiag_absent is False
        and clean_firewall
    )
    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and source_only_identical
        and neutral_hessian_varies
        and offdiag_varies
        and determinant_positive
        and det_support_only
        and reflection_det_not_primitive
        and neutral_offdiag_absent
        and source_only_lsz_boundary
        and effective_hessian_boundary
        and minimal_axioms_not_authority
        and assembly_open
        and retained_route_open
        and logdet_hessian_bridge_closes is False
        and clean_firewall
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("source-only-logdet-tower-identical", source_only_identical, "W_eps(s,0)=log(1+s) for all eps")
    report("neutral-hessian-rows-vary", neutral_hessian_varies, f"d_hh={sorted(hh_values)} d_shh={sorted(shh_values)}")
    report("offdiagonal-generator-varies", offdiag_varies, f"eps={sorted(offdiag_values)}")
    report("determinant-positive-near-origin", determinant_positive, "all toy determinants positive at s=h=0.1")
    report("determinant-positivity-support-only", det_support_only, statuses["det_positivity_intake"])
    report("reflection-det-does-not-imply-primitive", reflection_det_not_primitive, statuses["reflection_det_primitive_upgrade"])
    report("neutral-offdiagonal-generator-still-absent", neutral_offdiag_absent, statuses["neutral_offdiagonal_attempt"])
    report("source-only-lsz-identifiability-boundary-loaded", source_only_lsz_boundary, statuses["source_functional_lsz_identifiability"])
    report("effective-hessian-source-overlap-boundary-loaded", effective_hessian_boundary, statuses["effective_potential_hessian_no_go"])
    report("minimal-axioms-summary-not-authority", minimal_axioms_not_authority, statuses["minimal_axioms_firewall"])
    report("assembly-still-open", assembly_open, statuses["full_positive_assembly"])
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("logdet-hessian-bridge-does-not-close", logdet_hessian_bridge_closes is False, "one-source logdet does not define h/O_H")
    report("forbidden-firewall-clean", clean_firewall, str(firewall))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "source-only determinant data underdetermine neutral mixing")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / source-only staggered logdet Hessian "
            "does not derive the neutral Higgs mixing bridge"
        ),
        "conditional_surface_status": (
            "A future two-source same-surface determinant functional Z(s,h), "
            "with h identified as canonical O_H and with C_sH/C_HH or "
            "primitive-cone rows, would be relevant.  The current W(s,0) "
            "surface is insufficient."
        ),
        "admitted_observation_status": None,
        "hypothetical_axiom_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The counterfamily keeps the entire source-only logdet tower fixed "
            "while varying the neutral h-Hessian and off-diagonal generator.  "
            "Thus source-only determinant/Hessian data cannot replace a "
            "same-surface O_H/h source or neutral primitive certificate."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "logdet_hessian_bridge_closes_pr230": logdet_hessian_bridge_closes,
        "counterfamily": rows,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "Does not define y_t_bare.",
            "Does not use H_unit or the Ward identity as proof authority.",
            "Does not use minimal-axioms y_t/m_t summary rows as proof authority.",
            "Does not use observed top/yukawa targets.",
            "Does not identify source-only mass derivatives with canonical O_H.",
            "Does not supply C_sH/C_HH, W/Z, Schur, scalar-LSZ, or matching/running authority.",
        ],
        "exact_next_action": (
            "Either construct a two-source PR230 functional Z(s,h) with a "
            "same-surface canonical O_H certificate, or derive a true neutral "
            "off-diagonal/primitive transfer theorem."
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
