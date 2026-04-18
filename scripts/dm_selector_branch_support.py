#!/usr/bin/env python3
"""
Shared support for the final DM selector branch authority runners.

This module is intentionally small and branch-local. It keeps the recovered
bank data, positive-probe helpers, and simple presentation utilities out of the
front-door authority notes while avoiding any dependency on the deleted
candidate forest.
"""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np

from frontier_dm_leptogenesis_ne_charged_source_response_reduction import source_response
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
)
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor

RECOVERED_LIFTS = np.array(
    [
        [1.021038842009447, 1.380791428981559, 0.215677476525045],
        [-0.086813625538201, 0.487118372315374, 0.34281415691339],
        [-0.297977556432843, 0.522960277548281, 0.482915971050468],
        [-0.974907636711156, 0.36604942473565, 0.782053575857018],
        [-1.899713042657682, 0.053096931345221, 1.133008944166234],
    ],
    dtype=float,
)

PREFERRED_RECOVERED_LIFT = np.array(
    [1.021038842009447, 1.380791428981559, 0.215677476525045],
    dtype=float,
)

SHIFT_OFFSETS = np.linspace(0.02, 2.0, 20)
ANCHOR_OFFSET = 0.20
GENERIC_OFFSET = 0.40
STRICT_GAP_FLOOR = 1.0e-9

EXCEPTIONAL_WINDOWS = {
    "endpoint": (-1.899713, -1.87),
    "split_1": (-1.16, -1.10),
    "split_2": (-0.19, -0.14),
}


