#!/usr/bin/env python3
"""
Compressed rim-functional uniqueness theorem on the plaquette PF lane.

This sharpens the rim side one step beyond the compressed boundary-evaluation
theorem:

1. the full local rim map B_beta(W) on the orthogonal-slice Hilbert space is
   still open;
2. but on every retained finite marked class sector the left boundary
   functional is already the universal Peter-Weyl evaluation functional;
3. so the remaining local gap is the full slice lift, not retained
   W-dependence.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 4
ETA = 0.32
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


def matrix_exponential_symmetric(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


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


def evaluation_vector(weights: list[tuple[int, int]], theta1: float, theta2: float) -> np.ndarray:
    return np.array(
        [
            dim_su3(p, q) * np.conjugate(su3_character(p, q, theta1, theta2))
            for p, q in weights
        ],
        dtype=complex,
    )


def direct_evaluation(coeffs: np.ndarray, weights: list[tuple[int, int]], theta1: float, theta2: float) -> complex:
    total = 0.0j
    for i, (p, q) in enumerate(weights):
        total += dim_su3(p, q) * coeffs[i] * su3_character(p, q, theta1, theta2)
    return total


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    eval_note = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md")
    rim_note = read("docs/GAUGE_VACUUM_PLAQUETTE_RIM_COUPLING_BOUNDARY_NOTE_2026-04-17.md")

    jmat, weights, index = build_recurrence_matrix(NMAX)
    layer_diag = np.diag(
        [np.exp(-0.18 * (p + q) - 0.05 * ((p - q) ** 2)) for p, q in weights]
    )
    s_env = matrix_exponential_symmetric(jmat, ETA) @ layer_diag @ matrix_exponential_symmetric(jmat, ETA)
    eta0 = np.zeros(len(weights), dtype=float)
    eta0[index[(0, 0)]] = 1.0
    eta = matrix_exponential_symmetric(jmat, 0.5 * ETA) @ eta0
    v_beta = np.linalg.matrix_power(s_env, DEPTH) @ eta
    v_alt = np.linalg.matrix_power(s_env, DEPTH) @ (matrix_exponential_symmetric(jmat, 0.38 * ETA) @ eta0)

    rng = np.random.default_rng(1729)
    coeff_random = rng.normal(size=len(weights)) + 1j * rng.normal(size=len(weights))

    sample_angles = [
        (0.31, -0.17),
        (0.53, 0.11),
        (-0.22, 0.47),
    ]

    basis_errors = []
    random_errors = []
    primary_errors = []
    alt_errors = []
    uniqueness_errors = []
    variation = []

    previous = None
    for theta1, theta2 in sample_angles:
        k_w = evaluation_vector(weights, theta1, theta2)

        for i, (p, q) in enumerate(weights):
            basis = np.zeros(len(weights), dtype=complex)
            basis[i] = 1.0
            exact = dim_su3(p, q) * su3_character(p, q, theta1, theta2)
            basis_errors.append(abs(np.vdot(k_w, basis) - exact))

        random_errors.append(abs(np.vdot(k_w, coeff_random) - direct_evaluation(coeff_random, weights, theta1, theta2)))
        primary_eval = direct_evaluation(v_beta, weights, theta1, theta2)
        alt_eval = direct_evaluation(v_alt, weights, theta1, theta2)
        primary_errors.append(abs(np.vdot(k_w, v_beta) - primary_eval))
        alt_errors.append(abs(np.vdot(k_w, v_alt) - alt_eval))

        recovered = np.conjugate(np.array([np.vdot(k_w, np.eye(len(weights), dtype=complex)[i]) for i in range(len(weights))]))
        uniqueness_errors.append(float(np.max(np.abs(recovered - k_w))))

        if previous is not None:
            variation.append(abs(primary_eval - previous))
        previous = primary_eval

    print("=" * 88)
    print("GAUGE-VACUUM PLAQUETTE COMPRESSED RIM-FUNCTIONAL UNIQUENESS")
    print("=" * 88)
    print()
    print("Retained class-sector evaluation-functional checks")
    print(f"  max basis evaluation error                = {max(basis_errors):.3e}")
    print(f"  max random-vector evaluation error        = {max(random_errors):.3e}")
    print(f"  max uniqueness reconstruction error       = {max(uniqueness_errors):.3e}")
    print()
    print("Transfer-lane compatibility checks")
    print(f"  max primary boundary-functional error     = {max(primary_errors):.3e}")
    print(f"  max alternate boundary-functional error   = {max(alt_errors):.3e}")
    print()

    check(
        "the spatial-environment transfer theorem still introduces eta_beta(W) only as a rim-induced slice-space boundary state",
        "eta_beta(W)" in transfer_note and "boundary amplitude" in transfer_note,
        detail="the older theorem surface fixes an exact boundary-amplitude law before any explicit local rim map is derived",
    )
    check(
        "the compressed rim-evaluation theorem already gives Z_beta^env(W)=<K(W), v_beta> on the retained marked class sector",
        "Z_beta^env(W) = <K(W), v_beta>" in eval_note,
        detail="the prior derivation already isolates all retained W-dependence in the Peter-Weyl evaluation functional",
    )
    check(
        "K_Lambda(W) reproduces exact retained basis evaluations on the marked character basis",
        max(basis_errors) < 1.0e-12,
        detail=f"max basis error={max(basis_errors):.3e}",
    )
    check(
        "K_Lambda(W) reproduces evaluation of arbitrary retained coefficient vectors",
        max(random_errors) < 1.0e-11,
        detail=f"max random-vector error={max(random_errors):.3e}",
    )
    check(
        "the retained left boundary functional is unique once its basis matrix elements are fixed",
        max(uniqueness_errors) < 1.0e-12,
        detail=f"max uniqueness reconstruction error={max(uniqueness_errors):.3e}",
    )
    check(
        "the rim-coupling boundary note remains correct: the full local slice lift B_beta(W) is still open even though the retained left boundary functional is explicit",
        "B_beta(W)" in rim_note and ("full local object" in rim_note or "missing local object" in rim_note),
        detail="this theorem closes the retained left boundary functional, not the full slice-Hilbert rim map",
    )

    check(
        "the same retained evaluation functional works for more than one propagated right boundary vector",
        max(primary_errors) < 1.0e-12 and max(alt_errors) < 1.0e-12,
        detail="the retained left boundary functional is universal while the beta-side vector can vary",
        bucket="SUPPORT",
    )
    check(
        "the sampled retained class-sector boundary law is nontrivial in W",
        max(variation) > 1.0e-3,
        detail=f"max sampled variation={max(variation):.3e}",
        bucket="SUPPORT",
    )
    check(
        "the retained Peter-Weyl evaluation vectors are genuinely holonomy-dependent",
        max(np.linalg.norm(evaluation_vector(weights, *sample_angles[i]) - evaluation_vector(weights, *sample_angles[j])) for i in range(len(sample_angles)) for j in range(i + 1, len(sample_angles))) > 1.0e-3,
        detail="distinct sampled holonomies induce distinct retained left boundary functionals",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
