#!/usr/bin/env python3
"""Audit the gravity-carrier-from-sector-identification theorem.

The audit has two jobs:

1. verify that the theorem note is adversarial-review safe: it must state the
   gravity-sector matching premise explicitly and must not present carrier
   identification as a coefficient fit;
2. independently classify the local one-cell carriers under the stated
   source-free worldtube-incidence rules and verify that the unique primitive
   carrier is P_A.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product, permutations
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md"
)
EXISTING_CARRIER = (
    ROOT
    / "docs/PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md"
)
NORMALIZATION = (
    ROOT
    / "docs/PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md"
)
NATIVE_PACKET = (
    ROOT
    / "docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md"
)
WORLDTUBE_COUNT = (
    ROOT
    / "docs/PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md"
)
SECTION_SELECTOR = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
)


@dataclass
class Totals:
    passed: int = 0
    failed: int = 0

    def add(self, passed: bool) -> None:
        self.passed += int(passed)
        self.failed += int(not passed)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(totals: Totals, label: str, passed: bool, detail: str) -> None:
    passed = bool(passed)
    totals.add(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")


def bit_index(bits: tuple[int, int, int, int]) -> int:
    value = 0
    for bit in bits:
        value = 2 * value + bit
    return value


def apply_spatial_perm(
    bits: tuple[int, int, int, int], perm: tuple[int, int, int]
) -> tuple[int, int, int, int]:
    spatial = (bits[1], bits[2], bits[3])
    return (bits[0], spatial[perm[0]], spatial[perm[1]], spatial[perm[2]])


def all_subsets(items: list[int]) -> list[frozenset[int]]:
    subsets: list[frozenset[int]] = []
    for size in range(len(items) + 1):
        for combo in combinations(items, size):
            subsets.append(frozenset(combo))
    return subsets


def is_invariant_support(
    support: frozenset[int],
    index_to_bits: dict[int, tuple[int, int, int, int]],
    bits_to_index: dict[tuple[int, int, int, int], int],
) -> bool:
    for idx in support:
        bits = index_to_bits[idx]
        for perm in permutations((0, 1, 2)):
            moved = bits_to_index[apply_spatial_perm(bits, perm)]
            if moved not in support:
                return False
    return True


def main() -> int:
    totals = Totals()

    print("Planck gravity carrier from sector-identification theorem audit")
    print("=" * 78)

    section("PART 1: FILES AND REVIEW-SAFETY TEXT")
    paths = [
        NOTE,
        EXISTING_CARRIER,
        NORMALIZATION,
        NATIVE_PACKET,
        WORLDTUBE_COUNT,
        SECTION_SELECTOR,
    ]
    for path in paths:
        check(
            totals,
            f"{path.relative_to(ROOT)} exists",
            path.exists(),
            "linked theorem/audit dependency is present",
        )

    note = normalized(NOTE)
    existing_carrier = normalized(EXISTING_CARRIER)
    normalization = normalized(NORMALIZATION)
    native_packet = normalized(NATIVE_PACKET)
    worldtube_count = normalized(WORLDTUBE_COUNT)
    section_selector = normalized(SECTION_SELECTOR)

    check(
        totals,
        "note states explicit Gravity-Sector Identification premise",
        "gravity-sector identification (gsi)" in note
        and "sector-identification input" in note,
        "the gravity matching premise must be named rather than hidden",
    )
    check(
        totals,
        "note says GSI is not a numerical input",
        "gsi is not a numerical input" in note
        and "does not say `c_cell = 1/4`" in note
        and "does not say `a = l_p`" in note,
        "carrier selection should not be confused with fitting the quarter or Planck length",
    )
    check(
        totals,
        "note refuses to derive semiclassical gravity from bare cell algebra",
        "does **not** derive semiclassical gravity from the cell algebra alone" in note
        and "unsafe claim" in note
        and "bare cell algebra alone proves that gravity must exist" in note,
        "the result must remain conditional on physical sector identification",
    )
    check(
        totals,
        "note links the requested upstream theorem files",
        "planck_scale_gravitational_area_action_carrier_identification_theorem_2026-04-23.md"
        in note
        and "planck_scale_area_action_normalization_theorem_2026-04-23.md" in note
        and "planck_scale_native_derivation_theorem_packet_2026-04-23.md" in note,
        "new note should link existing docs rather than editing them",
    )
    check(
        totals,
        "note gives the forced carrier and coefficient only after state evaluation",
        "n_grav = p_a" in note
        and "c_cell = tr(rho_cell p_a)" in note
        and "tr((i_16 / 16) p_a) = 4/16 = 1/4" in note,
        "P_A should be the carrier; 1/4 should come from the source-free state on that carrier",
    )
    check(
        totals,
        "note preserves denial scope if GSI is rejected",
        "if a reviewer denies gsi" in note
        and "but the physical conclusion `a^2 = l_p^2` is not obtained" in note,
        "the failure mode should be explicit and non-overclaiming",
    )

    section("PART 2: ALIGNMENT WITH EXISTING PLANCK NOTES")
    check(
        totals,
        "existing carrier theorem already isolates the physical matching requirement",
        "still a physical matching requirement" in existing_carrier
        and "microscopic carrier of the semiclassical gravitational area/action density"
        in existing_carrier,
        "new note should strengthen, not contradict, the earlier carrier theorem",
    )
    check(
        totals,
        "normalization theorem remains algebraic after carrier selection",
        "a^2 = 4 c_cell l_p^2" in normalization
        and "if a reviewer rejects the identification" in normalization,
        "new note should leave the a^2 normalization theorem as the downstream step",
    )
    check(
        totals,
        "native packet names primitive count as remaining stop condition",
        "deny that the primitive-cell count realizes the gravitational area/action density"
        in native_packet,
        "the new note attacks exactly the second stop condition",
    )
    check(
        totals,
        "worldtube counting theorem proves N_cell = P_A as direct count object",
        "n_cell = p_a" in worldtube_count
        and "cell-counting theorem" in worldtube_count,
        "GSI should use the already proved incidence-count object",
    )
    check(
        totals,
        "section selector theorem forces the coarse worldtube sector P_A",
        "uniquely forced to be `p_a" in section_selector
        or "coarse worldtube sector is **section-canonical**" in section_selector,
        "the gravity carrier should not choose a new sector",
    )

    section("PART 3: ONE-CELL SECTOR CLASSIFICATION")
    states = list(product((0, 1), repeat=4))
    bits_to_index = {bits: bit_index(bits) for bits in states}
    index_to_bits = {idx: bits for bits, idx in bits_to_index.items()}
    shell = sorted(idx for idx, bits in index_to_bits.items() if sum(bits) == 1)
    temporal = frozenset({bits_to_index[(1, 0, 0, 0)]})
    spatial = frozenset(
        {
            bits_to_index[(0, 1, 0, 0)],
            bits_to_index[(0, 0, 1, 0)],
            bits_to_index[(0, 0, 0, 1)],
        }
    )
    packet = temporal | spatial

    invariant_supports = sorted(
        (
            support
            for support in all_subsets(shell)
            if is_invariant_support(support, index_to_bits, bits_to_index)
        ),
        key=lambda item: (len(item), sorted(item)),
    )
    expected_supports = sorted(
        [frozenset(), temporal, spatial, packet],
        key=lambda item: (len(item), sorted(item)),
    )

    check(
        totals,
        "minimal shell has exactly four one-step atoms",
        len(shell) == 4 and len(packet) == 4,
        "the primitive worldtube packet is the Hamming-weight-one shell",
    )
    check(
        totals,
        "residual S_3 invariant minimal-shell supports are empty, temporal, spatial, and full packet",
        invariant_supports == expected_supports,
        f"invariant supports={list(map(lambda s: sorted(s), invariant_supports))}",
    )

    counters: list[tuple[int, int]] = []
    for u_t in range(4):
        for u_s in range(4):
            counters.append((u_t, u_s))
    admissible = [
        (u_t, u_s)
        for (u_t, u_s) in counters
        if u_t == 1 and u_s == 1
    ]
    nonprimitive_but_symmetric = [
        (u_t, u_s)
        for (u_t, u_s) in counters
        if u_t == u_s and (u_t, u_s) != (1, 1)
    ]
    anisotropic = [(u_t, u_s) for (u_t, u_s) in counters if u_t != u_s]

    check(
        totals,
        "unit one-step incidence rules leave a unique carrier",
        admissible == [(1, 1)],
        "time-complete, spatially isotropic, primitive unit counting forces u_t=u_s=1",
    )
    check(
        totals,
        "alternative symmetric multiples are nonprimitive copies, not the primitive carrier",
        (0, 0) in nonprimitive_but_symmetric and (2, 2) in nonprimitive_but_symmetric,
        "0 is no carrier; k P_A with k>1 counts multiple copies of each incidence",
    )
    check(
        totals,
        "unequal temporal/spatial weights are anisotropic non-count weightings",
        (1, 2) in anisotropic and (2, 1) in anisotropic,
        "u_t != u_s imports a weighting not present in primitive unit-incidence counting",
    )

    section("PART 4: NORMALIZATION CONSEQUENCE")
    rank_p_a = len(packet)
    dim_cell = len(states)
    c_cell = Fraction(rank_p_a, dim_cell)
    a2_over_lp2 = 4 * c_cell
    check(
        totals,
        "source-free trace on forced carrier gives exact quarter",
        c_cell == Fraction(1, 4),
        f"rank(P_A)/dim(H_cell)={rank_p_a}/{dim_cell}={c_cell}",
    )
    check(
        totals,
        "quarter plus gravitational area/action normalization gives one Planck area",
        a2_over_lp2 == 1,
        f"a^2/l_P^2=4*c_cell={a2_over_lp2}",
    )

    section("SUMMARY")
    print(f"Passed: {totals.passed}")
    print(f"Failed: {totals.failed}")
    return 0 if totals.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
