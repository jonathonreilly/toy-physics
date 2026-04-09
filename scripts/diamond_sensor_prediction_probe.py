#!/usr/bin/env python3
"""Diamond/NV phase-sensitive prediction probe.

This is a small theory harness, not an experimental simulator.

It packages the smallest defensible lab-facing discriminator from the
retained retarded / wavefield lanes:

- standard null: calibrated quasi-static / instantaneous response -> zero
  quadrature and flat phase
- retained prediction: finite delay -> nonzero lock-in quadrature and a
  phase lag that grows with omega * tau

The script prints a compact prediction card that a diamond/NV collaborator can
read quickly or adapt to a lab geometry.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionPoint:
    frequency_hz: float
    delay_s: float

    @property
    def omega_tau(self) -> float:
        return 2.0 * math.pi * self.frequency_hz * self.delay_s

    @property
    def phase_rad(self) -> float:
        return math.atan(self.omega_tau)

    @property
    def phase_deg(self) -> float:
        return math.degrees(self.phase_rad)


def build_points(freqs_hz: list[float], delays_s: list[float]) -> list[PredictionPoint]:
    return [
        PredictionPoint(frequency_hz=f, delay_s=t)
        for t in delays_s
        for f in freqs_hz
    ]


def format_card(points: list[PredictionPoint]) -> str:
    lines: list[str] = []
    lines.append("Diamond/NV phase-sensitive prediction card")
    lines.append("")
    lines.append("Observable:")
    lines.append("  lock-in quadrature Y, phase lag phi = atan2(Y, X), and widefield phase ramp")
    lines.append("")
    lines.append("Standard null:")
    lines.append("  after calibration, quasi-static / instantaneous coupling gives Y ~ 0 and flat phase")
    lines.append("")
    lines.append("Retained prediction:")
    lines.append("  finite delay gives Y != 0, phi != 0, and a coherent spatial phase ramp")
    lines.append("")
    lines.append("Minimal controls:")
    lines.append("  drive off; source retracted / dummy load; pi reference flip; static-source baseline")
    lines.append("")
    lines.append("Toy scaling law:")
    lines.append("  Y/X ~ omega * tau, phi = atan(omega * tau)")
    lines.append("")
    lines.append("| f (Hz) | tau (us) | omega*tau | phi (deg) |")
    lines.append("| --- | ---: | ---: | ---: |")
    for p in points:
        lines.append(
            f"| {p.frequency_hz:.0f} | {p.delay_s * 1e6:.3f} | {p.omega_tau:.3e} | {p.phase_deg:.3e} |"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a bounded diamond/NV phase-sensitive prediction card."
    )
    parser.add_argument(
        "--freq-hz",
        type=float,
        nargs="+",
        default=[1e2, 1e3, 1e4],
        help="Drive frequencies in Hz for the toy phase-lag table.",
    )
    parser.add_argument(
        "--delay-us",
        type=float,
        nargs="+",
        default=[0.0, 0.1, 1.0],
        help="Effective delay values in microseconds for the toy table.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    points = build_points(args.freq_hz, [d * 1e-6 for d in args.delay_us])
    print(format_card(points))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
