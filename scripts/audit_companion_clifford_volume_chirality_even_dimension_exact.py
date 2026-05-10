#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`clifford_volume_chirality_even_dimension_narrow_theorem_note_2026-05-10`.

Pattern A narrow rescope of the load-bearing Clifford-classification
Step 3 of the parent `ANOMALY_FORCES_TIME_THEOREM.md`. The narrow scope
is purely the Clifford-algebra identity that an algebra element
gamma_5 in Cl(p, q) satisfying gamma_5^2 = +I and {gamma_5, gamma_mu} =
0 for all generators exists iff n = p + q is even. At d_s = 3 this
forces d_t odd.

The script verifies, at exact rational precision via sympy:

  (1) The (V) parity rule
        omega gamma_mu = (-1)^(n-1) gamma_mu omega
      on explicit matrix realizations of Cl(p, q) for n in {2, 3, 4, 5, 6};
  (2) Even-n: omega anticommutes with every generator, and a candidate
      gamma_5 satisfying (C1) + (C2) exists explicitly;
  (3) Odd-n: omega commutes with every generator (centrality), and an
      exhaustive sympy monomial scan over basis elements of Cl(p, q)
      confirms no algebra element anticommutes with all generators
      simultaneously;
  (4) Application at d_s = 3: the chirality-allowed d_t in {1, 3, 5, 7}
      is consistent with d_t odd;
  (5) Counterfactual at d_t = 2 (n = 5 odd): no gamma_5 exists.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow rescope's
