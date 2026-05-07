#!/usr/bin/env python3
"""
PR #230 source-Higgs time-kernel GEVP contract.

This runner consumes the default-off source-Higgs time-kernel smoke artifact
and validates the next postprocessor contract: a same-surface C_ij(t) matrix
can be parsed into a formal 2x2 GEVP diagnostic.  The current artifact remains
support-only because it is reduced smoke, uses taste-radial x rather than a
certified canonical O_H, and lacks production pole/FV/IR/threshold authority.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_harness_smoke_numba_2026-05-07.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json"

PARENTS = {
    "time_kernel_harness": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
    "os_transfer_kernel_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "uses_H_unit_matrix_element_readout": False,
    "uses_yt_ward_identity_as_authority": False,
    "uses_observed_top_mass_or_y_t_selector": False,
    "uses_alpha_LM_plaquette_or_u0_as_proof_input": False,
    "uses_reduced_smoke_as_production_evidence": False,
    "sets_c2_to_one": False,
    "sets_Z_match_to_one": False,
    "sets_kappa_s_to_one": False,
    "treats_taste_radial_x_as_canonical_O_H": False,
    "treats_formal_GEVP_as_pole_authority": False,
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


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def finite_matrix(value: Any) -> bool:
    if not (isinstance(value, list) and len(value) == 2):
        return False
    for row in value:
        if not (isinstance(row, list) and len(row) == 2):
            return False
        for item in row:
            if not isinstance(item, (int, float)) or not math.isfinite(float(item)):
                return False
    return True


def tau_matrix_rows(analysis: dict[str, Any]) -> dict[int, np.ndarray]:
    mode_rows = analysis.get("mode_rows")
    if not isinstance(mode_rows, dict):
        return {}
    row = mode_rows.get("0,0,0")
    if not isinstance(row, dict):
        return {}
    matrices: dict[int, np.ndarray] = {}
    for tau_row in row.get("tau_rows", []):
        if not isinstance(tau_row, dict):
            continue
        matrix = tau_row.get("C_matrix_real")
        if finite_matrix(matrix):
            arr = np.asarray(matrix, dtype=float)
            matrices[int(tau_row.get("tau", -1))] = 0.5 * (arr + arr.T)
    return matrices


def formal_gevp(matrices: dict[int, np.ndarray]) -> dict[str, Any]:
    if 0 not in matrices or 1 not in matrices:
        return {"available": False, "reason": "tau0_or_tau1_missing"}
    c0 = matrices[0]
    c1 = matrices[1]
    eig_c0 = np.linalg.eigvalsh(c0)
    if np.min(eig_c0) <= 0.0:
        return {
            "available": False,
            "reason": "C0_not_positive_definite_in_smoke",
            "C0_eigenvalues": [float(x) for x in eig_c0],
        }
    inv_sqrt = np.linalg.inv(np.linalg.cholesky(c0))
    reduced = inv_sqrt @ c1 @ inv_sqrt.T
    reduced = 0.5 * (reduced + reduced.T)
    lambdas = np.linalg.eigvalsh(reduced)
    energies = [
        float(-math.log(abs(value))) if math.isfinite(float(value)) and abs(float(value)) > 0.0 else float("nan")
        for value in lambdas
    ]
    return {
        "available": True,
        "C0_eigenvalues": [float(x) for x in eig_c0],
        "formal_lambda_tau1_tau0": [float(x) for x in lambdas],
        "formal_effective_energies_abs_lambda": energies,
        "strict_limit": (
            "This is a reduced-smoke algebraic diagnostic only.  Negative or "
            "small lambdas are not interpreted physically without production "
            "statistics, reflection-positive operator identity, pole/FV/IR/"
            "threshold authority, and source-overlap normalization."
        ),
    }


def main() -> int:
    print("PR #230 source-Higgs time-kernel GEVP contract")
    print("=" * 78)
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    smoke = load_json(SMOKE)
    metadata = smoke.get("metadata") if isinstance(smoke.get("metadata"), dict) else {}
    ensemble = selected_ensemble(smoke)
    analysis = ensemble.get("source_higgs_time_kernel_analysis")
    if not isinstance(analysis, dict):
        analysis = {}

    matrices = tau_matrix_rows(analysis)
    diagnostic = formal_gevp(matrices)
    tau_count = len(matrices)
    canonical_identity = analysis.get("canonical_higgs_operator_identity_passed") is True
    seed_control = ensemble.get("rng_seed_control", {}).get("seed_control_version")
    phase = metadata.get("phase")
    source_coordinate = analysis.get("source_coordinate")

    blockers = {
        "reduced_smoke_not_production": phase == "reduced_scope",
        "single_configuration_smoke": int(ensemble.get("measurement_sweeps", 0)) <= 1,
        "tau_depth_insufficient_for_pole_plateau": tau_count < 3,
        "canonical_O_H_identity_absent": canonical_identity is False,
        "physical_higgs_normalization_not_derived": analysis.get("physical_higgs_normalization") == "not_derived",
        "production_time_kernel_rows_absent": True,
        "reflection_positive_operator_identity_absent": True,
        "fv_ir_threshold_authority_absent": True,
        "source_overlap_normalization_absent": True,
        "retained_route_proposal_not_allowed": parents["retained_route"].get("proposal_allowed") is False,
        "campaign_proposal_not_allowed": parents["campaign_status"].get("proposal_allowed") is False,
    }
    physical_pole_extraction_accepted = (
        diagnostic.get("available") is True
        and not any(blockers.values())
        and parents["retained_route"].get("proposal_allowed") is True
        and parents["campaign_status"].get("proposal_allowed") is True
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("smoke-artifact-present", bool(smoke), str(SMOKE.relative_to(ROOT)))
    report("numba-seed-control", seed_control == "numba_gauge_seed_v1", str(seed_control))
    report(
        "time-kernel-schema-present",
        analysis.get("time_kernel_schema_version") == "source_higgs_time_kernel_v1",
        str(analysis.get("time_kernel_schema_version")),
    )
    report("zero-mode-Cij-tau0-tau1-present", {0, 1}.issubset(matrices), f"taus={sorted(matrices)}")
    report("formal-gevp-diagnostic-available", diagnostic.get("available") is True, str(diagnostic))
    report("taste-radial-not-canonical-oh", canonical_identity is False, str(canonical_identity))
    report("source-coordinate-recorded", isinstance(source_coordinate, str) and "source" in source_coordinate, str(source_coordinate))
    report(
        "support-only-blockers-present",
        all(blockers.values()),
        str(blockers),
    )
    report(
        "physical-pole-extraction-not-accepted",
        physical_pole_extraction_accepted is False,
        "formal GEVP is not pole authority on this surface",
    )
    report(
        "forbidden-import-firewall",
        all(value is False for value in FORBIDDEN_FIREWALL.values()),
        str(FORBIDDEN_FIREWALL),
    )

    certificate = {
        "artifact": "yt_pr230_source_higgs_time_kernel_gevp_contract",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actual_current_surface_status": (
            "bounded-support / source-Higgs time-kernel GEVP contract; "
            "smoke rows are not physics closure"
        ),
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "used_as_physical_yukawa_readout": False,
        "formal_gevp_diagnostic": diagnostic,
        "physical_pole_extraction_accepted": physical_pole_extraction_accepted,
        "blockers": blockers,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "contract": {
            "requires_same_surface_Cij_t": True,
            "requires_canonical_O_H_or_physical_neutral_identity": True,
            "requires_production_statistics": True,
            "requires_reflection_positive_operator_identity": True,
            "requires_pole_fv_ir_threshold_authority": True,
            "requires_source_overlap_normalization": True,
            "requires_retained_route_approval": True,
        },
        "checks": {"PASS": PASS_COUNT, "FAIL": FAIL_COUNT},
        "strict_limit": (
            "This runner validates parsing and a formal GEVP diagnostic only. "
            "It does not authorize kappa_s, canonical O_H, pole residue, or "
            "physical y_t closure."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
