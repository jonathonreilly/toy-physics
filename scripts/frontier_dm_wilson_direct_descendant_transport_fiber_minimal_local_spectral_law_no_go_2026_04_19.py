#!/usr/bin/env python3
"""
DM Wilson direct-descendant transport-fiber minimal local spectral-law no-go.

Purpose:
  Starting from the completed local spectral coordinates

      (T, Q, Delta) = (Tr(H_e), Tr(H_e^2), det(H_e)),

  test whether a minimal exact law on those three local scalars can select the
  current interior physical source candidate W1 against the explicit
  boundary-drifting competitors already known on the constructive transport
  plateau.

Result:
  1. no single completed scalar selects W1 against the explicit competitor
     set;
  2. any scale-free law factors through the normalized pair
         (q2, q3) = (Q / T^2, Delta / T^3),
     and that normalized map has rank 2 on the 3-real transport fiber, so
     canonically normalized laws are under-complete locally;
  3. among positive coefficient-free monomials of total degree <= 2, the
     unique minimal packet-separating law is
         Q Delta = Tr(H_e^2) det(H_e);
  4. but raw affine and monomial laws are too rigid to be exact interior
     selectors: because (T, Q, Delta) are local coordinates on the transport
     fiber, any nonconstant affine law or nontrivial monomial has nonzero
     fiber gradient at every positive interior point.

So the completed spectral data are explicit, but no natural low-complexity
exact selector law is found in the normalized, affine, or monomial classes.
"""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import linprog

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19 import (
    fixed_seed_source5_from_params,
)
from frontier_dm_wilson_direct_descendant_constructive_transport_plateau_j_iso_derivation_and_schur_isotropy_no_go_2026_04_19 import (
    BOUNDARY_DRIFT_PACKET,
    MORE_UNIFORM_CERTIFICATE,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    observable_pack,
)
from frontier_dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_2026_04_19 import (
    reduced_favored_column,
    spectral_invariants,
)


PASS_COUNT = 0
FAIL_COUNT = 0

FD_STEP = 1.0e-6
RANK_TOL = 1.0e-8
RAW_COORD_TOL = 1.0e-4
NORM_COORD_TOL = 5.0e-4
LOCAL_ASCENT_STEP = 1.0e-3
AFFINE_MARGIN = 1.0


@dataclass(frozen=True)
class Record:
    label: str
    source5: np.ndarray
    pack: np.ndarray
    invariants: np.ndarray
    normalized_pair: np.ndarray

    @property
    def t(self) -> float:
        return float(self.invariants[0])

    @property
    def q(self) -> float:
        return float(self.invariants[1])

    @property
    def delta(self) -> float:
        return float(self.invariants[2])

    @property
    def q2(self) -> float:
        return float(self.normalized_pair[0])

    @property
    def q3(self) -> float:
        return float(self.normalized_pair[1])

    @property
    def q_delta(self) -> float:
        return float(self.q * self.delta)


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


def jacobian(fun, vector: np.ndarray, step: float = FD_STEP) -> np.ndarray:
    vector = np.asarray(vector, dtype=float)
    value = np.asarray(fun(vector), dtype=float)
    out = np.zeros((value.size, vector.size), dtype=float)
    for idx in range(vector.size):
        dv = np.zeros_like(vector)
        dv[idx] = step
        out[:, idx] = (np.asarray(fun(vector + dv), dtype=float) - np.asarray(fun(vector - dv), dtype=float)) / (
            2.0 * step
        )
    return out


def gradient(fun, vector: np.ndarray, step: float = FD_STEP) -> np.ndarray:
    vector = np.asarray(vector, dtype=float)
    out = np.zeros_like(vector)
    for idx in range(vector.size):
        dv = np.zeros_like(vector)
        dv[idx] = step
        out[idx] = (fun(vector + dv) - fun(vector - dv)) / (2.0 * step)
    return out


def normalized_pair_from_source5(vector: np.ndarray) -> np.ndarray:
    t, q, delta = spectral_invariants(vector)
    return np.array([q / (t**2), delta / (t**3)], dtype=float)


def q_delta_law(vector: np.ndarray) -> float:
    _t, q, delta = spectral_invariants(vector)
    return float(q * delta)


def build_record(label: str, source5: np.ndarray) -> Record:
    source5 = np.asarray(source5, dtype=float)
    return Record(
        label=label,
        source5=source5,
        pack=np.asarray(observable_pack(source5), dtype=float),
        invariants=np.asarray(spectral_invariants(source5), dtype=float),
        normalized_pair=normalized_pair_from_source5(source5),
    )


def plateau_records() -> list[Record]:
    return [
        build_record(label, fixed_seed_source5_from_params(params))
        for label, params in zip(plateau.PLATEAU_LABELS, plateau.plateau_witness_params())
    ]


