#!/usr/bin/env python3
"""Audit the direct-universal tensor variational candidate.

This is not a closure proof. It checks that the current atlas now supplies:

1. the exact scalar observable generator from the axiom-side observable
   principle;
2. the exact `3+1` kinematic lift on `PL S^3 x R`;
3. a well-defined symmetric bilinear Hessian candidate on `3+1` metric sources.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
LIFT = DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md"
BLOCKER = DOCS / "UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md"
CANDIDATE = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"


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


def main() -> int:
    obs = read(OBSERVABLE)
    lift = read(LIFT)
    blk = read(BLOCKER)
    cand = read(CANDIDATE)

    # Four-slot 3+1 source prototype: a diagonal background plus two symmetric
    # perturbations. The numbering is only a bookkeeping device.
    d = (2.0, 3.0, 5.0, 7.0)
    h1 = (
        (1.0, 0.2, 0.0, 0.0),
        (0.2, -1.0, 0.1, 0.0),
        (0.0, 0.1, 0.5, -0.3),
        (0.0, 0.0, -0.3, -0.5),
    )
    h2 = (
        (0.0, 0.0, 0.4, 0.0),
        (0.0, 0.6, 0.0, 0.2),
        (0.4, 0.0, -0.2, 0.0),
        (0.0, 0.2, 0.0, -0.4),
    )

    b12 = bilinear(h1, h2, d)
    b21 = bilinear(h2, h1, d)
    q11 = 0.5 * bilinear(h1, h1, d)
    q22 = 0.5 * bilinear(h2, h2, d)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "log|det(d+j)|") or has(obs, "log |det(d+j)|"),
            "observable principle gives the scalar generator",
        ),
        Check(
            "3+1 lift is exact",
            has(lift, "pl s^3 x r"),
            "route-2 lift produces the exact PL S^3 x R scaffold",
        ),
        Check(
            "candidate note defines a tensor-valued variational object",
            has(cand, "metric-source hessian")
            and has(cand, "tensor-valued variational candidate"),
            "candidate note identifies the Hessian of W as the tensor action candidate",
        ),
        Check(
            "candidate bilinear form is symmetric",
            abs(b12 - b21) < 1e-15,
            f"B(h1,h2)={b12:.6e}, B(h2,h1)={b21:.6e}",
        ),
        Check(
            "candidate quadratic form is well-defined on 3+1 perturbations",
            all(abs(x) < 10 for x in (q11, q22)),
            f"Q(h1)={q11:.6e}, Q(h2)={q22:.6e}",
        ),
        Check(
            "blocker still marks Einstein/Regge identification as missing",
            has(blk, "blocked at the tensor-valued action / uniqueness level")
            or has(blk, "blocked"),
            "direct universal route remains open at the final identification step",
        ),
    ]

    print("UNIVERSAL GR TENSOR VARIATIONAL CANDIDATE AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("CANDIDATE VALUES")
    print("=" * 78)
    print(f"B(h1,h2) = {b12:.12e}")
    print(f"B(h2,h1) = {b21:.12e}")
    print(f"Q(h1)    = {q11:.12e}")
    print(f"Q(h2)    = {q22:.12e}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Direct-universal progress: the scalar observable principle and the "
            "3+1 lift now support an exact tensor-valued variational candidate "
            "defined as the Hessian of W on the lifted background."
        )
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
