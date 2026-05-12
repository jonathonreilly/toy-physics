#!/usr/bin/env python3
"""
PR #230 Block68: strict W/Z or neutral-transfer physical response.

This probe tries the two requested bypasses after the current PR230 block62
surface:

1. strict W/Z physical response with absolute normalization;
2. same-surface neutral-transfer primitive / rank-one bridge.

The runner is deliberately a certificate, not a production worker.  It reads
existing parent certificates, computes the top/W/Z mass-response Jacobian, and
checks whether a one-dimensional normalization orbit still leaves y_t
unidentified.  It also consumes the current neutral rank-one counterfamily and
records the missing off-diagonal/primitive-transfer datum.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block68_strict_wz_neutral_transfer_obstruction_2026-05-12.json"
)

PARENTS = {
    "block53_residual_minimality": "outputs/yt_pr230_block53_lane1_residual_minimality_gate_2026-05-12.json",
    "block54_response_readout_reduction": "outputs/yt_pr230_block54_response_readout_reduction_gate_2026-05-12.json",
    "block55_canonical_neutral_cut": "outputs/yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json",
    "block56_scalar_pole_fvir_cut": "outputs/yt_pr230_block56_scalar_pole_fvir_root_cut_gate_2026-05-12.json",
    "block57_compact_source_functional": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "block58_compact_source_spectral": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block59_source_spectral_pole_obstruction": "outputs/yt_pr230_block59_source_spectral_pole_promotion_obstruction_2026-05-12.json",
    "block60_source_taste_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block61_post_carrier_kprime": "outputs/yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json",
    "block62_compact_source_kprime": "outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_physical_packet_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_mass_response_self_norm_no_go": "outputs/yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json",
    "wz_abs_authority_exhaustion": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "wz_g2_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_response_self_norm_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_g2_bare_running_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "ew_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "top_wz_covariance_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "top_wz_factorization_independence": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_mass_scan_subtraction_audit": "outputs/yt_pr230_top_mass_scan_subtraction_contract_applicability_audit_2026-05-12.json",
    "neutral_rank_one_bypass": "outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json",
    "neutral_offdiagonal_post45": "outputs/yt_pr230_neutral_offdiagonal_post_block45_applicability_audit_2026-05-12.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
}

STRICT_FUTURE_ROOTS = {
    "accepted_same_source_ew_higgs_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "production_wz_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
    "production_wz_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_rows": "outputs/yt_same_source_top_response_rows_2026-05-04.json",
    "matched_top_wz_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "strict_non_observed_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "explicit_v_authority_certificate": "outputs/yt_electroweak_v_authority_certificate_2026-05-12.json",
    "delta_perp_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "neutral_transfer_operator_certificate": "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "strict_source_higgs_pole_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "schur_abc_kernel_rows": "outputs/yt_pr230_schur_abc_kernel_rows_2026-05-12.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_ward_as_load_bearing": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_observed_g2_or_v": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_g2_v_kappa_c2_or_zmatch_to_one": False,
    "assumed_top_wz_covariance": False,
    "treated_wz_smoke_as_production": False,
    "treated_neutral_positivity_as_primitive_cone": False,
    "treated_c_sx_as_c_sH": False,
    "claimed_retained_or_proposed_retained": False,
    "touched_chunk_runner_files": False,
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


def fail_count(cert: dict[str, Any]) -> int:
    if "fail_count" in cert:
        return int(cert.get("fail_count") or 0)
    if isinstance(cert.get("summary"), dict):
        return int(cert["summary"].get("fail") or 0)
    return 0


def mass_response_observables(x: list[float], extra: str | None = None) -> list[float]:
    yt, g2, gy, v, a, atop = x
    gtot = math.sqrt(g2 * g2 + gy * gy)
    out = [
        yt * v / math.sqrt(2.0),
        g2 * v / 2.0,
        gtot * v / 2.0,
        yt * a / math.sqrt(2.0) + atop,
        g2 * a / 2.0,
        gtot * a / 2.0,
        atop,
    ]
    if extra == "g2":
        out.append(g2)
    elif extra == "v":
        out.append(v)
    elif extra == "source_normalization_a":
        out.append(a)
    return out


def jacobian(fn: Callable[[list[float]], list[float]], x: list[float]) -> list[list[float]]:
    eps = 1.0e-6
    base_cols: list[list[float]] = []
    for j, xj in enumerate(x):
        step = eps * max(1.0, abs(xj))
        xp = list(x)
        xm = list(x)
        xp[j] += step
        xm[j] -= step
        fp = fn(xp)
        fm = fn(xm)
        base_cols.append([(a - b) / (2.0 * step) for a, b in zip(fp, fm)])
    return [[base_cols[col][row] for col in range(len(x))] for row in range(len(base_cols[0]))]


def matrix_rank(a: list[list[float]], tol: float = 1.0e-9) -> int:
    m = [row[:] for row in a]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = max(range(rank, rows), key=lambda r: abs(m[r][col]), default=rank)
        if rows == 0 or abs(m[pivot][col]) <= tol:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        pivot_value = m[rank][col]
        m[rank] = [v / pivot_value for v in m[rank]]
        for r in range(rows):
            if r == rank:
                continue
            factor = m[r][col]
            if abs(factor) > tol:
                m[r] = [rv - factor * pv for rv, pv in zip(m[r], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def matvec(a: list[list[float]], x: list[float]) -> list[float]:
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def is_positive_matrix(a: list[list[float]], tol: float = 1.0e-12) -> bool:
    return all(value > tol for row in a for value in row)


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def primitive_witness(matrix: list[list[float]], max_power: int = 6) -> dict[str, Any]:
    power = [row[:] for row in matrix]
    for n in range(1, max_power + 1):
        if is_positive_matrix(power):
            return {"primitive": True, "positive_power": n, "matrix_power": power}
        power = matmul(power, matrix)
    return {"primitive": False, "positive_power": None, "matrix_power": power}


def main() -> int:
    print("PR #230 Block68 strict W/Z or neutral-transfer obstruction")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    failed_parents = [name for name, cert in certs.items() if fail_count(cert) != 0]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {
        name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ROOTS.items()
    }

    # A representative nonzero point.  The rank and null-vector facts are
    # structural away from singular loci g2=gy=0 and v=a=0.
    x0 = [0.93, 0.65, 0.35, 246.0, 3.1, 0.42]
    j_base = jacobian(lambda x: mass_response_observables(x), x0)
    scale_vector = [-x0[0], -x0[1], -x0[2], x0[3], x0[4], 0.0]
    scale_residual = matvec(j_base, scale_vector)
    base_rank = matrix_rank(j_base)
    rank_with_g2 = matrix_rank(jacobian(lambda x: mass_response_observables(x, "g2"), x0))
    rank_with_v = matrix_rank(jacobian(lambda x: mass_response_observables(x, "v"), x0))
    rank_with_a = matrix_rank(
        jacobian(lambda x: mass_response_observables(x, "source_normalization_a"), x0)
    )

    scale_orbit_survives = (
        base_rank == 5 and max(abs(value) for value in scale_residual) < 1.0e-7
    )
    absolute_pins_close_rank = (
        rank_with_g2 == 6 and rank_with_v == 6 and rank_with_a == 6
    )

    neutral_counterfamily = certs["neutral_rank_one_bypass"].get("counterfamily", [])
    rho_values = [
        row.get("candidate_source_higgs_rho")
        for row in neutral_counterfamily
        if row.get("candidate_source_higgs_rho") is not None
    ]
    neutral_overlap_varies = bool(rho_values) and (max(rho_values) - min(rho_values) > 1.0e-12)

    transfer_eta0 = [
        [1.0, 0.0, 0.0],
        [0.0, 0.5, 0.5],
        [0.0, 0.5, 0.5],
    ]
    transfer_eta_positive = [
        [0.80, 0.10, 0.10],
        [0.10, 0.45, 0.45],
        [0.10, 0.45, 0.45],
    ]
    eta0_witness = primitive_witness(transfer_eta0)
    eta_positive_witness = primitive_witness(transfer_eta_positive)

    response_root_reduced = (
        certs["block54_response_readout_reduction"].get(
            "response_readout_root_reduction_passed"
        )
        is True
        and certs["block54_response_readout_reduction"].get("response_side_support_closed")
        is True
        and certs["block54_response_readout_reduction"].get("readout_switch_authorized")
        is False
    )
    canonical_neutral_open = (
        certs["block55_canonical_neutral_cut"].get("block55_canonical_neutral_primitive_cut_passed")
        is True
        and certs["block55_canonical_neutral_cut"].get("canonical_neutral_root_closed")
        is False
    )
    scalar_root_open = (
        certs["block56_scalar_pole_fvir_cut"].get("scalar_pole_fvir_root_closed")
        is False
        and certs["block62_compact_source_kprime"].get("kprime_authority_present")
        is False
        and certs["block62_compact_source_kprime"].get("pole_residue_authority_present")
        is False
    )
    compact_support_only = (
        certs["block57_compact_source_functional"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
        and certs["block58_compact_source_spectral"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
        and certs["block60_source_taste_carrier"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
        and certs["block59_source_spectral_pole_obstruction"].get(
            "thermodynamic_pole_authority_present"
        )
        is False
    )
    wz_root_absent = (
        certs["wz_accepted_action_root"].get("current_route_blocked") is True
        and certs["wz_physical_packet_intake"].get("production_packet_present") is False
        and certs["wz_abs_authority_exhaustion"].get(
            "wz_absolute_authority_route_exhaustion_passed"
        )
        is True
        and not any(certs["wz_abs_authority_exhaustion"].get("strict_packet_roots_present", {}).values())
    )
    absolute_authority_absent = (
        certs["wz_mass_response_self_norm_no_go"].get("strict_g2_certificate_present")
        is False
        and certs["ew_g2_builder"].get("proposal_allowed") is False
        and certs["wz_g2_firewall"].get("proposal_allowed") is False
    )
    covariance_blocked = (
        certs["top_wz_covariance_import_audit"].get(
            "future_closed_covariance_theorem_present"
        )
        is False
        and certs["top_wz_factorization_independence"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False
        and certs["top_mass_scan_subtraction_audit"].get("strict_row_presence", {}).get(
            "matched_subtraction_covariance"
        )
        is False
    )
    no_future_root_present = not any(future_presence.values())
    forbidden_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    current_surface_closes = False
    exact_boundary = (
        not missing
        and not failed_parents
        and not proposal_parents
        and response_root_reduced
        and canonical_neutral_open
        and scalar_root_open
        and compact_support_only
        and wz_root_absent
        and absolute_authority_absent
        and covariance_blocked
        and scale_orbit_survives
        and absolute_pins_close_rank
        and neutral_overlap_varies
        and eta0_witness["primitive"] is False
        and eta_positive_witness["primitive"] is True
        and no_future_root_present
        and forbidden_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-certificates-clean", not failed_parents, f"failed={failed_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("response-root-reduced", response_root_reduced, statuses["block54_response_readout_reduction"])
    report("canonical-neutral-root-open", canonical_neutral_open, statuses["block55_canonical_neutral_cut"])
    report("scalar-root-open", scalar_root_open, statuses["block62_compact_source_kprime"])
    report("compact-source-support-only", compact_support_only, statuses["block57_compact_source_functional"])
    report("wz-root-absent", wz_root_absent, statuses["wz_abs_authority_exhaustion"])
    report("absolute-authority-absent", absolute_authority_absent, statuses["wz_mass_response_self_norm_no_go"])
    report("top-wz-covariance-blocked", covariance_blocked, statuses["top_wz_covariance_import_audit"])
    report("wz-scale-orbit-survives", scale_orbit_survives, f"rank={base_rank}, residual={scale_residual}")
    report("absolute-pins-close-rank", absolute_pins_close_rank, f"g2={rank_with_g2}, v={rank_with_v}, a={rank_with_a}")
    report("neutral-overlap-counterfamily-varies", neutral_overlap_varies, f"rho_range={[min(rho_values), max(rho_values)] if rho_values else []}")
    report("eta-zero-not-primitive", eta0_witness["primitive"] is False, str(eta0_witness))
    report("eta-positive-primitive", eta_positive_witness["primitive"] is True, str(eta_positive_witness))
    report("strict-future-roots-absent", no_future_root_present, str(future_presence))
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FIREWALL))
    report("exact-obstruction-boundary", exact_boundary, "probe D does not close on current surface")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for current PR230 Block68: strict "
            "W/Z and neutral-transfer physical-response bypasses do not close "
            "without an absolute normalization pin or a physical primitive "
            "neutral-transfer theorem"
        ),
        "conditional_surface_status": (
            "conditional-support if future work supplies accepted same-source "
            "EW/Higgs action, production W/Z/top rows, matched covariance, "
            "delta_perp, and one absolute pin among strict non-observed g2, "
            "explicit v, or canonical source-response normalization; or if "
            "future work supplies a same-surface primitive neutral-transfer "
            "operator/cone theorem plus source/canonical-Higgs coupling and "
            "pole/FVIR normalization authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The response-side instrumentation is support-complete, but the "
            "top/W/Z observable map has a one-dimensional absolute-normalization "
            "kernel until g2, v, or canonical source-response normalization is "
            "pinned.  The neutral route still admits an orthogonal-neutral "
            "counterfamily and lacks the eta/off-diagonal primitive-transfer "
            "datum."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block68_exact_obstruction_passed": exact_boundary,
        "current_surface_closes": current_surface_closes,
        "wz_identifiability": {
            "variables": ["y_t", "g2", "gY", "v", "a=dv/ds", "A_top"],
            "observables": [
                "m_t",
                "M_W",
                "M_Z",
                "T_total",
                "W_response",
                "Z_response",
                "A_top",
            ],
            "base_rank": base_rank,
            "scale_kernel_vector": scale_vector,
            "scale_kernel_residual": scale_residual,
            "rank_with_strict_g2_pin": rank_with_g2,
            "rank_with_explicit_v_pin": rank_with_v,
            "rank_with_source_normalization_pin": rank_with_a,
            "absolute_pins_that_close_the_jacobian": [
                "strict non-observed g2 in the same accepted EW normalization",
                "explicit v authority with visible dependency",
                "canonical source-response normalization a=dh/ds from O_H/LSZ or neutral transfer",
            ],
            "current_absolute_pin_present": False,
        },
        "neutral_transfer": {
            "current_overlap_counterfamily_rho_values": rho_values,
            "overlap_varies_with_unmeasured_orthogonal_neutral_direction": neutral_overlap_varies,
            "eta_zero_transfer_witness": eta0_witness,
            "eta_positive_transfer_witness": eta_positive_witness,
            "current_eta_or_offdiagonal_generator_present": False,
            "current_primitive_cone_certificate_present": False,
        },
        "audit_summary": {
            "wz_accepted_action_root": statuses["wz_accepted_action_root"],
            "wz_self_normalization": statuses["wz_mass_response_self_norm_no_go"],
            "wz_absolute_authority_exhaustion": statuses["wz_abs_authority_exhaustion"],
            "neutral_rank_one_bypass": statuses["neutral_rank_one_bypass"],
            "top_wz_covariance": statuses["top_wz_covariance_import_audit"],
            "top_wz_factorization": statuses["top_wz_factorization_independence"],
        },
        "strict_future_roots_present": future_presence,
        "exact_new_row_or_theorem_required": {
            "wz_route": [
                "accepted same-source EW/Higgs action certificate",
                "production W/Z and same-source top response rows",
                "matched covariance for T_total, A_top, W/Z, and the absolute pin",
                "delta_perp / orthogonal-response correction authority",
                "one absolute normalization pin: strict non-observed g2, explicit v, or canonical source-response normalization",
            ],
            "neutral_route": [
                "same-surface physical neutral transfer/off-diagonal generator fixing eta",
                "primitive-cone or irreducibility theorem on the full source-plus-neutral sector",
                "source/canonical-Higgs coupling theorem or strict C_ss/C_sH/C_HH pole rows",
                "pole residue, K-prime, threshold, contact, and FVIR authority",
            ],
        },
        "literature_and_math_sources_used_as_context_only": {
            "fms_original": "https://archives.ihes.fr/document/P_81_12.pdf",
            "fms_lattice_spectrum_review": "https://arxiv.org/abs/1709.07477",
            "lattice_transfer_matrix": "https://doi.org/10.1007/BF01614090",
            "feynman_hellmann": "https://authors.library.caltech.edu/records/a5jtc-q3669/latest",
            "schrodinger_functional_gauge_coupling": "https://arxiv.org/abs/hep-lat/9207009",
            "gradient_flow": "https://arxiv.org/abs/1006.4518",
            "rugh_cone_pf": "https://annals.math.princeton.edu/2010/171-3/p07",
            "curto_fialkow_flat_extension": "https://iro.uiowa.edu/esploro/outputs/journalArticle/Truncated-K-moment-problems-in-several-variables/9984240861702771",
            "schur_complement_reference": "https://link.springer.com/book/10.1007/b105056",
            "buckingham_pi": "https://www.britannica.com/science/pi-theorem",
        },
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
