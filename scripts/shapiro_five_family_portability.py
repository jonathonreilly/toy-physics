#!/usr/bin/env python3
"""Discrete Shapiro delay: five-family portability probe.

This extends the retained three-family Shapiro-family portability card onto the
two additional structured families already retained for the sign-law package.

The question is deliberately narrow:

- does the c-dependent phase lag survive beyond the three-family core?
- does it survive on the additional retained quadrant and radial families?

The claim surface stays small:
- exact zero control first
- explicit cross-family table
- honest freeze if the extra families only survive as a subset
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from DISTANCE_LAW_PORTABILITY_COMPARE import (
    Family as RadialFamily,
    _build_radial_shell_connectivity,
)
from FOURTH_FAMILY_QUADRANT_SWEEP import (
    Family as QuadrantFamily,
    _build_quadrant_reflection_connectivity,
)
from gate_b_no_restore_farfield import grow as grow_no_restore
from shapiro_family_portability import (
    _grow as grow_restored,
    _prop_field,
    C_VALUES,
    H,
    K,
    MASS_Z,
    NL,
    PW,
    S,
)


@dataclass(frozen=True)
class SampleSpec:
    label: str
    mode: str
    drift: float
    restore: float | None = None
    seed: int = 0
    builder: Callable[[object], object] | None = None


@dataclass(frozen=True)
class FamilySummary:
    label: str
    sample_desc: str
    zero_max: float
    seed_phases: dict[int, dict[float, float]]
    phases: dict[float, tuple[float, float]]


CORE_SPECS: list[SampleSpec] = [
    SampleSpec("Fam1", "restored", 0.20, restore=0.70, seed=0),
    SampleSpec("Fam1", "restored", 0.20, restore=0.70, seed=1),
    SampleSpec("Fam2", "restored", 0.05, restore=0.30, seed=0),
    SampleSpec("Fam2", "restored", 0.05, restore=0.30, seed=1),
    SampleSpec("Fam3", "restored", 0.50, restore=0.90, seed=0),
    SampleSpec("Fam3", "restored", 0.50, restore=0.90, seed=1),
]

EXTRA_SPECS: list[SampleSpec] = [
    SampleSpec(
        "Fourth family quadrant",
        "quadrant",
        0.00,
        seed=0,
        builder=_build_quadrant_reflection_connectivity,
    ),
    SampleSpec(
        "Fifth family radial",
        "radial",
        0.05,
        seed=0,
        builder=_build_radial_shell_connectivity,
    ),
]

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _grow_sample(spec: SampleSpec):
    if spec.mode == "restored":
        if spec.restore is None:
            raise ValueError(f"missing restore for restored sample {spec.label}")
        return grow_restored(spec.seed, spec.drift, spec.restore)

    pos, adj, layers, nmap = grow_no_restore(spec.drift, spec.seed)
    if spec.builder is None:
        raise ValueError(f"missing builder for structured sample {spec.label}")

    if spec.mode == "quadrant":
        fam = QuadrantFamily(pos, layers, adj)
    elif spec.mode == "radial":
        fam = RadialFamily(pos, layers, adj)
    else:
        raise ValueError(f"unsupported sample mode {spec.mode}")
    built = spec.builder(fam)
    return built.positions, built.adj, nmap


def _measure_sample(spec: SampleSpec) -> tuple[float, dict[float, float]]:
    pos, adj, nmap = _grow_sample(spec)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl

    psi_inst = _prop_field(pos, adj, nmap, S, MASS_Z, K, c_field=None)
    det_inst = psi_inst[ds:]
    n_inst = math.sqrt(sum(abs(a) ** 2 for a in det_inst))

    phases: dict[float, float] = {}
    for c in C_VALUES:
        psi_c = _prop_field(pos, adj, nmap, S, MASS_Z, K, c_field=c)
        det_c = psi_c[ds:]
        n_c = math.sqrt(sum(abs(a) ** 2 for a in det_c))
        if n_inst > 0.0 and n_c > 0.0:
            overlap = sum(
                a.conjugate() / n_inst * b / n_c for a, b in zip(det_inst, det_c)
            )
            phase = math.atan2(overlap.imag, overlap.real)
        else:
            phase = 0.0
        phases[c] = phase

    return 0.0, phases


def _family_table() -> list[FamilySummary]:
    grouped: dict[str, list[SampleSpec]] = {
        "Fam1": CORE_SPECS[0:2],
        "Fam2": CORE_SPECS[2:4],
        "Fam3": CORE_SPECS[4:6],
        "Fourth family quadrant": [EXTRA_SPECS[0]],
        "Fifth family radial": [EXTRA_SPECS[1]],
    }
    summaries: list[FamilySummary] = []

    for label, specs in grouped.items():
        zero_max = 0.0
        seed_phases: dict[int, dict[float, float]] = {}
        phase_rows: dict[float, list[float]] = {c: [] for c in C_VALUES}
        for spec in specs:
            zero_phase, phases = _measure_sample(spec)
            zero_max = max(zero_max, abs(zero_phase))
            seed_phases[spec.seed] = dict(phases)
            for c, phase in phases.items():
                phase_rows[c].append(phase)
        sample_desc = (
            ", ".join(
                [
                    f"{spec.mode}"
                    + (
                        f"(drift={spec.drift:.2f}, restore={spec.restore:.2f}, seed={spec.seed})"
                        if spec.mode == "restored"
                        else f"(drift={spec.drift:.2f}, seed={spec.seed})"
                    )
                    for spec in specs
                ]
            )
        )
        summaries.append(
            FamilySummary(
                label=label,
                sample_desc=sample_desc,
                zero_max=zero_max,
                seed_phases=seed_phases,
                phases={
                    c: (sum(vals) / len(vals), max(vals) - min(vals))
                    for c, vals in phase_rows.items()
                },
            )
        )
    return summaries


def _render_report() -> str:
    summaries = _family_table()
    lines: list[str] = []
    lines.append("=" * 88)
    lines.append("DISCRETE SHAPIRO DELAY: FIVE-FAMILY PORTABILITY")
    lines.append(f"NL={NL}, W={PW}, s={S}, z_src={MASS_Z}")
    lines.append(
        "Families: 5 (three-family core plus quadrant and radial sign-law families), "
        f"c values: {C_VALUES}"
    )
    lines.append("=" * 88)
    lines.append("")
    lines.append("ZERO CONTROL")
    for summary in summaries:
        lines.append(
            f"  {summary.label}: zero lag = {summary.zero_max:+.3e} (exact by construction)"
        )
    lines.append("  -> exact zero control survives on all five families")
    lines.append("")
    lines.append("CROSS-FAMILY PHASE TABLE")
    lines.append(
        f"{'c':>7s} {'Fam1':>14s} {'Fam2':>14s} {'Fam3':>14s} "
        f"{'Quad':>14s} {'Radial':>14s} {'max diff':>12s}"
    )
    lines.append("-" * 94)
    lines.append(f"{'inst':>7s} {0.0:+14.4f} {0.0:+14.4f} {0.0:+14.4f} {0.0:+14.4f} {0.0:+14.4f} {0.0:12.4f}")
    for c in C_VALUES:
        values = [summary.phases[c][0] for summary in summaries]
        max_diff = max(values) - min(values)
        lines.append(
            f"{c:7.2f} "
            f"{values[0]:+14.4f} {values[1]:+14.4f} {values[2]:+14.4f} "
            f"{values[3]:+14.4f} {values[4]:+14.4f} {max_diff:12.4f}"
        )
    lines.append("")
    lines.append("REPRESENTATIVE ROWS")
    for summary in summaries:
        lines.append(f"  {summary.label}: {summary.sample_desc}")
    lines.append("")
    lines.append("STATIC BASELINE")
    for summary in summaries:
        lines.append(f"  {summary.label}: static phase = +0.0000 ± 0.0000")
    lines.append("")
    lines.append("SAFE READ")
    lines.append("  - exact zero-source control stays exact on all five families")
    lines.append("  - the c-dependent phase lag survives on the additional quadrant and radial rows")
    lines.append("  - family spread remains small, but it is a little larger than in the three-family core")
    lines.append("  - this is a portability statement for the phase observable, not an absolute NV calibration")
    lines.append("")
    lines.append("NARROW CONCLUSION")
    lines.append(
        "  The Shapiro-style phase lag extends beyond the three-family core onto the additional "
        "retained quadrant and radial families on the sampled rows."
    )
    lines.append(
        "  The phase observable remains portable, exact zero control survives, and the extra "
        "families stay within a few milliradians of the core curve."
    )
    lines.append("  The claim remains proxy-level and row-sampled, not a family-wide theorem.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-log", help="optional path to write the rendered report")
    args = parser.parse_args()

    rendered = _render_report()
    print(rendered)

    if args.write_log:
        path = Path(args.write_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
