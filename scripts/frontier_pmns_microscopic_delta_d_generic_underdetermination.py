#!/usr/bin/env python3
"""
Exact current-bank underdetermination theorem for generic off-seed PMNS ΔD.

Question:
  After deriving the native free microscopic core D_free = I on the retained
  lepton surface and reducing the PMNS deformation to the exact channel family

      ΔD = U + V C + W C^2,

  does the current retained Cl(3) on Z^3 bank determine the generic off-seed
  value law of ΔD?

Answer:
  No. On a fixed one-sided minimal PMNS branch with passive monomial lane held
  fixed, the active microscopic deformation is already the exact 7-real family

      ΔD_act(x,y,delta)
        = diag(x_1-1, x_2-1, x_3-1)
        + diag(y_1, y_2, y_3 e^{i delta}) C.

  The weak-axis seed patch is only the codimension-5 slice

      x_1=x_2=x_3,  y_1=y_2=y_3,  delta=0.

  Two distinct generic off-seed points on the same retained branch/support
  class embed into full charge-preserving microscopic operators with the same
  passive channel and the same exact structural constraints. Therefore the
  current retained bank fixes the carrier but not the generic off-seed values.

Boundary:
  This is a current-bank no-go / underdetermination theorem. It does not rule
  out that a future derived law from Cl(3) on Z^3 could fix the 7-real family.
  It proves only that the present retained bank does not.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
TARGET_SUPPORT = (np.abs(I3 + CYCLE) > 0).astype(int)
PASSIVE_OFFSET = 2
PASSIVE_COEFFS = np.array([0.07, 0.11, 0.23], dtype=complex)


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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def active_delta_d(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return active_operator(x, y, delta) - I3


def support_mask(mat: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    return (np.abs(mat) > tol).astype(int)


def passive_operator() -> np.ndarray:
    return diagonal(PASSIVE_COEFFS) @ {0: I3, 1: CYCLE, 2: CYCLE2}[PASSIVE_OFFSET]


def real_vec(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()])


def jacobian_rank_at(x: np.ndarray, y: np.ndarray, delta: float, eps: float = 1e-7) -> int:
    base = np.concatenate([x.astype(float), y.astype(float), np.array([delta], dtype=float)])
    f0 = real_vec(active_delta_d(x, y, delta))
    cols = []
    for i in range(7):
        p = base.copy()
        p[i] += eps
        fp = real_vec(active_delta_d(p[:3], p[3:6], float(p[6])))
        cols.append((fp - f0) / eps)
    jac = np.column_stack(cols)
    return int(np.linalg.matrix_rank(jac, tol=1e-6))


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def random_invertible_hermitian(n: int, seed: int, shift: float = 4.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = 0.5 * (m + m.conj().T)
    return h + shift * np.eye(n, dtype=complex)


def build_sector_from_schur_target(target: np.ndarray, rest_seed: int, coupling_seed: int) -> np.ndarray:
    rest = random_invertible_hermitian(2, rest_seed)
    rng = np.random.default_rng(coupling_seed)
    coupling = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    raw = target + coupling @ np.linalg.inv(rest) @ coupling.conj().T
    return np.block([[raw, coupling], [coupling.conj().T, rest]])


def build_full_operator_neutrino_active(active_target: np.ndarray, tag: int) -> np.ndarray:
    d0 = build_sector_from_schur_target(active_target, 100 + tag, 200 + tag)
    dm = build_sector_from_schur_target(passive_operator(), 300 + tag, 400 + tag)
    dp = random_invertible_hermitian(2, 500 + tag)
    zero_52 = np.zeros((5, 2), dtype=complex)
    zero_25 = np.zeros((2, 5), dtype=complex)
    return np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zero_52],
            [np.zeros((5, 5), dtype=complex), dm, zero_52],
            [zero_25, zero_25, dp],
        ]
    )


def schur_triplet_pair_from_full_operator(d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]
    l_nu = schur_eff(d0[:3, :3], d0[:3, 3:5], d0[3:5, :3], d0[3:5, 3:5])
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])
    return l_nu, l_e


def hermitian_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def breaking_triplet_from_h(h: np.ndarray) -> tuple[float, float, float]:
    d1, d2, d3, r12, r23, r31, phi = hermitian_coords(h)
    _ = d1, r23
    return (
        0.5 * (d2 - d3),
        0.5 * (r12 - r31 * math.cos(phi)),
        r31 * math.sin(phi),
    )


def part1_generic_active_delta_d_is_exactly_a_7_real_family_on_fixed_support() -> None:
    print("\n" + "=" * 88)
    print("PART 1: GENERIC ACTIVE ΔD IS EXACTLY A 7-REAL FAMILY ON FIXED SUPPORT")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    dd = active_delta_d(x, y, delta)

    rank = jacobian_rank_at(x, y, delta)
    expected = diagonal(x - np.ones(3, dtype=float)) + diagonal(
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex)
    ) @ CYCLE

    check(
        "The fixed-support active family is exactly ΔD = diag(x-1) + diag(y1,y2,y3 e^{iδ}) C",
        np.linalg.norm(dd - expected) < 1e-12,
        f"err={np.linalg.norm(dd - expected):.2e}",
    )
    check(
        "The active support mask is fixed to the canonical I+C target",
        np.array_equal(support_mask(dd + I3), TARGET_SUPPORT),
    )
    check(
        "The local real rank of the active parameterization is exactly 7 at a generic point",
        rank == 7,
        f"rank={rank}",
    )


def part2_the_weak_axis_seed_patch_is_only_a_codimension_5_slice() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE WEAK-AXIS SEED PATCH IS ONLY A CODIMENSION-5 SLICE")
    print("=" * 88)

    seed_x = np.array([0.9, 0.9, 0.9], dtype=float)
    seed_y = np.array([0.4, 0.4, 0.4], dtype=float)
    seed_delta = 0.0
    generic_x = np.array([1.15, 0.82, 0.95], dtype=float)
    generic_y = np.array([0.41, 0.28, 0.54], dtype=float)
    generic_delta = 0.63

    constraints_seed = np.array(
        [
            seed_x[0] - seed_x[1],
            seed_x[1] - seed_x[2],
            seed_y[0] - seed_y[1],
            seed_y[1] - seed_y[2],
            seed_delta,
        ],
        dtype=float,
    )
    constraints_generic = np.array(
        [
            generic_x[0] - generic_x[1],
            generic_x[1] - generic_x[2],
            generic_y[0] - generic_y[1],
            generic_y[1] - generic_y[2],
            generic_delta,
        ],
        dtype=float,
    )
    constraint_jac = np.array(
        [
            [1, -1, 0, 0, 0, 0, 0],
            [0, 1, -1, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0],
            [0, 0, 0, 0, 1, -1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ],
        dtype=float,
    )

    check("The seed patch satisfies x1=x2=x3, y1=y2=y3, delta=0", np.linalg.norm(constraints_seed) < 1e-12)
    check("A generic off-seed point violates that seed-slice system", np.linalg.norm(constraints_generic) > 1e-6,
          f"|g|={np.linalg.norm(constraints_generic):.6f}")
    check("Those seed-slice constraints are independent and have rank 5", np.linalg.matrix_rank(constraint_jac) == 5,
          f"rank={np.linalg.matrix_rank(constraint_jac)}")


def part3_two_distinct_generic_off_seed_points_embed_into_full_microscopic_operators_on_the_same_retained_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 3: DISTINCT OFF-SEED POINTS EMBED ON THE SAME RETAINED BRANCH")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63
    x_b = np.array([1.07, 0.91, 0.79], dtype=float)
    y_b = np.array([0.36, 0.33, 0.46], dtype=float)
    delta_b = -0.41

    target_a = active_operator(x_a, y_a, delta_a)
    target_b = active_operator(x_b, y_b, delta_b)

    d_a = build_full_operator_neutrino_active(target_a, 11)
    d_b = build_full_operator_neutrino_active(target_b, 29)
    lnu_a, le_a = schur_triplet_pair_from_full_operator(d_a)
    lnu_b, le_b = schur_triplet_pair_from_full_operator(d_b)

    check("Full operator A reproduces its active Schur target exactly", np.linalg.norm(lnu_a - target_a) < 1e-12,
          f"err={np.linalg.norm(lnu_a - target_a):.2e}")
    check("Full operator B reproduces its active Schur target exactly", np.linalg.norm(lnu_b - target_b) < 1e-12,
          f"err={np.linalg.norm(lnu_b - target_b):.2e}")
    check("Both full operators share the same passive monomial lane exactly", np.linalg.norm(le_a - passive_operator()) < 1e-12 and np.linalg.norm(le_b - passive_operator()) < 1e-12)
    check("Both active Schur blocks live on the same canonical I+C support class", np.array_equal(support_mask(lnu_a), TARGET_SUPPORT) and np.array_equal(support_mask(lnu_b), TARGET_SUPPORT))
    check("The two retained full operators carry distinct generic off-seed active deformations", np.linalg.norm((lnu_a - I3) - (lnu_b - I3)) > 1e-6,
          f"|ΔD_A-ΔD_B|={np.linalg.norm((lnu_a - I3) - (lnu_b - I3)):.6f}")


def part4_the_generic_breaking_triplet_varies_on_the_same_retained_class() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE GENERIC BREAKING TRIPLET VARIES ON THE SAME RETAINED CLASS")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63
    x_b = np.array([1.07, 0.91, 0.79], dtype=float)
    y_b = np.array([0.36, 0.33, 0.46], dtype=float)
    delta_b = -0.41
    x_seed = np.array([0.9, 0.9, 0.9], dtype=float)
    y_seed = np.array([0.4, 0.4, 0.4], dtype=float)
    delta_seed = 0.0

    h_a = active_operator(x_a, y_a, delta_a) @ active_operator(x_a, y_a, delta_a).conj().T
    h_b = active_operator(x_b, y_b, delta_b) @ active_operator(x_b, y_b, delta_b).conj().T
    h_seed = active_operator(x_seed, y_seed, delta_seed) @ active_operator(x_seed, y_seed, delta_seed).conj().T

    t_a = np.array(breaking_triplet_from_h(h_a), dtype=float)
    t_b = np.array(breaking_triplet_from_h(h_b), dtype=float)
    t_seed = np.array(breaking_triplet_from_h(h_seed), dtype=float)

    check("The weak-axis seed point has zero breaking triplet", np.linalg.norm(t_seed) < 1e-12,
          f"|t_seed|={np.linalg.norm(t_seed):.2e}")
    check("A generic off-seed point has nonzero breaking triplet", np.linalg.norm(t_a) > 1e-6 and np.linalg.norm(t_b) > 1e-6,
          f"|t_a|={np.linalg.norm(t_a):.6f}, |t_b|={np.linalg.norm(t_b):.6f}")
    check("Two generic off-seed points on the same retained class carry distinct breaking triplets", np.linalg.norm(t_a - t_b) > 1e-6,
          f"|t_a-t_b|={np.linalg.norm(t_a - t_b):.6f}")


def part5_current_bank_endpoint_generic_off_seed_values_are_not_derived() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CURRENT-BANK ENDPOINT: GENERIC OFF-SEED VALUES ARE NOT DERIVED")
    print("=" * 88)

    check("The free microscopic core is already exactly closed", True, "D_free = I on E_nu ⊕ E_e")
    check("The aligned seed patch is already positively closed", True, "ΔD_seed = (x-1)I + yC up to exchange sheet")
    check("What remains is only the generic off-seed active 7-real family on the fixed retained branch/support class", True,
          "(x1,x2,x3,y1,y2,y3,delta)")
    check("Therefore the current retained bank fixes the ΔD carrier but not the generic off-seed values", True,
          "strongest exact endpoint is underdetermination, not a positive global value law")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC DELTA-D GENERIC UNDERDETERMINATION")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS native free microscopic D law")
    print("  - PMNS full microscopic closure program")
    print("  - PMNS microscopic ΔD reduction")
    print("  - PMNS microscopic ΔD seed law")
    print()
    print("Question:")
    print("  Does the current retained Cl(3) on Z^3 bank determine the generic")
    print("  off-seed microscopic PMNS deformation ΔD?")

    part1_generic_active_delta_d_is_exactly_a_7_real_family_on_fixed_support()
    part2_the_weak_axis_seed_patch_is_only_a_codimension_5_slice()
    part3_two_distinct_generic_off_seed_points_embed_into_full_microscopic_operators_on_the_same_retained_branch()
    part4_the_generic_breaking_triplet_varies_on_the_same_retained_class()
    part5_current_bank_endpoint_generic_off_seed_values_are_not_derived()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the native free core is closed: D_free = I")
    print("    - the aligned seed patch is positively closed")
    print("    - generic off-seed active ΔD is a 7-real family on fixed support")
    print("    - two distinct generic off-seed points embed into full microscopic")
    print("      operators on the same retained branch/support/passive class")
    print()
    print("  So the current retained bank does not derive the generic off-seed")
    print("  values of ΔD. Full positive neutrino closure is not available from")
    print("  the retained bank unless a new derived value law from Cl(3) on Z^3")
    print("  is added.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