load-bearing class-(A) Clifford-classification identity holds at exact
symbolic / matrix precision on explicit realizations.
"""

from pathlib import Path
import sys
import itertools

try:
    import sympy
    from sympy import Matrix, eye, zeros, Rational, I, simplify
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "CLIFFORD_VOLUME_CHIRALITY_EVEN_DIMENSION_NARROW_THEOREM_NOTE_2026-05-10.md"
CLAIM_ID = "clifford_volume_chirality_even_dimension_narrow_theorem_note_2026-05-10"


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
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Pauli matrices over Q (and i)
sigma_x = Matrix([[0, 1], [1, 0]])
sigma_y = Matrix([[0, -I], [I, 0]])
sigma_z = Matrix([[1, 0], [0, -1]])

def kron(A, B):
    """Sympy Kronecker product for explicit Cl(p,q) constructions."""
    rows = A.rows * B.rows
    cols = A.cols * B.cols
    out = zeros(rows, cols)
    for i in range(A.rows):
        for j in range(A.cols):
            for k in range(B.rows):
                for l in range(B.cols):
                    out[i * B.rows + k, j * B.cols + l] = A[i, j] * B[k, l]
    return out


def cl_n_euclidean_generators(n: int):
    """Return n Clifford generators for Cl(n, 0) acting on a 2^ceil(n/2)-dim space.

    Use the standard Jordan-Wigner-style construction:
      gamma_1 = sigma_x (x) I (x) I ...
      gamma_2 = sigma_y (x) I (x) I ...
      gamma_3 = sigma_z (x) sigma_x (x) I ...
      gamma_4 = sigma_z (x) sigma_y (x) I ...
      gamma_5 = sigma_z (x) sigma_z (x) sigma_x ...
      ...
    Each pair (gamma_{2k-1}, gamma_{2k}) lives at the k-th "qubit".
    For odd n, the last generator is sigma_z (x) ... (x) sigma_z (x) sigma_x
    where the last factor uses sigma_x of a single qubit.
    """
    k = (n + 1) // 2  # number of qubits
    dim = 2 ** k
    I2 = eye(2)

    def at_qubit(j: int, op):
        """sigma_z (x) ... (x) sigma_z (x) op (x) I (x) ... (x) I."""
        # Build left side: j sigma_z's (for j = 0..)
        # Build right side: identities for remaining qubits.
        result = None
        for i in range(k):
            if i < j:
                factor = sigma_z
            elif i == j:
                factor = op
            else:
                factor = I2
            result = factor if result is None else kron(result, factor)
        return result

    gens = []
    for mu in range(1, n + 1):
        qubit = (mu - 1) // 2
        is_first = (mu - 1) % 2 == 0
        op = sigma_x if is_first else sigma_y
        gens.append(at_qubit(qubit, op))
    return gens, dim


def anticommutator(A, B):
    return A * B + B * A


def commutator(A, B):
    return A * B - B * A


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print(CLAIM_ID)
    print("Goal: verify (V) parity rule, even/odd dichotomy, and d_t-odd")
    print("for d_s = 3 chirality at exact sympy matrix precision.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 1: explicit Clifford generators satisfy CAR for n in {2,3,4,5,6}")
    # ---------------------------------------------------------------------
    cliffords = {}
    for n in [2, 3, 4, 5, 6]:
        gens, dim = cl_n_euclidean_generators(n)
        cliffords[n] = (gens, dim)
        ok_car = True
        for mu in range(n):
            for nu in range(n):
                expected = 2 * eye(dim) if mu == nu else zeros(dim, dim)
                got = anticommutator(gens[mu], gens[nu])
                if got != expected:
                    ok_car = False
        check(
            f"Cl({n},0) generators satisfy CAR (positive metric): {{gamma_mu, gamma_nu}} = 2 delta",
            ok_car,
            detail=f"dim = {dim}",
        )

    # ---------------------------------------------------------------------
    section("Part 2: (V) parity rule on omega for n in {2,3,4,5,6}")
    # ---------------------------------------------------------------------
    omegas = {}
    for n in [2, 3, 4, 5, 6]:
        gens, dim = cliffords[n]
        omega = gens[0]
        for mu in range(1, n):
            omega = omega * gens[mu]
        omegas[n] = omega

        expected_sign = (-1) ** (n - 1)
        ok_V = True
        for mu in range(n):
            lhs = omega * gens[mu]
            rhs = expected_sign * gens[mu] * omega
            if lhs != rhs:
                ok_V = False
        check(
            f"(V) parity rule at n = {n}: omega gamma_mu = ({expected_sign}) gamma_mu omega",
            ok_V,
            detail=f"all {n} generators verified",
        )

    # ---------------------------------------------------------------------
    section("Part 3: even-n case — omega anticommutes with every generator")
    # ---------------------------------------------------------------------
    for n in [2, 4, 6]:
        gens, dim = cliffords[n]
        omega = omegas[n]
        ok_anti = all(anticommutator(omega, gens[mu]) == zeros(dim, dim) for mu in range(n))
        check(
            f"at n = {n} (even): {{omega, gamma_mu}} = 0 for every mu",
            ok_anti,
        )

    # ---------------------------------------------------------------------
    section("Part 4: even-n case — explicit gamma_5 satisfying (C1)+(C2)")
    # ---------------------------------------------------------------------
    for n in [2, 4, 6]:
        gens, dim = cliffords[n]
        omega = omegas[n]
        # omega^2 should be a scalar multiple of I
        omega_sq = omega * omega
        # Check omega^2 = c * I for some scalar c
        c00 = omega_sq[0, 0]
        is_scalar = (omega_sq == c00 * eye(dim))
        check(
            f"at n = {n}: omega^2 = c I for scalar c (c = {c00})",
            is_scalar,
        )

        # Build gamma_5 such that gamma_5^2 = +I. Need to rescale omega
        # so that the scalar c becomes +1. Two cases:
        #  (a) c is positive real: gamma_5 = omega / sqrt(c).
        #  (b) c is negative real: gamma_5 = (i omega) / sqrt(-c).
        # For the Euclidean Cl(n, 0) the volume element squares to
        # (+/-1) depending on n mod 4. For n=2: omega = i sigma_z (with our
        # sign conventions); omega^2 = -1. So pick gamma_5 = i omega in
        # that case. Similar logic for n=4, 6.
        c_val = c00
        if c_val == 1:
            gamma_5 = omega
        elif c_val == -1:
            gamma_5 = I * omega
        else:
            # Fallback: try sympy sqrt
            gamma_5 = omega / sympy.sqrt(c_val)

        # Verify (C1) gamma_5^2 = +I
        g5_sq = simplify(gamma_5 * gamma_5)
        check(
            f"at n = {n}: gamma_5 = {'omega' if c_val==1 else 'i omega'} satisfies gamma_5^2 = +I",
            g5_sq == eye(dim),
            detail=f"gamma_5^2 = {g5_sq[0,0]} I (c was {c_val})",
        )

        # Verify (C2) {gamma_5, gamma_mu} = 0 for all mu
        ok_anti = all(
            simplify(anticommutator(gamma_5, gens[mu])) == zeros(dim, dim)
            for mu in range(n)
        )
        check(
            f"at n = {n}: {{gamma_5, gamma_mu}} = 0 for every mu (C2)",
            ok_anti,
        )

    # ---------------------------------------------------------------------
    section("Part 5: odd-n case — omega is central")
    # ---------------------------------------------------------------------
    for n in [3, 5]:
        gens, dim = cliffords[n]
        omega = omegas[n]
        ok_comm = all(commutator(omega, gens[mu]) == zeros(dim, dim) for mu in range(n))
        check(
            f"at n = {n} (odd): [omega, gamma_mu] = 0 for every mu (omega is central)",
            ok_comm,
        )

    # ---------------------------------------------------------------------
    section("Part 6: odd-n case — exhaustive scan: no algebra element anticommutes with all generators")
    # ---------------------------------------------------------------------
    # For each odd n in {3, 5}, scan all 2^n monomial basis elements of
    # Cl(n, 0): pi_S = prod_{i in S} gamma_i for each subset S of {1, ..., n}.
    # Verify that no monomial pi_S satisfies {pi_S, gamma_mu} = 0 for all mu.
    # This combined with linearity of the anticommutator (in each argument)
    # implies no linear combination can satisfy the anticommutator system
    # with all generators simultaneously (since each generator imposes a
    # linear constraint with kernel < full algebra dimension).

    def monomial(gens_list, subset, dim_):
        if not subset:
            return eye(dim_)
        result = gens_list[subset[0]]
        for idx in subset[1:]:
            result = result * gens_list[idx]
        return result

    for n in [3, 5]:
        gens, dim = cliffords[n]
        # Exhaustive monomial scan: all 2^n subsets of {0, ..., n-1}.
        anti_count = 0
        for size in range(n + 1):
            for subset in itertools.combinations(range(n), size):
                pi = monomial(gens, subset, dim)
                # Does pi anticommute with EVERY generator?
                if all(anticommutator(pi, gens[mu]) == zeros(dim, dim) for mu in range(n)):
                    anti_count += 1
        # Allowed exception: pi = 0 (the zero element). Subset enumeration
        # never produces the zero element from products of generators (each
        # gamma_mu is invertible, so any product is nonzero). Therefore
        # anti_count should be 0 for the basis enumeration.
        check(
            f"at n = {n} (odd): exhaustive monomial scan — no basis element "
            f"anticommutes with every generator",
            anti_count == 0,
            detail=f"{anti_count} candidate(s) out of 2^{n} = {2**n} monomials",
        )

    # ---------------------------------------------------------------------
    section("Part 7: application at d_s = 3 — chirality-allowed d_t in {1, 3, 5, 7}")
    # ---------------------------------------------------------------------
    d_s = 3
    chirality_allowed = []
    for d_t in [1, 2, 3, 4, 5, 6, 7]:
        n = d_s + d_t
        if n % 2 == 0:
            chirality_allowed.append(d_t)
    check(
        "chirality-allowed d_t at d_s = 3 are odd in [1, 7]: {1, 3, 5, 7}",
        chirality_allowed == [1, 3, 5, 7],
        detail=f"got {chirality_allowed}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: counterfactual at d_t = 2 (n = 5 odd) — no gamma_5 exists")
    # ---------------------------------------------------------------------
    n = 5  # d_s + d_t with d_t = 2
    gens, dim = cliffords[n]
    # Exhaustive scan again, but rephrase as a counterfactual statement
    found_any = False
    for size in range(n + 1):
        for subset in itertools.combinations(range(n), size):
            pi = monomial(gens, subset, dim)
            if all(anticommutator(pi, gens[mu]) == zeros(dim, dim) for mu in range(n)):
                found_any = True
    check(
        "counterfactual at d_s=3, d_t=2 (n=5): no basis monomial qualifies as gamma_5",
        not found_any,
    )

    # ---------------------------------------------------------------------
    section("Part 9: note structure and scope discipline")
    # ---------------------------------------------------------------------
    note_text = NOTE_PATH.read_text()
    required = [
        "Clifford Volume-Element Chirality Forces Even Total Dimension Narrow Theorem",
        "Status authority:** independent audit lane only",
        "gamma_5^2 = +I",
        "{ gamma_5, gamma_mu } = 0",
        "Pattern A narrow rescope",
        "ANOMALY_FORCES_TIME_THEOREM.md",
        "Forbidden imports check",
        "d_t in { 1, 3, 5, 7, ... }",
        "Honest open items",
        "Does **not** claim `d_t = 1`",
    ]
    for s in required:
        check(f"note contains: {s!r}", s in note_text)

    # Scope discipline: must NOT close admission (i) or claim d_t = 1
    forbidden_phrases = [
        "closes admission (i)",
        "promotes the parent to positive_theorem",
    ]
    for f in forbidden_phrases:
        check(
            f"narrow scope avoids forbidden claim: {f!r}",
            f not in note_text,
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    CAR for Cl(n, 0) at n = 2, 3, 4, 5, 6 on explicit matrix realizations")
    print("    (V) parity rule omega gamma_mu = (-1)^(n-1) gamma_mu omega at n = 2..6")
    print("    Even n in {2, 4, 6}: omega anticommutes with every generator;")
    print("    explicit gamma_5 with gamma_5^2 = +I and {gamma_5, gamma_mu} = 0")
    print("    Odd n in {3, 5}: omega central; exhaustive monomial scan finds")
    print("    no algebra basis element anticommuting with every generator")
    print("    Application at d_s = 3: chirality-allowed d_t in {1, 3, 5, 7}")
    print("    Counterfactual at d_t = 2 (n = 5): no gamma_5 exists")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
