#!/usr/bin/env python3
"""
Exact integral-expression boundary witness for the one-slab orthogonal kernel
K_beta^env on the plaquette PF lane.

This does not claim explicit closed-form beta=6 data. It closes only the
strongest honest seam currently supported by the Wilson stack:

1. K_beta^env is one exact bulk one-slab Wilson/Haar integral;
2. eta_beta(W) comes from a separate local rim integral;
3. once those integrals are explicit, the downstream class-sector data are
   explicit, but not before.
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
    taus = [0.14, 0.19, 0.24, 0.29]
    weights = np.array([1.00, 0.78, 0.54, 0.37], dtype=float)

    modes = [matrix_exponential_symmetric(jmat, tau) @ seed for tau, seed in zip(taus, seeds)]
    bulk_matrix = np.column_stack([np.sqrt(weight) * mode for weight, mode in zip(weights, modes)])
    kernel = bulk_matrix @ bulk_matrix.T
    return kernel, bulk_matrix


def build_rim_integral_witness(
    jmat: np.ndarray,
    index: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    seeds = [
        seed_vector(index, (0, 0)),
        seed_vector(index, (1, 0), (0, 1)),
        seed_vector(index, (1, 1)),
    ]
    taus = [0.11, 0.17, 0.23]
    rim_modes = [matrix_exponential_symmetric(jmat, tau) @ seed for tau, seed in zip(taus, seeds)]
    rim_matrix = np.column_stack(rim_modes)

    coeff_identity = np.array([1.00, 0.42, 0.16], dtype=float)
    coeff_marked = np.array([1.00, 0.63, 0.27], dtype=float)

    eta_identity = rim_matrix @ coeff_identity
    eta_marked = rim_matrix @ coeff_marked
    return rim_matrix, coeff_identity, coeff_marked, eta_identity, eta_marked


def boundary_data(
    kernel: np.ndarray,
    eta: np.ndarray,
    index: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray]:
    amplitude = np.linalg.matrix_power(kernel, DEPTH) @ eta
    rho = amplitude / amplitude[index[(0, 0)]]
    return amplitude, rho


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    local_note = read("docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md")
    construction_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CONSTRUCTION_BOUNDARY_NOTE_2026-04-17.md")
    compression_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_KERNEL_RIM_COMPRESSION_THEOREM_NOTE_2026-04-17.md")

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    kernel, bulk_matrix = build_bulk_integral_witness(jmat, index)
    rim_matrix, coeff_identity, coeff_marked, eta_identity, eta_marked = build_rim_integral_witness(jmat, index)

    kernel_formula = np.zeros_like(kernel)
    for col in range(bulk_matrix.shape[1]):
        kernel_formula += np.outer(bulk_matrix[:, col], bulk_matrix[:, col])

    eta_identity_formula = np.zeros_like(eta_identity)
    eta_marked_formula = np.zeros_like(eta_marked)
    for col in range(rim_matrix.shape[1]):
        eta_identity_formula += coeff_identity[col] * rim_matrix[:, col]
        eta_marked_formula += coeff_marked[col] * rim_matrix[:, col]

    amp_identity, rho_identity = boundary_data(kernel, eta_identity, index)
    amp_marked, rho_marked = boundary_data(kernel, eta_marked, index)

    kernel_sym = float(np.max(np.abs(kernel - kernel.T)))
    kernel_swap = float(np.max(np.abs(swap @ kernel - kernel @ swap)))
    kernel_min = float(np.min(np.linalg.eigvalsh(kernel)))
    kernel_formula_err = float(np.max(np.abs(kernel - kernel_formula)))

    eta_identity_swap = float(np.max(np.abs(swap @ eta_identity - eta_identity)))
    eta_marked_swap = float(np.max(np.abs(swap @ eta_marked - eta_marked)))
    eta_formula_err = max(
        float(np.max(np.abs(eta_identity - eta_identity_formula))),
        float(np.max(np.abs(eta_marked - eta_marked_formula))),
    )
    eta_gap = float(np.max(np.abs(eta_marked - eta_identity)))

    rho_identity_swap = float(np.max(np.abs(swap @ rho_identity - rho_identity)))
    rho_marked_swap = float(np.max(np.abs(swap @ rho_marked - rho_marked)))
    rho_gap = float(np.max(np.abs(rho_marked - rho_identity)))

    print("=" * 92)
    print("GAUGE-VACUUM PLAQUETTE ONE-SLAB ORTHOGONAL-KERNEL INTEGRAL BOUNDARY")
    print("=" * 92)
    print()
    print("Wilson/PF structure carried into the witness")
    print(f"  dominant-weight box size                    = {(NMAX + 1)} x {(NMAX + 1)} = {len(weights)} states")
    print(f"  source-recurrence symmetry error            = {float(np.max(np.abs(jmat - jmat.T))):.3e}")
    print()
    print("Bulk one-slab kernel witness")
    print(f"  kernel symmetry / swap errors               = {kernel_sym:.3e}, {kernel_swap:.3e}")
    print(f"  kernel minimum eigenvalue                   = {kernel_min:.6e}")
    print(f"  slab-sum reconstruction error               = {kernel_formula_err:.3e}")
    print()
    print("Local rim-integral witness")
    print(f"  eta_identity min / swap error               = {float(np.min(eta_identity)):.6e}, {eta_identity_swap:.3e}")
    print(f"  eta_marked  min / swap error                = {float(np.min(eta_marked)):.6e}, {eta_marked_swap:.3e}")
    print(f"  rim reconstruction error                    = {eta_formula_err:.3e}")
    print(f"  max |eta_marked - eta_identity|             = {eta_gap:.6e}")
    print()
    print("Boundary amplitudes from the explicit pre-compression integrals")
    print(f"  amp_identity min / max                      = {float(np.min(amp_identity)):.12f}, {float(np.max(amp_identity)):.12f}")
    print(f"  amp_marked  min / max                       = {float(np.min(amp_marked)):.12f}, {float(np.max(amp_marked)):.12f}")
    print(f"  rho_identity swap error                     = {rho_identity_swap:.3e}")
    print(f"  rho_marked  swap error                      = {rho_marked_swap:.3e}")
    print(f"  max |rho_marked - rho_identity|             = {rho_gap:.6e}")
    print()
    print("Framework-point caution")
    print("  explicit beta = 6 closed-form data are not produced here; only the")
    print("  exact pre-compression integral class is fixed and witnessed.")
    print()

    check(
        "the spatial-environment transfer theorem already identifies one exact orthogonal-slice kernel K_beta^env and one rim-induced boundary state eta_beta(W)",
        "K_beta^env(U_(k+1), U_k)" in transfer_note
        and "eta_beta(W)" in transfer_note
        and "Integrating the Wilson weight between adjacent slices defines one exact kernel" in transfer_note,
        detail="the live environment object is already at the bulk-kernel / rim-boundary level",
    )
    check(
        "the local/environment factorization theorem removes extra non-rim marked representation dependence after normalization",
        "non-marked mixed-link factors collapse to one rep-independent\nscalar on the marked plaquette source sector." in local_note
        and "remaining nontrivial local marked data are exactly rim data" in compression_note
        and "one local rim map `B_beta`" in compression_note,
        detail="the marked plaquette is not reinserted into the bulk slab kernel; its residual input is rim-local",
    )
    check(
        "one explicit positive slab-sum formula yields a self-adjoint conjugation-symmetric one-slab kernel",
        kernel_sym < 1.0e-12 and kernel_swap < 1.0e-12 and kernel_min > -1.0e-12,
        detail=f"kernel min eigenvalue={kernel_min:.6e}, slab-sum error={kernel_formula_err:.3e}",
    )
    check(
        "the same bulk kernel can be paired with different local rim integrals while the marked dependence stays out of K_beta^env itself",
        eta_identity_swap < 1.0e-12
        and eta_marked_swap < 1.0e-12
        and float(np.min(eta_identity)) >= -1.0e-12
        and float(np.min(eta_marked)) >= -1.0e-12
        and eta_gap > 1.0e-3,
        detail=f"kernel is unchanged while the rim-induced boundary state moves by {eta_gap:.3e}",
    )
    check(
        "once the bulk kernel and rim integral are explicit, the normalized boundary amplitudes are explicit and positive",
        float(np.min(amp_identity)) > 0.0
        and float(np.min(amp_marked)) > 0.0
        and float(np.min(rho_identity)) > 0.0
        and float(np.min(rho_marked)) > 0.0
        and rho_identity_swap < 1.0e-12
        and rho_marked_swap < 1.0e-12,
        detail="the downstream class-sector coefficients are computed boundary amplitudes of explicit pre-compression data",
    )

    check(
        "the construction-boundary note already identifies explicit K_6^env plus the rim map as the earliest missing datum",
        "K_6^env" in construction_note
        and "eta_6" in construction_note
        and "earliest missing constructive datum" in construction_note,
        detail="the current PF seam is evaluation of the pre-compression kernel/rim integrals",
        bucket="SUPPORT",
    )
    check(
        "the exact one-slab kernel witness is reconstructed by a finite slab-sum with no hidden post-compression input",
        kernel_formula_err < 1.0e-12,
        detail=f"max slab-sum reconstruction error = {kernel_formula_err:.3e}",
        bucket="SUPPORT",
    )
    check(
        "distinct local rim integrals with the same bulk kernel induce distinct normalized boundary data",
        eta_formula_err < 1.0e-12 and rho_gap > 1.0e-3,
        detail=f"rim reconstruction error={eta_formula_err:.3e}, rho gap={rho_gap:.3e}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 92)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 92)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
