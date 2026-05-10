#!/usr/bin/env python3
"""Diamond/NV experiment-facing protocol probe.

This is a small theory harness, not an experimental simulator.

It prints the narrowest lab-facing protocol we can defend from the cited
retarded / wavefield proxy lanes:

- standard null: calibrated quasi-static coupling gives Y ~ 0 and flat phase
- cited proxy expectation: a phase-sensitive / lock-in readout should show a
  nonzero quadrature channel, a nonzero phase lag, and ideally a spatial phase
  ramp in widefield mode

The repo cannot yet support calibrated absolute gravity amplitudes, so the
output stays qualitative and discriminator-first.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class ScanClass:
    drive_band: str
    separation_band: str
    null_x: str
    null_y: str
    null_phi: str
    proxy_expectation: str


SCAN_CLASSES = [
    ScanClass(
        drive_band="low",
        separation_band="near",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="weak / marginal phase-lag candidate",
    ),
    ScanClass(
        drive_band="low",
        separation_band="far",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="weak phase lag if the lane is real",
    ),
    ScanClass(
        drive_band="mid",
        separation_band="near",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="detectable quadrature becomes plausible",
    ),
    ScanClass(
        drive_band="mid",
        separation_band="far",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="stronger phase lag than near separation",
    ),
    ScanClass(
        drive_band="high",
        separation_band="near",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="stronger phase-sensitive response than low drive",
    ),
    ScanClass(
        drive_band="high",
        separation_band="far",
        null_x="dominant",
        null_y="~0",
        null_phi="~0",
        proxy_expectation="best candidate for coherent Y / phase ramp",
    ),
]


def format_card() -> str:
    lines: list[str] = []
    lines.append("Diamond/NV phase-sensitive protocol card")
    lines.append("")
    lines.append("Observable:")
    lines.append("  lock-in quadrature Y, phase lag phi = atan2(Y, X), widefield phase ramp")
    lines.append("")
    lines.append("Standard null:")
    lines.append("  calibrated quasi-static / instantaneous coupling -> Y ~ 0, phi ~ 0, flat phase")
    lines.append("")
    lines.append("Cited proxy expectation:")
    lines.append("  a retarded / wave-like lane should produce nonzero Y, nonzero phi, and a spatial phase ramp")
    lines.append("")
    lines.append("Minimal controls:")
    lines.append("  drive off; source retracted or dummy load; pi reference flip; static-source baseline")
    lines.append("")
    lines.append("Protocol table:")
    lines.append("| drive | separation | null X | null Y | null phi | proxy expectation |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in SCAN_CLASSES:
        lines.append(
            f"| {row.drive_band} | {row.separation_band} | {row.null_x} | {row.null_y} | {row.null_phi} | {row.proxy_expectation} |"
        )
    lines.append("")
    lines.append("Interpretation rule:")
    lines.append("  any real signal should survive calibration, flip sign under the pi control, and strengthen with drive and separation")
    lines.append("")
    lines.append("What this is not:")
    lines.append("  not an absolute gravity amplitude budget, and not a claim that the null is already beat")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a bounded diamond/NV experiment-facing protocol card."
    )
    return parser.parse_args()


def main() -> int:
    parse_args()
    print(format_card())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
