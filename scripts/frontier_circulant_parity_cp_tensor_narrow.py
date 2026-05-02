#!/usr/bin/env python3
"""Pattern A narrow runner for `CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone linear-algebra / parity-decomposition identity:

  Let S be the 3x3 cyclic permutation matrix and P_{23} the residual-Z_2
  transposition swapping basis indices 2 and 3. Define the Hermitian
  circulant family
      K(d, c_even, c_odd) = d I + c_even (S + S^2) + i c_odd (S - S^2),
  with d, c_even, c_odd ∈ R.

  THEN:
    (i)   P_{23} S P_{23} = S^2 (and conversely);
    (ii)  P_{23} I P_{23} = I; P_{23} (S + S^2) P_{23} = S + S^2;
    (iii) P_{23} (i (S - S^2)) P_{23} = -i (S - S^2);
    (iv)  hence d, c_even are residual-Z_2 even coefficients and c_odd is
          residual-Z_2 odd;
    (v)   the CP-tensor formula on K is
              Im[(K_01)^2] = 2 c_even c_odd;
    (vi)  c_odd = 0 forces Im[(K_01)^2] = 0;
    (vii) c_odd != 0 with c_even != 0 gives a nonzero value of this scalar.

This is pure linear algebra on 3x3 Hermitian circulants and the
residual Z_2 transposition. No DM-side / DM-circulant CP / two-Higgs
right-Gram bridge / weak-axis-1+2 split / standard CP tensor readout
authority is consumed; the narrow theorem treats (d, c_even, c_odd) as
abstract real symbols.

Companion role: this is a Pattern A new narrow claim row carving out the
algebraic core from `dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15`.
The narrow theorem isolates the parity-decomposition + CP-tensor algebra on
Hermitian circulants from any DM-side / Wilson-environment / weak-axis-split
framework-specific input.
"""

import sys

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros, I as sym_I, im, re
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (C)" if ok else "FAIL (C)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: Hermitian circulant parity + CP tensor")
# Statement: parity-decomposition of the Hermitian circulant family under
# residual-Z_2 transposition + CP-tensor formula Im[(K_01)^2] = 2 c_even
# c_odd. Pure linear algebra on 3x3 matrices.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: build S, S^2, P_{23} and verify P_{23} S P_{23} = S^2")
# ----------------------------------------------------------------------------
S = Matrix([[0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]])
S2 = S * S
S3 = S * S * S
I3 = eye(3)

P23 = Matrix([[1, 0, 0],
              [0, 0, 1],
              [0, 1, 0]])

check("S^3 = I exact",
      S3 == I3)
check("P_{23}^2 = I exact (involution)",
      P23 * P23 == I3)

# Residual-Z_2 swap: P_{23} S P_{23} = S^2
swap_S = simplify(P23 * S * P23 - S2)
check("P_{23} S P_{23} = S^2 exact (Z_2 swap)",
      swap_S == zeros(3, 3))

