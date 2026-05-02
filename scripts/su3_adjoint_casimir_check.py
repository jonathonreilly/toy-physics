"""SU(3) quadratic Casimir on the adjoint = N = 3.

By cl3_color_automorphism_theorem (retained), SU(3)_c acts on the framework's
3-dim symmetric base subspace via the canonical Gell-Mann generators
T^a = λ^a / 2 satisfying Tr[T^a T^b] = (1/2) δ^{ab} (fundamental "3").

The adjoint representation is the action of su(3) on itself by commutator:
    (T^a_adj)_{bc} := -i f^{abc}
which is an 8-dim Hermitian rep on the Lie algebra.

The quadratic Casimir on the adjoint is
    C_2(adj) := Σ_a (T^a_adj)² = N · I_8 = 3 · I_8
in the same Tr[T^a T^b] = (1/2) δ^{ab} normalization. This is the "color
charge squared" of a gluon, the structural counterpart of C_2(3) = 4/3
for quarks.

Tests:
  (T1) Adjoint generators (T^a_adj)_{bc} := -i f^{abc} are Hermitian (8x8)
  (T2) Adjoint generators close under su(3) Lie algebra: [T^a_adj, T^b_adj] = i f^{abc} T^c_adj
  (T3) Trace normalization: Tr[T^a_adj T^b_adj] = N · δ^{ab} = 3 δ^{ab}
  (T4) Casimir C_2(adj) = Σ_a T^a_adj T^a_adj is proportional to identity
  (T5) C_2(adj) eigenvalue = N = 3 exactly
  (T6) Trace argument: Tr[C_2(adj)] = 8 · 3 = 24 ⇒ C_2 = 3
"""
from __future__ import annotations

import numpy as np


def gell_mann_matrices() -> list[np.ndarray]:
    """The 8 Gell-Mann matrices λ^1, ..., λ^8 (Hermitian, 3x3)."""
    L1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    L2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    L3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    L4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    L5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    L6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    L7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    L8 = (1 / np.sqrt(3)) * np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex
    )
    return [L1, L2, L3, L4, L5, L6, L7, L8]


def compute_structure_constants(T: list[np.ndarray]) -> np.ndarray:
    """Compute f^{abc} from [T^a, T^b] = i f^{abc} T^c via trace formula."""
    f = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            comm = T[a] @ T[b] - T[b] @ T[a]
            for c in range(8):
                # f^{abc} = -2i Tr[[T^a, T^b] T^c]
                f[a, b, c] = (-2j * np.trace(comm @ T[c])).real
    return f


