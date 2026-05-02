#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_dirac_bridge_theorem_note_2026-04-15`
(claim_type=positive_theorem, audit_status=audited_conditional, td=115,
load_bearing_step_class=C).

The parent's load-bearing step bundles two distinct components:

(a) Algebraic content (in-scope of this companion):
    - Gamma_1, Gamma_2, Gamma_3 are Hermitian involutions on a Cl(4)
      Euclidean Dirac representation;
    - Gamma_i Gamma_j + Gamma_j Gamma_i = 2 delta_{ij} I (Clifford);
    - {Gamma_i, gamma_5} = 0 (chiral off-diagonal);
    - M(phi) = sum_i phi_i Gamma_i is Hermitian;
    - M(phi)^2 = |phi|^2 I;
    - P_L M(phi) P_L = P_R M(phi) P_R = 0;
    - M(phi) at axis vector e_i equals Gamma_i.

(b) The selector V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 has minima at the
    axis vectors -- this is a calculus-of-variations claim that the
    audit verdict identifies as depending on the unaudited weak-axis
    branch convention. Out of scope of this companion.

This Pattern B companion verifies the in-scope algebraic content (a) at
sympy `Rational` exact precision via the standard 4x4 Euclidean Cl(4)
Dirac realization. It does NOT address the upstream Higgs family,
selector, 3+1 chirality operator, or weak-axis convention -- the audit
verdict identifies those as requiring separate retained dependencies.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's load-bearing class-(C)
algebraic content holds at exact precision. Does not modify the
parent's audit_status; that decision belongs to the audit lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Matrix, Rational, eye, zeros, simplify, I as sym_I, symbols
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


# Build 4x4 Euclidean Cl(4) Dirac matrices via Kronecker product.
sigma_x = Matrix([[0, 1], [1, 0]])
sigma_y = Matrix([[0, -sym_I], [sym_I, 0]])
sigma_z = Matrix([[1, 0], [0, -1]])
I2 = eye(2)


def kron(A, B):
    """Symbolic Kronecker product."""
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape
    result = sympy.Matrix.zeros(rows_A * rows_B, cols_A * cols_B)
    for i in range(rows_A):
        for j in range(cols_A):
            for k in range(rows_B):
                for l in range(cols_B):
                    result[i * rows_B + k, j * cols_B + l] = A[i, j] * B[k, l]
    return result


# Standard 4x4 Euclidean Cl(4) Dirac realization:
#   gamma_i = sigma_i (x) sigma_x  for i = 1, 2, 3
#   gamma_4 = I_2 (x) sigma_y
#   gamma_5 = gamma_1 gamma_2 gamma_3 gamma_4
gamma_1 = kron(sigma_x, sigma_x)
gamma_2 = kron(sigma_y, sigma_x)
gamma_3 = kron(sigma_z, sigma_x)
gamma_4 = kron(I2, sigma_y)
gamma_5 = simplify(gamma_1 * gamma_2 * gamma_3 * gamma_4)

# In the source note's notation, "Gamma_i" for i = 1, 2, 3 are the spatial
# Cl(4) generators; we identify them with our gamma_1, gamma_2, gamma_3.
Gamma = [gamma_1, gamma_2, gamma_3]


# ============================================================================
section("Audit companion for dm_neutrino_dirac_bridge_theorem_note_2026-04-15 (td=115)")
# Goal: exact symbolic verification of the algebraic content (a)
# (Hermiticity, involution, Clifford, anticommute with gamma_5, M(phi)^2,
# chiral off-diagonal) at sympy exact precision.
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: Gamma_i are Hermitian involutions on the 4x4 Cl(4) realization")
# ----------------------------------------------------------------------------
for i in range(3):
    check(f"Gamma_{i+1} = Gamma_{i+1}^dagger (Hermitian)",
          Gamma[i] == Gamma[i].H,
          detail=f"Hermiticity of gamma_{i+1}")
    check(f"Gamma_{i+1}^2 = I_4 (involution)",
          simplify(Gamma[i] * Gamma[i] - eye(4)) == zeros(4, 4),
          detail=f"gamma_{i+1}^2 = I")


# ----------------------------------------------------------------------------
section("Part 2: Cl(3) anticommutation {Gamma_i, Gamma_j} = 2 delta_{ij} I")
# ----------------------------------------------------------------------------
for i in range(3):
    for j in range(i, 3):
        anticomm = simplify(Gamma[i] * Gamma[j] + Gamma[j] * Gamma[i])
        expected = (2 * eye(4)) if i == j else zeros(4, 4)
        check(f"{{Gamma_{i+1}, Gamma_{j+1}}} = {2 if i == j else 0} I_4",
              anticomm == expected,
              detail=f"anticommutator at exact precision")


# ----------------------------------------------------------------------------
section("Part 3: gamma_5 properties on the 4x4 realization")
# ----------------------------------------------------------------------------
check("gamma_5 is Hermitian",
      gamma_5 == gamma_5.H)
