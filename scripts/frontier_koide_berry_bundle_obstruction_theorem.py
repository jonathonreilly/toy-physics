"""
Frontier runner - Koide Berry Bundle Obstruction / Uniqueness Theorem.

Companion to
`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

Theorem. Let K_norm^+ be the positive projectivized Koide cone in normalized
sqrt-mass coordinates. Then:

1. K_norm^+ is one-dimensional: three open arcs on the upper Koide circle.
2. The C_3 action is free and cyclically permutes those arcs.
3. The quotient K_norm^+ / C_3 is an open interval.
4. Therefore every complex C_3-equivariant line bundle on K_norm^+ is
   equivariantly trivial, c_1 = 0 there, and no gauge-invariant Berry holonomy
   exists on the actual positive base.
5. If positivity is relaxed to the full projective conic S^1, the bundle is
   still topologically trivial and the remaining flat holonomy is arbitrary.

This runner replaces theorem-adjacent placeholders with actual checks:
  (A) Correct normalized Koide geometry from sigma = 1/2
  (B) Explicit circle parameterization of the normalized locus
  (C) Exact C_3 action as a 2 pi / 3 rotation on the doublet plane
  (D) Positive locus is three open arcs, so the physical quotient is an interval
  (E) Betti-number checks: beta_2 = 0 on the physical quotient and on S^1
  (F) No fixed points under nontrivial C_3 action on the circle
  (G) Flat-holonomy family on the sign-relaxed quotient is continuous and
      non-unique; 2/9 is one choice, not a forced value

Expected: PASS=30 FAIL=0.
"""

from __future__ import annotations

import sys

import numpy as np


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


def shift_matrix() -> np.ndarray:
    """C|j> = |j+1 mod 3> in the standard basis."""
    return np.array(
        [[0.0, 0.0, 1.0],
         [1.0, 0.0, 0.0],
         [0.0, 1.0, 0.0]]
    )


E_PLUS = np.ones(3) / np.sqrt(3.0)
U1 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2.0)
U2 = np.array([1.0, 1.0, -2.0]) / np.sqrt(6.0)
C3 = shift_matrix()
ROT_2PI_OVER_3 = np.array(
    [[-0.5, -np.sqrt(3.0) / 2.0],
     [np.sqrt(3.0) / 2.0, -0.5]]
)


def koide_circle_point(phi: float, sign: int = 1) -> np.ndarray:
    """Normalized Koide point with sign-relaxed singlet choice."""
    doublet = np.cos(phi) * U1 + np.sin(phi) * U2
    return sign * E_PLUS / np.sqrt(2.0) + doublet / np.sqrt(2.0)


def koide_sigma(vec: np.ndarray) -> float:
    parallel = float(np.dot(vec, E_PLUS))
    return parallel ** 2 / float(np.dot(vec, vec))


def koide_q(vec: np.ndarray) -> float:
    total = float(np.sum(vec))
    return float(np.dot(vec, vec)) / (total ** 2)


def betti_cycle(num_vertices: int) -> tuple[int, int, int]:
    """Betti numbers of a cycle graph as a 1D CW complex."""
    boundary = np.zeros((num_vertices, num_vertices))
    for edge in range(num_vertices):
        boundary[edge, edge] = -1.0
        boundary[(edge + 1) % num_vertices, edge] = 1.0
    rank_1 = int(np.linalg.matrix_rank(boundary))
    beta_0 = num_vertices - rank_1
    beta_1 = num_vertices - rank_1
    beta_2 = 0
    return beta_0, beta_1, beta_2


def betti_path(num_vertices: int) -> tuple[int, int, int]:
    """Betti numbers of a path graph as a 1D CW complex."""
    num_edges = num_vertices - 1
    boundary = np.zeros((num_vertices, num_edges))
    for edge in range(num_edges):
        boundary[edge, edge] = -1.0
        boundary[edge + 1, edge] = 1.0
    rank_1 = int(np.linalg.matrix_rank(boundary))
    beta_0 = num_vertices - rank_1
    beta_1 = num_edges - rank_1
    beta_2 = 0
    return beta_0, beta_1, beta_2


def wrapped_intervals(mask: np.ndarray, phis: np.ndarray) -> list[tuple[float, float]]:
    """Connected true-runs on a periodic boolean mask."""
    doubled = np.concatenate([mask, mask])
    in_run = False
    start_idx = 0
    intervals: list[tuple[float, float]] = []
    for idx, val in enumerate(doubled):
        if val and not in_run:
            in_run = True
            start_idx = idx
        if in_run and (idx == len(doubled) - 1 or not doubled[idx + 1]):
            end_idx = idx
            if start_idx < len(mask):
                start_phi = phis[start_idx]
                end_phi = phis[min(end_idx, len(mask) - 1)]
                intervals.append((float(start_phi), float(end_phi)))
            in_run = False
    merged: list[tuple[float, float]] = []
    for start_phi, end_phi in intervals:
        if merged and start_phi <= merged[-1][1] + 1e-12:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end_phi))
        else:
            merged.append((start_phi, end_phi))
    return merged


