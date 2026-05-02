"""Translation group composition: T_a T_b = T_{a+b} on lattice Hilbert.

Test that the lattice translation operators T_a (defined by T_a |x⟩ = |x+a⟩
on the Z^3 lattice basis, dual to lattice momentum P̂^μ via N1 of the
retained lattice Noether theorem) satisfy:

    (G1) closure:        T_a T_b = T_{a+b}             ∀ a, b ∈ Z^3
    (G2) commutativity:  T_a T_b = T_b T_a             ∀ a, b ∈ Z^3
    (G3) inverse:        T_{-a} = T_a^{-1} = T_a^†
    (G4) identity:       T_0 = I
    (G5) order:          T_a^N = I  on a periodic chain of size N (when a is unit)

Therefore the lattice translation group is exactly Z^3 (or Z/NZ × Z/NZ × Z/NZ
on a finite-N periodic lattice), matching A_min A2 (lattice geometry).
"""
from __future__ import annotations

import itertools

import numpy as np


def build_translation_3d(L: int, a: tuple[int, int, int]) -> np.ndarray:
    """Build T_a as permutation matrix on |x_1, x_2, x_3⟩ basis (L^3 dim).

    T_a |x⟩ = |x + a (mod L)⟩.
    """
    dim = L ** 3
    T = np.zeros((dim, dim), dtype=complex)
    for x1, x2, x3 in itertools.product(range(L), repeat=3):
        idx_in = x1 * L * L + x2 * L + x3
        y1 = (x1 + a[0]) % L
        y2 = (x2 + a[1]) % L
        y3 = (x3 + a[2]) % L
        idx_out = y1 * L * L + y2 * L + y3
        T[idx_out, idx_in] = 1.0
    return T


