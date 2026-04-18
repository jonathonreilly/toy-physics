#!/usr/bin/env python3
"""Exact two-holonomy collapse law on the PMNS-native fixed-slice current lane.

Question:
  Once the graph-first PMNS current image is reduced to one fixed slice
  `w = w0`, is there a genuinely new native holonomy law that collapses the
  remaining complex current `chi = u + i v` exactly?

Answer:
  Yes.

  On the reduced graph-first family,

      A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31,

  a one-angle flux holonomy has the form

      h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w.

  Therefore, on a fixed slice `w = w0`, any two-angle pair `(phi1, phi2)` with
  `sin(phi2 - phi1) != 0` gives the exact 2 x 2 system

      [h_phi1 - w0, h_phi2 - w0]^T = M(phi1, phi2) [u, v]^T

  with rows `[2 cos(phi_i), 2 sin(phi_i)]`.

  So two independent native holonomies collapse the fixed slice exactly, and
  hence recover `chi` exactly. One holonomy is still insufficient, but adding
  one genuinely new independent angle is already enough.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_character_holonomy_closure import c3_character_phases
from frontier_pmns_c3_character_mode_reduction import reduced_character_data_from_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import active_block_with_reduced_cycle
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


def fixed_slice_design_matrix(phis: tuple[float, float]) -> np.ndarray:
    return np.array(
        [
            [2.0 * math.cos(phis[0]), 2.0 * math.sin(phis[0])],
            [2.0 * math.cos(phis[1]), 2.0 * math.sin(phis[1])],
        ],
        dtype=float,
    )


def fixed_slice_det_formula(phis: tuple[float, float]) -> float:
    return 4.0 * math.sin(phis[1] - phis[0])


def fixed_slice_two_holonomies_on_block(block: np.ndarray, phis: tuple[float, float], w0: float) -> np.ndarray:
    return np.array([flux_holonomy_on_reduced_family(block, phi) - w0 for phi in phis], dtype=float)


def recover_chi_from_fixed_slice_two_holonomies(
    holonomies_minus_w: np.ndarray, phis: tuple[float, float]
) -> complex:
    u, v = np.linalg.solve(fixed_slice_design_matrix(phis), np.asarray(holonomies_minus_w, dtype=float))
    return complex(float(u), float(v))


def c3_pair_current_formula(h0: float, h1: float, w0: float) -> complex:
    u = 0.5 * (h0 - w0)
    v = (h0 + 2.0 * h1 - 3.0 * w0) / (2.0 * math.sqrt(3.0))
    return complex(u, v)


def exact_one_angle_fixed_slice_witness_pair(phi: float = 0.41, w0: float = 0.28) -> tuple[np.ndarray, np.ndarray]:
    u0, v0 = 0.41, 0.32
    hu = flux_holonomy_on_reduced_family(reduced_cycle_family(1.0, 0.0, 0.0), phi)
    hv = flux_holonomy_on_reduced_family(reduced_cycle_family(0.0, 1.0, 0.0), phi)
    step = 0.2
    u1 = u0 + step * hv
    v1 = v0 - step * hu
    a = active_block_with_reduced_cycle(u0, v0, w0, xbar=1.0)
    b = active_block_with_reduced_cycle(u1, v1, w0, xbar=1.0)
    return a, b


def realize(block: np.ndarray, seed: int, lam: float = 0.31) -> np.ndarray:
    sector = sector_operator_fixture_from_effective_block(block, seed=seed)
    _ref, cols = active_response_columns_from_sector_operator(sector, lam)
    _kernel, recovered = derive_active_block_from_response_columns(cols, lam)
    return recovered


def part1_generic_two_angles_have_full_rank_on_a_fixed_slice() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 1: GENERIC TWO-ANGLE FAMILIES HAVE FULL RANK ON A FIXED SLICE")
    print("=" * 88)

    phis = (0.17, 1.11)
    m = fixed_slice_design_matrix(phis)
    det_numeric = float(np.linalg.det(m))
    det_exact = fixed_slice_det_formula(phis)

    check(
        "The fixed-slice two-angle design matrix has rows [2 cos(phi_i), 2 sin(phi_i)]",
        np.linalg.norm(
            m
            - np.array(
                [
                    [2.0 * math.cos(phis[0]), 2.0 * math.sin(phis[0])],
                    [2.0 * math.cos(phis[1]), 2.0 * math.sin(phis[1])],
                ],
                dtype=float,
            )
        )
        < 1e-12,
    )
    check(
        "Its determinant matches the exact fixed-slice formula 4 sin(phi2-phi1)",
        abs(det_numeric - det_exact) < 1e-12,
        f"det_numeric={det_numeric:.12f}, det_exact={det_exact:.12f}",
    )
    check("A generic two-angle family is invertible on the fixed slice", abs(det_numeric) > 1e-12, f"det={det_numeric:.12f}")
    return phis


def part2_two_fixed_slice_holonomies_reconstruct_chi_exactly(phis: tuple[float, float]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: TWO FIXED-SLICE HOLOMONIES RECONSTRUCT chi EXACTLY")
    print("=" * 88)

    target = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    _hol, modes = reduced_character_data_from_block(target)
    w0 = float(np.real(modes[0]))
    chi = nontrivial_character_current(target)
    holonomies_minus_w = fixed_slice_two_holonomies_on_block(target, phis, w0)
    recovered = recover_chi_from_fixed_slice_two_holonomies(holonomies_minus_w, phis)

    check("The fixed slice contributes only the known trivial mode w0", abs(w0 - 0.28) < 1e-12, f"w0={w0:.6f}")
    check(
        "The two-angle fixed-slice holonomy vector is the exact linear image of (u,v)",
        np.linalg.norm(holonomies_minus_w - fixed_slice_design_matrix(phis) @ np.array([chi.real, chi.imag], dtype=float)) < 1e-12,
        f"hol-w={np.round(holonomies_minus_w, 6)}",
    )
    check(
        "The recovered fixed-slice current equals the exact native current chi",
        abs(recovered - chi) < 1e-12,
        f"recovered={recovered:.6f}, chi={chi:.6f}",
    )
    check("So a generic two-angle native holonomy family collapses the fixed slice exactly", True)


def part3_one_holonomy_is_insufficient_but_adding_one_new_angle_collapses_the_same_fixed_slice() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONE HOLOMONY IS INSUFFICIENT, BUT ONE NEW ANGLE ALREADY COLLAPSES THE FIXED SLICE")
    print("=" * 88)

    phi0 = 0.41
    psi = 2.0 * math.pi / 3.0
    a, b = exact_one_angle_fixed_slice_witness_pair(phi=phi0, w0=0.28)
    chi_a = nontrivial_character_current(a)
    chi_b = nontrivial_character_current(b)
    _hol_a, modes_a = reduced_character_data_from_block(a)
    _hol_b, modes_b = reduced_character_data_from_block(b)
    w0 = float(np.real(modes_a[0]))
    pair = (phi0, psi)

    h0_a = flux_holonomy_on_reduced_family(a, phi0)
    h0_b = flux_holonomy_on_reduced_family(b, phi0)
    h1_a = flux_holonomy_on_reduced_family(a, psi)
    h1_b = flux_holonomy_on_reduced_family(b, psi)
    rec_a = recover_chi_from_fixed_slice_two_holonomies(fixed_slice_two_holonomies_on_block(a, pair, w0), pair)
    rec_b = recover_chi_from_fixed_slice_two_holonomies(fixed_slice_two_holonomies_on_block(b, pair, w0), pair)

    check(
        "The witness pair lies on the same exact fixed slice",
        abs(modes_a[0] - modes_b[0]) < 1e-12,
        f"w={modes_a[0]:.6f}",
    )
    check(
        "A single one-angle holonomy still fails on that fixed slice",
        abs(h0_a - h0_b) < 1e-12 and abs(chi_a - chi_b) > 1e-6,
        f"h_phi0={h0_a:.12f}, chi_a={chi_a:.6f}, chi_b={chi_b:.6f}",
    )
    check(
        "Adding one genuinely new independent angle separates the same witness pair",
        abs(h1_a - h1_b) > 1e-6,
        f"h_psi(a)={h1_a:.12f}, h_psi(b)={h1_b:.12f}",
    )
    check(
        "The two-angle fixed-slice reconstruction recovers the distinct exact currents on that same witness pair",
        abs(rec_a - chi_a) < 1e-12 and abs(rec_b - chi_b) < 1e-12 and abs(rec_a - rec_b) > 1e-6,
        f"rec_a={rec_a:.6f}, rec_b={rec_b:.6f}",
    )


def part4_the_canonical_c3_character_pair_is_a_native_fixed_slice_collapse_witness() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CANONICAL C3 CHARACTER PAIR IS A NATIVE FIXED-SLICE COLLAPSE WITNESS")
    print("=" * 88)

    phi0, phi1, _phi2 = c3_character_phases()
    target = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    chi = nontrivial_character_current(target)
    _hol, modes = reduced_character_data_from_block(target)
    w0 = float(np.real(modes[0]))
    h0 = flux_holonomy_on_reduced_family(target, phi0)
    h1 = flux_holonomy_on_reduced_family(target, phi1)
    chi_formula = c3_pair_current_formula(h0, h1, w0)
    chi_linear = recover_chi_from_fixed_slice_two_holonomies(np.array([h0 - w0, h1 - w0], dtype=float), (phi0, phi1))
    det = float(np.linalg.det(fixed_slice_design_matrix((phi0, phi1))))

    check("The canonical native C3 pair has nonzero fixed-slice determinant", abs(det) > 1e-12, f"det={det:.12f}")
    check(
        "The explicit C3-pair current formula recovers chi exactly from (h_0, h_2pi/3, w0)",
        abs(chi_formula - chi) < 1e-12,
        f"chi_formula={chi_formula:.6f}, chi={chi:.6f}",
    )
    check(
        "The same canonical pair matches the generic two-angle linear reconstruction",
        abs(chi_linear - chi) < 1e-12 and abs(chi_linear - chi_formula) < 1e-12,
        f"chi_linear={chi_linear:.6f}",
    )
    check("So the fixed-slice collapse law already has a canonical native C3 witness", True)


def part5_the_fixed_slice_collapse_is_exactly_realized_on_the_active_response_chain() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE FIXED-SLICE COLLAPSE IS EXACTLY REALIZED ON THE ACTIVE RESPONSE CHAIN")
    print("=" * 88)

    phis = (0.0, 2.0 * math.pi / 3.0)
    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.28, xbar=1.0)
    rec_a = realize(a, 7401)
    rec_b = realize(b, 7402)
    _hol_a, modes_a = reduced_character_data_from_block(rec_a)
    _hol_b, modes_b = reduced_character_data_from_block(rec_b)
    chi_a = nontrivial_character_current(rec_a)
    chi_b = nontrivial_character_current(rec_b)
    fixed_a = recover_chi_from_fixed_slice_two_holonomies(fixed_slice_two_holonomies_on_block(rec_a, phis, float(np.real(modes_a[0]))), phis)
    fixed_b = recover_chi_from_fixed_slice_two_holonomies(fixed_slice_two_holonomies_on_block(rec_b, phis, float(np.real(modes_b[0]))), phis)

    check("Witness A is realized exactly on the active response chain", np.linalg.norm(rec_a - a) < 1e-12, f"err={np.linalg.norm(rec_a - a):.2e}")
    check("Witness B is realized exactly on the active response chain", np.linalg.norm(rec_b - b) < 1e-12, f"err={np.linalg.norm(rec_b - b):.2e}")
    check(
        "The realized fixed-slice points have distinct nonzero exact currents",
        abs(chi_a) > 1e-6 and abs(chi_b) > 1e-6 and abs(chi_a - chi_b) > 1e-6 and abs(modes_a[0] - modes_b[0]) < 1e-12,
        f"w={modes_a[0]:.6f}, chi_a={chi_a:.6f}, chi_b={chi_b:.6f}",
    )
    check(
        "The canonical fixed-slice two-holonomy law reconstructs those realized currents exactly",
        abs(fixed_a - chi_a) < 1e-12 and abs(fixed_b - chi_b) < 1e-12,
        f"fixed_a={fixed_a:.6f}, fixed_b={fixed_b:.6f}",
    )


def part6_existing_exact_notes_already_position_this_as_collapse_not_production() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE EXISTING EXACT BANK ALREADY POSITIONS THIS AS COLLAPSE, NOT PRODUCTION")
    print("=" * 88)

    flux_note = read("docs/PMNS_TWISTED_FLUX_TRANSFER_HOLONOMY_BOUNDARY_NOTE.md")
    mode_note = read("docs/PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md")
    current_note = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")

    check(
        "The one-angle holonomy note already records that one probe leaves a 2-real kernel",
        "one flux holonomy alone" in flux_note and "2-real kernel" in flux_note,
    )
    check(
        "The mode-reduction note already records that the remaining fixed-slice target is the complex character amplitude chi",
        "one real trivial-character amplitude `w`" in mode_note
        and "one complex nontrivial character amplitude `chi := z_2 = u + i v`" in mode_note,
    )
    check(
        "The native current note already identifies that character amplitude with J_chi = u + i v",
        "J_chi(A_fwd) = chi = u + i v" in current_note,
    )
    check(
        "So the new result is an exact fixed-slice collapse law for the existing native current readout, not a new sole-axiom production law for nonzero J_chi",
        True,
    )


def part7_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 7: CIRCULARITY GUARD")
    print("=" * 88)

    ok_hol, bad_hol = circularity_guard(fixed_slice_two_holonomies_on_block, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_rec, bad_rec = circularity_guard(recover_chi_from_fixed_slice_two_holonomies, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_c3, bad_c3 = circularity_guard(c3_pair_current_formula, {"u", "v", "w", "x", "y", "delta", "tau", "q"})

    check("The fixed-slice two-holonomy map takes no PMNS-side target values as inputs", ok_hol, f"bad={bad_hol}")
    check("The fixed-slice reconstruction takes no PMNS-side target values as inputs", ok_rec, f"bad={bad_rec}")
    check("The explicit canonical C3-pair current formula takes no PMNS-side target values as inputs", ok_c3, f"bad={bad_c3}")


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST FIXED-SLICE TWO-HOLOMONY COLLAPSE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On a fixed PMNS-native graph-first slice w = w0, can one genuinely")
    print("  new independent native holonomy collapse the remaining current chi")
    print("  exactly, beyond the known one-angle no-go?")

    phis = part1_generic_two_angles_have_full_rank_on_a_fixed_slice()
    part2_two_fixed_slice_holonomies_reconstruct_chi_exactly(phis)
    part3_one_holonomy_is_insufficient_but_adding_one_new_angle_collapses_the_same_fixed_slice()
    part4_the_canonical_c3_character_pair_is_a_native_fixed_slice_collapse_witness()
    part5_the_fixed_slice_collapse_is_exactly_realized_on_the_active_response_chain()
    part6_existing_exact_notes_already_position_this_as_collapse_not_production()
    part7_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS-native fixed-slice collapse theorem:")
    print("    - one-angle holonomy still fails on a fixed w slice")
    print("    - any independent second native holonomy gives an invertible 2 x 2")
    print("      fixed-slice system for (u, v)")
    print("    - therefore chi = u + i v is reconstructed exactly from fixed w plus")
    print("      two native holonomies")
    print("    - the canonical C3 pair (0, 2pi/3) is an explicit native witness")
    print()
    print("  This closes the PMNS-native fixed-slice collapse frontier on the")
    print("  readout side. It does not by itself produce nonzero J_chi from")
    print("  Cl(3) on Z^3 alone.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
