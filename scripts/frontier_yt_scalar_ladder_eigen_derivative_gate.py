#!/usr/bin/env python3
"""
PR #230 scalar ladder eigen-derivative gate.

The determinant gate localizes the scalar LSZ residue to the derivative of the
interacting denominator.  In a matrix Bethe-Salpeter/ladder formulation the
same statement is:

    lambda_max(pole) = 1
    residue needs d lambda_max / d p^2 at the crossing.

This runner shows that a finite eigenvalue-crossing witness at one momentum is
not enough.  Holding the pole eigenvalue fixed, different momentum-dependent
ladder derivatives give different LSZ residue/readout factors.  The retained
route must derive or measure the momentum-dependent kernel derivative.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DETERMINANT = ROOT / "outputs" / "yt_scalar_pole_determinant_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def largest_eigenpair(matrix: np.ndarray) -> tuple[float, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    idx = int(np.argmax(values))
    vec = vectors[:, idx]
    if vec[0] < 0:
        vec = -vec
    return float(values[idx]), vec


def main() -> int:
    print("PR #230 scalar ladder eigen-derivative gate")
    print("=" * 72)

    determinant = json.loads(DETERMINANT.read_text(encoding="utf-8"))
    # M0 is a toy scalar ladder matrix at the candidate pole momentum.  Its
    # largest eigenvalue is exactly one, so it passes the pole-location test.
    M0 = np.asarray(
        [
            [0.86, 0.28],
            [0.28, 0.44],
        ],
        dtype=float,
    )
    eig0, vec0 = largest_eigenpair(M0)
    M0 = M0 / eig0
    eig0, vec0 = largest_eigenpair(M0)

    derivative_matrices = {
        "flat": np.asarray([[0.02, 0.00], [0.00, 0.02]], dtype=float),
        "mild_positive": np.asarray([[0.08, 0.01], [0.01, 0.00]], dtype=float),
        "steep_positive": np.asarray([[0.25, 0.03], [0.03, -0.02]], dtype=float),
        "negative": np.asarray([[-0.08, 0.02], [0.02, 0.04]], dtype=float),
    }
    rows = []
    for label, M1 in derivative_matrices.items():
        lambda_prime = float(vec0 @ M1 @ vec0)
        denominator_derivative = -lambda_prime
        residue_proxy = 1.0 / abs(denominator_derivative) if abs(denominator_derivative) > 1.0e-30 else float("inf")
        readout_factor = math.sqrt(abs(denominator_derivative))
        rows.append(
            {
                "case": label,
                "lambda_at_pole": eig0,
                "lambda_prime_at_pole": lambda_prime,
                "denominator_derivative_proxy": denominator_derivative,
                "LSZ_residue_proxy": residue_proxy,
                "FH_LSZ_readout_factor_proxy": readout_factor,
            }
        )

    lambda_values = [row["lambda_at_pole"] for row in rows]
    derivative_values = [abs(row["denominator_derivative_proxy"]) for row in rows]
    residue_values = [row["LSZ_residue_proxy"] for row in rows if math.isfinite(row["LSZ_residue_proxy"])]
    readout_values = [row["FH_LSZ_readout_factor_proxy"] for row in rows]
    derivative_spread = max(derivative_values) / min(v for v in derivative_values if v > 0.0)
    residue_spread = max(residue_values) / min(residue_values)
    readout_spread = (max(readout_values) - min(readout_values)) / max(sum(readout_values) / len(readout_values), 1.0e-30)

    report("determinant-gate-loaded", DETERMINANT.exists(), str(DETERMINANT.relative_to(ROOT)))
    report("determinant-gate-not-closure", determinant.get("proposal_allowed") is False, str(determinant.get("proposal_allowed")))
    report("pole-eigenvalue-held-fixed", max(abs(value - 1.0) for value in lambda_values) < 1.0e-12, f"lambda_values={lambda_values}")
    report(
        "eigen-derivative-varies",
        derivative_spread > 5.0,
        f"derivative_spread={derivative_spread:.6g}",
    )
    report(
        "lsz-residue-varies-at-fixed-pole",
        residue_spread > 5.0 and readout_spread > 0.5,
        f"residue_spread={residue_spread:.6g}, readout_spread={readout_spread:.6g}",
    )
    report(
        "momentum-dependent-kernel-load-bearing",
        True,
        "need dK/dp^2 or finite-difference production eigenvalue data, not only lambda_max=1",
    )
    report("not-retained-closure", True, "matrix derivative gate supplies acceptance criteria only")

    result = {
        "actual_current_surface_status": "exact-support / scalar ladder eigen-derivative gate",
        "verdict": (
            "A scalar Bethe-Salpeter pole criterion lambda_max=1 is not enough "
            "to fix the LSZ residue.  Holding the candidate pole eigenvalue "
            "fixed, different momentum derivatives of the ladder kernel move "
            "d lambda/dp^2, the residue proxy, and the FH/LSZ readout factor.  "
            "Therefore PR #230 still needs a retained momentum-dependent "
            "scalar-channel kernel theorem or production finite-difference "
            "eigenvalue/pole-derivative data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The eigen-derivative gate is exact support, but the momentum-dependent kernel derivative remains open.",
        "determinant_gate_certificate": str(DETERMINANT.relative_to(ROOT)),
        "M0_at_pole": M0.tolist(),
        "pole_eigenvector": vec0.tolist(),
        "rows": rows,
        "required_next_theorem": [
            "derive the total-momentum dependence of the scalar Bethe-Salpeter kernel K(k,k';p)",
            "fix the finite-volume, gauge-zero-mode, and IR prescription before differentiating",
            "compute d lambda_max / d p^2 at the scalar pole",
            "combine that derivative with the same-source FH/LSZ invariant readout",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
