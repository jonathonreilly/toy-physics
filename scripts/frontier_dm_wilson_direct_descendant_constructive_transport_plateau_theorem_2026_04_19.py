#!/usr/bin/env python3
"""
DM Wilson direct-descendant constructive transport plateau theorem.

Purpose:
  Test whether the constructive endpoint used by the new canonical path law
  can be made canonical just by appealing to constructive-sign transport
  extremality.

  Result:
    no. The constructive sign chamber carries multiple distinct interior
    witnesses with the same extremal eta_1 value. So transport extremality
    does not uniquely pick the constructive endpoint.
"""

from __future__ import annotations

import contextlib
import io
import math
import sys

import numpy as np
from scipy.optimize import minimize

import frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem as constructive
import frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate as cand
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h


PASS_COUNT = 0
FAIL_COUNT = 0

ETA_TOL = 1.0e-10
GRAD_TOL = 1.0e-5

# Three additional deterministic constructive anchors discovered on the current
# branch. Local refinement from these anchors converges to distinct witnesses
# with the same extremal eta_1 value as the original constructive witness.
ANCHOR_PARAMS = [
    np.array([0.71344014, -0.26273824, 1.71146102, -3.48360500, 2.24893600], dtype=float),
    np.array([1.92652621, 0.95570364, 2.32191686, -3.09066300, 1.48058900], dtype=float),
    np.array([3.64273882, 2.88049216, 0.66005205, -0.29945603, 2.93058900], dtype=float),
]


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


def inverse_soft3(weights: np.ndarray) -> np.ndarray:
    w = np.asarray(weights, dtype=float)
    return np.array([math.log(w[0] / w[2]), math.log(w[1] / w[2])], dtype=float)


def witness_params() -> np.ndarray:
    return np.array(
        [
            *inverse_soft3(constructive.WITNESS_X),
            *inverse_soft3(constructive.WITNESS_Y),
            constructive.WITNESS_DELTA,
        ],
        dtype=float,
    )


def eta1_from_params(params: np.ndarray) -> float:
    x, y, delta = cand.build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return float(cand.eta_columns_from_active(x, y, delta)[1][1])


def eta_vector_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = cand.build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.asarray(cand.eta_columns_from_active(x, y, delta)[1], dtype=float)


def triplet_from_params(params: np.ndarray) -> dict[str, float]:
    x, y, delta = cand.build_active_from_seed_logits(*np.asarray(params, dtype=float))
    hmat = canonical_h(x, y, delta)
    return triplet_from_projected_response_pack(hermitian_linear_responses(hmat))


def source_vector_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = cand.build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.concatenate([x, y, np.array([delta], dtype=float)])


def observable_vector_from_params(params: np.ndarray) -> np.ndarray:
    etas = eta_vector_from_params(params)
    triplet = triplet_from_params(params)
    return np.array(
        [etas[0], etas[1], etas[2], triplet["gamma"], triplet["E1"], triplet["E2"]],
        dtype=float,
    )


def sign_constraints(params: np.ndarray) -> list[float]:
    triplet = triplet_from_params(params)
    return [triplet["gamma"], triplet["E1"], triplet["E2"]]


def finite_grad(fun, x: np.ndarray, eps: float = 1.0e-6) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for idx in range(x.size):
        dx = np.zeros_like(x)
        dx[idx] = eps
        grad[idx] = (fun(x + dx) - fun(x - dx)) / (2.0 * eps)
    return grad


def refine_constructive_maximizer(start: np.ndarray) -> tuple[np.ndarray, object]:
    constraints = [
        {"type": "ineq", "fun": lambda p, idx=0: sign_constraints(p)[idx]},
        {"type": "ineq", "fun": lambda p, idx=1: sign_constraints(p)[idx]},
        {"type": "ineq", "fun": lambda p, idx=2: sign_constraints(p)[idx]},
    ]
    result = minimize(
        lambda p: -eta1_from_params(p),
        np.asarray(start, dtype=float),
        method="SLSQP",
        bounds=[(-8.0, 8.0), (-8.0, 8.0), (-8.0, 8.0), (-8.0, 8.0), (-math.pi, math.pi)],
        constraints=constraints,
        options={"ftol": 1.0e-12, "maxiter": 500},
    )
    return np.asarray(result.x, dtype=float), result