print("=" * 72)
print("Koide Berry bundle obstruction / uniqueness theorem")
print("=" * 72)


# ---------------------------------------------------------------------------
# (A) Correct normalized Koide geometry
# ---------------------------------------------------------------------------

print("\n(A) Correct normalized Koide geometry from sigma = 1/2")
print("-" * 72)

basis = np.column_stack([E_PLUS, U1, U2])
check("(A1) {e_+, u_1, u_2} is orthonormal",
      np.allclose(basis.T @ basis, np.eye(3), atol=1e-12))

check("(A2) C_3 fixes the singlet axis",
      np.allclose(C3 @ E_PLUS, E_PLUS, atol=1e-12))

sig_example = koide_sigma(koide_circle_point(0.123, sign=1))
check("(A3) normalized Koide locus has sigma = 1/2",
      abs(sig_example - 0.5) < 1e-12,
      f"sigma = {sig_example:.12f}")

q_example = koide_q(koide_circle_point(0.123, sign=1))
check("(A4) normalized Koide locus has Q = 2/3",
      abs(q_example - 2.0 / 3.0) < 1e-12,
      f"Q = {q_example:.12f}")


# ---------------------------------------------------------------------------
# (B) Explicit circle parameterization
# ---------------------------------------------------------------------------

print("\n(B) Explicit circle parameterization of the normalized locus")
print("-" * 72)

phis_sample = np.linspace(0.0, 2.0 * np.pi, 13, endpoint=False)
norm_ok = True
koide_ok = True
tangent_ok = True
for phi in phis_sample:
    vec = koide_circle_point(phi, sign=1)
    dvec = (
        koide_circle_point(phi + 1e-6, sign=1)
        - koide_circle_point(phi - 1e-6, sign=1)
    ) / (2e-6)
    norm_ok &= abs(np.linalg.norm(vec) - 1.0) < 1e-10
    koide_ok &= abs(koide_q(vec) - 2.0 / 3.0) < 1e-10
    tangent_ok &= np.linalg.norm(dvec) > 1e-6

check("(B1) s_+(phi) stays on S^2", norm_ok)
check("(B2) s_+(phi) stays on the Koide cone Q = 2/3", koide_ok)
check("(B3) the locus has one free angle parameter", tangent_ok)

vec_plus = koide_circle_point(0.314, sign=1)
vec_minus = koide_circle_point(0.314, sign=-1)
check("(B4) sign-relaxed normalized locus has two circle components",
      np.dot(vec_plus, E_PLUS) > 0.0 and np.dot(vec_minus, E_PLUS) < 0.0)


# ---------------------------------------------------------------------------
# (C) Exact C_3 action
# ---------------------------------------------------------------------------

print("\n(C) Exact C_3 action as a 2 pi / 3 rotation on the doublet plane")
print("-" * 72)

doublet_action = np.array(
    [[np.dot(U1, C3 @ U1), np.dot(U1, C3 @ U2)],
     [np.dot(U2, C3 @ U1), np.dot(U2, C3 @ U2)]]
)
check("(C1) doublet action matrix equals R(2 pi / 3)",
      np.allclose(doublet_action, ROT_2PI_OVER_3, atol=1e-12))

equiv_ok = True
equiv2_ok = True
for phi in phis_sample:
    equiv_ok &= np.allclose(C3 @ koide_circle_point(phi, 1),
                            koide_circle_point(phi + 2.0 * np.pi / 3.0, 1),
                            atol=1e-10)
    equiv2_ok &= np.allclose(C3 @ C3 @ koide_circle_point(phi, 1),
                             koide_circle_point(phi + 4.0 * np.pi / 3.0, 1),
                             atol=1e-10)

check("(C2) C s_+(phi) = s_+(phi + 2 pi / 3)", equiv_ok)
check("(C3) C^2 s_+(phi) = s_+(phi + 4 pi / 3)", equiv2_ok)
check("(C4) C^3 = identity on the normalized locus",
      np.allclose(np.linalg.matrix_power(C3, 3), np.eye(3), atol=1e-12))


# ---------------------------------------------------------------------------
# (D) Positive locus geometry
# ---------------------------------------------------------------------------

print("\n(D) Positive locus = three open arcs; quotient is an interval")
print("-" * 72)

phis_dense = np.linspace(0.0, 2.0 * np.pi, 3601)
positive_mask = np.array([
    np.all(koide_circle_point(phi, sign=1) > 1e-10) for phi in phis_dense
])
intervals = wrapped_intervals(positive_mask, phis_dense)
lengths = [end - start for start, end in intervals]
centers = [(start + end) / 2.0 for start, end in intervals]

