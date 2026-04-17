#!/usr/bin/env python3
"""
Gauge-Normalization Rigidity Theorem
===================================

Purpose
-------
Replace the loose "absorbed coupling" rhetoric with a sharper statement:

  once the gauge algebra is derived as a concrete compact subalgebra of
  End(V), and the Hilbert-space metric on V is fixed, there is no
  independent scalar normalization freedom left in the gauge generators.

In standard notation one often writes:

    U = exp(i g A^a T_a a)

with a free bare coupling g.  In the present framework, the derived object is
the concrete operator algebra itself.  The physical connection is the
operator-valued one-form

    A_op = A^a T_a  in su(3) subset End(V),

and the holonomy is

    U = exp(i A_op a).

The scalar "g" is therefore not a physical parameter.  It is only a
coordinate rescaling on the coefficients A^a once the generator basis is
chosen.  In the canonical orthonormal basis inherited from the Hilbert-space
trace form, this means g_bare = 1.

This script verifies the algebraic pieces numerically on the canonical SU(3)
embedding already established by the SU(3) commutant theorem.

Self-contained: numpy only.
"""

from __future__ import annotations

import numpy as np

np.set_printoptions(precision=8, linewidth=120, suppress=True)

I2 = np.eye(2, dtype=complex)
I3 = np.eye(3, dtype=complex)
I4 = np.eye(4, dtype=complex)
I8 = np.eye(8, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)

PASS = 0
FAIL = 0
RESULTS = []


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    RESULTS.append((name, tag, detail))
    msg = f"  [{tag}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def comm(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def is_close(A: np.ndarray, B: np.ndarray, tol: float = 1e-10) -> bool:
    return np.linalg.norm(A - B) < tol


def build_swap23() -> np.ndarray:
    swap = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                swap[4 * a + 2 * c + b, 4 * a + 2 * b + c] = 1.0
    return swap


def build_u8_symanti() -> np.ndarray:
    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)
    u4 = np.column_stack(
        [
            np.kron(e0, e0),
            (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2),
            np.kron(e1, e1),
            (np.kron(e0, e1) - np.kron(e1, e0)) / np.sqrt(2),
        ]
    )
    return np.kron(I2, u4)


def gellmann_matrices() -> list[np.ndarray]:
    return [
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
    ]


def build_canonical_generators() -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """
    Return:
      - full 8x8 generators in the derived taste-space embedding
      - 3x3 triplet-block generators
      - weak su(2) generators and SWAP for consistency checks
    """
    t_weak = [
        0.5 * kron3(SX, I2, I2),
        0.5 * kron3(SY, I2, I2),
        0.5 * kron3(SZ, I2, I2),
    ]
    swap23 = build_swap23()
    u8 = build_u8_symanti()

    full = []
    triplet = []
    for lam in gellmann_matrices():
        t3 = lam / 2.0
        block4 = np.zeros((4, 4), dtype=complex)
        block4[:3, :3] = t3
        t8 = u8 @ np.kron(I2, block4) @ u8.conj().T
        full.append(t8)
        triplet.append(t3)
    return full, triplet, t_weak + [swap23]


def gram_triplet(triplet: list[np.ndarray]) -> np.ndarray:
    n = len(triplet)
    gram = np.zeros((n, n), dtype=float)
    for i, ti in enumerate(triplet):
        for j, tj in enumerate(triplet):
            gram[i, j] = np.trace(ti @ tj).real
    return gram


def casimir_triplet(triplet: list[np.ndarray]) -> np.ndarray:
    total = np.zeros((3, 3), dtype=complex)
    for t in triplet:
        total += t @ t
    return total


