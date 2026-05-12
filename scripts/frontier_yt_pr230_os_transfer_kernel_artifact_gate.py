#!/usr/bin/env python3
"""
PR #230 OS transfer-kernel artifact gate.

This runner targets the clean source-Higgs/neutral-transfer obligation from a
fresh angle: Osterwalder-Schrader reconstruction and the lattice transfer
matrix require Euclidean-time correlation kernels.  The current two-source
taste-radial chunks contain equal-time finite C_ss/C_sx/C_xx covariance rows
over configurations.  They do not contain a same-surface time-lag matrix
C_ij(t) that can determine a transfer/action generator, a pole residue, or a
canonical source-to-Higgs overlap.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json"
MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
COMBINER = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"

PARENTS = {
    "clean_source_higgs_route_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "same_surface_neutral_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "same_surface_neutral_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "neutral_offdiagonal_generator_attempt": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "two_source_row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "two_source_primitive_transfer_candidate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "orthogonal_top_exclusion_candidate": "outputs/yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate_2026-05-07.json",
    "strict_scalar_lsz_moment_fv": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "source_higgs_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
ZERO_MODE = "0,0,0"
FORBIDDEN_FIREWALL = {
    "uses_H_unit_matrix_element_readout": False,
    "uses_yt_ward_identity": False,
    "uses_observed_targets": False,
    "uses_alpha_lm_plaquette_u0": False,
    "uses_reduced_pilot_evidence": False,
    "sets_c2_to_one": False,
    "sets_z_match_to_one": False,
    "sets_kappa_s_to_one": False,
    "uses_pslq_or_value_recognition_selector": False,
    "treats_equal_time_covariance_as_transfer_matrix": False,
    "treats_configuration_timeseries_as_euclidean_time_kernel": False,
    "treats_taste_radial_x_as_canonical_O_H": False,
}

LITERATURE_REFRESH = [
    {
        "id": "osterwalder_schrader_1975",
        "citation": "K. Osterwalder and R. Schrader, Axioms for Euclidean Green's functions. II, Commun. Math. Phys. 42 (1975) 281-305.",
        "url": "https://www.osti.gov/biblio/4131077",
        "route_use": "reflection-positive Euclidean functions reconstruct the physical Hilbert/transfer structure only when the required Euclidean correlation functions are supplied",
        "pr230_boundary": "does not turn PR230 equal-time C_sx covariance rows into an action generator or canonical O_H overlap",
    },
    {
        "id": "luscher_transfer_matrix_1977",
        "citation": "M. Luscher, Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories, Commun. Math. Phys. 54 (1977) 283-292.",
        "url": "https://doi.org/10.1007/BF01614090",
        "route_use": "supports asking for an actual same-surface transfer kernel or time-lag correlator, not a static covariance proxy",
        "pr230_boundary": "transfer positivity by itself is not neutral-sector irreducibility, source-Higgs identity, or kappa_s authority",
    },
    {
        "id": "luscher_wolff_1990_gevp",
        "citation": "M. Luscher and U. Wolff, How to calculate the elastic scattering matrix in two-dimensional quantum field theories by numerical simulation, Nucl. Phys. B339 (1990) 222-252.",
        "url": "https://courses.physics.ucsd.edu/2016/Spring/physics142/Labs/FinalProjects/LuscherWolff.pdf",
        "route_use": "the GEVP route uses correlation matrices C(t) and C(t0) to extract levels and overlaps",
        "pr230_boundary": "current source/taste rows are configuration timeseries at fixed row definitions, not C_ij(t) matrices",
    },
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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def ready_manifest_rows(manifest: dict[str, Any], combiner: dict[str, Any]) -> list[dict[str, Any]]:
    commands = manifest.get("chunk_commands")
    ready = combiner.get("ready_chunk_indices")
    if not isinstance(commands, list) or not isinstance(ready, list):
        return []
    ready_indices = {int(index) for index in ready if isinstance(index, int)}
    return [
        row
        for row in commands
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and int(row["chunk_index"]) in ready_indices
    ]


def mode_has_euclidean_time_kernel(row: dict[str, Any]) -> bool:
    accepted_time_keys = {
        "euclidean_time_separations",
        "time_lag_correlation_matrix",
        "C_matrix_by_t",
        "C_ss_by_t",
        "C_sx_by_t",
        "C_xx_by_t",
        "C_sH_by_t",
        "C_HH_by_t",
        "transfer_kernel_rows",
        "gevp_C_t",
    }
    if any(key in row for key in accepted_time_keys):
        return True
    values = row.get("C_ss_timeseries")
    if isinstance(values, list) and values:
        sample = values[0]
        # These rows are configuration timeseries.  A tau field would be the
        # minimal signal that the scalar matrix is time-lag resolved.
        return isinstance(sample, dict) and any(key in sample for key in ("tau", "t", "time_separation"))
    return False


def parse_scalar_rows(manifest_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    issues: list[str] = []
    schema = {
        "chunks_with_top_tau_correlators": 0,
        "chunks_with_scalar_time_kernel": 0,
        "chunks_with_taste_radial_alias_metadata": 0,
        "taste_radial_alias_mismatch_count": 0,
        "source_mode_keys_seen": {},
    }
    for manifest_row in manifest_rows:
        output = ROOT / str(manifest_row.get("output", ""))
        if not output.exists():
            issues.append(f"chunk{manifest_row.get('chunk_index')} output absent")
            continue
        data = load_json(output)
        ensemble = selected_ensemble(data)
        top_corr = ensemble.get("correlators")
        if isinstance(top_corr, list) and top_corr and isinstance(top_corr[0], dict) and "tau" in top_corr[0]:
            schema["chunks_with_top_tau_correlators"] += 1
        source = ensemble.get("source_higgs_cross_correlator_analysis")
        if not isinstance(source, dict):
            issues.append(f"chunk{manifest_row.get('chunk_index')} source-higgs block absent")
            continue
        alias = source.get("two_source_taste_radial_row_aliases")
        if (
            isinstance(alias, dict)
            and alias.get("C_sx_aliases_C_sH_schema_field") is True
            and alias.get("C_xx_aliases_C_HH_schema_field") is True
        ):
            schema["chunks_with_taste_radial_alias_metadata"] += 1
        mode_rows = source.get("mode_rows")
        if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
            issues.append(f"chunk{manifest_row.get('chunk_index')} mode set mismatch")
            continue
        chunk_has_scalar_time_kernel = False
        for mode, mode_row in sorted(mode_rows.items()):
            if not isinstance(mode_row, dict):
                issues.append(f"chunk{manifest_row.get('chunk_index')} {mode} row not object")
                continue
            schema["source_mode_keys_seen"][mode] = sorted(set(schema["source_mode_keys_seen"].get(mode, [])) | set(mode_row.keys()))
            has_kernel = mode_has_euclidean_time_kernel(mode_row)
            chunk_has_scalar_time_kernel = chunk_has_scalar_time_kernel or has_kernel
            c_ss = mode_row.get("C_ss_real")
            c_sx = mode_row.get("C_sx_real")
            c_xx = mode_row.get("C_xx_real")
            c_sh = mode_row.get("C_sH_real")
            c_hh = mode_row.get("C_HH_real")
            if not (finite(c_ss) and finite(c_sx) and finite(c_xx)):
                issues.append(f"chunk{manifest_row.get('chunk_index')} {mode} nonfinite finite-row Gram")
                continue
            if finite(c_sh) and abs(float(c_sh) - float(c_sx)) > 1.0e-15:
                schema["taste_radial_alias_mismatch_count"] += 1
            if finite(c_hh) and abs(float(c_hh) - float(c_xx)) > 1.0e-15:
                schema["taste_radial_alias_mismatch_count"] += 1
            rows.append(
                {
                    "chunk_index": int(manifest_row["chunk_index"]),
                    "mode": mode,
                    "C_ss_real": float(c_ss),
                    "C_sx_real": float(c_sx),
                    "C_xx_real": float(c_xx),
                    "determinant": float(c_ss) * float(c_xx) - float(c_sx) * float(c_sx),
                    "has_scalar_euclidean_time_kernel": has_kernel,
                }
            )
        if chunk_has_scalar_time_kernel:
            schema["chunks_with_scalar_time_kernel"] += 1
    return rows, issues, schema


def mean_gram(rows: list[dict[str, Any]], mode: str) -> np.ndarray:
    selected = [row for row in rows if row.get("mode") == mode]
    if not selected:
        return np.eye(2)
    return np.asarray(
        [
            [statistics.fmean(float(row["C_ss_real"]) for row in selected), statistics.fmean(float(row["C_sx_real"]) for row in selected)],
            [statistics.fmean(float(row["C_sx_real"]) for row in selected), statistics.fmean(float(row["C_xx_real"]) for row in selected)],
        ],
        dtype=float,
    )


def offdiag_norm(matrix: np.ndarray) -> float:
    row = np.array(matrix, dtype=float)
    np.fill_diagonal(row, 0.0)
    return float(np.linalg.norm(row, ord=1))


def matrix_rows(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in np.asarray(matrix, dtype=float)]


def build_static_gram_witness(g: np.ndarray) -> dict[str, Any]:
    eigenvalues, eigenvectors = np.linalg.eigh(g)
    min_eval = float(np.min(eigenvalues))
    if min_eval <= 0.0:
        return {
            "static_gram_positive_definite": False,
            "minimum_gram_eigenvalue": min_eval,
            "witness_valid": False,
        }
    w = eigenvectors @ np.diag(np.sqrt(eigenvalues)) @ eigenvectors.T
    w_inv = np.linalg.inv(w)
    lam = np.diag([math.exp(-0.42), math.exp(-1.27)])
    theta = 0.43
    rotation = np.asarray(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )
    s_diag = lam
    s_rot = rotation @ lam @ rotation.T
    t_diag = w_inv @ s_diag @ w
    t_rot = w_inv @ s_rot @ w
    c1_diag = g @ t_diag
    c1_rot = g @ t_rot
    return {
        "static_gram_positive_definite": True,
        "minimum_gram_eigenvalue": min_eval,
        "same_C0_gram": matrix_rows(g),
        "candidate_A_whitened_transfer": matrix_rows(s_diag),
        "candidate_B_whitened_transfer": matrix_rows(s_rot),
        "candidate_A_transfer_in_source_x_basis": matrix_rows(t_diag),
        "candidate_B_transfer_in_source_x_basis": matrix_rows(t_rot),
        "candidate_A_C1_kernel": matrix_rows(c1_diag),
        "candidate_B_C1_kernel": matrix_rows(c1_rot),
        "candidate_A_C1_symmetric_error": float(np.linalg.norm(c1_diag - c1_diag.T, ord=1)),
        "candidate_B_C1_symmetric_error": float(np.linalg.norm(c1_rot - c1_rot.T, ord=1)),
        "candidate_A_offdiagonal_transfer_norm": offdiag_norm(t_diag),
        "candidate_B_offdiagonal_transfer_norm": offdiag_norm(t_rot),
        "C1_kernel_delta_norm": float(np.linalg.norm(c1_diag - c1_rot, ord=1)),
        "offdiagonal_transfer_delta_norm": float(abs(offdiag_norm(t_diag) - offdiag_norm(t_rot))),
        "witness_valid": True,
        "interpretation": (
            "The same equal-time positive Gram C(0)=G admits multiple positive "
            "self-adjoint transfer candidates once the Euclidean-time kernel is "
            "not supplied.  Static C_ss/C_sx/C_xx rows therefore cannot select "
            "the physical off-diagonal generator, pole residue, or O_H overlap."
        ),
    }


def required_artifact_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_operator_basis",
            "current_satisfied": False,
            "required_evidence": (
                "operators O_i include source and canonical O_H, or a certified "
                "physical neutral transfer basis with source/canonical-Higgs "
                "coordinates"
            ),
        },
        {
            "id": "euclidean_time_correlation_matrix",
            "current_satisfied": False,
            "required_evidence": (
                "same-ensemble C_ij(t) matrix for at least two positive Euclidean "
                "time separations plus C_ij(t0), with configuration covariance and "
                "seed/provenance metadata"
            ),
        },
        {
            "id": "reflection_positive_transfer_or_gevp",
            "current_satisfied": False,
            "required_evidence": (
                "OS/transfer-matrix or GEVP certificate extracting energies and "
                "overlap vectors from C(t) rather than static covariance"
            ),
        },
        {
            "id": "pole_fv_ir_threshold_authority",
            "current_satisfied": False,
            "required_evidence": "isolated pole, threshold separation, FV/IR/zero-mode limiting order",
        },
        {
            "id": "source_to_canonical_higgs_overlap",
            "current_satisfied": False,
            "required_evidence": "O_sp = O_H identity/normalization or Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))",
        },
        {
            "id": "claim_firewall",
            "current_satisfied": True,
            "required_evidence": "no H_unit, Ward identity, observed target, alpha/plaquette/u0, pilot, unit-normalization, or value-recognition selector",
        },
    ]


def main() -> int:
    print("PR #230 OS transfer-kernel artifact gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    ready_rows = ready_manifest_rows(manifest, combiner)
    scalar_rows, row_issues, schema = parse_scalar_rows(ready_rows)
    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")

    finite_grams_positive = bool(scalar_rows) and all(float(row["determinant"]) > 0.0 for row in scalar_rows)
    scalar_time_kernel_absent = schema["chunks_with_scalar_time_kernel"] == 0
    top_tau_present_but_not_scalar_matrix = (
        schema["chunks_with_top_tau_correlators"] == len(ready_rows)
        and scalar_time_kernel_absent
        and bool(ready_rows)
    )
    taste_radial_alias_firewall = (
        schema["chunks_with_taste_radial_alias_metadata"] == len(ready_rows)
        and schema["taste_radial_alias_mismatch_count"] == 0
        and bool(ready_rows)
    )
    static_witness = build_static_gram_witness(mean_gram(scalar_rows, ZERO_MODE))
    os_kernel_artifact_present = False
    same_surface_transfer_or_gevp_present = False
    clean_firewall = all(value is False for value in FORBIDDEN_FIREWALL.values())
    no_closure = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
        and os_kernel_artifact_present is False
        and taste_radial_alias_firewall
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("ready-row-packet-loaded", len(ready_rows) == ready_chunks, f"ready={ready_chunks}/{expected_chunks}")
    report("scalar-finite-rows-schema-clean", not row_issues, f"issues={row_issues[:4]}")
    report("finite-equal-time-gram-positive", finite_grams_positive, "C_ss*C_xx-C_sx^2 positive on ready rows")
    report("top-time-correlators-not-confused-with-scalar-kernel", top_tau_present_but_not_scalar_matrix, str(schema))
    report("taste-radial-csH-cHH-alias-firewall", taste_radial_alias_firewall, str(schema))
    report("scalar-euclidean-time-kernel-absent", scalar_time_kernel_absent, f"chunks_with_scalar_time_kernel={schema['chunks_with_scalar_time_kernel']}")
    report("static-gram-underdetermination-witness-valid", static_witness.get("witness_valid") is True, f"C1_delta={static_witness.get('C1_kernel_delta_norm')}")
    report("os-transfer-kernel-artifact-absent", not os_kernel_artifact_present, "no same-surface C_ij(t) row packet")
    report("same-surface-transfer-or-gevp-absent", not same_surface_transfer_or_gevp_present, "no transfer/GEVP certificate")
    report("forbidden-firewall-clean", clean_firewall, str(FORBIDDEN_FIREWALL))
    report("aggregate-still-denies-closure", no_closure, "retained/campaign proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact support plus negative boundary / OS transfer-kernel artifact "
            "absent; equal-time C_ss/C_sx/C_xx covariance rows do not determine "
            "a same-surface transfer generator, pole residue, or source-Higgs overlap"
        ),
        "conditional_surface_status": (
            "conditional-support if future production supplies same-surface "
            "Euclidean-time C_ij(t) matrices for source and canonical O_H or a "
            "certified physical neutral basis, then OS/transfer/GEVP pole and "
            "overlap authority can be evaluated"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current finite row packet is an equal-time source/taste-radial "
            "covariance diagnostic.  It is not a time-lag transfer kernel, not a "
            "canonical O_H row packet, and not scalar-LSZ normalization authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "os_transfer_kernel_artifact_present": os_kernel_artifact_present,
        "same_surface_transfer_or_gevp_present": same_surface_transfer_or_gevp_present,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "combined_rows_written": combiner.get("combined_rows_written"),
        "finite_equal_time_gram_rows": {
            "row_count": len(scalar_rows),
            "positive_definite": finite_grams_positive,
            "zero_mode_mean_gram": matrix_rows(mean_gram(scalar_rows, ZERO_MODE)),
        },
        "current_schema_boundary": schema,
        "static_gram_underdetermination_witness": static_witness,
        "required_future_artifact_contract": required_artifact_contract(),
        "literature_refresh": LITERATURE_REFRESH,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, c2=1, Z_match=1, or kappa_s=1",
            "does not treat configuration timeseries as Euclidean-time correlation kernels",
            "does not treat finite C_sx covariance as a transfer/action matrix",
            "does not treat aliased C_sH/C_HH schema fields as canonical source-Higgs rows",
            "does not treat taste-radial x as canonical O_H",
            "does not use OS, transfer-matrix, GEVP, D-module, tensor, PSLQ, or value-recognition method names as proof authority",
        ],
        "exact_next_action": (
            "Implement a same-surface scalar correlation-matrix production row: "
            "C_ss(t), C_sH(t), and C_HH(t) for certified canonical O_H, or "
            "C_ss(t), C_sx(t), and C_xx(t) plus a same-surface theorem identifying "
            "x with canonical O_H/physical neutral transfer.  The certificate must "
            "include reflection-positive/GEVP pole extraction, FV/IR/threshold "
            "authority, overlap normalization, covariance, seed metadata, and all "
            "claim firewalls."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