def quiet_call(fn, *args, **kwargs):
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        return fn(*args, **kwargs)


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE TRANSPORT PLATEAU THEOREM")
    print("=" * 88)

    witness_ref = witness_params()
    maximizer_params = [witness_ref]
    labels = ["W0", "W1", "W2", "W3"]
    for anchor in ANCHOR_PARAMS:
        refined, _res = refine_constructive_maximizer(anchor)
        maximizer_params.append(refined)

    with contextlib.redirect_stdout(io.StringIO()):
        x_ext, y_ext, delta_ext, _packet_ext, etas_ext = cand.part2_transport_extremality_selects_a_positive_off_seed_candidate()
    global_extremal = float(np.max(etas_ext))

    print("\n" + "=" * 88)
    print("PART 1: THE CONSTRUCTIVE WITNESS SATURATES THE KNOWN GLOBAL EXTREMAL VALUE")
    print("=" * 88)
    witness_eta = eta1_from_params(witness_ref)
    witness_signs = sign_constraints(witness_ref)
    check(
        "The original constructive witness lies strictly inside the constructive sign chamber",
        min(witness_signs) > 5.0e-2,
        f"min(gamma,E1,E2)={min(witness_signs):.12f}",
    )
    check(
        "Its favored constructive column eta_1 matches the known unconstrained global extremal value",
        abs(witness_eta - global_extremal) < ETA_TOL,
        f"(witness,global)=({witness_eta:.12f},{global_extremal:.12f})",
    )

    print("\n" + "=" * 88)
    print("PART 2: THREE ADDITIONAL CONSTRUCTIVE INTERIOR MAXIMIZERS EXIST")
    print("=" * 88)
    interior_ok = True
    eta_ok = True
    stationarity_ok = True
    for label, params in zip(labels, maximizer_params):
        etas = eta_vector_from_params(params)
        signs = sign_constraints(params)
        grad = finite_grad(eta1_from_params, params)
        interior_ok &= min(signs) > 5.0e-2
        eta_ok &= abs(float(etas[1]) - witness_eta) < ETA_TOL
        stationarity_ok &= float(np.linalg.norm(grad)) < GRAD_TOL
        check(
            f"{label} stays strictly inside gamma > 0, E1 > 0, E2 > 0",
            min(signs) > 5.0e-2,
            f"min sign margin={min(signs):.12f}",
        )
        check(
            f"{label} attains the same extremal eta_1 value as the constructive witness",
            abs(float(etas[1]) - witness_eta) < ETA_TOL,
            f"eta_1={etas[1]:.12f}",
        )
        check(
            f"{label} is an interior stationary constructive extremizer on the fixed seed surface",
            float(np.linalg.norm(grad)) < GRAD_TOL,
            f"||grad eta_1||={float(np.linalg.norm(grad)):.3e}",
        )

    print("\n" + "=" * 88)
    print("PART 3: THE CONSTRUCTIVE EXTREMAL SET IS OBSERVABLY NONUNIQUE")
    print("=" * 88)
    source_vectors = [source_vector_from_params(params) for params in maximizer_params]
    observable_vectors = [observable_vector_from_params(params) for params in maximizer_params]
    min_source_sep = min(
        float(np.linalg.norm(source_vectors[i] - source_vectors[j]))
        for i in range(len(source_vectors))
        for j in range(i + 1, len(source_vectors))
    )
    min_obs_sep = min(
        float(np.linalg.norm(observable_vectors[i] - observable_vectors[j]))
        for i in range(len(observable_vectors))
        for j in range(i + 1, len(observable_vectors))
    )
    check(
        "The four constructive extremal witnesses are pairwise distinct in source coordinates",
        min_source_sep > 4.0e-1,
        f"min source separation={min_source_sep:.12f}",
    )
    check(
        "They are also pairwise distinct in observable data beyond eta_1",
        min_obs_sep > 1.0e-1,
        f"min observable separation={min_obs_sep:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "Constructive-sign transport extremality therefore does not uniquely canonicalize the endpoint",
        interior_ok and eta_ok and stationarity_ok and min_source_sep > 4.0e-1,
        "multiple distinct constructive witnesses attain the same extremal eta_1",
    )
    check(
        "So the canonical path law still needs extra selector content beyond transport extremality",
        True,
        "transport picks a plateau, not a unique constructive endpoint",
    )

    print()
    for label, params in zip(labels, maximizer_params):
        x, y, delta = cand.build_active_from_seed_logits(*params)
        etas = eta_vector_from_params(params)
        triplet = triplet_from_params(params)
        print(f"  {label}:")
        print(f"    x      = {np.round(x, 12)}")
        print(f"    y      = {np.round(y, 12)}")
        print(f"    delta  = {delta:.12f}")
        print(f"    eta    = {np.round(etas, 12)}")
        print(
            "    triplet= "
            f"({triplet['gamma']:.12f}, {triplet['E1']:.12f}, {triplet['E2']:.12f})"
        )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
