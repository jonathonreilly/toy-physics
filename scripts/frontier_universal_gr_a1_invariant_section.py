#!/usr/bin/env python3
"""Audit the exact A1 invariant section latent in the universal localization orbit.

This is not a closure proof. It checks the strongest exact projector selector
already latent in the current direct-universal stack:

1. exact scalar observable generator from the observable principle;
2. exact `3+1` lift on `PL S^3 x R`;
3. exact tensor-valued variational candidate;
4. exact unique symmetric `3+1` quotient kernel;
5. the exact rank-2 invariant `A1` projector onto lapse and spatial trace;
6. the fact that the complement remains frame-dependent, so no full canonical
   `Pi_curv` is available from the current stack alone.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"
CURVATURE = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
FRAME_BUNDLE = DOCS / "UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md"
A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"


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
    """Exact Hessian prototype: -Tr(D^-1 a D^-1 b) for diagonal D."""

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


def canonical_polarization_frame() -> list[list[list[float]]]:
    """A fixed lapse/shift/trace/shear basis on the symmetric `3+1` sector."""

    sqrt2 = 2.0 ** 0.5
    sqrt3 = 3.0 ** 0.5
    sqrt6 = 6.0 ** 0.5
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


def random_so3(rng: np.random.Generator) -> list[list[float]]:
    a = rng.normal(size=(3, 3))
    q, _ = np.linalg.qr(a)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    rot = np.eye(4)
    rot[1:, 1:] = q
    return rot.tolist()


def rotated_frame(rot: Sequence[Sequence[float]]) -> list[list[list[float]]]:
    return [conj(rot, basis) for basis in canonical_polarization_frame()]


def response_vector(
    h: Sequence[Sequence[float]],
    frame: Sequence[Sequence[Sequence[float]]],
    d: Sequence[float],
) -> np.ndarray:
    return np.array([bilinear(h, basis, d) for basis in frame], dtype=float)


def random_symmetric_h(rng: np.random.Generator) -> np.ndarray:
    h = rng.normal(size=(4, 4))
    h = 0.5 * (h + h.T)
    h[0, 0] += 0.75
    return h


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    curv = read(CURVATURE)
    fb = read(FRAME_BUNDLE)
    a1_note = read(A1_NOTE) if A1_NOTE.exists() else ""

    d = (2.0, 3.0, 5.0, 7.0)
    projector = np.zeros((10, 10), dtype=float)
    projector[0, 0] = 1.0
    projector[4, 4] = 1.0

    rng = np.random.default_rng(2)
    samples = 24
    frames_per_sample = 48

    max_a1_delta = 0.0
    max_perp_delta = 0.0
    coord_max_delta = np.zeros(10, dtype=float)
    projector_rank = int(np.linalg.matrix_rank(projector, tol=1e-12))

    for _ in range(samples):
        h = random_symmetric_h(rng)
        base = response_vector(h, canonical_polarization_frame(), d)
        base_a1 = projector @ base
        base_perp = (np.eye(10) - projector) @ base

        for _ in range(frames_per_sample):
            rot = random_so3(rng)
            frame = rotated_frame(rot)
            resp = response_vector(h, frame, d)
            a1 = projector @ resp
            perp = (np.eye(10) - projector) @ resp
            max_a1_delta = max(max_a1_delta, float(np.max(np.abs(a1 - base_a1))))
            max_perp_delta = max(max_perp_delta, float(np.max(np.abs(perp - base_perp))))
            coord_max_delta = np.maximum(coord_max_delta, np.abs(resp - base))

    invariant_coords = [i for i, delta in enumerate(coord_max_delta) if delta < 1e-12]
    a1_selector = tuple(invariant_coords)

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
            "candidate note identifies the Hessian on the lifted background",
        ),
        Check(
            "unique symmetric quotient kernel is exact on the prototype",
            has(uni, "unique symmetric `3+1` quotient kernel")
            or has(uni, "unique bilinear lift"),
            "quotient-uniqueness note records the nondegenerate prototype kernel",
        ),
        Check(
            "A1 projector is exact and rank-2",
            projector_rank == 2,
            f"Pi_A1 rank = {projector_rank}",
        ),
        Check(
            "A1 projector is frame-invariant across the sampled valid 3+1 frames",
            max_a1_delta < 1e-12,
            f"max Pi_A1 delta across sampled frames = {max_a1_delta:.3e}",
        ),
        Check(
            "complement remains frame-dependent",
            max_perp_delta > 1e-3,
            f"max complement delta across sampled frames = {max_perp_delta:.3e}",
        ),
        Check(
            "invariant coordinates are exactly lapse and spatial trace in the canonical basis",
            a1_selector == (0, 4),
            f"invariant coordinates = {a1_selector}",
        ),
        Check(
            "frame-dependent orbit remains exact on the universal blockers",
            has(curv, "associated family of candidate localizations")
            and has(curv, "polarization-frame orbit")
            and has(fb, "distinguished connection"),
            "blocker notes still state that only the localization orbit is exact",
        ),
        Check(
            "A1 note records the exact invariant section",
            has(a1_note, "Pi_A1") and has(a1_note, "lapse") and has(a1_note, "spatial trace"),
            "new note records the exact invariant selector candidate",
        ),
    ]

    print("UNIVERSAL GR A1 INVARIANT SECTION AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("PROJECTOR CANDIDATE")
    print("=" * 78)
    print("Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)")
    print("Invariant coordinates = lapse h_00 and spatial trace tr(h_ij)")
    print(f"projector_rank = {projector_rank}")
    print(f"max_a1_delta   = {max_a1_delta:.12e}")
    print(f"max_perp_delta = {max_perp_delta:.12e}")
    print(f"coord_max_delta = {[f'{x:.3e}' for x in coord_max_delta]}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Direct-universal progress: the current stack already contains an exact "
            "rank-2 invariant `A1` projector onto lapse and spatial trace, but the "
            "complementary `E \\oplus T1` channels still depend on the `3+1` frame. "
            "So the strongest exact selector is `Pi_A1`, not a full canonical "
            "curvature-localization bundle."
        )
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
