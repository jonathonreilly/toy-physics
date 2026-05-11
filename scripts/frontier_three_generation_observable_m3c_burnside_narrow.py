#!/usr/bin/env python3
"""Verify the M_3(C) Burnside narrow theorem at exact symbolic precision.

The narrow theorem note
`THREE_GENERATION_OBSERVABLE_M3C_BURNSIDE_NARROW_THEOREM_NOTE_2026-05-10.md`
states a purely abstract finite-dimensional matrix-algebra theorem on
C^3:

  - C is the cyclic permutation matrix sending e_1 -> e_2 -> e_3 -> e_1;
  - T_1 = diag(-1, +1, +1), T_2 = diag(+1, -1, +1), T_3 = diag(+1, +1, -1)
    are three commuting Z_2 reflections with distinct joint sign triples;
  - P_i = product of three Z_2 projectors selecting the (-1, +1, +1)-,
    (+1, -1, +1)-, (+1, +1, -1)- sign triples respectively;
  - E_ij = P_i C^{(i-j) mod 3} P_j gives every matrix unit;
  - the algebra <C, T_1, T_2, T_3>_alg = M_3(C);
  - no proper nonzero subspace is invariant under all four generators.

This runner exhibits each conclusion symbolically (exact rationals /
complex roots of unity via sympy) and verifies the Burnside hypotheses.
"""

from __future__ import annotations

