#!/usr/bin/env python3
"""Koide Matrix-Unit Source Law + Cyclic Projection (Route 2).

Verifies every algebraic claim of
`docs/KOIDE_MATRIX_UNIT_SOURCE_LAW_CYCLIC_PROJECTION_NOTE_2026-04-18.md`
against exact numerical matrices on the retained hw=1 triplet.

Axiom base: Cl(3)/Z^3 retained triplet T_1, observable principle
W[J] = log|det(D+J)| - log|det D|, Schur inheritance, HW1 shape theorem.

No PDG masses. No fitted flavor input. Random circulant D and dense
random D used to separate the axiom-forced content from the free scalar.

Exit: PASS/FAIL count; nonzero failures surface as exceptions.
"""
from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------
# Section 0 : retained cyclic / matrix-unit basis
# --------------------------------------------------------------------------

I3 = np.eye(3, dtype=complex)
# retained forward cycle C: C |X_j> = |X_{j+1}> so (C)_{i,j} = delta_{i, j+1 mod 3}
C = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)

C2 = C @ C
assert np.allclose(C @ C2, I3), "C^3 = I"
assert np.allclose(C.conj().T, C2), "C^{-1} = C^2 = C^dag"

# axis projectors
P = [np.zeros((3, 3), dtype=complex) for _ in range(3)]
for i in range(3):
    P[i][i, i] = 1.0


def E(i, j):
    """Matrix unit E_ij: 1 at (i,j), zero elsewhere."""
    M = np.zeros((3, 3), dtype=complex)
    M[i, j] = 1.0
    return M


# Cyclic Hermitian basis (Koide compression basis)
B0 = I3.copy()
B1 = C + C2
B2 = 1j * (C - C2)

# Standard Hermitian matrix-unit Hermitian basis (9-real)
D1 = E(0, 0)
D2 = E(1, 1)
D3 = E(2, 2)
# symmetric
X12 = E(0, 1) + E(1, 0)
X23 = E(1, 2) + E(2, 1)
X13 = E(0, 2) + E(2, 0)
# antisymmetric
Y12 = 1j * (E(0, 1) - E(1, 0))
Y23 = 1j * (E(1, 2) - E(2, 1))
Y13 = 1j * (E(0, 2) - E(2, 0))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

pass_count = 0
fail_count = 0


def check(name, cond, detail=""):
    global pass_count, fail_count
    if cond:
        pass_count += 1
        print(f"[PASS] {name}")
    else:
        fail_count += 1
        print(f"[FAIL] {name}  {detail}")


def close(a, b, tol=1e-12):
    return np.allclose(a, b, atol=tol)


def dW(X, G):
    """Observable-principle linear functional: dW(X) = Re Tr(X G)."""
    return np.real(np.trace(X @ G))


# --------------------------------------------------------------------------
# Section 1 : basis sanity
# --------------------------------------------------------------------------

check("B0 Hermitian", close(B0, B0.conj().T))
check("B1 Hermitian", close(B1, B1.conj().T))
check("B2 Hermitian", close(B2, B2.conj().T))

# Orthogonality under real trace pairing
for (a, na), (b, nb) in [
    ((B0, "B0"), (B0, "B0")),
    ((B1, "B1"), (B1, "B1")),
    ((B2, "B2"), (B2, "B2")),
    ((B0, "B0"), (B1, "B1")),
    ((B0, "B0"), (B2, "B2")),
    ((B1, "B1"), (B2, "B2")),
]:
    val = np.real(np.trace(a.conj().T @ b))
    target = 0.0
    if na == nb:
        target = {"B0": 3.0, "B1": 6.0, "B2": 6.0}[na]
    check(f"<{na},{nb}> = {target}", np.isclose(val, target))

# Matrix units generate M_3(C): check 9 real span.
basis9 = [D1, D2, D3, X12, X23, X13, Y12, Y23, Y13]
M = np.stack([m.reshape(-1) for m in basis9])
# Stacked as 9 x 9 complex; convert to 18 real rows (real/imag parts of each
# entry), then rank should be 9 (since Herm(3) is 9-real).
real_rows = np.concatenate([M.real, M.imag], axis=0)
check(
    "9 Hermitian matrix units span Herm(3)",
    np.linalg.matrix_rank(real_rows, tol=1e-10) == 9,
)


# --------------------------------------------------------------------------
# Section 2 : cyclic projector and compression formulas
# --------------------------------------------------------------------------

def Pcyc(X):
    return (X + C @ X @ C2 + C2 @ X @ C) / 3.0


# All diagonals -> B0/3
for D in (D1, D2, D3):
    check(f"P_cyc(D) = B0/3 for diagonal", close(Pcyc(D), B0 / 3.0))

# All symmetric off-diagonals -> B1/3
for name, X in [("X12", X12), ("X23", X23), ("X13", X13)]:
    check(f"P_cyc({name}) = B1/3", close(Pcyc(X), B1 / 3.0))

