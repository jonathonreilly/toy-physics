#!/usr/bin/env python3
"""
PR #230 Schur K'(pole) row absence guard.

The Schur-complement support theorem gives a positive row contract:
same-surface neutral scalar kernel rows A/B/C and their pole derivatives would
compute D_eff'(pole).  This guard prevents the current finite source-only
C_ss(q) rows from being treated as those missing Schur rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_schur_kprime_row_absence_guard_2026-05-03.json"

PARENTS = {
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "finite_shell_identifiability": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
    "source_higgs_harness_absence_guard": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
    "wz_response_harness_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

SCAN_PATTERNS = [
    "outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json",
    "outputs/yt_pr230_fh_lsz_production_L12_T24_chunk*_2026-05-01.json",
    "outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk*/L12xT24/ensemble_measurement.json",
]

REQUIRED_ROW_KEYS = {
    "A_at_pole",
    "A_prime_at_pole",
    "B_at_pole",
    "B_prime_at_pole",
    "C_at_pole",
    "C_prime_at_pole",
    "C_inverse_at_pole",
    "D_eff_prime_at_pole",
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


def iter_scan_paths() -> list[Path]:
    paths: list[Path] = []
    for pattern in SCAN_PATTERNS:
        matches = sorted(ROOT.glob(pattern))
        paths.extend(path for path in matches if path.is_file())
    return paths


def collect_schur_row_hits(data: Any, path: str = "$") -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    if isinstance(data, dict):
        if "schur_kprime_kernel_rows" in data:
            rows = data.get("schur_kprime_kernel_rows")
            if isinstance(rows, list) and rows:
                complete = [
                    row
                    for row in rows
                    if isinstance(row, dict) and REQUIRED_ROW_KEYS.issubset(row)
                ]
                hits.append(
                    {
                        "json_path": f"{path}.schur_kprime_kernel_rows",
                        "row_count": len(rows),
                        "complete_row_count": len(complete),
                    }
                )
        if "neutral_scalar_kernel_partition" in data:
            partition = data.get("neutral_scalar_kernel_partition")
            complete = isinstance(partition, dict) and REQUIRED_ROW_KEYS.issubset(partition)
            hits.append(
                {
                    "json_path": f"{path}.neutral_scalar_kernel_partition",
                    "row_count": 1,
                    "complete_row_count": 1 if complete else 0,
                }
            )
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                hits.extend(collect_schur_row_hits(value, f"{path}.{key}"))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            if isinstance(value, (dict, list)):
                hits.extend(collect_schur_row_hits(value, f"{path}[{index}]"))
    return hits


def scan_current_outputs() -> dict[str, Any]:
    scanned = []
    row_hits = []
    metadata_absent_guards = []
    for path in iter_scan_paths():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rel = str(path.relative_to(ROOT))
        scanned.append(rel)
        for hit in collect_schur_row_hits(data):
            row_hits.append({"file": rel, **hit})
        metadata = data.get("metadata") if isinstance(data, dict) else None
        if isinstance(metadata, dict):
            guard = metadata.get("schur_kprime_kernel_rows")
            if isinstance(guard, dict) and guard.get("implementation_status") == "absent_guarded":
                metadata_absent_guards.append(rel)
    complete_hits = [hit for hit in row_hits if hit["complete_row_count"] > 0]
    return {
        "scanned_files": scanned,
        "scanned_file_count": len(scanned),
        "schur_row_hits": row_hits,
        "complete_schur_row_hits": complete_hits,
        "metadata_absent_guards": metadata_absent_guards,
        "current_schur_kernel_rows_present": bool(complete_hits),
    }


def finite_source_only_counterfamily() -> dict[str, Any]:
    x_pole = -0.2
    finite_points = [0.25, 0.5, 0.75, 1.0]
    epsilon = 0.17
    mixing_b = 0.31
    c_value = 1.4

    def product(x: float) -> float:
        out = 1.0
        for point in finite_points:
            out *= x - point
        return out

    def d1(x: float) -> float:
        return x - x_pole

    def d2(x: float) -> float:
        return d1(x) + epsilon * (x - x_pole) * product(x)

    source_rows = []
    for point in finite_points:
        d1_value = d1(point)
        d2_value = d2(point)
        source_rows.append(
            {
                "x": point,
                "D_eff_family_1": d1_value,
                "D_eff_family_2": d2_value,
                "C_ss_family_1": 1.0 / d1_value,
                "C_ss_family_2": 1.0 / d2_value,
                "absolute_c_ss_difference": abs(1.0 / d1_value - 1.0 / d2_value),
            }
        )

    d1_prime = 1.0
    d2_prime = 1.0 + epsilon * product(x_pole)
    family_1_rows = {
        "B_at_pole": 0.0,
        "C_at_pole": c_value,
        "A_at_pole": 0.0,
        "D_eff_prime_at_pole": d1_prime,
    }
    family_2_rows = {
        "B_at_pole": mixing_b,
        "C_at_pole": c_value,
        "A_at_pole": mixing_b * mixing_b / c_value,
        "D_eff_prime_at_pole": d2_prime,
    }
    return {
        "x_pole": x_pole,
        "finite_points": finite_points,
        "epsilon": epsilon,
        "source_rows": source_rows,
        "family_1_schur_rows_at_pole": family_1_rows,
        "family_2_schur_rows_at_pole": family_2_rows,
        "same_finite_source_rows": all(row["absolute_c_ss_difference"] < 1.0e-12 for row in source_rows),
        "same_pole_location": math.isclose(d1(x_pole), 0.0) and math.isclose(d2(x_pole), 0.0),
        "different_schur_rows": family_1_rows != family_2_rows,
        "different_d_eff_prime": abs(d1_prime - d2_prime) > 1.0e-6,
        "d_eff_prime_difference": d2_prime - d1_prime,
    }


def main() -> int:
    print("PR #230 Schur K'(pole) row absence guard")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    source = HARNESS.read_text(encoding="utf-8")
    scan = scan_current_outputs()
    witness = finite_source_only_counterfamily()

    schur_support_loaded = (
        "Schur-complement K-prime sufficiency theorem" in status(parents["schur_sufficiency"])
        and parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_closure_gate_passed") is False
    )
    source_only_boundary_loaded = (
        "source-functional LSZ identifiability theorem"
        in status(parents["source_functional_lsz_identifiability"])
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    finite_shell_boundary_loaded = (
        "finite-shell pole-fit identifiability no-go"
        in status(parents["finite_shell_identifiability"])
        and parents["finite_shell_identifiability"].get("proposal_allowed") is False
    )
    rank_repair_inputs_absent = (
        parents["source_higgs_harness_absence_guard"].get("proposal_allowed") is False
        and parents["wz_response_harness_absence_guard"].get("proposal_allowed") is False
    )
    retained_still_open = "retained closure not yet reached" in status(parents["retained_route"])
    harness_guard_present = '"schur_kprime_kernel_rows"' in source
    harness_guard_absent = '"implementation_status": "absent_guarded"' in source
    harness_rejects_source_only = '"finite_source_only_c_ss_is_not_schur_rows": True' in source
    harness_not_yukawa = '"used_as_physical_yukawa_readout": False' in source
    counterfamily_passed = (
        witness["same_finite_source_rows"]
        and witness["same_pole_location"]
        and witness["different_schur_rows"]
        and witness["different_d_eff_prime"]
    )
    guard_passed = (
        schur_support_loaded
        and source_only_boundary_loaded
        and finite_shell_boundary_loaded
        and rank_repair_inputs_absent
        and not scan["current_schur_kernel_rows_present"]
        and harness_guard_present
        and harness_guard_absent
        and harness_rejects_source_only
        and harness_not_yukawa
        and counterfamily_passed
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-sufficiency-loaded", schur_support_loaded, status(parents["schur_sufficiency"]))
    report("source-only-identifiability-boundary-loaded", source_only_boundary_loaded, status(parents["source_functional_lsz_identifiability"]))
    report("finite-shell-boundary-loaded", finite_shell_boundary_loaded, status(parents["finite_shell_identifiability"]))
    report("rank-repair-inputs-absent", rank_repair_inputs_absent, "source-Higgs and W/Z guards remain non-evidence")
    report("current-schur-rows-absent", not scan["current_schur_kernel_rows_present"], f"complete_hits={len(scan['complete_schur_row_hits'])}")
    report("harness-schur-guard-present", harness_guard_present, "schur_kprime_kernel_rows metadata block")
    report("harness-schur-guard-absent", harness_guard_absent, "absent_guarded")
    report("harness-rejects-source-only-c-ss", harness_rejects_source_only, "finite_source_only_c_ss_is_not_schur_rows")
    report("harness-not-yukawa-readout", harness_not_yukawa, "used_as_physical_yukawa_readout False")
    report("finite-source-only-counterfamily-passed", counterfamily_passed, f"Dprime_delta={witness['d_eff_prime_difference']:.6g}")
    report("retained-route-still-open", retained_still_open, status(parents["retained_route"]))
    report("guard-passed", guard_passed, "absence guard and counterfamily checks")

    result = {
        "actual_current_surface_status": (
            "bounded-support / Schur K-prime row absence guard; finite source-only rows rejected"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The guard proves that current finite source-only C_ss rows are not "
            "Schur A/B/C kernel rows and confirms that no complete current "
            "Schur row certificate exists."
        ),
        "bare_retained_allowed": False,
        "schur_kprime_row_absence_guard_passed": guard_passed,
        "current_schur_kernel_rows_present": scan["current_schur_kernel_rows_present"],
        "finite_source_only_counterfamily_passed": counterfamily_passed,
        "scan": scan,
        "counterfamily": witness,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer Schur A/B/C rows from C_ss(q), dE_top/ds, or finite source slopes",
            "does not set kappa_s=1, D_eff'(pole)=1, or O_sp=O_H",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Produce explicit same-surface Schur A/B/C kernel rows and pole "
            "derivatives, or use a non-source rank-repair route: certified "
            "O_H/C_sH/C_HH pole rows or same-source W/Z response rows with "
            "identity certificates."
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
