#!/usr/bin/env python3
"""
PMNS selector iter 2: observable-principle W[J] = log|det H| with
scale-fixing constraint — is the pinned point a *constrained* critical
point on the retained affine chart?

Context. Iter 1 showed the naive doublet-block AM-GM functional
F_d(m, delta, q+) has large gradient (||grad|| = 7.78) at the pinned
point (m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042) — so the
physical point is NOT an *unconstrained* critical point of F_d. The
structural reason was the absence of a retained scale-fixing
constraint: without fixing Tr(K_d^2) = const, F_d diverges.

Iter 2 attack. The framework's retained "observable principle" is
W[J] = log|det(H_base + J)|. We test whether the pinned point is a
*constrained* critical point of W under each of four candidate
constraint surfaces, chosen because they are natural framework
scalars:

  g1(J) = ||J||_F^2                   (perturbation Frobenius norm)
  g2(J) = Tr(H^2)                     (total Frobenius of H, Ad-invariant)
  g3(J) = Tr(H)                        (trace of H, Ad-invariant)
  g4(J) = Tr(H^3)                      (cubic Casimir, Ad-invariant)

A point is a constrained critical point of W on the level set
{g = const} iff grad W is parallel to grad g at that point. Equivalently,
the component of grad W orthogonal to grad g vanishes.

What this runner tests.
  A. Sanity: W and its gradient at the pinned point are well-defined
     (chamber interior, det H > 0, etc).
  B. For each candidate constraint g_i (i = 1..4):
        - compute grad g_i at the pinned point
        - compute the parallel-component angle:
              cos(theta_i) = (grad W . grad g_i) / (|grad W| |grad g_i|)
        - compute the orthogonal-component magnitude:
              ||(grad W)_perp|| = |grad W|·sin(theta_i)
        - test whether cos(theta_i) = ±1 (i.e., parallel).
  C. For each constraint that passes (B), numerically search for the
     constrained critical point on the constraint surface (starting
     from random chamber points) and verify it coincides with the
     pinned point.

Honest outcome reporting. If any of g1..g4 produces ||grad W_perp|| < 1e-3
AND the constrained search converges to the pinned point, that
constraint IS the retained scale-fixing constraint and W[J] under it is
the retained selector — iter 2 closes the gate. If none does, report
the best-alignment constraint (the minimum ||grad W_perp||) and the
direction in which the pinned point fails to be constrained-critical,
which informs iter 3.
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
# Retained atlas constants (same as iter 1)
# ============================================================================

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

M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_PLUS_STAR = 0.715042


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def J(m: float, delta: float, q_plus: float) -> np.ndarray:
    return m * T_M + delta * T_DELTA + q_plus * T_Q


def W(m: float, delta: float, q_plus: float) -> float:
    """W[J] = log |det(H_base + J)|."""
    H_m = H(m, delta, q_plus)
    det_val = np.linalg.det(H_m).real
    if det_val <= 0:
        return float("-inf")
    return math.log(det_val)


def numerical_grad(
    fn, m: float, delta: float, q_plus: float, h: float = 1e-6
) -> np.ndarray:
    """Central-difference gradient."""
    g = np.zeros(3)
    for i, (dm, dd, dq) in enumerate(
        [(h, 0, 0), (0, h, 0), (0, 0, h)]
    ):
        f_plus = fn(m + dm, delta + dd, q_plus + dq)
        f_minus = fn(m - dm, delta - dd, q_plus - dq)
        g[i] = (f_plus - f_minus) / (2 * h)
    return g


# Candidate constraint functionals
def g1_frob(m, delta, q_plus):
    """||J||_F^2 = Tr(J^dag J)."""
    J_m = J(m, delta, q_plus)
    return np.trace(J_m.conj().T @ J_m).real


def g2_trH2(m, delta, q_plus):
    """Tr(H^2) for Hermitian H (= ||H||_F^2)."""
    H_m = H(m, delta, q_plus)
    return np.trace(H_m @ H_m).real


def g3_trH(m, delta, q_plus):
    """Tr(H)."""
    H_m = H(m, delta, q_plus)
    return np.trace(H_m).real


def g4_trH3(m, delta, q_plus):
    """Tr(H^3) — cubic Casimir."""
    H_m = H(m, delta, q_plus)
    return np.trace(H_m @ H_m @ H_m).real


CONSTRAINTS = {
    "g1 = ||J||_F^2": g1_frob,
    "g2 = Tr(H^2)": g2_trH2,
    "g3 = Tr(H)": g3_trH,
    "g4 = Tr(H^3)": g4_trH3,
}


# ============================================================================
# Part A: Sanity at the pinned point
# ============================================================================
print("=" * 72)
print("Part A: Sanity — W, grad W, grad g_i well-defined at pinned point")
print("=" * 72)

H_star = H(M_STAR, DELTA_STAR, Q_PLUS_STAR)
det_star = np.linalg.det(H_star).real

check(
    "A.1 det(H) > 0 at pinned point (baseline-connected chamber)",
    det_star > 0,
    f"det(H_*) = {det_star:.6f}",
)

W_star = W(M_STAR, DELTA_STAR, Q_PLUS_STAR)
print(f"\n  W[J] at pinned = log|det H_*| = {W_star:.6f}")

grad_W = numerical_grad(W, M_STAR, DELTA_STAR, Q_PLUS_STAR)
grad_W_norm = np.linalg.norm(grad_W)
print(f"  grad W at pinned = {grad_W}")
print(f"  ||grad W|| = {grad_W_norm:.6f}")

check(
    "A.2 grad W at pinned is finite (chamber-interior)",
    np.all(np.isfinite(grad_W)),
    f"grad W = {grad_W}",
)

# Record whether the unconstrained W is already critical (very unlikely)
check(
    "A.3 ||grad W|| == 0 (unconstrained critical, iter 2 would close trivially)",
    grad_W_norm < 1e-3,
    f"||grad W|| = {grad_W_norm:.6f}  (unconstrained critical test — expected FAIL)",
)


# ============================================================================
# Part B: Test each constraint g_i — is grad W parallel to grad g_i?
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Constrained critical-point test for each candidate g_i")
print("=" * 72)

best_constraint = None
best_perp_norm = float("inf")
results_B = {}

for name, g_fn in CONSTRAINTS.items():
    g_star = g_fn(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    grad_g = numerical_grad(g_fn, M_STAR, DELTA_STAR, Q_PLUS_STAR)
    grad_g_norm = np.linalg.norm(grad_g)
    if grad_g_norm < 1e-12:
        # Constraint gradient vanishes — can't use Lagrange
        print(f"\n  {name}: grad g = 0 at pinned, skipping")
        continue

    # Compute parallel component of grad W along grad g
    u_g = grad_g / grad_g_norm
    W_parallel = float(np.dot(grad_W, u_g))
    W_perp_vec = grad_W - W_parallel * u_g
    W_perp_norm = float(np.linalg.norm(W_perp_vec))

    # Angle between grad W and grad g
    if grad_W_norm > 0:
        cos_theta = W_parallel / grad_W_norm
    else:
        cos_theta = 0.0

    print(f"\n  {name}:")
    print(f"    g(*)               = {g_star:.6f}")
    print(f"    grad g(*)          = {grad_g}")
    print(f"    ||grad g||         = {grad_g_norm:.6f}")
    print(f"    cos(grad W, grad g)= {cos_theta:+.6f}")
    print(f"    ||(grad W)_perp||  = {W_perp_norm:.6f}")

    results_B[name] = {
        "grad_g": grad_g,
        "grad_g_norm": grad_g_norm,
        "cos_theta": cos_theta,
        "W_perp_norm": W_perp_norm,
        "g_star": g_star,
    }

    check(
        f"B.{name}: (grad W)_perp ~ 0 ⟺ pinned is constrained-critical under {name}",
        W_perp_norm < 1e-3,
        f"||(grad W)_perp|| = {W_perp_norm:.6f}",
    )

    if W_perp_norm < best_perp_norm:
        best_perp_norm = W_perp_norm
        best_constraint = name


# ============================================================================
# Part C: For the best-aligned constraint, search the constraint surface
# for constrained critical points and compare with pinned
# ============================================================================
print("\n" + "=" * 72)
print(f"Part C: Constrained search on best-aligned constraint = {best_constraint}")
print(f"         best ||(grad W)_perp|| = {best_perp_norm:.6f}")
print("=" * 72)

if best_constraint is None:
    print("  [WARN] No viable constraint identified")
else:
    best_g_fn = CONSTRAINTS[best_constraint]
    g_star_val = results_B[best_constraint]["g_star"]

    def neg_W_on_constraint(x):
        m, delta, q_plus = x
        # Chamber: q_+ >= sqrt(8/3) - delta
        chamber = q_plus - (math.sqrt(8.0 / 3.0) - delta)
        if chamber < 0:
            return 1e6 - chamber * 1e6
        # Constraint: g(J) = g_star
        g_val = best_g_fn(m, delta, q_plus)
        constraint_penalty = 100.0 * (g_val - g_star_val) ** 2
        # Maximize W (log|det H|), minimize its negative, plus penalty
        w_val = W(m, delta, q_plus)
        if not math.isfinite(w_val):
            return 1e6
        return -w_val + constraint_penalty

    best_constrained_W = -float("inf")
    best_constrained_xyz = None

    rng = np.random.default_rng(20260421)
    M_BOUND = (M_STAR - 2.0, M_STAR + 2.0)
    DELTA_BOUND = (DELTA_STAR - 1.5, DELTA_STAR + 1.5)
    Q_BOUND = (Q_PLUS_STAR - 1.0, Q_PLUS_STAR + 1.5)

    for _ in range(80):
        m0 = float(rng.uniform(*M_BOUND))
        d0 = float(rng.uniform(*DELTA_BOUND))
        q_min = math.sqrt(8.0 / 3.0) - d0 + 0.05
        q0 = float(rng.uniform(max(q_min, Q_BOUND[0]), Q_BOUND[1]))
        # Project starting point to the constraint surface roughly by scaling q.
        r = optimize.minimize(
            neg_W_on_constraint,
            x0=[m0, d0, q0],
            method="Nelder-Mead",
            options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000},
        )
        m_r, d_r, q_r = r.x
        if q_r >= math.sqrt(8.0 / 3.0) - d_r - 1e-6:
            g_check = best_g_fn(m_r, d_r, q_r)
            # Only keep runs that actually satisfy the constraint
            if abs(g_check - g_star_val) < 1e-4:
                w_val = W(m_r, d_r, q_r)
                if math.isfinite(w_val) and w_val > best_constrained_W:
                    best_constrained_W = w_val
                    best_constrained_xyz = r.x

    if best_constrained_xyz is None:
        print("  [WARN] constrained search did not find a valid optimum")
    else:
        m_opt, d_opt, q_opt = best_constrained_xyz
        print(f"\n  Constrained max of W under {best_constraint} = {g_star_val:.6f}:")
        print(f"    optimum (m, delta, q_+) = ({m_opt:.6f}, {d_opt:.6f}, {q_opt:.6f})")
        print(f"    W at optimum            = {best_constrained_W:.6f}")
        print(f"  Pinned point:")
        print(f"    (m_*, delta_*, q_+*)    = ({M_STAR:.6f}, {DELTA_STAR:.6f}, {Q_PLUS_STAR:.6f})")
        print(f"    W at pinned             = {W_star:.6f}")
        gap = np.linalg.norm(
            np.array([m_opt - M_STAR, d_opt - DELTA_STAR, q_opt - Q_PLUS_STAR])
        )
        check(
            f"C.1 constrained W maximum under {best_constraint} coincides with pinned",
            gap < 1e-3,
            f"||(optimum - pinned)|| = {gap:.6f}",
        )
        check(
            f"C.2 W at constrained optimum = W at pinned (same critical value)",
            abs(best_constrained_W - W_star) < 1e-4,
            f"|W_opt - W_*| = {abs(best_constrained_W - W_star):.6f}",
        )


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 2 attack: observable-principle W[J] = log|det H| constrained
critical-point test on the 2-real (m, delta, q_+) chart, under each of
four candidate constraints on H or J.

Best-aligned constraint: {best_constraint}
Best ||(grad W)_perp||  = {best_perp_norm:.6f}

Hypothesis under test:
  the physical pinned point is a CONSTRAINED critical point of
  W[J] under one of the retained Casimir constraints {{||J||_F^2,
  Tr(H^2), Tr(H), Tr(H^3)}}, forcing the PMNS angle triple.

Interpretation:
  - If Part B identifies any g_i with ||(grad W)_perp|| < 1e-3 AND
    Part C constrained search matches the pinned point: that constraint
    IS the retained scale-fixing axis, and W[J] under it is the
    retained selector — gate closes at iter 2.
  - If all g_i give ||(grad W)_perp|| >> 0: the scalar-Casimir
    constraint class is not the right one. Iter 3 should pivot to
    non-scalar constraints (e.g. Brannen-phase invariant, Dedekind-sum
    constraint, or retained cyclic-bundle invariant).
  - The specific direction of (grad W)_perp at pinned tells us which
    direction is NOT accounted for by any scalar Casimir — informing
    where iter 3 must look.
""")
