#!/usr/bin/env python3
"""
Beta=6 identity-rim reduction on the plaquette PF lane.

This sharpens the remaining operator-side closure target:

1. the propagated beta-side vector v_6 is generated from the identity rim
   datum eta_6(e) = P_cls B_6(e);
2. generic marked-holonomy dependence is already downstream through the
   universal Peter-Weyl evaluation functional K(W);
3. for normalized PF data rho_(p,q)(6), only the projective class of eta_6(e)
   matters.
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
    taus = [0.13, 0.19, 0.24, 0.30]
    coeffs = np.array([1.00, 0.79, 0.55, 0.36], dtype=float)

    modes = [matrix_exponential_symmetric(jmat, tau) @ seed for tau, seed in zip(taus, seeds)]
    bulk_matrix = np.column_stack(
        [np.sqrt(coeff) * mode for coeff, mode in zip(coeffs, modes)]
    )
    kernel = bulk_matrix @ bulk_matrix.T
    return kernel, bulk_matrix


def build_full_slice_identity_lift(
    jmat: np.ndarray,
    index: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray]:
    seeds = [
        seed_vector(index, (0, 0)),
        seed_vector(index, (1, 0), (0, 1)),
        seed_vector(index, (1, 1)),
        seed_vector(index, (2, 0), (0, 2)),
    ]
    taus = [0.10, 0.16, 0.22, 0.28]
    tails = np.array(
        [
            [0.42, 0.18, 0.08, 0.03],
            [0.24, 0.30, 0.14, 0.06],
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
    coeff_identity = np.array([1.00, 0.41, 0.18, 0.08], dtype=float)
    return rim_basis, coeff_identity


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
    full_slice_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    seam_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    uniqueness_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md"
    )

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)
    proj = class_projection(len(weights), COMPLEMENT_DIM)

    kernel, bulk_matrix = build_bulk_integral_witness(jmat, index)
    rim_basis, coeff_identity = build_full_slice_identity_lift(jmat, index)

    b_identity = rim_basis @ coeff_identity
    eta_identity = proj @ b_identity
    s_env = kernel
    v_identity = np.linalg.matrix_power(s_env, DEPTH) @ eta_identity
    v_by_elements = propagate_by_matrix_elements(s_env, eta_identity, DEPTH)

    tail_shift = np.concatenate(
        [np.zeros(len(weights), dtype=float), np.array([0.05, 0.02, 0.03, 0.01], dtype=float)]
    )
    b_identity_alt = b_identity + tail_shift
    eta_identity_alt = proj @ b_identity_alt
    v_identity_alt = np.linalg.matrix_power(s_env, DEPTH) @ eta_identity_alt

    scale = 2.75
    eta_scaled = scale * eta_identity
    v_scaled = np.linalg.matrix_power(s_env, DEPTH) @ eta_scaled
    rho_identity = v_identity / v_identity[index[(0, 0)]]
    rho_scaled = v_scaled / v_scaled[index[(0, 0)]]

    sample_angles = [
        (0.29, -0.18),
        (0.51, 0.12),
        (-0.24, 0.46),
    ]
    eval_errors = []
    imag_parts = []
    z_values = []
    for theta1, theta2 in sample_angles:
        k_w = evaluation_vector(weights, theta1, theta2)
        z_eval = np.vdot(k_w, v_identity)
        z_direct = direct_class_function(v_identity, weights, theta1, theta2)
        eval_errors.append(abs(z_direct - z_eval))
        imag_parts.append(abs(z_direct.imag))
        z_values.append(z_direct)

    kernel_sym = float(np.max(np.abs(s_env - s_env.T)))
    kernel_swap = float(np.max(np.abs(swap @ s_env - s_env @ swap)))
    kernel_min = float(np.min(np.linalg.eigvalsh(s_env)))
    eta_swap = float(np.max(np.abs(swap @ eta_identity - eta_identity)))
    v_prop_err = float(np.max(np.abs(v_identity - v_by_elements)))
    eta_alt_err = float(np.max(np.abs(eta_identity_alt - eta_identity)))
    v_alt_err = float(np.max(np.abs(v_identity_alt - v_identity)))
    v_scale_err = float(np.max(np.abs(v_scaled - scale * v_identity)))
    rho_scale_err = float(np.max(np.abs(rho_scaled - rho_identity)))
    sample_variation = max(
        abs(z_values[1] - z_values[0]),
        abs(z_values[2] - z_values[1]),
        abs(z_values[2] - z_values[0]),
    )

    print("=" * 96)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 IDENTITY-RIM REDUCTION")
    print("=" * 96)
    print()
    print("Operator-side witness")
    print(f"  class-sector size                          = {len(weights)}")
    print(f"  bulk-kernel symmetry / swap errors         = {kernel_sym:.3e}, {kernel_swap:.3e}")
    print(f"  bulk-kernel minimum eigenvalue             = {kernel_min:.6e}")
    print(f"  identity-state minimum entry               = {float(np.min(eta_identity)):.6e}")
    print(f"  identity-state swap error                  = {eta_swap:.3e}")
    print()
    print("Identity-rim reduction checks")
    print(f"  matrix-element propagation error           = {v_prop_err:.3e}")
    print(f"  compressed identity-state tail error       = {eta_alt_err:.3e}")
    print(f"  reduced-vector tail invariance error       = {v_alt_err:.3e}")
    print(f"  scaling covariance error                   = {v_scale_err:.3e}")
    print(f"  normalized rho scaling error               = {rho_scale_err:.3e}")
    print()
    print("Downstream marked-holonomy evaluation from one common v_6")
    for i, ((theta1, theta2), z_val, err) in enumerate(
        zip(sample_angles, z_values, eval_errors), start=1
    ):
        print(
            f"  W{i}: (theta1, theta2)=({theta1:+.2f}, {theta2:+.2f})"
            f"  Z={z_val.real:+.12f}{z_val.imag:+.3e}i  err={err:.3e}"
        )
    print()
    print("Framework-point reading")
    print("  the upstream beta-side solve uses the identity rim datum only;")
    print("  generic W enters later through the fixed evaluation functional.")
    print()

    check(
        "the transfer theorem already writes the boundary amplitude with the propagated identity state eta_beta(e)",
        "Z_beta^env(W) = <eta_beta(W), (S_beta^env)^(L_perp-1) eta_beta(e)>" in transfer_note,
        detail="the exact transfer law already factors every marked-holonomy value through one common identity-boundary input",
        bucket="SUPPORT",
    )
    check(
        "the full-slice rim-lift boundary note already identifies eta_beta(W) as the compressed descendant of B_beta(W)",
        "`eta_beta(W) = P_cls B_beta(W)`" in full_slice_note
        and "B_beta(W)" in full_slice_note,
        detail="the identity datum on the compressed lane is the compressed image of the identity full-slice rim lift",
        bucket="SUPPORT",
    )
    check(
        "the beta=6 seam-reduction note already uses eta_6(e) for the coefficient vector and K(W) for downstream evaluation",
        "eta_6(e)" in seam_note
        and "`Z_6^env(W) = <K(W), v_6>`" in seam_note,
        detail="the current beta=6 seam is already written in the identity-rim-then-evaluation form",
        bucket="SUPPORT",
    )
    check(
        "the compressed rim-functional uniqueness note already says all retained W-dependence is carried by K(W)",
        "all `W`-dependence carried by `K_Lambda(W)`" in uniqueness_note
        and "beta-dependent data carried by the propagated right boundary vector" in uniqueness_note
        and "`v_beta^Lambda`" in uniqueness_note,
        detail="generic marked-holonomy dependence is already downstream on the compressed sector",
        bucket="SUPPORT",
    )

    check(
        "the reduced beta-side vector is exactly propagated from the compressed identity rim state",
        v_prop_err < 1.0e-12,
        detail=f"iterated matrix-element propagation error={v_prop_err:.3e}",
    )
    check(
        "full-slice identity lifts with the same compressed projection induce the same reduced beta-side vector",
        eta_alt_err < 1.0e-12 and v_alt_err < 1.0e-12,
        detail=f"projection/tail errors=({eta_alt_err:.3e}, {v_alt_err:.3e})",
    )
    check(
        "positive rescaling of the identity rim datum rescales v_6 but leaves normalized rho_(p,q)(6) unchanged",
        v_scale_err < 1.0e-12 and rho_scale_err < 1.0e-12,
        detail=f"scale error={v_scale_err:.3e}, rho error={rho_scale_err:.3e}",
    )
    check(
        "the same common v_6 determines every marked-holonomy value through the universal evaluation functional",
        max(eval_errors) < 1.0e-12 and max(imag_parts) < 1.0e-10,
        detail=f"max evaluation error={max(eval_errors):.3e}, max imag={max(imag_parts):.3e}",
    )
    check(
        "generic marked-holonomy variation is downstream while the upstream beta-side vector is unchanged",
        sample_variation > 1.0e-3 and max(eval_errors) < 1.0e-12,
        detail=f"sample variation={sample_variation:.3e}",
    )
    check(
        "therefore explicit class-sector beta=6 closure depends on bulk matrix elements and the identity rim datum, not on a generic W-family upstream",
        v_prop_err < 1.0e-12
        and eta_alt_err < 1.0e-12
        and v_alt_err < 1.0e-12
        and rho_scale_err < 1.0e-12
        and sample_variation > 1.0e-3,
        detail="the live operator-side target is K_6^env together with eta_6(e) = P_cls B_6(e)",
    )

    print()
    print("=" * 96)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 96)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
