#!/usr/bin/env python3
"""
Expanded chiral core card scaffold.

This script is intentionally lightweight: it does not run the heavy physics
tests. It encodes the current best N-card structure so the next integrated
harness can wire it up without guessing the row set or ordering.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BottleneckRow:
    code: str
    title: str
    category: str
    target: str
    readout: str
    why_it_matters: str


ROWS = [
    BottleneckRow(
        code="C1",
        title="Born barrier / slit |I3|/P",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="three-slit |I3|/P with absorptive blocking",
        why_it_matters="Still the non-negotiable linearity/interference gate.",
    ),
    BottleneckRow(
        code="C2",
        title="d_TV / slit distinguishability",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="total variation distance between slit-resolved branches",
        why_it_matters="Checks that the slit harness is informative rather than degenerate.",
    ),
    BottleneckRow(
        code="C3",
        title="Null control (k=0 or f=0)",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="no-field / no-phase baseline drift",
        why_it_matters="Protects against built-in drift being mistaken for gravity.",
    ),
    BottleneckRow(
        code="C4",
        title="F∝M scaling",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="weak-field log-log exponent and linear fit quality",
        why_it_matters="Keeps the gravity claim honest at first order.",
    ),
    BottleneckRow(
        code="C5",
        title="Gravity sign at retained operating point",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="TOWARD/AWAY sign and magnitude",
        why_it_matters="Still the minimal gravity gate.",
    ),
    BottleneckRow(
        code="C6",
        title="Decoherence / record proxy",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="purity drop / branch-environment coupling proxy",
        why_it_matters="Retains the measurement-side pressure in the core card.",
    ),
    BottleneckRow(
        code="C7",
        title="Mutual information",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="branch correlation strength",
        why_it_matters="Useful companion to decoherence and purity.",
    ),
    BottleneckRow(
        code="C8",
        title="Purity stability",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="purity variability across the scanned window",
        why_it_matters="Guards against one lucky purity operating point.",
    ),
    BottleneckRow(
        code="C9",
        title="Gravity growth with propagation",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="sign and magnitude trend over propagation depth",
        why_it_matters="Checks that the signal is a real trend rather than one layer count.",
    ),
    BottleneckRow(
        code="C10",
        title="Distance law",
        category="operating-point",
        target="existing chiral closure-card harness",
        readout="offset exponent and fit quality",
        why_it_matters="Still needed, but no longer overread as the whole gravity story.",
    ),
    BottleneckRow(
        code="C11",
        title="3D KG isotropy / coupled-coin dispersion",
        category="structural",
        target="3+1D coupled coin scan",
        readout="E^2 vs k^2 R^2, axis/diagonal slope spread, isotropy ratio",
        why_it_matters="Fails immediately if the coin remains factorized across axes.",
    ),
    BottleneckRow(
        code="C12",
        title="3D gauge-loop / AB visibility",
        category="structural",
        target="3+1D closed-loop flux harness",
        readout="Wilson loop visibility, pure-gauge invariance, detector contrast",
        why_it_matters="Detects whether 3D gauge response really exists or only a lower-D proxy.",
    ),
    BottleneckRow(
        code="C13",
        title="Fixed-theta k-achromaticity",
        category="structural",
        target="1D or 2D corrected carrier-k sweep",
        readout="deflection CV across k at fixed theta and matched travel distance",
        why_it_matters="Separates structural gravity from wave-window chromaticity.",
    ),
    BottleneckRow(
        code="C14",
        title="Theta vs gravity-susceptibility split",
        category="structural",
        target="separated mass and gravity couplings",
        readout="deflection vs theta_m and vs g_f in the same harness",
        why_it_matters="Tests whether theta is overloaded as mass plus gravity response.",
    ),
    BottleneckRow(
        code="C15",
        title="Boundary-condition robustness",
        category="structural",
        target="periodic / reflecting / open sweep at fixed delta and lambda",
        readout="sign-map stability, TOWARD fraction, recurrence windows",
        why_it_matters="Exposes wrap and recurrence artifacts before they are mistaken for physics.",
    ),
    BottleneckRow(
        code="C16",
        title="Multi-observable gravity consistency",
        category="structural",
        target="single-run observable panel",
        readout="first-arrival, peak, current, centroid, torus-aware centroid",
        why_it_matters="Shows whether gravity is real or only one readout is drifting.",
    ),
]


def print_rows() -> None:
    print("Chiral Expanded Core Card (N=16)")
    print("=" * 36)
    for row in ROWS:
        print(f"{row.code} [{row.category}] | {row.title}")
        print(f"  target: {row.target}")
        print(f"  readout: {row.readout}")
        print(f"  why: {row.why_it_matters}")
        print()


if __name__ == "__main__":
    print_rows()
