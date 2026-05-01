#!/usr/bin/env python3
"""Validate the corrected sign character and unique-stationary-solution
content of the universal-GR positive-background local closure.

The note's bilinear form is

    B_D(h, k) = -Tr(D^-1 h D^-1 k)

For symmetric positive-definite D and symmetric h, this script verifies:

  CHECK A1: B_D(h, h) <= 0 for symmetric h, with equality iff h = 0
            (i.e. H_D is negative-definite on symmetric tangents — NOT
            positive-definite as an earlier draft of the note claimed).
  CHECK A2: The reformulation B_D(h, h) = -Tr(H_tilde^2) holds, where
            H_tilde = D^{-1/2} h D^{-1/2}.
  CHECK B:  The induced operator K_GR := H_D (acting as B_D(h, .) ) admits
            a unique stationary point F_* = K^{-1} J for any source J,
            and the completion identity
                I_GR(F_* + Δ) - I_GR(F_*) = (1/2) <Δ, K Δ>
            holds.
  CHECK C:  Reproducing the *earlier* (incorrect) positive-definite claim
            on the same family explicitly fails (sanity check on the
            corrected polarity).

Reports PASS=N FAIL=N for the audit-lane runner classifier.
"""
from __future__ import annotations

import numpy as np


RNG = np.random.default_rng(20260501)


def random_spd(n: int) -> np.ndarray:
    A = RNG.standard_normal((n, n))
    return A.T @ A + n * np.eye(n)


def random_symmetric(n: int) -> np.ndarray:
    A = RNG.standard_normal((n, n))
    return 0.5 * (A + A.T)


def symmetric_inverse_sqrt(D: np.ndarray) -> np.ndarray:
    w, V = np.linalg.eigh(D)
    return V @ np.diag(1.0 / np.sqrt(w)) @ V.T


def B_D(D: np.ndarray, h: np.ndarray, k: np.ndarray) -> float:
    Dinv = np.linalg.inv(D)
    return float(-np.trace(Dinv @ h @ Dinv @ k))


def vec_sym(h: np.ndarray) -> np.ndarray:
    """Vectorize a symmetric n×n matrix into n(n+1)/2 independent components
    (upper-triangular flatten, with sqrt(2) factors for off-diagonal so that
    Frobenius inner products on matrices match Euclidean inner products on
    vectors)."""
    n = h.shape[0]
    out = []
    for i in range(n):
        for j in range(i, n):
            if i == j:
                out.append(h[i, i])
            else:
                out.append(np.sqrt(2.0) * h[i, j])
    return np.array(out)


def unvec_sym(v: np.ndarray, n: int) -> np.ndarray:
    h = np.zeros((n, n))
    idx = 0
    for i in range(n):
        for j in range(i, n):
            if i == j:
                h[i, i] = v[idx]
            else:
                h[i, j] = v[idx] / np.sqrt(2.0)
                h[j, i] = h[i, j]
            idx += 1
    return h


def operator_matrix(D: np.ndarray) -> np.ndarray:
    """Build the dense matrix K of the operator induced by B_D on the
    symmetric tangent space, in the orthonormal vec basis above. So
    B_D(h, k) = vec(h)^T K vec(k)."""
    n = D.shape[0]
    dim = n * (n + 1) // 2
    K = np.zeros((dim, dim))
    basis = []
    for i in range(dim):
        e = np.zeros(dim)
        e[i] = 1.0
        basis.append(unvec_sym(e, n))
    for i in range(dim):
        for j in range(dim):
            K[i, j] = B_D(D, basis[i], basis[j])
    K = 0.5 * (K + K.T)
    return K


