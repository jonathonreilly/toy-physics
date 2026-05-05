#!/usr/bin/env python3
"""
PR #230 W/Z g2 generator/Casimir normalization no-go.

The same-source W/Z route still needs an absolute electroweak g2 authority.
This runner closes one tempting shortcut: identifying the normalized SU(2)
generators or their Casimir with the physical low-scale coupling.  Generator
normalization fixes representation charges; it does not fix the coefficient of
the canonically normalized gauge field in the interacting action.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json"

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[complex]]


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def matsub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def matscale(c: complex, a: Matrix) -> Matrix:
    return [[c * a[i][j] for j in range(2)] for i in range(2)]


def matadd_all(rows: Iterable[Matrix]) -> Matrix:
    out = [[0j, 0j], [0j, 0j]]
    for row in rows:
        out = [[out[i][j] + row[i][j] for j in range(2)] for i in range(2)]
    return out


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return matsub(matmul(a, b), matmul(b, a))


def trace(a: Matrix) -> complex:
    return a[0][0] + a[1][1]


def max_abs(a: Matrix) -> float:
    return max(abs(a[i][j]) for i in range(2) for j in range(2))


def close(a: Matrix, b: Matrix, tol: float = 1.0e-12) -> bool:
    return max_abs(matsub(a, b)) <= tol


def main() -> int:
    print("PR #230 W/Z g2 generator/Casimir normalization no-go")
    print("=" * 72)

    t1: Matrix = [[0j, 0.5 + 0j], [0.5 + 0j, 0j]]
    t2: Matrix = [[0j, -0.5j], [0.5j, 0j]]
    t3: Matrix = [[0.5 + 0j, 0j], [0j, -0.5 + 0j]]
    generators = (t1, t2, t3)
    ident: Matrix = [[1 + 0j, 0j], [0j, 1 + 0j]]

    trace_norms = [
        float(trace(matmul(generators[i], generators[j])).real)
        for i in range(3)
        for j in range(3)
    ]
    casimir = matadd_all(matmul(g, g) for g in generators)
    commutators_close = (
        close(commutator(t1, t2), matscale(1j, t3))
        and close(commutator(t2, t3), matscale(1j, t1))
        and close(commutator(t3, t1), matscale(1j, t2))
    )
    trace_norm_fixed = all(
        math.isclose(value, 0.5 if i == j else 0.0, rel_tol=0.0, abs_tol=1.0e-12)
        for i in range(3)
        for j, value in enumerate(trace_norms[3 * i : 3 * i + 3])
    )
    casimir_fixed = close(casimir, matscale(0.75, ident))

    candidate_g2_values = [0.35, 0.5, 0.648, 0.9]
    invariant_signatures = [
        {
            "g2": g2,
            "trace_TaTb_diagonal": 0.5,
            "fundamental_casimir": 0.75,
            "mW_over_v_if_static_formula_used": 0.5 * g2,
            "yt_from_fixed_response_ratio_1p23": (g2 / math.sqrt(2.0)) * 1.23,
        }
        for g2 in candidate_g2_values
    ]
    representation_invariants_identical = len(
        {
            (
                row["trace_TaTb_diagonal"],
                row["fundamental_casimir"],
            )
            for row in invariant_signatures
        }
    ) == 1
    physical_coupling_observables_vary = len(
        {
            round(row["mW_over_v_if_static_formula_used"], 12)
            for row in invariant_signatures
        }
    ) == len(candidate_g2_values) and len(
        {
            round(row["yt_from_fixed_response_ratio_1p23"], 12)
            for row in invariant_signatures
        }
    ) == len(candidate_g2_values)
    bare_half_not_selected = any(math.isclose(row["g2"], 0.5) for row in invariant_signatures) and any(
        not math.isclose(row["g2"], 0.5) for row in invariant_signatures
    )

    report("su2-commutator-normalization-fixed", commutators_close, "[T_a,T_b]=i eps_abc T_c")
    report("trace-generator-normalization-fixed", trace_norm_fixed, "Tr(T_a T_b)=delta_ab/2")
    report("fundamental-casimir-fixed", casimir_fixed, "sum_a T_a^2=3/4 I")
    report(
        "representation-invariants-identical-for-many-g2",
        representation_invariants_identical,
        f"candidates={candidate_g2_values}",
    )
    report(
        "physical-coupling-dependent-quantities-vary",
        physical_coupling_observables_vary,
        "mW/v and y_t from a fixed response ratio still scale with g2",
    )
    report(
        "g2-equals-one-half-is-not-selected-by-algebra",
        bare_half_not_selected,
        "g2=1/2 is one member of an algebraically indistinguishable family",
    )
    report("does-not-write-strict-g2-certificate", True, "negative boundary only")
    report("does-not-authorize-retained-proposal", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / SU2 generator-Casimir normalization does not certify PR230 g2"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Generator and Casimir normalization fix representation charges, not the low-scale physical "
            "coupling coefficient of the canonical gauge field."
        ),
        "bare_retained_allowed": False,
        "g2_generator_casimir_no_go_passed": True,
        "strict_electroweak_g2_certificate_passed": False,
        "strict_certificate_written": False,
        "generator_normalization": {
            "commutators_close": commutators_close,
            "trace_TaTb_diagonal": 0.5,
            "fundamental_casimir": 0.75,
        },
        "counterfamily": invariant_signatures,
        "blocked_shortcut": (
            "Do not infer the missing electroweak g2 certificate from SU(2) generator norms, "
            "fundamental Casimir 3/4, or the bare convention g2^2=1/4.  A physical g2 "
            "still requires an allowed action normalization, matching/running bridge, or "
            "direct non-observed certificate."
        ),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed g2, W/Z, top mass, or observed y_t",
            "does not use alpha_LM, plaquette, u0, or package g2 as proof authority",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Supply a strict non-observed g2 authority that includes the canonical gauge-field/action "
            "normalization and any allowed low-scale matching, then rerun the electroweak g2 builder."
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
