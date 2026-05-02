#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_cascade_geometry_note_2026-04-14`
(claim_type=positive_theorem, load_bearing_step_class=A).

The parent's load-bearing step is the exact operator-algebra identity on
the C^8 taste cube. With Gamma_1 = sigma_x (x) I_2 (x) I_2 acting on the
basis {(s1, s2, s3) : si in {0, 1}}, the projectors

    P_O0  on  O_0 = {(0, 0, 0)},
    P_T1  on  T_1 = {(1, 0, 0), (0, 1, 0), (0, 0, 1)},
    P_T2  on  T_2 = {(1, 1, 0), (1, 0, 1), (0, 1, 1)},

satisfy:

  (a) P_T1 Gamma_1 P_T1 = 0        (Gamma_1 does not act inside T_1 at one hop)
  (b) P_O0 Gamma_1 P_T1 = [1 0 0]   (rank 1: only the (1,0,0) component goes to O_0)
  (c) P_T2 Gamma_1 P_T1 has rank 2  (the other two T_1 components go to T_2)

Second-order return operators on T_1:

  (d) via O_0:  P_T1 Gamma_1 P_O0 Gamma_1 P_T1  =  diag(1, 0, 0)
  (e) via T_2:  P_T1 Gamma_1 P_T2 Gamma_1 P_T1  =  diag(0, 1, 1)
  (f) total = I_3

The existing primary runner verifies these at numpy float precision; this
companion verifies them at sympy `Rational` exact precision.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's load-bearing class-(A)
operator algebra holds at exact precision. Does not modify the parent's
status; that decision belongs to the independent audit lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Matrix, Rational, eye, zeros, simplify, KroneckerProduct
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
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Audit companion for dm_neutrino_cascade_geometry_note_2026-04-14 (td=153)")
# Goal: exact symbolic verification of the operator-algebra identities
# (a)-(f) on the C^8 taste cube.
# ============================================================================

# Build Pauli matrices and Gamma_1 = sigma_x (x) I_2 (x) I_2 explicitly.
sigma_x = Matrix([[0, 1], [1, 0]])
I2 = eye(2)
# 8x8 representation of Gamma_1
Gamma_1 = sympy.Matrix.zeros(8, 8)
# Build via direct Kronecker product of 2x2 matrices
def kron(A, B):
    return sympy.Matrix([
        [A[i, j] * B[k, l] for j in range(A.cols) for l in range(B.cols)]
        for i in range(A.rows) for k in range(B.rows)
    ])

Gamma_1 = kron(kron(sigma_x, I2), I2)

# Basis labeling: state (s1, s2, s3) -> index s1*4 + s2*2 + s3
def state_index(s):
    return s[0] * 4 + s[1] * 2 + s[2]

O0_states = [(0, 0, 0)]
T1_states = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2_states = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]

# Build basis matrices b0, b1, b2: 8 x |sector| with columns = basis vectors of sector
def make_basis(states):
    cols = []
    for s in states:
        col = sympy.Matrix.zeros(8, 1)
        col[state_index(s), 0] = 1
        cols.append(col)
    return sympy.Matrix.hstack(*cols)

b0 = make_basis(O0_states)  # 8x1
b1 = make_basis(T1_states)  # 8x3
b2 = make_basis(T2_states)  # 8x3

# Projectors P_S = b_S @ b_S^T (real basis, no conjugation needed for these vectors)
P_O0 = b0 * b0.T  # 8x8
P_T1 = b1 * b1.T  # 8x8
P_T2 = b2 * b2.T  # 8x8


# ----------------------------------------------------------------------------
section("Part 1: Gamma_1 = sigma_x (x) I_2 (x) I_2 is an 8x8 permutation/involution")
# ----------------------------------------------------------------------------
Gamma_1_squared = Gamma_1 * Gamma_1
check("Gamma_1^2 = I_8 exact (sigma_x squared = I_2)",
      Gamma_1_squared == eye(8))


# ----------------------------------------------------------------------------
section("Part 2: P_T1 Gamma_1 P_T1 = 0 (one-hop closure off T_1)")
# ----------------------------------------------------------------------------
inside_T1 = P_T1 * Gamma_1 * P_T1
check("P_T1 Gamma_1 P_T1 = 0 (Gamma_1 does not act inside T_1 at one hop)",
      inside_T1 == sympy.Matrix.zeros(8, 8))


