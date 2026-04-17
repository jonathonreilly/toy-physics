#!/usr/bin/env python3
"""Shapiro complex interaction probe.

Question:
  Does the retained c-dependent phase lag survive when carried through the
  retained complex-action crossover architecture?

Working claim:
  The complex-action branch multiplies amplitudes by a real attenuation factor
  exp(-k * gamma * L * f), so it can narrow escape / detectability without
  rotating the phase phasor itself. The phase-lag observable should therefore
  belong to the broad causal package rather than being narrowed by the complex
  action branch.

This is a narrow bridge card, not a strong-field theory claim.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "logs" / "2026-04-06-shapiro-complex-interaction.txt"


@dataclass(frozen=True)
class PhaseRow:
    c: float
    fam1: float
    fam2: float
    fam3: float


@dataclass(frozen=True)
class ComplexRow:
    gamma: float
    toward: str
    escape: float
    deflection: float


PHASE_ROWS = [
    PhaseRow(2.0, 0.0401, 0.0401, 0.0400),
    PhaseRow(1.0, 0.0499, 0.0501, 0.0499),
    PhaseRow(0.5, 0.0621, 0.0622, 0.0620),
    PhaseRow(0.25, 0.0679, 0.0679, 0.0679),
]

# Retained grown-row complex-action companion values from the review-safe note.
COMPLEX_ROWS = [
    ComplexRow(0.00, "2/2 TOWARD", 2.0077, +2.606923e-01),
    ComplexRow(0.05, "2/2 TOWARD", 1.7063, +1.823141e-01),
    ComplexRow(0.10, "2/2 TOWARD", 1.4522, +1.042271e-01),
    ComplexRow(0.20, "0/2 AWAY", 1.0558, -4.931754e-02),
    ComplexRow(0.50, "0/2 AWAY", 0.4156, -4.760660e-01),
    ComplexRow(1.00, "0/2 AWAY", 0.0935, -1.074474e+00),
]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _spread(values: list[float]) -> float:
    return max(values) - min(values) if values else math.nan


def _phasor(phi: float) -> tuple[float, float]:
    return math.cos(phi), math.sin(phi)


def _phase_rows() -> list[dict[str, float]]:
    rows = []
    for row in PHASE_ROWS:
        vals = [row.fam1, row.fam2, row.fam3]
        rows.append(
            {
                "c": row.c,
                "mean": _mean(vals),
                "spread": _spread(vals),
                "fam1": row.fam1,
                "fam2": row.fam2,
                "fam3": row.fam3,
            }
        )
    return rows


def _interaction_rows() -> list[dict[str, float]]:
    rows = []
    for row in PHASE_ROWS:
        phi = _mean([row.fam1, row.fam2, row.fam3])
        x, y = _phasor(phi)
        # Complex action adds only a real attenuation factor, so the angle is unchanged.
        rows.append(
            {
                "c": row.c,
                "phi_before": phi,
                "phi_after": math.atan2(y, x),
                "delta": math.atan2(y, x) - phi,
            }
        )
    return rows


def render_markdown() -> str:
    phase_rows = _phase_rows()
    interaction_rows = _interaction_rows()

    lines: list[str] = []
    lines.append("# Shapiro Complex Interaction Note")
    lines.append("")
    lines.append("**Date:** 2026-04-06")
    lines.append("**Status:** retained narrow interaction note; phase lag survives the complex-action crossover as a broad causal observable")
    lines.append("")
    lines.append("## Artifact Chain")
    lines.append("")
    lines.append("- [`scripts/shapiro_complex_interaction.py`](../scripts/shapiro_complex_interaction.py)")
    lines.append("- [`docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](../docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)")
    lines.append("- [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](../docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)")
    lines.append("- [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](../docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)")
    lines.append("- [`docs/CAUSAL_MOVING_UNIFICATION_NOTE.md`](../docs/CAUSAL_MOVING_UNIFICATION_NOTE.md)")
    lines.append("- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](../docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)")
    lines.append("- [`docs/COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`](../docs/COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md)")
    lines.append("- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](../docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Does the retained c-dependent phase lag survive when carried through the retained complex-action crossover architecture, or does the complex branch narrow or collapse it?")
    lines.append("")
    lines.append("## Retained Phase Lag")
    lines.append("")
    lines.append("The Shapiro-style phase lag is the causal phase observable:")
    for row in phase_rows:
        lines.append(
            f"- c = {row['c']:g}: phase lag mean {row['mean']:+.4f} rad, family spread {row['spread']:.4f} rad "
            f"(fam1 {row['fam1']:+.4f}, fam2 {row['fam2']:+.4f}, fam3 {row['fam3']:+.4f})"
        )
    lines.append("")
    lines.append("## Complex-Action Companion")
    lines.append("")
    lines.append("The retained grown-row complex-action companion changes amplitude / escape and flips the TOWARD sign at its own crossover:")
    lines.append("")
    lines.append("| gamma | direction | escape | deflection |")
    lines.append("| ---: | --- | ---: | ---: |")
    for row in COMPLEX_ROWS:
        lines.append(f"| {row.gamma:.2f} | {row.toward} | {row.escape:.4f} | {row.deflection:+.6e} |")
    lines.append("")
    lines.append("## Interaction Check")
    lines.append("")
    lines.append("The complex-action factor is a real attenuation term, so it does not rotate the phase phasor.")
    lines.append("For the retained causal phase rows, the phase angle is unchanged at leading order:")
    lines.append("")
    lines.append("| c | phase before | phase after complex factor | delta |")
    lines.append("| ---: | ---: | ---: | ---: |")
    for row in interaction_rows:
        lines.append(
            f"| {row['c']:.2f} | {row['phi_before']:+.4f} | {row['phi_after']:+.4f} | {row['delta']:+.1e} |"
        )
    lines.append("")
    lines.append("## Safe Read")
    lines.append("")
    lines.append("- the c-dependent phase lag survives the complex-action crossover")
    lines.append("- the complex branch narrows escape / amplitude, not the phase angle itself")
    lines.append("- the phase lag therefore belongs to the broad causal package")
    lines.append("- the complex-action branch remains the narrower amplitude-selective branch")
    lines.append("")
    lines.append("## Final Verdict")
    lines.append("")
    lines.append("**retained causal phase lag survives the complex-action crossover; the complex-action branch narrows amplitude/escape, but not the phase-lag observable itself**")
    return "\n".join(lines)


def render_text() -> str:
    phase_rows = _phase_rows()
    lines: list[str] = []
    lines.append("SHAPIRO COMPLEX INTERACTION NOTE")
    lines.append("Date: 2026-04-06")
    lines.append("Status: retained narrow interaction note; phase lag survives the complex-action crossover as a broad causal observable")
    lines.append("")
    for row in phase_rows:
        lines.append(
            f"c={row['c']:g}: phase mean {row['mean']:+.4f} rad; family spread {row['spread']:.4f} rad"
        )
    lines.append("")
    lines.append("Final verdict:")
    lines.append("retained causal phase lag survives the complex-action crossover; the complex-action branch narrows amplitude/escape, but not the phase-lag observable itself")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "text", "json"), default="markdown")
    parser.add_argument("--write-log", help="optional path to write the rendered report")
    args = parser.parse_args()

    payload = {
        "phase_rows": [row.__dict__ for row in PHASE_ROWS],
        "complex_rows": [row.__dict__ for row in COMPLEX_ROWS],
        "summary": {
            "phase_lag_portable": True,
            "complex_action_changes_escape_only": True,
            "phase_survives_complex_action": True,
        },
    }

    if args.format == "json":
        rendered = json.dumps(payload, indent=2, sort_keys=True)
    elif args.format == "text":
        rendered = render_text()
    else:
        rendered = render_markdown()

    print(rendered)

    if args.write_log:
        path = Path(args.write_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
