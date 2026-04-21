#!/usr/bin/env python3
"""
PMNS selector iter 1: doublet-block AM-GM variational attack.

Context. The framework has:
  - Exact affine Hermitian chart H(m, delta, q+) = H_base + m T_m + delta T_delta + q+ T_q
    (DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16)
  - Chamber q+ >= sqrt(8/3) - delta (ACTIVE_HALF_PLANE)
  - Z_3-doublet-block chamber-blindness (Z3_DOUBLET_BLOCK_*): K = U_Z3^dag H U_Z3
    has FROZEN singlet-doublet slots K_01 = a_*, K_02 = b_*, while the doublet
    block K_d = K[1:3, 1:3] moves by an exact 2-real law in (delta, q+).
  - Physical pinned point (m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042),
    derived as the unique chamber inversion of PDG (sin^2 theta_12, sin^2 theta_13,
    sin^2 theta_23) under the A-BCC and sigma_hier = (2, 1, 0) rules.

The open item. The Z_3 center law is "too weak": it leaves a positive-sheet
family on the 2-real doublet manifold rather than uniquely picking the
physical point. The question: is there a FRAMEWORK-NATIVE functional on
the doublet block whose extremum is the physical pinned point?

Attack. Parallel to the I1 Koide closure: on Herm_circ(3) the AM-GM
extremum of log(E_+ * E_perp) under fixed Frobenius E_+ + E_perp = N forces
kappa = 2 and Q = 2/3. Here we test the direct analog on the DOUBLET BLOCK
Herm_2(C):

  E_sym_d  = (tr K_d)^2 / 2        (scalar-subspace Frobenius energy)
  E_anti_d = Tr(K_d^2) - E_sym_d   (traceless-subspace Frobenius energy)
  F_d(m, delta, q+) = log(E_sym_d) + log(E_anti_d)

The AM-GM extremum condition is E_sym_d = E_anti_d at the critical point.

What this runner tests.
  A. Explicit numerical construction of K(m, delta, q+) on a chamber
     lattice of (m, delta, q+) and verification of the frozen slots
     K_01 = a_*, K_02 = b_* and the 2-real-law inversion
     q+ = sqrt(8/3) - (K_11 + K_22)/2,
     delta = (Im K_12 + 4 sqrt(2)/3) / sqrt(3).
  B. Evaluation of E_sym_d and E_anti_d at the physical pinned point.
  C. Evaluation of ∇F_d at the pinned point: is it a critical point of
     the doublet AM-GM functional?
  D. Full 2D variational scan over the (delta, q+) chamber: where is the
     global maximum of F_d, and does it coincide with the pinned point?
  E. Full 3D variational scan over (m, delta, q+) including the spectator
     direction; same question.

Honest outcome reporting. If the pinned point IS the critical point of F_d,
we have the retained selector (iter 1 closes the gate). If it is NOT,
report the exact gap (distance on the chart, value of F_d at pinned vs at
the critical point) and identify the direction(s) in which the pinned
point deviates from the AM-GM extremum — that failure mode informs iter 2.
"""
from __future__ import annotations

import math
import numpy as np
from scipy import optimize

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


# ============================================================================
# Retained atlas constants (copied verbatim from
# frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py)
# ============================================================================

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

# Physical pinned chamber point
M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_PLUS_STAR = 0.715042

# Frozen singlet-doublet slots (from Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS
# theorem). These are chamber-independent; we will verify numerically.
# a_* = K_01, b_* = K_02 quoted in the briefing
A_STAR_EXPECTED = 0.16993211 + 1.19280904j
B_STAR_EXPECTED = 0.45860725 - 0.69280904j


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    """Retained affine Hermitian chart on the live source-oriented sheet."""
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def K_z3(m: float, delta: float, q_plus: float) -> np.ndarray:
    """K = U_Z3^dag H U_Z3 on the Z_3 isotype basis."""
    H_m = H(m, delta, q_plus)
    return U_Z3.conj().T @ H_m @ U_Z3


