#!/usr/bin/env python3
"""Hardening card for the diamond/NV signal-budget lane.

This is intentionally narrow.

The retained moving-source proxy gives us:

- one explicit source geometry
- one signed scaling map in source velocity
- one proxy-budget estimate from the weakest retained nonzero observables

What it does not give us is an absolute lab budget. That still needs a
calibrated transfer coefficient from the retained proxy units into the actual
NV readout / noise floor.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fabs


@dataclass(frozen=True)
class RetainedRow:
    velocity: float
    delta_y_vs_static: float
    phase_lag_rad: float


GEOMETRY = {
    "family": "drift=0.2, restore=0.7",
    "seeds": 6,
    "source_layer": 8,
    "source_anchor_target": (0.0, 3.0),
    "motion_law": "y_src(layer) = y0 + v * (layer - source_layer) * h",
    "h": 0.5,
}


ROWS = [
    RetainedRow(velocity=-1.00, delta_y_vs_static=-1.641405e-06, phase_lag_rad=4.852935e-05),
    RetainedRow(velocity=-0.50, delta_y_vs_static=-9.233039e-07, phase_lag_rad=1.309075e-05),
    RetainedRow(velocity=0.00, delta_y_vs_static=0.0, phase_lag_rad=0.0),
    RetainedRow(velocity=0.50, delta_y_vs_static=8.665715e-07, phase_lag_rad=1.401315e-05),
    RetainedRow(velocity=1.00, delta_y_vs_static=1.472200e-06, phase_lag_rad=4.334258e-05),
]


def _nonzero_rows() -> list[RetainedRow]:
    return [row for row in ROWS if fabs(row.velocity) > 1e-12]


def _min_abs(values: list[float]) -> float:
    return min(fabs(v) for v in values)


def _max_abs(values: list[float]) -> float:
    return max(fabs(v) for v in values)


def _format_float(value: float) -> str:
    return f"{value:+.6e}"


def build_report() -> str:
    nonzero = _nonzero_rows()
    delta_vals = [row.delta_y_vs_static for row in nonzero]
    phase_vals = [row.phase_lag_rad for row in nonzero]

    delta_min = _min_abs(delta_vals)
    delta_max = _max_abs(delta_vals)
    phase_min = _min_abs(phase_vals)
    phase_max = _max_abs(phase_vals)

    delta_3sigma = delta_min / 3.0
    phase_3sigma = phase_min / 3.0

    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("DIAMOND SIGNAL BUDGET HARDENING")
    lines.append("  one geometry, one scaling map, one proxy-budget estimate")
    lines.append("=" * 100)
    lines.append("")
    lines.append("GEOMETRY ANCHOR")
    lines.append(f"  family: {GEOMETRY['family']}")
    lines.append(f"  seeds: {GEOMETRY['seeds']}")
    lines.append(f"  source_layer: {GEOMETRY['source_layer']}")
    lines.append(f"  source_anchor_target: (y, z) = {GEOMETRY['source_anchor_target']}")
    lines.append(f"  motion law: {GEOMETRY['motion_law']}")
    lines.append(f"  h: {GEOMETRY['h']}")
    lines.append("")
    lines.append("SCALING MAP")
    lines.append("  v    delta_y vs static        phase lag (rad)")
    lines.append("  ---  -----------------------  ----------------")
    for row in ROWS:
        lines.append(
            f"  {row.velocity:+.2f}  {_format_float(row.delta_y_vs_static):>23s}  {_format_float(row.phase_lag_rad):>16s}"
        )
    lines.append("")
    lines.append("PROXY BUDGET")
    lines.append(f"  weakest nonzero |delta_y vs static| = {delta_min:.6e}")
    lines.append(f"  strongest nonzero |delta_y vs static| = {delta_max:.6e}")
    lines.append(f"  weakest nonzero |phase lag| = {phase_min:.6e} rad")
    lines.append(f"  strongest nonzero |phase lag| = {phase_max:.6e} rad")
    lines.append(f"  conservative 3-sigma centroid-noise target = {delta_3sigma:.6e}")
    lines.append(f"  conservative 3-sigma phase-noise target = {phase_3sigma:.6e} rad")
    lines.append("")
    lines.append("DIAGNOSIS")
    lines.append(
        "  the centroid sign flip is the sharper retained observable; the phase lag is a weaker secondary residue"
    )
    lines.append(
        "  a real absolute lab budget is still blocked by the missing transfer coefficient from proxy units to NV readout units"
    )
    lines.append("  until that calibration exists, this remains a proxy-budget card rather than a lab-ready amplitude claim")
    lines.append("")
    lines.append("FINAL VERDICT")
    lines.append("  retained narrow hardening: one explicit source geometry, one signed scaling map, and one proxy budget")
    return "\n".join(lines)


def main() -> int:
    print(build_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