def explicit_records() -> list[Record]:
    records = plateau_records()
    records.append(build_record("B_major", MORE_UNIFORM_CERTIFICATE))
    for floor in sorted(BOUNDARY_DRIFT_PACKET.keys(), reverse=True):
        records.append(build_record(f"eps={floor:g}", BOUNDARY_DRIFT_PACKET[floor]))
    return records


def monomial_value(invariants: np.ndarray, exponents: tuple[int, int, int]) -> float:
    t, q, delta = np.asarray(invariants, dtype=float)
    a_exp, b_exp, c_exp = exponents
    return float((t**a_exp) * (q**b_exp) * (delta**c_exp))


def monomial_winners(records: list[Record], max_degree: int) -> dict[int, list[tuple[tuple[int, int, int], str, float]]]:
    winners: dict[int, list[tuple[tuple[int, int, int], str, float]]] = {degree: [] for degree in range(1, max_degree + 1)}
    labels = [record.label for record in records]
    by_label = {record.label: record for record in records}
    for degree in range(1, max_degree + 1):
        for a_exp in range(degree + 1):
            for b_exp in range(degree + 1 - a_exp):
                c_exp = degree - a_exp - b_exp
                exponents = (a_exp, b_exp, c_exp)
                scores = {
                    label: monomial_value(by_label[label].invariants, exponents)
                    for label in labels
                }
                ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
                winners[degree].append((exponents, ordered[0][0], float(ordered[0][1] - ordered[1][1])))
    return winners


def normalized_monomial_winners(records: list[Record], max_degree: int) -> list[tuple[tuple[int, int], str]]:
    out: list[tuple[tuple[int, int], str]] = []
    for degree in range(1, max_degree + 1):
        for a_exp in range(degree + 1):
            b_exp = degree - a_exp
            if a_exp == 0 and b_exp == 0:
                continue
            scores = {
                record.label: float((record.q2**a_exp) * (record.q3**b_exp))
                for record in records
            }
            winner = max(scores.items(), key=lambda item: item[1])[0]
            out.append(((a_exp, b_exp), winner))
    return out


def affine_separator(target_label: str, records: list[Record]) -> tuple[np.ndarray | None, float]:
    target = next(record for record in records if record.label == target_label)
    constraints = []
    bounds = []
    for record in records:
        if record.label == target_label:
            continue
        constraints.append(record.invariants - target.invariants)
        bounds.append(-AFFINE_MARGIN)
    result = linprog(
        c=np.zeros(3, dtype=float),
        A_ub=np.asarray(constraints, dtype=float),
        b_ub=np.asarray(bounds, dtype=float),
        bounds=[(None, None), (None, None), (None, None)],
        method="highs",
    )
    if not result.success:
        return None, 0.0
    scores = {
        record.label: float(result.x @ record.invariants)
        for record in records
    }
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return np.asarray(result.x, dtype=float), float(ordered[0][1] - ordered[1][1])


def fiber_basis(vector: np.ndarray) -> np.ndarray:
    return null_space(jacobian(reduced_favored_column, vector))


