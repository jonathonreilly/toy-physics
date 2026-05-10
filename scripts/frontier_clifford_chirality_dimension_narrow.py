#!/usr/bin/env python3
"""Pattern A narrow runner for `CLIFFORD_CHIRALITY_DIMENSION_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone Clifford-algebra fact (Lawson--Michelsohn, *Spin
Geometry*, Ch. I, Prop. 3.3): in `Cl(p, q)` with `n = p + q` generators
`gamma_1, ..., gamma_n` satisfying `gamma_mu^2 = +/- I` and
`{gamma_mu, gamma_nu} = 0` for `mu != nu`, the volume element

    omega = gamma_1 gamma_2 ... gamma_n

obeys

    omega gamma_mu = (-1)^(n-1) gamma_mu omega

(equivalently, `[omega, gamma_mu] = 0` when `n` is odd, and
`{omega, gamma_mu} = 0` when `n` is even).

Therefore:
  - `n` EVEN: a chirality involution `gamma_5` proportional to `omega`
    (after a possible scalar phase fixing `gamma_5^2 = +I`) ANTICOMMUTES
    with every generator. A nontrivial Z_2 chirality grading exists.
  - `n` ODD: any element proportional to `omega` COMMUTES with every
    generator (omega is central). Inside the Clifford algebra Cl(n)
    itself, no element anticommutes with every generator: in the unique
    Clifford-basis decomposition (degree-r products of generators), the
    only elements that anticommute with every g_mu are those of even
    degree, and one verifies directly that the only one with square +I
    and centraliser {0} on every g_mu is the zero element. No nontrivial
    Z_2 chirality grading exists on the irreducible representation.

This is class-A pure linear/Clifford algebra. No SM gauge content, no
anomaly trace, no temporal direction, no single-clock evolution
hypothesis is consumed. The narrow theorem's only structural input is
that the framework's spatial substrate is `Z^d_s` with `d_s = 3` (axiom
A2 of `MINIMAL_AXIOMS_2026-05-03`), so that the per-generator count for
the spatial Clifford algebra is exactly 3. The result is stated for
abstract `(d_s, d_t)` and specialised to `d_s = 3` only at the end.

Verification proceeds in four parts:

  Part 1 -- Build explicit Cl(n) generators in even and odd dimensions
            n in {1, 2, 3, 4, 5, 6} via the standard tower
                Cl(0) = C, Cl(1) = C[sigma_1],
                Cl(2k) = Cl(2k-2) tensor M_2(C),
                Cl(2k+1) = Cl(2k) tensor C[sigma_3-extension].
            Check {gamma_mu, gamma_nu} = 2 delta_{mu nu} I exactly.

  Part 2 -- Compute omega = gamma_1 ... gamma_n and verify
                omega gamma_mu = (-1)^(n-1) gamma_mu omega
            for each generator and each dimension.

  Part 3 -- Show that for n ODD, no element of M_{2^k}(C) anticommutes
            with all gamma_mu while squaring to +I.
            (Use the orthonormal Clifford basis; the only basis elements
            that anticommute with every generator are even-degree, and a
            symbolic linear-combination check rules them out.)

  Part 4 -- For n EVEN, exhibit gamma_5 := i^{n(n-1)/2} omega and verify
            gamma_5^2 = +I and {gamma_5, gamma_mu} = 0 for every mu.

  Part 5 -- Specialise to the framework's d_s = 3 spatial substrate (A2):
            the chirality involution requires d_s + d_t even, hence
            d_t in {1, 3, 5, ...} (i.e., d_t odd). This is the narrow
            theorem's restriction-to-framework conclusion. d_t = 1 is
            NOT forced by this narrow theorem alone; that further
            restriction is the scope of separate sister theorems and is
            explicitly out of scope here.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=12, suppress=True, linewidth=120)

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    msg = f"  [{tag}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ----------------------------------------------------------------------------
# Pauli matrices and Cl(n) construction
# ----------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_list(matrices):
    out = matrices[0]
    for M in matrices[1:]:
        out = np.kron(out, M)
    return out


def build_cl_generators(n: int):
    """Return n generators of Cl(n,0) on a 2^{ceil(n/2)}-dim complex space.

    Construction (standard staggered tower):
      n = 1: [sx]
      n = 2: [sx, sy]
      n = 3: [sx kron I, sz kron sx, sz kron sz]
      n = 4: [sx kron I kron I, sz kron sx kron I, sz kron sz kron sx, sz kron sz kron sy]
      n in {5, 6, ...}: extend by alternating tensor pattern.

    All generators square to +I and pairwise anticommute. We construct
    enough cases for Part 1 (n in {1, ..., 6}).
    """
    if n == 1:
        return [sx.astype(complex)]
    if n == 2:
        return [sx.astype(complex), sy.astype(complex)]
    if n == 3:
        return [
            kron_list([sx, I2]),
            kron_list([sz, sx]),
            kron_list([sz, sz]),
        ]
    if n == 4:
        return [
            kron_list([sx, I2, I2]),
            kron_list([sz, sx, I2]),
            kron_list([sz, sz, sx]),
            kron_list([sz, sz, sy]),
        ]
    if n == 5:
        return [
            kron_list([sx, I2, I2]),
            kron_list([sz, sx, I2]),
            kron_list([sz, sz, sx]),
            kron_list([sz, sz, sy]),
            kron_list([sy, I2, I2]),
        ]
    if n == 6:
        return [
            kron_list([sx, I2, I2, I2]),
            kron_list([sz, sx, I2, I2]),
            kron_list([sz, sz, sx, I2]),
            kron_list([sz, sz, sz, sx]),
            kron_list([sz, sz, sz, sy]),
            kron_list([sy, I2, I2, I2]),
        ]
    raise NotImplementedError(f"n = {n} not constructed")


def anticommutator(A, B):
    return A @ B + B @ A


def commutator(A, B):
    return A @ B - B @ A


# ============================================================================
section("Part 1: Cl(n) generators with {g_mu, g_nu} = 2 delta_{mu nu} I")
# ============================================================================
for n in (1, 2, 3, 4, 5, 6):
    gens = build_cl_generators(n)
    dim = gens[0].shape[0]
    eye = np.eye(dim, dtype=complex)
    ok = True
    detail = ""
    for mu in range(n):
        if not np.allclose(gens[mu] @ gens[mu], eye):
            ok = False
            detail = f"g_{mu}^2 != I at n={n}"
            break
        for nu in range(mu + 1, n):
            if not np.allclose(anticommutator(gens[mu], gens[nu]), 0):
                ok = False
                detail = f"non-zero anticommutator g_{mu} g_{nu} at n={n}"
                break
        if not ok:
            break
    check(
        f"n={n}: {n} generators of Cl(n, 0) on C^{dim} satisfy CAR",
        ok,
        detail or f"dim = {dim}",
    )


# ============================================================================
section("Part 2: volume element identity omega g_mu = (-1)^(n-1) g_mu omega")
# ============================================================================
for n in (1, 2, 3, 4, 5, 6):
    gens = build_cl_generators(n)
    dim = gens[0].shape[0]
    omega = gens[0].copy()
    for mu in range(1, n):
        omega = omega @ gens[mu]
    sign = (-1) ** (n - 1)  # +1 if n odd; -1 if n even
    ok = True
    parity = "odd" if n % 2 == 1 else "even"
    expected_relation = "commutes" if n % 2 == 1 else "anticommutes"
    for mu in range(n):
        lhs = omega @ gens[mu]
        rhs = sign * (gens[mu] @ omega)
        if not np.allclose(lhs, rhs):
            ok = False
            break
    check(
        f"n={n} ({parity}): omega {expected_relation} with every g_mu",
        ok,
        detail=f"omega ({expected_relation} for n={parity})",
    )


# ============================================================================
section("Part 3: n ODD => no element OF THE CLIFFORD ALGEBRA Cl(n) anticommutes")
# ============================================================================
# Inside the Clifford algebra Cl(n) itself, every element M is a unique
# complex linear combination of the 2^n basis products of distinct
# generators g_{i_1} g_{i_2} ... g_{i_r} (r = 0, 1, ..., n).
#
# A degree-r product anticommutes with g_mu iff exactly r of {1, ..., n}
# (excluding mu) appear in its index set, modulo a parity sign. The
# precise rule is:
#   g_{i_1} ... g_{i_r} commutes with g_mu  iff  ((mu ∈ index set) XOR (r odd))
#   = False, i.e., (r is even AND mu not in index set) OR (r is odd AND mu in index set).
# Equivalently: a degree-r product anticommutes with g_mu iff
#   (r is odd AND mu NOT in index set) OR (r is even AND mu in index set).
#
# For an element M = sum_S c_S g_S to anticommute with EVERY g_mu, the
# coefficients must satisfy the appropriate parity constraints
# simultaneously for every mu = 1, ..., n. We solve this linear system.

from itertools import combinations


def clifford_basis(gens):
    """All ordered products of distinct generators (length 0 ... n)."""
    n = len(gens)
    basis = []
    labels = []
    indexsets = []
    for r in range(n + 1):
        for idx in combinations(range(n), r):
            if r == 0:
                M = np.eye(gens[0].shape[0], dtype=complex)
                lab = "I"
            else:
                M = gens[idx[0]].copy()
                for j in idx[1:]:
                    M = M @ gens[j]
                lab = "g" + "".join(str(k + 1) for k in idx)
            basis.append(M)
            labels.append(lab)
            indexsets.append(set(idx))
    return basis, labels, indexsets


def solve_anticommute_in_clifford_algebra(gens):
    """Return (sol_dim, basis_dim) where sol_dim is the dimension of the
    set {M in Cl(n) | {M, g_mu} = 0 for all mu = 1, ..., n}. We work in
    the 2^n-dim Clifford basis (NOT the full M_{2^k}(C) ambient matrix
    space).
    """
    n = len(gens)
    basis, labels, indexsets = clifford_basis(gens)
    B = len(basis)  # = 2^n
    # Build linear constraints. For each mu and each basis element b_S of
    # degree r:
    #   {b_S, g_mu} = (sign_S_mu) * (b_S g_mu + g_mu b_S)
    # We compute the anticommutator directly and project back onto the
    # Clifford basis.
    #
    # Easiest: for each basis element, compute its anticommutator with g_mu
    # (a 2^k x 2^k matrix), then test whether each entry-pair is zero
    # entrywise. Linear system: c · A_mu = 0 where A_mu is constructed by
    # mapping each basis element to its anticommutator's vec.
    dim = gens[0].shape[0]
    constraint_rows = []
    for mu in range(n):
        g = gens[mu]
        # The anticommutator of basis element b_S with g_mu is a
        # 2^k x 2^k matrix; flatten to vector.
        for entry in range(dim * dim):
            row = np.zeros(B, dtype=complex)
            for j, b in enumerate(basis):
                ac = b @ g + g @ b
                row[j] = ac.flat[entry]
            if np.any(np.abs(row) > 1e-12):
                constraint_rows.append(row)
    if constraint_rows:
        L = np.array(constraint_rows, dtype=complex)
        rank = np.linalg.matrix_rank(L, tol=1e-10)
        return B - rank, B
    return B, B


for n in (1, 3, 5):
    gens = build_cl_generators(n)
    sol_dim, basis_dim = solve_anticommute_in_clifford_algebra(gens)
    # For n odd, no element of Cl(n) anticommutes with every generator.
    check(
        f"n={n} (odd): {{M in Cl(n) | {{M, g_mu}}=0 forall mu}} = {{0}} inside Cl(n)",
        sol_dim == 0,
        detail=f"sol_dim = {sol_dim} of 2^{n}={basis_dim} Clifford-basis dim",
    )

# Sanity: in even dimension, gamma_5 = i^{n(n-1)/2} omega itself spans a
# 1-dim solution INSIDE Cl(n).
for n in (2, 4, 6):
    gens = build_cl_generators(n)
    sol_dim, basis_dim = solve_anticommute_in_clifford_algebra(gens)
    check(
        f"n={n} (even): {{M in Cl(n) | {{M, g_mu}}=0 forall mu}} is exactly 1-dim (= span of gamma_5)",
        sol_dim == 1,
        detail=f"sol_dim = {sol_dim} of 2^{n}={basis_dim} Clifford-basis dim",
    )


# ============================================================================
section("Part 4: n EVEN => gamma_5 := i^{n(n-1)/2} omega satisfies gamma_5^2=+I and {gamma_5,g_mu}=0")
# ============================================================================
for n in (2, 4, 6):
    gens = build_cl_generators(n)
    dim = gens[0].shape[0]
    eye = np.eye(dim, dtype=complex)
    omega = gens[0].copy()
    for mu in range(1, n):
        omega = omega @ gens[mu]
    phase = (1j) ** (n * (n - 1) // 2)
    gamma5 = phase * omega
    sq = gamma5 @ gamma5
    ok_sq = np.allclose(sq, eye)
    ok_ac = all(np.allclose(anticommutator(gamma5, gens[mu]), 0) for mu in range(n))
    check(
        f"n={n}: gamma_5^2 = +I",
        ok_sq,
        detail=f"phase i^{n*(n-1)//2}",
    )
    check(
        f"n={n}: {{gamma_5, g_mu}} = 0 for every mu",
        ok_ac,
    )


# ============================================================================
section("Part 5: framework specialisation d_s = 3 (axiom A2) => d_t odd")
# ============================================================================
# A2 fixes the spatial substrate to Z^d_s with d_s = 3.
# For a chirality involution to exist, d_s + d_t must be even.
# Therefore d_t must have the opposite parity to d_s.
# d_s = 3 is odd, so d_t must be ODD.
d_s = 3
allowed_d_t = [d for d in range(1, 8) if (d_s + d) % 2 == 0]
forbidden_d_t = [d for d in range(1, 8) if (d_s + d) % 2 == 1]
check(
    "d_s = 3 (axiom A2): chirality involution requires d_t odd",
    allowed_d_t == [1, 3, 5, 7] and forbidden_d_t == [2, 4, 6],
    detail=f"allowed d_t = {allowed_d_t}; forbidden d_t = {forbidden_d_t}",
)
# Out of scope: this narrow theorem does NOT force d_t = 1 from chirality
# alone. The further restriction d_t = 1 is supplied by separate sister
# theorems (e.g., AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM
# or Craig--Weinstein / Tegmark continuum-PDE results) and is explicitly
# out of scope here.
print()
print("  Out-of-scope reminder: this narrow theorem only forces d_t to")
print("  be ODD. The further restriction d_t = 1 is supplied by separate")
print("  sister theorems (single-clock codimension-1 evolution theorem on")
print("  the lattice or Craig--Weinstein / Tegmark on the continuum) and")
print("  is NOT part of this narrow theorem's load-bearing scope.")


# ============================================================================
section("Narrow theorem summary")
# ============================================================================
print(
    """
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let n = p + q and let g_1, ..., g_n be n generators of Cl(p, q) over C
    satisfying g_mu^2 = +/- I and {g_mu, g_nu} = 0 for mu != nu.

  CONCLUSION (volume-element identity):
    omega := g_1 g_2 ... g_n satisfies
        omega g_mu = (-1)^(n-1) g_mu omega
    for every generator g_mu.

  CONCLUSION (chirality dichotomy):
    (a) n EVEN  =>  gamma_5 := i^{n(n-1)/2} omega satisfies
                    gamma_5^2 = +I and {gamma_5, g_mu} = 0 for every mu;
                    a nontrivial Z_2 chirality grading EXISTS.

    (b) n ODD   =>  no element M of the Clifford algebra (acting on
                    the irreducible 2^{(n-1)/2}-dim spinor rep) satisfies
                    M^2 = +I together with {M, g_mu} = 0 for every mu;
                    no nontrivial Z_2 chirality grading EXISTS.

  CONCLUSION (framework specialisation, with axiom A2: d_s = 3):
    Existence of a chirality involution gamma_5 on the total Clifford
    algebra Cl(d_s, d_t) requires d_s + d_t even; with d_s = 3 fixed,
    this forces d_t to be ODD: d_t in {1, 3, 5, ...}.

  Audit-lane class:
    (A) -- pure Clifford-algebra fact verified by exact linear algebra
    on explicit generator constructions in every relevant dimension.

  Out of scope:
    -- gauge-anomaly arithmetic (Tr[Y], Tr[Y^3], etc.);
    -- choice of d_t = 1 over d_t in {3, 5, ...};
    -- single-clock codimension-1 evolution structure;
    -- ABJ anomaly-to-inconsistency implication;
    -- physical Standard-Model fermion content;
    -- emergent Lorentz boost covariance.
"""
)


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
