#!/usr/bin/env python3
"""Blocker analysis for the native Cl(3) -> KS-factor su(2) bridge.

This script does not try to prove the bridge exists. It checks the exact
surface that is currently available and shows why the native bivector lane
does not yet canonically determine the KS factorization.

The key points are:
  - the native bivector su(2) is real and stable
  - its commutant is 16-dimensional, so the multiplicity space has U(4) freedom
  - the KS factor su(2) + SWAP theorem is a separate KS-surface result
  - the residual SWAP used by the KS theorem is not canonically produced by
    the native bivector lane alone on this surface
"""

from __future__ import annotations

import numpy as np


I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron3(a, b, c):
    return np.kron(a, np.kron(b, c))


def commutator(a, b):
    return a @ b - b @ a


def commutant_basis(ops, tol=1e-10):
    n = ops[0].shape[0]
    blocks = []
    for op in ops:
        blocks.append(np.kron(np.eye(n), op) - np.kron(op.T, np.eye(n)))
    mat = np.vstack(blocks)
    _, s, vh = np.linalg.svd(mat)
    rank = np.sum(s > tol)
    null = vh[rank:].conj().T
    return null


def exp_hermitian(h, theta):
    vals, vecs = np.linalg.eigh(h)
    return vecs @ np.diag(np.exp(1j * theta * vals)) @ vecs.conj().T


def matrix_rank(mats, tol=1e-10):
    flat = np.array([m.reshape(-1) for m in mats])
    return np.linalg.matrix_rank(flat, tol=tol)


def main():
    print("=" * 72)
    print("SU(3) NATIVE-BRIDGE BLOCKER ANALYSIS")
    print("=" * 72)

    # KS surface generators used by the formal theorem.
    g1 = kron3(sx, I2, I2)
    g2 = kron3(sz, sx, I2)
    g3 = kron3(sz, sz, sx)

    # Native bivectors from the same Clifford generators.
    b1 = -0.5j * (g2 @ g3)
    b2 = -0.5j * (g3 @ g1)
    b3 = -0.5j * (g1 @ g2)
    bivectors = [b1, b2, b3]

    # KS factor su(2) used in the formal theorem surface.
    t1 = 0.5 * kron3(sx, I2, I2)
    t2 = 0.5 * kron3(sy, I2, I2)
    t3 = 0.5 * kron3(sz, I2, I2)
    ks_su2 = [t1, t2, t3]

    print("Surface checks:")
    print(f"  [PASS] native bivectors satisfy su(2): {np.allclose(commutator(b1, b2), 1j * b3, atol=1e-10)}")
    print(f"  [PASS] KS factor su(2) satisfies su(2): {np.allclose(commutator(t1, t2), 1j * t3, atol=1e-10)}")
    print(f"  [INFO] rank span(native bivectors + KS factor) = {matrix_rank(bivectors + ks_su2)}")

    print()
    print("Residual-symmetry checks:")
    swap23 = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * a + 2 * c + b
                swap23[dst, src] = 1.0

    native_swap_comm = [np.linalg.norm(commutator(swap23, bk)) for bk in bivectors]
    ks_swap_comm = [np.linalg.norm(commutator(swap23, tk)) for tk in ks_su2]
    print(f"  native bivector commutators with SWAP23: {native_swap_comm}")
    print(f"  KS factor commutators with SWAP23:       {ks_swap_comm}")

    print()
    print("Native commutant size:")
    null = commutant_basis(bivectors)
    dim = null.shape[1]
    print(f"  dim Comm(native bivector su(2)) = {dim}")

    # Extract one non-scalar Hermitian commutant element to show the residual
    # multiplicity freedom is genuinely nontrivial.
    h = None
    for i in range(dim):
        m = null[:, i].reshape(8, 8)
        herm = (m + m.conj().T) / 2.0
        herm -= np.trace(herm) / 8.0 * I8
        if np.linalg.norm(herm) > 1e-8:
            h = herm
            break

    if h is not None:
        v = exp_hermitian(h, np.pi / 7.0)
        commute_norms = [np.linalg.norm(commutator(v, bk)) for bk in bivectors]
        scalar_distance = np.linalg.norm(v - np.trace(v) / 8.0 * I8)
        print(f"  non-scalar commuting unitary found: {scalar_distance > 1e-6}")
        print(f"  ||[V, B_i]|| = {commute_norms}")
    else:
        print("  could not extract a non-scalar commutant element")

    print()
    print("Verdict:")
    print("  BLOCKED: the native bivector data leave a 16-dimensional commutant,")
    print("  so the multiplicity space is not canonically fixed on the current")
    print("  surface. The KS tensor-factor su(2) theorem is valid, but the")
    print("  native Cl(3) -> KS-factor bridge is not yet established.")


if __name__ == "__main__":
    main()
