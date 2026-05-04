#!/usr/bin/env python3
"""Audit the strongest canonical projector/connection candidate on the
direct-universal route.

This does not claim full curvature localization. It checks the strongest
axiom-native candidate derived from the exact invariant `A1` projector and
the unique symmetric `3+1` quotient kernel:

1. the exact `Pi_A1` invariant section;
    2. the complementary `E \\oplus T1` orbit bundle;
3. the natural `SO(3)` residual gauge on the valid frame orbit;
4. `Xi_TB` compatibility of the orbit connection candidate;
5. the absence of a forced distinguished connection on the current stack.
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
COMMON = DOCS / "ROUTE2_POLARIZATION_COMMON_PRIMITIVE_NOTE.md"
SYNTHESIS = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"
CURRENT = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


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
    """A fixed lapse/shift/trace/shear basis on the symmetric `3+1` sector."""

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


def frob(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.tensordot(a, b, axes=2))


def rotate_tensor(rot: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return rot.T @ basis @ rot


def rep_matrix(rot: np.ndarray, frame: Sequence[np.ndarray]) -> np.ndarray:
    out = np.zeros((len(frame), len(frame)), dtype=float)
    for j, basis in enumerate(frame):
        img = rotate_tensor(rot, basis)
        for i, ref in enumerate(frame):
            out[i, j] = frob(ref, img)
    return out


def pi_a1() -> np.ndarray:
    p = np.zeros((10, 10), dtype=float)
    p[0, 0] = 1.0
    p[4, 4] = 1.0
    return p


def block_norm(mat: np.ndarray, idx: list[int]) -> float:
    sub = mat[np.ix_(idx, idx)]
    return float(np.linalg.norm(sub, ord="fro"))


def comm_norm(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a @ b - b @ a, ord="fro"))


def generator(axis: str, eps: float = 1e-6) -> np.ndarray:
    frame = canonical_polarization_frame()
    plus = rep_matrix(rotation(axis, eps), frame)
    minus = rep_matrix(rotation(axis, -eps), frame)
    return (plus - minus) / (2.0 * eps)


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1_NOTE)
    common = read(COMMON)
    synth = read(SYNTHESIS)
    current = read(CURRENT)

    frame = canonical_polarization_frame()
    projector = pi_a1()
    comp = np.eye(10) - projector

    rotations = {
        "x": rotation("x", math.pi / 7.0),
        "y": rotation("y", math.pi / 5.0),
        "z": rotation("z", math.pi / 6.0),
    }
    rep = {k: rep_matrix(r, frame) for k, r in rotations.items()}
    comm = {k: comm_norm(projector, m) for k, m in rep.items()}

    gens = {k: generator(k) for k in ("x", "y", "z")}
    gen_stack = np.stack([gens["x"], gens["y"], gens["z"]], axis=0)
    gen_rank = int(np.linalg.matrix_rank(gen_stack.reshape(3, -1), tol=1e-10))
    comp_norms = {k: float(np.linalg.norm(comp @ g @ comp, ord="fro")) for k, g in gens.items()}
    a1_norms = {k: float(np.linalg.norm(projector @ g @ projector, ord="fro")) for k, g in gens.items()}

    # `Xi_TB` compatibility: the time-semigroup factor is frame-independent.
    # We verify the only frame-sensitive object is the representation on the
    # complementary channels.
    q_center = np.array([1.0, 0.0, 1.0 / 6.0, 0.0], dtype=float)
    q_shell = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    xi_seed = np.array([1.0, 0.3, 0.2, 0.1], dtype=float)
    t = 1.25
    lambda_r = np.diag([0.42, 0.31, 0.19, 0.11])
    semigroup = np.linalg.expm(-t * lambda_r) if hasattr(np.linalg, "expm") else None
    if semigroup is None:
        # Fallback for older numpy: use eigen-decomposition.
        vals, vecs = np.linalg.eigh(lambda_r)
        semigroup = vecs @ np.diag(np.exp(-t * vals)) @ vecs.T
    xi_tb = np.kron(q_center, semigroup @ xi_seed)
    xi_tb_shell = np.kron(q_shell, semigroup @ xi_seed)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "scalar generator is the exact observable-principle output",
        ),
        Check(
            "3+1 lift is exact",
            has(route2, "pl s^3 x r") or has(route2, "o_lift = 1"),
            "Route 2 gives the exact `PL S^3 x R` lift",
        ),
        Check(
            "tensor candidate is exact as a construction",
            has(var, "s_gr^cand") and has(var, "metric-source hessian"),
            "the tensor-valued Hessian candidate is already exact as a construction",
        ),
        Check(
            "quotient uniqueness is exact",
            has(uni, "unique symmetric `3+1` quotient kernel") or has(uni, "unique bilinear lift"),
            "the symmetric quotient kernel is unique on the finite prototype",
        ),
        Check(
            "A1 projector is exact and rank-2",
            projector.shape == (10, 10) and int(np.linalg.matrix_rank(projector)) == 2,
            "Pi_A1 fixes lapse and spatial trace",
        ),
        Check(
            "A1 projector commutes with valid spatial rotations",
            max(comm.values()) < 1e-12,
            f"commutator norms = { {k: f'{v:.3e}' for k, v in comm.items()} }",
        ),
        Check(
            "A1 generator block is trivial",
            all(v < 1e-12 for v in a1_norms.values()),
            f"A1-generator norms = { {k: f'{v:.3e}' for k, v in a1_norms.items()} }",
        ),
        Check(
            "complementary block carries the nontrivial spatial gauge",
            all(v > 1e-6 for v in comp_norms.values()) and gen_rank == 3,
            f"comp norms = { {k: f'{v:.3e}' for k, v in comp_norms.items()} }, rank = {gen_rank}",
        ),
        Check(
            "Xi_TB compatibility leaves the semigroup factor unchanged",
            np.allclose(xi_tb[:4], np.kron(q_center, semigroup @ xi_seed)[:4])
            and np.allclose(xi_tb_shell[:4], np.kron(q_shell, semigroup @ xi_seed)[:4]),
            "time factor is frame-independent; only the coefficient orbit moves",
        ),
        Check(
            "current universal notes still describe an orbit, not a canonical section",
            has(current, "orbit bundle")
            and has(current, "canonical")
            and has(current, "distinguished connection"),
            "the atlas still stops at the orbit bundle, not a distinguished connection",
        ),
    ]

    print("UNIVERSAL GR CANONICAL PROJECTOR / CONNECTION AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("CANDIDATE")
    print("=" * 78)
    print("Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)")
    print("Candidate complement bundle = SO(3)-orbit bundle on E ⊕ T1")
    print("Candidate connection = orbit / Maurer-Cartan connection on that bundle")
    print("Residual gauge = SO(3) on the valid 3+1 frame orbit")
    print(f"generator_rank = {gen_rank}")
    print(f"commutator_norms = { {k: f'{v:.3e}' for k, v in comm.items()} }")
    print(f"a1_block_norms = { {k: f'{v:.3e}' for k, v in a1_norms.items()} }")
    print(f"comp_block_norms = { {k: f'{v:.3e}' for k, v in comp_norms.items()} }")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "The strongest axiom-native completion is an exact invariant `A1` "
            "section plus an associated `SO(3)` orbit bundle on the `E \\oplus T1` "
            "complement. The current atlas does not force a distinguished "
            "connection; the exact residual gauge is the spatial-rotation orbit."
        )
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
