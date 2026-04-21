#!/usr/bin/env python3
"""
PMNS selector iter 5: precision-sharpen test of the iter-4 hint
  delta * q_+ = Q = 2/3

Iter 4 scalar-invariant scan found the pinned-point product
delta_* * q_+* = 0.66770 very close to Q = 2/3 = 0.66667 (|dev| = 0.0010,
0.15%). Because the 6-digit-rounded pinned values already carry a ~1e-6
chart-precision, 0.001 could either be (a) the true deviation (hypothesis
wrong) or (b) slack in the 6-digit pinning (hypothesis right, pinned
values rounded away).

This iter re-pins the chamber at HIGH precision using the retained
closed-form PMNS map, reads off the exact product delta * q_+, and
compares to Q = 2/3. Then it re-pins UNDER the exact constraint
delta * q_+ = 2/3 and checks whether the resulting PMNS angles stay
within PDG 2024 3-sigma NO.

Decisive outcomes:
  D1. If high-precision delta * q_+ = 2/3 to better than 1e-8, the
      retained identity is confirmed. Iter 6 moves to its framework-
      native derivation.
  D2. If the re-pin UNDER the constraint delta * q_+ = 2/3 stays inside
      PDG 3-sigma in all three angles, the identity is at minimum
      observationally admissible.
  D3. If D1 fails at 1e-8 but passes at 1e-3, it's a near-identity
      with a small correction — iter 6 investigates the correction.
  D4. If both D1 and D2 fail, the hint is ruled out and iter 6 pivots.
"""
from __future__ import annotations

import math
import numpy as np
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


# Retained atlas constants
GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

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

# PDG 2024 central values (normal ordering) — the chamber-inversion target
TARGET = {
    "sin^2 theta_12": 0.307,
    "sin^2 theta_13": 0.0218,
    "sin^2 theta_23": 0.545,
}
# NuFit 5.3 3-sigma NO ranges
NUFIT_3SIG = {
    "sin^2 theta_12": (0.275, 0.345),
    "sin^2 theta_13": (0.02029, 0.02391),
    "sin^2 theta_23": (0.430, 0.596),
}

# Retained I1 Koide value
Q_KOIDE = 2.0 / 3.0


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


PMNS_PERMUTATION = (2, 1, 0)  # electron <-> largest eigenvalue (per retained closure theorem)


def pmns_angles_from_H(H_m: np.ndarray) -> tuple[float, float, float, float]:
    """Extract (sin^2 theta_12, sin^2 theta_13, sin^2 theta_23, delta_CP)
    from H using the EXACT same convention as the retained closure-theorem
    runner: ASCENDING eigenvalue order, then PMNS = V[PMNS_PERMUTATION, :]
    (row permutation so electron <-> largest eigenvalue)."""
    w, V = np.linalg.eigh(H_m)
    order = np.argsort(np.real(w))  # ascending
    V = V[:, order]
    P = V[list(PMNS_PERMUTATION), :]
    s13_sq = abs(P[0, 2]) ** 2
    c13_sq = max(1.0 - s13_sq, 1e-18)
    s12_sq = abs(P[0, 1]) ** 2 / c13_sq
    s23_sq = abs(P[1, 2]) ** 2 / c13_sq
    J = (P[0, 0] * np.conj(P[0, 1]) * np.conj(P[1, 0]) * P[1, 1]).imag
    s12 = math.sqrt(max(s12_sq, 0.0))
    c12 = math.sqrt(max(1.0 - s12_sq, 0.0))
    s13 = math.sqrt(max(s13_sq, 0.0))
    c13 = math.sqrt(max(c13_sq, 0.0))
    s23 = math.sqrt(max(s23_sq, 0.0))
    c23 = math.sqrt(max(1.0 - s23_sq, 0.0))
    denom = s12 * c12 * s23 * c23 * s13 * c13 * c13
    sin_dcp = J / denom if denom > 1e-18 else 0.0
    sin_dcp = max(-1.0, min(1.0, sin_dcp))
    dCP = math.asin(sin_dcp)  # convention: principal branch
    return s12_sq, s13_sq, s23_sq, dCP


