#!/usr/bin/env python3
"""Pattern A narrow runner for
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_POSITIVITY_EQUIVARIANCE_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone nonnegative-matrix algebra identity:

  Let W be any nonempty finite index set, and let sigma : W -> W be
  any involution (sigma^2 = id). Let D = diag(d_w) be a diagonal
  matrix on R^W with strictly positive entries and assume D is
  sigma-invariant (d_{sigma(w)} = d_w). Let M_+, M_- be matrices on
  R^W with entries in the nonnegative integers satisfying the
  involution conjugacy
      sigma M_+ sigma = M_-.

  Define the symmetric tensor word
      Word(D, M_+, M_-) := D (M_+ + M_-) D (M_+ + M_-)^T D.

  THEN:
    (T1) Every entry of Word(D, M_+, M_-) is a nonnegative real number.
    (T2) sigma * Word * sigma = Word (sigma-equivariance).
    (T3) For any sigma-invariant nonnegative vector eta in R^W,
         the image y := Word * eta is sigma-invariant and
         entry-wise nonnegative.

This is a class-A pure linear-algebra fact on a finite index set
carrying an involution. No Wilson character coefficient identification,
no SU(3) representation theory, no Peter-Weyl identification, no
Perron solve, and no boundary-character bridge is consumed; the
narrow theorem treats (W, sigma, D, M_+, M_-) as abstract finite-data
inputs.

Companion role: this is a Pattern A new narrow claim row carving out
the abstract algebraic core of the runner-checked one-word packet from
`gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`,
following the auditor-named OR-narrow path "split note scoped only to
the one finite tensor-word packet" recorded in the conditional verdict
on the parent note.
"""

from __future__ import annotations

import sys

try:
    import sympy as sp
    from sympy import Matrix, eye, zeros, symbols, simplify, expand, Rational
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


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
    line = f"  [{tag}] {label}"
    if detail:
        line += f"  ({detail})"
    print(line)


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


def involution_matrix_from_pairs(n: int, pairs: list[tuple[int, int]],
                                 fixed: list[int] | None = None) -> Matrix:
    """Build the |W|=n permutation matrix for the involution that swaps each
    (i, j) in `pairs` and fixes each index in `fixed`. The constructed
    matrix M satisfies M[a, b] = 1 iff b = sigma(a)."""
    fixed = fixed or []
    n_used = set()
    sigma = [None] * n
    for i, j in pairs:
        assert i != j and 0 <= i < n and 0 <= j < n
        sigma[i], sigma[j] = j, i
        n_used.update({i, j})
    for k in fixed:
        assert 0 <= k < n
        sigma[k] = k
        n_used.add(k)
    for k in range(n):
        if sigma[k] is None:
            sigma[k] = k  # fix any unassigned index
    M = zeros(n, n)
    for a in range(n):
        M[a, sigma[a]] = 1
    return M


def assert_involution(sigma: Matrix, label: str) -> bool:
    n = sigma.shape[0]
    return simplify(sigma * sigma - eye(n)) == zeros(n, n) and sigma.T == sigma


def is_sigma_invariant_diagonal(D: Matrix, sigma: Matrix) -> bool:
    """sigma D sigma == D (true iff D is diagonal and d_{sigma(w)} = d_w)."""
    return simplify(sigma * D * sigma - D) == zeros(*D.shape)


def has_nonneg_int_entries(M: Matrix) -> bool:
    """Check that every entry of M is a concrete nonnegative integer."""
    n, m = M.shape
    for r in range(n):
        for c in range(m):
            entry = M[r, c]
            if not entry.is_Integer:
                return False
            if int(entry) < 0:
                return False
    return True


def all_entries_nonneg_at_positive_diag(W_mat: Matrix, d_syms: list,
                                        positive_value: int = 1) -> bool:
    """Substitute every symbolic positive into `positive_value` and verify
    every entry of W_mat evaluates to a nonnegative integer/rational."""
    subs_map = {d: positive_value for d in d_syms}
    n, m = W_mat.shape
    for r in range(n):
        for c in range(m):
            v = W_mat[r, c].subs(subs_map)
            if v < 0:
                return False
    return True


