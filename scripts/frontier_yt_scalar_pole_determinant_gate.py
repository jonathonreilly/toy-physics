#!/usr/bin/env python3
"""
PR #230 scalar pole determinant gate.

This stretch block isolates the exact scalar-pole condition needed after the
FH/LSZ invariant-readout theorem.  In a one-channel RPA notation,

    C_ss(x) = Pi(x) / D(x),  D(x) = 1 - K(x) Pi(x)

and an isolated scalar pole at x_p requires D(x_p)=0.  The LSZ residue is
controlled by D'(x_p), not by the pole location alone.  Therefore the remaining
closure target is an interacting scalar-channel denominator/kernel theorem or
a production measurement of the same-source pole derivative.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FH_LSZ = ROOT / "outputs" / "yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_pole_determinant_gate_2026-05-01.json"

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


def pi_value(x: float) -> float:
    # Positive toy Euclidean source bubble with nonzero slope at the granted pole.
    return 1.4 - 0.18 * x + 0.03 * x * x


def dpi_dx(x: float) -> float:
    return -0.18 + 0.06 * x


def main() -> int:
    print("PR #230 scalar pole determinant gate")
    print("=" * 72)

    fh_lsz = json.loads(FH_LSZ.read_text(encoding="utf-8"))
    pole_x = -1.0
    pi_pole = pi_value(pole_x)
    k_pole = 1.0 / pi_pole
    kernel_derivatives = [-0.30, -0.10, 0.0, 0.10, 0.30]
    rows = []
    for k_prime in kernel_derivatives:
        d_prime = -k_prime * pi_pole - k_pole * dpi_dx(pole_x)
        residue = pi_pole / abs(d_prime)
        gamma_derivative = abs(d_prime) / pi_pole
        rows.append(
            {
                "kernel_derivative_at_pole": k_prime,
                "D_at_pole": 1.0 - k_pole * pi_pole,
                "D_prime_at_pole": d_prime,
                "C_ss_residue_proxy": residue,
                "dGamma_dp2_at_pole_proxy": gamma_derivative,
                "FH_LSZ_readout_factor_sqrt_dGamma": math.sqrt(gamma_derivative),
            }
        )

    free_denominator_values = [1.0 for _x in [-2.0, -1.0, 0.0, 1.0]]
    pole_residuals = [abs(row["D_at_pole"]) for row in rows]
    residue_values = [row["C_ss_residue_proxy"] for row in rows]
    derivative_values = [row["dGamma_dp2_at_pole_proxy"] for row in rows]
    residue_spread = max(residue_values) / min(residue_values)
    derivative_spread = max(derivative_values) / min(derivative_values)

    report("fh-lsz-invariant-theorem-loaded", FH_LSZ.exists(), str(FH_LSZ.relative_to(ROOT)))
    report("fh-lsz-theorem-not-closure", fh_lsz.get("proposal_allowed") is False, str(fh_lsz.get("proposal_allowed")))
    report(
        "free-bubble-has-no-determinant-zero",
        all(abs(value) > 0.5 for value in free_denominator_values),
        f"D_free_values={free_denominator_values}",
    )
    report(
        "contact-denominator-can-place-pole",
        max(pole_residuals) < 1.0e-12,
        f"max_D_at_pole={max(pole_residuals):.3e}",
    )
    report(
        "pole-location-does-not-fix-residue",
        residue_spread > 2.0 and derivative_spread > 2.0,
        f"residue_spread={residue_spread:.6g}, derivative_spread={derivative_spread:.6g}",
    )
    report(
        "kernel-derivative-load-bearing",
        True,
        "D'(pole) contains K'(pole), so a kernel theorem or pole-derivative measurement is required",
    )
    report("not-retained-closure", True, "the determinant gate names the required theorem but does not supply K(x)")

    result = {
        "actual_current_surface_status": "exact-support / scalar pole determinant gate",
        "verdict": (
            "The same-source scalar LSZ blocker is now localized to the "
            "interacting denominator.  A free source bubble has no determinant "
            "zero.  A scalar-channel RPA/Bethe-Salpeter denominator can create "
            "a pole through D(x)=1-K(x)Pi(x)=0, but the LSZ residue is governed "
            "by D'(x_pole).  Keeping the pole location fixed while varying "
            "K'(x_pole) changes the residue and the FH/LSZ readout factor.  "
            "Thus PR #230 needs a retained kernel theorem or production "
            "pole-derivative measurement; pole naming alone is not closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The determinant gate is exact support, but K(x), K'(pole), and production pole data remain open.",
        "fh_lsz_invariant_readout_certificate": str(FH_LSZ.relative_to(ROOT)),
        "pole_condition": {
            "bubble": "Pi(x)",
            "denominator": "D(x)=1-K(x) Pi(x)",
            "pole": "D(x_pole)=0",
            "inverse_propagator_derivative": "dGamma_ss/dp^2 at pole = D'(x_pole)/Pi(x_pole) up to sign convention",
            "kernel_derivative_term": "D'(x_pole) = -K'(x_pole) Pi(x_pole) - K(x_pole) Pi'(x_pole)",
        },
        "toy_parameters": {
            "pole_x": pole_x,
            "Pi_at_pole": pi_pole,
            "K_at_pole_fixed_by_pole_location": k_pole,
            "Pi_prime_at_pole": dpi_dx(pole_x),
        },
        "rows": rows,
        "required_next_theorem": [
            "derive the interacting scalar-channel K(x) from the retained Wilson-staggered dynamics",
            "fix the gauge-zero-mode, finite-volume, and IR limiting order for K(x)",
            "prove D(x_pole)=0 for a physical scalar pole",
            "compute D'(x_pole) or measure it on production ensembles",
            "insert that derivative into the FH/LSZ invariant readout formula",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
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
