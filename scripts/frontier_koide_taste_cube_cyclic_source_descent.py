#!/usr/bin/env python3
"""
Koide taste-cube cyclic-source descent runner
=============================================

STATUS: constructive positive-path reduction theorem on the full 8-corner
carrier

Question:
  If we work on the physical taste cube C^8 first, rather than assuming the
  bare T_1 / hw=1 triplet is already the whole charged-lepton story, what
  exact response target survives after:

    1. full-cube C_3[111] averaging, and
    2. a Schur-compatible charged-sector reduction onto T_1?

Answer:
  The target is still exactly the same 3-response cyclic Koide bundle. Full-
  cube averaging descends to the same T_1 cyclic projector, and every
  Schur-compatible charged-sector response factors through the same three
  cyclic channels B0, B1, B2.
"""

from __future__ import annotations

import sys
from typing import Iterable

import numpy as np
import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0

BASIS = [
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
]
INDEX = {alpha: i for i, alpha in enumerate(BASIS)}
T1 = [INDEX[(1, 0, 0)], INDEX[(0, 1, 0)], INDEX[(0, 0, 1)]]


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_bits(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = alpha
    return (c, a, b)


def cube_cycle_np() -> np.ndarray:
    u = np.zeros((8, 8), dtype=complex)
    for j, alpha in enumerate(BASIS):
        i = INDEX[cycle_bits(alpha)]
        u[i, j] = 1.0
    return u


def cube_cycle_sp() -> sp.Matrix:
    u = sp.zeros(8)
    for j, alpha in enumerate(BASIS):
        i = INDEX[cycle_bits(alpha)]
        u[i, j] = 1
    return u


def projector_t1_sp() -> sp.Matrix:
    p = sp.zeros(8)
    for i in T1:
        p[i, i] = 1
    return p


def matrix_unit_sp(n: int, i: int, j: int) -> sp.Matrix:
    e = sp.zeros(n)
    e[i, j] = 1
    return e


def compress_t1_sp(x: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[sp.simplify(x[i, j]) for j in T1] for i in T1])


def compress_t1_np(x: np.ndarray) -> np.ndarray:
    return x[np.ix_(T1, T1)]


def embed_t1_np(y: np.ndarray) -> np.ndarray:
    out = np.zeros((8, 8), dtype=complex)
    out[np.ix_(T1, T1)] = y
    return out


