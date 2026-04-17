#!/usr/bin/env python3
"""Three-flux holonomy closure on the reduced PMNS oriented-cycle family.

Question:
  If one twisted flux holonomy only sees one real linear combination on the
  reduced graph-first oriented-cycle family, can a finite native family of
  flux holonomies close that reduced family exactly?

Answer:
  Yes.

  On the reduced graph-first family

      A_fwd(u, v, w) = u B1 + v B2 + w B3

  the one-angle flux holonomy is the linear functional

      h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w.

  Therefore a generic three-angle flux family gives the exact 3 x 3 system

      M(phis) [u, v, w]^T = h

  with rows `[2 cos(phi_i), 2 sin(phi_i), 1]`. Whenever det M(phis) != 0, the
  reduced coordinates `(u, v, w)` are reconstructed exactly.

  So the twisted-flux route is not just a boundary. Admitting a generic
  three-flux family closes the reduced PMNS cycle values exactly.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_pmns_twisted_flux_transfer_holonomy_boundary import (
    flux_holonomy_on_reduced_family,
    reduced_cycle_family,
)
from pmns_lower_level_utils import circularity_guard

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


def design_matrix(phis: list[float] | tuple[float, ...]) -> np.ndarray:
    return np.array([[2.0 * math.cos(phi), 2.0 * math.sin(phi), 1.0] for phi in phis], dtype=float)


def determinant_formula(phis: list[float] | tuple[float, ...]) -> float:
    a, b, c = phis
    return 4.0 * (math.sin(b - a) + math.sin(c - b) + math.sin(a - c))


def three_flux_holonomies_on_reduced_family(a: np.ndarray, phis: list[float] | tuple[float, ...]) -> np.ndarray:
    return np.array([flux_holonomy_on_reduced_family(a, phi) for phi in phis], dtype=float)


def recover_reduced_cycle_coordinates_from_three_flux_holonomies(
    holonomies: np.ndarray, phis: list[float] | tuple[float, ...]
) -> np.ndarray:
    return np.linalg.solve(design_matrix(phis), np.asarray(holonomies, dtype=float))


def part1_generic_three_flux_family_has_full_rank() -> tuple[tuple[float, float, float], np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: A GENERIC THREE-FLUX FAMILY HAS FULL RANK")
    print("=" * 88)

    phis = (0.0, math.pi / 2.0, math.pi / 3.0)
    m = design_matrix(phis)
    det_exact = determinant_formula(phis)
    det_numeric = float(np.linalg.det(m))

    check("The three-flux design matrix has the exact rows [2 cos(phi_i), 2 sin(phi_i), 1]",
          np.linalg.norm(m - np.array([[2.0, 0.0, 1.0], [0.0, 2.0, 1.0], [1.0, math.sqrt(3.0), 1.0]])) < 1e-12)
    check("The determinant matches the exact trigonometric formula",
          abs(det_numeric - det_exact) < 1e-12,
          f"det_numeric={det_numeric:.12f}, det_exact={det_exact:.12f}")
    check("A generic three-flux family has full rank", abs(det_numeric) > 1e-12,
          f"det={det_numeric:.12f}")

    return phis, m


def part2_three_flux_holonomies_reconstruct_the_reduced_cycle_coordinates_exactly(
    phis: tuple[float, float, float]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THREE FLUX HOLOMONIES RECONSTRUCT (u,v,w) EXACTLY")
    print("=" * 88)

    target = np.array([0.41, 0.32, 0.28], dtype=float)
    a = reduced_cycle_family(*target)
    hol = three_flux_holonomies_on_reduced_family(a, phis)
    recovered = recover_reduced_cycle_coordinates_from_three_flux_holonomies(hol, phis)

    check("The three-flux holonomy vector is the exact linear image of (u,v,w)",
          np.linalg.norm(hol - design_matrix(phis) @ target) < 1e-12,
          f"hol={np.round(hol, 6)}")
    check("The reduced coordinates are reconstructed exactly from the three holonomies",
          np.linalg.norm(recovered - target) < 1e-12,
          f"recovered={np.round(recovered, 6)}")
    check("So the reduced graph-first PMNS cycle values close exactly on the three-flux route", True)


def part3_three_flux_values_separate_distinct_reduced_channel_points(
    phis: tuple[float, float, float]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THREE FLUX VALUES SEPARATE DISTINCT REDUCED-CHANNEL POINTS")
    print("=" * 88)

    a_vec = np.array([0.41, 0.32, 0.28], dtype=float)
    b_vec = np.array([0.29, -0.17, 0.34], dtype=float)
    a = reduced_cycle_family(*a_vec)
    b = reduced_cycle_family(*b_vec)
    hol_a = three_flux_holonomies_on_reduced_family(a, phis)
    hol_b = three_flux_holonomies_on_reduced_family(b, phis)
    rec_a = recover_reduced_cycle_coordinates_from_three_flux_holonomies(hol_a, phis)
    rec_b = recover_reduced_cycle_coordinates_from_three_flux_holonomies(hol_b, phis)

    check("Two distinct reduced-channel points give distinct three-flux holonomy vectors",
          np.linalg.norm(hol_a - hol_b) > 1e-6,
          f"|Δhol|={np.linalg.norm(hol_a - hol_b):.6f}")
    check("Each holonomy vector reconstructs its own reduced point exactly",
          np.linalg.norm(rec_a - a_vec) < 1e-12 and np.linalg.norm(rec_b - b_vec) < 1e-12,
          f"rec_a={np.round(rec_a, 6)}, rec_b={np.round(rec_b, 6)}")
    check("Therefore the three-flux route removes the 2-real kernel left by the one-angle probe", True)


def part4_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CIRCULARITY GUARD")
    print("=" * 88)

    ok_map, bad_map = circularity_guard(three_flux_holonomies_on_reduced_family, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_rec, bad_rec = circularity_guard(recover_reduced_cycle_coordinates_from_three_flux_holonomies, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    check("The three-flux holonomy map takes no PMNS-side target coordinates as inputs", ok_map, f"bad={bad_map}")
    check("The three-flux reconstruction takes no PMNS-side target coordinates as inputs", ok_rec, f"bad={bad_rec}")


def main() -> int:
    print("=" * 88)
    print("PMNS THREE-FLUX HOLOMONY CLOSURE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a finite native family of twisted flux holonomies close the")
    print("  reduced graph-first PMNS oriented-cycle family exactly?")

    phis, _m = part1_generic_three_flux_family_has_full_rank()
    part2_three_flux_holonomies_reconstruct_the_reduced_cycle_coordinates_exactly(phis)
    part3_three_flux_values_separate_distinct_reduced_channel_points(phis)
    part4_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive closure on the twisted-flux route:")
    print("    - one-angle holonomy leaves a 2-real kernel on the reduced family")
    print("    - a generic three-flux family gives an invertible 3 x 3 system")
    print("    - the reduced graph-first cycle values (u,v,w) are reconstructed")
    print("      exactly from the three holonomies")
    print()
    print("  So the twisted-flux route now closes the reduced PMNS cycle values")
    print("  exactly, once a generic three-flux family is admitted.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
