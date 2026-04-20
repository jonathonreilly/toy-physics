#!/usr/bin/env python3
"""
Shared helper layer for the retained `3d+1 -> 3d` complement-line reduction
on the least-positive-bulk selected Wilson branch.
"""

from __future__ import annotations

import numpy as np

from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_packet_theorem_2026_04_19 import (
    selected_transfer_and_packet,
)
from frontier_gauge_vacuum_plaquette_spatial_environment_character_measure import (
    build_recurrence_matrix,
)
from frontier_perron_frobenius_step2_nilpotent_chain_source_response_calculus_2026_04_19 import (
    live_from_response_pack,
)


ORIGINAL_RETAINED_WEIGHTS = ((0, 0), (1, 0), (0, 1), (1, 1))
ORDERED_LINE_BASIS = (1, 0, 2, 3)
BOUNDARY_FIRST_WEIGHTS = tuple(ORIGINAL_RETAINED_WEIGHTS[i] for i in ORDERED_LINE_BASIS)
_RETAINED_BLOCK_ORIGINAL: np.ndarray | None = None

def normalize_line(line: np.ndarray) -> np.ndarray:
    arr = np.asarray(line, dtype=float).reshape(4)
    norm = float(np.linalg.norm(arr))
    if norm <= 0.0:
        raise ValueError("complement line must be nonzero")
    return arr / norm


def line_from_positive_angles(theta: float, phi: float, psi: float) -> np.ndarray:
    """
    Unit complement line on the positive `(1,1)` hemisphere of the retained
    ambient `S^3/{±1}`.
    """

    cpsi = float(np.cos(psi))
    return normalize_line(
        np.array(
            [
                np.cos(theta) * np.cos(phi) * cpsi,
                np.sin(theta) * np.cos(phi) * cpsi,
                np.sin(phi) * cpsi,
                np.sin(psi),
            ],
            dtype=float,
        )
    )


def positive_angles_from_line(line: np.ndarray) -> np.ndarray:
    vec = normalize_line(line)
    if vec[3] < 0.0:
        vec = -vec
    xy = float(np.hypot(vec[0], vec[1]))
    theta = float(np.arctan2(vec[1], vec[0]))
    phi = float(np.arctan2(vec[2], xy))
    psi = float(np.arcsin(np.clip(vec[3], -1.0, 1.0)))
    return np.array([theta, phi, psi], dtype=float)


def selected_retained_block_original() -> np.ndarray:
    global _RETAINED_BLOCK_ORIGINAL
    if _RETAINED_BLOCK_ORIGINAL is not None:
        return np.array(_RETAINED_BLOCK_ORIGINAL, dtype=float)
    pkg = selected_transfer_and_packet()
    transfer = np.asarray(pkg["transfer"], dtype=float)
    _jmat, weights, index = build_recurrence_matrix(5)
    retained = [index[w] for w in ORIGINAL_RETAINED_WEIGHTS]
    _RETAINED_BLOCK_ORIGINAL = transfer[np.ix_(retained, retained)]
    return np.array(_RETAINED_BLOCK_ORIGINAL, dtype=float)


def selected_retained_block_boundary_first() -> np.ndarray:
    """
    Retained `4x4` block in the original retained basis
    `((0,0),(1,0),(0,1),(1,1))`.

    The boundary-first structure is carried by `ORDERED_LINE_BASIS` during the
    ordered projection/Gram-Schmidt reduction, not by a separate coordinate
    permutation of the retained block.
    """

    return selected_retained_block_original()


def induced_ordered_slice_from_line(line: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    In the original retained coordinates, fix the ambient order
    `(1,0) -> (0,0) -> (0,1) -> (1,1)` and let the chosen complement line be
    the only free datum. The induced `3d` slice is obtained by projecting those
    ordered ambient basis vectors off the line and Gram-Schmidt
    orthonormalizing in that fixed order.
    """

    c = normalize_line(line)
    cols: list[np.ndarray] = []
    basis = np.eye(4, dtype=float)
    for idx in ORDERED_LINE_BASIS:
        v = basis[:, idx].copy()
        v -= float(c @ v) * c
        for q in cols:
            v -= float(q @ v) * q
        norm = float(np.linalg.norm(v))
        if norm > 1.0e-14:
            cols.append(v / norm)
        if len(cols) == 3:
            break
    if len(cols) != 3:
        raise RuntimeError("ordered line reduction failed to recover a 3d slice")
    return np.column_stack(cols), c


def compressed_local_block_from_line(line: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    block = selected_retained_block_original()
    qmat, c = induced_ordered_slice_from_line(line)
    h = qmat.T @ block @ qmat
    responses = np.array(hermitian_linear_responses(h.astype(complex)), dtype=float)
    live = np.array(live_from_response_pack(responses.tolist()), dtype=float)
    return h, responses, live, qmat


def slice_projector_from_line(line: np.ndarray) -> np.ndarray:
    qmat, _c = induced_ordered_slice_from_line(line)
    return qmat @ qmat.T


def reference_slice_projector(slot: str) -> np.ndarray:
    basis = np.eye(4, dtype=float)
    if slot == "rho1":
        cols = (1, 0, 3)
    elif slot == "rho2":
        cols = (0, 2, 3)
    else:
        raise ValueError("slot must be 'rho1' or 'rho2'")
    qmat = basis[:, cols]
    return qmat @ qmat.T


def projection_frobenius_distance(line: np.ndarray, slot: str) -> float:
    return float(
        np.linalg.norm(slice_projector_from_line(line) - reference_slice_projector(slot))
    )


def boundary_anchor_krylov_complement_line() -> np.ndarray:
    """
    Orthogonal complement of the boundary-anchored Krylov plane
    `span{e_(1,0), T e_(1,0), T^2 e_(1,0)}` on the boundary-first retained
    block. This is a natural cheap candidate selector used in later boundary
    theorems.
    """

    block = selected_retained_block_original()
    anchor = np.zeros(4, dtype=float)
    anchor[ORDERED_LINE_BASIS[0]] = 1.0
    krylov = np.column_stack([anchor, block @ anchor, block @ (block @ anchor)])
    qmat, _r = np.linalg.qr(krylov)
    u, _s, _vt = np.linalg.svd(qmat, full_matrices=True)
    line = u[:, 3]
    return normalize_line(line if line[0] >= 0.0 else -line)