check("gamma_5^2 = I_4 exact",
      simplify(gamma_5 * gamma_5 - eye(4)) == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 4: {Gamma_i, gamma_5} = 0 (Gamma_i is chiral off-diagonal)")
# ----------------------------------------------------------------------------
for i in range(3):
    anticomm_with_5 = simplify(Gamma[i] * gamma_5 + gamma_5 * Gamma[i])
    check(f"{{Gamma_{i+1}, gamma_5}} = 0 exact",
          anticomm_with_5 == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 5: M(phi) = sum phi_i Gamma_i Hermitian and M^2 = |phi|^2 I")
# ----------------------------------------------------------------------------
phi_1, phi_2, phi_3 = symbols('phi_1 phi_2 phi_3', real=True)
M_phi = phi_1 * Gamma[0] + phi_2 * Gamma[1] + phi_3 * Gamma[2]

check("M(phi) is Hermitian (all real phi)",
      M_phi == M_phi.H)

# M(phi)^2 = sum_{i,j} phi_i phi_j Gamma_i Gamma_j
# = sum_i phi_i^2 Gamma_i^2 + sum_{i<j} phi_i phi_j {Gamma_i, Gamma_j}
# = sum_i phi_i^2 I + 0  (by Clifford anticommute and Gamma_i^2 = I)
# = |phi|^2 I.
M_phi_squared = simplify(M_phi * M_phi)
expected_M_squared = (phi_1**2 + phi_2**2 + phi_3**2) * eye(4)
check("M(phi)^2 = |phi|^2 I_4 (Clifford involution-squared identity)",
      simplify(M_phi_squared - expected_M_squared) == zeros(4, 4),
      detail="symbolic in (phi_1, phi_2, phi_3)")


# ----------------------------------------------------------------------------
section("Part 6: P_L M(phi) P_L = P_R M(phi) P_R = 0 (chiral off-diagonal)")
# ----------------------------------------------------------------------------
P_L = (eye(4) + gamma_5) / 2
P_R = (eye(4) - gamma_5) / 2

check("P_L^2 = P_L (idempotent)",
      simplify(P_L * P_L - P_L) == zeros(4, 4))
check("P_R^2 = P_R (idempotent)",
      simplify(P_R * P_R - P_R) == zeros(4, 4))
check("P_L + P_R = I (resolution)",
      simplify(P_L + P_R - eye(4)) == zeros(4, 4))
check("P_L P_R = 0 (orthogonal)",
      simplify(P_L * P_R) == zeros(4, 4))

# {M(phi), gamma_5} = 0 implies M(phi) gamma_5 = -gamma_5 M(phi).
# Then P_L M(phi) P_L = (1/4) (1 + gamma_5) M (1 + gamma_5)
#   = (1/4) (M + M gamma_5 + gamma_5 M + gamma_5 M gamma_5)
#   = (1/4) (M - gamma_5 M + gamma_5 M - gamma_5^2 M)  (use M gamma_5 = -gamma_5 M)
# Actually let's just compute:
PLMPL = simplify(P_L * M_phi * P_L)
PRMPR = simplify(P_R * M_phi * P_R)
check("P_L M(phi) P_L = 0 exact (chiral off-diagonal LL block vanishes)",
      PLMPL == zeros(4, 4))
check("P_R M(phi) P_R = 0 exact (chiral off-diagonal RR block vanishes)",
      PRMPR == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 7: M(phi) at axis vector e_i equals Gamma_i")
# ----------------------------------------------------------------------------
# At phi = (1, 0, 0): M = Gamma_1. At phi = (0, 1, 0): M = Gamma_2. Etc.
for i in range(3):
    sub = {phi_1: 1 if i == 0 else 0, phi_2: 1 if i == 1 else 0, phi_3: 1 if i == 2 else 0}
    M_axis = simplify(M_phi.subs(sub))
    check(f"M at axis e_{i+1}: M = Gamma_{i+1}",
          simplify(M_axis - Gamma[i]) == zeros(4, 4))


# ----------------------------------------------------------------------------
section("Part 8: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('dm_neutrino_dirac_bridge_theorem_note_2026-04-15', {})
print(f"\n  dm_neutrino_dirac_bridge_theorem_note_2026-04-15 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-C load-bearing step (first-principles compute)",
      parent.get('load_bearing_step_class') == 'C',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(C) algebraic content on the
  4x4 Euclidean Cl(4) Dirac realization:

    - Gamma_i Hermitian involutions;
    - {Gamma_i, Gamma_j} = 2 delta_{ij} I (Clifford);
    - {Gamma_i, gamma_5} = 0 (chiral off-diagonal);
    - M(phi) = sum phi_i Gamma_i Hermitian, M^2 = |phi|^2 I;
    - P_L M P_L = P_R M P_R = 0;
    - M at axis e_i = Gamma_i.

  Audit-lane class for the parent's algebraic content:
    (C) — first-principles compute on the standard 4x4 Euclidean Cl(4)
    Dirac realization. No external observed/fitted/literature input.

  The companion does NOT address the parent's:
    - Higgs family upstream;
    - V_sel = 32 sum phi_i^2 phi_j^2 selector minima claim;
    - 3+1 chirality operator gamma_5 = G_0 G_1 G_2 G_3 framework
      derivation;
    - weak-axis branch convention.

  Those four items are the verdict-identified upstream gaps that require
  separate retained dependencies. This companion only certifies the
  algebraic content of the bridge theorem at exact precision.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
