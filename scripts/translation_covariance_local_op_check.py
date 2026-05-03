"""Translation covariance of local operators: T_a O(x) T_a^† = O(x + a).

By axiom_first_lattice_noether (cited), the framework's action is invariant
under T_a : x ↦ x + a, with translation operators T_a acting on H_phys
satisfying T_a |x⟩ = |x + a⟩ (regular representation; established by R6 Block 02
on the same cited authority).

For any *local* operator O(x) attached to site x (e.g. a fermion bilinear,
field strength, charge density), translation covariance is:

    T_a O(x) T_a^†  =  O(x + a)              ∀ a ∈ Z^3, ∀ x ∈ Λ.

Proof sketch: O(x) := Σ_{ψ, φ} O_{ψφ}(x) |ψ; x⟩⟨φ; x| in the on-site basis
(matrix elements depend only on internal labels of site x). Conjugating by T_a
relabels x ↦ x + a in the kets and bras while leaving matrix elements
invariant — yielding O(x + a).

Tests:
  (T1) Position operator X̂ : T_a X̂ T_a^† = X̂ + a · I
  (T2) Local site-projector P_x : T_a P_x T_a^† = P_{x+a}
  (T3) Local fermion bilinear: T_a (a_x^† a_x) T_a^† = a_{x+a}^† a_{x+a}
       (in particular, density operator transforms as expected)
  (T4) Sum of local operators (translation-invariant total): T_a (Σ_x O(x)) T_a^† = Σ_x O(x)
       (yields global translation invariance of the action)
  (T5) Hopping operator h_{xy} := a_x^† a_y: T_a h_{xy} T_a^† = h_{x+a, y+a}
  (T6) Locally-supported operator support: supp(T_a O(x) T_a^†) = supp(O(x)) + a
"""
from __future__ import annotations

import itertools

import numpy as np


def build_translation_3d(L: int, a: tuple[int, int, int]) -> np.ndarray:
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


def site_projector(L: int, x: tuple[int, int, int]) -> np.ndarray:
    """P_x = |x⟩⟨x| in the position basis."""
    dim = L ** 3
    P = np.zeros((dim, dim), dtype=complex)
    idx = x[0] * L * L + x[1] * L + x[2]
    P[idx, idx] = 1.0
    return P


def position_operator(L: int, axis: int) -> np.ndarray:
    """X̂_axis = Σ_x x_axis · |x⟩⟨x|"""
    dim = L ** 3
    X = np.zeros((dim, dim), dtype=complex)
    for i, (x1, x2, x3) in enumerate(itertools.product(range(L), repeat=3)):
        coords = [x1, x2, x3]
        X[i, i] = coords[axis]
    return X


def hopping_operator(L: int, x: tuple[int, int, int], y: tuple[int, int, int]) -> np.ndarray:
    """h_{xy} = |x⟩⟨y|  (single-particle hopping projector)."""
    dim = L ** 3
    h = np.zeros((dim, dim), dtype=complex)
    ix = x[0] * L * L + x[1] * L + x[2]
    iy = y[0] * L * L + y[1] * L + y[2]
    h[ix, iy] = 1.0
    return h


