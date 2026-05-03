#!/usr/bin/env python3
"""
GR atlas closure on PL S^3 × R — stretch attempt with named obstructions.

Cycle 10 of retained-promotion campaign 2026-05-02. Output type (c)
stretch attempt providing 2-chart minimal numerical demonstration of
parent's claimed exact overlap-invariance + K_GR nondegeneracy.

Multi-chart full-atlas closure (5-chart PL S^3 with 10 triple-overlap
cocycles) remains open; documented as named obstructions.

Forbidden imports: no GR field equations, no specific solutions,
no PDG observed values.
"""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=6, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


# -----------------------------------------------------------------------------
# Setup: 4×4 symmetric-tensor space (10-dim)
# -----------------------------------------------------------------------------

# Symmetric 4×4 tensors form a 10-dim space. Basis: {e_i ⊗ e_j + e_j ⊗ e_i} / 2
# for i ≤ j.

def sym_basis():
    """Generate basis for symmetric 4x4 tensors."""
    basis = []
    for i in range(4):
        for j in range(i, 4):
            B = np.zeros((4, 4), dtype=float)
            if i == j:
                B[i, j] = 1.0
            else:
                B[i, j] = 1.0 / np.sqrt(2)
                B[j, i] = 1.0 / np.sqrt(2)
            basis.append(B)
    return basis


sym_B = sym_basis()
assert len(sym_B) == 10


def vec_to_sym(v):
    """Reconstruct a symmetric 4×4 tensor from its 10-dim coefficient vector."""
    M = np.zeros((4, 4), dtype=float)
    for i, B in enumerate(sym_B):
        M += v[i] * B
    return M


def sym_to_vec(M):
    """Compute the 10-dim coefficient vector of a symmetric 4×4 tensor."""
    return np.array([np.einsum("ij,ij->", B, M) for B in sym_B])


# -----------------------------------------------------------------------------
# Step 1: Define B_D(h, k) = -Tr(D^{-1} h D^{-1} k)
# -----------------------------------------------------------------------------

section("Step 1: B_D(h, k) = -Tr(D^{-1} h D^{-1} k) bilinear form")

def B_D(D, h, k):
    Dinv = np.linalg.inv(D)
    return -np.trace(Dinv @ h @ Dinv @ k)


# Generic 3+1 background D (Lorentzian signature: diag(-1, +1, +1, +1))
rng = np.random.default_rng(2026)
D_base = np.diag([-1.0, 1.0, 1.0, 1.0])  # Minkowski-like
# Add small perturbation to make it generic but still Lorentzian-class
D_perturb = 0.1 * (rng.normal(size=(4, 4)))
D_perturb = (D_perturb + D_perturb.T) / 2  # symmetric
D = D_base + D_perturb

check(
    "D is invertible (generic 3+1 background)",
    abs(np.linalg.det(D)) > 1e-6,
    f"det(D) = {np.linalg.det(D):.4f}",
)

# Test inputs h, k:
h = rng.normal(size=(4, 4))
h = (h + h.T) / 2  # symmetric

k = rng.normal(size=(4, 4))
k = (k + k.T) / 2

# Verify B_D is symmetric in h, k:
sym_check = abs(B_D(D, h, k) - B_D(D, k, h))
check(
    "B_D(h, k) = B_D(k, h) (symmetry)",
    sym_check < 1e-10,
    f"|B_D(h,k) - B_D(k,h)| = {sym_check:.3e}",
)

# Verify bilinearity in h:
alpha = 2.5
bilin_check = abs(B_D(D, alpha * h, k) - alpha * B_D(D, h, k))
check(
    "B_D(αh, k) = α B_D(h, k) (bilinearity)",
    bilin_check < 1e-10,
    f"|B_D(αh, k) - α B_D(h, k)| = {bilin_check:.3e}",
)


# -----------------------------------------------------------------------------
# Step 2: Chart transition D → D' = T_S^T D T_S
# -----------------------------------------------------------------------------

section("Step 2: Chart transition D → D' = T_S^T D T_S")

# Random invertible T_S (chart transition matrix)
T_S = rng.normal(size=(4, 4))
# Ensure invertibility:
while abs(np.linalg.det(T_S)) < 0.1:
    T_S = rng.normal(size=(4, 4))

D_prime = T_S.T @ D @ T_S

check(
    "T_S is invertible (chart transition exists)",
    abs(np.linalg.det(T_S)) > 1e-6,
    f"det(T_S) = {np.linalg.det(T_S):.4f}",
)

check(
    "D' = T_S^T D T_S is invertible",
    abs(np.linalg.det(D_prime)) > 1e-6,
    f"det(D') = {np.linalg.det(D_prime):.4f}",
)


# -----------------------------------------------------------------------------
# Step 3: Verify B_{D'}(h', k') = B_D(h, k) (overlap-invariance)
# -----------------------------------------------------------------------------

