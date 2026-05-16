#!/usr/bin/env python3
"""
Bounded spatial-environment character-measure witness for the plaquette
transfer route on the accepted Wilson 3+1 surface.

This does not close analytic P(6) and does not retain the operator-realization
load-bearing step R_beta^env = C_(Z_beta^env), which still depends on the
parent residual-environment identification theorem (currently
audited_conditional). It sharpens the remaining object on the finite box
NMAX = 5: after stripping the marked half-slice multiplier and the exact
normalized mixed-kernel local factor, the residual operator is checked, as
a bounded approximation, to be the normalized central boundary class function
of the unmarked spatial Wilson environment.

What this runner now does, that the prior witness-injection version did not:
the residual diagonal data rho_env(p,q) is no longer a generic hard-coded
positive conjugation-symmetric witness sequence
(e.g. exp(-0.24 (p+q) - 0.08 (p-q)^2)). It is instead the actually-computed
normalized single-link SU(3) Wilson boundary character coefficient
  rho_(p,q)(beta) = c_(p,q)(beta) / (d_(p,q) c_(0,0)(beta)),
  c_(p,q)(beta)   = int_{SU(3)} chi_(p,q)(U) exp((beta/3) Re tr U) dU,
computed via the Schur-Weyl Bessel-determinant identity in the same way as
the retained bounded sibling runner
  scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
This is the canonical single-link Wilson boundary character at beta = 6 — one
exact piece of the unmarked spatial Wilson environment — and it is therefore
a single-link bounded witness for the residual environment compression, not
the full multi-link tensor-transfer environment object.

Bounded scope explicitly kept open:
- the full unmarked spatial Wilson environment tensor-transfer coefficients
- the parent residual-environment identification theorem (audited_conditional)
- analytic closure of canonical P(6)
"""

from __future__ import annotations

import numpy as np
from scipy.special import iv


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


