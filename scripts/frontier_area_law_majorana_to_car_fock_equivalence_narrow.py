#!/usr/bin/env python3
"""Pattern A narrow runner for
``AREA_LAW_MAJORANA_CAR_FOCK_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-09``.

Verifies the standalone Clifford-Majorana-to-complex-CAR Fock equivalence on
an abstract four-dimensional complex Hilbert space ``K``:

  Hypothesis:
      gamma_1, gamma_2, gamma_3, gamma_4   Hermitian on K = C^4
      {gamma_i, gamma_j} = 2 delta_ij I_K        (complex Cl_4)

  Define:
      c_a = (gamma_{2a-1} + i gamma_{2a}) / 2,   a in {1, 2}
      c_a^dag = (gamma_{2a-1} - i gamma_{2a}) / 2

  Conclusion:
      (T1)  {c_a, c_b}        = 0
            {c_a, c_b^dag}    = delta_ab I_K
      (T2)  If the four (gamma_i) generate End(K) ~= M_4(C), then there
            exists a unitary U: K -> F(C^2) (unique up to overall phase)
            such that U c_a U^dag = a_a, where (a_1, a_2) are the standard
            CAR annihilation operators on F(C^2) ~= C^4.
      (T3)  Hilbert-rank four alone does not force CAR: commuting Pauli
            factors A = X (x) I, B = I (x) X on C^2 (x) C^2 satisfy
            [A, B] = 0 and {A, B} != 0, so they are not CAR generators.

This runner is class-A pure finite-dimensional algebra. No physical
identification of K with a primitive horizon block, no substrate-to-P_A
forcing, no Wald-Noether or coframe-response authority is consumed.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

try:
    import sympy as sp
except ImportError:
    print("FAIL: sympy required for class-A symbolic algebra")
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
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
# Symbolic part: (T1) using sympy noncommutative symbols.
# ============================================================================
section("Part 1 (T1, symbolic): Cl_4 relations imply CAR identities for c_a")

g1, g2, g3, g4 = sp.symbols("g1 g2 g3 g4", commutative=False)
gammas_sym = [g1, g2, g3, g4]
i_unit = sp.I


def c_sym(a: int) -> sp.Expr:
    return sp.Rational(1, 2) * (gammas_sym[2 * a - 2] + i_unit * gammas_sym[2 * a - 1])


def cdag_sym(a: int) -> sp.Expr:
    return sp.Rational(1, 2) * (gammas_sym[2 * a - 2] - i_unit * gammas_sym[2 * a - 1])


def _gamma_index(sym: sp.Symbol) -> int:
    name = str(sym)
    return int(name[1:])


def _normalize_term(term: sp.Expr) -> sp.Expr:
    """Normalize one monomial under the relations
        g_i * g_i = 1,
        g_i * g_j = -g_j * g_i (i != j).
    Returns a canonical form: scalar coefficient times a strictly increasing
    product of distinct generators g_{i_1} ... g_{i_k} with i_1 < ... < i_k.
    """
    if term.is_number:
        return term
    if term.is_Mul:
        factors = list(term.args)
    else:
        factors = [term]

    coef = sp.S.One
    syms: list[sp.Symbol] = []
    for f in factors:
        if f.is_commutative:
            coef *= f
        elif f.is_Symbol:
            syms.append(f)
        elif f.is_Pow and f.base.is_Symbol and f.exp.is_integer:
            # g_i ** k = (g_i^2)^(k//2) * g_i^(k%2) = 1^(k//2) * g_i^(k%2)
            k = int(f.exp)
            if k % 2 == 1:
                syms.append(f.base)
            # k % 2 == 0 contributes I (handled by coef *= 1 implicitly)
        else:
            # Should not appear after sp.expand.
            return None  # signal failure

    # Bubble-sort with relations g_i * g_i = 1 and g_i * g_j = -g_j * g_i.
    sign = 1
    while True:
        changed = False
        # First, look for adjacent identical generators -> g_i * g_i = 1.
        i = 0
        while i + 1 < len(syms):
            if syms[i] == syms[i + 1]:
                # Remove both.
                del syms[i : i + 2]
                changed = True
                # Continue scanning at the new position (don't increment).
            else:
                i += 1
        if changed:
            continue
        # Then, swap adjacent out-of-order distinct generators with sign flip.
        for k in range(len(syms) - 1):
            if _gamma_index(syms[k]) > _gamma_index(syms[k + 1]):
                syms[k], syms[k + 1] = syms[k + 1], syms[k]
                sign = -sign
                changed = True
                break
        if not changed:
            break

    out = sign * coef
    for s in syms:
        out = out * s
    return out


def reduce_cl4(expr: sp.Expr) -> sp.Expr:
    """Reduce a polynomial in g1..g4 to canonical form using
        g_i^2 = 1,                  (from {g_i, g_i} = 2 I)
        g_i * g_j = -g_j * g_i      (from {g_i, g_j} = 0, i != j)
    after expanding into monomials. Returns a polynomial whose monomials are
    coefficient * (g_{i_1} g_{i_2} ... g_{i_k}) with i_1 < i_2 < ... < i_k.
    """
    expr = sp.expand(expr)
    if expr.is_Add:
        terms = expr.args
    else:
        terms = (expr,)
    out = sp.S.Zero
    for t in terms:
        nt = _normalize_term(t)
        if nt is None:
            raise ValueError(f"Could not normalize term: {t}")
        out = out + nt
    return sp.expand(out)


# {c_a, c_b} reduces to 0 for all a, b in {1, 2}
all_zero = True
for a, b in itertools.product([1, 2], repeat=2):
    expr = c_sym(a) * c_sym(b) + c_sym(b) * c_sym(a)
    reduced = reduce_cl4(expr)
    ok = reduced == 0
    if not ok:
        all_zero = False
    check(
        f"{{c_{a}, c_{b}}} reduces to 0 in Cl_4",
        ok,
        detail=f"reduced = {reduced}",
    )

# {c_a, c_b^dag} reduces to delta_ab * I (i.e., the scalar 1 in the reduced ring)
all_kron = True
for a, b in itertools.product([1, 2], repeat=2):
    expr = c_sym(a) * cdag_sym(b) + cdag_sym(b) * c_sym(a)
    reduced = reduce_cl4(expr)
    expected = sp.Integer(1) if a == b else sp.Integer(0)
    ok = reduced == expected
    if not ok:
        all_kron = False
    check(
        f"{{c_{a}, c_{b}^dag}} reduces to delta_{{{a}{b}}} I in Cl_4",
        ok,
        detail=f"reduced = {reduced}, expected = {expected}",
    )


# ============================================================================
# Numerical part: explicit C^4 ~= F(C^2) representation.
# ============================================================================
section("Part 2 (numerical baseline): canonical Cl_4 / CAR representation on C^4")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SM = np.array([[0, 1], [0, 0]], dtype=complex)


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


# Standard two-mode CAR on F(C^2) ~= C^4 via Jordan-Wigner:
a1 = kron(SM, I2)
a2 = kron(Z, SM)
ident4 = np.eye(4, dtype=complex)


def anticomm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def comm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


# CAR check on F(C^2)
max_aa = 0.0
max_aad = 0.0
for i, ci in enumerate([a1, a2]):
    for j, cj in enumerate([a1, a2]):
        max_aa = max(max_aa, np.linalg.norm(anticomm(ci, cj)))
        expected = ident4 if i == j else np.zeros((4, 4), dtype=complex)
        max_aad = max(
            max_aad,
            np.linalg.norm(anticomm(ci, cj.conj().T) - expected),
        )
check(
    "F(C^2) annihilation operators satisfy {a_i, a_j} = 0",
    max_aa < 1e-12,
    detail=f"max error = {max_aa:.2e}",
)
check(
    "F(C^2) annihilation operators satisfy {a_i, a_j^dag} = delta_ij I",
    max_aad < 1e-12,
    detail=f"max error = {max_aad:.2e}",
)

# Build canonical Majorana from CAR via gamma_{2a-1} = a_a + a_a^dag,
# gamma_{2a} = -i (a_a - a_a^dag).
g_can = [
    a1 + a1.conj().T,
    -1j * (a1 - a1.conj().T),
    a2 + a2.conj().T,
    -1j * (a2 - a2.conj().T),
]
max_herm = max(np.linalg.norm(g - g.conj().T) for g in g_can)
check(
    "canonical four Majoranas are Hermitian",
    max_herm < 1e-12,
    detail=f"max ||g - g^dag|| = {max_herm:.2e}",
)
max_cliff = 0.0
for i, gi in enumerate(g_can):
    for j, gj in enumerate(g_can):
        expected = (2.0 if i == j else 0.0) * ident4
        max_cliff = max(max_cliff, np.linalg.norm(anticomm(gi, gj) - expected))
check(
    "canonical four Majoranas satisfy {g_i, g_j} = 2 delta_ij I",
    max_cliff < 1e-12,
    detail=f"max ||{{g_i,g_j}} - 2 delta_ij I|| = {max_cliff:.2e}",
)

# Generation of M_4(C): four Majoranas span End(C^4) ~= M_4(C).
# Use products over subsets {1, g_1, g_2, g_3, g_4, g_1 g_2, ..., g_1 g_2 g_3 g_4}
# which span 2^4 = 16 elements. Their flattened forms span a 16-dim subspace of C^16.
words = [ident4]
for r in range(1, 5):
    for indices in itertools.combinations(range(4), r):
        m = ident4.copy()
        for k in indices:
            m = m @ g_can[k]
        words.append(m)
columns = np.column_stack([w.reshape(-1) for w in words])
rank_words = int(np.linalg.matrix_rank(columns, tol=1e-10))
check(
    "canonical four Majoranas generate End(C^4) ~= M_4(C)",
    rank_words == 16,
    detail=f"complex span rank = {rank_words} (expected 16)",
)


section("Part 3 (numerical (T1)): CAR identities for c_a = (g_{2a-1} + i g_{2a})/2")

c1 = 0.5 * (g_can[0] + 1j * g_can[1])
c2 = 0.5 * (g_can[2] + 1j * g_can[3])

# CAR check: {c_a, c_b} = 0, {c_a, c_b^dag} = delta_ab I
max_cc = 0.0
max_ccd = 0.0
for ci in [c1, c2]:
    for cj in [c1, c2]:
        max_cc = max(max_cc, np.linalg.norm(anticomm(ci, cj)))
for i, ci in enumerate([c1, c2]):
    for j, cj in enumerate([c1, c2]):
        expected = ident4 if i == j else np.zeros((4, 4), dtype=complex)
        max_ccd = max(max_ccd, np.linalg.norm(anticomm(ci, cj.conj().T) - expected))

check(
    "{c_a, c_b} = 0 numerically (canonical Cl_4 representation)",
    max_cc < 1e-12,
    detail=f"max error = {max_cc:.2e}",
)
check(
    "{c_a, c_b^dag} = delta_ab I numerically (canonical Cl_4 representation)",
    max_ccd < 1e-12,
    detail=f"max error = {max_ccd:.2e}",
)


section("Part 4 (T2): Pauli intertwiner — second Cl_4 representation by unitary conjugation")

# Generate a "different" Cl_4 representation by random unitary conjugation:
# any U in U(4) gives g'_i = U g_i U^dag, which still satisfies the same Cl_4
# relations and still generates M_4(C). The Pauli theorem says there exists a
# unitary U' (unique up to phase) such that U' g_i U'^dag = g_can[i].
np.random.seed(20260509)
H = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
H = (H + H.conj().T) / 2
import scipy.linalg as la

U_random = la.expm(1j * H)
g_alt = [U_random @ g @ U_random.conj().T for g in g_can]

max_herm_alt = max(np.linalg.norm(g - g.conj().T) for g in g_alt)
max_cliff_alt = 0.0
for i, gi in enumerate(g_alt):
    for j, gj in enumerate(g_alt):
        expected = (2.0 if i == j else 0.0) * ident4
        max_cliff_alt = max(max_cliff_alt, np.linalg.norm(anticomm(gi, gj) - expected))
check(
    "alternative Cl_4 representation: Hermiticity preserved",
    max_herm_alt < 1e-10,
    detail=f"max ||g'_i - g'_i^dag|| = {max_herm_alt:.2e}",
)
check(
    "alternative Cl_4 representation: relations preserved",
    max_cliff_alt < 1e-10,
    detail=f"max ||{{g'_i, g'_j}} - 2 delta_ij I|| = {max_cliff_alt:.2e}",
)


def find_intertwiner(
    src: list[np.ndarray], tgt: list[np.ndarray]
) -> tuple[np.ndarray, int, float]:
    """Return (U, null_dim, residual) such that U src[i] = tgt[i] U.

    The intertwining condition vec(U) is the right null space of the stacked
    operator A = sum_i kron(tgt[i], I) - kron(I, src[i]^T).
    """
    blocks = []
    for s, t in zip(src, tgt):
        blocks.append(np.kron(t, np.eye(4)) - np.kron(np.eye(4), s.T))
    A = np.vstack(blocks)
    u, s_vals, vh = np.linalg.svd(A)
    null_dim = int(np.sum(s_vals < 1e-9))
    if null_dim == 0:
        return np.zeros((4, 4)), 0, float("inf")
    v = vh.conj().T[:, -1]
    U = v.reshape(4, 4)
    norm2 = np.trace(U @ U.conj().T).real / 4
    if norm2 < 1e-12:
        return U, null_dim, float("inf")
    U_unit = U / np.sqrt(norm2)
    residual = max(np.linalg.norm(U_unit @ s - t @ U_unit) for s, t in zip(src, tgt))
    return U_unit, null_dim, residual


U_inter, null_dim, residual = find_intertwiner(g_alt, g_can)
check(
    "intertwiner null space has dimension exactly one (Schur uniqueness)",
    null_dim == 1,
    detail=f"null_dim = {null_dim}",
)
check(
    "intertwiner U is unitary (up to phase)",
    np.linalg.norm(U_inter @ U_inter.conj().T - ident4) < 1e-9,
    detail=f"||U U^dag - I|| = {np.linalg.norm(U_inter @ U_inter.conj().T - ident4):.2e}",
)
check(
    "U g_alt[i] U^dag = g_can[i] (Pauli intertwiner equation (4))",
    residual < 1e-9,
    detail=f"max ||U g'_i U^dag - g_i|| = {residual:.2e}",
)

# Same check at the CAR level: U c'_a U^dag = a_a (the canonical CAR pair).
c1_alt = 0.5 * (g_alt[0] + 1j * g_alt[1])
c2_alt = 0.5 * (g_alt[2] + 1j * g_alt[3])
err_c1 = np.linalg.norm(U_inter @ c1_alt @ U_inter.conj().T - c1)
err_c2 = np.linalg.norm(U_inter @ c2_alt @ U_inter.conj().T - c2)
check(
    "U c'_a U^dag = a_a (CAR-level intertwiner)",
    max(err_c1, err_c2) < 1e-9,
    detail=f"max CAR intertwiner error = {max(err_c1, err_c2):.2e}",
)


section("Part 5 (T3): rank-four Hilbert space alone does not force CAR")

A_op = kron(X, I2)
B_op = kron(I2, X)
ab_comm = np.linalg.norm(comm(A_op, B_op))
ab_anticomm = np.linalg.norm(anticomm(A_op, B_op))
check(
    "commuting Pauli pair on C^2 (x) C^2: [A, B] = 0",
    ab_comm < 1e-12,
    detail=f"||[X (x) I, I (x) X]|| = {ab_comm:.2e}",
)
check(
    "commuting Pauli pair on C^2 (x) C^2: {A, B} != 0 (so not CAR)",
    ab_anticomm > 1.0,
    detail=f"||{{X (x) I, I (x) X}}|| = {ab_anticomm:.2e}",
)


section("Part 6: inverse map — recover Majoranas from CAR pair")

# gamma_{2a-1} = c_a + c_a^dag, gamma_{2a} = -i (c_a - c_a^dag)
g_recover = [
    c1 + c1.conj().T,
    -1j * (c1 - c1.conj().T),
    c2 + c2.conj().T,
    -1j * (c2 - c2.conj().T),
]
max_recover = max(
    np.linalg.norm(g_recover[k] - g_can[k]) for k in range(4)
)
check(
    "inverse map (c_a, c_a^dag) -> (gamma_{2a-1}, gamma_{2a}) recovers original",
    max_recover < 1e-12,
    detail=f"max ||gamma_recovered - gamma|| = {max_recover:.2e}",
)


section("Narrow theorem summary")
print(
    """
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let K be a four-dimensional complex Hilbert space and let
    gamma_1, gamma_2, gamma_3, gamma_4 be Hermitian operators on K
    satisfying  {gamma_i, gamma_j} = 2 delta_ij I_K  (complex Cl_4).
    Define  c_a = (gamma_{2a-1} + i gamma_{2a}) / 2  for a in {1, 2}.

  CONCLUSION:
    (T1)  {c_a, c_b}        = 0       symbolically from Cl_4 alone.
          {c_a, c_b^dag}    = delta_ab I_K     symbolically from Cl_4 alone.

    (T2)  If (gamma_i) generate End(K) ~= M_4(C), then there exists a
          unitary U: K -> F(C^2), unique up to overall phase, with
              U c_a U^dag = a_a       a in {1, 2},
          where (a_1, a_2) are the standard CAR annihilators on F(C^2).

    (T3)  Hilbert dimension four alone is insufficient: the commuting
          Pauli pair (X (x) I, I (x) X) on C^2 (x) C^2 has [.,.] = 0
          and {.,.} != 0, so it is not a CAR pair.

  Audit-lane class:
    (A) — finite-dimensional algebra and Pauli-style Clifford
    representation theory on an abstract complex Hilbert space C^4.
    No physical horizon, substrate-to-P_A, Cl(3)/Z^3, Wald-Noether,
    coframe-response, or BH-quarter authority is consumed.
"""
)


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
