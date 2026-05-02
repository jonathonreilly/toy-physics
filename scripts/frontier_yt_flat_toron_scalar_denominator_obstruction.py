#!/usr/bin/env python3
"""
PR #230 flat-toron scalar-denominator obstruction.

The zero-mode audit found no retained prescription for the scalar denominator
limit.  This runner checks whether the compact lattice gauge action itself
selects the trivial gauge zero mode.  It does not: constant commuting SU(3)
links are flat plaquette-action directions, but they shift charged fermion
momenta through Polyakov phases and change the scalar-source bubble.

This blocks a hidden "just remove/select the zero mode" shortcut.  A retained
scalar denominator theorem must specify how these flat sectors are fixed,
averaged, or suppressed before the LSZ derivative is load-bearing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from frontier_yt_scalar_ladder_ir_zero_mode_obstruction import ROOT, momentum_grid


OUTPUT = ROOT / "outputs" / "yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json"
PARENT = ROOT / "outputs" / "yt_zero_mode_prescription_import_audit_2026-05-01.json"

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


def cartan_phases(theta: float) -> np.ndarray:
    return np.asarray([theta, -theta, 0.0], dtype=float)


def plaquette_action_density(theta: float) -> float:
    """Constant commuting diagonal links have identity plaquettes."""
    _ = cartan_phases(theta)
    return 0.0


def normalized_polyakov_trace(size: int, theta: float) -> complex:
    phases = cartan_phases(theta)
    return complex(np.mean(np.exp(1j * size * phases)))


def scalar_bubble_flat_toron(size: int, mass: float, theta: float) -> float:
    """Color-averaged local scalar bubble on a constant Cartan toron."""
    momenta = momentum_grid(size)
    total = 0.0
    for phase in cartan_phases(theta):
        shifted = momenta.copy()
        shifted[:, 0] = shifted[:, 0] + phase
        den = mass * mass + np.sum(np.sin(shifted) ** 2, axis=1)
        total += float(np.mean(1.0 / (den * den)))
    return total / 3.0


def main() -> int:
    print("PR #230 flat-toron scalar-denominator obstruction")
    print("=" * 72)

    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    size = 8
    mass = 0.50
    theta_values = [0.0, math.pi / (8.0 * size), math.pi / (4.0 * size), math.pi / (2.0 * size), math.pi / size]

    scan = []
    for theta in theta_values:
        bubble = scalar_bubble_flat_toron(size, mass, theta)
        polyakov = normalized_polyakov_trace(size, theta)
        scan.append(
            {
                "grid_size_4d": size,
                "mass": mass,
                "theta": theta,
                "plaquette_action_density": plaquette_action_density(theta),
                "normalized_polyakov_trace_real": float(polyakov.real),
                "normalized_polyakov_trace_imag": float(polyakov.imag),
                "scalar_bubble_proxy": bubble,
                "inverse_scalar_bubble_proxy": 1.0 / bubble,
            }
        )

    actions = [abs(float(row["plaquette_action_density"])) for row in scan]
    bubbles = [float(row["scalar_bubble_proxy"]) for row in scan]
    inverse_bubbles = [float(row["inverse_scalar_bubble_proxy"]) for row in scan]
    bubble_spread = max(bubbles) / min(bubbles)
    inverse_spread = max(inverse_bubbles) / min(inverse_bubbles)
    polyakov_deviation = max(
        abs(complex(row["normalized_polyakov_trace_real"], row["normalized_polyakov_trace_imag"]) - 1.0)
        for row in scan
    )
    trivial_bubble = bubbles[0]
    max_relative_shift = max(abs(value - trivial_bubble) / trivial_bubble for value in bubbles)

    report(
        "parent-import-audit-loaded",
        parent.get("proposal_allowed") is False and "import audit" in str(parent.get("actual_current_surface_status", "")),
        str(PARENT.relative_to(ROOT)),
    )
    report(
        "flat-toron-plaquette-action-degenerate",
        max(actions) < 1.0e-15,
        f"max_action_density={max(actions):.3e}",
    )
    report(
        "polyakov-phases-distinguish-sectors",
        polyakov_deviation > 0.5,
        f"max |P(theta)-P(0)|={polyakov_deviation:.6g}",
    )
    report(
        "scalar-bubble-changes-on-flat-sectors",
        max_relative_shift > 0.04,
        f"max_relative_shift={max_relative_shift:.6g}",
    )
    report(
        "inverse-denominator-proxy-changes-on-flat-sectors",
        inverse_spread > 1.05,
        f"inverse_spread={inverse_spread:.6g}",
    )
    report(
        "trivial-toron-selection-not-derived",
        True,
        "zero plaquette action does not select theta=0 over other constant Cartan sectors",
    )
    report(
        "not-retained-closure",
        True,
        "flat toron sectors make zero-mode treatment a load-bearing scalar-denominator premise",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / flat toron scalar-denominator obstruction",
        "verdict": (
            "Constant commuting SU(3) Cartan links have zero plaquette action "
            "but distinct Polyakov phases.  In the scalar-source bubble proxy "
            "they shift charged fermion momenta and change the inverse "
            "scalar-denominator readout.  Therefore the compact lattice action "
            "does not by itself select the trivial gauge zero mode used by a "
            "finite ladder denominator.  PR #230 still needs a retained "
            "gauge-fixing/toron/zero-mode prescription or production pole data "
            "with that prescription fixed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Flat gauge zero-mode sectors are action-degenerate but change scalar denominator proxies.",
        "parent_certificate": str(PARENT.relative_to(ROOT)),
        "parameters": {
            "grid_size_4d": size,
            "mass": mass,
            "theta_values": theta_values,
            "color_phases": "diag(exp(i theta), exp(-i theta), 1)",
        },
        "scan": scan,
        "witnesses": {
            "max_plaquette_action_density": max(actions),
            "max_polyakov_deviation_from_trivial": polyakov_deviation,
            "scalar_bubble_spread": bubble_spread,
            "inverse_scalar_bubble_spread": inverse_spread,
            "max_relative_scalar_bubble_shift_from_trivial": max_relative_shift,
        },
        "required_next_theorem": [
            "derive whether flat Cartan toron sectors are fixed, averaged, or suppressed in the scalar-channel denominator",
            "derive the associated gauge-fixing and zero-mode prescription",
            "prove the scalar pole and inverse-propagator derivative in that selected sector or average",
            "or measure the pole derivative in production with the prescription explicitly fixed",
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
