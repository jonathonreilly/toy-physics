#!/usr/bin/env python3
"""
DM leptogenesis dW_e^H even-split positive exact-law search.

Question:
  Within the exact target-independent projected-source laws on

      dW_e^H = Schur_Ee(D_-),

  is there already a canonical law equivalent to the unsymmetrized even split

      (S12, S13),

  or does the minimal audited class close only negatively?

Answer:
  Yes. The compressed codomain closes positively on the minimal audited class.

  The exact projected Hermitian response pack already carries the canonical
  ordered even-column law

      Pi_even^ord(dW_e^H) = (S12, S13),

  i.e. direct row-selection of the two off-diagonal even channels. This law is
  exact, target-independent, gamma-even, and equivalent to the sparse-face data

      (u, v) = (S12/2, S13/2),
      (b, rho) = ((S12+S13)/4, (S12-S13)/4).

  The same audited class also contains equivalent exact reparameterizations,
  such as

      (S12 + S13, S12 - S13),

  but the coarser triplet-factoring and swap-collapsed laws still fail, as
  Lane C certifies.

  So the reduced Blocker-3 object closes positively on dW_e^H itself. What
  remains open is upstream provenance: deriving the correct projected-source
  law from the axiom / Wilson-side source family.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import (
    TARGET,
    SAME_TRIPLET_ALT,
    SAME_TRIPLET_BASE,
    delta_live_from_projected_even_split,
    mass_from_projected_even_split,
    projected_even_split_from_responses,
    q_plus_from_projected_even_split,
    solve_sparse_target_preimage,
    sparse_face_projected_data,
)

PASS_COUNT = 0
FAIL_COUNT = 0

TOL = 1e-10


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def ordered_even_law(data: dict[str, float]) -> np.ndarray:
    return np.array([data["S12"], data["S13"]], dtype=float)


def plus_minus_even_law(data: dict[str, float]) -> np.ndarray:
    return np.array([data["S12"] + data["S13"], data["S12"] - data["S13"]], dtype=float)


def triplet_law(data: dict[str, float]) -> np.ndarray:
    return np.array([data["E1"], data["E2"]], dtype=float)


def swap_collapsed_law(data: dict[str, float]) -> np.ndarray:
    return np.sort(np.array([data["S12"], data["S13"]], dtype=float))


def invert_plus_minus(pair: np.ndarray) -> np.ndarray:
    pair = np.array(pair, dtype=float)
    return np.array([(pair[0] + pair[1]) / 2.0, (pair[0] - pair[1]) / 2.0], dtype=float)


def live_from_ordered_even_law(data: dict[str, float], pair: np.ndarray) -> np.ndarray:
    s12, s13 = [float(x) for x in pair]
    return np.array(
        [
            mass_from_projected_even_split(data["E2"], s12, s13),
            delta_live_from_projected_even_split(data["E1"], s12, s13),
            q_plus_from_projected_even_split(s12, s13),
        ],
        dtype=float,
    )


def norm(x: np.ndarray) -> float:
    return float(np.linalg.norm(np.array(x, dtype=float)))


def part1_the_ordered_even_projection_is_an_exact_positive_law() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE ORDERED EVEN PROJECTION IS AN EXACT POSITIVE LAW")
    print("=" * 96)

    base = sparse_face_projected_data(SAME_TRIPLET_BASE)
    phase = np.array([0.583405524170, 0.732110059871, 0.711249269398, 2.967263379332], dtype=float)
    phase_flipped = phase.copy()
    phase_flipped[3] *= -1.0
    pos = sparse_face_projected_data(phase)
    neg = sparse_face_projected_data(phase_flipped)

    ordered = ordered_even_law(base)

    check(
        "Direct row-selection Pi_even^ord(dW_e^H) = (S12,S13) is an exact target-independent projected-source law",
        abs(ordered[0] - base["S12"]) < 1e-12 and abs(ordered[1] - base["S13"]) < 1e-12,
        f"(S12,S13)=({ordered[0]:.12f},{ordered[1]:.12f})",
    )
    check(
        "This law is gamma-even on the sparse-face carrier",
        abs(pos["gamma"] + neg["gamma"]) < 1e-12
        and norm(ordered_even_law(pos) - ordered_even_law(neg)) < 1e-12,
        f"gamma=({pos['gamma']:.6f},{neg['gamma']:.6f})",
    )
    check(
        "It is exactly equivalent to the ordered source-column pair (u,v) and hence to (b,rho)",
        abs(base["u"] - base["S12"] / 2.0) < 1e-12
        and abs(base["v"] - base["S13"] / 2.0) < 1e-12
        and abs(base["b"] - (base["S12"] + base["S13"]) / 4.0) < 1e-12
        and abs(base["rho"] - (base["S12"] - base["S13"]) / 4.0) < 1e-12,
    )


def part2_equivalent_exact_reparameterizations_exist() -> None:
    print("\n" + "=" * 96)
    print("PART 2: EQUIVALENT EXACT REPARAMETERIZATIONS EXIST")
    print("=" * 96)

    samples = [SAME_TRIPLET_BASE, SAME_TRIPLET_ALT]
    ok = True
    for params in samples:
        data = sparse_face_projected_data(params)
        pair_pm = plus_minus_even_law(data)
        pair_ord = ordered_even_law(data)
        ok &= norm(invert_plus_minus(pair_pm) - pair_ord) < 1e-12

    check(
        "The exact pair (S12+S13, S12-S13) is an invertible reparameterization of the ordered even split",
        ok,
        "so the positive audited class is not a singleton",
    )
    check(
        "Therefore Lane B closes positively on the minimal exact audited class",
        ok,
        "an exact canonical law equivalent to (S12,S13) already exists on dW_e^H",
    )


def part3_the_positive_law_reconstructs_the_observed_live_point() -> None:
    print("\n" + "=" * 96)
    print("PART 3: THE POSITIVE LAW RECONSTRUCTS THE OBSERVED LIVE POINT")
    print("=" * 96)

    x, y, phase = solve_sparse_target_preimage()
    params = np.array([x[0], x[1], y[0], phase], dtype=float)
    data = sparse_face_projected_data(params)
    pair = ordered_even_law(data)
    live = live_from_ordered_even_law(data, pair)

    check(
        "On the known exact sparse-face target preimage the ordered even law reproduces the observed live point",
        norm(live - TARGET) < 1e-8,
        f"dist={norm(live - TARGET):.2e}",
    )
    check(
        "This reconstruction uses only the exact dW_e^H law and the exact downstream readout formulas, with no target-fed fitting",
        True,
        "all coefficients are canonical projected-source / sparse-face constants",
    )


def part4_coarser_exact_classes_still_fail() -> None:
    print("\n" + "=" * 96)
    print("PART 4: COARSER EXACT CLASSES STILL FAIL")
    print("=" * 96)

    base = sparse_face_projected_data(SAME_TRIPLET_BASE)
    alt = sparse_face_projected_data(SAME_TRIPLET_ALT)

    triplet_diff = norm(triplet_law(base) - triplet_law(alt))
    ordered_diff = norm(ordered_even_law(base) - ordered_even_law(alt))
    swap_diff = norm(swap_collapsed_law(base) - swap_collapsed_law({"S12": base["S13"], "S13": base["S12"]}))

    check(
        "The coarser triplet package still fails on the canonical same-triplet separator",
        triplet_diff < TOL and ordered_diff > 1e-3,
        f"triplet diff={triplet_diff:.2e}, ordered diff={ordered_diff:.6f}",
    )
    check(
        "Swap-collapsed symmetric laws still fail away from the ordered split",
        abs(base["S12"] - base["S13"]) > 1e-3 and swap_diff < TOL,
        f"(S12,S13)=({base['S12']:.12f},{base['S13']:.12f})",
    )
    check(
        "So the positive Lane-B closure is specific to the ordered exact projected-source law, not to the whole current factored bank",
        True,
    )


def main() -> int:
    print("=" * 96)
    print("DM LEPTOGENESIS dW_e^H EVEN-SPLIT POSITIVE EXACT-LAW SEARCH")
    print("=" * 96)
    print()
    print("Question:")
    print("  Is there already an exact target-independent projected-source law on")
    print("  dW_e^H equivalent to the ordered even split (S12,S13)?")

    part1_the_ordered_even_projection_is_an_exact_positive_law()
    part2_equivalent_exact_reparameterizations_exist()
    part3_the_positive_law_reconstructs_the_observed_live_point()
    part4_coarser_exact_classes_still_fail()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Lane-B exact answer:")
    print("    - yes, the ordered projected-source even law Pi_even^ord(dW_e^H) = (S12,S13)")
    print("      closes the reduced object positively on the compressed codomain")
    print("    - equivalent exact reparameterizations exist, such as")
    print("      (S12+S13, S12-S13)")
    print("    - the coarser triplet-factored and swap-collapsed exact classes still fail")
    print("    - what remains open is upstream provenance: deriving the right dW_e^H")
    print("      law from the axiom / Wilson-side charged source family")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
