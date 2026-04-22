#!/usr/bin/env python3
"""
DM Wilson direct-descendant constructive transport plateau Schur spectral-isotropy selector.

Purpose:
  Identify the first coefficient-free source-side law on the constructive
  transport plateau that actually selects one current-branch plateau witness.

Result:
  On the current certified constructive plateau witness set {W0, W1, W2, W3},
  the normalized Schur spectrum of

      H_e(L_e) = Herm(L_e^{-1})

  is most isotropic at W1. More sharply, the normalized W1 spectrum is
  majorized by the normalized spectra of W0, W2, and W3. Therefore every
  strictly Schur-concave symmetric law of the normalized Schur spectrum
  uniquely selects W1 on this certified witness set. Representative winners
  include Shannon entropy, the Renyi entropy family, participation ratio,
  normalized determinant, and inverse condition number.

  The aligned-seed -> W1 affine segment then yields a unique exact constructive
  eta_1 = 1 crossing, giving a fully specified source-visible selector
  candidate.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import (
    constructive_column_eta,
    path_point,
    seed_point,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    build_active_from_seed_logits,
    eta_columns_from_active,
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
    params: np.ndarray
    source5: np.ndarray
    favored_sorted_column: np.ndarray
    normalized_spectrum_desc: np.ndarray
    shannon_entropy: float
    participation_ratio: float
    normalized_logdet: float
    inverse_condition: float


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


def normalized_spectrum_desc(hmat: np.ndarray) -> np.ndarray:
    evals = np.sort(np.linalg.eigvalsh(np.asarray(hmat, dtype=complex)))[::-1]
    return np.asarray(evals / np.sum(evals), dtype=float)


def shannon_entropy(p: np.ndarray) -> float:
    probs = np.asarray(p, dtype=float)
    return float(-np.sum(probs * np.log(probs)))


def renyi_entropy(p: np.ndarray, alpha: float) -> float:
    probs = np.asarray(p, dtype=float)
    if abs(alpha - 1.0) < 1.0e-12:
        return shannon_entropy(probs)
    return float(np.log(np.sum(probs**alpha)) / (1.0 - alpha))


def majorized_by(more_uniform: np.ndarray, comparator: np.ndarray, tol: float = MAJOR_TOL) -> bool:
    u = np.asarray(more_uniform, dtype=float)
    v = np.asarray(comparator, dtype=float)
    partial_u = np.cumsum(u[:-1])
    partial_v = np.cumsum(v[:-1])
    return bool(np.all(partial_u <= partial_v + tol) and np.any(partial_u < partial_v - tol))


def build_records() -> list[WitnessRecord]:
    out: list[WitnessRecord] = []
    for label, params in zip(plateau.PLATEAU_LABELS, plateau.plateau_witness_params()):
        x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
        hmat = canonical_h(x, y, delta)
        packet, _etas = eta_columns_from_active(x, y, delta)
        spectrum = normalized_spectrum_desc(hmat)
        out.append(
            WitnessRecord(
                label=label,
                params=np.asarray(params, dtype=float),
                source5=np.array([x[0], x[1], y[0], y[1], delta], dtype=float),
                favored_sorted_column=np.sort(np.asarray(packet[:, 1], dtype=float)),
                normalized_spectrum_desc=spectrum,
                shannon_entropy=shannon_entropy(spectrum),
                participation_ratio=float(1.0 / np.sum(spectrum * spectrum)),
                normalized_logdet=float(np.sum(np.log(spectrum))),
                inverse_condition=float(spectrum[-1] / spectrum[0]),
            )
        )
    return out


def argmax_label(records: list[WitnessRecord], getter) -> str:
    return max(records, key=getter).label


def seed_vector() -> np.ndarray:
    seed_x, seed_y, seed_delta = seed_point()
    return np.array([seed_x[0], seed_x[1], seed_y[0], seed_y[1], seed_delta], dtype=float)


def segment(seed: np.ndarray, endpoint: np.ndarray, lam: float) -> np.ndarray:
    return (1.0 - lam) * seed + lam * endpoint


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


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE TRANSPORT PLATEAU SCHUR SPECTRAL-ISOTROPY SELECTOR")
    print("=" * 88)

    records = build_records()
    w1 = next(record for record in records if record.label == "W1")
    seed = seed_vector()

    print("\n" + "=" * 88)
    print("PART 1: THE NORMALIZED SCHUR SPECTRUM IS SOURCE-VISIBLE BUT TRANSPORT-BLIND")
    print("=" * 88)
    max_column_orbit_spread = max(
        float(np.linalg.norm(records[i].favored_sorted_column - records[j].favored_sorted_column))
        for i in range(len(records))
        for j in range(i + 1, len(records))
    )
    min_spectral_sep = min(
        float(np.linalg.norm(records[i].normalized_spectrum_desc - records[j].normalized_spectrum_desc))
        for i in range(len(records))
        for j in range(i + 1, len(records))
    )
    check(
        "All four certified plateau witnesses still realize the same favored transport-column orbit",
        max_column_orbit_spread < 5.0e-8,
        f"max sorted-column spread={max_column_orbit_spread:.3e}",
    )
    check(
        "Their normalized Schur spectra are nevertheless pairwise distinct",
        min_spectral_sep > 1.0e-2,
        f"min normalized-spectrum separation={min_spectral_sep:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: W1 IS THE MOST ISOTROPIC NORMALIZED SCHUR SPECTRUM")
    print("=" * 88)
    majorization_ok = True
    details: list[str] = []
    for record in records:
        if record.label == "W1":
            continue
        is_majorized = majorized_by(w1.normalized_spectrum_desc, record.normalized_spectrum_desc)
        majorization_ok &= is_majorized
        partial_w1 = np.cumsum(w1.normalized_spectrum_desc[:-1])
        partial_other = np.cumsum(record.normalized_spectrum_desc[:-1])
        details.append(
            f"{record.label}: partials W1={np.round(partial_w1, 12)}, other={np.round(partial_other, 12)}"
        )
    check(
        "The normalized W1 spectrum is majorized by the normalized spectra of W0, W2, and W3",
        majorization_ok,
        " | ".join(details),
    )
    check(
        "So every strictly Schur-concave symmetric law on the normalized Schur spectrum selects W1 on the certified witness set",
        majorization_ok,
        "majorization gives a whole coefficient-free selector family, not one fitted score",
    )

    print("\n" + "=" * 88)
    print("PART 3: REPRESENTATIVE SCHUR-SPECTRAL ISOTROPY LAWS ALL PICK W1")
    print("=" * 88)
    alpha_grid = [0.5, 1.0, 2.0, 4.0]
    renyi_winners = {
        alpha: argmax_label(records, lambda rec, a=alpha: renyi_entropy(rec.normalized_spectrum_desc, a))
        for alpha in alpha_grid
    }
    check(
        "The Renyi entropy family on the normalized Schur spectrum selects W1 for alpha in {1/2,1,2,4}",
        all(winner == "W1" for winner in renyi_winners.values()),
        f"winners={renyi_winners}",
    )
    check(
        "Participation ratio, normalized logdet, and inverse condition number also all select W1",
        argmax_label(records, lambda rec: rec.participation_ratio) == "W1"
        and argmax_label(records, lambda rec: rec.normalized_logdet) == "W1"
        and argmax_label(records, lambda rec: rec.inverse_condition) == "W1",
        (
            "winners="
            f"(PR={argmax_label(records, lambda rec: rec.participation_ratio)}, "
            f"logdet={argmax_label(records, lambda rec: rec.normalized_logdet)}, "
            f"invcond={argmax_label(records, lambda rec: rec.inverse_condition)})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 4: THE ALIGNED-SEED -> W1 SEGMENT GIVES A UNIQUE EXACT CONSTRUCTIVE ROOT")
    print("=" * 88)
    root_count = eta_root_count(seed, w1.source5)
    root_lambda = float(brentq(lambda lam: eta1(segment(seed, w1.source5, lam)) - 1.0, 0.0, 1.0))
    root_point = segment(seed, w1.source5, root_lambda)
    root_pack = observable_pack(root_point)
    deriv = float(
        (eta1(segment(seed, w1.source5, root_lambda + FD_STEP)) - eta1(segment(seed, w1.source5, root_lambda - FD_STEP)))
        / (2.0 * FD_STEP)
    )
    rank_data = local_rank_data(root_point)
    current_path_lambda = float(brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0))
    px, py, pdelta = path_point(current_path_lambda)
    current_path_root = np.array([px[0], px[1], py[0], py[1], pdelta], dtype=float)
    check(
        "The aligned-seed -> W1 affine segment has a unique eta_1 = 1 crossing on [0,1]",
        root_count == 1 and 0.0 < root_lambda < 1.0,
        f"lambda_iso={root_lambda:.12f}",
    )
    check(
        "That crossing is transverse, constructive, positive-branch, and locally full-rank",
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
    check(
        "The isotropy-selected root is distinct from the earlier hand-chosen canonical-path root",
        float(np.linalg.norm(root_point - current_path_root)) > 5.0e-1,
        f"distance={np.linalg.norm(root_point - current_path_root):.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The first concrete science that closes the current certified plateau issue is a coefficient-free normalized Schur spectral-isotropy law",
        majorization_ok and all(winner == "W1" for winner in renyi_winners.values()),
        "it selects the endpoint W1 from source-side data alone",
    )
    check(
        "Combined with the unique seed -> W1 exact crossing, that law yields a fully specified constructive selector candidate",
        root_count == 1 and np.min(root_pack[1:]) > 0.0,
        "endpoint law = spectral isotropy on H_e(L_e); closure law = unique eta_1 = 1 crossing on the aligned-seed -> W1 segment",
    )

    print()
    print("  normalized Schur spectra (descending):")
    for record in records:
        print(f"    {record.label}: {np.round(record.normalized_spectrum_desc, 12)}")
    print()
    print(f"  isotropy-selected endpoint witness = {w1.label}")
    print(f"  aligned-seed -> {w1.label} root lambda = {root_lambda:.12f}")
    print(f"  selected root observable pack       = {np.round(root_pack, 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
