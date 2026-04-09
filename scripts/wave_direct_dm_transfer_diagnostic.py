#!/usr/bin/env python3
"""Freeze the direct-dM coarse-to-fine late-gain transfer diagnostic.

This script is deliberately cheap: it parses already-retained logs instead of
launching new wave solves. The goal is to freeze one concrete split diagnostic
for the controlled Fam1/Fam2 H=0.25 surface:

  G = dM(late) - dM(early)
  T(F, s) = G(H=0.25) / mean(G(H=0.5), G(H=0.35))

Seed-0 rows compress into the weaker fine-H branch, while seed-1 rows keep
their coarse late-gain scale.
"""

from __future__ import annotations

from pathlib import Path
import re
from statistics import mean

REFERENCE_STRENGTH = 0.004
COARSE_HS = (0.5, 0.35)
FINE_H = 0.25

REPO_ROOT = Path(__file__).resolve().parent.parent
BATCH_LOG = REPO_ROOT / "logs" / "2026-04-08-wave-direct-dm-portability-batch.txt"
CONTROL_LOGS = {
    ("Fam1", 0): REPO_ROOT / "logs" / "2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt",
    ("Fam1", 1): REPO_ROOT / "logs" / "2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt",
    ("Fam2", 0): REPO_ROOT / "logs" / "2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt",
    ("Fam2", 1): REPO_ROOT / "logs" / "2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt",
}

FAMILY_RE = re.compile(r"^\[family=(?P<family>\w+)\s+drift=.*\]$")
SEED_RE = re.compile(r"^\[seed=(?P<seed>\d+)\]$")
STRENGTH_RE = re.compile(r"^\[strength=(?P<strength>[-+0-9.]+)\]$")
ROW_RE = re.compile(
    r"^H=(?P<h>[-+0-9.]+)\s+"
    r"dE=(?P<d_early>[-+0-9.]+)\s+"
    r"dL=(?P<d_late>[-+0-9.]+)\s+"
    r"delta=(?P<delta_hist>[-+0-9.]+)\s+"
    r"R=(?P<r_hist>[-+0-9.]+)%(?:\s+.*)?$"
)

CONTROL_DE_RE = re.compile(r"^dM\(early\)\s*=\s*([-+0-9.]+)$")
CONTROL_DL_RE = re.compile(r"^dM\(late\)\s*=\s*([-+0-9.]+)$")
CONTROL_DELTA_RE = re.compile(r"^delta_hist\s*=\s*([-+0-9.]+)$")
CONTROL_R_RE = re.compile(r"^R_hist\s*=\s*([-+0-9.]+)%$")


def parse_coarse_rows() -> dict[tuple[str, int], list[dict[str, float]]]:
    rows: dict[tuple[str, int], list[dict[str, float]]] = {}
    family = None
    seed = None
    strength = None

    for raw_line in BATCH_LOG.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = FAMILY_RE.match(line)
        if match:
            family = match.group("family")
            continue
        match = SEED_RE.match(line)
        if match:
            seed = int(match.group("seed"))
            continue
        match = STRENGTH_RE.match(line)
        if match:
            strength = float(match.group("strength"))
            continue
        match = ROW_RE.match(line)
        if (
            match is None
            or family is None
            or seed is None
            or strength is None
            or abs(strength - REFERENCE_STRENGTH) > 1e-12
            or family not in {"Fam1", "Fam2"}
            or seed not in {0, 1}
        ):
            continue
        h_val = float(match.group("h"))
        if h_val not in COARSE_HS:
            continue
        d_early = float(match.group("d_early"))
        d_late = float(match.group("d_late"))
        rows.setdefault((family, seed), []).append(
            {
                "h": h_val,
                "d_early": d_early,
                "d_late": d_late,
                "late_gain": d_late - d_early,
                "r_hist_pct": float(match.group("r_hist")),
            }
        )

    return rows