def all_entries_polynomial_positive_combination(W_mat: Matrix, d_syms: list) -> bool:
    """Verify every entry of W_mat is a polynomial in the symbols `d_syms`
    with nonnegative-integer coefficients (i.e. a sum of products of
    positives). We expand each entry and inspect coefficients."""
    n, m = W_mat.shape
    for r in range(n):
        for c in range(m):
            poly_expr = sp.Poly(sp.expand(W_mat[r, c]), *d_syms, domain=sp.ZZ)
            for monomial, coeff in poly_expr.as_dict().items():
                if coeff < 0:
                    return False
    return True


# ============================================================================
section("Pattern A narrow theorem: tensor-word positivity + sigma-equivariance")
# Statement: on any finite index set W with involution sigma, sigma-invariant
# positive diagonal D, and nonnegative integer M_+, M_- with sigma M_+ sigma
# = M_-, the symmetric tensor word D (M_+ + M_-) D (M_+ + M_-)^T D is
# entry-wise nonnegative, sigma-equivariant, and maps sigma-invariant
# nonnegative vectors to sigma-invariant nonnegative vectors. Pure
# nonnegative-matrix linear algebra.
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: instance W = {0, 1, 2, 3}, sigma = (0 1)(2 3), simple M_+")
# ----------------------------------------------------------------------------
# A 4-element index set with an involution that has no fixed points.
sigma_4 = involution_matrix_from_pairs(4, [(0, 1), (2, 3)])
check("sigma is an involution: sigma^2 = I and sigma^T = sigma",
      assert_involution(sigma_4, "sigma_4"))

# sigma-invariant positive diagonal: pair (0,1) and (2,3) share scalars.
d0, d1 = symbols('d_0 d_1', positive=True)
D_4 = sp.diag(d0, d0, d1, d1)
check("D is sigma-invariant (sigma D sigma = D)",
      is_sigma_invariant_diagonal(D_4, sigma_4))

# Pick an arbitrary nonnegative integer M_+ and define M_- via the
# involution conjugacy hypothesis (1).
M_plus_4 = Matrix([
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 1, 0],
])
M_minus_4 = sigma_4 * M_plus_4 * sigma_4
check("M_+ has entries in Z_{>=0}", has_nonneg_int_entries(M_plus_4))
check("M_- := sigma M_+ sigma has entries in Z_{>=0}",
      has_nonneg_int_entries(M_minus_4))
check("conjugacy (1): sigma M_+ sigma = M_- by construction",
      simplify(sigma_4 * M_plus_4 * sigma_4 - M_minus_4) == zeros(4, 4))

# Symmetrized fusion matrix is sigma-equivariant by (T2)-step:
# sigma (M_+ + M_-) sigma = M_- + M_+.
M_sum_4 = M_plus_4 + M_minus_4
check("M_+ + M_- is sigma-equivariant: sigma (M_+ + M_-) sigma = M_+ + M_-",
      simplify(sigma_4 * M_sum_4 * sigma_4 - M_sum_4) == zeros(4, 4))

# Build the symmetric tensor word and verify (T1)-(T3).
Word_4 = D_4 * M_sum_4 * D_4 * M_sum_4.T * D_4
check("(T1) every entry of Word(D, M_+, M_-) is a polynomial in {d_0, d_1} "
      "with nonnegative integer coefficients",
      all_entries_polynomial_positive_combination(Word_4, [d0, d1]))
check("(T1) Word(D, M_+, M_-) evaluated at d_0 = d_1 = 1 has every entry >= 0",
      all_entries_nonneg_at_positive_diag(Word_4, [d0, d1], positive_value=1))

check("(T2) sigma * Word * sigma = Word (sigma-equivariance)",
      simplify(sigma_4 * Word_4 * sigma_4 - Word_4) == zeros(4, 4))

# (T3): image of a sigma-invariant nonnegative vector.
a, b = symbols('a b', positive=True)
eta_4 = Matrix([a, a, b, b])  # sigma_4-invariant by construction
check("eta is sigma-invariant: sigma eta = eta",
      simplify(sigma_4 * eta_4 - eta_4) == zeros(4, 1))