# ============================================================================
# Part A: HIGH-PRECISION re-pin of the chamber to PDG central values
# ============================================================================
print("=" * 72)
print("Part A: High-precision chamber re-pin to PDG 2024 central values")
print("=" * 72)


def residuals(x):
    m, d, q = x
    H_m = H(m, d, q)
    s12, s13, s23, _ = pmns_angles_from_H(H_m)
    return [
        s12 - TARGET["sin^2 theta_12"],
        s13 - TARGET["sin^2 theta_13"],
        s23 - TARGET["sin^2 theta_23"],
    ]


# IMPORTANT: fsolve can jump across chamber basins; we need to stay within
# the A-BCC basin (signature(H_base + J) = (2, 0, 1)). Approach: use
# optimize.root with method='hybr' starting from the 6-digit seed AND use
# a small step via Levenberg-Marquardt (method='lm') with tight tolerance.
# Then verify the resulting point is still in the A-BCC basin.
x0 = np.array([0.657061, 0.933806, 0.715042])

# Step 1: verify the seed is in the A-BCC basin (det H > 0, connected to
# H_base). Compute signature of H_base and of the seed H and require match.
H_seed = H(*x0)
evals_seed, _ = np.linalg.eigh(H_seed)
sig_seed = (int(np.sum(evals_seed > 1e-12)), int(np.sum(np.abs(evals_seed) < 1e-12)),
            int(np.sum(evals_seed < -1e-12)))
evals_base, _ = np.linalg.eigh(H_BASE)
sig_base = (int(np.sum(evals_base > 1e-12)), int(np.sum(np.abs(evals_base) < 1e-12)),
            int(np.sum(evals_base < -1e-12)))
print(f"\n  H_base signature (pos, zero, neg) = {sig_base}  det = {np.linalg.det(H_BASE).real:+.6f}")
print(f"  Seed signature   (pos, zero, neg) = {sig_seed}  det = {np.linalg.det(H_seed).real:+.6f}")
A_BCC_sig = sig_base
assert sig_seed == A_BCC_sig, f"Seed {sig_seed} not in A-BCC basin {A_BCC_sig} — abort"
print(f"  Seed is in A-BCC basin (matches H_base signature).")

# Step 2: high-precision refine using Levenberg-Marquardt with small step
# Use a damped Newton to avoid basin-jumping
def residuals_scalar_sum(x):
    r = residuals(x)
    return sum(ri * ri for ri in r)

# Use scipy.optimize.least_squares with 'lm' (Levenberg-Marquardt)
res_ls = optimize.least_squares(
    residuals,
    x0,
    method='lm',
    xtol=1e-15, ftol=1e-15, gtol=1e-15,
    max_nfev=10000,
)
x_hp = res_ls.x
m_hp, delta_hp, q_hp = x_hp

# Verify basin preservation
H_hp_check = H(m_hp, delta_hp, q_hp)
evals_hp, _ = np.linalg.eigh(H_hp_check)
sig_hp = (int(np.sum(evals_hp > 1e-12)), int(np.sum(np.abs(evals_hp) < 1e-12)),
          int(np.sum(evals_hp < -1e-12)))
res_hp = residuals(x_hp)

print(f"\n  Starting seed (iter-4 6-digit): {x0}")
print(f"\n  High-precision LM refined point:")
print(f"    m_hp     = {m_hp:.15f}")
print(f"    delta_hp = {delta_hp:.15f}")
print(f"    q_hp     = {q_hp:.15f}")
print(f"  Signature (pos, zero, neg): {sig_hp}")
print(f"  Residuals (s12^2, s13^2, s23^2) - target:")
print(f"    {res_hp[0]:+.3e}, {res_hp[1]:+.3e}, {res_hp[2]:+.3e}")
print(f"  Seed-to-refined displacement: "
      f"({m_hp - x0[0]:+.3e}, {delta_hp - x0[1]:+.3e}, {q_hp - x0[2]:+.3e})")

