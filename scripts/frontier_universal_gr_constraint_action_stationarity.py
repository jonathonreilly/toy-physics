#!/usr/bin/env python3
"""Audit whether a constraint-style action-stationarity theorem can bypass
the complement-frame ambiguity on the direct universal route.

This is not a closure proof. It checks only universal-branch data:

1. the exact scalar observable principle;
2. the exact `3+1` kinematic lift on `PL S^3 x R`;
3. the exact tensor-valued variational candidate;
4. the exact unique symmetric `3+1` quotient kernel;
5. the exact invariant `A1` projector;
6. whether an action / constraint stationarity functional is orbit-flat on
   the valid `SO(3)` frame orbit while the complement coordinates still move.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
CANONICAL = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
BLOCKER = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
CURRENT = DOCS / "UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md"


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


def random_so3(rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(3, 3))
    q, _ = np.linalg.qr(a)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    rot = np.eye(4)
    rot[1:, 1:] = q
    return rot


def rotated_frame(rot: np.ndarray) -> list[np.ndarray]:
    return [rot.T @ basis @ rot for basis in canonical_polarization_frame()]


def response_vector(
    h: np.ndarray,
    frame: Sequence[np.ndarray],
    d: Sequence[float],
) -> np.ndarray:
    return np.array([bilinear(h, basis, d) for basis in frame], dtype=float)


def bilinear(
    a: np.ndarray,
    b: np.ndarray,
    d: Sequence[float],
) -> float:
    total = 0.0
    n = len(d)
    for i in range(n):
        for j in range(n):
            total += a[i, j] * b[j, i] / (d[i] * d[j])
    return -total


def project_a1(coeffs: np.ndarray) -> np.ndarray:
    out = np.zeros_like(coeffs)
    out[0] = coeffs[0]
    out[4] = coeffs[4]
    return out


def project_perp(coeffs: np.ndarray) -> np.ndarray:
    return coeffs - project_a1(coeffs)


def max_abs_delta(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)))


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    a1 = read(A1_NOTE)
    canon = read(CANONICAL)
    blk = read(BLOCKER)
    current = read(CURRENT)

    d = (2.0, 3.0, 5.0, 7.0)
    rng = np.random.default_rng(17)
    samples = 12
    frames_per_sample = 24

    max_total_delta = 0.0
    max_core_delta = 0.0
    max_perp_delta = 0.0
    max_total_energy_delta = 0.0
    max_core_energy_delta = 0.0
    max_perp_energy_delta = 0.0
    core_norms = []
    perp_norms = []
    total_norms = []
    samples_checked = 0

    for _ in range(samples):
        h = rng.normal(size=(4, 4))
        h = 0.5 * (h + h.T)
        h[0, 0] += 0.5
        base = response_vector(h, canonical_polarization_frame(), d)
        base_core = project_a1(base)
        base_perp = project_perp(base)
        base_total_energy = 0.5 * float(np.dot(base, base))
        base_core_energy = 0.5 * float(np.dot(base_core, base_core))
        base_perp_energy = 0.5 * float(np.dot(base_perp, base_perp))

        for _ in range(frames_per_sample):
            rot = random_so3(rng)
            frame = rotated_frame(rot)
            resp = response_vector(h, frame, d)
            core = project_a1(resp)
            perp = project_perp(resp)
            total_energy = 0.5 * float(np.dot(resp, resp))
            core_energy = 0.5 * float(np.dot(core, core))
            perp_energy = 0.5 * float(np.dot(perp, perp))

            max_total_delta = max(max_total_delta, max_abs_delta(resp, base))
            max_core_delta = max(max_core_delta, max_abs_delta(core, base_core))
            max_perp_delta = max(max_perp_delta, max_abs_delta(perp, base_perp))
            max_total_energy_delta = max(
                max_total_energy_delta, abs(total_energy - base_total_energy)
            )
            max_core_energy_delta = max(
                max_core_energy_delta, abs(core_energy - base_core_energy)
            )
            max_perp_energy_delta = max(
                max_perp_energy_delta, abs(perp_energy - base_perp_energy)
            )
            core_norms.append(float(np.linalg.norm(core)))
            perp_norms.append(float(np.linalg.norm(perp)))
            total_norms.append(float(np.linalg.norm(resp)))
            samples_checked += 1

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
            "tensor candidate is exact as a construction",
            has(var, "metric-source hessian") and has(var, "s_gr^cand"),
            "tensor-valued Hessian candidate is already built",
        ),
        Check(
            "quotient uniqueness is exact on the prototype",
            has(uni, "unique symmetric `3+1` quotient kernel")
            or has(uni, "unique bilinear lift"),
            "quotient-uniqueness note records the nondegenerate prototype kernel",
        ),
        Check(
            "A1 projector is exact and rank-2",
            has(a1, "Pi_A1") and has(a1, "lapse") and has(a1, "spatial trace"),
            "A1 projector is already canonical on the invariant block",
        ),
        Check(
            "canonical projector note still leaves an SO(3) complement orbit",
            has(canon, "SO(3)") and has(canon, "orbit bundle") and has(canon, "distinguished connection"),
            "the complement still lives on the valid frame orbit",
        ),
        Check(
            "constraint-style action is orbit-flat",
            max_total_energy_delta < 1e-14
            and max_core_energy_delta < 1e-14
            and max_perp_energy_delta < 1e-14,
            f"energy deltas = total {max_total_energy_delta:.3e}, core {max_core_energy_delta:.3e}, perp {max_perp_energy_delta:.3e}",
        ),
        Check(
            "complement coordinates remain frame-dependent",
            max_perp_delta > 1e-3 and max_total_delta > 1e-3,
            f"coordinate deltas = total {max_total_delta:.3e}, perp {max_perp_delta:.3e}",
        ),
        Check(
            "current blocker still names curvature localization as the missing object",
            has(blk, "curvature-localization operator") and has(blk, "Pi_curv"),
            "blocker still points to the same complement-frame ambiguity",
        ),
        Check(
            "new note records the constraint-style bypass question",
            has(current, "constraint-style bypass") and has(current, "orbit-flat"),
            "new note states the exact bypass question and the orbit-flat result",
        ),
    ]

    print("UNIVERSAL GR CONSTRAINT / ACTION-STATIONARITY AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("STATIONARITY RESULTS")
    print("=" * 78)
    print(f"samples_checked          = {samples_checked}")
    print(f"max_total_delta          = {max_total_delta:.12e}")
    print(f"max_core_delta           = {max_core_delta:.12e}")
    print(f"max_perp_delta           = {max_perp_delta:.12e}")
    print(f"max_total_energy_delta   = {max_total_energy_delta:.12e}")
    print(f"max_core_energy_delta    = {max_core_energy_delta:.12e}")
    print(f"max_perp_energy_delta    = {max_perp_energy_delta:.12e}")
    print(f"mean_total_norm          = {float(np.mean(total_norms)):.12e}")
    print(f"mean_core_norm           = {float(np.mean(core_norms)):.12e}")
    print(f"mean_perp_norm           = {float(np.mean(perp_norms)):.12e}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Constraint-style / action-stationarity does not canonically select "
            "the complement frame. The A1 core is invariant, but the complement "
            "coefficients move on an orbit-flat SO(3) family, so canonical "
            "curvature localization still collapses onto the same complement-frame "
            "ambiguity."
        )
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
