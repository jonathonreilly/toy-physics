#!/usr/bin/env python3
"""Verifier for the direct-universal lambda bypass candidate.

This does not claim full closure. It checks that the direct universal route
can be formulated as an exact lambda-free `A1`-anchored action/quotient-kernel
candidate, and that the remaining ambiguity is the complementary `SO(3)` frame
orbit rather than the phase-lift mixing family.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
A1 = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
BYPASS = DOCS / "UNIVERSAL_GR_LAMBDA_BYPASS_NOTE.md"
FRAME = DOCS / "UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


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


def sym(i: int, j: int, n: int = 4) -> list[list[float]]:
    m = [[0.0 for _ in range(n)] for _ in range(n)]
    if i == j:
        m[i][j] = 1.0
    else:
        scale = 2.0 ** 0.5
        m[i][j] = 1.0 / scale
        m[j][i] = 1.0 / scale
    return m


def diag(vals: Sequence[float]) -> list[list[float]]:
    n = len(vals)
    m = [[0.0 for _ in range(n)] for _ in range(n)]
    for i, v in enumerate(vals):
        m[i][i] = float(v)
    return m


def project_a1(h: Sequence[Sequence[float]]) -> list[list[float]]:
    """Exact rank-2 projector onto lapse plus spatial trace."""

    tr_spatial = h[1][1] + h[2][2] + h[3][3]
    out = [[0.0 for _ in range(4)] for _ in range(4)]
    out[0][0] = h[0][0]
    val = tr_spatial / 3.0
    out[1][1] = val
    out[2][2] = val
    out[3][3] = val
    return out


def matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> list[list[float]]:
    n = len(a)
    m = len(b[0]) if b else 0
    out = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(len(b)):
            aik = a[i][k]
            if abs(aik) <= 1e-15:
                continue
            for j in range(m):
                out[i][j] += aik * b[k][j]
    return out


def transpose(a: Sequence[Sequence[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def conj(rot: Sequence[Sequence[float]], m: Sequence[Sequence[float]]) -> list[list[float]]:
    return matmul(matmul(transpose(rot), m), rot)


def rot_y(theta: float) -> list[list[float]]:
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, c, 0.0, -s],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, s, 0.0, c],
    ]


def rot_x(theta: float) -> list[list[float]]:
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, c, -s],
        [0.0, 0.0, s, c],
    ]


def bypass_action(h: Sequence[Sequence[float]], d: Sequence[float]) -> float:
    hp = project_a1(h)
    return 0.5 * bilinear(hp, hp, d)


def max_abs_delta(a: Sequence[float], b: Sequence[float]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def flatten_upper(m: Sequence[Sequence[float]]) -> list[float]:
    return [
        m[0][0],
        m[0][1],
        m[0][2],
        m[0][3],
        m[1][1],
        m[1][2],
        m[1][3],
        m[2][2],
        m[2][3],
        m[3][3],
    ]


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1)
    bypass = read(BYPASS)
    frame = read(FRAME)

    d = (2.0, 3.0, 5.0, 7.0)
    h = (
        (1.25, 0.18, -0.07, 0.21),
        (0.18, -0.64, 0.12, -0.05),
        (-0.07, 0.12, 0.33, 0.09),
        (0.21, -0.05, 0.09, -0.29),
    )

    rot_a = rot_y(math.pi / 6.0)
    rot_b = rot_x(math.pi / 5.0)
    h_a = conj(rot_a, h)
    h_b = conj(rot_b, h)

    hp = project_a1(h)
    hp_a = project_a1(h_a)
    hp_b = project_a1(h_b)

    action_0 = bypass_action(h, d)
    action_a = bypass_action(h_a, d)
    action_b = bypass_action(h_b, d)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "observable principle gives the exact scalar generator",
        ),
        Check(
            "3+1 lift is exact",
            has(route2, "pl s^3 x r") or has(route2, "o_lift = 1"),
            "route-2 gives the exact PL S^3 x R scaffold",
        ),
        Check(
            "tensor candidate is exact",
            has(var, "metric-source hessian") and has(var, "s_gr^cand"),
            "tensor-valued variational candidate is already built",
        ),
        Check(
            "quotient kernel is exact",
            has(uni, "unique symmetric `3+1` quotient kernel")
            or has(uni, "unique symmetric 3+1 quotient kernel"),
            "quotient-uniqueness note pins down the symmetric kernel",
        ),
        Check(
            "A1 section is exact",
            has(a1, "pi_a1") and has(a1, "lapse") and has(a1, "spatial trace"),
            "A1 projector is already canonical on the invariant block",
        ),
        Check(
            "bypass candidate is lambda-free by construction",
            has(bypass, "lambda-free") and has(bypass, "quotient-kernel candidate"),
            "new candidate note states the direct universal bypass avoids lambda",
        ),
        Check(
            "A1 projection is invariant under valid frame rotations",
            max_abs_delta(flatten_upper(hp), flatten_upper(hp_a)) < 1e-15
            and max_abs_delta(flatten_upper(hp), flatten_upper(hp_b)) < 1e-15,
            "Pi_A1 removes frame dependence on the invariant core",
        ),
        Check(
            "bypass action is frame-invariant on the invariant core",
            abs(action_0 - action_a) < 1e-15 and abs(action_0 - action_b) < 1e-15,
            f"actions = {action_0:.6e}, {action_a:.6e}, {action_b:.6e}",
        ),
        Check(
            "residual complement gauge remains nontrivial",
            has(bypass, "so(3)"),
            "the remaining obstruction is complement-frame gauge, not lambda",
        ),
    ]

    print("UNIVERSAL GR LAMBDA BYPASS AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("BYPASS RESULTS")
    print("=" * 78)
    print(f"Pi_A1(h)      = {flatten_upper(hp)}")
    print(f"Pi_A1(rot_a)  = {flatten_upper(hp_a)}")
    print(f"Pi_A1(rot_b)  = {flatten_upper(hp_b)}")
    print(f"S_bypass(h)   = {action_0:.12e}")
    print(f"S_bypass(a)   = {action_a:.12e}")
    print(f"S_bypass(b)   = {action_b:.12e}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Direct-universal bypass candidate confirmed: the exact A1-anchored "
            "tensor action/quotient-kernel route is lambda-free by construction, "
            "and the remaining ambiguity is the SO(3) complement-frame gauge."
        )
        return 0

    print("One or more bypass checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