y_4 = Word_4 * eta_4
check("(T3) sigma y = y (image of sigma-invariant vector is sigma-invariant)",
      simplify(sigma_4 * y_4 - y_4) == zeros(4, 1))
y_polys_nonneg = all([
    all([
        sp.Poly(sp.expand(y_4[k]), a, b, d0, d1, domain=sp.ZZ).as_dict().get(mon, 0) >= 0
        for mon in sp.Poly(sp.expand(y_4[k]), a, b, d0, d1, domain=sp.ZZ).as_dict()
    ])
    for k in range(4)
])
check("(T3) every entry of y is a polynomial in (a, b, d_0, d_1) with "
      "nonnegative integer coefficients",
      y_polys_nonneg)


# ----------------------------------------------------------------------------
section("Part 2: instance W = {0, ..., 5}, sigma = (0 1)(2 3)(4 5)")
# ----------------------------------------------------------------------------
# Confirm the algebra is not specific to |W| = 4: try a 6-element index set.
sigma_6 = involution_matrix_from_pairs(6, [(0, 1), (2, 3), (4, 5)])
check("sigma_6 is an involution",
      assert_involution(sigma_6, "sigma_6"))

d2 = symbols('d_2', positive=True)
D_6 = sp.diag(d0, d0, d1, d1, d2, d2)
check("D_6 is sigma_6-invariant",
      is_sigma_invariant_diagonal(D_6, sigma_6))

M_plus_6 = Matrix([
    [0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0],
])
M_minus_6 = sigma_6 * M_plus_6 * sigma_6
check("M_+ on 6x6 has entries in Z_{>=0}", has_nonneg_int_entries(M_plus_6))
check("M_- := sigma M_+ sigma on 6x6 has entries in Z_{>=0}",
      has_nonneg_int_entries(M_minus_6))

M_sum_6 = M_plus_6 + M_minus_6
Word_6 = D_6 * M_sum_6 * D_6 * M_sum_6.T * D_6
check("(T1) on 6x6 instance: every entry is a polynomial in {d_0, d_1, d_2} "
      "with nonnegative integer coefficients",
      all_entries_polynomial_positive_combination(Word_6, [d0, d1, d2]))
check("(T2) on 6x6 instance: sigma * Word * sigma = Word",
      simplify(sigma_6 * Word_6 * sigma_6 - Word_6) == zeros(6, 6))

# Sigma-invariant test vector on the 6x6 instance.
a6, b6, c6 = symbols('a_6 b_6 c_6', positive=True)
eta_6 = Matrix([a6, a6, b6, b6, c6, c6])
y_6 = Word_6 * eta_6
check("(T3) on 6x6 instance: sigma y = y",
      simplify(sigma_6 * y_6 - y_6) == zeros(6, 1))


# ----------------------------------------------------------------------------
section("Part 3: degenerate boundary case M_+ = M_- = 0 gives Word = 0")
# ----------------------------------------------------------------------------
M_plus_zero = zeros(4, 4)
M_minus_zero = sigma_4 * M_plus_zero * sigma_4
check("the conjugacy holds vacuously when M_+ = 0",
      simplify(sigma_4 * M_plus_zero * sigma_4 - M_minus_zero) == zeros(4, 4))
Word_zero = D_4 * (M_plus_zero + M_minus_zero) * D_4 * (M_plus_zero + M_minus_zero).T * D_4
check("(T1) Word = 0 in the degenerate boundary case",
      simplify(Word_zero) == zeros(4, 4))
check("(T2) sigma * 0 * sigma = 0 trivially",
      simplify(sigma_4 * Word_zero * sigma_4 - Word_zero) == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 4: confirmation that the conjugacy hypothesis is the "
        "load-bearing input")