import sympy as sp
from sympy import Matrix, eye, zeros, I, exp, pi, sqrt, Rational, simplify


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    print("Three-Generation Observable M_3(C) Burnside narrow theorem check")
    print()

    # ------------------------------------------------------------------
    # Setup: C, T_1, T_2, T_3 on C^3
    # ------------------------------------------------------------------
    C = Matrix([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ])
    T = [
        sp.diag(-1, 1, 1),
        sp.diag(1, -1, 1),
        sp.diag(1, 1, -1),
    ]
    e = [
        Matrix([1, 0, 0]),
        Matrix([0, 1, 0]),
        Matrix([0, 0, 1]),
    ]

    # ------------------------------------------------------------------
    # T1 / step 1-3: orders, involutions, commutativity
    # ------------------------------------------------------------------
    check("(1) C^3 = I_3", (C ** 3) == eye(3))
    for i in range(3):
        check(f"(2) T_{i + 1}^2 = I_3", (T[i] ** 2) == eye(3))
    for i in range(3):
        for j in range(i + 1, 3):
            comm = T[i] * T[j] - T[j] * T[i]
            check(
                f"(3) [T_{i + 1}, T_{j + 1}] = 0",
                comm.is_zero_matrix,
            )

    # Pairwise commutativity of C with T_i — NOT required by the
    # theorem (the theorem does not assert it; in fact C T_i != T_i C
    # in general). We do not check this; we only check the algebra
    # generated, not its abelian-ness.

    # ------------------------------------------------------------------
    # T1 / step 4: P_i are rank-1 orthogonal projectors with P_i e_j = δ_{ij} e_i
    # ------------------------------------------------------------------
    proj_plus = [(eye(3) + T[i]) / 2 for i in range(3)]
    proj_minus = [(eye(3) - T[i]) / 2 for i in range(3)]

    P = [
        proj_minus[0] * proj_plus[1] * proj_plus[2],
        proj_plus[0] * proj_minus[1] * proj_plus[2],
        proj_plus[0] * proj_plus[1] * proj_minus[2],
    ]

    for i in range(3):
        check(f"(4a) P_{i + 1}^2 = P_{i + 1}", sp.simplify(P[i] * P[i] - P[i]).is_zero_matrix)
        check(f"(4b) P_{i + 1} = P_{i + 1}^dagger", sp.simplify(P[i] - P[i].H).is_zero_matrix)
        check(f"(4c) rank(P_{i + 1}) = 1", P[i].rank() == 1)

    for i in range(3):
        for j in range(3):
            actual = P[i] * e[j]
            expected = e[i] if i == j else zeros(3, 1)
            check(
                f"(4d) P_{i + 1} e_{j + 1} = δ_{{{i + 1}{j + 1}}} e_{i + 1}",
                sp.simplify(actual - expected).is_zero_matrix,
            )

    # Pairwise orthogonality of projectors
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            prod = P[i] * P[j]
            check(
                f"(4e) P_{i + 1} P_{j + 1} = 0 (i != j)",
                sp.simplify(prod).is_zero_matrix,
            )

    # Resolution of identity
    sum_P = P[0] + P[1] + P[2]
    check("(4f) P_1 + P_2 + P_3 = I_3", sp.simplify(sum_P - eye(3)).is_zero_matrix)

    # ------------------------------------------------------------------
    # T2 / step 5: matrix-unit formula E_ij = P_i C^{(i-j) mod 3} P_j
    # ------------------------------------------------------------------
    def matrix_unit(i, j):
        # 1-indexed (i, j) ∈ {1, 2, 3}^2
        k = (i - j) % 3
        return P[i - 1] * C ** k * P[j - 1]

    def expected_E(i, j):
        # 1-indexed
        E = zeros(3, 3)
        E[i - 1, j - 1] = 1
        return E

    for i in range(1, 4):
        for j in range(1, 4):
            E_actual = matrix_unit(i, j)
            E_exp = expected_E(i, j)
            check(
                f"(5) E_{i}{j} = P_{i} C^{(i - j) % 3} P_{j}",
                sp.simplify(E_actual - E_exp).is_zero_matrix,
            )

    # ------------------------------------------------------------------
    # T3 / step 6: 9 matrix units span all of M_3(C); rank-9 check
    # ------------------------------------------------------------------
    units = []
    for i in range(1, 4):
        for j in range(1, 4):
            E = matrix_unit(i, j)
            # Flatten 3x3 -> 9-vector for rank check
            flat = list(E)
            units.append(flat)
    spanning_matrix = Matrix(units)
    check(
        "(6) generated matrix units span M_3(C) (rank 9)",
        spanning_matrix.rank() == 9,
        f"rank={spanning_matrix.rank()}",
    )

    # ------------------------------------------------------------------
    # T4 / step 7: irreducibility — no proper invariant subspace
    # ------------------------------------------------------------------
    # Test 1: enumerate all 1-dim subspaces with components in {-1, 0, 1}
    # and check whether any is invariant under all four generators.
    # By T2-induction: an invariant subspace is invariant under E_ij,
    # so it is invariant under M_3(C), hence equals C^3 or {0}.
    invariants_1d = []
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                v = Matrix([a, b, c])
                if v.norm() == 0:
                    continue
                ok = True
                for A in [T[0], T[1], T[2], C]:
                    Av = A * v
                    # Check Av is a scalar multiple of v
                    # Find first nonzero index k of v
                    k = next(idx for idx in range(3) if v[idx] != 0)
                    lam = Rational(int(Av[k]), int(v[k]))
                    if (Av - lam * v).norm() != 0:
                        ok = False
                        break
                if ok:
                    invariants_1d.append((a, b, c))
    check(
        "(7a) no integer-triple 1-dim invariant subspace under {C, T_1, T_2, T_3}",
        not invariants_1d,
        f"invariants={invariants_1d}",
    )

    # Test 2: T_i-only invariance of a 1-dim subspace forces the
    # vector to be a coordinate axis (or zero). The 6 axis vectors
    # (±e_1, ±e_2, ±e_3) are joint T_i-eigenvectors but they are NOT
    # C-invariant individually (C cycles them). Verify both halves:
    # (i) joint T_i-invariant 1-dim subspaces are exactly the
    # coordinate axis lines; (ii) none of those is C-invariant.
    t_invariant_axes = []
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if (a, b, c) == (0, 0, 0):
                    continue
                t1_ok = (a == 0) or (b == 0 and c == 0)
                t2_ok = (b == 0) or (a == 0 and c == 0)
                t3_ok = (c == 0) or (a == 0 and b == 0)
                if t1_ok and t2_ok and t3_ok:
                    t_invariant_axes.append((a, b, c))
    # The 6 unit axes (±e_1, ±e_2, ±e_3) are exactly these
    expected_axes = {
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    }
    check(
        "(7b-i) T_i-invariant integer-triple 1-dim subspaces = coordinate axes",
        set(t_invariant_axes) == expected_axes,
        f"actual={sorted(t_invariant_axes)}",
    )

    # Now check none of these 6 axis 1-dim subspaces is also C-invariant.
    c_breakage = []
    for (a, b, c) in t_invariant_axes:
        v = Matrix([a, b, c])
        Cv = C * v
        # Is Cv parallel to v? Find the first nonzero index of v
        k = next(idx for idx in range(3) if v[idx] != 0)
        lam = Rational(int(Cv[k]), int(v[k])) if v[k] != 0 else None
        if lam is None or (Cv - lam * v).norm() != 0:
            c_breakage.append((a, b, c))
    check(
        "(7b-ii) no T_i-invariant axis 1-dim subspace is C-invariant",
        len(c_breakage) == 6,
        f"all six broken under C: {c_breakage}",
    )

    # Test 3: 2-dim subspace span{e_i, e_j} (i != j) invariant under
    # {T_1, T_2, T_3} (yes — each T_k is diagonal, so span{e_i, e_j}
    # is T_k-invariant for any pair). Invariance under C requires the
    # cyclic permutation to map span{e_i, e_j} into itself — but
    # C{e_1, e_2} = {e_2, e_3} which is not contained in {e_1, e_2}.
    # So no axis-pair span is C-invariant.
    failed_pairs = []
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        # span{e_i, e_j}. Check whether C e_i and C e_j are in this span.
        ce_i = C * e[i]
        ce_j = C * e[j]
        # span{e_i, e_j} consists of vectors with a zero in the third position
        third = [k for k in [0, 1, 2] if k != i and k != j][0]
        if ce_i[third] != 0 or ce_j[third] != 0:
            failed_pairs.append((i, j))
    check(
        "(7c) no axis-pair 2-dim subspace is C-invariant",
        len(failed_pairs) == 3,
        f"non-invariant pairs={failed_pairs}",
    )

    # ------------------------------------------------------------------
    # T5 / step 8: Burnside hypothesis — rank-1 element in algebra
    # ------------------------------------------------------------------
    for i in range(3):
        check(
            f"(8) rank-1 element in algebra: rank(P_{i + 1}) = 1",
            P[i].rank() == 1,
            f"rank={P[i].rank()}",
        )

    # ------------------------------------------------------------------
    # Forbidden imports check (programmatic)
    # ------------------------------------------------------------------
    # We do not import any framework module, any audit ledger row,
    # or any external numerical value. The runner consumes
    # only sympy.
    import sys
    framework_modules = [
        m for m in sys.modules
        if m.startswith("toy_") or "audit" in m.lower() or "lattice" in m.lower()
    ]
    check(
        "(9) no framework / audit / lattice modules imported",
        not framework_modules,
        f"forbidden={framework_modules}" if framework_modules else "",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
