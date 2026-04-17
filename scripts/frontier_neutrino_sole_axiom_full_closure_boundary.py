#!/usr/bin/env python3
"""Full retained-neutrino sole-axiom closure boundary.

Question:
  Does the retained neutrino lane close top-to-bottom from the sole axiom
  `Cl(3)` on `Z^3` alone?

Answer:
  No.

  On the retained science branch the sole axiom fixes the exact carrier and the
  downstream closure interfaces, but it does not produce a full positive
  neutrino realization:

    - on the Dirac/PMNS side, the sole-axiom response profiles are the trivial
      free ones, scalar routes stay too small, and the surviving graph-first
      reduced oriented-cycle channel is not value-selected by the current bank
    - on the Majorana side, the lower-level charge-preserving response layer
      induces no anomalous Nambu block

  Therefore full retained-neutrino sole-axiom closure is blocked on the current
  exact bank.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_neutrino_majorana_lower_level_pairing_nogo import (
    induced_pairing_block,
    nambu_response_kernel,
    random_invertible_hermitian,
)
from frontier_pmns_current_bank_value_selection_nogo import (
    active_block_with_reduced_cycle,
    reduced_cycle_coordinates,
    residual_swap_conjugate,
)
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_response_columns
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    passive_response_columns_from_sector_operator,
    sector_operator_fixture_from_effective_block,
    support_mask,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
TARGET_SUPPORT = (
    np.abs(np.eye(3, dtype=complex) + np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)) > 0
).astype(int)


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


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def part1_dirac_pmns_sole_axiom_route_is_not_positively_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: DIRAC/PMNS SOLE-AXIOM ROUTE IS NOT POSITIVELY CLOSED")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27

    free_active_cols = active_response_columns_from_sector_operator(I3, lam_act)[1]
    free_passive_cols = passive_response_columns_from_sector_operator(I3, lam_pass)[1]
    ok_free, detail_free = expect_raises(
        lambda: close_from_lower_level_observables(free_active_cols, free_passive_cols, lam_act, lam_pass),
        ValueError,
    )
    check("The sole-axiom free response profiles are rejected by the retained PMNS closure stack", ok_free, detail_free)
    check("The sole-axiom free active response profile has only diagonal support",
          np.array_equal(support_mask(np.column_stack(free_active_cols)), np.eye(3, dtype=int)))

    diagonal_active = np.diag([1.21, 0.94, 1.08]).astype(complex)
    scalar_passive = scalar_triplet_block(1.13)
    scalar_active_cols = active_response_columns_from_sector_operator(diagonal_active, lam_act)[1]
    scalar_passive_cols = passive_response_columns_from_sector_operator(scalar_passive, lam_pass)[1]
    _diag_kernel, diag_block = derive_active_block_from_response_columns(scalar_active_cols, lam_act)
    ok_scalar, detail_scalar = expect_raises(
        lambda: close_from_lower_level_observables(scalar_active_cols, scalar_passive_cols, lam_act, lam_pass),
        ValueError,
    )
    check("The retained scalar deformation route stays diagonal on the active triplet",
          np.array_equal(support_mask(diag_block), np.eye(3, dtype=int)))
    check("The retained PMNS closure stack rejects the scalar route too", ok_scalar, detail_scalar)


def part2_graph_first_reduced_cycle_channel_is_realized_but_not_selected() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE GRAPH-FIRST REDUCED CYCLE CHANNEL IS REALIZED BUT NOT SELECTED")
    print("=" * 88)

    lam = 0.31
    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)

    sector_a = sector_operator_fixture_from_effective_block(a, seed=5101)
    sector_b = sector_operator_fixture_from_effective_block(b, seed=5102)
    _ref_a, cols_a = active_response_columns_from_sector_operator(sector_a, lam)
    _ref_b, cols_b = active_response_columns_from_sector_operator(sector_b, lam)
    _ker_a, rec_a = derive_active_block_from_response_columns(cols_a, lam)
    _ker_b, rec_b = derive_active_block_from_response_columns(cols_b, lam)
    coeffs_a = oriented_cycle_coeffs_from_response_columns(cols_a, lam)
    coeffs_b = oriented_cycle_coeffs_from_response_columns(cols_b, lam)
    coords_a = reduced_cycle_coordinates(rec_a)
    coords_b = reduced_cycle_coordinates(rec_b)

    check("Two distinct reduced-channel points are both realized exactly on the lower-level active response chain",
          np.linalg.norm(rec_a - a) < 1e-12 and np.linalg.norm(rec_b - b) < 1e-12 and np.linalg.norm(a - b) > 1e-6,
          f"|A-B|={np.linalg.norm(a - b):.6f}")
    check("Both realized points satisfy the same graph-first residual antiunitary symmetry",
          np.linalg.norm(residual_swap_conjugate(rec_a) - rec_a) < 1e-12
          and np.linalg.norm(residual_swap_conjugate(rec_b) - rec_b) < 1e-12)
    check("The native oriented-cycle observable law separates the two realized points exactly",
          np.linalg.norm(coeffs_a - coeffs_b) > 1e-6 and np.linalg.norm(coords_a - coords_b) > 1e-6,
          f"|Δcoords|={np.linalg.norm(coords_a - coords_b):.6f}")
    print("  [INFO] The current exact bank does not select a unique reduced-channel value")
    check("The surviving positive carrier has canonical diagonal-plus-forward-cycle support",
          np.array_equal(support_mask(rec_a), TARGET_SUPPORT) and np.array_equal(support_mask(rec_b), TARGET_SUPPORT))


def part3_majorana_stays_closed_negatively_on_the_lower_level_charge_preserving_lane() -> None:
    print("\n" + "=" * 88)
    print("PART 3: MAJORANA STAYS CLOSED NEGATIVELY ON THE LOWER-LEVEL LANE")
    print("=" * 88)

    n3 = random_invertible_hermitian(3, 6003)
    kernel3 = nambu_response_kernel(n3)
    pair3 = induced_pairing_block(kernel3, 3)

    check("The lower-level charge-preserving Nambu response has zero anomalous block in the three-generation channel",
          np.linalg.norm(pair3) < 1e-12,
          f"|pair|={np.linalg.norm(pair3):.2e}")
    print("  [INFO] The retained Majorana lane does not reopen on the lower-level charge-preserving response layer")


def part4_circularity_guards() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CIRCULARITY GUARDS")
    print("=" * 88)

    ok_active, bad_active = circularity_guard(active_response_columns_from_sector_operator, {"x", "y", "delta", "tau", "q"})
    ok_cycle, bad_cycle = circularity_guard(oriented_cycle_coeffs_from_response_columns, {"u", "v", "w", "sigma"})
    ok_close, bad_close = circularity_guard(close_from_lower_level_observables, {"tau", "q", "x", "y", "delta"})

    check("The lower-level active response derivation takes no PMNS-side value targets as inputs", ok_active, f"bad={bad_active}")
    check("The native oriented-cycle readout takes no reduced-channel coordinates as inputs", ok_cycle, f"bad={bad_cycle}")
    check("The downstream PMNS closure stack takes no target PMNS values as inputs", ok_close, f"bad={bad_close}")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO SOLE-AXIOM FULL CLOSURE BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the retained neutrino lane close top-to-bottom from the sole axiom")
    print("  Cl(3) on Z^3 alone?")

    part1_dirac_pmns_sole_axiom_route_is_not_positively_closed()
    part2_graph_first_reduced_cycle_channel_is_realized_but_not_selected()
    part3_majorana_stays_closed_negatively_on_the_lower_level_charge_preserving_lane()
    part4_circularity_guards()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained-neutrino sole-axiom boundary:")
    print("    - the sole axiom does not produce PMNS-active lower-level response profiles")
    print("    - retained scalar deformation routes stay too small")
    print("    - the surviving graph-first reduced oriented-cycle channel is realized")
    print("      but not value-selected by the current exact bank")
    print("    - the retained Majorana lane does not reopen on the lower-level")
    print("      charge-preserving response layer")
    print()
    print("  Therefore full retained-neutrino closure from Cl(3) on Z^3 alone is")
    print("  blocked on the current exact bank. Any further positive closure would")
    print("  require genuinely new dynamics or a further admitted extension.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
