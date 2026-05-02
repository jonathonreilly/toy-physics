#!/usr/bin/env python3
"""
PR #230 scalar ladder derivative limiting-order obstruction.

The total-momentum derivative scout showed that d lambda_max / d p^2 is
computable in a finite Wilson-exchange ladder.  This runner asks whether that
derivative is stable under the still-open gauge-zero-mode and IR limiting
prescription.

It is not closure: with the gauge zero mode retained, the derivative grows
strongly as the IR regulator is lowered and the pole test crosses.  With the
zero mode removed, the derivative is comparatively stable and the pole test
does not cross on the same surface.  Therefore the scalar-LSZ route still
needs a retained limiting-order theorem or production pole derivative.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from frontier_yt_scalar_ladder_total_momentum_derivative_scout import (
    OUTPUT as TOTAL_MOMENTUM_CERT,
    ROOT,
    derivative_row,
)


OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json"

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


def power_slope(x0: float, y0: float, x1: float, y1: float) -> float:
    return math.log(abs(y1) / abs(y0)) / math.log(x0 / x1)


def main() -> int:
    print("PR #230 scalar ladder derivative limiting-order obstruction")
    print("=" * 72)

    parent = json.loads(TOTAL_MOMENTUM_CERT.read_text(encoding="utf-8"))
    sizes = [3, 4, 5]
    mass = 0.50
    ir_values = [0.50, 0.20, 0.10, 0.05, 0.02]
    projectors = ["local", "point_split_zero_momentum_normalized"]

    scan = []
    for size in sizes:
        for projector in projectors:
            for remove_zero_mode in [False, True]:
                for ir_mu_sq in ir_values:
                    scan.append(
                        derivative_row(
                            size=size,
                            mass=mass,
                            ir_mu_sq=ir_mu_sq,
                            projector=projector,
                            remove_zero_mode=remove_zero_mode,
                        )
                    )

    def get(size: int, projector: str, remove_zero_mode: bool, ir_mu_sq: float) -> dict[str, object]:
        zero_mode = "removed" if remove_zero_mode else "included"
        for row in scan:
            if (
                row["grid_size_4d"] == size
                and row["projector"] == projector
                and row["zero_mode"] == zero_mode
                and abs(float(row["ir_mu_sq"]) - ir_mu_sq) < 1.0e-12
            ):
                return row
        raise AssertionError("missing scan row")

    local_included_hi = get(4, "local", False, 0.50)
    local_included_lo = get(4, "local", False, 0.02)
    local_removed_hi = get(4, "local", True, 0.50)
    local_removed_lo = get(4, "local", True, 0.02)
    ps_included_hi = get(4, "point_split_zero_momentum_normalized", False, 0.50)
    ps_included_lo = get(4, "point_split_zero_momentum_normalized", False, 0.02)
    ps_removed_hi = get(4, "point_split_zero_momentum_normalized", True, 0.50)
    ps_removed_lo = get(4, "point_split_zero_momentum_normalized", True, 0.02)

    local_included_ratio = abs(float(local_included_lo["d_lambda_dp_hat_sq"])) / abs(float(local_included_hi["d_lambda_dp_hat_sq"]))
    local_removed_ratio = abs(float(local_removed_lo["d_lambda_dp_hat_sq"])) / abs(float(local_removed_hi["d_lambda_dp_hat_sq"]))
    ps_included_ratio = abs(float(ps_included_lo["d_lambda_dp_hat_sq"])) / abs(float(ps_included_hi["d_lambda_dp_hat_sq"]))
    ps_removed_ratio = abs(float(ps_removed_lo["d_lambda_dp_hat_sq"])) / abs(float(ps_removed_hi["d_lambda_dp_hat_sq"]))
    zero_mode_split_low_ir = abs(float(local_included_lo["d_lambda_dp_hat_sq"])) / abs(float(local_removed_lo["d_lambda_dp_hat_sq"]))
    ps_zero_mode_split_low_ir = abs(float(ps_included_lo["d_lambda_dp_hat_sq"])) / abs(float(ps_removed_lo["d_lambda_dp_hat_sq"]))
    local_included_slope = power_slope(0.50, float(local_included_hi["d_lambda_dp_hat_sq"]), 0.02, float(local_included_lo["d_lambda_dp_hat_sq"]))
    local_removed_slope = power_slope(0.50, float(local_removed_hi["d_lambda_dp_hat_sq"]), 0.02, float(local_removed_lo["d_lambda_dp_hat_sq"]))

    included_poles = [
        bool(get(4, "local", False, ir_mu_sq)["pole_condition_at_p0"])
        for ir_mu_sq in ir_values
    ]
    removed_poles = [
        bool(get(4, "local", True, ir_mu_sq)["pole_condition_at_p0"])
        for ir_mu_sq in ir_values
    ]

    report(
        "parent-total-momentum-scout-loaded",
        TOTAL_MOMENTUM_CERT.exists() and parent.get("proposal_allowed") is False,
        str(TOTAL_MOMENTUM_CERT.relative_to(ROOT)),
    )
    report(
        "limiting-order-scan-runs",
        len(scan) == len(sizes) * len(projectors) * 2 * len(ir_values),
        f"points={len(scan)}",
    )
    report(
        "zero-mode-included-derivative-ir-sensitive",
        local_included_ratio > 10.0 and ps_included_ratio > 10.0,
        f"local_ratio={local_included_ratio:.6g}, point_split_ratio={ps_included_ratio:.6g}",
    )
    report(
        "zero-mode-removed-derivative-stable-in-same-scan",
        local_removed_ratio < 1.2 and ps_removed_ratio < 1.2,
        f"local_ratio={local_removed_ratio:.6g}, point_split_ratio={ps_removed_ratio:.6g}",
    )
    report(
        "zero-mode-choice-load-bearing-at-low-ir",
        zero_mode_split_low_ir > 20.0 and ps_zero_mode_split_low_ir > 20.0,
        f"local_split={zero_mode_split_low_ir:.6g}, point_split_split={ps_zero_mode_split_low_ir:.6g}",
    )
    report(
        "pole-test-crosses-only-with-zero-mode-included",
        any(included_poles) and not all(included_poles) and not any(removed_poles),
        f"included={included_poles}, removed={removed_poles}",
    )
    report(
        "included-and-removed-limits-have-different-ir-powers",
        local_included_slope > 0.75 and local_removed_slope < 0.05,
        f"included_slope={local_included_slope:.6g}, removed_slope={local_removed_slope:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "the scout exposes the limiting-order theorem required before scalar LSZ use",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar ladder derivative limiting-order obstruction",
        "verdict": (
            "The total-momentum derivative is not a retained scalar-LSZ input "
            "until the gauge-zero-mode and IR limiting order is fixed.  In the "
            "finite Wilson-exchange scout, retaining the zero mode makes "
            "d lambda_max/dp^2 grow strongly as the IR regulator is lowered "
            "and makes the pole test cross.  Removing the zero mode gives a "
            "comparatively stable derivative and no crossing on the same "
            "surface.  Therefore the route needs a retained zero-mode/IR/"
            "finite-volume prescription or production pole-derivative data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The derivative has prescription-dependent IR behavior; no retained limiting order is derived.",
        "parent_certificate": str(TOTAL_MOMENTUM_CERT.relative_to(ROOT)),
        "parameters": {
            "sizes": sizes,
            "mass": mass,
            "ir_mu_sq_values": ir_values,
            "projectors": projectors,
        },
        "scan": scan,
        "witnesses": {
            "local_included_ratio_mu2_0_50_to_0_02": local_included_ratio,
            "local_removed_ratio_mu2_0_50_to_0_02": local_removed_ratio,
            "point_split_included_ratio_mu2_0_50_to_0_02": ps_included_ratio,
            "point_split_removed_ratio_mu2_0_50_to_0_02": ps_removed_ratio,
            "local_zero_mode_split_at_mu2_0_02": zero_mode_split_low_ir,
            "point_split_zero_mode_split_at_mu2_0_02": ps_zero_mode_split_low_ir,
            "local_included_ir_power_slope": local_included_slope,
            "local_removed_ir_power_slope": local_removed_slope,
            "local_included_pole_pattern_by_ir": included_poles,
            "local_removed_pole_pattern_by_ir": removed_poles,
        },
        "required_next_theorem": [
            "derive the gauge fixing and zero-mode prescription for the scalar-channel kernel",
            "derive the IR and finite-volume limiting order before taking d lambda_max / d p^2 as an LSZ residue",
            "prove the scalar projector/source normalization in that limit",
            "or measure the pole derivative directly on production ensembles",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette, u0, or observed top/Yukawa values",
            "does not use reduced cold pilots as production evidence",
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
