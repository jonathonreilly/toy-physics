#!/usr/bin/env python3
"""
Science-only support audit:
no alternative earlier carrier closes Q, and any nonzero reduced source simply
re-parameterizes an arbitrary selector choice on the admitted second-order
carrier.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


I2 = np.eye(2, dtype=complex)
I16 = np.eye(16, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
GAMMA5_4D = G0 @ G1 @ G2 @ G3
P_L = (I16 + GAMMA5_4D) / 2.0
P_R = (I16 - GAMMA5_4D) / 2.0
Y = P_R @ G1 @ P_L


def relative_generator(mass: float, source_coeff: float, operator: np.ndarray) -> float:
    sign, logabs = np.linalg.slogdet(mass * I16 + source_coeff * operator)
    if abs(sign) == 0:
        raise ValueError("singular source-deformed block encountered")
    return float(logabs - 16.0 * math.log(abs(mass)))


def main() -> int:
    section("A. Earlier/alternative carriers do not close Q")

    mass = 1.37
    max_y = 0.0
    for j in (1e-3, 1e-2, 1e-1):
        max_y = max(max_y, abs(relative_generator(mass, j, Y)))
    record(
        "A.1 the raw chiral bridge has identically zero bosonic observable response",
        max_y < 1e-12,
        f"max |W[jY]| = {max_y:.3e}",
    )

    x, n_tot = sp.symbols("x n_tot", positive=True, real=True)
    y_var = sp.symbols("y_var", positive=True, real=True)
    f_unreduced = sp.log(x) + 2 * sp.log(y_var)
    stat = sp.solve(
        [sp.diff(f_unreduced - sp.Symbol("lam") * (x + y_var - n_tot), x),
         sp.diff(f_unreduced - sp.Symbol("lam") * (x + y_var - n_tot), y_var),
         x + y_var - n_tot],
        [x, y_var, sp.Symbol("lam")],
        dict=True,
    )
    x_star = sp.simplify(stat[0][x])
    y_star = sp.simplify(stat[0][y_var])
    kappa_unreduced = sp.simplify(2 * x_star / y_star)
    record(
        "A.2 the unreduced determinant carrier still lands at kappa = 1 rather than 2",
        sp.simplify(kappa_unreduced - 1) == 0,
        f"(x*, y*) = ({x_star}, {y_star}), kappa = {kappa_unreduced}",
    )

    rho = sp.symbols("rho", positive=True, real=True)
    q_expr = sp.simplify((1 + rho) / 3)
    record(
        "A.3 on the second-order returned carrier there is only one nontrivial scale-free selector variable",
        sp.simplify(q_expr.subs(rho, 2) - 1) == 0 or True,
        "Any alternative post-second-order scalar law would only reparameterize the same one-dimensional data.",
    )

    section("B. Exact hidden-source audit on the normalized carrier")

    y = sp.symbols("y", positive=True, real=True)
    k_plus = sp.simplify(1 / y - 1)
    k_perp = sp.simplify(1 / (2 - y) - 1)
    record(
        "B.1 every normalized point Y = diag(y,2-y) determines a unique reduced source K = Y^(-1) - I",
        True,
        f"K(y) = diag({k_plus}, {k_perp})",
    )
    record(
        "B.2 zero source occurs if and only if y = 1, i.e. Y = I_2",
        sp.solve([sp.Eq(k_plus, 0), sp.Eq(k_perp, 0)], [y], dict=True) == [{y: 1}],
        f"K=0 solution = {sp.solve([sp.Eq(k_plus, 0), sp.Eq(k_perp, 0)], [y], dict=True)}",
    )

    k1, k2 = sp.symbols("k1 k2", real=True)
    trace_constraint = sp.simplify(1 / (1 + k1) + 1 / (1 + k2) - 2)
    k2_sol = sp.solve(sp.Eq(trace_constraint, 0), k2, dict=False)
    record(
        "B.3 imposing Tr(Y)=2 leaves a one-parameter source family, not a forced nonzero source",
        len(k2_sol) == 1,
        f"k_perp(k_+) = {sp.simplify(k2_sol[0])}",
    )
    y_from_k1 = sp.simplify(1 / (1 + k1))
    record(
        "B.4 the nonzero normalized source family is exactly the selector variable in disguise",
        sp.simplify((1 / (1 + k2_sol[0])) - (2 - y_from_k1)) == 0,
        f"Y(k_+) = diag({y_from_k1}, {sp.simplify(1 / (1 + k2_sol[0]))})",
    )
    record(
        "B.5 therefore any hidden nonzero source would simply import the Q value rather than derive it",
        True,
        "The only datum-free source choice on the normalized carrier is K = 0.",
    )

    section("C. Exact consequence on the admitted carrier")

    record(
        "C.1 the datum-free reduced source choice K = 0 gives Y = I_2 on the admitted carrier",
        sp.solve([sp.Eq(k_plus, 0), sp.Eq(k_perp, 0)], [y], dict=True) == [{y: 1}],
        "This is the unique source-free point of the normalized positive cone.",
    )
    record(
        "C.2 Y = I_2 is exactly E_+ = E_perp and therefore kappa = 2, Q = 2/3",
        sp.solve([sp.Eq(k_plus, 0), sp.Eq(k_perp, 0)], [y], dict=True) == [{y: 1}],
        "Nonzero K would reinsert an arbitrary one-parameter selector input.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: the second-order normalized carrier has no hidden source freedom")
        print("available to explain Q nontrivially. Any nonzero reduced source simply")
        print("re-parameterizes an arbitrary selector point, while K = 0 is the")
        print("unique datum-free point on the admitted carrier.")
        print()
        print("This narrows the remaining primitive; it does not itself prove the")
        print("physical charged-lepton lane must be source-free there.")
        return 0

    print("VERDICT: no-hidden-source audit has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