def q_plus_from_slack_point(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    return q_floor(float(x[1])) + float(x[2])


def h_from_slack_point(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return active_affine_h(float(x[0]), float(x[1]), q_plus_from_slack_point(x))


def repair_from_slack_point(x: np.ndarray) -> float:
    h = h_from_slack_point(np.asarray(x, dtype=float))
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def recovered_bank() -> tuple[list[np.ndarray], list[np.ndarray], np.ndarray, list[tuple[float, float]]]:
    lifts = [np.asarray(x, dtype=float) for x in RECOVERED_LIFTS]
    hs = [h_from_slack_point(x) for x in lifts]
    repairs = np.array([repair_from_slack_point(x) for x in lifts], dtype=float)
    targets = [active_target_from_h(h) for h in hs]
    return lifts, hs, repairs, targets


def common_shift(repairs: np.ndarray, offset: float) -> float:
    return float(np.max(np.asarray(repairs, dtype=float)) + float(offset))


def normalize(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=complex)
    return v / max(float(np.linalg.norm(v)), 1.0e-12)


def rank_one_probe(v: np.ndarray) -> np.ndarray:
    u = normalize(v)
    return np.outer(u, u.conj())


def positive_response(h: np.ndarray, mu: float, j: np.ndarray) -> float:
    h_mu = np.asarray(h, dtype=complex) + float(mu) * np.eye(3, dtype=complex)
    return float(np.real(source_response(h_mu, np.asarray(j, dtype=complex))))


def response_matrix(hs: list[np.ndarray], mu: float, probes: list[tuple[str, np.ndarray]]) -> np.ndarray:
    return np.array(
        [[positive_response(h, mu, j) for _name, j in probes] for h in hs],
        dtype=float,
    )


def strict_probe_dominance(scores_a: np.ndarray, scores_b: np.ndarray) -> bool:
    return bool(np.all(np.asarray(scores_a, dtype=float) + STRICT_GAP_FLOOR < np.asarray(scores_b, dtype=float)))


def frontier_on_fiber(scores: np.ndarray) -> tuple[list[int], dict[int, int]]:
    undominated: list[int] = []
    witness: dict[int, int] = {}
    vals = np.asarray(scores, dtype=float)
    for idx in range(vals.shape[0]):
        dominated = False
        for other in range(vals.shape[0]):
            if idx == other:
                continue
            if strict_probe_dominance(vals[other], vals[idx]):
                dominated = True
                witness[idx] = other
                break
        if not dominated:
            undominated.append(idx)
    return undominated, witness


def universal_frontier_indices(hs: list[np.ndarray], repairs: np.ndarray, probes: list[tuple[str, np.ndarray]]) -> list[int]:
    frontier: set[int] | None = None
    for offset in SHIFT_OFFSETS:
        scores = response_matrix(hs, common_shift(repairs, float(offset)), probes)
        undominated, _witness = frontier_on_fiber(scores)
        if frontier is None:
            frontier = set(undominated)
        else:
            frontier &= set(undominated)
    return sorted(frontier or [])


def response_via_rayleigh(a: np.ndarray, v: np.ndarray) -> float:
    u = normalize(v)
    inv = np.linalg.inv(np.asarray(a, dtype=complex))
    rayleigh = float(np.real(u.conj().T @ inv @ u))
    return math.log1p(rayleigh)


def spectral_projector_data(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[np.ndarray]]:
    evals, evecs = np.linalg.eigh(np.asarray(a, dtype=complex))
    responses: list[float] = []
    projectors: list[np.ndarray] = []
    for idx in range(len(evals)):
        vec = np.asarray(evecs[:, idx], dtype=complex)
        proj = rank_one_probe(vec)
        projectors.append(proj)
        responses.append(float(np.real(source_response(np.asarray(a, dtype=complex), proj))))
    return np.asarray(evals, dtype=float), np.asarray(responses, dtype=float), projectors


def canonical_score_from_repairs(repairs: np.ndarray, mu: float) -> np.ndarray:
    vals = np.asarray(repairs, dtype=float)
    return np.array([math.log1p(1.0 / float(mu - repair)) for repair in vals], dtype=float)


def base_vector_family() -> list[tuple[str, np.ndarray]]:
    e1 = np.array([1.0, 0.0, 0.0], dtype=complex)
    e2 = np.array([0.0, 1.0, 0.0], dtype=complex)
    e3 = np.array([0.0, 0.0, 1.0], dtype=complex)
    return [
        ("e1", e1),
        ("e2", e2),
        ("e3", e3),
        ("e1_plus_e2", e1 + e2),
        ("e1_plus_ie3", e1 + 1j * e3),
    ]


def positive_probe_family() -> list[tuple[str, np.ndarray]]:
    return [(name, rank_one_probe(v)) for name, v in base_vector_family()]


def projective_family(
    presentation: list[tuple[str, np.ndarray]],
) -> list[tuple[str, np.ndarray]]:
    return [(name, rank_one_probe(v)) for name, v in presentation]


def relabeled_presentation(presentation: list[tuple[str, np.ndarray]]) -> list[tuple[str, np.ndarray]]:
    return [(f"relabeled_{idx}", np.asarray(v, dtype=complex)) for idx, (_name, v) in enumerate(reversed(presentation))]


def duplicated_presentation(presentation: list[tuple[str, np.ndarray]]) -> list[tuple[str, np.ndarray]]:
    return list(presentation) + [("dup_e1", 3.0 * np.asarray(presentation[0][1], dtype=complex))]


def changed_support_presentation(presentation: list[tuple[str, np.ndarray]]) -> list[tuple[str, np.ndarray]]:
    out = list(presentation[:-1])
    e2 = np.array([0.0, 1.0, 0.0], dtype=complex)
    e3 = np.array([0.0, 0.0, 1.0], dtype=complex)
    out.append(("e2_plus_ie3", e2 + 1j * e3))
    return out


def response_matrix_from_presentation(
    hs: list[np.ndarray], mu: float, presentation: list[tuple[str, np.ndarray]]
) -> np.ndarray:
    return response_matrix(hs, mu, projective_family(presentation))


def recover_scores_from_atomic_thresholds(scores: np.ndarray) -> np.ndarray:
    vals = np.asarray(scores, dtype=float)
    recovered = np.zeros_like(vals)
    for col in range(vals.shape[1]):
        levels = np.unique(vals[:, col])
        events = vals[:, [col]] >= levels[None, :]
        recovered[:, col] = np.array([float(np.max(levels[row])) for row in events], dtype=float)
    return recovered


def family_witness_from_atomic_thresholds(scores: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vals = np.asarray(scores, dtype=float)
    levels = np.unique(vals)
    events = vals[None, :, :] >= levels[:, None, None]
    witness = np.any(events, axis=2)
    envelope = np.array([float(np.max(levels[witness[:, idx]])) for idx in range(vals.shape[0])], dtype=float)
    return levels, witness, envelope


def projector_key(p: np.ndarray) -> tuple[float, ...]:
    arr = np.asarray(p, dtype=complex)
    vec = np.concatenate([np.real(arr).ravel(), np.imag(arr).ravel()])
    return tuple(np.round(vec, 12))


def extensional_response_map(
    hs: list[np.ndarray], mu: float, presentation: list[tuple[str, np.ndarray]]
) -> dict[tuple[float, ...], np.ndarray]:
    out: dict[tuple[float, ...], np.ndarray] = {}
    for _name, v in presentation:
        p = rank_one_probe(v)
        key = projector_key(p)
        if key not in out:
            out[key] = np.array([positive_response(h, mu, p) for h in hs], dtype=float)
    return out


def maps_equal(
    left: dict[tuple[float, ...], np.ndarray], right: dict[tuple[float, ...], np.ndarray]
) -> bool:
    if set(left) != set(right):
        return False
    return all(np.allclose(left[key], right[key], atol=1.0e-12) for key in left)


def maps_differ(
    left: dict[tuple[float, ...], np.ndarray], right: dict[tuple[float, ...], np.ndarray]
) -> bool:
    return not maps_equal(left, right)


def transformed_scores(values: np.ndarray) -> dict[str, np.ndarray]:
    vals = np.asarray(values, dtype=float)
    return {
        "id": vals.copy(),
        "square": vals * vals,
        "log1p": np.log1p(vals),
        "expm1": np.expm1(vals),
    }


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    phases = np.where(np.abs(diag) > 1.0e-12, diag / np.abs(diag), 1.0)
    return q @ np.diag(np.conj(phases))


def response_orders(values: Iterable[float]) -> list[int]:
    return [int(idx) for idx in np.argsort(np.asarray(list(values), dtype=float))]
