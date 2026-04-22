#!/usr/bin/env python3
"""
Support runner for a proposed three-identity PMNS selector law on the affine
Hermitian chart.

This script does not claim retained closure. It checks:

1. exact chart/scalar identities already present on the retained chart;
2. numerical solution of the proposed system
      Tr(H) = Q_Koide,
      delta * q_+ = Q_Koide,
      det(H) = E2;
3. PMNS/chamber consequences at that recovered point;
4. heuristic one-cluster evidence from a bounded multi-start search.
"""
from __future__ import annotations

import math

import numpy as np
import sympy as sp
from scipy import optimize

np.set_printoptions(precision=12, suppress=True, linewidth=140)

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return cond


GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SELECTOR = math.sqrt(6.0) / 3.0
Q_KOIDE = 2.0 / 3.0
OMEGA = np.exp(2j * math.pi / 3.0)

U_Z3 = (1.0 / math.sqrt(3.0)) * np.array(
    [[1, 1, 1], [1, OMEGA, OMEGA**2], [1, OMEGA**2, OMEGA]], dtype=complex
)

T_M = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_DELTA = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
H_BASE = np.array(
    [[0, E1, -E1 - 1j * GAMMA], [E1, 0, -E2], [-E1 + 1j * GAMMA, -E2, 0]],
    dtype=complex,
)

PMNS_PERMUTATION = (2, 1, 0)

NUFIT_1SIG = {
    "s12sq": (0.295, 0.318),
    "s13sq": (0.02063, 0.02297),
    "s23sq": (0.530, 0.558),
}
NUFIT_3SIG = {
    "s12sq": (0.275, 0.345),
    "s13sq": (0.02029, 0.02391),
    "s23sq": (0.430, 0.596),
}


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def pmns_angles(H_m: np.ndarray) -> dict:
    w, V = np.linalg.eigh(H_m)
    order = np.argsort(np.real(w))
    w = np.real(w[order])
    V = V[:, order]
    P = V[list(PMNS_PERMUTATION), :]
    s13sq = abs(P[0, 2]) ** 2
    c13sq = max(1.0 - s13sq, 1e-18)
    s12sq = abs(P[0, 1]) ** 2 / c13sq
    s23sq = abs(P[1, 2]) ** 2 / c13sq
    J = float((P[0, 0] * np.conj(P[0, 1]) * np.conj(P[1, 0]) * P[1, 1]).imag)
    s12 = math.sqrt(max(s12sq, 0.0))
    c12 = math.sqrt(max(1.0 - s12sq, 0.0))
    s13 = math.sqrt(max(s13sq, 0.0))
    c13 = math.sqrt(max(c13sq, 0.0))
    s23 = math.sqrt(max(s23sq, 0.0))
    c23 = math.sqrt(max(1.0 - s23sq, 0.0))
    denom = s12 * c12 * s23 * c23 * s13 * c13 * c13
    sin_dcp = J / denom if denom > 1e-18 else 0.0
    sin_dcp = max(-1.0, min(1.0, sin_dcp))
    return {
        "s12sq": float(s12sq),
        "s13sq": float(s13sq),
        "s23sq": float(s23sq),
        "J": J,
        "sin_dcp": float(sin_dcp),
        "det_H": float(np.linalg.det(H_m).real),
    }


def signature_of(H_m: np.ndarray) -> tuple[int, int, int]:
    evals = np.linalg.eigvalsh(H_m).real
    return (
        int(np.sum(evals > 1e-10)),
        int(np.sum(np.abs(evals) < 1e-10)),
        int(np.sum(evals < -1e-10)),
    )


print("=" * 72)
print("Part A: exact chart-side identities")
print("=" * 72)

check(
    "A.1 SELECTOR^2 = Q_Koide = 2/3",
    abs(SELECTOR**2 - Q_KOIDE) < 1e-15,
    f"SELECTOR^2 = {SELECTOR**2}, Q = {Q_KOIDE}",
)
check(
    "A.2 2 * SELECTOR / sqrt(3) = E2 = sqrt(8)/3",
    abs(2.0 * SELECTOR / math.sqrt(3.0) - E2) < 1e-15,
    f"2*SELECTOR/sqrt(3) = {2.0 * SELECTOR / math.sqrt(3.0)}, E2 = {E2}",
)

