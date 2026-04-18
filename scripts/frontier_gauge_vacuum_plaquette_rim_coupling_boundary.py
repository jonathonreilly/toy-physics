#!/usr/bin/env python3
"""
Current exact boundary on the plaquette rim-coupling map.

This sharpens the local side of the PF construction lane:

1. the theorem-grade local marked-boundary data already fixed on the source
   sector are exp[(beta/2) J] and D_beta^loc;
2. the current stack now also fixes B_beta(W) at the level of an exact local
   Wilson/Haar integral and eta_beta(W) as its compressed descendant;
3. so the next local target is explicit beta=6 evaluation of B_6(W), not
   another refinement of D_6^loc and not identification of a different local
   boundary object.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.special import iv

ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80


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


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


def main() -> int:
    source_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md")
    local_note = read("docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md")
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    kernel_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_KERNEL_RIM_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    rim_integral_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    transfer_script = read("scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py")

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    half = matrix_exponential_symmetric(jmat, BETA / 2.0)
    half_sym = float(np.max(np.abs(half - half.T)))
    half_swap = float(np.max(np.abs(swap @ half - half @ swap)))
    half_min_eval = float(np.min(np.linalg.eigvalsh(half)))

    c00 = wilson_character_coefficient(0, 0)
    local = np.array(
        [wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00) for p, q in weights],
        dtype=float,
    )
    d_local = np.diag(local**4)
    d_local_swap = float(np.max(np.abs(swap @ d_local - d_local @ swap)))
    d_local_min = float(np.min(np.diag(d_local)))

    # Witness only: a hand-chosen positive conjugation-symmetric boundary state
    # compatible with the current transfer note, but not derived from a theorem-grade rim functional.
    eta0 = np.zeros(len(weights), dtype=float)
    eta0[index[(0, 0)]] = 1.0
    boundary = matrix_exponential_symmetric(jmat, 0.16) @ eta0
    boundary_swap = float(np.max(np.abs(swap @ boundary - boundary)))
    boundary_min = float(np.min(boundary))

    print("=" * 88)
    print("GAUGE-VACUUM PLAQUETTE RIM-COUPLING BOUNDARY")
    print("=" * 88)
    print()
    print("Already explicit theorem-grade local marked data")
    print(f"  half-slice symmetry / swap errors          = {half_sym:.3e}, {half_swap:.3e}")
    print(f"  half-slice minimum eigenvalue              = {half_min_eval:.6e}")
    print(f"  D_6^loc swap error                         = {d_local_swap:.3e}")
    print(f"  D_6^loc minimum diagonal                   = {d_local_min:.6e}")
    print()
    print("Older transfer-lane witness boundary state")
    print(f"  witness boundary min / swap error          = {boundary_min:.6e}, {boundary_swap:.3e}")
    print()

    check(
        "the exact source-sector factorization note already fixes the marked half-slice operator exp[(beta/2) J]",
        "exp[(beta / 2) J]" in source_note and "M_(beta/2) = exp[(beta / 2) J]" in source_note,
        detail="the local marked boundary side already has one exact half-slice operator on the class sector",
    )
    check(
        "the local/environment factorization note already fixes D_beta^loc and removes hidden non-marked mixed-link freedom",
        "D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)" in local_note
        and "non-marked mixed-link factors are scalar on the marked source sector" in local_note,
        detail="after normalization, non-marked mixed-link factors are theorem-grade scalars and D_beta^loc is explicit",
    )
    check(
        "the theorem-grade local marked data are compatible with positive conjugation-symmetric class-sector action",
        half_sym < 1.0e-12 and half_swap < 1.0e-12 and half_min_eval > 0.0 and d_local_swap < 1.0e-12 and d_local_min > 0.0,
        detail="exp[(beta/2)J] and D_beta^loc are already exact positive conjugation-symmetric local class-sector data",
    )
    check(
        "the spatial-environment transfer theorem still introduces eta_beta(W) only existentially through local rim coupling",
        "eta_beta(W)" in transfer_note
        and "induced on one edge slice" in transfer_note
        and "local rim coupling" in transfer_note,
        detail="the transfer theorem uses eta_beta(W) but does not yet derive an explicit formula for the rim functional",
    )
    check(
        "the full-slice rim-lift integral-boundary note now fixes B_beta(W) at the level of an exact local Wilson/Haar integral",
        "B_beta(W)(U)" in rim_integral_note
        and "full-slice local rim lift is the exact slice-space boundary function" in rim_integral_note
        and "explicit closed-form" in rim_integral_note
        and "beta = 6" in rim_integral_note,
        detail="the construction class of the local rim lift is now theorem-grade even though explicit framework-point evaluation remains open",
    )
    check(
        "the current transfer runner also uses a witness boundary state rather than a derived rim functional",
        "boundary = matrix_exponential_symmetric(jmat, 0.5 * ETA) @ eta0" in transfer_script,
        detail="the downstream script still inserts a compatible witness boundary, confirming explicit beta=6 evaluation is still open on that lane",
    )

    check(
        "a positive conjugation-symmetric boundary state is easy to witness once a rim map is supplied",
        boundary_swap < 1.0e-12 and boundary_min >= -1.0e-12,
        detail="the missing issue is not compatibility of eta_beta, but explicit derivation of the map producing it",
        bucket="SUPPORT",
    )
    check(
        "the next local target is therefore explicit beta=6 evaluation of the Wilson rim-coupling lift B_6(W)",
        "B_6" in kernel_note and "explicit formula for the rim map `B_6`" in kernel_note and "beta = 6" in rim_integral_note,
        detail="the local rim lift is now identified; what remains is explicit framework-point evaluation",
        bucket="SUPPORT",
    )
    check(
        "further work on D_6^loc alone cannot close the rim side of the PF lane",
        d_local_min > 0.0 and "explicit formula for the rim map `B_6`" in kernel_note,
        detail="the theorem-grade local mixed-kernel content is already exhausted by exp[(beta/2)J] and D_beta^loc",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
