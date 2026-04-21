#!/usr/bin/env python3
"""
PMNS selector iter 4: operator-commutation attack.

Context. Iters 1-3 ruled out:
  - direct doublet AM-GM (iter 1)
  - W[J] = log|det H| under any single scalar-Casimir constraint (iter 2)
  - direct Brannen-phase gate at 1e-4 precision (iter 3)

Iter 4 attack. The remaining natural class is operator-valued
constraints: the pinned point might lie on a sub-manifold
  S_O = {(m, delta, q+) : [H(m, delta, q+), O] = 0}
for some retained operator O. If dim S_O < 2, the zero-set cuts the
chamber; combined with another retained condition it could pin the
point.

What this runner tests.

  Part A. For each retained operator O, compute the commutator
    c_O(m, delta, q+) = ||[H(m, delta, q+), O]||_F^2
  and evaluate at the pinned point. If c_O(*) = 0, the pinned point
  IS a commutation point and S_O contains it.

  Part B. For each O with c_O(*) near 0, scan a chamber neighborhood
  and check dim S_O (i.e., dim of the zero-set near pinned).

  Part C. For commutators that are NOT zero at pinned, compute other
  natural scalars: (i) eigenvalue ratios of H, (ii) Re/Im ratios of
  K_12, (iii) specific trace quantities. Check whether any hits a
  retained simple value (0, 1, 1/2, 1/3, 2/3, sqrt(6)/3 = SELECTOR,
  2/9, ...) at pinned within 1e-4.

Candidate operators O tested:
  O1. C  (cyclic shift)
  O2. C + C^2 (Z_3 symmetric combination)
  O3. i(C - C^2) (Z_3 antisymmetric)
  O4. T_M (spectator perturbation direction)
  O5. T_Delta (CP-odd perturbation direction)
  O6. T_Q (even-carrier perturbation direction)
  O7. U_Z3 (Z_3 representation unitary)
  O8. P_0 = J/3 (Z_3 singlet projector on C^3)
  O9. I - P_0 (doublet projector on C^3)
  O10. H_base (retained baseline Hermitian)
  O11. diag(1, omega, omega^2) (diagonal Z_3 phase)
  O12. T_Delta + i T_Q (complex combination of CP-odd and even)

Honest outcome. Report which commutators (if any) are small or zero
at pinned, and which scalars hit retained simple values.
"""
from __future__ import annotations

import math
import cmath
import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=140)

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


# Retained atlas constants
GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
OMEGA = np.exp(2j * math.pi / 3.0)

U_Z3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)

T_M = np.array(
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex
)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
)
T_Q = np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)

M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_PLUS_STAR = 0.715042

# Cyclic shift
C_cyclic = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
# Z_3 singlet projector
J_ones = np.ones((3, 3), dtype=complex)
P0 = J_ones / 3.0
P_doublet = np.eye(3, dtype=complex) - P0

# Retained "SELECTOR" = sqrt(6)/3
SELECTOR = math.sqrt(6.0) / 3.0

OPERATORS = {
    "O1  C (cyclic shift)":       C_cyclic,
    "O2  C + C^2":                C_cyclic + C_cyclic @ C_cyclic,
    "O3  i(C - C^2)":             1j * (C_cyclic - C_cyclic @ C_cyclic),
    "O4  T_M":                    T_M,
    "O5  T_Delta":                T_DELTA,
    "O6  T_Q":                    T_Q,
    "O7  U_Z3":                   U_Z3,
    "O8  P_0 = J/3":              P0,
    "O9  I - P_0":                P_doublet,
    "O10 H_base":                 H_BASE,
    "O11 diag(1, ω, ω²)":         np.diag([1, OMEGA, OMEGA * OMEGA]),
    "O12 T_Delta + i T_Q":        T_DELTA + 1j * T_Q,
}


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def comm_norm_sq(H_m: np.ndarray, O: np.ndarray) -> float:
    """||[H, O]||_F^2 — Frobenius squared of the commutator."""
    comm = H_m @ O - O @ H_m
    return float(np.linalg.norm(comm, ord="fro") ** 2)


# ============================================================================
# Part A: Commutator norms at the pinned point
# ============================================================================
print("=" * 72)
print("Part A: ||[H(m*, delta*, q+*), O]||_F^2 for each retained operator O")
print("=" * 72)

H_star = H(M_STAR, DELTA_STAR, Q_PLUS_STAR)

print(f"\n  {'Operator':40s} {'||[H*, O]||_F^2':>16s}")
comm_vals = {}
for name, O in OPERATORS.items():
    c = comm_norm_sq(H_star, O)
    comm_vals[name] = c
    print(f"  {name:40s} {c:>16.6f}")