m_sym, d_sym, q_sym = sp.symbols("m delta q_plus", real=True)
H_sym = sp.Matrix(H_BASE) + m_sym * sp.Matrix(T_M) + d_sym * sp.Matrix(T_DELTA) + q_sym * sp.Matrix(T_Q)
tr_H_sym = sp.simplify(sp.trace(H_sym))

check(
    "A.3 Tr(H_base) = 0",
    abs(float(np.trace(H_BASE).real)) < 1e-12,
    f"Tr(H_base) = {float(np.trace(H_BASE).real)}",
)
check(
    "A.4 Tr(H) = m on the affine chart",
    sp.simplify(tr_H_sym - m_sym) == 0,
    f"Tr(H) = {tr_H_sym}",
)
check(
    "A.5 H(m, delta, q_+) is Hermitian for real chart coordinates",
    np.allclose(H(0.66, 0.93, 0.71), H(0.66, 0.93, 0.71).conj().T, atol=1e-14),
    "checked at a generic interior point",
)

print("\n" + "=" * 72)
print("Part B: solve the proposed three-identity system")
print("=" * 72)


def proposal_residuals(x):
    m, delta, q_plus = x
    H_m = H(m, delta, q_plus)
    return [
        m - Q_KOIDE,
        delta * q_plus - Q_KOIDE,
        float(np.linalg.det(H_m).real) - E2,
    ]


x0 = np.array([Q_KOIDE, 0.93, 0.715])
x_c, info, ier, msg = optimize.fsolve(proposal_residuals, x0, xtol=1e-15, full_output=True)
m_c, d_c, q_c = x_c
residuals = proposal_residuals(x_c)
H_c = H(m_c, d_c, q_c)
det_c = float(np.linalg.det(H_c).real)

print(f"\n  Proposed-system solution:")
print(f"    m     = {m_c:.15f}")
print(f"    delta = {d_c:.15f}")
print(f"    q_+   = {q_c:.15f}")
print(f"    residuals = ({residuals[0]:+.2e}, {residuals[1]:+.2e}, {residuals[2]:+.2e})")

check(
    "B.1 proposed system solves to machine precision",
    ier == 1 and max(abs(r) for r in residuals) < 1e-12,
    f"ier = {ier}, max |res| = {max(abs(r) for r in residuals):.3e}",
)
check(
    "B.2 recovered m equals 2/3",
    abs(m_c - Q_KOIDE) < 1e-14,
    f"|m - 2/3| = {abs(m_c - Q_KOIDE):.3e}",
)
check(
    "B.3 recovered delta * q_+ equals 2/3",
    abs(d_c * q_c - Q_KOIDE) < 1e-12,
    f"|delta*q_+ - 2/3| = {abs(d_c * q_c - Q_KOIDE):.3e}",
)
check(
    "B.4 recovered det(H) equals E2",
    abs(det_c - E2) < 1e-12,
    f"|det(H) - E2| = {abs(det_c - E2):.3e}",
)

print("\n" + "=" * 72)
print("Part C: chamber and PMNS consequences at the recovered point")
print("=" * 72)

sig_base = signature_of(H_BASE)
sig_c = signature_of(H_c)
chamber_gap = q_c + d_c - math.sqrt(8.0 / 3.0)
obs_c = pmns_angles(H_c)

check(
    "C.1 recovered point preserves the H_base signature",
    sig_c == sig_base,
    f"sig(H_c) = {sig_c}, sig(H_base) = {sig_base}",
)
check(
    "C.2 recovered point is in the chamber interior",
    chamber_gap > 0,
    f"q_+ + delta - sqrt(8/3) = {chamber_gap:.6f}",
)
check(
    "C.3 recovered point has positive determinant",
    det_c > 0,
    f"det(H) = {det_c:.6f}",
)