def main() -> int:
    print("=" * 78)
    print("UNIVERSAL GR POSITIVE-BACKGROUND LOCAL CLOSURE — sign and uniqueness")
    print("=" * 78)
    print()
    print("Bilinear form: B_D(h, k) = -Tr(D^-1 h D^-1 k)")
    print()

    passes = 0
    fails = 0

    # CHECK A1 + A2: negative-definiteness via random samples
    print("CHECK A1/A2: negative-definiteness of H_D on symmetric tangents")
    n_dims = (3, 5, 7)
    n_trials = 30
    a1_pass = True
    a2_pass = True
    for n in n_dims:
        for _ in range(n_trials):
            D = random_spd(n)
            h = random_symmetric(n)
            val = B_D(D, h, h)
            if val > 1e-10:
                a1_pass = False
                print(f"  [FAIL] n={n}: B_D(h,h) = {val:+.3e} > 0")
            # alt formulation
            Dinv_half = symmetric_inverse_sqrt(D)
            H_tilde = Dinv_half @ h @ Dinv_half
            val_alt = -np.trace(H_tilde @ H_tilde)
            if abs(val - val_alt) > 1e-10 * max(1.0, abs(val)):
                a2_pass = False
                print(f"  [FAIL] n={n}: alt formulation differs by {abs(val-val_alt):.3e}")
    if a1_pass:
        passes += 1
        print("  [PASS] B_D(h,h) <= 0 for all sampled symmetric h on SPD D")
    else:
        fails += 1
    if a2_pass:
        passes += 1
        print("  [PASS] B_D(h,h) = -Tr(H_tilde^2) reformulation matches")
    else:
        fails += 1
    print()

    # CHECK B: full operator on symmetric tangent space is negative-definite,
    # has unique stationary point, completion identity holds
    print("CHECK B: dense operator K is symmetric negative-definite; unique F_*; completion identity")
    n = 5
    D = random_spd(n)
    K = operator_matrix(D)
    sym_err = float(np.linalg.norm(K - K.T))
    eigs = np.linalg.eigvalsh(K)
    is_sym = sym_err < 1e-10
    is_neg_def = eigs.max() < -1e-10
    if is_sym:
        passes += 1
        print(f"  [PASS] K is symmetric  (||K - K^T|| = {sym_err:.3e})")
    else:
        fails += 1
        print(f"  [FAIL] K not symmetric  (||K - K^T|| = {sym_err:.3e})")
    if is_neg_def:
        passes += 1
        print(f"  [PASS] K is negative-definite  (max eig = {eigs.max():+.3e}, min eig = {eigs.min():+.3e})")
    else:
        fails += 1
        print(f"  [FAIL] K not negative-definite  (max eig = {eigs.max():+.3e})")

    # Stationary point: K F_* = J
    dim = K.shape[0]
    J = RNG.standard_normal(dim)
    F_star = np.linalg.solve(K, J)
    grad_at_star = K @ F_star - J
    if np.linalg.norm(grad_at_star) < 1e-10 * (1 + np.linalg.norm(J)):
        passes += 1
        print(f"  [PASS] F_* = K^-1 J satisfies stationary condition  (||grad|| = {np.linalg.norm(grad_at_star):.3e})")
    else:
        fails += 1
        print(f"  [FAIL] stationary condition violated  (||grad|| = {np.linalg.norm(grad_at_star):.3e})")

    # Completion identity: I(F_* + Δ) - I(F_*) = (1/2) <Δ, K Δ>
    completion_ok = True
    for _ in range(20):
        delta = RNG.standard_normal(dim)
        I_star = 0.5 * F_star @ K @ F_star - J @ F_star
        I_perturbed = 0.5 * (F_star + delta) @ K @ (F_star + delta) - J @ (F_star + delta)
        diff = I_perturbed - I_star
        rhs = 0.5 * delta @ K @ delta
        if abs(diff - rhs) > 1e-8 * max(1.0, abs(rhs)):
            completion_ok = False
            print(f"  [FAIL] completion identity off: lhs={diff:+.3e}, rhs={rhs:+.3e}")
            break
    if completion_ok:
        passes += 1
        print("  [PASS] completion identity I(F_*+Δ) - I(F_*) = (1/2)<Δ, K Δ>  holds for 20 random Δ")
    else:
        fails += 1
    print()

    # CHECK C: explicit refutation of the prior PD claim
    print("CHECK C: explicit refutation of the earlier 'positive-definite' framing")
    if eigs.max() < 0:
        passes += 1
        print(f"  [PASS] K has NO positive eigenvalues  (max eig = {eigs.max():+.3e})")
        print("         The earlier draft's K ≻ 0 claim is explicitly false on this sample.")
    else:
        fails += 1
        print(f"  [FAIL] K has a positive eigenvalue  (max eig = {eigs.max():+.3e})")
    print()

    print(f"PASS={passes} FAIL={fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
