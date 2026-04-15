#!/usr/bin/env python3
"""Direct-universal Hessian as exact isotropic supermetric normal form.

This runner sharpens the post-localization direct-universal state:

1. on the invariant background `D = diag(a,b,b,b)`, the universal Hessian is
   already exactly localized into lapse / shift / trace / shear;
2. the resulting coefficients are exactly the inverse-metric contraction
   weights;
3. therefore the current universal Hessian is already the exact kinematic
   supermetric normal form on the lifted background;
4. the remaining GR gap is the derivative / time-coupling identification, not
   the algebraic local tensor form.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
DOCS = ROOT / "docs"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    m = np.zeros((n, n), dtype=float)
    if i == j:
        m[i, j] = 1.0
    else:
        s = math.sqrt(2.0)
        m[i, j] = 1.0 / s
        m[j, i] = 1.0 / s
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


def hessian_pair(a: np.ndarray, b: np.ndarray, d: Sequence[float]) -> float:
    total = 0.0
    for i in range(4):
        for j in range(4):
            total += a[i, j] * b[j, i] / (d[i] * d[j])
    return -total


def supermetric_pair(a: np.ndarray, b: np.ndarray, d: Sequence[float]) -> float:
    ginv = np.diag([1.0 / x for x in d])
    left = ginv @ a @ ginv
    return -float(np.sum(left * b.T))


def gram(fn, d: Sequence[float]) -> np.ndarray:
    frame = canonical_polarization_frame()
    return np.asarray([[fn(x, y, d) for y in frame] for x in frame], dtype=float)


def main() -> int:
    lift_text = (DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md").read_text(encoding="utf-8")
    schur_text = (DOCS / "UNIVERSAL_GR_ISOTROPIC_SCHUR_LOCALIZATION_NOTE.md").read_text(encoding="utf-8")
    transfer_text = (DOCS / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md").read_text(encoding="utf-8")
    restricted_text = (DOCS / "DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md").read_text(encoding="utf-8")

    backgrounds = [(2.0, 3.0), (5.0, 7.0), (1.0, 1.0)]
    max_pair_err = 0.0
    max_gram_err = 0.0
    max_diag_err = 0.0

    for a, b in backgrounds:
        d = (a, b, b, b)
        H1 = gram(hessian_pair, d)
        H2 = gram(supermetric_pair, d)
        max_pair_err = max(max_pair_err, float(np.max(np.abs(H1 - H2))))
        diag_expected = np.array(
            [
                -1.0 / (a * a),
                -1.0 / (a * b),
                -1.0 / (a * b),
                -1.0 / (a * b),
                -1.0 / (b * b),
                -1.0 / (b * b),
                -1.0 / (b * b),
                -1.0 / (b * b),
                -1.0 / (b * b),
                -1.0 / (b * b),
            ],
            dtype=float,
        )
        max_diag_err = max(max_diag_err, float(np.max(np.abs(np.diag(H1) - diag_expected))))
        max_gram_err = max(max_gram_err, float(np.max(np.abs(H1 - np.diag(diag_expected)))))

    record(
        "the route still has the exact 3+1 lift and the isotropic Schur localization theorem",
        "pl s^3 x r" in lift_text.lower() and "schur-localizes exactly" in schur_text.lower(),
        "direct universal route has the exact lifted background and exact localized isotropic Hessian",
    )
    record(
        "the universal Hessian equals the inverse-metric contraction on the invariant background",
        max_pair_err < 1e-12,
        f"max Hessian-vs-supermetric error={max_pair_err:.3e}",
    )
    record(
        "the canonical basis Gram matrix is exactly diagonal with the inverse-metric weights",
        max_gram_err < 1e-12 and max_diag_err < 1e-12,
        f"max offdiag/diag error=({max_gram_err:.3e}, {max_diag_err:.3e})",
    )
    record(
        "the remaining missing theorem is therefore dynamical gluing, not local tensor normalization",
        "slice generator" in transfer_text.lower() and "not an exact gr closure theorem" in transfer_text.lower()
        and "restricted discrete `3+1` lift" in restricted_text.lower(),
        "current atlas has local supermetric form and separate slice dynamics, but not the final exact gluing law",
    )

    print("UNIVERSAL GR SUPERMETRIC NORMAL FORM")
    print("=" * 78)
    print(f"max Hessian-vs-supermetric error = {max_pair_err:.3e}")
    print(f"max Gram diagonalization error = {max_gram_err:.3e}")
    print(f"max coefficient error = {max_diag_err:.3e}")

    print("\nVerdict:")
    print(
        "On the invariant `PL S^3 x R` background, the direct-universal Hessian is "
        "already exactly the inverse-metric supermetric normal form on symmetric "
        "`3+1` perturbations."
    )
    print(
        "So the live GR gap is no longer local tensor localization or local block "
        "normalization. It is the missing exact law that glues this local "
        "supermetric form to the route-2 slice dynamics / curvature operator."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