def main() -> None:
    print("=" * 72)
    print("SU(3) ADJOINT CASIMIR C_2(8) = N = 3")
    print("=" * 72)
    print()

    lambdas = gell_mann_matrices()
    T = [L / 2 for L in lambdas]
    I8 = np.eye(8, dtype=complex)

    # Compute structure constants
    f = compute_structure_constants(T)
    print(f"  Computed structure constants f^{{abc}}; max nonzero = {np.max(np.abs(f)):.4f}")
    print()

    # Build adjoint generators: (T^a_adj)_{bc} = -i f^{abc}
    T_adj = [np.zeros((8, 8), dtype=complex) for _ in range(8)]
    for a in range(8):
        for b in range(8):
            for c in range(8):
                T_adj[a][b, c] = -1j * f[a, b, c]

    # ----- Test 1: T^a_adj are Hermitian (since f^{abc} is real and totally antisymmetric) -----
    print("-" * 72)
    print("TEST 1: T^a_adj are Hermitian 8x8 matrices")
    print("-" * 72)
    max_herm = 0.0
    for a in range(8):
        d = np.linalg.norm(T_adj[a] - T_adj[a].conj().T)
        max_herm = max(max_herm, d)
    print(f"  max ||T^a_adj - (T^a_adj)†|| = {max_herm:.3e}")
    t1_ok = max_herm < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: [T^a_adj, T^b_adj] = i f^{abc} T^c_adj (su(3) closure) -----
    print("-" * 72)
    print("TEST 2: su(3) Lie algebra closure on adjoint:")
    print("        [T^a_adj, T^b_adj] = i f^{abc} T^c_adj")
    print("-" * 72)
    max_close = 0.0
    for a in range(8):
        for b in range(8):
            comm = T_adj[a] @ T_adj[b] - T_adj[b] @ T_adj[a]
            target = sum(1j * f[a, b, c] * T_adj[c] for c in range(8))
            d = np.linalg.norm(comm - target)
            max_close = max(max_close, d)
    print(f"  max ||[T^a_adj, T^b_adj] - i f^{{abc}} T^c_adj|| = {max_close:.3e}")
    t2_ok = max_close < 1e-10
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: Trace normalization Tr[T^a_adj T^b_adj] = N δ^{ab} = 3 δ^{ab} -----
    print("-" * 72)
    print("TEST 3: Tr[T^a_adj T^b_adj] = N δ^{ab} = 3 δ^{ab}")
    print("-" * 72)
    max_trace = 0.0
    N_color = 3
    for a in range(8):
        for b in range(8):
            tr = np.trace(T_adj[a] @ T_adj[b]).real
            target = N_color if a == b else 0.0
            d = abs(tr - target)
            max_trace = max(max_trace, d)
    print(f"  max |Tr[T^a_adj T^b_adj] - N δ^{{ab}}| = {max_trace:.3e}")
    t3_ok = max_trace < 1e-10
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: C_2(adj) = Σ T^a_adj T^a_adj is proportional to I_8 -----
    print("-" * 72)
    print("TEST 4: C_2(adj) := Σ_a T^a_adj T^a_adj is proportional to I_8")
    print("-" * 72)
    C2_adj = sum(Ta @ Ta for Ta in T_adj)
    # Check Schur (proportional to identity)
    eigs = np.linalg.eigvalsh(0.5 * (C2_adj + C2_adj.conj().T))
    eigs_real = sorted(eigs.tolist())
    print(f"  C_2(adj) eigenvalues (8 of): {eigs_real[:4]}, ..., {eigs_real[-1]}")
    spread = max(eigs_real) - min(eigs_real)
    print(f"  spread (max - min) = {spread:.3e}")
    t4_ok = spread < 1e-10
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: C_2(adj) value = N = 3 -----
    print("-" * 72)
    print("TEST 5: C_2(adj) eigenvalue = N = 3 exactly")
    print("-" * 72)
    c2_value = eigs_real[0]
    target = float(N_color)
    dev = abs(c2_value - target)
    print(f"  C_2(adj) = {c2_value} (expected {target})")
    print(f"  |C_2(adj) - 3| = {dev:.3e}")
    t5_ok = dev < 1e-10
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Trace argument Tr[C_2(adj)] = 8 · 3 = 24 ⇒ C_2 = 3 -----
    print("-" * 72)
    print("TEST 6: Trace argument: Tr[C_2(adj)] = 24 ⇒ C_2(adj) = 3")
    print("-" * 72)
    tr_C2 = np.trace(C2_adj).real
    expected_tr = 8 * 3.0  # dim(adj) × C_2(adj)
    print(f"  Tr[C_2(adj)] = {tr_C2}")
    print(f"  expected (8 × 3) = {expected_tr}")
    t6_ok = abs(tr_C2 - expected_tr) < 1e-10
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Companion check — fundamental Casimir C_2(3) = 4/3 ≠ adjoint -----
    print("-" * 72)
    print("TEST 7: Verify fundamental and adjoint Casimirs differ:")
    print("        C_2(3) = 4/3 ≠ C_2(8) = 3, with C_2(8) = N · C_2(3) = ?")
    print("-" * 72)
    # In standard normalization: C_2(N) = (N²-1)/(2N) for fundamental
    # C_2(adj) = N for adjoint
    # Ratio C_2(adj) / C_2(fund) = N / [(N²-1)/(2N)] = 2N²/(N²-1) = 18/8 = 9/4 for N=3
    ratio = c2_value / (4 / 3)
    expected_ratio = 9 / 4
    print(f"  C_2(adj) / C_2(fund) = {ratio} (expected 9/4 = {expected_ratio})")
    print(f"  also: C_2(adj) - C_2(fund) = {c2_value - 4/3}")
    t7_ok = abs(ratio - expected_ratio) < 1e-10
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (T^a_adj Hermitian):                       {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (su(3) closure on adjoint):                {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (Tr[T^a_adj T^b_adj] = N δ^{{ab}}):         {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (C_2(adj) ∝ I_8, Schur):                   {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (C_2(adj) = 3 numerically):                {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (Tr[C_2(adj)] = 24 trace argument):        {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (ratio C_2(adj)/C_2(fund) = 9/4):          {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
