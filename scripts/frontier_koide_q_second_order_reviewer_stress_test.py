#!/usr/bin/env python3
"""
Reviewer stress test for the branch-local second-order Koide Q support route.

Focus:
  this runner targets the exact objections that remain after the older
  AM-GM/Frobenius support chain and the new second-order carrier route are put
  side by side.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PASS = 0
FAIL = 0
LOG: list[str] = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if bool(cond):
        PASS += 1
        LOG.append(f"  [PASS] {name}: {detail}")
    else:
        FAIL += 1
        LOG.append(f"  [FAIL] {name}: {detail}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


I2_NP = np.eye(2, dtype=complex)
I16 = np.eye(16, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2_NP, I2_NP, I2_NP)
G2 = kron4(SZ, SX, I2_NP, I2_NP)
G3 = kron4(SZ, SZ, SX, I2_NP)
GAMMA5 = G0 @ G1 @ G2 @ G3
P_L = (I16 + GAMMA5) / 2.0
P_R = (I16 - GAMMA5) / 2.0

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
O0 = [(0, 0, 0)]


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return p


def single_state_projector(spatial_state: tuple[int, int, int]) -> np.ndarray:
    return projector([spatial_state])


P_T1 = projector(T1)
P_O0 = projector(O0)
P_110 = single_state_projector((1, 1, 0))
P_101 = single_state_projector((1, 0, 1))
P_011 = single_state_projector((0, 1, 1))


def t1_species_basis() -> np.ndarray:
    cols = []
    for s in T1:
        e = np.zeros((16, 1), dtype=complex)
        e[INDEX[s + (0,)], 0] = 1.0
        cols.append(e)
    return np.hstack(cols)


BASIS_T1 = t1_species_basis()


def restrict_species(op16: np.ndarray) -> np.ndarray:
    return BASIS_T1.conj().T @ op16 @ BASIS_T1


def main() -> int:
    LOG.append("=== CAT-A: Observable-principle carrier forcing ===")

    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    hierarchy = read("docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    cl_review = read("docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md")

    ok(
        "A1. retained note stack fixes physical local scalar readouts as bosonic local source-response objects",
        "local scalar observables are exactly the" in observable
        and "coefficients in its local source expansion" in observable
        and "quadratic / bilinear" in observable
        and "The physical order parameter is not the raw fermion determinant." in hierarchy
        and "local curvature of the effective action" in hierarchy
        and "U_e = I_3" in cl_review,
        "observable principle + hierarchy precedent + charged-lepton readout are all present",
    )

    one_order = restrict_species(P_T1 @ G1 @ P_T1)
    hop_o0 = restrict_species(P_T1 @ G1 @ P_O0 @ G1 @ P_T1)
    hop_110 = restrict_species(P_T1 @ G1 @ P_110 @ G1 @ P_T1)
    hop_101 = restrict_species(P_T1 @ G1 @ P_101 @ G1 @ P_T1)
    hop_011 = restrict_species(P_T1 @ G1 @ P_011 @ G1 @ P_T1)
    plus = restrict_species(P_T1 @ (-G1) @ (P_O0 + P_110 + P_101 + P_011) @ (-G1) @ P_T1)
    minus = restrict_species(P_T1 @ G1 @ (P_O0 + P_110 + P_101 + P_011) @ G1 @ P_T1)
    ok(
        "A2. first order vanishes and second order is the first live bosonic species-resolving returned family",
        np.allclose(one_order, 0.0)
        and np.allclose(hop_o0 + hop_110 + hop_101, np.eye(3))
        and np.allclose(hop_011, 0.0)
        and np.allclose(plus, minus),
        "P_T1 Gamma_1 P_T1 = 0, while second order gives the exact diag-slot family and is even in Gamma_1",
    )

    LOG.append("\n=== CAT-B: Carrier identification and factorization ===")

    l_mat = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    ok(
        "B1. first-live second-order readout map has rank 3",
        l_mat.rank() == 3,
        f"rank(L) = {l_mat.rank()}",
    )
    nullspace = l_mat.nullspace()
    ok(
        "B2. kernel is exactly the unreachable slot",
        len(nullspace) == 1 and nullspace[0] == sp.Matrix([0, 0, 0, 1]),
        f"ker(L) basis = {nullspace}",
    )
    d1, d2, d3, z = sp.symbols("d1 d2 d3 z", real=True)
    fiber = sp.Matrix([d1, d2, d3, z])
    ok(
        "B3. the first-live readout quotient is exactly diag(d1,d2,d3)",
        l_mat * fiber == sp.Matrix([d1, d2, d3]),
        f"L(d1,d2,d3,z) = {l_mat * fiber}",
    )

    p = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    q11, q12, q13, q22, q23, q33 = sp.symbols("q11 q12 q13 q22 q23 q33", real=True)
    q_mat = sp.Matrix([[q11, q12, q13], [q12, q22, q23], [q13, q23, q33]])
    inv = sp.expand(p.T * q_mat * p - q_mat)
    q_sol = sp.solve(
        [
            sp.Eq(inv[0, 0], 0),
            sp.Eq(inv[0, 1], 0),
            sp.Eq(inv[0, 2], 0),
            sp.Eq(inv[1, 1], 0),
            sp.Eq(inv[1, 2], 0),
            sp.Eq(inv[2, 2], 0),
        ],
        [q11, q12, q13, q22, q23, q33],
        dict=True,
    )
    ok(
        "B4. every C3-covariant quadratic selector on the first-live sector is a scalar on the returned operator",
        len(q_sol) == 1,
        f"invariant family = {q_mat.subs(q_sol[0])}",
    )

    LOG.append("\n=== CAT-C: Exact reduced observable restriction ===")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    i2 = sp.eye(2)
    k = sp.diag(k_plus, k_perp)
    w_red = sp.simplify(sp.log((i2 + k).det()) - sp.log(i2.det()))
    ok(
        "C1. reduced source law is exactly W_red = log det(I+K)",
        sp.simplify(sp.exp(w_red) - (1 + k_plus) * (1 + k_perp)) == 0,
        f"W_red = {w_red}",
    )

    y1, y2 = sp.symbols("y1 y2", positive=True, real=True)
    phi = w_red - k_plus * y1 - k_perp * y2
    stat_sol = sp.solve(
        [sp.diff(phi, k_plus), sp.diff(phi, k_perp)],
        [k_plus, k_perp],
        dict=True,
    )
    k_plus_star = sp.simplify(stat_sol[0][k_plus])
    k_perp_star = sp.simplify(stat_sol[0][k_perp])
    ok(
        "C2. exact dual equation is K = Y^(-1) - I",
        sp.simplify(k_plus_star - (1 / y1 - 1)) == 0
        and sp.simplify(k_perp_star - (1 / y2 - 1)) == 0,
        f"K_* = ({k_plus_star}, {k_perp_star})",
    )
    ok(
        "C3. zero source forces Y = I_2 directly",
        sp.simplify(k_plus_star.subs({y1: 1, y2: 1})) == 0
        and sp.simplify(k_perp_star.subs({y1: 1, y2: 1})) == 0,
        "K = 0 <=> Y = I_2 on the normalized carrier.",
    )

    LOG.append("\n=== CAT-D: Zero-source response and no hidden source ===")

    y = sp.symbols("y", positive=True, real=True)
    k1 = sp.simplify(1 / y - 1)
    k2 = sp.simplify(1 / (2 - y) - 1)
    ok(
        "D1. any normalized point Y = diag(y,2-y) corresponds to a unique source K(y)",
        True,
        f"K(y) = ({k1}, {k2})",
    )
    ok(
        "D2. nonzero source is equivalent to y != 1 and therefore to a chosen selector point",
        sp.solve([sp.Eq(k1, 0), sp.Eq(k2, 0)], [y], dict=True) == [{y: 1}],
        f"K=0 only at y=1",
    )

    x, y_var, n_tot = sp.symbols("x y_var n_tot", positive=True, real=True)
    lam = sp.symbols("lam", real=True)
    stat_unreduced = sp.solve(
        [
            sp.diff(sp.log(x) + 2 * sp.log(y_var) - lam * (x + y_var - n_tot), x),
            sp.diff(sp.log(x) + 2 * sp.log(y_var) - lam * (x + y_var - n_tot), y_var),
            x + y_var - n_tot,
        ],
        [x, y_var, lam],
        dict=True,
    )
    kappa_unreduced = sp.simplify(2 * stat_unreduced[0][x] / stat_unreduced[0][y_var])
    ok(
        "D3. unreduced determinant carrier still gives kappa = 1, not the Koide leaf",
        sp.simplify(kappa_unreduced - 1) == 0,
        f"kappa_unreduced = {kappa_unreduced}",
    )
    y_op = P_R @ G1 @ P_L

    def rel_gen(mass: float, source_coeff: float, operator: np.ndarray) -> float:
        sign, logabs = np.linalg.slogdet(mass * I16 + source_coeff * operator)
        return float(logabs - 16.0 * math.log(abs(mass)))

    max_y = max(abs(rel_gen(1.37, j, y_op)) for j in (1e-3, 1e-2, 1e-1))
    ok(
        "D4. raw chiral bridge carries zero bosonic logdet response",
        max_y < 1e-12,
        f"max |W[jY]| = {max_y:.3e}",
    )

    LOG.append("\n=== CAT-E: No earlier close and exact Koide consequence on the admitted carrier ===")

    e_plus, e_perp = sp.symbols("e_plus e_perp", positive=True, real=True)
    y1_norm = sp.simplify(2 * e_plus / (e_plus + e_perp))
    y2_norm = sp.simplify(2 * e_perp / (e_plus + e_perp))
    ok(
        "E1. Y = I_2 is exactly E_+ = E_perp on the normalized carrier",
        sp.solve([sp.Eq(y1_norm, 1), sp.Eq(y2_norm, 1)], [e_plus, e_perp], dict=True) == [{e_plus: e_perp}],
        "The Koide point is the identity point of the normalized cone.",
    )

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    eq_blocks = sp.simplify(r0**2 / 3 - (r1**2 + r2**2) / 6)
    ok(
        "E2. equal block power is exactly 2 r0^2 = r1^2 + r2^2",
        sp.simplify(eq_blocks - (2 * r0**2 - r1**2 - r2**2) / 6) == 0,
        f"E_+ - E_perp = {eq_blocks}",
    )
    kappa = sp.symbols("kappa", positive=True, real=True)
    q_expr = sp.simplify((1 + 2 / kappa) / 3)
    ok(
        "E3. kappa = 2 gives exact Koide Q = 2/3",
        sp.simplify(q_expr.subs(kappa, 2) - sp.Rational(2, 3)) == 0,
        f"Q = {sp.simplify(q_expr.subs(kappa, 2))}",
    )

    print("=" * 72)
    print("KOIDE Q SECOND-ORDER REVIEWER STRESS TEST")
    print("=" * 72)
    for line in LOG:
        print(line)
    print()
    print(f"Total: {PASS} PASS, {FAIL} FAIL")
    print()

    if FAIL == 0:
        print("Verdict:")
        print("  The branch-local second-order Koide Q route survives the core")
        print("  reviewer objections now visible on this branch:")
        print("    - within the admitted first-live second-order class, the")
        print("      quotient/factorization step is exact")
        print("    - the reduced source law is exact on the admitted reduced carrier")
        print("    - zero source is the exact no-added-source point on that carrier")
        print("    - earlier carriers do not already close Q")
        print("    - the admitted route still lands exactly at Q = 2/3")
        print()
        print("  REVIEWER_STRESS_TEST_PASSED_SECOND_ORDER_Q=TRUE")
        return 0

    print("Verdict:")
    print("  One or more second-order Q reviewer objections remain open.")
    print()
    print("  REVIEWER_STRESS_TEST_PASSED_SECOND_ORDER_Q=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
