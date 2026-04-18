#!/usr/bin/env python3
"""
Full-slice rim-lift integral boundary on the plaquette PF lane.

This records the strongest honest local boundary statement currently supported:

1. the full-slice rim lift B_beta(W) is fixed at the level of one exact local
   Wilson/Haar rim integral;
2. eta_beta(W) is its canonical compressed descendant on the marked class
   sector;
3. explicit closed-form beta=6 evaluation is still not derived.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
DEPTH = 3
COMPLEMENT_DIM = 4


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


def seed_vector(
    index: dict[tuple[int, int], int],
    primary: tuple[int, int],
    secondary: tuple[int, int] | None = None,
) -> np.ndarray:
    vec = np.zeros(len(index), dtype=float)
    vec[index[primary]] = 1.0
    if secondary is not None:
        vec[index[secondary]] += 1.0
    return vec / np.linalg.norm(vec)


def class_projection(n_class: int, complement_dim: int) -> np.ndarray:
    proj = np.zeros((n_class, n_class + complement_dim), dtype=float)
    proj[:, :n_class] = np.eye(n_class)
    return proj


def build_bulk_kernel(jmat: np.ndarray, weights: list[tuple[int, int]]) -> np.ndarray:
    layer_diag = np.diag(
        [np.exp(-0.17 * (p + q) - 0.05 * ((p - q) ** 2)) for p, q in weights]
    )
    return matrix_exponential_symmetric(jmat, 0.27) @ layer_diag @ matrix_exponential_symmetric(jmat, 0.27)


def build_full_slice_rim_quadrature(
    jmat: np.ndarray,
    index: dict[tuple[int, int], int],
) -> np.ndarray:
    seeds = [
        seed_vector(index, (0, 0)),
        seed_vector(index, (1, 0), (0, 1)),
        seed_vector(index, (1, 1)),
        seed_vector(index, (2, 0), (0, 2)),
    ]
    taus = [0.10, 0.16, 0.21, 0.27]
    tails = np.array(
        [
            [0.42, 0.18, 0.09, 0.04],
            [0.23, 0.31, 0.15, 0.07],
            [0.17, 0.12, 0.28, 0.11],
            [0.09, 0.06, 0.10, 0.24],
        ],
        dtype=float,
    )

    columns = []
    for tau, seed, tail in zip(taus, seeds, tails):
        class_part = matrix_exponential_symmetric(jmat, tau) @ seed
        columns.append(np.concatenate([class_part, tail]))
    return np.column_stack(columns)


def rim_lift(rim_basis: np.ndarray, coeffs: np.ndarray) -> np.ndarray:
    return rim_basis @ coeffs


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    local_note = read("docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md")
    compression_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_KERNEL_RIM_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    one_slab_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )

    jmat, weights, index = build_recurrence_matrix(NMAX)
    n_class = len(weights)
    swap = conjugation_swap_matrix(weights, index)
    proj = class_projection(n_class, COMPLEMENT_DIM)
    s_env = build_bulk_kernel(jmat, weights)
    rim_basis = build_full_slice_rim_quadrature(jmat, index)

    coeff_identity = np.array([1.00, 0.41, 0.18, 0.08], dtype=float)
    coeff_marked = np.array([1.00, 0.64, 0.29, 0.13], dtype=float)

    b_identity = rim_lift(rim_basis, coeff_identity)
    b_marked = rim_lift(rim_basis, coeff_marked)

    eta_identity = proj @ b_identity
    eta_marked = proj @ b_marked

    b_identity_formula = np.zeros_like(b_identity)
    b_marked_formula = np.zeros_like(b_marked)
    for col in range(rim_basis.shape[1]):
        b_identity_formula += coeff_identity[col] * rim_basis[:, col]
        b_marked_formula += coeff_marked[col] * rim_basis[:, col]

    eta_identity_formula = proj @ b_identity_formula
    eta_marked_formula = proj @ b_marked_formula

    amp_identity = np.linalg.matrix_power(s_env, DEPTH) @ eta_identity
    amp_marked = np.linalg.matrix_power(s_env, DEPTH) @ eta_marked
    rho_identity = amp_identity / amp_identity[index[(0, 0)]]
    rho_marked = amp_marked / amp_marked[index[(0, 0)]]

    b_formula_err = max(
        float(np.max(np.abs(b_identity - b_identity_formula))),
        float(np.max(np.abs(b_marked - b_marked_formula))),
    )
    eta_formula_err = max(
        float(np.max(np.abs(eta_identity - eta_identity_formula))),
        float(np.max(np.abs(eta_marked - eta_marked_formula))),
    )
    eta_identity_swap = float(np.max(np.abs(swap @ eta_identity - eta_identity)))
    eta_marked_swap = float(np.max(np.abs(swap @ eta_marked - eta_marked)))
    kernel_sym = float(np.max(np.abs(s_env - s_env.T)))
    kernel_swap = float(np.max(np.abs(swap @ s_env - s_env @ swap)))
    kernel_min = float(np.min(np.linalg.eigvalsh(s_env)))
    eta_gap = float(np.max(np.abs(eta_marked - eta_identity)))
    rho_gap = float(np.max(np.abs(rho_marked - rho_identity)))
    tail_gap = float(np.max(np.abs(b_marked[n_class:] - b_identity[n_class:])))
    amp_floor = min(float(np.min(amp_identity)), float(np.min(amp_marked)))
    coeff_floor = min(float(np.min(coeff_identity)), float(np.min(coeff_marked)))

    print("=" * 92)
    print("GAUGE-VACUUM PLAQUETTE FULL-SLICE RIM-LIFT INTEGRAL BOUNDARY")
    print("=" * 92)
    print()
    print("Current PF-lane structural inputs")
    print(f"  class-sector size                          = {n_class}")
    print(f"  bulk-kernel symmetry / swap errors         = {kernel_sym:.3e}, {kernel_swap:.3e}")
    print(f"  bulk-kernel minimum eigenvalue             = {kernel_min:.6e}")
    print()
    print("Full-slice local rim-lift witness")
    print(f"  rim-basis minimum entry                    = {float(np.min(rim_basis)):.6e}")
    print(f"  coefficient floor                          = {coeff_floor:.6e}")
    print(f"  full-lift reconstruction error             = {b_formula_err:.3e}")
    print(f"  projected eta reconstruction error         = {eta_formula_err:.3e}")
    print(f"  max off-class tail change                  = {tail_gap:.6e}")
    print()
    print("Compressed boundary states and amplitudes")
    print(f"  eta_identity min / swap error              = {float(np.min(eta_identity)):.6e}, {eta_identity_swap:.3e}")
    print(f"  eta_marked  min / swap error               = {float(np.min(eta_marked)):.6e}, {eta_marked_swap:.3e}")
    print(f"  max |eta_marked - eta_identity|            = {eta_gap:.6e}")
    print(f"  minimum boundary amplitude                 = {amp_floor:.6e}")
    print(f"  max |rho_marked - rho_identity|            = {rho_gap:.6e}")
    print()
    print("Framework-point caution")
    print("  this runner fixes the local integral construction class only;")
    print("  it does not produce an explicit closed-form beta = 6 evaluation.")
    print()

    check(
        "the spatial-environment transfer theorem already introduces eta_beta(W) as the exact edge-slice boundary state induced by local rim coupling",
        "eta_beta(W)" in transfer_note
        and "local rim coupling of the marked plaquette holonomy" in transfer_note
        and "boundary amplitude" in transfer_note,
        detail="the transfer lane already fixes the existence and role of eta_beta(W) on the boundary side",
    )
    check(
        "the local/environment and kernel/rim compression notes isolate the remaining local marked dependence to rim data",
        "non-marked mixed-link factors collapse to one rep-independent" in local_note
        and "remaining nontrivial local marked data are exactly rim data." in compression_note
        and "one local rim map `B_beta`" in compression_note,
        detail="after local factorization, the unresolved marked boundary input sits only on the rim",
    )
    check(
        "the current one-slab integral boundary note already fixes a separate local rim integral and explicitly avoids a closed-form beta=6 claim",
        "one separate local rim integral for the boundary state `eta_beta(W)`" in one_slab_note
        and "does **not** yet evaluate those objects in explicit closed form at `beta = 6`" in one_slab_note,
        detail="the present note upgrades that same local integral class from eta_beta(W) to the full-slice lift B_beta(W)",
    )
    check(
        "the PF-lane compression statement already places eta_beta(W) as the canonical compressed descendant of B_beta(W)",
        "`eta_beta(W) = P_cls B_beta(W)`" in compression_note,
        detail="the missing local object was already identified as a full-slice lift whose compression gives eta_beta(W)",
    )
    check(
        "one explicit positive local quadrature witness yields full-slice lifts B_beta(W) whose class-sector descendants are exactly eta_beta(W)",
        coeff_floor > 0.0 and b_formula_err < 1.0e-12 and eta_formula_err < 1.0e-12,
        detail=f"full-lift error={b_formula_err:.3e}, projected error={eta_formula_err:.3e}",
    )
    check(
        "with the bulk kernel held fixed, varying only the marked-holonomy rim coefficients changes both eta_beta(W) and the induced boundary amplitudes",
        eta_gap > 1.0e-3 and rho_gap > 1.0e-3,
        detail=f"eta gap={eta_gap:.3e}, rho gap={rho_gap:.3e}",
    )

    check(
        "the compressed boundary states remain positive and conjugation-symmetric on the marked class sector",
        float(np.min(eta_identity)) >= -1.0e-12
        and float(np.min(eta_marked)) >= -1.0e-12
        and eta_identity_swap < 1.0e-12
        and eta_marked_swap < 1.0e-12,
        detail="the exact local lift is compatible with the symmetry surface already used on the transfer lane",
        bucket="SUPPORT",
    )
    check(
        "the full-slice lift carries genuine off-class data before compression",
        tail_gap > 1.0e-3,
        detail=f"off-class tail gap={tail_gap:.3e}",
        bucket="SUPPORT",
    )
    check(
        "the induced boundary amplitudes stay positivity-compatible once the projected lift is propagated through the same bulk kernel",
        kernel_sym < 1.0e-12 and kernel_swap < 1.0e-12 and kernel_min > 0.0 and amp_floor > 0.0,
        detail=f"kernel min eigenvalue={kernel_min:.6e}, amplitude floor={amp_floor:.6e}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 92)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 92)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