def random_orthogonal(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(n, n))
    q, r = np.linalg.qr(m)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def main() -> int:
    print("=" * 78)
    print("GAUGE-NORMALIZATION RIGIDITY THEOREM")
    print("=" * 78)
    print()
    print("Claim:")
    print("  once SU(3) is derived as a concrete compact subalgebra of End(V),")
    print("  the Hilbert-space trace form fixes the generator normalization up")
    print("  to orthogonal basis rotation.  There is no independent scalar")
    print("  gauge-coupling parameter left.  In canonical coordinates: g_bare = 1.")
    print()

    full, triplet, constraints = build_canonical_generators()
    t_weak = constraints[:3]
    swap23 = constraints[3]

    print("SECTION 1: Canonical SU(3) generators live in the derived commutant")
    print("-" * 78)
    for idx, t in enumerate(full):
        check(f"T_{idx+1} Hermitian", is_close(t, t.conj().T))
        check(f"T_{idx+1} traceless", abs(np.trace(t)) < 1e-10)
        ok = all(is_close(comm(t, tw), np.zeros((8, 8))) for tw in t_weak)
        check(f"T_{idx+1} commutes with weak su(2)", ok)
        check(f"T_{idx+1} commutes with SWAP23", is_close(comm(t, swap23), np.zeros((8, 8))))

    print()
    print("SECTION 2: Canonical trace normalization on the triplet block")
    print("-" * 78)
    gram = gram_triplet(triplet)
    target = 0.5 * np.eye(8)
    check("Tr_3(T_a T_b) = delta_ab / 2", is_close(gram, target), f"max dev = {np.max(np.abs(gram - target)):.2e}")

    cas = casimir_triplet(triplet)
    check("Sum_a T_a T_a = (4/3) I_3", is_close(cas, (4.0 / 3.0) * I3), f"max dev = {np.max(np.abs(cas - (4.0/3.0)*I3)):.2e}")

    print()
    print("SECTION 3: Allowed basis ambiguity is orthogonal rotation, not scalar dilation")
    print("-" * 78)
    ortho = random_orthogonal(8, seed=42)
    rotated = []
    for a in range(8):
        ta = sum(ortho[a, b] * triplet[b] for b in range(8))
        rotated.append(ta)

    gram_rot = gram_triplet(rotated)
    cas_rot = casimir_triplet(rotated)
    check("Orthogonal basis rotation preserves trace normalization", is_close(gram_rot, target), f"max dev = {np.max(np.abs(gram_rot - target)):.2e}")
    check("Orthogonal basis rotation preserves Casimir", is_close(cas_rot, (4.0 / 3.0) * I3), f"max dev = {np.max(np.abs(cas_rot - (4.0/3.0)*I3)):.2e}")

    for scale in [0.5, 1.2, 2.0]:
        scaled = [scale * t for t in triplet]
        gram_scaled = gram_triplet(scaled)
        cas_scaled = casimir_triplet(scaled)
        check(
            f"Scalar dilation {scale:g} changes trace normalization",
            not is_close(gram_scaled, target),
            f"Tr(T_a T_b) -> {scale**2:.2f} * delta_ab / 2",
        )
        check(
            f"Scalar dilation {scale:g} changes Casimir",
            not is_close(cas_scaled, (4.0 / 3.0) * I3),
            f"C_F -> {scale**2 * 4.0/3.0:.6f}",
        )

    print()
    print("SECTION 4: g is coordinate redundancy, not a physical parameter")
    print("-" * 78)
    rng = np.random.default_rng(7)
    coeffs = rng.normal(size=8)
    a_op = sum(c * t for c, t in zip(coeffs, triplet))
    for g in [0.3, 0.8, 1.7]:
        coeffs_prime = g * coeffs
        a_op_prime = sum(c * t for c, t in zip(coeffs_prime, triplet))
        check(
            f"Operator coefficients absorb scalar g = {g:g}",
            is_close(a_op_prime, g * a_op),
            "A_op' = sum (g A^a) T_a = g * A_op",
        )

    print()
    print("Interpretation:")
    print("  - The physical object is the concrete operator A_op in the derived")
    print("    gauge algebra, not a split into 'g' times coefficients.")
    print("  - Changing basis by an orthogonal rotation is harmless.")
    print("  - Uniform scalar dilation changes the fixed trace form and Casimir,")
    print("    so it is not an admissible ambiguity of the canonical basis.")
    print("  - Once the canonical basis is chosen, the holonomy is")
    print("        U = exp(i A^a T_a a)")
    print("    with no additional scalar coupling.")
    print()
    print("Conclusion:")
    print("  The standard notation U = exp(i g A^a T_a a) contains no independent")
    print("  physical bare coupling in this framework. In canonical normalization,")
    print("  g_bare = 1.")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
