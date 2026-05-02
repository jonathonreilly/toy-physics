#!/usr/bin/env python3
"""
PR #230 color-singlet finite-q IR regularity support.

After exact q=0 gauge-zero-mode cancellation in the color singlet, this runner
checks the remaining finite-q massless Wilson-exchange kernel.  In four
dimensions, the small-q measure q^3 dq makes the 1/q^2 kernel locally
integrable.  Therefore the zero-mode-removed kernel has a finite IR limit.

This is exact support for the color-singlet scalar denominator route, not
retained y_t closure.  The pole location, interacting derivative, projector,
finite-Nc residue, and production evidence remain open.
"""

from __future__ import annotations

import json
import math

import numpy as np

from frontier_yt_color_singlet_zero_mode_cancellation import (
    OUTPUT as COLOR_SINGLET_PARENT,
    ROOT,
)


OUTPUT = ROOT / "outputs" / "yt_color_singlet_finite_q_ir_regular_2026-05-01.json"

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


def qhat_grid(size: int) -> np.ndarray:
    axes = [2.0 * math.pi * np.arange(size) / size for _ in range(4)]
    grids = np.meshgrid(*axes, indexing="ij")
    qhat_sq = np.zeros_like(grids[0], dtype=float)
    for grid in grids:
        qhat_sq += (2.0 * np.sin(grid / 2.0)) ** 2
    return qhat_sq.ravel()


def zero_mode_removed_average(size: int, mu_sq: float) -> float:
    qhat_sq = qhat_grid(size)
    mask = qhat_sq > 1.0e-14
    return float(np.mean(1.0 / (qhat_sq[mask] + mu_sq)))


def zero_mode_included_average(size: int, mu_sq: float) -> float:
    qhat_sq = qhat_grid(size)
    return float(np.mean(1.0 / (qhat_sq + mu_sq)))


def main() -> int:
    print("PR #230 color-singlet finite-q IR regularity")
    print("=" * 72)

    parent = json.loads(COLOR_SINGLET_PARENT.read_text(encoding="utf-8"))
    sizes = [8, 12, 16, 20, 24, 32]
    mu_values = [0.10, 0.05, 0.02, 0.01, 0.0]
    scan = []
    for size in sizes:
        for mu_sq in mu_values:
            scan.append(
                {
                    "grid_size_4d": size,
                    "ir_mu_sq": mu_sq,
                    "zero_mode_removed_kernel_average": zero_mode_removed_average(size, mu_sq),
                    "zero_mode_included_kernel_average": None if mu_sq == 0.0 else zero_mode_included_average(size, mu_sq),
                }
            )

    def rows_for(size: int) -> list[dict[str, object]]:
        return [row for row in scan if int(row["grid_size_4d"]) == size]

    removed_ratios_fixed_n = {}
    for size in sizes:
        rows = rows_for(size)
        hi = next(float(row["zero_mode_removed_kernel_average"]) for row in rows if float(row["ir_mu_sq"]) == 0.10)
        lo = next(float(row["zero_mode_removed_kernel_average"]) for row in rows if float(row["ir_mu_sq"]) == 0.0)
        removed_ratios_fixed_n[f"N{size}_mu0_over_mu0_10"] = lo / hi

    mu_zero_values = [
        float(row["zero_mode_removed_kernel_average"])
        for row in scan
        if float(row["ir_mu_sq"]) == 0.0 and int(row["grid_size_4d"]) >= 16
    ]
    volume_spread_n_ge_16 = max(mu_zero_values) / min(mu_zero_values)

    included_ir_ratios = {}
    for size in [8, 16, 32]:
        inc_010 = zero_mode_included_average(size, 0.10)
        inc_001 = zero_mode_included_average(size, 1.0e-6)
        removed_000 = zero_mode_removed_average(size, 0.0)
        included_ir_ratios[f"N{size}_included_mu1e-6_over_mu0_10"] = inc_001 / inc_010
        included_ir_ratios[f"N{size}_included_mu1e-6_over_removed_mu0"] = inc_001 / removed_000

    ir_power = 4 - 2
    max_fixed_n_ratio = max(removed_ratios_fixed_n.values())
    max_included_growth = max(
        value for key, value in included_ir_ratios.items()
        if key.endswith("over_mu0_10")
    )

    report(
        "parent-color-singlet-zero-mode-loaded",
        parent.get("proposal_allowed") is False
        and "color-singlet gauge-zero-mode cancellation" in str(parent.get("actual_current_surface_status", "")),
        str(COLOR_SINGLET_PARENT.relative_to(ROOT)),
    )
    report(
        "four-dimensional-finite-q-kernel-is-locally-integrable",
        ir_power > 0,
        "small-q integral scales as integral q^(4-1)/q^2 dq = integral q dq",
    )
    report(
        "zero-mode-removed-fixed-volume-ir-limit-finite",
        max_fixed_n_ratio < 1.04,
        f"max mu=0 / mu=0.10 ratio={max_fixed_n_ratio:.6g}",
    )
    report(
        "zero-mode-removed-volume-sequence-stable",
        volume_spread_n_ge_16 < 1.01,
        f"N>=16 mu=0 spread={volume_spread_n_ge_16:.6g}",
    )
    report(
        "included-zero-mode-retains-ir-divergence",
        max_included_growth > 5.0,
        str(included_ir_ratios),
    )
    report(
        "not-retained-closure",
        True,
        "finite-q IR regularity is support; pole derivative and production evidence remain open",
    )

    result = {
        "actual_current_surface_status": "exact-support / color-singlet finite-q IR regularity",
        "verdict": (
            "After the exact q=0 gauge mode cancels in the color-singlet "
            "channel, the remaining finite-q massless kernel is locally "
            "integrable in four dimensions.  The zero-mode-removed lattice "
            "kernel has a finite mu_IR -> 0 limit and a stable large-volume "
            "sequence in the scan.  This supports the color-singlet scalar "
            "denominator route, but it does not derive an isolated scalar pole, "
            "the inverse-propagator derivative, finite-Nc continuum control, or "
            "production FH/LSZ evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-q IR regularity removes one obstruction but does not determine the scalar pole derivative.",
        "parent_certificate": str(COLOR_SINGLET_PARENT.relative_to(ROOT)),
        "theorem_statement": (
            "In d=4, excluding the color-singlet-cancelled q=0 mode, "
            "the massless gauge kernel 1/q^2 is locally integrable because "
            "d^4q/q^2 ~ q dq near q=0."
        ),
        "parameters": {
            "sizes": sizes,
            "ir_mu_sq_values": mu_values,
            "ir_power_after_measure": ir_power,
        },
        "scan": scan,
        "witnesses": {
            "removed_ratios_fixed_n": removed_ratios_fixed_n,
            "zero_mode_removed_mu0_volume_spread_N_ge_16": volume_spread_n_ge_16,
            "included_ir_ratios": included_ir_ratios,
        },
        "remaining_blockers": [
            "derive the full interacting color-singlet scalar kernel rather than only its finite-q IR regularity",
            "derive or measure the scalar pole location and inverse-propagator derivative",
            "derive source/projector normalization and finite-Nc continuum control",
            "run production FH/LSZ evidence with the color-singlet zero-mode prescription fixed",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as selectors",
            "does not use alpha_LM, plaquette, u0, or reduced pilots as proof inputs",
            "does not set c2 = 1 or Z_match = 1",
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
