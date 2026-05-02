"""SU(3) symmetric structure constants d^{abc} from {T^a, T^b}.

By cl3_color_automorphism_theorem (retained), Gell-Mann generators T^a = λ^a/2
satisfy Tr[T^a T^b] = (1/2) δ^{ab}. The anticommutator decomposes as

    {T^a, T^b}  =  T^a T^b + T^b T^a  =  (1/3) δ^{ab} I_3  +  d^{abc} T^c

with d^{abc} the **symmetric structure constants** (companion to the
antisymmetric f^{abc} from the commutator).

Properties:
  (D1) d^{abc} is real and totally symmetric in (a, b, c)
  (D2) d^{abc} = 2 Tr[{T^a, T^b} T^c]
  (D3) Some d^{abc} are zero (selection rule ε(a)·ε(b)·ε(c) symmetry)
  (D4) Specific nonzero values match the standard SU(3) reference values

Tests:
  (T1) Anticommutator decomposition {T^a, T^b} = (1/3) δ^{ab} I + d^{abc} T^c
  (T2) d^{abc} totally symmetric (a, b, c)
  (T3) d^{abc} real
  (T4) Specific reference values d^{118}, d^{146}, etc. match standard table
  (T5) Combined identity: T^a T^b = (1/2)(δ^{ab}/3 · I + (d^{abc} + i f^{abc}) T^c)
  (T6) Independence of d from f: f^{abc} is anti-symmetric and d^{abc} is
       symmetric — they live in orthogonal tensor decomposition
"""
from __future__ import annotations

import numpy as np


def gell_mann_matrices() -> list[np.ndarray]:
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