def doublet_block(K: np.ndarray) -> np.ndarray:
    """Extract the 2x2 doublet block K_d = K[1:3, 1:3]."""
    return K[1:3, 1:3]


def doublet_amgm_energies(K_d: np.ndarray) -> tuple[float, float]:
    """Return (E_sym_d, E_anti_d) — the scalar and traceless Frobenius
    energies of the 2x2 doublet block under the canonical Herm_2(C) isotype
    split.

    E_sym_d  = ||P_I(K_d)||_F^2 = (tr K_d)^2 / 2
    E_anti_d = ||(I - P_I)(K_d)||_F^2 = Tr(K_d @ K_d) - E_sym_d
    """
    tr = np.trace(K_d).real  # Hermitian -> real trace
    E_sym = tr ** 2 / 2.0
    E_total = np.trace(K_d @ K_d).real  # for Hermitian M, Tr(M M) real
    E_anti = E_total - E_sym
    return float(E_sym), float(E_anti)


def F_doublet(m: float, delta: float, q_plus: float) -> float:
    """AM-GM functional on the doublet block: F_d = log(E_sym * E_anti)."""
    K = K_z3(m, delta, q_plus)
    K_d = doublet_block(K)
    E_sym, E_anti = doublet_amgm_energies(K_d)
    if E_sym <= 0 or E_anti <= 0:
        return float("-inf")
    return math.log(E_sym) + math.log(E_anti)


# ============================================================================
# Part A: Sanity checks — retained atlas, frozen slots, 2-real law
# ============================================================================
print("=" * 72)
print("Part A: Retained atlas sanity + 2-real law verification")
print("=" * 72)

H_star = H(M_STAR, DELTA_STAR, Q_PLUS_STAR)
K_star = K_z3(M_STAR, DELTA_STAR, Q_PLUS_STAR)

# A.1: chamber interior
chamber_gap = Q_PLUS_STAR - (math.sqrt(8.0 / 3.0) - DELTA_STAR)
check(
    "A.1 pinned point is strictly inside active half-plane",
    chamber_gap > 0,
    f"q+ - (sqrt(8/3) - delta) = {chamber_gap:.6f}",
)

# A.2: Hermiticity of H
check(
    "A.2 H(m*, delta*, q+*) is Hermitian",
    np.allclose(H_star, H_star.conj().T, atol=1e-12),
    f"||H - H^dag||_F = {np.linalg.norm(H_star - H_star.conj().T):.3e}",
)

# A.3: frozen singlet-doublet slots at pinned point
check(
    "A.3 K[0,1] matches the retained a_* slot",
    np.abs(K_star[0, 1] - A_STAR_EXPECTED) < 1e-6,
    f"|K01 - a_*| = {np.abs(K_star[0, 1] - A_STAR_EXPECTED):.3e}",
)
check(
    "A.4 K[0,2] matches the retained b_* slot",
    np.abs(K_star[0, 2] - B_STAR_EXPECTED) < 1e-6,
    f"|K02 - b_*| = {np.abs(K_star[0, 2] - B_STAR_EXPECTED):.3e}",
)

# A.5: verify 2-real doublet law at pinned point
K_d_star = doublet_block(K_star)
q_plus_from_K = math.sqrt(8.0 / 3.0) - (K_d_star[0, 0].real + K_d_star[1, 1].real) / 2.0
delta_from_K = (K_d_star[0, 1].imag + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)
check(
    "A.5 q_+ = sqrt(8/3) - (K_11 + K_22)/2 holds at pinned point",
    abs(q_plus_from_K - Q_PLUS_STAR) < 1e-9,
    f"q+ recovered = {q_plus_from_K:.6f} vs q+* = {Q_PLUS_STAR:.6f}",
)
check(
    "A.6 delta = (Im K_12 + 4 sqrt(2)/3) / sqrt(3) holds at pinned point",
    abs(delta_from_K - DELTA_STAR) < 1e-9,
    f"delta recovered = {delta_from_K:.6f} vs delta* = {DELTA_STAR:.6f}",
)

