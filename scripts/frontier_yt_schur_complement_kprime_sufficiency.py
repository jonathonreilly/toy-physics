#!/usr/bin/env python3
"""
PR #230 Schur-complement K'(pole) sufficiency theorem.

This support block sharpens the scalar denominator route.  If the neutral
scalar kernel is partitioned into a source-pole coordinate A and orthogonal
neutral coordinates C with mixing B, then the effective same-source denominator
is the Schur complement

    D_eff(x) = A(x) - B(x)^T C(x)^-1 B(x).

The derivative D_eff'(x_pole) is therefore computable from same-surface kernel
rows A, B, C and their x-derivatives.  The current PR #230 surface does not
provide those rows, so this is exact support / sufficiency, not closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_schur_complement_kprime_sufficiency_2026-05-03.json"

PARENTS = {
    "feshbach_response_boundary": "outputs/yt_feshbach_operator_response_boundary_2026-05-01.json",
    "determinant_gate": "outputs/yt_scalar_pole_determinant_gate_2026-05-01.json",
    "eigen_derivative_gate": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "kprime_closure_attempt": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
    "scalar_denominator_closure": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
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


def schur_value(a: float, b: float, c: float) -> float:
    return a - b * b / c


def schur_derivative(a1: float, b0: float, b1: float, c0: float, c1: float) -> float:
    return a1 - 2.0 * b0 * b1 / c0 + (b0 * b0 * c1) / (c0 * c0)


def finite_difference_witness() -> dict[str, Any]:
    x0 = -0.37
    a0, a1 = 0.82, 0.31
    b0, b1 = 0.24, -0.08
    c0, c1 = 1.35, 0.22

    # Shift A so the Schur complement has a pole at x0: D_eff(x0)=0.
    def raw_a(x: float) -> float:
        return a0 + a1 * (x - x0)

    def b(x: float) -> float:
        return b0 + b1 * (x - x0)

    def c(x: float) -> float:
        return c0 + c1 * (x - x0)

    shift = schur_value(raw_a(x0), b(x0), c(x0))

    def a(x: float) -> float:
        return raw_a(x) - shift

    def d_eff(x: float) -> float:
        return schur_value(a(x), b(x), c(x))

    analytic = schur_derivative(a1, b0, b1, c0, c1)
    eps = 1.0e-5
    finite_diff = (d_eff(x0 + eps) - d_eff(x0 - eps)) / (2.0 * eps)
    return {
        "x_pole": x0,
        "A_at_pole": a(x0),
        "B_at_pole": b0,
        "C_at_pole": c0,
        "A_prime": a1,
        "B_prime": b1,
        "C_prime": c1,
        "D_eff_at_pole": d_eff(x0),
        "D_eff_prime_formula": analytic,
        "D_eff_prime_finite_difference": finite_diff,
        "absolute_error": abs(analytic - finite_diff),
        "formula_terms": {
            "A_prime": a1,
            "-2_B_Bprime_over_C": -2.0 * b0 * b1 / c0,
            "B2_Cprime_over_C2": (b0 * b0 * c1) / (c0 * c0),
        },
    }


def main() -> int:
    print("PR #230 Schur-complement K'(pole) sufficiency")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = finite_difference_witness()

    feshbach_support_loaded = "Feshbach response boundary" in status(parents["feshbach_response_boundary"])
    determinant_support_loaded = "scalar pole determinant gate" in status(parents["determinant_gate"])
    eigen_support_loaded = "scalar ladder eigen-derivative gate" in status(parents["eigen_derivative_gate"])
    kprime_still_open = "K-prime closure attempt blocked" in status(parents["kprime_closure_attempt"])
    denominator_still_open = "scalar denominator theorem closure attempt blocked" in status(
        parents["scalar_denominator_closure"]
    )
    source_only_identifiability_boundary = "source-functional LSZ identifiability theorem" in status(
        parents["source_functional_lsz_identifiability"]
    )

    formula_matches_finite_difference = witness["absolute_error"] < 1.0e-10
    current_rows_present = False
    current_closure_gate_passed = False
    schur_sufficiency_theorem_passed = (
        formula_matches_finite_difference
        and feshbach_support_loaded
        and determinant_support_loaded
        and eigen_support_loaded
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("feshbach-support-loaded", feshbach_support_loaded, status(parents["feshbach_response_boundary"]))
    report("determinant-support-loaded", determinant_support_loaded, status(parents["determinant_gate"]))
    report("eigen-derivative-support-loaded", eigen_support_loaded, status(parents["eigen_derivative_gate"]))
    report("schur-derivative-matches-finite-difference", formula_matches_finite_difference, f"error={witness['absolute_error']:.3e}")
    report("kprime-still-open", kprime_still_open, status(parents["kprime_closure_attempt"]))
    report("scalar-denominator-still-open", denominator_still_open, status(parents["scalar_denominator_closure"]))
    report(
        "source-only-identifiability-boundary-loaded",
        source_only_identifiability_boundary,
        status(parents["source_functional_lsz_identifiability"]),
    )
    report("current-schur-kernel-rows-absent", not current_rows_present, f"current_rows_present={current_rows_present}")
    report("sufficiency-theorem-passed", schur_sufficiency_theorem_passed, "D_eff' formula checked")
    report("support-not-current-closure", not current_closure_gate_passed, f"current_closure_gate_passed={current_closure_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact-support / Schur-complement K-prime sufficiency theorem; current rows absent"
        ),
        "conditional_surface_status": (
            "If same-surface production or theorem rows provide A, B, C and "
            "their pole derivatives in a certified neutral scalar kernel "
            "partition, then D_eff'(pole) and the same-source scalar LSZ "
            "normalization are computable by the Schur-complement formula."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The sufficiency formula is exact support, but the required "
            "same-surface A/B/C kernel rows and derivatives are absent, and "
            "K'(pole) / scalar denominator closure remains open."
        ),
        "bare_retained_allowed": False,
        "schur_sufficiency_theorem_passed": schur_sufficiency_theorem_passed,
        "current_schur_kernel_rows_present": current_rows_present,
        "current_closure_gate_passed": current_closure_gate_passed,
        "witness": witness,
        "required_future_rows": [
            "A(pole), A'(pole) for the source-pole coordinate",
            "B(pole), B'(pole) for source-orthogonal neutral mixing",
            "C(pole), C'(pole), or matrix C^{-1} and C' for the orthogonal neutral block",
            "pole isolation, FV/IR/model-class, and canonical-Higgs/source identity gates",
        ],
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer the A/B/C rows from source-only C_ss data",
            "does not set kappa_s=1 or O_sp=O_H",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either produce the Schur kernel rows by a same-surface neutral "
            "scalar kernel theorem/measurement, or pivot to direct rank-repair "
            "observables: certified O_H/C_sH/C_HH pole rows or same-source W/Z "
            "response rows with identity certificates."
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
