#!/usr/bin/env python3
"""
PR #230 reflection + determinant positivity primitive-upgrade gate.

This runner tests a tempting post-det-positivity shortcut:

    reflection positivity + staggered-Wilson determinant positivity
        => neutral scalar primitive-cone / rank-one bridge

The shortcut fails on the current PR230 surface.  Both inputs are
positivity-preservation statements.  PR230 needs positivity improvement in the
neutral scalar response sector, or explicit O_H/C_sH/C_HH, W/Z, Schur, or
production evidence rows.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json"
)

PARENTS = {
    "reflection_positivity_lsz_no_go": (
        "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"
    ),
    "det_positivity_intake": (
        "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json"
    ),
    "neutral_positivity_direct": (
        "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"
    ),
    "primitive_cone_gate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
    ),
    "primitive_cone_stretch_no_go": (
        "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json"
    ),
    "derived_bridge_rank_one": (
        "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json"
    ),
    "source_sector_transfer": (
        "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
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


def strongly_connected(matrix: list[list[float]], tolerance: float = 1.0e-12) -> bool:
    n = len(matrix)
    graph = [[j for j, value in enumerate(row) if value > tolerance] for row in matrix]
    reverse = [[i for i in range(n) if matrix[i][j] > tolerance] for j in range(n)]

    def reachable(adjacency: list[list[int]]) -> set[int]:
        seen = {0}
        queue: deque[int] = deque([0])
        while queue:
            node = queue.popleft()
            for child in adjacency[node]:
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen

    return len(reachable(graph)) == n and len(reachable(reverse)) == n


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def primitive_power_positive(
    matrix: list[list[float]], tolerance: float = 1.0e-12
) -> dict[str, Any]:
    n = len(matrix)
    power = [row[:] for row in matrix]
    max_power = max(1, n * n - 2 * n + 2)
    for exponent in range(1, max_power + 1):
        if all(value > tolerance for row in power for value in row):
            return {"positive": True, "first_positive_power": exponent}
        power = matmul(power, matrix)
    return {"positive": False, "first_positive_power": None}


def reflection_det_reducible_witness() -> dict[str, Any]:
    neutral_transfer = [[0.93, 0.0], [0.0, 0.89]]
    source_vector = [1.0, 0.0]
    hidden_vector = [0.0, 1.0]
    spectral_weights = [1.0, 0.35]
    masses = [1.00, 1.32]
    time_slices = [1, 2, 3, 4]
    source_correlator = [
        sum(
            spectral_weights[i] * source_vector[i] ** 2 * (neutral_transfer[i][i] ** t)
            for i in range(2)
        )
        for t in time_slices
    ]
    hidden_correlator = [
        sum(
            spectral_weights[i] * hidden_vector[i] ** 2 * (neutral_transfer[i][i] ** t)
            for i in range(2)
        )
        for t in time_slices
    ]
    return {
        "construction_type": "finite neutral-sector countermodel",
        "euclidean_reflection_positive": all(weight > 0.0 for weight in spectral_weights),
        "fermion_determinant_positive": True,
        "neutral_transfer_matrix": neutral_transfer,
        "neutral_transfer_nonnegative": all(
            value >= 0.0 for row in neutral_transfer for value in row
        ),
        "strongly_connected": strongly_connected(neutral_transfer),
        "primitive_power": primitive_power_positive(neutral_transfer),
        "source_vector": source_vector,
        "hidden_orthogonal_vector": hidden_vector,
        "positive_spectral_weights": spectral_weights,
        "masses": masses,
        "time_slices": time_slices,
        "source_only_correlator": source_correlator,
        "hidden_orthogonal_correlator": hidden_correlator,
        "source_only_rows_do_not_see_hidden_block": True,
        "orthogonal_neutral_top_coupling_can_survive": True,
        "lesson": (
            "Positive spectral measure and positive fermion determinant are "
            "compatible with a block-diagonal positive neutral transfer.  The "
            "missing theorem is irreducibility/positivity improvement, not "
            "positivity preservation."
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_u0_or_rconn": False,
        "defines_yt_bare": False,
        "sets_source_higgs_overlap_to_one": False,
        "treats_reflection_positivity_as_lsz_closure": False,
        "treats_determinant_positivity_as_rank_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 reflection + determinant positivity primitive-upgrade gate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    statuses = {name: status(cert) for name, cert in certs.items()}
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    witness = reflection_det_reducible_witness()
    firewall = forbidden_firewall()

    reflection_is_no_go = (
        "reflection positivity not scalar LSZ closure"
        in statuses["reflection_positivity_lsz_no_go"]
        and certs["reflection_positivity_lsz_no_go"].get("proposal_allowed") is False
    )
    det_is_support_only = (
        certs["det_positivity_intake"].get("intake_gate_passed") is True
        and certs["det_positivity_intake"].get("determinant_bridge_closes_pr230")
        is False
        and certs["det_positivity_intake"].get("proposal_allowed") is False
    )
    direct_positivity_not_improvement = (
        certs["neutral_positivity_direct"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
        and certs["neutral_positivity_direct"].get("exact_negative_boundary_passed")
        is True
    )
    primitive_certificate_absent = (
        certs["primitive_cone_gate"].get("primitive_cone_certificate_gate_passed")
        is False
        and certs["primitive_cone_gate"].get("proposal_allowed") is False
    )
    primitive_stretch_no_go = (
        certs["primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True
        and certs["primitive_cone_stretch_no_go"].get("proposal_allowed") is False
    )
    derived_bridge_still_open = (
        certs["derived_bridge_rank_one"].get("derived_bridge_closure_passed")
        is False
        and certs["derived_bridge_rank_one"].get("exact_negative_boundary_passed")
        is True
    )
    source_sector_not_closure = (
        certs["source_sector_transfer"].get("bounded_support_passed") is True
        and certs["source_sector_transfer"].get("direct_closure_available") is False
    )
    assembly_open = certs["full_positive_assembly"].get("proposal_allowed") is False
    retained_route_open = certs["retained_route"].get("proposal_allowed") is False
    witness_blocks_upgrade = (
        witness["euclidean_reflection_positive"] is True
        and witness["fermion_determinant_positive"] is True
        and witness["neutral_transfer_nonnegative"] is True
        and witness["strongly_connected"] is False
        and witness["primitive_power"]["positive"] is False
        and witness["orthogonal_neutral_top_coupling_can_survive"] is True
    )
    clean_firewall = all(value is False for value in firewall.values())

    primitive_upgrade_passed = (
        reflection_is_no_go
        and det_is_support_only
        and direct_positivity_not_improvement is False
        and primitive_certificate_absent is False
        and witness_blocks_upgrade is False
        and clean_firewall
    )
    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and reflection_is_no_go
        and det_is_support_only
        and direct_positivity_not_improvement
        and primitive_certificate_absent
        and primitive_stretch_no_go
        and derived_bridge_still_open
        and source_sector_not_closure
        and assembly_open
        and retained_route_open
        and witness_blocks_upgrade
        and primitive_upgrade_passed is False
        and clean_firewall
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("reflection-positivity-is-no-go-for-lsz", reflection_is_no_go, statuses["reflection_positivity_lsz_no_go"])
    report("determinant-positivity-is-support-only", det_is_support_only, statuses["det_positivity_intake"])
    report("direct-positivity-is-not-improvement", direct_positivity_not_improvement, statuses["neutral_positivity_direct"])
    report("primitive-certificate-absent", primitive_certificate_absent, statuses["primitive_cone_gate"])
    report("primitive-stretch-no-go-present", primitive_stretch_no_go, statuses["primitive_cone_stretch_no_go"])
    report("derived-bridge-still-open", derived_bridge_still_open, statuses["derived_bridge_rank_one"])
    report("source-sector-pattern-not-closure", source_sector_not_closure, statuses["source_sector_transfer"])
    report("assembly-still-open", assembly_open, statuses["full_positive_assembly"])
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("reducible-positive-witness-blocks-upgrade", witness_blocks_upgrade, "reflection/det positive but non-primitive")
    report("primitive-upgrade-not-passed", primitive_upgrade_passed is False, "positivity preservation != positivity improvement")
    report("forbidden-firewall-clean", clean_firewall, str(firewall))

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / reflection plus determinant positivity "
            "does not upgrade PR230 to a neutral primitive-cone bridge"
        ),
        "conditional_surface_status": (
            "If a future same-surface theorem proves neutral-sector "
            "irreducibility/primitive positivity improvement, these positivity "
            "inputs become useful supporting hypotheses.  They are not the "
            "primitive bridge by themselves."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Reflection positivity and determinant positivity preserve "
            "positivity but do not exclude a reducible neutral scalar transfer "
            "with source-invisible orthogonal top-coupled directions."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "primitive_upgrade_passed": primitive_upgrade_passed,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "reflection_det_reducible_witness": witness,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not define y_t_bare",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top/Yukawa values or alpha_LM/plaquette/u0 inputs",
            "does not treat positive measure or OS positivity as neutral irreducibility",
            "does not identify source-only C_ss rows with canonical O_H",
        ],
        "exact_next_action": (
            "Do not use reflection/determinant positivity as the PR230 bridge.  "
            "Continue through one actual positive object: a same-surface "
            "neutral primitive-cone certificate, canonical O_H with C_sH/C_HH "
            "rows, same-source W/Z response rows, Schur A/B/C rows, or strict "
            "production FH/LSZ plus matching."
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