def main() -> None:
    print("=" * 72)
    print("TRANSLATION GROUP COMPOSITION T_a T_b = T_{a+b} ON Z^3 LATTICE")
    print("=" * 72)
    print()

    L = 4  # 4×4×4 periodic lattice = 64-dim per-site basis
    dim = L ** 3
    print(f"  Toy model: {L}×{L}×{L} periodic lattice, dim = {dim}")
    print()

    e1 = (1, 0, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    zero = (0, 0, 0)

    T_e1 = build_translation_3d(L, e1)
    T_e2 = build_translation_3d(L, e2)
    T_e3 = build_translation_3d(L, e3)
    T_0 = build_translation_3d(L, zero)
    Iden = np.eye(dim, dtype=complex)

    # ----- Test 1: T_0 = I -----
    print("-" * 72)
    print("TEST 1: T_0 = I (identity element)")
    print("-" * 72)
    dev0 = np.linalg.norm(T_0 - Iden)
    print(f"  ||T_0 - I|| = {dev0:.3e}")
    t1_ok = dev0 < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: closure T_a T_b = T_{a+b} (sweep over generators) -----
    print("-" * 72)
    print("TEST 2: closure T_a T_b = T_{a+b} (sweep over basis vectors)")
    print("-" * 72)
    max_close_dev = 0.0
    test_pairs = [
        (e1, e1, (2, 0, 0)),
        (e1, e2, (1, 1, 0)),
        (e1, e3, (1, 0, 1)),
        (e2, e3, (0, 1, 1)),
        (e1, (3, 2, 1), (4 % L, 2, 1)),
        ((2, 1, 0), (1, 2, 3), (3, 3, 3)),
        ((3, 3, 3), (1, 1, 1), (0, 0, 0)),  # wraps around
    ]
    for a, b, expected_sum in test_pairs:
        T_a = build_translation_3d(L, a)
        T_b = build_translation_3d(L, b)
        T_ab = T_a @ T_b
        T_sum = build_translation_3d(L, tuple((a[i] + b[i]) % L for i in range(3)))
        d = np.linalg.norm(T_ab - T_sum)
        max_close_dev = max(max_close_dev, d)
        print(f"  a={a}, b={b}: ||T_a T_b - T_{{a+b}}|| = {d:.3e}")
    t2_ok = max_close_dev < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: commutativity [T_a, T_b] = 0 (abelian) -----
    print("-" * 72)
    print("TEST 3: [T_a, T_b] = 0 (translation group is abelian)")
    print("-" * 72)
    max_comm_dev = 0.0
    for (a, label_a), (b, label_b) in itertools.combinations(
        [(e1, "e_1"), (e2, "e_2"), (e3, "e_3"), ((2, 1, 3), "(2,1,3)"), ((3, 0, 2), "(3,0,2)")], 2
    ):
        T_a = build_translation_3d(L, a)
        T_b = build_translation_3d(L, b)
        comm = T_a @ T_b - T_b @ T_a
        d = np.linalg.norm(comm)
        max_comm_dev = max(max_comm_dev, d)
        print(f"  ||[T_{label_a}, T_{label_b}]|| = {d:.3e}")
    t3_ok = max_comm_dev < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: inverse T_{-a} = T_a^† -----
    print("-" * 72)
    print("TEST 4: T_{-a} = T_a^†  (inverse equals adjoint, T_a unitary)")
    print("-" * 72)
    max_inv_dev = 0.0
    for a in [e1, e2, e3, (2, 1, 0), (3, 2, 1)]:
        T_a = build_translation_3d(L, a)
        T_minus_a = build_translation_3d(L, tuple((-a[i]) % L for i in range(3)))
        d_dag = np.linalg.norm(T_minus_a - T_a.conj().T)
        d_inv = np.linalg.norm(T_a @ T_minus_a - Iden)
        max_inv_dev = max(max_inv_dev, d_dag, d_inv)
        print(f"  a={a}: ||T_{{-a}} - T_a†|| = {d_dag:.3e}, ||T_a T_{{-a}} - I|| = {d_inv:.3e}")
    t4_ok = max_inv_dev < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: T_e1^L = I (cyclic order L on each axis) -----
    print("-" * 72)
    print(f"TEST 5: T_e_i^{L} = I  (each axial generator has order L = {L})")
    print("-" * 72)
    max_order_dev = 0.0
    for ei, label in [(e1, "e_1"), (e2, "e_2"), (e3, "e_3")]:
        T_ei = build_translation_3d(L, ei)
        T_ei_L = np.linalg.matrix_power(T_ei, L)
        d = np.linalg.norm(T_ei_L - Iden)
        max_order_dev = max(max_order_dev, d)
        print(f"  ||T_{label}^{L} - I|| = {d:.3e}")
    t5_ok = max_order_dev < 1e-12
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: total group order = L^3 (full translation group is (Z/L)^3) -----
    print("-" * 72)
    print(f"TEST 6: total translation group has order L^3 = {L ** 3}")
    print("        (count distinct T_a as a ranges over (Z/L)^3)")
    print("-" * 72)
    seen = set()
    for a in itertools.product(range(L), repeat=3):
        T_a = build_translation_3d(L, a)
        # Use a canonical hash via the matrix (rounded)
        key = tuple(np.round(T_a.real.flatten(), 6).tolist())
        seen.add(key)
    distinct_count = len(seen)
    print(f"  distinct translations: {distinct_count}")
    print(f"  expected: {L ** 3}")
    t6_ok = distinct_count == L ** 3
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: structure constants — homomorphism Z^3 → U(dim) is faithful -----
    print("-" * 72)
    print("TEST 7: T : (Z/L)^3 → U(dim) is a faithful group homomorphism")
    print("        (kernel is trivial: T_a = I  ⇒  a = 0)")
    print("-" * 72)
    # Faithfulness: only T_a equal to I is T_0
    n_kernel = 0
    for a in itertools.product(range(L), repeat=3):
        T_a = build_translation_3d(L, a)
        if np.linalg.norm(T_a - Iden) < 1e-12:
            n_kernel += 1
    print(f"  |kernel| = {n_kernel} (should be 1, the identity)")
    t7_ok = n_kernel == 1
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (T_0 = I):                                 {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (closure T_a T_b = T_{{a+b}}):              {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 ([T_a, T_b] = 0 — abelian):                 {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (T_{{-a}} = T_a† — unitary inverse):        {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (T_e_i^L = I — cyclic order):               {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (group order = L^3):                       {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (faithful homomorphism):                   {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