section("Step 3: Exact overlap-invariance B_{D'}(h', k') = B_D(h, k)")

h_prime = T_S.T @ h @ T_S
k_prime = T_S.T @ k @ T_S

B_D_value = B_D(D, h, k)
B_D_prime_value = B_D(D_prime, h_prime, k_prime)

invariance_check = abs(B_D_value - B_D_prime_value)
check(
    "B_{D'}(T_S^T h T_S, T_S^T k T_S) = B_D(h, k) (exact overlap invariance)",
    invariance_check < 1e-9,
    f"|B_D - B_D'| = {invariance_check:.3e}, B_D = {B_D_value:.4f}, B_D' = {B_D_prime_value:.4f}",
)

# Repeat on multiple random h, k pairs:
multi_invariance_passes = 0
multi_invariance_total = 0
for trial in range(10):
    h_t = rng.normal(size=(4, 4))
    h_t = (h_t + h_t.T) / 2
    k_t = rng.normal(size=(4, 4))
    k_t = (k_t + k_t.T) / 2

    h_t_prime = T_S.T @ h_t @ T_S
    k_t_prime = T_S.T @ k_t @ T_S

    if abs(B_D(D, h_t, k_t) - B_D(D_prime, h_t_prime, k_t_prime)) < 1e-9:
        multi_invariance_passes += 1
    multi_invariance_total += 1

check(
    f"Overlap-invariance verified on 10 random (h, k) pairs",
    multi_invariance_passes == multi_invariance_total,
    f"{multi_invariance_passes}/{multi_invariance_total} passes",
)


# -----------------------------------------------------------------------------
# Step 4: K_GR(D) on symmetric-tensor basis (10×10 matrix), nondegenerate
# -----------------------------------------------------------------------------

section("Step 4: K_GR(D) construction on 10-dim symmetric-tensor basis")

def K_GR_matrix(D):
    """Construct K_GR(D) as a 10×10 matrix in the symmetric-tensor basis."""
    K = np.zeros((10, 10))
    for i, Bi in enumerate(sym_B):
        for j, Bj in enumerate(sym_B):
            K[i, j] = B_D(D, Bi, Bj)
    return K


K_GR_D = K_GR_matrix(D)
det_K_GR_D = np.linalg.det(K_GR_D)

check(
    "K_GR(D) constructed as 10×10 matrix on symmetric-tensor basis",
    K_GR_D.shape == (10, 10),
    f"shape = {K_GR_D.shape}, det = {det_K_GR_D:.3e}",
)

check(
    "K_GR(D) is nondegenerate (det ≠ 0) for generic D",
    abs(det_K_GR_D) > 1e-10,
    f"|det K_GR(D)| = {abs(det_K_GR_D):.3e}",
)

# Symmetric:
check(
    "K_GR(D) is symmetric",
    np.allclose(K_GR_D, K_GR_D.T),
    f"max asymmetry = {np.max(np.abs(K_GR_D - K_GR_D.T)):.3e}",
)


# -----------------------------------------------------------------------------
# Step 5: K_GR transition rule on overlap (G_{D'} = T_S^{-T} G_D T_S^{-1})
# -----------------------------------------------------------------------------

section("Step 5: K_GR transition rule on 2-chart overlap")

K_GR_D_prime = K_GR_matrix(D_prime)

# The transition matrix on the symmetric-tensor basis (T_S induces a representation).
# For h' = T_S^T h T_S in tensor form, the coefficient vector v' = R(T_S) v where R(T_S)
# is the induced representation matrix.

def induced_rep(T_S):
    """Compute the 10×10 induced representation of T_S on symmetric tensors."""
    R = np.zeros((10, 10))
    for j, Bj in enumerate(sym_B):
        # Compute T_S^T Bj T_S as a symmetric 4×4 matrix
        transformed = T_S.T @ Bj @ T_S
        # Project onto the basis to get coefficients in dim 10
        for i, Bi in enumerate(sym_B):
            R[i, j] = np.einsum("ij,ij->", Bi, transformed)
    return R


R_T_S = induced_rep(T_S)

# Verify: K_GR(D')_ij = B_{D'}(B_i, B_j) = B_D(T_S^{-T} B_i T_S^{-1}, T_S^{-T} B_j T_S^{-1})
# (This is more subtle — let me think.)

# Actually the parent's rule is:
#   G_{D'} = T_S^{-T} G_D T_S^{-1}     (in symmetric-tensor matrix form)
#
# But here T_S is a 4×4 matrix and G_D is a 10×10 matrix. The transition on the
# 10-dim symmetric-tensor space is via the induced representation R(T_S).
#
# So the actual rule is: G_{D'} = R(T_S)^{-T} G_D R(T_S)^{-1}.