def main() -> None:
    print("=" * 72)
    print("SU(3) SYMMETRIC STRUCTURE CONSTANTS d^{abc}")
    print("=" * 72)
    print()

    lambdas = gell_mann_matrices()
    T = [L / 2 for L in lambdas]
    I3 = np.eye(3, dtype=complex)

    # Compute d^{abc} via projection: d^{abc} = 2 Tr[{T^a, T^b} T^c]
    d = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            anti = T[a] @ T[b] + T[b] @ T[a]
            for c in range(8):
                d[a, b, c] = (2 * np.trace(anti @ T[c])).real

    # ----- Test 1: anticommutator decomposition -----
    print("-" * 72)
    print("TEST 1: {T^a, T^b} = (1/3) δ^{ab} I_3 + d^{abc} T^c")
    print("-" * 72)
    max_dec_dev = 0.0
    for a in range(8):
        for b in range(8):
            anti = T[a] @ T[b] + T[b] @ T[a]
            target = (1.0 if a == b else 0.0) * (1.0 / 3.0) * I3 + sum(
                d[a, b, c] * T[c] for c in range(8)
            )
            dev = np.linalg.norm(anti - target)
            max_dec_dev = max(max_dec_dev, dev)
    print(f"  max ||{{T^a, T^b}} - ((1/3) δ^{{ab}} I + d^{{abc}} T^c)|| = {max_dec_dev:.3e}")
    t1_ok = max_dec_dev < 1e-10
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: d^{abc} totally symmetric -----
    print("-" * 72)
    print("TEST 2: d^{abc} totally symmetric in (a, b, c)")
    print("-" * 72)
    max_sym_dev = 0.0
    for a in range(8):
        for b in range(8):
            for c in range(8):
                # Check all 5 swaps
                for perm in [(b, a, c), (a, c, b), (c, b, a), (c, a, b), (b, c, a)]:
                    pa, pb, pc = perm
                    dev = abs(d[a, b, c] - d[pa, pb, pc])
                    max_sym_dev = max(max_sym_dev, dev)
    print(f"  max |d^{{abc}} - d^{{permuted}}| = {max_sym_dev:.3e}")
    t2_ok = max_sym_dev < 1e-10
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: d^{abc} real -----
    print("-" * 72)
    print("TEST 3: d^{abc} all real")
    print("-" * 72)
    # Already real-valued by construction; verify by re-projecting with complex
    d_complex = np.zeros((8, 8, 8), dtype=complex)
    for a in range(8):
        for b in range(8):
            anti = T[a] @ T[b] + T[b] @ T[a]
            for c in range(8):
                d_complex[a, b, c] = 2 * np.trace(anti @ T[c])
    max_imag = np.max(np.abs(d_complex.imag))
    print(f"  max |Im d^{{abc}}| = {max_imag:.3e}")
    t3_ok = max_imag < 1e-10
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: Reference values from standard SU(3) table -----
    print("-" * 72)
    print("TEST 4: Specific reference values match standard SU(3) table")
    print("-" * 72)
    # Standard SU(3) d^{abc} reference (1-indexed):
    # d^{118} = d^{228} = d^{338} = 1/√3
    # d^{146} = d^{157} = -d^{247} = d^{256} = 1/2
    # d^{344} = d^{355} = -d^{366} = -d^{377} = 1/2
    # d^{448} = d^{558} = d^{668} = d^{778} = -1/(2√3)
    # d^{888} = -1/√3
    inv_sqrt3 = 1.0 / np.sqrt(3.0)
    reference = {
        (0, 0, 7): inv_sqrt3,        # d^{118}
        (1, 1, 7): inv_sqrt3,        # d^{228}
        (2, 2, 7): inv_sqrt3,        # d^{338}
        (0, 3, 5): 0.5,              # d^{146}
        (0, 4, 6): 0.5,              # d^{157}
        (1, 3, 6): -0.5,             # d^{247}
        (1, 4, 5): 0.5,              # d^{256}
        (2, 3, 3): 0.5,              # d^{344}
        (2, 4, 4): 0.5,              # d^{355}
        (2, 5, 5): -0.5,             # d^{366}
        (2, 6, 6): -0.5,             # d^{377}
        (3, 3, 7): -0.5 * inv_sqrt3, # d^{448}
        (4, 4, 7): -0.5 * inv_sqrt3, # d^{558}
        (5, 5, 7): -0.5 * inv_sqrt3, # d^{668}
        (6, 6, 7): -0.5 * inv_sqrt3, # d^{778}
        (7, 7, 7): -inv_sqrt3,       # d^{888}
    }
    max_ref_dev = 0.0
    matched = 0
    for (a, b, c), expected in reference.items():
        observed = d[a, b, c]
        dev = abs(observed - expected)
        max_ref_dev = max(max_ref_dev, dev)
        if dev < 1e-10:
            matched += 1
    print(f"  reference values matched: {matched}/{len(reference)}")
    print(f"  max |observed - reference| = {max_ref_dev:.3e}")
    t4_ok = max_ref_dev < 1e-10
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Combined identity T^a T^b = ... -----
    print("-" * 72)
    print("TEST 5: T^a T^b = (1/6) δ^{ab} I + (1/2)(d^{abc} + i f^{abc}) T^c")
    print("-" * 72)
    # Compute f^{abc}
    f = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            comm = T[a] @ T[b] - T[b] @ T[a]
            for c in range(8):
                f[a, b, c] = (-2j * np.trace(comm @ T[c])).real
    max_id_dev = 0.0
    for a in range(8):
        for b in range(8):
            prod = T[a] @ T[b]
            target = (1.0 if a == b else 0.0) * (1.0 / 6.0) * I3 + sum(
                0.5 * (d[a, b, c] + 1j * f[a, b, c]) * T[c] for c in range(8)
            )
            dev = np.linalg.norm(prod - target)
            max_id_dev = max(max_id_dev, dev)
    print(f"  max ||T^a T^b - ((1/6) δ^{{ab}} I + (1/2)(d + if) T^c)|| = {max_id_dev:.3e}")
    t5_ok = max_id_dev < 1e-10
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: f anti-symmetric, d symmetric (orthogonal decomposition) -----
    print("-" * 72)
    print("TEST 6: f^{abc} antisymmetric in (a, b); d^{abc} symmetric in (a, b)")
    print("-" * 72)
    max_f_anti = 0.0
    max_d_sym = 0.0
    for a in range(8):
        for b in range(8):
            for c in range(8):
                max_f_anti = max(max_f_anti, abs(f[a, b, c] + f[b, a, c]))
                max_d_sym = max(max_d_sym, abs(d[a, b, c] - d[b, a, c]))
    print(f"  max |f^{{abc}} + f^{{bac}}| = {max_f_anti:.3e}  (should be 0)")
    print(f"  max |d^{{abc}} - d^{{bac}}| = {max_d_sym:.3e}  (should be 0)")
    t6_ok = max_f_anti < 1e-10 and max_d_sym < 1e-10
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 ({{T^a, T^b}} decomposition):              {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (d^{{abc}} totally symmetric):              {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (d^{{abc}} real):                           {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (reference values match):                  {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (combined T^a T^b identity):               {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (f anti-sym, d sym in (a,b)):              {'PASS' if t6_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