check(
    f"A.1 high-precision re-pin preserves A-BCC basin (signature {A_BCC_sig})",
    sig_hp == A_BCC_sig,
    f"signature = {sig_hp}",
)
check(
    "A.2 high-precision re-pin stays close to seed (each coord within 1e-3)",
    max(abs(m_hp - x0[0]), abs(delta_hp - x0[1]), abs(q_hp - x0[2])) < 1e-3,
    f"max displacement = {max(abs(m_hp - x0[0]), abs(delta_hp - x0[1]), abs(q_hp - x0[2])):.3e}",
)
check(
    "A.3 high-precision residuals < 1e-12",
    all(abs(r) < 1e-12 for r in res_hp),
    f"max |residual| = {max(abs(r) for r in res_hp):.3e}",
)


# ============================================================================
# Part B: Compute delta_hp * q_hp to 15 digits; compare to Q = 2/3
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Precision test of delta * q_+ = Q = 2/3")
print("=" * 72)

product_hp = delta_hp * q_hp
print(f"\n  delta_hp * q_hp = {product_hp:.15f}")
print(f"  Q = 2/3         = {Q_KOIDE:.15f}")
print(f"  difference      = {product_hp - Q_KOIDE:+.3e}")

check(
    "B.1 delta * q_+ = 2/3 to better than 1e-8 (exact identity)",
    abs(product_hp - Q_KOIDE) < 1e-8,
    f"|delta*q_+ - 2/3| = {abs(product_hp - Q_KOIDE):.3e}",
)
check(
    "B.2 delta * q_+ = 2/3 to better than 1e-4 (strong hint)",
    abs(product_hp - Q_KOIDE) < 1e-4,
    f"|delta*q_+ - 2/3| = {abs(product_hp - Q_KOIDE):.3e}",
)
check(
    "B.3 delta * q_+ = 2/3 to better than 1e-2 (weak hint)",
    abs(product_hp - Q_KOIDE) < 1e-2,
    f"|delta*q_+ - 2/3| = {abs(product_hp - Q_KOIDE):.3e}",
)

# Also check the iter-4 other near-hit: sum lambda / sum|lambda| = 1/6
H_hp = H(m_hp, delta_hp, q_hp)
w = np.linalg.eigvalsh(H_hp)
lam_ratio = np.sum(w) / np.sum(np.abs(w))
print(f"\n  sum(lambda) / sum(|lambda|) = {lam_ratio:.15f}")
print(f"  1/6                         = {1/6:.15f}")
print(f"  difference                  = {lam_ratio - 1/6:+.3e}")

check(
    "B.4 sum lambda / sum|lambda| = 1/6 to better than 1e-4 (iter-4 #2 hint)",
    abs(lam_ratio - 1/6) < 1e-4,
    f"|sum/sum|abs| - 1/6| = {abs(lam_ratio - 1/6):.3e}",
)


# ============================================================================
# Part C: Re-pin UNDER the constraint delta * q_+ = 2/3, check PDG 3-sigma
# ============================================================================
print("\n" + "=" * 72)
print("Part C: Re-pin UNDER exact constraint delta * q_+ = 2/3; check PDG 3-sigma")
print("=" * 72)


def residuals_constrained(x):
    """Re-pin to two of the PDG angles + the constraint delta*q+ = 2/3."""
    m, d, q = x
    H_m = H(m, d, q)
    s12, s13, s23, _ = pmns_angles_from_H(H_m)
    return [
        s12 - TARGET["sin^2 theta_12"],
        s13 - TARGET["sin^2 theta_13"],
        d * q - Q_KOIDE,   # enforce delta * q_+ = 2/3
    ]


sol2 = optimize.fsolve(residuals_constrained, x_hp, xtol=1e-15, full_output=True)
x_c, info2, ier2, msg2 = sol2
m_c, d_c, q_c = x_c
H_c = H(m_c, d_c, q_c)
s12_c, s13_c, s23_c, dCP_c = pmns_angles_from_H(H_c)

print(f"\n  Constrained re-pin (delta * q_+ = 2/3 exactly):")
print(f"    m_c     = {m_c:.12f}")
print(f"    delta_c = {d_c:.12f}")
print(f"    q_c     = {q_c:.12f}")
print(f"    delta_c * q_c = {d_c * q_c:.15f}  (should be 2/3 = {Q_KOIDE:.15f})")
print(f"\n  Resulting PMNS angles:")
print(f"    sin^2 theta_12 = {s12_c:.6f}  (target {TARGET['sin^2 theta_12']}, 3sigma {NUFIT_3SIG['sin^2 theta_12']})")
print(f"    sin^2 theta_13 = {s13_c:.6f}  (target {TARGET['sin^2 theta_13']}, 3sigma {NUFIT_3SIG['sin^2 theta_13']})")
print(f"    sin^2 theta_23 = {s23_c:.6f}  (target {TARGET['sin^2 theta_23']}, 3sigma {NUFIT_3SIG['sin^2 theta_23']})")
print(f"    sin(delta_CP)  = {math.sin(dCP_c):.6f}")

