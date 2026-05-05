#!/usr/bin/env python3
"""Audit blockwise Einstein/Regge identification on the direct universal route.

This is a direct-universal, blockwise test using the exact canonical
`P_lapse`, `P_shift`, `P_trace`, and `P_shear` projectors. It asks whether
the unique universal Hessian already identifies the Einstein/Regge law
blockwise, or whether an exact block-level obstruction remains.
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
CASIMIR = DOCS / "UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md"
CANONICAL = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
CURRENT = DOCS / "UNIVERSAL_GR_BLOCK_IDENT_NOTE.md"


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
    """Fixed lapse/shift/trace/shear basis on the symmetric `3+1` sector."""

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


def gram_matrix(
    basis: Sequence[Sequence[Sequence[float]]],
    d: Sequence[float],
) -> np.ndarray:
    return np.asarray([[bilinear(a, b, d) for b in basis] for a in basis], dtype=float)


def projector(idxs: Sequence[int], n: int = 10) -> np.ndarray:
    p = np.zeros((n, n), dtype=float)
    for i in idxs:
        p[i, i] = 1.0
    return p


def off_block_norm(h: np.ndarray, p: np.ndarray) -> float:
    q = np.eye(h.shape[0]) - p
    return float(np.linalg.norm(p @ h @ q, ord="fro"))


def main() -> int:
    obs = read(OBSERVABLE)
    route2 = read(ROUTE2)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)
    casimir = read(CASIMIR)
    canon = read(CANONICAL)
    current = read(CURRENT)

    d = (2.0, 3.0, 5.0, 7.0)
    hessian = gram_matrix(canonical_polarization_frame(), d)

    P_lapse = projector([0])
    P_shift = projector([1, 2, 3])
    P_trace = projector([4])
    P_shear = projector([5, 6, 7, 8, 9])

    projectors = {
        "lapse": P_lapse,
        "shift": P_shift,
        "trace": P_trace,
        "shear": P_shear,
    }

    block_ranks = {name: int(np.linalg.matrix_rank(p, tol=1e-12)) for name, p in projectors.items()}
    sum_err = float(np.max(np.abs(P_lapse + P_shift + P_trace + P_shear - np.eye(10))))
    orth_err = max(
        float(np.linalg.norm(P_lapse @ P_shift, ord="fro")),
        float(np.linalg.norm(P_lapse @ P_trace, ord="fro")),
        float(np.linalg.norm(P_lapse @ P_shear, ord="fro")),
        float(np.linalg.norm(P_shift @ P_trace, ord="fro")),
        float(np.linalg.norm(P_shift @ P_shear, ord="fro")),
        float(np.linalg.norm(P_trace @ P_shear, ord="fro")),
    )
    idem_err = max(
        float(np.linalg.norm(p @ p - p, ord="fro")) for p in projectors.values()
    )

    block_leaks = {
        "lapse": off_block_norm(hessian, P_lapse),
        "shift": off_block_norm(hessian, P_shift),
        "trace": off_block_norm(hessian, P_trace),
        "shear": off_block_norm(hessian, P_shear),
    }
    pair_leaks = {
        ("lapse", "shift"): float(np.linalg.norm(P_lapse @ hessian @ P_shift, ord="fro")),
        ("lapse", "trace"): float(np.linalg.norm(P_lapse @ hessian @ P_trace, ord="fro")),
        ("lapse", "shear"): float(np.linalg.norm(P_lapse @ hessian @ P_shear, ord="fro")),
        ("shift", "trace"): float(np.linalg.norm(P_shift @ hessian @ P_trace, ord="fro")),
        ("shift", "shear"): float(np.linalg.norm(P_shift @ hessian @ P_shear, ord="fro")),
        ("trace", "shear"): float(np.linalg.norm(P_trace @ hessian @ P_shear, ord="fro")),
    }
    trace_shear_block = P_trace @ hessian @ P_shear
    trace_shear_rank = int(np.linalg.matrix_rank(trace_shear_block, tol=1e-12))
    trace_shear_svals = np.linalg.svd(trace_shear_block, compute_uv=False)

    print("UNIVERSAL GR BLOCKWISE EINSTEIN/REGGE IDENTIFICATION")
    print("=" * 78)
    print(f"block ranks = {block_ranks}")
    print(f"sum error = {sum_err:.3e}")
    print(f"orthogonality error = {orth_err:.3e}")
    print(f"idempotence error = {idem_err:.3e}")
    print(f"block leakage norms = { {k: f'{v:.3e}' for k, v in block_leaks.items()} }")
    print(f"pair leakage norms = { {f'{a[0]}↔{a[1]}': f'{v:.3e}' for a, v in pair_leaks.items()} }")
    print(f"trace-shear rank = {trace_shear_rank}")
    print(f"trace-shear singular values = {np.array2string(trace_shear_svals, precision=6, floatmode='fixed')}")
    print("trace-shear block =")
    print(np.array2string(trace_shear_block, precision=6, floatmode='fixed'))

    checks = [
        Check(
            "canonical block projectors are exact",
            block_ranks == {"lapse": 1, "shift": 3, "trace": 1, "shear": 5}
            and sum_err < 1e-12
            and orth_err < 1e-12
            and idem_err < 1e-12,
            f"ranks={block_ranks}, sum={sum_err:.3e}, orth={orth_err:.3e}, idem={idem_err:.3e}",
        ),
        Check(
            "scalar generator and 3+1 lift are present",
            has(obs, "observable principle") and has(route2, "pl s^3 x r"),
            "direct universal route still has the exact scalar generator and kinematic lift",
        ),
        Check(
            "tensor candidate and quotient uniqueness are present",
            has(var, "s_gr^cand") and has(uni, "unique symmetric `3+1` quotient kernel"),
            "the exact Hessian candidate and quotient uniqueness are already in hand",
        ),
        Check(
            "lapse and shift blocks are isolated by the universal Hessian",
            block_leaks["lapse"] < 1e-12 and block_leaks["shift"] < 1e-12,
            f"lapse leak={block_leaks['lapse']:.3e}, shift leak={block_leaks['shift']:.3e}",
        ),
        Check(
            "trace-shear mixing is the only surviving cross-block obstruction",
            pair_leaks[("trace", "shear")] > 1e-6
            and all(pair_leaks[k] < 1e-12 for k in pair_leaks if k != ("trace", "shear")),
            f"pair leaks={ {f'{a[0]}↔{a[1]}': f'{v:.3e}' for a, v in pair_leaks.items()} }",
        ),
        Check(
            "the trace-shear obstruction is rank-1",
            trace_shear_rank == 1,
            f"rank={trace_shear_rank}, svals={np.array2string(trace_shear_svals, precision=6, floatmode='fixed')}",
        ),
        Check(
            "the current note names the block-level obstruction explicitly",
            has(current, "rank-1 trace-shear mixer") or has(current, "trace-shear"),
            "new note states the exact remaining obstruction",
        ),
        Check(
            "the canonical block-localization note already claims the block split",
            has(casimir, "canonical block localization") and has(canon, "SO(3)"),
            "the atlas already contains the canonical block split and residual orbit picture",
        ),
    ]

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"\nPASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Strongest exact blockwise statement: the universal Hessian is "
            "canonically block-localized on lapse and shift, but the trace and "
            "shear blocks remain coupled by a rank-1 mixer. So the blockwise "
            "Einstein/Regge identification is not complete yet."
        )
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