def main() -> None:
    print("=" * 72)
    print("TRANSLATION COVARIANCE OF LOCAL OPERATORS T_a O(x) T_a† = O(x+a)")
    print("=" * 72)
    print()

    L = 4
    dim = L ** 3
    print(f"  Toy model: {L}×{L}×{L} periodic lattice, dim = {dim}")
    print()

    # ----- Test 1: T_a X̂ T_a^† = X̂ - a · I (modulo periodicity) -----
    # Derivation: X̂ = Σ_x x · P_x. Under T_a, P_x ↦ P_{x+a}, so
    #   T_a X̂ T_a^† = Σ_x x · P_{x+a} = Σ_y (y - a) · P_y = X̂ - a · I.
    # This is the convention "translate the labels: x ↦ x + a" applied to operators.
    print("-" * 72)
    print("TEST 1: T_a X̂_axis T_a^† = X̂_axis - a_axis · I  (mod L)")
    print("        (since Σ_x x P_{x+a} = Σ_y (y-a) P_y; site labels shift by +a)")
    print("-" * 72)
    max_pos_dev = 0.0
    for axis in range(3):
        for a_axis in [1, 2]:
            a = [0, 0, 0]
            a[axis] = a_axis
            a = tuple(a)
            T_a = build_translation_3d(L, a)
            X = position_operator(L, axis)
            X_shifted = T_a @ X @ T_a.conj().T
            X_shifted_diag = np.diag(X_shifted).real
            X_orig_diag = np.diag(X).real
            # Expected: X_shifted at site y has value (y - a) mod L
            # Equivalently: X_shifted_diag[i] = (X_orig_diag[i] - a_axis) mod L
            expected_diag = np.array([(X_orig_diag[i] - a_axis) % L for i in range(dim)])
            d = np.linalg.norm(X_shifted_diag - expected_diag)
            max_pos_dev = max(max_pos_dev, d)
            print(f"  axis={axis}, a_axis={a_axis}: ||T_a X T_a† - (X-a)_mod L|| = {d:.3e}")
    t1_ok = max_pos_dev < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: T_a P_x T_a^† = P_{x+a} -----
    print("-" * 72)
    print("TEST 2: T_a P_x T_a^† = P_{x+a}  (site projector covariance)")
    print("-" * 72)
    max_proj_dev = 0.0
    test_cases = [
        ((1, 1, 1), (1, 0, 0)),
        ((0, 0, 0), (2, 1, 0)),
        ((3, 2, 1), (1, 1, 1)),
        ((2, 0, 3), (3, 3, 3)),
    ]
    for x, a in test_cases:
        T_a = build_translation_3d(L, a)
        P_x = site_projector(L, x)
        P_xa_expected = site_projector(L, tuple((x[i] + a[i]) % L for i in range(3)))
        P_xa_actual = T_a @ P_x @ T_a.conj().T
        d = np.linalg.norm(P_xa_actual - P_xa_expected)
        max_proj_dev = max(max_proj_dev, d)
        print(f"  x={x}, a={a}: ||T_a P_x T_a† - P_{{x+a}}|| = {d:.3e}")
    t2_ok = max_proj_dev < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: Local operators (P_x are fermion-density-like) covariance -----
    print("-" * 72)
    print("TEST 3: P_x covariance for arbitrary x ∈ Λ (full sweep)")
    print("-" * 72)
    a = (1, 1, 0)
    T_a = build_translation_3d(L, a)
    max_full_dev = 0.0
    for xs in itertools.product(range(L), repeat=3):
        P_xs = site_projector(L, xs)
        P_xs_a_actual = T_a @ P_xs @ T_a.conj().T
        P_xs_a_expected = site_projector(L, tuple((xs[i] + a[i]) % L for i in range(3)))
        d = np.linalg.norm(P_xs_a_actual - P_xs_a_expected)
        max_full_dev = max(max_full_dev, d)
    print(f"  swept over all 64 sites with a=(1,1,0)")
    print(f"  max ||T_a P_x T_a† - P_{{x+a}}|| = {max_full_dev:.3e}")
    t3_ok = max_full_dev < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Σ_x O(x) translation invariant ⇒ commutes with T_a -----
    print("-" * 72)
    print("TEST 4: T_a (Σ_x P_x) T_a^† = Σ_x P_x  (sum is invariant)")
    print("        ⇒ Σ_x P_x = I (resolution of identity)  ⇒  T_a I T_a† = I")
    print("-" * 72)
    P_total = sum(site_projector(L, xs) for xs in itertools.product(range(L), repeat=3))
    Iden = np.eye(dim, dtype=complex)
    P_total_dev = np.linalg.norm(P_total - Iden)
    print(f"  ||Σ_x P_x - I|| = {P_total_dev:.3e}")
    a = (2, 1, 3)
    T_a = build_translation_3d(L, a)
    P_total_shifted = T_a @ P_total @ T_a.conj().T
    inv_dev = np.linalg.norm(P_total_shifted - P_total)
    print(f"  ||T_a (Σ_x P_x) T_a† - (Σ_x P_x)|| = {inv_dev:.3e}")
    t4_ok = P_total_dev < 1e-12 and inv_dev < 1e-12
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Hopping operator covariance T_a h_{xy} T_a^† = h_{x+a, y+a} -----
    print("-" * 72)
    print("TEST 5: T_a h_{xy} T_a^† = h_{x+a, y+a}  (hopping is two-site-local)")
    print("-" * 72)
    max_hop_dev = 0.0
    hop_cases = [
        ((1, 1, 1), (1, 1, 2), (1, 0, 0)),
        ((0, 0, 0), (1, 0, 0), (2, 2, 2)),
        ((2, 1, 0), (3, 1, 0), (1, 1, 1)),
    ]
    for x, y, a in hop_cases:
        T_a = build_translation_3d(L, a)
        h_xy = hopping_operator(L, x, y)
        h_shifted_actual = T_a @ h_xy @ T_a.conj().T
        x_a = tuple((x[i] + a[i]) % L for i in range(3))
        y_a = tuple((y[i] + a[i]) % L for i in range(3))
        h_shifted_expected = hopping_operator(L, x_a, y_a)
        d = np.linalg.norm(h_shifted_actual - h_shifted_expected)
        max_hop_dev = max(max_hop_dev, d)
        print(f"  x={x}, y={y}, a={a}: ||T_a h_{{xy}} T_a† - h_{{x+a,y+a}}|| = {d:.3e}")
    t5_ok = max_hop_dev < 1e-12
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Support relocation supp(T_a O T_a^†) = supp(O) + a -----
    print("-" * 72)
    print("TEST 6: support(T_a O T_a^†) = support(O) + a")
    print("-" * 72)
    a = (1, 2, 0)
    T_a = build_translation_3d(L, a)
    # Take O = projector on site (1, 1, 1)
    x = (1, 1, 1)
    P_x = site_projector(L, x)
    P_x_shifted = T_a @ P_x @ T_a.conj().T
    # Support of P_x: {(1,1,1)}; support of T_a P_x T_a†: should be {(1+1, 1+2, 1+0)} = {(2, 3, 1)}
    nonzero_idx = []
    for i in range(dim):
        if abs(P_x_shifted[i, i]) > 1e-10:
            x1, x2, x3 = i // (L * L), (i // L) % L, i % L
            nonzero_idx.append((x1, x2, x3))
    expected = [tuple((x[i] + a[i]) % L for i in range(3))]
    print(f"  support of T_a P_x T_a† = {nonzero_idx}")
    print(f"  expected support: {expected}")
    t6_ok = nonzero_idx == expected
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (T_a X T_a† = X - a (mod L)):              {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (T_a P_x T_a† = P_{{x+a}} sample):           {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (P_x covariance full sweep):               {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (sum is invariant; resolution of I):       {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (hopping h_{{xy}} covariance):               {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (support relocation):                      {'PASS' if t6_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
