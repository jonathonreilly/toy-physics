#!/usr/bin/env python3
"""Shared lower-level PMNS utilities."""

from __future__ import annotations

import inspect
import itertools
import math
from typing import Callable

import numpy as np

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERMUTATIONS = {
    0: I3,
    1: CYCLE,
    2: CYCLE @ CYCLE,
}
TARGET_SUPPORT = (np.abs(I3 + CYCLE) > 0).astype(int)
BANNED_INPUT_NAMES = {"d0_trip", "dm_trip", "delta_d_act", "diag_a_pq", "m_r"}


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(np.asarray(x, dtype=complex)) + diagonal(y_eff) @ CYCLE


def passive_operator(coeffs: np.ndarray, q: int) -> np.ndarray:
    return diagonal(np.asarray(coeffs, dtype=complex)) @ PERMUTATIONS[q]


def active_delta_d(block: np.ndarray) -> np.ndarray:
    return block - I3


def kernel_from_response_columns(columns: list[np.ndarray]) -> np.ndarray:
    return np.column_stack(columns)


def response_columns_from_block(
    block: np.ndarray, lam: float, subtract_identity: bool
) -> list[np.ndarray]:
    delta = block - I3 if subtract_identity else block
    kernel = np.linalg.inv(I3 - lam * delta)
    return [kernel[:, i].copy() for i in range(3)]


def active_response_columns_from_coordinates(
    x: np.ndarray, y: np.ndarray, delta: float, lam: float
) -> list[np.ndarray]:
    block = active_operator(x, y, delta)
    return response_columns_from_block(block, lam, subtract_identity=True)


def passive_response_columns_from_coordinates(
    coeffs: np.ndarray, q: int, lam: float
) -> list[np.ndarray]:
    block = passive_operator(coeffs, q)
    return response_columns_from_block(block, lam, subtract_identity=False)


def effective_block_from_sector_operator(sector_operator: np.ndarray, support_dim: int = 3) -> np.ndarray:
    if sector_operator.shape[0] == support_dim:
        return sector_operator.copy()
    a = sector_operator[:support_dim, :support_dim]
    b = sector_operator[:support_dim, support_dim:]
    c = sector_operator[support_dim:, :support_dim]
    f = sector_operator[support_dim:, support_dim:]
    return schur_eff(a, b, c, f)


def active_response_columns_from_sector_operator(
    sector_operator: np.ndarray, lam: float, support_dim: int = 3
) -> tuple[np.ndarray, list[np.ndarray]]:
    block = effective_block_from_sector_operator(sector_operator, support_dim)
    return block, response_columns_from_block(block, lam, subtract_identity=True)


def passive_response_columns_from_sector_operator(
    sector_operator: np.ndarray, lam: float, support_dim: int = 3
) -> tuple[np.ndarray, list[np.ndarray]]:
    block = effective_block_from_sector_operator(sector_operator, support_dim)
    return block, response_columns_from_block(block, lam, subtract_identity=False)