# Antisymmetric pattern: with this convention
#   Y_ij := i(E_ij - E_ji),  C[k+1,k] = 1 (forward)
# we get  P_cyc(Y12) = P_cyc(Y23) = -B2/3 ;  P_cyc(Y13) = +B2/3.
# (Sign convention matches internal algebra; cyclic compression statement
# is identical up to this overall sign flip on the antisymmetric block.)
check("P_cyc(Y12) = -B2/3", close(Pcyc(Y12), -B2 / 3.0))
check("P_cyc(Y23) = -B2/3", close(Pcyc(Y23), -B2 / 3.0))
check("P_cyc(Y13) = +B2/3", close(Pcyc(Y13), +B2 / 3.0))


# --------------------------------------------------------------------------
# Section 3 : the retained source response on the matrix-unit basis
# --------------------------------------------------------------------------
#
# Step 2a closed form claim:
# if G = g0 I + g1 C + g1* C^2, then
#   dW(E_ij) = Re G_{ji}
#     with G_{ji} = g0 d_{ij} + g1 d_{j,i+1} + g1* d_{j,i+2}  (indices mod 3)
#   so dW(E_ij) is one of {g0, Re g1, Re g1} depending on (j - i) mod 3.

rng = np.random.default_rng(42)
for trial in range(20):
    g0 = float(rng.normal())
    g1 = complex(rng.normal(), rng.normal())
    G = g0 * I3 + g1 * C + np.conj(g1) * C2
    # Hermitian?
    check(f"[trial {trial}] circulant G Hermitian", close(G, G.conj().T))

    # Matrix-unit responses
    for i in range(3):
        for j in range(3):
            predicted = {
                0: g0,
                1: np.real(g1),
                2: np.real(g1),
            }[(j - i) % 3]
            actual = dW(E(i, j), G)
            check(
                f"[trial {trial}] dW(E_{i}{j}) = predicted (s={(j-i)%3})",
                np.isclose(actual, predicted),
            )

    # Sym / antisym closed forms
    alpha = np.real(g1)
    beta = np.imag(g1)
    for Xs in (X12, X23, X13):
        check(
            f"[trial {trial}] sym off-diag -> 2 alpha",
            np.isclose(dW(Xs, G), 2 * alpha),
        )
    check(f"[trial {trial}] dW(Y12) = -2 beta", np.isclose(dW(Y12, G), -2 * beta))
    check(f"[trial {trial}] dW(Y23) = -2 beta", np.isclose(dW(Y23, G), -2 * beta))
    check(f"[trial {trial}] dW(Y13) = +2 beta", np.isclose(dW(Y13, G), +2 * beta))

    # Cyclic channel formulas (with this convention r_2 = -6 beta)
    r0 = dW(B0, G)
    r1 = dW(B1, G)
    r2_direct = dW(B2, G)
    r2_indirect = dW(Y12, G) + dW(Y23, G) - dW(Y13, G)
    check(f"[trial {trial}] r0 = 3 g0", np.isclose(r0, 3 * g0))
    check(f"[trial {trial}] r1 = 6 alpha", np.isclose(r1, 6 * alpha))
    check(f"[trial {trial}] r2 = +6 beta", np.isclose(r2_direct, +6 * beta))
    # Note: dW(Y12)+dW(Y23)-dW(Y13) = -2b-2b-2b = -6b, not equal to r2=+6b.
    # The direct B2 computation is the canonical r_2; the Y-sum reconstruction
    # uses the DWEH compression signs (P_cyc(Y12)=-B2/3 etc.), giving -r2.
    check(
        f"[trial {trial}] Y-sum reconstruction = -r2 = -6 beta",
        np.isclose(r2_indirect, -6 * beta),
    )

    # Koide equivalence
    lhs = 2 * r0 ** 2
    rhs = r1 ** 2 + r2_direct ** 2
    circle_scalar = g0 ** 2 - 2 * (alpha ** 2 + beta ** 2)
    check(
        f"[trial {trial}] 2 r0^2 - (r1^2+r2^2) = 18 (g0^2 - 2|g1|^2)",
        np.isclose(lhs - rhs, 18 * circle_scalar),
    )


# --------------------------------------------------------------------------
# Section 4 : Schur inheritance forces G circulant starting from D circulant
# --------------------------------------------------------------------------
#
# Observable principle gives dW(X) = Re Tr(X G) with G = D^{-1} (for Hermitian
# invertible D on T_1). Cl(3)/Z^3 invariance of D (C D C^{-1} = D) implies G
# circulant. Verify numerically on random circulant Hermitian D.

