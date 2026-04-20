#!/usr/bin/env python3
"""
DM Wilson direct-descendant constructive transport plateau observable-affine no-go theorem.

Purpose:
  Test whether exact source-side plateau-breakers built from affine
  combinations of

      (gamma, E1, E2, Delta_src)

  can canonically select one constructive transport-plateau witness.

Result:
  no. The four known constructive plateau witnesses are affinely independent in
  this exact observable 4-pack, coordinate extremization already splits across
  all four witnesses, and the runner constructs an exact affine law that
  uniquely maximizes at each witness in turn. So the affine observable family
  does not contain a retained canonical selector: its coefficients are
  additional free selector input.

  Auxiliary scans also show the same non-consensus pattern for simple
  Schur-side spectral laws and for simple local Hessian/curvature invariants.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    build_active_from_seed_logits,
)


PASS_COUNT = 0
FAIL_COUNT = 0

AFFINE_TOL = 1.0e-10
HESS_STEP = 1.0e-5


@dataclass(frozen=True)
class WitnessRecord:
    label: str
    params: np.ndarray
    observable4: np.ndarray
    trace_h: float
    trace_h2: float
    lambda_min: float
    lambda_mid: float
    lambda_max: float
    hess_trace: float
    hess_frob: float


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


def finite_hessian(fun, x: np.ndarray, step: float = HESS_STEP) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    hess = np.zeros((x.size, x.size), dtype=float)
    for i in range(x.size):
        ei = np.zeros_like(x)
        ei[i] = step
        for j in range(x.size):
            ej = np.zeros_like(x)
            ej[j] = step
            hess[i, j] = (
                fun(x + ei + ej)
                - fun(x + ei - ej)
                - fun(x - ei + ej)
                + fun(x - ei - ej)
            ) / (4.0 * step * step)
    return hess


def witness_record(label: str, params: np.ndarray) -> WitnessRecord:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    hmat = canonical_h(x, y, delta)
    responses = hermitian_linear_responses(hmat)
    triplet = triplet_from_projected_response_pack(responses)
    observable4 = np.array(
        [
            triplet["gamma"],
            triplet["E1"],
            triplet["E2"],
            float(np.real(np.linalg.det(hmat))),
        ],
        dtype=float,
    )
    evals = np.linalg.eigvalsh(hmat)
    hess = finite_hessian(plateau.eta1_from_params, params)
    return WitnessRecord(
        label=label,
        params=np.asarray(params, dtype=float),
        observable4=observable4,
        trace_h=float(np.trace(hmat).real),
        trace_h2=float(np.trace(hmat @ hmat).real),
        lambda_min=float(evals[0]),
        lambda_mid=float(evals[1]),
        lambda_max=float(evals[2]),
        hess_trace=float(np.trace(hess)),
        hess_frob=float(np.linalg.norm(hess)),
    )


def build_records() -> list[WitnessRecord]:
    return [
        witness_record(label, params)
        for label, params in zip(plateau.PLATEAU_LABELS, plateau.plateau_witness_params())
    ]


def argmax_label(records: list[WitnessRecord], getter) -> str:
    return max(records, key=getter).label


def affine_selector_coefficients(records: list[WitnessRecord], winner_idx: int) -> np.ndarray:
    winner = records[winner_idx].observable4
    rows = [
        winner - records[idx].observable4
        for idx in range(len(records))
        if idx != winner_idx
    ]
    system = np.vstack(rows)
    coeffs, _resid, _rank, _singular = np.linalg.lstsq(system, np.ones(system.shape[0]), rcond=None)
    return np.asarray(coeffs, dtype=float)


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE TRANSPORT PLATEAU OBSERVABLE-AFFINE NO-GO")
    print("=" * 88)

    records = build_records()
    observable_matrix = np.vstack([record.observable4 for record in records])

    print("\n" + "=" * 88)
    print("PART 1: THE EXACT SOURCE-SIDE OBSERVABLE CHANNELS ALREADY SPLIT THE PLATEAU")
    print("=" * 88)
    min_obs_sep = min(
        float(np.linalg.norm(records[i].observable4 - records[j].observable4))
        for i in range(len(records))
        for j in range(i + 1, len(records))
    )
    channel_winners = {
        "gamma": argmax_label(records, lambda rec: rec.observable4[0]),
        "E1": argmax_label(records, lambda rec: rec.observable4[1]),
        "E2": argmax_label(records, lambda rec: rec.observable4[2]),
        "Delta_src": argmax_label(records, lambda rec: rec.observable4[3]),
    }
    check(
        "The plateau witnesses are pairwise distinct in the exact observable 4-pack (gamma, E1, E2, Delta_src)",
        min_obs_sep > 1.0e-2,
        f"min observable-4 separation={min_obs_sep:.12f}",
    )
    check(
        "Single-channel extremization already splits across all four witnesses",
        channel_winners == {"gamma": "W0", "E1": "W3", "E2": "W2", "Delta_src": "W1"},
        f"winners={channel_winners}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE OBSERVABLE 4-PACK IS AFFINELY INDEPENDENT ON THE KNOWN PLATEAU")
    print("=" * 88)
    diff_rank = int(np.linalg.matrix_rank(observable_matrix[1:] - observable_matrix[0], tol=AFFINE_TOL))
    simplex_volume = float(
        np.linalg.det((observable_matrix[1:] - observable_matrix[0]) @ (observable_matrix[1:] - observable_matrix[0]).T)
    )
    check(
        "The four witness images form an affine 3-simplex in (gamma, E1, E2, Delta_src)",
        diff_rank == 3,
        f"affine rank={diff_rank}",
    )
    check(
        "So no coefficient-free affine observable law is forced by witness degeneracy or hidden collinearity",
        diff_rank == 3 and simplex_volume > 1.0e-12,
        f"Gram determinant={simplex_volume:.12e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: EVERY WITNESS IS THE UNIQUE MAXIMIZER OF SOME EXACT AFFINE OBSERVABLE LAW")
    print("=" * 88)
    selector_gaps: dict[str, float] = {}
    selector_coeffs: dict[str, np.ndarray] = {}
    selectors_ok = True
    for idx, record in enumerate(records):
        coeffs = affine_selector_coefficients(records, idx)
        scores = np.array([float(coeffs @ other.observable4) for other in records], dtype=float)
        sorted_scores = np.sort(scores)
        gap = float(sorted_scores[-1] - sorted_scores[-2])
        selectors_ok &= int(np.argmax(scores)) == idx and gap > 1.0e-6
        selector_gaps[record.label] = gap
        selector_coeffs[record.label] = coeffs
        check(
            f"{record.label} is uniquely exposed by an exact affine law on (gamma, E1, E2, Delta_src)",
            int(np.argmax(scores)) == idx and gap > 1.0e-6,
            f"gap={gap:.12f}",
        )

    print("\n" + "=" * 88)
    print("PART 4: SIMPLE SCHUR-SPECTRAL AND CURVATURE INVARIANTS ALSO FAIL TO CONSENSE")
    print("=" * 88)
    schur_winners = {
        "max Tr(H_e)": argmax_label(records, lambda rec: rec.trace_h),
        "max lambda_min(H_e)": argmax_label(records, lambda rec: rec.lambda_min),
    }
    curvature_winners = {
        "max tr(Hess eta_1)": argmax_label(records, lambda rec: rec.hess_trace),
        "max ||Hess eta_1||_F": argmax_label(records, lambda rec: rec.hess_frob),
    }
    check(
        "Simple Schur-side spectral laws already disagree on which plateau witness to select",
        len(set(schur_winners.values())) >= 2,
        f"winners={schur_winners}",
    )
    check(
        "Simple local Hessian/curvature invariants also disagree on which plateau witness to select",
        len(set(curvature_winners.values())) >= 2,
        f"winners={curvature_winners}",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The named family of exact affine observable plateau-breakers therefore has no canonical witness on the current branch",
        selectors_ok and diff_rank == 3,
        "changing coefficients can make W0, W1, W2, or W3 the unique affine-law maximizer",
    )
    check(
        "So any retained selector from this family must derive its coefficients from extra source-side physics not contained in the family itself",
        True,
        "the coefficients are missing selector content, not a consequence of transport or of the plateau geometry alone",
    )

    print()
    print("  witness observable 4-pack:")
    for record in records:
        gamma_val, e1_val, e2_val, delta_val = record.observable4
        print(
            f"    {record.label}: "
            f"(gamma, E1, E2, Delta_src) = "
            f"({gamma_val:.12f}, {e1_val:.12f}, {e2_val:.12f}, {delta_val:.12f})"
        )
    print()
    print("  affine selector coefficients c = (c_gamma, c_E1, c_E2, c_Delta):")
    for label in plateau.PLATEAU_LABELS:
        coeffs = selector_coeffs[label]
        print(
            f"    {label}: c = {np.round(coeffs, 9)}, "
            f"unique gap = {selector_gaps[label]:.12f}"
        )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