swap_S2 = simplify(P23 * S2 * P23 - S)
check("P_{23} S^2 P_{23} = S exact (inverse direction)",
      swap_S2 == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 2: I and (S + S^2) are Z_2-even; (S - S^2) is Z_2-odd up to factor i")
# ----------------------------------------------------------------------------
even_basis_I = simplify(P23 * I3 * P23 - I3)
check("P_{23} I P_{23} = I exact (I is Z_2-even)",
      even_basis_I == zeros(3, 3))

even_basis_sum = simplify(P23 * (S + S2) * P23 - (S + S2))
check("P_{23} (S + S^2) P_{23} = (S + S^2) exact (Z_2-even)",
      even_basis_sum == zeros(3, 3))

# Z_2-odd basis: i(S - S^2). Under P_23: P_23 (S - S^2) P_23 = (S^2 - S) = -(S - S^2),
# and Hermitian "i" is itself fixed (a scalar), so i(S - S^2) -> -i(S - S^2).
odd_basis_diff = simplify(P23 * (S - S2) * P23 - (-(S - S2)))
check("P_{23} (S - S^2) P_{23} = -(S - S^2) exact (sign-flip)",
      odd_basis_diff == zeros(3, 3))

# P_{23} [i(S - S^2)] P_{23} = -i(S - S^2)
odd_basis = simplify(P23 * (sym_I * (S - S2)) * P23 - (-sym_I * (S - S2)))
check("P_{23} [i(S - S^2)] P_{23} = -i(S - S^2) exact (Z_2-odd)",
      odd_basis == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 3: K(d, c_even, c_odd) parity decomposition")
# ----------------------------------------------------------------------------
d, c_even, c_odd = symbols('d c_even c_odd', real=True)
K = d * I3 + c_even * (S + S2) + sym_I * c_odd * (S - S2)

# K is Hermitian
K_dagger = K.H
check("K is Hermitian (K = K^dagger)",
      simplify(K - K_dagger) == zeros(3, 3))

# Parity transform: P_{23} K P_{23}
K_parity = simplify(P23 * K * P23)
expected_parity = d * I3 + c_even * (S + S2) - sym_I * c_odd * (S - S2)
check("P_{23} K P_{23} = d I + c_even(S+S^2) - i c_odd(S-S^2) (parity sends c_odd -> -c_odd)",
      simplify(K_parity - expected_parity) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 4: CP-tensor formula Im[(K_01)^2] = 2 c_even c_odd")
# ----------------------------------------------------------------------------
# K_01 = K[0, 1] (first row, second column)
K_01 = K[0, 1]
print(f"\n  K[0, 1] = {K_01}")

K_01_squared = simplify(K_01**2)
print(f"  K[0, 1]^2 = {K_01_squared}")

K_01_squared_imag = simplify(im(K_01_squared))
expected_cp_tensor = 2 * c_even * c_odd
check("Im[(K_01)^2] = 2 c_even c_odd exact",
      simplify(K_01_squared_imag - expected_cp_tensor) == 0,
      detail=f"Im[K_01^2] = {K_01_squared_imag}")


# ----------------------------------------------------------------------------
section("Part 5: vanishing of Im[(K_01)^2] at c_odd = 0")
# ----------------------------------------------------------------------------
K_even_only = K.subs(c_odd, 0)
K01_even = K_even_only[0, 1]
K01_even_squared_imag = simplify(im(K01_even**2))
check("c_odd = 0 forces Im[(K_01)^2] = 0 exact",
      K01_even_squared_imag == 0,
      detail=f"Im[K_01^2] at c_odd = 0 = {K01_even_squared_imag}")


# ----------------------------------------------------------------------------
section("Part 6: nonzero scalar at concrete instance (d, c_even, c_odd) = (1, 1/3, 1/5)")
# ----------------------------------------------------------------------------
sub = {d: Rational(1), c_even: Rational(1, 3), c_odd: Rational(1, 5)}
K_concrete = K.subs(sub)
K01_concrete = K_concrete[0, 1]
K01_concrete_squared_imag = simplify(im(K01_concrete**2))
expected_cp_concrete = 2 * Rational(1, 3) * Rational(1, 5)  # = 2/15
check("Im[(K_01)^2] = 2 c_even c_odd = 2/15 at (1, 1/3, 1/5)",
      simplify(K01_concrete_squared_imag - expected_cp_concrete) == 0,
      detail=f"Im[K_01^2] = {K01_concrete_squared_imag}, expected = {expected_cp_concrete}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let S be the 3x3 cyclic permutation matrix and P_{23} the residual-Z_2
    transposition (swap of indices 2, 3). Consider the Hermitian circulant
    family
        K(d, c_even, c_odd) = d I + c_even (S + S^2) + i c_odd (S - S^2),
    with d, c_even, c_odd ∈ R.

  CONCLUSION:
    (i)   P_{23} S P_{23} = S^2 (residual-Z_2 swap of S, S^2);
    (ii)  I and (S + S^2) are residual-Z_2-even; i(S - S^2) is residual-Z_2-odd;
    (iii) P_{23} K P_{23} sends c_odd -> -c_odd, leaves d, c_even fixed;
    (iv)  Im[(K_01)^2] = 2 c_even c_odd  (exact CP-tensor formula);
    (v)   c_odd = 0 forces Im[(K_01)^2] = 0.

  Audit-lane class:
    pure linear algebra on 3x3 Hermitian circulants and a residual Z_2
    transposition. No DM-side / Wilson-environment / weak-axis-split / two-Higgs
    right-Gram / standard CP tensor readout authority consumed.

  This narrow theorem isolates the circulant parity decomposition + CP-tensor
  formula from any DM-side framework-specific framing, so it can be
  checked independently of the parent's authority-stack inputs.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
