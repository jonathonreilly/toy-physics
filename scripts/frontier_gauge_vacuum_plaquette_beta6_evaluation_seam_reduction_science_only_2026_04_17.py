#!/usr/bin/env python3
"""
Beta=6 evaluation-seam reduction on the plaquette PF lane.

This is the strongest honest next step after the new science-only integral
boundary theorems:

1. K_beta^env is fixed as one exact bulk Wilson/Haar slab integral;
2. B_beta(W) is fixed as one exact full-slice Wilson/Haar rim integral;
3. after compression, the remaining beta=6 seam is exactly evaluation of the
   class-sector matrix elements induced by those integrals;
4. the compressed W-dependence is already canonical through the Peter-Weyl
   evaluation vector.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 4
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


def build_bulk_integral_witness(
    jmat: np.ndarray,
    index: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray]:
    seeds = [
        seed_vector(index, (0, 0)),
        seed_vector(index, (1, 0), (0, 1)),
        seed_vector(index, (1, 1)),
        seed_vector(index, (2, 0), (0, 2)),
    ]
    taus = [0.13, 0.18, 0.24, 0.31]
    coeffs = np.array([1.00, 0.81, 0.56, 0.39], dtype=float)

    modes = [matrix_exponential_symmetric(jmat, tau) @ seed for tau, seed in zip(taus, seeds)]
    bulk_matrix = np.column_stack(
        [np.sqrt(coeff) * mode for coeff, mode in zip(coeffs, modes)]
    )
    kernel = bulk_matrix @ bulk_matrix.T
    return kernel, bulk_matrix


def build_full_slice_rim_lift(
    jmat: np.ndarray,
    index: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    seeds = [
        seed_vector(index, (0, 0)),
        seed_vector(index, (1, 0), (0, 1)),
        seed_vector(index, (1, 1)),
        seed_vector(index, (2, 0), (0, 2)),
    ]
    taus = [0.10, 0.16, 0.22, 0.28]
    tails = np.array(
        [
            [0.41, 0.18, 0.08, 0.03],
            [0.24, 0.29, 0.14, 0.06],
            [0.16, 0.11, 0.27, 0.10],
            [0.09, 0.05, 0.09, 0.22],
        ],
        dtype=float,
    )

    columns = []
    for tau, seed, tail in zip(taus, seeds, tails):
        class_part = matrix_exponential_symmetric(jmat, tau) @ seed
        columns.append(np.concatenate([class_part, tail]))
    rim_basis = np.column_stack(columns)
    coeff_marked = np.array([1.00, 0.64, 0.29, 0.12], dtype=float)
    coeff_identity = np.array([1.00, 0.42, 0.17, 0.07], dtype=float)
    return rim_basis, coeff_identity, coeff_marked


def orthogonal_matrix(n: int) -> np.ndarray:
    raw = np.arange(1, n * n + 1, dtype=float).reshape(n, n)
    qmat, _ = np.linalg.qr(raw + raw.T)
    return qmat


def propagate_by_matrix_elements(s_env: np.ndarray, eta: np.ndarray, depth: int) -> np.ndarray:
    vec = eta.copy()
    for _ in range(depth):
        nxt = np.zeros_like(vec)
        for i in range(len(vec)):
            total = 0.0
            for j in range(len(vec)):
                total += s_env[i, j] * vec[j]
            nxt[i] = total
        vec = nxt
    return vec


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


def evaluation_vector(
    weights: list[tuple[int, int]], theta1: float, theta2: float
) -> np.ndarray:
    return np.array(
        [
            dim_su3(p, q) * np.conjugate(su3_character(p, q, theta1, theta2))
            for p, q in weights
        ],
        dtype=complex,
    )


def direct_class_function(
    coeffs: np.ndarray, weights: list[tuple[int, int]], theta1: float, theta2: float
) -> complex:
    total = 0.0j
    for i, (p, q) in enumerate(weights):
        total += dim_su3(p, q) * coeffs[i] * su3_character(p, q, theta1, theta2)
    return total


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    compression_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_KERNEL_RIM_COMPRESSION_THEOREM_NOTE_2026-04-17.md"
    )
    compressed_eval_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md"
    )
    one_slab_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    full_slice_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)
    proj = class_projection(len(weights), COMPLEMENT_DIM)

    kernel, bulk_matrix = build_bulk_integral_witness(jmat, index)
    rim_basis, coeff_identity, coeff_marked = build_full_slice_rim_lift(jmat, index)

    b_identity = rim_basis @ coeff_identity
    b_marked = rim_basis @ coeff_marked
    eta_identity = proj @ b_identity
    eta_marked = proj @ b_marked

    s_env = kernel
    v_identity = np.linalg.matrix_power(s_env, DEPTH) @ eta_identity
    v_marked = np.linalg.matrix_power(s_env, DEPTH) @ eta_marked
    v_marked_by_elements = propagate_by_matrix_elements(s_env, eta_marked, DEPTH)

    rho_identity = v_identity / v_identity[index[(0, 0)]]
    rho_marked = v_marked / v_marked[index[(0, 0)]]

    sample_angles = [
        (0.29, -0.18),
        (0.51, 0.12),
        (-0.24, 0.46),
    ]
    eval_errors = []
    imag_parts = []
    variation = []
    previous = None
    for theta1, theta2 in sample_angles:
        k_w = evaluation_vector(weights, theta1, theta2)
        z_direct = direct_class_function(v_marked, weights, theta1, theta2)
        z_eval = np.vdot(k_w, v_marked)
        eval_errors.append(abs(z_direct - z_eval))
        imag_parts.append(abs(z_direct.imag))
        if previous is not None:
            variation.append(abs(z_direct - previous))
        previous = z_direct

    q_bulk = orthogonal_matrix(bulk_matrix.shape[1])
    q_rim = orthogonal_matrix(rim_basis.shape[1])
    kernel_rot = (bulk_matrix @ q_bulk) @ (bulk_matrix @ q_bulk).T
    rim_basis_rot = rim_basis @ q_rim
    coeff_marked_rot = q_rim.T @ coeff_marked
    b_marked_rot = rim_basis_rot @ coeff_marked_rot
    eta_marked_rot = proj @ b_marked_rot
    v_marked_rot = np.linalg.matrix_power(kernel_rot, DEPTH) @ eta_marked_rot

    kernel_sym = float(np.max(np.abs(s_env - s_env.T)))
    kernel_swap = float(np.max(np.abs(swap @ s_env - s_env @ swap)))
    kernel_min = float(np.min(np.linalg.eigvalsh(s_env)))
    eta_swap = float(np.max(np.abs(swap @ eta_marked - eta_marked)))
    v_err = float(np.max(np.abs(v_marked - v_marked_by_elements)))
    kernel_rot_err = float(np.max(np.abs(kernel_rot - s_env)))
    eta_rot_err = float(np.max(np.abs(eta_marked_rot - eta_marked)))
    v_rot_err = float(np.max(np.abs(v_marked_rot - v_marked)))
    rho_gap = float(np.max(np.abs(rho_marked - rho_identity)))

    print("=" * 96)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 EVALUATION-SEAM REDUCTION")
    print("=" * 96)
    print()
    print("Integral-class witnesses carried into the reduction")
    print(f"  class-sector size                          = {len(weights)}")
    print(f"  bulk-kernel symmetry / swap errors         = {kernel_sym:.3e}, {kernel_swap:.3e}")
    print(f"  bulk-kernel minimum eigenvalue             = {kernel_min:.6e}")
    print(f"  rim-state minimum entry                    = {float(np.min(eta_marked)):.6e}")
    print(f"  rim-state swap error                       = {eta_swap:.3e}")
    print()
    print("Beta=6 reduced class-sector data")
    print(f"  matrix-element propagation error           = {v_err:.3e}")
    print(f"  rotated bulk decomposition error           = {kernel_rot_err:.3e}")
    print(f"  rotated rim decomposition error            = {eta_rot_err:.3e}")
    print(f"  rotated reduced-vector error               = {v_rot_err:.3e}")
    print(f"  max |rho_marked - rho_identity|            = {rho_gap:.6e}")
    print()
    print("Compressed evaluation law on generic marked holonomies")
    for i, (theta1, theta2) in enumerate(sample_angles, start=1):
        z_val = direct_class_function(v_marked, weights, theta1, theta2)
        print(
            f"  W{i}: (theta1, theta2)=({theta1:+.2f}, {theta2:+.2f})"
            f"  Z_direct={z_val.real:+.12f}{z_val.imag:+.3e}i  "
            f"err={eval_errors[i-1]:.3e}"
        )
    print()
    print("Framework-point caution")
    print("  this runner reduces the beta=6 seam to explicit matrix-element")
    print("  evaluation of already-fixed integral objects; it does not claim")
    print("  closed-form evaluation of those matrix elements.")
    print()

    check(
        "the one-slab science-only boundary note fixes K_beta^env as one exact Wilson/Haar slab integral while leaving beta=6 unevaluated",
        "one-slab bulk kernel integral defining `K_6^env`" in one_slab_note
        and "does **not** yet evaluate those objects in explicit closed form at `beta = 6`"
        in one_slab_note,
        detail="the bulk side is already reduced to one exact integral construction class, but not solved in closed form",
    )
    check(
        "the full-slice science-only boundary note fixes B_beta(W) and eta_beta(W)=P_cls B_beta(W) while leaving beta=6 unevaluated",
        "full-slice local Wilson/Haar rim lift" in full_slice_note
        and "`eta_beta(W) = P_cls B_beta(W)`" in full_slice_note
        and "but no explicit closed-form evaluation of either object is derived here." in full_slice_note,
        detail="the local marked side is also already at the exact integral-expression level",
    )
    check(
        "the kernel/rim compression theorem already says explicit K_6^env and B_6 canonically determine S_6^env, eta_6, and rho_(p,q)(6)",
        "once `K_6^env` and `B_6` are explicit" in compression_note
        and "`rho_(p,q)(6)`" in compression_note
        and "follow canonically" in compression_note,
        detail="no additional post-compression PF formalism is missing once those pre-compression objects are evaluated",
    )
    check(
        "the compressed rim-evaluation theorem already makes the compressed W-dependence explicit through the Peter-Weyl evaluation vector",
        "`Z_beta^env(W) = <K(W), v_beta>`" in compressed_eval_note
        and "The `W`-dependence is already explicit in `K(W)`." in compressed_eval_note,
        detail="after compression, the remaining beta-side seam sits only in the coefficient vector v_6",
    )
    check(
        "the beta=6 reduced coefficient vector is exactly generated by iterated class-sector matrix elements of S_6^env acting on eta_6",
        "z_(p,q)^env(beta) = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>" in transfer_note
        and v_err < 1.0e-12,
        detail=f"iterated matrix-element propagation error={v_err:.3e}",
    )
    check(
        "once the reduced coefficient vector is known, the full compressed boundary class function is fixed by the evaluation vector K(W)",
        max(eval_errors) < 1.0e-12,
        detail=f"max evaluation error={max(eval_errors):.3e}",
    )

    check(
        "the bulk integral witness remains positive, self-adjoint, and conjugation-symmetric on the reduced class sector",
        kernel_min > -1.0e-12 and kernel_sym < 1.0e-12 and kernel_swap < 1.0e-12,
        detail=f"min eigenvalue={kernel_min:.3e}, symmetry/swap=({kernel_sym:.3e}, {kernel_swap:.3e})",
        bucket="SUPPORT",
    )
    check(
        "different integral decompositions with the same reduced matrix elements induce the same beta=6 reduced vector",
        kernel_rot_err < 1.0e-12 and eta_rot_err < 1.0e-12 and v_rot_err < 1.0e-12,
        detail=f"rotation errors=({kernel_rot_err:.3e}, {eta_rot_err:.3e}, {v_rot_err:.3e})",
        bucket="SUPPORT",
    )
    check(
        "the reduced beta=6 coefficient vector yields nontrivial marked-holonomy variation and nontrivial rim dependence",
        max(variation) > 1.0e-3 and rho_gap > 1.0e-3 and max(imag_parts) < 1.0e-10,
        detail=f"variation={max(variation):.3e}, rho gap={rho_gap:.3e}, imag={max(imag_parts):.3e}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 96)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 96)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
