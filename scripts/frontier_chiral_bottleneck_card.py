#!/usr/bin/env python3
"""
Proposed chiral bottleneck card.

This script is intentionally lightweight: it does not run the heavy physics
tests. It just encodes the proposed early-failure rows so the next harness can
wire them in without guessing the structure.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BottleneckRow:
    code: str
    title: str
    target: str
    readout: str
    why_it_matters: str


ROWS = [
    BottleneckRow(
        code="B1",
        title="3D KG isotropy / coupled-coin dispersion",
        target="3+1D coupled coin scan",
        readout="E^2 vs k^2 R^2, axis/diagonal slope spread, isotropy ratio",
        why_it_matters="Fails immediately if the coin remains factorized across axes.",
    ),
    BottleneckRow(
        code="B2",
        title="3D gauge-loop / AB visibility",
        target="3+1D closed-loop flux harness",
        readout="Wilson loop visibility, pure-gauge invariance, detector contrast",
        why_it_matters="Detects whether 3D gauge response really exists or only a lower-D proxy.",
    ),
    BottleneckRow(
        code="B3",
        title="Fixed-theta k-achromaticity",
        target="1D or 2D corrected carrier-k sweep",
        readout="Deflection CV across k at fixed theta and matched travel distance",
        why_it_matters="Separates structural gravity from wave-window chromaticity.",
    ),
    BottleneckRow(
        code="B4",
        title="Theta vs gravity-susceptibility split",
        target="Separated mass and gravity couplings",
        readout="Deflection vs theta_m and vs g_f in the same harness",
        why_it_matters="Tests whether theta is overloaded as mass plus gravity response.",
    ),
    BottleneckRow(
        code="B5",
        title="Boundary-condition robustness",
        target="Periodic / reflecting / open sweep at fixed delta and lambda",
        readout="Sign-map stability, TOWARD fraction, recurrence windows",
        why_it_matters="Exposes wrap and recurrence artifacts before they are mistaken for physics.",
    ),
    BottleneckRow(
        code="B6",
        title="Multi-observable gravity consistency",
        target="Single-run observable panel",
        readout="First-arrival, peak, current, centroid, torus-aware centroid",
        why_it_matters="Shows whether gravity is real or only one readout is drifting.",
    ),
]


def print_rows() -> None:
    print("Chiral Bottleneck Card Proposal")
    print("=" * 33)
    for row in ROWS:
        print(f"{row.code} | {row.title}")
        print(f"  target: {row.target}")
        print(f"  readout: {row.readout}")
        print(f"  why: {row.why_it_matters}")
        print()


if __name__ == "__main__":
    print_rows()