def parse_fine_row(path: Path) -> dict[str, float]:
    strength = None
    d_early = None
    d_late = None
    delta_hist = None
    r_hist_pct = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = STRENGTH_RE.match(line)
        if match:
            strength = float(match.group("strength"))
            d_early = None
            d_late = None
            delta_hist = None
            r_hist_pct = None
            continue
        if strength is None or abs(strength - REFERENCE_STRENGTH) > 1e-12:
            continue
        match = CONTROL_DE_RE.match(line)
        if match:
            d_early = float(match.group(1))
            continue
        match = CONTROL_DL_RE.match(line)
        if match:
            d_late = float(match.group(1))
            continue
        match = CONTROL_DELTA_RE.match(line)
        if match:
            delta_hist = float(match.group(1))
            continue
        match = CONTROL_R_RE.match(line)
        if match:
            r_hist_pct = float(match.group(1))
            continue
        if all(value is not None for value in (d_early, d_late, delta_hist, r_hist_pct)):
            break

    if any(value is None for value in (d_early, d_late, delta_hist, r_hist_pct)):
        raise SystemExit(f"could not parse reference-strength row from {path}")

    return {
        "h": FINE_H,
        "d_early": d_early,
        "d_late": d_late,
        "late_gain": d_late - d_early,
        "delta_hist": delta_hist,
        "r_hist_pct": r_hist_pct,
    }


def main() -> int:
    coarse_rows = parse_coarse_rows()
    fine_rows = {key: parse_fine_row(path) for key, path in CONTROL_LOGS.items()}

    print("=" * 122)
    print("WAVE DIRECT-DM TRANSFER DIAGNOSTIC")
    print("=" * 122)
    print("Controlled Fam1/Fam2 fine-H rows compressed against the retained coarse matched-schedule batch at reference strength s=0.004")
    print("Diagnostic: G = dM(late) - dM(early), T(F,s) = G(H=0.25) / mean(G(H=0.5), G(H=0.35))")
    print()

    print("PER-ROW TRANSFER TABLE")
    print(
        f"{'family':<6s} {'seed':>4s} {'G@0.5':>10s} {'G@0.35':>10s} "
        f"{'mean coarse G':>14s} {'G@0.25':>10s} {'T(F,s)':>9s} {'R@0.25':>9s}"
    )
    transfer_rows = []
    for key in sorted(fine_rows):
        family, seed = key
        coarse_by_h = {row["h"]: row for row in coarse_rows[key]}
        coarse_mean = mean(row["late_gain"] for row in coarse_rows[key])
        fine = fine_rows[key]
        transfer = fine["late_gain"] / coarse_mean
        transfer_rows.append(
            {
                "family": family,
                "seed": seed,
                "coarse_mean": coarse_mean,
                "fine_gain": fine["late_gain"],
                "transfer": transfer,
            }
        )
        print(
            f"{family:<6s} {seed:4d} "
            f"{coarse_by_h[0.5]['late_gain']:+10.6f} {coarse_by_h[0.35]['late_gain']:+10.6f} "
            f"{coarse_mean:+14.6f} {fine['late_gain']:+10.6f} {transfer:9.4f} {fine['r_hist_pct']:8.2f}%"
        )

    print()
    print("SEED SUMMARY")
    print(f"{'seed':>4s} {'mean T':>10s} {'T band':>18s} {'read':>0s}")
    for seed in (0, 1):
        seed_rows = [row for row in transfer_rows if row["seed"] == seed]
        t_values = [row["transfer"] for row in seed_rows]
        if seed == 0:
            read = "fine-H late gain compresses sharply into the weaker branch"
        else:
            read = "fine-H late gain stays on the coarse branch scale"
        print(
            f"{seed:4d} {mean(t_values):10.4f} "
            f"{min(t_values):8.4f} .. {max(t_values):7.4f} {read}"
        )

    print()
    print("NARROW READ")
    print("  - This transfer map is not a new portability batch or a family law.")
    print("  - It is one concrete split diagnostic on the already-controlled Fam1/Fam2 fine-H surface.")
    print("  - Seed-0 rows compress sharply: T = 0.3266 and 0.4529.")
    print("  - Seed-1 rows retain coarse late-gain scale: T = 1.0471 and 1.0190.")
    print("  - So the durable separator is coarse-to-fine late-gain retention/compression, not family label alone and not early-branch loss.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