def unique_winner(weights: np.ndarray, records: list[Record]) -> tuple[str, float]:
    scores = {
        record.label: float(np.asarray(weights, dtype=float) @ record.invariants)
        for record in records
    }
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ordered[0][0], float(ordered[0][1] - ordered[1][1])


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT TRANSPORT-FIBER MINIMAL LOCAL SPECTRAL-LAW NO-GO")
    print("=" * 88)

    plateau_packet = plateau_records()
    explicit_packet = explicit_records()
    w1 = next(record for record in plateau_packet if record.label == "W1")
    boundary_packet = [record for record in explicit_packet if record.label.startswith("eps=")]

    print("\n" + "=" * 88)
    print("PART 1: NO SINGLE COMPLETED SPECTRAL SCALAR PICKS W1")
    print("=" * 88)
    t_winner = max(explicit_packet, key=lambda record: record.t)
    q_winner = max(explicit_packet, key=lambda record: record.q)
    delta_winner = max(explicit_packet, key=lambda record: record.delta)
    q3_winner = max(explicit_packet, key=lambda record: record.q3)
    check(
        "No single raw completed scalar in (T, Q, Delta) selects W1 on the explicit competitor set",
        t_winner.label != "W1" and q_winner.label != "W1" and delta_winner.label != "W1",
        f"max T={t_winner.label}, max Q={q_winner.label}, max Delta={delta_winner.label}",
    )
    check(
        "The canonical normalized determinant ratio q3 = Delta / T^3 still prefers a boundary-drifting competitor to W1",
        q3_winner.label != "W1" and q3_winner.q3 > w1.q3,
        f"max q3={q3_winner.label}, (W1,max)=({w1.q3:.12f},{q3_winner.q3:.12f})",
    )

    print("\n" + "=" * 88)
    print("PART 2: SCALE-FREE LOCAL SPECTRAL LAWS ARE UNDER-COMPLETE")
    print("=" * 88)
    raw_coord_ok = True
    raw_coord_min_sv = float("inf")
    norm_coord_ok = True
    norm_coord_min_sv = float("inf")
    for record in plateau_packet:
        basis = fiber_basis(record.source5)
        raw_jac = jacobian(spectral_invariants, record.source5) @ basis
        raw_sv = np.linalg.svd(raw_jac, compute_uv=False)
        raw_coord_ok &= raw_jac.shape == (3, 3) and int(np.sum(raw_sv > RANK_TOL)) == 3
        raw_coord_min_sv = min(raw_coord_min_sv, float(np.min(raw_sv)))

        norm_jac = jacobian(normalized_pair_from_source5, record.source5) @ basis
        norm_sv = np.linalg.svd(norm_jac, compute_uv=False)
        norm_coord_ok &= norm_jac.shape == (2, 3) and int(np.sum(norm_sv > RANK_TOL)) == 2
        norm_coord_min_sv = min(norm_coord_min_sv, float(np.min(norm_sv)))

    normalized_degree_winners = normalized_monomial_winners(explicit_packet, max_degree=4)
    normalized_w1_winners = [exponents for exponents, winner in normalized_degree_winners if winner == "W1"]
    check(
        "Restricted to the 3-real transport fiber, the raw spectral completion (T, Q, Delta) remains a full local coordinate chart",
        raw_coord_ok and raw_coord_min_sv > RAW_COORD_TOL,
        f"min restricted raw singular value={raw_coord_min_sv:.12e}",
    )
    check(
        "After canonical scale normalization, only the 2-scalar pair (Q/T^2, Delta/T^3) survives locally on that fiber",
        norm_coord_ok and norm_coord_min_sv > NORM_COORD_TOL,
        f"min restricted normalized singular value={norm_coord_min_sv:.12e}",
    )
    check(
        "So every scale-free local spectral law leaves a 1-real local degeneracy and cannot exactly isolate an interior source",
        raw_coord_ok and norm_coord_ok,
        "rank(T,Q,Delta)|fiber = 3, rank(Q/T^2,Delta/T^3)|fiber = 2",
    )
    check(
        "Positive normalized monomials in (Q/T^2, Delta/T^3) of total degree <= 4 do not even beat the explicit boundary competitors",
        len(normalized_w1_winners) == 0,
        f"W1-winning normalized monomials={normalized_w1_winners}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE MINIMAL COEFFICIENT-FREE PACKET-SEPARATING MONOMIAL IS Q Delta")
    print("=" * 88)
    degree_winners = monomial_winners(explicit_packet, max_degree=3)
    degree1_w1 = [item for item in degree_winners[1] if item[1] == "W1"]
    degree2_w1 = [item for item in degree_winners[2] if item[1] == "W1"]
    q_delta_gap = w1.q_delta - max(record.q_delta for record in explicit_packet if record.label != "W1")
    boundary_monotone = all(
        boundary_packet[idx + 1].q_delta < boundary_packet[idx].q_delta - 1.0e-4
        for idx in range(len(boundary_packet) - 1)
    )
    check(
        "No positive coefficient-free monomial of total degree 1 in (T, Q, Delta) selects W1",
        len(degree1_w1) == 0,
        f"degree-1 winners={[(exp, winner) for exp, winner, _gap in degree_winners[1]]}",
    )
    check(
        "The unique positive coefficient-free degree-2 monomial that selects W1 on the explicit competitor set is Q Delta",
        len(degree2_w1) == 1 and degree2_w1[0][0] == (0, 1, 1),
        f"degree-2 W1 winners={degree2_w1}",
    )
    check(
        "That minimal monomial beats B_major and the whole explicit boundary-drift packet",
        q_delta_gap > 3.0e-3,
        f"top gap={q_delta_gap:.12f}, W1 QDelta={w1.q_delta:.12f}",
    )
    check(
        "Along the explicit boundary-evacuation packet, Q Delta decreases as the sign floor shrinks",
        boundary_monotone,
        ", ".join(f"{record.label}:{record.q_delta:.12f}" for record in boundary_packet),
    )

    print("\n" + "=" * 88)
    print("PART 4: COEFFICIENT FREEDOM CAN EXPOSE WHICHEVER POINT ONE ASKS FOR")
    print("=" * 88)
    w1_affine, w1_gap = affine_separator("W1", explicit_packet)
    bmajor_affine, bmajor_gap = affine_separator("B_major", explicit_packet)
    w1_affine_winner = unique_winner(w1_affine, explicit_packet) if w1_affine is not None else ("", 0.0)
    bmajor_affine_winner = unique_winner(bmajor_affine, explicit_packet) if bmajor_affine is not None else ("", 0.0)
    check(
        "An affine law in the raw spectral invariants can be tuned to select W1 on the finite competitor set",
        w1_affine is not None and w1_affine_winner[0] == "W1" and w1_gap > 0.5,
        f"weights={np.round(w1_affine, 6) if w1_affine is not None else None}",
    )
    check(
        "The same affine family can also be tuned to select a different explicit competitor, so its coefficients are extra selector input",
        bmajor_affine is not None and bmajor_affine_winner[0] == "B_major" and bmajor_gap > 0.5,
        f"weights={np.round(bmajor_affine, 6) if bmajor_affine is not None else None}",
    )
    check(
        "Because (T, Q, Delta) are local transport-fiber coordinates, no nonconstant affine law can have an interior exact maximum there",
        raw_coord_ok and raw_coord_min_sv > RAW_COORD_TOL,
        "grad(a T + b Q + c Delta + r) = (a,b,c) and vanishes only for the constant law",
    )

    print("\n" + "=" * 88)
    print("PART 5: THE MINIMAL MONOMIAL CANDIDATE IS STILL NOT AN EXACT SELECTOR")
    print("=" * 88)
    basis_w1 = fiber_basis(w1.source5)
    q_delta_grad = gradient(q_delta_law, w1.source5)
    projected_grad = basis_w1.T @ q_delta_grad
    ascent_direction = basis_w1 @ projected_grad
    ascent_direction = ascent_direction / float(np.linalg.norm(ascent_direction))
    nearby = w1.source5 + LOCAL_ASCENT_STEP * ascent_direction
    nearby_pack = np.asarray(observable_pack(nearby), dtype=float)
    nearby_q_delta = q_delta_law(nearby)
    nearby_col_drift = float(np.linalg.norm(reduced_favored_column(nearby) - reduced_favored_column(w1.source5)))
    nearby_eta_drift = float(abs(nearby_pack[0] - w1.pack[0]))
    check(
        "The minimal monomial Q Delta has nonzero projected gradient on the exact transport fiber through W1",
        float(np.linalg.norm(projected_grad)) > 1.0e-3,
        f"||P_fiber grad(QDelta)||={float(np.linalg.norm(projected_grad)):.12f}",
    )
    check(
        "A small transport-fiber ascent step increases Q Delta while preserving eta_1 and the favored column to first order and staying constructive",
        nearby_q_delta > w1.q_delta + 1.0e-5
        and nearby_col_drift < 5.0e-6
        and nearby_eta_drift < 1.0e-8
        and np.min(nearby_pack[1:4]) > 0.0,
        (
            f"delta(QDelta)={nearby_q_delta - w1.q_delta:.12f}, "
            f"delta_col={nearby_col_drift:.3e}, delta_eta={nearby_eta_drift:.3e}"
        ),
    )
    check(
        "So no nontrivial raw monomial law can be an exact interior selector on the completed spectral fiber",
        raw_coord_ok and float(np.linalg.norm(projected_grad)) > 1.0e-3,
        "grad(T^a Q^b Delta^c) = law * (a/T, b/Q, c/Delta), hence it never vanishes at a positive interior point unless the law is constant",
    )

    print("\n" + "=" * 88)
    print("PART 6: BOTTOM LINE")
    print("=" * 88)
    check(
        "The completed spectral data identify the live local selector coordinates but not a natural exact low-complexity selector law",
        len(degree2_w1) == 1 and norm_coord_ok and raw_coord_ok and float(np.linalg.norm(projected_grad)) > 1.0e-3,
        "minimal packet-separator = Q Delta; exact low-complexity normalized/affine/monomial selector = no-go",
    )

    print()
    print(f"  W1 invariants                 = {np.round(w1.invariants, 12)}")
    print(f"  W1 normalized pair            = {np.round(w1.normalized_pair, 12)}")
    print(f"  W1 minimal candidate QDelta   = {w1.q_delta:.12f}")
    print(f"  best explicit rival QDelta    = {max(record.q_delta for record in explicit_packet if record.label != 'W1'):.12f}")
    print(f"  affine W1 weights             = {np.round(w1_affine, 12) if w1_affine is not None else None}")
    print(f"  affine B_major weights        = {np.round(bmajor_affine, 12) if bmajor_affine is not None else None}")
    print(f"  ||P_fiber grad(QDelta)||      = {float(np.linalg.norm(projected_grad)):.12f}")
    print(f"  nearby ascent pack            = {np.round(nearby_pack, 12)}")
    print(f"  PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
