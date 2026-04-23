#!/usr/bin/env python3
"""Audit the C^16 taste-cell one-sixteenth lane honestly.

This lane does not claim full Planck closure. It proves a sharp reduction:

  - the same structural 2^4 = 16 that appears in the hierarchy/taste lane
    gives an exact primitive-cell share 1/16 on the minimal 4D taste-cell cube
  - conditioning the same full democratic C^16 state to the hw=1 axis sector
    gives the exact democratic four-state carrier with 2 bits
  - therefore 1/32 per bit is exactly (1/16) / 2 on the same underlying carrier

The still-open step is the physical identification q_* = primitive-cell share.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md"
P2 = ROOT / "docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md"
RIGHT = ROOT / "scripts/frontier_right_handed_sector.py"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def bit_entropy(probabilities: list[float]) -> float:
    return -sum(p * math.log(p, 2) for p in probabilities if p > 0.0)


def main() -> int:
    lane = normalized(LANE)
    timelock = normalized(TIMELOCK)
    p2 = normalized(P2)
    right = normalized(RIGHT)

    n_pass = 0
    n_fail = 0

    print("Planck C^16 taste-cell one-sixteenth lane audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY ALIGNMENT")
    p = check(
        "hierarchy support still identifies the structural 16 as 2^4",
        "16 = 2^4 tastes" in p2 or "2^4 = 16" in p2,
        "the comparison target must be the structural four-dimensional taste/corner count",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "non-hierarchy C^16 support still exists on the 4D carrier",
        "c^16" in right and "2^4 = 16" in right,
        "the full 4D carrier beyond the hierarchy lane is already present in the repo",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "time-locked information lane still fixes 2 bits and 1/32 per bit",
        "log 4" in timelock and "1/32" in timelock,
        "the new lane must connect to the existing Planck information target rather than replace it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: FULL C^16 TASTE-CELL CUBE")
    states = list(itertools.product((0, 1), repeat=4))
    dim = len(states)
    rho = np.eye(dim, dtype=float) / dim

    p = check(
        "the minimal 4D cell carrier has exactly 16 primitive states",
        dim == 16,
        "eta in {0,1}^4 gives the exact 2^4 = 16 structural carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    fine_weights = []
    for idx, eta in enumerate(states):
        proj = np.zeros((dim, dim), dtype=float)
        proj[idx, idx] = 1.0
        fine_weights.append(float(np.trace(rho @ proj)))

    p = check(
        "each primitive taste cell carries exact share 1/16 on the democratic full-cell state",
        all(abs(w - 1.0 / 16.0) < 1.0e-15 for w in fine_weights),
        "rho_cell = I_16 / 16 assigns equal fine weight to every primitive cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    fine_entropy = bit_entropy(fine_weights)
    p = check(
        "the full democratic C^16 carrier has exactly 4 bits of entropy",
        abs(fine_entropy - 4.0) < 1.0e-15,
        "uniform distribution on 16 states has log2(16) = 4 bits",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: HW=1 AXIS SECTOR")
    axis_states = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    axis_indices = [states.index(state) for state in axis_states]
    p_axis = np.zeros((dim, dim), dtype=float)
    for idx in axis_indices:
        p_axis[idx, idx] = 1.0

    axis_mass = float(np.trace(rho @ p_axis))
    conditioned = (p_axis @ rho @ p_axis) / axis_mass
    coarse_weights = [float(conditioned[idx, idx]) for idx in axis_indices]

    p = check(
        "the hw=1 axis sector has exactly four canonical states",
        len(axis_indices) == 4 and axis_mass == 0.25,
        "there are four Hamming-weight-one axis cells, carrying total mass 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "conditioning to the axis sector gives the exact democratic four-state carrier",
        all(abs(w - 0.25) < 1.0e-15 for w in coarse_weights),
        "rho_A = P_A rho P_A / Tr(rho P_A) = I_4 / 4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    coarse_entropy = bit_entropy(coarse_weights)
    p = check(
        "the conditioned axis carrier has exactly 2 bits",
        abs(coarse_entropy - 2.0) < 1.0e-15,
        "uniform distribution on the four axis states has log2(4) = 2 bits",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: EXACT 1/32 PER BIT FROM THE SAME CARRIER")
    q_cell = 1.0 / 16.0
    kappa_bits = q_cell / coarse_entropy
    p = check(
        "the exact coarse/fine ratio is 1/32 per bit",
        abs(kappa_bits - 1.0 / 32.0) < 1.0e-15,
        f"(1/16) / 2 = {kappa_bits:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the new lane keeps the structural and defect 16s conceptually distinct",
        "conceptually different `16`s" in lane
        and "full 4d cell count" in lane
        and "einstein/regge defect coefficient" in lane,
        "exact Planck may identify the two coefficient chains, but they are not the same theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the lane honestly marks one remaining physical-identification step",
        "not yet a closure theorem" in lane
        and "remaining open step" in lane
        and "physical elementary action phase" in lane,
        "the writeup must present this as a reduction theorem rather than as a fake closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The Planck-lane 1/16 can be realized exactly as the primitive-cell "
        "share of the same structural 2^4 = 16 four-bit carrier that appears "
        "in the hierarchy/taste lane. Conditioning the same democratic full "
        "carrier to the hw=1 axis sector yields the exact four-state carrier "
        "with 2 bits, so 1/32 per bit is exactly (1/16)/2 on one and the same "
        "underlying C^16 object. The surviving gap is the physical law "
        "q_* = primitive-cell share."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