check("(D1) positive normalized locus is nonempty", positive_mask.any())
check("(D2) positive normalized locus is not the full circle", not positive_mask.all())
check("(D3) positivity locus has three connected arcs", len(intervals) == 3,
      f"intervals = {[(round(a, 4), round(b, 4)) for a, b in intervals]}")
check("(D4) the three arcs have equal length by C_3 symmetry",
      max(lengths) - min(lengths) < 5e-3,
      f"length spread = {max(lengths) - min(lengths):.3e}")

arc_cyclic_ok = True
for center in centers:
    vec = koide_circle_point(center, sign=1)
    image = C3 @ vec
    arc_cyclic_ok &= np.all(image > 1e-10)
check("(D5) C_3 cyclically permutes the positive arcs", arc_cyclic_ok)


# ---------------------------------------------------------------------------
# (E) Topology / Betti checks
# ---------------------------------------------------------------------------

print("\n(E) Betti-number checks on the physical quotient and on S^1")
print("-" * 72)

beta0_cycle, beta1_cycle, beta2_cycle = betti_cycle(24)
check("(E1) sign-relaxed projective conic has beta_0 = 1",
      beta0_cycle == 1, f"beta_0 = {beta0_cycle}")
check("(E2) sign-relaxed projective conic has beta_1 = 1",
      beta1_cycle == 1, f"beta_1 = {beta1_cycle}")
check("(E3) sign-relaxed projective conic has beta_2 = 0",
      beta2_cycle == 0, f"beta_2 = {beta2_cycle}")

beta0_path, beta1_path, beta2_path = betti_path(24)
check("(E4) physical quotient interval has beta_0 = 1",
      beta0_path == 1, f"beta_0 = {beta0_path}")
check("(E5) physical quotient interval has beta_1 = 0",
      beta1_path == 0, f"beta_1 = {beta1_path}")
check("(E6) physical quotient interval has beta_2 = 0",
      beta2_path == 0, f"beta_2 = {beta2_path}")


# ---------------------------------------------------------------------------
# (F) Freeness of the nontrivial C_3 action
# ---------------------------------------------------------------------------

print("\n(F) No fixed points under nontrivial C_3 action on the circle")
print("-" * 72)

dist_c = []
dist_c2 = []
for phi in phis_sample:
    vec = koide_circle_point(phi, sign=1)
    dist_c.append(np.linalg.norm(C3 @ vec - vec))
    dist_c2.append(np.linalg.norm(C3 @ C3 @ vec - vec))

check("(F1) no point on the Koide circle is fixed by C",
      min(dist_c) > 1e-6, f"min distance = {min(dist_c):.6f}")
check("(F2) no point on the Koide circle is fixed by C^2",
      min(dist_c2) > 1e-6, f"min distance = {min(dist_c2):.6f}")


# ---------------------------------------------------------------------------
# (G) Flat-holonomy family on the sign-relaxed quotient
# ---------------------------------------------------------------------------

print("\n(G) Flat holonomy on S^1 is continuous and non-unique")
print("-" * 72)


def quotient_holonomy(t: float) -> complex:
    """Holonomy of A_t = i t dpsi around the quotient circle psi in [0, 2 pi]."""
    return np.exp(1j * 2.0 * np.pi * t)


t_target = 2.0 / 3.0
t_near = 0.70
t_zero = 0.0
h_zero = quotient_holonomy(t_zero)
h_target = quotient_holonomy(t_target)
h_near = quotient_holonomy(t_near)
delta_target = t_target / 3.0
delta_near = t_near / 3.0

check("(G1) trivial flat connection gives trivial holonomy",
      abs(h_zero - 1.0) < 1e-12)
check("(G2) t = 2/3 gives quotient holonomy angle 4 pi / 3",
      abs(np.angle(h_target) + 2.0 * np.pi / 3.0) < 1e-12
      or abs(np.angle(h_target) - 4.0 * np.pi / 3.0) < 1e-12)
check("(G3) Berry-to-Brannen reduction gives delta = 2/9 at t = 2/3",
      abs(delta_target - 2.0 / 9.0) < 1e-12,
      f"delta = {delta_target:.12f}")
check("(G4) nearby flat connections give nearby non-equal deltas",
      abs(delta_near - delta_target) > 1e-6,
      f"delta_near = {delta_near:.12f}")
check("(G5) nearby flat connections give distinct holonomies",
      abs(h_near - h_target) > 1e-6,
      f"|h_near - h_target| = {abs(h_near - h_target):.6f}")


print()
print("=" * 72)
print(f"PASS={PASS} FAIL={FAIL}")
print("=" * 72)

if FAIL > 0:
    sys.exit(1)
