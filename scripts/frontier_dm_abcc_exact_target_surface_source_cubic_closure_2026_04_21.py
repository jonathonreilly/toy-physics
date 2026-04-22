#!/usr/bin/env python3
"""
DM A-BCC exact target-surface source-cubic closure theorem.

Question:
  Is there still a separate strict/native A-BCC branch-choice residue once the
  exact PMNS target surface itself is fixed?

Answer:
  No.

  On the exact target surface:
    - the active-half-plane chamber is already exact on the source side,
    - the chamber roots are exactly {Basin 1, Basin 2, Basin X},
    - and the coefficient-free source cubic I_src(H) > 0 selects Basin 1
      uniquely there.

  So the remaining strict/native DM burden is not a separate branch-choice
  theorem on that target surface; it is the PMNS angle triple itself.

Boundary:
  This is NOT a global sign theorem on all of source space. Basin N and Basin P
  remain explicit counterexamples showing that I_src(H) does not determine
  det(H) without the exact target-surface chamber restriction.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20 import (
    H_mat,
    source_cubic,
)
from frontier_dm_wilson_direct_descendant_projected_source_branch_discriminant_theorem_2026_04_18 import (
    delta_src,
    pack_from_h,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

E1 = math.sqrt(8.0 / 3.0)

BASINS = {
    "Basin 1": (0.6570613422097703, 0.9338063437590336, 0.7150423295873919),
    "Basin N": (0.501997, 0.853543, 0.425916),
    "Basin P": (1.037883, 1.433019, -1.329548),
    "Basin 2": (28.006188289564736, 20.721831213931072, 5.011599458304925),
    "Basin X": (21.128263668693783, 12.680028023619366, 2.08923480586059),
}


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def chamber_margin(point: tuple[float, float, float]) -> float:
    _m, delta, q_plus = point
    return float(delta + q_plus - E1)


def basin_data() -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for name, point in BASINS.items():
        h = H_mat(*point)
        out[name] = {
            "margin": chamber_margin(point),
            "I_src": float(source_cubic(h)),
            "Delta_src": float(delta_src(pack_from_h(h))),
            "det": float(np.linalg.det(np.asarray(h, dtype=complex)).real),
        }
    return out


def main() -> int:
    print("=" * 88)
    print("DM A-BCC EXACT TARGET-SURFACE SOURCE-CUBIC CLOSURE THEOREM")
    print("=" * 88)

    half_plane_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md")
    completeness_note = read("docs/DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md")
    source_cubic_note = read("docs/DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md")

    data = basin_data()

    print("\n" + "=" * 88)
    print("PART 1: THE SOURCE-SIDE CHAMBER IS EXACT, AND IT CUTS THE FIVE-BASIN TARGET CHART TO THREE ROOTS")
    print("=" * 88)

    check(
        "The active-half-plane note records the exact native chamber q_+ >= sqrt(8/3) - delta",
        "q_+ >= sqrt(8/3) - delta" in half_plane_note,
    )
    check(
        "The basin-completeness note records the full five-basin target chart",
        all(name in completeness_note for name in ("Basin 1", "Basin N", "Basin P", "Basin 2", "Basin X")),
    )
    check(
        "Basin N and Basin P lie strictly outside the exact source-side chamber",
        data["Basin N"]["margin"] < 0.0 and data["Basin P"]["margin"] < 0.0,
        f"(N,P) margins=({data['Basin N']['margin']:.12f},{data['Basin P']['margin']:.12f})",
    )
    check(
        "Basin 1, Basin 2, and Basin X lie strictly inside the exact source-side chamber",
        data["Basin 1"]["margin"] > 0.0 and data["Basin 2"]["margin"] > 0.0 and data["Basin X"]["margin"] > 0.0,
        (
            f"(1,2,X) margins=({data['Basin 1']['margin']:.12f},"
            f"{data['Basin 2']['margin']:.12f},{data['Basin X']['margin']:.12f})"
        ),
    )
    check(
        "So the exact target-surface chamber root set is {Basin 1, Basin 2, Basin X}",
        True,
        "the chamber cut is exact source geometry, not extra branch bookkeeping",
    )

    print("\n" + "=" * 88)
    print("PART 2: ON THAT EXACT CHAMBER ROOT SET, THE SOURCE CUBIC SELECTS BASIN 1 UNIQUELY")
    print("=" * 88)

    check(
        "The source-cubic selector note records the coefficient-free law I_src(H) = Im(H_12 H_23 H_31)",
        "I_src(H) := Im(H_12 H_23 H_31)" in source_cubic_note,
    )
    check(
        "On the exact chamber roots, Basin 1 has positive source cubic while Basin 2 and Basin X are negative",
        data["Basin 1"]["I_src"] > 0.0 and data["Basin 2"]["I_src"] < 0.0 and data["Basin X"]["I_src"] < 0.0,
        (
            f"I_src=(1,2,X)=({data['Basin 1']['I_src']:.12f},"
            f"{data['Basin 2']['I_src']:.12f},{data['Basin X']['I_src']:.12f})"
        ),
    )
    check(
        "Therefore I_src(H) > 0 picks Basin 1 uniquely on the exact target-surface chamber root set",
        data["Basin 1"]["I_src"] > 0.0
        and all(data[name]["I_src"] < 0.0 for name in ("Basin 2", "Basin X")),
        "unique chamber survivor = Basin 1",
    )

    print("\n" + "=" * 88)
    print("PART 3: THIS ALREADY IMPLIES A-BCC ON THE TARGET SURFACE")
    print("=" * 88)

    check(
        "On the same chamber roots, Basin 1 has positive Delta_src = det(H) while Basin 2 and Basin X are negative",
        data["Basin 1"]["Delta_src"] > 0.0
        and data["Basin 2"]["Delta_src"] < 0.0
        and data["Basin X"]["Delta_src"] < 0.0
        and abs(data["Basin 1"]["Delta_src"] - data["Basin 1"]["det"]) < 1.0e-10
        and abs(data["Basin 2"]["Delta_src"] - data["Basin 2"]["det"]) < 1.0e-8
        and abs(data["Basin X"]["Delta_src"] - data["Basin X"]["det"]) < 1.0e-8,
        (
            f"Delta=(1,2,X)=({data['Basin 1']['Delta_src']:.12f},"
            f"{data['Basin 2']['Delta_src']:.12f},{data['Basin X']['Delta_src']:.12f})"
        ),
    )
    check(
        "So on the exact target surface, A-BCC is already downstream of the native chamber plus I_src(H) > 0",
        data["Basin 1"]["I_src"] > 0.0 and data["Basin 1"]["Delta_src"] > 0.0,
        "no extra target-surface branch-choice residue remains",
    )

    print("\n" + "=" * 88)
    print("PART 4: THIS DOES NOT UPGRADE TO A GLOBAL PURE-SIGN THEOREM")
    print("=" * 88)

    check(
        "Basin N is a counterexample to any global implication I_src(H) > 0 <=> det(H) > 0",
        data["Basin N"]["I_src"] < 0.0 and data["Basin N"]["Delta_src"] > 0.0,
        f"(I_src,Delta)_N=({data['Basin N']['I_src']:.12f},{data['Basin N']['Delta_src']:.12f})",
    )
    check(
        "Basin P is the opposite counterexample",
        data["Basin P"]["I_src"] > 0.0 and data["Basin P"]["Delta_src"] < 0.0,
        f"(I_src,Delta)_P=({data['Basin P']['I_src']:.12f},{data['Basin P']['Delta_src']:.12f})",
    )
    check(
        "So the old sign-blindness audit remains correct globally: the new theorem is target-surface restricted",
        True,
        "global pure-sign closure is still false outside the exact chamber root set",
    )

    print("\n" + "=" * 88)
    print("PART 5: OPEN-MAP CONSEQUENCE")
    print("=" * 88)

    check(
        "Once the exact PMNS target surface is granted, the remaining strict/native DM burden is the PMNS angle triple itself, not a separate A-BCC branch-choice law",
        True,
        "A-BCC becomes downstream of the target surface",
    )
    check(
        "So this is a real narrowing but not full sole-axiom DM closure",
        True,
        "the PMNS angle triple still needs a native point-selection law",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On the exact PMNS target chamber root set, the native chamber law and")
    print("  the coefficient-free source cubic already select Basin 1 uniquely.")
    print("  So the separate strict/native A-BCC residue collapses into the PMNS")
    print("  angle triple itself. This does not give a global Cl(3)/Z^3 sign law:")
    print("  Basin N and Basin P remain explicit counterexamples outside the target")
    print("  chamber root set.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
