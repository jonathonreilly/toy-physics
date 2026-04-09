#!/usr/bin/env python3
"""Print a compact diamond/NV phase-ramp bridge card.

This is intentionally a proxy-unit bridge card, not an absolute NV
calibration. It synthesizes the retained exact-family phase-ramp results into
the narrowest handoff card we can state in-repo:

- one highlighted retained row
- a small source-strength sweep
- a nearby source-depth / separation sweep
- normalized proxy phasor components and phase-ramp slope

The card is meant to support a future lab conversation, not to claim
absolute detectability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StrengthRow:
    s: float
    inst: float
    same: float
    wave: float
    phase_lag: float
    ramp_slope: float
    ramp_r2: float
    wave_same_ratio: float


@dataclass(frozen=True)
class DepthRow:
    layer: int
    depth: float
    ramp_slope: float
    ramp_r2: float
    phase_lag: float


STRENGTH_ROWS = [
    StrengthRow(0.0010, 2.931018e-03, 3.658426e-03, 1.759245e-01, -0.740, -0.1215, 0.959, 60.022),
    StrengthRow(0.0020, 5.873223e-03, 7.321503e-03, 3.559416e-01, -1.473, -0.2444, 0.959, 60.604),
    StrengthRow(0.0040, 1.179000e-02, 1.466136e-02, 7.157359e-01, -2.880, -0.4925, 0.960, 60.707),
    StrengthRow(0.0080, 2.374397e-02, 2.939408e-02, 1.326988e00, +0.337, -1.0274, 0.966, 55.887),
]

DEPTH_ROWS = [
    DepthRow(1, 31.0, -0.2422, 0.969, -0.589),
    DepthRow(2, 30.0, -0.2718, 0.967, -0.696),
    DepthRow(3, 29.0, -0.2989, 0.966, -0.793),
    DepthRow(4, 28.0, -0.3226, 0.965, -0.877),
]


def _fmt(x: float, ndp: int = 3) -> str:
    return f"{x:.{ndp}f}"


def _phasor(phi: float) -> tuple[float, float]:
    return math.cos(phi), math.sin(phi)


def build_report() -> str:
    ref = STRENGTH_ROWS[0]
    ref_x, ref_y = _phasor(ref.phase_lag)

    hi = STRENGTH_ROWS[2]
    hi_x, hi_y = _phasor(hi.phase_lag)

    hi_x_norm = hi_x / ref_x if abs(ref_x) > 1e-30 else 0.0
    hi_y_norm = hi_y / ref_y if abs(ref_y) > 1e-30 else 0.0
    hi_phi_norm = hi.phase_lag / ref.phase_lag if abs(ref.phase_lag) > 1e-30 else 0.0
    hi_slope_norm = hi.ramp_slope / ref.ramp_slope if abs(ref.ramp_slope) > 1e-30 else 0.0

    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("DIAMOND PHASE-RAMP BRIDGE CARD")
    lines.append("  proxy-level bridge card, not an absolute NV claim")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Bridge row")
    lines.append("  retained exact-family row: s = 0.004")
    lines.append(f"  raw proxy phasor: X = {hi_x:+.3f}, Y = {hi_y:+.3f}, phi = {hi.phase_lag:+.3f} rad")
    lines.append(f"  raw phase-ramp slope: {hi.ramp_slope:+.4f} rad / z")
    lines.append(
        "  normalized to the s = 0.001 reference row:"
        f" X = {hi_x_norm:+.3f}, Y = {hi_y_norm:+.3f}, phi = {hi_phi_norm:+.3f}, slope = {hi_slope_norm:+.3f}"
    )
    lines.append("")
    lines.append("Source-strength sweep")
    lines.append("  s       phi(rad)   ramp_slope(rad/z)   phi/s      slope/s     wave/same")
    lines.append("  ------  ---------  -----------------  -------   ---------   ---------")
    for row in STRENGTH_ROWS:
        phi_over_s = row.phase_lag / row.s
        slope_over_s = row.ramp_slope / row.s
        lines.append(
            f"  {row.s:0.4f}  {row.phase_lag:+9.3f}  {row.ramp_slope:+17.4f}"
            f"  {phi_over_s:+7.1f}   {slope_over_s:+9.1f}   {row.wave_same_ratio:9.3f}"
        )
    lines.append("")
    lines.append("Nearby separation / depth change")
    lines.append("  layer  depth   phase_lag(rad)   ramp_slope(rad/z)   R^2")
    lines.append("  -----  -----   --------------   -----------------   ----")
    for row in DEPTH_ROWS:
        lines.append(
            f"  {row.layer:5d}  {row.depth:5.0f}   {row.phase_lag:+14.3f}   {row.ramp_slope:+17.4f}   {row.ramp_r2:4.3f}"
        )
    lines.append("")
    lines.append("Narrow conclusion")
    lines.append(
        "  the proxy bridge is strong enough to hand to a diamond/NV collaborator,"
        " but the absolute NV transfer coefficient is still missing"
    )
    lines.append(
        "  the cleanest tightening handle is the normalized phase-ramp slope,"
        " together with the small source-strength and depth sweeps"
    )
    return "\n".join(lines)


def main() -> int:
    print(build_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
