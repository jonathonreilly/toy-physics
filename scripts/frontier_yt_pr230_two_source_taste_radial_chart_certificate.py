#!/usr/bin/env python3
"""
PR #230 two-source taste-radial chart certificate.

The one-dimensional PR230 source line cannot be reparametrized into the
trace-zero Higgs/taste axes.  This runner checks the next honest source-route
move: if a future block explicitly adds a second source coordinate on the same
Cl(3)/Z^3 taste algebra, is there a canonical algebraic taste-radial axis and
source/taste chart to target?

The answer is exact support, not closure.  The chart is a same-surface
two-source extension, but it is not a current production row, not canonical
O_H, and not a physical y_t readout until an action/source authority and pole
rows land.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json"
)

PARENTS = {
    "source_coordinate_transport_gate": (
        "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json"
    ),
    "source_coordinate_transport_completion": (
        "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
    ),
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "taste_condensate_oh_bridge_audit": (
        "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"
    ),
    "source_higgs_builder": (
        "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json"
    ),
    "source_higgs_readiness": (
        "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json"
    ),
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "two_source_production_action": (
        "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
    ),
    "taste_radial_measurement_rows": (
        "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json"
    ),
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def pauli_x() -> np.ndarray:
    return np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def taste_axes() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = pauli_x()
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def cyclic_tensor_permutation() -> np.ndarray:
    """Matrix for U|a,b,c> = |c,a,b> in the binary tensor basis."""
    u = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * c + 2 * a + b
                u[dst, src] = 1.0
    return u


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def hs_norm(a: np.ndarray) -> float:
    return math.sqrt(max(float(hs_inner(a, a).real), 0.0))


def normalize(a: np.ndarray) -> np.ndarray:
    n = hs_norm(a)
    if n == 0.0:
        raise ValueError("cannot normalize zero operator")
    return a / n


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "set_kappa_s_equal_one": False,
        "identified_taste_radial_axis_with_canonical_oh": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 two-source taste-radial chart certificate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    identity = np.eye(8, dtype=complex)
    source_raw = identity
    source_hat = normalize(source_raw)
    axes = taste_axes()
    axis_hats = [normalize(axis) for axis in axes]
    radial_raw = axes[0] + axes[1] + axes[2]
    radial_hat = normalize(radial_raw)
    u = cyclic_tensor_permutation()

    axis_orthogonal = all(
        abs(hs_inner(axis_hats[i], axis_hats[j]).real - (1.0 if i == j else 0.0))
        < 1.0e-14
        for i in range(3)
        for j in range(3)
    )
    source_radial_orthogonal = abs(hs_inner(source_hat, radial_hat)) < 1.0e-14
    source_norm_ok = abs(hs_norm(source_hat) - 1.0) < 1.0e-14
    radial_norm_ok = abs(hs_norm(radial_hat) - 1.0) < 1.0e-14
    radial_z3_invariant = max_abs(u @ radial_hat @ u.conj().T - radial_hat) < 1.0e-14
    source_z3_invariant = max_abs(u @ source_raw @ u.conj().T - source_raw) < 1.0e-14
    radial_trace_zero = abs(np.trace(radial_hat).real) < 1.0e-14
    source_trace_nonzero = abs(np.trace(source_raw).real - 8.0) < 1.0e-14
    raw_chart_gram = [
        [float(hs_inner(source_raw, source_raw).real), float(hs_inner(source_raw, radial_hat).real)],
        [float(hs_inner(radial_hat, source_raw).real), float(hs_inner(radial_hat, radial_hat).real)],
    ]
    normalized_chart_gram = [
        [float(hs_inner(source_hat, source_hat).real), float(hs_inner(source_hat, radial_hat).real)],
        [float(hs_inner(radial_hat, source_hat).real), float(hs_inner(radial_hat, radial_hat).real)],
    ]
    normalized_chart_is_orthonormal = (
        abs(normalized_chart_gram[0][0] - 1.0) < 1.0e-14
        and abs(normalized_chart_gram[1][1] - 1.0) < 1.0e-14
        and abs(normalized_chart_gram[0][1]) < 1.0e-14
        and abs(normalized_chart_gram[1][0]) < 1.0e-14
    )

    one_source_gate_blocks = (
        "source-coordinate transport to canonical O_H not derivable"
        in statuses["source_coordinate_transport_gate"]
        and parents["source_coordinate_transport_gate"].get("proposal_allowed") is False
    )
    one_source_completion_blocks = (
        "source-coordinate transport not derivable"
        in statuses["source_coordinate_transport_completion"]
        and parents["source_coordinate_transport_completion"].get(
            "exact_negative_boundary_passed"
        )
        is True
        and parents["source_coordinate_transport_completion"].get("proposal_allowed")
        is False
    )
    z3_triplet_loaded = (
        "same-surface Z3 taste-triplet artifact" in statuses["same_surface_z3_taste_triplet"]
        and parents["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
    )
    taste_bridge_support_only = (
        parents["taste_condensate_oh_bridge_audit"].get("proposal_allowed") is False
        and parents["taste_condensate_oh_bridge_audit"].get(
            "taste_condensate_oh_bridge_audit_passed"
        )
        is True
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    source_higgs_rows_absent = (
        parents["source_higgs_builder"].get("input_present") is False
        and parents["source_higgs_readiness"].get("future_rows_present") is False
    )
    retained_route_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    futures = future_presence()
    action_cert = load(FUTURE_FILES["two_source_production_action"])
    action_absent_or_support_only = (
        futures["two_source_production_action"] is False
        or (
            action_cert.get("two_source_taste_radial_action_passed") is True
            and action_cert.get("proposal_allowed") is False
            and action_cert.get("operator_certificate_payload", {}).get(
                "canonical_higgs_operator_identity_passed"
            )
            is False
            and action_cert.get("forbidden_firewall", {}).get(
                "used_taste_radial_axis_as_canonical_oh"
            )
            is False
        )
    )
    closure_rows_absent = (
        futures["taste_radial_measurement_rows"] is False
        and futures["canonical_oh_certificate"] is False
        and futures["source_higgs_rows"] is False
    )
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("one-source-transport-gate-still-blocks", one_source_gate_blocks, statuses["source_coordinate_transport_gate"])
    report("one-source-completion-boundary-loaded", one_source_completion_blocks, statuses["source_coordinate_transport_completion"])
    report("same-surface-z3-triplet-loaded", z3_triplet_loaded, statuses["same_surface_z3_taste_triplet"])
    report("taste-bridge-support-only", taste_bridge_support_only, statuses["taste_condensate_oh_bridge_audit"])
    report("source-and-radial-axes-orthogonal", source_radial_orthogonal, f"<Ihat,Rhat>={hs_inner(source_hat, radial_hat).real:.3e}")
    report("taste-axis-orthonormal-frame", axis_orthogonal, "HS-normalized S_i frame")
    report("source-normalized", source_norm_ok, f"||Ihat||={hs_norm(source_hat):.12f}")
    report("radial-normalized", radial_norm_ok, f"||Rhat||={hs_norm(radial_hat):.12f}")
    report("radial-trace-zero", radial_trace_zero, f"Tr(Rhat)={np.trace(radial_hat).real:.3e}")
    report("source-trace-nonzero", source_trace_nonzero, f"Tr(I)={np.trace(source_raw).real:.1f}")
    report("source-z3-invariant", source_z3_invariant, "U I U^-1 = I")
    report("radial-z3-invariant", radial_z3_invariant, "U Rhat U^-1 = Rhat")
    report("two-source-normalized-chart-orthonormal", normalized_chart_is_orthonormal, str(normalized_chart_gram))
    report("canonical-oh-still-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-still-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("future-action-absent-or-support-only", action_absent_or_support_only, str(futures))
    report("closure-row-files-still-absent", closure_rows_absent, str(futures))
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))

    support_passed = (
        not missing
        and not proposal_allowed
        and one_source_gate_blocks
        and one_source_completion_blocks
        and z3_triplet_loaded
        and taste_bridge_support_only
        and source_radial_orthogonal
        and axis_orthogonal
        and source_norm_ok
        and radial_norm_ok
        and radial_trace_zero
        and source_trace_nonzero
        and source_z3_invariant
        and radial_z3_invariant
        and normalized_chart_is_orthonormal
        and canonical_oh_absent
        and source_higgs_rows_absent
        and action_absent_or_support_only
        and closure_rows_absent
        and retained_route_open
        and campaign_open
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / same-surface two-source taste-radial chart; "
            "canonical O_H and production rows absent"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface production action "
            "uses this second source axis and supplies C_sx/C_xx rows, or if a "
            "separate certificate identifies the taste-radial axis with canonical O_H"
        ),
        "hypothetical_axiom_status": (
            "Adding the h_taste source as dynamics is a new two-source surface "
            "until a production action or measurement-row certificate lands."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The artifact certifies an exact algebraic two-source chart only. "
            "It does not supply a same-source EW/Higgs action, canonical O_H "
            "identity/normalization, source-Higgs pole rows, or physical y_t readout."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "two_source_taste_radial_chart_support_passed": support_passed,
        "certificate_kind": "pr230_two_source_taste_radial_chart",
        "source_coordinate": {
            "raw_pr230_source_tangent": "I_8 from m_bare+s",
            "hs_normalized_source_tangent": "I_8/sqrt(8)",
            "raw_source_norm_squared": raw_chart_gram[0][0],
        },
        "new_second_source_axis": {
            "operator": "R_hat = (S0 + S1 + S2)/sqrt(24)",
            "S_i": "sigma_x on taste tensor factor i",
            "trace": float(np.trace(radial_hat).real),
            "hs_norm": hs_norm(radial_hat),
            "z3_invariant": radial_z3_invariant,
            "orthogonal_to_pr230_source": source_radial_orthogonal,
        },
        "chart_grams": {
            "raw_pr230_s_and_h_taste": raw_chart_gram,
            "hs_normalized_s_hat_and_h_taste": normalized_chart_gram,
        },
        "future_file_presence": futures,
        "future_action_status": (
            action_cert.get("actual_current_surface_status")
            if futures["two_source_production_action"]
            else "absent"
        ),
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not reparametrize the existing one-source line into O_H",
            "does not identify the taste-radial source with canonical O_H",
            "does not write source-Higgs C_sH/C_HH rows",
            "does not supply a same-source EW/Higgs production action",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "If pursuing the source-coordinate route, implement a genuine "
            "two-source production/action row for h_taste and measure C_sx/C_xx, "
            "then separately prove or reject whether x is canonical O_H.  "
            "Otherwise pivot to W/Z response, Schur A/B/C, neutral primitive, "
            "or strict scalar-LSZ authority."
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
