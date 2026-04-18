#!/usr/bin/env python3
"""Sharper fixed-slice no-go on the PMNS-native graph-first current lane.

Question:
  Starting from the exact graph-first current image (chi, w), can the current
  PMNS-native exact bank already collapse a fixed slice w = w0 by reusing its
  current graph-first selector/holonomy data?

Answer:
  No.

  The stronger exact no-go is:
    - the exact PMNS-native current image is already (chi, w) in C x R
    - the graph-first projected-commutant selector bundle (tau, q) is constant
      on the reduced family
    - even after fixing one exact native twisted-flux holonomy on a fixed-w
      slice, distinct nonzero chi values are both realized exactly

  So the current bank still does not collapse chi after the currently admitted
  selector/holonomy data are held fixed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_character_mode_reduction import reduced_character_data_from_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_graph_commutant_cycle_value_boundary import (
    projected_commutant_bundle,
    route_signature_for_block,
)
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import (
    active_block_with_reduced_cycle,
    residual_swap_conjugate,
)
from frontier_pmns_twisted_flux_transfer_holonomy_boundary import (
    flux_holonomy_on_reduced_family,
    reduced_cycle_family,
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


def exact_witness_pair(phi: float = 0.41, w0: float = 0.28) -> tuple[np.ndarray, np.ndarray, float]:
    """Two reduced graph-first points with the same fixed-slice holonomy."""
    u0, v0 = 0.41, 0.32
    hu = flux_holonomy_on_reduced_family(reduced_cycle_family(1.0, 0.0, 0.0), phi)
    hv = flux_holonomy_on_reduced_family(reduced_cycle_family(0.0, 1.0, 0.0), phi)
    step = 0.2
    u1 = u0 + step * hv
    v1 = v0 - step * hu
    a = active_block_with_reduced_cycle(u0, v0, w0, xbar=1.0)
    b = active_block_with_reduced_cycle(u1, v1, w0, xbar=1.0)
    return a, b, phi


def realize(block: np.ndarray, seed: int, lam: float = 0.31) -> np.ndarray:
    sector = sector_operator_fixture_from_effective_block(block, seed=seed)
    _ref, cols = active_response_columns_from_sector_operator(sector, lam)
    _kernel, recovered = derive_active_block_from_response_columns(cols, lam)
    return recovered


def part1_the_exact_current_image_is_already_chi_times_r() -> tuple[np.ndarray, np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT CURRENT IMAGE IS ALREADY (chi, w) IN C x R")
    print("=" * 88)

    a, b, phi = exact_witness_pair()
    current_a = nontrivial_character_current(a)
    current_b = nontrivial_character_current(b)
    _hol_a, modes_a = reduced_character_data_from_block(a)
    _hol_b, modes_b = reduced_character_data_from_block(b)

    check("The witness pair lies on the same exact trivial-character slice", abs(modes_a[0] - modes_b[0]) < 1e-12, f"w={modes_a[0]:.6f}")
    check("The exact native current is the nontrivial character amplitude on each witness", abs(current_a - modes_a[2]) < 1e-12 and abs(current_b - modes_b[2]) < 1e-12)
    check(
        "The witness pair carries distinct nonzero currents chi on the same exact w slice",
        abs(current_a) > 1e-6 and abs(current_b) > 1e-6 and abs(current_a - current_b) > 1e-6,
        f"chi_a={current_a:.6f}, chi_b={current_b:.6f}",
    )
    return a, b, phi


def part2_the_selector_bundle_is_constant_on_the_fixed_slice(a: np.ndarray, b: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SELECTOR BUNDLE DOES NOT COLLAPSE THE FIXED SLICE")
    print("=" * 88)

    comm = projected_commutant_bundle()
    sig_a = route_signature_for_block(a, comm)
    sig_b = route_signature_for_block(b, comm)

    check("Both fixed-slice witnesses satisfy the residual graph-first antiunitary symmetry", np.linalg.norm(residual_swap_conjugate(a) - a) < 1e-12 and np.linalg.norm(residual_swap_conjugate(b) - b) < 1e-12)
    check(
        "The projected-commutant selector bundle (tau, q) is the same on both fixed-slice witnesses",
        sig_a["tau"] == sig_b["tau"] and sig_a["q"] == sig_b["q"],
        f"(tau,q)_a=({sig_a['tau']},{sig_a['q']}), (tau,q)_b=({sig_b['tau']},{sig_b['q']})",
    )
    check(
        "So the current graph-first selector bundle adds no collapse on this fixed-w slice",
        sig_a["tau"] == sig_b["tau"] and sig_a["q"] == sig_b["q"] and np.linalg.norm(a - b) > 1e-6,
    )


def part3_one_exact_native_flux_holonomy_still_does_not_collapse_the_fixed_slice(a: np.ndarray, b: np.ndarray, phi: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONE EXACT NATIVE FLUX HOLOMONY STILL DOES NOT COLLAPSE THE FIXED SLICE")
    print("=" * 88)

    m_a = a - np.eye(3, dtype=complex)
    m_b = b - np.eye(3, dtype=complex)
    hol_a = flux_holonomy_on_reduced_family(m_a, phi)
    hol_b = flux_holonomy_on_reduced_family(m_b, phi)

    hu = flux_holonomy_on_reduced_family(reduced_cycle_family(1.0, 0.0, 0.0), phi)
    hv = flux_holonomy_on_reduced_family(reduced_cycle_family(0.0, 1.0, 0.0), phi)
    witness_kernel = reduced_cycle_family(hv, -hu, 0.0)

    check("The chosen one-angle native flux holonomy has a nontrivial tangent kernel on the fixed-w slice", np.linalg.norm(witness_kernel) > 1e-12 and abs(flux_holonomy_on_reduced_family(witness_kernel, phi)) < 1e-12, f"|k|={np.linalg.norm(witness_kernel):.6f}")
    check(
        "The two fixed-slice witnesses have the same exact one-angle native flux holonomy",
        abs(hol_a - hol_b) < 1e-12,
        f"h_a={hol_a:.12f}, h_b={hol_b:.12f}",
    )
    check(
        "So even fixed w plus one exact native twisted-flux holonomy still does not select chi",
        abs(hol_a - hol_b) < 1e-12 and np.linalg.norm(a - b) > 1e-6,
    )


def part4_both_witnesses_are_realized_exactly_on_the_active_response_chain(a: np.ndarray, b: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTH FIXED-SLICE WITNESSES ARE REALIZED EXACTLY")
    print("=" * 88)

    rec_a = realize(a, 7301)
    rec_b = realize(b, 7302)
    current_a = nontrivial_character_current(rec_a)
    current_b = nontrivial_character_current(rec_b)
    _hol_a, modes_a = reduced_character_data_from_block(rec_a)
    _hol_b, modes_b = reduced_character_data_from_block(rec_b)

    check("Witness A is realized exactly on the active response chain", np.linalg.norm(rec_a - a) < 1e-12, f"err={np.linalg.norm(rec_a - a):.2e}")
    check("Witness B is realized exactly on the active response chain", np.linalg.norm(rec_b - b) < 1e-12, f"err={np.linalg.norm(rec_b - b):.2e}")
    check(
        "The realized witnesses retain the same exact fixed slice and distinct nonzero currents",
        abs(modes_a[0] - modes_b[0]) < 1e-12 and abs(current_a - current_b) > 1e-6 and abs(current_a) > 1e-6 and abs(current_b) > 1e-6,
        f"w={modes_a[0]:.6f}, chi_a={current_a:.6f}, chi_b={current_b:.6f}",
    )


def part5_the_current_exact_notes_already_point_to_this_sharper_no_go() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE CURRENT EXACT NOTES ALREADY POINT TO THIS SHARPER NO-GO")
    print("=" * 88)

    current_image = read("docs/PMNS_GRAPH_FIRST_CURRENT_IMAGE_NONCOLLAPSE_NOTE_2026-04-17.md")
    native_exhaust = read("docs/PMNS_SOLE_AXIOM_NATIVE_CURRENT_ROUTE_EXHAUSTION_NOTE_2026-04-17.md")
    commutant = read("docs/PMNS_GRAPH_COMMUTANT_CYCLE_VALUE_BOUNDARY_NOTE.md")
    flux = read("docs/PMNS_TWISTED_FLUX_TRANSFER_HOLONOMY_BOUNDARY_NOTE.md")

    check(
        "The current-image noncollapse note already records that fixed-w slices still realize distinct nonzero chi",
        "Even fixed `w` slices do not select `chi`" in current_image
        and "distinct nonzero currents `chi != chi'`" in current_image,
    )
    check(
        "The route-exhaustion note already identifies the next target as a fixed-slice current-image collapse law",
        "graph-first current-image collapse law" in native_exhaust and "fixed-slice nontrivial-current" in native_exhaust,
    )
    check(
        "The graph-commutant boundary note already says the selector bundle is constant on the reduced family",
        "constant on the reduced" in commutant and "selector bundle `(tau, q)`" in commutant,
    )
    check(
        "The twisted-flux boundary note already says one exact native holonomy probe still has a kernel on the reduced carrier",
        "one flux holonomy alone" in flux and "2-real kernel" in flux,
    )


def part6_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CIRCULARITY GUARD")
    print("=" * 88)

    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_hol, bad_hol = circularity_guard(flux_holonomy_on_reduced_family, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")
    check("The one-angle native holonomy probe takes no PMNS-side target values as inputs", ok_hol, f"bad={bad_hol}")


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST FIXED-SLICE SELECTOR/HOLOMONY NONCOLLAPSE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current PMNS-native exact bank already collapse a fixed")
    print("  current-image slice w = w0 by reusing its admitted graph-first")
    print("  selector/holonomy data?")

    a, b, phi = part1_the_exact_current_image_is_already_chi_times_r()
    part2_the_selector_bundle_is_constant_on_the_fixed_slice(a, b)
    part3_one_exact_native_flux_holonomy_still_does_not_collapse_the_fixed_slice(a, b, phi)
    part4_both_witnesses_are_realized_exactly_on_the_active_response_chain(a, b)
    part5_the_current_exact_notes_already_point_to_this_sharper_no_go()
    part6_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Sharper exact PMNS-native fixed-slice no-go:")
    print("    - the exact current image is already (chi, w)")
    print("    - the graph-first selector bundle (tau, q) is constant on the reduced family")
    print("    - one exact native twisted-flux holonomy still does not collapse a fixed-w slice")
    print("    - the explicit witness pair is realized exactly and carries distinct nonzero chi")
    print()
    print("  So the next honest PMNS-native theorem surface is now a genuinely new")
    print("  fixed-slice current-image collapse law beyond the current selector/holonomy bank.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