# Check: any commutator exactly zero at pinned?
print()
sorted_comm = sorted(comm_vals.items(), key=lambda kv: kv[1])
print("  Sorted (smallest first):")
for name, v in sorted_comm[:5]:
    print(f"    {name:40s} {v:.6f}")

for name, v in sorted_comm[:3]:
    check(
        f"A.{name}: commutator vanishes at pinned (< 1e-6)",
        v < 1e-6,
        f"||[H*, O]||_F^2 = {v:.6f}",
    )


# ============================================================================
# Part B: For the smallest commutators, scan for zero-set dimensionality
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Zero-set structure of smallest-commutator operators")
print("=" * 72)

rng = np.random.default_rng(20260421)


def scan_zero_set(O: np.ndarray, n_samples: int = 400) -> tuple[float, float, float]:
    """Scan chamber for points where ||[H, O]||_F^2 < epsilon.
    Return (min_found, mean_found, frac_near_zero) over random chamber samples.
    """
    samples = []
    for _ in range(n_samples):
        m_r = M_STAR + float(rng.uniform(-1.0, 1.0))
        d_r = DELTA_STAR + float(rng.uniform(-1.0, 1.0))
        q_min = math.sqrt(8.0 / 3.0) - d_r + 0.05
        q_r = max(q_min, Q_PLUS_STAR + float(rng.uniform(-1.0, 1.0)))
        H_here = H(m_r, d_r, q_r)
        c = comm_norm_sq(H_here, O)
        samples.append(c)
    arr = np.array(samples)
    return float(arr.min()), float(arr.mean()), float((arr < 0.1).mean())


# Only scan the top candidates
for name, v in sorted_comm[:5]:
    O = OPERATORS[name]
    mn, mean, frac_near = scan_zero_set(O)
    print(f"\n  {name}:")
    print(f"    at pinned:            {v:.6f}")
    print(f"    scan min:             {mn:.6f}")
    print(f"    scan mean:            {mean:.6f}")
    print(f"    frac (< 0.1) in scan: {frac_near:.4f}")

    # If pinned is significantly smaller than the scan mean, it's a special point
    if v > 0:
        ratio = v / mean if mean > 0 else 1.0
        print(f"    pinned / scan_mean:   {ratio:.4f}")
        check(
            f"B.{name}: pinned commutator is special (< 0.1 × scan mean)",
            ratio < 0.1,
            f"ratio = {ratio:.4f}",
        )


# ============================================================================
# Part C: Scalar invariants of H at pinned — do any hit retained simple values?
# ============================================================================
print("\n" + "=" * 72)
print("Part C: Retained-simple-value hits for scalar invariants of H*")
print("=" * 72)

# Natural retained simple values for comparison (dimensionless, ratio-like)
SIMPLE_VALUES = {
    "0":             0.0,
    "1":             1.0,
    "1/2":           0.5,
    "1/3":           1.0 / 3,
    "2/3":           2.0 / 3,
    "1/9":           1.0 / 9,
    "2/9":           2.0 / 9,
    "4/9":           4.0 / 9,
    "sqrt(6)/3":     SELECTOR,           # = 0.8165
    "1/sqrt(6)":     1.0 / math.sqrt(6), # = 0.4082
    "sqrt(2)":       math.sqrt(2),
    "sqrt(3)":       math.sqrt(3),
    "sqrt(6)":       math.sqrt(6),
    "pi":            math.pi,
    "pi/9":          math.pi / 9,
    "2*pi/9":        2 * math.pi / 9,
    "pi/3":          math.pi / 3,
    "-1":            -1.0,
    "1/6":           1.0 / 6,
    "5/6":           5.0 / 6,
    "1/sqrt(3)":     1.0 / math.sqrt(3),
    "2/sqrt(3)":     2.0 / math.sqrt(3),
    "sqrt(8/3)":     math.sqrt(8.0 / 3),  # = E1
    "sqrt(8)/3":     math.sqrt(8.0) / 3,   # = E2
}

# Scalar invariants to test
w_star, V_star = np.linalg.eigh(H_star)
w_star_sorted = np.sort(w_star)[::-1]  # descending

K_star = U_Z3.conj().T @ H_star @ U_Z3
K12 = K_star[1, 2]

