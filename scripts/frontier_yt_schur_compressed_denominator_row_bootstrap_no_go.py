#!/usr/bin/env python3
"""
PR #230 Schur compressed-denominator row-bootstrap no-go.

The Schur route needs same-surface A/B/C kernel rows.  A tempting shortcut is
to use an already-compressed scalar denominator D_eff(x), or D_eff'(pole), to
reconstruct those missing rows.  This runner proves that shortcut is
underdetermined: many same-surface Schur partitions have exactly the same
compressed denominator and pole derivative while carrying different A/B/C rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json"
FUTURE_ROW_FILES = (
    ROOT / "outputs" / "yt_schur_kernel_rows_2026-05-03.json",
    ROOT / "outputs" / "yt_schur_scalar_kernel_rows_2026-05-03.json",
)

PARENTS = {
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "scalar_denominator_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "kprime_attempt": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def schur_eff(a: float, b: float, c: float) -> float:
    return a - b * b / c


def make_partition(
    *,
    label: str,
    pole: float,
    slope: float,
    b0: float,
    b1: float,
    c0: float,
    c1: float,
) -> dict[str, Any]:
    def target_d(x: float) -> float:
        return slope * (x - pole)

    def b_of(x: float) -> float:
        return b0 + b1 * (x - pole)

    def c_of(x: float) -> float:
        return c0 + c1 * (x - pole)

    def a_of(x: float) -> float:
        b = b_of(x)
        c = c_of(x)
        return target_d(x) + b * b / c

    a0 = a_of(pole)
    a1 = slope + (2.0 * b0 * b1) / c0 - (b0 * b0 * c1) / (c0 * c0)
    rows = {
        "A_at_pole": a0,
        "B_at_pole": b0,
        "C_at_pole": c0,
        "A_prime_at_pole": a1,
        "B_prime_at_pole": b1,
        "C_prime_at_pole": c1,
    }
    return {
        "id": label,
        "rows": rows,
        "D_eff_at_pole": schur_eff(a0, b0, c0),
        "D_eff_prime_at_pole": (
            a1 - 2.0 * b0 * b1 / c0 + b0 * b0 * c1 / (c0 * c0)
        ),
        "functions": {
            "A": a_of,
            "B": b_of,
            "C": c_of,
            "D_eff": lambda x: schur_eff(a_of(x), b_of(x), c_of(x)),
            "target_D_eff": target_d,
        },
    }


def max_abs(values: list[float]) -> float:
    return max((abs(value) for value in values), default=0.0)


def evaluate_partition_pair(
    first: dict[str, Any],
    second: dict[str, Any],
    sample_points: list[float],
) -> dict[str, Any]:
    def fn(partition: dict[str, Any], name: str) -> Callable[[float], float]:
        return partition["functions"][name]

    first_d = [fn(first, "D_eff")(x) for x in sample_points]
    second_d = [fn(second, "D_eff")(x) for x in sample_points]
    target_d = [fn(first, "target_D_eff")(x) for x in sample_points]
    same_compressed = max_abs([a - b for a, b in zip(first_d, second_d)]) < 1.0e-12
    first_matches_target = max_abs([a - b for a, b in zip(first_d, target_d)]) < 1.0e-12
    second_matches_target = max_abs([a - b for a, b in zip(second_d, target_d)]) < 1.0e-12
    rows_differ = any(
        abs(first["rows"][key] - second["rows"][key]) > 1.0e-12
        for key in first["rows"]
    )
    c_nonzero = all(
        abs(fn(partition, "C")(x)) > 1.0e-9
        for partition in (first, second)
        for x in sample_points
    )
    same_pole_data = (
        abs(first["D_eff_at_pole"]) < 1.0e-12
        and abs(second["D_eff_at_pole"]) < 1.0e-12
        and abs(first["D_eff_prime_at_pole"] - second["D_eff_prime_at_pole"]) < 1.0e-12
        and first["D_eff_prime_at_pole"] != 0.0
    )
    return {
        "sample_points": sample_points,
        "first_D_eff_samples": first_d,
        "second_D_eff_samples": second_d,
        "target_D_eff_samples": target_d,
        "same_compressed_denominator_on_grid": same_compressed,
        "first_matches_target_denominator": first_matches_target,
        "second_matches_target_denominator": second_matches_target,
        "rows_differ": rows_differ,
        "orthogonal_block_nonzero_on_grid": c_nonzero,
        "same_pole_and_kprime_data": same_pole_data,
    }


def main() -> int:
    print("PR #230 Schur compressed-denominator row-bootstrap no-go")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_rows_present = [str(path.relative_to(ROOT)) for path in FUTURE_ROW_FILES if path.exists()]

    pole = 0.0
    slope = 0.73
    first = make_partition(label="partition_A", pole=pole, slope=slope, b0=0.22, b1=-0.04, c0=1.40, c1=0.10)
    second = make_partition(label="partition_B", pole=pole, slope=slope, b0=-0.51, b1=0.16, c0=2.30, c1=-0.18)
    sample_points = [-0.42, -0.17, 0.0, 0.11, 0.39]
    pair = evaluate_partition_pair(first, second, sample_points)

    parent_statuses = {name: status(cert) for name, cert in certs.items()}
    parents_loaded = not missing
    parents_open_or_support = (
        "Schur-complement K-prime sufficiency theorem" in parent_statuses["schur_sufficiency"]
        and "Schur K-prime row absence guard" in parent_statuses["schur_absence_guard"]
        and "Schur kernel row contract gate" in parent_statuses["schur_contract"]
        and "Schur row candidate extraction" in parent_statuses["schur_candidate_extraction"]
        and certs["schur_sufficiency"].get("proposal_allowed") is False
        and certs["schur_absence_guard"].get("proposal_allowed") is False
        and certs["schur_contract"].get("proposal_allowed") is False
        and certs["schur_candidate_extraction"].get("proposal_allowed") is False
    )
    bootstrap_no_go_passed = (
        parents_loaded
        and not proposal_allowed
        and parents_open_or_support
        and not future_rows_present
        and pair["same_compressed_denominator_on_grid"]
        and pair["first_matches_target_denominator"]
        and pair["second_matches_target_denominator"]
        and pair["same_pole_and_kprime_data"]
        and pair["rows_differ"]
        and pair["orthogonal_block_nonzero_on_grid"]
    )

    report("parent-certificates-present", parents_loaded, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-parent-surface-open-or-support", parents_open_or_support, "contract, sufficiency, absence, extraction parents loaded")
    report("future-schur-row-files-absent", not future_rows_present, f"present={future_rows_present}")
    report("same-compressed-denominator", pair["same_compressed_denominator_on_grid"], "two different Schur partitions share D_eff(x)")
    report("first-denominator-target-match", pair["first_matches_target_denominator"], "partition_A")
    report("second-denominator-target-match", pair["second_matches_target_denominator"], "partition_B")
    report("same-pole-and-kprime-data", pair["same_pole_and_kprime_data"], f"slope={slope}")
    report("abc-rows-differ", pair["rows_differ"], "row bootstrap is non-unique")
    report("orthogonal-block-nondegenerate", pair["orthogonal_block_nonzero_on_grid"], "C(x) nonzero on test grid")
    report("compressed-bootstrap-no-go-passed", bootstrap_no_go_passed, "D_eff and D_eff'(pole) do not reconstruct A/B/C rows")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Schur compressed-denominator row-bootstrap no-go"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface has no same-surface Schur A/B/C row file, and "
            "the compressed scalar denominator plus pole derivative are "
            "compatible with multiple inequivalent Schur partitions."
        ),
        "bare_retained_allowed": False,
        "bootstrap_no_go_passed": bootstrap_no_go_passed,
        "future_rows_present": future_rows_present,
        "counterfamily": {
            "shared_pole": pole,
            "shared_D_eff_prime_at_pole": slope,
            "partition_A_rows": first["rows"],
            "partition_B_rows": second["rows"],
            "pair_checks": pair,
        },
        "parent_statuses": parent_statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not produce Schur A/B/C rows",
            "does not claim physical top-Yukawa closure",
            "does not use external numerical targets or banned readout shortcuts",
            "does not package chunk outputs",
        ],
        "exact_next_action": (
            "Produce genuine same-surface Schur A/B/C kernel rows from a "
            "neutral scalar kernel theorem or measurement.  If those rows "
            "remain absent, pivot to O_H/source-Higgs rows, same-source W/Z "
            "response rows, scalar-LSZ moment-threshold-FV authority, or a "
            "neutral-sector irreducibility certificate."
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