# ----------------------------------------------------------------------------
section("Part 3: P_O0 Gamma_1 P_T1 has rank 1 with explicit form [1, 0, 0]")
# ----------------------------------------------------------------------------
# In the T_1 basis (3-dim), P_O0 Gamma_1 P_T1 reduced by b0 and b1:
#   M_O0_T1 = b0^T Gamma_1 b1   (1x3)
M_O0_T1 = b0.T * Gamma_1 * b1
print(f"\n  M_O0_T1 (1x3 in T_1 basis) = {M_O0_T1}")
expected_O0_T1 = sympy.Matrix([[1, 0, 0]])
check("P_O0 Gamma_1 P_T1 reduced to T_1 basis equals [1, 0, 0]",
      M_O0_T1 == expected_O0_T1)
check("rank of M_O0_T1 = 1",
      M_O0_T1.rank() == 1)


# ----------------------------------------------------------------------------
section("Part 4: P_T2 Gamma_1 P_T1 has rank 2")
# ----------------------------------------------------------------------------
M_T2_T1 = b2.T * Gamma_1 * b1  # 3x3 in (T_2, T_1) basis
print(f"\n  M_T2_T1 (3x3) =\n{M_T2_T1}")
check("rank of P_T2 Gamma_1 P_T1 reduced = 2",
      M_T2_T1.rank() == 2)


# ----------------------------------------------------------------------------
section("Part 5: second-order return operator on T_1 via O_0 = diag(1, 0, 0)")
# ----------------------------------------------------------------------------
return_via_O0 = b1.T * Gamma_1 * P_O0 * Gamma_1 * b1  # 3x3 in T_1 basis
print(f"\n  return_via_O0 = {return_via_O0}")
expected_via_O0 = sympy.diag(1, 0, 0)
check("P_T1 Gamma_1 P_O0 Gamma_1 P_T1 = diag(1, 0, 0) in T_1 basis",
      return_via_O0 == expected_via_O0)


# ----------------------------------------------------------------------------
section("Part 6: second-order return operator on T_1 via T_2 = diag(0, 1, 1)")
# ----------------------------------------------------------------------------
return_via_T2 = b1.T * Gamma_1 * P_T2 * Gamma_1 * b1  # 3x3 in T_1 basis
print(f"\n  return_via_T2 = {return_via_T2}")
expected_via_T2 = sympy.diag(0, 1, 1)
check("P_T1 Gamma_1 P_T2 Gamma_1 P_T1 = diag(0, 1, 1) in T_1 basis",
      return_via_T2 == expected_via_T2)


# ----------------------------------------------------------------------------
section("Part 7: total second-order return on T_1 = I_3")
# ----------------------------------------------------------------------------
total_return = return_via_O0 + return_via_T2
check("via O_0 + via T_2 = I_3 (full return, completeness on T_1)",
      total_return == eye(3))


# ----------------------------------------------------------------------------
section("Part 8: 1+2 cascade decomposition signature")
# ----------------------------------------------------------------------------
# The decomposition diag(1,0,0) + diag(0,1,1) = I_3 cleanly splits into a
# 1-dim singlet channel (T_1 component (1,0,0) going to O_0) and a 2-dim
# T_2 channel (T_1 components (0,1,0) and (0,0,1) going into T_2).
#
# Verify that diag(1,0,0) is rank 1 and diag(0,1,1) is rank 2.
check("diag(1, 0, 0) is rank 1 (singlet channel)",
      sympy.diag(1, 0, 0).rank() == 1)
check("diag(0, 1, 1) is rank 2 (T_2 channel)",
      sympy.diag(0, 1, 1).rank() == 2)


# ----------------------------------------------------------------------------
section("Part 9: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('dm_neutrino_cascade_geometry_note_2026-04-14', {})
print(f"\n  dm_neutrino_cascade_geometry_note_2026-04-14 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (operator-algebra identity)",
      parent.get('load_bearing_step_class') == 'A',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(A) operator-algebra identities on
  the C^8 taste cube:

    P_T1 Gamma_1 P_T1 = 0;
    P_O0 Gamma_1 P_T1 = [1, 0, 0];
    P_T2 Gamma_1 P_T1 has rank 2;
    P_T1 Gamma_1 P_O0 Gamma_1 P_T1 = diag(1, 0, 0);
    P_T1 Gamma_1 P_T2 Gamma_1 P_T1 = diag(0, 1, 1);
    via O_0 + via T_2 = I_3 (1+2 cascade signature).

  Audit-lane class for the parent's load-bearing step:
    (A) — algebraic identity / linear algebra on the explicit C^8 Clifford
    realization. No external observed/fitted/literature input.

  This companion does NOT introduce a new claim row, a new source note,
  or any modification of the parent row's status. Independent audit
  remains responsible for any later parent-row disposition.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