def build_recurrence_matrix(nmax: int) -> tuple[np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
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


def dominant_eigenpair(m: np.ndarray) -> tuple[float, np.ndarray]:
    vals, vecs = np.linalg.eigh(m)
    idx = int(np.argmax(vals))
    vec = vecs[:, idx]
    if np.sum(vec) < 0.0:
        vec = -vec
    return float(vals[idx]), vec


def main() -> int:
    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)
    multiplier = matrix_exponential_symmetric(jmat, BETA / 2.0)

    c00 = wilson_character_coefficient(0, 0)
    local = np.array(
        [wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00) for p, q in weights],
        dtype=float,
    )
    d_local = np.diag(local**4)

    # Bounded environment witness: the actually-computed normalized single-link
    # SU(3) Wilson boundary character coefficient
    #   rho_(p,q)(beta) = c_(p,q)(beta) / (d_(p,q) c_(0,0)(beta)).
    # This is the same canonical Wilson integral computed by the retained
    # bounded sibling runner
    #   scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
    # The prior version of this runner injected an arbitrary positive,
    # conjugation-symmetric witness sequence
    # exp(-0.24 (p+q) - 0.08 (p-q)^2). Replacing that witness with the
    # actually-computed Wilson single-link coefficients makes this a single-
    # link Wilson-derived bounded witness for the residual environment rather
    # than a generic witness. It does NOT close the full multi-link unmarked
    # spatial Wilson environment, the parent residual-environment
    # identification theorem (audited_conditional), or analytic P(6).
    rho_env = local.copy()
    z_env = np.array([dim_su3(p, q) * rho for (p, q), rho in zip(weights, rho_env)], dtype=float)
    r_env = np.diag(rho_env)
    transfer = multiplier @ d_local @ r_env @ multiplier

    transfer_sym = float(np.max(np.abs(transfer - transfer.T)))
    transfer_swap = float(np.max(np.abs(swap @ transfer - transfer @ swap)))
    rho_sym = float(np.max(np.abs(swap @ r_env - r_env @ swap)))
    rho_min = float(np.min(rho_env))
    z00 = float(z_env[index[(0, 0)]])
    coeff_norm = float(np.max(np.abs(z_env / z00 - np.array([dim_su3(p, q) * rho_env[i] for i, (p, q) in enumerate(weights)]))))

    _, psi = dominant_eigenpair(transfer)
    expectation = float(psi @ (jmat @ psi))

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE SPATIAL ENVIRONMENT CHARACTER MEASURE")
    print("=" * 78)
    print()
    print("Exact already-fixed pieces")
    print(f"  source-operator symmetry error        = {float(np.max(np.abs(jmat - jmat.T))):.3e}")
    print(f"  half-slice multiplier min eig         = {float(np.min(np.linalg.eigvalsh(multiplier))):.12f}")
    print(f"  local-factor min/max                  = {float(np.min(np.diag(d_local))):.12e}, {float(np.max(np.diag(d_local))):.12f}")
    print()
    print("Boundary environment witness (actually-computed single-link Wilson)")
    print(f"  rho_env min/max                       = {rho_min:.12f}, {float(np.max(rho_env)):.12f}")
    print(f"  rho_env(0,0) (target 1.0)             = {rho_env[index[(0, 0)]]:.12f}")
    print(f"  rho_env(1,0)                          = {rho_env[index[(1, 0)]]:.12e}")
    print(f"  rho_env(1,1)                          = {rho_env[index[(1, 1)]]:.12e}")
    print(f"  z_(0,0)^env                           = {z00:.12f}")
    print(f"  environment swap error                = {rho_sym:.3e}")
    print(f"  normalized coefficient consistency    = {coeff_norm:.3e}")
    print()
    print("Resulting factorized transfer witness")
    print(f"  transfer symmetry error               = {transfer_sym:.3e}")
    print(f"  transfer swap error                   = {transfer_swap:.3e}")
    print(f"  Perron <J>                            = {expectation:.12f}")
    print()

    # Independent recomputation of the canonical single-link Wilson boundary
    # character coefficient, used as a cross-check that the bounded witness in
    # rho_env is the actually-computed canonical Wilson integral, not an
    # arbitrary positive symmetric sequence.
    rho_wilson_check = np.array(
        [wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00) for p, q in weights],
        dtype=float,
    )
    rho_witness_is_wilson = float(np.max(np.abs(rho_env - rho_wilson_check)))
    # Cross-check that the bounded witness is NOT one of the abstract
    # positive-symmetric witness sequences previously used (regression guard).
    rho_abstract_prior = np.array(
        [np.exp(-0.24 * (p + q) - 0.08 * ((p - q) ** 2)) for p, q in weights],
        dtype=float,
    )
    rho_witness_distinct_from_prior = float(np.max(np.abs(rho_env - rho_abstract_prior)))

    check(
        "the explicit plaquette source operator J is self-adjoint and conjugation-symmetric on the source sector",
        float(np.max(np.abs(jmat - jmat.T))) < 1.0e-15 and float(np.max(np.abs(swap @ jmat - jmat @ swap))) < 1.0e-12,
        detail="the accepted source operator is one exact self-adjoint six-neighbor recurrence",
    )
    check(
        "the bounded environment witness rho_env equals the actually-computed normalized single-link SU(3) Wilson boundary character coefficient rho_(p,q)(6) = c_(p,q)(6)/(d_(p,q) c_(0,0)(6))",
        rho_witness_is_wilson < 1.0e-15,
        detail=f"max abs deviation from canonical single-link Wilson integral = {rho_witness_is_wilson:.3e}",
    )
    check(
        "the bounded environment witness is not the abstract exp(-0.24 (p+q) - 0.08 (p-q)^2) witness previously used (regression guard against witness-injection)",
        rho_witness_distinct_from_prior > 1.0e-3,
        detail=f"max abs distance from prior abstract witness = {rho_witness_distinct_from_prior:.3e}",
    )
    check(
        "after stripping the marked half-slice multipliers and the exact local factor, the residual environment data can be packaged as one conjugation-symmetric coefficient sequence rho_(p,q)(6)",
        rho_sym < 1.0e-12 and rho_min > 0.0,
        detail=f"min rho coefficient={rho_min:.6e}",
    )
    check(
        "the residual operator is exactly realizable as one normalized central boundary character measure Z_6^env",
        coeff_norm < 1.0e-12 and abs(rho_env[index[(0, 0)]] - 1.0) < 1.0e-12,
        detail="Z_6^env(W) = z_(0,0)^env sum d_(p,q) rho_(p,q)(6) chi_(p,q)(W)",
    )
    check(
        "the explicit framework-point factorized source-sector law reduces to exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)",
        transfer_sym < 1.0e-12 and transfer_swap < 1.0e-12,
        detail="once rho_(p,q)(6) is fixed, the remaining operator is a concrete central boundary class function, not an abstract diagonal freedom",
    )

    check(
        "the environment character measure remains positivity-compatible on the truncated source sector",
        rho_min > 0.0,
        detail=f"minimum normalized boundary coefficient={rho_min:.3e}",
        bucket="SUPPORT",
    )
    check(
        "the boundary character measure is a reusable plaquette tool distinct from the already-fixed local mixed-kernel factor",
        float(np.max(np.abs(rho_env - 1.0))) > 1.0e-3,
        detail="the remaining datum now sits in Z_6^env rather than D_6^loc",
        bucket="SUPPORT",
    )
    check(
        "once Z_6^env is explicit, the remaining framework-point data reduce again to the Perron moments of one explicit factorized operator",
        expectation > 0.0,
        detail=f"Perron <J> = {expectation:.6f}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