# A.7: frozen-slot chamber-blindness on a few random chamber points
rng = np.random.default_rng(20260421)
blind_checks_pass = 0
blind_checks_total = 10
for _ in range(blind_checks_total):
    # Sample a random (m, delta, q+) inside the chamber
    m_r = float(rng.uniform(-3.0, 3.0))
    delta_r = float(rng.uniform(-1.5, 1.5))
    q_min = math.sqrt(8.0 / 3.0) - delta_r
    q_r = float(rng.uniform(q_min + 0.01, q_min + 2.0))
    K_r = K_z3(m_r, delta_r, q_r)
    if (
        np.abs(K_r[0, 1] - A_STAR_EXPECTED) < 1e-6
        and np.abs(K_r[0, 2] - B_STAR_EXPECTED) < 1e-6
    ):
        blind_checks_pass += 1
check(
    f"A.7 frozen slots K_01 = a_*, K_02 = b_* on {blind_checks_total} random chamber points",
    blind_checks_pass == blind_checks_total,
    f"pass {blind_checks_pass}/{blind_checks_total}",
)


# ============================================================================
# Part B: AM-GM functional evaluation at the physical pinned point
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Evaluate E_sym_d, E_anti_d, F_d at the pinned point")
print("=" * 72)

E_sym_star, E_anti_star = doublet_amgm_energies(K_d_star)
F_star = F_doublet(M_STAR, DELTA_STAR, Q_PLUS_STAR)

print(f"\n  At (m*, delta*, q_+*) = ({M_STAR:.6f}, {DELTA_STAR:.6f}, {Q_PLUS_STAR:.6f}):")
print(f"    E_sym_d   = {E_sym_star:.6f}")
print(f"    E_anti_d  = {E_anti_star:.6f}")
print(f"    ratio     = E_sym / E_anti = {E_sym_star / E_anti_star:.6f}")
print(f"    F_d       = log(E_sym) + log(E_anti) = {F_star:.6f}")

check(
    "B.1 E_sym_d > 0 at pinned point",
    E_sym_star > 0,
    f"E_sym = {E_sym_star:.6f}",
)
check(
    "B.2 E_anti_d > 0 at pinned point",
    E_anti_star > 0,
    f"E_anti = {E_anti_star:.6f}",
)
# AM-GM extremum predicts E_sym = E_anti at the critical point
check(
    "B.3 AM-GM prediction: E_sym_d = E_anti_d at critical point (naive)",
    abs(E_sym_star - E_anti_star) < 1e-3,
    f"|E_sym - E_anti| = {abs(E_sym_star - E_anti_star):.6f}"
    f" (ratio = {E_sym_star / E_anti_star:.3f})",
)


# ============================================================================
# Part C: Gradient of F_d at the pinned point (critical-point test)
# ============================================================================
print("\n" + "=" * 72)
print("Part C: Gradient of F_d at the pinned point")
print("=" * 72)


def grad_F_d_numeric(m: float, delta: float, q_plus: float, h: float = 1e-6):
    """Numerical gradient of F_d at (m, delta, q+)."""
    F0 = F_doublet(m, delta, q_plus)
    dF_dm = (F_doublet(m + h, delta, q_plus) - F0) / h
    dF_dd = (F_doublet(m, delta + h, q_plus) - F0) / h
    dF_dq = (F_doublet(m, delta, q_plus + h) - F0) / h
    return np.array([dF_dm, dF_dd, dF_dq])


grad_star = grad_F_d_numeric(M_STAR, DELTA_STAR, Q_PLUS_STAR)
print(f"\n  grad F_d at pinned point:")
print(f"    dF_d / dm      = {grad_star[0]:+.6f}")
print(f"    dF_d / ddelta  = {grad_star[1]:+.6f}")
print(f"    dF_d / dq+     = {grad_star[2]:+.6f}")

grad_norm = np.linalg.norm(grad_star)
check(
    "C.1 ||grad F_d|| small at pinned point (critical-point test)",
    grad_norm < 1e-3,
    f"||grad F_d|| = {grad_norm:.6f}",
)