def sector_operator_fixture_from_effective_block(
    block: np.ndarray, *, seed: int, support_dim: int = 3, spectator_dim: int = 2, spectator_shift: float = 3.0
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if spectator_dim == 0:
        return np.asarray(block, dtype=complex).copy()
    f_raw = rng.normal(size=(spectator_dim, spectator_dim)) + 1j * rng.normal(size=(spectator_dim, spectator_dim))
    f = 0.5 * (f_raw + f_raw.conj().T) + spectator_shift * np.eye(spectator_dim, dtype=complex)
    b = rng.normal(size=(support_dim, spectator_dim)) + 1j * rng.normal(size=(support_dim, spectator_dim))
    a = np.asarray(block, dtype=complex) + b @ np.linalg.inv(f) @ b.conj().T
    return np.block([[a, b], [b.conj().T, f]])


def derive_active_block_from_response_columns(
    response_columns: list[np.ndarray], lam: float
) -> tuple[np.ndarray, np.ndarray]:
    kernel = kernel_from_response_columns(response_columns)
    delta = (I3 - np.linalg.inv(kernel)) / lam
    return kernel, I3 + delta


def derive_passive_block_from_response_columns(
    response_columns: list[np.ndarray], lam: float
) -> tuple[np.ndarray, np.ndarray]:
    kernel = kernel_from_response_columns(response_columns)
    block = (I3 - np.linalg.inv(kernel)) / lam
    return kernel, block


def support_trace_moments(block: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(block @ PERMUTATIONS[0].conj().T),
            np.trace(block @ PERMUTATIONS[1].conj().T),
            np.trace(block @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def recover_q_from_block(block: np.ndarray) -> int:
    return int(np.argmax(np.abs(support_trace_moments(block))))


def recover_passive_coeffs(block: np.ndarray, q: int) -> np.ndarray:
    coeff_diag = block @ PERMUTATIONS[q].conj().T
    return np.diag(coeff_diag)


def support_mask(y: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    return (np.abs(y) > tol).astype(int)


def all_permutation_matrices() -> list[np.ndarray]:
    mats: list[np.ndarray] = []
    for perm in itertools.permutations(range(3)):
        mat = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            mat[i, j] = 1.0
        mats.append(mat)
    return mats


PERM_FAMILY = all_permutation_matrices()


def detect_monomial(y: np.ndarray, tol: float = 1e-10) -> dict | None:
    mask = support_mask(y, tol)
    if not (
        np.array_equal(mask.sum(axis=1), np.ones(3, dtype=int))
        and np.array_equal(mask.sum(axis=0), np.ones(3, dtype=int))
        and np.count_nonzero(mask) == 3
    ):
        return None
    for offset, perm in PERMUTATIONS.items():
        if np.array_equal(mask, perm.real.astype(int)):
            coeff_diag = y @ perm.conj().T
            offdiag = coeff_diag - diagonal(np.diag(coeff_diag))
            if np.linalg.norm(offdiag) < tol:
                return {"offset": offset, "coeffs": np.diag(coeff_diag), "matrix": y}
    return None


def canonicalize_active(y: np.ndarray, tol: float = 1e-10) -> dict | None:
    for perm in PERM_FAMILY:
        y_perm = perm @ y @ perm.conj().T
        if not np.array_equal(support_mask(y_perm, tol), TARGET_SUPPORT):
            continue
        a = np.array([y_perm[0, 0], y_perm[1, 1], y_perm[2, 2]], dtype=complex)
        b = np.array([y_perm[0, 1], y_perm[1, 2], y_perm[2, 0]], dtype=complex)
        if np.min(np.abs(a)) < tol or np.min(np.abs(b)) < tol:
            continue
        phase_a = np.angle(a)
        alpha = np.zeros(3, dtype=float)
        alpha[1] = alpha[0] + phase_a[1] - np.angle(b[0])
        alpha[2] = alpha[1] + phase_a[2] - np.angle(b[1])
        beta = alpha - phase_a
        left = np.diag(np.exp(-1j * alpha))
        right = np.diag(np.exp(1j * beta))
        y_can = left @ y_perm @ right
        x = np.real(np.array([y_can[0, 0], y_can[1, 1], y_can[2, 2]], dtype=complex))
        b_can = np.array([y_can[0, 1], y_can[1, 2], y_can[2, 0]], dtype=complex)
        y_mod = np.array([np.real(b_can[0]), np.real(b_can[1]), np.abs(b_can[2])], dtype=float)
        delta = float(np.angle(b_can[2]))
        rebuilt = active_operator(x, y_mod, delta)
        if np.linalg.norm(rebuilt - y_can) < 1e-8:
            return {"perm": perm, "x": x, "y": y_mod, "delta": delta, "y_can": y_can}
    return None


def classify_tau_and_q_from_response_columns(
    neutral_columns: list[np.ndarray], charge_columns: list[np.ndarray], lam_act: float, lam_pass: float
) -> tuple[int, int, np.ndarray, np.ndarray]:
    _, neutral_as_passive = derive_passive_block_from_response_columns(neutral_columns, lam_pass)
    _, charge_as_passive = derive_passive_block_from_response_columns(charge_columns, lam_pass)

    neutral_passive = detect_monomial(neutral_as_passive) is not None
    charge_passive = detect_monomial(charge_as_passive) is not None

    if (not neutral_passive) and charge_passive:
        _, neutral_as_active = derive_active_block_from_response_columns(neutral_columns, lam_act)
        tau = 0
        q = recover_q_from_block(charge_as_passive)
        return tau, q, neutral_as_active, charge_as_passive
    if neutral_passive and (not charge_passive):
        _, charge_as_active = derive_active_block_from_response_columns(charge_columns, lam_act)
        tau = 1
        q = recover_q_from_block(neutral_as_passive)
        return tau, q, neutral_as_passive, charge_as_active
    raise ValueError("response packs do not realize a one-sided minimal PMNS class")


def seed_source_from_active_block(block: np.ndarray) -> dict:
    x = np.real(np.diag(block))
    y1 = float(np.real(block[0, 1]))
    y2 = float(np.real(block[1, 2]))
    y3 = float(np.abs(block[2, 0]))
    delta = float(np.angle(block[2, 0]))
    y = np.array([y1, y2, y3], dtype=float)
    xbar = float(np.mean(x))
    ybar = float(np.mean(y))
    xi = x - xbar * np.ones(3, dtype=float)
    eta = y - ybar * np.ones(3, dtype=float)
    return {
        "x": x,
        "y": y,
        "delta": delta,
        "xbar": xbar,
        "ybar": ybar,
        "xi": xi,
        "eta": eta,
        "xi1": float(xi[0]),
        "xi2": float(xi[1]),
        "eta1": float(eta[0]),
        "eta2": float(eta[1]),
    }


def invariant_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def quadratic_coefficients(obs: np.ndarray) -> tuple[float, float, float]:
    d1, d2, d3, r12, r23, r31, _phi = obs
    a = d2 * d3 - r23 * r23
    b = d1 * d2 * d3 + r31 * r31 * d2 - r12 * r12 * d3 - r23 * r23 * d1
    c = r31 * r31 * (d1 * d2 - r12 * r12)
    return float(a), float(b), float(c)


def quadratic_roots(obs: np.ndarray) -> np.ndarray:
    a, b, c = quadratic_coefficients(obs)
    disc = max(b * b - 4.0 * a * c, 0.0)
    roots = np.array(
        [
            (b - math.sqrt(disc)) / (2.0 * a),
            (b + math.sqrt(disc)) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    return roots


def reconstruct_squares_from_root(obs: np.ndarray, t1: float) -> tuple[np.ndarray, np.ndarray, float]:
    d1, d2, d3, r12, r23, _r31, phi = obs
    t2 = r12 * r12 / (d1 - t1)
    t3 = r23 * r23 / (d2 - t2)
    xsq = np.array([t1, t2, t3], dtype=float)
    ysq = np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float)
    return xsq, ysq, float(phi)


def reconstruct_sheets_from_h(h: np.ndarray) -> list[dict]:
    obs = invariant_coordinates(h)
    roots = quadratic_roots(obs)
    sheets: list[dict] = []
    for idx, root in enumerate(roots):
        xsq, ysq, phi = reconstruct_squares_from_root(obs, float(root))
        x = np.sqrt(np.maximum(xsq, 0.0))
        y = np.sqrt(np.maximum(ysq, 0.0))
        sheets.append({"index": idx, "y_can": active_operator(x, y, phi)})
    return sheets


def solve_triplet_pair(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    d0_m = detect_monomial(d0_trip)
    dm_m = detect_monomial(dm_trip)
    d0_a = canonicalize_active(d0_trip)
    dm_a = canonicalize_active(dm_trip)

    if d0_a is not None and dm_m is not None and d0_m is None and dm_a is None:
        branch = "neutrino-active"
        active = d0_a
        passive = dm_m
    elif dm_a is not None and d0_m is not None and dm_m is None and d0_a is None:
        branch = "charged-lepton-active"
        active = dm_a
        passive = d0_m
    else:
        raise ValueError("pair is not on a one-sided minimal PMNS class")

    h_active = active["y_can"] @ active["y_can"].conj().T
    sheets = reconstruct_sheets_from_h(h_active)
    sheet_scores = [np.linalg.norm(active["y_can"] - sheet["y_can"]) for sheet in sheets]
    sheet_index = int(np.argmin(sheet_scores))

    return {
        "branch": branch,
        "active_x": active["x"],
        "active_y": active["y"],
        "active_delta": active["delta"],
        "passive_offset": passive["offset"],
        "passive_coeffs": passive["coeffs"],
        "sheet": sheet_index,
        "sheet_scores": sheet_scores,
    }


def masses_and_pmns_from_pair(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    solved = solve_triplet_pair(d0_trip, dm_trip)
    if solved["branch"] == "neutrino-active":
        y_nu, y_e = d0_trip, dm_trip
    else:
        y_nu, y_e = dm_trip, d0_trip
    h_nu = y_nu @ y_nu.conj().T
    h_e = y_e @ y_e.conj().T

    evals_nu, vecs_nu = np.linalg.eigh(h_nu)
    evals_e, vecs_e = np.linalg.eigh(h_e)
    order_nu = np.argsort(np.real(evals_nu))
    order_e = np.argsort(np.real(evals_e))
    evals_nu = np.real(evals_nu[order_nu])
    evals_e = np.real(evals_e[order_e])
    vecs_nu = vecs_nu[:, order_nu]
    vecs_e = vecs_e[:, order_e]
    pmns = vecs_e.conj().T @ vecs_nu

    return {
        "branch": solved["branch"],
        "sheet": solved["sheet"],
        "H_nu": h_nu,
        "H_e": h_e,
        "m_nu": np.sqrt(np.maximum(evals_nu, 0.0)),
        "m_e": np.sqrt(np.maximum(evals_e, 0.0)),
        "pmns": pmns,
        "solved": solved,
    }


def circularity_guard(function: Callable[..., object], extra_banned: set[str] | None = None) -> tuple[bool, list[str]]:
    banned = set(BANNED_INPUT_NAMES)
    if extra_banned:
        banned |= set(extra_banned)
    params = list(inspect.signature(function).parameters.keys())
    bad = [p for p in params if p in banned]
    return len(bad) == 0, bad
