#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15`
(claim_type=positive_theorem, audit_status=audited_conditional, td=111,
load_bearing_step_class=C).

The parent's load-bearing step is the residual-Z_2-parity preservation
argument:

  - the weak-axis split d = diag(a, b, b) is residual-Z_2 even under
    P_{23} (transposition swap of indices 2, 3);
  - the Z_3-bridged Dirac surface Y_even = U_Z3^dagger d U_Z3 stays
    residual-Z_2 even;
  - the Hermitian kernel H = Y_even^dagger Y_even is residual-Z_2 even
    and has zero odd-circulant coefficient (Im H_01 = 0);
  - equivariant functionals (Y^dag Y, symmetrization, resolvent, etc.)
    preserve residual-Z_2 evenness;
  - circulant from even data c_even = d I + r (S + S^2) has c_odd = 0;
  - circulant + i r (S - S^2) breaks evenness and gives c_odd != 0.

The existing primary runner verifies these at numpy float precision
with 1e-10 to 1e-12 tolerance. This Pattern B companion verifies the
same algebra at sympy `Rational` exact precision -- including the
Z_3-bridge U_Z3 with omega = exp(2 pi i/3), so all parity tests close
with exact-zero residuals (not just within 1e-12).

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's load-bearing class-(C)
parity-preservation step holds at exact symbolic precision. Does not
modify the parent's audit_status; that decision belongs to the audit
lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros, exp, I as sym_I, pi, sqrt, conjugate, im, re
except ImportError:
    print("FAIL: sympy required for exact algebra")
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
    tag = "PASS (C)" if ok else "FAIL (C)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


def matrix_simplify(M):
    """Apply trig rewrite + complex-expand + simplify elementwise."""
    return M.applyfunc(lambda e: simplify(e.rewrite(sympy.cos).expand(complex=True)))


# ============================================================================
section("Audit companion for dm_neutrino_odd_circulant_current_stack_zero_law (td=111)")
# Goal: exact symbolic verification of the residual-Z_2 parity-preservation
# argument and the c_odd = 0 conclusion at sympy exact precision.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: build symbolic generators S, S^2, P_{23}, U_Z3 at exact precision")
# ----------------------------------------------------------------------------
# 3-cycle S
S_mat = Matrix([[0, 1, 0],
                [0, 0, 1],
                [1, 0, 0]])
S2_mat = S_mat * S_mat
S3_mat = S_mat * S_mat * S_mat
check("S^3 = I exact",
      S3_mat == eye(3))

# Residual Z_2 transposition P_{23}
P23 = Matrix([[1, 0, 0],
              [0, 0, 1],
              [0, 1, 0]])
check("P_{23}^2 = I exact (involution)",
      P23 * P23 == eye(3))

# Z_3 bridge: U_Z3 = (1/sqrt(3)) * [[1,1,1],[1,omega,omega^2],[1,omega^2,omega]]
omega = exp(sym_I * 2 * pi / Rational(3))
U_Z3 = Matrix([
    [1, 1, 1],
    [1, omega, omega**2],
    [1, omega**2, omega],
]) / sqrt(Rational(3))

