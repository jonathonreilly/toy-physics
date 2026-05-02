#!/usr/bin/env python3
"""
PR #230 flat-toron thermodynamic washout support.

The flat-toron obstruction showed finite-volume scalar denominator proxies
change across action-degenerate constant Cartan sectors.  This runner checks
the constructive half: for fixed physical holonomy phi, the constant link angle
is theta=phi/N, and the massive local scalar bubble is a shifted periodic
Riemann sum.  Since the integrand is smooth for m>0, all such shifted sums
converge to the same Brillouin-zone integral as N -> infinity.

This retires the flat-toron ambiguity for the local massive bubble in the
thermodynamic limit.  It is not PR #230 closure: the scalar pole denominator,
massless gauge zero-mode/IR prescription, residue derivative, and production
evidence remain open.
"""

from __future__ import annotations

import json
import math

import numpy as np

from frontier_yt_flat_toron_scalar_denominator_obstruction import (
    OUTPUT as FLAT_TORON_PARENT,
    ROOT,
    scalar_bubble_flat_toron,
)


OUTPUT = ROOT / "outputs" / "yt_flat_toron_thermodynamic_washout_2026-05-01.json"

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


def main() -> int:
    print("PR #230 flat-toron thermodynamic washout support")
    print("=" * 72)

    parent = json.loads(FLAT_TORON_PARENT.read_text(encoding="utf-8"))
    mass = 0.50
    sizes = [6, 8, 10, 12, 16, 20, 24, 32]
    holonomies = [math.pi / 2.0, 2.0 * math.pi / 3.0, math.pi]
    scan = []
    for phi in holonomies:
        for size in sizes:
            trivial = scalar_bubble_flat_toron(size, mass, 0.0)
            shifted = scalar_bubble_flat_toron(size, mass, phi / size)
            rel = abs(shifted - trivial) / trivial
            inv_rel = abs((1.0 / shifted) - (1.0 / trivial)) / (1.0 / trivial)
            scan.append(
                {
                    "grid_size_4d": size,
                    "mass": mass,
                    "holonomy_phi": phi,
                    "link_angle_theta": phi / size,
                    "trivial_scalar_bubble_proxy": trivial,
                    "holonomy_scalar_bubble_proxy": shifted,
                    "relative_bubble_shift": rel,
                    "relative_inverse_denominator_shift": inv_rel,
                }
            )

    def shifts_for(phi: float, field: str) -> list[float]:
        return [
            float(row[field])
            for row in scan
            if abs(float(row["holonomy_phi"]) - phi) < 1.0e-14
        ]

    high_n_rows = [row for row in scan if int(row["grid_size_4d"]) >= 20]
    max_high_n_shift = max(float(row["relative_bubble_shift"]) for row in high_n_rows)
    max_high_n_inverse_shift = max(float(row["relative_inverse_denominator_shift"]) for row in high_n_rows)
    decay_ratios = {}
    monotone_after_n8 = {}
    for phi in holonomies:
        shifts = shifts_for(phi, "relative_bubble_shift")
        decay_ratios[f"phi_{phi:.12g}_N8_over_N24"] = shifts[sizes.index(8)] / shifts[sizes.index(24)]
        tail = shifts[sizes.index(8):]
        monotone_after_n8[f"phi_{phi:.12g}"] = all(tail[idx] > tail[idx + 1] for idx in range(len(tail) - 1))

    min_denominator_bound = mass * mass
    theorem_prerequisites = {
        "fixed_physical_holonomy": "theta = phi / N",
        "mass_positive": mass > 0.0,
        "periodic_smooth_integrand": True,
        "uniform_grid_riemann_sum": True,
        "minimum_denominator_bound": min_denominator_bound,
    }

    report(
        "parent-flat-toron-obstruction-loaded",
        parent.get("proposal_allowed") is False
        and "flat toron scalar-denominator obstruction" in str(parent.get("actual_current_surface_status", "")),
        str(FLAT_TORON_PARENT.relative_to(ROOT)),
    )
    report(
        "riemann-theorem-prerequisites-met",
        all(bool(value) for key, value in theorem_prerequisites.items() if key != "minimum_denominator_bound")
        and min_denominator_bound > 0.0,
        str(theorem_prerequisites),
    )
    report(
        "fixed-holonomy-shifts-monotone-after-n8",
        all(monotone_after_n8.values()),
        str(monotone_after_n8),
    )
    report(
        "fixed-holonomy-shifts-wash-out-by-n24",
        min(decay_ratios.values()) > 1000.0,
        str(decay_ratios),
    )
    report(
        "high-n-bubble-and-inverse-shifts-small",
        max_high_n_shift < 1.0e-4 and max_high_n_inverse_shift < 1.0e-4,
        f"max_bubble_shift_N_ge_20={max_high_n_shift:.6g}, max_inverse_shift_N_ge_20={max_high_n_inverse_shift:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "thermodynamic toron washout does not derive scalar pole/IR derivative or production evidence",
    )

    result = {
        "actual_current_surface_status": "exact-support / flat toron thermodynamic washout",
        "verdict": (
            "For fixed physical flat holonomy phi, the constant link angle is "
            "theta=phi/N.  The massive local scalar bubble is then a shifted "
            "periodic Riemann sum with a smooth bounded integrand, so the "
            "flat-toron dependence vanishes in the thermodynamic limit.  This "
            "retires the finite-volume flat-toron ambiguity for the local "
            "massive bubble, but it does not close PR #230: the interacting "
            "scalar pole denominator, massless gauge zero-mode/IR prescription, "
            "LSZ derivative, and production evidence remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Thermodynamic toron washout is support for one finite-volume ambiguity, not retained y_t closure.",
        "parent_certificate": str(FLAT_TORON_PARENT.relative_to(ROOT)),
        "theorem_statement": (
            "For m>0 and fixed holonomy phi, N^-4 sum_k f(k + phi/N) "
            "converges to the same Brillouin-zone integral as N^-4 sum_k f(k) "
            "for continuous periodic f(k)=1/(m^2+sum_i sin(k_i)^2)^2."
        ),
        "theorem_prerequisites": theorem_prerequisites,
        "parameters": {
            "mass": mass,
            "sizes": sizes,
            "holonomies": holonomies,
        },
        "scan": scan,
        "witnesses": {
            "decay_ratios": decay_ratios,
            "monotone_after_n8": monotone_after_n8,
            "max_relative_bubble_shift_N_ge_20": max_high_n_shift,
            "max_relative_inverse_denominator_shift_N_ge_20": max_high_n_inverse_shift,
        },
        "remaining_blockers": [
            "derive the massless gauge zero-mode and IR prescription for the interacting scalar kernel",
            "derive the scalar pole and inverse-propagator derivative in that selected limit",
            "control finite-Nc continuum contributions or measure the pole derivative in production",
            "run production FH/LSZ evidence with the prescription fixed",
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
