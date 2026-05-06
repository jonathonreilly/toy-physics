#!/usr/bin/env python3
"""Direct-universal Hessian as exact isotropic supermetric normal form.

This runner sharpens the post-localization direct-universal state:

1. from the route scalar generator
   `W[J] = log det(D+J) - log det(D)`, the mixed Hessian is exactly
   `-Tr(D^-1 h D^-1 k)`;
2. on the invariant background `D = diag(a,b,b,b)`, that Hessian is already
   localized into lapse / shift / trace / shear;
3. the resulting coefficients are exactly the inverse-metric contraction
   weights;
4. therefore the current universal Hessian is already the exact kinematic
   supermetric normal form on the lifted background;
5. the remaining GR gap is the derivative / time-coupling identification, not
   the algebraic local tensor form.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import sympy


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


def symbolic_hessian_identity() -> bool:
    """Exact symbolic check of the load-bearing log-det Hessian identity."""

    a, b, s, t = sympy.symbols("a b s t", positive=True, nonzero=True)
    h00, h01, h02, h03, h11, h12, h13, h22, h23, h33 = sympy.symbols(
        "h00 h01 h02 h03 h11 h12 h13 h22 h23 h33"
    )
    k00, k01, k02, k03, k11, k12, k13, k22, k23, k33 = sympy.symbols(
        "k00 k01 k02 k03 k11 k12 k13 k22 k23 k33"
    )
    h = sympy.Matrix(
        [
            [h00, h01, h02, h03],
            [h01, h11, h12, h13],
            [h02, h12, h22, h23],
            [h03, h13, h23, h33],
        ]
    )
    k = sympy.Matrix(
        [
            [k00, k01, k02, k03],
            [k01, k11, k12, k13],
            [k02, k12, k22, k23],
            [k03, k13, k23, k33],
        ]
    )
    d = sympy.diag(a, b, b, b)
    dinv = d.inv()

    det_first_variation = sympy.diff((d + s * h).det(), s).subs(s, 0)
    jacobi_first_variation = d.det() * sympy.trace(dinv * h)
    first_ok = sympy.simplify(det_first_variation - jacobi_first_variation) == 0

    det_source = (d + s * h + t * k).det()
    mixed_hessian = sympy.diff(sympy.log(det_source), s, t).subs({s: 0, t: 0})
    target = -sympy.trace(dinv * h * dinv * k)
    mixed_ok = sympy.simplify(mixed_hessian - target) == 0
    return bool(first_ok and mixed_ok)


def symbolic_canonical_gram_identity() -> bool:
    """Exact symbolic check of the canonical lapse/shift/trace/shear weights."""

    a, b = sympy.symbols("a b", positive=True, nonzero=True)
    sqrt2 = sympy.sqrt(2)
    sqrt3 = sympy.sqrt(3)
    sqrt6 = sympy.sqrt(6)

    def sm(i: int, j: int) -> sympy.Matrix:
        m = sympy.zeros(4, 4)
        if i == j:
            m[i, j] = 1
        else:
            m[i, j] = 1 / sqrt2
            m[j, i] = 1 / sqrt2
        return m

    basis = [
        sm(0, 0),
        sm(0, 1),
        sm(0, 2),
        sm(0, 3),
        sympy.diag(0, 1 / sqrt3, 1 / sqrt3, 1 / sqrt3),
        sympy.diag(0, 1 / sqrt2, -1 / sqrt2, 0),
        sympy.diag(0, 1 / sqrt6, 1 / sqrt6, -2 / sqrt6),
        sm(1, 2),
        sm(1, 3),
        sm(2, 3),
    ]
    dinv = sympy.diag(1 / a, 1 / b, 1 / b, 1 / b)
    gram_entries = [[-sympy.trace(dinv * x * dinv * y) for y in basis] for x in basis]
    gram_mat = sympy.Matrix(gram_entries)
    expected = sympy.diag(
        -1 / a**2,
        -1 / (a * b),
        -1 / (a * b),
        -1 / (a * b),
        -1 / b**2,
        -1 / b**2,
        -1 / b**2,
        -1 / b**2,
        -1 / b**2,
        -1 / b**2,
    )
    return bool(sympy.simplify(gram_mat - expected) == sympy.zeros(10, 10))


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
    sym_hessian_ok = symbolic_hessian_identity()
    sym_gram_ok = symbolic_canonical_gram_identity()

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
        "the log-det second variation derives the universal Hessian formula",
        sym_hessian_ok,
        "sympy exact: d^2 log det(D+s h+t k)/ds dt at zero equals -Tr(D^-1 h D^-1 k)",
    )
    record(
        "the universal Hessian equals the inverse-metric contraction on the invariant background",
        max_pair_err < 1e-12,
        f"max Hessian-vs-supermetric error={max_pair_err:.3e}",
    )
    record(
        "the canonical Gram matrix has the exact symbolic lapse/shift/trace/shear weights",
        sym_gram_ok,
        "sympy exact: diag(-a^-2, -(ab)^-1 x3, -b^-2 x6) with zero off-diagonal entries",
    )
    record(
        "the canonical basis Gram matrix is exactly diagonal with the inverse-metric weights",
        max_gram_err < 1e-12 and max_diag_err < 1e-12,
        f"max offdiag/diag error=({max_gram_err:.3e}, {max_diag_err:.3e})",
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