# PDG-3sigma compatibility
within_3sig = (
    NUFIT_3SIG["sin^2 theta_12"][0] <= s12_c <= NUFIT_3SIG["sin^2 theta_12"][1]
    and NUFIT_3SIG["sin^2 theta_13"][0] <= s13_c <= NUFIT_3SIG["sin^2 theta_13"][1]
    and NUFIT_3SIG["sin^2 theta_23"][0] <= s23_c <= NUFIT_3SIG["sin^2 theta_23"][1]
)

check(
    "C.1 constrained re-pin has all 3 PMNS angles within NuFit 3-sigma NO",
    within_3sig,
    "s12: [%.3f, %.3f], s13: [%.4f, %.4f], s23: [%.3f, %.3f]"
    % (
        NUFIT_3SIG["sin^2 theta_12"][0], NUFIT_3SIG["sin^2 theta_12"][1],
        NUFIT_3SIG["sin^2 theta_13"][0], NUFIT_3SIG["sin^2 theta_13"][1],
        NUFIT_3SIG["sin^2 theta_23"][0], NUFIT_3SIG["sin^2 theta_23"][1],
    ),
)

# Deviation from PDG central
dev_s23 = abs(s23_c - TARGET["sin^2 theta_23"])
print(f"\n  Deviation from PDG central: sin^2 theta_23 moves by {dev_s23:+.4f}")
# The 2-angle-fixed (s12, s13) + constraint test: s23 is the one that can move.
# Ideally this would be within experimental 1-sigma.


# ============================================================================
# Part D: Gradient check — is the constraint delta*q+ = 2/3 a smooth
#          cut through the pinned chamber?
# ============================================================================
print("\n" + "=" * 72)
print("Part D: Level-set geometry of delta * q_+ = 2/3 near pinned point")
print("=" * 72)

# grad(delta * q_+) = (0, q_+, delta); at pinned this is (0, 0.715, 0.934) — non-zero.
grad_constraint = np.array([0.0, q_hp, delta_hp])
print(f"\n  grad(delta * q_+) at pinned = {grad_constraint}")
print(f"  ||grad|| = {np.linalg.norm(grad_constraint):.6f}")

check(
    "D.1 grad(delta * q_+) at pinned is non-zero (valid constraint)",
    np.linalg.norm(grad_constraint) > 1e-6,
    f"||grad|| = {np.linalg.norm(grad_constraint):.6f}",
)


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 5 attack: precision-sharpen test of iter-4 hint delta * q_+ = 2/3.

Key findings:
  - High-precision chamber re-pin: m = {m_hp:.10f},
    delta = {delta_hp:.10f}, q+ = {q_hp:.10f}
  - delta * q_+ at high-precision pinned = {product_hp:.15f}
  - Q = 2/3                             = {Q_KOIDE:.15f}
  - difference                          = {product_hp - Q_KOIDE:+.3e}

Interpretation:
  - If |delta*q_+ - 2/3| < 1e-8: CONFIRMED retained identity. Iter 6
    moves to framework-native derivation (likely via Koide I1 AM-GM
    structure applied to the chart coordinates).
  - If 1e-8 <= |delta*q_+ - 2/3| < 1e-4: near-miss with systematic
    deviation. Iter 6 investigates the correction.
  - If |delta*q_+ - 2/3| >= 1e-4: hint ruled out. Iter 6 pivots
    (remaining attacks in backlog: A5 A-BCC derivation,
    A8 cross-sector A-BCC × I2/P, A9 chamber-boundary variational,
    A10 symplectic).

Constrained re-pin (Part C) tells us whether the identity is at least
observationally admissible: the angle that's freed (sin^2 theta_23)
gives the falsifiable prediction.
""")
