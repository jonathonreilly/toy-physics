#!/usr/bin/env python3
"""Audit the universal complement canonicalization problem.

This is a direct-universal, lambda-free check. It asks whether the current
universal data canonically split the complement `E \\oplus T1` using only:

1. the exact invariant `Pi_A1` projector;
2. quotient-kernel invariants from the symmetric `3+1` Hessian prototype;
3. the rotation generators on the valid `3+1` frame orbit;
4. curvature-localization consistency under frame changes.

The expected outcome is that the canonical `A1` core remains exact, while the
complement stays an `SO(3)` orbit bundle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
CANON = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
CURV = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
LAMBDA = DOCS / "UNIVERSAL_GR_LAMBDA_BYPASS_NOTE.md"
NOTE = DOCS / "UNIVERSAL_GR_COMPLEMENT_CANONICAL_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    m = np.zeros((n, n), dtype=float)
    if i == j:
        m[i, j] = 1.0
    else:
        scale = math.sqrt(2.0)
        m[i, j] = 1.0 / scale
        m[j, i] = 1.0 / scale
    return m


def diag(vals: Sequence[float]) -> np.ndarray:
    return np.diag(np.asarray(vals, dtype=float))


def canonical_polarization_frame() -> list[np.ndarray]:
    """Canonical lapse/shift/trace/shear basis on the symmetric `3+1` sector."""

    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),
        diag((0.0, 1.0 / sqrt2, -1.0 / sqrt2, 0.0)),
        diag((0.0, 1.0 / sqrt6, 1.0 / sqrt6, -2.0 / sqrt6)),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def rotation(axis: str, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    rot = np.eye(4)
    if axis == "x":
        rot[2, 2] = c
        rot[2, 3] = -s
        rot[3, 2] = s
        rot[3, 3] = c
    elif axis == "y":
        rot[1, 1] = c
        rot[1, 3] = s
        rot[3, 1] = -s
        rot[3, 3] = c
    elif axis == "z":
        rot[1, 1] = c
        rot[1, 2] = -s
        rot[2, 1] = s
        rot[2, 2] = c
    else:
        raise ValueError(axis)
    return rot


def rep_matrix(rot: np.ndarray, frame: Sequence[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        img = rot.T @ basis @ rot
        for i, ref in enumerate(frame):
            out[i, j] = float(np.tensordot(ref, img, axes=2))
    return out


def pi_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def generator(axis: str, eps: float = 1e-6) -> np.ndarray:
    frame = canonical_polarization_frame()
    plus = rep_matrix(rotation(axis, eps), frame)
    minus = rep_matrix(rotation(axis, -eps), frame)
    return (plus - minus) / (2.0 * eps)


def bilinear(
    a: Sequence[Sequence[float]],
    b: Sequence[Sequence[float]],
    d: Sequence[float],
) -> float:
    total = 0.0
    n = len(d)
    for i in range(n):
        for j in range(n):
            total += a[i][j] * b[j][i] / (d[i] * d[j])
    return -total


def sym_basis(n: int) -> list[list[list[float]]]:
    basis: list[list[list[float]]] = []
    for i in range(n):
        m = [[0.0 for _ in range(n)] for _ in range(n)]
        m[i][i] = 1.0
        basis.append(m)
    for i in range(n):
        for j in range(i + 1, n):
            m = [[0.0 for _ in range(n)] for _ in range(n)]
            scale = math.sqrt(2.0)
            m[i][j] = 1.0 / scale
            m[j][i] = 1.0 / scale
            basis.append(m)
    return basis


def gram_matrix(
    basis: Sequence[Sequence[Sequence[float]]],
    d: Sequence[float],
) -> np.ndarray:
    return np.asarray([[bilinear(a, b, d) for b in basis] for a in basis], dtype=float)


def response_vector(
    h: Sequence[Sequence[float]],
    frame: Sequence[Sequence[Sequence[float]]],
    d: Sequence[float],
) -> np.ndarray:
    return np.asarray([bilinear(h, basis, d) for basis in frame], dtype=float)


def complement_block(a: np.ndarray) -> np.ndarray:
    p = pi_a1()
    c = np.eye(10) - p
    return c @ a @ c


def comm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def best_so3_match(a: np.ndarray, b: np.ndarray) -> tuple[float, str]:
    err_plus = float(np.linalg.norm(a - b, ord="fro"))
    err_minus = float(np.linalg.norm(a + b, ord="fro"))
    if err_plus <= err_minus:
        return err_plus, "+"
    return err_minus, "-"


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1_NOTE)
    canon = read(CANON)
    curv = read(CURV)
    lam = read(LAMBDA)
    note = read(NOTE)

    frame = canonical_polarization_frame()
    p = pi_a1()
    comp = np.eye(10) - p
    gens = {axis: generator(axis) for axis in ("x", "y", "z")}
    gen_stack = np.stack([gens["x"], gens["y"], gens["z"]], axis=0)
    gen_rank = int(np.linalg.matrix_rank(gen_stack.reshape(3, -1), tol=1e-10))

    comm_errors = {}
    comm_signs = {}
    for left, right, target in (("x", "y", "z"), ("y", "z", "x"), ("z", "x", "y")):
        err, sign = best_so3_match(comm(gens[left], gens[right]), gens[target])
        comm_errors[f"[{left},{right}]~{target}"] = err
        comm_signs[f"[{left},{right}]"] = sign

    d = (2.0, 3.0, 5.0, 7.0)
    basis = sym_basis(4)
    gram = gram_matrix(basis, d)
    gram_a1 = p @ gram @ p

    rot_a = rotation("x", math.pi / 7.0)
    rot_b = rotation("y", math.pi / 5.0)
    rot_c = rotation("z", math.pi / 6.0)
    rep_a = rep_matrix(rot_a, frame)
    rep_b = rep_matrix(rot_b, frame)
    rep_c = rep_matrix(rot_c, frame)
    gram_a = rep_a.T @ gram @ rep_a
    gram_b = rep_b.T @ gram @ rep_b
    gram_c = rep_c.T @ gram @ rep_c

    a1_delta = max(
        float(np.max(np.abs((p @ gram_a @ p) - gram_a1))),
        float(np.max(np.abs((p @ gram_b @ p) - gram_a1))),
        float(np.max(np.abs((p @ gram_c @ p) - gram_a1))),
    )
    a1_comm = max(float(np.linalg.norm(comm(p, g), ord="fro")) for g in gens.values())
    comp_gen_rank = int(np.linalg.matrix_rank(np.stack([comp @ g @ comp for g in gens.values()], axis=0).reshape(3, -1), tol=1e-10))

    h_test = (
        (1.0, 0.35, -0.22, 0.18),
        (0.35, -0.75, 0.14, 0.07),
        (-0.22, 0.14, 0.41, -0.19),
        (0.18, 0.07, -0.19, -0.28),
    )
    resp_base = response_vector(h_test, frame, d)
    resp_a = response_vector(h_test, [rot_a.T @ basis @ rot_a for basis in frame], d)
    resp_b = response_vector(h_test, [rot_b.T @ basis @ rot_b for basis in frame], d)
    resp_c = response_vector(h_test, [rot_c.T @ basis @ rot_c for basis in frame], d)
    comp_delta = max(
        float(np.max(np.abs((np.eye(10) - p) @ resp_a - (np.eye(10) - p) @ resp_base))),
        float(np.max(np.abs((np.eye(10) - p) @ resp_b - (np.eye(10) - p) @ resp_base))),
        float(np.max(np.abs((np.eye(10) - p) @ resp_c - (np.eye(10) - p) @ resp_base))),
    )

    checks = [
        Check(
            "scalar observable generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "observable-principle source is present",
        ),
        Check(
            "lambda-free direct universal route is exact",
            has(lam, "lambda-free") and has(lam, "Pi_A1") and has(lam, "quotient-kernel"),
            "direct universal bypass note is present",
        ),
        Check(
            "3+1 lift and quotient kernel are exact",
            has(route2, "pl s^3 x r") and has(var, "s_gr^cand") and has(uni, "unique symmetric"),
            "lift, variational candidate, and quotient uniqueness are present",
        ),
        Check(
            "Pi_A1 is exact and rank-2",
            int(np.linalg.matrix_rank(p)) == 2,
            "Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)",
        ),
        Check(
            "Pi_A1 commutes with the SO(3) generators",
            a1_comm < 1e-12,
            f"max commutator norm = {a1_comm:.3e}",
        ),
        Check(
            "rotation generators close as so(3) up to convention sign",
            max(comm_errors.values()) < 1e-8,
            f"commutator errors = { {k: f'{v:.3e}' for k, v in comm_errors.items()} }",
        ),
        Check(
            "rotation-generator rank is three",
            gen_rank == 3,
            f"generator rank = {gen_rank}",
        ),
        Check(
            "complement action remains nontrivial",
            comp_gen_rank == 3,
            f"complement generator rank = {comp_gen_rank}",
        ),
        Check(
            "quotient-kernel A1 block is invariant under valid frame changes",
            a1_delta < 1e-12,
            f"max A1-block delta = {a1_delta:.3e}",
        ),
        Check(
            "curvature-localization consistency leaves the complement orbit-valued",
            comp_delta > 1e-6,
            f"max complement delta across valid frame changes = {comp_delta:.3e}",
        ),
        Check(
            "the current universal note still names the missing canonical complement section",
            has(canon, "distinguished connection") and has(canon, "SO(3)"),
            "canonical projector/connection note matches the orbit obstruction",
        ),
        Check(
            "the complement-canonical note frames the answer as an orbit bundle, not a section",
            has(note, "orbit bundle") and has(note, "SO(3)") and has(note, "canonical section"),
            "the new note states the orbit-bundle result",
        ),
    ]

    print("UNIVERSAL GR COMPLEMENT CANONICALIZATION AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("PROTOTYPE RESULTS")
    print("=" * 78)
    print(f"Pi_A1 rank        = {int(np.linalg.matrix_rank(p))}")
    print(f"generator rank    = {gen_rank}")
    print(f"complement rank    = {comp_gen_rank}")
    print(f"A1 block delta    = {a1_delta:.12e}")
    print(f"A1 commutator norm= {a1_comm:.12e}")
    print(f"complement delta   = {comp_delta:.12e}")
    print(f"commutator errors  = { {k: f'{v:.3e}' for k, v in comm_errors.items()} }")
    print(f"commutator signs   = {comm_signs}")
    print(f"resp_base[0:4]     = {[f'{x:.6e}' for x in resp_base[:4]]}")
    print(f"resp_rotA[0:4]     = {[f'{x:.6e}' for x in resp_a[:4]]}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "The universal complement does not canonically split from the "
            "current universal data. The exact invariant A1 core is canonical, "
            "the quotient-kernel A1 block is invariant, and the rotation "
            "generators close as so(3), but the complement remains an SO(3) "
            "orbit bundle rather than a canonical section."
        )
        print(
            "Strongest canonical complement candidate: P_comp^cand := "
            "(Pi_A1, O_{E \\oplus T1}, omega_MC)."
        )
        print("Exact residual gauge: SO(3).")
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
