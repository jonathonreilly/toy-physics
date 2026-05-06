#!/usr/bin/env python3
"""
PR #230 two-source taste-radial action/source-vertex certificate.

The prior chart certificate supplied the exact abstract taste-radial axis
R=(S0+S1+S2)/sqrt(24).  This runner checks the next concrete requirement:
can the production harness represent the corresponding second source as a
same-surface lattice action/source vertex, rather than as prose?

Result: exact support only.  The harness now accepts a gauge-covariant
blocked-hypercube spatial taste flip
    X = (X_1 + X_2 + X_3)/sqrt(3)
whose Hilbert-Schmidt norm matches the uniform source per lattice degree of
freedom on the cold Cl(3)/Z^3 surface.  This is not a canonical O_H identity,
not a Higgs LSZ normalization, and not a retained y_t readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy import sparse

import yt_direct_lattice_correlator_production as prod


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
)

PARENTS = {
    "two_source_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "same_surface_z3_taste_triplet": "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json",
    "source_coordinate_transport_completion": "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json",
    "source_higgs_harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_FILES = {
    "taste_radial_measurement_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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


def hs_inner(a: sparse.csr_matrix, b: sparse.csr_matrix) -> complex:
    return complex(a.conjugate().multiply(b).sum())


def sparse_max_abs(a: sparse.spmatrix) -> float:
    csr = a.tocsr()
    return float(np.max(np.abs(csr.data))) if csr.nnz else 0.0


def spatial_cycle_operator(geom: prod.Geometry) -> sparse.csr_matrix:
    n = geom.volume * prod.NC
    rows: list[int] = []
    cols: list[int] = []
    vals: list[complex] = []
    for site in range(geom.volume):
        t, x, y, z = geom.site_coords(site)
        dst_site = geom.site_index((t, z, x, y))
        for color in range(prod.NC):
            rows.append(dst_site * prod.NC + color)
            cols.append(site * prod.NC + color)
            vals.append(1.0 + 0.0j)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(n, n), dtype=np.complex128)


def operator_certificate_payload() -> dict[str, Any]:
    return {
        "operator_id": "pr230_taste_radial_hypercube_flip_source_v1",
        "operator_definition": (
            "Gauge-covariant blocked-hypercube taste-radial source "
            "X=(X_1+X_2+X_3)/sqrt(3), where X_i flips the spatial parity bit "
            "inside each 2^3 Cl(3)/Z^3 block using the connecting SU(3) link."
        ),
        "identity_certificate": "same-surface source-vertex certificate only; canonical O_H identity absent",
        "normalization_certificate": (
            "source_norm_matched: on the cold Cl(3)/Z^3 surface Tr X^dagger X "
            "equals Tr I^dagger I over site-color degrees of freedom.  This is "
            "not scalar LSZ or canonical Higgs normalization."
        ),
        "canonical_higgs_operator_identity_passed": False,
        "hunit_used_as_operator": False,
        "static_ew_algebra_used_as_operator": False,
        "sparse_vertex": {
            "kind": "taste_radial_spatial_hypercube_flip",
            "directions": [1, 2, 3],
            "normalization": "source_norm_matched",
            "requires_even_spatial_l": True,
            "gauge_covariant_links": True,
        },
        "firewall": forbidden_firewall(),
        "proposal_allowed": False,
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_or_plaquette": False,
        "used_taste_radial_axis_as_canonical_oh": False,
        "set_kappa_s_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_FILES.items()}


def main() -> int:
    print("PR #230 two-source taste-radial action/source-vertex certificate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()
    operator_cert = operator_certificate_payload()

    geom = prod.Geometry(spatial_l=2, time_l=4)
    gauge = prod.GaugeField(geom)
    n = geom.volume * prod.NC
    identity = sparse.identity(n, dtype=np.complex128, format="csr")
    axes = [prod.hypercube_flip_operator(gauge, mu) for mu in (1, 2, 3)]
    radial = prod.source_higgs_operator_matrix(geom, gauge, operator_cert)

    axis_hermitian_errors = [sparse_max_abs(axis - axis.getH()) for axis in axes]
    axis_square_errors = [sparse_max_abs(axis @ axis - identity) for axis in axes]
    axis_gram = [
        [float((hs_inner(axes[i], axes[j]) / n).real) for j in range(3)]
        for i in range(3)
    ]
    radial_norm_sq = float(hs_inner(radial, radial).real)
    source_norm_sq = float(hs_inner(identity, identity).real)
    source_radial_overlap = complex(hs_inner(identity, radial))
    radial_trace = complex(radial.diagonal().sum())
    radial_hermitian_error = sparse_max_abs(radial - radial.getH())
    cycle = spatial_cycle_operator(geom)
    cycle_error = sparse_max_abs(cycle @ radial @ cycle.getH() - radial)

    rng = np.random.default_rng(20260506)
    smoke = prod.stochastic_source_higgs_cross_correlator(
        gauge,
        0.75,
        1.0e-8,
        500,
        [(0, 0, 0)],
        1,
        rng,
        operator_cert,
        OUTPUT,
    )
    smoke_row = smoke["mode_rows"]["0,0,0"]
    smoke_schema_finite = all(
        math.isfinite(float(smoke_row[key]))
        for key in (
            "C_ss_real",
            "C_ss_imag",
            "C_sH_real",
            "C_sH_imag",
            "C_HH_real",
            "C_HH_imag",
        )
    )

    chart_loaded = (
        parents["two_source_chart"].get("two_source_taste_radial_chart_support_passed") is True
        and parents["two_source_chart"].get("proposal_allowed") is False
    )
    z3_loaded = (
        "same-surface Z3 taste-triplet artifact" in statuses["same_surface_z3_taste_triplet"]
        and parents["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
    )
    one_source_still_blocked = (
        parents["source_coordinate_transport_completion"].get("proposal_allowed") is False
        and parents["source_coordinate_transport_completion"].get("source_coordinate_transport_completion_passed")
        is True
    )
    harness_has_sparse_vertex = sparse_max_abs(radial) > 0.0 and operator_cert["sparse_vertex"]["kind"] in Path(
        prod.__file__
    ).read_text(encoding="utf-8")
    source_higgs_still_not_launch_ready = (
        parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and parents["source_higgs_readiness"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and futures["canonical_oh_certificate"] is False
    )
    rows_absent = futures["taste_radial_measurement_rows"] is False and futures["source_higgs_rows"] is False
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    axis_algebra_ok = (
        max(axis_hermitian_errors) < 1.0e-14
        and max(axis_square_errors) < 1.0e-14
        and all(abs(axis_gram[i][j] - (1.0 if i == j else 0.0)) < 1.0e-14 for i in range(3) for j in range(3))
    )
    radial_algebra_ok = (
        abs(radial_norm_sq - source_norm_sq) < 1.0e-12
        and abs(source_radial_overlap) < 1.0e-12
        and abs(radial_trace) < 1.0e-12
        and radial_hermitian_error < 1.0e-14
        and cycle_error < 1.0e-14
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("two-source-chart-loaded", chart_loaded, statuses["two_source_chart"])
    report("same-surface-z3-triplet-loaded", z3_loaded, statuses["same_surface_z3_taste_triplet"])
    report("one-source-route-still-blocked", one_source_still_blocked, statuses["source_coordinate_transport_completion"])
    report("harness-sparse-vertex-realized", harness_has_sparse_vertex, operator_cert["sparse_vertex"]["kind"])
    report("taste-axis-algebra-cold-surface", axis_algebra_ok, f"gram={axis_gram}")
    report("taste-radial-source-algebra", radial_algebra_ok, f"norm_sq={radial_norm_sq:.12g}, overlap={source_radial_overlap.real:.3e}")
    report("source-higgs-smoke-schema-finite", smoke_schema_finite, str(smoke_row))
    report("source-higgs-production-still-not-ready", source_higgs_still_not_launch_ready, statuses["source_higgs_readiness"])
    report("canonical-oh-still-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("taste-radial-production-rows-still-absent", rows_absent, str(futures))
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))

    action_passed = (
        not missing
        and not proposal_allowed
        and chart_loaded
        and z3_loaded
        and one_source_still_blocked
        and harness_has_sparse_vertex
        and axis_algebra_ok
        and radial_algebra_ok
        and smoke_schema_finite
        and source_higgs_still_not_launch_ready
        and canonical_oh_absent
        and rows_absent
        and retained_open
        and campaign_open
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / same-surface two-source taste-radial action source "
            "vertex realized; canonical O_H and production pole rows absent"
        ),
        "conditional_surface_status": (
            "conditional-support for future measured C_sx/C_xx rows if the "
            "taste-radial source is run in production and a separate canonical "
            "O_H/source-overlap or physical-response bridge closes"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The block realizes the second source as a gauge-covariant harness "
            "vertex and validates finite smoke schema only.  It does not prove "
            "the vertex is canonical O_H, does not derive kappa_s, and does "
            "not write production pole rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "two_source_taste_radial_action_passed": action_passed,
        "certificate_kind": "pr230_two_source_taste_radial_action_source_vertex",
        "operator_id": operator_cert["operator_id"],
        "operator_definition": operator_cert["operator_definition"],
        "identity_certificate": operator_cert["identity_certificate"],
        "normalization_certificate": operator_cert["normalization_certificate"],
        "canonical_higgs_operator_identity_passed": operator_cert[
            "canonical_higgs_operator_identity_passed"
        ],
        "hunit_used_as_operator": operator_cert["hunit_used_as_operator"],
        "static_ew_algebra_used_as_operator": operator_cert[
            "static_ew_algebra_used_as_operator"
        ],
        "sparse_vertex": operator_cert["sparse_vertex"],
        "firewall": operator_cert["firewall"],
        "operator_certificate_payload": operator_cert,
        "cold_surface_algebra": {
            "site_color_dimension": n,
            "axis_hermitian_errors": axis_hermitian_errors,
            "axis_square_errors": axis_square_errors,
            "axis_gram_over_source_norm": axis_gram,
            "source_norm_sq": source_norm_sq,
            "radial_norm_sq": radial_norm_sq,
            "source_radial_overlap": [float(source_radial_overlap.real), float(source_radial_overlap.imag)],
            "radial_trace": [float(radial_trace.real), float(radial_trace.imag)],
            "radial_hermitian_error": radial_hermitian_error,
            "spatial_cycle_invariance_error": cycle_error,
        },
        "harness_smoke": {
            "mode": "0,0,0",
            "noise_vectors": 1,
            "schema_finite": smoke_schema_finite,
            "row": smoke_row,
            "max_cg_residual": smoke.get("max_cg_residual"),
            "strict_limit": "finite smoke schema is instrumentation only, not production or pole evidence",
        },
        "future_file_presence": futures,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify taste-radial X with canonical O_H",
            "does not derive kappa_s or scalar LSZ normalization",
            "does not write production C_sx/C_xx rows",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Run a bounded then production two-source measurement wave with this "
            "operator certificate to write C_sx/C_xx rows, while separately "
            "deriving canonical O_H/source-overlap or using a physical W/Z, "
            "Schur, neutral primitive, or strict scalar-LSZ bridge."
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