scalars = {
    "det(H*)":                    float(np.linalg.det(H_star).real),
    "Tr(H*)":                     float(np.trace(H_star).real),
    "Tr(H*^2)":                   float(np.trace(H_star @ H_star).real),
    "Tr(H*^3)":                   float(np.trace(H_star @ H_star @ H_star).real),
    "lambda_1 (largest)":         float(w_star_sorted[0]),
    "lambda_2 (middle)":          float(w_star_sorted[1]),
    "lambda_3 (smallest)":        float(w_star_sorted[2]),
    "lambda_2 / lambda_1":        float(w_star_sorted[1] / w_star_sorted[0]) if w_star_sorted[0] != 0 else 0,
    "lambda_3 / lambda_1":        float(w_star_sorted[2] / w_star_sorted[0]) if w_star_sorted[0] != 0 else 0,
    "lambda_3 / lambda_2":        float(w_star_sorted[2] / w_star_sorted[1]) if w_star_sorted[1] != 0 else 0,
    "Q_Koide(|lambda_i|)":        (sum(abs(w_star_sorted))) / (sum(abs(w_star_sorted)**0.5))**2,
    "sum lambda / sum|lambda|":   float(sum(w_star_sorted) / sum(abs(w_star_sorted))),
    "Re(K_12)":                   float(K12.real),
    "Im(K_12)":                   float(K12.imag),
    "|K_12|":                     float(abs(K12)),
    "Re(K_12) / Im(K_12)":        float(K12.real / K12.imag) if K12.imag != 0 else 0,
    "Im(K_12) / Re(K_12)":        float(K12.imag / K12.real) if K12.real != 0 else 0,
    "K_00 = Tr(H*) + K_d slot":   float(K_star[0, 0].real),
    "K_11":                       float(K_star[1, 1].real),
    "K_22":                       float(K_star[2, 2].real),
    "K_11 / K_22":                float(K_star[1, 1].real / K_star[2, 2].real)
                                    if K_star[2, 2].real != 0 else 0,
    "K_11 - K_22":                float(K_star[1, 1].real - K_star[2, 2].real),
    "K_00 / K_11":                float(K_star[0, 0].real / K_star[1, 1].real)
                                    if K_star[1, 1].real != 0 else 0,
    "K_00 / sqrt(Tr(H*^2))":      float(K_star[0, 0].real / math.sqrt(np.trace(H_star @ H_star).real)),
    "sum |lambda_i|":             float(sum(abs(w_star_sorted))),
    "sum lambda_i^2":             float(sum(w_star_sorted**2)),
    "SELECTOR * m_*":             SELECTOR * M_STAR,
    "SELECTOR * delta_*":         SELECTOR * DELTA_STAR,
    "SELECTOR * q_+*":            SELECTOR * Q_PLUS_STAR,
    "q_+* + delta_*":             Q_PLUS_STAR + DELTA_STAR,
    "q_+* - delta_*":             Q_PLUS_STAR - DELTA_STAR,
    "delta_* * q_+*":             DELTA_STAR * Q_PLUS_STAR,
    "m_* + delta_* + q_+*":       M_STAR + DELTA_STAR + Q_PLUS_STAR,
}

print(f"\n  {'Scalar':40s} {'value':>12s}  {'closest simple':>18s}  {'|dev|':>10s}")
hit_count = 0
for name, v in scalars.items():
    best_name = None
    best_dev = float("inf")
    for sv_name, sv in SIMPLE_VALUES.items():
        dev = abs(v - sv)
        if dev < best_dev:
            best_dev = dev
            best_name = sv_name
    print(f"  {name:40s} {v:+.4f}  {best_name:>18s}  {best_dev:>10.4f}")
    if best_dev < 1e-4:
        hit_count += 1

print(f"\n  Total < 1e-4 hits: {hit_count}")

check(
    "C.1 at least one scalar invariant hits a retained simple value (< 1e-4)",
    hit_count >= 1,
    f"hits = {hit_count}",
)


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 4 attack: operator-commutation selector.

Part A: looked for ||[H, O]||_F^2 = 0 at pinned for each retained O.
Part B: scanned zero-set of smallest-commutator operators for
         chamber-cutting sub-manifolds.
Part C: scanned scalar invariants of H* against retained simple values.

Interpretation:
  - If any O gives ||[H*, O]||_F^2 = 0 AND zero-set is chamber-cutting
    AND has codim = 1 passing through pinned: that is the retained
    selector's first cut; combined with one more retained condition
    it closes the gate.
  - If Part C finds any scalar invariant hitting a retained simple
    value < 1e-4 at pinned: that may be the retained selector-condition
    itself (a specific identity that picks out the chamber point).
  - Otherwise: the operator-commutation class is ruled out and
    iter 5 must pivot to cross-sector or arithmetic attacks.
""")
