#!/usr/bin/env python3
"""
PR #230 scalar ladder residue-envelope obstruction.

The previous scalar-ladder blocks showed that a finite eigenvalue crossing is
only a pole-location condition and that the total-momentum derivative is
prescription-sensitive.  This runner removes the pole-location ambiguity by
tuning each finite ladder surface to its own pole, then asks whether the
resulting LSZ residue proxy has a controlled finite-volume / IR envelope.

It does not.  The pole-tuned residue proxy remains sensitive to the zero-mode
prescription, source projector, and small-volume sequence.  Therefore the
same-source scalar Bethe-Salpeter route still needs a retained limiting theorem
or production pole-derivative data before it can carry kappa_s / scalar LSZ
normalization.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from frontier_yt_scalar_ladder_total_momentum_derivative_scout import (
    ROOT,
    derivative_row,
)


DERIVATIVE_LIMIT = ROOT / "outputs" / "yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json"

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


def pole_tuned_residue_proxy(row: dict[str, object]) -> float:
    """Return |1 / d(1 - g lambda)/dp_hat^2| with g fixed by g lambda(0)=1."""
    lambda0 = float(row["lambda_p0"])
    derivative = float(row["d_lambda_dp_hat_sq"])
    return abs(lambda0 / derivative)


def main() -> int:
    print("PR #230 scalar ladder residue-envelope obstruction")
    print("=" * 72)

    derivative_limit = json.loads(DERIVATIVE_LIMIT.read_text(encoding="utf-8"))
    sizes = [3, 4, 5]
    mass = 0.50
    ir_paths = {
        "fixed_mu2_0_10": lambda size: 0.10,
        "fixed_mu2_0_05": lambda size: 0.05,
        "fixed_mu2_0_02": lambda size: 0.02,
        "box_scaled_from_N4_mu2_0_10": lambda size: 0.10 * (4.0 / size) ** 2,
    }
    projectors = ["local", "point_split_zero_momentum_normalized"]

    scan = []
    for path_name, mu_rule in ir_paths.items():
        for size in sizes:
            for projector in projectors:
                for remove_zero_mode in [False, True]:
                    row = derivative_row(
                        size=size,
                        mass=mass,
                        ir_mu_sq=float(mu_rule(size)),
                        projector=projector,
                        remove_zero_mode=remove_zero_mode,
                    )
                    proxy = pole_tuned_residue_proxy(row)
                    scan.append(
                        {
                            **row,
                            "ir_path": path_name,
                            "pole_tuned_residue_proxy": proxy,
                            "pole_tuned_derivative_abs": 1.0 / proxy,
                        }
                    )

    def get(path_name: str, size: int, projector: str, remove_zero_mode: bool) -> dict[str, object]:
        zero_mode = "removed" if remove_zero_mode else "included"
        for row in scan:
            if (
                row["ir_path"] == path_name
                and row["grid_size_4d"] == size
                and row["projector"] == projector
                and row["zero_mode"] == zero_mode
            ):
                return row
        raise AssertionError("missing scan row")

    proxies = [float(row["pole_tuned_residue_proxy"]) for row in scan]
    finite_positive = all(np.isfinite(proxies)) and min(proxies) > 0.0
    envelope_spread = max(proxies) / min(proxies)

    local_included = [
        float(get("fixed_mu2_0_05", size, "local", False)["pole_tuned_residue_proxy"])
        for size in sizes
    ]
    local_removed = [
        float(get("fixed_mu2_0_05", size, "local", True)["pole_tuned_residue_proxy"])
        for size in sizes
    ]
    point_split_removed = [
        float(get("fixed_mu2_0_05", size, "point_split_zero_momentum_normalized", True)["pole_tuned_residue_proxy"])
        for size in sizes
    ]
    n5_local_included = float(get("fixed_mu2_0_05", 5, "local", False)["pole_tuned_residue_proxy"])
    n5_local_removed = float(get("fixed_mu2_0_05", 5, "local", True)["pole_tuned_residue_proxy"])
    n5_ps_removed = float(
        get("fixed_mu2_0_05", 5, "point_split_zero_momentum_normalized", True)["pole_tuned_residue_proxy"]
    )

    local_included_fit = np.polyfit([1.0 / size for size in sizes], local_included, 1)
    local_removed_fit = np.polyfit([1.0 / size for size in sizes], local_removed, 1)

    report(
        "derivative-limit-parent-loaded",
        DERIVATIVE_LIMIT.exists() and derivative_limit.get("proposal_allowed") is False,
        str(DERIVATIVE_LIMIT.relative_to(ROOT)),
    )
    report(
        "pole-tuned-residue-scan-runs",
        len(scan) == len(ir_paths) * len(sizes) * len(projectors) * 2,
        f"points={len(scan)}",
    )
    report(
        "pole-location-normalized-proxies-finite",
        finite_positive,
        f"min={min(proxies):.6g}, max={max(proxies):.6g}",
    )
    report(
        "residue-envelope-not-single-valued",
        envelope_spread > 5.0,
        f"proxy_spread={envelope_spread:.6g}",
    )
    report(
        "zero-mode-choice-changes-pole-tuned-residue",
        n5_local_removed / n5_local_included > 5.0,
        f"N5 local removed/included={n5_local_removed / n5_local_included:.6g}",
    )
    report(
        "projector-choice-changes-removed-zero-mode-residue",
        n5_local_removed / n5_ps_removed > 2.0,
        f"N5 removed local/point_split={n5_local_removed / n5_ps_removed:.6g}",
    )
    report(
        "removed-zero-mode-volume-sequence-nonmonotone",
        local_removed[1] < local_removed[0] and local_removed[1] < local_removed[2],
        f"local_removed_fixed_mu2_0_05={local_removed}",
    )
    report(
        "naive-finite-volume-fits-not-retained",
        local_included_fit[1] < 0.0 and local_removed_fit[1] > 0.0,
        f"included_intercept={local_included_fit[1]:.6g}, removed_intercept={local_removed_fit[1]:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "finite pole-tuned residue envelope is not a scalar LSZ/canonical-Higgs theorem",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar ladder residue-envelope obstruction",
        "verdict": (
            "Tuning each finite scalar ladder surface to its own pole removes "
            "the pole-location ambiguity, but it does not produce a unique "
            "scalar LSZ residue.  The pole-tuned residue proxy still changes "
            "under the open zero-mode prescription, source projector, and "
            "finite-volume sequence.  Therefore finite Bethe-Salpeter ladder "
            "data do not yet fix kappa_s or the same-source FH/LSZ readout; "
            "the route needs a retained finite-volume/IR/zero-mode theorem or "
            "production pole-derivative data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The pole-tuned residue proxy is not single-valued across allowed "
            "current-surface prescriptions."
        ),
        "parent_certificate": str(DERIVATIVE_LIMIT.relative_to(ROOT)),
        "parameters": {
            "sizes": sizes,
            "mass": mass,
            "ir_paths": list(ir_paths),
            "projectors": projectors,
        },
        "scan": scan,
        "witnesses": {
            "proxy_spread": envelope_spread,
            "fixed_mu2_0_05_local_included_by_size": local_included,
            "fixed_mu2_0_05_local_removed_by_size": local_removed,
            "fixed_mu2_0_05_point_split_removed_by_size": point_split_removed,
            "N5_local_zero_mode_removed_over_included": n5_local_removed / n5_local_included,
            "N5_removed_local_over_point_split": n5_local_removed / n5_ps_removed,
            "linear_1_over_N_intercepts": {
                "local_included_fixed_mu2_0_05": float(local_included_fit[1]),
                "local_removed_fixed_mu2_0_05": float(local_removed_fit[1]),
            },
        },
        "required_next_theorem": [
            "derive the gauge-zero-mode prescription for the scalar ladder kernel",
            "derive the finite-volume and IR limiting order for d lambda_max / d p^2",
            "derive the scalar source/projector normalization in that limit",
            "bound the continuum contribution at physical N_c=3 or measure the pole derivative in production",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as selectors",
            "does not use alpha_LM, plaquette, u0, or reduced pilots as proof inputs",
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