# The spectator direction m might not affect F_d (pure doublet-block observable);
# check that separately from (delta, q+).
grad_doublet_dir = np.array([grad_star[1], grad_star[2]])
check(
    "C.2 ||grad F_d||_{delta, q+} (restricted to 2-real manifold) small at pinned",
    np.linalg.norm(grad_doublet_dir) < 1e-3,
    f"|dF/ddelta| = {abs(grad_star[1]):.6f}, |dF/dq+| = {abs(grad_star[2]):.6f}",
)


# ============================================================================
# Part D: Full 2D scan of F_d over (delta, q+) at m = m_* fixed
# ============================================================================
print("\n" + "=" * 72)
print("Part D: 2D scan of F_d over (delta, q+) chamber slice at m = m_*")
print("=" * 72)


# Use bounded chamber-local optimization so the scan probes the local
# neighborhood of the pinned point, not unbounded growth of F_d.
DELTA_BOUND = (DELTA_STAR - 3.0, DELTA_STAR + 3.0)
Q_BOUND = (Q_PLUS_STAR - 3.0, Q_PLUS_STAR + 3.0)
M_BOUND = (M_STAR - 3.0, M_STAR + 3.0)


def neg_F_d_2d(x):
    delta, q_plus = x
    # Enforce chamber: q+ >= sqrt(8/3) - delta
    chamber = q_plus - (math.sqrt(8.0 / 3.0) - delta)
    if chamber < 0:
        return 1e6 - chamber * 1e6
    return -F_doublet(M_STAR, delta, q_plus)


best_F = -float("inf")
best_xy = None
n_starts = 40
for _ in range(n_starts):
    delta_0 = float(rng.uniform(DELTA_BOUND[0], DELTA_BOUND[1]))
    q_min = math.sqrt(8.0 / 3.0) - delta_0 + 0.05
    q_0 = float(rng.uniform(max(q_min, Q_BOUND[0]), Q_BOUND[1]))
    result = optimize.minimize(
        neg_F_d_2d,
        x0=[delta_0, q_0],
        method="Nelder-Mead",
        bounds=[DELTA_BOUND, Q_BOUND],
        options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 10000},
    )
    if -result.fun > best_F:
        d_r, q_r = result.x
        if q_r >= math.sqrt(8.0 / 3.0) - d_r - 1e-6:
            best_F = -result.fun
            best_xy = result.x

if best_xy is None:
    print("  [WARN] 2D scan did not find a finite interior maximum")
else:
    delta_max, q_plus_max = best_xy
    print(f"\n  2D scan over (delta, q+) at m = m_* = {M_STAR:.6f}:")
    print(f"    Global max F_d found at:")
    print(f"      delta = {delta_max:.6f}")
    print(f"      q+    = {q_plus_max:.6f}")
    print(f"      F_d   = {best_F:.6f}")
    print(f"    Pinned point was:")
    print(f"      delta_* = {DELTA_STAR:.6f}")
    print(f"      q_+*    = {Q_PLUS_STAR:.6f}")
    print(f"      F_d(*)  = {F_star:.6f}")
    gap_delta = abs(delta_max - DELTA_STAR)
    gap_q = abs(q_plus_max - Q_PLUS_STAR)
    gap_F = best_F - F_star
    check(
        "D.1 2D F_d scan maximum coincides with pinned (delta_*, q_+*)",
        gap_delta < 1e-3 and gap_q < 1e-3,
        f"|delta_max - delta_*| = {gap_delta:.6f}, |q+_max - q+*| = {gap_q:.6f}",
    )
    check(
        "D.2 F_d at the pinned point equals the 2D scan maximum value",
        abs(gap_F) < 1e-4,
        f"F_d(max) - F_d(*) = {gap_F:+.6e}",
    )


# ============================================================================
# Part E: Full 3D scan of F_d over (m, delta, q+)
# ============================================================================
print("\n" + "=" * 72)
print("Part E: 3D scan of F_d over (m, delta, q+)")
print("=" * 72)


