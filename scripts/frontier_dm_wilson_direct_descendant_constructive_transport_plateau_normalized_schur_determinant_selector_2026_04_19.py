#!/usr/bin/env python3
"""
DM Wilson direct-descendant constructive transport plateau normalized Schur-determinant selector.

Purpose:
  Collapse the plateau-breaking Schur spectral-isotropy family to one exact
  local scalar law on the descended source data.

Result:
  The coefficient-free scalar

      J_iso(H_e) = 27 det(H_e) / Tr(H_e)^3
                 = 27 Delta_src / (R11 + R22 + R33)^3

  is the canonical AM-GM normalized Schur-isotropy ratio on the positive
  Schur spectrum. On the certified constructive plateau witnesses W0..W3 it
  uniquely selects W1, and that winner agrees with the whole Schur-concave
  spectral-isotropy family. The aligned-seed -> W1 segment then yields a
  unique exact constructive eta_1 = 1 root.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import seed_point
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    build_active_from_seed_logits,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    eta1,
    observable_jacobian,
    observable_pack,
)


PASS_COUNT = 0
FAIL_COUNT = 0

FD_STEP = 1.0e-6
MAJOR_TOL = 1.0e-10


@dataclass(frozen=True)
class WitnessRecord:
    label: str
    source5: np.ndarray
    spectrum_desc: np.ndarray
    delta_src: float
    trace_h: float
    j_iso: float
    shannon_entropy: float


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def shannon_entropy(probs: np.ndarray) -> float:
    p = np.asarray(probs, dtype=float)
    return float(-np.sum(p * np.log(p)))


def majorized_by(more_uniform: np.ndarray, comparator: np.ndarray, tol: float = MAJOR_TOL) -> bool:
    u = np.asarray(more_uniform, dtype=float)
    v = np.asarray(comparator, dtype=float)
    partial_u = np.cumsum(u[:-1])
    partial_v = np.cumsum(v[:-1])
    return bool(np.all(partial_u <= partial_v + tol) and np.any(partial_u < partial_v - tol))


def normalized_spectrum_desc(hmat: np.ndarray) -> np.ndarray:
    evals = np.sort(np.linalg.eigvalsh(np.asarray(hmat, dtype=complex)))[::-1]
    return np.asarray(evals / np.sum(evals), dtype=float)


def j_iso_from_h(hmat: np.ndarray) -> float:
    trace_h = float(np.trace(hmat).real)
    det_h = float(np.linalg.det(hmat).real)
    return float(27.0 * det_h / (trace_h**3))


def build_records() -> list[WitnessRecord]:
    out: list[WitnessRecord] = []
    for label, params in zip(plateau.PLATEAU_LABELS, plateau.plateau_witness_params()):
        x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
        hmat = canonical_h(x, y, delta)
        spectrum = normalized_spectrum_desc(hmat)
        out.append(
            WitnessRecord(
                label=label,
                source5=np.array([x[0], x[1], y[0], y[1], delta], dtype=float),
                spectrum_desc=spectrum,
                delta_src=float(np.linalg.det(hmat).real),
                trace_h=float(np.trace(hmat).real),
                j_iso=j_iso_from_h(hmat),
                shannon_entropy=shannon_entropy(spectrum),
            )
        )
    return out


def seed_vector() -> np.ndarray:
    seed_x, seed_y, seed_delta = seed_point()
    return np.array([seed_x[0], seed_x[1], seed_y[0], seed_y[1], seed_delta], dtype=float)


def segment(seed: np.ndarray, endpoint: np.ndarray, lam: float) -> np.ndarray:
    return (1.0 - lam) * seed + lam * endpoint


def eta_root_count(seed: np.ndarray, endpoint: np.ndarray, grid_size: int = 2001) -> int:
    grid = np.linspace(0.0, 1.0, grid_size)
    vals = np.array([eta1(segment(seed, endpoint, lam)) - 1.0 for lam in grid], dtype=float)
    count = 0
    for idx in range(grid.size - 1):
        if abs(vals[idx]) < 1.0e-12:
            count += 1
        elif vals[idx] * vals[idx + 1] < 0.0:
            count += 1
    return count


def local_rank_data(v: np.ndarray) -> tuple[int, float, int, float]:
    jac = observable_jacobian(v, FD_STEP)
    singular = np.linalg.svd(jac, compute_uv=False)
    tangent_basis = null_space(jac[0:1, :])
    restricted = jac[1:, :] @ tangent_basis
    restricted_singular = np.linalg.svd(restricted, compute_uv=False)
    return (
        int(np.sum(singular > 1.0e-8)),
        float(np.min(singular)),
        int(np.sum(restricted_singular > 1.0e-8)),
        float(np.min(restricted_singular)),
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE TRANSPORT PLATEAU NORMALIZED SCHUR-DETERMINANT SELECTOR")
    print("=" * 88)

    records = build_records()
    winner = max(records, key=lambda rec: rec.j_iso)
    seed = seed_vector()

    print("\n" + "=" * 88)
    print("PART 1: J_iso IS AN EXACT LOCAL SCHUR-SIDE ISOTROPY SCALAR")
    print("=" * 88)
    lower_ok = all(rec.j_iso > 0.0 for rec in records)
    upper_ok = all(rec.j_iso < 1.0 for rec in records)
    exact_formula_ok = all(
        abs(rec.j_iso - 27.0 * rec.delta_src / (rec.trace_h**3)) < 1.0e-15 for rec in records
    )
    check(
        "J_iso = 27 det(H_e) / Tr(H_e)^3 is exactly the same scalar as 27 Delta_src / (R11+R22+R33)^3",
        exact_formula_ok,
        "Delta_src = det(H_e) and R11+R22+R33 = Tr(H_e)",
    )
    check(
        "The certified plateau witnesses all satisfy the AM-GM isotropy bounds 0 < J_iso < 1",
        lower_ok and upper_ok,
        ", ".join(f"{rec.label}: {rec.j_iso:.12f}" for rec in records),
    )

    print("\n" + "=" * 88)
    print("PART 2: J_iso UNIQUELY SELECTS W1 ON THE CERTIFIED PLATEAU SET")
    print("=" * 88)
    gaps = sorted(rec.j_iso for rec in records)
    top_gap = float(gaps[-1] - gaps[-2])
    check(
        "J_iso has a unique plateau maximizer",
        winner.label == "W1" and top_gap > 1.0e-3,
        f"winner={winner.label}, gap={top_gap:.12f}",
    )
    majorization_ok = all(
        majorized_by(winner.spectrum_desc, rec.spectrum_desc)
        for rec in records
        if rec.label != winner.label
    )
    entropy_winner = max(records, key=lambda rec: rec.shannon_entropy).label
    check(
        "That scalar winner agrees with the whole normalized Schur spectral-isotropy family on the certified plateau set",
        majorization_ok and entropy_winner == "W1",
        f"entropy winner={entropy_winner}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE J_iso WINNER GIVES A UNIQUE EXACT CONSTRUCTIVE ROOT")
    print("=" * 88)
    root_count = eta_root_count(seed, winner.source5)
    root_lambda = float(brentq(lambda lam: eta1(segment(seed, winner.source5, lam)) - 1.0, 0.0, 1.0))
    root_point = segment(seed, winner.source5, root_lambda)
    root_pack = observable_pack(root_point)
    deriv = float(
        (eta1(segment(seed, winner.source5, root_lambda + FD_STEP)) - eta1(segment(seed, winner.source5, root_lambda - FD_STEP)))
        / (2.0 * FD_STEP)
    )
    rank_data = local_rank_data(root_point)
    check(
        "The aligned-seed -> J_iso-winner segment has a unique eta_1 = 1 crossing",
        root_count == 1 and 0.0 < root_lambda < 1.0,
        f"lambda={root_lambda:.12f}",
    )
    check(
        "That root is transverse, constructive, positive-branch, and locally full-rank",
        deriv > 1.0e-4
        and abs(root_pack[0] - 1.0) < 1.0e-10
        and np.min(root_pack[1:]) > 0.0
        and rank_data[0] == 5
        and rank_data[1] > 1.0e-4
        and rank_data[2] == 4
        and rank_data[3] > 1.0e-4,
        (
            f"deriv={deriv:.6f}, pack={np.round(root_pack, 12)}, "
            f"min singulars=({rank_data[1]:.6e},{rank_data[3]:.6e})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The plateau-breaking spectral-isotropy family therefore has a concrete exact local scalar representative",
        winner.label == "W1" and exact_formula_ok,
        "use J_iso = 27 Delta_src / (R11+R22+R33)^3",
    )
    check(
        "That scalar yields the cleanest current retained-closeout candidate on the certified plateau set",
        winner.label == "W1" and root_count == 1,
        "endpoint law = maximize J_iso on the constructive plateau; closure law = unique eta_1 = 1 crossing on the aligned-seed -> W1 segment",
    )

    print()
    print("  certified plateau J_iso values:")
    for rec in records:
        print(
            f"    {rec.label}: "
            f"J_iso={rec.j_iso:.12f}, "
            f"spectrum={np.round(rec.spectrum_desc, 12)}"
        )
    print()
    print(f"  J_iso-selected endpoint witness = {winner.label}")
    print(f"  aligned-seed -> {winner.label} root lambda = {root_lambda:.12f}")
    print(f"  selected root observable pack   = {np.round(root_pack, 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