# ----------------------------------------------------------------------------
# Take any nonnegative integer matrix A and define M_+ = A, M_- = sigma A sigma.
# By construction sigma M_+ sigma = sigma A sigma = M_-, so the
# conjugacy hypothesis holds. The narrow theorem then guarantees (T1) -
# (T3). This shows the recurrence form of M_+ in the parent runner is
# not load-bearing - any nonnegative integer A works.
A_arb = Matrix([
    [2, 0, 1, 1],
    [0, 3, 0, 0],
    [0, 0, 0, 2],
    [1, 0, 0, 1],
])
check("A_arb has nonnegative integer entries",
      has_nonneg_int_entries(A_arb))
M_plus_arb = A_arb
M_minus_arb = sigma_4 * A_arb * sigma_4
check("conjugacy (1) holds for the constructed pair (M_+ = A, M_- = sigma A "
      "sigma)",
      simplify(sigma_4 * M_plus_arb * sigma_4 - M_minus_arb) == zeros(4, 4))
M_sum_arb = M_plus_arb + M_minus_arb
Word_arb = D_4 * M_sum_arb * D_4 * M_sum_arb.T * D_4
check("(T1) on the (M_+ = A, M_- = sigma A sigma) instance: every entry is "
      "a polynomial with nonnegative integer coefficients in {d_0, d_1}",
      all_entries_polynomial_positive_combination(Word_arb, [d0, d1]))
check("(T2) on the (M_+ = A, M_- = sigma A sigma) instance: "
      "sigma * Word * sigma = Word",
      simplify(sigma_4 * Word_arb * sigma_4 - Word_arb) == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 5: structural explicit checks of the proof's algebraic steps")
# ----------------------------------------------------------------------------
# (T1) proof step: nonnegative * nonnegative = nonnegative, factor by factor.
intermediate_1 = D_4 * M_sum_4
check("intermediate D * (M_+ + M_-) is entry-wise polynomially nonneg",
      all_entries_polynomial_positive_combination(intermediate_1, [d0, d1]))
intermediate_2 = intermediate_1 * D_4
check("intermediate D * (M_+ + M_-) * D is entry-wise polynomially nonneg",
      all_entries_polynomial_positive_combination(intermediate_2, [d0, d1]))
intermediate_3 = intermediate_2 * M_sum_4.T
check("intermediate D * (M_+ + M_-) * D * (M_+ + M_-)^T is entry-wise "
      "polynomially nonneg",
      all_entries_polynomial_positive_combination(intermediate_3, [d0, d1]))

# (T2) proof step: sigma (M_+ + M_-) sigma = (M_- + M_+) = M_sum.
check("sigma * M_+ * sigma = M_- (the conjugacy hypothesis)",
      simplify(sigma_4 * M_plus_4 * sigma_4 - M_minus_4) == zeros(4, 4))
check("sigma * M_- * sigma = M_+ (squaring the involution)",
      simplify(sigma_4 * M_minus_4 * sigma_4 - M_plus_4) == zeros(4, 4))
check("sigma * (M_+ + M_-) * sigma = M_- + M_+ = (M_+ + M_-)",
      simplify(sigma_4 * M_sum_4 * sigma_4 - M_sum_4) == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let W be any nonempty finite index set, and let sigma : W -> W be
    any involution. Let D = diag(d_w) be a diagonal matrix on R^W with
    strictly positive entries and d_{sigma(w)} = d_w. Let M_+, M_- be
    matrices with entries in Z_{>= 0} satisfying
        sigma M_+ sigma = M_-.
    Define Word(D, M_+, M_-) := D (M_+ + M_-) D (M_+ + M_-)^T D.

  CONCLUSION:
    (T1) Every entry of Word(D, M_+, M_-) is a nonnegative real.
    (T2) sigma * Word * sigma = Word.
    (T3) For any sigma-invariant nonneg vector eta, Word * eta is
         sigma-invariant and nonnegative.

  Audit-lane class:
    (A) - pure nonnegative-matrix linear algebra. No Wilson character
    coefficient identification, no SU(3) representation theory, no
    Peter-Weyl / Perron / boundary-character bridge consumed.

  This narrow theorem isolates the abstract algebraic core of the
  runner-checked one-word packet from the parent
  gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note,
  per the auditor-named OR-narrow path "split note scoped only to the
  one finite tensor-word packet".
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
print(f"\nSUMMARY: PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