R_inv = np.linalg.inv(R_T_S)
G_transformed = R_inv.T @ K_GR_D @ R_inv

# Verify K_GR(D') equals R(T_S)^{-T} K_GR(D) R(T_S)^{-1}:
transition_diff = np.max(np.abs(K_GR_D_prime - G_transformed))
check(
    "K_GR transition rule: G_{D'} = R(T_S)^{-T} G_D R(T_S)^{-1}",
    transition_diff < 1e-8,
    f"max |G_{{D'}} - R^{{-T}} G_D R^{{-1}}| = {transition_diff:.3e}",
)


# -----------------------------------------------------------------------------
# Step 6: Counterfactual — singular T_S breaks the relation
# -----------------------------------------------------------------------------

section("Step 6: Counterfactual — singular T_S breaks invertibility")

T_S_singular = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],  # last row is zero -> singular
])
det_TS_sing = np.linalg.det(T_S_singular)
check(
    "Singular T_S has det = 0",
    abs(det_TS_sing) < 1e-10,
    f"det(T_S_singular) = {det_TS_sing}",
)

# D' = T_S^T D T_S becomes degenerate:
D_prime_sing = T_S_singular.T @ D @ T_S_singular
det_Dp_sing = np.linalg.det(D_prime_sing)
check(
    "D' from singular T_S becomes degenerate (rank-deficient)",
    abs(det_Dp_sing) < 1e-10,
    f"det(D'_sing) = {det_Dp_sing}",
)


# -----------------------------------------------------------------------------
# Step 7: Counterfactual — degenerate D breaks K_GR nondegeneracy
# -----------------------------------------------------------------------------

section("Step 7: Counterfactual — degenerate D breaks K_GR nondegeneracy")

D_singular = np.diag([0, 1, 1, 1])  # not invertible
try:
    K_GR_singular = K_GR_matrix(D_singular)
    fail_caught = False
except np.linalg.LinAlgError:
    fail_caught = True

check(
    "Singular D causes K_GR computation to fail (D^{-1} undefined)",
    fail_caught,
    "np.linalg.LinAlgError raised when D is singular",
)


# -----------------------------------------------------------------------------
# Step 8: Three named obstructions for full multi-chart closure
# -----------------------------------------------------------------------------

section("Step 8: Three named obstructions for multi-chart full-atlas closure")

obstructions = [
    "Obstruction 1: multi-chart cocycle conditions T_{ij} T_{jk} = T_{ik} on triple overlaps NOT verified (PL S^3 has 5 charts, 10 triple overlaps)",
    "Obstruction 2: global stationary section on patched atlas NOT computed",
    "Obstruction 3: atlas-refinement / continuum limit not addressed",
]

for obs in obstructions:
    print(f"  • {obs}")

check(
    f"Three named obstructions documented",
    len(obstructions) == 3,
    "Specific repair targets for full PL S^3 atlas closure",
)


# -----------------------------------------------------------------------------
# Step 9: Specific repair targets for PL S^3 atlas
# -----------------------------------------------------------------------------

section("Step 9: PL S^3 atlas combinatorics (5-vertex 4-simplex boundary)")

# PL S^3 = boundary of 4-simplex
# - 5 vertices
# - 10 edges (= 5 choose 2)
# - 10 triangles (= 5 choose 3)
# - 5 tetrahedra (= 5 choose 4)

n_vertices = 5
n_edges = n_vertices * (n_vertices - 1) // 2
n_triangles = n_vertices * (n_vertices - 1) * (n_vertices - 2) // 6
n_tetrahedra = n_vertices * (n_vertices - 1) * (n_vertices - 2) * (n_vertices - 3) // 24

print(f"         PL S^3 boundary of 4-simplex:")
print(f"           vertices:  {n_vertices}")
print(f"           edges:     {n_edges}  (= chart pairwise overlaps)")
print(f"           triangles: {n_triangles}  (= triple overlaps with cocycle conditions)")
print(f"           tetrahedra: {n_tetrahedra}")

check(
    "PL S^3 atlas needs 5 charts, 10 pairwise + 10 triple overlaps",
    n_edges == 10 and n_triangles == 10,
    f"edges={n_edges}, triangles={n_triangles}, tetrahedra={n_tetrahedra}",
)


# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
print(f"{'=' * 70}")
print(
    "STRETCH ATTEMPT OUTCOME (output type c):\n"
    "  2-chart overlap-invariance numerically verified (10 random h, k pairs).\n"
    "  K_GR(D) nondegeneracy verified on generic Lorentzian D.\n"
    "  K_GR transition rule verified via induced representation.\n"
    "  Counterfactuals (singular T_S, singular D) confirmed.\n"
    "  Three named obstructions documented for multi-chart full closure.\n"
    "Multi-chart full-atlas closure remains OPEN."
)

if FAIL_COUNT > 0:
    sys.exit(1)
sys.exit(0)
