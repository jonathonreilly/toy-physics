#!/usr/bin/env python3
"""Pattern B audit-companion runner for the existing EW Fierz row.

The parent note's primary runner verifies the Fierz channel ratio
(N_c^2 - 1)/N_c^2 at N_c = 3. This companion adds exact algebraic checks:
the closed-form singlet/adjoint fractions are verified symbolically, sampled
at exact rational precision, and cross-checked against explicit normalized
SU(N_c) generator completeness for N_c = 2, 3, 4.

Companion role: not a new claim row, not a new source note, and not an audit
verdict. It supplies focused class-(A) evidence for the parent row's
load-bearing algebraic step.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import I, Rational, diag, simplify, sqrt, symbols, trace, zeros
except ImportError:
    print("FAIL: sympy required")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Audit companion for ew_current_fierz_channel_decomposition_note_2026-05-01")
# Goal: exact-precision verification of Fierz channel ratio at general N_c
# ============================================================================

# The Fierz identity for SU(N_c) gives, on the q-qbar bilinear space:
#   N_c x N_c-bar = 1 (singlet) + (N_c^2 - 1) (adjoint)
# Channel-count fraction:
#   F_singlet = 1 / N_c^2
#   F_adjoint = (N_c^2 - 1) / N_c^2 = 1 - 1/N_c^2
#
# This is a pure dimension-counting identity on irreducible representations
# of SU(N_c) acting on N_c x N_c-bar = N_c^2 states.

def channel_fractions(N_c):
    F_singlet = Rational(1, N_c * N_c)
    F_adjoint = Rational(N_c * N_c - 1, N_c * N_c)
    return F_singlet, F_adjoint


def matrix_unit(N_c, row, col):
    matrix = zeros(N_c, N_c)
    matrix[row, col] = 1
    return matrix


def su_n_generators(N_c):
    """Return the standard Hermitian SU(N) generators with Tr(T_a T_b)=1/2 delta_ab."""
    generators = []
    for j in range(N_c):
        for k in range(j + 1, N_c):
            e_jk = matrix_unit(N_c, j, k)
            e_kj = matrix_unit(N_c, k, j)
            generators.append((e_jk + e_kj) / 2)
            generators.append(-I * (e_jk - e_kj) / 2)

    for ell in range(1, N_c):
        entries = [1] * ell + [-ell] + [0] * (N_c - ell - 1)
        generators.append(diag(*entries) / sqrt(2 * ell * (ell + 1)))

    return generators


def delta(a, b):
    return 1 if a == b else 0


def is_traceless(generator):
    return simplify(trace(generator)) == 0


def is_hermitian(generator):
    n_rows, n_cols = generator.shape
    return all(
        simplify(generator[i, j] - sympy.conjugate(generator[j, i])) == 0
        for i in range(n_rows)
        for j in range(n_cols)
    )


def trace_normalization_holds(generators):
    for a, lhs_generator in enumerate(generators):
        for b, rhs_generator in enumerate(generators):
            expected = Rational(1, 2) if a == b else 0
            observed = simplify(trace(lhs_generator * rhs_generator))
            if observed != expected:
                return False, f"a={a}, b={b}: Tr(T_a T_b)={observed}, expected {expected}"
    return True, "Tr(T_a T_b)=1/2 delta_ab for all generator pairs"


def fierz_completeness_holds(N_c, generators):
    for i in range(N_c):
        for j in range(N_c):
            for k in range(N_c):
                for ell in range(N_c):
                    lhs = sum(generator[i, j] * generator[k, ell] for generator in generators)
                    rhs = Rational(1, 2) * (
                        delta(i, ell) * delta(j, k)
                        - Rational(1, N_c) * delta(i, j) * delta(k, ell)
                    )
                    if simplify(lhs - rhs) != 0:
                        return (
                            False,
                            f"indices {(i, j, k, ell)}: lhs={simplify(lhs)}, rhs={rhs}",
                        )
    return True, f"all {N_c ** 4} tensor entries match exactly"


# ----------------------------------------------------------------------------
section("Part 1: symbolic channel-fraction identity")
# ----------------------------------------------------------------------------
N = symbols("N", integer=True, positive=True)
F_s_symbolic = 1 / N**2
F_a_symbolic = (N**2 - 1) / N**2

check("F_singlet(N) + F_adjoint(N) = 1 symbolically",
      simplify(F_s_symbolic + F_a_symbolic - 1) == 0,
      detail=f"F_s={F_s_symbolic}, F_a={F_a_symbolic}")
check("F_adjoint(N) = 1 - 1/N^2 symbolically",
      simplify(F_a_symbolic - (1 - 1 / N**2)) == 0)


# ----------------------------------------------------------------------------
section("Part 2: SU(N_c) channel fractions at exact rational precision")
# ----------------------------------------------------------------------------
for N_c in [2, 3, 4, 5, 7, 10, 100]:
    F_s, F_a = channel_fractions(N_c)
    # Sum to 1
    check(f"N_c={N_c}: F_singlet + F_adjoint = 1 exactly",
          F_s + F_a == 1,
          detail=f"F_s = {F_s}, F_a = {F_a}")
    # Adjoint dim = N_c² − 1
    check(f"N_c={N_c}: F_adjoint = (N_c^2-1)/N_c^2 = {N_c*N_c-1}/{N_c*N_c}",
          F_a == Rational(N_c * N_c - 1, N_c * N_c))


# ----------------------------------------------------------------------------
section("Part 3: at N_c = 3, F_adjoint = 8/9 (parent note's central value)")
# ----------------------------------------------------------------------------
F_s_3, F_a_3 = channel_fractions(3)
check("F_adjoint(N_c=3) = 8/9 exactly",
      F_a_3 == Rational(8, 9),
      detail=f"F_adjoint = {F_a_3}")
check("F_singlet(N_c=3) = 1/9 exactly",
      F_s_3 == Rational(1, 9),
      detail=f"F_singlet = {F_s_3}")
check("F_singlet + F_adjoint = 1 (probability conservation)",
      F_s_3 + F_a_3 == 1)


# ----------------------------------------------------------------------------
section("Part 4: sampled large-N_c monotonic approach")
# ----------------------------------------------------------------------------
# For increasing sampled N_c, F_adjoint approaches 1 and F_singlet approaches
# 0 as 1/N_c^2. The symbolic identity above is the general statement; these
# checks are exact samples, not a separate universal proof.
sampled_N = [2, 3, 4, 5, 10, 100]
for previous_N, current_N in zip(sampled_N, sampled_N[1:]):
    _, previous_F_a = channel_fractions(previous_N)
    _, current_F_a = channel_fractions(current_N)
    check(f"F_adjoint(N_c={current_N}) = {current_F_a} > F_adjoint(N_c={previous_N})",
          current_F_a > previous_F_a,
          detail="sampled exact monotonic increase toward 1")


# ----------------------------------------------------------------------------
section("Part 5: explicit SU(N_c) generator Fierz completeness")
# ----------------------------------------------------------------------------
for N_c in [2, 3, 4]:
    expected_adjoint_dim = N_c * N_c - 1
    expected_singlet_dim = 1
    expected_total = N_c * N_c

    generators = su_n_generators(N_c)
    check(f"SU({N_c}): generator count is N_c^2 - 1",
          len(generators) == expected_adjoint_dim,
          detail=f"count={len(generators)}, expected={expected_adjoint_dim}")
    check(f"SU({N_c}): generators are traceless and Hermitian",
          all(is_traceless(g) and is_hermitian(g) for g in generators))
    normalization_ok, normalization_detail = trace_normalization_holds(generators)
    check(f"SU({N_c}): generator trace normalization",
          normalization_ok,
          detail=normalization_detail)
    fierz_ok, fierz_detail = fierz_completeness_holds(N_c, generators)
    check(f"SU({N_c}): Fierz completeness tensor identity",
          fierz_ok,
          detail=fierz_detail)
    check(f"SU({N_c}): adjoint_dim + singlet_dim = N_c^2",
          expected_adjoint_dim + expected_singlet_dim == expected_total,
          detail=f"{expected_adjoint_dim} + {expected_singlet_dim} = {expected_total}")


# ----------------------------------------------------------------------------
section("Part 6: parent row ledger compatibility")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
allowed_dependency_statuses = {'retained', 'retained_bounded', 'retained_no_go'}

parent_id = "ew_current_fierz_channel_decomposition_note_2026-05-01"
parent_row = rows.get(parent_id, {})
print(f"\n  {parent_id} current ledger state:")
print(f"    transitive_descendants: {parent_row.get('transitive_descendants')}")
print(f"    deps: {parent_row.get('deps')}")

deps = parent_row.get('deps') or []
expected_deps = {'native_gauge_closure_note', 'graph_first_su3_integration_note'}
dependency_closes = all(rows.get(d, {}).get('effective_status') in allowed_dependency_statuses for d in deps)
check(f"{parent_id} exists in the audit ledger",
      bool(parent_row))
check(f"{parent_id} has the expected load-bearing deps",
      set(deps) == expected_deps,
      detail=f"deps: {deps}")
check(f"{parent_id} deps satisfy review-loop closure policy",
      dependency_closes,
      detail=f"deps: {deps}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT rational verification of the SU(N_c)
  Fierz channel-fraction identity F_adjoint = (N_c^2 - 1)/N_c^2 by
  symbolic algebra, exact rational samples, and explicit generator
  completeness checks for SU(2), SU(3), and SU(4). This demonstrates that
  the parent note's central result at N_c = 3 (= 8/9) is the finite-N_c
  specialization of the class-(A) algebraic identity, not a numerical fit.

  Audit-lane class for the parent note's load-bearing step:
    (A) — algebraic dimension-counting identity on irreducible SU(N_c)
    representations. No external observed/fitted/literature input.

  This companion does NOT introduce a new claim row and does NOT set an
  audit verdict. It gives focused class-(A) breakdown evidence on the
  parent row's load-bearing step.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
