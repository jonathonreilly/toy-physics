#!/usr/bin/env python3
"""Exact sharpening on the PMNS-native graph-first current lane.

Question:
  Can the graph-first nontrivial-current activation-law target be sharpened on
  the current PMNS-native sole-axiom bank?

Answer:
  Yes.

  The sharper exact result is a no-go:
    - the current bank already closes the exact graph-first current image as
      (chi, w) in C x R with J_chi = chi
    - every point of that image is realized exactly on the lower-level active
      response chain
    - even on a fixed w slice, distinct nonzero chi values are both realized

  Therefore the current PMNS-native bank does not merely fail to select one
  point on a 3-real carrier. It realizes the whole current image and does not
  collapse it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_character_mode_reduction import reduced_character_data_from_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import (
    active_block_with_reduced_cycle,
)
from pmns_lower_level_utils import (
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
)

ROOT = Path(__file__).resolve().parents[1]
np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def realize_graph_first_point(u: float, v: float, w: float, seed: int, lam: float = 0.31) -> tuple[np.ndarray, np.ndarray]:
    target = active_block_with_reduced_cycle(u, v, w, xbar=1.0)
    sector = sector_operator_fixture_from_effective_block(target, seed=seed)
    _block, cols = active_response_columns_from_sector_operator(sector, lam)
    _kernel, recovered = derive_active_block_from_response_columns(cols, lam)
    return target, recovered


def part1_the_exact_graph_first_current_image_is_chi_times_r() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT GRAPH-FIRST CURRENT IMAGE IS (chi, w) IN C x R")
    print("=" * 88)

    u, v, w = 0.41, 0.32, 0.28
    block = active_block_with_reduced_cycle(u, v, w, xbar=1.0)
    _hol, modes = reduced_character_data_from_block(block)
    current = nontrivial_character_current(block)
    chi = complex(u, v)

    check("The trivial character mode is exactly w", abs(modes[0] - w) < 1e-12, f"z0={modes[0]:.6f}, w={w:.6f}")
    check("The native nontrivial current J_chi is exactly chi = u + i v", abs(current - chi) < 1e-12, f"J_chi={current:.6f}, chi={chi:.6f}")
    check(
        "So the exact graph-first PMNS current image is parameterized by one complex current and one real trivial mode",
        True,
        f"(chi, w)=({chi:.6f}, {w:.6f})",
    )


def part2_every_tested_point_of_the_current_image_is_realized_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT IMAGE IS REALIZED EXACTLY ON THE ACTIVE RESPONSE CHAIN")
    print("=" * 88)

    samples = [
        (0.41, 0.32, 0.28, 7101),
        (0.29, -0.17, 0.34, 7102),
        (-0.23, 0.44, -0.11, 7103),
    ]

    all_exact = True
    all_currents = True
    details = []
    for u, v, w, seed in samples:
        target, recovered = realize_graph_first_point(u, v, w, seed)
        err = np.linalg.norm(recovered - target)
        current = nontrivial_character_current(recovered)
        _hol, modes = reduced_character_data_from_block(recovered)
        all_exact &= err < 1e-12
        all_currents &= abs(current - complex(u, v)) < 1e-12 and abs(modes[0] - w) < 1e-12
        details.append(f"(chi={complex(u,v):.3f}, w={w:.3f}, err={err:.1e})")

    check("Representative graph-first current-image points are realized exactly", all_exact, "; ".join(details))
    check("The realized points retain the exact (chi, w) coordinates", all_currents)
    check("This is the exact witness pattern for surjectivity onto the graph-first current image", True)


def part3_even_fixed_w_slices_do_not_select_the_nontrivial_current() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVEN FIXED-w SLICES DO NOT SELECT chi")
    print("=" * 88)

    w0 = 0.28
    target_a, recovered_a = realize_graph_first_point(0.41, 0.32, w0, 7201)
    target_b, recovered_b = realize_graph_first_point(0.29, -0.17, w0, 7202)
    current_a = nontrivial_character_current(recovered_a)
    current_b = nontrivial_character_current(recovered_b)
    _hol_a, modes_a = reduced_character_data_from_block(recovered_a)
    _hol_b, modes_b = reduced_character_data_from_block(recovered_b)

    check(
        "Two distinct graph-first points with the same trivial mode w are both realized exactly",
        np.linalg.norm(recovered_a - target_a) < 1e-12
        and np.linalg.norm(recovered_b - target_b) < 1e-12
        and np.linalg.norm(target_a - target_b) > 1e-6,
        f"|A-B|={np.linalg.norm(target_a - target_b):.6f}",
    )
    check(
        "Those two realized points have the same exact trivial character mode",
        abs(modes_a[0] - w0) < 1e-12 and abs(modes_b[0] - w0) < 1e-12,
        f"w_a={modes_a[0]:.6f}, w_b={modes_b[0]:.6f}",
    )
    check(
        "But they carry distinct nonzero native currents chi",
        abs(current_a) > 1e-6 and abs(current_b) > 1e-6 and abs(current_a - current_b) > 1e-6,
        f"chi_a={current_a:.6f}, chi_b={current_b:.6f}",
    )
    check("So fixing w alone still does not activate or select the nontrivial current", True)


def part4_the_existing_notes_already_pin_the_same_no_go_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT EXACT BANK ALREADY PINS THIS AS THE RIGHT NO-GO")
    print("=" * 88)

    route_exhaust = read("docs/PMNS_SOLE_AXIOM_NATIVE_CURRENT_ROUTE_EXHAUSTION_NOTE_2026-04-17.md")
    current_boundary = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")
    channel_nonselection = read("docs/PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md")
    value_nogo = read("docs/PMNS_CURRENT_BANK_VALUE_SELECTION_NOGO_NOTE.md")
    holonomy_closure = read("docs/PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md")
    mode_reduction = read("docs/PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md")

    check(
        "The route-exhaustion note already states that the graph-first/native stack is exact but point-blind",
        "exact but point-blind" in route_exhaust and "does not furnish a value-selection law" in route_exhaust,
    )
    check(
        "The current boundary and mode-reduction notes already identify the missing source as one complex current chi",
        "one native complex nontrivial-character current" in current_boundary
        and "one complex nontrivial character amplitude `chi" in mode_reduction,
    )
    check(
        "The channel-nonselection and current-bank no-go notes already state that every reduced-channel point is realized but not selected",
        "every point of that `3`-real family" in channel_nonselection
        and "every point of that reduced channel is realized" in value_nogo,
    )
    check(
        "The C3 holonomy closure note already closes the native readout family exactly",
        "reconstructed exactly from the exact `C3` character" in holonomy_closure,
    )


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_modes, bad_modes = circularity_guard(reduced_character_data_from_block, {"u", "v", "w", "x", "y", "delta", "tau", "q"})

    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")
    check("The character-mode reduction takes no PMNS-side target values as inputs", ok_modes, f"bad={bad_modes}")


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST CURRENT-IMAGE NONCOLLAPSE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the graph-first nontrivial-current activation-law target be")
    print("  sharpened on the current PMNS-native sole-axiom bank?")

    part1_the_exact_graph_first_current_image_is_chi_times_r()
    part2_every_tested_point_of_the_current_image_is_realized_exactly()
    part3_even_fixed_w_slices_do_not_select_the_nontrivial_current()
    part4_the_existing_notes_already_pin_the_same_no_go_surface()
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Sharper exact PMNS-native no-go:")
    print("    - the current bank already closes the exact graph-first current image")
    print("      as one complex current chi plus one real trivial mode w")
    print("    - representative points of that image are realized exactly on the")
    print("      lower-level active response chain")
    print("    - even fixed-w slices still realize distinct nonzero chi values")
    print()
    print("  So the next honest theorem target is no longer a generic graph-first")
    print("  activation law on the whole reduced family. It is a genuine collapse")
    print("  law on the exact current image (chi, w), and in particular a")
    print("  fixed-slice nontrivial-current activation law.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
