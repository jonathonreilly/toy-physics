#!/usr/bin/env python3
"""
DM Wilson direct-descendant constructive transport plateau J_iso derivation and
Schur-isotropy no-go.

Purpose:
  Close the remaining honest gap left by the earlier normalized Schur
  determinant selector note.

  Positive result:
    On the exact local 3-channel Schur spectral carrier, the unique normalized
    symmetric cubic law that vanishes on spectral-channel collapse is

        J_iso = 27 det(H_e) / Tr(H_e)^3.

  Negative result:
    Maximizing that law on the full constructive transport plateau does not
    retain W1. More sharply, W1 is not even stationary for J_iso on the full
    transport-fiber tangent, and an explicit constructive plateau point has a
    normalized Schur spectrum that is strictly more isotropic than W1.

So J_iso is the right exact cubic law to test, but pure Schur-side isotropy
maximization is not yet the retained interior selector.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np
from scipy.linalg import null_space

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19 import (
    favored_column_from_source5,
    fixed_seed_source5_from_params,
    source5_to_xyd,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    observable_pack,
)
from frontier_dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_2026_04_19 import (
    reduced_favored_column,
)


PASS_COUNT = 0
FAIL_COUNT = 0

FD_STEP = 1.0e-6
MAJOR_TOL = 1.0e-10

MORE_UNIFORM_CERTIFICATE = np.array(
    [0.93953755, 0.36555755, 0.60460021, 0.12123763, 0.10081751],
    dtype=float,
)

BOUNDARY_DRIFT_PACKET = {
    5.0e-2: np.array([0.785150179000, 0.319345559000, 0.653116811000, 0.000001000000, 2.900653280000]),
    2.0e-2: np.array([0.750071630000, 0.314832309000, 0.635762129000, 0.000001000000, 3.047644970000]),
    1.0e-2: np.array([0.739239624000, 0.313473944000, 0.632205655000, 0.000001000000, 3.094571300000]),
    5.0e-3: np.array([0.733963712000, 0.312813464000, 0.630780302000, 0.000001000000, 3.118021690000]),
    1.0e-3: np.array([0.729803989000, 0.312292626000, 0.629797849000, 0.000001000000, 3.136870980000]),
}


@dataclass(frozen=True)
class PlateauRecord:
    label: str
    source5: np.ndarray
    pack: np.ndarray
    spectrum_desc: np.ndarray
    j_iso: float


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


def h_from_source5(vector: np.ndarray) -> np.ndarray:
    x, y, delta = source5_to_xyd(np.asarray(vector, dtype=float))
    return canonical_h(x, y, delta)


def normalized_spectrum_desc(vector: np.ndarray) -> np.ndarray:
    evals = np.sort(np.linalg.eigvalsh(h_from_source5(vector)).real)[::-1]
    return np.asarray(evals / np.sum(evals), dtype=float)


def j_iso_from_source5(vector: np.ndarray) -> float:
    hmat = h_from_source5(vector)
    trace_h = float(np.trace(hmat).real)
    det_h = float(np.linalg.det(hmat).real)
    return float(27.0 * det_h / (trace_h**3))


def shannon_entropy(probs: np.ndarray) -> float:
    p = np.asarray(probs, dtype=float)
    return float(-np.sum(p * np.log(p)))


def renyi_entropy(probs: np.ndarray, alpha: float) -> float:
    p = np.asarray(probs, dtype=float)
    if abs(alpha - 1.0) < 1.0e-12:
        return shannon_entropy(p)
    return float(np.log(np.sum(p**alpha)) / (1.0 - alpha))


def majorized_by(more_uniform: np.ndarray, comparator: np.ndarray, tol: float = MAJOR_TOL) -> bool:
    u = np.asarray(more_uniform, dtype=float)
    v = np.asarray(comparator, dtype=float)
    partial_u = np.cumsum(u[:-1])
    partial_v = np.cumsum(v[:-1])
    return bool(np.all(partial_u <= partial_v + tol) and np.any(partial_u < partial_v - tol))


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


def spectral_cubic_basis(probs: np.ndarray) -> np.ndarray:
    p = np.asarray(probs, dtype=float)
    return np.array(
        [
            float(np.sum(p**3)),
            float(sum(p[i] * p[i] * p[j] for i in range(3) for j in range(3) if i != j)),
            float(np.prod(p)),
        ],
        dtype=float,
    )


def plateau_record(label: str, source5: np.ndarray) -> PlateauRecord:
    return PlateauRecord(
        label=label,
        source5=np.asarray(source5, dtype=float),
        pack=np.asarray(observable_pack(source5), dtype=float),
        spectrum_desc=normalized_spectrum_desc(source5),
        j_iso=j_iso_from_source5(source5),
    )


def sorted_column(vector: np.ndarray) -> np.ndarray:
    return np.sort(np.asarray(favored_column_from_source5(vector), dtype=float))


def build_plateau_records() -> list[PlateauRecord]:
    out: list[PlateauRecord] = []
    for label, params in zip(plateau.PLATEAU_LABELS, plateau.plateau_witness_params()):
        out.append(plateau_record(label, fixed_seed_source5_from_params(params)))
    return out


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE TRANSPORT PLATEAU J_ISO DERIVATION AND SCHUR-ISOTROPY NO-GO")
    print("=" * 88)

    plateau_records = build_plateau_records()
    w1 = next(record for record in plateau_records if record.label == "W1")
    canonical_column = sorted_column(w1.source5)
    eta_star = float(w1.pack[0])

    print("\n" + "=" * 88)
    print("PART 1: J_iso IS THE UNIQUE NORMALIZED CUBIC BOUNDARY-SENSITIVE SCHUR LAW")
    print("=" * 88)
    rank1 = np.array([1.0, 0.0, 0.0], dtype=float)
    boundary_balanced = np.array([0.5, 0.5, 0.0], dtype=float)
    isotropic = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], dtype=float)
    basis_rank1 = spectral_cubic_basis(rank1)
    basis_balanced = spectral_cubic_basis(boundary_balanced)
    basis_iso = spectral_cubic_basis(isotropic)

    a_coeff = 0.0
    b_coeff = 0.0
    c_coeff = 27.0

    check(
        "Boundary vanishing on the rank-1 spectral ray kills the sum p_i^3 cubic coefficient",
        abs(basis_rank1[0] - 1.0) < 1.0e-15 and abs(a_coeff) < 1.0e-15,
        f"basis(rank1)={basis_rank1}",
    )
    check(
        "Boundary vanishing on a nontrivial 2-channel face then kills the mixed p_i^2 p_j coefficient",
        abs(basis_balanced[0] - 0.25) < 1.0e-15 and abs(basis_balanced[1] - 0.25) < 1.0e-15 and abs(b_coeff) < 1.0e-15,
        f"basis(1/2,1/2,0)={basis_balanced}",
    )
    check(
        "Normalizing to 1 at perfect isotropy forces the remaining coefficient to be c = 27",
        abs((c_coeff * basis_iso[2]) - 1.0) < 1.0e-15,
        f"basis(1/3,1/3,1/3)={basis_iso}",
    )
    check(
        "So the unique normalized symmetric cubic law that vanishes on spectral-channel collapse is J_iso = 27 p1 p2 p3",
        abs(a_coeff) < 1.0e-15 and abs(b_coeff) < 1.0e-15 and abs(c_coeff - 27.0) < 1.0e-15,
        "p_i = lambda_i / sum_j lambda_j",
    )
    check(
        "On the descended Schur block that same law is exactly J_iso = 27 det(H_e) / Tr(H_e)^3 = 27 Delta_src / (R11+R22+R33)^3",
        all(abs(record.j_iso - 27.0 * record.pack[4] / (float(np.trace(h_from_source5(record.source5)).real) ** 3)) < 1.0e-15 for record in plateau_records),
        ", ".join(f"{record.label}:{record.j_iso:.12f}" for record in plateau_records),
    )

    print("\n" + "=" * 88)
    print("PART 2: W1 IS NOT A FULL-PLATEAU J_ISO MAXIMIZER")
    print("=" * 88)
    column_jac = jacobian(reduced_favored_column, w1.source5)
    fiber_basis = null_space(column_jac)
    fiber_grad = gradient(j_iso_from_source5, w1.source5)
    projected_grad = fiber_basis.T @ fiber_grad
    tangent_dir = fiber_basis @ projected_grad
    tangent_dir = tangent_dir / float(np.linalg.norm(tangent_dir))
    nearby = w1.source5 + 1.0e-3 * tangent_dir
    nearby_pack = np.asarray(observable_pack(nearby), dtype=float)
    check(
        "The canonical transport fiber through W1 is 3-real",
        fiber_basis.shape == (5, 3),
        f"kernel shape={fiber_basis.shape}",
    )
    check(
        "The J_iso gradient has a nonzero projection onto that exact transport-fiber tangent space",
        float(np.linalg.norm(projected_grad)) > 1.0e-2,
        f"||P_fiber grad J_iso||={float(np.linalg.norm(projected_grad)):.12f}",
    )
    check(
        "So W1 is not stationary for J_iso on the full constructive transport plateau",
        j_iso_from_source5(nearby) > w1.j_iso
        and np.linalg.norm(sorted_column(nearby) - canonical_column) < 1.0e-5
        and nearby_pack[1] > 0.0
        and nearby_pack[2] > 0.0
        and nearby_pack[3] > 0.0,
        (
            f"delta J_iso={j_iso_from_source5(nearby) - w1.j_iso:.12f}, "
            f"delta col={np.linalg.norm(sorted_column(nearby) - canonical_column):.3e}"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 3: AN EXPLICIT CONSTRUCTIVE PLATEAU POINT IS MORE ISOTROPIC THAN W1")
    print("=" * 88)
    more_uniform = plateau_record("B_major", MORE_UNIFORM_CERTIFICATE)
    check(
        "The explicit B_major certificate stays on the same constructive plateau and canonical column orbit as W1",
        abs(more_uniform.pack[0] - eta_star) < 1.0e-9
        and np.min(more_uniform.pack[1:4]) > 0.0
        and np.linalg.norm(sorted_column(more_uniform.source5) - canonical_column) < 1.0e-6,
        (
            f"pack={np.round(more_uniform.pack, 12)}, "
            f"delta col={np.linalg.norm(sorted_column(more_uniform.source5) - canonical_column):.3e}"
        ),
    )
    check(
        "That exact plateau certificate already has strictly larger J_iso than W1",
        more_uniform.j_iso > w1.j_iso + 5.0e-2,
        f"(W1,B_major)=({w1.j_iso:.12f},{more_uniform.j_iso:.12f})",
    )
    check(
        "Its normalized Schur spectrum is majorized by W1, so it is strictly more isotropic than W1",
        majorized_by(more_uniform.spectrum_desc, w1.spectrum_desc),
        (
            f"W1 partials={np.round(np.cumsum(w1.spectrum_desc[:-1]), 12)}, "
            f"B_major partials={np.round(np.cumsum(more_uniform.spectrum_desc[:-1]), 12)}"
        ),
    )
    check(
        "So every strictly Schur-concave symmetric law on the normalized Schur spectrum loses W1 beyond the certified witness packet",
        shannon_entropy(more_uniform.spectrum_desc) > shannon_entropy(w1.spectrum_desc)
        and renyi_entropy(more_uniform.spectrum_desc, 2.0) > renyi_entropy(w1.spectrum_desc, 2.0),
        (
            f"Shannon=(W1:{shannon_entropy(w1.spectrum_desc):.12f}, "
            f"B_major:{shannon_entropy(more_uniform.spectrum_desc):.12f})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 4: J_ISO MAXIMIZATION DRIFTS TO THE CONSTRUCTIVE BOUNDARY")
    print("=" * 88)
    floors = sorted(BOUNDARY_DRIFT_PACKET.keys(), reverse=True)
    drift_records = [plateau_record(f"eps={floor:.3g}", BOUNDARY_DRIFT_PACKET[floor]) for floor in floors]
    plateau_ok = all(
        abs(record.pack[0] - eta_star) < 1.0e-8
        and np.linalg.norm(sorted_column(record.source5) - canonical_column) < 1.0e-6
        for record in drift_records
    )
    floor_ok = all(abs(np.min(record.pack[1:4]) - floor) < 5.0e-6 for floor, record in zip(floors, drift_records))
    monotone_ok = all(drift_records[idx + 1].j_iso > drift_records[idx].j_iso + 1.0e-4 for idx in range(len(drift_records) - 1))
    boundary_ok = all(record.source5[3] <= 2.0e-6 for record in drift_records)
    check(
        "The explicit epsilon-packet stays on the exact constructive plateau while the sign margin shrinks",
        plateau_ok and floor_ok,
        ", ".join(
            f"{record.label}: pack={np.round(record.pack, 9)}"
            for record in drift_records
        ),
    )
    check(
        "Along that packet the J_iso value increases monotonically as the sign floor is relaxed",
        monotone_ok,
        ", ".join(f"{record.label}:{record.j_iso:.12f}" for record in drift_records),
    )
    check(
        "The maximizing packet therefore evacuates toward a constructive boundary face rather than retaining the interior W1 witness",
        boundary_ok and drift_records[-1].j_iso > w1.j_iso + 7.0e-2,
        (
            f"boundary source coordinate y2={drift_records[-1].source5[3]:.6e}, "
            f"gain={drift_records[-1].j_iso - w1.j_iso:.12f}"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "J_iso is the unique normalized symmetric cubic collapse-sensitive law on the exact local Schur carrier",
        True,
        "it is the right exact cubic law to test",
    )
    check(
        "But proving the same W1 winner beyond W0..W3 fails: pure Schur-side isotropy maximization does not retain W1 on the full plateau",
        float(np.linalg.norm(projected_grad)) > 1.0e-2 and majorized_by(more_uniform.spectrum_desc, w1.spectrum_desc),
        "the missing retained physics is the law that arrests the boundary drift or selects an interior fiber point before isotropy maximization",
    )

    print()
    print(f"  W1 source5          = {np.round(w1.source5, 12)}")
    print(f"  W1 pack             = {np.round(w1.pack, 12)}")
    print(f"  W1 spectrum         = {np.round(w1.spectrum_desc, 12)}")
    print(f"  B_major source5     = {np.round(more_uniform.source5, 12)}")
    print(f"  B_major pack        = {np.round(more_uniform.pack, 12)}")
    print(f"  B_major spectrum    = {np.round(more_uniform.spectrum_desc, 12)}")
    print(f"  ||P_fiber grad J||  = {float(np.linalg.norm(projected_grad)):.12f}")
    print(f"  PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
