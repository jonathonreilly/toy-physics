#!/usr/bin/env python3
"""
First three-sample environment evaluator route on the plaquette PF lane.

This sharpens the current beta=6 three-sample seam in the strongest honest way
supported by the existing exact stack:

1. the compressed-sector evaluator route for Z_6^env(W_A), Z_6^env(W_B),
   Z_6^env(W_C) factors through one common propagated beta-side vector;
2. the left sample operator is already fixed and unique, and on the first
   symmetric witness sector it is exactly the radical matrix F;
3. the current exact stack still does not determine that common beta-side
   vector, so it does not yet furnish an actual evaluator for the three
   sample values.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
DEPTH = 3


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def sample_angle_units() -> dict[str, tuple[int, int]]:
    return {
        "W_A": (-13, 10),
        "W_B": (-5, -7),
        "W_C": (7, -11),
    }


def recurrence_neighbors(p: int, q: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for a, b in [
        (p + 1, q),
        (p - 1, q + 1),
        (p, q - 1),
        (p, q + 1),
        (p + 1, q - 1),
        (p - 1, q),
    ]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_recurrence_matrix(
    nmax: int,
) -> tuple[np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    jmat = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                jmat[index[(a, b)], i] += 1.0 / 6.0
    return jmat, weights, index


def conjugation_swap_matrix(
    weights: list[tuple[int, int]], index: dict[tuple[int, int], int]
) -> np.ndarray:
    swap = np.zeros((len(weights), len(weights)), dtype=float)
    for w in weights:
        swap[index[(w[1], w[0])], index[w]] = 1.0
    return swap


def matrix_exponential_symmetric(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def spatial_pair(
    jmat: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    tau_transfer: float,
    tau_boundary: float,
    linear_decay: float,
    asym_decay: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    layer_diag = np.diag(
        [np.exp(-linear_decay * (p + q) - asym_decay * ((p - q) ** 2)) for p, q in weights]
    )
    exp_transfer = matrix_exponential_symmetric(jmat, tau_transfer)
    transfer = exp_transfer @ layer_diag @ exp_transfer

    eta0 = np.zeros(len(weights), dtype=float)
    eta0[index[(0, 0)]] = 1.0
    boundary = matrix_exponential_symmetric(jmat, tau_boundary) @ eta0
    amplitude = np.linalg.matrix_power(transfer, DEPTH) @ boundary
    rho = amplitude / amplitude[index[(0, 0)]]
    return transfer, boundary, amplitude, rho


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = np.array(
        [
            np.exp(1j * theta1),
            np.exp(1j * theta2),
            np.exp(-1j * (theta1 + theta2)),
        ],
        dtype=complex,
    )
    lam = [p + q, q, 0]
    num = np.array(
        [[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    den = np.array(
        [[x[i] ** (2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    return complex(np.linalg.det(num) / np.linalg.det(den))


def sample_operator(weights: list[tuple[int, int]]) -> np.ndarray:
    rows: list[np.ndarray] = []
    for theta1_units, theta2_units in sample_angle_units().values():
        theta1 = theta1_units * np.pi / 16.0
        theta2 = theta2_units * np.pi / 16.0
        rows.append(
            np.array(
                [
                    dim_su3(p, q) * su3_character(p, q, theta1, theta2)
                    for p, q in weights
                ],
                dtype=complex,
            )
        )
    return np.vstack(rows)


def first_symmetric_basis(
    nweights: int, index: dict[tuple[int, int], int]
) -> np.ndarray:
    basis = np.zeros((nweights, 3), dtype=float)
    basis[index[(0, 0)], 0] = 1.0
    basis[index[(1, 0)], 1] = 1.0
    basis[index[(0, 1)], 1] = 1.0
    basis[index[(1, 1)], 2] = 1.0
    return basis


def exact_first_symmetric_matrix() -> sp.Matrix:
    pi = sp.pi
    rows: list[list[sp.Expr]] = []
    for theta1_units, theta2_units in sample_angle_units().values():
        theta1 = theta1_units * pi / 16
        theta2 = theta2_units * pi / 16
        rows.append(
            [
                sp.Integer(1),
                sp.simplify(6 * (sp.cos(theta1) + sp.cos(theta2) + sp.cos(theta1 + theta2))),
                sp.simplify(
                    16
                    * (
                        1
                        + sp.cos(theta1 - theta2)
                        + sp.cos(2 * theta1 + theta2)
                        + sp.cos(theta1 + 2 * theta2)
                    )
                ),
            ]
        )
    return sp.Matrix(rows)


def format_triple(values: np.ndarray) -> str:
    names = list(sample_angle_units())
    return ", ".join(
        f"{name}={float(np.real_if_close(values[i]).real):.12f}" for i, name in enumerate(names)
    )


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    eval_reduction_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    uniqueness_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md"
    )
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    current_stack_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CURRENT_STACK_CONSTRAINT_BOUNDARY_NOTE_2026-04-17.md"
    )
    underdetermination_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_UNDERDETERMINATION_NOTE_2026-04-17.md"
    )
    local_obstruction_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md"
    )

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)
    e_three = sample_operator(weights)
    basis = first_symmetric_basis(len(weights), index)
    reduced_matrix = e_three @ basis
    exact_f = exact_first_symmetric_matrix()
    exact_f_numeric = np.array(exact_f.evalf(50), dtype=np.complex128)
    reduced_matrix_error = float(np.max(np.abs(reduced_matrix - exact_f_numeric)))
    reduced_rank = int(np.linalg.matrix_rank(exact_f_numeric))

    s_a, eta_a, amp_a, rho_a = spatial_pair(
        jmat, weights, index, tau_transfer=0.32, tau_boundary=0.14, linear_decay=0.18, asym_decay=0.05
    )
    s_b, eta_b, amp_b, rho_b = spatial_pair(
        jmat, weights, index, tau_transfer=0.24, tau_boundary=0.22, linear_decay=0.13, asym_decay=0.09
    )

    s_a_sym = float(np.max(np.abs(s_a - s_a.T)))
    s_b_sym = float(np.max(np.abs(s_b - s_b.T)))
    s_a_swap = float(np.max(np.abs(swap @ s_a - s_a @ swap)))
    s_b_swap = float(np.max(np.abs(swap @ s_b - s_b @ swap)))
    eta_a_swap = float(np.max(np.abs(swap @ eta_a - eta_a)))
    eta_b_swap = float(np.max(np.abs(swap @ eta_b - eta_b)))
    rho_a_swap = float(np.max(np.abs(swap @ rho_a - rho_a)))
    rho_b_swap = float(np.max(np.abs(swap @ rho_b - rho_b)))
    rho_gap = float(np.max(np.abs(rho_a - rho_b)))
    rho00_a = float(rho_a[index[(0, 0)]])
    rho00_b = float(rho_b[index[(0, 0)]])

    zhat_a = e_three @ rho_a
    zhat_b = e_three @ rho_b
    triple_gap = float(np.max(np.abs(zhat_a - zhat_b)))
    imag_gap = float(
        max(
            np.max(np.abs(np.imag(zhat_a))),
            np.max(np.abs(np.imag(zhat_b))),
        )
    )
    min_real_a = float(np.min(np.real_if_close(zhat_a).real))
    min_real_b = float(np.min(np.real_if_close(zhat_b).real))

    rng = np.random.default_rng(1729)
    trial_vector = np.abs(rng.normal(size=len(weights)))
    direct_errors: list[float] = []
    for row, (theta1_units, theta2_units) in zip(e_three, sample_angle_units().values()):
        theta1 = theta1_units * np.pi / 16.0
        theta2 = theta2_units * np.pi / 16.0
        direct = 0.0j
        for coeff, (p, q) in zip(trial_vector, weights):
            direct += dim_su3(p, q) * coeff * su3_character(p, q, theta1, theta2)
        direct_errors.append(abs(row @ trial_vector - direct))

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FIRST THREE-SAMPLE ENVIRONMENT EVALUATOR ROUTE")
    print("=" * 104)
    print()
    print("Exact first symmetric restriction of the universal three-sample operator")
    print(exact_f)
    print()
    print(f"  rank(F)                                     = {reduced_rank}")
    print(f"  max restriction error                       = {reduced_matrix_error:.3e}")
    print()
    print("Two admissible normalized beta-side witnesses on the current structural surface")
    print(f"  S_A symmetry / swap errors                  = {s_a_sym:.3e}, {s_a_swap:.3e}")
    print(f"  S_B symmetry / swap errors                  = {s_b_sym:.3e}, {s_b_swap:.3e}")
    print(f"  eta_A / eta_B swap errors                   = {eta_a_swap:.3e}, {eta_b_swap:.3e}")
    print(f"  rho_A / rho_B swap errors                   = {rho_a_swap:.3e}, {rho_b_swap:.3e}")
    print(f"  rho_A(0,0), rho_B(0,0)                      = {rho00_a:.12f}, {rho00_b:.12f}")
    print(f"  max |rho_A-rho_B|                           = {rho_gap:.12f}")
    print()
    print("Induced normalized three-sample values under the same universal left operator")
    print(f"  Zhat_A                                      = {format_triple(zhat_a)}")
    print(f"  Zhat_B                                      = {format_triple(zhat_b)}")
    print(f"  max |Zhat_A-Zhat_B|                         = {triple_gap:.12f}")
    print(f"  max imaginary residue                       = {imag_gap:.3e}")
    print()

    check(
        "the transfer and beta=6 seam-reduction notes already factor the compressed route through one propagated beta-side vector built from the identity boundary state",
        "Z_beta^env(W) = <eta_beta(W), (S_beta^env)^(L_perp-1) eta_beta(e)>" in transfer_note
        and "z_(p,q)^env(6)" in eval_reduction_note
        and "eta_6(e)" in eval_reduction_note
        and "v_6 = sum_(p,q) z_(p,q)^env(6) chi_(p,q)" in eval_reduction_note,
        detail="the right-hand beta-side datum is common across all three sample points",
        bucket="SUPPORT",
    )
    check(
        "the compressed rim-functional uniqueness note already fixes the left boundary functional as the unique universal Peter-Weyl evaluation functional",
        "universal Peter-Weyl evaluation functional" in uniqueness_note
        and "the retained left boundary functional is unique" in uniqueness_note,
        detail="sample dependence is already fixed on the left side before any beta=6 environment evaluation",
        bucket="SUPPORT",
    )
    check(
        "the exact radical three-sample map and current-stack constraint notes already fix the first symmetric sample operator and show it does not collapse below three",
        "exact radical-form three-sample matrix" in radical_note
        and "there is no further universal linear collapse below" in radical_note
        and "the first retained three-sample `beta = 6` seam remains exactly" in current_stack_note,
        detail="the first witness-sector route is already explicit and irreducible",
        bucket="SUPPORT",
    )
    check(
        "the spatial-environment underdetermination note already records that the current stack does not force unique explicit beta=6 environment data",
        "the current exact stack still does **not** determine unique explicit" in underdetermination_note
        or "the current exact stack still does **not** determine unique explicit `beta = 6` spatial-environment data." in underdetermination_note,
        detail="the current lane still leaves the beta-side vector open",
        bucket="SUPPORT",
    )
    check(
        "the local-Wilson obstruction note already rules out the strongest obvious local shortcut on the three-sample seam",
        "cannot itself be the first symmetric positive-type environment evaluator" in local_obstruction_note,
        detail="the unresolved route cannot be closed by reusing the local Wilson triple alone",
        bucket="SUPPORT",
    )

    check(
        "the universal three-sample operator restricts exactly to the radical first symmetric matrix F",
        reduced_rank == 3 and reduced_matrix_error < 1.0e-12,
        detail=f"rank(F)={reduced_rank}, max restriction error={reduced_matrix_error:.3e}",
    )
    check(
        "the explicit row-operator implementation reproduces direct character evaluation on a generic class-sector test vector",
        max(direct_errors) < 1.0e-11,
        detail=f"max direct-evaluation error={max(direct_errors):.3e}",
    )
    check(
        "the current structural surface admits distinct positive self-adjoint conjugation-symmetric beta-side witnesses",
        s_a_sym < 1.0e-12
        and s_b_sym < 1.0e-12
        and s_a_swap < 1.0e-12
        and s_b_swap < 1.0e-12
        and float(np.min(np.linalg.eigvalsh(s_a))) > 0.0
        and float(np.min(np.linalg.eigvalsh(s_b))) > 0.0
        and eta_a_swap < 1.0e-12
        and eta_b_swap < 1.0e-12
        and rho_a_swap < 1.0e-12
        and rho_b_swap < 1.0e-12
        and abs(rho00_a - 1.0) < 1.0e-12
        and abs(rho00_b - 1.0) < 1.0e-12,
        detail=f"rho-gap={rho_gap:.3e} on the same exact structural surface",
    )
    check(
        "the same universal left operator sends those two admissible normalized beta-side vectors to different normalized three-sample triples",
        rho_gap > 1.0e-3
        and triple_gap > 1.0e-2
        and imag_gap < 1.0e-10
        and min_real_a > 0.0
        and min_real_b > 0.0,
        detail=f"Zhat_A=({format_triple(zhat_a)}); Zhat_B=({format_triple(zhat_b)})",
    )
    check(
        "therefore the current exact stack does not yet furnish an actual evaluator for Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C): even the normalized triple is still not unique",
        reduced_rank == 3 and rho_gap > 1.0e-3 and triple_gap > 1.0e-2,
        detail="the real route is one common beta-side vector hit by a fixed three-row operator, and that beta-side vector is still not determined",
    )

    print()
    print("=" * 104)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 104)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
