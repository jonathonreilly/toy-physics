#!/usr/bin/env python3
"""
PMNS selector iter 3: Brannen-phase gate — cross-sector I2/P -> I5 attack.

Context. The framework has a retained I2/P invariant delta_Brannen = 2/9
(APS eta-invariant on Z_3 orbifold with tangent weights (1, 2)), exactly
landed on morning-4-21 as a retained-forced theorem.

Iters 1-2 ruled out direct variational/Lagrangian selectors (naive AM-GM
on doublet block; W[J] = log|det H| under any single scalar Casimir).

Iter 3 attack: a CROSS-SECTOR gate. Test whether any natural "intrinsic
phase" of H(m, delta, q_+) on the chamber evaluates to 2/9 (in radians,
or as a fraction of 2*pi, or 4*pi/9 = 2*pi*(2/9), or similar framework-
natural interpretation) at the pinned point (m_*, delta_*, q_+*) =
(0.657061, 0.933806, 0.715042), AND does so on a sub-manifold that cuts
the 2-real (delta, q_+) family to lower dimension.

Candidate phase invariants tested:

  P1. arg(K_12)           — phase of the moving doublet off-diagonal
  P2. arg(det H)          — phase of overall determinant (real for H
                            Hermitian, so ± pi; informational)
  P3. arg(K_12 / a_*)      — K_12 rescaled by the frozen a_* slot
  P4. arg(K_12 / b_*)      — K_12 rescaled by the frozen b_* slot
  P5. arg(Pfaffian)       — 2x2 Pfaffian-like combination of doublet block
  P6. arg(U_PMNS[0,2])    — phase of U_e3 (Dirac CP phase ingredient)
  P7. arg(Jarlskog)       — phase of the PMNS invariant J
  P8. (1/(2 pi)) * Sum_k arg(K_0k * conj(K_0k_base))   — Z_3 Berry loop
  P9. arg(Tr(H T_Delta))  — overlap of H with the CP-odd direction
  P10. arg(Tr(H^2 T_Delta)) — same, quadratic

For each phase P_i, compute the value at the pinned point and compare
to the retained I2/P values 2/9 (rad), 4 pi/9, 2 pi/9, pi/9, and related
simple multiples modulo 2 pi.

If any P_i matches a retained-I2/P-value at the pinned point, we then:
  (a) Check whether the level set {P_i = value} intersects the pinned
      point (trivially it does since we matched there).
  (b) Check whether the level set is 1-dim (not the full 2-real chart)
      — i.e., it genuinely cuts the chamber.
  (c) Start narrowing: is the retained value forced by some framework
      identity, not just coincidence?

Honest outcome. If any P_i matches to within 1e-4 at the pinned point,
report it as a CANDIDATE linkage and flag for iter 4 to verify retention.
Otherwise, report the closest match and rule out the Brannen-phase-gate
class for iter 4.
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


# ============================================================================
# Retained atlas constants
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

M_STAR = 0.657061
DELTA_STAR = 0.933806
Q_PLUS_STAR = 0.715042

# Frozen slots (constants from chamber-blindness theorem)
A_STAR = 0.16993211 + 1.19280904j
B_STAR = 0.45860725 - 0.69280904j

# Retained I2/P value
DELTA_BRANNEN = 2.0 / 9.0   # radians
RETAINED_CANDIDATES = {
    "2/9 rad":            DELTA_BRANNEN,
    "-2/9 rad":           -DELTA_BRANNEN,
    "2*pi/9":             2 * math.pi / 9,
    "-2*pi/9":            -2 * math.pi / 9,
    "4*pi/9":             4 * math.pi / 9,   # = 2*pi * (2/9)
    "-4*pi/9":            -4 * math.pi / 9,
    "pi/9":               math.pi / 9,
    "-pi/9":              -math.pi / 9,
    "pi - 2/9 rad":       math.pi - DELTA_BRANNEN,
    "-(pi - 2/9 rad)":    -(math.pi - DELTA_BRANNEN),
    "2/9 * 2*pi":         2.0 / 9.0 * 2 * math.pi,  # = 4*pi/9
    "pi/3 - 2/9 rad":     math.pi / 3 - DELTA_BRANNEN,
}


def H(m: float, delta: float, q_plus: float) -> np.ndarray:
    return H_BASE + m * T_M + delta * T_DELTA + q_plus * T_Q


def K_z3(m: float, delta: float, q_plus: float) -> np.ndarray:
    H_m = H(m, delta, q_plus)
    return U_Z3.conj().T @ H_m @ U_Z3


def pmns_U(H_m: np.ndarray) -> np.ndarray:
    """PMNS-like unitary: eigenvectors of H sorted by descending eigenvalue,
    matched to sigma_hier = (2, 1, 0) = (electron, muon, tau) <-> (high, mid, low).
    """
    w, V = np.linalg.eigh(H_m)
    # eigh returns ascending; reverse to descending
    order = np.argsort(-w)
    return V[:, order]


def jarlskog(U: np.ndarray) -> complex:
    """PMNS Jarlskog invariant J = Im(U_e1 U_e2* U_mu1* U_mu2)."""
    return U[0, 0] * np.conj(U[0, 1]) * np.conj(U[1, 0]) * U[1, 1]


def phase_invariants(m: float, delta: float, q_plus: float) -> dict:
    H_m = H(m, delta, q_plus)
    K = K_z3(m, delta, q_plus)
    U = pmns_U(H_m)
    J = jarlskog(U)

    # Pfaffian-like: for a 2x2 block [[a, b], [b^*, c]] real-Hermitian,
    # a natural "phase" is arg(b) (the only complex degree of freedom).
    K_12 = K[1, 2]
    detH = np.linalg.det(H_m)

    phases = {
        "P1 arg(K_12)": cmath.phase(K_12) if K_12 != 0 else float("nan"),
        "P2 arg(det H)": cmath.phase(detH) if detH != 0 else float("nan"),
        "P3 arg(K_12 / a_*)": cmath.phase(K_12 / A_STAR),
        "P4 arg(K_12 / b_*)": cmath.phase(K_12 / B_STAR),
        "P5 arg(Pfaffian_doublet)": cmath.phase(K_12) if K_12 != 0 else float("nan"),
        "P6 arg(U_e3)": cmath.phase(U[0, 2]) if U[0, 2] != 0 else float("nan"),
        "P7 arg(Jarlskog)": cmath.phase(J) if J != 0 else float("nan"),
        "P8 arg(K_00 * conj(sum a, b))": cmath.phase(
            K[0, 0] * np.conj(A_STAR + B_STAR)
        ),
        "P9 arg(Tr(H T_Delta))": cmath.phase(
            np.trace(H_m @ T_DELTA)
        ),
        "P10 arg(Tr(H^2 T_Delta))": cmath.phase(
            np.trace(H_m @ H_m @ T_DELTA)
        ),
        "P11 arg(K[0,1] / K[1,2])": cmath.phase(
            K[0, 1] / K[1, 2]
        ) if K[1, 2] != 0 else float("nan"),
        "P12 arg(K[0,2] / K[1,2])": cmath.phase(
            K[0, 2] / K[1, 2]
        ) if K[1, 2] != 0 else float("nan"),
    }
    return phases


def best_match(phase_val: float, candidates: dict) -> tuple[str, float, float]:
    """For a numerical phase_val, find the best matching retained candidate
    (accounting for mod 2 pi). Return (name, target, |deviation|)."""
    best_name = None
    best_target = None
    best_dev = float("inf")
    for name, target in candidates.items():
        # Compare modulo 2 pi (wrap into [-pi, pi])
        diff = (phase_val - target + math.pi) % (2 * math.pi) - math.pi
        if abs(diff) < best_dev:
            best_dev = abs(diff)
            best_name = name
            best_target = target
    return best_name, best_target, best_dev


# ============================================================================
# Part A: Compute all phases at the pinned point
# ============================================================================
print("=" * 72)
print("Part A: Phases at pinned point")
print("=" * 72)

phases_star = phase_invariants(M_STAR, DELTA_STAR, Q_PLUS_STAR)

print(f"\n  At (m_*, delta_*, q_+*) = ({M_STAR}, {DELTA_STAR}, {Q_PLUS_STAR}):\n")
print(f"  {'Invariant':40s} {'value (rad)':>14s}  {'value (deg)':>14s}")
for name, val in phases_star.items():
    if math.isnan(val):
        print(f"  {name:40s} {'nan':>14s}  {'nan':>14s}")
    else:
        print(f"  {name:40s} {val:+.6f}  {math.degrees(val):+.4f}")

# Retained candidate table
print(f"\n  Retained-I2/P candidate values to match against:\n")
for name, val in RETAINED_CANDIDATES.items():
    print(f"    {name:22s} = {val:+.6f} rad  = {math.degrees(val):+.4f} deg")


# ============================================================================
# Part B: Best match per phase invariant
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Closest retained-I2/P match for each phase invariant")
print("=" * 72)

matches = []
print(f"\n  {'Invariant':40s} {'value':>10s}  {'closest retained':>22s}  {'|dev|':>10s}")
for name, val in phases_star.items():
    if math.isnan(val):
        continue
    match_name, match_target, dev = best_match(val, RETAINED_CANDIDATES)
    print(
        f"  {name:40s} {val:+.4f}  {match_name:>22s}  {dev:>10.6f}"
    )
    matches.append((name, val, match_name, match_target, dev))

matches.sort(key=lambda x: x[4])
print(f"\n  Top 3 closest matches:")
for name, val, match_name, match_target, dev in matches[:3]:
    print(
        f"    {name} ({val:+.4f}) vs {match_name} ({match_target:+.4f}): |dev| = {dev:.6f}"
    )


# ============================================================================
# Part C: Check best match — is it at or below tolerance (< 1e-4)?
# ============================================================================
print("\n" + "=" * 72)
print("Part C: Did any phase invariant hit a retained-I2/P value exactly?")
print("=" * 72)

best_overall = matches[0]
print(f"\n  Best overall match: {best_overall[0]} = {best_overall[1]:+.6f}")
print(f"                       vs {best_overall[2]} = {best_overall[3]:+.6f}")
print(f"                       |deviation| = {best_overall[4]:.6f}")

check(
    f"C.1 Best match has |dev| < 1e-4 (exact retained-I2/P linkage)",
    best_overall[4] < 1e-4,
    f"|dev| = {best_overall[4]:.6f}",
)
check(
    f"C.2 Best match has |dev| < 1e-2 (strong hint)",
    best_overall[4] < 1e-2,
    f"|dev| = {best_overall[4]:.6f}",
)
check(
    f"C.3 Best match has |dev| < 1e-1 (weak hint)",
    best_overall[4] < 1e-1,
    f"|dev| = {best_overall[4]:.6f}",
)


# ============================================================================
# Part D: For each phase invariant, scan the level set and check whether
#          it passes through the pinned point (it trivially does) AND
#          whether the level set is dimension-reducing.
# ============================================================================
print("\n" + "=" * 72)
print("Part D: Level-set dimensionality test for top-3 phase candidates")
print("=" * 72)

rng = np.random.default_rng(20260421)


def phase_at(name, m, delta, q_plus):
    phs = phase_invariants(m, delta, q_plus)
    return phs[name]


for name, val_star, match_name, match_target, dev in matches[:3]:
    print(f"\n  {name} (target value: {val_star:+.6f}):")
    # How does phase vary in a random chamber neighborhood?
    phase_samples = []
    n_samples = 200
    for _ in range(n_samples):
        m_r = M_STAR + float(rng.uniform(-0.5, 0.5))
        d_r = DELTA_STAR + float(rng.uniform(-0.5, 0.5))
        q_min = math.sqrt(8.0 / 3.0) - d_r + 0.05
        q_r = max(q_min, Q_PLUS_STAR + float(rng.uniform(-0.5, 0.5)))
        try:
            p_here = phase_at(name, m_r, d_r, q_r)
            if not math.isnan(p_here):
                phase_samples.append(p_here)
        except (ValueError, ZeroDivisionError):
            continue

    if phase_samples:
        phase_arr = np.array(phase_samples)
        # Wrap into [-pi, pi] for std
        phase_arr_wrapped = np.array([
            ((p - val_star + math.pi) % (2 * math.pi)) - math.pi + val_star
            for p in phase_arr
        ])
        std = np.std(phase_arr_wrapped)
        print(
            f"    Neighborhood std of phase: {std:.4f}  (pinned value: {val_star:+.6f})"
        )
        # If std is small, the phase is nearly constant across the chamber
        # neighborhood — level set is essentially the full chamber, not
        # dimension-reducing.
        check(
            f"D.{name} — phase varies across neighborhood (level set is 1-dim cut)",
            std > 0.01,
            f"std = {std:.4f}",
        )


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 3 attack: Brannen-phase gate (cross-sector I2/P -> I5).

Hypothesis: some natural phase invariant of H(m, delta, q_+) evaluates
to a retained I2/P value (2/9 rad and related simple expressions) at
the physical pinned point, and the level set cuts the 2-real manifold
to lower dimension.

Best match found: {best_overall[0]} = {best_overall[1]:+.6f}
  vs retained {best_overall[2]} = {best_overall[3]:+.6f}
  |deviation| = {best_overall[4]:.6f}

Interpretation:
  - If best |dev| < 1e-4: confirmed Brannen-phase linkage. Iter 4
    should pursue this as a retained derivation route.
  - If 1e-4 <= |dev| < 1e-2: strong hint but not exact; iter 4 should
    check whether the deviation is systematic (numerical noise vs
    genuine mismatch).
  - If |dev| > 1e-2: Brannen-phase-gate class is ruled out at this
    accuracy; pivot iter 4 to other candidates in the backlog
    (operator-commutation, A-BCC derivation, or cyclic-bundle W[J]).

The level-set dimensionality test tells us whether the phase invariant
genuinely cuts the chamber (needed for any useful sub-manifold) or
whether it's chamber-blind (locked to the frozen Z_3 structure).
""")