def avg_sp(u: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(u.rows)
    uk = sp.eye(u.rows)
    for _ in range(3):
        out += uk * x * uk.T
        uk = u * uk
    return sp.simplify(out / 3)


def avg_np(u: np.ndarray, x: np.ndarray) -> np.ndarray:
    out = np.zeros_like(x, dtype=complex)
    uk = np.eye(u.shape[0], dtype=complex)
    for _ in range(3):
        out += uk @ x @ uk.conj().T
        uk = u @ uk
    return out / 3.0


def cycle_matrix_sp() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def cycle_matrix_np() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def avg_t1_sp(x: sp.Matrix) -> sp.Matrix:
    c = cycle_matrix_sp()
    out = sp.zeros(3)
    ck = sp.eye(3)
    for _ in range(3):
        out += ck * x * ck.T
        ck = c * ck
    return sp.simplify(out / 3)


def cyclic_basis_sp() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    c = cycle_matrix_sp()
    b0 = sp.eye(3)
    b1 = c + c.T
    b2 = sp.I * (c - c.T)
    return b0, b1, b2, c


def cyclic_basis_np() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    c = cycle_matrix_np()
    cd = c.conj().T
    b0 = np.eye(3, dtype=complex)
    b1 = c + cd
    b2 = 1j * (c - cd)
    return b0, b1, b2


def full_source_channels_sp() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    u = cube_cycle_sp()
    i100 = INDEX[(1, 0, 0)]
    i010 = INDEX[(0, 1, 0)]

    q0 = sp.simplify(3 * avg_sp(u, matrix_unit_sp(8, i100, i100)))
    qf = sp.simplify(3 * avg_sp(u, matrix_unit_sp(8, i010, i100)))
    qb = sp.simplify(3 * avg_sp(u, matrix_unit_sp(8, i100, i010)))
    q1 = sp.simplify(qf + qb)
    q2 = sp.simplify(sp.I * (qf - qb))
    return q0, q1, q2, qf, qb


def matrix_to_np(x: sp.Matrix) -> np.ndarray:
    return np.array(x.tolist(), dtype=complex)


def schur_complement(m: np.ndarray, target: Iterable[int]) -> np.ndarray:
    target = list(target)
    rest = [i for i in range(m.shape[0]) if i not in target]
    a = m[np.ix_(target, target)]
    b = m[np.ix_(target, rest)]
    d = m[np.ix_(rest, rest)]
    return a - b @ np.linalg.inv(d) @ b.conj().T


def random_positive_covariant(u: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(u.shape[0], u.shape[0])) + 1j * rng.normal(size=(u.shape[0], u.shape[0]))
    m0 = x.conj().T @ x + 0.5 * np.eye(u.shape[0], dtype=complex)
    return avg_np(u, m0)


def random_hermitian(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return x + x.conj().T


def real_trace_pair(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.real(np.trace(a @ b)))


def cyclic_coordinates(y: np.ndarray) -> tuple[float, float, float]:
    b0, b1, b2 = cyclic_basis_np()
    u0 = real_trace_pair(y, b0) / 3.0
    u1 = real_trace_pair(y, b1) / 6.0
    u2 = real_trace_pair(y, b2) / 6.0
    return u0, u1, u2


def part1_full_cube_average_descends_exactly() -> None:
    print("=" * 88)
    print("PART 1: full-cube C_3 averaging descends exactly to the same T_1 projector")
    print("=" * 88)

    u8 = cube_cycle_sp()
    p1 = projector_t1_sp()
    c = cycle_matrix_sp()

    check(
        "The one-hot T_1 projector commutes with the full taste-cube C_3[111] cycle",
        sp.simplify(u8 * p1 - p1 * u8) == sp.zeros(8),
    )
    check(
        "The restricted action on T_1 is exactly the retained 3-cycle",
        compress_t1_sp(u8) == c,
    )

    descent_ok = True
    first_fail = ""
    for i in range(8):
        for j in range(8):
            eij = matrix_unit_sp(8, i, j)
            lhs = compress_t1_sp(avg_sp(u8, eij))
            rhs = avg_t1_sp(compress_t1_sp(eij))
            if sp.simplify(lhs - rhs) != sp.zeros(3):
                descent_ok = False
                first_fail = f"basis unit ({i},{j})"
                break
        if not descent_ok:
            break

    check(
        "For every basis source, compress(full average) = T_1 cyclic average(compress)",
        descent_ok,
        detail=first_fail or "tested all 64 matrix units exactly",
    )


def part2_canonical_full_cube_source_channels() -> None:
    print()
    print("=" * 88)
    print("PART 2: exact full-cube orbit channels descend to B0, B1, B2")
    print("=" * 88)

    q0, q1, q2, qf, qb = full_source_channels_sp()
    b0, b1, b2, c = cyclic_basis_sp()

    check(
        "The diagonal one-hot orbit source descends to B0",
        compress_t1_sp(q0) == b0,
    )
    check(
        "The forward oriented one-hot orbit source descends to C",
        compress_t1_sp(qf) == c,
    )
    check(
        "The backward oriented one-hot orbit source descends to C^2",
        compress_t1_sp(qb) == c**2,
    )
    check(
        "Hermitian full-cube orbit combinations descend to B1 and B2",
        compress_t1_sp(q1) == b1 and compress_t1_sp(q2) == b2,
    )
    check(
        "Q0, Q1, Q2 are already C_3-averaged Hermitian full-cube source channels",
        sp.simplify(avg_sp(cube_cycle_sp(), q0) - q0) == sp.zeros(8)
        and sp.simplify(avg_sp(cube_cycle_sp(), q1) - q1) == sp.zeros(8)
        and sp.simplify(avg_sp(cube_cycle_sp(), q2) - q2) == sp.zeros(8)
        and q0 == q0.H
        and q1 == q1.H
        and q2 == q2.H,
    )


def part3_schur_reduction_hits_same_three_response_bundle() -> None:
    print()
    print("=" * 88)
    print("PART 3: positive full-cube parents reduce to the same 3-response cyclic bundle")
    print("=" * 88)

    u8 = cube_cycle_np()
    c = cycle_matrix_np()
    b0, b1, b2 = cyclic_basis_np()

    positive_ok = True
    commute_ok = True
    reconstruct_ok = True
    saw_nontrivial = False
    details = []

    for seed in range(5):
        m = random_positive_covariant(u8, seed)
        s = schur_complement(m, T1)
        m_min = float(np.min(np.linalg.eigvalsh(m)).real)
        s_min = float(np.min(np.linalg.eigvalsh(s)).real)
        commute_err = float(np.linalg.norm(c @ s @ c.conj().T - s))
        r0 = real_trace_pair(s, b0)
        r1 = real_trace_pair(s, b1)
        r2 = real_trace_pair(s, b2)
        s_rec = (r0 / 3.0) * b0 + (r1 / 6.0) * b1 + (r2 / 6.0) * b2
        rec_err = float(np.linalg.norm(s - s_rec))
        offdiag_max = float(np.max(np.abs(s - np.diag(np.diag(s)))))

        positive_ok &= m_min > 1e-10 and s_min > 1e-10
        commute_ok &= commute_err < 1e-10
        reconstruct_ok &= rec_err < 1e-10
        saw_nontrivial |= offdiag_max > 1e-3
        details.append(
            f"seed{seed}: eigM={m_min:.3e}, eigS={s_min:.3e}, "
            f"comm={commute_err:.1e}, rec={rec_err:.1e}"
        )

    check(
        "Every tested averaged full-cube parent and its T_1 Schur block stay positive",
        positive_ok,
        detail="; ".join(details),
        kind="NUMERIC",
    )
    check(
        "Every tested T_1 Schur block commutes with the retained 3-cycle",
        commute_ok,
        kind="NUMERIC",
    )
    check(
        "Every tested T_1 Schur block is reconstructed exactly from r0, r1, r2",
        reconstruct_ok,
        kind="NUMERIC",
    )
    check(
        "Full-cube couplings still generate nontrivial reduced operators without leaving the 3-response bundle",
        saw_nontrivial,
        kind="NUMERIC",
    )


def part4_schur_compatible_response_factorization() -> None:
    print()
    print("=" * 88)
    print("PART 4: any Schur-compatible full-cube response factors through r0, r1, r2")
    print("=" * 88)

    u8 = cube_cycle_np()
    b0, b1, b2 = cyclic_basis_np()
    q0_sp, q1_sp, q2_sp, _, _ = full_source_channels_sp()
    q0 = matrix_to_np(q0_sp)
    q1 = matrix_to_np(q1_sp)
    q2 = matrix_to_np(q2_sp)

    channel_ok = True
    coord_ok = True
    factor_ok = True
    channel_details = []
    factor_details = []

    for m_seed in range(3):
        m = random_positive_covariant(u8, 40 + m_seed)
        s = schur_complement(m, T1)
        s_ext = embed_t1_np(s)
        r0 = real_trace_pair(s, b0)
        r1 = real_trace_pair(s, b1)
        r2 = real_trace_pair(s, b2)

        err0 = abs(real_trace_pair(s_ext, q0) - r0)
        err1 = abs(real_trace_pair(s_ext, q1) - r1)
        err2 = abs(real_trace_pair(s_ext, q2) - r2)
        channel_ok &= max(err0, err1, err2) < 1e-10
        channel_details.append(
            f"seed{m_seed}: ({err0:.1e}, {err1:.1e}, {err2:.1e})"
        )

        for x_seed in range(4):
            x = random_hermitian(100 + 10 * m_seed + x_seed, 8)
            y = compress_t1_np(avg_np(u8, x))
            u0, u1, u2 = cyclic_coordinates(y)
            y_rec = u0 * b0 + u1 * b1 + u2 * b2
            coord_err = float(np.linalg.norm(y - y_rec))
            lhs = real_trace_pair(s, y)
            rhs = u0 * r0 + u1 * r1 + u2 * r2
            fact_err = abs(lhs - rhs)
            coord_ok &= coord_err < 1e-10
            factor_ok &= fact_err < 1e-10
            factor_details.append(
                f"M{m_seed}/X{x_seed}: coord={coord_err:.1e}, fact={fact_err:.1e}"
            )

    check(
        "The canonical full-cube orbit channels read the same three responses as B0, B1, B2",
        channel_ok,
        detail="; ".join(channel_details),
        kind="NUMERIC",
    )
    check(
        "Every averaged full-cube Hermitian source compresses to the B0, B1, B2 bundle",
        coord_ok,
        detail="; ".join(factor_details[:4]) + ("; ..." if len(factor_details) > 4 else ""),
        kind="NUMERIC",
    )
    check(
        "The response law ReTr(S(M) P1 A8(X) P1) factors exactly through r0, r1, r2",
        factor_ok,
        detail="; ".join(factor_details[:4]) + ("; ..." if len(factor_details) > 4 else ""),
        kind="NUMERIC",
    )


def main() -> int:
    part1_full_cube_average_descends_exactly()
    part2_canonical_full_cube_source_channels()
    part3_schur_reduction_hits_same_three_response_bundle()
    part4_schur_compatible_response_factorization()

    print()
    print("Interpretation:")
    print("  The physical taste cube does not force us back to a vague large-source")
    print("  target. Exact C_3[111] averaging and a Schur-compatible charged-sector")
    print("  reduction collapse the full 8-corner source bank to the same three")
    print("  cyclic response channels already identified on T_1. So the honest")
    print("  remaining job is not to rediscover the carrier size. It is to derive")
    print("  the microscopic full-cube source law for those channels, and then the")
    print("  selector law that would put them on the Koide cone.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