print("\n  PMNS observables at the recovered point:")
print(f"    sin^2 theta_12 = {obs_c['s12sq']:.6f}  1sigma {NUFIT_1SIG['s12sq']}")
print(f"    sin^2 theta_13 = {obs_c['s13sq']:.6f}  1sigma {NUFIT_1SIG['s13sq']}")
print(f"    sin^2 theta_23 = {obs_c['s23sq']:.6f}  1sigma {NUFIT_1SIG['s23sq']}")
print(f"    sin(delta_CP)  = {obs_c['sin_dcp']:+.6f}")
print(f"    |Jarlskog|     = {abs(obs_c['J']):.6f}")

for ang in ("s12sq", "s13sq", "s23sq"):
    lo, hi = NUFIT_1SIG[ang]
    val = obs_c[ang]
    check(
        f"C.{ '4' if ang == 's12sq' else ('5' if ang == 's13sq' else '6') } {ang} is within NuFit 1sigma",
        lo <= val <= hi,
        f"value = {val:.6f}",
    )

check(
    "C.7 sin(delta_CP) is negative at the recovered point",
    obs_c["sin_dcp"] < 0,
    f"sin(delta_CP) = {obs_c['sin_dcp']:+.6f}",
)
check(
    "C.8 |Jarlskog| is in the current experimental comparison band",
    0.030 <= abs(obs_c["J"]) <= 0.035,
    f"|J| = {abs(obs_c['J']):.6f}",
)
check(
    "C.9 all three PMNS angles are also within the broader 3sigma bands",
    all(NUFIT_3SIG[ang][0] <= obs_c[ang] <= NUFIT_3SIG[ang][1] for ang in ("s12sq", "s13sq", "s23sq")),
    "sanity check on the recovered point",
)

print("\n" + "=" * 72)
print("Part D: heuristic uniqueness evidence in the audited search box")
print("=" * 72)

rng = np.random.default_rng(20260421)
solutions = []
for _ in range(60):
    x_start = [
        rng.uniform(0.1, 1.5),
        rng.uniform(0.5, 1.5),
        rng.uniform(0.3, 1.5),
    ]
    try:
        x_found, info, ier, _ = optimize.fsolve(proposal_residuals, x_start, xtol=1e-13, full_output=True)
    except Exception:
        continue
    if ier != 1:
        continue
    res_found = proposal_residuals(x_found)
    if max(abs(r) for r in res_found) > 1e-8:
        continue
    H_found = H(*x_found)
    sig_found = signature_of(H_found)
    chamber_found = x_found[2] + x_found[1] >= math.sqrt(8.0 / 3.0) - 1e-6
    if sig_found == sig_base and chamber_found:
        solutions.append(tuple(float(v) for v in x_found))

unique_solutions = []
for sol in solutions:
    if all(max(abs(sol[i] - other[i]) for i in range(3)) >= 1e-6 for other in unique_solutions):
        unique_solutions.append(sol)

print(f"\n  audited random starts: 60")
print(f"  chamber clusters found: {len(unique_solutions)}")
for sol in unique_solutions:
    print(f"    (m, delta, q_+) = ({sol[0]:.6f}, {sol[1]:.6f}, {sol[2]:.6f})")

check(
    "D.1 audited search box returns one chamber cluster",
    len(unique_solutions) == 1,
    f"clusters = {len(unique_solutions)}",
)

print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

if FAIL == 0:
    print(
        """
  All checks passed.

  Honest interpretation:
    - the chart/scalar identities are exact;
    - the proposed three-equation system has a clean recovered point;
    - that point gives a strong PMNS numerical fit;
    - the bounded multi-start audit found one chamber cluster.

  This is support for a candidate selector law, not retained closure.

  PMNS_SELECTOR_THREE_IDENTITY_SUPPORT = TRUE
"""
    )
else:
    print("\n  PMNS_SELECTOR_THREE_IDENTITY_SUPPORT = FALSE")