for trial in range(20):
    d0 = float(rng.normal()) + 5.0  # bounded away from singular
    d1 = complex(rng.normal(), rng.normal())
    D = d0 * I3 + d1 * C + np.conj(d1) * C2
    check(f"[Schur trial {trial}] D Hermitian", close(D, D.conj().T))
    check(f"[Schur trial {trial}] [C, D] = 0", close(C @ D, D @ C))
    G = np.linalg.inv(D)
    check(f"[Schur trial {trial}] [C, G] = 0", close(C @ G, G @ C))
    # G has circulant form. Note: for G = g0 I + g1 C + g1* C^2,
    #   G[1,0] = g1   (since C[1,0] = 1, C^2[1,0] = 0, I[1,0] = 0).
    g0 = np.real(np.trace(G)) / 3.0
    g1 = G[1, 0]
    G_recon = g0 * I3 + g1 * C + np.conj(g1) * C2
    check(
        f"[Schur trial {trial}] G = g0 I + g1 C + g1* C^2",
        close(G, G_recon),
    )


# --------------------------------------------------------------------------
# Section 5 : Schur equivariant reduction from larger carrier preserves circulant
# --------------------------------------------------------------------------
# V = T_1 (+) W with U = C (+) R and positive Hermitian C_3-covariant parent M.
# Schur complement S = A - B D^{-1} B^dagger is circulant on T_1.

for trial in range(10):
    # W dimension
    dW_dim = int(rng.integers(1, 5))
    # random unitary on W commuting with itself (pick R as a random permutation-
    # like unitary that matches C_3 via a 3-fold block)
    # simplest: R acts trivially (identity) - already covered; so build random
    # R as a 3-fold diagonal cycle if dW is multiple of 3, else identity.
    if dW_dim % 3 == 0:
        blocks = dW_dim // 3
        R = np.kron(np.eye(blocks, dtype=complex), C)
    else:
        R = np.eye(dW_dim, dtype=complex)

    # build C_3-covariant positive M
    # A circulant on T_1
    a0 = float(rng.normal()) + 5
    a1 = complex(rng.normal(), rng.normal())
    A = a0 * I3 + a1 * C + np.conj(a1) * C2

    # D-block on W: commutes with R. pick D_block positive and commuting with R.
    D_block = np.eye(dW_dim, dtype=complex) * (abs(float(rng.normal())) + 3.0)
    # We need B satisfying C B = B R, i.e., B intertwines C with R.
    # Solve: parametrize B by random complex, project onto intertwiner subspace.
    B_raw = rng.normal(size=(3, dW_dim)) + 1j * rng.normal(size=(3, dW_dim))

    # Project onto intertwiner: (1/3) sum_k C^k B R^{-k}
    B = np.zeros((3, dW_dim), dtype=complex)
    Ck = I3
    Rinvk = np.eye(dW_dim, dtype=complex)
    Rinv = np.linalg.inv(R)
    for k in range(3):
        B += Ck @ B_raw @ Rinvk
        Ck = Ck @ C
        Rinvk = Rinvk @ Rinv
    B = B / 3.0

    check(f"[fullSchur trial {trial}] intertwiner C B = B R", close(C @ B, B @ R))

    M = np.block([[A, B], [B.conj().T, D_block]])
    U = np.block(
        [
            [C, np.zeros((3, dW_dim), dtype=complex)],
            [np.zeros((dW_dim, 3), dtype=complex), R],
        ]
    )
    check(
        f"[fullSchur trial {trial}] U M U^dag = M",
        close(U @ M @ U.conj().T, M),
    )

    # Schur complement
    S = A - B @ np.linalg.inv(D_block) @ B.conj().T
    check(f"[fullSchur trial {trial}] [C, S] = 0", close(C @ S, S @ C))


# --------------------------------------------------------------------------
# Section 6 : demonstrate the Koide circle is NOT pinned by axioms alone
# --------------------------------------------------------------------------
# Produce two circulant G with equal 'shape' but different g0^2 / |g1|^2.
# Both satisfy C G C^-1 = G but only one satisfies Koide circle.

G_on = 1.0 * I3 + (1.0 / np.sqrt(2)) * C + (1.0 / np.sqrt(2)) * C2
# g0 = 1, alpha = 1/sqrt(2), beta = 0 -> g0^2 = 1, 2|g1|^2 = 2*(1/2) = 1. ON.

G_off = 1.0 * I3 + 1.0 * C + 1.0 * C2
# g0 = 1, alpha = 1, beta = 0 -> g0^2 = 1, 2|g1|^2 = 2. OFF.

for name, G, expected_on_circle in [("G_on", G_on, True), ("G_off", G_off, False)]:
    g0 = np.real(np.trace(G)) / 3.0
    g1 = G[1, 0]
    on = np.isclose(g0 ** 2, 2 * abs(g1) ** 2)
    check(f"{name} on Koide circle?", on == expected_on_circle)
    r0 = dW(B0, G)
    r1 = dW(B1, G)
    r2 = dW(B2, G)
    lhs = 2 * r0 ** 2
    rhs = r1 ** 2 + r2 ** 2
    koide = np.isclose(lhs, rhs)
    check(f"{name} Koide <=> circle scalar", koide == on)


# --------------------------------------------------------------------------
# Section 7 : report
# --------------------------------------------------------------------------
print("")
print(f"PASS={pass_count}  FAIL={fail_count}")
if fail_count:
    raise SystemExit(1)