# Verify U_Z3 is unitary: U_Z3^dag U_Z3 = I
U_Z3_dag = U_Z3.H
prod = matrix_simplify(U_Z3_dag * U_Z3)
check("U_Z3^dag U_Z3 = I_3 exact (Z_3 bridge is unitary)",
      simplify(prod - eye(3)) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 2: weak-axis split d = diag(a, b, b) is residual-Z_2 even")
# ----------------------------------------------------------------------------
a_sym, b_sym = symbols('a b', complex=True)
d_split = sympy.diag(a_sym, b_sym, b_sym)

# P_{23} d P_{23}^dag = d
parity_d = simplify(P23 * d_split * P23.T - d_split)
check("P_{23} d P_{23}^dag = d exact (d is residual-Z_2 even, symbolic in a, b)",
      parity_d == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 3: bridged Dirac surface Y_even = U_Z3^dag d U_Z3 stays residual-Z_2 even")
# ----------------------------------------------------------------------------
# To allow symbolic parity check with omega, we evaluate at concrete rational
# values for (a, b) and verify Y_even is residual-Z_2 even at exact symbolic
# precision via sympy's complex expansion.
a_val = Rational(7, 5)
b_val = Rational(4, 5)
d_concrete = sympy.diag(a_val, b_val, b_val)

Y_even = U_Z3_dag * d_concrete * U_Z3
Y_even = matrix_simplify(Y_even)

parity_Y = matrix_simplify(P23 * Y_even * P23.T - Y_even)
check("P_{23} Y_even P_{23}^dag = Y_even exact (bridged Dirac surface is residual-Z_2 even)",
      parity_Y == zeros(3, 3),
      detail=f"a = {a_val}, b = {b_val}")


# ----------------------------------------------------------------------------
section("Part 4: H_even = Y_even^dag Y_even is Z_2-even with c_odd = Im(H_01) = 0")
# ----------------------------------------------------------------------------
H_even = matrix_simplify(Y_even.H * Y_even)

parity_H = matrix_simplify(P23 * H_even * P23.T - H_even)
check("P_{23} H_even P_{23}^dag = H_even exact",
      parity_H == zeros(3, 3))

# c_odd is defined as Im(H[0, 1]).
H_01 = simplify(H_even[0, 1])
H_01_imag = simplify(im(H_01))
check("c_odd = Im(H_even[0, 1]) = 0 exact",
      H_01_imag == 0,
      detail=f"H[0,1] = {H_01}, Im(H[0,1]) = {H_01_imag}")


# ----------------------------------------------------------------------------
section("Part 5: equivariant functionals of Y_even preserve residual-Z_2 evenness")
# ----------------------------------------------------------------------------
# Test functionals: Y^dag Y, Hermitian symmetrization, Hermitian quadratic combo.
def parity_check(label, M):
    M_simplified = matrix_simplify(M)
    parity_diff = matrix_simplify(P23 * M_simplified * P23.T - M_simplified)
    odd_coeff = simplify(im(M_simplified[0, 1]))
    return parity_diff == zeros(3, 3), odd_coeff == 0, M_simplified

f1 = Y_even.H * Y_even  # Y^dag Y
f2 = Y_even + Y_even.H  # Hermitian symmetrization
f3 = Y_even.H * Y_even + Rational(3, 10) * (Y_even + Y_even.H) + Rational(2, 10) * eye(3)  # quadratic combo

for label, M in [("Y^dag Y", f1), ("Y + Y^dag", f2), ("Y^dag Y + 0.3(Y + Y^dag) + 0.2 I", f3)]:
    even_ok, odd_zero, _ = parity_check(label, M)
    check(f"functional '{label}': residual-Z_2 even",
          even_ok)
    check(f"functional '{label}': c_odd = 0",
          odd_zero)


# ----------------------------------------------------------------------------
section("Part 6: circulant from even data has c_odd = 0; odd perturbation breaks it")
# ----------------------------------------------------------------------------
mu_sym, nu_sym = symbols('mu nu', real=True)
circulant_even = mu_sym * eye(3) + nu_sym * (S_mat + S2_mat)
# c_odd of circulant_even = Im(K_01)
c_odd_even = simplify(im(circulant_even[0, 1]))
check("circulant from even data c_even = mu I + nu(S + S^2) has c_odd = 0 exact",
      c_odd_even == 0,
      detail=f"K[0,1] = {circulant_even[0, 1]}, Im = {c_odd_even}")

# Odd perturbation: + i r (S - S^2)
r_sym = symbols('r', positive=True, real=True)
circulant_odd = circulant_even + sym_I * r_sym * (S_mat - S2_mat)
c_odd_perturbed = simplify(im(circulant_odd[0, 1]))
check("circulant + i r (S - S^2) has c_odd = r != 0 (odd perturbation breaks evenness)",
      simplify(c_odd_perturbed - r_sym) == 0,
      detail=f"K[0,1] = {circulant_odd[0, 1]}, Im = {c_odd_perturbed}")

# Verify the odd perturbation breaks residual-Z_2 evenness as well.
parity_odd_pert = simplify(P23 * circulant_odd * P23.T - circulant_odd)
check("circulant + i r (S - S^2) breaks residual-Z_2 evenness",
      parity_odd_pert != zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 7: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15', {})
print(f"\n  dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-C load-bearing step (first-principles compute / parity preservation)",
      parent.get('load_bearing_step_class') == 'C',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(C) residual-Z_2 parity-preservation
  argument:

    weak-axis split d = diag(a, b, b) is Z_2 even (P_23 d P_23^T = d);
    Z_3-bridged Y_even = U_Z3^dag d U_Z3 stays Z_2 even at exact omega;
    H_even = Y_even^dag Y_even has c_odd = Im(H_even[0, 1]) = 0 exact;
    equivariant functionals of Y_even preserve evenness exact;
    circulant from even data has c_odd = 0; odd perturbation breaks it.

  The existing primary runner verifies these at numpy float precision
  (1e-10 to 1e-12 tolerance); this companion reduces those errors to
  exact symbolic zero via sympy `rewrite(cos).expand(complex=True)`
  reductions on the cube-root-of-unity expressions in U_Z3.

  Audit-lane class for the parent's load-bearing step:
    (C) — first-principles compute / parity preservation. No external
    observed/fitted/literature input.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the
  upstream weak-axis split / Z_3 bridge / DM-circulant authorities.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
