#!/usr/bin/env python3
"""Canonical reconstruction for the retained Shapiro scaling laws.

This is the smallest honest artifact-chain replay for the scaling result that
was already anchored on main in commit 1730b52. It does not rerun a fresh
physics sweep. Instead, it reconstructs the retained scaling card from:

* the exact zero-control phase table already retained in the Shapiro delay
  lane,
* the portable family replay,
* the diamond frequency bridge note, and
* the commit-1730b52 scaling anchor.

The goal is to keep the exact controls explicit while freezing the three
scaling statements that are already retained on main:

* phase is linear in source strength / mass proxy
* phase decreases with impact parameter b
* phase is proportional to k
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

from shapiro_phase_lag_probe import PHASE_ROWS


DATE = "2026-04-06"
ANCHOR_COMMIT = "1730b52"
ANCHOR_COMMIT_MSG = "feat(shapiro): phase scales as s^1.000 (linear in mass), proportional to k"


@dataclass(frozen=True)
class ScalingLaw:
    label: str
    exact_control: str
    retained_readout: str
    support: str


SCALING_LAWS = [
    ScalingLaw(
        label="phase ~ s^1.000",
        exact_control="s = 0 -> phase = 0",
        retained_readout="linear in source strength / mass proxy",
        support=f"commit {ANCHOR_COMMIT} + SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE",
    ),
    ScalingLaw(
        label="phase decreases with b",
        exact_control="large-b tail is the low-delay side of the sweep",
        retained_readout="b = 3 -> +0.062 rad; b = 7 -> +0.040 rad",
        support=f"commit {ANCHOR_COMMIT} + retained Shapiro bridge card",
    ),
    ScalingLaw(
        label="phase ~ k",
        exact_control="k -> 0 removes the phase accumulation in the action convention",
        retained_readout="chromatic / frequency-sensitive response",
        support="SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE",
    ),
]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _spread(values: list[float]) -> float:
    return max(values) - min(values) if values else math.nan


def _phase_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
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


def render_markdown() -> str:
    rows = _phase_rows()
    phase_only = [r for r in rows if r["c"] != "inst"]
    max_spread = max(r["spread"] for r in phase_only) if phase_only else 0.0

    lines: list[str] = []
    lines.append("# Shapiro Scaling Note")
    lines.append("")
    lines.append(f"**Date:** {DATE}")
    lines.append(
        "**Status:** reconstruction from retained Shapiro artifacts anchored in commit "
        f"`{ANCHOR_COMMIT}`"
    )
    lines.append("")
    lines.append("## Replay Kind")
    lines.append("")
    lines.append(
        "This is a reconstruction, not a fresh simulation. The retained delay "
        "rows already exist on main; this note freezes the scaling laws they "
        "support."
    )
    lines.append("")
    lines.append("## Artifact Chain")
    lines.append("")
    lines.append("- [`scripts/shapiro_scaling_probe.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_probe.py)")
    lines.append("- [`logs/2026-04-06-shapiro-scaling-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-scaling-probe.txt)")
    lines.append("- [`docs/SHAPIRO_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DELAY_NOTE.md)")
    lines.append("- [`docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md)")
    lines.append("- [`docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)")
    lines.append("- [`docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md)")
    lines.append("- [`docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)")
    lines.append(f"- retained scaling anchor: commit `{ANCHOR_COMMIT}` (`{ANCHOR_COMMIT_MSG}`)")
    lines.append("")
    lines.append("## Exact Controls")
    lines.append("")
    lines.append("- `s = 0` maps to phase `0.000 rad` in the scaling interpretation")
    lines.append("- `c = inst` stays exactly `0.000 rad` in the retained delay table")
    lines.append("- exact zero control survives; this is the first gate for the scaling chain")
    lines.append("")
    lines.append("## Retained Scaling Laws")
    lines.append("")
    lines.append("| law | exact control | retained readout | support |")
    lines.append("| --- | --- | --- | --- |")
    for law in SCALING_LAWS:
        lines.append(
            f"| {law.label} | {law.exact_control} | {law.retained_readout} | {law.support} |"
        )
    lines.append("")
    lines.append("## Retained Delay Table")
    lines.append("")
    lines.append("| c | phase lag mean | family spread | fam1 | fam2 | fam3 |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in phase_only:
        lines.append(
            f"| {row['c']:.2f} | {row['mean']:+.4f} rad | {row['spread']:.4f} rad | "
            f"{row['fam1']:+.4f} | {row['fam2']:+.4f} | {row['fam3']:+.4f} |"
        )
    lines.append("")
    lines.append("## Narrow Read")
    lines.append("")
    lines.append("- the source/mass scaling law is the retained `phase ~ s^1.000` anchor")
    lines.append("- the impact-parameter trend is the retained `b`-decreasing tail")
    lines.append("- the frequency law is the retained `phase ~ k` bridge")
    lines.append(
        f"- family spread on the portable delay table stays at or below `{max_spread:.1e} rad`"
    )
    lines.append("- this is a portability/scaling reconstruction, not a uniqueness proof")
    lines.append("")
    lines.append("## Final Verdict")
    lines.append("")
    lines.append(
        "**the retained Shapiro scaling card is a reconstruction from already-retained "
        "artifacts: phase is linear in source strength / mass proxy, decreases with "
        "impact parameter b, and is proportional to k, with exact zero control explicit**"
    )
    return "\n".join(lines)


def render_text() -> str:
    rows = _phase_rows()
    lines: list[str] = []
    lines.append("SHAPIRO SCALING NOTE")
    lines.append(f"Date: {DATE}")
    lines.append(
        f"Status: reconstruction from retained artifacts anchored in commit {ANCHOR_COMMIT}"
    )
    lines.append("")
    lines.append("Exact controls:")
    lines.append("  - s = 0 -> phase = 0.000 rad")
    lines.append("  - c = inst -> phase = 0.000 rad on all three families")
    lines.append("")
    lines.append("Retained scaling laws:")
    for law in SCALING_LAWS:
        lines.append(f"  - {law.label}: {law.retained_readout} [{law.support}]")
    lines.append("")
    lines.append("Retained delay rows:")
    for row in rows:
        lines.append(
            f"  c={row['c']}: mean={row['mean']:+.4f} rad; spread={row['spread']:.4f} rad; "
            f"fam1={row['fam1']:+.4f}; fam2={row['fam2']:+.4f}; fam3={row['fam3']:+.4f}"
        )
    lines.append("")
    lines.append("Final verdict:")
    lines.append(
        "  reconstruction from retained artifacts; phase is linear in source strength / mass, "
        "decreases with b, and is proportional to k"
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "text", "json"), default="markdown")
    parser.add_argument("--write-log", help="optional path to write the rendered report")
    args = parser.parse_args()

    payload = {
        "anchor_commit": ANCHOR_COMMIT,
        "anchor_commit_msg": ANCHOR_COMMIT_MSG,
        "exact_zero_control": True,
        "replay_kind": "reconstruction",
        "rows": [row.__dict__ for row in PHASE_ROWS],
        "scaling_laws": [law.__dict__ for law in SCALING_LAWS],
        "summary": {
            "source_mass_linear": True,
            "impact_parameter_decreasing": True,
            "k_proportional": True,
            "portable_across_three_families": True,
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