def neg_F_d_3d(x):
    m, delta, q_plus = x
    # Enforce chamber: q+ >= sqrt(8/3) - delta
    chamber = q_plus - (math.sqrt(8.0 / 3.0) - delta)
    if chamber < 0:
        return 1e6 - chamber * 1e6
    return -F_doublet(m, delta, q_plus)


best_F_3d = -float("inf")
best_xyz = None
for _ in range(60):
    m_0 = float(rng.uniform(M_BOUND[0], M_BOUND[1]))
    delta_0 = float(rng.uniform(DELTA_BOUND[0], DELTA_BOUND[1]))
    q_min = math.sqrt(8.0 / 3.0) - delta_0 + 0.05
    q_0 = float(rng.uniform(max(q_min, Q_BOUND[0]), Q_BOUND[1]))
    result = optimize.minimize(
        neg_F_d_3d,
        x0=[m_0, delta_0, q_0],
        method="Nelder-Mead",
        bounds=[M_BOUND, DELTA_BOUND, Q_BOUND],
        options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000},
    )
    if -result.fun > best_F_3d:
        m_r, d_r, q_r = result.x
        if q_r >= math.sqrt(8.0 / 3.0) - d_r - 1e-6:
            best_F_3d = -result.fun
            best_xyz = result.x

if best_xyz is None:
    print("  [WARN] 3D scan did not find a finite interior maximum")
else:
    m_max, delta_max_3d, q_plus_max_3d = best_xyz
    print(f"\n  3D scan over (m, delta, q+):")
    print(f"    Global max F_d found at:")
    print(f"      m     = {m_max:.6f}")
    print(f"      delta = {delta_max_3d:.6f}")
    print(f"      q+    = {q_plus_max_3d:.6f}")
    print(f"      F_d   = {best_F_3d:.6f}")
    print(f"    Pinned point:")
    print(f"      m_*     = {M_STAR:.6f}")
    print(f"      delta_* = {DELTA_STAR:.6f}")
    print(f"      q_+*    = {Q_PLUS_STAR:.6f}")
    print(f"      F_d(*)  = {F_star:.6f}")
    gap_m = abs(m_max - M_STAR)
    gap_delta_3d = abs(delta_max_3d - DELTA_STAR)
    gap_q_3d = abs(q_plus_max_3d - Q_PLUS_STAR)
    check(
        "E.1 3D F_d scan maximum coincides with pinned (m_*, delta_*, q_+*)",
        gap_m < 1e-3 and gap_delta_3d < 1e-3 and gap_q_3d < 1e-3,
        f"|m_max - m_*| = {gap_m:.6f}, "
        f"|delta_max - delta_*| = {gap_delta_3d:.6f}, "
        f"|q+_max - q+*| = {gap_q_3d:.6f}",
    )


# ============================================================================
# Summary and verdict
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print("""
Iter 1 attack: doublet-block AM-GM variational functional
  F_d(m, delta, q+) = log((tr K_d)^2 / 2) + log(Tr(K_d^2) - (tr K_d)^2 / 2)
on the 2-real manifold (delta, q+) of the Z_3 doublet block.

Hypothesis under test: the physical pinned point (m_*, delta_*, q_+*)
is the extremum of F_d, i.e., F_d is the retained framework-native
selector for the PMNS angle triple.

Interpretation of results:
  - If Parts B, C, D, E all PASS ==> F_d IS the retained selector.
    The PMNS angle-triple gate closes at iter 1 via this functional.
  - If Part B (E_sym = E_anti) fails ==> AM-GM naive prediction wrong;
    F_d is likely not the right functional, pivot iter 2 to a DIFFERENT
    retained functional (W[J] = log|det H|, eigenvalue-product, or a
    mixed I_1 / I_2 construction).
  - If Part C (gradient) fails but E_sym != E_anti ==> interesting:
    the pinned point is not a critical point of the naive doublet AM-GM,
    but the gap reveals which framework direction is missing.
  - If Part D or E differ from the pinned point ==> tells us the direction
    to extend the attack.

In all cases, the gap reveals what iter 2 must attack.
""")
