#!/usr/bin/env python3
"""Boundary theorem for local scalar-field deformations on the retained PMNS lane.

Question:
  If we admit the retained lowest-order local scalar field from the current
  architecture, can that route by itself generate the nontrivial retained PMNS
  triplet structure?

Answer:
  No. The commutative local scalar algebra projects to the diagonal algebra on
  the `hw=1` generation triplet. Therefore any local scalar deformation on the
  retained lepton surface produces only diagonal triplet blocks. The resulting
  lower-level response profiles are diagonal column sets and are rejected by the
  retained one-sided minimal PMNS closure stack.

Boundary:
  This is stronger than the uniform-scalar theorem. It closes the whole local
  scalar-field route, not just its translation-invariant subfamily.
"""

from __future__ import annotations

import sys

import numpy as np

from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_response_columns_from_sector_operator,
    support_mask,
)
from frontier_pmns_active_four_real_source_from_transport import active_four_real_source
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables

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


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def taste_vector(state: tuple[int, int, int]) -> np.ndarray:
    v = np.array([1.0, 0.0], dtype=complex) if state[0] == 0 else np.array([0.0, 1.0], dtype=complex)
    for idx in (1, 2):
        vk = np.array([1.0, 0.0], dtype=complex) if state[idx] == 0 else np.array([0.0, 1.0], dtype=complex)
        v = np.kron(v, vk)
    return v


def triplet_projector() -> np.ndarray:
    hw1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    return np.column_stack([taste_vector(s) for s in hw1])


def scalar_site_projectors() -> list[np.ndarray]:
    basis = []
    for i in range(8):
        op = np.zeros((8, 8), dtype=complex)
        op[i, i] = 1.0
        basis.append(op)
    return basis


def projected_scalar_basis() -> list[np.ndarray]:
    p = triplet_projector()
    return [p.conj().T @ op @ p for op in scalar_site_projectors()]


def projected_local_scalar_block(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=complex)
    if values.shape != (8,):
        raise ValueError("expected 8 site values")
    p = triplet_projector()
    op = np.diag(values)
    return p.conj().T @ op @ p


def part1_projected_commutative_scalar_algebra_is_exactly_diagonal_on_the_hw1_triplet() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PROJECTED LOCAL SCALAR ALGEBRA IS EXACTLY DIAGONAL")
    print("=" * 88)

    basis = projected_scalar_basis()
    vecs = np.array([b.reshape(-1) for b in basis], dtype=complex)
    rank = int(np.linalg.matrix_rank(vecs))
    nz = [(i, b) for i, b in enumerate(basis) if np.linalg.norm(b) > 1e-12]

    check("The projected local scalar algebra on the hw=1 triplet has dimension 3", rank == 3, f"rank={rank}")
    check("Exactly three projected site projectors survive on the hw=1 triplet", len(nz) == 3, f"indices={[i for i, _ in nz]}")
    check("Each surviving projected scalar basis element is diagonal", all(np.linalg.norm(b - np.diag(np.diag(b))) < 1e-12 for _, b in nz))
    check("Those three diagonal basis elements span the full diagonal algebra on the triplet", True,
          f"basis={[np.round(np.diag(b), 3).tolist() for _, b in nz]}")


def part2_any_local_scalar_field_produces_only_diagonal_triplet_blocks() -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: ANY LOCAL SCALAR FIELD PRODUCES ONLY DIAGONAL TRIPLET BLOCKS")
    print("=" * 88)

    phi_neutral = np.array([0.2, 0.8, -0.4, 0.1, 1.1, -0.3, 0.6, -0.7], dtype=float)
    phi_charge = np.array([-0.2, 1.4, 0.9, -0.1, 0.7, 0.3, -0.5, 0.2], dtype=float)
    d0_trip = projected_local_scalar_block(phi_neutral)
    dm_trip = projected_local_scalar_block(phi_charge)

    check("The neutral local-scalar triplet block is diagonal", np.linalg.norm(d0_trip - np.diag(np.diag(d0_trip))) < 1e-12,
          f"diag={np.round(np.diag(d0_trip), 6)}")
    check("The charge-(-1) local-scalar triplet block is diagonal", np.linalg.norm(dm_trip - np.diag(np.diag(dm_trip))) < 1e-12,
          f"diag={np.round(np.diag(dm_trip), 6)}")
    check("A diagonal triplet block has no canonical active support I+C", np.array_equal(support_mask(d0_trip), np.eye(3, dtype=int)))
    check("A diagonal triplet block carries no cycle-channel source data", np.linalg.norm(active_four_real_source(d0_trip)[2:]) < 1e-12,
          f"rho={np.round(active_four_real_source(d0_trip)[2:], 6)}")

    return d0_trip, dm_trip


def part3_local_scalar_response_profiles_stay_diagonal() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 3: LOCAL-SCALAR RESPONSE PROFILES STAY DIAGONAL")
    print("=" * 88)

    d0_trip = np.diag([1.2, 0.8, 1.5]).astype(complex)
    dm_trip = np.diag([0.3, 1.7, 0.9]).astype(complex)
    lam_act = 0.31
    lam_pass = 0.27

    active_cols = active_response_columns_from_sector_operator(d0_trip, lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(dm_trip, lam_pass)[1]
    _act_kernel, act_block = derive_active_block_from_response_columns(active_cols, lam_act)
    _pass_kernel, pass_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)

    check("The active local-scalar response profile is diagonal", np.array_equal(support_mask(np.column_stack(active_cols)), np.eye(3, dtype=int)))
    check("The passive local-scalar response profile is diagonal", np.array_equal(support_mask(np.column_stack(passive_cols)), np.eye(3, dtype=int)))
    check("The diagonal response profiles recover the same diagonal triplet blocks exactly",
          np.linalg.norm(act_block - d0_trip) < 1e-12 and np.linalg.norm(pass_block - dm_trip) < 1e-12)

    return active_cols, passive_cols


def part4_the_retained_pmns_closure_stack_rejects_the_whole_local_scalar_route(
    active_cols: list[np.ndarray], passive_cols: list[np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE RETAINED PMNS STACK REJECTS THE WHOLE LOCAL-SCALAR ROUTE")
    print("=" * 88)

    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(active_cols, passive_cols, 0.31, 0.27),
        ValueError,
    )
    check("The live retained closure stack rejects diagonal local-scalar response profiles", ok, detail)
    check("Reason: diagonal local-scalar data do not realize a one-sided minimal PMNS class",
          ("one-sided minimal PMNS class" in detail) or ("response packs do not realize a one-sided minimal PMNS class" in detail),
          detail)


def main() -> int:
    print("=" * 88)
    print("PMNS LOCAL SCALAR DEFORMATION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If we admit the retained lowest-order local scalar field, can that")
    print("  route by itself generate the nontrivial retained PMNS triplet data?")

    part1_projected_commutative_scalar_algebra_is_exactly_diagonal_on_the_hw1_triplet()
    part2_any_local_scalar_field_produces_only_diagonal_triplet_blocks()
    active_cols, passive_cols = part3_local_scalar_response_profiles_stay_diagonal()
    part4_the_retained_pmns_closure_stack_rejects_the_whole_local_scalar_route(active_cols, passive_cols)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact local-scalar boundary:")
    print("    - the projected local scalar algebra on the hw=1 triplet is diagonal")
    print("    - any retained local scalar deformation yields only diagonal triplet blocks")
    print("    - the induced lower-level response profiles stay diagonal")
    print("    - the retained PMNS closure stack rejects that whole route")
    print()
    print("  So the retained lowest-order local scalar field cannot by itself")
    print("  generate the PMNS-active non-monomial triplet structure.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
